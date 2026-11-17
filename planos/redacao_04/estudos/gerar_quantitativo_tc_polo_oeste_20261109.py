"""Quantitativo mensal de tomografia do polo Oeste, para o parceiro (09/11/2026, pedido do usuário).

Contexto: 4 polos de tomografia (Oeste, Central, Norte e Leste) em 12 meses. Só quantidades, sem valores.

De onde vêm os números:
- a TC total é a do cenário 2 da readequação (estudo_readequacao_candanga_margem_20261109, médico por hora): 14.565;
- a parte de cada Região é a origem da fila de TC por Região de Saúde (estudo das filas de 02/11, participações;
  os pedidos sem Região, de URD e contratados, se repartem na mesma proporção);
- as Regiões sem polo vão ao mais perto: a Sudoeste ao Oeste; o Sul e o Centro-Sul ao Central (premissa deste estudo);
- a rampa: mês 1 a 60% e mês 2 a 85% do ritmo, o resto igual (premissa deste estudo).

Gera tempos/quantitativo_tc_polo_oeste_20261109.xlsx (para o parceiro, uma aba, sem nada interno) e imprime a conta
dos 4 polos.
"""
import os

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(AQUI, "quantitativo_tc_polo_oeste_20261109.xlsx")

TC_TOTAL = 14565
PARTE = {"Oeste": 0.1354, "Sudoeste": 0.4024, "Norte": 0.1348, "Leste": 0.0754, "Central e Centro-Sul": 0.1224,
         "Sul": 0.1296}
POLOS = {"Oeste": ["Oeste", "Sudoeste"], "Central": ["Central e Centro-Sul", "Sul"], "Norte": ["Norte"],
         "Leste": ["Leste"]}
RAMPA = [0.60, 0.85]  # meses 1 e 2, em fração do ritmo pleno

parte_polo = {p: sum(PARTE[r] for r in rs) for p, rs in POLOS.items()}
anual = {p: TC_TOTAL * v for p, v in parte_polo.items()}

A = "Arial"
F, FB, FT, FS = Font(name=A, size=10), Font(name=A, size=10, bold=True), Font(name=A, size=14, bold=True), \
    Font(name=A, size=9, italic=True, color="555555")
CAB = PatternFill("solid", fgColor="D9E1F2")
TOT = PatternFill("solid", fgColor="EDEDED")
BORDA = Border(*(Side(style="thin", color="BFBFBF"),) * 4)
CEN = Alignment(horizontal="center", vertical="center")
ESQ = Alignment(vertical="center", wrap_text=False)

wb = Workbook()
ws = wb.active
ws.title = "Tomografia por mês"
ws.sheet_view.showGridLines = False
ws.column_dimensions["A"].width = 26
ws.column_dimensions["B"].width = 22


def put(ref, v, fmt=None, font=F, fill=None, alin=CEN, borda=True):
    c = ws[ref]
    c.value, c.font, c.alignment = v, font, alin
    if borda:
        c.border = BORDA
    if fill:
        c.fill = fill
    if fmt:
        c.number_format = fmt


put("A1", "Tomografia no polo Oeste: previsão de exames por mês", font=FT, alin=ESQ, borda=False)
put("A2", "Projeto de exames de imagem, 12 meses, 4 polos de tomografia (Oeste, Central, Norte e Leste).", font=FS,
    alin=ESQ, borda=False)
put("A3", "O polo Oeste recebe os pacientes das Regiões de Saúde Oeste e Sudoeste.", font=FS, alin=ESQ, borda=False)

put("A5", "Mês de execução", font=FB, fill=CAB)
put("B5", "Exames de tomografia", font=FB, fill=CAB)
# o ritmo pleno é o que fecha o total com os dois meses de rampa
ritmo = anual["Oeste"] / (12 - (2 - sum(RAMPA)))
valores = [round(ritmo * f) for f in RAMPA] + [round(ritmo)] * 10
valores[-1] += round(anual["Oeste"]) - sum(valores)  # o arredondamento fecha no último mês
for i, v in enumerate(valores):
    r = 6 + i
    put(f"A{r}", f"Mês {i + 1}")
    put(f"B{r}", v, "#,##0")
