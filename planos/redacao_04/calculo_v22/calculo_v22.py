"""v22 do plano 4 (07/10/2026): oito meses de vigencia e de execucao, dez polos, novo quadro de gestao.

Decisoes do usuario:
- vigencia e execucao de 8 meses, sem folga (os quatro periodos passam de trimestres a bimestres);
- dez polos sem localizacao fixa (os da v21): Oeste 1, Sudoeste 2, Norte e Leste 2, Central 2, Sul 2, Centro-Sul 1;
- gestao e apoio: Direcao Executiva de Projeto (14.500, pt_ses_01), Coordenacao Administrativa e Financeira
  (10.500), Coordenacao Operacional (9.500), Assessoria de Prestacao de Contas (5.455), 10 operadores de registro
  (um por polo, 4.300) e 10 assistentes administrativos (um por polo, 3.200), tudo por 8 meses;
- tomografia: pelo menos um tomografo por Regiao; a Sudoeste com dois.

Metodo igual ao da v20/v21 (calculo_v19/calculo.py): fila de 10/09 inteira, acrescimo pelas abertas de 2026,
rateio por nome de fila com as participacoes de 15/09, horas por tempo de exame, salas pela regra dos 80%,
curva por codigo (um quarto por periodo, resto nos ultimos), parcela = producao do periodo + apoio/4.
"""
import sys, os, json, math
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "calculo_v19"))
import calculo as K
from calculo import D, F, Q18, COD, UNIT, maiores_restos, por_codigo, curva

MESES = 8
DIAS = 21 * MESES                      # 168 dias uteis
HORAS_DIA = 10
H_MEDICO = 1800 * MESES // 12          # 1.200 h por medico no periodo (1.800 h anuais)
RECURSO = D("11592762.00")
TETO = RECURSO * D("0.08")
QUADRO = [  # (posto, qtd, R$/mes, meta, item)
    ("Direção Executiva de Projeto", 1, D("14500.00"), 1, "1.1.1"),
    ("Coordenação Operacional", 1, D("9500.00"), 1, "1.1.2"),
    ("Assistente Administrativo", 10, D("3200.00"), 2, "2.1.1"),
    ("Operador de registro de sistemas", 10, D("4300.00"), 3, "3.1.1"),
    ("Coordenação Administrativa e Financeira", 1, D("10500.00"), 6, "6.1.1"),
    ("Assessoria de Prestação de Contas", 1, D("5455.00"), 6, "6.1.2"),
]
APOIO = sum(q * v * MESES for _, q, v, _, _ in QUADRO)
assert APOIO == D("919640.00") and APOIO <= TETO

K.POLO = {"Oeste": ["Região Oeste"], "Sudoeste": ["Região Sudoeste"],
          "Norte e Leste": ["Região Norte", "Região Leste"], "Central": ["Região Central"],
          "Sul": ["Região Sul"], "Centro-Sul": ["Região Centro-Sul"]}
K.ORD = ORD = ["Oeste", "Sudoeste", "Norte e Leste", "Central", "Sul", "Centro-Sul"]
POLOS = {"Oeste": 1, "Sudoeste": 2, "Norte e Leste": 2, "Central": 2, "Sul": 2, "Centro-Sul": 1}

AB_COD = {"02.05.02.009-7": 5528, "02.05.02.018-6": 4117, "02.05.01.004-0": 7245, "02.05.02.004-6": 5865,
          "02.05.02.005-4": 1576, "02.05.02.012-7": 1430, "02.05.02.010-0": 1116, "02.05.02.003-8": 807,
          "02.06.03.001-0": 4321, "02.06.03.003-7": 3739, "02.06.02.003-1": 3370}
AB = {"mama": 5528, "transvag": 4117, "abd_total": 4737, "parede": 1128, "dop_mmii": 2834, "carotidas": 4411,
      "urinario": 1576, "tireoide": 1430, "prostata": 1116, "abd_sup": 807, "tc_abd": 4321, "tc_pelve": 3739,
      "tc_torax_c": 2477, "coronarias": 783, "tc_torax_s": 110}


