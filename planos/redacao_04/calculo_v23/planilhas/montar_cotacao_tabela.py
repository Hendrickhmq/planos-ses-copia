"""Versao so com a tabela da pesquisa de precos: sem a coluna do valor unitario do plano, sem notas, sem a celula
do percentual, sem a legenda, sem o bloco de dados das clinicas e sem os totais por clinica fora da tabela.
Preco de referencia = 50% do valor unitario do plano v23 (tabela SUS + incremento), gravado como numero."""
import json, sys
from decimal import Decimal as D, ROUND_HALF_UP
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.formatting.rule import FormulaRule

matriz_json, saida = sys.argv[1:3]
d = json.load(open(matriz_json))
M, ORD = d["matriz"], d["ORD"]
REF = {c: float((D(v) / 2).quantize(D("0.01"), ROUND_HALF_UP)) for c, v in d["unit"].items()}
PROC = [
    ("02.05.02.009-7", "Ultrassonografia mamária bilateral"),
    ("02.05.01.004-0", "Ultrassonografia doppler colorido de vasos"),
    ("02.05.02.004-6", "Ultrassonografia de abdômen total"),
    ("02.05.02.018-6", "Ultrassonografia transvaginal"),
    ("02.05.02.005-4", "Ultrassonografia de aparelho urinário"),
    ("02.05.02.012-7", "Ultrassonografia de tireoide"),
    ("02.05.02.010-0", "Ultrassonografia de próstata por via abdominal"),
    ("02.05.02.003-8", "Ultrassonografia de abdômen superior"),
    ("02.06.02.003-1", "Tomografia computadorizada de tórax"),
    ("02.06.03.001-0", "Tomografia computadorizada de abdômen superior"),
    ("02.06.03.003-7", "Tomografia computadorizada de pelve, bacia e abdômen inferior"),
]
QTD = {c: sum(M[c][p] for p in ORD) for c, _ in PROC}
NCLIN = 4
POLOS = {"Oeste": 1, "Sudoeste": 2, "Norte e Leste": 2, "Central": 2, "Sul": 2, "Centro-Sul": 1}   # estado.yaml, v21

A = "Arial"
f_cab = Font(name=A, size=10, bold=True, color="FFFFFF")
f_in = Font(name=A, size=10, color="0000FF")
f_txt = Font(name=A, size=10)
f_lnk = Font(name=A, size=10, color="008000")
f_b = Font(name=A, size=10, bold=True)
fill_cab = PatternFill("solid", fgColor="1F4E78")
fill_ref = PatternFill("solid", fgColor="E2EFDA")
fill_in = PatternFill("solid", fgColor="FFF2CC")
fill_sub = PatternFill("solid", fgColor="DDEBF7")
fill_tot = PatternFill("solid", fgColor="BDD7EE")
fino = Side(style="thin", color="BFBFBF")
borda = Border(left=fino, right=fino, top=fino, bottom=fino)
N0, RS, PC = '#,##0', '"R$" #,##0.00', '0%'
CAB_AL = Alignment(horizontal="center", vertical="center", wrap_text=True)


def cel(ws, r, c, v=None, font=f_txt, fill=None, fmt=None, al=None):
    x = ws.cell(row=r, column=c)
    if v is not None:
        x.value = v
    x.font, x.border = font, borda
    if fill:
        x.fill = fill
    if fmt:
        x.number_format = fmt
    if al:
        x.alignment = al
    return x


wb = Workbook()
ws = wb.active
ws.title = "Cotação"
cab = (["Código", "Procedimento", "Exames no plano", "Preço de referência", "Valor total na referência"]
       + [f"Clínica {j + 1}" for j in range(NCLIN)] + ["Menor preço ofertado", "Menor preço ÷ referência"])
for j, h in enumerate(cab, 1):
    cel(ws, 1, j, h, f_cab, fill_cab, al=CAB_AL)
ws.row_dimensions[1].height = 32
C0 = 6                                            # F = primeira clinica
G, J = get_column_letter(C0), get_column_letter(C0 + NCLIN - 1)
CK, CL = C0 + NCLIN, C0 + NCLIN + 1
K = get_column_letter(CK)
L0, L1 = 2, 2 + len(PROC) - 1
for i, (cod, nome) in enumerate(PROC):
    r = L0 + i
    cel(ws, r, 1, cod)
    cel(ws, r, 2, nome)
    cel(ws, r, 3, QTD[cod], f_in, fmt=N0)
    cel(ws, r, 4, REF[cod], f_in, fill_ref, RS)
    cel(ws, r, 5, f"=C{r}*D{r}", fmt=RS)
    for j in range(NCLIN):
        cel(ws, r, C0 + j, None, f_in, fill_in, RS)
    cel(ws, r, CK, f'=IF(COUNT({G}{r}:{J}{r})=0,"",MIN({G}{r}:{J}{r}))', fmt=RS)
    cel(ws, r, CL, f'=IF({K}{r}="","",{K}{r}/D{r})', fmt=PC, al=Alignment(horizontal="center"))
