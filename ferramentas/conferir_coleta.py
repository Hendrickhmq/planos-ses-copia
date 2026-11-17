#!/usr/bin/env python3
"""
conferir_coleta.py - confere uma coleta do Mapa Social contra o metodo.

Uso:
    python3 conferir_coleta.py planos/redacao_NN/dados/fontes/mapa_social_AAAAMMDD.md

O metodo e metodo/coleta/mapa_social.md. Esta conferencia nao recalcula a fila: diz
se a coleta traz o que o documento precisa para citar o numero (fonte, datas, medida),
se o resumo mostra o que o numero esconde (os alarmes) e se nenhum dado pessoal saiu
do painel.

AS VERIFICACOES
  A  FONTE        o painel do Mapa Social (MPDFT) nomeado
  B  DATAS        recarga da base, hora da consulta e solicitacao mais recente, com data
  C  MEDIDA       a fila pelos tres status, com as devolvidas fora e ditas
  D  CONTEUDO     pessoas e Regiao de Saude
  E  BRUTO        a pasta <nome>_bruto/ com o JSON do motor e o script; o JSON guarda o
                  enquadramento (a medida da fila e os nomes internos exatos das filas)
  F  PRIVACIDADE  nenhum CPF nem CNS no .md nem na pasta bruta
  G  VARREDURA    uma secao com todas as filas que o objeto atende e a decisao de cada
                  uma (regra do usuario, 09/10/2026)
  H  ALARMES      refeitos pelo JSON (CID largo, CID dominante, CID raro, fila velha,
                  estoque, fila generica), cada um na secao "Alarmes" do resumo
  I  TRES NUMEROS na OCI, a tabela com teto, finalidade e nucleo, inteira e viva, com os
                  numeros do JSON
  J  ORDEM        a ordem.json na pasta bruta, completa, igual a que o kit rodou (hash), e
                  cada objeto, dimensao e universo pedido com numero ou lacuna com motivo
  K  MONTADO      o .md, o README, o JSON da coleta e o do motor sao os que os scripts
                  gravaram (montagem.json); na mesma versao do montador, a coleta se refaz
                  inteira das partes que sairam do navegador e tem de dar o mesmo texto

H e I valem para as coletas a partir de 25/10/2026; nas anteriores, nao se aplicam, e no
panorama tambem nao (nao ha objeto). J e K valem para as coletas a partir de 27/10/2026 e
para as que tem a ordem.json na pasta bruta (o contrato da ordem).

Codigo 1 se alguma falhar.
"""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

from comum import saida_utf8, sem_acento

DATA = r"\d{2}/\d{2}/\d{4}"
CPF = re.compile(r"(?<![\d.])\d{3}\.\d{3}\.\d{3}-\d{2}(?![\d])")
# CNS: quinze digitos, comecando por 1, 2, 7, 8 ou 9; fora de numero decimal
CNS = re.compile(r"(?<![\d.,])[12789]\d{14}(?![\d])")

# os alarmes (metodo/coleta/mapa_social.md, "Os alarmes"); limites propostos em 25/10/2026
DESDE_ALARMES = "20261025"
# a ordem de coleta, o kit e o montador (metodo/coleta/mapa_social.md, "Quem faz o que")
DESDE_ORDEM = "20261027"
LIM_DOMINANTE, LIM_RARO, LIM_VELHA, LIM_ESTOQUE, LIM_CATEGORIAS = 0.30, 0.05, 0.30, 3, 20
# a fila achada so pelo CID vai ao resumo quando o CID do objeto e esta parte dos pedidos dela;
# as outras ficam no JSON e na planilha (prova de 26/10/2026: J30-J39 em 120 filas, 34 acima de 5%)
LIM_VARREDURA = 0.05
# a fila pedida para muitos fins (regra 4 do enquadramento); o JSON marca, e esta lista
# apanha a que ele esquecer de marcar
GENERICAS = re.compile(r"ELETROCARDIOGRAMA|HOLTER|ECOCARDIOGRA(?:FIA|MA)(?!.*(?:ESTRESSE|TRANSESOF))|"
                       r"^\W*(?:RX|RAIO.?X|RADIOGRAFIA)?\s*(?:DE\s+)?TORAX\b|HEMOGRAMA|"
                       r"^CONSULTA\b.*-\s*(?:ADULTO|GERAL)\s*$")
CODIGO_OCI = re.compile(r"\b09\.\d{2}\.\d{2}\.\d{3}-\d\b")


