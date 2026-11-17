"""Planilha para os parceiros: valor cheio de cada procedimento (tabela SUS + incremento da Portaria SAES/MS
4.282/2026), o valor ao parceiro (50%) e os exames previstos nos 8 meses. Vai a quem nao tem o plano: sem
versao, secao, custo administrativo nem a diferenca que fica no projeto."""
import json, sys
from decimal import Decimal as D
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side

matriz_json, saida = sys.argv[1:3]
PARTE = D("0.5")
d = json.load(open(matriz_json))
M, ORD, UNIT = d["matriz"], d["ORD"], {c: D(v) for c, v in d["unit"].items()}
GRUPOS = [
    ("Ultrassonografia", [
        ("02.05.02.009-7", "Ultrassonografia mamária bilateral"),
        ("02.05.01.004-0", "Ultrassonografia doppler colorido de vasos"),
        ("02.05.02.004-6", "Ultrassonografia de abdômen total"),
        ("02.05.02.018-6", "Ultrassonografia transvaginal"),
        ("02.05.02.005-4", "Ultrassonografia de aparelho urinário"),
        ("02.05.02.012-7", "Ultrassonografia de tireoide"),
        ("02.05.02.010-0", "Ultrassonografia de próstata por via abdominal"),
        ("02.05.02.003-8", "Ultrassonografia de abdômen superior"),
    ]),
    ("Tomografia computadorizada", [
        ("02.06.02.003-1", "Tomografia computadorizada de tórax"),
        ("02.06.03.001-0", "Tomografia computadorizada de abdômen superior"),
        ("02.06.03.003-7", "Tomografia computadorizada de pelve, bacia e abdômen inferior"),
    ]),
]

A = "Arial"
f_tit = Font(name=A, size=14, bold=True, color="1F4E78")
f_sub = Font(name=A, size=10, color="555555")
f_cab = Font(name=A, size=10, bold=True, color="FFFFFF")
f_grp = Font(name=A, size=10, bold=True, color="1F4E78")
f_txt = Font(name=A, size=10)
f_b = Font(name=A, size=10, bold=True)
f_nota = Font(name=A, size=9, color="555555")
fill_cab = PatternFill("solid", fgColor="1F4E78")
fill_par = PatternFill("solid", fgColor="E2EFDA")
fill_tot = PatternFill("solid", fgColor="DDEBF7")
linha = Side(style="thin", color="D9D9D9")
borda = Border(bottom=linha)
N0, RS = '#,##0', '"R$" #,##0.00'
CEN = Alignment(horizontal="center", vertical="center", wrap_text=True)

wb = Workbook()
ws = wb.active
ws.title = "Valores"
ws["A1"] = "Exames de ultrassonografia e tomografia — valores por procedimento"
ws["A1"].font = f_tit
ws["A2"] = "Valor por exame realizado, laudado e entregue. Exames previstos para os 8 meses de execução."
ws["A2"].font = f_sub

cab = ["Código SUS", "Procedimento", "Valor cheio por exame", "Valor ao parceiro (50%)",
       "Exames previstos", "Total ao parceiro"]
H = 4
for j, h in enumerate(cab, 1):
    x = ws.cell(row=H, column=j, value=h)
    x.font, x.fill, x.alignment = f_cab, fill_cab, CEN
ws.row_dimensions[H].height = 32

r = H + 1
subtot = []
for grupo, procs in GRUPOS:
    ws.cell(row=r, column=1, value=grupo).font = f_grp
    r += 1
    i0 = r
    for cod, nome in procs:
        vals = [cod, nome, float(UNIT[cod]), float(UNIT[cod] * PARTE), sum(M[cod][p] for p in ORD),
                f"=D{r}*E{r}"]
        for j, v in enumerate(vals, 1):
            x = ws.cell(row=r, column=j, value=v)
            x.font, x.border = f_txt, borda
            x.number_format = {3: RS, 4: RS, 5: N0, 6: RS}.get(j, "General")
            if j == 4:
                x.font, x.fill = f_b, fill_par
        r += 1
    subtot.append(r)
    ws.cell(row=r, column=2, value=f"Subtotal {grupo.split()[0].lower()}").font = f_b
    for j, col in ((5, "E"), (6, "F")):
        x = ws.cell(row=r, column=j, value=f"=SUM({col}{i0}:{col}{r - 1})")
        x.font, x.number_format = f_b, N0 if j == 5 else RS
    r += 2

for j in range(1, 7):
    ws.cell(row=r, column=j).fill = fill_tot
ws.cell(row=r, column=2, value="Total").font = f_b
for j, col in ((5, "E"), (6, "F")):
    x = ws.cell(row=r, column=j, value="=" + "+".join(f"{col}{s}" for s in subtot))
    x.font, x.number_format = f_b, N0 if j == 5 else RS
r += 2

for nota in (
    "Valor cheio: Tabela do SUS com o incremento do Anexo I da Portaria SAES/MS nº 4.282/2026.",
    "Na tomografia, o contraste está incluído no valor do exame e não é pago à parte.",
    "O doppler de vasos inclui o venoso de membros inferiores e o de carótidas; o abdômen total inclui a parede "
    "abdominal; a tomografia de tórax inclui a angiotomografia de coronárias.",
):
    ws.cell(row=r, column=1, value=nota).font = f_nota
    r += 1

for col, w in zip("ABCDEF", (15, 56, 15, 15, 12, 17)):
    ws.column_dimensions[col].width = w
ws.freeze_panes = ws.cell(row=H + 1, column=1)
ws.sheet_view.showGridLines = False
ws.page_setup.orientation = "landscape"
ws.sheet_properties.pageSetUpPr.fitToPage = True
ws.page_setup.fitToWidth, ws.page_setup.fitToHeight = 1, 0
wb.save(saida)
print("salvo:", saida)
