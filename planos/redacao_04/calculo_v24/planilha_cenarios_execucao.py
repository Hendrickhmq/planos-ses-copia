"""Quanto custa executar o plano 4, em tres cenarios (20/10/2026, v2 do custo por exame): controle interno.

1. tudo nas clinicas: o ultrassom pago por exame (50% do valor do convenio, a planilha aos parceiros de 16/10/2026) e a
   tomografia pelo preco negociado;
2. ultrassom feito por nos nos 6 polos: aluguel de sala e de aparelho, medico por exame, recepcionistas e insumos; a
   tomografia nas clinicas;
3. misto: o ultrassom feito por nos nos polos marcados (amarelo) e pelas clinicas nos outros.
A equipe de agenda e faturamento e a de gestao sao as do plano nos tres. Le v24.json e polos_capacidade.json.

Uso: python3 planilha_cenarios_execucao.py v24.json polos_capacidade.json ../estudos/custo_por_exame_v2_20261020.xlsx
"""
import json, sys
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter as COL
from openpyxl.worksheet.datavalidation import DataValidation

V = json.load(open(sys.argv[1]))
PC = json.load(open(sys.argv[2]))
SAIDA = sys.argv[3]

A = "Arial"
F_TIT = Font(name=A, size=15, bold=True, color="1F4E79")
F_SEC = Font(name=A, size=11, bold=True, color="1F4E79")
F_SUB = Font(name=A, size=10, italic=True, color="595959")
F_TXT = Font(name=A, size=10)
F_NEG = Font(name=A, size=10, bold=True)
F_GRANDE = Font(name=A, size=11, bold=True)
F_IN = Font(name=A, size=10, color="0000FF")
F_LINK = Font(name=A, size=10, color="008000")
F_CAB = Font(name=A, size=10, bold=True, color="FFFFFF")
CAB = PatternFill("solid", fgColor="1F4E79")
AMAR = PatternFill("solid", fgColor="FFF2CC")
CINZA = PatternFill("solid", fgColor="F2F2F2")
AZUL = PatternFill("solid", fgColor="DDEBF7")
VERDE = PatternFill("solid", fgColor="E2EFDA")
L = Side(style="thin", color="BFBFBF")
B = Border(left=L, right=L, top=L, bottom=L)
R0 = '#,##0;(#,##0);"-"'
R2 = '#,##0.00;(#,##0.00);"-"'
PCT = '0%'
ESQ = Alignment(wrap_text=True, vertical="center")
CEN = Alignment(horizontal="center", vertical="center", wrap_text=True)
DIR = Alignment(horizontal="right", vertical="center")
wb = Workbook()


def c(ws, ref, v, f=F_TXT, fmt=None, fill=None, al=None, borda=True):
    x = ws[ref]
    x.value = v
    x.font = f
    if fmt: x.number_format = fmt
    if fill: x.fill = fill
    x.alignment = al or (DIR if isinstance(v, (int, float)) or (isinstance(v, str) and v.startswith("=")) else ESQ)
    if borda: x.border = B
    return x


def cab(ws, linha, textos, col0=1, h=36):
    for i, t in enumerate(textos):
        c(ws, f"{COL(col0 + i)}{linha}", t, F_CAB, fill=CAB, al=CEN)
    ws.row_dimensions[linha].height = h


def texto(ws, linha, t, ate, f=F_TXT, h=None):
    c(ws, f"A{linha}", t, f, al=ESQ, borda=False)
    ws.merge_cells(f"A{linha}:{ate}{linha}")
    if h: ws.row_dimensions[linha].height = h


def larg(ws, ls):
    for i, w in enumerate(ls):
        ws.column_dimensions[COL(i + 1)].width = w


ORD, P = V["ORD"], V["polos"]
US, TC = V["us_total"], V["tc_total"]
M4 = sum(V["qc"][k] * {"02.05.01.004-0": 100.18, "02.05.02.004-6": 100.18}.get(k, 99.94) for k in V["qc"] if k.startswith("02.05"))
M5 = sum(V["qc"][k] * (300.10 if k == "02.06.02.003-1" else 299.44) for k in V["qc"] if k.startswith("02.06"))

cen = wb.active
cen.title = "Cenários"
us = wb.create_sheet("Ultrassom por polo")
tc = wb.create_sheet("Tomografia por polo")
eq = wb.create_sheet("Equipe")
pr = wb.create_sheet("Premissas")
PR, US_, TC_, EQ = "Premissas!", "'Ultrassom por polo'!", "'Tomografia por polo'!", "Equipe!"

