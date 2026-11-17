#!/usr/bin/env python3
"""
montar_coleta.py - monta a coleta do Mapa Social a partir do JSON do motor.

Uso:
    python3 ferramentas/montar_coleta.py --ordem <pasta bruta>    confere a ordem e imprime a forma do kit
    python3 ferramentas/montar_coleta.py <pasta bruta>            monta a coleta
    python3 ferramentas/montar_coleta.py <pasta bruta> --anterior <coleta_AAAAMMDD.json>

O metodo e metodo/coleta/mapa_social.md ("O montador"). Le a ordem.json e o motor_<data>.json
da pasta bruta, o enquadramento do plano (dados/enquadramento_mapa_social.json) e a coleta
anterior, se houver, e grava:
  - coleta_<data>.json   o JSON da coleta, no formato do metodo, com as entradas que usou;
  - ../<nome>.md          o resumo: cabecalho, alarmes, tres numeros, varredura, dimensoes, diferenca;
  - ../<nome>.xlsx        a planilha;
  - README.md            o que tem a pasta bruta.

Nao decide nada: a decisao de cada fila vem do enquadramento (o usuario decide na conversa
principal), e a fila sem decisao sai "a decidir". Os alarmes sao os do conferir_coleta.py,
com os limites de la. O .md se refaz do JSON byte a byte: a conferencia K derruba a edicao a mao.

Codigo 1 se a ordem estiver incompleta ou faltar o motor.
"""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

import conferir_coleta as C
import ler_motor as L
from comum import saida_utf8

VERSAO = "2026-10-27"
# a versao do montador: sobe quando o que ele grava muda, e a conferencia K so refaz a coleta da
# mesma versao (a de outra versao se confere pelos hashes do montagem.json)
MONTADOR = "2026-10-27.3"
PAINEL = "https://paineis-ext.mpdft.mp.br/extensions/mapasauderegulamentacao/mapasauderegulamentacao.html"
DIMENSOES = ("regiao", "idade", "cid", "entrantes", "ano", "oferta", "situacao")
# no panorama, o rumo de cada codigo das filas do universo (metodo, "O rumo por codigo")
POR_CODIGO = ("entrantes", "oferta", "situacao")
POR = {"codigo": "código", "nome": "nome", "termo": "termo", "cid_aceito": "CID aceito", "cid_finalidade": "CID da finalidade"}
SEXOS = ("ambos", "feminino", "masculino")
SAIDAS = ("area_de_transferencia", "transcricao")


# --------------------------------------------------------------------- a ordem
def validar_ordem(ordem, plano: Path | None = None):
    """o que falta na ordem para o agente medir; vazio quando ela esta completa"""
    faltas = []
    if not isinstance(ordem, dict):
        return ["a ordem nao e um objeto JSON"]
    for k in ("contrato", "tipo", "plano", "saida"):
        if not ordem.get(k):
            faltas.append(f"a ordem nao diz '{k}'")
    if ordem.get("tipo") not in (None, "panorama", "medicao"):
        faltas.append(f"tipo '{ordem.get('tipo')}': a ordem e de panorama ou de medicao")
    if ordem.get("saida") and ordem["saida"] not in SAIDAS:
        faltas.append(f"saida '{ordem['saida']}': area_de_transferencia ou transcricao")
    if not isinstance(ordem.get("janela_viva_meses", 24), int):
        faltas.append("janela_viva_meses tem de ser um numero inteiro de meses")
    for d in ordem.get("dimensoes") or []:
        if d not in DIMENSOES:
            faltas.append(f"dimensao '{d}': o kit mede {', '.join(DIMENSOES)}")
    if ordem.get("tipo") == "panorama":
        uni = ordem.get("universo")
        if not uni:
            faltas.append("panorama sem 'universo' (subgrupo SIGTAP, termos do nome ou tudo)")
        for i, u in enumerate(uni or []):
            if not u.get("rotulo"):
                faltas.append(f"universo {i + 1} sem 'rotulo'")
            if not (u.get("codigos") or u.get("termos") or u.get("tudo")):
                faltas.append(f"universo '{u.get('rotulo', i + 1)}' sem 'codigos', 'termos' nem 'tudo'")
        if len({u.get("rotulo") for u in uni or []}) != len(uni or []):
            faltas.append("dois universos com o mesmo rotulo")
        for d in ordem.get("por_codigo") or []:
            if d not in POR_CODIGO:
                faltas.append(f"por_codigo '{d}': o kit mede {', '.join(POR_CODIGO)}")
    elif ordem.get("tipo") == "medicao":
        if ordem.get("por_codigo"):
            faltas.append("por_codigo e so do panorama: na medicao, pedir 'entrantes', 'oferta' e 'situacao' em 'dimensoes'")
        objs = ordem.get("objetos")
        if not objs:
            faltas.append("medicao sem 'objetos'")
        ids = [o.get("id") for o in objs or []]
        if len(set(ids)) != len(ids):
            faltas.append("dois objetos com o mesmo id")
        for o in objs or []:
            q = o.get("id") or "(objeto sem id)"
            for k in ("id", "tipo", "nome", "codigos", "filas"):
                if not o.get(k):
                    faltas.append(f"{q}: falta '{k}'")
            if o.get("tipo") not in (None, "oci", "exame"):
                faltas.append(f"{q}: tipo '{o.get('tipo')}': oci ou exame")
            for f in o.get("filas") or []:
                if not (isinstance(f, dict) and f.get("nome")):
                    faltas.append(f"{q}: fila de partida sem 'nome'")
            if any(L_codigo(c) == "301010072" for c in o.get("codigos") or []):
                faltas.append(f"{q}: o codigo 03.01.01.007-2 e o de toda consulta especializada do SISREG, e a varredura "
                              "acharia todas: tire-o dos 'codigos' (na OCI, a consulta se acha pelo CID)")
            if o.get("sexo") and o["sexo"] not in SEXOS:
                faltas.append(f"{q}: sexo '{o['sexo']}': {', '.join(SEXOS)}")
            if o.get("tipo") == "oci":
                for k, o_que in (("cid_aceito", "o CID aceito da ficha"), ("cid_finalidade", "o CID da finalidade da ficha"),
                                 ("ficha", "a ficha do SIGTAP na pasta do plano"), ("idade", "a idade da ficha"),
                                 ("sexo", "o sexo da ficha")):
                    if not o.get(k):
                        faltas.append(f"{q}: falta '{k}' ({o_que})")
                if o.get("ficha") and plano is not None and not (plano / o["ficha"]).exists():
                    faltas.append(f"{q}: a ficha {o['ficha']} nao existe em {plano.name}/")
                if o.get("idade") and not isinstance(o["idade"], dict):
                    faltas.append(f"{q}: idade como {{\"min\": anos, \"max\": anos}}")
                if not any(f.get("entrada") or f.get("obrigatorio") for f in o.get("filas") or [] if isinstance(f, dict)):
                    faltas.append(f"{q}: nenhuma fila marcada 'entrada' (a consulta de entrada) nem 'obrigatorio' "
                                  "(os exames obrigatorios): sem elas o nucleo nao se mede")
    return faltas


def L_codigo(c) -> str:
    """o codigo como o motor guarda (o mesmo K.codigo do kit): sem pontos e sem o zero da frente"""
    s = str(c).strip()
    d = re.sub(r"\D", "", s)
    return d[1:] if len(d) == 10 or (s.endswith("*") and d.startswith("0")) else d


def forma_do_kit(ordem) -> str:
    """a ordem como vai para __ms.rodar(...): JSON em ASCII, com o \\u do espaco nao separavel"""
    return json.dumps(ordem, ensure_ascii=True, separators=(",", ":"))


# --------------------------------------------------------------------- formato
def sig(c):
    c = str(c or "")
    return f"0{c[0]}.{c[1:3]}.{c[3:5]}.{c[5:8]}-{c[8]}" if re.fullmatch(r"\d{9}", c) else c


def n(v):
    if v is None:
        return "—"
    return f"{int(round(v)):,}".replace(",", ".")


def d1(v):
    if v is None:
        return "—"
    return f"{v:,.1f}".replace(",", "X").replace(".", ",").replace("X", ".")


def pct(a, b):
    return "—" if not b or a is None else f"{100 * a / b:.0f}%"


def bonito(nome):
    return re.sub(r" {2,}", " ", str(nome).replace("\u00a0", " ")).strip().replace("|", "\\|")


def visivel(nome):
    """o nome exato com o invisivel a mostra: o espaco nao separavel e os espacos repetidos"""
    return str(nome).replace("\u00a0", "{NBSP}").replace("|", "\\|")


def cids(lista, k=5):
    return ", ".join(f"{c} {n(q)}" for c, q in (lista or [])[:k]) or "—"


