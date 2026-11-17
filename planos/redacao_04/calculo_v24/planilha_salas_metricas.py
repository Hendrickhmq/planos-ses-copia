"""Metricas das salas de ultrassom da rede (20/10/2026): controle interno.

Mede as 13 salas do documento da equipe (ISHP, Projeto Zero Fila | USG, quantitativo revisado de 20/10/2026) contra a
demanda de cada unidade: pela fila (o rateio do plano v24, fila de 10/09 com as participacoes de 15/09 por RA) e pela
populacao (o rateio do documento). Cenarios de tempo por exame, faltas e prazo; tudo em formula, premissas numa aba.
Le v24.json e polos_capacidade.json.

Uso: python3 planilha_salas_metricas.py v24.json polos_capacidade.json ../estudos/salas_ultrassom_metricas_20261020.xlsx
"""
import json, sys
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.formatting.rule import CellIsRule

V = json.load(open(sys.argv[1]))
PC = json.load(open(sys.argv[2]))
SAIDA = sys.argv[3]

A = "Arial"
F_TIT = Font(name=A, size=15, bold=True, color="1F4E79")
F_SEC = Font(name=A, size=11, bold=True, color="1F4E79")
F_SUB = Font(name=A, size=10, italic=True, color="595959")
F_TXT = Font(name=A, size=10)
F_NEG = Font(name=A, size=10, bold=True)
F_IN = Font(name=A, size=10, color="0000FF")
F_LINK = Font(name=A, size=10, color="008000")
F_CAB = Font(name=A, size=10, bold=True, color="FFFFFF")
CAB = PatternFill("solid", fgColor="1F4E79")
CAB2 = PatternFill("solid", fgColor="2E75B6")
CINZA = PatternFill("solid", fgColor="F2F2F2")
L = Side(style="thin", color="BFBFBF")
B = Border(left=L, right=L, top=L, bottom=L)
N0 = '#,##0;(#,##0);"-"'
N1 = '#,##0.0;(#,##0.0);"-"'
PCT = '0%'
ESQ = Alignment(wrap_text=True, vertical="center")
CEN = Alignment(horizontal="center", vertical="center", wrap_text=True)
DIR = Alignment(horizontal="right", vertical="center")
TIT = Alignment(vertical="center")
VERM = PatternFill("solid", fgColor="F8CBAD")
AMAR = PatternFill("solid", fgColor="FFE699")
VERD = PatternFill("solid", fgColor="C6EFCE")
wb = Workbook()


def c(ws, ref, v, f=F_TXT, fmt=None, fill=None, al=None):
    x = ws[ref]
    x.value = v
    x.font = f
    if fmt: x.number_format = fmt
    if fill: x.fill = fill
    x.alignment = al or (DIR if isinstance(v, (int, float)) or (isinstance(v, str) and v.startswith("=")) else ESQ)
    x.border = B
    return x


def cab(ws, linha, textos, h=42, fill=CAB):
    for i, t in enumerate(textos):
        x = ws.cell(row=linha, column=i + 1, value=t)
        x.font, x.fill, x.alignment, x.border = F_CAB, fill, CEN, B
    ws.row_dimensions[linha].height = h


def larguras(ws, ls):
    for i, w in enumerate(ls):
        ws.column_dimensions[chr(65 + i)].width = w


def semaforo(ws, faixa):
    """ocupacao: ate 85% verde, de 85% a 100% amarelo, acima de 100% vermelho."""
    ws.conditional_formatting.add(faixa, CellIsRule(operator="greaterThan", formula=["1"], fill=VERM))
    ws.conditional_formatting.add(faixa, CellIsRule(operator="between", formula=["0.85", "1"], fill=AMAR))
    ws.conditional_formatting.add(faixa, CellIsRule(operator="lessThan", formula=["0.85"], fill=VERD))


# ---- dados: fila por unidade (rateio do plano por RA) e minutos do plano pelo mix de cada Regiao
RAS = {a["nome"]: a for a in PC["ras"]}
MIN_REG = {}
for x in V["ORD"]:
    p = V["polos"][x]
    for r in V["POLO_REG"][x]:
        MIN_REG[r] = p["hus"] / p["us"] * 60
