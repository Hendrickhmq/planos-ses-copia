#!/usr/bin/env python3
"""
extrair_planos.py - extracao de planos de trabalho em PDF com pdfplumber.

Uso:
    python extrair_planos.py planos_aprovados/ extraidos/
    python extrair_planos.py planos_aprovados/ extraidos/ --doc pt_ses_01

Para cada PDF gera:
    extraidos/<ID>/texto.md          texto corrido, sem o conteudo das tabelas
    extraidos/<ID>/tabelas/*.csv     uma CSV por tabela detectada
    extraidos/<ID>/meta.yaml         metadados e estatisticas da extracao

Convencao de nome:  pt_ses_<NN>_<processo>.pdf
Exemplo:            pt_ses_01_030989-2026.pdf

O <ID> e a parte pt_ses_NN. O numero do processo e lido do nome e gravado no
meta.yaml como metadado, nao entra no caminho das pastas. Nome fora do padrao
vira ID igual ao nome do arquivo, sem processo.

O texto e as tabelas sao extraidos na MESMA varredura, pagina a pagina. O texto
das tabelas e removido do texto corrido (senao viria embaralhado) e substituido
por um marcador [[tabela: pNNN_tNN]] na posicao onde a tabela estava.

Esta e a quarta geracao do script. As tres anteriores estao em `historico/`,
sem uso: ficam pelo rastro de como a leitura foi sendo corrigida. A extracao
atual de todos os quatro planos sai deste arquivo - inclusive a dos planos 02 e
03, que foram extraidos pela v3 e que esta versao reproduz byte a byte.

Mudancas em relacao a historico/extrair_planos_v3.py:

1. AJUSTES por (documento, pagina). Tabela sem borda, moldura de pagina lida
   como coluna e sombreado de linha lido como separador nao se resolvem com um
   ajuste global: o que conserta uma pagina estraga outra. Cada entrada de
   AJUSTES carrega opcionalmente um "recorte" (a regiao onde a tabela vive) e
   um dicionario "settings" repassado a find_tables. As paginas sem entrada
   seguem exatamente como no v3 - por isso os documentos nao reprocessados
   continuam validos.

2. Modo --doc: reprocessa so os ids indicados, para nao mexer no que ja esta
   conferido. Mesma opcao do conferir.py.

3. OCR de recuperacao so por pytesseract, com o caminho usual do Windows como
   alternativa quando o binario nao esta no PATH. O rapidocr saiu: perde
   acentuacao, e texto sem acento contamina as verificacoes de cobertura.

4. Descarte de moldura: grade de tabela sem texto em celula nenhuma nao e
   tabela. Em PDF digitalizado inteiro o find_tables acha o desenho da grade e
   devolve celulas vazias - o que gerava CSV vazia e, pior, bloqueava o OCR,
   cujo gatilho exige pagina sem texto E sem tabela. Nenhum dos planos 01 a 04
   tem tabela assim, entao a extracao dos quatro nao muda.

As duas heuristicas do v3 continuam valendo, sem alteracao: descarte de falsa
tabela (caixa de texto do Word com borda) e normalizacao de bullets da Area de
Uso Privado.

Dependencias: pip install -r requirements.txt
OCR opcional: binario tesseract com idioma 'por' (ver README, Instalacao)

Os arquivos saem em UTF-8 com LF em qualquer sistema, para que a mesma
extracao tenha os mesmos bytes no Mac e no Windows.
"""

import argparse
import csv
import sys
from datetime import datetime
from pathlib import Path

from comum import (escrever_texto, identificar, nfc, preparar_tesseract,
                   saida_utf8, sha256_arquivo, yaml_simples)

try:
    import pdfplumber
except ImportError:
    sys.exit("Falta a dependencia. Rode: pip install -r requirements.txt")

# Paginas com menos caracteres que isso sao tratadas como possivelmente
# digitalizadas (precisariam de OCR).
MIN_CHARS_PAGINA = 50

# Resolucao de renderizacao para OCR. 300 dpi e o ponto de equilibrio entre
# qualidade e tempo; abaixo de 200 a taxa de erro sobe muito.
DPI_OCR = 300

