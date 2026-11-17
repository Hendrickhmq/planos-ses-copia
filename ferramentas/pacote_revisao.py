#!/usr/bin/env python3
"""
pacote_revisao.py - monta o pacote cego da revisao (Claude cego, ChatGPT, Gemini).

Uso:
    python3 pacote_revisao.py --documento planos/redacao_NN/plano.md --saida <pasta> \\
        [--titulo "objeto"] [--norma <nome>]... [--aprovados] [--fichas-de planos/redacao_NN] \\
        [--fonte <arquivo>]...

O metodo e metodo/revisao/cega.md. O pacote leva so o documento e as fontes oficiais:
nunca estado.yaml, licoes, pendencias, a conversa ou metodo/.

  --norma     o nome da pasta em biblioteca/extraidos_normas/ (texto.md e as tabelas) ou
              o nome de um arquivo em biblioteca/normas/ (PDF pelo pdftotext)
  --aprovados os cinco planos aprovados, de estudo/normalizados/pt_ses_0N/texto.md
  --fichas-de as fichas do SIGTAP em <plano>/dados/fontes/sigtap_*.md
  --fonte     qualquer outro arquivo de texto

CPF e CNS sao mascarados em todos os arquivos. Depois da mascara o pacote inteiro e
varrido de novo: se sobrar um, a montagem para com codigo 2 e o pacote nao serve.
"""
from __future__ import annotations
import argparse, csv, json, re, subprocess, sys, unicodedata
from datetime import date
from pathlib import Path

from comum import saida_utf8, sha256_arquivo, localizar
from conferir_coleta import CPF, CNS

RAIZ = Path(__file__).resolve().parent.parent
EXTRAIDOS = RAIZ / "biblioteca" / "extraidos_normas"
NORMAS = RAIZ / "biblioteca" / "normas"
NORMALIZADOS = RAIZ / "estudo" / "normalizados"


def slug(nome: str) -> str:
    s = unicodedata.normalize("NFKD", nome).encode("ascii", "ignore").decode()
    s = re.sub(r"[^A-Za-z0-9.-]+", "_", s).strip("_")
    return s


def mascarar(texto: str) -> tuple[str, int]:
    n = 0
    for pad, rotulo in ((CPF, "[CPF mascarado]"), (CNS, "[CNS mascarado]")):
        texto, k = pad.subn(rotulo, texto)
        n += k
    return texto, n


def texto_da_norma(nome: str) -> tuple[str, str]:
    """(texto, origem) da norma pelo nome da pasta extraida ou do arquivo em normas/."""
    pasta = EXTRAIDOS / nome
    texto = next((pasta / n for n in ("texto.md", "texto.txt") if (pasta / n).exists()), None)
    if texto:
        partes = [texto.read_text(encoding="utf-8")]
        for tab in sorted((pasta / "tabelas").glob("*.csv")) if (pasta / "tabelas").exists() else []:
            linhas = list(csv.reader(tab.open(encoding="utf-8", errors="replace")))
            corpo = "\n".join(" | ".join(c.strip() for c in l) for l in linhas)
            partes.append(f"\n\n## Tabela extraída: {tab.stem}\n\n{corpo}")
        return "".join(partes), f"biblioteca/extraidos_normas/{nome}/"
    candidatos = ([p for p in NORMAS.glob("*") if p.stem == nome or p.name == nome]
                  or [p for p in NORMAS.glob("*") if p.stem.startswith(nome)])
    if not candidatos:
        raise SystemExit(f"norma nao encontrada: {nome} (nem em extraidos_normas/ nem em normas/)")
    arq = candidatos[0]
    if arq.suffix.lower() == ".pdf":
        exe = localizar("pdftotext")
        if not exe:
            raise SystemExit("pdftotext nao encontrado")
        txt = subprocess.run([exe, str(arq), "-"], capture_output=True, text=True, check=True).stdout
        return txt, f"biblioteca/normas/{arq.name}"
    return arq.read_text(encoding="utf-8", errors="replace"), f"biblioteca/normas/{arq.name}"


