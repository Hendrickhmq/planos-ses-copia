#!/usr/bin/env python3
"""
extrair_planos_v3.py - extracao de planos de trabalho em PDF com pdfplumber.

Uso:
    python extrair_planos_v3.py planos_aprovados/ extraidos/

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

Mudancas em relacao ao v2:

1. Descarte de falsa tabela. Caixa de texto do Word com borda tem retangulo
   vetorial e era detectada como tabela: o texto corrido da pagina ia parar
   dentro de uma celula de CSV e sumia do texto.md. Agora uma tabela com no
   maximo MAX_COLS_PROSA colunas cuja maior celula passa de LIMIAR_PROSA
   caracteres e reclassificada como prosa - nao gera CSV e o texto volta para
   o texto.md, na posicao original.

   Efeito colateral: a numeracao tNN conta so as tabelas reais, entao os nomes
   das CSVs podem diferir dos gerados pelo v2 nas paginas que tinham prosa.

2. Normalizacao de bullets da Area de Uso Privado. Lista feita no Word com
   fonte Symbol ou Wingdings sai como U+F0B7 / U+F0D8 / U+F0A7, que nao tem
   glifo fora daquelas fontes e aparecem como quadrado vazio - parece erro de
   acentuacao e nao e. Sao mapeados para bullet normal, no texto e nas celulas.

Dependencia:  pip install pdfplumber
OCR opcional: pip install pytesseract  (+ binario tesseract com idioma 'por')
              ou  pip install rapidocr-onnxruntime
"""

import csv
import hashlib
import re
import sys
from datetime import datetime
from pathlib import Path

try:
    import pdfplumber
except ImportError:
    sys.exit("Falta a dependencia. Rode: pip install pdfplumber")

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


def carregar_ocr():
    """Devolve (funcao_ocr, nome) ou (None, "") se nada estiver instalado.

    Prioridade: pytesseract com pacote 'por' (melhor acentuacao) e, na falta
    dele, rapidocr-onnxruntime (instalavel so por pip, sem binario externo).
    """
    try:
        import pytesseract
        if "por" in pytesseract.get_languages():
            return (lambda img: pytesseract.image_to_string(img, lang="por"),
                    "pytesseract/por")
    except Exception:
        pass
    try:
        from rapidocr_onnxruntime import RapidOCR
        motor = RapidOCR()

        def _rapid(img):
            import numpy as np
            res, _ = motor(np.array(img.convert("RGB")))
            return "\n".join(bloco[1] for bloco in res) if res else ""

        return _rapid, "rapidocr-onnxruntime"
    except Exception:
        pass
    return None, ""


def ocr_pagina(page, motor) -> str:
    """Renderiza a pagina e devolve o texto reconhecido."""
    imagem = page.to_image(resolution=DPI_OCR).original
    return normalizar(motor(imagem))


PADRAO_NOME = re.compile(r"^(pt_ses_\d+)\s*[-_ ]+\s*(.+)$", re.IGNORECASE)


def identificar(stem: str):
    """Separa o id do numero do processo a partir do nome do arquivo."""
    m = PADRAO_NOME.match(stem.strip())
    if m:
        return m.group(1).lower(), m.group(2).strip()
    return stem.strip(), ""


def sha256(caminho: Path) -> str:
    h = hashlib.sha256()
    with caminho.open("rb") as f:
        for bloco in iter(lambda: f.read(1 << 16), b""):
            h.update(bloco)
    return h.hexdigest()


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


