#!/usr/bin/env python3
"""
conferir_revisao.py - confere por maquina o que o revisor externo devolveu.

Uso:
    python3 conferir_revisao.py <pacote> <achados.json>
    python3 conferir_revisao.py <pacote> <achados.json> --resposta <resposta.json>
    python3 conferir_revisao.py <pacote> <achados.json> --veredito <veredito.json>

O metodo e metodo/revisao/cega.md. A conferencia nao julga o merito: diz se o que
foi citado existe.

  ACHADOS   cada trecho_documento existe literalmente em documento.md; quando ha fonte,
            o arquivo existe no pacote e o trecho_fonte existe nele. Sem o arquivo, o
            trecho_fonte se procura em todo o pacote, e o arquivo achado vale. O resultado vai para
            o campo "citacao" de cada achado, gravado de volta no mesmo arquivo.
  RESPOSTA  todo achado tem resposta; aceito e aceito_em_parte dizem a secao alterada e a
            fonte; contestado traz o trecho literal da fonte, que tem de existir;
            decisao_do_usuario traz a nota.
  VEREDITO  todo achado em discussao tem veredito.

"Literal" tolera o que nao muda o texto: maiusculas, aspas e travessoes tipograficos,
negrito e italico do Markdown, barras de tabela, espacos e quebras de linha, e as marcas
de citacao do Gemini ([1], [2, 3]). Reticencias separam pedacos, que tem de aparecer na
ordem. O que nao confere literal ainda pode conferir "aproximado": a mesma sequencia de
palavras, com 85% de semelhanca ou mais (a tabela que o revisor achatou com dois-pontos e
virgulas). A triagem le o aproximado com mais cuidado. Codigo 1 se a resposta ou o
veredito tiverem falha.
"""
from __future__ import annotations
import argparse, json, re, sys, unicodedata
from difflib import SequenceMatcher
from pathlib import Path

from comum import saida_utf8

RAIZ = Path(__file__).resolve().parent.parent
TROCAS = {"“": '"', "”": '"', "„": '"', "‘": "'", "’": "'", "–": "-", "—": "-", "−": "-",
          " ": " ", "º": "o", "°": "o", "ª": "a"}
MINIMO = 8  # pedaco menor que isto nao prova nada


def normalizar(t: str) -> str:
    t = unicodedata.normalize("NFC", t or "")
    for a, b in TROCAS.items():
        t = t.replace(a, b)
    t = re.sub(r"\[\d+(?:\s*[,-]\s*\d+)*\]", " ", t)       # marcas de citacao
    t = re.sub(r"[*_`#|>]", " ", t)                         # Markdown e tabela
    t = re.sub(r"\\(.)", r"\1", t)                          # escapes do Markdown
    t = re.sub(r"\s+", " ", t).strip().lower()
    return t.strip(' "\'')


def existe(trecho: str, texto: str) -> bool:
    if not trecho or not trecho.strip():
        return False
    alvo = normalizar(texto)
    pedacos = [normalizar(p) for p in re.split(r"\.\.\.|…|\[\.\.\.\]", trecho)]
    pedacos = [p for p in pedacos if p]
    if not pedacos or all(len(p) < MINIMO for p in pedacos):
        return False
    pos = 0
    for p in pedacos:
        if len(p) < MINIMO:
            continue
        i = alvo.find(p, pos)
        if i < 0:
            return False
        pos = i + len(p)
    return True


LIMIAR = 0.85  # semelhanca minima do trecho aproximado


def aproximado(trecho: str, texto: str, limiar: float = LIMIAR) -> bool:
    """O trecho existe com pequenas diferencas de pontuacao ou de tabela achatada? Compara
    por palavras, numa janela do tamanho do trecho, ancorada nas palavras mais raras dele.
    Paráfrase longa e texto inventado ficam abaixo do limiar."""
    q = re.findall(r"\w+", normalizar(trecho))
    if len(q) < 5:
        return False
    alvo = re.findall(r"\w+", normalizar(texto))
    pos = {}
    for i, w in enumerate(alvo):
        pos.setdefault(w, []).append(i)
    ancoras = sorted(set(q), key=lambda w: (len(pos.get(w, [])) or 10**9, -len(w)))[:3]
    n = len(q)
    vistos = set()
    for w in ancoras:
        k = q.index(w)
        for i in pos.get(w, [])[:200]:
            ini = max(0, i - k - 3)
            if ini in vistos:
                continue
            vistos.add(ini)
            janela = alvo[ini:ini + n + 6]
            if SequenceMatcher(None, q, janela, autojunk=False).ratio() * (len(q) + len(janela)) / (2 * len(q)) >= limiar:
                return True
    return False


def ler_arquivo(pacote: Path, rel: str | None):
    if not rel:
        return None
    rel = rel.strip().lstrip("./")
    for base in (pacote, RAIZ):
        p = (base / rel)
        if p.is_file():
            return p.read_text(encoding="utf-8", errors="replace")
    # o Gemini cita pelo titulo da fonte; o revisar_gemini.py ja traduz para o arquivo
    return None