reg = lambda *rs: [a for a in RAS if RAS[a]["regiao"] in rs]
UNID = [  # unidade, prestador, situacao, quem vai, RAs, salas e populacao do documento de 20/10
    ("Ceilândia", "Clínica Brasília", "Fechado", "Oeste + Taguatinga e Vicente Pires",
     ["Ceilândia", "Sol Nascente/Pôr do Sol", "Brazlândia", "Taguatinga", "Vicente Pires"], 3, 17088),
    ("Samambaia", "MedBrasília", "Fechado", "Samambaia, Águas Claras, Arniqueira e Recanto das Emas",
     ["Samambaia", "Águas Claras", "Arniqueira", "Recanto das Emas e Água Quente"], 2, 11751),
    ("Sobradinho", "Clínica Padrão", "Aguardando resposta", "Norte", reg("Norte"), 2, 8031),
    ("São Sebastião", "Hpaes Hospital Dia", "Aguardando resposta final", "Leste", reg("Leste"), 2, 7111),
    ("Asa Sul", "DaVida", "Fechado", "Central + Centro-Sul", reg("Central", "Centro-Sul"), 3, 15593),
    ("Gama", "Provida Centro Médico", "Fechado", "Sul", reg("Sul"), 1, 5956),
]
FILA, MINP = [], []
for _, _, _, _, ras, _, _ in UNID:
    us = sum(RAS[a]["us"] for a in ras)
    FILA.append(us)
    MINP.append(sum(RAS[a]["us"] * MIN_REG[RAS[a]["regiao"]] for a in ras) / us)
FILA = [round(f) for f in FILA]
FILA[0] += V["us_total"] - sum(FILA)              # o arredondamento preserva o total do plano
assert sum(FILA) == V["us_total"] == sum(u[6] for u in UNID)
DOPPLER = V["qc"]["02.05.01.004-0"]

# ---- Premissas
P = wb.active
P.title = "Premissas"
c(P, "A1", "Premissas e de onde vem cada número", F_TIT, al=TIT).border = Border()
c(P, "A2", "Azul = valor que você pode mudar; o resto da planilha recalcula. Preto = conta.", F_SUB).border = Border()
cab(P, 4, ["Premissa", "Valor", "Unidade", "De onde vem"], h=24)
PRE = [  # linha 5 em diante
    ("Meses de execução", 8, "meses", "Plano v24: 8 meses de execução.", F_IN, N0),
    ("Dias úteis por mês", 21, "dias", "Plano v24, 7.3: 168 dias úteis em 8 meses.", F_IN, N0),
    ("Dias úteis no período", "=B5*B6", "dias", "Conta.", F_TXT, N0),
    ("Horas de agenda por dia em cada sala", 10, "horas", "Plano v24, 7.3, e documento da equipe de 20/10.", F_IN, N0),
    ("Aproveitamento da agenda", 0.8, "", "Reserva operacional de 20% (troca de paciente, limpeza, atraso). Plano v24, 7.3, e "
     "documento da equipe. Não é a falta do paciente.", F_IN, PCT),
    ("Minutos por exame (média do gestor)", 13, "min", "Documento da equipe de 20/10/2026, item 4: premissa informada pelo "
     "gestor, ainda sem medida das clínicas.", F_IN, N1),
    ("Faltas de pacientes", 0.2, "", "Documento da equipe de 20/10/2026, item 5. Entra só nos cenários \"com faltas\", em que a "
     "vaga do faltoso fica parada (sem encaixe).", F_IN, PCT),
    ("Exames de ultrassom a realizar", V["us_total"], "exames", "Plano v24: a meta é de exames realizados (65.530). O "
     "documento da equipe usa o mesmo total.", F_IN, N0),
    ("Minutos de planejamento: ultrassom simples", 20, "min", "Plano v24, 7.3 (tempo de planejamento).", F_IN, N0),
    ("Minutos de planejamento: doppler", 30, "min", "Plano v24, 7.3 (tempo de planejamento).", F_IN, N0),
    ("Exames de doppler no plano (02.05.01.004-0)", DOPPLER, "exames", "Plano v24, quantitativo por procedimento.", F_IN, N0),
    ("Parte do doppler nos exames", "=B15/B12", "", "Conta.", F_TXT, '0.0%'),
    ("Média do plano por exame", "=B16*B14+(1-B16)*B13", "min", "Conta: o mix do plano no tempo de planejamento.", F_TXT, N1),
    ("Capacidade de uma sala no período (média do gestor)", "=B7*B8*60*B9/B10", "exames",
     "Conta: dias × horas × 60 × aproveitamento ÷ minutos. Dá 6.203, como no documento da equipe.", F_TXT, N0),
    ("Capacidade de uma sala no período (média do plano)", "=B7*B8*60*B9/B17", "exames", "Conta.", F_TXT, N0),
    ("Minutos do doppler, para testar a média do gestor", 25, "min", "Valor de teste: muda para ver quanto o exame simples "
     "precisa durar.", F_IN, N0),
    ("Quanto o exame simples precisa durar para a média dar a do gestor", "=(B10-B16*B20)/(1-B16)", "min",
     "Conta: com o doppler no tempo da linha acima.", F_TXT, N1),
]
for i, (n, v, u, f, fv, fmt) in enumerate(PRE):
    r = 5 + i
    c(P, f"A{r}", n)
    c(P, f"B{r}", v, fv, fmt)
    c(P, f"C{r}", u, al=CEN)
    c(P, f"D{r}", f)
    P.row_dimensions[r].height = 30
