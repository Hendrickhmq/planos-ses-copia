"""Planilha resumida da seção 7.1 (falta da SES), com fórmulas. Uso: python3 gerar_faltas_na_taxa_da_ses_20261102.py estudo_filas_imagem_20261102.json faltas_na_taxa_da_ses_20261102.xlsx"""
import json, sys
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.comments import Comment

src, dst = sys.argv[1], sys.argv[2]
rv = json.load(open(src, encoding="utf-8"))["revisao"]
F = {f["codigo"]: f for f in rv["faltas"]}
CURTO = {"ULTRASSONOGRAFIA DOPPLER COLORIDO DE VASOS": "US Doppler de vasos"}
def curto(n):
    n = n.replace("ULTRASSONOGRAFIA", "US").replace("TOMOGRAFIA COMPUTADORIZADA", "TC")
    return n.capitalize().replace("Us ", "US ").replace("Tc ", "TC ")

AR = "Arial"
fn = lambda **k: Font(name=AR, **k)
AZUL, NEG = fn(color="0000FF"), fn(bold=True)
CAB = PatternFill("solid", fgColor="1F4E78"); CABF = fn(bold=True, color="FFFFFF")
AMA = PatternFill("solid", fgColor="FFFF00"); CIN = PatternFill("solid", fgColor="EEEEEE")
ALERTA = PatternFill("solid", fgColor="F8CBAD")
fino = Side(style="thin", color="BFBFBF"); BOR = Border(top=fino, bottom=fino, left=fino, right=fino)
INT, PCT = '#,##0;(#,##0);"-"', '0.0%;(0.0%);"-"'

wb = Workbook()
# ---------- Premissas
pr = wb.active; pr.title = "Premissas"
pr["A1"] = "Premissas"; pr["A1"].font = fn(bold=True, size=14)
pr["A2"] = "Células em amarelo podem ser mudadas; o resto recalcula."; pr["A2"].font = fn(italic=True)
lin = [("Parte das faltas reagendada no mesmo pedido", 0, PCT,
        "0% = cada falta gasta o pedido (pior caso). 100% = toda falta volta ao projeto no mesmo pedido. A fonte não mostra; premissa."),
       ("Falta da premissa do estudo (para comparar)", 0.2, PCT, "Premissa de 20% do estudo das filas (seção 7). O plano não traz taxa."),
       ("Meses de execução", 8, INT, "Prazo de produção usado no estudo das filas.")]
for i, (r, v, f, nota) in enumerate(lin, 4):
    pr.cell(i, 1, r).font = fn(); c = pr.cell(i, 2, v); c.font = AZUL; c.fill = AMA; c.number_format = f
    pr.cell(i, 3, nota).font = fn(italic=True, color="595959")
pr.column_dimensions["A"].width = 46; pr.column_dimensions["B"].width = 12; pr.column_dimensions["C"].width = 100
R, P20 = "Premissas!$B$4", "Premissas!$B$5"

# ---------- Por exame
ws = wb.create_sheet("Por exame")
ws["A1"] = "Pedidos que a carteira 1 gasta com a falta da SES, exame a exame"; ws["A1"].font = fn(bold=True, size=14)
ws["A2"] = ("Azul = dado da fonte (Mapa Social, 02/11/2026; filas do plano, sem emergência, angio coronária, sedação e "
            "reservas do IEV). Preto = fórmula. Controle interno: o plano não traz taxa de faltas."); ws["A2"].font = fn(italic=True)
cab = ["Exame", "Código", "Meta (exames)", "SES: realizados 12 m", "SES: faltas 12 m", "Falta na SES",
       "Pedidos gastos", "A mais que a meta", "Pedidos gastos com 20%", "A mais que com 20%",
       "Fila de hoje", "Entradas em 8 meses", "SES agenda em 8 meses", "Disponíveis, SES mantém a agenda",
       "Faltam, SES mantém a agenda", "Parte da agenda da SES a encaminhar", "Faltam mesmo se a SES parar"]
H = 4
for j, t in enumerate(cab, 1):
    c = ws.cell(H, j, t); c.font = CABF; c.fill = CAB; c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center"); c.border = BOR