def extrair(pdf_path: Path, destino_raiz: Path, motor_ocr=None,
            nome_ocr: str = "") -> dict:
    doc_id, processo_sei = identificar(pdf_path.stem)
    destino = destino_raiz / doc_id
    dir_tabelas = destino / "tabelas"
    dir_tabelas.mkdir(parents=True, exist_ok=True)

    linhas_md = [f"# {doc_id}", f"Fonte: `{pdf_path.name}`"]
    tabelas_por_pagina = {}
    prosa_por_pagina = {}
    paginas_suspeitas = []
    paginas_ocr = []
    total_chars = 0
    total_tabelas = 0
    total_prosa = 0

    with pdfplumber.open(pdf_path) as pdf:
        n_paginas = len(pdf.pages)

        for i, page in enumerate(pdf.pages, start=1):
            # Classifica antes de recortar: so tabela de verdade e removida do
            # texto corrido. O que for prosa fica onde esta.
            reais = []
            n_prosa_pagina = 0
            for candidata in sorted(page.find_tables(), key=lambda t: t.bbox[1]):
                dados = candidata.extract()
                if not dados:
                    continue
                if e_prosa(dados):
                    n_prosa_pagina += 1
                    continue
                reais.append((candidata, dados))

            bboxes = [t.bbox for t, _ in reais]

            def texto_da_faixa(topo, base):
                """Texto entre duas alturas da pagina, sem conteudo de tabela."""
                if base - topo < 2:
                    return ""
                faixa = page.crop((0, max(0, topo), page.width,
                                   min(page.height, base)))
                if bboxes:
                    faixa = faixa.filter(lambda o: fora_das_tabelas(o, bboxes))
                bruto = faixa.extract_text(layout=True) or ""
                return normalizar(bruto)

            partes = []
            chars_pagina = 0
            cursor = 0.0

            for j, (tabela, dados) in enumerate(reais, start=1):
                topo, base = tabela.bbox[1], tabela.bbox[3]
                acima = texto_da_faixa(cursor, topo)
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

            resto = texto_da_faixa(cursor, page.height)
            if resto:
                partes.append(resto)
                chars_pagina += len(resto)

            tabelas_por_pagina[i] = len(reais)
            prosa_por_pagina[i] = n_prosa_pagina
            total_prosa += n_prosa_pagina
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

    (destino / "texto.md").write_text("\n\n".join(linhas_md) + "\n", encoding="utf-8")

    meta = {
        "id": doc_id,
        "arquivo": pdf_path.name,
        "processo_sei": processo_sei,
        "sha256": sha256(pdf_path),
        "paginas": n_paginas,
        "chars_texto": total_chars,
        "tabelas_total": total_tabelas,
        "tabelas_por_pagina": {k: v for k, v in tabelas_por_pagina.items() if v},
        "prosa_reclassificada_total": total_prosa,
        "prosa_reclassificada_por_pagina": {k: v for k, v in prosa_por_pagina.items() if v},
        "paginas_sem_texto": paginas_suspeitas,
        "paginas_ocr": paginas_ocr,
        "ocr_ferramenta": nome_ocr,
        "ocr_revisado": False,
        "ferramenta": f"pdfplumber {pdfplumber.__version__}",
        "data_extracao": datetime.now().isoformat(timespec="seconds"),
        "tabelas_conferidas": False,
        "observacoes": "",
    }

    linhas_yaml = []
    for chave, valor in meta.items():
        if isinstance(valor, dict):
            linhas_yaml.append(f"{chave}:")
            for k, v in valor.items():
                linhas_yaml.append(f"  pagina_{k}: {v}")
        elif isinstance(valor, list):
            linhas_yaml.append(f"{chave}: [{', '.join(str(v) for v in valor)}]")
        elif isinstance(valor, bool):
            linhas_yaml.append(f"{chave}: {str(valor).lower()}")
        elif isinstance(valor, str):
            linhas_yaml.append(f'{chave}: "{valor}"')
        else:
            linhas_yaml.append(f"{chave}: {valor}")
    (destino / "meta.yaml").write_text("\n".join(linhas_yaml) + "\n", encoding="utf-8")

    return meta


def main():
    if len(sys.argv) != 3:
        sys.exit("Uso: python extrair_planos_v3.py <pasta_pdfs> <pasta_saida>")

    origem = Path(sys.argv[1])
    destino = Path(sys.argv[2])
    if not origem.is_dir():
        sys.exit(f"Pasta nao encontrada: {origem}")
    destino.mkdir(parents=True, exist_ok=True)

    pdfs = sorted(origem.glob("*.pdf"))
    if not pdfs:
        sys.exit(f"Nenhum PDF em {origem}")

    motor_ocr, nome_ocr = carregar_ocr()
    print(f"{len(pdfs)} PDF(s) encontrado(s).")
    print(f"OCR de recuperacao: {nome_ocr or 'INDISPONIVEL (paginas sem texto ficarao vazias)'}\n")
    for pdf in pdfs:
        print(f"-> {pdf.name}")
        meta = extrair(pdf, destino, motor_ocr, nome_ocr)
        print(f"   id={meta['id']}  processo={meta['processo_sei'] or '?'}")
        print(f"   {meta['paginas']} paginas, {meta['chars_texto']} chars, "
              f"{meta['tabelas_total']} tabela(s)")
        if meta["prosa_reclassificada_total"]:
            print(f"   {meta['prosa_reclassificada_total']} falsa(s) tabela(s) "
                  f"devolvida(s) ao texto: paginas "
                  f"{sorted(meta['prosa_reclassificada_por_pagina'])}")
        if meta["paginas_ocr"]:
            print(f"   OCR aplicado nas paginas {meta['paginas_ocr']} - conferir")
        elif meta["paginas_sem_texto"]:
            print(f"   ATENCAO paginas sem texto e sem OCR: "
                  f"{meta['paginas_sem_texto']}")

    print("\nProximo passo: conferir as tabelas contra o PDF e marcar "
          "tabelas_conferidas: true no meta.yaml de cada documento.")


if __name__ == "__main__":
    main()