def texto_alarme(a):
    """o texto do alarme sem repetir o codigo da OCI, que ja vai entre parenteses"""
    t = a["texto"]
    return bonito(t[len(a["oci"]) + 2:] if a.get("oci") and t.startswith(a["oci"] + ": ") else t)


def tabela(cab, linhas):
    out = ["| " + " | ".join(cab) + " |", "|" + "---|" * len(cab)]
    out += ["| " + " | ".join(str(x) for x in l) + " |" for l in linhas]
    return "\n".join(out)


def como_dicts(t):
    return [dict(zip(t["cols"], l)) for l in (t or {}).get("linhas") or []]


def anos_estoque(fila, ag):
    if not fila or ag is None:
        return "—"
    return "sem agendamento" if ag == 0 else d1(fila / ag)


# ------------------------------------------------------------------- as entradas
def plano_da_pasta(bruto: Path) -> Path:
    """planos/redacao_NN/dados/fontes/<x>_bruto -> planos/redacao_NN"""
    return bruto.resolve().parent.parent.parent


def ler_enquadramento(plano: Path):
    arq = plano / "dados" / "enquadramento_mapa_social.json"
    if not arq.exists():
        return {"arquivo": None, "filas": {}, "ocis": {}}
    e = json.loads(arq.read_text(encoding="utf-8"))
    return {"arquivo": "dados/enquadramento_mapa_social.json", "atualizado": e.get("atualizado"),
            "filas": e.get("filas") or {}, "ocis": e.get("ocis") or {}}


def resumo_anterior(arq: Path, plano: Path):
    """o que a diferenca usa de uma coleta anterior: a fila e as pessoas por fila, os numeros por objeto"""
    d = json.loads(arq.read_text(encoding="utf-8"))
    filas = {}
    if C.formato_novo(d):
        for nome, f in d["filas"].items():
            filas[nome] = {"fila": f.get("fila"), "pessoas": f.get("pessoas")}
    ocis = {}
    for cod, o in (d.get("ocis") or {}).items() if isinstance(d.get("ocis"), dict) else []:
        ocis[cod] = {k: (o.get(k) or {}).get("pessoas") for k in ("teto", "finalidade", "nucleo")}
    exames = {cod: {"pessoas": ((e.get("uniao") or {}).get("pessoas"))} for cod, e in (d.get("exames") or {}).items()}
    panorama = {}
    for rot, p in (d.get("panorama") or {}).items():
        panorama[rot] = {f"{r['nome']}|{r['codigo']}": r.get("fila") for r in p.get("filas") or []}
    if not (filas or ocis or exames or panorama):
        return None
    try:
        rel = arq.resolve().relative_to(plano.resolve()).as_posix()
    except ValueError:
        rel = arq.name
    recarga = (d.get("datas") or {}).get("recarga") or d.get("recarga_brasilia") or d.get("recarga_utc")
    return {"arquivo": rel, "recarga": recarga, "filas": filas, "ocis": ocis, "exames": exames, "panorama": panorama}


def achar_anterior(bruto: Path):
    """a coleta mais recente da mesma pasta de fontes, de antes desta (pela data no nome da pasta)"""
    data = L.data_da_pasta(bruto)
    cands = []
    for b in bruto.parent.glob("mapa_social_*_bruto"):
        if b.resolve() == bruto.resolve():
            continue
        m = re.search(r"mapa_social_(\d{8})", b.name)
        if not m or m.group(1) > data:
            continue
        for j in sorted(b.glob("coleta_*.json")):
            cands.append((m.group(1), b.name, j))
    return max(cands)[2] if cands else None


def entradas_de(bruto: Path, anterior: Path | None = None):
    plano = plano_da_pasta(bruto)
    ant = anterior or achar_anterior(bruto)
    return {"enquadramento": ler_enquadramento(plano),
            "anterior": resumo_anterior(ant, plano) if ant else None}


# --------------------------------------------------------------------- montar
def decisao(nome, enq, partida):
    e = (enq.get("filas") or {}).get(nome)
    if e and e.get("decisao"):
        return e["decisao"], e.get("motivo") or "", True
    if nome in partida:
        return "a decidir", "fila de partida da ordem, sem decisao no enquadramento", False
    return "a decidir", "achada pela varredura, sem decisao no enquadramento", False


def montar(motor: dict, ordem: dict, entradas: dict) -> dict:
    """a coleta, so a partir do motor, da ordem e das entradas gravadas (sem ler mais nada)"""
    enq = entradas.get("enquadramento") or {"filas": {}, "ocis": {}}
    d0, dfim = (motor.get("datas") or {}).get("inicio") or {}, (motor.get("datas") or {}).get("fim") or {}
    coleta = {
        "metodo": VERSAO, "tipo": ordem["tipo"], "janela_viva_meses": ordem.get("janela_viva_meses", 24),
        "app": motor.get("app"), "titulo_app": motor.get("titulo_app"), "painel": PAINEL,
        "datas": {"recarga": d0.get("recarga_brasilia"), "recarga_utc": d0.get("recarga_utc"),
                  "consulta_inicio": d0.get("consulta"), "consulta_fim": dfim.get("consulta"),
                  "solicitacao_mais_recente": d0.get("solicitacao_max"), "agendamento_mais_distante": d0.get("agendamento_max")},
        "filtro_fila": motor.get("filtro_fila"), "filtro_devolvidas": motor.get("filtro_devolvidas"),
        "janelas": motor.get("janelas"), "ordem": ordem, "ordem_hash": motor.get("ordem_hash"),
        "kit": motor.get("kit"), "leitura": motor.get("leitura"), "montado_por": f"ferramentas/montar_coleta.py {MONTADOR}",
        "nomes_internos": {}, "filas": {}, "ocis": {}, "exames": {}, "varredura": [], "panorama": {}, "dimensoes": {},
        "por_codigo": {}, "rumo": [], "lacunas": list(motor.get("lacunas") or []), "entradas": entradas,
    }
    if ordem["tipo"] == "panorama":
        montar_panorama(coleta, motor, ordem)
    else:
        montar_medicao(coleta, motor, ordem, enq)
    coleta["alarmes"] = [] if ordem["tipo"] == "panorama" else C.alarmes(coleta)
    coleta["diferenca"] = diferenca(coleta, entradas.get("anterior"))
    return coleta


def por_objeto(r):
    """as colunas 'fila_cid_aceito <id>' do kit -> {'<id> cid aceito': n}"""
    out = {}
    for k, v in r.items():
        m = re.match(r"fila_(cid_aceito|cid_finalidade) (.+)$", k)
        if m:
            out[f"{m.group(2)} {m.group(1).replace('_', ' ')}"] = v
    return out


