"""Quanto custa um exame para o ISHP (20/10/2026): primeira nocao, controle interno.

Ultrassom pela execucao propria nas salas alugadas (aluguel, aparelho, medico, recepcao, insumos); tomografia pelo preco
por exame negociado com as clinicas, nos planos de 6 e de 5 polos, com a comparacao da tomografia feita pelo proprio
ISHP. Le v24.json e polos_capacidade.json. Recalcular depois com o recalc.py da skill xlsx.

Uso: python3 planilha_custo_por_exame.py v24.json polos_capacidade.json ../estudos/custo_por_exame_v1_20261020.xlsx
"""
import json, sys
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter as COL

V = json.load(open(sys.argv[1]))
PC = json.load(open(sys.argv[2]))
SAIDA = sys.argv[3]

A = "Arial"
F_TIT = Font(name=A, size=14, bold=True, color="1F4E79")
F_SUB = Font(name=A, size=10, italic=True, color="555555")
F_TXT = Font(name=A, size=10)
F_NEG = Font(name=A, size=10, bold=True)
F_IN = Font(name=A, size=10, color="0000FF")
F_VERDE = Font(name=A, size=10, color="008000")
F_CAB = Font(name=A, size=10, bold=True, color="FFFFFF")
CAB = PatternFill("solid", fgColor="1F4E79")
AMAR = PatternFill("solid", fgColor="FFF2CC")
TOT = PatternFill("solid", fgColor="DDEBF7")
DEST = PatternFill("solid", fgColor="E2EFDA")
L = Side(style="thin", color="BFBFBF")
B = Border(left=L, right=L, top=L, bottom=L)
R2 = '#,##0.00;(#,##0.00);"-"'
N0 = '#,##0;(#,##0);"-"'
PCT = '0.0%'
QUEBRA = Alignment(wrap_text=True, vertical="center")
CENTRO = Alignment(horizontal="center", vertical="center", wrap_text=True)
MEIO = Alignment(vertical="center")
wb = Workbook()


def c(ws, ref, v, f=F_TXT, fmt=None, fill=None, al=None, borda=True):
    x = ws[ref]
    x.value = v
    x.font = f
    if fmt: x.number_format = fmt
    if fill: x.fill = fill
    x.alignment = al or MEIO
    if borda: x.border = B
    return x


def cab(ws, linha, textos, h=40):
    for i, t in enumerate(textos):
        c(ws, f"{COL(i + 1)}{linha}", t, F_CAB, fill=CAB, al=CENTRO)
    ws.row_dimensions[linha].height = h


def txt(ws, linha, t, ate, f=F_TXT, h=None):
    c(ws, f"A{linha}", t, f, al=QUEBRA, borda=False)
    ws.merge_cells(f"A{linha}:{ate}{linha}")
    if h: ws.row_dimensions[linha].height = h


def larg(ws, ws_l):
    for i, w in enumerate(ws_l):
        ws.column_dimensions[COL(i + 1)].width = w


ORD, P = V["ORD"], V["polos"]
US, TC = V["us_total"], V["tc_total"]
M4 = sum(V["qc"][k] * {"02.05.01.004-0": 100.18, "02.05.02.004-6": 100.18}.get(k, 99.94) for k in V["qc"] if k.startswith("02.05"))
M5 = sum(V["qc"][k] * (300.10 if k == "02.06.02.003-1" else 299.44) for k in V["qc"] if k.startswith("02.06"))

r = wb.active
r.title = "Resumo"
pp = wb.create_sheet("Por polo")
u = wb.create_sheet("Ultrassom")
t = wb.create_sheet("Tomografia")
f = wb.create_sheet("Fontes e premissas")
UA, TA = "'Ultrassom'!", "'Tomografia'!"

# ------------------------------------------------------------------ Ultrassom
c(u, "A1", "Ultrassom: execução própria nas salas alugadas", F_TIT, borda=False)
c(u, "A2", "O ISHP aluga a sala (e o aparelho, onde a clínica não tem) e paga o médico por exame. Células amarelas são "
  "premissas: mude e a conta se refaz.", F_SUB, borda=False)
cab(u, 4, ["Premissa", "Econômico", "Conservador", "De onde vem"])
PREM = [
    ("Exames de ultrassom no projeto", US, US, N0, "plano v24, Meta 4"),
    ("Meses de execução", 8, 8, N0, "plano v24"),
    ("Salas de ultrassom", 20, 20, N0, "plano v24, 7.3: salas a 80% de 10 h por dia útil, no tempo de planejamento por exame"),
    ("Aluguel por sala por mês (R$)", 3000, 3000, R2, "rede do ISHP: R$ 6.000 por polo com 2 salas, recepção e guichê, 8h às 18h"),
    ("Salas que precisam de aparelho alugado", 0, 20, N0, "econômico: a clínica tem o aparelho; conservador: todas alugadas"),
    ("Aparelho por sala por mês (R$)", 2500, 2500, R2, "rede do ISHP: opção mapeada em Samambaia, com manutenção"),
    ("Médico por exame (R$)", 33.33, 40.00, R2, "modelos do ISHP: R$ 1.000 por lote de 30 exames ou R$ 4.000 por lote de 100"),
    ("Recepcionistas pagos à parte", 0, 12, N0, "econômico: incluídos no aluguel; conservador: 2 por polo"),
    ("Custo de cada recepcionista por mês (R$)", 2959, 2959, R2, "salario.com.br, Recepcionista de consultório, Brasília (custo para a empresa)"),
    ("Insumos por exame (R$)", 3.00, 3.00, R2, "hipótese: gel, papel, lençol, capa do transdutor, desinfecção"),
]
for i, (rot, e, k, fmt, fonte) in enumerate(PREM):
    l = 5 + i
    c(u, f"A{l}", rot)
    c(u, f"B{l}", e, F_IN, fmt, AMAR)
    c(u, f"C{l}", k, F_IN, fmt, AMAR)
    c(u, f"D{l}", fonte, al=QUEBRA)
    u.row_dimensions[l].height = 28
