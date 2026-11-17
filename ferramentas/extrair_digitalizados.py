#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
extrair_digitalizados.py - extracao de planos em PDF DIGITALIZADO (imagem).

Uso:
    python extrair_digitalizados.py planos_aprovados/ extraidos_ocr/ --doc pt_ses_05
    python extrair_digitalizados.py planos_aprovados/ extraidos_ocr/ --doc pt_ses_05 --paginas 50,51,58

POR QUE ESTE SCRIPT EXISTE

O extrair_planos.py resolve PDF nativo: o pdfplumber le o texto e acha as
tabelas pelo desenho vetorial da grade. Em PDF digitalizado nao ha texto nem
vetor - ha pixels. O extrator cai no OCR de recuperacao, que chama
image_to_string na pagina inteira e devolve texto corrido.

Isso PERDE A GEOMETRIA, e sem geometria nao existe tabela. Foi o que aconteceu
com o pt_ses_05: 58 paginas de OCR, ZERO tabelas, e os totais da planilha
saindo embaralhados entre colunas ("Sub-tot | al Etapa 1.2").

A saida nao e mais DPI. Medido no pt_ses_05, pagina 50:

    dpi 150 -> confianca media 85,5
    dpi 300 -> confianca media 86,5
    dpi 400 -> confianca media 87,0

Subir resolucao rende quase nada porque o scan ja e limpo. O que falta e ler a
GRADE, que no digitalizado esta desenhada em pixel:

1. binariza a pagina;
2. acha as reguas VERTICAIS - colunas de pixel escuro cobrindo >=35% da altura;
3. acha as reguas HORIZONTAIS dentro da faixa das verticais, exigindo >=85% de
   travessia (o que descarta sublinhado de texto e borda de bloco);
4. para cada celula, confere se a regua vertical existe DENTRO daquela linha.
   Nao existindo, a celula esta MESCLADA e se junta a vizinha - e assim que
   "Sub-total Etapa 1.2" para de ser partido ao meio;
5. faz OCR de cada celula isoladamente, com --psm 6.

Celula lida sozinha nao embaralha com a coluna vizinha. Esse e o ganho inteiro.

O texto corrido sai com --psm 4 (coluna unica de tamanhos variaveis), que na
mesma pagina mede confianca 90,1 contra 86,5 do --psm 6 usado pelo extrator
antigo.

SAIDA