def montar_medicao(coleta, motor, ordem, enq):
    partida = set()
    for o in ordem["objetos"]:
        mo = (motor.get("objetos") or {}).get(o["id"]) or {}
        nomes = mo.get("nomes") or {}
        for f in o["filas"]:
            coleta["nomes_internos"][f["nome"]] = nomes.get(f["nome"], [])
            partida.update(nomes.get(f["nome"], []))
        val = mo.get("valores") or {}
        por_nome = {r["nome"]: r for r in como_dicts(mo.get("filas"))}
        cp = mo.get("cid_principais") or {}
        ags = mo.get("agendadas_12m") or {}
        exatos_de = {f["nome"]: nomes.get(f["nome"], []) for f in o["filas"]}
        for f in o["filas"]:
            for ex in exatos_de[f["nome"]]:
                r = por_nome.get(ex, {})
                e = (enq.get("filas") or {}).get(ex) or {}
                fila = coleta["filas"].setdefault(ex, {
                    "pedido": f["nome"], "objetos": [], "papel": f.get("papel") or e.get("papel") or "exame",
                    "generica": bool(f.get("generica") or e.get("generica") or C.GENERICAS.search(C._norm(ex))),
                    "codigos": sorted({sig(l[2]) for l in motor["varredura"]["linhas"]
                                       if l[0] == "sol" and l[1] == ex}) if motor.get("varredura") else [],
                    **{k: r.get(k) for k in ("fila", "fila_viva", "pessoas", "pessoas_viva", "devolvidas", "espera_media",
                                             "espera_mediana", "espera_max", "mais_antiga", "idade_mediana", "total")},
                    "agendadas_12m": ags.get(f["nome"]), "cid_principais": None, "recortes": {}})
                fila["objetos"].append(o["id"])
                if f.get("entrada"):
                    fila["entrada"] = True
                if f.get("obrigatorio"):
                    fila["obrigatorio"] = True
                recs = ([("teto", "teto"), ("finalidade", "finalidade")] if o["tipo"] == "oci"
                        else [(x["rotulo"], x["rotulo"]) for x in o.get("recortes") or []])
                for rot, kit_rot in recs:
                    rotulo = f"{rot} {o['id']}" if o["tipo"] == "oci" else rot
                    fila["recortes"][rotulo] = {"fila": r.get(f"recorte {kit_rot} fila"), "fila_viva": r.get(f"recorte {kit_rot} fila_viva"),
                                                "cid_principais": (cp.get(kit_rot) or {}).get(ex)}
                if not recs:
                    fila["cid_principais"] = (cp.get("sem recorte") or {}).get(ex)
                elif o["tipo"] == "oci" and fila["cid_principais"] is None:
                    fila["cid_principais"] = (cp.get("teto") or {}).get(ex)
        comp = [ex for f in o["filas"] for ex in exatos_de[f["nome"]]]
        grupo = lambda k: {c: val.get(f"{k}.{c}") for c in ("pessoas", "pessoas_viva", "fila", "fila_viva",
                                                             "espera_media", "espera_mediana", "devolvidas")}
        if o["tipo"] == "oci":
            teto, fin = grupo("teto"), grupo("finalidade")
            fin["pessoas_sem_idade_sexo"] = val.get("finalidade_sem_idade_sexo.pessoas")
            fin["pessoas_viva_sem_idade_sexo"] = val.get("finalidade_sem_idade_sexo.pessoas_viva")
            for p in ("exames", "consultas"):
                if val.get(f"finalidade_{p}.pessoas") is not None:
                    fin[p] = {"pessoas": val[f"finalidade_{p}.pessoas"], "pessoas_viva": val.get(f"finalidade_{p}.pessoas_viva")}
            ent = [ex for f in o["filas"] if f.get("entrada") for ex in exatos_de[f["nome"]]]
            obr = [f["nome"] for f in o["filas"] if f.get("obrigatorio") and exatos_de[f["nome"]]]
            cand = []
            if val.get("nucleo_entrada.pessoas") is not None:
                cand.append({"pessoas": val["nucleo_entrada.pessoas"], "pessoas_viva": val.get("nucleo_entrada.pessoas_viva"),
                             "como": "consulta de entrada (" + ", ".join(bonito(x) for x in ent) + ")"})
            if val.get("nucleo_obrigatorios.pessoas") is not None:
                cand.append({"pessoas": val["nucleo_obrigatorios.pessoas"], "pessoas_viva": val.get("nucleo_obrigatorios.pessoas_viva"),
                             "como": ("exames obrigatorios ao mesmo tempo (" if len(obr) > 1 else "o unico exame obrigatorio com fila (")
                             + ", ".join(bonito(x) for x in obr) + ")"})
            nucleo = dict(max(cand, key=lambda c: (c["pessoas"], c["como"]))) if cand else {"pessoas": None, "pessoas_viva": None, "como": None}
            nucleo["candidatos"] = cand
            if not cand:
                coleta["lacunas"].append({"onde": f"{o['id']} nucleo", "motivo": "nem a consulta de entrada nem os exames obrigatorios responderam"})
            coleta["ocis"][o["id"]] = {
                "nome": o["nome"], "ficha": o.get("ficha"), "cid_aceito": o["cid_aceito"], "cid_finalidade": o["cid_finalidade"],
                "finalidade_igual_ao_teto": sorted(C.tokens(o["cid_aceito"])) == sorted(C.tokens(o["cid_finalidade"])),
                "idade": o.get("idade"), "sexo": o.get("sexo"),
                "recorte_teto": f"teto {o['id']}", "recorte_finalidade": f"finalidade {o['id']}",
                "filas": comp, "entrada": ent, "obrigatorios": obr,
                "teto": teto, "finalidade": fin, "nucleo": nucleo}
        else:
            coleta["exames"][o["id"]] = {"nome": o["nome"], "codigos": o["codigos"], "idade": o.get("idade"),
                                         "sexo": o.get("sexo"), "filas": comp, "uniao": grupo("uniao")}
        coleta["dimensoes"][o["id"]] = mo.get("dimensoes") or {}
    # a varredura: toda fila achada, com a decisao do enquadramento. A fila que tambem esta nas
    # solicitacoes ja traz as agendadas na linha dela; da tabela de agendamentos fica so a que
    # nao tem pedido na de solicitacoes
    linhas = como_dicts(motor.get("varredura"))
    na_sol = {(r["nome"], r["codigo"]) for r in linhas if r["tabela"] == "sol"}
    for r in linhas:
        if r["tabela"] == "ag" and (r["nome"], r["codigo"]) in na_sol:
            continue
        dec, motivo, no_enq = decisao(r["nome"], enq, partida)
        item = {"tabela": r["tabela"], "nome": r["nome"], "codigo": sig(r["codigo"]), "por": r["por"], "objetos": r["objetos"],
                **{k: r.get(k) for k in ("fila", "fila_viva", "pessoas", "devolvidas", "espera_media", "espera_mediana",
                                         "mais_antiga", "idade_mediana", "total", "agendadas_12m", "cid_principais")},
                "por_objeto": por_objeto(r),
                "generica": bool((enq.get("filas") or {}).get(r["nome"], {}).get("generica") or C.GENERICAS.search(C._norm(r["nome"]))),
                "na_ordem": r["nome"] in partida, "decisao": dec, "motivo": motivo, "no_enquadramento": no_enq}
        # a fila achada so pelo CID vai ao resumo quando o CID do objeto e parte relevante dos pedidos
        # dela (conferir_coleta.LIM_VARREDURA); as outras ficam no JSON e na planilha
        no_cid = [v for k, v in item["por_objeto"].items() if k.endswith("cid aceito") and v is not None]
        item["parte_cid"] = round(max(no_cid) / item["fila"], 4) if no_cid and item["fila"] else None
        so_cid = set(item["por"]) <= {"cid_aceito", "cid_finalidade"}
        item["no_resumo"] = (not so_cid) or item["na_ordem"] or no_enq or (
            item["parte_cid"] is not None and item["parte_cid"] >= C.LIM_VARREDURA)
        coleta["varredura"].append(item)
    coleta["varredura"].sort(key=lambda x: (x["tabela"] != "sol", -(x["fila"] or 0), -(x["agendadas_12m"] or 0), x["nome"], x["codigo"]))


def montar_panorama(coleta, motor, ordem):
    for u in ordem["universo"]:
        p = (motor.get("panorama") or {}).get(u["rotulo"])
        if p is None:
            coleta["lacunas"].append({"onde": u["rotulo"], "motivo": "o kit nao devolveu este universo"})
            continue
        filas = []
        for r in como_dicts(p.get("filas")):
            r = dict(r)
            r["codigo"] = sig(r["codigo"])
            ag = r.get("agendadas_12m")
            r["anos_estoque"] = None if not r.get("fila") or ag is None else (None if ag == 0 else round(r["fila"] / ag, 2))
            r["sem_agendamento_12m"] = ag == 0
            filas.append(r)
        filas.sort(key=lambda r: (-(r.get("pessoas") or 0), r["nome"], r["codigo"]))
        coleta["panorama"][u["rotulo"]] = {"universo": {k: u.get(k) for k in ("codigos", "termos", "tudo") if u.get(k)},
                                           "total": p.get("total"), "filas": filas, "dimensoes": p.get("dimensoes") or {}}
    for d, t in (motor.get("por_codigo") or {}).items():
        coleta["por_codigo"][d] = {"cols": t["cols"], "linhas": [[sig(l[0])] + list(l[1:]) for l in t["linhas"]]}
    coleta["rumo"] = rumo_por_codigo(coleta)


def meses_fechados(coleta):
    """os 12 meses fechados antes do mes da solicitacao mais recente, e os 12 de antes deles"""
    m = re.match(r"\d{2}/(\d{2})/(\d{4})", coleta["datas"].get("solicitacao_mais_recente") or "")
    if not m:
        return [], []
    agora = int(m.group(2)) * 12 + int(m.group(1)) - 1
    meses = [f"{k // 12}-{k % 12 + 1:02d}" for k in range(agora - 24, agora)]
    return meses[12:], meses[:12]