cab(u, 16, ["Resultado", "Econômico", "Conservador", "Conta"])
RES = [
    (17, "Aluguel das salas no período (R$)", "={c}7*{c}8*{c}6", "salas × aluguel × meses"),
    (18, "Aparelhos no período (R$)", "={c}9*{c}10*{c}6", "salas com aparelho × preço × meses"),
    (19, "Médicos no período (R$)", "={c}5*{c}11", "exames × médico por exame"),
    (20, "Recepção à parte no período (R$)", "={c}12*{c}13*{c}6", "recepcionistas × custo × meses"),
    (21, "Insumos no período (R$)", "={c}5*{c}14", "exames × insumos"),
    (22, "Custo total do ultrassom (R$)", "=SUM({c}17:{c}21)", ""),
    (23, "Custo por exame (R$)", "={c}22/{c}5", ""),
    (24, "O convênio paga, em média, por exame (R$)", f"={M4 / US:.6f}", "Meta 4 ÷ exames de ultrassom (valor de tabela mais o incremento)"),
    (25, "Folga por exame (R$)", "={c}24-{c}23", "o que o convênio paga menos o custo"),
    (26, "Custo como parte do que o convênio paga", "={c}23/{c}24", ""),
    (27, "Folga no projeto (R$)", "={c}25*{c}5", ""),
]
for l, rot, fm, conta in RES:
    neg = l in (22, 23, 25, 27)
    c(u, f"A{l}", rot, F_NEG if neg else F_TXT, fill=TOT if neg else None)
    for col in "BC":
        c(u, f"{col}{l}", fm.format(c=col), F_NEG if neg else F_TXT, PCT if l == 26 else R2, DEST if l in (23, 25) else None)
    c(u, f"D{l}", conta, al=QUEBRA)
txt(u, 29, "Por polo, no cenário econômico (aluguel, médico e insumos): o polo pequeno paga mais aluguel por exame.", "F", F_NEG, 16)
cab(u, 30, ["Polo", "Exames de ultrassom", "Salas", "Aluguel no período (R$)", "Aluguel por exame (R$)", "Custo por exame (R$)"])
for i, x in enumerate(ORD):
    l = 31 + i
    c(u, f"A{l}", x)
    c(u, f"B{l}", P[x]["us"], F_IN, N0)
    c(u, f"C{l}", P[x]["salas"], F_IN, N0, al=CENTRO)
    c(u, f"D{l}", f"=C{l}*$B$8*$B$6", fmt=R2)
    c(u, f"E{l}", f"=D{l}/B{l}", fmt=R2)
    c(u, f"F{l}", f"=E{l}+$B$11+$B$14", F_NEG, R2, DEST)
c(u, "A37", "Total", F_NEG, fill=TOT)
for col, fm in [("B", "=SUM(B31:B36)"), ("C", "=SUM(C31:C36)"), ("D", "=SUM(D31:D36)"), ("E", "=D37/B37"), ("F", "=E37+$B$11+$B$14")]:
    c(u, f"{col}37", fm, F_NEG, N0 if col in "BC" else R2, TOT)
txt(u, 39, "Referência de médico contratado por salário: o IgesDF paga R$ 18.115,68 brutos a ultrassonografista por 24 horas "
    "semanais (Edital 070/2026). São cerca de R$ 174 por hora antes dos encargos, ou uns R$ 58 por exame a 3 exames por hora. "
    "O pagamento por exame (R$ 33 a R$ 40) é o que cabe no valor do convênio.", "F", h=44)
txt(u, 41, "Aluguel como negociado com as clínicas: R$ 6.000 por polo, com 2 salas (planilha da rede de ultrassom do ISHP). "
    "Quantas salas o aluguel cobre e quantas o plano pede.", "G", F_NEG, 30)
cab(u, 42, ["Polo", "Unidade", "Aluguel mensal negociado (R$)", "Aparelho opcional por mês (R$)", "Salas no aluguel",
            "Salas que o plano pede", "Salas a mais a negociar"], 44)
NEG = [("Oeste", "Ceilândia — Clínica Brasília", 6000, 0), ("Sudoeste", "Samambaia — Med Saúde", 6000, 2500),
       ("Norte", "Sobradinho — Clínica Padrão", 6000, 0), ("Leste", "São Sebastião — GPAES/HPAES", 6000, 0),
       ("Central e Centro-Sul", "Asa Sul (DaVida) ou bairro Sudoeste (Ana Maia)", 6000, 0),
       ("Sul", "Gama — CIG (valor a consolidar; aqui, R$ 6.000)", 6000, 0)]