def _norm(nome: str) -> str:
    return re.sub(r"\s+", " ", sem_acento(nome.replace("\u00a0", " "))).strip().upper()


def tokens(expr: str):
    """os valores de uma expressao de CID: 'codigo_cid_solicitado={"I20*","Z136"}' -> ['I20*', 'Z136']"""
    return [t.upper() for t in re.findall(r"[\"']([A-Za-z0-9*]+)[\"']", expr or "")]


def categorias(expr: str) -> int:
    """quantas categorias de CID (tres caracteres) a expressao cobre: 'I*' e o capitulo"""
    n = 0
    for t in tokens(expr):
        base = t.rstrip("*")
        n += 100 if t.endswith("*") and len(base) == 1 else 10 if t.endswith("*") and len(base) == 2 else 1
    return n


def dentro(cid: str, expr: str) -> bool:
    """a categoria esta na expressao (inteira ou em parte)"""
    cid = cid.upper()
    return any(cid.startswith(p) or p.startswith(cid) for p in (t.rstrip("*") for t in tokens(expr)))


def por_categoria(cid_principais):
    """[[cid, n], ...] somado pelos tres primeiros caracteres, do maior para o menor"""
    soma = {}
    for cid, n in cid_principais or []:
        c = re.sub(r"[^A-Z0-9]", "", str(cid).upper())[:3]
        soma[c] = soma.get(c, 0) + (n or 0)
    return sorted(soma.items(), key=lambda x: -x[1])


def _n(v) -> str:
    """o inteiro com o ponto do milhar: 50317 -> 50.317"""
    return f"{int(v):,}".replace(",", ".")


def generica(nome: str, fila: dict) -> bool:
    return bool(fila.get("generica")) or bool(GENERICAS.search(_norm(nome)))


def alarmes(dados: dict):
    """os alarmes que o JSON da coleta dispara: [{tipo, oci, fila, texto}]"""
    out = []
    filas = dados.get("filas") or {}
    ocis = dados.get("ocis") or {}

    def add(tipo, texto, oci=None, fila=None):
        out.append({"tipo": tipo, "oci": oci, "fila": fila, "texto": texto})

    def recorte(f, rotulo):
        return ((filas.get(f) or {}).get("recortes") or {}).get(rotulo) or {}

    for cod, o in ocis.items():
        aceito, fin = o.get("cid_aceito", ""), o.get("cid_finalidade", "") or o.get("cid_aceito", "")
        compos = o.get("filas") or []
        ncat = categorias(aceito)
        if any(t.endswith("*") and len(t) == 2 for t in tokens(aceito)) or ncat > LIM_CATEGORIAS:
            add("CID largo", f"{cod}: o CID aceito cobre {_n(ncat)} categorias", oci=cod)
        total = sum((filas.get(f) or {}).get("fila") or 0 for f in compos)
        na_fin = sum(recorte(f, o.get("recorte_finalidade")).get("fila") or 0 for f in compos)
        if total and na_fin / total < LIM_RARO:
            add("CID raro", f"{cod}: a finalidade pega {_n(na_fin)} de {_n(total)} solicitações das filas da composição", oci=cod)
        p = (o.get("finalidade") or {}).get("pessoas")
        pv = (o.get("finalidade") or {}).get("pessoas_viva")
        if p and pv is not None and (p - pv) / p > LIM_VELHA:
            add("fila velha", f"{cod}: {_n(p - pv)} de {_n(p)} pessoas da finalidade só têm pedido de antes da janela", oci=cod)
        if sorted(tokens(aceito)) != sorted(tokens(fin)):
            for f in compos:
                r = recorte(f, o.get("recorte_teto"))
                n = r.get("fila") or 0
                for cid, q in por_categoria(r.get("cid_principais")):
                    if n and q / n > LIM_DOMINANTE and not dentro(cid, fin):
                        add("CID dominante", f"{cid} em {q / n:.0%} de {f} no teto da {cod}", oci=cod, fila=f)
        for f in compos:
            if generica(f, filas.get(f) or {}):
                add("fila genérica", f"{f} na composição da {cod}", oci=cod, fila=f)

    # as filas do objeto: as da composicao das OCI e as dos exames avulsos (o montador de 27/10/2026
    # grava os dois na mesma coleta); sem OCI nem exame, todas as do JSON
    exames = dados.get("exames") if isinstance(dados.get("exames"), dict) else {}
    na_oci = {f for o in ocis.values() for f in (o.get("filas") or [])}
    alvo = sorted(na_oci | {f for e in exames.values() for f in (e.get("filas") or [])}) if ocis or exames else sorted(filas)
    for f in alvo:
        d = filas.get(f) or {}
        fila, ag = d.get("fila"), d.get("agendadas_12m")
        if fila and ag is not None and (ag == 0 or fila / ag > LIM_ESTOQUE):
            anos = "sem agendamento em 12 meses" if ag == 0 else f"{fila / ag:.1f} anos de agendamentos".replace(".", ",")
            add("estoque", f"{f}: {_n(fila)} na fila, {anos}", fila=f)
        if f not in na_oci and fila and d.get("fila_viva") is not None and (fila - d["fila_viva"]) / fila > LIM_VELHA:
            add("fila velha", f"{f}: {_n(fila - d['fila_viva'])} de {_n(fila)} pedidos de antes da janela", fila=f)
    return out


