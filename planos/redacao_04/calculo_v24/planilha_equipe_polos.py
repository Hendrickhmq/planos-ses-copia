"""Planilha para a equipe que negocia com as clinicas (20/10/2026): os 6 polos, as unidades, a demanda, as salas e
os tomografos que cada clinica precisa, a tomografia em 6 e em 5 polos (a Leste sem) e as perguntas.

Vai a quem nao tem o plano: nao cita versao nem secao, nem custo de gestao. Le polos_capacidade.json.
Uso: python3 planilha_equipe_polos.py polos_capacidade.json ../dados/rede_imagem_6_polos_20261020.xlsx
"""
import json, sys
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter as COL

P = json.load(open(sys.argv[1]))
SAIDA = sys.argv[2]

A = "Arial"
F_TIT = Font(name=A, size=14, bold=True, color="1F4E79")
F_SUB = Font(name=A, size=10, italic=True, color="555555")
F_TXT = Font(name=A, size=10)
F_NEG = Font(name=A, size=10, bold=True)
F_IN = Font(name=A, size=10, color="0000FF")
F_CAB = Font(name=A, size=10, bold=True, color="FFFFFF")
F_DEST = Font(name=A, size=12, bold=True, color="1F4E79")
CAB = PatternFill("solid", fgColor="1F4E79")
AMAR = PatternFill("solid", fgColor="FFF2CC")
TOT = PatternFill("solid", fgColor="DDEBF7")
DEST = PatternFill("solid", fgColor="E2EFDA")
L = Side(style="thin", color="BFBFBF")
B = Border(left=L, right=L, top=L, bottom=L)
N0, N1, PCT = '#,##0;(#,##0);"-"', '0.0', '0%'
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


def cab(ws, linha, textos, h=44):
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


UNI_US = {"Oeste": ("Ceilândia — Clínica Brasília", "aguardando aceite"),
          "Sudoeste": ("Samambaia — Med Saúde", "fechado"),
          "Norte": ("Sobradinho — Clínica Padrão", "aguardando aceite"),
          "Leste": ("São Sebastião — GPAES/HPAES Hospital Dia", "aguardando confirmação"),
          "Central e Centro-Sul": ("Asa Sul — DaVida (SGAS 915) ou bairro Sudoeste — Ana Maia (CLSW 105)", "a escolher; aguardando aceite"),
          "Sul": ("Gama — CIG (Santa Maria — Clinisan de reserva)", "proposta aceita")}
TOMO = {"Ceilândia": ("Ceilândia — Clínica Brasília", "aguardando aceite"),
        "Taguatinga": ("Taguatinga — Clínica Padrão", "alinhado"),
        "Plano Piloto": ("Central e Centro-Sul — clínica a definir", "a definir"),
        "Sobradinho": ("Sobradinho — Clínica Padrão", "alinhado"),
        "Gama": ("Gama — CIG", "alinhado"),
        "São Sebastião": ("Leste — clínica a definir", "a definir")}
ORD_TC = ["Ceilândia", "Taguatinga", "Plano Piloto", "Sobradinho", "Gama", "São Sebastião"]

# ------------------------------------------------------------------ Leia primeiro
r = wb.active
r.title = "Leia primeiro"
c(r, "A1", "Rede de imagem do projeto: agora são 6 polos", F_TIT, borda=False)
c(r, "A2", "Exames de ultrassonografia e tomografia pela regulação da SES-DF · situação em 20/10/2026", F_SUB, borda=False)
txt(r, 4, "O projeto passa a ter 6 polos de ultrassom, um por Região de Saúde. A Região Central e a Centro-Sul formam um polo "
    "só: a Centro-Sul não tem clínica na rede, e a Central tem três unidades para a menor demanda do DF. Cada polo tem uma "
    "unidade de ultrassom. A tomografia fica em 6 polos ou em 5; no cenário de 5, a Leste não tem tomógrafo e os pacientes "
    "dela vão à Asa Sul (o Itapoã, a Sobradinho).", "H", F_DEST, 74)