for i, (x, uni, alug, apar) in enumerate(NEG):
    l = 43 + i
    c(u, f"A{l}", x)
    c(u, f"B{l}", uni, al=QUEBRA)
    c(u, f"C{l}", alug, F_IN, R2, AMAR)
    c(u, f"D{l}", apar, F_IN, R2, AMAR)
    c(u, f"E{l}", 2, F_IN, N0, AMAR, CENTRO)
    c(u, f"F{l}", P[x]["salas"], F_IN, N0, al=CENTRO)
    c(u, f"G{l}", f"=MAX(0,F{l}-E{l})", F_NEG, N0, DEST, CENTRO)
    u.row_dimensions[l].height = 28
c(u, "A49", "Total", F_NEG, fill=TOT)
for col in "CDEFG":
    c(u, f"{col}49", f"=SUM({col}43:{col}48)", F_NEG, R2 if col in "CD" else N0, TOT, CENTRO)
c(u, "A50", "Aluguel e aparelho no período, como negociado (R$)")
c(u, "C50", "=(C49+D49)*$B$6", F_NEG, R2)
c(u, "A51", "Aluguel e aparelho por exame, como negociado (R$)")
c(u, "C51", "=C50/$B$5", F_NEG, R2)
c(u, "A52", "Custo por exame como negociado: aluguel, aparelho, médico a R$ 33,33 e insumos (R$)", F_NEG, fill=TOT)
c(u, "C52", "=C51+$B$11+$B$14", F_NEG, R2, DEST)
c(u, "A53", "Salas a mais, ao preço de R$ 3.000 por sala, no período (R$)")
c(u, "C53", "=G49*$B$8*$B$6", F_NEG, R2)
for l in (50, 51, 52, 53):
    u.merge_cells(f"A{l}:B{l}")
    u.row_dimensions[l].height = 28
txt(u, 55, "Como negociado, o aluguel sai barato por exame, mas cobre 12 salas, e o plano pede 20 no tempo de planejamento. "
    "As salas a mais estão na última coluna: Samambaia e Gama concentram quase todas. Se as clínicas derem as salas a mais "
    "pelo mesmo valor do polo, vale a conta de cima; se cobrarem por sala, vale a de baixo, igual ao cenário econômico.", "G", h=44)
larg(u, [42, 30, 16, 16, 12, 12, 14])

# ------------------------------------------------------------------ Tomografia
c(t, "A1", "Tomografia: preço por exame nas clínicas", F_TIT, borda=False)
c(t, "A2", "Preços negociados (planilha de tomografia do ISHP). As clínicas a definir entram no teto de R$ 175. A divisão dos "
  "exames é a do estudo dos polos (Samambaia e Recanto das Emas a Ceilândia; no plano de 5, a Leste à Asa Sul e o Itapoã a "
  "Sobradinho).", F_SUB, borda=False)
t.merge_cells("A2:F2")
t.row_dimensions[2].height = 30
NOME = {"Ceilândia": ("Ceilândia — Clínica Brasília", 175), "Taguatinga": ("Taguatinga — Clínica Padrão", 165),
        "Plano Piloto": ("Central e Centro-Sul — a definir", 175), "Sobradinho": ("Sobradinho — Clínica Padrão", 165),
        "Gama": ("Gama — CIG", 175), "São Sebastião": ("Leste — a definir", 175)}
ORDT = ["Ceilândia", "Taguatinga", "Plano Piloto", "Sobradinho", "Gama", "São Sebastião"]
LT = {}
for bloco, (chave, titulo, l0) in enumerate([("tc6", "Plano de 6 polos com tomografia", 4), ("tc5", "Plano de 5 polos (Leste sem)", 14)]):
    txt(t, l0, titulo, "F", F_NEG, 16)
    cab(t, l0 + 1, ["Clínica", "Preço por exame (R$)", "Exames no projeto", "Custo no período (R$)", "O convênio paga (R$)", "Folga (R$)"])
    sedes = [s for s in ORDT if s in PC[chave]["por_sede"]]
    for i, sd in enumerate(sedes):
        l = l0 + 2 + i
        c(t, f"A{l}", NOME[sd][0])
        c(t, f"B{l}", NOME[sd][1], F_IN, R2, AMAR)
        c(t, f"C{l}", round(PC[chave]["por_sede"][sd]), F_IN, N0)
        c(t, f"D{l}", f"=B{l}*C{l}", fmt=R2)
        c(t, f"E{l}", f"=C{l}*$B$31", fmt=R2)
        c(t, f"F{l}", f"=E{l}-D{l}", fmt=R2)
    lt = l0 + 2 + len(sedes)
    LT[chave] = lt
    c(t, f"A{lt}", "Total e preço médio", F_NEG, fill=TOT)
    c(t, f"B{lt}", f"=D{lt}/C{lt}", F_NEG, R2, DEST)
    for col in "CDEF":
        c(t, f"{col}{lt}", f"=SUM({col}{l0 + 2}:{col}{lt - 1})", F_NEG, N0 if col == "C" else R2, TOT)
