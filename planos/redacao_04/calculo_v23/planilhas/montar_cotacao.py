"""Planilha de pesquisa de precos nas clinicas: referencia = percentual (50%) do valor unitario do plano v23
(tabela SUS + incremento da Portaria SAES/MS 4.282/2026), com colunas para as cotacoes."""
import json, sys
from decimal import Decimal as D
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.formatting.rule import FormulaRule

matriz_json, saida = sys.argv[1:3]
d = json.load(open(matriz_json))
M, UNIT, ORD = d["matriz"], {c: float(D(v)) for c, v in d["unit"].items()}, d["ORD"]
PROC = [
    ("02.05.02.009-7", "Ultrassonografia mamária bilateral", "US"),
    ("02.05.01.004-0", "Ultrassonografia doppler colorido de vasos", "US"),
    ("02.05.02.004-6", "Ultrassonografia de abdômen total", "US"),
    ("02.05.02.018-6", "Ultrassonografia transvaginal", "US"),
    ("02.05.02.005-4", "Ultrassonografia de aparelho urinário", "US"),
    ("02.05.02.012-7", "Ultrassonografia de tireoide", "US"),
    ("02.05.02.010-0", "Ultrassonografia de próstata por via abdominal", "US"),
    ("02.05.02.003-8", "Ultrassonografia de abdômen superior", "US"),
    ("02.06.02.003-1", "Tomografia computadorizada de tórax", "TC"),
    ("02.06.03.001-0", "Tomografia computadorizada de abdômen superior", "TC"),
    ("02.06.03.003-7", "Tomografia computadorizada de pelve, bacia e abdômen inferior", "TC"),
]
QTD = {c: sum(M[c][p] for p in ORD) for c, _, _ in PROC}
NCLIN = 4

A = "Arial"
f_tit = Font(name=A, size=13, bold=True)
f_nota = Font(name=A, size=9, italic=True, color="555555")
f_leg = Font(name=A, size=9, color="333333")
f_cab = Font(name=A, size=10, bold=True, color="FFFFFF")
f_in = Font(name=A, size=10, color="0000FF")
f_txt = Font(name=A, size=10)
f_lnk = Font(name=A, size=10, color="008000")          # vem da outra aba
f_b = Font(name=A, size=10, bold=True)
fill_cab = PatternFill("solid", fgColor="1F4E78")
fill_ref = PatternFill("solid", fgColor="E2EFDA")
fill_in = PatternFill("solid", fgColor="FFF2CC")       # celula para preencher
fill_sub = PatternFill("solid", fgColor="DDEBF7")
fill_tot = PatternFill("solid", fgColor="BDD7EE")
fino = Side(style="thin", color="BFBFBF")
borda = Border(left=fino, right=fino, top=fino, bottom=fino)
N0, RS, PC = '#,##0', '"R$" #,##0.00', '0%'


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


wb = Workbook()
ws = wb.active
ws.title = "Cotação"
ws["A1"] = "Pesquisa de preços nas clínicas — ultrassonografia e tomografia (plano v23, 8 meses, 10 polos)"
ws["A1"].font = f_tit
ws["A2"] = ("Preço de referência = percentual (célula D4) do valor unitário do plano, que já inclui o incremento do "
            "Anexo I da Portaria SAES/MS nº 4.282/2026. Exames no plano: total dos 8 meses (planilha do plano).")
ws["A2"].font = f_nota

cel(ws, 4, 1, "Percentual de referência sobre o valor do plano", f_b, b=False)
cel(ws, 4, 4, 0.5, f_in, fill_in, PC, Alignment(horizontal="center"))
ws["E4"] = "← altere aqui para testar outro percentual"
ws["E4"].font = f_leg
ws["A5"] = ("Preencha só as células amarelas: o percentual (D4), os dados de cada clínica (linhas 7 a 10) e o preço "
            "oferecido por exame (colunas G a J). Exemplo: Clínica Imagem Sul · Região Sul · (61) 3333-0000 · "
            "08/10/2026 · US mamária bilateral R$ 48,00. Verde: preço até a referência; vermelho: acima.")
ws["A5"].font = f_leg
ws.merge_cells("A5:L5")
ws["A5"].alignment = Alignment(wrap_text=True, vertical="top")
ws.row_dimensions[5].height = 26

