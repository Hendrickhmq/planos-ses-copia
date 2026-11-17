"""Gera cenarios_oci_otorrino.xlsx — valor de cada OCI e quantidade em cada cenário.
Entradas na aba 'Valores das OCIs'; cenários calculados por fórmula."""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.comments import Comment

AZUL_ESC = "1F3864"; CINZA = "F2F2F2"
F = lambda **k: Font(name="Arial", **k)
fina = Side(style="thin", color="8EA9DB")
borda = Border(left=fina, right=fina, top=fina, bottom=fina)
BRL = 'R$ #,##0.00;-R$ #,##0.00;"-"'
INT = '#,##0;-#,##0;"-"'

wb = Workbook()

def titulo(ws, texto, sub, larg):
    ws.sheet_view.showGridLines = False
    ws["A1"] = texto; ws["A1"].font = F(size=14, bold=True, color=AZUL_ESC)
    ws["A2"] = sub; ws["A2"].font = F(size=9, italic=True, color="595959")
    for i, w in enumerate(larg, start=1):
        ws.column_dimensions[chr(64 + i)].width = w

def cab(ws, linha, textos):
    for i, t in enumerate(textos, start=1):
        c = ws.cell(row=linha, column=i, value=t)
        c.font = F(bold=True, color="FFFFFF"); c.fill = PatternFill("solid", fgColor=AZUL_ESC)
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True); c.border = borda
    ws.row_dimensions[linha].height = 28

def cel(ws, ref, valor, fmt=None, entrada=False, negrito=False, fundo=None, alin="right"):
    c = ws[ref]; c.value = valor
    c.font = F(bold=negrito, color="0000FF" if entrada else "000000")
    if fmt: c.number_format = fmt
    if fundo: c.fill = PatternFill("solid", fgColor=fundo)
    c.alignment = Alignment(horizontal=alin, vertical="center")
    c.border = borda
    return c

# ---------------- Valores das OCIs ----------------
ws = wb.active; ws.title = "Valores das OCIs"
titulo(ws, "Valores das OCIs em Otorrinolaringologia", "Tabela de Procedimentos do SUS (SIGTAP), competência 09/2026. Valores em azul são entradas.", [56, 18, 18])
cab(ws, 4, ["OCI", "Código SIGTAP", "Valor SIGTAP"])
ocis = [("Avaliação Diagnóstica de Nasofaringe e de Orofaringe", "09.04.01.003-1", 393.55),
        ("Progressão da Avaliação Diagnóstica de Déficit Auditivo", "09.04.01.002-3", 471.57),
        ("Avaliação Inicial Diagnóstica de Déficit Auditivo", "09.04.01.001-5", 100.00)]
for r, (n, cod, v) in enumerate(ocis, start=5):
    cel(ws, f"A{r}", n, alin="left"); cel(ws, f"B{r}", cod, alin="center")
    c = cel(ws, f"C{r}", v, BRL, entrada=True)
    c.comment = Comment("SIGTAP, competência 09/2026." + (" Valor fixado pela Portaria SAES/MS nº 4.795/2026." if cod != "09.04.01.001-5" else ""), "planos-ses")
ws["A9"] = "Parâmetros dos cenários"; ws["A9"].font = F(bold=True, color=AZUL_ESC)
cel(ws, "A10", "Valor disponível para as OCIs", alin="left")
c = cel(ws, "B10", 1379087.00, BRL, entrada=True); c.comment = Comment("Valor da proposta destinado às OCIs.", "planos-ses")
cel(ws, "A11", "Limite da OCI inicial no Cenário 2 (pessoas na fila)", alin="left")
c = cel(ws, "B11", 4255, INT, entrada=True); c.comment = Comment("Fila de audiometria e imitanciometria com CID compatível — Mapa Social da Saúde (MPDFT/SISREG), base de 08/10/2026.", "planos-ses")

def cenario(nome, tit, sub, quantidades):
    s = wb.create_sheet(nome)
    titulo(s, tit, sub, [56, 18, 16, 20])
    cab(s, 4, ["OCI", "Valor SIGTAP", "Quantidade", "Valor total"])
    for i, q in enumerate(quantidades):
        r = 5 + i; pr = 5 + i
        cel(s, f"A{r}", f"='Valores das OCIs'!A{pr}", alin="left")
        cel(s, f"B{r}", f"='Valores das OCIs'!C{pr}", BRL)
        cel(s, f"C{r}", q, INT, negrito=True)
        cel(s, f"D{r}", f"=C{r}*B{r}", BRL)
    cel(s, "A8", "Total", alin="left", negrito=True, fundo=CINZA)
    cel(s, "B8", None, fundo=CINZA)
    cel(s, "C8", "=SUM(C5:C7)", INT, negrito=True, fundo=CINZA)
    cel(s, "D8", "=SUM(D5:D7)", BRL, negrito=True, fundo=CINZA)
    return s

V = "'Valores das OCIs'!"
cenario("Cenário 1", "Cenário 1 — Só Nasofaringe e Orofaringe",
        "Todo o valor disponível na OCI de nasofaringe e orofaringe. Quantidade = parte inteira de (valor disponível ÷ valor da OCI).",
        [f"=INT({V}B10/{V}C5)", 0, 0])
cenario("Cenário 2", "Cenário 2 — Três OCIs",
        "A OCI inicial fica com o menor valor entre 1/3 do disponível e o limite da fila; o restante é dividido em partes iguais entre nasofaringe e progressão.",
        [f"=INT(({V}B10-C7*B7)/2/B5)", f"=INT(({V}B10-C7*B7)/2/B6)", f"=MIN({V}B11,INT({V}B10/3/B7))"])
for s in wb.worksheets:
    s.page_setup.orientation = "landscape"; s.page_setup.fitToWidth = 1; s.sheet_properties.pageSetUpPr.fitToPage = True
wb.save("cenarios_oci_otorrino.xlsx"); print("ok")