cab(r, 6, ["Parâmetro", "Valor", "Observação"])
PAR = [
    ("Exames do projeto", P["N"], N0, "ultrassonografia e tomografia, em 8 meses"),
    ("Ultrassonografias", sum(P["R"]["us"].values()), N0, ""),
    ("Tomografias", sum(P["R"]["tc"].values()), N0, "95% com contraste"),
    ("Meses de execução", 8, N0, "produção desde o 1º mês"),
    ("Dias úteis no período", 168, N0, "21 por mês"),
    ("Ocupação máxima de uma sala ou tomógrafo", 0.8, PCT, "20% de folga para exame que se estende, atraso e manutenção"),
    ("Faltas esperadas", 0.25, PCT, "hipótese (de cada 10 agendados, 7 a 8 comparecem); só muda as vagas a abrir"),
]
G = {}
for i, (n, v, fmt, obs) in enumerate(PAR):
    l = 7 + i
    G[n] = f"'Leia primeiro'!$B${l}"
    c(r, f"A{l}", n)
    c(r, f"B{l}", v, F_IN, fmt, AMAR if i >= 5 else None)
    c(r, f"C{l}", obs, al=QUEBRA)
DIAS, OCUP, FALTA, MESES = G["Dias úteis no período"], G["Ocupação máxima de uma sala ou tomógrafo"], G["Faltas esperadas"], G["Meses de execução"]
COMO = [
    "Como usar",
    "• As células amarelas são para preencher com o que cada clínica informar: salas, minutos por exame, horas por dia e "
    "mínimo mensal. A planilha refaz a conta e diz se cabe ou quanto falta.",
    "• Enquanto a clínica não informa o tempo por exame, vale o tempo de planejamento (20 minutos; doppler 30; tomografia "
    "20 com contraste e 15 sem). É premissa, não medida: o tempo real da clínica a substitui.",
    "• A demanda de cada Região vem da fila de regulação de 15/09/2026. O volume que chega a cada clínica depende da "
    "regulação da SES-DF, que ocupa as vagas que o polo abre.",
    "• Abas: Polos e unidades · Ultrassom · Tomografia 6 polos · Tomografia 5 polos · 6 ou 5 polos · Para onde vai cada RA · "
    "Perguntas · Premissas e fontes.",
]
for i, t in enumerate(COMO):
    txt(r, 16 + i, t, "H", F_NEG if i == 0 else F_TXT, 16 if i == 0 else 32)
larg(r, [42, 14, 70, 10, 10, 10, 10, 10])

# ------------------------------------------------------------------ Polos e unidades
pu = wb.create_sheet("Polos e unidades")
c(pu, "A1", "Os 6 polos e as unidades", F_TIT, borda=False)
cab(pu, 3, ["Polo", "Regiões de Saúde", "Exames em 8 meses", "% do projeto", "Unidade de ultrassom", "Situação",
            "Tomografia: 6 polos", "Tomografia: 5 polos (Leste sem)"])
TC6 = {"Oeste": "Ceilândia — Clínica Brasília", "Sudoeste": "Taguatinga — Clínica Padrão", "Norte": "Sobradinho — Clínica Padrão",
       "Leste": "Leste — clínica a definir", "Central e Centro-Sul": "clínica a definir", "Sul": "Gama — CIG"}
TC5 = dict(TC6, Leste="sem tomógrafo: Asa Sul (Itapoã: Sobradinho)")
for i, x in enumerate(P["polos"]):
    l = 4 + i
    c(pu, f"A{l}", x["polo"], F_NEG)
    c(pu, f"B{l}", ", ".join(x["regioes"]), al=QUEBRA)
    c(pu, f"C{l}", x["us"] + x["tc"], F_IN, N0)
    c(pu, f"D{l}", f"=C{l}/SUM($C$4:$C$9)", fmt=PCT, al=CENTRO)
    c(pu, f"E{l}", UNI_US[x["polo"]][0], al=QUEBRA)
    c(pu, f"F{l}", UNI_US[x["polo"]][1], al=QUEBRA)
    c(pu, f"G{l}", TC6[x["polo"]], al=QUEBRA)
    c(pu, f"H{l}", TC5[x["polo"]], al=QUEBRA)
    pu.row_dimensions[l].height = 36
