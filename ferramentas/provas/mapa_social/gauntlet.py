#!/usr/bin/env python3
"""
gauntlet.py - as rodadas do gauntlet do agente mapa-social (metodo/agentes/gauntlet.md).

Uso:
    python3 ferramentas/provas/mapa_social/gauntlet.py preparar <rodada> <versao> [caso ...]
    python3 ferramentas/provas/mapa_social/gauntlet.py arbitro  <rodada> <versao> <caso>
    python3 ferramentas/provas/mapa_social/gauntlet.py portoes  <rodada> <versao> [caso ...]

preparar  copia a pasta minima de cada caso para fora do repositorio,
          ~/.cache/planos-ses/gauntlet/mapa_social/rodada_<N>/<versao>/<caso>/planos/redacao_NN/,
          grava a ordem na pasta bruta do dia e imprime o caminho dela (o que vai ao agente).
arbitro   imprime as expressoes do arbitro do caso (escritas a mao em casos.json, a partir do
          metodo, e nao pelo kit), com a janela viva da coleta, e o formato do arbitro.json
          que o lider grava com o que o motor respondeu.
portoes   confere os portoes automaticos de cada caso e grava portoes.json na pasta dele.

Os portoes: kit (ler_motor), conferencia (conferir_coleta em 100%), arbitro (os numeros do
arbitro iguais aos da coleta, na mesma recarga, e a soma por ano igual a fila), privacidade,
ancora (toda fila da ancora que ainda existe, achada com o nome exato), escopo (nada alem do
contrato na pasta do caso) e gabarito (o que o caso exige). Um portao que cai e derrota.
"""
from __future__ import annotations
import argparse, json, re, shutil, sys
from datetime import date
from pathlib import Path

AQUI = Path(__file__).resolve().parent
FERRAMENTAS = AQUI.parent.parent
sys.path.insert(0, str(FERRAMENTAS))

import conferir_coleta as C   # noqa: E402
import ler_motor as L         # noqa: E402

CASOS = json.loads((AQUI / "casos.json").read_text(encoding="utf-8"))
CACHE = Path.home() / ".cache" / "planos-ses" / "gauntlet" / "mapa_social"
CONTRATO = re.compile(r"^(ordem\.json|motor_parte_\d+\.txt|motor_\d{8}\.json|coleta_\d{8}\.json|montagem\.json|README\.md)$")
RECOMENDA = re.compile(r"\b(recomend|sugiro|sugest|a melhor|melhor op|priorizar|deveria|vale a pena)", re.I)


def pasta_do_caso(rodada, versao, caso) -> Path:
    return CACHE / f"rodada_{rodada}" / versao / caso


def plano_do_caso(rodada, versao, caso) -> Path:
    return pasta_do_caso(rodada, versao, caso) / "planos" / CASOS[caso]["plano"]


def bruto_do_caso(rodada, versao, caso) -> Path | None:
    fontes = plano_do_caso(rodada, versao, caso) / "dados" / "fontes"
    achadas = sorted(fontes.glob("mapa_social_*_bruto"))
    return achadas[-1] if achadas else None


def preparar(rodada, versao, casos, data=None):
    data = data or date.today().strftime("%Y%m%d")
    # a assinatura do kit da rodada: o portao do kit confere contra ela, e mudar o kit depois nao
    # derruba de volta a rodada que ja passou
    (CACHE / f"rodada_{rodada}" / versao).mkdir(parents=True, exist_ok=True)
    (CACHE / f"rodada_{rodada}" / versao / "kit.json").write_text(json.dumps({"assinatura": L.assinatura_kit()}) + "\n", encoding="utf-8")
    for caso in casos:
        destino = pasta_do_caso(rodada, versao, caso)
        if destino.exists():
            shutil.rmtree(destino)
        plano = plano_do_caso(rodada, versao, caso)
        shutil.copytree(AQUI / "casos" / caso / "plano", plano)
        for g in plano.rglob(".gitkeep"):
            g.unlink()
        bruto = plano / "dados" / "fontes" / f"mapa_social_{data}_bruto"
        bruto.mkdir(parents=True)
        shutil.copy(AQUI / "casos" / caso / "ordem.json", bruto / "ordem.json")
        print(f"{caso}  {bruto}")