ws.row_dimensions[H].height = 48
expl = {6: "faltas ÷ (realizados + faltas), nos agendamentos de out./2025 a set./2026",
        7: "meta + (meta ÷ (1 − falta) − meta) × (1 − parte reagendada da aba Premissas)",
        9: "mesma conta com 20% de faltas",
        14: "fila de hoje + entradas − o que a SES agenda (arranjo a do estudo)",
        16: "o que falta ÷ o que a SES agenda; 100% = ela teria de passar toda a agenda e ainda não basta",
        17: "pedidos gastos − (fila de hoje + entradas): pedido que não existe nas filas do plano (arranjo c)"}
for j, t in expl.items():
    ws.cell(H, j).comment = Comment(t, "estudo")
enc = rv["encaminhamento"]
r0 = H + 1
for k, e in enumerate(enc):
    r = r0 + k; f = F[e["codigo"]]
    vals = {1: curto(e["exame"]), 2: e["codigo"], 3: e["meta"], 4: f["ses_realizados"], 5: f["ses_faltas"],
            11: e["estoque_inicio"], 12: e["entradas_periodo"], 13: e["ses_agenda_periodo"]}
    for j, v in vals.items():
        c = ws.cell(r, j, v); c.font = AZUL if j > 2 else fn()
    form = {6: f"=E{r}/(D{r}+E{r})",
            7: f"=C{r}+(C{r}/(1-F{r})-C{r})*(1-{R})",
            8: f"=G{r}-C{r}",
            9: f"=C{r}+(C{r}/(1-{P20})-C{r})*(1-{R})",
            10: f"=G{r}-I{r}",
            14: f"=MAX(0,K{r}+L{r}-M{r})",
            15: f"=MAX(0,G{r}-N{r})",
            16: f"=IF(M{r}=0,0,MIN(1,O{r}/M{r}))",
            17: f"=MAX(0,G{r}-(K{r}+L{r}))"}
    for j, v in form.items():
        ws.cell(r, j, v).font = fn()
rl = r0 + len(enc) - 1; rt = rl + 1
ws.cell(rt, 1, "Total").font = NEG
for j in (3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17):
    L = ws.cell(4, j).column_letter
    ws.cell(rt, j, f"=SUM({L}{r0}:{L}{rl})").font = NEG
ws.cell(rt, 6, f"=1-C{rt}/(C{rt}+SUMPRODUCT(C{r0}:C{rl},F{r0}:F{rl}/(1-F{r0}:F{rl})))").font = NEG
ws.cell(rt, 6).comment = Comment("Falta média dos pedidos: 1 − meta ÷ (meta ÷ (1 − falta)) somados os exames.", "estudo")
ws.cell(rt, 16, f"=SUMPRODUCT((O{r0}:O{rl}>M{r0}:M{rl})*M{r0}:M{rl}+(O{r0}:O{rl}<=M{r0}:M{rl})*O{r0}:O{rl})/M{rt}").font = NEG
ws.cell(rt, 16).comment = Comment("Pedidos encaminhados (limitados à agenda de cada exame) ÷ toda a agenda da SES.", "estudo")
for r in range(r0, rt + 1):
    for j in range(1, 18):
        c = ws.cell(r, j); c.border = BOR
        c.number_format = PCT if j in (6, 16) else INT
        if r == rt: c.fill = CIN
from openpyxl.formatting.rule import FormulaRule
ws.conditional_formatting.add(f"Q{r0}:Q{rl}", FormulaRule(formula=[f"Q{r0}>0"], fill=ALERTA))
ws.conditional_formatting.add(f"P{r0}:P{rl}", FormulaRule(formula=[f"P{r0}>=0.7"], fill=ALERTA))
ws.column_dimensions["A"].width = 40; ws.column_dimensions["B"].width = 15
for j in range(3, 18): ws.column_dimensions[ws.cell(4, j).column_letter].width = 14
ws.freeze_panes = "C5"
ws.cell(rt + 2, 1, "Laranja: a SES teria de passar 70% ou mais da agenda, ou falta pedido mesmo com ela parando.").font = fn(italic=True)