c(pu, "A10", "Total", F_NEG, fill=TOT)
c(pu, "C10", "=SUM(C4:C9)", F_NEG, N0, TOT)
c(pu, "D10", "=SUM(D4:D9)", F_NEG, PCT, TOT)
txt(pu, 12, "Ficam fora, com 6 unidades: Asa Norte (Everaldo Maia) e Santa Maria (Clinisan, de reserva no Sul). A Taguatinga "
    "da Clínica Padrão é de tomografia; o ultrassom da Sudoeste é Samambaia.", "H", h=30)
larg(pu, [20, 18, 12, 10, 40, 20, 30, 32])

# ------------------------------------------------------------------ Ultrassom
us = wb.create_sheet("Ultrassom")
c(us, "A1", "Ultrassom: o que cada unidade precisa ter", F_TIT, borda=False)
c(us, "A2", "Preencha as colunas amarelas com o que a clínica informar. Salas necessárias = horas de exame por dia ÷ "
    "(horas abertas × ocupação máxima).", F_SUB, borda=False)
cab(us, 4, ["Polo", "Unidade", "Exames em 8 meses", "Por mês", "Por dia útil", "Vagas a abrir por dia (com faltas)",
            "Minutos por exame (planejamento)", "Minutos por exame informados pela clínica", "Horas por dia que a clínica abre",
            "Salas necessárias", "Salas se o 1º mês se perder", "Salas que a clínica oferece", "Situação"], 58)
for i, x in enumerate(P["polos"]):
    l = 5 + i
    mn = round(x["h_us"] * 60 / x["us"], 1)
    c(us, f"A{l}", x["polo"], F_NEG)
    c(us, f"B{l}", UNI_US[x["polo"]][0], al=QUEBRA)
    c(us, f"C{l}", x["us"], F_IN, N0)
    c(us, f"D{l}", f"=ROUND(C{l}/{MESES},0)", fmt=N0)
    c(us, f"E{l}", f"=ROUND(C{l}/{DIAS},0)", fmt=N0)
    c(us, f"F{l}", f"=ROUNDUP(E{l}/(1-{FALTA}),0)", fmt=N0)
    c(us, f"G{l}", mn, F_IN, N1)
    c(us, f"H{l}", None, F_IN, N1, AMAR)
    c(us, f"I{l}", 10, F_IN, N1, AMAR)
    m = f'IF(H{l}="",G{l},H{l})'
    c(us, f"J{l}", f"=MAX(1,ROUNDUP(C{l}/{DIAS}*{m}/60/(I{l}*{OCUP}),0))", F_NEG, N0, DEST, CENTRO)
    c(us, f"K{l}", f"=MAX(1,ROUNDUP(C{l}/({DIAS}-21)*{m}/60/(I{l}*{OCUP}),0))", fmt=N0, al=CENTRO)
    c(us, f"L{l}", None, F_IN, N0, AMAR, CENTRO)
    c(us, f"M{l}", f'=IF(L{l}="","informar",IF(L{l}>=J{l},"cabe","falta "&(J{l}-L{l})&" sala(s)"))', F_NEG, al=CENTRO)
    us.row_dimensions[l].height = 36
c(us, "A11", "Total", F_NEG, fill=TOT)
for col in "CDEFJKL":
    c(us, f"{col}11", f"=SUM({col}5:{col}10)", F_NEG, N0, TOT, CENTRO)
txt(us, 13, "Leitura: Samambaia e Gama são as duas unidades grandes da rede. Com 2 salas, Samambaia não comporta a Sudoeste nem a "
    "12 minutos por exame. A Clínica Brasília ofereceu um andar com 5 salas em Ceilândia, ao lado da Sudoeste: pode receber a "
    "parte que Samambaia não comportar.", "M", h=44)
larg(us, [20, 34, 11, 9, 9, 12, 12, 13, 11, 11, 11, 11, 14])

