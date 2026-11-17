"""Planilha de tomografia para a negociacao com os parceiros: a demanda por Regiao e por RA, os cenarios de 6
(o pedido da SES-DF, um polo por Regiao), 5 e 4 polos contra a faixa de 300 a 500 exames por mes, a capacidade
do tomografo e o contraste. Vai para a equipe de negociacao, que nao tem o plano: nao cita versao nem secao.

Uso: montar_tomografia.py matriz_v23.json polos_de_imagem_no_df_v20.html saida.xlsx

A divisao de cada Regiao entre as suas RAs segue a populacao do Censo 2022 (simulador v20): a fila nao traz
a RA do usuario. Norte e Leste, juntas no plano, se separam pela fila de cada uma em 15/09/2026."""
import json, re, sys
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.workbook.defined_name import DefinedName

matriz_json, sim_html, saida = sys.argv[1:4]
d = json.load(open(matriz_json))
M = d["matriz"]
SIM = json.loads(re.search(r"const D = (\{.*?\});\n", open(sim_html, encoding="utf-8").read(), re.S).group(1))

TC = [("02.06.02.003-1", "TC de tórax"),
      ("02.06.03.001-0", "TC de abdômen superior"),
      ("02.06.03.003-7", "TC de pelve, bacia e abdômen inferior")]
TERR = ["Oeste", "Sudoeste", "Norte e Leste", "Central", "Sul", "Centro-Sul"]      # os seis territorios do plano
LOCAIS = {"Oeste": "Ceilândia", "Sudoeste": "Taguatinga, Samambaia", "Norte e Leste": "Sobradinho, São Sebastião",
          "Central": "Asa Sul, Sudoeste (bairro)", "Sul": "Gama, Santa Maria", "Centro-Sul": "nenhuma",
          "Norte": "Sobradinho", "Leste": "São Sebastião"}

# Norte e Leste: a fila de 15/09 por Regiao (simulador v20), levada aos totais v23 de cada codigo pelo maior resto
REG = {r["nome"]: r for r in SIM["regioes"]}
NL = {}
for k, (cod, _) in enumerate(TC):
    tot = M[cod]["Norte e Leste"]
    n, l = REG["Norte"]["cod"][8 + k], REG["Leste"]["cod"][8 + k]
    vn = tot * n / (n + l)
    NL[cod] = {"Norte": round(vn), "Leste": tot - round(vn)}

# RAs: populacao do Censo 2022 e o polo de cada uma em cada cenario
ORD_RA = ["Oeste", "Sudoeste", "Norte", "Leste", "Central", "Sul", "Centro-Sul"]
RAS = sorted(SIM["ras"], key=lambda r: (ORD_RA.index(r["regiao"]), -r["pop"]))
SO_CEIL = {"Samambaia", "Recanto das Emas e Água Quente"}          # a parte da Sudoeste que vai com a Oeste
P6 = {"Oeste": "Ceilândia", "Sudoeste": "Taguatinga ou Samambaia", "Norte": "Sobradinho ou São Sebastião",
      "Leste": "Sobradinho ou São Sebastião", "Central": "Asa Sul ou Sudoeste (bairro)", "Sul": "Gama ou Santa Maria",
      "Centro-Sul": "Centro-Sul (sem parceiro mapeado)"}
P5 = {"Oeste": "Ceilândia ou Samambaia", "Sudoeste": "Taguatinga", "Norte": "Sobradinho", "Leste": "Sobradinho",
      "Central": "Asa Sul", "Centro-Sul": "Asa Sul", "Sul": "Gama"}
P4 = {"Oeste": "Ceilândia ou Samambaia", "Sudoeste": "Taguatinga", "Norte": "Sobradinho", "Leste": "Sobradinho",
      "Central": "Asa Sul ou Gama", "Centro-Sul": "Taguatinga", "Sul": "Asa Sul ou Gama"}


def polo(tab, r):
    if r["regiao"] == "Sudoeste" and r["nome"] in SO_CEIL and tab is not P6:
        return "Ceilândia ou Samambaia"
    return tab[r["regiao"]]