C0 = 7                                            # coluna G = primeira clinica
for k, rot in enumerate(["Clínica", "Região", "Contato", "Data da cotação"]):
    r = 7 + k
    cel(ws, r, C0 - 1, rot, f_b, fill_sub, al=Alignment(horizontal="right"))
    for j in range(NCLIN):
        cel(ws, r, C0 + j, None, f_in, fill_in, "dd/mm/yyyy" if rot.startswith("Data") else None,
            Alignment(horizontal="center"))

H = 11
cab = ["Código", "Procedimento", "Exames no plano", "Valor unitário do plano", "Preço de referência",
       "Valor total na referência"]
for j, h in enumerate(cab, 1):
    cel(ws, H, j, h, f_cab, fill_cab, al=Alignment(horizontal="center", vertical="center", wrap_text=True))
for j in range(NCLIN):
    col = get_column_letter(C0 + j)
    cel(ws, H, C0 + j, f'=IF({col}7="","Clínica {j + 1}",{col}7)', f_cab, fill_cab,
        al=Alignment(horizontal="center", vertical="center", wrap_text=True))
CK, CL = C0 + NCLIN, C0 + NCLIN + 1
cel(ws, H, CK, "Menor preço ofertado", f_cab, fill_cab, al=Alignment(horizontal="center", vertical="center", wrap_text=True))
cel(ws, H, CL, "Menor preço ÷ referência", f_cab, fill_cab,
    al=Alignment(horizontal="center", vertical="center", wrap_text=True))
ws.row_dimensions[H].height = 32

L0 = H + 1
L1 = L0 + len(PROC) - 1
G, J = get_column_letter(C0), get_column_letter(C0 + NCLIN - 1)
for i, (cod, nome, mod) in enumerate(PROC):
    r = L0 + i
    cel(ws, r, 1, cod)
    cel(ws, r, 2, nome)
    cel(ws, r, 3, QTD[cod], f_in, fmt=N0)
    cel(ws, r, 4, UNIT[cod], f_in, fmt=RS)
    cel(ws, r, 5, f"=ROUND(D{r}*$D$4,2)", f_b, fill_ref, RS)
    cel(ws, r, 6, f"=C{r}*E{r}", fmt=RS)
    for j in range(NCLIN):
        cel(ws, r, C0 + j, None, f_in, fill_in, RS)
    cel(ws, r, CK, f'=IF(COUNT({G}{r}:{J}{r})=0,"",MIN({G}{r}:{J}{r}))', fmt=RS)
    cel(ws, r, CL, f'=IF({get_column_letter(CK)}{r}="","",{get_column_letter(CK)}{r}/E{r})', fmt=PC,
        al=Alignment(horizontal="center"))

rng = f"{G}{L0}:{J}{L1}"
ws.conditional_formatting.add(rng, FormulaRule(formula=[f'AND({G}{L0}<>"",{G}{L0}<=$E{L0})'],
                                               fill=PatternFill("solid", fgColor="C6EFCE"), font=Font(color="006100")))
ws.conditional_formatting.add(rng, FormulaRule(formula=[f'AND({G}{L0}<>"",{G}{L0}>$E{L0})'],
                                               fill=PatternFill("solid", fgColor="FFC7CE"), font=Font(color="9C0006")))

US0, US1, TC0 = L0, L0 + 7, L0 + 8
r = L1 + 2
for rot, i0, i1, fill in (("Ultrassonografia", US0, US1, fill_sub), ("Tomografia", TC0, L1, fill_sub),
                          ("Total", L0, L1, fill_tot)):
    cel(ws, r, 2, rot, f_b, fill)
    cel(ws, r, 3, f"=SUM(C{i0}:C{i1})", f_b, fill, N0)
    cel(ws, r, 6, f"=SUM(F{i0}:F{i1})", f_b, fill, RS)
    for j in (1, 4, 5):
        cel(ws, r, j, None, f_b, fill)
    r += 1
r += 1
cel(ws, r, C0 - 1, "Procedimentos cotados", f_b, fill_sub, al=Alignment(horizontal="right"))
for j in range(NCLIN):
    col = get_column_letter(C0 + j)
    cel(ws, r, C0 + j, f"=COUNT({col}{L0}:{col}{L1})&\" de {len(PROC)}\"", f_b, fill_sub,
        al=Alignment(horizontal="center"))