# ------------------------------------------------------------------ Tomografia 6 e 5
def aba_tomo(nome, cenario, titulo, nota):
    t = wb.create_sheet(nome)
    c(t, "A1", titulo, F_TIT, borda=False)
    c(t, "A2", "Tomógrafos necessários = horas de exame por dia ÷ (horas reservadas × ocupação máxima). A demanda cobre o "
      "mínimo quando os exames por mês da clínica alcançam o mínimo proposto.", F_SUB, borda=False)
    cab(t, 4, ["Tomógrafo", "Recebe os pacientes de", "Situação", "Exames em 8 meses", "Por mês (8 meses)",
               "Por mês, se feito em 6 meses", "Minutos por exame (planejamento)", "Minutos informados pela clínica",
               "Horas por dia reservadas", "Tomógrafos necessários", "Mínimo mensal proposto", "A demanda cobre o mínimo?"], 58)
    por = {}
    for x in P[cenario]["por_ra"]:
        por.setdefault(x["vai_a"], []).append(x)
    sedes = [s for s in ORD_TC if s in P[cenario]["por_sede"]]
    for i, sd in enumerate(sedes):
        l = 5 + i
        regs = {}
        for x in por[sd]:
            regs.setdefault(x["regiao"], []).append(x["ra"])
        recebe = "; ".join(f"{rg} ({', '.join(sorted(v))})" if len(v) < sum(1 for a in P['ras'] if a['regiao'] == rg)
                           else f"{rg} (toda)" for rg, v in regs.items())
        c(t, f"A{l}", TOMO[sd][0], F_NEG, al=QUEBRA)
        c(t, f"B{l}", recebe, al=QUEBRA)
        c(t, f"C{l}", TOMO[sd][1], al=QUEBRA)
        c(t, f"D{l}", round(P[cenario]["por_sede"][sd]), F_IN, N0)
        c(t, f"E{l}", f"=ROUND(D{l}/{MESES},0)", F_NEG, N0)
        c(t, f"F{l}", f"=ROUND(D{l}/6,0)", fmt=N0)
        c(t, f"G{l}", round(P["h_por_tc"] * 60, 1), F_IN, N1)
        c(t, f"H{l}", None, F_IN, N1, AMAR)
        c(t, f"I{l}", 10, F_IN, N1, AMAR)
        m = f'IF(H{l}="",G{l},H{l})'
        c(t, f"J{l}", f"=ROUND(D{l}/{DIAS}*{m}/60/(I{l}*{OCUP}),2)", F_NEG, '0.00', DEST, CENTRO)
        c(t, f"K{l}", 400, F_IN, N0, AMAR, CENTRO)
        c(t, f"L{l}", f'=IF(E{l}>=K{l},"sim","não: faltam "&(K{l}-E{l})&" por mês")', F_NEG, al=CENTRO)
        t.row_dimensions[l].height = 44
    lt = 5 + len(sedes)
    c(t, f"A{lt}", "Total", F_NEG, fill=TOT)
    for col in "DJK":
        c(t, f"{col}{lt}", f"=SUM({col}5:{col}{lt - 1})", F_NEG, '0.00' if col == "J" else N0, TOT, CENTRO)
    c(t, f"E{lt}", f"=ROUND(D{lt}/{MESES},0)", F_NEG, N0, TOT, CENTRO)
    c(t, f"F{lt}", f"=ROUND(D{lt}/6,0)", F_NEG, N0, TOT, CENTRO)
    c(t, f"L{lt}", f'=IF(E{lt}>=K{lt},"os mínimos cabem na demanda","mínimos somados passam a demanda em "&(K{lt}-E{lt})&" por mês")',
      F_NEG, fill=TOT, al=CENTRO)
    c(t, f"A{lt + 2}", "Mínimo mensal que cabe em todas as clínicas", F_NEG)
    t.merge_cells(f"A{lt + 2}:D{lt + 2}")
    c(t, f"E{lt + 2}", f"=MIN(E5:E{lt - 1})", F_NEG, N0, DEST)
    c(t, f"A{lt + 3}", "Mínimo mensal médio (demanda ÷ clínicas)", F_NEG)
    t.merge_cells(f"A{lt + 3}:D{lt + 3}")
    c(t, f"E{lt + 3}", f"=ROUND(E{lt}/{len(sedes)},0)", F_NEG, N0)
    txt(t, lt + 5, nota, "L", h=58)
    larg(t, [30, 44, 14, 11, 11, 11, 12, 12, 11, 12, 11, 22])
    return t, lt