CEN = [  # (titulo, coluna na aba Por RA, polos na ordem, area atendida de cada polo)
    ("6 polos — um por Região (pedido da SES-DF)", "G",
     [("Taguatinga ou Samambaia", "Sudoeste"),
      ("Sobradinho ou São Sebastião", "Norte e Leste"),
      ("Gama ou Santa Maria", "Sul"),
      ("Asa Sul ou Sudoeste (bairro)", "Central"),
      ("Ceilândia", "Oeste"),
      ("Centro-Sul (sem parceiro mapeado)", "Centro-Sul")]),
    ("5 polos", "H",
     [("Sobradinho", "Norte e Leste"),
      ("Ceilândia ou Samambaia", "Oeste, Samambaia e Recanto das Emas"),
      ("Taguatinga", "Taguatinga, Águas Claras, Vicente Pires e Arniqueira"),
      ("Asa Sul", "Central e Centro-Sul"),
      ("Gama", "Sul")]),
    ("4 polos", "I",
     [("Taguatinga", "Taguatinga, Águas Claras, Vicente Pires, Arniqueira e Centro-Sul"),
      ("Sobradinho", "Norte e Leste"),
      ("Asa Sul ou Gama", "Central e Sul"),
      ("Ceilândia ou Samambaia", "Oeste, Samambaia e Recanto das Emas")]),
]

A = "Arial"
f_tit = Font(name=A, size=13, bold=True)
f_sec = Font(name=A, size=11, bold=True, color="1F4E78")
f_nota = Font(name=A, size=9, italic=True, color="555555")
f_cab = Font(name=A, size=10, bold=True, color="FFFFFF")
f_in = Font(name=A, size=10, color="0000FF")
f_txt = Font(name=A, size=10)
f_lnk = Font(name=A, size=10, color="008000")
f_b = Font(name=A, size=10, bold=True)
fill_cab = PatternFill("solid", fgColor="1F4E78")
fill_in = PatternFill("solid", fgColor="FFF2CC")
fill_tot = PatternFill("solid", fgColor="BDD7EE")
fill_alerta = PatternFill("solid", fgColor="FFC7CE")
fino = Side(style="thin", color="BFBFBF")
borda = Border(left=fino, right=fino, top=fino, bottom=fino)
N0, N1, RS, PC = '#,##0', '#,##0.0', '"R$" #,##0.00', '0%'
CENTRO = Alignment(horizontal="center", vertical="center", wrap_text=True)
QUEBRA = Alignment(wrap_text=True, vertical="top")
MEIO = Alignment(horizontal="center")


def cel(ws, r, c, v=None, font=f_txt, fill=None, fmt=None, al=None, b=True):
    x = ws.cell(row=r, column=c)
    if v is not None:
        x.value = v
    x.font = font
    if fill:
        x.fill = fill
    if fmt:
        x.number_format = fmt
    if al:
        x.alignment = al
    if b:
        x.border = borda
    return x


def titulo(ws, texto, nota, ate):
    ws["A1"] = texto
    ws["A1"].font = f_tit
    ws["A2"] = nota
    ws["A2"].font = f_nota
    ws["A2"].alignment = QUEBRA
    ws.merge_cells(f"A2:{ate}2")
    ws.row_dimensions[2].height = 40


def cabecalho(ws, r, nomes, altura=42):
    for j, h in enumerate(nomes, 1):
        cel(ws, r, j, h, f_cab, fill_cab, al=CENTRO)
    ws.row_dimensions[r].height = altura


def larguras(ws, ws_w):
    for j, w in enumerate(ws_w, 1):
        ws.column_dimensions[get_column_letter(j)].width = w


def nota(ws, r, texto):
    cel(ws, r, 1, texto, f_nota, b=False)


def faixa_cores(ws, rng):
    for txt, fundo, letra in (("dentro", "C6EFCE", "006100"), ("abaixo", "FFEB9C", "9C5700"),
                              ("acima", "FFC7CE", "9C0006")):
        ws.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=[f'"{txt}"'],
                                                      fill=PatternFill("solid", fgColor=fundo), font=Font(color=letra)))


FAIXA = 'IF({m}<faixa_min,"abaixo",IF({m}>faixa_max,"acima","dentro"))'
wb = Workbook()

# ---------------- Premissas ----------------
p = wb.active
p.title = "Premissas"
titulo(p, "Tomografia — premissas",
       "As células amarelas podem ser alteradas, e as outras abas recalculam. Números em azul são entradas; em preto, "
       "fórmulas; em verde, valores trazidos de outra aba.", "C")
