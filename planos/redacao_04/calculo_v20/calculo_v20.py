"""v20 do plano 4 (06/10/2026): recurso do Oficio 40/2026 (proposta 36000720055202500,
R$ 11.592.762,00), apoio da opcao C (v18 + 2 assistentes) e seis polos.

Mesmo metodo da v19 (../calculo_v19): fila de 10/09 inteira (Q18), acrescimo pelas
solicitacoes de 2026 sem agendamento (cenario G), rateio por nome de fila com as
participacoes das Regioes de 15/09, horas por tempo de exame, salas pela regra dos 80%,
curva por codigo e parcelas por trimestre. O que muda e o recurso, o apoio e os polos.
"""
import sys, os, json, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "calculo_v19"))
import calculo as K
from calculo import D, F, Q18, COD, UNIT, maiores_restos, por_codigo, curva

RECURSO = D("11592762.00")
# apoio, opcao C: 1 coord. adm. 10.500 + 1 coord. fin. 9.500 + assessoria 5.455 + 6 operadores 4.300 + 8 assistentes 3.200, x 12
APOIO = {"coord_adm": (1, D("10500.00")), "coord_fin": (1, D("9500.00")), "assessoria": (1, D("5455.00")),
         "operadores": (6, D("4300.00")), "assistentes": (8, D("3200.00"))}
APOIO_TOTAL = sum(n * v * 12 for n, v in APOIO.values())
assert APOIO_TOTAL == D("922260.00")

# seis polos - Leste fica com Sobradinho, como na v19 e no pt_ses_05 ("Norte e Leste")
K.POLO = {"Ceilândia": ["Região Oeste"], "Taguatinga": ["Região Sudoeste"],
          "Sobradinho": ["Região Norte", "Região Leste"], "Plano Piloto": ["Região Central"],
          "Gama": ["Região Sul"], "Guará": ["Região Centro-Sul"]}
K.ORD = ORD = ["Ceilândia", "Taguatinga", "Sobradinho", "Plano Piloto", "Gama", "Guará"]

# abertas de 2026 (Mapa Social, 05/10/2026) - por codigo e por nome de fila
AB_COD = {"02.05.02.009-7": 5528, "02.05.02.018-6": 4117, "02.05.01.004-0": 7245, "02.05.02.004-6": 5865,
          "02.05.02.005-4": 1576, "02.05.02.012-7": 1430, "02.05.02.010-0": 1116, "02.05.02.003-8": 807,
          "02.06.03.001-0": 4321, "02.06.03.003-7": 3739, "02.06.02.003-1": 3370}
AB = {"mama": 5528, "transvag": 4117, "abd_total": 4737, "parede": 1128, "dop_mmii": 2834, "carotidas": 4411,
      "urinario": 1576, "tireoide": 1430, "prostata": 1116, "abd_sup": 807, "tc_abd": 4321, "tc_pelve": 3739,
      "tc_torax_c": 2477, "coronarias": 783, "tc_torax_s": 110}


def montar(N):
    """fila inteira + N exames repartidos pelas abertas de 2026 (codigo, depois nome de fila)"""
    e = maiores_restos({c: F(N * AB_COD[c], sum(AB_COD.values())) for c in AB_COD}, N)
    Q = dict(Q18)
    for c, x in e.items():
        nomes = [n for n in COD if COD[n] == c]
        for n, v in maiores_restos({n: F(x * AB[n], sum(AB[m] for m in nomes)) for n in nomes}, x).items():
            Q[n] += v
    return Q


def custo(Q):
    return sum(q * UNIT[c] for c, q in por_codigo(Q).items())


envelope = RECURSO - APOIO_TOTAL
N = 0
while custo(montar(N + 1)) <= envelope:
    N += 1
Q = montar(N)
# a sobra que ainda comporta um exame vai ao codigo com mais abertas de 2026 que caiba (nome de fila com mais abertas)
preenchidos = []
while RECURSO - APOIO_TOTAL - custo(Q) >= min(UNIT.values()):
    sobra = RECURSO - APOIO_TOTAL - custo(Q)
    c = max((c for c in AB_COD if UNIT[c] <= sobra), key=lambda c: AB_COD[c])
    n = max((n for n in COD if COD[n] == c), key=lambda n: AB[n])
    Q[n] += 1
    preenchidos.append(n)