# ================================================================== Premissas
c(pr, "A1", "Premissas", F_TIT, borda=False)
c(pr, "A2", "As células amarelas são premissas: mude e as outras abas se refazem.", F_SUB, borda=False)
PREM = [
    ("Geral", None),
    ("Meses de execução", (8, R0, "plano v24")),
    ("Plano de tomografia: A (6 polos com tomógrafo) ou B (5 polos, a Leste sem)", ("A", None, "escreva A ou B")),
    ("Ultrassom feito por nós (alugando sala e aparelho)", None),
    ("Aluguel de uma sala por mês (R$)", (3000, R2, "rede do ISHP: R$ 6.000 por polo com 2 salas, recepção e guichê")),
    ("Aluguel de um aparelho de ultrassom por mês (R$)", (2500, R2, "rede do ISHP: opção mapeada em Samambaia, com manutenção")),
    ("Parte das salas em que alugamos o aparelho", (1, PCT, "100% = alugamos o aparelho de toda sala; 0% = a clínica ou o médico traz o aparelho")),
    ("Médico de ultrassom, por exame (R$)", (33.33, R2, "modelo do ISHP: R$ 1.000 por lote de 30 exames (R$ 40 no lote de 100)")),
    ("Recepcionistas em cada polo", (2, R0, "plano, 4.15: o polo fica aberto 50 h por semana")),
    ("Custo de um recepcionista por mês (R$)", (2959, R2, "salario.com.br, Recepcionista de consultório, Brasília, custo para a empresa")),
    ("Insumos por exame (R$)", (3, R2, "hipótese: gel, papel, lençol, capa do transdutor, desinfecção")),
    ("Outros custos de cada polo por mês: limpeza, energia, internet, sistema de imagem (R$)", (0, R2, "a confirmar se vêm no aluguel")),
    ("Ultrassom feito pela clínica (pagamos por exame)", None),
    ("Parte do valor do convênio paga à clínica", (0.5, PCT, "planilha de valores aos parceiros, 16/10/2026: 50%")),
    ("O que o convênio paga", None),
    ("Por exame de ultrassom, em média (R$)", (round(M4 / US, 6), R2, "plano v24, Meta 4 ÷ exames de ultrassom")),
    ("Por exame de tomografia, em média (R$)", (round(M5 / TC, 6), R2, "plano v24, Meta 5 ÷ exames de tomografia")),
]
REF = {}
l = 4
for rot, val in PREM:
    if val is None:
        c(pr, f"A{l}", rot, F_SEC, borda=False)
        pr.row_dimensions[l].height = 22
    else:
        v, fmt, fonte = val
        c(pr, f"A{l}", rot)
        c(pr, f"B{l}", v, F_IN, fmt, AMAR, CEN if isinstance(v, str) else None)
        c(pr, f"C{l}", fonte, F_SUB)
        REF[rot] = f"{PR}$B${l}"
    l += 1
larg(pr, [62, 14, 80])
MESES = REF["Meses de execução"]
PLANO = REF["Plano de tomografia: A (6 polos com tomógrafo) ou B (5 polos, a Leste sem)"]
SALA, APAR = REF["Aluguel de uma sala por mês (R$)"], REF["Aluguel de um aparelho de ultrassom por mês (R$)"]
PARTE_AP, MED = REF["Parte das salas em que alugamos o aparelho"], REF["Médico de ultrassom, por exame (R$)"]
NREC, CREC = REF["Recepcionistas em cada polo"], REF["Custo de um recepcionista por mês (R$)"]
INS, OUT = REF["Insumos por exame (R$)"], REF["Outros custos de cada polo por mês: limpeza, energia, internet, sistema de imagem (R$)"]
PARTE_CL = REF["Parte do valor do convênio paga à clínica"]
VUS, VTC = REF["Por exame de ultrassom, em média (R$)"], REF["Por exame de tomografia, em média (R$)"]

# ================================================================== Ultrassom por polo
c(us, "A1", "Ultrassom por polo: feito por nós ou pela clínica", F_TIT, borda=False)
c(us, "A2", "Feito por nós: alugamos a sala e o aparelho e pagamos o médico e a recepção. Feito pela clínica: pagamos um preço "
  "por exame. A última coluna diz quem faz em cada polo no cenário misto.", F_SUB, borda=False)