def formato_novo(dados) -> bool:
    """o JSON no formato de 25/10/2026: 'filas' com um objeto por nome de fila (o de 22/10/2026
    tambem tinha 'filas', mas por recorte e com listas)"""
    if not isinstance(dados, dict) or not isinstance(dados.get("filas"), dict):
        return False
    if not isinstance(dados.get("ocis", {}), dict):
        return False
    return all(isinstance(v, dict) for v in dados["filas"].values())


def secao_titulo(txt: str, padrao: str):
    """o corpo da secao cujo titulo casa com o padrao, ate o titulo seguinte do mesmo nivel ou acima"""
    m = re.search(r"^(#+)\s+.*(?:" + padrao + r").*$", txt, re.I | re.M)
    if not m:
        return None
    nivel = len(m.group(1))
    fim = re.search(r"^#{1,%d}\s" % nivel, txt[m.end():], re.M)
    return txt[m.end(): m.end() + fim.start()] if fim else txt[m.end():]


def inteiros(texto: str):
    return {int(x.replace(".", "")) for x in re.findall(r"\d{1,3}(?:\.\d{3})+|\d+", texto.replace("*", ""))}


def carregar_json(bruto: Path):
    # no contrato da ordem, o JSON da coleta e o coleta_<data>.json (o motor e a ordem ficam ao lado)
    for j in (sorted(bruto.glob("coleta_*.json")) + sorted(bruto.glob("*.json"))) if bruto.is_dir() else []:
        try:
            d = json.loads(j.read_text(encoding="utf-8"))
        except (ValueError, UnicodeDecodeError):
            continue
        if isinstance(d, dict) and ("filas" in d or "ocis" in d or "filtro_fila" in d):
            return d
    return None