def rumo_por_codigo(coleta):
    """por codigo, o que a serie mensal diz (calculado): entrantes e oferta nos 12 meses fechados e
    nos 12 de antes, a falta, o saldo por mes, o maior mes de oferta e a media dos 3 ultimos"""
    pc = coleta["por_codigo"]
    ult, ant = meses_fechados(coleta)
    if not (ult and pc):
        return []
    ent, ofe = como_dicts(pc.get("entrantes")), como_dicts(pc.get("oferta"))
    serie = {}
    for r in ent:
        x = serie.setdefault(r["codigo"], {}).setdefault(r["mes"], {})
        x["entrantes"] = (r.get("abertas") or 0) + (r.get("agendadas") or 0)
    for r in ofe:
        x = serie.setdefault(r["codigo"], {}).setdefault(r["mes"], {})
        x.update(oferta=r.get("agendamentos") or 0, realizados=r.get("realizados") or 0, faltas=r.get("faltas") or 0)
    filas, vistos = {}, set()
    for p in coleta["panorama"].values():
        for r in p["filas"]:
            if (r["nome"], r["codigo"]) in vistos:
                continue
            vistos.add((r["nome"], r["codigo"]))
            f = filas.setdefault(r["codigo"], {"fila": 0, "fila_viva": 0, "devolvidas": 0, "nomes": []})
            for k in ("fila", "fila_viva", "devolvidas"):
                f[k] += r.get(k) or 0
            f["nomes"].append((r.get("fila") or 0, r["nome"]))
    out = []
    for cod in sorted(set(filas) | set(serie)):
        s_ = serie.get(cod, {})
        soma = lambda meses, k: sum((s_.get(m_) or {}).get(k, 0) for m_ in meses)
        of = [(m_, (s_.get(m_) or {}).get("oferta", 0)) for m_ in ant + ult]
        pico = max(of, key=lambda x: x[1])
        real, falt = soma(ult, "realizados"), soma(ult, "faltas")
        f = filas.get(cod) or {}
        out.append({"codigo": cod, "fila_maior": max(f["nomes"])[1] if f.get("nomes") else None,
                    "fila": f.get("fila"), "fila_viva": f.get("fila_viva"), "devolvidas": f.get("devolvidas"),
                    "entrantes_12m": soma(ult, "entrantes"), "entrantes_12m_antes": soma(ant, "entrantes"),
                    "oferta_12m": soma(ult, "oferta"), "oferta_12m_antes": soma(ant, "oferta"),
                    "realizados_12m": real, "faltas_12m": falt, "falta_12m": round(falt / (real + falt), 3) if real + falt else None,
                    "saldo_mes": round((soma(ult, "entrantes") - soma(ult, "oferta")) / 12, 1),
                    "pico_oferta_mes": pico[0] if pico[1] else None, "pico_oferta": pico[1],
                    "oferta_media_3m": round(sum(v for _, v in of[-3:]) / 3, 1)})
    out.sort(key=lambda r: (-(r["fila"] or 0), r["codigo"]))
    return out


def diferenca(coleta, ant):
    if not ant:
        return None
    out = {"arquivo": ant["arquivo"], "recarga": ant.get("recarga"), "filas": {}, "ocis": {}, "exames": {}, "panorama": {}}
    for nome, f in coleta["filas"].items():
        a = (ant.get("filas") or {}).get(nome)
        if a:
            out["filas"][nome] = {"fila_antes": a.get("fila"), "fila_agora": f.get("fila"),
                                  "pessoas_antes": a.get("pessoas"), "pessoas_agora": f.get("pessoas")}
    for cod, o in coleta["ocis"].items():
        a = (ant.get("ocis") or {}).get(cod)
        if a:
            out["ocis"][cod] = {k: {"antes": a.get(k), "agora": (o.get(k) or {}).get("pessoas")} for k in ("teto", "finalidade", "nucleo")}
    for cod, e in coleta["exames"].items():
        a = (ant.get("exames") or {}).get(cod)
        if a:
            out["exames"][cod] = {"antes": a.get("pessoas"), "agora": e["uniao"].get("pessoas")}
    for rot, p in coleta["panorama"].items():
        a = (ant.get("panorama") or {}).get(rot)
        if a:
            out["panorama"][rot] = {"filas_antes": len(a), "filas_agora": len(p["filas"]),
                                    "fila_antes": sum(v or 0 for v in a.values()), "fila_agora": sum(r.get("fila") or 0 for r in p["filas"])}
    return out


# -------------------------------------------------------------------- o resumo
def titulo(coleta):
    o = coleta["ordem"]
    if o["tipo"] == "panorama":
        return "panorama: " + ", ".join(u["rotulo"] for u in o["universo"])
    partes = []
    for x in o["objetos"]:
        partes.append(f"OCI {x['id']} ({x['nome']})" if x["tipo"] == "oci" else f"{x['nome']} ({x['id']})")
    return "fila de " + "; ".join(partes)


def renderizar_md(coleta) -> str:
    o, d = coleta["ordem"], coleta["datas"]
    data = (d.get("consulta_inicio") or "")[:10]
    via = "área de transferência" if o.get("saida") == "area_de_transferencia" else "transcrição"
    L_ = [f"# Mapa Social da Saúde — {titulo(coleta)}, coleta de {data}", ""]
    if o.get("pedido"):
        L_ += [f"Ordem de coleta: {o['pedido']}", ""]
    L_ += ["Coleta montada por `ferramentas/montar_coleta.py` a partir da saída do kit do motor: o modelo não escreveu número "
           "nenhum, e o resumo não se edita à mão (conferência K). A decisão de cada fila vem do enquadramento do plano.", ""]
    j = coleta.get("janelas") or {}
    cab = [
        ("Fonte", f"Mapa Social da Saúde – Regulamentação (MPDFT) · Lista de Espera – Exames e Consultas · `{PAINEL}` · "
                  f"app Qlik `{coleta.get('app')}` · dados SISREG/DATASUS"),
        ("Última recarga da base", f"{d.get('recarga')} (qLastReloadTime {d.get('recarga_utc')})"),
        ("Consulta", f"{d.get('consulta_inicio')} a {(d.get('consulta_fim') or '')[11:]} (relógio do motor), sem recarga no meio"),
        ("Solicitação mais recente na base", f"{d.get('solicitacao_mais_recente')} (agendamento mais distante: {d.get('agendamento_mais_distante')})"),
        ("Medida", "**fila** = os três status: pendente de regulação, corrigida e reenviada para regulação, pendente de "
                   "regulação por fila de espera. Devolvidas para complementação ficam fora e são contadas à parte"),
        ("Fila viva", f"só as solicitações a partir de `{j.get('viva', '')}` ({coleta['janela_viva_meses']} meses contados da solicitação mais recente)"),
        ("Agendadas em 12 meses", f"`{j.get('agendadas_12m', '')}`, todos os status"),
        ("Ordem", f"{o['tipo']}; `ordem.json` (hash {coleta.get('ordem_hash')})"),
        ("Via", f"kit do motor `ferramentas/mapa_social/motor.js` (versão {(coleta.get('kit') or {}).get('versao')}, assinatura "
                f"{(coleta.get('kit') or {}).get('assinatura')}); saída pela {via}, {(coleta.get('leitura') or {}).get('partes')} parte(s) "
                f"conferidas por hash (`ferramentas/ler_motor.py`)"),
    ]
    L_ += [tabela(["campo", "conteúdo"], cab), "", "Pessoas = CNS distintos no conjunto (quem espera por mais de um exame conta "
           "uma vez); só a contagem sai do motor. Espera em dias, calculada no motor sobre os registros do conjunto.", ""]
    L_ += ["## Alarmes", ""]
    if coleta["tipo"] == "panorama":
        L_ += ["Não se aplicam ao panorama: os alarmes são do objeto (CID, composição, fila viva), e o panorama não tem objeto.", ""]
    elif coleta["alarmes"]:
        lim = (f"Limites de `ferramentas/conferir_coleta.py`: {C.LIM_DOMINANTE:.0%} (CID dominante), {C.LIM_RARO:.0%} (CID raro), "
               f"{C.LIM_VELHA:.0%} (fila velha), {C.LIM_ESTOQUE} anos (estoque), {C.LIM_CATEGORIAS} categorias (CID largo).")
        vistos = []
        for a in coleta["alarmes"]:
            linha = f"- **{a['tipo']}**" + (f" ({a['oci']})" if a.get("oci") else "") + f": {texto_alarme(a)}"
            if linha not in vistos:
                vistos.append(linha)
        L_ += [lim, ""] + vistos + [""]
    else:
        L_ += ["nenhum", ""]
    L_ += ["## Lacunas", ""]
    L_ += ([f"- {bonito(x['onde'])}: {bonito(x['motivo'])}" for x in coleta["lacunas"]] or ["nenhuma"]) + [""]
    if coleta["tipo"] == "panorama":
        L_ += md_panorama(coleta)
    else:
        L_ += md_medicao(coleta)
    L_ += md_diferenca(coleta)
    return "\n".join(L_).rstrip() + "\n"