cabecalho(p, 4, ["Premissa", "Valor", "Origem"], 20)
PREM = [
    ("meses", "Período assistencial (meses)", 8, N0, "Período assistencial do projeto"),
    ("atraso", "Meses sem paciente por atraso da regulação (teste)", 0, N0,
     "Para testar o risco da regulação: os exames do período se concentram nos meses que sobram. Deixe 0 para o normal"),
    ("dias", "Dias úteis por mês", 21, N0, "Segunda a sexta-feira"),
    ("horas_dia", "Horas de funcionamento do tomógrafo por dia útil", 10, N0, "Premissa de planejamento"),
    ("ocup", "Ocupação máxima de cada tomógrafo", 0.8, PC, "Folga para exame que se estende e para manutenção"),
    ("min_exame", "Minutos de tomógrafo por exame", 19.73, '0.00',
     "Média de 20 minutos com contraste e 15 sem. Premissa sem fonte: trocar pelo tempo informado pela clínica"),
    ("h_turno", "Horas por turno", 4, N0, "Turno de referência para reservar agenda"),
    ("faixa_min", "Faixa por polo — mínimo de tomografias por mês", 300, N0, "Modelo de referência para as negociações (14/10/2026)"),
    ("faixa_max", "Faixa por polo — máximo de tomografias por mês", 500, N0, "Modelo de referência para as negociações (14/10/2026)"),
    ("teto", "Teto por tomografia", 175, RS, "Modelo de referência para as negociações (14/10/2026)"),
    ("contraste_ref", "Contraste — referência de custo por exame", 60, RS,
     "Tabela do SUS, 02.06.03.004-5 (contraste para tomografia computadorizada). Só referência de custo"),
    ("n_contraste", "Tomografias com contraste iodado", 12958, N0, "Estimativa pela fila de regulação"),
]
for i, (nome, rot, val, fmt, fonte) in enumerate(PREM):
    r = 5 + i
    cel(p, r, 1, rot, f_b)
    cel(p, r, 2, val, f_in, fill_in, fmt, MEIO)
    cel(p, r, 3, fonte, al=QUEBRA)
    wb.defined_names[nome] = DefinedName(nome, attr_text=f"Premissas!$B${r}")
r = 5 + len(PREM)
cel(p, r, 1, "Meses de produção (período − atraso)", f_b)
cel(p, r, 2, "=meses-atraso", fmt=N0, al=MEIO)
cel(p, r, 3, "Calculado", al=QUEBRA)
wb.defined_names["meses_ef"] = DefinedName("meses_ef", attr_text=f"Premissas!$B${r}")
larguras(p, (50, 14, 100))

# ---------------- Por Região ----------------
g = wb.create_sheet("Por Região")
titulo(g, "Tomografias por Região de Saúde",
       "Demanda do período pela fila de regulação de cada Região em 15/09/2026 (Mapa Social da Saúde). Por mês e por "
       "dia útil, arredondado para cima. A faixa vale para o caso de a Região ter um só polo de tomografia.", "J")
cabecalho(g, 4, ["Região de Saúde", "Localidades mapeadas", "TC de tórax", "TC de abdômen superior",
                 "TC de pelve, bacia e abdômen inferior", "Tomografias no período", "Por mês", "Por dia útil",
                 "Com contraste por mês (≈)", "Um polo só: faixa de 300 a 500"], 56)
G0 = 5
G1 = G0 + len(TERR) - 1
GT = G1 + 1
TOTAL_TC = f"'Por Região'!$F${GT}"


def linha_regiao(r, nome, vals):
    cel(g, r, 1, nome, f_b)
    cel(g, r, 2, LOCAIS[nome])
    for k, v in enumerate(vals):
        cel(g, r, 3 + k, v, f_in, fmt=N0)
    cel(g, r, 6, f"=SUM(C{r}:E{r})", fmt=N0)
    cel(g, r, 7, f"=ROUNDUP(F{r}/meses_ef,0)", fmt=N0)
    cel(g, r, 8, f"=ROUNDUP(F{r}/(meses_ef*dias),0)", fmt=N0)
    cel(g, r, 9, f"=ROUND(F{r}/meses_ef*n_contraste/$F${GT},0)", fmt=N0)
    cel(g, r, 10, "=" + FAIXA.format(m=f"G{r}"), al=MEIO)


for i, t in enumerate(TERR):
    linha_regiao(G0 + i, t, [M[c][t] for c, _ in TC])