us.merge_cells("A2:P2")
c(us, "E4", "Feito por nós", F_CAB, fill=CAB, al=CEN)
us.merge_cells("E4:L4")
c(us, "M4", "Feito pela clínica", F_CAB, fill=CAB, al=CEN)
us.merge_cells("M4:N4")
cab(us, 5, ["Polo", "Unidade mapeada", "Exames de ultrassom", "Salas", "Aluguel das salas", "Aluguel dos aparelhos",
            "Médicos", "Recepcionistas", "Insumos", "Outros custos", "Total", "Por exame", "Preço por exame", "Total",
            "Diferença por exame (nós − clínica)", "Quem faz no cenário misto"], h=48)
UNI = {"Oeste": "Ceilândia — Clínica Brasília", "Sudoeste": "Samambaia — Med Saúde", "Norte": "Sobradinho — Clínica Padrão",
       "Leste": "São Sebastião — GPAES/HPAES", "Central e Centro-Sul": "Asa Sul (DaVida) ou bairro Sudoeste (Ana Maia)",
       "Sul": "Gama — CIG"}
MISTO = {"Sudoeste": "nós", "Sul": "nós", "Leste": "nós"}
dv = DataValidation(type="list", formula1='"nós,clínica"', allow_blank=False)
us.add_data_validation(dv)
for i, x in enumerate(ORD):
    l = 6 + i
    c(us, f"A{l}", x, F_NEG)
    c(us, f"B{l}", UNI[x], F_TXT)
    c(us, f"C{l}", P[x]["us"], F_IN, R0)
    c(us, f"D{l}", P[x]["salas"], F_IN, R0, al=CEN)
    c(us, f"E{l}", f"=D{l}*{SALA}*{MESES}", fmt=R0)
    c(us, f"F{l}", f"=D{l}*{PARTE_AP}*{APAR}*{MESES}", fmt=R0)
    c(us, f"G{l}", f"=C{l}*{MED}", fmt=R0)
    c(us, f"H{l}", f"={NREC}*{CREC}*{MESES}", fmt=R0)
    c(us, f"I{l}", f"=C{l}*{INS}", fmt=R0)
    c(us, f"J{l}", f"={OUT}*{MESES}", fmt=R0)
    c(us, f"K{l}", f"=SUM(E{l}:J{l})", F_NEG, R0, AZUL)
    c(us, f"L{l}", f"=K{l}/C{l}", F_NEG, R2, AZUL)
    c(us, f"M{l}", f"={VUS}*{PARTE_CL}", fmt=R2)
    c(us, f"N{l}", f"=C{l}*M{l}", F_NEG, R0, AZUL)
    c(us, f"O{l}", f"=L{l}-M{l}", F_NEG, R2, VERDE)
    c(us, f"P{l}", MISTO.get(x, "clínica"), F_IN, fill=AMAR, al=CEN)
    dv.add(f"P{l}")
    us.row_dimensions[l].height = 28
LU = 12
c(us, f"A{LU}", "Total", F_GRANDE, fill=CINZA)
c(us, f"B{LU}", "", fill=CINZA)
for col in "CDEFGHIJK":
    c(us, f"{col}{LU}", f"=SUM({col}6:{col}11)", F_GRANDE, R0, CINZA)
c(us, f"L{LU}", f"=K{LU}/C{LU}", F_GRANDE, R2, CINZA)
c(us, f"M{LU}", f"=N{LU}/C{LU}", F_GRANDE, R2, CINZA)
c(us, f"N{LU}", f"=SUM(N6:N11)", F_GRANDE, R0, CINZA)
c(us, f"O{LU}", f"=L{LU}-M{LU}", F_GRANDE, R2, CINZA)
c(us, f"P{LU}", f'=COUNTIF(P6:P11,"nós")&" por nós"', F_GRANDE, fill=CINZA, al=CEN)
texto(us, 14, "Diferença positiva: fazer nós mesmos sai mais caro que pagar a clínica. O que mais pesa no \"feito por nós\" é o "
      "médico; o aparelho alugado e a recepção fixa pesam mais nos polos pequenos (Oeste e Norte). Se a clínica ou o médico "
      "trouxer o aparelho (Premissas, parte das salas = 0%), fazer nós mesmos fica mais barato nos polos grandes.", "P", h=44)
larg(us, [20, 36, 11, 7, 12, 12, 12, 13, 10, 10, 13, 10, 10, 13, 13, 12])
us.freeze_panes = "C6"

