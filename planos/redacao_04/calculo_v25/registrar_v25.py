"""Registra os numeros da v25 em estado.yaml, dados/envelope.md e dados/capacidade.md de uma pasta do plano.

uso: registrar_v25.py <pasta_do_plano>

Roda sobre a pasta real quando a v25 for ao plano, ou sobre uma copia, para conferir as variantes antes. Le v25.json.
"""
import sys, os, json, re
from decimal import Decimal as D

AQUI = os.path.dirname(os.path.abspath(__file__))
PASTA = sys.argv[1]
V = json.load(open(os.path.join(AQUI, "v25.json")))
ORD, P = V["ORD"], V["polos"]
APOIO, GLOB, PROD = D(V["apoio"]), D(V["global"]), D(V["producao"])
RECURSO = D("11592762.00")
UNIT = {"02.05.01.004-0": D("100.18"), "02.05.02.004-6": D("100.18"), "02.06.02.003-1": D("300.10"),
        "02.06.03.001-0": D("299.44"), "02.06.03.003-7": D("299.44")}
un = lambda c: UNIT.get(c, D("99.94"))
M4 = sum(un(c) * V["qc"][c] for c in V["qc"] if c.startswith("02.05"))
M5 = sum(un(c) * V["qc"][c] for c in V["qc"] if c.startswith("02.06"))
POSTO = {p: (qt, D(v), D(tt)) for p, qt, v, _, _, tt in V["quadro"]}
M1 = sum(POSTO[k][2] for k in ["Direção Executiva de Projeto", "Coordenação Assistencial", "Supervisão de Polo Assistencial"])
M2 = POSTO["Operador de registro de sistemas — pré-exame"][2]
M3 = POSTO["Operador de registro de sistemas — pós-exame"][2]
M6 = sum(POSTO[k][2] for k in ["Coordenação Administrativa e Financeira", "Assessoria de Prestação de Contas",
                               "Assistente Administrativo"])
assert M1 + M2 + M3 + M6 == APOIO and M4 + M5 == PROD
M1, M2, M3, M4, M5, M6 = (x.quantize(D("0.01")) for x in (M1, M2, M3, M4, M5, M6))
pct = (APOIO / GLOB).quantize(D("0.00001"))
media = (PROD / V["total"]).quantize(D("0.01"))


def n(x):
    return f"{int(x):,}".replace(",", ".")


def r(x):
    s = f"{D(str(x)).quantize(D('0.01')):,.2f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def troca(txt, padrao, novo):
    txt2, k = re.subn(padrao, novo, txt, count=1, flags=re.M)
    assert k == 1, padrao
    return txt2


# ---------------- estado.yaml ----------------
ey = os.path.join(PASTA, "estado.yaml")
s = open(ey, encoding="utf-8").read()
s = troca(s, r"^    realizado: 954560\.00 .*$", f"    realizado: {APOIO}           # v25 (21/10/2026): Direcao Executiva, "
          "Coord. Assistencial e Coord. Adm. e Financeira, 3 supervisores de polo, 10 operadores (5 pre e 5 pos-exame), "
          "6 assistentes e a assessoria - x 8 meses")
s = troca(s, r"^    percentual_realizado: 0\.08234 .*$", f"    percentual_realizado: {pct}  # DERIVADO do realizado "
          f"({r(APOIO)} / {r(GLOB)}), nunca o contrario")
for x in ORD:
    s = troca(s, rf'^      "{re.escape(x)}": \{{pct: (0\.\d+), exames: \d+\}}',
              f'      "{x}": {{pct: \\1, exames: {P[x]["tot"]}}}')
s = s.replace("rateio_objeto:                 # participacoes por procedimento de 15/09, nas 7 Regioes somadas nos 6 "
              "polos - v24", "rateio_objeto:                 # participacoes por procedimento de 15/09, nas 7 Regioes "
              "somadas nos 6 polos - v25")
for chave, valor in [("soma_procedimentos", f"{PROD}"), ("valor_global", f"{GLOB}        # soma + apoio realizado - v25"),
                     ("apoio_total", f"{APOIO}           # o realizado, montado de baixo para cima"),
                     ("apoio_realizado", f"{APOIO}       # v25: quadro de 21/10/2026 (D-007)"),
                     ("apoio_percentual_realizado", f"{pct}   # DERIVADO do quadro, nunca o contrario"),
                     ("valor_global_derivado", f"{GLOB}    # soma + apoio realizado"),
                     ("envelope_producao", f"{RECURSO - APOIO}        # recurso - apoio"),
                     ("sobra_nao_aplicada", f"{D(V['sobra'])}             # recurso - global; menor que o menor unitario "
                      "(99,94)"),
                     ("horas_sala_us", f"{V['hus']}"), ("horas_sala_tc", f"{V['htc']}"),
                     ("horas_sala_total", f"{V['hus'] + V['htc']}"),
                     ("quantitativo_exames", f"{V['total']}        # v25: 78.572 da extracao + {V['acrescimo']} das entradas"),
                     ("media_por_exame", f"{media}            # {PROD} / {V['total']}")]:
    s = troca(s, rf"^  {chave}: .*$", f"  {chave}: {valor}")
s = troca(s, r'^  1: \{nome: "Estruturacao e coordenacao da execucao".*$',
          f'  1: {{nome: "Estruturacao e coordenacao da execucao", quantitativo: "6 polos em operacao", dotacao: {M1}}}'
          '   # v25: Direcao Executiva, Coord. Assistencial, 3 supervisores de polo')