rng = f"{G}{L0}:{J}{L1}"
ws.conditional_formatting.add(rng, FormulaRule(formula=[f'AND({G}{L0}<>"",{G}{L0}<=$D{L0})'],
                                               fill=PatternFill("solid", fgColor="C6EFCE"), font=Font(color="006100")))
ws.conditional_formatting.add(rng, FormulaRule(formula=[f'AND({G}{L0}<>"",{G}{L0}>$D{L0})'],
                                               fill=PatternFill("solid", fgColor="FFC7CE"), font=Font(color="9C0006")))
r = L1 + 1
for rot, i0, i1, fill in (("Ultrassonografia", L0, L0 + 7, fill_sub), ("Tomografia", L0 + 8, L1, fill_sub),
                          ("Total", L0, L1, fill_tot)):
    for j in range(1, CL + 1):
        cel(ws, r, j, None, f_b, fill)
    ws.cell(row=r, column=2, value=rot)
    ws.cell(row=r, column=3, value=f"=SUM(C{i0}:C{i1})").number_format = N0
    ws.cell(row=r, column=5, value=f"=SUM(E{i0}:E{i1})").number_format = RS
    r += 1
for col, w in zip("ABCDE", (16, 58, 11, 14, 17)):
    ws.column_dimensions[col].width = w
for j in range(NCLIN):
    ws.column_dimensions[get_column_letter(C0 + j)].width = 14
ws.column_dimensions[K].width = 13
ws.column_dimensions[get_column_letter(CL)].width = 12
ws.freeze_panes = "C2"

v = wb.create_sheet("Volume por Região")
cab = ["Código", "Procedimento", "Preço de referência"] + ORD + ["Total"]
for j, h in enumerate(cab, 1):
    cel(v, 1, j, h, f_cab, fill_cab, al=CAB_AL)
v.row_dimensions[1].height = 32
CT = 4 + len(ORD)                                 # coluna do total
for i, (cod, nome) in enumerate(PROC):
    r = L0 + i
    cel(v, r, 1, cod)
    cel(v, r, 2, nome)
    cel(v, r, 3, f"=Cotação!D{r}", f_lnk, fill_ref, RS)
    for k, p in enumerate(ORD):
        cel(v, r, 4 + k, M[cod][p], f_in, fmt=N0)
    cel(v, r, CT, f"=SUM(D{r}:{get_column_letter(CT - 1)}{r})", fmt=N0)
r = L1 + 1
for rot, i0, i1, fill in (("Ultrassonografia", L0, L0 + 7, fill_sub), ("Tomografia", L0 + 8, L1, fill_sub),
                          ("Total de exames", L0, L1, fill_tot)):
    for j in range(1, CT + 1):
        cel(v, r, j, None, f_b, fill)
    v.cell(row=r, column=2, value=rot)
    for k in range(len(ORD) + 1):
        col = get_column_letter(4 + k)
        v.cell(row=r, column=4 + k, value=f"=SUM({col}{i0}:{col}{i1})").number_format = N0
    r += 1
for j in range(1, CT + 1):
    cel(v, r, j, None, f_b, fill_tot)
v.cell(row=r, column=2, value="Valor no preço de referência")
for k in range(len(ORD) + 1):
    col = get_column_letter(4 + k)
    f = (f"=SUMPRODUCT({col}{L0}:{col}{L1},$C${L0}:$C${L1})" if k < len(ORD)
         else f"=SUM(D{r}:{get_column_letter(CT - 1)}{r})")
    v.cell(row=r, column=4 + k, value=f).number_format = RS
r += 1
for j in range(1, CT + 1):
    cel(v, r, j, None, f_b, fill_sub)
v.cell(row=r, column=2, value="Polos na Região")
for k, p in enumerate(ORD):
    cel(v, r, 4 + k, POLOS[p], Font(name=A, size=10, bold=True, color="0000FF"), fill_sub, N0)
v.cell(row=r, column=CT, value=f"=SUM(D{r}:{get_column_letter(CT - 1)}{r})").number_format = N0
v.column_dimensions["A"].width = 16
v.column_dimensions["B"].width = 58
v.column_dimensions["C"].width = 14
for k in range(len(ORD) + 1):
    v.column_dimensions[get_column_letter(4 + k)].width = 15
v.freeze_panes = "D2"

for s in (ws, v):
    s.sheet_view.showGridLines = False
    s.page_setup.orientation = "landscape"
    s.sheet_properties.pageSetUpPr.fitToPage = True
    s.page_setup.fitToWidth = 1
    s.page_setup.fitToHeight = 0
wb.save(saida)
print("salvo:", saida)