# ================================================================== Tomografia por polo
c(tc, "A1", "Tomografia por polo: sempre na clínica", F_TIT, borda=False)
c(tc, "A2", "A clínica cobra por exame, com tomógrafo, técnico, enfermagem, contraste e laudo. Fazer com equipe própria sai mais "
  "caro (versão 1 desta planilha, aba Tomografia).", F_SUB, borda=False)
tc.merge_cells("A2:G2")
cab(tc, 4, ["Tomógrafo", "Exames no plano A", "Exames no plano B", "Exames no plano escolhido", "Preço por exame (R$)",
            "Custo (R$)", "Quem recebe os pacientes"], h=40)
NOME = {"Ceilândia": ("Ceilândia — Clínica Brasília", 175, "Oeste, Samambaia e Recanto das Emas"),
        "Taguatinga": ("Taguatinga — Clínica Padrão", 165, "o resto da Sudoeste"),
        "Plano Piloto": ("Central e Centro-Sul — a definir", 175, "Central e Centro-Sul; no plano B, também a Leste (sem o Itapoã)"),
        "Sobradinho": ("Sobradinho — Clínica Padrão", 165, "Norte; no plano B, também o Itapoã"),
        "Gama": ("Gama — CIG", 175, "Sul"),
        "São Sebastião": ("Leste — a definir", 175, "Leste; no plano B, não há")}
for i, sd in enumerate(["Ceilândia", "Taguatinga", "Plano Piloto", "Sobradinho", "Gama", "São Sebastião"]):
    l = 5 + i
    nome, preco, quem = NOME[sd]
    c(tc, f"A{l}", nome, F_NEG)
    c(tc, f"B{l}", round(PC["tc6"]["por_sede"].get(sd, 0)), F_IN, R0)
    c(tc, f"C{l}", round(PC["tc5"]["por_sede"].get(sd, 0)), F_IN, R0)
    c(tc, f"D{l}", f'=IF({PLANO}="B",C{l},B{l})', fmt=R0)
    c(tc, f"E{l}", preco, F_IN, R2, AMAR)
    c(tc, f"F{l}", f"=D{l}*E{l}", F_NEG, R0, AZUL)
    c(tc, f"G{l}", quem, F_SUB)
    tc.row_dimensions[l].height = 28
LT = 11
c(tc, f"A{LT}", "Total", F_GRANDE, fill=CINZA)
for col in "BCDF":
    c(tc, f"{col}{LT}", f"=SUM({col}5:{col}10)", F_GRANDE, R0, CINZA)
c(tc, f"E{LT}", f"=F{LT}/D{LT}", F_GRANDE, R2, CINZA)
c(tc, f"G{LT}", "preço médio na coluna E", F_SUB, fill=CINZA)
texto(tc, 13, "Preços da planilha da rede de tomografia do ISHP: Clínica Padrão R$ 165; CIG e Clínica Brasília R$ 175; as "
      "clínicas a definir, no teto de R$ 175. A condição é o contraste incluído: cobrado à parte, são cerca de R$ 57 a mais por "
      "exame.", "G", h=30)
larg(tc, [34, 12, 12, 13, 12, 14, 52])

# ================================================================== Equipe
c(eq, "A1", "Equipe do plano: igual nos três cenários", F_TIT, borda=False)
c(eq, "A2", "Paga pelo apoio do convênio (R$ 954.560,00 no plano). Quantidades e preços do quadro decidido em 20/10/2026.",
  F_SUB, borda=False)
cab(eq, 4, ["Grupo", "Cargo", "Quantidade", "Custo por mês, cada (R$)", "Custo no período (R$)"], h=36)
EQUIPE = [
    ("Agenda e faturamento", "Operador de registro — pré-exame (agenda no SISREG, contato, confirmação, busca ativa)", 4, 4300),
    ("Agenda e faturamento", "Operador de registro — pós-exame (TrakCare, APAC, faturamento)", 4, 4300),
    ("Gestão", "Direção Executiva de Projeto", 1, 14500),
    ("Gestão", "Coordenação Operacional", 1, 8400),
    ("Gestão", "Coordenação Assistencial", 1, 10500),
    ("Gestão", "Coordenação Administrativa e Financeira", 1, 8400),
    ("Gestão", "Supervisão de Polo (uma para cada dois polos)", 3, 6155),
    ("Gestão", "Assistente Administrativo (um por polo, documentação)", 6, 3200),
    ("Gestão", "Assessoria de Prestação de Contas (serviço)", 1, 5455),
]
for i, (g, cargo, qtd, v) in enumerate(EQUIPE):
    l = 5 + i
    c(eq, f"A{l}", g, F_NEG if i in (0, 2) else F_SUB)
    c(eq, f"B{l}", cargo)
    c(eq, f"C{l}", qtd, F_IN, R0, AMAR, CEN)
    c(eq, f"D{l}", v, F_IN, R2, AMAR)
    c(eq, f"E{l}", f"=C{l}*D{l}*{MESES}", fmt=R0)
    eq.row_dimensions[l].height = 26