c(P, "A24", "Fontes", F_SEC, al=ESQ).border = Border()
FONTES = [
    "Exames pela fila: plano v24 (calculo_v24/polos_capacidade.json), a fila de 10/09 com as participações por Região de "
    "15/09, distribuída por RA e somada nas RAs que o documento da equipe manda a cada unidade.",
    "Exames pela população, salas, prestador e situação: documento ISHP \"Rede de ultrassonografia: quantitativo revisado\", "
    "Projeto Zero Fila | USG, 20/10/2026, página 1.",
    "Minutos do plano por unidade: as horas de ultrassom de cada Região no plano v24 (7.3) divididas pelos exames, nas RAs "
    "da unidade. A Norte sai mais alta porque tem mais doppler na fila.",
]
for i, t in enumerate(FONTES):
    P.merge_cells(f"A{25 + i}:D{25 + i}")
    c(P, f"A{25 + i}", t).border = Border()
    P.row_dimensions[25 + i].height = 30
larguras(P, [46, 12, 9, 80])

# ---- Por unidade
U = wb.create_sheet("Por unidade")
c(U, "A1", "As 13 salas, unidade por unidade", F_TIT, al=TIT).border = Border()
c(U, "A2", "Ocupação = exames ÷ o que as salas comportam no período, já com os 20% de reserva operacional. Verde até 85%, "
           "amarelo de 85% a 100%, vermelho acima de 100% (não cabe). Salas contratadas em azul: mude para testar.",
  F_SUB).border = Border()
U.merge_cells("A2:P2")
U.row_dimensions[2].height = 28
# faixa de grupos
GR = [("A4:E4", "A unidade"), ("F4:H4", "Demanda (exames em 8 meses)"), ("I4:L4", "Na média do gestor (13 min)"),
      ("M4:P4", "O que falta ou sobra, pela fila"), ("Q4:S4", "No tempo do plano")]
for faixa, t in GR:
    U.merge_cells(faixa)
    x = U[faixa.split(":")[0]]
    x.value, x.font, x.fill, x.alignment = t, F_CAB, CAB2, CEN
U.row_dimensions[4].height = 20
cab(U, 5, ["Unidade", "Prestador", "Situação", "Quem vai para lá", "Salas contratadas",
           "Pela fila (plano)", "Pela população (documento)", "Exames por dia útil, pela fila",
           "Comportam no período", "Ocupação pela fila", "Ocupação pela população", "Ocupação pela fila, com faltas",
           "Salas necessárias pela fila", "Salas a mais (+) ou a menos (−)", "Exames que não cabem (vão a outro polo)",
           "Exames de folga", "Minutos do plano (mix da fila)", "Ocupação no tempo do plano", "Salas necessárias no tempo do plano"],
    h=54)
