#!/usr/bin/env python3
"""
conferir_precos.py - confere os precos do objeto de um plano contra o metodo.

Uso:
    python3 conferir_precos.py planos/redacao_NN/dados/precos.md

O metodo e metodo/coleta/precos.md. A conferencia nao pesquisa preco: diz se cada preco
tem fonte, endereco, data e local no DF, se o valor que a unidade recebe e o da Tabela
SUS Candanga (licao LI-002) e refaz o resumo e a conta.

AS VERIFICACOES
  A  CABECALHO   titulo, "controle interno", "Pesquisado em", origem do recurso, as 7 secoes
  B  VALOR       o valor recebido, em qualquer origem: o codigo da Candanga cita a Candanga
                 e bate com o Anexo, ou cita o SIGTAP da ficha quando ele e igual ou maior;
                 o codigo fora dela cita o SIGTAP, bate com a ficha (salvo incremento, que
                 cita a portaria) e diz que nao esta na Candanga. Pesquisa antes de
                 01/11/2026 segue a regra de entao: federal cita o SIGTAP e bate com a
                 ficha; distrital cita a Candanga
  C  SES-DF      o que a SES-DF paga: linhas com codigo, valor e fonte, ou "nada se achou";
                 cada codigo da secao 1 aparece na secao
  D  MERCADO     cada preco: codigo(s) da secao 1, componente, fonte, endereco (ou cotacao),
                 data, preco em reais e tipo; ao menos um preco por codigo, do DF ou de fora;
                 sem nome de profissional; a mesma fonte uma vez por componente e base
  E  LOCAL       cada preco no DF, ou marcado "fora do DF: <cidade>/<UF>"
  F  RESUMO      quantos, minimo, mediana e maximo de cada componente, por base (DF e fora
                 do DF), refeitos das linhas; "na conta" sim ou nao, igual nas duas bases; a
                 alternativa aponta para um componente que entra na conta
  G  CONTA       a soma dos componentes "na conta", com o DF e, so no componente sem preco
                 no DF, fora do DF (a coluna base diz qual); cobertura, oferta inicial,
                 teto e margem no teto, refeitos
  H  ATUALIDADE  nenhum preco com mais de 180 dias na data da pesquisa, nem depois dela
  I  APOIO       preco, fonte e data; tres orcamentos na locacao e no servico, ou
                 "pendente"; "Nao se aplica" no pre-plano
  J  APAC        nas pesquisas a partir de 25/10/2026: o minimo da APAC (os
                 obrigatorios e a consulta) e a cobertura APAC refeitos; a APAC num so
                 prestador de cada codigo; cada preco fraco da APAC minima marcado (um so
                 preco no DF, sem preco no DF, ou o minimo um "a partir de")

Codigo 1 se alguma falhar.
"""
from __future__ import annotations
import argparse, re, statistics, sys
from datetime import date, datetime
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

from comum import saida_utf8, sem_acento, valor_moeda
from conferir_ficha import linhas_da_tabela

SECOES = ["Valor que a unidade recebe", "O que a SES-DF paga", "Mercado privado",
          "Resumo do mercado", "A conta", "Apoio", "O que falta"]
TIPOS = {"fixo", "a partir de", "faixa mín", "faixa máx", "cotação"}
CANDANGA = Path(__file__).resolve().parent.parent / "biblioteca" / "precos" / "tabela_sus_candanga" / "tabela_sus_candanga.csv"
# a pesquisa desta data em diante usa a Candanga em qualquer origem (LI-002, 01/11/2026)
CANDANGA_PARA_TODOS = date(2026, 11, 1)
CODIGO = re.compile(r"\b\d{2}\.\d{2}\.\d{2}\.\d{3}-\d\b")
REAIS = re.compile(r"R\$\s*([\d.]+,\d{2})")
DIAS_MAX = 180
BASES = {"df", "fora do df"}
# a fonte e o estabelecimento ou a plataforma; o profissional nao se nomeia
PROFISSIONAL = re.compile(r"\b(Dr[a]?\.|Fonoaudi[oó]log[ao]|Fga?\.)\s+[A-ZÁÉÍÓÚ]|\bCRM[\s:]|\bCRFa\b")
# Regioes Administrativas e bairros do DF, sem acento
DF_LOCAIS = re.compile(
    r"\b(df|distrito federal|brasilia|plano piloto|asa sul|asa norte|lago sul|lago norte|sudoeste|"
    r"noroeste|octogonal|cruzeiro|guara|aguas claras|taguatinga|ceilandia|samambaia|recanto das emas|"
    r"riacho fundo|gama|santa maria|sobradinho|planaltina|paranoa|sao sebastiao|brazlandia|"
    r"nucleo bandeirante|candangolandia|park way|vicente pires|jardim botanico|itapoa|varjao|"
    r"estrutural|scia|sol nascente|por do sol|arapoanga|agua quente|sia)\b")