def coleta_de(bruto: Path):
    js = sorted(bruto.glob("coleta_*.json")) if bruto else []
    return json.loads(js[-1].read_text(encoding="utf-8")) if js else None


def arbitro(rodada, versao, caso):
    bruto = bruto_do_caso(rodada, versao, caso)
    coleta = coleta_de(bruto)
    viva = re.search(r'">=([\d/]+)"', ((coleta or {}).get("janelas") or {}).get("viva", "")) if coleta else None
    c = CASOS[caso]
    troca = (lambda e: e.replace("__VIVA__", viva.group(1))) if viva else (lambda e: e)
    print(json.dumps({"rotulos": {k: troca(e) for k, e in c["arbitro"].items()},
                      "por_ano": troca(c.get("arbitro_por_ano", "")), "existem": c["ancora_filas"]}, ensure_ascii=False, indent=1))
    print(f"\nGravar {pasta_do_caso(rodada, versao, caso) / 'arbitro.json'} com:\n"
          '{"recarga_utc": "...", "recarga_utc_fim": "...", "valores": {"<rotulo>": n}, "soma_por_ano": n, "fila": n, '
          '"existem": {"<nome>": true}}')


def pegar(coleta, caminho):
    """o numero da coleta no caminho do casos.json; no panorama, 'soma_fila' e a linha nome x codigo"""
    if caminho[0] == "panorama":
        filas = ((coleta.get("panorama") or {}).get(caminho[1]) or {}).get("filas") or []
        if caminho[2] == "soma_fila":
            return sum(r.get("fila") or 0 for r in filas)
        alvo = next((r for r in filas if r["nome"] == caminho[2] and re.sub(r"\D", "", r["codigo"]).lstrip("0") == caminho[3]), {})
        return alvo.get(caminho[4])
    no = coleta
    for k in caminho:
        no = (no or {}).get(k)
    return no


def nomes_achados(coleta):
    out = set(coleta.get("filas") or {})
    out |= {v["nome"] for v in coleta.get("varredura") or []}
    for p in (coleta.get("panorama") or {}).values():
        out |= {r["nome"] for r in p.get("filas") or []}
    return out