cab(t, 23, ["Leitura", "6 polos", "5 polos", "Conta", "", ""])
t.merge_cells("D23:F23")
LEI = [
    (24, "Custo por exame (R$)", f"=B{LT['tc6']}", f"=B{LT['tc5']}", "preço médio ponderado pelos exames de cada clínica"),
    (25, "O convênio paga, em média (R$)", "=$B$31", "=$B$31", "Meta 5 ÷ exames de tomografia"),
    (26, "Folga por exame (R$)", "=B25-B24", "=C25-C24", ""),
    (27, "Custo como parte do que o convênio paga", "=B24/B25", "=C24/C25", ""),
    (28, "Se a clínica cobrar o contraste à parte: custo por exame (R$)", "=B24+$B$33*$B$32", "=C24+$B$33*$B$32",
     "mais R$ 60 em 95% dos exames"),
    (29, "Folga no projeto (R$)", f"=F{LT['tc6']}", f"=F{LT['tc5']}", ""),
]
for l, rot, a, b, conta in LEI:
    neg = l in (24, 26, 29)
    c(t, f"A{l}", rot, F_NEG if neg else F_TXT, al=QUEBRA)
    c(t, f"B{l}", a, F_NEG if neg else F_TXT, PCT if l == 27 else R2, DEST if l in (24, 26) else None)
    c(t, f"C{l}", b, F_NEG if neg else F_TXT, PCT if l == 27 else R2, DEST if l in (24, 26) else None)
    c(t, f"D{l}", conta, al=QUEBRA)
    t.merge_cells(f"D{l}:F{l}")
PT = [
    (31, "O convênio paga, em média, por tomografia (R$)", round(M5 / TC, 6), R2, "Meta 5 ÷ exames de tomografia (tabela mais incremento)"),
    (32, "Parte dos exames com contraste", round(V["contraste"] / TC, 6), PCT, f"{V['contraste']} de {TC} (plano v24, 4.8)"),
    (33, "Contraste, se cobrado à parte (R$)", 60, R2, "referência do SUS: 02.06.03.004-5, R$ 60,00"),
]
for l, rot, v, fmt, fonte in PT:
    c(t, f"A{l}", rot)
    c(t, f"B{l}", v, F_IN, fmt, AMAR)
    c(t, f"C{l}", fonte, al=QUEBRA)
    t.merge_cells(f"C{l}:F{l}")
txt(t, 35, "Comparação: e se o ISHP fizesse a tomografia, com equipe própria na sala da clínica?", "F", F_NEG, 16)
cab(t, 36, ["Item", "6 tomógrafos", "5 tomógrafos", "Premissa (amarelo) e conta", "", ""])
t.merge_cells("D36:F36")
EXE = [
    (37, "Técnicos em radiologia por tomógrafo", 3, 3, N0, "3 por tomógrafo (50 h semanais ÷ 24 h), como no plano"),
    (38, "Custo de cada técnico por mês (R$)", 4872, 4872, R2, "média nacional de R$ 2.866 (salario.com.br, 2026) × 1,7 de encargos"),
    (39, "Enfermagem por tomógrafo", 2, 2, N0, "2 por tomógrafo, como no plano"),
    (40, "Custo de cada técnico de enfermagem por mês (R$)", 4945, 4945, R2, "salario.com.br, Técnico de enfermagem, Brasília (custo para a empresa)"),
    (41, "Laudo do radiologista por exame (R$)", 60, 60, R2, "pregão de Garça/SP, 2026: R$ 60 por laudo (pesquisa de R$ 40 a R$ 80)"),
    (42, "Insumos por exame com contraste (R$)", 20, 20, R2, "hipótese: seringa da bomba injetora, cateter, equipo, soro"),
]
for l, rot, a, b, fmt, fonte in EXE:
    c(t, f"A{l}", rot)
    c(t, f"B{l}", a, F_IN, fmt, AMAR)
    c(t, f"C{l}", b, F_IN, fmt, AMAR)
    c(t, f"D{l}", fonte, al=QUEBRA)
    t.merge_cells(f"D{l}:F{l}")
    t.row_dimensions[l].height = 28
CALC = [
    (43, "Equipe por exame (R$)", "=({c}37*{c}38+{c}39*{c}40)*8*{n}/{tc}", "equipe × meses × tomógrafos ÷ exames"),
    (44, "Laudo, contraste e insumos por exame (R$)", "={c}41+($B$33+{c}42)*$B$32", "laudo + (contraste + insumos) nos exames com contraste"),
    (45, "Custo por exame sem a sala nem o tomógrafo (R$)", "={c}43+{c}44", ""),
    (46, "Preço médio das clínicas, com tudo incluído (R$)", "=B24", ""),
    (47, "O que sobra para pagar sala e tomógrafo, por exame (R$)", "={c}46-{c}45", "negativo: a execução própria custa mais que comprar o exame"),
]
for l, rot, fm, conta in CALC:
    neg = l in (45, 47)
    c(t, f"A{l}", rot, F_NEG if neg else F_TXT, al=QUEBRA, fill=TOT if neg else None)
    for col, ntomo, ch in [("B", 6, "tc6"), ("C", 5, "tc5")]:
        v = fm.format(c=col, n=ntomo, tc=f"$C${LT['tc6']}")
        if l == 46:
            v = "=B24" if col == "B" else "=C24"
        c(t, f"{col}{l}", v, F_NEG if neg else F_TXT, R2, DEST if l == 47 else None)
    c(t, f"D{l}", conta, al=QUEBRA)
    t.merge_cells(f"D{l}:F{l}")
larg(t, [46, 16, 16, 22, 18, 16])