for i, (un, pr, si, quem, _, salas, pop) in enumerate(UNID):
    r = 6 + i
    c(U, f"A{r}", un, F_NEG)
    c(U, f"B{r}", pr)
    c(U, f"C{r}", si, al=CEN)
    c(U, f"D{r}", quem)
    c(U, f"E{r}", salas, F_IN, N0)
    c(U, f"F{r}", FILA[i], F_IN, N0)
    c(U, f"G{r}", pop, F_IN, N0)
    c(U, f"H{r}", f"=F{r}/Premissas!$B$7", F_TXT, N0)
    c(U, f"I{r}", f"=E{r}*Premissas!$B$18", F_TXT, N0)
    c(U, f"J{r}", f"=F{r}/I{r}", F_TXT, PCT)
    c(U, f"K{r}", f"=G{r}/I{r}", F_TXT, PCT)
    c(U, f"L{r}", f"=F{r}/(1-Premissas!$B$11)/I{r}", F_TXT, PCT)
    c(U, f"M{r}", f"=CEILING(F{r}/Premissas!$B$18,1)", F_TXT, N0)
    c(U, f"N{r}", f"=E{r}-M{r}", F_TXT, '+#,##0;−#,##0;0')
    c(U, f"O{r}", f"=MAX(F{r}-I{r},0)", F_TXT, N0)
    c(U, f"P{r}", f"=MAX(I{r}-F{r},0)", F_TXT, N0)
    c(U, f"Q{r}", round(MINP[i], 1), F_IN, N1)
    c(U, f"R{r}", f"=F{r}*Q{r}/(E{r}*Premissas!$B$7*Premissas!$B$8*60*Premissas!$B$9)", F_TXT, PCT)
    c(U, f"S{r}", f"=CEILING(F{r}*Q{r}/(Premissas!$B$7*Premissas!$B$8*60*Premissas!$B$9),1)", F_TXT, N0)
    U.row_dimensions[r].height = 30
r = 12
c(U, f"A{r}", "Rede", F_NEG, fill=CINZA)
for col in "BCD":
    c(U, f"{col}{r}", None, fill=CINZA)
for col in "EFGHIMOPS":
    c(U, f"{col}{r}", f"=SUM({col}6:{col}11)", F_NEG, N0, CINZA)
c(U, f"J{r}", f"=F{r}/I{r}", F_NEG, PCT, CINZA)
c(U, f"K{r}", f"=G{r}/I{r}", F_NEG, PCT, CINZA)
c(U, f"L{r}", f"=F{r}/(1-Premissas!$B$11)/I{r}", F_NEG, PCT, CINZA)
c(U, f"N{r}", f"=E{r}-M{r}", F_NEG, '+#,##0;−#,##0;0', CINZA)
c(U, f"Q{r}", f"=SUMPRODUCT(F6:F11,Q6:Q11)/F{r}", F_NEG, N1, CINZA)
c(U, f"R{r}", f"=SUMPRODUCT(F6:F11,Q6:Q11)/(E{r}*Premissas!$B$7*Premissas!$B$8*60*Premissas!$B$9)", F_NEG, PCT, CINZA)
semaforo(U, "J6:L12")
semaforo(U, "R6:R12")
U.conditional_formatting.add("N6:N12", CellIsRule(operator="lessThan", formula=["0"], fill=VERM))
NOTAS_U = [
    "Como ler: \"Comportam no período\" = salas × 6.203 (168 dias × 10 h × 60 × 80% ÷ 13 min). \"Exames que não cabem\" é o "
    "que a unidade não atende com as salas contratadas e tem de ir a outra unidade pela regulação.",
    "\"Com faltas\": a vaga do faltoso fica parada (sem encaixe). Para realizar os 65.530, a agenda oferta 65.530 ÷ 80% = "
    "81.913 vagas, como diz o item 6 do documento.",
    "A soma das \"salas necessárias\" é por unidade (cada uma arredondada para cima); por isso passa a conta da rede inteira, "
    "que está na aba Cenários.",
]
for i, t in enumerate(NOTAS_U):
    U.merge_cells(f"A{14 + i}:S{14 + i}")
    c(U, f"A{14 + i}", t).border = Border()
    U.row_dimensions[14 + i].height = 26
larguras(U, [14, 20, 15, 30, 10, 11, 12, 11, 12, 11, 11, 11, 11, 11, 12, 11, 11, 11, 11])
U.freeze_panes = "B6"

# ---- Cenários (rede inteira)
C = wb.create_sheet("Cenários", 0)
c(C, "A1", "As 13 salas aguentam? Rede inteira, em cenários", F_TIT, al=TIT).border = Border()
c(C, "A2", "Cada linha muda uma coisa em relação ao documento da equipe. Ocupação acima de 100% = a rede não realiza os "
           "65.530 exames no prazo. Os valores em azul podem ser mudados.", F_SUB).border = Border()
C.merge_cells("A2:J2")
C.row_dimensions[2].height = 28
cab(C, 4, ["Cenário", "O que muda", "Salas", "Minutos por exame", "Faltas que deixam a vaga parada", "Meses",
           "Vagas a ofertar", "As salas comportam", "Ocupação", "Salas necessárias", "Salas a mais (+) ou a menos (−)"], h=48)