cel(g, GT, 1, "Total", f_b, fill_tot)
cel(g, GT, 2, None, f_b, fill_tot)
for c in range(3, 10):
    col = get_column_letter(c)
    cel(g, GT, c, f"=SUM({col}{G0}:{col}{G1})", f_b, fill_tot, N0)
cel(g, GT, 10, None, f_b, fill_tot)
faixa_cores(g, f"J{G0}:J{G1}")
nota(g, GT + 1, "Por mês e por dia útil, o total é a soma das Regiões.")

NL0 = GT + 3
cel(g, NL0 - 1, 1, "Norte e Leste separadas", f_b, b=False)
for k, nome in enumerate(["Norte", "Leste"]):
    linha_regiao(NL0 + k, nome, [NL[c][nome] for c, _ in TC])
faixa_cores(g, f"J{NL0}:J{NL0 + 1}")
rc = NL0 + 2
nota(g, rc, "Conferência: Norte + Leste − Norte e Leste")
idx = G0 + TERR.index("Norte e Leste")
for c in range(3, 7):
    col = get_column_letter(c)
    cel(g, rc, c, f"={col}{NL0}+{col}{NL0 + 1}-{col}{idx}", f_nota, fmt=N0)
nota(g, rc + 1, "Norte e Leste se separam pela fila de cada uma em 15/09/2026.")
larguras(g, (17, 26, 11, 13, 15, 13, 9, 9, 13, 14))
g.freeze_panes = "C5"
NOME_REG = f"'Por Região'!$A${G0}:$A${G1}"
TOT_REG = f"'Por Região'!$F${G0}:$F${G1}"
NORTE_TOT, LESTE_TOT = f"'Por Região'!$F${NL0}", f"'Por Região'!$F${NL0 + 1}"

# ---------------- Por RA ----------------
a = wb.create_sheet("Por RA")
titulo(a, "Tomografias por Região Administrativa e o polo de cada uma em cada cenário",
       "Estimativa: a fila não traz a RA do usuário. Cada Região se divide entre as suas RAs pela população do Censo "
       "2022 (IBGE, elaboração IPEDF). As colunas amarelas dizem a que polo cada RA vai em cada cenário: troque o "
       "nome para testar outro desenho, e a aba Cenários recalcula. O nome tem de ser igual ao da aba Cenários.", "I")
cabecalho(a, 4, ["Região Administrativa", "Região de Saúde", "População (Censo 2022)", "Parte da Região",
                 "Tomografias no período (≈)", "Por mês (≈)"] + [f"Polo — {c[0]}" for c in CEN], 42)
A0 = 5
A1 = A0 + len(RAS) - 1
for i, r_ in enumerate(RAS):
    r = A0 + i
    cel(a, r, 1, r_["nome"])
    cel(a, r, 2, r_["regiao"])
    cel(a, r, 3, r_["pop"], f_in, fmt=N0)
    cel(a, r, 4, f"=C{r}/SUMIF($B${A0}:$B${A1},B{r},$C${A0}:$C${A1})", fmt='0.0%')
    total = (f'IF(B{r}="Norte",{NORTE_TOT},IF(B{r}="Leste",{LESTE_TOT},'
             f'INDEX({TOT_REG},MATCH(B{r},{NOME_REG},0))))')
    cel(a, r, 5, f"=D{r}*{total}", f_lnk, fmt=N0)
    cel(a, r, 6, f"=E{r}/meses_ef", fmt=N0)
    for k, tab in enumerate((P6, P5, P4)):
        cel(a, r, 7 + k, polo(tab, r_), f_in, fill_in)
AT = A1 + 1
cel(a, AT, 1, "Total", f_b, fill_tot)
for c in (2, 4, 7, 8, 9):
    cel(a, AT, c, None, f_b, fill_tot)
for c in (3, 5, 6):
    col = get_column_letter(c)
    cel(a, AT, c, f"=SUM({col}{A0}:{col}{A1})", f_b, fill_tot, N0)
larguras(a, (30, 13, 13, 10, 13, 10, 32, 24, 24))
a.freeze_panes = "C5"
RA_TC = f"'Por RA'!$E${A0}:$E${A1}"
RA_TOTAL = f"'Por RA'!$E${AT}"

# ---------------- Cenários ----------------
s = wb.create_sheet("Cenários")
titulo(s, "Polos de tomografia: 6, 5 ou 4 contra a faixa de 300 a 500 exames por mês",
       "Cada polo soma as RAs que a aba Por RA manda para ele. Tomógrafos: um por polo, nas células amarelas; altere "
       "para testar. A ocupação fica vermelha acima do máximo das Premissas. O volume depende da regulação da SES-DF: "
       "é demanda estimada, não volume garantido. Os números são totais, sem taxa de absenteísmo.", "L")
