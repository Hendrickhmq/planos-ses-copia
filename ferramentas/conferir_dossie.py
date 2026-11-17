#!/usr/bin/env python3
"""
conferir_dossie.py - confere o dossie do objeto de um plano contra o metodo.

Uso:
    python3 conferir_dossie.py planos/redacao_NN/dossie/

O metodo e metodo/coleta/dossie.md. A conferencia nao escolhe o objeto: diz se cada
pagina tem as seis partes com fonte, se os numeros batem com a ficha, a coleta e os
precos, se a conta e o comparativo estao certos e se a justificativa publica nao fala
do que se recebe nem do que se paga.

AS VERIFICACOES
  A  PASTA          comparativo (ponto de partida, recurso e origem, apoio, data), uma
                    pagina por OCI do comparativo, a justificativa
  B  PARTES         as seis partes; a ficha, a coleta e o precos.md citados existem, e o
                    numero de pessoas esta na coleta; na coleta de 25/10/2026 em diante, ele
                    e a finalidade (inteira ou viva, como a 'medida' diz) e os alarmes da
                    OCI estao na linha 'alarmes'
  C  VALOR          o da Tabela SUS Candanga, em qualquer origem, e a parte 3 a cita; o
                    da ficha quando o SIGTAP e igual ou maior, ou o codigo esta fora dela.
                    Comparativo montado antes de 01/11/2026: o da ficha na emenda federal;
                    a Tabela SUS Candanga na distrital
  D  CUSTO          mercado minimo, mediana, cobertura (e a do minimo da APAC, quando o
                    precos.md a tem) e margem no teto iguais aos do dados/precos.md
  E  CONTA          piso de (recurso - apoio) / valor; o menor entre as OCI e as pessoas;
                    a parte da fila; a sobra do recurso depois de atender
  F  COMPARATIVO    igual as paginas, na ordem da cobertura (e do valor no empate)
  G  JUSTIFICATIVA  sem reais, margem, mercado, oferta, teto, cobertura, plataforma de
                    preco nem codigo do metodo (LI-, AC-...); com a fonte da fila; sem o
                    numero do teto quando ele passa da finalidade
  H  INTERNO        a marca de controle interno no comparativo e nas paginas, e nao na
                    justificativa

Codigo 1 se alguma falhar.
"""
from __future__ import annotations
import argparse, re, sys
from decimal import Decimal
from pathlib import Path

from comum import saida_utf8
from conferir_coleta import alarmes, carregar_json, formato_novo, inteiros, _norm
from conferir_precos import (CANDANGA_PARA_TODOS, CODIGO, chave, data_br, reais, secao, tabela,
                             tabela_candanga, valor_da_ficha)

PARTES = ["Ficha", "Fila", "Normas", "Aprovados", "Custo de executar", "A conta"]
# "Oferta de Cuidados Integrados" e o nome da OCI; os codigos do metodo ficam fora do documento
# (comum, regra 12)
PROIBIDO = re.compile(r"R\$|\bmargem|\bmercado|\boferta(?!s? de cuidados? integrad)|\bteto\b|\bcobertura|"
                      r"doctoralia|medprev|amorsa[uú]de|dr\.?\s?consulta|\blucr|\brentab|paga melhor|"
                      r"\bpre[çc]os?\b|\b(?:LI|AC|DV|NM|CT|OB|DD|EX|L)-\d{3}\b", re.I)


def pares(corpo: str | None):
    """{rotulo sem acento: valor} das linhas | rotulo | valor | de uma secao"""
    out = {}
    for l in (corpo or "").splitlines():
        m = re.match(r"^\|\s*([^|]+?)\s*\|\s*(.+?)\s*\|\s*$", l)
        if m and not set(m.group(1)) <= set("-: "):
            out.setdefault(chave(m.group(1)), m.group(2).strip())
    return out


def inteiro(celula: str):
    d = re.sub(r"\D", "", (celula or "").split("%")[0])
    return int(d) if d else None


def caminho(celula: str):
    m = re.search(r"`([^`]+)`", celula or "")
    return m.group(1) if m else None