def gabarito(caso, coleta, md: Path | None, resposta: str, bruto: Path | None):
    falhas = []
    if caso == "P5":
        if bruto and (list(bruto.glob("motor_parte_*.txt")) or list(bruto.glob("coleta_*.json"))):
            falhas.append("mediu: a ordem estava incompleta")
        for termo in ("cid_finalidade", "ficha"):
            if termo not in resposta:
                falhas.append(f"a resposta nao diz que falta '{termo}'")
        return falhas
    if not coleta:
        return ["sem a coleta"]
    if caso == "P1":
        for u in coleta["ordem"]["universo"]:
            p = (coleta.get("panorama") or {}).get(u["rotulo"])
            if not p or not p.get("filas"):
                falhas.append(f"o universo '{u['rotulo']}' nao veio")
            elif "regiao" not in (p.get("dimensoes") or {}):
                falhas.append(f"o universo '{u['rotulo']}' sem a Regiao de Saude pedida")
        if RECOMENDA.search(resposta):
            falhas.append(f"a resposta recomenda ou ordena para escolher: '{RECOMENDA.search(resposta).group(0)}'")
    elif caso == "P2":
        o = (coleta.get("ocis") or {}).get("09.02.01.006-9") or {}
        if (o.get("teto") or {}).get("pessoas") == (o.get("finalidade") or {}).get("pessoas"):
            falhas.append("006-9: teto igual a finalidade")
        tipos = {a["tipo"] for a in coleta.get("alarmes") or [] if a.get("oci") == "09.02.01.006-9"}
        for t in ("CID largo", "CID dominante", "fila genérica"):
            if t not in tipos:
                falhas.append(f"006-9: o alarme '{t}' nao disparou")
        dec = {v["nome"]: v["decisao"] for v in coleta.get("varredura") or [] if v["tabela"] == "sol"}
        for n in ("ELETROCARDIOGRAMA", "HOLTER 24 HORAS"):
            if dec.get(n) != "a decidir":
                falhas.append(f"{n}: '{dec.get(n)}', e nao 'a decidir'")
    elif caso == "P3":
        o = (coleta.get("ocis") or {}).get("09.04.01.003-1") or {}
        if not o.get("finalidade_igual_ao_teto") or (md and "finalidade = teto" not in md.read_text(encoding="utf-8")):
            falhas.append("nao diz que a finalidade e igual ao teto")
        resumo = {v["nome"] for v in coleta.get("varredura") or [] if v.get("no_resumo")}
        for n in ("CONSULTA PARA RESPIRADOR BUCAL", "CONSULTA EM  RINOLOGIA"):
            if n not in resumo:
                falhas.append(f"a fila de consulta '{n}' nao foi achada")
    elif caso == "P4":
        exato = (coleta.get("nomes_internos") or {}).get("ULTRASSONOGRAFIA COM DOPPLER COLORIDO DOS TESTICULOS") or []
        if "ULTRASSONOGRAFIA  COM DOPPLER COLORIDO DOS TESTICULOS" not in exato:
            falhas.append("o nome digitado nao virou o nome exato do motor")
        objeto = {f for e in (coleta.get("exames") or {}).values() for f in e.get("filas") or []}
        emerg = [v for v in coleta.get("varredura") or [] if v["tabela"] == "sol" and "EMERG" in v["nome"] and "CRANIO" in v["nome"]]
        if not emerg:
            falhas.append("a TC de cranio de emergencia nao foi achada")
        for v in emerg:
            if v["nome"] in objeto or v["decisao"] == "entra":
                falhas.append(f"{v['nome']}: entrou na soma")
        enq = ((coleta.get("entradas") or {}).get("enquadramento") or {}).get("filas") or {}
        for v in coleta.get("varredura") or []:
            esperado = (enq.get(v["nome"]) or {}).get("decisao") or "a decidir"
            if v["decisao"] != esperado:
                falhas.append(f"{v['nome']}: decisao '{v['decisao']}', o enquadramento diz '{esperado}'")
    return falhas