# Reclassificacao de falsa tabela. Celula de tabela de verdade e curta; bloco
# longo em tabela de uma ou duas colunas e paragrafo dentro de caixa com borda.
MAX_COLS_PROSA = 2
LIMIAR_PROSA = 200

# Bullets do Word em fonte Symbol/Wingdings, que caem na Area de Uso Privado.
# Escritos como escape de proposito: o caractere literal e invisivel no editor.
SUBSTITUICOES_PUA = {
    "\uf0b7": "•",   # Symbol, bullet redondo
    "\uf0d8": "•",   # Wingdings, bullet em ponta de seta
    "\uf0a7": "•",   # Wingdings, bullet quadrado
    "\uf0fc": "✓",   # Wingdings, marca de conferido
}


# ---------------------------------------------------------------- ajustes ----

AJUSTES = {}


def ajustar(doc, paginas, recorte=None, settings=None, nota=""):
    """Registra um ajuste de leitura de tabela para (doc, pagina)."""
    for pagina in paginas:
        AJUSTES[(doc, pagina)] = {"recorte": recorte,
                                  "settings": dict(settings or {}),
                                  "nota": nota}


# pt_ses_01, pagina 5: bloco de texto com uma tarja de fundo por linha. As
# tarjas sao retangulos preenchidos, viram bordas e o texto corrido da pagina
# (METAS, Distribuicao Regional dos Atendimentos, Observancia da Regulacao
# Assistencial) ia parar dentro de uma CSV de uma coluna. As celulas tem ~93
# caracteres, abaixo do LIMIAR_PROSA, entao a heuristica de prosa nao pega.
# lines_strict considera so linha de verdade, e nesta pagina nao ha nenhuma.
ajustar("pt_ses_01", [5],
        settings={"vertical_strategy": "lines_strict",
                  "horizontal_strategy": "lines_strict"},
        nota="tarja de fundo lida como tabela; so linha de verdade conta")

# pt_ses_01, paginas 34-54: planilha orcamentaria. Dois problemas na mesma
# regiao, e por isso o mesmo ajuste vale para o bloco inteiro:
#
#   - a moldura da pagina (retangulo em volta da area util, x 49,7 e 560,2)
#     entrava como coluna e produzia colunas vazias a esquerda e a direita;
#     o recorte a corta e deixa so as 8 colunas da planilha.
#   - o item que atravessa a virada de pagina nao tem borda superior: sem uma
#     horizontal no topo da area util nao se fecha celula nenhuma e a pagina
#     inteira saia sem CSV (p. 39 e 40) ou perdia a primeira linha. A linha
#     explicita em 113,75 fecha a celula do item continuado.
ajustar("pt_ses_01", range(34, 55),
        recorte=(55.4, 113.7, 545.1, 760.0),
        settings={"explicit_horizontal_lines": [113.75]},
        nota="recorte tira a moldura da pagina; linha explicita no topo fecha "
             "a celula do item que vira a pagina")

# pt_ses_04, paginas 21-32: cronograma de metas. Cada linha de texto tem um
# retangulo de sombreado atras, e a borda desses retangulos passa a menos de
# 3 pontos da coluna - dentro da tolerancia padrao de intersecao. O resultado
# era uma linha de CSV por linha de texto (47 linhas onde ha 5 metas). Baixar
# a tolerancia horizontal para 1 ponto mantem os separadores de verdade, que
# encostam na coluna, e descarta o sombreado.
#
# O mesmo ajuste NAO vale para as paginas 16-18, que tem sombreado parecido:
# la ele piora a leitura, fundindo a primeira e a terceira coluna. Por isso o
# ajuste e por pagina, e nao por documento.
ajustar("pt_ses_04", range(21, 33),
        settings={"intersection_x_tolerance": 1.0},
        nota="sombreado de linha lido como separador de linha")


def carregar_ocr():
    """Devolve (funcao_ocr, nome) ou (None, "") se o Tesseract nao estiver la.

    Sem OCR a pagina digitalizada fica vazia, o que e melhor que texto sem
    acento entrando no texto.md. O nome leva a versao do Tesseract e vai para
    o meta.yaml: versoes diferentes leem a mesma pagina de jeito diferente.
    """
    pytesseract, nome = preparar_tesseract()
    if pytesseract is None:
        return None, ""
    return (lambda img: pytesseract.image_to_string(img, lang="por"), nome)