# ------------------------------------------------------------------ Por polo
PA = "'Por polo'!"
c(pp, "A1", "Custo por polo, com a execução do ultrassom pelo ISHP: tudo explícito", F_TIT, borda=False)
c(pp, "A2", "Ultrassom feito pelo ISHP nas salas alugadas; tomografia comprada da clínica de cada polo (o mais barato, aba "
  "Tomografia). Células amarelas são premissas. A coluna B diz como cada linha se calcula.", F_SUB, borda=False)
pp.merge_cells("A2:I2")
cab(pp, 4, ["Premissa", "Valor", "De onde vem"])
pp.merge_cells("C4:I4")
PRE = [
    (5, "Meses de execução", 8, N0, "plano v24"),
    (6, "Plano de tomografia: A (6 polos) ou B (5, a Leste sem)", "A", None, "escreva A ou B"),
    (7, "Aluguel por sala de ultrassom por mês (R$)", 3000, R2, "rede do ISHP: R$ 6.000 por polo com 2 salas, recepção e guichê"),
    (8, "Aluguel do aparelho de ultrassom por sala por mês (R$)", 2500, R2, "rede do ISHP: opção mapeada em Samambaia, com manutenção"),
    (9, "Parte das salas com aparelho alugado", 1, PCT, "execução própria: o ISHP aluga o aparelho de toda sala (mude se a clínica tiver)"),
    (10, "Médico de ultrassom por exame (R$)", 33.33, R2, "modelo do ISHP: R$ 1.000 por lote de 30 exames (R$ 40 no lote de 100)"),
    (11, "Recepcionistas por polo", 2, N0, "plano, 4.15: polo aberto 50 h por semana ÷ 44 h"),
    (12, "Custo de cada recepcionista por mês (R$)", 2959, R2, "salario.com.br, Recepcionista de consultório, Brasília, custo para a empresa"),
    (13, "Insumos por exame de ultrassom (R$)", 3, R2, "hipótese: gel, papel, lençol, capa do transdutor, desinfecção"),
    (14, "Outros custos do polo por mês: limpeza, energia, internet, sistema de imagem (R$)", 0, R2,
     "a confirmar se vêm no aluguel; se não vierem, ponha o valor aqui"),
    (15, "Operadores de registro no pré-exame (agenda no SISREG, contato, confirmação, busca ativa)", 4, N0, "plano v24 (D-005)"),
    (16, "Operadores de registro no pós-exame (TrakCare, APAC, faturamento)", 4, N0, "plano v24 (D-005)"),
    (17, "Custo de cada operador por mês (R$)", 4300, R2, "plano v24, preço do IEV"),
    (18, "Direção Executiva de Projeto por mês (R$)", 14500, R2, "plano v24"),
    (19, "Coordenação Operacional por mês (R$)", 8400, R2, "plano v24"),
    (20, "Coordenação Assistencial por mês (R$)", 10500, R2, "plano v24"),
    (21, "Coordenação Administrativa e Financeira por mês (R$)", 8400, R2, "plano v24"),
    (22, "Supervisão de Polo por mês, cada uma (R$); são 3, uma para cada 2 polos", 6155, R2, "plano v24"),
    (23, "Assistente Administrativo por mês, um por polo (R$)", 3200, R2, "plano v24"),
    (24, "Assessoria de Prestação de Contas por mês (R$)", 5455, R2, "plano v24"),
    (25, "O convênio paga por exame de ultrassom, em média (R$)", round(M4 / US, 6), R2, "Meta 4 ÷ exames de ultrassom"),
    (26, "O convênio paga por exame de tomografia, em média (R$)", round(M5 / TC, 6), R2, "Meta 5 ÷ exames de tomografia"),
    (27, "Apoio que o convênio paga no período (R$)", "=(B15+B16)*B17*B5+(B18+B19+B20+B21+3*B22+6*B23+B24)*B5", R2,
     "a soma dos postos de gestão e apoio (R$ 954.560,00 no plano)"),
]
for l, rot, v, fmt, fonte in PRE:
    c(pp, f"A{l}", rot, al=QUEBRA)
    c(pp, f"B{l}", v, F_NEG if str(v).startswith("=") else F_IN, fmt, None if str(v).startswith("=") else AMAR,
      CENTRO if l == 6 else None)
    c(pp, f"C{l}", fonte, al=QUEBRA)
    pp.merge_cells(f"C{l}:I{l}")
    pp.row_dimensions[l].height = 28
COLS = "CDEFGH"
cab(pp, 29, ["Item", "Como se calcula"] + ORD + ["Total"], 44)
TC_A = {"Oeste": "Ceilândia", "Sudoeste": "Taguatinga", "Norte": "Sobradinho", "Leste": "São Sebastião",
        "Central e Centro-Sul": "Plano Piloto", "Sul": "Gama"}
PRECO_TC = {"Oeste": 175, "Sudoeste": 165, "Norte": 165, "Leste": 175, "Central e Centro-Sul": 175, "Sul": 175}


def secao(l, titulo):
    c(pp, f"A{l}", titulo, F_CAB, fill=CAB)
    pp.merge_cells(f"A{l}:I{l}")


def linha(l, rot, conta, vals=None, form=None, total="soma", fmt=R2, neg=False, fill=None, entrada=False):
    c(pp, f"A{l}", rot, F_NEG if neg else F_TXT, al=QUEBRA, fill=fill)
    c(pp, f"B{l}", conta, F_SUB, al=QUEBRA)
    for i, col in enumerate(COLS):
        v = vals[i] if vals is not None else form.format(c=col)
        c(pp, f"{col}{l}", v, F_IN if entrada else (F_NEG if neg else F_TXT), fmt, AMAR if entrada and l == 38 else fill)
    if total == "soma":
        c(pp, f"I{l}", f"=SUM(C{l}:H{l})", F_NEG, fmt, TOT)
    elif total:
        c(pp, f"I{l}", total, F_NEG, fmt, TOT)
    pp.row_dimensions[l].height = 30


