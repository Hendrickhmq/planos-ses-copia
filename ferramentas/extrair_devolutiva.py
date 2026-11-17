#!/usr/bin/env python3
"""
extrair_devolutiva.py — le a devolutiva de um plano em .docx e diz o que falta tratar.

Uso:
    python3 extrair_devolutiva.py redacao_03/dados/devolutiva_20260905.docx
    python3 extrair_devolutiva.py <devolutiva.docx> --plano redacao_03/plano.md

POR QUE ISTO EXISTE

Em 05/09/2026 o professor devolveu o terceiro plano com 130 trechos marcados e
nenhum controle de revisoes. Ler isso na tela perde apontamento: marca em celula de
tabela some, cor diferente quer dizer coisa diferente, e o que ele DIGITA dentro do
documento nao aparece como marca nenhuma. O parser le o XML e nao perde.

E, depois de tratada a devolutiva, a pergunta "sobrou alguma coisa?" nao se responde
de memoria: com --plano, cada trecho marcado e procurado no plano atual, normalizando
acento, espaco e negrito.

O QUE A COR QUER DIZER — lido da devolutiva de 05/09/2026, nao e regra do Word:

    vermelho          sai do documento
    rosa em celula    o valor esta errado, corrija
    amarelo           reescreva
    verde             texto que ELE escreveu dentro do plano
    branco            ele passou por ali e nao marcou
    outra cor         pergunte a ele o que significa — nao adivinhe

E as edicoes digitadas nao tem cor: comparar o texto corrido da devolutiva com o do
plano enviado e a unica forma de acha-las.
"""
from __future__ import annotations
import argparse, difflib, re, unicodedata, zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

from comum import saida_utf8

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

# Onde um run pode morar dentro do paragrafo sem ser filho direto dele. O texto
# de link fica em w:hyperlink, e o que o revisor DIGITA com controle de
# alteracoes ligado fica em w:ins - justamente o que este script existe para
# achar. Lendo so os filhos diretos, os dois sumiam.
RECIPIENTES = {"hyperlink", "ins", "smartTag", "sdt", "sdtContent", "fldSimple",
               "customXml"}
CORES = {"red": "sai", "yellow": "reescreve", "green": "texto dele",
         "white": "passou e nao marcou", "#f4cccc": "valor errado"}


def texto_do_run(r):
    out = []
    for e in r:
        tag = e.tag.replace(W, "")
        if tag == "t":
            out.append(e.text or "")
        elif tag == "tab":
            out.append("\t")
        elif tag == "br":
            out.append("\n")
    return "".join(out)


def marcas_do_run(r):
    """cor de realce e cor de fundo do run, se houver"""
    rpr = r.find(W + "rPr")
    if rpr is None:
        return None
    h = rpr.find(W + "highlight")
    if h is not None and h.get(W + "val") != "none":
        return h.get(W + "val")
    s = rpr.find(W + "shd")
    if s is not None and (s.get(W + "fill") or "").lower() not in ("", "auto", "ffffff"):
        return "#" + s.get(W + "fill").lower()
    return None


def runs(no):
    """runs do paragrafo, em ordem, inclusive os que estao dentro de link,
    insercao controlada e campo. Nao desce em w:del (texto apagado) nem em
    paragrafo aninhado (caixa de texto), que o laco de paragrafos ja visita."""
    for filho in no:
        tag = filho.tag.replace(W, "")
        if tag == "r":
            yield filho
        elif tag in RECIPIENTES:
            yield from runs(filho)


def ler(caminho):
    with zipfile.ZipFile(caminho) as z:
        doc = ET.fromstring(z.read("word/document.xml"))
        comentarios = {}
        if "word/comments.xml" in z.namelist():
            for c in ET.fromstring(z.read("word/comments.xml")).iter(W + "comment"):
                comentarios[c.get(W + "id")] = {
                    "autor": c.get(W + "author") or "?",
                    "data": c.get(W + "date") or "",
                    "texto": "".join(t.text or "" for t in c.iter(W + "t")).strip()}
    return doc, comentarios