# ---------- Reagendamento
rg = wb.create_sheet("Reagendamento")
rg["A1"] = "O peso do reagendamento: a mesma falta da SES, com 0%, 50% e 100% das faltas reagendadas"; rg["A1"].font = fn(bold=True, size=14)
rg["A2"] = "Linha 4 em amarelo pode ser mudada. Conta independente da aba Premissas."; rg["A2"].font = fn(italic=True)
rg["A4"] = "Parte das faltas reagendada no mesmo pedido"; rg["A4"].font = NEG
for j, v in zip("BCD", (0, 0.5, 1)):
    c = rg[f"{j}4"]; c.value = v; c.font = AZUL; c.fill = AMA; c.number_format = PCT
X = "'Por exame'!"
M, Fx, K, Lx, Mx = (f"{X}${c}${r0}:${c}${rl}" for c in "CFKLM")
rows = [("Pedidos gastos", lambda c: f"=SUMPRODUCT({M}+({M}/(1-{Fx})-{M})*(1-{c}4))"),
        ("A mais que a meta", lambda c: f"={c}5-{X}$C${rt}"),
        ("Faltam, SES mantém a agenda", lambda c: f"=SUMPRODUCT(({M}+({M}/(1-{Fx})-{M})*(1-{c}4)>{X}$N${r0}:$N${rl})*({M}+({M}/(1-{Fx})-{M})*(1-{c}4)-{X}$N${r0}:$N${rl}))"),
        ("Exames em que falta pedido, SES mantém a agenda", lambda c: f"=SUMPRODUCT(--({M}+({M}/(1-{Fx})-{M})*(1-{c}4)>{X}$N${r0}:$N${rl}+0.5))"),
        ("Faltam mesmo se a SES parar", lambda c: f"=SUMPRODUCT(({M}+({M}/(1-{Fx})-{M})*(1-{c}4)>{K}+{Lx})*({M}+({M}/(1-{Fx})-{M})*(1-{c}4)-{K}-{Lx}))")]
for i, (t, fx) in enumerate(rows, 5):
    rg.cell(i, 1, t).font = fn()
    for j in "BCD":
        c = rg[f"{j}{i}"]; c.value = fx(j); c.font = fn(); c.number_format = INT; c.border = BOR
rg.column_dimensions["A"].width = 52
for j in "BCD": rg.column_dimensions[j].width = 16
rg["A11"] = "Para comparar: a premissa de 20% sem reagendamento pede"; rg["A11"].font = fn()
rg["B11"] = f"=SUMPRODUCT({M}/(1-{P20}))"; rg["B11"].number_format = INT
rg["A12"] = "Falta da SES sem reagendamento, a mais que os 20%"; rg["B12"] = "=B5-B11"; rg["B12"].number_format = INT
rg["A12"].font = fn(); rg["B11"].font = fn(); rg["B12"].font = NEG

# ---------- Resumo (primeira aba)
rs = wb.create_sheet("Resumo", 0)
rs["A1"] = "Plano 4, carteira 1: quantos pedidos a mais com a falta da SES"; rs["A1"].font = fn(bold=True, size=14)
rs["A2"] = "Controle interno, 02/11/2026. Fonte: estudo_filas_imagem_20261102 (seção 7.1). O plano não traz taxa de faltas."
rs["A2"].font = fn(italic=True)
PE = "'Por exame'!"
kpis = [("Exames da carteira 1 (meta)", f"={PE}C{rt}", INT),
        ("Falta da SES, média dos pedidos", f"={PE}F{rt}", PCT),
        ("Parte das faltas reagendada (aba Premissas)", f"={R}", PCT),
        ("Pedidos gastos", f"={PE}G{rt}", INT),
        ("A mais que a meta", f"={PE}H{rt}", INT),
        ("A mais que com 20% de faltas", f"={PE}J{rt}", INT),
        ("Faltam se a SES mantém a agenda", f"={PE}O{rt}", INT),
        ("Parte da agenda da SES a encaminhar", f"={PE}P{rt}", PCT),
        ("Faltam mesmo se a SES parar o eletivo", f"={PE}Q{rt}", INT)]
for i, (t, fx, nf) in enumerate(kpis, 4):
    rs.cell(i, 1, t).font = fn(); c = rs.cell(i, 2, fx); c.font = NEG; c.number_format = nf; c.border = BOR