def md_medicao(coleta):
    L_ = []
    if coleta["ocis"]:
        L_ += ["## Os três números", "", "Em pessoas, na idade e no sexo da ficha. A finalidade é a fila da OCI; o teto fica como "
               "referência e nunca vai ao dossiê nem à justificativa.", ""]
        linhas = []
        for cod, x in coleta["ocis"].items():
            linhas.append([cod, f"`{x['cid_aceito']}`", f"`{x['cid_finalidade']}`", n(x["teto"]["pessoas"]), n(x["teto"]["pessoas_viva"]),
                           f"**{n(x['finalidade']['pessoas'])}**", n(x["finalidade"]["pessoas_viva"]), n(x["nucleo"]["pessoas"]),
                           n(x["nucleo"]["pessoas_viva"]), d1(x["finalidade"]["espera_media"])])
        L_ += [tabela(["OCI", "CID aceito", "CID da finalidade", "teto", "teto viva", "finalidade", "finalidade viva", "núcleo",
                       "núcleo viva", "espera média (finalidade)"], linhas), ""]
        for cod, x in coleta["ocis"].items():
            f = x["finalidade"]
            nota = [f"- **{cod}** ({x['nome']}): ficha `{x.get('ficha')}`; idade {x['idade'].get('min', 0)} a "
                    f"{x['idade'].get('max', 130)} anos, sexo {x['sexo']}."]
            if x["finalidade_igual_ao_teto"]:
                nota.append(" A ficha não separa a finalidade do CID aceito: **finalidade = teto**.")
            nota.append(f" Na idade e no sexo da ficha ficam {n(f['pessoas'])} das {n(f.get('pessoas_sem_idade_sexo'))} pessoas da finalidade.")
            if f.get("exames"):
                nota.append(f" Só nas filas de exame: {n(f['exames']['pessoas'])} ({n(f['exames']['pessoas_viva'])} na viva); só nas de "
                            f"consulta: {n(f['consultas']['pessoas'])} ({n(f['consultas']['pessoas_viva'])} na viva).")
            nota.append(f" Núcleo: {x['nucleo']['como'] or 'sem número'}" + "".join(
                f"; {c['como']}: {n(c['pessoas'])} ({n(c['pessoas_viva'])} na viva)" for c in x["nucleo"]["candidatos"]
                if c["como"] != x["nucleo"]["como"]) + ".")
            nota.append(f" Fila (pedidos) na finalidade: {n(f['fila'])} ({n(f['fila_viva'])} na viva), devolvidas {n(f['devolvidas'])},"
                        f" espera mediana {d1(f['espera_mediana'])} dias.")
            L_.append("".join(nota))
        L_.append("")
    if coleta["exames"]:
        L_ += ["## Exames", "", "A união das filas de cada exame, na idade e no sexo da ordem, quando ela os dá.", ""]
        linhas = [[f"{bonito(e['nome'])} ({cod})", len(e["filas"]), n(e["uniao"]["fila"]), n(e["uniao"]["fila_viva"]),
                   f"**{n(e['uniao']['pessoas'])}**", n(e["uniao"]["pessoas_viva"]), n(e["uniao"]["devolvidas"]),
                   d1(e["uniao"]["espera_media"]), d1(e["uniao"]["espera_mediana"])] for cod, e in coleta["exames"].items()]
        L_ += [tabela(["exame", "filas", "fila", "fila viva", "pessoas", "pessoas viva", "devolvidas", "espera média",
                       "espera mediana"], linhas), ""]
    L_ += ["## Filas do objeto", "", "As filas de partida da ordem, pelo nome exato do motor, sem recorte de CID. Anos de estoque "
           "= fila ÷ agendadas em 12 meses (**calculado** no montador).", ""]
    linhas = []
    for nome, f in coleta["filas"].items():
        linhas.append([bonito(nome), ", ".join(f["codigos"]) or "—", ", ".join(f["objetos"]), f["papel"] + (" (genérica)" if f["generica"] else "")
                       + (", entrada" if f.get("entrada") else "") + (", obrigatório" if f.get("obrigatorio") else ""),
                       n(f["fila"]), n(f["fila_viva"]), n(f["pessoas"]), n(f["devolvidas"]), d1(f["espera_media"]),
                       d1(f["espera_mediana"]), d1(f["espera_max"]), f["mais_antiga"] or "—", n(f["agendadas_12m"]),
                       anos_estoque(f["fila"], f["agendadas_12m"]), cids(f["cid_principais"])])
    L_ += [tabela(["fila", "código", "objeto", "papel", "fila", "fila viva", "pessoas", "devolvidas", "espera média",
                   "espera mediana", "espera máxima", "pedido mais antigo", "agendadas 12 m", "anos de estoque", "CID principais"],
                  linhas), ""]
    rec = [(nome, rot, r) for nome, f in coleta["filas"].items() for rot, r in f["recortes"].items()]
    if rec:
        L_ += ["**Por recorte de CID**, em pedidos:", ""]
        L_ += [tabela(["fila", "recorte", "fila", "fila viva", "parte da fila (calculado)", "CID principais no recorte"],
                      [[bonito(nm), rot, n(r["fila"]), n(r["fila_viva"]), pct(r["fila"], coleta["filas"][nm]["fila"]),
                        cids(r["cid_principais"])] for nm, rot, r in rec]), ""]
    L_ += ["## Varredura das filas", "", "Toda fila que a varredura achou, pelo código, pelo nome e, na OCI, pelo CID aceito e "
           "pelo da finalidade, nas tabelas de solicitações e de agendamentos. A decisão é a do enquadramento do plano; "
           "fila sem decisão sai **a decidir** e não entra na soma.", ""]
    linhas = []
    for v in (x for x in coleta["varredura"] if x["no_resumo"]):
        linhas.append([bonito(v["nome"]) + (" (genérica)" if v["generica"] else ""), v["codigo"],
                       "solicitações" if v["tabela"] == "sol" else "só agendamentos", ", ".join(POR.get(p, p) for p in v["por"]),
                       ", ".join(v["objetos"]),
                       n(v["fila"]), n(v["fila_viva"]), n(v["pessoas"]), n(v["devolvidas"]), d1(v["espera_media"]),
                       v["mais_antiga"] or "—", n(v["agendadas_12m"]), cids(v["cid_principais"]),
                       "; ".join(f"{k} {n(q)}" for k, q in v["por_objeto"].items() if q is not None) or "—",
                       pct(v["parte_cid"], 1) if v["parte_cid"] is not None else "—", v["decisao"], bonito(v["motivo"])])
    L_ += [tabela(["fila", "código", "tabela", "achada por", "objeto", "fila", "fila viva", "pessoas", "devolvidas", "espera média",
                   "pedido mais antigo", "agendadas 12 m", "CID principais", "no CID do objeto", "parte no CID aceito (calculado)",
                   "decisão", "motivo"], linhas), ""]
    fora = [v for v in coleta["varredura"] if not v["no_resumo"]]
    if fora:
        sol = [v for v in fora if v["tabela"] == "sol"]
        soma = sum(max([q for k, q in v["por_objeto"].items() if k.endswith("cid aceito") and q is not None] or [0]) for v in sol)
        L_ += [f"Mais {len(sol)} filas de solicitação achadas só pelo CID, com menos de {C.LIM_VARREDURA:.0%} dos pedidos no CID "
               f"aceito do objeto ({n(soma)} pedidos no CID, somados), e {len(fora) - len(sol)} nomes só da tabela de agendamentos "
               "achados só pelo CID: estão no JSON da coleta e na aba Varredura da planilha.", ""]
    L_ += md_dimensoes(coleta)
    L_ += ["## Nomes internos", "", "O nome pedido na ordem e o nome exato do motor, com o invisível à mostra ({NBSP} é o espaço "
           "não separável). O JSON guarda o exato.", ""]
    L_ += [tabela(["pedido", "exato"], [[visivel(p), "; ".join(visivel(x) for x in ex) or "**não existe no motor**"]
                                        for p, ex in coleta["nomes_internos"].items()]), ""]
    return L_