def verificar(md: Path):
    txt = md.read_text(encoding="utf-8")
    baixo = txt.lower()
    itens = []

    def add(sigla, nome, falhas, na=False):
        itens.append((sigla, nome, not falhas, falhas, na))

    add("A", "fonte", [] if ("mapa social" in baixo and ("mpdft" in baixo or "paineis-ext.mpdft" in baixo))
        else ["o painel do Mapa Social (MPDFT) nao esta nomeado"])

    falhas = []
    for rotulo, pad in (("recarga da base", r"recar(?:ga|regad)[a-z]*[^\n]{0,80}?" + DATA),
                        ("hora da consulta", r"consulta[^\n]{0,80}?" + DATA),
                        ("solicitacao mais recente",
                         r"(mais recente|solicita[çc][õo]es at[ée])[^\n]{0,80}?" + DATA)):
        if not re.search(pad, txt, re.I):
            falhas.append(f"sem {rotulo} com data (dd/mm/aaaa)")
    add("B", "datas", falhas)

    falhas = []
    tres = (re.search(r"tr[êe]s status", baixo)
            or all(s in baixo for s in ("pendente de regula", "corrigida e reenviada", "fila de espera")))
    if not tres:
        falhas.append("a medida da fila nao diz os tres status")
    if "devolvid" not in baixo:
        falhas.append("as devolvidas nao sao ditas (fora da fila, contadas a parte)")
    add("C", "medida", falhas)

    falhas = [f"sem {x}" for x, pad in (("pessoas", r"pessoas"), ("Regiao de Saude", r"regi[ãa]o"))
              if not re.search(pad, baixo)]
    add("D", "conteudo", falhas)

    bruto = md.with_name(md.stem + "_bruto")
    data = re.search(r"(\d{8})", md.stem)
    # o contrato da ordem: o kit mede, os scripts montam, e a pasta bruta tem a ordem e as partes
    contrato = (bruto / "ordem.json").exists() or (bool(data) and data.group(1) >= DESDE_ORDEM)
    falhas = []
    if not bruto.is_dir():
        falhas.append(f"sem a pasta {bruto.name}/")
    else:
        jsons = list(bruto.glob("*.json"))
        if not jsons:
            falhas.append(f"{bruto.name}/ sem o JSON do motor")
        else:
            # a coleta seguinte parte do enquadramento gravado, nao do .md
            # (metodo/coleta/mapa_social.md, "As quatro regras do enquadramento")
            todo = " ".join(j.read_text(encoding="utf-8", errors="replace") for j in jsons)
            if '"filtro_fila"' not in todo:
                falhas.append(f"o JSON de {bruto.name}/ nao guarda a medida da fila (filtro_fila)")
            if '"nomes_internos"' not in todo and '"nome_sisreg"' not in todo:
                falhas.append(f"o JSON de {bruto.name}/ nao guarda os nomes internos das filas")
        if contrato:
            for pad, o_que in (("ordem.json", "a ordem de coleta"), ("motor_parte_*.txt", "as partes que sairam do navegador"),
                               ("motor_*.json", "o JSON do motor"), ("coleta_*.json", "o JSON da coleta"),
                               ("montagem.json", "o registro do montador"), ("README.md", "o README")):
                if not list(bruto.glob(pad)):
                    falhas.append(f"{bruto.name}/ sem {pad} ({o_que})")
        elif not list(bruto.glob("*.py")):
            falhas.append(f"{bruto.name}/ sem o script que monta a planilha")
    add("E", "pasta bruta", falhas)

    falhas = []
    arquivos = [md] + (sorted(p for p in bruto.rglob("*") if p.is_file() and p.suffix in
                                (".json", ".md", ".csv", ".txt", ".py")) if bruto.is_dir() else [])
    for arq in arquivos:
        conteudo = arq.read_text(encoding="utf-8", errors="replace")
        for nome, pad in (("CPF", CPF), ("CNS", CNS)):
            achados = pad.findall(conteudo)
            if achados:
                falhas.append(f"{len(achados)} possivel(is) {nome} em {arq.name}")
    add("F", "privacidade", falhas)

    # a varredura de todas as filas que o objeto atende, com a decisao de cada uma.
    # A coleta piloto de 08/10/2026 a chamou de "filas ... que ficam fora da soma".
    m = re.search(r"^#+ .*(varredura|fora da soma).*$", txt, re.I | re.M)
    add("G", "varredura das filas", [] if m else
        ["sem a secao de varredura: todas as filas que o objeto atende, com a decisao de cada uma"])

    # H e I: o numero do painel pode nao ser a fila do objeto (redacao_08, 22/10/2026: 50.317
    # pessoas com qualquer CID do capitulo I, e 7/7 nesta conferencia)
    antiga = bool(data) and data.group(1) < DESDE_ALARMES
    dados = None if antiga else carregar_json(bruto)
    panorama = (dados or {}).get("tipo") == "panorama"
    falhas = []
    if not antiga and not panorama:
        if not formato_novo(dados):
            falhas.append(f"o JSON de {bruto.name}/ nao traz 'filas' no formato do metodo de 25/10/2026 "
                          "(um objeto por nome de fila): sem ele os alarmes nao se refazem")
        else:
            sec = secao_titulo(txt, r"alarme")
            if sec is None:
                falhas.append("sem a secao 'Alarmes' (sem alarme, ela diz 'nenhum')")
            else:
                s = _norm(sec)
                vistos = set()
                for a in alarmes(dados):
                    chave = (a["tipo"], a["oci"])
                    if chave in vistos:
                        continue
                    vistos.add(chave)
                    if _norm(a["tipo"]) not in s or (a["oci"] and a["oci"][-5:] not in sec):
                        falhas.append(f"o alarme '{a['tipo']}' nao esta na secao Alarmes: {a['texto']}")
    add("H", "alarmes", falhas[:12], na=antiga or panorama)

    falhas = []
    ocis = (dados or {}).get("ocis") or {}
    ocis = ocis if isinstance(ocis, dict) else {}
    # a coleta e de OCI pelo JSON ou pelo titulo; a coleta de um exame avulso pode citar no texto
    # as OCI que usam o exame sem virar coleta de OCI
    titulo = next((l for l in txt.splitlines() if l.startswith("# ")), "")
    de_oci = bool(ocis) or bool(CODIGO_OCI.search(titulo)) or bool(re.search(r"\bOCIs?\b", titulo))
    na_i = antiga or not de_oci or panorama
    if not na_i:
        if not ocis:
            falhas.append("a coleta e de OCI e o JSON nao traz 'ocis' (teto, finalidade e nucleo)")
        else:
            linhas = txt.splitlines()
            cab = next((i for i, l in enumerate(linhas) if l.startswith("|") and
                        all(k in _norm(l) for k in ("TETO", "FINALIDADE", "NUCLEO", "VIVA"))), None)
            if cab is None:
                falhas.append("sem a tabela dos tres numeros (teto, finalidade, nucleo, com a viva)")
            else:
                corpo = []
                for l in linhas[cab + 2:]:
                    if not l.startswith("|"):
                        break
                    corpo.append(l)
                for cod, o in ocis.items():
                    linha = next((l for l in corpo if cod in l or cod[-5:] in l), None)
                    if linha is None:
                        falhas.append(f"{cod}: sem linha na tabela dos tres numeros")
                        continue
                    achados = inteiros(linha)
                    for numero in ("teto", "finalidade", "nucleo"):
                        for campo in ("pessoas", "pessoas_viva"):
                            v = (o.get(numero) or {}).get(campo)
                            if v is None:
                                falhas.append(f"{cod}: o JSON nao traz {numero}.{campo}")
                            elif v not in achados:
                                falhas.append(f"{cod}: {numero} {campo.replace('_', ' ')} {v} no JSON e nao na tabela")
    add("I", "tres numeros da OCI", falhas[:12], na=na_i)

    # J e K: a coleta e so fonte - o kit mediu o que a ordem pediu, e o texto e o que os
    # scripts gravaram (o teto de 22/10/2026 passou 7/7 porque o mesmo agente media e julgava)
    add("J", "ordem", (verificar_ordem(bruto, dados) if contrato else [])[:12], na=not contrato)
    add("K", "montado pelos scripts", (verificar_montado(md, bruto, dados) if contrato else [])[:12], na=not contrato)
    return itens


