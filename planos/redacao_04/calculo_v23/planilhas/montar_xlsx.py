"""Planilha exportavel: exames por procedimento (valor unitario e total) e por Regiao, plano v23."""
import json, sys
from decimal import Decimal as D
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

matriz_json, saida = sys.argv[1:3]
d = json.load(open(matriz_json))
M, UNIT, ORD = d["matriz"], {c: float(D(v)) for c, v in d["unit"].items()}, d["ORD"]

PROC = [  # ordem da planilha do plano (Metas 4 e 5)
    ("02.05.02.009-7", "Ultrassonografia mamária bilateral", "Ultrassonografia"),
    ("02.05.01.004-0", "Ultrassonografia doppler colorido de vasos", "Ultrassonografia"),
    ("02.05.02.004-6", "Ultrassonografia de abdômen total", "Ultrassonografia"),
    ("02.05.02.018-6", "Ultrassonografia transvaginal", "Ultrassonografia"),
    ("02.05.02.005-4", "Ultrassonografia de aparelho urinário", "Ultrassonografia"),
    ("02.05.02.012-7", "Ultrassonografia de tireoide", "Ultrassonografia"),
    ("02.05.02.010-0", "Ultrassonografia de próstata por via abdominal", "Ultrassonografia"),
    ("02.05.02.003-8", "Ultrassonografia de abdômen superior", "Ultrassonografia"),
    ("02.06.02.003-1", "Tomografia computadorizada de tórax", "Tomografia"),
    ("02.06.03.001-0", "Tomografia computadorizada de abdômen superior", "Tomografia"),
    ("02.06.03.003-7", "Tomografia computadorizada de pelve, bacia e abdômen inferior", "Tomografia"),
]
QTD = {c: sum(M[c][p] for p in ORD) for c, _, _ in PROC}

ARIAL = "Arial"
f_tit = Font(name=ARIAL, size=13, bold=True)
f_nota = Font(name=ARIAL, size=9, italic=True, color="555555")
f_cab = Font(name=ARIAL, size=10, bold=True, color="FFFFFF")
f_in = Font(name=ARIAL, size=10, color="0000FF")      # numero digitado (vem do plano / do calculo)
f_txt = Font(name=ARIAL, size=10)
f_frm = Font(name=ARIAL, size=10)                      # formula
f_tot = Font(name=ARIAL, size=10, bold=True)
fill_cab = PatternFill("solid", fgColor="1F4E78")
fill_sub = PatternFill("solid", fgColor="DDEBF7")
fill_tot = PatternFill("solid", fgColor="BDD7EE")
fino = Side(style="thin", color="BFBFBF")
borda = Border(left=fino, right=fino, top=fino, bottom=fino)
N0 = '#,##0'
RS = '"R$" #,##0.00'

wb = Workbook()

# ---------------- aba 1: por procedimento ----------------
a = wb.active
a.title = "Por procedimento"
a["A1"] = "Exames por procedimento — plano de ultrassonografia e tomografia (v23, 8 meses, 10 polos)"
a["A1"].font = f_tit
a["A2"] = ("Fonte: planilha do plano (Metas 4 e 5) e seção 8.1. Valor unitário = valor de tabela do SUS + incremento do "
           "Anexo I da Portaria SAES/MS nº 4.282/2026. Números em azul vêm do plano; os demais são fórmulas.")
a["A2"].font = f_nota
cab = ["Código", "Procedimento", "Modalidade", "Exames", "Valor unitário", "Valor total"]
for j, h in enumerate(cab, 1):
    c = a.cell(row=4, column=j, value=h)
    c.font, c.fill, c.border = f_cab, fill_cab, borda
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
L0 = 5
for i, (cod, nome, mod) in enumerate(PROC):
    r = L0 + i
    vals = [cod, nome, mod, QTD[cod], UNIT[cod], f"=D{r}*E{r}"]
    for j, v in enumerate(vals, 1):
        c = a.cell(row=r, column=j, value=v)
        c.border = borda
        c.font = f_in if j in (4, 5) else (f_frm if j == 6 else f_txt)
    a.cell(row=r, column=4).number_format = N0
    a.cell(row=r, column=5).number_format = RS
    a.cell(row=r, column=6).number_format = RS
L1 = L0 + len(PROC) - 1                                   # ultima linha de procedimento
r = L1 + 2
for rot, filtro, fill in (("Ultrassonografia", "Ultrassonografia", fill_sub), ("Tomografia", "Tomografia", fill_sub),
                          ("Total", None, fill_tot)):
    a.cell(row=r, column=2, value=rot)
    if filtro:
        a.cell(row=r, column=4, value=f'=SUMIF($C${L0}:$C${L1},"{filtro}",D{L0}:D{L1})')
        a.cell(row=r, column=6, value=f'=SUMIF($C${L0}:$C${L1},"{filtro}",F{L0}:F{L1})')
    else:
        a.cell(row=r, column=4, value=f"=SUM(D{L0}:D{L1})")
        a.cell(row=r, column=6, value=f"=SUM(F{L0}:F{L1})")
    for j in range(1, 7):
        c = a.cell(row=r, column=j)
        c.font, c.fill, c.border = f_tot, fill, borda
    a.cell(row=r, column=4).number_format = N0
    a.cell(row=r, column=6).number_format = RS
    r += 1