aba_tomo("Tomografia 6 polos", "tc6", "Tomografia em 6 polos",
         "Taguatinga sozinha passaria de um tomógrafo (1,19). Por isso Samambaia e o Recanto das Emas vão a Ceilândia, que "
         "estava ociosa: Samambaia fica a 6,7 km de Ceilândia e 5,8 km de Taguatinga. Faltam duas clínicas de tomografia, "
         "uma na Leste e outra na Central e Centro-Sul (Asa Sul ou arredores).")
aba_tomo("Tomografia 5 polos", "tc5", "Tomografia em 5 polos: a Leste sem tomógrafo",
         "A tomografia da Leste vai à Asa Sul: Paranoá a 11 km, Jardim Botânico a 12 km e São Sebastião a 16,5 km, com ônibus "
         "direto ao Plano Piloto. O Itapoã vai a Sobradinho (10,8 km, contra 13,3 km da Asa Sul). Samambaia e o Recanto das "
         "Emas vão a Ceilândia, como no cenário de 6. Falta uma clínica de tomografia, na Central e Centro-Sul.")

# ------------------------------------------------------------------ 6 ou 5
cp = wb.create_sheet("6 ou 5 polos")
c(cp, "A1", "Tomografia: 6 ou 5 polos", F_TIT, borda=False)
cab(cp, 3, ["", "6 polos com tomografia", "5 polos (a Leste sem)"])
LT6, LT5 = 5 + len(P["tc6"]["por_sede"]), 5 + len(P["tc5"]["por_sede"])
COMP = [
    ("Distância média até o tomógrafo (linha reta, km)", round(P["tc6"]["km_medio"], 1), round(P["tc5"]["km_medio"], 1), N1),
    ("Clínicas de tomografia a encontrar", 2, 1, N0),
    ("Clínica mais carregada (tomógrafos)", f"=MAX('Tomografia 6 polos'!J5:J{LT6 - 1})", f"=MAX('Tomografia 5 polos'!J5:J{LT5 - 1})", '0.00'),
    ("Menor volume por clínica (por mês)", f"=MIN('Tomografia 6 polos'!E5:E{LT6 - 1})", f"=MIN('Tomografia 5 polos'!E5:E{LT5 - 1})", N0),
    ("Maior volume por clínica (por mês)", f"=MAX('Tomografia 6 polos'!E5:E{LT6 - 1})", f"=MAX('Tomografia 5 polos'!E5:E{LT5 - 1})", N0),
    ("Mínimos somados, se 400 por clínica", f"=400*{len(P['tc6']['por_sede'])}", f"=400*{len(P['tc5']['por_sede'])}", N0),
    ("Demanda de tomografia por mês", f"='Tomografia 6 polos'!E{LT6}", f"='Tomografia 5 polos'!E{LT5}", N0),
]
for i, (rot, a, b, fmt) in enumerate(COMP):
    l = 4 + i
    c(cp, f"A{l}", rot)
    c(cp, f"B{l}", a, F_IN if not str(a).startswith("=") else F_NEG, fmt, al=CENTRO)
    c(cp, f"C{l}", b, F_IN if not str(b).startswith("=") else F_NEG, fmt, al=CENTRO)
LEIT = ["Leitura",
        "• 6 polos: cada Região faz a tomografia perto de casa, mas 1.703 exames por mês se espalham por 6 clínicas, e três "
        "ficam abaixo de 260 por mês. Exige achar duas clínicas.",
        "• 5 polos: meio quilômetro a mais na média, volumes maiores por clínica e uma clínica só a achar.",
        "• Nos dois, o mínimo de 400 por mês por clínica não fecha: nenhuma clínica chega lá no cenário de 6, e só a Asa Sul no de 5. "
        "Negociar um mínimo próximo do volume de cada clínica (aba de cada cenário) ou um mínimo pela rede inteira.",
        "• Se a tomografia for feita em 6 meses, e não em 8, os volumes por mês sobem um terço (coluna \"se feito em 6 meses\")."]
for i, t in enumerate(LEIT):
    txt(cp, 13 + i, t, "C", F_NEG if i == 0 else F_TXT, 16 if i == 0 else 32)
larg(cp, [48, 24, 24])