s = troca(s, r'^  2: \{nome: "Gestao da fila".*$',
          f'  2: {{nome: "Gestao da fila", quantitativo: "{n(V["total"])} vagas disponibilizadas a regulacao", '
          f'dotacao: {M2}}}   # v25: 5 operadores do pre-exame')
s = troca(s, r'^  3: \{nome: "Registro da producao".*$',
          f'  3: {{nome: "Registro da producao", quantitativo: "{n(V["total"])} exames registrados", dotacao: {M3}}}'
          '   # v25: 5 operadores do pos-exame')
s = troca(s, r'^  4: \{nome: "Execucao assistencial em ultrassonografia".*$',
          f'  4: {{nome: "Execucao assistencial em ultrassonografia", quantitativo: {V["us_total"]}, dotacao: {M4}}}')
s = troca(s, r'^  5: \{nome: "Execucao assistencial em tomografia".*$',
          f'  5: {{nome: "Execucao assistencial em tomografia", quantitativo: {V["tc_total"]}, dotacao: {M5}}}')
open(ey, "w", encoding="utf-8").write(s)

# ---------------- dados/envelope.md ----------------
linhas = "".join(f"| {p_} | {qt} | {r(v)} | {r(tt)} |\n" for p_, qt, v, _, _, tt in V["quadro"])
env = (f"\n\n## v25, 21/10/2026 — o quadro de 21/10 (D-007)\n\n"
       "O professor orientou que três coordenações não se justificam com supervisores de polo. O usuário decidiu: sai a\n"
       "Coordenação Operacional; ficam a Assistencial e a Administrativa e Financeira, três supervisores de polo a 6.155 "
       "(um para\ndois polos), dez operadores de registro (cinco no pré-exame, cinco no pós-exame), seis assistentes e a "
       "assessoria, todos\npor 8 meses:\n\n| posto | qtd | R$/mês | total |\n|---|---|---|---|\n" + linhas +
       f"| **total** | | | **{r(APOIO)}** |\n\n| | exames | valor |\n|---|---|---|\n"
       f"| Recurso disponível | | R$ {r(RECURSO)} |\n| Apoio | | R$ {r(APOIO)} |\n"
       f"| **Envelope de produção assistencial** | | **R$ {r(RECURSO - APOIO)}** |\n"
       f"| Acréscimo pelas abertas de 2026 | {n(V['acrescimo'])} | |\n"
       f"| **Soma dos procedimentos** | **{n(V['total'])}** | **R$ {r(PROD)}** |\n"
       f"| **Valor global** | | **R$ {r(GLOB)}** |\n| Diferença não aplicada | | R$ {r(V['sobra'])} |\n"
       f"| apoio ÷ global | | **{str(pct * 100)[:4].replace('.', ',')}%** (teto de 8,5%: R$ 985.384,77) |\n\n"
       f"O apoio sobe R$ 1.600,00 sobre a v24; o acréscimo além da fila cai de 580 para {n(V['acrescimo'])} exames.\n")
with open(os.path.join(PASTA, "dados", "envelope.md"), "a", encoding="utf-8") as f:
    f.write(env)

# ---------------- dados/capacidade.md ----------------
cab = "| | " + " | ".join(ORD) + " | total |\n|" + "---|" * (len(ORD) + 2) + "\n"
lin = lambda rot, k, tot: f"| {rot} | " + " | ".join(n(P[x][k]) for x in ORD) + f" | {tot} |\n"
cap = (f"\n\n## v25, 21/10/2026 — o quadro de 21/10 e a capacidade em horas\n\n"
       f"Mesmo método da v24. A execução do objeto requer **{n(V['hus'] + V['htc'])} horas** de sala: **{n(V['hus'])} "
       f"horas** de ultrassonografia e\n**{n(V['htc'])} horas** de tomografia computadorizada ({n(V['htc'])} ÷ 1.344 h = "
       f"carga de **{V['carga_tc']:.2f}** equipamentos).\n\n".replace("3.33", "3,33") + cab +
       lin("exames", "tot", n(V["total"])) + lin("ultrassonografia", "us", n(V["us_total"])) +
       lin("tomografia", "tc", n(V["tc_total"])) + lin("horas de ultrassom", "hus", n(V["hus"])) +
       lin("horas de tomógrafo", "htc", n(V["htc"])) + lin("exames por dia útil, ultrassom", "dia_us",
                                                           n(sum(P[x]["dia_us"] for x in ORD))) +
       lin("exames por dia útil, tomografia", "dia_tc", n(sum(P[x]["dia_tc"] for x in ORD))) +
       "\nO texto passa a publicar a capacidade da ultrassonografia em horas, sem número de salas por polo (usuário, "
       "21/10/2026):\no número de salas de cada polo sai do tempo de exame praticado nele, conferido no mês 1. Variante A: "
       "seis tomógrafos,\num por polo no dimensionamento, com a tomografia de um polo podendo ser feita em outro da rede. "
       "Variante B: o texto\nnão diz quantos tomógrafos, só a carga de 3,33 equipamentos, que a rede atende com folga; "
       f"radiologistas da rede\n{n(V['htc'])} ÷ 1.200 = {V['htc'] / 1200:.2f} (no mínimo {V['radiologistas_rede']}).\n"
       .replace(f"{V['htc'] / 1200:.2f}", f"{V['htc'] / 1200:.2f}".replace(".", ",")))
with open(os.path.join(PASTA, "dados", "capacidade.md"), "a", encoding="utf-8") as f:
    f.write(cap)
print("registrado em", PASTA, "| apoio", APOIO, "| global", GLOB, "| metas", M1, M2, M3, M4, M5, M6)