for col, w in zip("ABCDEF", (16, 60, 18, 11, 15, 18)):
    a.column_dimensions[col].width = w
a.freeze_panes = "A5"

# ---------------- aba 2: por Regiao ----------------
b = wb.create_sheet("Por Região")
b["A1"] = "Exames por procedimento em cada Região de Saúde — plano v23"
b["A1"].font = f_tit
b["A2"] = ("Estimativa de planejamento: o plano fixa só o total de cada Região e a divisão entre ultrassonografia e "
           "tomografia (subseções 3.4 e 7.3). A divisão por procedimento segue a participação de cada Região na fila "
           "de cada exame em 15/09/2026, arredondada para fechar com os totais do plano.")
b["A2"].font = f_nota
b["A2"].alignment = Alignment(wrap_text=True, vertical="top")
b.merge_cells("A2:J2")
b.row_dimensions[2].height = 38
cab2 = ["Código", "Procedimento"] + ORD + ["Total", "Confere com a planilha"]
for j, h in enumerate(cab2, 1):
    c = b.cell(row=4, column=j, value=h)
    c.font, c.fill, c.border = f_cab, fill_cab, borda
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
b.row_dimensions[4].height = 30
cR0, cR1 = 3, 2 + len(ORD)                                # colunas das Regioes (C..H)
LR, LT = get_column_letter(cR0), get_column_letter(cR1)
CT, CK = get_column_letter(cR1 + 1), get_column_letter(cR1 + 2)
for i, (cod, nome, mod) in enumerate(PROC):
    r = L0 + i
    b.cell(row=r, column=1, value=cod)
    b.cell(row=r, column=2, value=nome)
    for k, p in enumerate(ORD):
        c = b.cell(row=r, column=cR0 + k, value=M[cod][p])
        c.font, c.number_format = f_in, N0
    b.cell(row=r, column=cR1 + 1, value=f"=SUM({LR}{r}:{LT}{r})").number_format = N0
    b.cell(row=r, column=cR1 + 2, value=f"=IF({CT}{r}='Por procedimento'!D{r},\"sim\",\"NÃO\")")
    for j in range(1, cR1 + 3):
        c = b.cell(row=r, column=j)
        c.border = borda
        if j in (1, 2, cR1 + 1, cR1 + 2):
            c.font = f_txt
    b.cell(row=r, column=cR1 + 2).alignment = Alignment(horizontal="center")
r = L1 + 2
US_R, TC_R = (L0, L0 + 7), (L0 + 8, L1)
linhas = [("Ultrassonografia", US_R, fill_sub, N0), ("Tomografia", TC_R, fill_sub, N0),
          ("Total de exames", (L0, L1), fill_tot, N0)]
for rot, (i0, i1), fill, fmt in linhas:
    b.cell(row=r, column=2, value=rot)
    for k in range(len(ORD) + 1):
        col = get_column_letter(cR0 + k)
        b.cell(row=r, column=cR0 + k, value=f"=SUM({col}{i0}:{col}{i1})").number_format = fmt
    for j in range(1, cR1 + 2):
        c = b.cell(row=r, column=j)
        c.font, c.fill, c.border = f_tot, fill, borda
    r += 1
b.cell(row=r, column=2, value="Valor da produção")
for k in range(len(ORD) + 1):
    col = get_column_letter(cR0 + k)
    v = (f"=SUMPRODUCT({col}{L0}:{col}{L1},'Por procedimento'!$E${L0}:$E${L1})" if k < len(ORD)
         else f"=SUM({LR}{r}:{LT}{r})")
    b.cell(row=r, column=cR0 + k, value=v).number_format = RS
for j in range(1, cR1 + 2):
    c = b.cell(row=r, column=j)
    c.font, c.fill, c.border = f_tot, fill_tot, borda
b.column_dimensions["A"].width = 16
b.column_dimensions["B"].width = 60
for k in range(len(ORD) + 1):
    b.column_dimensions[get_column_letter(cR0 + k)].width = 15
b.column_dimensions[CK].width = 13
b.freeze_panes = "C5"

for ws in (a, b):
    ws.sheet_view.showGridLines = False
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.sheet_properties.pageSetUpPr.fitToPage = True
wb.save(saida)
print("salvo:", saida)