# ------------------------------------------------------------------ Para onde vai cada RA
ra = wb.create_sheet("Para onde vai cada RA")
c(ra, "A1", "Para onde vai cada RA", F_TIT, borda=False)
c(ra, "A2", "Exames de cada RA estimados pela população do Censo 2022 (a fila não traz a RA do usuário). Distância em linha reta.",
  F_SUB, borda=False)
cab(ra, 4, ["RA", "Região de Saúde", "População (Censo 2022)", "Exames estimados", "Ultrassom em", "Tomografia: 6 polos",
            "km", "Tomografia: 5 polos", "km"])
US_EM = {"Oeste": "Ceilândia", "Sudoeste": "Samambaia", "Norte": "Sobradinho", "Leste": "São Sebastião",
         "Central": "Asa Sul ou bairro Sudoeste", "Centro-Sul": "Asa Sul ou bairro Sudoeste", "Sul": "Gama"}
NOME_TC = {"Plano Piloto": "Asa Sul (Central e Centro-Sul)", "São Sebastião": "São Sebastião (Leste)"}
d6 = {x["ra"]: x for x in P["tc6"]["por_ra"]}
d5 = {x["ra"]: x for x in P["tc5"]["por_ra"]}
ORDR = ["Oeste", "Sudoeste", "Norte", "Leste", "Central", "Centro-Sul", "Sul"]
lista = sorted(P["ras"], key=lambda a: (ORDR.index(a["regiao"]), -a["pop"]))
for i, a in enumerate(lista):
    l = 5 + i
    c(ra, f"A{l}", a["nome"])
    c(ra, f"B{l}", a["regiao"])
    c(ra, f"C{l}", a["pop"], F_IN, N0)
    c(ra, f"D{l}", round(a["tot"]), F_IN, N0)
    c(ra, f"E{l}", US_EM[a["regiao"]])
    c(ra, f"F{l}", NOME_TC.get(d6[a["nome"]]["vai_a"], d6[a["nome"]]["vai_a"]))
    c(ra, f"G{l}", round(d6[a["nome"]]["km"], 1), fmt=N1)
    mud = d5[a["nome"]]["vai_a"] != d6[a["nome"]]["vai_a"]
    c(ra, f"H{l}", NOME_TC.get(d5[a["nome"]]["vai_a"], d5[a["nome"]]["vai_a"]), F_NEG if mud else F_TXT, fill=DEST if mud else None)
    c(ra, f"I{l}", round(d5[a["nome"]]["km"], 1), fmt=N1)
larg(ra, [30, 14, 13, 11, 24, 28, 7, 28, 7])
ra.freeze_panes = "A5"

