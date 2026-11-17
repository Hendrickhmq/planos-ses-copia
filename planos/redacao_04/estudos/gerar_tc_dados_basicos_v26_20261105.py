"""Planilha curta com os dados básicos da tomografia na v26 do plano 4 (05/11/2026, pedido do usuário):
nomes e quantidade de exames, por procedimento da Tabela SUS e por fila (com e sem contraste).
As quantidades vêm de calculo_v25/v25.json, o mesmo cálculo da v26.
"""
import json, os

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

AQUI = os.path.dirname(os.path.abspath(__file__))
Q = json.load(open(os.path.join(AQUI, "..", "calculo_v25", "v25.json"), encoding="utf-8"))["Q"]
SAIDA = os.path.join(AQUI, "tc_dados_basicos_v26_20261105.xlsx")

CODIGOS = [("02.06.02.003-1", "Tomografia computadorizada de tórax"),
           ("02.06.03.001-0", "Tomografia computadorizada de abdômen superior"),
           ("02.06.03.003-7", "Tomografia computadorizada de pelve, bacia e abdômen inferior")]
FILAS = [("02.06.03.001-0", "TC de abdômen superior", "com contraste", Q["tc_abd"]),
         ("02.06.03.003-7", "TC de pelve, bacia e abdômen inferior", "com contraste", Q["tc_pelve"]),
         ("02.06.02.003-1", "TC de tórax com contraste", "com contraste", Q["tc_torax_c"]),
         ("02.06.02.003-1", "Angiotomografia de coronárias", "com contraste", Q["coronarias"]),
         ("02.06.02.003-1", "TC de tórax sem contraste", "sem contraste", Q["tc_torax_s"])]

F = Font(name="Arial", size=10)
FB = Font(name="Arial", size=10, bold=True)
CAB = PatternFill("solid", fgColor="D9E1F2")
TOT = PatternFill("solid", fgColor="EDEDED")
B = Border(*(Side(style="thin", color="BFBFBF"),) * 4)

wb = Workbook()
ws = wb.active
ws.title = "Tomografia"
ws.sheet_view.showGridLines = False
for col, w in zip("ABCD", (16, 58, 16, 12)):
    ws.column_dimensions[col].width = w


def linha(r, vals, font=F, fill=None, fmt=None):
    for c, v in enumerate(vals, 1):
        cell = ws.cell(row=r, column=c, value=v)
        cell.font, cell.border = font, B
        cell.alignment = Alignment(vertical="center", wrap_text=True)
        if fill:
            cell.fill = fill
        if fmt and c == len(vals):
            cell.number_format = fmt


ws["A1"] = "Plano 4 (v26) — tomografia: procedimentos e quantidade de exames"
ws["A1"].font = Font(name="Arial", size=13, bold=True)
ws["A2"] = "Plano de trabalho v26, enviado à SES (8 meses). Exames por procedimento da Tabela SUS e por fila."
ws["A2"].font = Font(name="Arial", size=9, italic=True, color="555555")

linha(4, ["Código", "Procedimento (Tabela SUS)", "", "Exames"], FB, CAB)
for i, (cod, nome) in enumerate(CODIGOS):
    r = 5 + i
    linha(r, [cod, nome, "", f'=SUMIF($A$13:$A$17,A{r},$D$13:$D$17)'], fmt="#,##0")
linha(8, ["", "Total", "", "=SUM(D5:D7)"], FB, TOT, "#,##0")

linha(12, ["Código", "Fila", "Contraste", "Exames"], FB, CAB)
for i, (cod, fila, contr, q) in enumerate(FILAS):
    linha(13 + i, [cod, fila, contr, q], fmt="#,##0")
linha(18, ["", "Com contraste", "", '=SUMIF($C$13:$C$17,"com contraste",$D$13:$D$17)'], FB, TOT, "#,##0")
linha(19, ["", "Sem contraste", "", '=SUMIF($C$13:$C$17,"sem contraste",$D$13:$D$17)'], FB, TOT, "#,##0")
linha(20, ["", "Total", "", "=SUM(D13:D17)"], FB, TOT, "#,##0")
ws["A11"] = "Por fila"
ws["A11"].font = FB
ws["A3"] = "Por procedimento"
ws["A3"].font = FB
ws["A22"] = ("A angiotomografia de coronárias e a TC de tórax sem contraste são registradas no código da TC de tórax "
             "(02.06.02.003-1).")
ws["A22"].font = Font(name="Arial", size=9, italic=True, color="555555")
wb.save(SAIDA)
print(SAIDA)