def ocr_pagina(page, motor) -> str:
    """Renderiza a pagina e devolve o texto reconhecido."""
    imagem = page.to_image(resolution=DPI_OCR).original
    return normalizar(motor(imagem))


def fora_das_tabelas(obj, bboxes):
    """True se o objeto grafico esta fora de todas as areas de tabela."""
    cx = (obj["x0"] + obj["x1"]) / 2
    cy = (obj["top"] + obj["bottom"]) / 2
    for x0, top, x1, bottom in bboxes:
        if x0 <= cx <= x1 and top <= cy <= bottom:
            return False
    return True


def trocar_pua(texto: str) -> str:
    """Troca os bullets da Area de Uso Privado por caractere com glifo."""
    for origem, destino in SUBSTITUICOES_PUA.items():
        texto = texto.replace(origem, destino)
    return texto


def normalizar(texto: str) -> str:
    """Remove espacos a direita e colapsa sequencias de linhas em branco."""
    texto = trocar_pua(texto)
    saida, vazias = [], 0
    for linha in texto.splitlines():
        linha = linha.rstrip()
        if linha:
            vazias = 0
            saida.append(linha)
        else:
            vazias += 1
            if vazias == 1 and saida:
                saida.append("")
    while saida and saida[-1] == "":
        saida.pop()
    return "\n".join(saida)


def limpar(celula):
    if celula is None:
        return ""
    return trocar_pua(" ".join(str(celula).split()))


def e_prosa(dados) -> bool:
    """True se o que foi detectado como tabela e, na verdade, texto corrido.

    Caixa de texto com borda vira tabela de uma ou duas colunas com um
    paragrafo inteiro dentro de uma celula.
    """
    if not dados:
        return False
    if max(len(linha) for linha in dados) > MAX_COLS_PROSA:
        return False
    maior = max((len(limpar(c)) for linha in dados for c in linha), default=0)
    return maior > LIMIAR_PROSA


def e_moldura(dados) -> bool:
    """True se a "tabela" detectada nao tem texto em celula nenhuma.

    Pagina digitalizada nao tem objeto de texto, mas tem as linhas do desenho
    da tabela, e o find_tables acha a grade e devolve celulas todas vazias.
    Isso e uma moldura, nao uma tabela: nao rende CSV e ainda bloqueava o OCR
    de recuperacao, porque o gatilho exige pagina sem texto E sem tabela.
    Resultado, na pt_ses_05: 23 das 58 paginas sairam em branco, entre elas a
    planilha orcamentaria inteira.
    """
    return not any(limpar(c) for linha in dados for c in linha)


def procurar_tabelas(page, doc_id, numero):
    """Tabelas da pagina, com o ajuste registrado para (doc, pagina), se houver.

    O recorte vale so para a deteccao: as coordenadas devolvidas continuam as
    da pagina inteira, entao o recorte do texto corrido nao muda.
    """
    ajuste = AJUSTES.get((doc_id, numero))
    if not ajuste:
        return sorted(page.find_tables(), key=lambda t: t.bbox[1]), False
    area = page.crop(ajuste["recorte"]) if ajuste["recorte"] else page
    achadas = area.find_tables(table_settings=ajuste["settings"])
    return sorted(achadas, key=lambda t: t.bbox[1]), True


def texto_da_faixa(page, bboxes, topo, base):
    """Texto entre duas alturas da pagina, sem conteudo de tabela.

    Recebe a pagina e as caixas das tabelas por parametro. Morava dentro do laco
    de paginas lendo as duas do escopo de fora - funcionava porque era chamada
    na mesma volta, e deixava de funcionar no dia em que alguem a guardasse
    para depois.
    """
    if base - topo < 2:
        return ""
    faixa = page.crop((0, max(0, topo), page.width, min(page.height, base)))
    if bboxes:
        faixa = faixa.filter(lambda o: fora_das_tabelas(o, bboxes))
    bruto = faixa.extract_text(layout=True) or ""
    return normalizar(bruto)