# ------------------------------------------------------------------ Perguntas
pg = wb.create_sheet("Perguntas")
c(pg, "A1", "O que perguntar a cada clínica", F_TIT, borda=False)
cab(pg, 3, ["Clínica", "Pergunta", "Por que importa", "Resposta"])
PERG = [
    ("Samambaia — Med Saúde", "Quantas salas de ultrassom podem ser reservadas, em que horário, e quanto tempo levam por exame?",
     "É a unidade da maior Região: 131 exames por dia útil. Pede 6 salas no tempo de planejamento, 4 a 12 minutos por exame."),
    ("Samambaia — Med Saúde", "O aparelho opcional (R$ 2.500 por mês) é para uma sala a mais?", "Define se a unidade chega às salas que precisa."),
    ("Gama — CIG", "Quantas salas de ultrassom, em que horário, e o valor final do espaço?", "86 exames por dia útil: 5 salas no tempo de planejamento, 3 a 12 minutos."),
    ("Gama — CIG", "Qual a capacidade mensal de tomografia e aceita mínimo perto de 230 por mês?", "A demanda da Sul é de 232 tomografias por mês."),
    ("Central e Centro-Sul — DaVida (Asa Sul) ou Ana Maia (bairro Sudoeste)", "Qual das duas aceita, com quantas salas e em que horário?",
     "59 exames por dia útil: 3 salas no tempo de planejamento. A Ana Maia tem 2 aparelhos de doppler no CNES."),
    ("Central e Centro-Sul", "Há clínica com tomógrafo na Asa Sul ou arredores (Guará, SIA, bairro Sudoeste)?",
     "Faz falta nos dois cenários: 307 tomografias por mês em 6 polos, 440 em 5 (recebe a Leste)."),
    ("São Sebastião — GPAES/HPAES", "Confirma o ultrassom, com quantas salas? Tem tomógrafo?",
     "65 exames por dia útil (3 salas). Tomógrafo só no cenário de 6 polos (170 por mês)."),
    ("Sobradinho — Clínica Padrão", "Aceite do ultrassom (2 salas) e capacidade de tomografia para 250 a 290 por mês?",
     "No cenário de 5 polos, Sobradinho recebe também o Itapoã."),
    ("Taguatinga — Clínica Padrão", "Capacidade de tomografia para cerca de 350 por mês?",
     "Sem Samambaia e Recanto das Emas, que vão a Ceilândia; com elas, passaria de um tomógrafo."),
    ("Ceilândia — Clínica Brasília", "Aceita cerca de 390 tomografias por mês, com Samambaia e o Recanto das Emas?",
     "Ceilândia sozinha tem só 132 por mês; com a divisão, o tomógrafo fica a 0,76 da capacidade."),
    ("Ceilândia — Clínica Brasília", "O andar com 5 salas de ultrassom fica pronto e licenciado antes da formalização?",
     "Ceilândia usa 1 sala; as outras podem receber a parte da Sudoeste que Samambaia não comportar."),
    ("Todas", "Quanto tempo de sala por exame (ultrassom simples, doppler, tomografia com e sem contraste)?",
     "Substitui a premissa de planejamento e pode reduzir as salas."),
    ("Todas de tomografia", "O preço inclui contraste, bomba injetora, enfermagem e atendimento a reação?",
     "95% das tomografias usam contraste."),
    ("Todas", "Podem começar no 1º mês? Se o 1º mês se perder, as salas sobem (coluna da aba Ultrassom).",
     "O projeto produz desde o 1º mês."),
]
for i, (cl, p, pq) in enumerate(PERG):
    l = 4 + i
    c(pg, f"A{l}", cl, F_NEG, al=QUEBRA)
    c(pg, f"B{l}", p, al=QUEBRA)
    c(pg, f"C{l}", pq, al=QUEBRA)
    c(pg, f"D{l}", None, F_IN, fill=AMAR, al=QUEBRA)
    pg.row_dimensions[l].height = 46
larg(pg, [30, 48, 52, 40])

# ------------------------------------------------------------------ Premissas e fontes
pf = wb.create_sheet("Premissas e fontes")
c(pf, "A1", "Premissas e fontes", F_TIT, borda=False)
FON = [
    "Demanda por Região: fila de regulação da SES-DF de 15/09/2026, por nome de fila e por Região de Saúde (Mapa Social da "
    "Saúde, MPDFT), distribuída sobre os exames do projeto.",
    "Divisão das Regiões entre as RAs: população do Censo 2022 (IBGE, elaboração IPEDF). É estimativa, porque a fila não traz a RA.",
    "Distância: em linha reta, do centro de cada RA à cidade do polo. Pela estrada e pelo transporte público a ordem tende a se manter.",
    "Transporte: o metrô liga Plano Piloto, Guará, Park Way, Águas Claras, Taguatinga, Ceilândia e Samambaia; o BRT Sul liga "
    "Gama e Santa Maria ao Plano Piloto; as linhas de ônibus da Leste e da Norte vão sobretudo ao Plano Piloto.",
    "Tempo por exame: premissa de planejamento (ultrassom 20 minutos, doppler 30; tomografia 20 com contraste e 15 sem), sem medida.",
    "Ocupação máxima de 80% e faltas de 25%: premissas de planejamento.",
    "Rede: levantamento de CNPJ e CNES do ISHP (ultrassom e tomografia). A unidade \"Sudoeste\" (Clínica Ana Maia, CNES 9010297) "
    "fica na CLSW 105, bairro Sudoeste, na Região Central, conforme a ficha do CNES consultada em 20/10/2026.",
]
for i, t in enumerate(FON):
    txt(pf, 3 + i, "• " + t, "F", h=32)
larg(pf, [30, 30, 30, 30, 30, 30])

for ws in wb.worksheets:
    ws.sheet_view.showGridLines = False
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
wb.save(SAIDA)
print("ok", SAIDA)