secao(30, "Volumes")
linha(31, "Exames de ultrassom", "plano v24, pela origem das solicitações", vals=[P[x]["us"] for x in ORD], fmt=N0, entrada=True)
linha(32, "Exames de tomografia no plano A", "estudo dos polos: Samambaia e Recanto das Emas a Ceilândia",
      vals=[round(PC["tc6"]["por_sede"].get(TC_A[x], 0)) for x in ORD], fmt=N0, entrada=True)
linha(33, "Exames de tomografia no plano B", "a Leste à Asa Sul; o Itapoã a Sobradinho",
      vals=[round(PC["tc5"]["por_sede"].get(TC_A[x], 0)) for x in ORD], fmt=N0, entrada=True)
linha(34, "Exames de tomografia no plano escolhido", "B6 = A: linha 32; B: linha 33", form='=IF($B$6="B",{c}33,{c}32)', fmt=N0)
linha(35, "Exames no polo", "ultrassom + tomografia", form="={c}31+{c}34", fmt=N0, neg=True)
linha(36, "Parte do polo nos exames", "exames do polo ÷ total (chave do rateio)", form="={c}35/$I$35", fmt=PCT)
linha(37, "Salas de ultrassom", "plano v24, 7.3", vals=[P[x]["salas"] for x in ORD], fmt=N0, entrada=True)
linha(38, "Preço da tomografia na clínica, por exame (R$)", "rede do ISHP; as a definir no teto de R$ 175",
      vals=[PRECO_TC[x] for x in ORD], total=None, entrada=True)
secao(40, "Conta 1 — linha de atendimento, do agendamento ao faturamento (sem direção, coordenações nem supervisores)")
linha(41, "Aluguel das salas de ultrassom", "salas × aluguel por sala × meses", form="={c}37*$B$7*$B$5")
linha(42, "Aluguel dos aparelhos de ultrassom", "salas × parte com aparelho × aluguel do aparelho × meses",
      form="={c}37*$B$9*$B$8*$B$5")
linha(43, "Médicos de ultrassom", "exames de ultrassom × médico por exame", form="={c}31*$B$10")
linha(44, "Recepcionistas", "recepcionistas por polo × custo × meses", form="=$B$11*$B$12*$B$5")
linha(45, "Insumos do ultrassom", "exames de ultrassom × insumos", form="={c}31*$B$13")
linha(46, "Outros custos do polo", "custo por mês × meses", form="=$B$14*$B$5")
linha(47, "Tomografia feita na clínica (tudo incluído: tomógrafo, técnico, enfermagem, contraste, laudo)",
      "exames de tomografia × preço da clínica", form="={c}34*{c}38")
linha(48, "Operadores do pré-exame, rateados", "operadores × custo × meses × parte do polo", form="=$B$15*$B$17*$B$5*{c}36")
linha(49, "Operadores do pós-exame, rateados", "operadores × custo × meses × parte do polo", form="=$B$16*$B$17*$B$5*{c}36")
linha(50, "Total da linha de atendimento", "soma das linhas 41 a 49", form="=SUM({c}41:{c}49)", neg=True, fill=TOT)
OPX = "($B$15+$B$16)*$B$17*$B$5/$I$35"
linha(51, "Custo por exame de ultrassom — linha (R$)", "(linhas 41 a 46) ÷ exames de ultrassom + operadores por exame",
      form="=SUM({c}41:{c}46)/{c}31+" + OPX, total="=SUM(C41:H46)/I31+" + OPX, neg=True, fill=DEST)
linha(52, "Custo por exame de tomografia — linha (R$)", "preço da clínica + operadores por exame",
      form='=IF({c}34=0,"sem tomografia",{c}38+' + OPX + ")", total="=I47/I34+" + OPX, neg=True, fill=DEST)
linha(53, "Custo médio por exame do polo — linha (R$)", "total da linha ÷ exames do polo", form="={c}50/{c}35",
      total="=I50/I35", neg=True, fill=DEST)
secao(55, "Conta 2 — tudo: a linha de atendimento mais direção, coordenações, supervisores, assistentes e assessoria")
linha(56, "Direção Executiva de Projeto, rateada", "custo × meses × parte do polo", form="=$B$18*$B$5*{c}36")
linha(57, "Coordenação Operacional, rateada", "custo × meses × parte do polo", form="=$B$19*$B$5*{c}36")
linha(58, "Coordenação Assistencial, rateada", "custo × meses × parte do polo", form="=$B$20*$B$5*{c}36")
linha(59, "Coordenação Administrativa e Financeira, rateada", "custo × meses × parte do polo", form="=$B$21*$B$5*{c}36")
linha(60, "Supervisão de Polo: meio supervisor por polo", "0,5 × custo × meses", form="=0.5*$B$22*$B$5")
linha(61, "Assistente Administrativo: um por polo", "custo × meses", form="=$B$23*$B$5")
linha(62, "Assessoria de Prestação de Contas, rateada", "custo × meses × parte do polo", form="=$B$24*$B$5*{c}36")
linha(63, "Total de gestão e apoio (sem os operadores, que estão na conta 1)", "soma das linhas 56 a 62",
      form="=SUM({c}56:{c}62)", neg=True, fill=TOT)