def paragrafos(doc):
    """(indice, estilo, texto puro, [(cor, trecho)], [ids de comentario])"""
    saida, abertos = [], set()
    for i, p in enumerate(doc.iter(W + "p"), 1):
        cids = []
        for no in p.iter():
            tag = no.tag.replace(W, "")
            if tag == "commentRangeStart":
                abertos.add(no.get(W + "id")); cids.append(no.get(W + "id"))
            elif tag in ("commentRangeEnd", "commentReference"):
                abertos.discard(no.get(W + "id"))
                if no.get(W + "id") not in cids:
                    cids.append(no.get(W + "id"))
        puro, grifos = [], []
        for r in runs(p):
            t = texto_do_run(r)
            if not t:
                continue
            puro.append(t)
            cor = marcas_do_run(r)
            if cor:
                if grifos and grifos[-1][0] == cor:
                    grifos[-1] = (cor, grifos[-1][1] + t)
                else:
                    grifos.append((cor, t))
        est = p.find(W + "pPr/" + W + "pStyle")
        saida.append((i, est.get(W + "val") if est is not None else "",
                      "".join(puro), grifos, cids, set(abertos)))
    return saida


def norm(t):
    t = unicodedata.normalize("NFKD", t or "")
    t = "".join(c for c in t if not unicodedata.combining(c))
    t = t.replace("“", '"').replace("”", '"').replace("’", "'")
    return re.sub(r"[\s*_]+", " ", t).strip().lower()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("devolutiva")
    ap.add_argument("--plano", help="plano.md atual; ativa a auditoria do que sobrou")
    ap.add_argument("--enviado", help=".docx que enviamos; acha o que ele DIGITOU")
    a = ap.parse_args()
    saida_utf8()

    doc, coms = ler(a.devolutiva)
    paras = paragrafos(doc)

    print(f"### COMENTARIOS: {len(coms)}")
    ordem = lambda x: (0, int(x[0])) if str(x[0]).isdigit() else (1, str(x[0]))
    for cid, c in sorted(coms.items(), key=ordem):
        print(f"[c{cid}] {c['autor']} | {c['data'][:10]} | {c['texto']}")

    por_cor = {}
    for _, _, _, grifos, _, _ in paras:
        for cor, _t in grifos:
            por_cor[cor] = por_cor.get(cor, 0) + 1
    print("\n### MARCAS POR COR")
    for cor, n in sorted(por_cor.items(), key=lambda x: -x[1]):
        print(f"  {cor:<10} {n:>4}   {CORES.get(cor, '*** COR DESCONHECIDA — pergunte ***')}")

    print("\n### PARAGRAFOS COM MARCA OU COMENTARIO")
    for i, est, puro, grifos, cids, abertos in paras:
        if not (grifos or cids or abertos):
            continue
        rot = []
        if grifos:
            rot.append("GRIFO:" + ",".join(sorted({c for c, _ in grifos})))
        if cids:
            rot.append("COM:" + ",".join("c" + c for c in cids))
        elif abertos:
            rot.append("DENTRO_DE:" + ",".join("c" + c for c in sorted(abertos)))
        print(f"\n--- p{i} [{est}] {' | '.join(rot)}")
        print(puro.strip() if puro.strip() else "(celula vazia)")
        for cor, t in grifos:
            if t.strip():
                print(f"    «{cor}» {t.strip()[:200]}")

    if a.enviado:
        d2, _ = ler(a.enviado)
        antes = [t for _, _, t, _, _, _ in paragrafos(d2)]
        depois = [t for _, _, t, _, _, _ in paras]
        print("\n### O QUE ELE DIGITOU DENTRO DO DOCUMENTO")
        achou = False
        for l in difflib.unified_diff(antes, depois, lineterm="", n=0):
            if l.startswith(("+", "-")) and not l.startswith(("+++", "---")):
                print("  " + l[:220]); achou = True
        if not achou:
            print("  nenhuma — so marcacao")

    if a.plano:
        alvo = norm(Path(a.plano).read_text(encoding="utf-8"))
        vivos, curtos = [], 0
        for i, _, _, grifos, _, _ in paras:
            for _cor, t in grifos:
                t = t.strip()
                if len(t) < 25:
                    curtos += 1
                    continue
                if norm(t)[:60] in alvo:
                    vivos.append((i, t))
        print(f"\n### AUDITORIA CONTRA {a.plano}")
        print(f"  celulas curtas, conferidas a olho: {curtos}")
        if not vivos:
            print("  nenhum trecho longo marcado continua no plano")
        else:
            print(f"  {len(vivos)} trecho(s) marcado(s) ainda presentes — conferir um a um:")
            for i, t in vivos:
                print(f"    p{i}: {t[:150]}")
        print("\n  ATENCAO: a auditoria so alcanca o que ele GRIFOU. O que ele digitou")
        print("  nao tem marca — use --enviado, e varra o texto em volta de cada edicao.")


if __name__ == "__main__":
    main()