def verificar_ordem(bruto: Path, dados):
    import ler_motor as L
    import montar_coleta as M
    arq = bruto / "ordem.json"
    if not arq.exists():
        return ["sem a ordem.json na pasta bruta: a coleta nao diz o que lhe pediram"]
    ordem = json.loads(arq.read_text(encoding="utf-8"))
    falhas = [f"a ordem: {f}" for f in M.validar_ordem(ordem)]
    if falhas:
        return falhas
    if not dados:
        return ["sem o JSON da coleta (coleta_<data>.json)"]
    if dados.get("ordem_hash") != L.hash_ordem(ordem):
        falhas.append("a ordem.json nao e a que o kit rodou (o hash nao bate)")
    lacunas = [x for x in dados.get("lacunas") or [] if x.get("motivo")]
    lacuna = lambda chave: any(str(x.get("onde", "")).startswith(chave) for x in lacunas)
    dims_de = lambda alvo: (dados.get("dimensoes") or {}).get(alvo) or {}
    if ordem["tipo"] == "medicao":
        for o in ordem["objetos"]:
            q = o["id"]
            if o["tipo"] == "oci":
                x = (dados.get("ocis") or {}).get(q) or {}
                for num in ("teto", "finalidade", "nucleo"):
                    for campo in ("pessoas", "pessoas_viva"):
                        if (x.get(num) or {}).get(campo) is None and not lacuna(q):
                            falhas.append(f"{q}: sem {num} {campo.replace('_', ' ')} e sem lacuna com motivo")
            elif ((dados.get("exames") or {}).get(q) or {}).get("uniao", {}).get("pessoas") is None and not lacuna(q):
                falhas.append(f"{q}: sem as pessoas do exame e sem lacuna com motivo")
            for d in o.get("dimensoes") or ordem.get("dimensoes") or []:
                if d not in dims_de(q) and not lacuna(f"{q} {d}"):
                    falhas.append(f"{q}: a dimensao '{d}' foi pedida e nao veio, nem como lacuna")
    else:
        for u in ordem["universo"]:
            p = (dados.get("panorama") or {}).get(u["rotulo"])
            if p is None and not lacuna(u["rotulo"]):
                falhas.append(f"universo '{u['rotulo']}': sem as filas e sem lacuna com motivo")
            for d in ordem.get("dimensoes") or []:
                if p is not None and p.get("filas") and d not in (p.get("dimensoes") or {}) and not lacuna(f"{u['rotulo']} {d}"):
                    falhas.append(f"universo '{u['rotulo']}': a dimensao '{d}' foi pedida e nao veio, nem como lacuna")
        tem_filas = any((p or {}).get("filas") for p in (dados.get("panorama") or {}).values())
        for d in ordem.get("por_codigo") or []:
            if tem_filas and d not in (dados.get("por_codigo") or {}) and not lacuna(f"por codigo {d}"):
                falhas.append(f"por codigo: '{d}' foi pedido e nao veio, nem como lacuna")
    return falhas