linha(64, "Total geral: linha de atendimento + gestão e apoio", "linha 50 + linha 63", form="={c}50+{c}63", neg=True, fill=TOT)
linha(65, "Custo médio por exame do polo — tudo (R$)", "total geral ÷ exames do polo", form="={c}64/{c}35",
      total="=I64/I35", neg=True, fill=DEST)
secao(67, "O que o convênio paga, e a folga")
linha(68, "Produção de ultrassom", "exames de ultrassom × valor do convênio", form="={c}31*$B$25")
linha(69, "Produção de tomografia", "exames de tomografia × valor do convênio", form="={c}34*$B$26")
linha(70, "Apoio, rateado", "apoio do convênio × parte do polo", form="=$B$27*{c}36")
linha(71, "Total que o convênio paga ao polo", "linhas 68 a 70", form="=SUM({c}68:{c}70)", neg=True, fill=TOT)
linha(72, "Folga da conta 1: produção − linha de atendimento (os operadores, pagos pelo apoio, entram aqui como custo)",
      "linhas 68 + 69 − linha 50", form="={c}68+{c}69-{c}50",
      neg=True, fill=DEST)
linha(73, "Folga da conta 2: tudo o que o convênio paga − tudo o que se gasta", "linha 71 − linha 64",
      form="={c}71-{c}64", neg=True, fill=DEST)
linha(74, "Custo da linha ÷ produção", "linha 50 ÷ (linhas 68 + 69)", form="={c}50/({c}68+{c}69)",
      total="=I50/(I68+I69)", fmt=PCT)
linha(75, "Custo total ÷ tudo o que o convênio paga", "linha 64 ÷ linha 71", form="={c}64/{c}71", total="=I64/I71", fmt=PCT)
txt(pp, 77, "Como ler: o que é centralizado (operadores, direção, coordenações, assessoria) se reparte pelos exames de cada "
    "polo; o supervisor conta meio por polo e o assistente, um. A tomografia entra pelo preço da clínica, que já inclui "
    "tomógrafo, técnico, enfermagem, contraste e laudo; feita por equipe própria ela sai mais cara (aba Tomografia). A folga não "
    "é receita do ISHP: no convênio, o que não se gasta no objeto volta como saldo ou vira mais exames por termo aditivo.",
    "I", h=58)
larg(pp, [46, 30, 13, 13, 13, 13, 15, 13, 15])
pp.freeze_panes = "C30"

# ------------------------------------------------------------------ Resumo
c(r, "A1", "Quanto custa um exame para o ISHP: primeira noção", F_TIT, borda=False)
c(r, "A2", "Controle interno de 20/10/2026, sobre a v24 (79.152 exames em 8 meses). Não vai ao plano nem aos parceiros.",
  F_SUB, borda=False)
cab(r, 4, ["", "O convênio paga, por exame (R$)", "Custo por exame: econômico (R$)", "Custo por exame: conservador (R$)",
           "Custo como parte do que o convênio paga", "Folga no projeto: econômico (R$)", "Folga no projeto: conservador (R$)"], 54)
LIN = [
    (5, "Ultrassom — execução própria (aluguel e médico)", f"={UA}B24", f"={UA}B23", f"={UA}C23", f"={UA}B26 & \" a \" & ", f"={UA}B27", f"={UA}C27"),
]
c(r, "A5", "Ultrassom — execução própria (aluguel e médico)", F_NEG, al=QUEBRA)
c(r, "B5", f"={UA}B24", F_VERDE, R2)
c(r, "C5", f"={UA}B23", F_VERDE, R2, DEST)
c(r, "D5", f"={UA}C23", F_VERDE, R2, DEST)
c(r, "E5", f'=TEXT({UA}B26,"0%")&" a "&TEXT({UA}C26,"0%")', F_VERDE, al=CENTRO)
c(r, "F5", f"={UA}B27", F_VERDE, R2)
c(r, "G5", f"={UA}C27", F_VERDE, R2)
for l, rot, col, extra in [(6, "Tomografia — clínicas, plano de 6 polos", "B", ""), (7, "Tomografia — clínicas, plano de 5 polos", "C", "")]:
    c(r, f"A{l}", rot, F_NEG, al=QUEBRA)
    c(r, f"B{l}", f"={TA}{col}25", F_VERDE, R2)
    c(r, f"C{l}", f"={TA}{col}24", F_VERDE, R2, DEST)
    c(r, f"D{l}", f"={TA}{col}28", F_VERDE, R2, DEST)
    c(r, f"E{l}", f'=TEXT({TA}{col}24/{TA}{col}25,"0%")&" a "&TEXT({TA}{col}28/{TA}{col}25,"0%")', F_VERDE, al=CENTRO)
    c(r, f"F{l}", f"={TA}{col}29", F_VERDE, R2)
    c(r, f"G{l}", f"={TA}{col}29-{TA}$B$33*{TA}$B$32*{TA}$C${LT['tc6']}", F_VERDE, R2)