for l, rot, fm in [(15, "Agenda e faturamento", "=SUM(E5:E6)"), (16, "Gestão", "=SUM(E7:E13)"),
                   (17, "Equipe inteira (= o apoio do convênio)", "=E15+E16")]:
    c(eq, f"A{l}", rot, F_GRANDE, fill=CINZA)
    eq.merge_cells(f"A{l}:D{l}")
    c(eq, f"E{l}", fm, F_GRANDE, R0, CINZA)
larg(eq, [24, 72, 12, 16, 18])

# ================================================================== Cenários
c(cen, "A1", "Quanto custa executar o plano: três cenários", F_TIT, borda=False)
c(cen, "A2", "Uso interno, sobre o plano v24: 79.152 exames em 8 meses (65.530 de ultrassom e 13.622 de tomografia).", F_SUB, borda=False)
cen.merge_cells("A2:D2")
LEIA = [
    "Tudo nas clínicas: pagamos o ultrassom por exame (50% do valor do convênio, como na planilha aos parceiros) e a tomografia "
    "pelo preço negociado.",
    "Ultrassom feito por nós nos 6 polos: alugamos sala e aparelho e pagamos médico e recepção em todos os polos. A tomografia "
    "fica nas clínicas.",
    "Misto: o ultrassom é feito por nós nos polos marcados na aba Ultrassom por polo (última coluna, amarela) e pelas clínicas "
    "nos outros. Hoje estão marcados os três maiores: Sudoeste, Sul e Leste.",
]
for i, tx in enumerate(LEIA):
    texto(cen, 4 + i, f"{i + 1}. {tx}", "D", h=30)
NC3 = f'="3. Misto: ultrassom feito por nós em "&COUNTIF({US_}P6:P11,"nós")&" polos"'
cab(cen, 8, ["", "1. Tudo nas clínicas", "2. Ultrassom feito por nós nos 6 polos", "3. Misto"], h=44)
c(cen, "D8", NC3, F_CAB, fill=CAB, al=CEN)
MISTO_US = (f'=SUMPRODUCT(({US_}P6:P11="nós")*{US_}K6:K11)+SUMPRODUCT(({US_}P6:P11<>"nós")*{US_}N6:N11)')
LIN = [
    ("sec", "Os exames"),
    (10, "Ultrassom (R$)", f"={US_}N12", f"={US_}K12", MISTO_US, R0, False),
    (11, "    por exame (R$)", "=B10/{us}".format(us=US), "=C10/{us}".format(us=US), "=D10/{us}".format(us=US), R2, False),
    (12, "Tomografia, nas clínicas (R$)", f"={TC_}F11", f"={TC_}F11", f"={TC_}F11", R0, False),
    (13, "    por exame (R$)", "=B12/{tc}".format(tc=TC), "=C12/{tc}".format(tc=TC), "=D12/{tc}".format(tc=TC), R2, False),
    (14, "Custo dos exames (R$)", "=B10+B12", "=C10+C12", "=D10+D12", R0, True),
    ("sec", "A equipe (igual nos três)"),
    (16, "Agenda e faturamento: 8 operadores (R$)", f"={EQ}E15", f"={EQ}E15", f"={EQ}E15", R0, False),
    (17, "Gestão: direção, coordenações, supervisores, assistentes e assessoria (R$)", f"={EQ}E16", f"={EQ}E16", f"={EQ}E16", R0, False),
    (18, "Custo da equipe (R$)", "=B16+B17", "=C16+C17", "=D16+D17", R0, True),
    ("sec", "O resultado"),
    (20, "Custo total (R$)", "=B14+B18", "=C14+C18", "=D14+D18", R0, True),
    (21, "O convênio paga pelos exames (R$)", f"={US}*{VUS}+{TC}*{VTC}", f"={US}*{VUS}+{TC}*{VTC}", f"={US}*{VUS}+{TC}*{VTC}", R0, False),
    (22, "O convênio paga pela equipe (R$)", f"={EQ}E17", f"={EQ}E17", f"={EQ}E17", R0, False),
    (23, "O convênio paga no total (R$)", "=B21+B22", "=C21+C22", "=D21+D22", R0, True),
    (24, "Sobra (R$)", "=B23-B20", "=C23-C20", "=D23-D20", R0, True),
    (25, "Custo total ÷ o que o convênio paga", "=B20/B23", "=C20/C23", "=D20/D23", PCT, False),
]
l = 9
for item in LIN:
    if item[0] == "sec":
        c(cen, f"A{l}", item[1], F_SEC, borda=False)
        cen.row_dimensions[l].height = 22
        l += 1
        continue
    ln, rot, b, cc, dd, fmt, neg = item
    assert ln == l, (ln, l)
    fill = VERDE if ln == 24 else (CINZA if neg else None)
    c(cen, f"A{l}", rot, F_GRANDE if neg else F_TXT, fill=fill)
    for col, v in zip("BCD", (b, cc, dd)):
        c(cen, f"{col}{l}", v, F_GRANDE if neg else F_LINK if "!" in str(v) else F_TXT, fmt, fill)
    cen.row_dimensions[l].height = 22
    l += 1