def localizar_fonte(pacote: Path, trecho_fonte: str, trecho_documento: str = "") -> str | None:
    """O arquivo do pacote onde o trecho_fonte esta, literal. Serve quando o revisor nao
    disse a fonte de um jeito que se possa ler (o Google troca "nome.md" por "[suspicious
    link removed]" e, no formato rigido, nao devolve a marca de citacao). Se o trecho da
    fonte e o proprio trecho do documento, a fonte e o documento."""
    if trecho_documento and normalizar(trecho_fonte) == normalizar(trecho_documento):
        return "documento.md"
    for arq in sorted(pacote.rglob("*.md")):
        if arq.name == "MANIFESTO.md":
            continue
        if existe(trecho_fonte, arq.read_text(encoding="utf-8", errors="replace")):
            return arq.relative_to(pacote).as_posix()
    return None


def conferir_achados(pacote: Path, dados: dict) -> list[dict]:
    doc = (pacote / "documento.md").read_text(encoding="utf-8")
    for a in dados.get("achados", []):
        aprox = False
        if not existe(a.get("trecho_documento", ""), doc):
            if not aproximado(a.get("trecho_documento", ""), doc):
                a["citacao"] = "documento: trecho não encontrado"
                continue
            aprox = True
        if not a.get("fonte_arquivo") and (a.get("trecho_fonte") or "").strip():
            a["fonte_arquivo"] = localizar_fonte(pacote, a["trecho_fonte"], a.get("trecho_documento", ""))
            if not a["fonte_arquivo"]:
                a["citacao"] = "fonte: trecho não encontrado em nenhum arquivo do pacote"
                continue
        if a.get("fonte_arquivo"):
            texto = ler_arquivo(pacote, a["fonte_arquivo"])
            if texto is None:
                a["citacao"] = "fonte: arquivo não existe no pacote"
                continue
            if not existe(a.get("trecho_fonte") or "", texto):
                if not aproximado(a.get("trecho_fonte") or "", texto):
                    a["citacao"] = "fonte: trecho não encontrado"
                    continue
                aprox = True
        a["citacao"] = "ok, aproximado" if aprox else "ok"
    return dados.get("achados", [])


def conferir_resposta(pacote: Path, achados: list[dict], resposta: dict) -> list[str]:
    falhas = []
    por_id = {r["id"]: r for r in resposta.get("respostas", [])}
    for a in achados:
        r = por_id.get(a["id"])
        if not r:
            falhas.append(f"{a['id']}: sem resposta")
            continue
        st = r.get("status")
        if st in ("aceito", "aceito_em_parte"):
            if not r.get("secao_alterada"):
                falhas.append(f"{a['id']}: {st} sem a seção alterada")
            if not r.get("fonte_arquivo"):
                falhas.append(f"{a['id']}: {st} sem a fonte que sustenta a correção")
        if st == "contestado":
            texto = ler_arquivo(pacote, r.get("fonte_arquivo"))
            if texto is None:
                falhas.append(f"{a['id']}: contestado sem fonte que exista")
            elif not existe(r.get("trecho_fonte") or "", texto):
                falhas.append(f"{a['id']}: contestado com trecho que não está na fonte")
        if st == "decisao_do_usuario" and not (r.get("nota") or "").strip():
            falhas.append(f"{a['id']}: decisão do usuário sem a nota (qual decisão, de quando)")
        if st == "citacao_invalida" and a.get("citacao", "ok").startswith("ok"):
            falhas.append(f"{a['id']}: marcado citação inválida, mas a citação confere")
    sobra = set(por_id) - {a["id"] for a in achados}
    falhas += [f"{i}: resposta a achado que não existe" for i in sorted(sobra)]
    return falhas


def conferir_veredito(achados: list[dict], veredito: dict) -> list[str]:
    ids = {v["id"] for v in veredito.get("vereditos", [])}
    return [f"{a['id']}: sem veredito" for a in achados if a["id"] not in ids]


def main():
    saida_utf8()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pacote")
    ap.add_argument("achados")
    ap.add_argument("--resposta")
    ap.add_argument("--veredito")
    args = ap.parse_args()
    pacote, arq = Path(args.pacote), Path(args.achados)
    dados = json.loads(arq.read_text(encoding="utf-8"))
    achados = conferir_achados(pacote, dados)
    arq.write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8")
    contagem = {}
    for a in achados:
        contagem[a["citacao"]] = contagem.get(a["citacao"], 0) + 1
    print(f"{arq}: {len(achados)} achados")
    for k, v in sorted(contagem.items(), key=lambda x: -x[1]):
        print(f"  {v:3d}  {k}")
    falhas = []
    if args.resposta:
        falhas += conferir_resposta(pacote, achados, json.loads(Path(args.resposta).read_text(encoding="utf-8")))
    if args.veredito:
        falhas += conferir_veredito(achados, json.loads(Path(args.veredito).read_text(encoding="utf-8")))
    if args.resposta or args.veredito:
        print("RESPOSTA/VEREDITO:", "ok" if not falhas else f"{len(falhas)} falha(s)")
        for f in falhas:
            print("  -", f)
    sys.exit(1 if falhas else 0)


if __name__ == "__main__":
    main()
