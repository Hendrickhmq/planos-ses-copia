"""Gera orcamento_propostas_oci_otorrino.xlsx — uma aba: valor por OCI e quantidade em cada cenário."""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

AZUL_ESC = "1F3864"; CINZA = "F2F2F2"
F = lambda **k: Font(name="Arial", **k)
fina = Side(style="thin", color="8EA9DB")
borda = Border(left=fina, right=fina, top=fina, bottom=fina)
BRL = 'R$ #,##0.00;-R$ #,##0.00;"-"'
INT = '#,##0;-#,##0;"-"'

wb = Workbook(); o = wb.active; o.title = "Orçamento"
o.sheet_view.showGridLines = False
for col, w in zip("ABCD", (56, 18, 14, 20)): o.column_dimensions[col].width = w
o["A1"] = "Orçamento — OCIs em Otorrinolaringologia"; o["A1"].font = F(size=14, bold=True, color=AZUL_ESC)
o["A2"] = "Valor por OCI concluída e quantidade de OCIs em cada cenário."; o["A2"].font = F(size=9, italic=True, color="595959")

def cel(ref, valor, fmt=None, negrito=False, fundo=None, alin="right", cor="000000"):
    c = o[ref]; c.value = valor; c.font = F(bold=negrito, color=cor)
    if fmt: c.number_format = fmt
    if fundo: c.fill = PatternFill("solid", fgColor=fundo)
    c.alignment = Alignment(horizontal=alin, vertical="center"); c.border = borda

OCIS = [("Avaliação Diagnóstica de Nasofaringe e de Orofaringe (09.04.01.003-1)", 196.78),
        ("Progressão da Avaliação Diagnóstica de Déficit Auditivo (09.04.01.002-3)", 235.79),
        ("Avaliação Inicial Diagnóstica de Déficit Auditivo (09.04.01.001-5)", 50.00)]

def bloco(l0, nome, qtds):
    o[f"A{l0}"] = nome; o[f"A{l0}"].font = F(bold=True, color=AZUL_ESC, size=11)
    for i, t in enumerate(["OCI", "Valor por OCI", "Quantidade", "Valor total"], start=1):
        c = o.cell(row=l0 + 1, column=i, value=t)
        c.font = F(bold=True, color="FFFFFF"); c.fill = PatternFill("solid", fgColor=AZUL_ESC)
        c.alignment = Alignment(horizontal="center", vertical="center"); c.border = borda
    for i, ((n, v), q) in enumerate(zip(OCIS, qtds)):
        r = l0 + 2 + i
        cel(f"A{r}", n, alin="left"); cel(f"B{r}", v, BRL, cor="0000FF"); cel(f"C{r}", q, INT, cor="0000FF")
        cel(f"D{r}", f"=B{r}*C{r}", BRL)
    t = l0 + 5
    cel(f"A{t}", "Total", alin="left", negrito=True, fundo=CINZA); cel(f"B{t}", None, fundo=CINZA)
    cel(f"C{t}", f"=SUM(C{l0+2}:C{l0+4})", INT, negrito=True, fundo=CINZA)
    cel(f"D{t}", f"=SUM(D{l0+2}:D{l0+4})", BRL, negrito=True, fundo=CINZA)

bloco(4, "Cenário 1 — Só nasofaringe e orofaringe", [3504, 0, 0])
bloco(12, "Cenário 2 — Três OCIs", [1211, 1011, 4255])
o.page_setup.orientation = "landscape"; o.page_setup.fitToWidth = 1; o.sheet_properties.pageSetUpPr.fitToPage = True
wb.save("orcamento_propostas_oci_otorrino.xlsx"); print("ok")