put("A18", "Total em 12 meses", font=FB, fill=TOT)
put("B18", "=SUM(B6:B17)", "#,##0", FB, TOT)
put("A19", "Média por mês", font=FB, fill=TOT)
put("B19", "=B18/12", "#,##0", FB, TOT)
put("A20", "Por dia útil, no ritmo pleno", font=FB, fill=TOT)
put("B20", "=B8/21", "#,##0", FB, TOT)
notas = [
    "Os dois primeiros meses são de início: a agenda cresce até o ritmo pleno no mês 3.",
    "São exames realizados, com e sem contraste. Os pacientes vêm da regulação da Secretaria de Saúde.",
    "É uma previsão: o número de cada mês pode variar com a fila e com a regulação.",
]
for i, t in enumerate(notas):
    put(f"A{22 + i}", t, font=FS, alin=ESQ, borda=False)
ws.page_setup.orientation = "portrait"
wb.save(SAIDA)

print(SAIDA)
for p in POLOS:
    print(f"{p}: {parte_polo[p]:.1%}  {anual[p]:,.0f} por ano  {anual[p] / 12:,.0f} por mês  {anual[p] / 252:,.1f} por dia")
print("Oeste mês a mês:", valores, sum(valores))


# ================================================================== a demanda total, por Região de Saúde
SAIDA2 = os.path.join(AQUI, "quantitativo_tc_total_por_regiao_20261109.xlsx")
# a Central e a Centro-Sul se separam pelos pedidos de cada uma nas filas de TC (504 e 245)
PARTE_R = {"Oeste": PARTE["Oeste"], "Sudoeste": PARTE["Sudoeste"],
           "Central": PARTE["Central e Centro-Sul"] * 504 / 749, "Centro-Sul": PARTE["Central e Centro-Sul"] * 245 / 749,
           "Sul": PARTE["Sul"], "Norte": PARTE["Norte"], "Leste": PARTE["Leste"]}
wb2 = Workbook()
ws = wb2.active
ws.title = "Tomografia por mês"
ws.sheet_view.showGridLines = False
for col, w in zip("ABCDEFGHI", [22, 12, 12, 12, 12, 12, 12, 12, 12]):
    ws.column_dimensions[col].width = w


def mensal(total):
    rit = total / (12 - (2 - sum(RAMPA)))
    v = [round(rit * f) for f in RAMPA] + [round(rit)] * 10
    v[-1] += round(total) - sum(v)
    return v


put("A1", "Tomografia: previsão de exames por mês, por Região de Saúde", font=FT, alin=ESQ, borda=False)
put("A2", "Projeto de exames de imagem, 12 meses. Pela Região de Saúde da unidade que pediu o exame.", font=FS,
    alin=ESQ, borda=False)
regs = list(PARTE_R)
serie = {g: mensal(TC_TOTAL * PARTE_R[g]) for g in regs}
serie["Leste"][-1] += TC_TOTAL - sum(sum(v) for v in serie.values())  # fecha o total no arredondamento
put("A4", "Mês de execução", font=FB, fill=CAB)
for j, g in enumerate(regs + ["Total"]):
    put(f"{'BCDEFGHI'[j]}4", g, font=FB, fill=CAB)
for i in range(12):
    r = 5 + i
    put(f"A{r}", f"Mês {i + 1}")
    for j, g in enumerate(regs):
        put(f"{'BCDEFGH'[j]}{r}", serie[g][i], "#,##0")
    put(f"I{r}", f"=SUM(B{r}:H{r})", "#,##0", FB)
put("A17", "Total em 12 meses", font=FB, fill=TOT)
for c in "BCDEFGHI":
    put(f"{c}17", f"=SUM({c}5:{c}16)", "#,##0", FB, TOT)
wb2.save(SAIDA2)
print(SAIDA2)