cel(s, 3, 1, "Resumo", f_sec, b=False)
cabecalho(s, 4, ["Cenário", "Polos", "Tomógrafos", "Polos dentro da faixa", "Ocupação do tomógrafo mais cheio",
                 "Média por polo (por mês)", "Menor polo (por mês)", "Maior polo (por mês)"], 42)
RES0 = 5
blocos = []
r = RES0 + len(CEN) + 3
CAP = "(meses_ef*dias*horas_dia)"
for titulo_c, col_ra, polos in CEN:
    cel(s, r, 1, titulo_c, f_sec, b=False)
    r += 1
    cabecalho(s, r, ["Polo", "Área atendida", "Tomografias no período", "Por mês", "Por dia útil",
                     "Com contraste por mês (≈)", "Tomógrafos", "Ocupação de cada tomógrafo", "Faixa de 300 a 500",
                     "Mínimo de tomógrafos para ficar no máximo", "Turnos de 4 h por semana",
                     "Faturamento do parceiro por mês no teto"], 56)
    b0 = r + 1
    for i, (nome, area) in enumerate(polos):
        rr = b0 + i
        cel(s, rr, 1, nome, f_b)
        cel(s, rr, 2, area, al=QUEBRA)
        cel(s, rr, 3, f"=SUMIF('Por RA'!${col_ra}${A0}:${col_ra}${A1},A{rr},{RA_TC})", f_lnk, fmt=N0)
        cel(s, rr, 4, f"=ROUNDUP(C{rr}/meses_ef,0)", f_b, fmt=N0)
        cel(s, rr, 5, f"=ROUNDUP(C{rr}/(meses_ef*dias),0)", fmt=N0)
        cel(s, rr, 6, f"=ROUND(C{rr}/meses_ef*n_contraste/{TOTAL_TC},0)", fmt=N0)
        cel(s, rr, 7, 1, f_in, fill_in, N0, MEIO)
        cel(s, rr, 8, f"=IF(G{rr}>0,C{rr}*min_exame/60/(G{rr}*{CAP}),0)", fmt=PC)
        cel(s, rr, 9, "=" + FAIXA.format(m=f"D{rr}"), al=MEIO)
        cel(s, rr, 10, f"=MAX(1,ROUNDUP(C{rr}*min_exame/60/({CAP}*ocup),0))", fmt=N0)
        cel(s, rr, 11, f"=ROUNDUP(C{rr}*min_exame/60/(meses_ef*dias)/h_turno*5,0)", fmt=N0)
        cel(s, rr, 12, f"=D{rr}*teto", fmt=RS)
    b1 = b0 + len(polos) - 1
    rt = b1 + 1
    cel(s, rt, 1, "Total", f_b, fill_tot)
    cel(s, rt, 2, None, f_b, fill_tot)
    for c in (3, 4, 5, 6, 7, 10, 11, 12):
        col = get_column_letter(c)
        cel(s, rt, c, f"=SUM({col}{b0}:{col}{b1})", f_b, fill_tot, RS if c == 12 else N0)
    cel(s, rt, 8, f"=IF(G{rt}>0,C{rt}*min_exame/60/(G{rt}*{CAP}),0)", f_b, fill_tot, PC)
    cel(s, rt, 9, f'=COUNTIF(I{b0}:I{b1},"dentro")&" de "&COUNTA(A{b0}:A{b1})', f_b, fill_tot, al=MEIO)
    faixa_cores(s, f"I{b0}:I{b1}")
    s.conditional_formatting.add(f"H{b0}:H{b1}", FormulaRule(formula=[f"H{b0}>ocup"], fill=fill_alerta,
                                                             font=Font(color="9C0006", bold=True)))
    rk = rt + 1
    nota(s, rk, "Tomografias sem polo neste cenário")
    cel(s, rk, 3, f"={RA_TOTAL}-C{rt}", f_nota, fmt=N0, b=False)
    s.conditional_formatting.add(f"C{rk}", FormulaRule(formula=[f"ABS(C{rk})>0.5"], fill=fill_alerta,
                                                       font=Font(color="9C0006", bold=True)))
    blocos.append((titulo_c, b0, b1, rt))
    r = rk + 3