def montar(args) -> int:
    saida = Path(args.saida)
    if saida.exists() and any(saida.iterdir()):
        raise SystemExit(f"a pasta de saida ja existe e nao esta vazia: {saida}")
    saida.mkdir(parents=True, exist_ok=True)
    itens = []  # (caminho no pacote, o que e, origem, mascarados)

    def gravar(rel: str, texto: str, oque: str, origem: str):
        texto, n = mascarar(texto)
        destino = saida / rel
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(texto, encoding="utf-8")
        itens.append((rel, oque, origem, n))

    doc = Path(args.documento)
    gravar("documento.md", doc.read_text(encoding="utf-8"), "o documento em análise",
           str(doc.resolve().relative_to(RAIZ)) if doc.resolve().is_relative_to(RAIZ) else str(doc))
    for nome in args.norma or []:
        txt, origem = texto_da_norma(nome)
        gravar(f"fontes/normas/{slug(nome)}.md", txt, f"norma: {nome}", origem)
    if args.aprovados:
        for pasta in sorted(NORMALIZADOS.glob("pt_ses_0*")):
            if (pasta / "texto.md").exists():
                gravar(f"fontes/aprovados/{pasta.name}.md", (pasta / "texto.md").read_text(encoding="utf-8"),
                       f"plano de trabalho aprovado pela SES-DF ({pasta.name})",
                       f"estudo/normalizados/{pasta.name}/texto.md")
    if args.fichas_de:
        for ficha in sorted((Path(args.fichas_de) / "dados" / "fontes").glob("sigtap_*.md")):
            gravar(f"fontes/fichas/{ficha.name}", ficha.read_text(encoding="utf-8"),
                   "ficha da Tabela do SUS (SIGTAP)", str(ficha))
    for f in args.fonte or []:
        p = Path(f)
        gravar(f"fontes/outras/{slug(p.stem)}{p.suffix or '.md'}", p.read_text(encoding="utf-8"),
               f"fonte: {p.name}", str(p))

    # a varredura de novo, no pacote inteiro
    sobra = []
    for arq in saida.rglob("*"):
        if arq.is_file():
            t = arq.read_text(encoding="utf-8", errors="replace")
            for nome, pad in (("CPF", CPF), ("CNS", CNS)):
                if pad.search(t):
                    sobra.append(f"{arq.relative_to(saida)}: {nome}")
    if sobra:
        print("DADO PESSOAL NO PACOTE, que nao pode sair:", *sobra, sep="\n  ")
        return 2

    manifesto = {"titulo": args.titulo or doc.stem, "data": date.today().isoformat(),
                 "arquivos": [{"arquivo": r, "o_que_e": o, "origem": g, "mascarados": n,
                               "sha256": sha256_arquivo(saida / r)} for r, o, g, n in itens]}
    (saida / "manifesto.json").write_text(json.dumps(manifesto, ensure_ascii=False, indent=2), encoding="utf-8")
    linhas = [f"# MANIFESTO — {manifesto['titulo']}", "",
              "Tudo o que esta pasta contém. O documento em análise é documento.md; o resto são as fontes.", "",
              "| arquivo | o que é |", "|---|---|"]
    linhas += [f"| {r} | {o} |" for r, o, _, _ in itens]
    (saida / "MANIFESTO.md").write_text("\n".join(linhas) + "\n", encoding="utf-8")
    mascarados = sum(n for *_, n in itens)
    print(f"pacote em {saida}: {len(itens)} arquivos, {mascarados} CPF/CNS mascarados, nenhum restante")
    return 0


def main():
    saida_utf8()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--documento", required=True)
    ap.add_argument("--saida", required=True)
    ap.add_argument("--titulo")
    ap.add_argument("--norma", action="append")
    ap.add_argument("--aprovados", action="store_true")
    ap.add_argument("--fichas-de")
    ap.add_argument("--fonte", action="append")
    sys.exit(montar(ap.parse_args()))


if __name__ == "__main__":
    main()