def md_dimensoes(coleta, fonte=None):
    L_ = ["## Região de Saúde", ""]
    fonte = fonte if fonte is not None else coleta["dimensoes"]
    tem = False
    for obj, dims in fonte.items():
        r = dims.get("regiao")
        if not r:
            continue
        tem = True
        linhas = sorted(r["linhas"], key=lambda l: (-(l[1] or 0), l[0]))
        sem = r.get("sem_regiao") or {}
        L_ += [f"**{obj}**, na medida da fila (o conjunto do objeto):", "",
               tabela(["Região de Saúde", "fila", "pessoas"], [[bonito(l[0]), n(l[1]), n(l[2])] for l in linhas]
                      + [["sem Região de Saúde", n(sem.get("fila")), n(sem.get("pessoas"))]]), ""]
    if not tem:
        L_ += ["Região de Saúde: não pedida na ordem.", ""]
    for chave, tit, cab, fmt in (
            ("idade", "Idade na solicitação", ["faixa", "fila", "pessoas"], lambda l: [f"{int(float(l[0]))} a {int(float(l[0])) + 9}", n(l[1]), n(l[2])]),
            ("cid", "CID principais", ["CID", "fila", "pessoas"], lambda l: [l[0], n(l[1]), n(l[2])]),
            ("ano", "Por ano da solicitação", ["ano", "fila", "fila viva"], lambda l: [l[0], n(l[1]), n(l[2])]),
            ("entrantes", "Entrantes por mês", ["mês", "abertas", "agendadas", "entrantes (calculado)"],
             lambda l: [l[0], n(l[1]), n(l[2]), n((l[1] or 0) + (l[2] or 0))]),
            ("oferta", "Oferta por mês do agendamento", ["mês", "agendamentos", "realizados", "faltas", "falta (calculado)"],
             lambda l: [l[0], n(l[1]), n(l[2]), n(l[3]), pct(l[3], (l[2] or 0) + (l[3] or 0))]),
            ("situacao", "Situação dos agendamentos em 12 meses", ["situação", "agendamentos", "parte (calculado)"], None)):
        blocos = [(obj, dims[chave]) for obj, dims in fonte.items() if dims.get(chave)]
        if not blocos:
            continue
        L_ += [f"## {tit}", ""]
        if chave == "entrantes":
            L_ += ["Abertas = solicitações de todos os status pelo mês do pedido; agendadas = agendamentos pelo mês da solicitação "
                   "(data do agendamento menos a espera). O último mês está incompleto.", ""]
        if chave == "oferta":
            L_ += ["Agendamentos pelo mês em que acontecem, em todas as situações; realizados e faltas pela situação do agendamento. "
                   "Os meses depois da solicitação mais recente são o que já está marcado, e o mês dela está incompleto. "
                   "Falta = faltas ÷ (realizados + faltas).", ""]
        for obj, t in blocos:
            linhas = t["linhas"]
            if chave == "idade":
                linhas = sorted(linhas, key=lambda l: float(l[0]))
            elif chave in ("ano", "entrantes", "oferta"):
                linhas = sorted(linhas, key=lambda l: l[0])
            if chave == "situacao":
                tot = sum(l[1] or 0 for l in linhas)
                linhas = sorted(linhas, key=lambda l: (-(l[1] or 0), l[0]))
                L_ += [f"**{obj}**:", "", tabela(cab, [[bonito(l[0]), n(l[1]), pct(l[1], tot)] for l in linhas]
                                                   + [["total", n(tot), "100%" if tot else "—"]]), ""]
                continue
            L_ += [f"**{obj}**:", "", tabela(cab, [fmt(l) for l in linhas]), ""]
    return L_


def md_panorama(coleta):
    L_ = ["## O universo", ""]
    L_ += ["O total de cada universo é do motor, com cada pedido e cada pessoa uma vez: a soma das filas pode passar dele, "
           "porque o mesmo pedido pode estar em dois pares nome × código.", ""]
    L_ += [tabela(["recorte", "o que entra", "filas", "fila", "fila viva", "pessoas"],
                  [[rot, "; ".join(f"{k}: {', '.join(v) if isinstance(v, list) else v}" for k, v in p["universo"].items()),
                    len(p["filas"]), n((p.get("total") or {}).get("fila")), n((p.get("total") or {}).get("fila_viva")),
                    n((p.get("total") or {}).get("pessoas"))] for rot, p in coleta["panorama"].items()]), ""]
    L_ += ["## Varredura das filas (panorama)", "", "Cada fila do universo (nome exato × código), sem decisão: o panorama só "
           "mostra. Anos de estoque = fila ÷ agendadas em 12 meses pelo mesmo nome e código (**calculado**).", ""]
    cab = ["fila", "código", "fila", "fila viva", "pessoas", "devolvidas", "espera média", "espera mediana", "espera máxima",
           "pedido mais antigo", "agendadas 12 m", "anos de estoque", "CID principais"]
    lin = lambda r: [bonito(r["nome"]), r["codigo"], n(r.get("fila")), n(r.get("fila_viva")), n(r.get("pessoas")), n(r.get("devolvidas")),
                     d1(r.get("espera_media")), d1(r.get("espera_mediana")), d1(r.get("espera_max")), r.get("mais_antiga") or "—",
                     n(r.get("agendadas_12m")), anos_estoque(r.get("fila"), r.get("agendadas_12m")), cids(r.get("cid_principais"), 3)]
    for rot, p in coleta["panorama"].items():
        L_ += [f"### {rot}: por pessoas", "", tabela(cab, [lin(r) for r in p["filas"]]), ""]
        esp = sorted(p["filas"], key=lambda r: (-(r.get("espera_media") or 0), r["nome"], r["codigo"]))[:20]
        L_ += [f"### {rot}: as 20 de maior espera média", "", tabela(cab, [lin(r) for r in esp]), ""]
        est = sorted([r for r in p["filas"] if r.get("anos_estoque") is not None or r.get("sem_agendamento_12m")],
                     key=lambda r: (not r.get("sem_agendamento_12m"), -(r.get("anos_estoque") or 0), r["nome"], r["codigo"]))[:20]
        L_ += [f"### {rot}: as 20 de mais anos de estoque", "", tabela(cab, [lin(r) for r in est]), ""]
    L_ += md_rumo(coleta)
    L_ += md_dimensoes(coleta, {rot: p["dimensoes"] for rot, p in coleta["panorama"].items()})
    return L_


def md_rumo(coleta):
    if not coleta.get("por_codigo"):
        return []
    ult, ant = meses_fechados(coleta)
    L_ = ["## Rumo por código", "",
          f"Um código por linha, com as filas do universo somadas (cada par nome × código uma vez). Tudo **calculado** no "
          f"montador sobre a série mensal do motor (abas \"Por código\" da planilha). Os 12 meses fechados vão de {ult[0]} a "
          f"{ult[-1]}, e os 12 de antes, de {ant[0]} a {ant[-1]}. Entrantes = pedidos abertos mais os já agendados, pelo mês do "
          "pedido. Oferta = agendamentos pelo mês em que acontecem, em todas as situações. Falta = faltas ÷ (realizados + faltas). "
          "Saldo por mês = (entrantes − oferta) ÷ 12: positivo, a fila cresce. Maior mês de oferta e média dos 3 últimos meses "
          "fechados, para ver o esforço que parou.", ""]
    cab = ["código", "fila mais pedida do código", "fila", "fila viva", "devolvidas", "entrantes 12 m", "entrantes 12 m antes",
           "oferta 12 m", "oferta 12 m antes", "saldo por mês", "falta 12 m", "maior mês de oferta", "oferta média 3 últimos meses"]
    lin = lambda r: [r["codigo"], bonito(r["fila_maior"]) if r["fila_maior"] else "—", n(r["fila"]), n(r["fila_viva"]), n(r["devolvidas"]),
                     n(r["entrantes_12m"]), n(r["entrantes_12m_antes"]), n(r["oferta_12m"]), n(r["oferta_12m_antes"]),
                     d1(r["saldo_mes"]), "—" if r["falta_12m"] is None else f"{100 * r['falta_12m']:.0f}%",
                     f"{r['pico_oferta_mes']} ({n(r['pico_oferta'])})" if r["pico_oferta_mes"] else "—", d1(r["oferta_media_3m"])]
    return L_ + [tabela(cab, [lin(r) for r in coleta["rumo"]]), ""]


def md_diferenca(coleta):
    dif = coleta.get("diferenca")
    if not dif:
        return ["## Diferença para a coleta anterior", "", "Sem coleta anterior na pasta.", ""]
    L_ = ["## Diferença para a coleta anterior", "", f"Contra `{dif['arquivo']}` (recarga {dif.get('recarga')}). Diferença "
          "**calculada** no montador.", ""]
    if dif["ocis"]:
        L_ += [tabela(["OCI", "número", "antes", "agora", "diferença"],
                      [[cod, k, n(v["antes"]), n(v["agora"]), n(v["agora"] - v["antes"]) if None not in (v["antes"], v["agora"]) else "—"]
                       for cod, x in dif["ocis"].items() for k, v in x.items()]), ""]
    if dif["exames"]:
        L_ += [tabela(["exame", "pessoas antes", "pessoas agora", "diferença"],
                      [[cod, n(v["antes"]), n(v["agora"]), n(v["agora"] - v["antes"]) if None not in (v["antes"], v["agora"]) else "—"]
                       for cod, v in dif["exames"].items()]), ""]
    if dif["filas"]:
        L_ += [tabela(["fila", "fila antes", "fila agora", "diferença", "pessoas antes", "pessoas agora"],
                      [[bonito(nm), n(v["fila_antes"]), n(v["fila_agora"]),
                        n(v["fila_agora"] - v["fila_antes"]) if None not in (v["fila_antes"], v["fila_agora"]) else "—",
                        n(v["pessoas_antes"]), n(v["pessoas_agora"])] for nm, v in dif["filas"].items()]), ""]
    if dif["panorama"]:
        L_ += [tabela(["recorte", "filas antes", "filas agora", "fila antes", "fila agora"],
                      [[rot, v["filas_antes"], v["filas_agora"], n(v["fila_antes"]), n(v["fila_agora"])] for rot, v in dif["panorama"].items()]), ""]
    if not (dif["ocis"] or dif["exames"] or dif["filas"] or dif["panorama"]):
        L_ += ["A coleta anterior não tem as mesmas filas nem os mesmos objetos.", ""]
    return L_