NOT = [
    "Como ler",
    "• A sobra não é lucro do ISHP. No convênio, o que não se gasta no objeto volta como saldo ou vira mais exames por termo "
    "aditivo (7.6 do plano; IN CGDF 01/2005).",
    "• Pagar a clínica por exame é comprar o exame, e a 4.14 do plano diz que a execução não é subcontratada. O formato do contrato "
    "precisa do jurídico do ISHP antes do protocolo.",
    "• Com o aparelho alugado em todas as salas, fazer o ultrassom nós mesmos sai mais caro que pagar a clínica a 50%. Se a clínica "
    "ou o médico trouxer o aparelho, passa a compensar nos polos grandes (aba Ultrassom por polo).",
    "• Ficam fora: impostos sobre os contratos com pessoa jurídica, deslocamento, exames repetidos e meses sem paciente se a "
    "regulação atrasar.",
]
for i, tx in enumerate(NOT):
    texto(cen, 27 + i, tx, "D", F_SEC if i == 0 else F_TXT, 18 if i == 0 else 30)
larg(cen, [62, 20, 22, 22])
cen.freeze_panes = "B9"

# ================================================================== Como cada valor foi calculado
pa = wb.create_sheet("Como cada valor foi calculado", 1)
c(pa, "A1", "Como cada valor foi calculado", F_TIT, borda=False)
c(pa, "A2", "Passo a passo do valor unitário (o que o convênio paga por exame) e do nosso custo por exame. Os números vêm das "
  "outras abas: se mudar uma premissa, eles mudam aqui também.", F_SUB, borda=False)
pa.merge_cells("A2:G2")
pa.row_dimensions[2].height = 28
TOTEX = f"({US_}C12+{TC_}D11)"


def secao(l, t):
    c(pa, f"A{l}", t, F_SEC, borda=False)
    pa.merge_cells(f"A{l}:G{l}")
    pa.row_dimensions[l].height = 24


# 1. valor unitario
secao(4, "1. O que o convênio paga por exame: o valor unitário do plano")
texto(pa, 5, "Valor da Tabela do SUS mais o incremento do Anexo I da Portaria SAES/MS nº 4.282/2026, truncado no centavo.", "G")
cab(pa, 6, ["Procedimento", "Valor de tabela (R$)", "Incremento", "Conta", "Valor unitário (R$)"], h=30)
VU = [("Ultrassonografia mamária, transvaginal, de tireoide, de próstata, de aparelho urinário e de abdômen superior", 24.20, 3.13),
      ("Ultrassonografia doppler colorido de vasos", 39.60, 1.53),
      ("Ultrassonografia de abdômen total", 37.95, 1.64),
      ("Tomografia de abdômen superior e de pelve, bacia e abdômen inferior", 138.63, 1.16),
      ("Tomografia de tórax", 136.41, 1.20)]