c(r, "A8", "Ultrassom — aluguel como negociado (2 salas por polo, sem as salas a mais)", F_NEG, al=QUEBRA)
c(r, "B8", f"={UA}B24", F_VERDE, R2)
c(r, "C8", f"={UA}C52", F_VERDE, R2, DEST)
c(r, "D8", "")
c(r, "E8", f'=TEXT({UA}C52/{UA}B24,"0%")', F_VERDE, al=CENTRO)
c(r, "F8", f"=({UA}B24-{UA}C52)*{UA}B5", F_VERDE, R2)
c(r, "G8", "")
for l in (5, 6, 7, 8):
    r.row_dimensions[l].height = 30
c(r, "A9", "Conservador da tomografia = a clínica cobrar o contraste à parte (R$ 60 em 95% dos exames).", F_SUB, borda=False)
r.merge_cells("A9:G9")
cab(r, 11, ["Por polo (aba Por polo): custo médio por exame", ""] + ORD + ["Total"], 44)
for k, (rot, lin) in enumerate([("Conta 1 — linha de atendimento (R$)", 53), ("Conta 2 — tudo, com gestão e apoio (R$)", 65),
                                ("O convênio paga, em média, por exame do polo (R$)", None)]):
    l = 12 + k
    c(r, f"A{l}", rot, F_NEG, al=QUEBRA)
    r.merge_cells(f"A{l}:B{l}")
    for i, col in enumerate("CDEFGH" + "I"):
        dest = "CDEFGHI"[i]
        fm = f"={PA}{col}{lin}" if lin else f"=({PA}{col}68+{PA}{col}69)/{PA}{col}35"
        c(r, f"{dest}{l}", fm, F_VERDE, R2, DEST if lin else None)
    r.row_dimensions[l].height = 30
NOTAS = [
    "Como ler",
    "• Ultrassom: o custo vai de cerca de R$ 44 a R$ 61 por exame, contra R$ 100 que o convênio paga. O que mais pesa é o "
    "médico (R$ 33 a R$ 40). Aluguel e aparelho somam de R$ 7 a R$ 13. Como negociado (R$ 6.000 por polo), o aluguel sai a "
    "menos de R$ 5 por exame, mas cobre 12 das 20 salas que o plano pede (aba Ultrassom, embaixo).",
    "• Tomografia: comprar o exame da clínica a R$ 165–175, com contraste incluído, custa pouco mais da metade do que o "
    "convênio paga (R$ 300). Se o contraste vier à parte, o custo sobe uns R$ 57.",
    "• Fazer a tomografia com equipe própria não compensa: só a equipe, o laudo, o contraste e os insumos já passam do preço "
    "da clínica, antes de pagar sala e tomógrafo. A equipe por tomógrafo é fixa, e cada tomógrafo fica com pouca carga.",
    "• A folga não é receita do ISHP. No convênio, o que não se gasta no objeto volta como saldo, ou vira mais exames por "
    "termo aditivo (7.6 do plano; IN CGDF 01/2005). E a equipe de gestão e apoio (R$ 954.560,00) é paga à parte, fora destes "
    "custos.",
    "• Ficam fora da conta: impostos sobre os contratos com pessoa jurídica, sistema de imagem e laudo do ultrassom (quando "
    "não vem com o médico), deslocamento, perdas por exame repetido e os meses sem paciente se a regulação atrasar.",
]
for i, tx in enumerate(NOTAS):
    txt(r, 16 + i, tx, "G", F_NEG if i == 0 else F_TXT, 16 if i == 0 else 32)
larg(r, [40, 15, 15, 15, 16, 17, 17, 14, 14])

# ------------------------------------------------------------------ Fontes
c(f, "A1", "Fontes e premissas", F_TIT, borda=False)
FON = [
    "Exames, salas, valor pago pelo convênio e exames com contraste: plano v24 (calculo_v24/v24.json).",
    "Divisão da tomografia por clínica: calculo_v24/polos_capacidade.json (estudo dos polos de 20/10/2026).",
    "Aluguel (R$ 3.000 por sala), aparelho (R$ 2.500 por mês), médico por lote (R$ 1.000 por 30 ou R$ 4.000 por 100) e preços "
    "de tomografia (R$ 165 a R$ 175, contraste incluído): plano de execução e planilhas da rede do ISHP, recebidos em 20/10/2026.",
    "Recepcionista de consultório (custo R$ 2.959) e técnico de enfermagem (custo R$ 4.945) em Brasília: salario.com.br, "
    "acesso em 20/10/2026. Técnico em radiologia: média nacional R$ 2.866 (a página de Brasília é paga), × 1,7 de encargos.",
    "Médico ultrassonografista por salário: IgesDF, Edital 070/2026, R$ 18.115,68 por 24 h semanais (Sou Brasília, 15/07/2026).",
    "Laudo de tomografia: pregão de Garça/SP, 2026, estimativa de R$ 60 por laudo (pesquisa de R$ 40 a R$ 80).",
    "Contraste: referência do SUS, 02.06.03.004-5, R$ 60,00 (Portaria SAES/MS 4.282/2026, Anexo II).",
    "Insumos do ultrassom (R$ 3) e da tomografia com contraste (R$ 20): hipóteses, sem cotação. Trocar pelo que a operação "
    "medir.",
]
for i, tx in enumerate(FON):
    txt(f, 3 + i, "• " + tx, "F", h=32)
larg(f, [30, 30, 30, 30, 30, 30])

for ws in wb.worksheets:
    ws.sheet_view.showGridLines = False
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
wb.save(SAIDA)
print("ok", SAIDA)