qc = por_codigo(Q)
producao = custo(Q)
glob = producao + APOIO_TOTAL
sobra = RECURSO - glob
assert D(0) <= sobra < min(UNIT.values())
tot, us, tc, hus, htc, pct = K.rateio(Q)
DIAS, HORAS = 252, 10
salas = {p: max(1, math.ceil(hus[p] / (DIAS * HORAS * 0.8))) for p in ORD}
mes_us = {p: math.ceil(us[p] / 12) for p in ORD}
mes_tc = {p: math.ceil(tc[p] / 12) for p in ORD}
dia_us = {p: math.ceil(us[p] / DIAS) for p in ORD}
dia_tc = {p: math.ceil(tc[p] / DIAS) for p in ORD}
por_sala = {p: math.ceil(dia_us[p] / salas[p]) for p in ORD}
operadores = {p: 1 for p in ORD}   # operador de registro dedicado em cada polo (R-11, 9.2)
# assistentes: um por polo (decisao do usuario, 06/10/2026); os dois restantes pela producao, por maiores restos
_resto = maiores_restos({p: F(2 * tot[p], sum(tot.values())) for p in ORD}, 2)
assistentes = {p: 1 + _resto[p] for p in ORD}
medicos_us = {p: math.ceil(hus[p] / 1800) for p in ORD}
radiologistas = {p: math.ceil(htc[p] / 1800) for p in ORD}
tri = curva(qc)
curva_tri = [sum(t.values()) for t in tri]
prod_tri = [sum(t[c] * UNIT[c] for c in t) for t in tri]
parcelas = [x + APOIO_TOTAL / 4 for x in prod_tri]
contraste = sum(Q[n] for n in ["tc_abd", "tc_pelve", "tc_torax_c", "coronarias"])
contraste_cod = {"02.06.03.001-0": Q["tc_abd"], "02.06.03.003-7": Q["tc_pelve"],
                 "02.06.02.003-1": Q["tc_torax_c"] + Q["coronarias"]}

out = {
    "recurso": str(RECURSO), "apoio": str(APOIO_TOTAL), "envelope": str(envelope),
    "acrescimo": N + len(preenchidos), "acrescimo_proporcional": N, "preenchidos": preenchidos,
    "Q": Q, "qc": qc, "total": sum(qc.values()),
    "us_total": sum(v for c, v in qc.items() if c.startswith("02.05")),
    "tc_total": sum(v for c, v in qc.items() if c.startswith("02.06")),
    "producao": str(producao), "global": str(glob), "sobra": str(sobra),
    "apoio_pct_global": float(APOIO_TOTAL / glob),
    "ORD": ORD, "POLO": K.POLO, "tot": tot, "us": us, "tc": tc, "hus": hus, "htc": htc,
    "pct": {p: float(pct[p]) for p in ORD},
    "mes_us": mes_us, "mes_tc": mes_tc, "dia_us": dia_us, "dia_tc": dia_tc, "salas": salas, "por_sala": por_sala,
    "operadores": operadores, "assistentes": assistentes, "medicos_us": medicos_us, "radiologistas": radiologistas,
    "curva": curva_tri, "pico_dia": math.ceil(max(curva_tri) / 63),
    "prod_tri": [str(x) for x in prod_tri], "parcelas": [str(x) for x in parcelas],
    "contraste": contraste, "contraste_cod": contraste_cod, "absorvido_contraste": str(contraste * D("60.00")),
    "tomografos_equivalentes": sum(htc.values()) / (DIAS * HORAS),
}

if __name__ == "__main__":
    for k in ["acrescimo", "preenchidos", "total", "us_total", "tc_total", "producao", "global", "sobra"]:
        print(k, out[k])
    print("apoio", APOIO_TOTAL, f"{float(APOIO_TOTAL / glob) * 100:.3f}% do global")
    print("por código", qc)
    print("polos", tot, {p: f"{float(pct[p]) * 100:.2f}%" for p in ORD}, "soma", sum(tot.values()))
    print("US", us, "| TC", tc)
    print("h US", hus, sum(hus.values()), "| h TC", htc, sum(htc.values()), f"| {out['tomografos_equivalentes']:.2f} tomógrafos")
    print("salas", salas, sum(salas.values()), "| ocupação", {p: f"{hus[p] / (salas[p] * 2520):.0%}" for p in ORD})
    print("mês US", mes_us, sum(mes_us.values()), "| mês TC", mes_tc, sum(mes_tc.values()))
    print("dia US", dia_us, sum(dia_us.values()), "| dia TC", dia_tc, sum(dia_tc.values()), "| por sala", por_sala)
    print("operadores", operadores, "| assistentes", assistentes)
    print("médicos US", medicos_us, sum(medicos_us.values()), "| radiologistas", radiologistas, sum(radiologistas.values()))
    print("curva", curva_tri, "pico/dia", out["pico_dia"])
    print("produção/tri", [f"{x:.2f}" for x in prod_tri], "| parcelas", [f"{x:.2f}" for x in parcelas])
    print("contraste", contraste, contraste_cod, "coronárias", Q["coronarias"])
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "v20.json"), "w"),
              ensure_ascii=False, indent=1, default=str)