for i, (nome, tab, inc) in enumerate(VU):
    l = 7 + i
    c(pa, f"A{l}", nome)
    c(pa, f"B{l}", tab, F_IN, R2)
    c(pa, f"C{l}", inc, F_IN, PCT, al=CEN)
    c(pa, f"D{l}", "tabela × (1 + incremento), truncado", F_SUB)
    c(pa, f"E{l}", f"=TRUNC(B{l}*(1+C{l}),2)", F_NEG, R2, AZUL)
    pa.row_dimensions[l].height = 28
c(pa, "A12", "Média do ultrassom: Meta 4 ÷ exames de ultrassom (pesa cada código pelo seu número de exames)")
c(pa, "E12", f"={VUS}", F_NEG, R2, AZUL)
c(pa, "A13", "Média da tomografia: Meta 5 ÷ exames de tomografia")
c(pa, "E13", f"={VTC}", F_NEG, R2, AZUL)
for l in (12, 13):
    pa.merge_cells(f"A{l}:D{l}")

# 2. ultrassom na clinica
secao(15, "2. Ultrassom feito pela clínica (cenário 1)")
c(pa, "A16", "Parte do valor do convênio paga à clínica (valor oferecido aos parceiros em 16/10/2026, sem aceite)")
c(pa, "E16", f"={PARTE_CL}", F_LINK, PCT)
c(pa, "A17", "Preço por exame = parte × média do ultrassom", F_NEG)
c(pa, "E17", f"=E16*E12", F_NEG, R2, AZUL)
for l in (16, 17):
    pa.merge_cells(f"A{l}:D{l}")

# 3. ultrassom feito por nos
secao(19, "3. Ultrassom feito por nós (cenário 2): cada custo dos 8 meses ÷ exames de ultrassom")
cab(pa, 20, ["Item", "Como se calcula", "", "Total no período (R$)", "Por exame (R$)"], h=30)
pa.merge_cells("B20:C20")
ITENS = [("Sala", "salas × aluguel de uma sala por mês × meses (R$ 3.000 = R$ 6.000 por polo ÷ 2 salas; as salas são as do "
          "cálculo do plano)", "E"),
         ("Aparelho", "salas × parte com aparelho alugado × aluguel do aparelho por mês × meses", "F"),
         ("Médico", "exames × médico por exame (R$ 1.000 por lote de 30 exames = R$ 33,33)", "G"),
         ("Recepção", "recepcionistas por polo × 6 polos × custo por mês × meses (custo = salário médio em Brasília × 1,7 "
          "de encargos)", "H"),
         ("Insumos", "exames × insumos por exame (hipótese)", "I"),
         ("Outros custos do polo", "custo por mês × 6 polos × meses (zero até confirmar se vêm no aluguel)", "J")]
for i, (item, como, col) in enumerate(ITENS):
    l = 21 + i
    c(pa, f"A{l}", item, F_NEG)
    c(pa, f"B{l}", como, F_SUB)
    pa.merge_cells(f"B{l}:C{l}")
    c(pa, f"D{l}", f"={US_}{col}12", F_LINK, R0)
    c(pa, f"E{l}", f"=D{l}/{US_}C12", F_TXT, R2)
    pa.row_dimensions[l].height = 44
c(pa, "A27", "Total", F_GRANDE, fill=CINZA)
c(pa, "B27", "soma dos itens ÷ exames de ultrassom", F_SUB, fill=CINZA)
pa.merge_cells("B27:C27")
c(pa, "D27", "=SUM(D21:D26)", F_GRANDE, R0, CINZA)
c(pa, "E27", f"=D27/{US_}C12", F_GRANDE, R2, AZUL)
texto(pa, 29, "Por polo, a conta é a mesma, com o volume do polo. O que é fixo (sala, aparelho, recepção) pesa mais onde há menos "
      "exame; o que vai por exame (médico e insumos) é igual em todos.", "G", h=30)
cab(pa, 30, ["Polo", "Fixos: sala + aparelho + recepção + outros (R$)", "Por exame: médico + insumos (R$)", "Total (R$)",
             "Exames", "Custo por exame (R$)"], h=40)
for i, x in enumerate(ORD):
    l = 31 + i
    r_ = 6 + i
    c(pa, f"A{l}", x, F_NEG)
    c(pa, f"B{l}", f"={US_}E{r_}+{US_}F{r_}+{US_}H{r_}+{US_}J{r_}", F_LINK, R0)
    c(pa, f"C{l}", f"={US_}G{r_}+{US_}I{r_}", F_LINK, R0)
    c(pa, f"D{l}", f"=B{l}+C{l}", F_TXT, R0)
    c(pa, f"E{l}", f"={US_}C{r_}", F_LINK, R0)
    c(pa, f"F{l}", f"=D{l}/E{l}", F_NEG, R2, AZUL)