r += 1
cel(ws, r, C0 - 1, "Valor total no preço da clínica", f_b, fill_sub, al=Alignment(horizontal="right"))
for j in range(NCLIN):
    col = get_column_letter(C0 + j)
    cel(ws, r, C0 + j, f"=SUMPRODUCT($C${L0}:$C${L1},{col}{L0}:{col}{L1})", f_b, fill_sub, RS)
r += 1
ws.cell(row=r, column=C0 - 1, value="(soma só os exames cotados)").font = f_nota

for col, w in zip("ABCDEF", (16, 58, 11, 14, 14, 17)):
    ws.column_dimensions[col].width = w
for j in range(NCLIN):
    ws.column_dimensions[get_column_letter(C0 + j)].width = 16
ws.column_dimensions[get_column_letter(CK)].width = 13
ws.column_dimensions[get_column_letter(CL)].width = 12
ws.column_dimensions["F"].width = 30            # rotulos do bloco das clinicas tambem ficam em F
ws.freeze_panes = ws.cell(row=L0, column=3)

# ---------------- aba 2: volume por Regiao ----------------
v = wb.create_sheet("Volume por Região")
v["A1"] = "Volume por Região e valor no preço de referência"
v["A1"].font = f_tit
v["A2"] = ("Estimativa de planejamento: o plano fixa só o total de cada Região e a divisão entre ultrassonografia e "
           "tomografia; a divisão por procedimento segue a fila de cada exame em 15/09/2026. O preço de referência "
           "vem da aba Cotação.")
v["A2"].font = f_nota
v["A2"].alignment = Alignment(wrap_text=True, vertical="top")
v.merge_cells("A2:J2")
v.row_dimensions[2].height = 26
cab = ["Código", "Procedimento", "Preço de referência"] + ORD + ["Total"]
for j, h in enumerate(cab, 1):
    cel(v, 4, j, h, f_cab, fill_cab, al=Alignment(horizontal="center", vertical="center", wrap_text=True))
v.row_dimensions[4].height = 30
R0 = 5
for i, (cod, nome, mod) in enumerate(PROC):
    r = R0 + i
    cel(v, r, 1, cod)
    cel(v, r, 2, nome)
    cel(v, r, 3, f"=Cotação!E{L0 + i}", f_lnk, fill_ref, RS)
    for k, p in enumerate(ORD):
        cel(v, r, 4 + k, M[cod][p], f_in, fmt=N0)
    cel(v, r, 4 + len(ORD), f"=SUM(D{r}:{get_column_letter(3 + len(ORD))}{r})", fmt=N0)
R1 = R0 + len(PROC) - 1
r = R1 + 2
for rot, i0, i1, fill in (("Ultrassonografia", R0, R0 + 7, fill_sub), ("Tomografia", R0 + 8, R1, fill_sub),
                          ("Total de exames", R0, R1, fill_tot)):
    cel(v, r, 2, rot, f_b, fill)
    cel(v, r, 1, None, f_b, fill)
    cel(v, r, 3, None, f_b, fill)
    for k in range(len(ORD) + 1):
        col = get_column_letter(4 + k)
        cel(v, r, 4 + k, f"=SUM({col}{i0}:{col}{i1})", f_b, fill, N0)
    r += 1
cel(v, r, 2, "Valor no preço de referência", f_b, fill_tot)
cel(v, r, 1, None, f_b, fill_tot)
cel(v, r, 3, None, f_b, fill_tot)
for k in range(len(ORD) + 1):
    col = get_column_letter(4 + k)
    f = (f"=SUMPRODUCT({col}{R0}:{col}{R1},$C${R0}:$C${R1})" if k < len(ORD)
         else f"=SUM(D{r}:{get_column_letter(3 + len(ORD))}{r})")
    cel(v, r, 4 + k, f, f_b, fill_tot, RS)
v.column_dimensions["A"].width = 16
v.column_dimensions["B"].width = 58
v.column_dimensions["C"].width = 14
for k in range(len(ORD) + 1):
    v.column_dimensions[get_column_letter(4 + k)].width = 15
v.freeze_panes = "D5"

for s in (ws, v):
    s.sheet_view.showGridLines = False
    s.page_setup.orientation = "landscape"
    s.sheet_properties.pageSetUpPr.fitToPage = True
    s.page_setup.fitToWidth = 1
    s.page_setup.fitToHeight = 0
wb.save(saida)
print("salvo:", saida)