for i, (titulo_c, b0, b1, rt) in enumerate(blocos):
    rr = RES0 + i
    cel(s, rr, 1, titulo_c, f_b)
    cel(s, rr, 2, f"=COUNTA(A{b0}:A{b1})", fmt=N0, al=MEIO)
    cel(s, rr, 3, f"=G{rt}", fmt=N0, al=MEIO)
    cel(s, rr, 4, f'=COUNTIF(I{b0}:I{b1},"dentro")', f_b, fmt=N0, al=MEIO)
    cel(s, rr, 5, f"=MAX(H{b0}:H{b1})", f_b, fmt=PC, al=MEIO)
    cel(s, rr, 6, f"=SUM(D{b0}:D{b1})/B{rr}", fmt=N0, al=MEIO)
    cel(s, rr, 7, f"=MIN(D{b0}:D{b1})", fmt=N0, al=MEIO)
    cel(s, rr, 8, f"=MAX(D{b0}:D{b1})", fmt=N0, al=MEIO)
s.conditional_formatting.add(f"E{RES0}:E{RES0 + len(CEN) - 1}",
                             FormulaRule(formula=[f"E{RES0}>ocup"], fill=fill_alerta, font=Font(color="9C0006", bold=True)))
nota(s, RES0 + len(CEN), "Para testar o atraso da regulação, mude os meses sem paciente nas Premissas: a ocupação "
                         "mostra se dá para recuperar nos meses que sobram.")
larguras(s, (40, 42, 13, 10, 13, 13, 12, 13, 12, 14, 12, 17))

# ---------------- Contraste ----------------
c_ = wb.create_sheet("Contraste")
titulo(c_, "Contraste iodado na tomografia",
       "Quase todas as tomografias usam contraste. Ele não é pago à parte: entra no valor de cada exame. Por isso a "
       "proposta de cada parceiro precisa dizer se o preço inclui o contraste.", "D")
cabecalho(c_, 4, ["", "Valor"], 20)
FATOS = [("Tomografias no período", f"={TOTAL_TC}", N0, f_lnk),
         ("Com contraste iodado (≈)", "=n_contraste", N0, f_lnk),
         ("Parte das tomografias com contraste", "=B6/B5", PC, f_txt),
         ("Referência de custo do contraste por exame (tabela do SUS)", "=contraste_ref", RS, f_lnk),
         ("Custo de referência por tomografia, na média", "=B8*B7", RS, f_txt),
         ("Custo de referência no período", "=B6*B8", RS, f_txt)]
for i, (rot, f, fmt, fonte) in enumerate(FATOS):
    cel(c_, 5 + i, 1, rot, f_b)
    cel(c_, 5 + i, 2, f, fonte, fmt=fmt, al=MEIO)
R = 5 + len(FATOS) + 1
cel(c_, R, 1, "Se o parceiro não incluir o contraste no preço, o custo é do projeto", f_sec, b=False)
cabecalho(c_, R + 1, ["Tomografias por mês no polo", "Com contraste por mês", "Custo de referência por mês"], 30)
for i, v in enumerate((300, 400, 500)):
    rr = R + 2 + i
    cel(c_, rr, 1, v, f_in, fill_in, N0, MEIO)
    cel(c_, rr, 2, f"=ROUND(A{rr}*$B$7,0)", fmt=N0, al=MEIO)
    cel(c_, rr, 3, f"=B{rr}*contraste_ref", fmt=RS, al=MEIO)
R = R + 6
cel(c_, R, 1, "O que o polo precisa ter, durante todo o horário da tomografia", f_sec, b=False)
EXIG = ["Bomba injetora.",
        "Enfermeiro ou técnico de enfermagem para o acesso venoso e a injeção do contraste, sob supervisão médica.",
        "Carro de emergência, oxigênio e medicação para reação ao contraste (adrenalina, anti-histamínico, "
        "corticoide, broncodilatador) e monitor.",
        "Espaço de repouso depois do exame.",
        "Antes do contraste: triagem de risco (doença renal e alergia a contraste), termo de consentimento e "
        "confirmação de gravidez."]
for i, t in enumerate(EXIG):
    x = c_.cell(row=R + 1 + i, column=1, value="• " + t)
    x.font = f_txt
    x.alignment = QUEBRA
    c_.merge_cells(start_row=R + 1 + i, start_column=1, end_row=R + 1 + i, end_column=4)
    c_.row_dimensions[R + 1 + i].height = 28
