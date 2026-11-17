#!/usr/bin/env python3
"""
extrair_planos.py - extracao de planos de trabalho em PDF com pdfplumber.

Uso:
    python extrair_planos.py planos_aprovados/ extraidos/

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

Dependencia:  pip install pdfplumber
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


def normalizar(texto: str) -> str:
    """Remove espacos a direita e colapsa sequencias de linhas em branco."""
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
    return " ".join(str(celula).split())


def extrair(pdf_path: Path, destino_raiz: Path) -> dict:
    doc_id, processo_sei = identificar(pdf_path.stem)
    destino = destino_raiz / doc_id
    dir_tabelas = destino / "tabelas"
    dir_tabelas.mkdir(parents=True, exist_ok=True)

    linhas_md = [f"# {doc_id}", f"Fonte: `{pdf_path.name}`"]
    tabelas_por_pagina = {}
    paginas_suspeitas = []
    total_chars = 0
    total_tabelas = 0

    with pdfplumber.open(pdf_path) as pdf:
        n_paginas = len(pdf.pages)

        for i, page in enumerate(pdf.pages, start=1):
            achadas = sorted(page.find_tables(), key=lambda t: t.bbox[1])
            bboxes = [t.bbox for t in achadas]

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
            n_tabelas_pagina = 0

            for j, tabela in enumerate(achadas, start=1):
                topo, base = tabela.bbox[1], tabela.bbox[3]
                acima = texto_da_faixa(cursor, topo)
                if acima:
                    partes.append(acima)
                    chars_pagina += len(acima)

                dados = tabela.extract()
                if dados:
                    tag = f"p{i:03d}_t{j:02d}"
                    with (dir_tabelas / f"{tag}.csv").open(
                            "w", newline="", encoding="utf-8") as f:
                        w = csv.writer(f)
                        for linha in dados:
                            w.writerow([limpar(c) for c in linha])
                    partes.append(
                        f"[[tabela: {tag}]]  <!-- {len(dados)} linhas x "
                        f"{max(len(l) for l in dados)} colunas -->")
                    n_tabelas_pagina += 1
                    total_tabelas += 1

                cursor = max(cursor, base)

            resto = texto_da_faixa(cursor, page.height)
            if resto:
                partes.append(resto)
                chars_pagina += len(resto)

            tabelas_por_pagina[i] = n_tabelas_pagina
            total_chars += chars_pagina
            if chars_pagina < MIN_CHARS_PAGINA and not n_tabelas_pagina:
                paginas_suspeitas.append(i)

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
        "paginas_sem_texto": paginas_suspeitas,
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
        sys.exit("Uso: python extrair_planos.py <pasta_pdfs> <pasta_saida>")

    origem = Path(sys.argv[1])
    destino = Path(sys.argv[2])
    if not origem.is_dir():
        sys.exit(f"Pasta nao encontrada: {origem}")
    destino.mkdir(parents=True, exist_ok=True)

    pdfs = sorted(origem.glob("*.pdf"))
    if not pdfs:
        sys.exit(f"Nenhum PDF em {origem}")

    print(f"{len(pdfs)} PDF(s) encontrado(s).\n")
    for pdf in pdfs:
        print(f"-> {pdf.name}")
        meta = extrair(pdf, destino)
        print(f"   id={meta['id']}  processo={meta['processo_sei'] or '?'}")
        print(f"   {meta['paginas']} paginas, {meta['chars_texto']} chars, "
              f"{meta['tabelas_total']} tabela(s)")
        if meta["paginas_sem_texto"]:
            print(f"   ATENCAO paginas sem texto (possivel digitalizacao): "
                  f"{meta['paginas_sem_texto']}")

    print("\nProximo passo: conferir as tabelas contra o PDF e marcar "
          "tabelas_conferidas: true no meta.yaml de cada documento.")


if __name__ == "__main__":
    main()