ME = "Premissas!$B$10"
MP = "Premissas!$B$17"
CEN_ = [  # nome, o que muda, salas, minutos, faltas, meses
    ("1. Documento da equipe", "13 salas, 13 min, faltas repostas por encaixe, 8 meses", 13, f"={ME}", 0, "=Premissas!$B$5"),
    ("2. Faltas sem encaixe", "A vaga do faltoso fica parada", 13, f"={ME}", "=Premissas!$B$11", "=Premissas!$B$5"),
    ("3. Só as salas já fechadas", "Sobradinho e São Sebastião não fecham: 9 salas", 9, f"={ME}", 0, "=Premissas!$B$5"),
    ("4. Só as fechadas, faltas sem encaixe", "9 salas e a vaga do faltoso parada", 9, f"={ME}", "=Premissas!$B$11",
     "=Premissas!$B$5"),
    ("5. Execução em 7 meses", "Começa um mês depois", 13, f"={ME}", 0, 7),
    ("6. 7 meses, faltas sem encaixe", "Começa um mês depois e a vaga do faltoso fica parada", 13, f"={ME}",
     "=Premissas!$B$11", 7),
    ("7. Média de 15 minutos", "Dois minutos a mais por exame", 13, 15, 0, "=Premissas!$B$5"),
    ("8. Média de 16 minutos", "Três minutos a mais por exame", 13, 16, 0, "=Premissas!$B$5"),
    ("9. Tempo do plano", "Simples a 20 min e doppler a 30 (média 22,2)", 13, f"={MP}", 0, "=Premissas!$B$5"),
    ("10. Tempo do plano, faltas sem encaixe", "O tempo do plano e a vaga do faltoso parada", 13, f"={MP}",
     "=Premissas!$B$11", "=Premissas!$B$5"),
    ("11. O plano v24 (20 salas)", "As 20 salas do plano, no tempo do plano", 20, f"={MP}", 0, "=Premissas!$B$5"),
]
for i, (n, o, s, m, f, me) in enumerate(CEN_):
    r = 5 + i
    c(C, f"A{r}", n, F_NEG)
    c(C, f"B{r}", o)
    c(C, f"C{r}", s, F_IN, N0)
    c(C, f"D{r}", m, F_LINK if str(m).startswith("=") else F_IN, N1)
    c(C, f"E{r}", f, F_LINK if str(f).startswith("=") else F_IN, PCT)
    c(C, f"F{r}", me, F_LINK if str(me).startswith("=") else F_IN, N0)
    c(C, f"G{r}", f"=Premissas!$B$12/(1-E{r})", F_TXT, N0)
    cap = f"(F{r}*Premissas!$B$6*Premissas!$B$8*60*Premissas!$B$9/D{r})"
    c(C, f"H{r}", f"=C{r}*{cap}", F_TXT, N0)
    c(C, f"I{r}", f"=G{r}/H{r}", F_NEG, PCT)
    c(C, f"J{r}", f"=CEILING(G{r}/{cap},1)", F_TXT, N0)
    c(C, f"K{r}", f"=C{r}-J{r}", F_TXT, '+#,##0;−#,##0;0')
    C.row_dimensions[r].height = 30
semaforo(C, "I5:I15")
C.conditional_formatting.add("K5:K15", CellIsRule(operator="lessThan", formula=["0"], fill=VERM))
C.merge_cells("A16:K16")
c(C, "A16", "Aqui é a rede inteira, como se a regulação mandasse cada paciente para onde há vaga. Unidade por unidade, pela "
            "fila, a conta pede as 13 salas em outra distribuição (aba Por unidade).", F_SUB).border = Border()