def extrair(pdf_path: Path, destino_raiz: Path, motor_ocr=None,
            nome_ocr: str = "") -> dict:
    doc_id, processo_sei = identificar(pdf_path.stem)
    destino = destino_raiz / doc_id
    dir_tabelas = destino / "tabelas"
    dir_tabelas.mkdir(parents=True, exist_ok=True)

    # Reprocessar sem limpar deixaria CSV de rodada anterior no meio das novas:
    # o numero tNN muda quando a contagem de tabelas da pagina muda.
    for antiga in dir_tabelas.glob("p*_t*.csv"):
        antiga.unlink()

    nome_pdf = nfc(pdf_path.name)
    linhas_md = [f"# {doc_id}", f"Fonte: `{nome_pdf}`"]
    tabelas_por_pagina = {}
    prosa_por_pagina = {}
    moldura_por_pagina = {}
    paginas_suspeitas = []
    paginas_ocr = []
    paginas_ajustadas = []
    total_chars = 0
    total_tabelas = 0
    total_prosa = 0
    total_moldura = 0

    with pdfplumber.open(pdf_path) as pdf:
        n_paginas = len(pdf.pages)

        for i, page in enumerate(pdf.pages, start=1):
            candidatas, ajustada = procurar_tabelas(page, doc_id, i)
            if ajustada:
                paginas_ajustadas.append(i)

            # Classifica antes de recortar: so tabela de verdade e removida do
            # texto corrido. O que for prosa fica onde esta.
            reais = []
            n_prosa_pagina = 0
            n_moldura_pagina = 0
            for candidata in candidatas:
                dados = candidata.extract()
                if not dados:
                    continue
                if e_moldura(dados):
                    n_moldura_pagina += 1
                    continue
                if e_prosa(dados):
                    n_prosa_pagina += 1
                    continue
                reais.append((candidata, dados))

            bboxes = [t.bbox for t, _ in reais]

            partes = []
            chars_pagina = 0
            cursor = 0.0

            for j, (tabela, dados) in enumerate(reais, start=1):
                topo, base = tabela.bbox[1], tabela.bbox[3]
                acima = texto_da_faixa(page, bboxes, cursor, topo)
                if acima:
                    partes.append(acima)
                    chars_pagina += len(acima)

                tag = f"p{i:03d}_t{j:02d}"
                with (dir_tabelas / f"{tag}.csv").open(
                        "w", newline="", encoding="utf-8") as f:
                    w = csv.writer(f)
                    for linha in dados:
                        w.writerow([limpar(c) for c in linha])
                partes.append(
                    f"[[tabela: {tag}]]  <!-- {len(dados)} linhas x "
                    f"{max(len(l) for l in dados)} colunas -->")
                total_tabelas += 1

                cursor = max(cursor, base)

            resto = texto_da_faixa(page, bboxes, cursor, page.height)
            if resto:
                partes.append(resto)
                chars_pagina += len(resto)

            tabelas_por_pagina[i] = len(reais)
            prosa_por_pagina[i] = n_prosa_pagina
            total_prosa += n_prosa_pagina
            moldura_por_pagina[i] = n_moldura_pagina
            total_moldura += n_moldura_pagina
            total_chars += chars_pagina

            # Camada de recuperacao: so entra quando a pagina nao rendeu nada
            # nem por texto nem por tabela. Nunca sobrepoe extracao nativa.
            if chars_pagina < MIN_CHARS_PAGINA and not reais:
                paginas_suspeitas.append(i)
                if motor_ocr is not None:
                    reconhecido = ocr_pagina(page, motor_ocr)
                    if reconhecido:
                        partes.append(
                            f"<!-- ocr pagina {i} ({nome_ocr}) - REVISAR -->")
                        partes.append(reconhecido)
                        chars_pagina += len(reconhecido)
                        total_chars += len(reconhecido)
                        paginas_ocr.append(i)

            linhas_md.append(f"<!-- pagina {i} -->")
            linhas_md.extend(partes)

    escrever_texto(destino / "texto.md", "\n\n".join(linhas_md) + "\n")

    meta = {
        "id": doc_id,
        "arquivo": nome_pdf,
        "processo_sei": processo_sei,
        "sha256": sha256_arquivo(pdf_path),
        "paginas": n_paginas,
        "chars_texto": total_chars,
        "tabelas_total": total_tabelas,
        "tabelas_por_pagina": {k: v for k, v in tabelas_por_pagina.items() if v},
        "prosa_reclassificada_total": total_prosa,
        "prosa_reclassificada_por_pagina": {k: v for k, v in prosa_por_pagina.items() if v},
        "molduras_descartadas_total": total_moldura,
        "molduras_descartadas_por_pagina": {k: v for k, v in moldura_por_pagina.items() if v},
        "paginas_ajustadas": paginas_ajustadas,
        "paginas_sem_texto": paginas_suspeitas,
        "paginas_ocr": paginas_ocr,
        "ocr_ferramenta": nome_ocr,
        "ferramenta": f"pdfplumber {pdfplumber.__version__}",
        "data_extracao": datetime.now().isoformat(timespec="seconds"),
    }
    # `tabelas_conferidas`, `ocr_revisado` e `observacoes` moraram aqui ate a
    # quarta geracao e sairam: nao sao saida do extrator, sao julgamento de
    # quem leu. Este script monta o meta.yaml do zero e escreve por cima, entao
    # reprocessar um documento com --doc apagava a marcacao de conferencia sem
    # avisar - exatamente o campo que existe para voce nao ter que lembrar.
    # O registro agora e registros/conferencia.csv, ancorado no hash do
    # conteudo conferido: ver conferencia.py.

    escrever_texto(destino / "meta.yaml", yaml_simples(meta))

    return meta


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("planos", help="pasta com os PDFs")
    ap.add_argument("extraidos", help="pasta de saida")
    ap.add_argument("--doc", action="append",
                    help="so este id (pode repetir); padrao: todos")
    args = ap.parse_args()

    saida_utf8()

    origem = Path(args.planos)
    destino = Path(args.extraidos)
    if not origem.is_dir():
        sys.exit(f"Pasta nao encontrada: {origem}")
    destino.mkdir(parents=True, exist_ok=True)

    pdfs = sorted(origem.glob("*.pdf"))
    if not pdfs:
        sys.exit(f"Nenhum PDF em {origem}")

    if args.doc:
        pedidos = {d.lower() for d in args.doc}
        # o id de plano vem em minusculas; o de norma guarda a caixa do nome do arquivo
        pdfs = [p for p in pdfs if identificar(p.stem)[0].lower() in pedidos]
        faltando = pedidos - {identificar(p.stem)[0].lower() for p in pdfs}
        if faltando:
            sys.exit(f"PDF nao encontrado para: {', '.join(sorted(faltando))}")

    motor_ocr, nome_ocr = carregar_ocr()
    print(f"{len(pdfs)} PDF(s) a processar.")
    print(f"OCR de recuperacao: {nome_ocr or 'INDISPONIVEL (paginas sem texto ficarao vazias)'}\n")
    for pdf in pdfs:
        print(f"-> {pdf.name}")
        meta = extrair(pdf, destino, motor_ocr, nome_ocr)
        print(f"   id={meta['id']}  processo={meta['processo_sei'] or '?'}")
        print(f"   {meta['paginas']} paginas, {meta['chars_texto']} chars, "
              f"{meta['tabelas_total']} tabela(s)")
        if meta["paginas_ajustadas"]:
            print(f"   ajuste de leitura aplicado nas paginas "
                  f"{meta['paginas_ajustadas']}")
        if meta["prosa_reclassificada_total"]:
            print(f"   {meta['prosa_reclassificada_total']} falsa(s) tabela(s) "
                  f"devolvida(s) ao texto: paginas "
                  f"{sorted(meta['prosa_reclassificada_por_pagina'])}")
        if meta["paginas_ocr"]:
            print(f"   OCR aplicado nas paginas {meta['paginas_ocr']} - conferir")
        elif meta["paginas_sem_texto"]:
            print(f"   ATENCAO paginas sem texto e sem OCR: "
                  f"{meta['paginas_sem_texto']}")

    print("\nProximo passo: conferir as tabelas contra o PDF e registrar em "
          "registros/conferencia.csv:")
    print("   python conferencia.py extraidos/ --marcar <id> --por <suas iniciais>")


if __name__ == "__main__":
    main()