def renderizar_readme(coleta, nome_md: str, data: str) -> str:
    d = coleta["datas"]
    via = "área de transferência" if coleta["ordem"].get("saida") == "area_de_transferencia" else "transcrição"
    linhas = [
        ("`ordem.json`", f"a ordem de coleta, gravada pelo líder antes de chamar o agente (hash {coleta.get('ordem_hash')})"),
        ("`motor_parte_N.txt`", f"a saída do kit do motor, tirada do navegador pela {via}: {(coleta.get('leitura') or {}).get('partes')} "
                                f"parte(s), cada uma com tamanho e hash djb2 no cabeçalho"),
        (f"`motor_{data}.json`", "o JSON do motor (`ferramentas/ler_motor.py`): as partes conferidas, os nomes exatos e as datas em DD/MM/AAAA"),
        (f"`coleta_{data}.json`", "o JSON da coleta no formato do método (`ferramentas/montar_coleta.py`), com as entradas que o "
                                  "montador usou (o enquadramento e a coleta anterior); é o que a conferência lê"),
        ("`montagem.json`", "a versão do montador e o hash djb2 de cada arquivo que ele gravou: a conferência K derruba a edição à mão"),
    ]
    return "\n".join([
        f"# Mapa Social, {d.get('recarga')} — dados brutos da coleta", "",
        f"{titulo(coleta)}. Resumo em `../{nome_md}`. Só contagens agregadas: nenhum CNS, CPF, nome ou data de nascimento.", "",
        tabela(["arquivo", "o que é"], linhas), "",
        "Refazer, da raiz do repositório:", "",
        "```bash",
        "python3 ferramentas/ler_motor.py <esta pasta>",
        "python3 ferramentas/montar_coleta.py <esta pasta>",
        f"python3 ferramentas/conferir_coleta.py <a pasta de cima>/{nome_md}",
        "```", ""])


# ------------------------------------------------------------------- a planilha
def gravar_xlsx(coleta, arq: Path):
    import openpyxl
    from openpyxl.styles import Font
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Leia-me"

    def aba(nome, cab, linhas):
        w = wb.create_sheet(re.sub(r"[\[\]:*?/\\]", " ", nome)[:31])
        w.append(cab)
        for c in w[1]:
            c.font = Font(bold=True)
        for l in linhas:
            w.append([json.dumps(x, ensure_ascii=False) if isinstance(x, (list, dict)) else x for x in l])
        w.freeze_panes = "A2"
        return w

    d = coleta["datas"]
    for l in (("Mapa Social da Saúde (MPDFT)", PAINEL), ("título", titulo(coleta)), ("recarga", d.get("recarga")),
              ("consulta", f"{d.get('consulta_inicio')} a {d.get('consulta_fim')}"),
              ("solicitação mais recente", d.get("solicitacao_mais_recente")), ("medida", coleta.get("filtro_fila")),
              ("devolvidas", coleta.get("filtro_devolvidas")), ("fila viva", (coleta.get("janelas") or {}).get("viva")),
              ("agendadas 12 meses", (coleta.get("janelas") or {}).get("agendadas_12m")),
              ("montado por", coleta.get("montado_por")),
              ("nota", "Números do motor; o que for calculado no montador diz 'calculado' no cabeçalho. Só contagens agregadas.")):
        ws.append(list(l))
    aba("Alarmes", ["tipo", "OCI", "fila", "texto"], [[a["tipo"], a.get("oci"), a.get("fila"), a["texto"]] for a in coleta["alarmes"]])
    aba("Lacunas", ["onde", "motivo"], [[x["onde"], x["motivo"]] for x in coleta["lacunas"]])
    if coleta["ocis"]:
        aba("Três números", ["OCI", "CID aceito", "CID da finalidade", "teto", "teto viva", "finalidade", "finalidade viva", "núcleo",
                             "núcleo viva", "como", "espera média (finalidade)", "finalidade sem idade e sexo"],
            [[cod, x["cid_aceito"], x["cid_finalidade"], x["teto"]["pessoas"], x["teto"]["pessoas_viva"], x["finalidade"]["pessoas"],
              x["finalidade"]["pessoas_viva"], x["nucleo"]["pessoas"], x["nucleo"]["pessoas_viva"], x["nucleo"]["como"],
              x["finalidade"]["espera_media"], x["finalidade"].get("pessoas_sem_idade_sexo")] for cod, x in coleta["ocis"].items()])
    if coleta["exames"]:
        aba("Exames", ["exame", "nome", "filas", "fila", "fila viva", "pessoas", "pessoas viva", "devolvidas", "espera média", "espera mediana"],
            [[cod, e["nome"], len(e["filas"])] + [e["uniao"].get(k) for k in ("fila", "fila_viva", "pessoas", "pessoas_viva", "devolvidas",
                                                                               "espera_media", "espera_mediana")] for cod, e in coleta["exames"].items()])
    if coleta["filas"]:
        ks = ("fila", "fila_viva", "pessoas", "pessoas_viva", "devolvidas", "espera_media", "espera_mediana", "espera_max",
              "mais_antiga", "idade_mediana", "total", "agendadas_12m")
        aba("Filas do objeto", ["nome exato", "pedido", "objetos", "papel", "genérica"] + list(ks) + ["anos de estoque (calculado)", "CID principais"],
            [[nm, f["pedido"], f["objetos"], f["papel"], f["generica"]] + [f.get(k) for k in ks]
             + [None if not f.get("fila") or not f.get("agendadas_12m") else round(f["fila"] / f["agendadas_12m"], 2), f["cid_principais"]]
             for nm, f in coleta["filas"].items()])
    if coleta["varredura"]:
        ks = ("tabela", "nome", "codigo", "por", "objetos", "fila", "fila_viva", "pessoas", "devolvidas", "espera_media",
              "espera_mediana", "mais_antiga", "idade_mediana", "total", "agendadas_12m", "cid_principais", "por_objeto",
              "generica", "na_ordem", "decisao", "motivo", "no_enquadramento", "parte_cid", "no_resumo")
        aba("Varredura", list(ks), [[v.get(k) for k in ks] for v in coleta["varredura"]])
    for rot, p in coleta["panorama"].items():
        if p["filas"]:
            ks = list(p["filas"][0].keys())
            aba("Panorama " + rot, ks, [[r.get(k) for k in ks] for r in p["filas"]])
    fontes = dict(coleta["dimensoes"])
    fontes.update({rot: p["dimensoes"] for rot, p in coleta["panorama"].items()})
    for chave, nome in (("regiao", "Região"), ("idade", "Idade"), ("cid", "CID"), ("ano", "Ano"), ("entrantes", "Entrantes"),
                        ("oferta", "Oferta"), ("situacao", "Situação")):
        linhas = [[obj] + l for obj, dims in fontes.items() if dims.get(chave) for l in dims[chave]["linhas"]]
        linhas += [[obj, "sem Região de Saúde", dims["regiao"]["sem_regiao"].get("fila"), dims["regiao"]["sem_regiao"].get("pessoas")]
                   for obj, dims in fontes.items() if chave == "regiao" and dims.get("regiao")]
        if linhas:
            cols = next(dims[chave]["cols"] for dims in fontes.values() if dims.get(chave))
            aba(nome, ["objeto"] + cols, linhas)
    if coleta.get("rumo"):
        ks = list(coleta["rumo"][0].keys())
        aba("Rumo por código (calculado)", ks, [[r.get(k) for k in ks] for r in coleta["rumo"]])
    for d, t in (coleta.get("por_codigo") or {}).items():
        aba("Por código " + d, t["cols"], t["linhas"])
    if coleta.get("diferenca"):
        dif = coleta["diferenca"]
        aba("Diferença (calculado)", ["tipo", "chave", "antes", "agora"],
            [["OCI " + k, cod, v["antes"], v["agora"]] for cod, x in dif["ocis"].items() for k, v in x.items()]
            + [["exame", cod, v["antes"], v["agora"]] for cod, v in dif["exames"].items()]
            + [["fila", nm, v["fila_antes"], v["fila_agora"]] for nm, v in dif["filas"].items()])
    aba("Nomes internos", ["pedido", "exato"], [[p, "; ".join(ex)] for p, ex in coleta["nomes_internos"].items()])
    wb.save(arq)