# 4. tomografia
secao(38, "4. Tomografia na clínica: exames de cada clínica × preço da clínica")
cab(pa, 39, ["Clínica", "Exames", "Preço por exame (R$)", "Total (R$)"], h=30)
for i in range(6):
    l = 40 + i
    r_ = 5 + i
    c(pa, f"A{l}", f"={TC_}A{r_}", F_LINK, al=ESQ)
    c(pa, f"B{l}", f"={TC_}D{r_}", F_LINK, R0)
    c(pa, f"C{l}", f"={TC_}E{r_}", F_LINK, R2)
    c(pa, f"D{l}", f"=B{l}*C{l}", F_TXT, R0)
c(pa, "A46", "Total ÷ exames = preço médio por exame", F_GRANDE, fill=CINZA)
c(pa, "B46", "=SUM(B40:B45)", F_GRANDE, R0, CINZA)
c(pa, "C46", "=D46/B46", F_GRANDE, R2, AZUL)
c(pa, "D46", "=SUM(D40:D45)", F_GRANDE, R0, CINZA)
texto(pa, 47, "A média fica abaixo de R$ 175 porque a Clínica Padrão (Taguatinga e Sobradinho) está a R$ 165 na planilha da rede. "
      "Com R$ 175 em todas, a média vai a R$ 175.", "G", h=30)

# 5. equipe
secao(49, "5. A equipe do plano por exame (paga pelo apoio do convênio, não pelo valor do exame)")
cab(pa, 50, ["Grupo", "Total no período (R$)", "Exames do plano", "Por exame (R$)"], h=30)
for i, (rot, ref) in enumerate([("Agenda e faturamento: 8 operadores", f"{EQ}E15"),
                                ("Gestão: direção, coordenações, supervisores, assistentes e assessoria", f"{EQ}E16"),
                                ("Equipe inteira", f"{EQ}E17")]):
    l = 51 + i
    neg = i == 2
    c(pa, f"A{l}", rot, F_GRANDE if neg else F_TXT, fill=CINZA if neg else None)
    c(pa, f"B{l}", f"={ref}", F_GRANDE if neg else F_LINK, R0, CINZA if neg else None)
    c(pa, f"C{l}", f"={TOTEX}", F_TXT, R0, CINZA if neg else None)
    c(pa, f"D{l}", f"=B{l}/C{l}", F_GRANDE if neg else F_TXT, R2, AZUL if neg else None)

# 6. juntando tudo
secao(55, "6. Juntando tudo, por exame")
cab(pa, 56, ["", "Custo do exame (R$)", "Mais a equipe, por exame (R$)", "Nosso custo por exame (R$)",
             "O convênio paga pelo exame (R$)", "Mais o apoio, por exame (R$)", "O convênio paga no total, por exame (R$)"], h=44)
JUN = [("Ultrassom feito por nós", "=E27", "=E12"), ("Ultrassom feito pela clínica", "=E17", "=E12"),
       ("Tomografia na clínica", "=C46", "=E13")]
for i, (rot, custo, paga) in enumerate(JUN):
    l = 57 + i
    c(pa, f"A{l}", rot, F_NEG)
    c(pa, f"B{l}", custo, F_TXT, R2)
    c(pa, f"C{l}", "=$D$53", F_TXT, R2)
    c(pa, f"D{l}", f"=B{l}+C{l}", F_GRANDE, R2, AZUL)
    c(pa, f"E{l}", paga, F_TXT, R2)
    c(pa, f"F{l}", "=$D$53", F_TXT, R2)
    c(pa, f"G{l}", f"=E{l}+F{l}", F_GRANDE, R2, VERDE)
    pa.row_dimensions[l].height = 24
texto(pa, 61, "Atenção aos nomes: no plano, \"valor unitário\" é o que o convênio paga por exame (parte 1). O que as partes 2 a 6 "
      "calculam é o nosso custo por exame.", "G", h=30)
larg(pa, [58, 22, 20, 22, 20, 18, 22])
pa.freeze_panes = "A4"

for ws in wb.worksheets:
    ws.sheet_view.showGridLines = False
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
wb.save(SAIDA)
print("ok", SAIDA)