def montar(N):
    e = maiores_restos({c: F(N * AB_COD[c], sum(AB_COD.values())) for c in AB_COD}, N)
    Q = dict(Q18)
    for c, x in e.items():
        nomes = [n for n in COD if COD[n] == c]
        for n, v in maiores_restos({n: F(x * AB[n], sum(AB[m] for m in nomes)) for n in nomes}, x).items():
            Q[n] += v
    return Q


def custo(Q):
    return sum(q * UNIT[c] for c, q in por_codigo(Q).items())


envelope = RECURSO - APOIO
N = 0
while custo(montar(N + 1)) <= envelope:
    N += 1
Q = montar(N)
preenchidos = []
while RECURSO - APOIO - custo(Q) >= min(UNIT.values()):
    sobra = RECURSO - APOIO - custo(Q)
    c = max((c for c in AB_COD if UNIT[c] <= sobra), key=lambda c: AB_COD[c])
    n = max((n for n in COD if COD[n] == c), key=lambda n: AB[n])
    Q[n] += 1
    preenchidos.append(n)
qc = por_codigo(Q)
producao = custo(Q)
glob = producao + APOIO
sobra = RECURSO - glob
assert D(0) <= sobra < min(UNIT.values())

tot, us, tc, hus, htc, pct = K.rateio(Q)
CAP = DIAS * HORAS_DIA * 0.8           # 1.344 h por sala ou tomografo a 80%
salas = {r: max(math.ceil(hus[r] / CAP), POLOS[r]) for r in ORD}
tomografos = {r: max(math.ceil(htc[r] / CAP), 1) for r in ORD}
mes_us = {r: math.ceil(us[r] / MESES) for r in ORD}
mes_tc = {r: math.ceil(tc[r] / MESES) for r in ORD}
dia_us = {r: math.ceil(us[r] / DIAS) for r in ORD}
dia_tc = {r: math.ceil(tc[r] / DIAS) for r in ORD}
por_sala = {r: math.ceil(dia_us[r] / salas[r]) for r in ORD}
medicos_us = {r: max(math.ceil(hus[r] / H_MEDICO), salas[r]) for r in ORD}
radiologistas = {r: max(math.ceil(htc[r] / H_MEDICO), tomografos[r]) for r in ORD}
tecnicos = {r: 3 * tomografos[r] for r in ORD}
enfermagem = {r: 2 * tomografos[r] for r in ORD}
rt = dict(POLOS)
retaguarda = dict(POLOS)
recepcao = {r: 2 * POLOS[r] for r in ORD}
operadores = dict(POLOS)
assistentes = dict(POLOS)
# dois trimestres e um bimestre final (decisao do usuario, 07/10/2026): cada codigo se reparte na proporcao dos
# meses (3/8, 3/8, 2/8), pelo piso; o resto da divisao vai aos ultimos periodos, como na curva por trimestre
PERIODOS = [("1º trimestre", "1 a 3", 3), ("2º trimestre", "4 a 6", 3), ("bimestre final", "7 a 8", 2)]
PESOS = [m for _, _, m in PERIODOS]
assert sum(PESOS) == MESES
tri = [{} for _ in PERIODOS]
for c, qq in qc.items():
    base = [qq * w // MESES for w in PESOS]
    for k in range(qq - sum(base)):
        base[len(PESOS) - 1 - k] += 1
    for i, v in enumerate(base):
        tri[i][c] = v
curva_b = [sum(t.values()) for t in tri]
assert sum(curva_b) == sum(qc.values())
prod_b = [sum(t[c] * UNIT[c] for c in t) for t in tri]
apoio_p = [APOIO * w / MESES for w in PESOS]
parcelas = [x + a for x, a in zip(prod_b, apoio_p)]
dias_p = [21 * w for w in PESOS]
taxa = [curva_b[i] / dias_p[i] for i in range(len(PESOS))]
i_pico = max(range(len(PESOS)), key=lambda i: taxa[i])
contraste = sum(Q[n] for n in ["tc_abd", "tc_pelve", "tc_torax_c", "coronarias"])

out = {
    "meses": MESES, "dias": DIAS, "h_medico": H_MEDICO, "recurso": str(RECURSO), "apoio": str(APOIO),
    "quadro": [(p, q, str(v), m, i, str(q * v * MESES)) for p, q, v, m, i in QUADRO],
    "envelope": str(envelope), "acrescimo": sum(qc.values()) - sum(Q18.values()), "preenchidos": preenchidos,
    "Q": Q, "qc": qc, "total": sum(qc.values()),
    "us_total": sum(v for c, v in qc.items() if c.startswith("02.05")),
    "tc_total": sum(v for c, v in qc.items() if c.startswith("02.06")),
    "producao": str(producao), "global": str(glob), "sobra": str(sobra), "apoio_pct": float(APOIO / glob),
    "ORD": ORD, "POLOS": POLOS, "tot": tot, "us": us, "tc": tc, "hus": hus, "htc": htc,
    "pct": {r: float(pct[r]) for r in ORD}, "salas": salas, "tomografos": tomografos, "mes_us": mes_us,
    "mes_tc": mes_tc, "dia_us": dia_us, "dia_tc": dia_tc, "por_sala": por_sala, "medicos_us": medicos_us,
    "radiologistas": radiologistas, "tecnicos": tecnicos, "enfermagem": enfermagem, "rt": rt,
    "retaguarda": retaguarda, "recepcao": recepcao, "operadores": operadores, "assistentes": assistentes,
    "periodos": PERIODOS, "dias_periodo": dias_p, "apoio_periodo": [str(x) for x in apoio_p],
    "curva": curva_b, "pico_dia": math.ceil(taxa[i_pico]), "pico_periodo": i_pico, "prod_b": [str(x) for x in prod_b],
    "parcelas": [str(x) for x in parcelas], "contraste": contraste, "coronarias": Q["coronarias"],
    "contraste_cod": {"02.06.03.001-0": Q["tc_abd"], "02.06.03.003-7": Q["tc_pelve"],
                      "02.06.02.003-1": Q["tc_torax_c"] + Q["coronarias"]},
    "absorvido_contraste": str(contraste * D("60.00")),
    "tomografos_equivalentes": sum(htc.values()) / (DIAS * HORAS_DIA),
}

if __name__ == "__main__":
    for k in ["total", "us_total", "tc_total", "acrescimo", "preenchidos", "producao", "global", "sobra"]:
        print(f"{k:12}", out[k])
    print("apoio", APOIO, f"{float(APOIO / glob) * 100:.3f}%", "| teto", TETO)
    print("por código", qc)
    print("polos/Região", tot, {r: f"{float(pct[r]) * 100:.2f}%" for r in ORD})
    print("h US", hus, sum(hus.values()), "| h TC", htc, sum(htc.values()),
          f"| carga TC {out['tomografos_equivalentes']:.2f}")
    print("salas", salas, sum(salas.values()), "| ocupação", {r: f"{hus[r] / (salas[r] * DIAS * HORAS_DIA):.0%}" for r in ORD})
    print("tomógrafos", tomografos, sum(tomografos.values()), "| ocupação",
          {r: f"{htc[r] / (tomografos[r] * DIAS * HORAS_DIA):.0%}" for r in ORD})
    print("mês US", mes_us, sum(mes_us.values()), "| mês TC", mes_tc, sum(mes_tc.values()))
    print("dia US", dia_us, sum(dia_us.values()), "| dia TC", dia_tc, sum(dia_tc.values()), "| por sala", por_sala)
    print("médicos US", medicos_us, sum(medicos_us.values()), "| radiologistas", radiologistas,
          sum(radiologistas.values()))
    print("técnicos", sum(tecnicos.values()), "| enfermagem", sum(enfermagem.values()), "| recepção",
          sum(recepcao.values()), "| RT", sum(rt.values()), "| retaguarda", sum(retaguarda.values()))
    print("curva (2 trimestres + bimestre)", curva_b, "por dia útil", [f"{t:.1f}" for t in taxa],
          "pico/dia", out["pico_dia"], "no período", PERIODOS[i_pico][0])
    print("produção/bimestre", [f"{x:.2f}" for x in prod_b], "| parcelas", [f"{x:.2f}" for x in parcelas])
    print("contraste", contraste, out["contraste_cod"], "coronárias", Q["coronarias"])
    json.dump(out, open(os.path.join(AQUI, "v22.json"), "w"), ensure_ascii=False, indent=1, default=str)