# ------------------------------------------------------------------ a resposta
def resposta(coleta, md: Path) -> str:
    """o que o agente devolve ao lider, pronto: alarmes, datas, tabela curta, achados, lacunas"""
    d = coleta["datas"]
    L_ = [f"COLETA MONTADA — {md.name}", "", "ALARMES"]
    L_ += [f"  - {a['tipo']}" + (f" ({a['oci']})" if a.get("oci") else "") + f": {texto_alarme(a)}" for a in coleta["alarmes"]] or \
          (["  não se aplicam ao panorama"] if coleta["tipo"] == "panorama" else ["  nenhum"])
    L_ += ["", f"DATAS  recarga {d.get('recarga')} · consulta {d.get('consulta_inicio')} a {(d.get('consulta_fim') or '')[11:]} · "
               f"solicitação mais recente {d.get('solicitacao_mais_recente')}", ""]
    if coleta["ocis"]:
        L_ += ["OCI          finalidade (viva)      teto (viva)            núcleo (viva)"]
        for cod, x in coleta["ocis"].items():
            L_.append(f"  {cod}  {n(x['finalidade']['pessoas'])} ({n(x['finalidade']['pessoas_viva'])})".ljust(38)
                      + f"{n(x['teto']['pessoas'])} ({n(x['teto']['pessoas_viva'])})".ljust(23)
                      + f"{n(x['nucleo']['pessoas'])} ({n(x['nucleo']['pessoas_viva'])}) {x['nucleo']['como'] or ''}")
    for cod, e in coleta["exames"].items():
        u = e["uniao"]
        L_.append(f"  {cod} {bonito(e['nome'])}: {n(u['pessoas'])} pessoas ({n(u['pessoas_viva'])} na viva), fila {n(u['fila'])}, "
                  f"espera média {d1(u['espera_media'])} dias, {len(e['filas'])} fila(s)")
    for rot, p in coleta["panorama"].items():
        tot = p.get("total") or {}
        L_.append(f"  {rot}: {len(p['filas'])} filas; fila {n(tot.get('fila'))} ({n(tot.get('fila_viva'))} na viva), pessoas {n(tot.get('pessoas'))}")
    if coleta.get("rumo"):
        L_.append(f"  rumo por código: {len(coleta['rumo'])} códigos, com {', '.join(coleta['por_codigo'])} (seção Rumo por código)")
    if coleta["tipo"] == "panorama":
        L_ += ["", "LACUNAS"] + ([f"  - {bonito(x['onde'])}: {bonito(x['motivo'])}" for x in coleta["lacunas"]] or ["  nenhuma"])
        return "\n".join(L_)
    no_cid = lambda v: max([q for k, q in v["por_objeto"].items() if k.endswith("cid aceito") and q is not None] or [0])
    achados = sorted((v for v in coleta["varredura"] if v["no_resumo"] and not v["no_enquadramento"] and not v["na_ordem"]
                      and ((v["fila"] or 0) > 0 or v["tabela"] == "ag")), key=lambda v: (-no_cid(v), -(v["fila"] or 0), v["nome"]))
    L_ += ["", f"ACHADOS FORA DO ENQUADRAMENTO ({len(achados)}), a decidir:"]
    L_ += [f"  - {bonito(v['nome'])} ({v['codigo']}, {'só agendamentos' if v['tabela'] == 'ag' else 'solicitações'}): "
           + (f"fila {n(v['fila'])}, pessoas {n(v['pessoas'])}" if v["tabela"] == "sol" else f"agendadas 12 m {n(v['agendadas_12m'])}")
           + (f", {n(no_cid(v))} no CID aceito ({pct(v['parte_cid'], 1)})" if v["parte_cid"] is not None else "")
           + f"; achada por {', '.join(POR.get(p, p) for p in v['por'])}" + (" (genérica)" if v["generica"] else "") for v in achados[:40]]
    if len(achados) > 40:
        L_.append(f"  ... e mais {len(achados) - 40}: a lista inteira está na seção Varredura das filas")
    # as filas que o enquadramento deixou a decidir tambem vao ao lider: sao decisao aberta dele
    # (gauntlet, rodada 2: a TC de cranio de emergencia so aparecia no .md)
    abertas = sorted((v for v in coleta["varredura"] if v["no_enquadramento"] and v["decisao"] == "a decidir"
                      and v["tabela"] == "sol" and (v["fila"] or 0) > 0 and not v["na_ordem"]),
                     key=lambda v: (-(v["fila"] or 0), v["nome"]))
    if abertas:
        L_ += ["", f"A DECIDIR NO ENQUADRAMENTO ({len(abertas)}):"]
        L_ += [f"  - {bonito(v['nome'])} ({v['codigo']}): fila {n(v['fila'])}, pessoas {n(v['pessoas'])}; {bonito(v['motivo'])}"
               for v in abertas[:20]]
        if len(abertas) > 20:
            L_.append(f"  ... e mais {len(abertas) - 20}: a lista inteira está na seção Varredura das filas")
    resto = [v for v in coleta["varredura"] if not v["no_resumo"]]
    if resto:
        L_.append(f"  ({len(resto)} filas achadas só pelo CID, com menos de {C.LIM_VARREDURA:.0%} dos pedidos no CID: no JSON e na planilha)")
    L_ += ["", "LACUNAS"] + ([f"  - {bonito(x['onde'])}: {bonito(x['motivo'])}" for x in coleta["lacunas"]] or ["  nenhuma"])
    return "\n".join(L_)


# ------------------------------------------------------------------- gravar
def nome_da_coleta(bruto: Path) -> str:
    return bruto.name[:-len("_bruto")] if bruto.name.endswith("_bruto") else bruto.name


def montar_pasta(bruto: Path, anterior: Path | None = None, xlsx: bool = True):
    bruto = Path(bruto).resolve()
    data = L.data_da_pasta(bruto)
    ordem = json.loads((bruto / "ordem.json").read_text(encoding="utf-8"))
    faltas = validar_ordem(ordem, plano_da_pasta(bruto))
    if faltas:
        raise L.ErroMotor("a ordem esta incompleta: " + "; ".join(faltas))
    motor_arq = bruto / f"motor_{data}.json"
    if not motor_arq.exists():
        raise L.ErroMotor(f"sem {motor_arq.name}: rode antes o ferramentas/ler_motor.py")
    motor = json.loads(motor_arq.read_text(encoding="utf-8"))
    coleta = montar(motor, ordem, entradas_de(bruto, anterior))
    nome = nome_da_coleta(bruto)
    textos = {f"coleta_{data}.json": json.dumps(coleta, ensure_ascii=False, indent=1) + "\n",
              f"../{nome}.md": renderizar_md(coleta),
              "README.md": renderizar_readme(coleta, f"{nome}.md", data)}
    for rel, texto in textos.items():
        (bruto / rel).write_text(texto, encoding="utf-8")
    textos[motor_arq.name] = motor_arq.read_text(encoding="utf-8")
    montagem = {"montador": MONTADOR, "arquivos": {rel: L.djb2(t) for rel, t in sorted(textos.items())}}
    (bruto / "montagem.json").write_text(json.dumps(montagem, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    md = bruto.parent / f"{nome}.md"
    if xlsx:
        gravar_xlsx(coleta, bruto.parent / f"{nome}.xlsx")
    return coleta, md


def main():
    ap = argparse.ArgumentParser(description="monta a coleta do Mapa Social a partir do JSON do motor")
    ap.add_argument("bruto", help="a pasta bruta da coleta (mapa_social_AAAAMMDD_bruto/)")
    ap.add_argument("--ordem", action="store_true", help="so confere a ordem e imprime a forma que vai para o kit")
    ap.add_argument("--anterior", help="a coleta anterior (coleta_AAAAMMDD.json), se nao for a mais recente da pasta")
    args = ap.parse_args()
    saida_utf8()
    bruto = Path(args.bruto).resolve()
    if args.ordem:
        arq = bruto / "ordem.json"
        if not arq.exists():
            print(f"FALTA: {bruto.name}/ sem a ordem.json (o lider grava a ordem antes de chamar o agente)")
            return 1
        ordem = json.loads(arq.read_text(encoding="utf-8"))
        faltas = validar_ordem(ordem, plano_da_pasta(bruto))
        if faltas:
            print("ORDEM INCOMPLETA: pare e devolva ao lider o que falta:")
            print("\n".join(f"  - {f}" for f in faltas))
            return 1
        print(f"ordem completa ({ordem['tipo']}); hash {L.hash_ordem(ordem)}. Para o kit:")
        print(f"__ms.rodar({forma_do_kit(ordem)})")
        return 0
    try:
        coleta, md = montar_pasta(bruto, Path(args.anterior).resolve() if args.anterior else None)
    except L.ErroMotor as e:
        print(f"FALHOU: {e}")
        return 1
    print(resposta(coleta, md))
    print(f"\nARQUIVOS  {md}\n          {md.with_suffix('.xlsx')}\n          {bruto}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