def verificar(pasta: Path):
    plano = pasta.parent
    itens = []

    def add(sigla, nome, falhas, na=False):
        itens.append((sigla, nome, not falhas, falhas, na))

    comp_md, just_md = pasta / "comparativo.md", pasta / "justificativa.md"
    comp = comp_md.read_text(encoding="utf-8") if comp_md.exists() else ""
    just = just_md.read_text(encoding="utf-8") if just_md.exists() else ""

    # A
    falhas = []
    if not comp:
        falhas.append("sem dossie/comparativo.md")
    if not just:
        falhas.append("sem dossie/justificativa.md")
    mp = re.search(r"Ponto de partida:\s*(escolher a fila|dada a fila)", comp, re.I)
    mr = re.search(r"Recurso:\s*R\$\s*([\d.]+,\d{2}),\s*(federal|distrital)", comp, re.I)
    ma = re.search(r"Apoio:\s*R\$\s*([\d.]+,\d{2})", comp)
    if comp and not mp:
        falhas.append("o comparativo nao diz o ponto de partida ('escolher a fila' ou 'dada a fila')")
    if comp and not mr:
        falhas.append("o comparativo nao diz 'Recurso: R$ <valor>, federal' (ou distrital)")
    if comp and not ma:
        falhas.append("o comparativo nao diz 'Apoio: R$ <valor>'")
    if comp and not re.search(r"Montado em \d{2}/\d{2}/\d{4}", comp):
        falhas.append("o comparativo nao diz 'Montado em dd/mm/aaaa'")
    recurso = reais("R$ " + mr.group(1)) if mr else None
    origem = mr.group(2).lower() if mr else None
    apoio = reais("R$ " + ma.group(1)) if ma else None
    linhas_c = [l for l in tabela(comp) if CODIGO.search(l.get("codigo", ""))]
    codigos = [CODIGO.search(l["codigo"]).group(0) for l in linhas_c]
    paginas = {}
    for cod in codigos:
        arq = pasta / (re.sub(r"\D", "", cod) + ".md")
        if not arq.exists():
            falhas.append(f"{cod}: sem a pagina {arq.name}")
        else:
            paginas[cod] = arq.read_text(encoding="utf-8")
    for arq in sorted(pasta.glob("[0-9]" * 10 + ".md")):
        if not any(re.sub(r"\D", "", c) == arq.stem for c in codigos):
            falhas.append(f"{arq.name}: pagina sem linha no comparativo")
    add("A", f"pasta ({len(paginas)} OCI)", falhas)

    # B, C, D, E: pagina a pagina
    fb, fc, fd, fe, dados, tetos = [], [], [], [], {}, {}
    candanga = tabela_candanga()
    mm = re.search(r"Montado em (\d{2}/\d{2}/\d{4})", comp or "")
    montado = data_br(mm.group(1)) if mm else None
    antiga = montado is not None and montado < CANDANGA_PARA_TODOS
    precos_md = plano / "dados" / "precos.md"
    conta_precos = {}
    if precos_md.exists():
        for l in tabela(secao(precos_md.read_text(encoding="utf-8"), 5)):
            mc = CODIGO.search(l.get("codigo", ""))
            if mc:
                conta_precos[mc.group(0)] = l
    for cod, txt in paginas.items():
        partes = {}
        for n, nome in enumerate(PARTES, 1):
            corpo = secao(txt, n)
            if corpo is None or not corpo.strip():
                fb.append(f"{cod}: sem a parte '## {n}. {nome}'")
            partes[n] = pares(corpo)
        p1, p2, p5, p6 = partes[1], partes[2], partes[5], partes[6]

        valor = reais(p1.get("valor", ""))
        ficha = caminho(p1.get("fonte", ""))
        if not ficha or not (plano / ficha).exists():
            fb.append(f"{cod}: a ficha citada na parte 1 nao existe ({ficha})")
            ficha = None
        coleta = caminho(p2.get("fonte", ""))
        pessoas_txt = p2.get("pessoas que se enquadram", "")
        pessoas = inteiro(pessoas_txt)
        if not coleta or not (plano / coleta).exists():
            fb.append(f"{cod}: a coleta citada na parte 2 nao existe ({coleta})")
        elif pessoas is None:
            fb.append(f"{cod}: a parte 2 nao diz as pessoas que se enquadram")
        elif re.sub(r"\*", "", pessoas_txt).strip() not in (plano / coleta).read_text(encoding="utf-8"):
            fb.append(f"{cod}: {pessoas_txt} pessoas nao aparece na coleta {coleta}")
        # na coleta de 25/10/2026 em diante, a fila da pagina e a finalidade, e os alarmes
        # da OCI vao junto (redacao_08: o teto de 50.317 virou a fila da pagina)
        jc = carregar_json((plano / coleta).with_name(Path(coleta).stem + "_bruto")) if coleta else None
        jc = jc if formato_novo(jc) else None
        oci = ((jc or {}).get("ocis") or {}).get(cod)
        if oci and pessoas is not None:
            viva = "viva" in chave(p2.get("medida", ""))
            fin = (oci.get("finalidade") or {}).get("pessoas_viva" if viva else "pessoas")
            if fin is not None and pessoas != fin:
                teto = (oci.get("teto") or {}).get("pessoas")
                fb.append(f"{cod}: {pessoas} pessoas na pagina e {fin} na finalidade da coleta"
                          + (" (o numero da pagina e o teto)" if pessoas == teto else ""))
            dela = [a for a in alarmes(jc) if a["oci"] == cod or (a["oci"] is None and a["fila"] in (oci.get("filas") or []))]
            linha = _norm(p2.get("alarmes", ""))
            for tipo in sorted({a["tipo"] for a in dela}):
                if _norm(tipo) not in linha:
                    fb.append(f"{cod}: o alarme '{tipo}' da coleta nao esta na linha 'alarmes' da parte 2")
            teto_p = (oci.get("teto") or {}).get("pessoas")
            fin_p = (oci.get("finalidade") or {}).get("pessoas")
            if teto_p and fin_p is not None and teto_p > fin_p:
                tetos[cod] = teto_p
        if caminho(p5.get("fonte", "")) != "dados/precos.md" or not precos_md.exists():
            fb.append(f"{cod}: a parte 5 nao cita dados/precos.md, ou ele nao existe")

        # C
        if valor is None:
            fc.append(f"{cod}: a parte 1 nao traz o valor em reais")
        elif antiga:
            if origem == "federal" and ficha:
                vf = valor_da_ficha(plano / ficha)
                if vf is not None and abs(vf - valor) > 0.005:
                    fc.append(f"{cod}: R$ {valor:.2f} na pagina e R$ {vf:.2f} na ficha")
            elif origem == "distrital" and not re.search(r"Candanga", secao(txt, 3) or "", re.I):
                fc.append(f"{cod}: emenda distrital e a parte 3 nao cita a Tabela SUS Candanga (LI-002 ate 31/10/2026)")
        else:
            vf = valor_da_ficha(plano / ficha) if ficha and (plano / ficha).exists() else None
            na_candanga = candanga.get(cod)
            if na_candanga:
                certos = list(na_candanga)
                if vf is not None and vf >= min(na_candanga) - 0.005:
                    certos.append(vf)
                if not any(abs(c - valor) <= 0.005 for c in certos):
                    fc.append(f"{cod}: R$ {valor:.2f} na pagina e R$ "
                              + " ou R$ ".join(f"{c:.2f}" for c in certos)
                              + " pela Candanga (LI-002)")
                if not re.search(r"Candanga", secao(txt, 3) or "", re.I):
                    fc.append(f"{cod}: a parte 3 nao cita a Tabela SUS Candanga (LI-002)")
            elif vf is not None and abs(vf - valor) > 0.005:
                fc.append(f"{cod}: R$ {valor:.2f} na pagina e R$ {vf:.2f} na ficha")

        # D
        lp = conta_precos.get(cod)
        margem = None
        if not lp:
            fd.append(f"{cod}: sem linha na conta de dados/precos.md")
        else:
            for rot in ("mercado minimo", "mercado mediana", "margem no teto"):
                a, b = p5.get(rot, ""), lp.get(rot, "")
                if (reais(a), "a definir" in a.lower()) != (reais(b), "a definir" in b.lower()):
                    fd.append(f"{cod}: {rot} {a!r} aqui e {b!r} no precos.md")
            if inteiro(p5.get("cobertura", "")) != inteiro(lp.get("cobertura", "")):
                fd.append(f"{cod}: cobertura {p5.get('cobertura')!r} aqui e {lp.get('cobertura')!r} no precos.md")
            if lp.get("cobertura apac") and inteiro(p5.get("cobertura (minimo da apac)", "")) != inteiro(lp["cobertura apac"]):
                fd.append(f"{cod}: cobertura pelo minimo da APAC {p5.get('cobertura (minimo da apac)')!r} aqui"
                          f" e {lp['cobertura apac']!r} no precos.md")
            margem = reais(p5.get("margem no teto", ""))

        # E
        r6, a6 = reais(p6.get("recurso", "")), reais(p6.get("apoio", ""))
        sobra = reais(p6.get("sobra do recurso", ""))
        qtd, atend, parte = (inteiro(p6.get(k, "")) for k in
                             ("oci que o recurso compra", "pessoas atendidas", "parte da fila"))
        if r6 != recurso or a6 != apoio:
            fe.append(f"{cod}: recurso ou apoio da pagina diferente do cabecalho do comparativo")
        if valor and recurso is not None and apoio is not None and pessoas:
            q = int((Decimal(str(recurso)) - Decimal(str(apoio))) // Decimal(str(valor)))
            at = min(q, pessoas)
            pt = round(at / pessoas * 100)
            sb = float(Decimal(str(recurso)) - Decimal(str(apoio)) - at * Decimal(str(valor)))
            for nome, achado, esperado in (("OCI que o recurso compra", qtd, q), ("pessoas atendidas", atend, at),
                                           ("parte da fila", parte, pt)):
                if achado != esperado:
                    fe.append(f"{cod}: {nome} {achado}, a conta da {esperado}")
            if sobra is None or abs(sobra - sb) > 0.005:
                fe.append(f"{cod}: sobra do recurso {p6.get('sobra do recurso')!r}, a conta da {sb:.2f}")
        dados[cod] = {"valor": valor, "mercado minimo": reais(p5.get("mercado minimo", "")), "margem": margem,
                      "cobertura": inteiro(p5.get("cobertura", "")), "pessoas": pessoas, "qtd": qtd,
                      "atend": atend, "parte": parte, "sobra": sobra}
    add("B", "as seis partes, com fonte", fb, na=not paginas)
    add("C", f"valor pela origem do recurso ({origem or '?'}), regra anterior a 01/11/2026" if antiga
        else "valor pela Tabela SUS Candanga", fc, na=not paginas)
    add("D", "custo de executar igual ao precos.md", fd, na=not paginas)
    add("E", "a conta", fe, na=not paginas)

    # F
    falhas = []
    for l in linhas_c:
        cod = CODIGO.search(l["codigo"]).group(0)
        d = dados.get(cod)
        if not d:
            continue
        lido = {"valor": reais(l.get("valor", "")), "mercado minimo": reais(l.get("mercado minimo", "")),
                "margem": reais(l.get("margem no teto", "")), "cobertura": inteiro(l.get("cobertura", "")),
                "pessoas": inteiro(l.get("pessoas que se enquadram", "")),
                "qtd": inteiro(l.get("oci que o recurso compra", "")), "atend": inteiro(l.get("pessoas atendidas", "")),
                "parte": inteiro(l.get("parte da fila", "")), "sobra": reais(l.get("sobra do recurso", ""))}
        for k, v in lido.items():
            if v != d[k]:
                falhas.append(f"{cod}: {k} {v} no comparativo e {d[k]} na pagina")
    ordem = [CODIGO.search(l["codigo"]).group(0) for l in linhas_c if CODIGO.search(l["codigo"]).group(0) in dados]
    # com o recurso fixo, o que sobra no total depende da razao entre o valor e o custo (a
    # cobertura), nao da diferenca por unidade; com um teto igual para todas, a margem no teto
    # so repete a ordem do valor (piloto do redacao_05, 10/10/2026)
    certa = sorted(ordem, key=lambda c: (-(dados[c]["cobertura"] if dados[c]["cobertura"] is not None else -1),
                                         -(dados[c]["valor"] or 0)))
    if ordem != certa:
        falhas.append(f"a ordem e {', '.join(ordem)}; pela cobertura seria {', '.join(certa)}")
    add("F", "comparativo", falhas, na=not dados)

    # G
    falhas = []
    if just:
        for m in PROIBIDO.finditer(just):
            ini = max(0, m.start() - 30)
            falhas.append(f"'{m.group(0)}' na justificativa: ...{just[ini:m.end() + 30].strip()}...")
        if not re.search(r"Mapa Social|mapa_social_\d{8}", just):
            falhas.append("a justificativa nao cita a fonte da fila (Mapa Social)")
        # o teto mede o que a OCI aceitaria, nao quem espera por ela
        numeros = inteiros(just)
        for cod, t in tetos.items():
            if t in numeros:
                falhas.append(f"{cod}: a justificativa cita {t}, o teto da coleta; a fila e a da finalidade")
    add("G", "justificativa publica", falhas[:12], na=not just)

    # H
    falhas = []
    marca = re.compile(r"controle interno", re.I)
    if comp and not marca.search(comp):
        falhas.append("o comparativo sem a marca de controle interno")
    for cod, txt in paginas.items():
        if not marca.search(txt):
            falhas.append(f"{cod}: a pagina sem a marca de controle interno")
    if just and marca.search(just):
        falhas.append("a justificativa com a marca de controle interno: ela e a parte que vai a fora")
    add("H", "controle interno", falhas)
    return itens


def main():
    ap = argparse.ArgumentParser(description="confere o dossie do objeto de um plano")
    ap.add_argument("pasta", help="planos/redacao_NN/dossie/")
    args = ap.parse_args()
    saida_utf8()
    pasta = Path(args.pasta).resolve()
    if not pasta.is_dir():
        raise SystemExit(f"erro: {pasta} nao e uma pasta")
    itens = verificar(pasta)
    print(f"\nCONFERENCIA DO DOSSIE — {pasta.parent.name}/{pasta.name}/")
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