rs["A14"] = "Os pontos principais"; rs["A14"].font = fn(bold=True, size=12)
pontos = [
    "A conta: pedidos gastos = meta ÷ (1 − falta da SES do exame), se cada falta gastar o pedido. A falta vai de 25% (Doppler, tireoide) a 44% (transvaginal).",
    "O que decide é o reagendamento: entre reagendar tudo (79.533 pedidos) e nada (120.712), são 41 mil pedidos. Veja a aba Reagendamento.",
    "O acordo com a SES precisa dizer que o pedido de quem faltou volta ao projeto, e não à fila.",
    "Com metade reagendada, a conta fica perto da premissa de 20% sem reagendamento (100.123 contra 99.419), e o encaminhamento de parte da agenda da SES basta.",
    "Sem reagendamento, só a mama (1.004) e a bolsa escrotal (182) não fecham nem com a SES parando: baixar a falta com confirmação e encaixe, ou remanejar a meta por termo aditivo.",
    "No ultrassom de abdômen total, abdômen superior e aparelho urinário, a SES teria de passar de 72% a 82% da agenda dela.",
    "A TC tem folga: a SES agenda muito mais do que o projeto pede (8% a 35% a encaminhar). A TC de crânio já pede encaminhamento mesmo sem falta (614 pedidos; no total, 1.767 em 8 exames).",
    "A transvaginal já está sem os 4.000 pedidos reservados à OCI GIN1 do IEV.",
]
for i, t in enumerate(pontos, 15):
    c = rs.cell(i, 1, f"{i-14}. {t}"); c.font = fn(); c.alignment = Alignment(wrap_text=True, vertical="top")
    rs.merge_cells(start_row=i, start_column=1, end_row=i, end_column=3); rs.row_dimensions[i].height = 32
rs.column_dimensions["A"].width = 60; rs.column_dimensions["B"].width = 16; rs.column_dimensions["C"].width = 60
rs["C4"] = "Os números dos pontos abaixo são com 0% das faltas reagendadas." ; rs["C4"].font = fn(italic=True, color="595959")

# ---------- Como calcular
cc = wb.create_sheet("Como calcular")
cc["A1"] = "Como calcular, com a mama"; cc["A1"].font = fn(bold=True, size=14)
mr = r0 + [e["codigo"] for e in enc].index("02.05.02.009-7")
passos = [("Falta da SES", f"faltas ÷ (realizados + faltas)", f"={PE}F{mr}", PCT),
          ("Meta", "exames realizados e laudados", f"={PE}C{mr}", INT),
          ("Pedidos gastos", "meta ÷ (1 − falta), com 0% reagendado", f"={PE}C{mr}/(1-{PE}F{mr})", INT),
          ("A mais que a meta", "pedidos gastos − meta", "=C6-C5", INT),
          ("Disponíveis, SES mantém a agenda", "fila de hoje + entradas em 8 meses − agenda da SES em 8 meses", f"={PE}N{mr}", INT),
          ("Faltam", "pedidos gastos − disponíveis", "=MAX(0,C6-C8)", INT),
          ("Agenda de mama da SES em 8 meses", "o máximo que ela pode encaminhar", f"={PE}M{mr}", INT),
          ("Faltam mesmo se a SES encaminhar tudo", "faltam − agenda da SES", "=MAX(0,C9-C10)", INT)]
for j, t in enumerate(["Passo", "Conta", "Resultado"], 1):
    c = cc.cell(3, j, t); c.font = CABF; c.fill = CAB
for i, (a, b, fx, nf) in enumerate(passos, 4):
    cc.cell(i, 1, a).font = fn(); cc.cell(i, 2, b).font = fn(); c = cc.cell(i, 3, fx); c.font = fn(); c.number_format = nf
    for j in (1, 2, 3): cc.cell(i, j).border = BOR
cc["A13"] = "Vaga não é pedido: o reagendamento não é pedido novo, e o exame realizado conta uma vez. Baixa na fila não é exame feito."
cc["A13"].font = fn(italic=True)
cc.column_dimensions["A"].width = 38; cc.column_dimensions["B"].width = 62; cc.column_dimensions["C"].width = 14
wb.save(dst)