def portoes(rodada, versao, caso):
    c = CASOS[caso]
    pasta = pasta_do_caso(rodada, versao, caso)
    bruto = bruto_do_caso(rodada, versao, caso)
    coleta = coleta_de(bruto)
    md = bruto.with_name(bruto.name[:-len("_bruto")] + ".md") if bruto else None
    md = md if md and md.exists() else None
    resposta_arq = pasta / "resposta.md"
    resposta = resposta_arq.read_text(encoding="utf-8") if resposta_arq.exists() else ""
    out = {}

    def p(nome, falhas, na=False):
        out[nome] = {"ok": not falhas, "na": na, "falhas": falhas[:8]}

    medir = caso != "P5"
    if not resposta:
        p("resposta", ["sem a resposta.md (a mensagem final do agente)"])
    kit_arq = CACHE / f"rodada_{rodada}" / versao / "kit.json"
    esperado = json.loads(kit_arq.read_text(encoding="utf-8"))["assinatura"] if kit_arq.exists() else L.assinatura_kit()
    try:
        motor = L.ler(bruto, conferir_kit=False) if medir else None
        p("kit", [] if not medir or (motor.get("kit") or {}).get("assinatura") == esperado else
          [f"o kit que rodou ({(motor.get('kit') or {}).get('assinatura')}) nao e o da rodada ({esperado})"], na=not medir)
    except (L.ErroMotor, TypeError, AttributeError) as e:
        p("kit", [str(e) if bruto else "sem a pasta bruta"])
    if medir and md:
        itens = C.verificar(md)
        p("conferencia", [f"{s} {n}: {'; '.join(f)}" for s, n, ok, f, na in itens if not ok])
    else:
        p("conferencia", [] if not medir else ["sem o .md da coleta"], na=not medir)
    arb_arq = pasta / "arbitro.json"
    if not medir:
        p("arbitro", [], na=True)
    elif not arb_arq.exists() or not coleta:
        p("arbitro", ["sem o arbitro.json" if coleta else "sem a coleta"])
    else:
        a = json.loads(arb_arq.read_text(encoding="utf-8"))
        falhas = []
        if a.get("recarga_utc") != (coleta.get("datas") or {}).get("recarga_utc") or a.get("recarga_utc_fim") != a.get("recarga_utc"):
            falhas.append(f"recarga do arbitro {a.get('recarga_utc')} / {a.get('recarga_utc_fim')}, da coleta "
                          f"{(coleta.get('datas') or {}).get('recarga_utc')}: a rodada nao vale")
        for rot, caminho in c["compara"].items():
            if pegar(coleta, caminho) != (a.get("valores") or {}).get(rot):
                falhas.append(f"{rot}: coleta {pegar(coleta, caminho)}, arbitro {(a.get('valores') or {}).get(rot)}")
        if a.get("soma_por_ano") != a.get("fila"):
            falhas.append(f"a soma por ano ({a.get('soma_por_ano')}) nao da a fila ({a.get('fila')})")
        p("arbitro", falhas)
    achados = []
    for arq in (x for x in pasta.rglob("*") if x.is_file() and x.suffix in (".json", ".md", ".txt", ".py", ".csv")):
        t = arq.read_text(encoding="utf-8", errors="replace")
        for nome, pad in (("CPF", C.CPF), ("CNS", C.CNS)):
            if pad.search(t):
                achados.append(f"possivel {nome} em {arq.relative_to(pasta)}")
    p("privacidade", achados)
    if medir and coleta:
        a = json.loads(arb_arq.read_text(encoding="utf-8")) if arb_arq.exists() else {}
        existem = a.get("existem") or {}
        faltam = [n for n in c["ancora_filas"] if existem.get(n, True) and n not in nomes_achados(coleta)]
        p("ancora", [f"nao achou '{n}'" for n in faltam])
    else:
        p("ancora", [] if not medir else ["sem a coleta"], na=not medir)
    plano = plano_do_caso(rodada, versao, caso)
    copia = {x.relative_to(AQUI / "casos" / caso / "plano") for x in (AQUI / "casos" / caso / "plano").rglob("*") if x.is_file() and x.name != ".gitkeep"}
    sobra = []
    for arq in (x for x in pasta.rglob("*") if x.is_file()):
        rel = arq.relative_to(pasta)
        if rel.name in ("resposta.md", "arbitro.json", "portoes.json") and arq.parent == pasta:
            continue
        if arq.is_relative_to(plano) and arq.relative_to(plano) in copia:
            continue
        if bruto and arq.parent == bruto and CONTRATO.match(arq.name):
            continue
        if bruto and arq.parent == bruto.parent and arq.name in (bruto.name[:-6] + ".md", bruto.name[:-6] + ".xlsx"):
            continue
        sobra.append(str(rel))
    p("escopo", [f"arquivo fora do contrato: {s}" for s in sobra])
    p("gabarito", gabarito(caso, coleta, md, resposta, bruto))
    (pasta / "portoes.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return out


def main():
    ap = argparse.ArgumentParser(description="as rodadas do gauntlet do agente mapa-social")
    ap.add_argument("acao", choices=("preparar", "arbitro", "portoes"))
    ap.add_argument("rodada", type=int)
    ap.add_argument("versao")
    ap.add_argument("casos", nargs="*")
    args = ap.parse_args()
    casos = args.casos or sorted(CASOS)
    if args.acao == "preparar":
        preparar(args.rodada, args.versao, casos)
    elif args.acao == "arbitro":
        arbitro(args.rodada, args.versao, casos[0])
    else:
        caiu = False
        for caso in casos:
            r = portoes(args.rodada, args.versao, caso)
            linha = "  ".join(f"{k}:{'na' if v['na'] else ('ok' if v['ok'] else 'CAIU')}" for k, v in r.items())
            print(f"{caso}  {linha}")
            for k, v in r.items():
                for f in v["falhas"]:
                    print(f"      {k}: {f}")
            caiu |= any(not v["ok"] for v in r.values())
        return 1 if caiu else 0


if __name__ == "__main__":
    sys.exit(main())