def chave(txt: str) -> str:
    return sem_acento(txt).lower().strip()


def secao(txt: str, n: int) -> str | None:
    """o corpo da secao '## n. Titulo', ou None"""
    m = re.search(rf"^## {n}\.[^\n]*\n([\s\S]*?)(?=^## \d+\.|\Z)", txt, re.M)
    return m.group(1) if m else None


def tabela(corpo: str | None):
    """[{coluna sem acento: celula}] da primeira tabela do corpo"""
    if not corpo:
        return []
    linhas = [l for l in corpo.splitlines() if l.strip().startswith("|")]
    if len(linhas) < 2:
        return []
    celulas = lambda l: [c.strip() for c in l.strip().strip("|").split("|")]
    cab = [chave(c) for c in celulas(linhas[0])]
    out = []
    for l in linhas[1:]:
        if re.match(r"^\|[-|: ]+\|$", l.strip()):
            continue
        cs = celulas(l)
        out.append(dict(zip(cab, cs + [""] * (len(cab) - len(cs)))))
    return out


def reais(celula: str):
    m = REAIS.search(celula or "")
    return valor_moeda(m.group(1)) if m else None


def dinheiro(x: float) -> float:
    return float(Decimal(str(x)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def parte(v: float, pct: float) -> float:
    """pct% de v, em centavos, arredondado como se arredonda dinheiro (em Decimal: o float
    de 393,55 x 0,7 da 275,48499... e arredondaria para baixo)"""
    x = Decimal(str(v)) * Decimal(str(pct)) / Decimal(100)
    return float(x.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def data_br(celula: str):
    m = re.search(r"\b(\d{2})/(\d{2})/(\d{4})\b", celula or "")
    if not m:
        return None
    try:
        return datetime.strptime(m.group(0), "%d/%m/%Y").date()
    except ValueError:
        return None


def percentual(txt: str, rotulo: str):
    """'Oferta inicial: 50%' -> 50.0; 'a definir' -> None; ausente -> False"""
    m = re.search(rf"{rotulo}:\s*(\d+(?:,\d+)?)\s*%", txt, re.I)
    if m:
        return float(m.group(1).replace(",", "."))
    return None if re.search(rf"{rotulo}[^\n·]*a definir", txt, re.I) else False


def tabela_candanga() -> dict:
    """codigo pontuado -> os valores do Anexo Unico, um por modalidade"""
    import csv
    out = {}
    with open(CANDANGA, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            out.setdefault(row["codigo_sigtap"], []).append(float(row["valor"]))
    return out


def valor_pela_origem(cod, v, fonte, origem, plano) -> list:
    """a regra de 09/10 a 31/10/2026: federal, o SIGTAP da ficha; distrital, a Candanga"""
    falhas = []
    if origem == "federal":
        if not re.search(r"SIGTAP", fonte) or re.search(r"Candanga", fonte, re.I):
            falhas.append(f"{cod}: emenda federal e a fonte nao e o SIGTAP (LI-002 ate 31/10/2026)")
        mf = re.search(r"`([^`]*sigtap_\d{10}_\d{6}\.md)`", fonte)
        if mf and not re.search(r"incremento", fonte, re.I):
            ficha = plano / mf.group(1)
            if not ficha.exists():
                falhas.append(f"{cod}: a ficha citada {mf.group(1)} nao existe")
            else:
                vf = valor_da_ficha(ficha)
                if vf is not None and abs(vf - v) > 0.005:
                    falhas.append(f"{cod}: R$ {v:.2f} aqui e R$ {vf:.2f} na ficha")
        elif re.search(r"incremento", fonte, re.I) and not re.search(r"(SAES|GM)\b[^|]*\d", fonte):
            falhas.append(f"{cod}: o incremento nao cita a portaria")
    elif origem == "distrital" and not re.search(r"Candanga|Delibera", fonte, re.I):
        falhas.append(f"{cod}: emenda distrital e a fonte nao e a Tabela SUS Candanga (LI-002 ate 31/10/2026)")
    return falhas


def valor_da_ficha(ficha: Path):
    tab = linhas_da_tabela(ficha.read_text(encoding="utf-8"))
    sa = next((v for k, v in tab.items() if re.search(r"servi[çc]o ambulatorial", k)), "")
    return reais(sa)


def verificar(md: Path, plano: Path | None = None):
    txt = md.read_text(encoding="utf-8")
    plano = plano or md.parent.parent
    itens = []

    def add(sigla, nome, falhas, na=False):
        itens.append((sigla, nome, not falhas, falhas, na))

    # A
    falhas = []
    if not re.search(r"^# Preços — \S", txt, re.M):
        falhas.append("o titulo nao e '# Preços — <objeto>'")
    if not re.search(r"controle interno", txt, re.I):
        falhas.append("sem a marca 'Controle interno: não vai ao documento'")
    pesquisa = None
    mp = re.search(r"Pesquisado em (\d{2}/\d{2}/\d{4})", txt)
    if not mp:
        falhas.append("sem 'Pesquisado em dd/mm/aaaa'")
    else:
        pesquisa = data_br(mp.group(1))
    mo = re.search(r"Origem do recurso:\s*(federal|distrital)\b", txt, re.I)
    if not mo:
        falhas.append("sem 'Origem do recurso: federal' ou 'distrital'")
    origem = mo.group(1).lower() if mo else None
    for n, titulo in enumerate(SECOES, 1):
        if secao(txt, n) is None:
            falhas.append(f"sem a secao '## {n}. {titulo}'")
    oferta, teto = percentual(txt, "Oferta inicial"), percentual(txt, "Teto")
    if oferta is False or teto is False:
        falhas.append("sem 'Oferta inicial: N%' e 'Teto: N%' (ou 'a definir')")
    add("A", "cabecalho", falhas)

    # B
    falhas, valores = [], {}
    candanga = tabela_candanga()
    linhas_1 = tabela(secao(txt, 1))
    if not linhas_1:
        falhas.append("a secao 1 nao traz nenhum codigo")
    antiga = pesquisa is not None and pesquisa < CANDANGA_PARA_TODOS
    for l in linhas_1:
        cod = (CODIGO.search(l.get("codigo", "")) or [None])[0]
        v = reais(l.get("valor", ""))
        fonte = l.get("fonte", "")
        if not cod or v is None:
            falhas.append(f"linha sem codigo ou sem valor em reais: {l.get('codigo', '')!r}")
            continue
        valores[cod] = v
        if antiga:
            falhas += valor_pela_origem(cod, v, fonte, origem, plano)
            continue
        na_candanga = candanga.get(cod)
        cita_candanga = bool(re.search(r"Candanga", fonte, re.I))
        mf = re.search(r"`([^`]*sigtap_\d{10}_\d{6}\.md)`", fonte)
        vf = None
        if mf:
            ficha = plano / mf.group(1)
            if not ficha.exists():
                falhas.append(f"{cod}: a ficha citada {mf.group(1)} nao existe")
            else:
                vf = valor_da_ficha(ficha)
        if na_candanga and cita_candanga and not re.search(r"SIGTAP", fonte):
            if not any(abs(c - v) <= 0.005 for c in na_candanga):
                falhas.append(f"{cod}: R$ {v:.2f} aqui e R$ "
                              + " ou R$ ".join(f"{c:.2f}" for c in na_candanga) + " na Candanga")
            continue
        if not re.search(r"SIGTAP", fonte):
            falhas.append(f"{cod}: a fonte nao e a Tabela SUS Candanga nem o SIGTAP (LI-002)")
            continue
        if na_candanga:
            if vf is None:
                falhas.append(f"{cod}: esta na Candanga e a fonte e o SIGTAP sem a ficha (LI-002)")
            elif vf < min(na_candanga) - 0.005:
                falhas.append(f"{cod}: esta na Candanga (R$ {min(na_candanga):.2f}), acima do "
                              f"SIGTAP da ficha (R$ {vf:.2f}); o valor e o da Candanga (LI-002)")
        elif not cita_candanga:
            falhas.append(f"{cod}: fora da Candanga, e a fonte nao diz isso (LI-002)")
        if vf is not None and not re.search(r"incremento", fonte, re.I) and abs(vf - v) > 0.005:
            falhas.append(f"{cod}: R$ {v:.2f} aqui e R$ {vf:.2f} na ficha")
        elif re.search(r"incremento", fonte, re.I) and not re.search(r"(SAES|GM)\b[^|]*\d", fonte):
            falhas.append(f"{cod}: o incremento nao cita a portaria")
    add("B", f"valor pela origem do recurso ({origem or '?'}), regra anterior a 01/11/2026" if antiga
        else "valor recebido pela Tabela SUS Candanga", falhas)

    # C
    corpo2 = secao(txt, 2) or ""
    linhas_2 = tabela(corpo2)
    falhas = []
    if not linhas_2 and not re.search(r"nada se achou|nenhum valor", corpo2, re.I):
        falhas.append("sem linhas e sem a frase de que nada se achou")
    for cod in valores:
        if cod not in corpo2:
            falhas.append(f"{cod}: a secao 2 nao diz nada deste codigo (uma linha, ou onde se procurou)")
    for l in linhas_2:
        if not l.get("valor") or not l.get("fonte"):
            falhas.append(f"linha sem valor ou sem fonte: {l.get('codigo', '')!r}")
        if not CODIGO.search(l.get("codigo", "")):
            falhas.append(f"linha sem codigo SIGTAP: {l.get('codigo', '')!r}")
    add("C", "o que a SES-DF paga", falhas)

    # D, E, H
    falhas_d, falhas_e, falhas_h, precos, fontes_vistas, tipos = [], [], [], [], set(), []
    for i, l in enumerate(tabela(secao(txt, 3)), 1):
        rot = f"linha {i}"
        # o componente comum a varias OCI se registra uma vez, com os codigos na mesma celula
        cods = CODIGO.findall(l.get("codigo", ""))
        tipo = chave(l.get("tipo", ""))
        if not cods or any(c not in valores for c in cods):
            falhas_d.append(f"{rot}: codigo {l.get('codigo', '')!r} nao esta na secao 1")
        cods = [c for c in cods if c in valores]
        for col in ("componente", "fonte"):
            if not l.get(col):
                falhas_d.append(f"{rot}: sem {col}")
        # so o nome do estabelecimento, antes do endereco: "Ed. Dr. Crispim" e rua, nao medico
        if PROFISSIONAL.search(l.get("fonte", "").split(",")[0]):
            falhas_d.append(f"{rot}: nome de profissional na fonte; a fonte e o estabelecimento")
        end = l.get("endereco", "")
        if tipo == "cotacao":
            if not end:
                falhas_d.append(f"{rot}: cotacao sem o documento")
        elif not re.match(r"https?://\S+", end.strip("<>` ")):
            falhas_d.append(f"{rot}: sem endereco http(s)")
        d = data_br(l.get("data", ""))
        if not d:
            falhas_d.append(f"{rot}: sem data dd/mm/aaaa")
        p = reais(l.get("preco", ""))
        if p is None:
            falhas_d.append(f"{rot}: sem preco em reais")
        if tipo not in {chave(t) for t in TIPOS}:
            falhas_d.append(f"{rot}: tipo {l.get('tipo', '')!r} fora de {sorted(TIPOS)}")
        local = chave(l.get("local", ""))
        fora = local.startswith("fora do df")
        if not fora and not DF_LOCAIS.search(local):
            falhas_e.append(f"{rot}: local {l.get('local', '')!r} nao e do DF nem esta marcado 'fora do DF'")
        if d and pesquisa:
            if d > pesquisa:
                falhas_h.append(f"{rot}: data {d:%d/%m/%Y} depois da pesquisa")
            elif (pesquisa - d).days > DIAS_MAX:
                falhas_h.append(f"{rot}: preco de {d:%d/%m/%Y}, mais de {DIAS_MAX} dias antes da pesquisa")
        # a faixa da mesma fonte da duas linhas, o minimo e o maximo
        for cod in cods:
            um = (cod, chave(l.get("componente", "")), fora, chave(l.get("fonte", "")),
                  tipo if tipo.startswith("faixa") else "")
            if um in fontes_vistas:
                falhas_d.append(f"{rot}: a mesma fonte repetida no mesmo componente de {cod}; fica o menor preco")
            fontes_vistas.add(um)
            if p is not None:
                precos.append((cod, chave(l.get("componente", "")), "fora do df" if fora else "df", p))
                tipos.append((cod, chave(l.get("componente", "")), "fora do df" if fora else "df", p, tipo))
    no_df = [x for x in precos if x[2] == "df"]
    for cod in valores:
        if not any(c == cod for c, *_ in precos):
            falhas_d.append(f"{cod}: nenhum preco de mercado")
    add("D", f"precos do mercado ({len(no_df)} no DF, {len(precos) - len(no_df)} fora)", falhas_d)
    add("E", "local no DF ou marcado fora do DF", falhas_e)
    add("H", f"atualidade (ate {DIAS_MAX} dias)", falhas_h, na=not precos)

    # F
    grupos = {}
    for cod, comp, base, p in precos:
        grupos.setdefault((cod, comp, base), []).append(p)
    resumo = {g: (len(ps), min(ps), statistics.median(ps), max(ps)) for g, ps in grupos.items()}
    falhas, vistos, na_conta, alternativas, marcas = [], set(), {}, set(), {}
    for l in tabela(secao(txt, 4)):
        cod = (CODIGO.search(l.get("codigo", "")) or [None])[0]
        comp, base = chave(l.get("componente", "")), chave(l.get("base", ""))
        rot = f"{l.get('codigo', '')} / {l.get('componente', '')} / {l.get('base', '')}"
        if base not in BASES:
            falhas.append(f"{rot}: base {l.get('base', '')!r}, e 'DF' ou 'fora do DF'")
            continue
        conta = chave(l.get("na conta", ""))
        ma = re.search(r"alternativa an?\s+(.+?)\)?\s*$", conta)
        if ma:
            alternativas.add((cod, comp, ma.group(1).strip()))
        marcas[(cod, comp)] = conta
        if not re.match(r"(sim|nao)\b", conta):
            falhas.append(f"{rot}: 'na conta' {l.get('na conta', '')!r}, e 'sim' ou 'não'")
        elif na_conta.setdefault((cod, comp), conta[:3]) != conta[:3]:
            falhas.append(f"{rot}: 'na conta' diferente entre o DF e fora do DF")
        g = (cod, comp, base)
        vistos.add(g)
        if g not in resumo:
            falhas.append(f"{rot}: sem preco desta base na secao 3")
            continue
        n, mn, md_, mx = resumo[g]
        lido = (re.sub(r"\D", "", l.get("precos", "")), reais(l.get("minimo", "")),
                reais(l.get("mediana", "")), reais(l.get("maximo", "")))
        if lido[0] != str(n):
            falhas.append(f"{rot}: {lido[0] or '?'} precos, as linhas dao {n}")
        for nome, esperado, achado in (("minimo", mn, lido[1]), ("mediana", md_, lido[2]), ("maximo", mx, lido[3])):
            if achado is None or abs(dinheiro(esperado) - achado) > 0.005:
                falhas.append(f"{rot}: {nome} {achado}, as linhas dao {dinheiro(esperado):.2f}")
    for g in resumo:
        if g not in vistos:
            falhas.append(f"{g[0]} / {g[1]} / {g[2]}: tem precos e nao esta no resumo")
    for cod in valores:
        if not any(c == cod and s == "sim" for (c, _), s in na_conta.items()):
            falhas.append(f"{cod}: nenhum componente com 'na conta: sim'")
    for cod, comp, outro in alternativas:
        if na_conta.get((cod, outro)) != "sim":
            falhas.append(f"{cod} / {comp}: alternativa a '{outro}', que nao esta no resumo com 'na conta: sim'")
    add("F", "resumo do mercado", falhas)

    # G
    falhas = []
    linhas_5 = {(CODIGO.search(l.get("codigo", "")) or [None])[0]: l for l in tabela(secao(txt, 5))}
    for cod, v in valores.items():
        l = linhas_5.get(cod)
        if not l:
            falhas.append(f"{cod}: sem linha na conta")
            continue
        comps = sorted(comp for (c, comp), s in na_conta.items() if c == cod and s == "sim")
        usados, bases = [], set()
        for comp in comps:
            r = resumo.get((cod, comp, "df")) or resumo.get((cod, comp, "fora do df"))
            if r:
                usados.append(r)
                bases.add("df" if (cod, comp, "df") in resumo else "fora do df")
        if not usados:
            continue
        rotulo = {frozenset({"df"}): "df", frozenset({"fora do df"}): "fora do df"}.get(
            frozenset(bases), "df e fora do df")
        if chave(l.get("base", "")) != rotulo:
            falhas.append(f"{cod}: base {l.get('base', '')!r}, a conta usa {rotulo.replace('df', 'DF')}")
        soma_min = dinheiro(sum(r[1] for r in usados))
        soma_med = dinheiro(sum(r[2] for r in usados))
        esperado = {"valor recebido": v, "mercado minimo": soma_min, "mercado mediana": soma_med}
        if oferta not in (None, False) and teto not in (None, False):
            t = parte(v, teto)
            esperado.update({"oferta inicial": parte(v, oferta), "teto": t,
                             "margem no teto": dinheiro(v - t)})
        else:
            for col in ("oferta inicial", "teto", "margem no teto"):
                if "a definir" not in l.get(col, "").lower():
                    falhas.append(f"{cod}: oferta e teto a definir no cabecalho, e '{col}' traz {l.get(col)!r}")
        for col, e in esperado.items():
            achado = reais(l.get(col, ""))
            if achado is None or abs(achado - e) > 0.005:
                falhas.append(f"{cod}: {col} {l.get(col, '')!r}, a conta da {e:.2f}")
        mc = re.search(r"(\d+)\s*%", l.get("cobertura", ""))
        cob = round(v / soma_min * 100) if soma_min else None
        if not mc or cob is None or abs(int(mc.group(1)) - cob) > 1:
            falhas.append(f"{cod}: cobertura {l.get('cobertura', '')!r}, a conta da {cob}%")
    add("G", "a conta", falhas)

    # J: o minimo da APAC, a APAC num so prestador e o preco fraco. O mercado minimo soma o
    # mais barato de cada lugar, e a cobertura de 105% da cintilografia do redacao_08 vinha
    # de um pacote de Sao Paulo e de um "a partir de" nacional (22/10/2026)
    falhas = []
    nova = bool(pesquisa) and pesquisa >= date(2026, 10, 25)
    if nova:
        linhas5_txt = sem_acento(secao(txt, 5) or "").lower().splitlines()

        def minimo(cod, comp):
            r = resumo.get((cod, comp, "df")) or resumo.get((cod, comp, "fora do df"))
            return r[1] if r else None

        def tipo_do_minimo(cod, comp, base):
            ps = sorted((p, t != "a partir de", t) for c, k, b, p, t in tipos if (c, k, b) == (cod, comp, base))
            return ps[0][2] if ps else None

        for cod, v in valores.items():
            sims = sorted(comp for (c, comp), s in na_conta.items() if c == cod and s == "sim")
            apac = [comp for comp in sims if re.search(r"obrigat|consulta", marcas.get((cod, comp), ""))]
            if not any("consulta" in marcas.get((cod, comp), "") for comp in sims):
                falhas.append(f"{cod}: nenhum componente com 'na conta: sim, consulta'")
            if len(apac) < 2:
                resto = sorted((minimo(cod, c), c) for c in sims if c not in apac and minimo(cod, c) is not None)
                apac += [c for _, c in resto[:2 - len(apac)]]
            mins = [minimo(cod, c) for c in apac]
            if not apac or None in mins:
                continue
            soma = dinheiro(sum(mins))
            l = linhas_5.get(cod) or {}
            achado = reais(l.get("minimo da apac", ""))
            if achado is None or abs(achado - soma) > 0.005:
                falhas.append(f"{cod}: minimo da APAC {l.get('minimo da apac', '')!r}, a conta da {soma:.2f} ({', '.join(apac)})")
            mc = re.search(r"(\d+)\s*%", l.get("cobertura apac", ""))
            cob = round(v / soma * 100) if soma else None
            if not mc or cob is None or abs(int(mc.group(1)) - cob) > 1:
                falhas.append(f"{cod}: cobertura APAC {l.get('cobertura apac', '')!r}, a conta da {cob}%")
            if not any(("num so prestador" in x or "nenhum prestador" in x) and (cod in x or cod[-5:] in x)
                       for x in linhas5_txt):
                falhas.append(f"{cod}: a secao 5 nao diz a APAC num so prestador")
            for comp in apac:
                rdf = resumo.get((cod, comp, "df"))
                motivo = ("sem preco no DF" if rdf is None else "um so preco no DF" if rdf[0] < 2 else
                          "o minimo e um 'a partir de'" if tipo_do_minimo(cod, comp, "df") == "a partir de" else None)
                if motivo and not any("preco fraco" in x and comp in x for x in linhas5_txt):
                    falhas.append(f"{cod}: {comp} ({motivo}) sem a marca de preco fraco na secao 5")
    add("J", "minimo da APAC e preco fraco", falhas[:12], na=not nova)

    # I
    corpo6 = secao(txt, 6) or ""
    if re.search(r"n[ãa]o se aplica", corpo6, re.I):
        add("I", "apoio", [], na=True)
    else:
        falhas = []
        linhas_6 = tabela(corpo6)
        if not linhas_6:
            falhas.append("sem linhas e sem 'Não se aplica'")
        for l in linhas_6:
            nome = l.get("posto ou servico", "")
            if reais(l.get("preco", "")) is None and "pendente" not in l.get("preco", "").lower():
                falhas.append(f"{nome}: sem preco em reais")
            if not l.get("fonte"):
                falhas.append(f"{nome}: sem fonte")
            if not data_br(l.get("data", "")):
                falhas.append(f"{nome}: sem data")
            if re.search(r"loca[çc][ãa]o|aluguel|servi[çc]o", nome, re.I):
                fontes = [f for f in re.split(r";", l.get("fonte", "")) if f.strip()]
                if len(fontes) < 3 and "pendente" not in l.get("fonte", "").lower():
                    falhas.append(f"{nome}: {len(fontes)} orcamento(s), sao tres (LI-021)")
        add("I", "apoio", falhas)

    ordem = "ABCDEFGHIJ"
    return sorted(itens, key=lambda i: ordem.index(i[0]))


def main():
    ap = argparse.ArgumentParser(description="confere os precos do objeto de um plano")
    ap.add_argument("precos", help="planos/redacao_NN/dados/precos.md")
    args = ap.parse_args()
    saida_utf8()
    md = Path(args.precos).resolve()
    if not md.exists():
        raise SystemExit(f"erro: {md} nao existe")
    itens = verificar(md)
    print(f"\nCONFERENCIA DOS PRECOS — {md.parent.parent.name}/{md.parent.name}/{md.name}")
    print("=" * 78)
    for sigla, nome, ok, falhas, na in itens:
        print(f"  {sigla}  {nome:<46} {'NAO SE APLICA' if na else ('PASSOU' if ok else 'FALHOU')}")
        for x in falhas:
            print(f"        - {x}")
    print("=" * 78)
    n_ok = sum(1 for i in itens if i[2] and not i[4])
    print(f"  {n_ok}/{len(itens)} verificacoes passaram\n")
    return 0 if all(i[2] for i in itens) else 1


if __name__ == "__main__":
    sys.exit(main())