larguras(c_, (58, 20, 24, 30))

# ---------------- Capacidade ----------------
k = wb.create_sheet("Capacidade")
titulo(k, "Capacidade de um tomógrafo e o que cada volume ocupa",
       "Um tomógrafo nas horas de funcionamento das Premissas, com a ocupação máxima e os minutos por exame de lá. "
       "Na tabela de baixo, troque os volumes amarelos para testar outros.", "G")
cabecalho(k, 4, ["Um tomógrafo", "Valor"], 20)
CAPS = [("Exames por turno de 4 horas", "=h_turno*60/min_exame", N1),
        ("Exames por dia útil, na ocupação máxima", "=horas_dia*ocup*60/min_exame", N1),
        ("Exames por mês, na ocupação máxima", "=horas_dia*ocup*60/min_exame*dias", N0),
        ("Exames por mês, com o tomógrafo 100% ocupado", "=horas_dia*60/min_exame*dias", N0)]
for i, (rot, f, fmt) in enumerate(CAPS):
    cel(k, 5 + i, 1, rot, f_b)
    cel(k, 5 + i, 2, f, fmt=fmt, al=MEIO)
T0 = 11
cabecalho(k, T0, ["Tomografias por mês", "Por dia útil", "Horas de tomógrafo por dia útil",
                  "Ocupação de um tomógrafo", "Turnos de 4 h por semana", "Tomógrafos para ficar no máximo"], 42)
VOL = [(133, "Oeste"), (300, "mínimo da faixa"), (425, "Norte e Leste"), (473, "maior polo com 4 polos"),
       (500, "máximo da faixa"), (613, "Sudoeste")]
for i, (v, rot) in enumerate(VOL):
    rr = T0 + 1 + i
    cel(k, rr, 1, v, f_in, fill_in, N0, MEIO)
    cel(k, rr, 2, f"=A{rr}/dias", fmt=N1)
    cel(k, rr, 3, f"=B{rr}*min_exame/60", fmt=N1)
    cel(k, rr, 4, f"=C{rr}/horas_dia", fmt=PC)
    cel(k, rr, 5, f"=ROUNDUP(C{rr}/h_turno*5,0)", fmt=N0)
    cel(k, rr, 6, f"=MAX(1,ROUNDUP(C{rr}/(horas_dia*ocup),0))", fmt=N0)
    cel(k, rr, 7, rot, f_nota, b=False)
nota(k, T0 + len(VOL) + 2, "Os cálculos usam os números totais, sem taxa de absenteísmo.")
larguras(k, (46, 12, 15, 13, 13, 15, 24))

# ---------------- Fontes ----------------
fo = wb.create_sheet("Fontes")
fo["A1"] = "Fontes e notas"
fo["A1"].font = f_tit
FONTES = [
    "Demanda de tomografia: fila de regulação da SES-DF no Mapa Social da Saúde (MPDFT), 15/09/2026, por Região de "
    "Saúde e por exame. O volume que chega a cada polo depende da regulação da SES-DF.",
    "Divisão das Regiões entre as RAs: população do Censo 2022 (IBGE, elaboração IPEDF). É estimativa, porque a fila "
    "não traz a RA do usuário.",
    "Faixa de 300 a 500 tomografias por mês por polo e teto de R$ 175: modelo de referência para as negociações "
    "(14/10/2026).",
    "Tempo de tomógrafo por exame e ocupação máxima: premissas de planejamento, sem fonte. Trocar pelos tempos que as "
    "clínicas informarem.",
    "\"Sudoeste\", na lista de localidades, foi lido como o bairro, na Região Central.",
]
for i, t in enumerate(FONTES):
    x = fo.cell(row=3 + i, column=1, value=t)
    x.font = f_txt
    x.alignment = QUEBRA
    fo.row_dimensions[3 + i].height = 30
fo.column_dimensions["A"].width = 120

ORDEM = ["Cenários", "Contraste", "Por Região", "Por RA", "Capacidade", "Premissas", "Fontes"]
wb._sheets = [wb[n] for n in ORDEM]           # abre nos cenarios; as premissas ficam a mao
wb.active = 0
for ws in wb.worksheets:                      # impressao: paisagem, uma pagina de largura
    ws.page_setup.orientation = "landscape"
    ws.page_setup.paperSize = ws.PAPERSIZE_A4
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
wb.save(saida)
print(saida)