def verificar_montado(md: Path, bruto: Path, dados):
    import ler_motor as L
    import montar_coleta as M
    reg_arq = bruto / "montagem.json"
    if not reg_arq.exists():
        return ["sem o montagem.json: a coleta nao foi gravada pelo montador (ferramentas/montar_coleta.py)"]
    reg = json.loads(reg_arq.read_text(encoding="utf-8"))
    falhas = []
    if f"../{md.name}" not in reg.get("arquivos", {}):
        falhas.append(f"o montador nao gravou {md.name}")
    for rel, h in sorted((reg.get("arquivos") or {}).items()):
        arq = bruto / rel
        if not arq.exists():
            falhas.append(f"{rel} nao existe")
        elif L.djb2(arq.read_text(encoding="utf-8")) != h:
            falhas.append(f"{arq.name} nao e o que o montador gravou: foi editado a mao "
                          "(refazer com ferramentas/ler_motor.py e ferramentas/montar_coleta.py)")
    if reg.get("montador") != M.MONTADOR or falhas or not dados:
        return falhas
    # na mesma versao do montador, a coleta inteira se refaz das partes que sairam do navegador
    try:
        motor = L.ler(bruto, conferir_kit=False)
    except L.ErroMotor as e:
        return [f"as partes da saida do navegador: {e}"]
    disco = json.loads((bruto / f"motor_{L.data_da_pasta(bruto)}.json").read_text(encoding="utf-8"))
    if motor != disco:
        return ["o JSON do motor nao e o que as partes dao"]
    ordem = json.loads((bruto / "ordem.json").read_text(encoding="utf-8"))
    refeita = json.loads(json.dumps(M.montar(disco, ordem, dados.get("entradas") or {}), ensure_ascii=False))
    if refeita != dados:
        return ["o JSON da coleta nao e o que o montador da a partir do motor e das entradas gravadas"]
    for texto, arq in ((M.renderizar_md(dados), md),
                       (M.renderizar_readme(dados, md.name, L.data_da_pasta(bruto)), bruto / "README.md")):
        atual = arq.read_text(encoding="utf-8")
        if texto != atual:
            n = next((i for i, (a, b) in enumerate(zip(texto.splitlines(), atual.splitlines()), 1) if a != b),
                     min(len(texto.splitlines()), len(atual.splitlines())) + 1)
            falhas.append(f"{arq.name} nao e o que o montador gera do JSON (primeira diferenca na linha {n})")
    return falhas


def main():
    ap = argparse.ArgumentParser(description="confere uma coleta do Mapa Social")
    ap.add_argument("coleta", help="o .md da coleta, por exemplo dados/fontes/mapa_social_20261006.md")
    args = ap.parse_args()
    saida_utf8()
    md = Path(args.coleta).resolve()
    if not md.exists():
        raise SystemExit(f"erro: {md} nao existe")
    itens = verificar(md)
    print(f"\nCONFERENCIA DA COLETA — {md.name}")
    print("=" * 78)
    for sigla, nome, ok, falhas, na in itens:
        print(f"  {sigla}  {nome:<46} {'NAO SE APLICA' if na else ('PASSOU' if ok else 'FALHOU')}")
        for x in falhas:
            print(f"        - {x}")
    print("=" * 78)
    n_ok = sum(1 for i in itens if i[2] and not i[4])
    n_na = sum(1 for i in itens if i[4])
    print(f"  {n_ok}/{len(itens) - n_na} verificacoes passaram"
          + (f" ({n_na} nao se aplicam)" if n_na else "") + "\n")
    return 0 if all(i[2] for i in itens) else 1


if __name__ == "__main__":
    sys.exit(main())