Mesma convencao do extrair_planos.py, para os dois lados serem comparaveis:

    <destino>/<ID>/texto.md          texto, com marcador [[tabela: pNNN_tNN]]
    <destino>/<ID>/tabelas/*.csv     uma CSV por tabela reconstruida
    <destino>/<ID>/meta.yaml         metadados + CONFIANCA DE OCR por pagina

O meta.yaml traz o que o do extrator nativo nao precisa ter: confianca media
por pagina e a lista das paginas abaixo do piso. Em documento digitalizado o
numero so vale acompanhado da confianca com que foi lido.

Com --paginas a saida e uma AMOSTRA e vai para <destino>/_amostras/<ID>/: um
texto.md com tres paginas nao pode ocupar o lugar da extracao inteira, que e a
conferida.

NAO ESCREVE EM extraidos/. Destino proprio, para a leitura antiga continuar de
pe e a comparacao ser possivel. Promover e decisao de quem confere - e implica
reconferir, porque o sha256 muda. O tratar_planos.py le daqui o documento que
existir aqui.

Os parametros de pixel (LIMIAR_ESCURO, MARGEM_ESQUERDA, ...) foram medidos no
pt_ses_05 a 300 dpi. Outro documento digitalizado pode pedir outros: a margem
esquerda, que descarta a moldura da pagina, e ajustavel por --margem-esquerda.
"""

import argparse
import csv
import re
import sys
import tempfile
from pathlib import Path

from comum import (escrever_texto, identificar, nfc, preparar_tesseract,
                   saida_utf8, sha256_arquivo)

try:
    import numpy as np
    import pdfplumber
    from PIL import Image
except ImportError as erro:
    sys.exit(f"Falta a dependencia ({erro.name}). Rode: pip install -r requirements.txt")

DPI = 300
LIMIAR_ESCURO = 160         # pixel abaixo disto e "tinta"
COBERTURA_VERTICAL = 0.35   # fracao da altura para uma coluna virar regua
COBERTURA_HORIZONTAL = 0.85 # fracao da largura da tabela para uma linha virar regua
MARGEM_ESQUERDA = 220       # px: descarta a moldura da pagina (--margem-esquerda)
SEPARADOR_PRESENTE = 0.50   # fracao da altura da linha com tinta na regua
MIN_COLUNAS = 3             # menos que isto nao e tabela
ALTURA_MINIMA_LINHA = 14    # px
CONF_PISO = 75.0            # abaixo disto a pagina entra na lista de revisao

# O pytesseract preparado por preparar_tesseract(); definido em main().
TESS = None


def agrupar(valores, tol=6):
    """Colapsa posicoes vizinhas: uma regua tem varios pixels de espessura."""
    grupos = []
    for v in valores:
        if not grupos or v - grupos[-1][-1] > tol:
            grupos.append([v])
        else:
            grupos[-1].append(v)
    return [int(sum(g) / len(g)) for g in grupos]


def reguas(dark, margem_esquerda=MARGEM_ESQUERDA):
    """Devolve (verticais, horizontais) em pixel.

    As somas por coluna e por linha sao feitas pelo numpy de uma vez: o laco
    Python coluna a coluna, sobre uma pagina de 2.500 x 3.500 pixels, era o
    grosso do tempo fora do OCR.
    """
    H, W = dark.shape
    por_coluna = dark.sum(axis=0)
    vx = np.flatnonzero(por_coluna > COBERTURA_VERTICAL * H).tolist()
    VX = [x for x in agrupar(vx) if x > margem_esquerda]
    if len(VX) < MIN_COLUNAS:
        return [], []
    x0, x1 = VX[0], VX[-1]
    largura = max(1, x1 - x0)
    por_linha = dark[:, x0:x1].sum(axis=1)
    hy = np.flatnonzero(por_linha > COBERTURA_HORIZONTAL * largura).tolist()
    return VX, agrupar(hy)


def mesclada(dark, x, y0, y1):
    """A regua vertical existe dentro desta linha? Nao existindo, as celulas
    a esquerda e a direita sao a mesma celula."""
    faixa = dark[y0:y1, max(0, x - 2):x + 3]
    if faixa.size == 0:
        return True
    return faixa.any(axis=1).mean() < SEPARADOR_PRESENTE


def ler(imagem_np, caixa, psm=6):
    y0, y1, x0, x1 = caixa
    if y1 - y0 < 8 or x1 - x0 < 8:
        return ""
    recorte = Image.fromarray(imagem_np[y0:y1, x0:x1])
    txt = TESS.image_to_string(recorte, lang="por", config="--psm %d" % psm)
    return re.sub(r"\s+", " ", txt).strip()


def confianca(imagem, psm=4):
    d = TESS.image_to_data(imagem, lang="por", config="--psm %d" % psm,
                           output_type=TESS.Output.DICT)
    # conf vem como int ou float conforme a versao do Tesseract; -1 e "sem texto"
    c = [float(v) for v in d["conf"] if float(v) > 0]
    return (sum(c) / len(c)) if c else 0.0


def tabela_da_pagina(cinza, dark, util=None, grade=None):
    """Reconstroi a tabela da pagina. Devolve lista de linhas (lista de celulas)."""
    VX, HY = grade if grade is not None else reguas(dark)
    if len(VX) < MIN_COLUNAS or len(HY) < 2:
        return None
    topo, base = util if util else (0, dark.shape[0] - 1)
    # a faixa util recorta o timbre; reguas fora dela viram os limites do corpo
    HY = [y for y in HY if topo <= y <= base]
    HY = ([topo] if not HY or HY[0] - topo > ALTURA_MINIMA_LINHA else []) + HY
    HY = HY + ([base] if base - HY[-1] > ALTURA_MINIMA_LINHA else [])
    if len(HY) < 2:
        return None
    linhas = []
    for r in range(len(HY) - 1):
        y0, y1 = max(HY[r] + 3, topo), min(HY[r + 1] - 3, base)
        if y1 - y0 < ALTURA_MINIMA_LINHA:
            continue
        celulas, c = [], 0
        while c < len(VX) - 1:
            fim = c + 1
            while fim < len(VX) - 1 and mesclada(dark, VX[fim], y0, y1):
                fim += 1
            celulas.append(ler(cinza, (y0, y1, VX[c] + 3, VX[fim] - 3)))
            # celula mesclada ocupa o lugar das que absorveu
            celulas.extend([""] * (fim - c - 1))
            c = fim
        if any(celulas):
            linhas.append(celulas)
    return linhas or None


RAZAO_CONSTANTE = 0.85   # tinta identica entre paginas = timbre, nao conteudo
TINTA_MINIMA = 20        # px por linha, para ignorar ruido de scanner


def faixa_util(paginas_bin):
    """Onde o CORPO da pagina comeca e termina, em pixel.

    Este documento imprime o timbre DENTRO da area da tabela. Na pagina 41 a
    primeira faixa de linha ia de y=61 a y=1831 e continha, na mesma tira, a
    data do cabecalho e o valor da rubrica - o OCR devolvia "de 2026 R$ 69."
    com o numero truncado.

    Tres tentativas de resolver isso PODANDO A LINHA ja falharam, e ficam
    registradas para nao voltarem:

    - casar o texto da faixa inteira: o OCR varia entre paginas, "3rasilia"
      nunca e igual a "Brasilia";
    - casar por token repetido: comeu a linha "3.1.1 Assessoria de Prestacao
      de Contas ... R$ 29.600,00";
    - exigir cauda numerica: apagou 1.1.1 e 1.2.4 INTEIRAS, dado junto, porque
      a data contamina a cauda da propria linha que se queria manter.

    Podar linha e errado de origem: o timbre e o dado dividem a mesma faixa.
    O que resolve e recortar por COORDENADA, antes do OCR.

    O timbre se identifica sozinho por ser CONSTANTE entre paginas: onde a
    tinta e a mesma em todas, e cabecalho ou rodape; onde varia, e conteudo.
    Mede-se a razao entre "tinta em todas as paginas" e "tinta em alguma".
    Perto de 1, faixa constante. Nao depende de saber o que o timbre diz.
    """
    P = np.stack(paginas_bin)
    H = P.shape[1]
    todos = P.all(0).sum(1).astype(float)
    algum = P.any(0).sum(1).astype(float)
    razao = np.divide(todos, np.maximum(algum, 1))
    constante = (razao > RAZAO_CONSTANTE) & (algum > TINTA_MINIMA)
    terco = H // 3
    topo = 0
    for y in range(terco):                 # ultima linha constante do topo
        if constante[y]:
            topo = y + 1
    base = H - 1
    for y in range(H - 1, H - terco, -1):  # primeira linha constante do rodape
        if constante[y]:
            base = y - 1
    return (topo, base) if base - topo > H // 4 else (0, H - 1)


TOLERANCIA_GRADE = 8   # px de folga entre as colunas de duas paginas


def mesma_grade(a, b):
    """Duas paginas pertencem a mesma tabela logica? A grade e a assinatura:
    mesmo numero de colunas, nas mesmas posicoes, a menos do tremor do scan."""
    return (len(a) == len(b)
            and all(abs(x - y) <= TOLERANCIA_GRADE for x, y in zip(a, b)))


def normalizar_codigo(celula):
    """Recupera o ponto perdido em codigo de item: "1.24" -> "1.2.4".

    So atua no caso PROVAVELMENTE UNIVOCO - exatamente tres digitos, que em
    planilha de meta/etapa/item so pode ser d.d.d. Quatro digitos ("2141", que
    deveria ser 2.1.1) ficam como estao: adivinhar onde entram os pontos seria
    inventar dado, e o codigo e rotulo, nao valor. O que nao normaliza sai
    listado no meta.yaml para conferencia - e a correcao, conferida no PDF,
    vai para registros/correcoes.csv.
    """
    bruto = (celula or "").strip()
    digitos = re.sub(r"\D", "", bruto)
    if re.fullmatch(r"\d[.\d]{1,3}", bruto) and len(digitos) == 3:
        return ".".join(digitos)
    return bruto


def codigo_suspeito(celula):
    """Celula que parece codigo de item mas nao virou d.d.d."""
    bruto = (celula or "").strip()
    return bool(re.fullmatch(r"\d[.\d]{2,5}", bruto)) and not re.fullmatch(r"\d\.\d\.\d", bruto)


def costurar(tabelas, grades):
    """Junta as paginas de UMA tabela partida pela paginacao.

    A planilha do ISHP e uma tabela so, quebrada em 13 folhas. Tratar cada
    folha como tabela independente devolve 12 CSVs que ninguem le em conjunto
    - e faz a linha que atravessa a quebra virar dois pedacos.

    Duas paginas seguidas com a MESMA GRADE sao a mesma tabela. Dentro dela,
    linha cuja primeira coluna vem vazia e CONTINUACAO da anterior: o numero
    do item foi impresso na folha em que a linha comecou. Essas se fundem
    celula a celula com a linha de cima.
    """
    blocos, atual = [], []
    for pag in sorted(tabelas):
        if atual and pag == atual[-1] + 1 and mesma_grade(grades[pag], grades[atual[-1]]):
            atual.append(pag)
        else:
            if atual:
                blocos.append(atual)
            atual = [pag]
    if atual:
        blocos.append(atual)

    saida = []
    for bloco in blocos:
        linhas = []
        for pag in bloco:
            for linha in tabelas[pag]:
                primeira = (linha[0] or "").strip()
                if not primeira and linhas:
                    # continuacao: concatena celula a celula na linha anterior
                    anterior = linhas[-1]
                    for k in range(min(len(anterior), len(linha))):
                        novo = (linha[k] or "").strip()
                        if novo:
                            anterior[k] = (anterior[k] + " " + novo).strip()
                else:
                    nova = list(linha)
                    nova[0] = normalizar_codigo(nova[0])
                    linhas.append(nova)
        if len(bloco) > 1:
            saida.append((bloco[0], bloco[-1], linhas))
    return saida


def escrever_csv(caminho, linhas):
    with open(caminho, "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(linhas)


def extrair(pdf_path, destino_raiz, paginas=None, margem_esquerda=MARGEM_ESQUERDA):
    doc_id, processo = identificar(pdf_path.stem)
    # Amostra (--paginas) nunca ocupa o lugar da extracao inteira.
    destino = (destino_raiz / "_amostras" / doc_id) if paginas else (destino_raiz / doc_id)
    dir_tabelas = destino / "tabelas"
    dir_tabelas.mkdir(parents=True, exist_ok=True)
    # CSV de rodada anterior no meio das novas seria lida como se fosse desta.
    for antiga in list(dir_tabelas.glob("p*_t*.csv")) + list(dir_tabelas.glob("planilha_*.csv")):
        antiga.unlink()

    nome_pdf = nfc(pdf_path.name)
    cabecalho = ["# %s\n" % doc_id,
                 "Fonte: `%s`  \nExtracao: extrair_digitalizados.py "
                 "(OCR por celula, %d dpi)\n" % (nome_pdf, DPI)]
    confs, tabelas, grades = {}, {}, {}
    por_pagina = {}

    with pdfplumber.open(pdf_path) as pdf, tempfile.TemporaryDirectory() as cache:
        total = len(pdf.pages)
        cache = Path(cache)

        # Primeira passada: renderiza cada pagina UMA vez, guarda a imagem em
        # disco (PNG, sem perda) e anota a grade. A segunda passada le do
        # disco - antes renderizava tudo de novo.
        #
        # A amostra do timbre so pode vir de paginas COM GRADE. Amostrar o
        # documento inteiro nao serve: as ultimas folhas sao um oficio de
        # resposta a diligencia, com outro timbre, e nada fica "constante".
        com_grade = []
        for k, page in enumerate(pdf.pages, 1):
            img = page.to_image(resolution=DPI).original.convert("L")
            img.save(cache / f"{k:03d}.png")
            b = np.array(img) < LIMIAR_ESCURO
            grade = reguas(b, margem_esquerda)
            grades[k] = grade
            if grade[0]:
                com_grade.append(k)
        util = None
        if len(com_grade) >= 3:
            passo = max(1, len(com_grade) // 8)
            amostra = com_grade[::passo][:8]
            util = faixa_util([np.array(Image.open(cache / f"{k:03d}.png")) < LIMIAR_ESCURO
                               for k in amostra])
        print("   %d pagina(s) com grade; faixa util y %d..%d"
              % (len(com_grade), util[0], util[1]) if util
              else "   faixa util nao detectada (%d paginas com grade)" % len(com_grade))

        for i in range(1, total + 1):
            if paginas and i not in paginas:
                continue
            img = Image.open(cache / f"{i:03d}.png")
            cinza = np.array(img)
            dark = cinza < LIMIAR_ESCURO
            conf = confianca(img)
            confs[i] = round(conf, 1)

            linhas = tabela_da_pagina(cinza, dark, util, grades[i])
            if linhas:
                tabelas[i] = linhas
            ty0, ty1 = util if util else (0, cinza.shape[0])
            por_pagina[i] = (conf, ler(cinza, (ty0, ty1, 0, cinza.shape[1]), psm=4))
            print("   pag %2d/%d  conf %.1f%s" % (i, total, conf,
                  "  grade %dx%d" % (len(linhas), max(len(l) for l in linhas))
                  if linhas else ""))

    grades = {p: grades[p][0] for p in tabelas}

    suspeitos = []
    for ini, fim, linhas in costurar(tabelas, grades):
        suspeitos += [l[0] for l in linhas if codigo_suspeito(l[0])]
        nome = "planilha_p%03d-p%03d.csv" % (ini, fim)
        escrever_csv(dir_tabelas / nome, linhas)
        print("   costurada: %s  (%d paginas -> %d linhas)"
              % (nome, fim - ini + 1, len(linhas)))

    # O cabecalho do documento entra como texto. A versao anterior tratava
    # toda parte como ("PAG" | "TXT", ...) e pegava parte[1] tambem das duas
    # linhas de cabecalho - o segundo CARACTERE de cada uma. O texto.md do
    # pt_ses_05 comecou assim com " " e "o" no lugar de "# pt_ses_05" e da
    # linha da fonte.
    saida = list(cabecalho)
    for i, (conf, texto) in sorted(por_pagina.items()):
        saida.append("\n<!-- pagina %d | confianca OCR %.1f -->\n" % (i, conf))
        if i in tabelas:
            linhas = tabelas[i]
            nome = "p%03d_t01.csv" % i
            escrever_csv(dir_tabelas / nome, linhas)
            saida.append("[[tabela: p%03d_t01]]  <!-- %d linhas x %d colunas -->\n"
                         % (i, len(linhas), max(len(l) for l in linhas)))
        saida.append(texto + "\n")

    escrever_texto(destino / "texto.md", "\n".join(saida))
    n_tab = len(tabelas)
    baixas = sorted([p for p, c in confs.items() if c < CONF_PISO])
    media = sum(confs.values()) / max(1, len(confs))
    meta = [
        'id: "%s"' % doc_id,
        'arquivo: "%s"' % nome_pdf,
        'processo_sei: "%s"' % processo,
        'sha256: "%s"' % sha256_arquivo(pdf_path),
        'extrator: "extrair_digitalizados.py"',
        'ocr_ferramenta: "%s"' % NOME_OCR,
        "paginas: %d" % len(confs),
        "dpi: %d" % DPI,
        "margem_esquerda_px: %d" % margem_esquerda,
        "tabelas_total: %d" % n_tab,
        "tabelas_por_pagina:",
    ] + ["  pagina_%d: 1" % p for p in sorted(tabelas)] + [
        "ocr_confianca_media: %.1f" % media,
        "ocr_confianca_piso: %.1f" % CONF_PISO,
        "ocr_paginas_abaixo_do_piso: [%s]" % ", ".join(str(p) for p in baixas),
        "codigos_de_item_a_conferir: [%s]" % ", ".join('"%s"' % s for s in suspeitos),
        "ocr_confianca_por_pagina:",
    ] + ["  pagina_%d: %.1f" % (p, c) for p, c in sorted(confs.items())]
    if paginas:
        meta.insert(0, "# AMOSTRA - so as paginas %s; a extracao inteira fica em %s/"
                    % (sorted(paginas), doc_id))
    escrever_texto(destino / "meta.yaml", "\n".join(meta) + "\n")
    return doc_id, n_tab, media, baixas, destino


NOME_OCR = ""


def main():
    global TESS, NOME_OCR
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("origem", type=Path)
    ap.add_argument("destino", type=Path)
    ap.add_argument("--doc", action="append", default=[])
    ap.add_argument("--paginas", default="",
                    help="so estas paginas (1,2,5); a saida vai para "
                         "<destino>/_amostras/<ID>/")
    ap.add_argument("--margem-esquerda", type=int, default=MARGEM_ESQUERDA,
                    help="px a 300 dpi descartados a esquerda (moldura da "
                         "pagina); padrao %d, medido no pt_ses_05" % MARGEM_ESQUERDA)
    a = ap.parse_args()
    saida_utf8()

    TESS, NOME_OCR = preparar_tesseract()
    if TESS is None:
        print("Tesseract com o idioma 'por' nao encontrado. Ver README, Instalacao.")
        return 1

    pags = {int(x) for x in a.paginas.split(",") if x.strip()} if a.paginas else None
    pedidos = {d.lower() for d in a.doc}
    pdfs = sorted(p for p in a.origem.glob("*.pdf")
                  if not pedidos or identificar(p.stem)[0] in pedidos)
    if not pdfs:
        print("nenhum PDF encontrado.")
        return 1
    for p in pdfs:
        print("-> %s" % p.name)
        doc_id, n, media, baixas, destino = extrair(p, a.destino, pags,
                                                    a.margem_esquerda)
        print("   %s: %d tabela(s), confianca media %.1f  -> %s"
              % (doc_id, n, media, destino))
        if baixas:
            print("   paginas abaixo do piso (%.0f): %s" % (CONF_PISO, baixas))
    return 0


if __name__ == "__main__":
    sys.exit(main())