C.row_dimensions[16].height = 28
c(C, "A17", "Indicadores", F_SEC, al=ESQ).border = Border()
cab(C, 18, ["Indicador", "Valor", "", "O que quer dizer"], h=22)
C.merge_cells("D18:K18")
IND = [
    ("Tempo médio máximo que as 13 salas aguentam (min)",
     "=$C$5*Premissas!$B$7*Premissas!$B$8*60*Premissas!$B$9/Premissas!$B$12", N1,
     "Acima disso, a rede não fecha os 65.530 em 8 meses. A margem sobre os 13 min do gestor é só essa diferença."),
    ("O mesmo, com faltas sem encaixe (min)",
     "=$C$5*Premissas!$B$7*Premissas!$B$8*60*Premissas!$B$9*(1-Premissas!$B$11)/Premissas!$B$12", N1,
     "Se a vaga do faltoso fica parada, a média tem de ficar abaixo disso: menos que os 13 min."),
    ("Folga da rede na média do gestor (exames)", "=H5-G5", N0,
     "A rede inteira tem essa sobra, mas ela está nas unidades erradas (aba Por unidade)."),
    ("Unidades acima de 100% pela fila", "=COUNTIF('Por unidade'!J6:J11,\">1\")", N0,
     "Gama e Samambaia: a fila delas passa do que as salas contratadas comportam."),
    ("Exames do Sul que não cabem no Gama", "='Por unidade'!O11", N0,
     "O Gama tem 1 sala para a fila do Sul, que é a 2ª maior da rede."),
    ("Folga da Asa Sul (exames)", "='Por unidade'!P10", N0,
     "É a unidade com folga mais perto do Sul; recebe o que não cabe no Gama, se a regulação mandar."),
    ("Exame simples precisa durar (min) para a média ser a do gestor", "=Premissas!$B$21", N1,
     "Com o doppler a 25 min (22% dos exames). É o ponto a confirmar com as clínicas."),
]
for i, (n, f, fmt, t) in enumerate(IND):
    r = 19 + i
    c(C, f"A{r}", n)
    c(C, f"B{r}", f, F_NEG, fmt)
    C.merge_cells(f"D{r}:K{r}")
    c(C, f"D{r}", t)
    C.row_dimensions[r].height = 30
larguras(C, [34, 40, 8, 11, 12, 8, 11, 12, 11, 11, 12])
C.freeze_panes = "A5"

# ---- Sensibilidade
S = wb.create_sheet("Sensibilidade")
c(S, "A1", "Quantas salas a rede precisa, por minuto de exame e por falta", F_TIT, al=TIT).border = Border()
c(S, "A2", "Rede inteira, sem o arredondamento por unidade (a conta por unidade dá um pouco mais). Ocupação das 13 salas "
           "nas tabelas de baixo.", F_SUB).border = Border()
S.merge_cells("A2:H2")
MINS = [11, 12, 13, 14, 15, 16, 18, 20, 22.2, 25]
FALT = [0, 0.1, 0.2]
lin = 4
for titulo, meses, modo in [("Salas necessárias em 8 meses", "Premissas!$B$5", "salas"),
                            ("Salas necessárias em 7 meses", "7", "salas"),
                            ("Ocupação das 13 salas em 8 meses", "Premissas!$B$5", "ocup"),
                            ("Ocupação das 13 salas em 7 meses", "7", "ocup")]:
    c(S, f"A{lin}", titulo, F_SEC, al=ESQ).border = Border()
    lin += 1
    cab(S, lin, ["Minutos por exame"] + [f"Faltas sem encaixe {int(f * 100)}%" for f in FALT], h=32)
    for j, f in enumerate(FALT):
        S.cell(row=lin, column=2 + j).value = f
        S.cell(row=lin, column=2 + j).number_format = '"Faltas sem encaixe "0%'
    h = lin
    for k, m in enumerate(MINS):
        r = lin + 1 + k
        c(S, f"A{r}", m, F_IN, N1)
        for j in range(len(FALT)):
            col = chr(66 + j)
            vagas = f"(Premissas!$B$12/(1-{col}${h}))"
            cap = f"({meses}*Premissas!$B$6*Premissas!$B$8*60*Premissas!$B$9/$A{r})"
            if modo == "salas":
                c(S, f"{col}{r}", f"=CEILING({vagas}/{cap},1)", F_TXT, N0)
            else:
                c(S, f"{col}{r}", f"={vagas}/(13*{cap})", F_TXT, PCT)
        if modo == "ocup":
            semaforo(S, f"B{lin + 1}:D{lin + len(MINS)}")
        else:
            S.conditional_formatting.add(f"B{lin + 1}:D{lin + len(MINS)}",
                                         CellIsRule(operator="greaterThan", formula=["13"], fill=VERM))
    lin += len(MINS) + 3
larguras(S, [18, 18, 18, 18])

wb._sheets = [C, U, S, P]
for ws in wb._sheets:
    ws.page_setup.orientation = 'landscape'
    ws.page_setup.fitToWidth, ws.page_setup.fitToHeight = 1, 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
wb.active = 0
wb.save(SAIDA)
print("gravado", SAIDA)
