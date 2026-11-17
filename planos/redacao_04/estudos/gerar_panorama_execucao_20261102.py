"""Planilha resumida do panorama de execução do plano 4 (carteira 1), com fórmulas, a partir do estudo das filas.
Uso: python3 gerar_panorama_execucao_20261102.py estudo_filas_imagem_20261102.json panorama_execucao_plano4_20261102.xlsx
Depois, recalcular (recalc.py do skill xlsx) para gravar os valores das fórmulas."""
import json
import sys
from collections import defaultdict
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.formatting.rule import FormulaRule, DataBarRule

src, dst = sys.argv[1], sys.argv[2]
d = json.load(open(src, encoding="utf-8"))
rv = d["revisao"]
c1 = next(v for k, v in d["cenarios"].items() if k.startswith("1 "))
CURTO = {"02.05.01.004-0": "Doppler (carótidas, membros, renais)", "02.05.02.004-6": "Abdômen total (com a parede)",
         "02.05.02.009-7": "Mama bilateral", "02.05.02.018-6": "Transvaginal (sem os 4.000 do IEV)",
         "02.05.02.005-4": "Aparelho urinário", "02.05.02.012-7": "Tireoide", "02.05.02.010-0": "Próstata por via abdominal",
         "02.05.02.003-8": "Abdômen superior", "02.05.02.007-0": "Bolsa escrotal", "02.05.02.016-0": "Pélvica",
         "02.05.02.017-8": "Transfontanela", "02.06.03.001-0": "TC de abdômen superior", "02.06.03.003-7": "TC de pelve",
         "02.06.02.003-1": "TC de tórax, sem a angio coronária", "02.06.01.007-9": "TC de crânio",
         "02.06.01.005-2": "TC de pescoço", "02.06.01.004-4": "TC de face"}

AR = "Arial"
def fn(**k): return Font(name=AR, **k)
AZUL_T = "1F4E78"
CAB, CABF = PatternFill("solid", fgColor=AZUL_T), fn(bold=True, color="FFFFFF")
TOT = PatternFill("solid", fgColor="DDEBF7")
ALERTA, ATENCAO, OK = (PatternFill("solid", fgColor=c) for c in ("F8CBAD", "FFE699", "C6E0B4"))
lado = Side(style="thin", color="BFBFBF")
BOR = Border(top=lado, bottom=lado, left=lado, right=lado)
INT, PCT, RS = '#,##0;(#,##0);"-"', '0%;(0%);"-"', '"R$" #,##0.00;("R$" #,##0.00);"-"'
ENTRADA = fn(color="0000FF")


def titulo(ws, t, nota):
    ws.sheet_view.showGridLines = False
    ws["A1"] = t; ws["A1"].font = fn(bold=True, size=15, color=AZUL_T)
    ws["A2"] = nota; ws["A2"].font = fn(italic=True, size=9, color="595959")


def cabecalho(ws, r, cols):
    for j, t in enumerate(cols, 1):
        c = ws.cell(r, j, t); c.font = CABF; c.fill = CAB; c.border = BOR
        c.alignment = Alignment(wrap_text=True, horizontal="center", vertical="center")
    ws.row_dimensions[r].height = 45


wb = Workbook()
pan = wb.active; pan.title = "Panorama"

# ---------- Por exame
ex = wb.create_sheet("Por exame")
titulo(ex, "Carteira 1, exame a exame: o que entregar, quanto agendar e de onde vêm os pedidos",
       "Azul = dado do estudo (Mapa Social de 02/11/2026; Tabela SUS Candanga). Preto = fórmula. Filas do plano: sem "
       "emergência, angio coronária, sedação e reservas do IEV. Falta = a da SES nos 12 meses, no código inteiro.")
cols = ["Exame", "Código", "Modalidade", "Meta (exames realizados)", "Preço (Candanga)", "Valor",
        "Fila de hoje", "Entradas em 8 meses", "SES agenda em 8 meses", "Falta na SES",
        "Vagas a agendar", "Vagas por mês", "Pedidos que sobram para o projeto, se a SES mantém a agenda",
        "Faltam pedidos: toda falta reagendada", "Faltam pedidos: nenhuma falta reagendada",
        "Parte da agenda da SES a encaminhar", "Leitura"]
H = 4
cabecalho(ex, H, cols)
it = defaultdict(lambda: {"meta": 0, "valor": 0.0, "precos": set(), "mod": ""})
for i in c1:
    x = it[i["codigo"]]; x["meta"] += i["meta"]; x["valor"] += i["valor"]; x["precos"].add(i["preco"]); x["mod"] = i["modalidade"]
fal = {f["codigo"]: f for f in rv["faltas"]}
enc = {e["codigo"]: e for e in rv["encaminhamento"]}
cods = sorted(it, key=lambda c: (it[c]["mod"], -it[c]["meta"]), reverse=False)
cods = [c for c in cods if it[c]["mod"] == "Ultrassom"] + [c for c in cods if it[c]["mod"] == "Tomografia"]
r0 = H + 1
for k, c in enumerate(cods):
    r = r0 + k; x, f, e = it[c], fal[c], enc[c]
    assert len(x["precos"]) == 1 and x["meta"] == f["meta"] == e["meta"], c
    falta = f["ses_faltas"] / (f["ses_realizados"] + f["ses_faltas"])
    dados = {1: CURTO[c], 2: c, 3: x["mod"], 4: x["meta"], 5: x["precos"].pop(), 7: e["estoque_inicio"],
             8: e["entradas_periodo"], 9: e["ses_agenda_periodo"], 10: falta}
    for j, v in dados.items():
        ex.cell(r, j, v).font = ENTRADA if j >= 4 else fn()
    form = {6: f"=D{r}*E{r}", 11: f"=D{r}/(1-J{r})", 12: f"=K{r}/Panorama!$C$7",
            13: f"=MAX(0,G{r}+H{r}-I{r})", 14: f"=MAX(0,D{r}-M{r})", 15: f"=MAX(0,K{r}-M{r})",
            16: f"=IF(I{r}=0,0,MIN(1,O{r}/I{r}))",
            17: (f'=IF(K{r}>G{r}+H{r},"falta pedido mesmo se a SES parar",IF(P{r}>=0.7,"a SES teria de passar 70% ou mais '
                 f'da agenda",IF(N{r}>0,"falta pedido mesmo sem faltas: a SES precisa encaminhar",IF(O{r}>0,'
                 f'"depende do reagendamento ou do encaminhamento","folgado"))))')}
    for j, v in form.items():
        ex.cell(r, j, v).font = fn()
rl = r0 + len(cods) - 1; rt = rl + 1
ex.cell(rt, 1, "Total").font = fn(bold=True)
for j in (4, 6, 7, 8, 9, 11, 12, 13, 14, 15):
    L = ex.cell(H, j).column_letter
    ex.cell(rt, j, f"=SUM({L}{r0}:{L}{rl})").font = fn(bold=True)
ex.cell(rt, 10, f"=1-D{rt}/K{rt}").font = fn(bold=True)
ex.cell(rt, 16, f"=SUMPRODUCT((O{r0}:O{rl}>I{r0}:I{rl})*I{r0}:I{rl}+(O{r0}:O{rl}<=I{r0}:I{rl})*O{r0}:O{rl})/I{rt}").font = fn(bold=True)
fmt = {4: INT, 5: RS, 6: RS, 7: INT, 8: INT, 9: INT, 10: PCT, 11: INT, 12: INT, 13: INT, 14: INT, 15: INT, 16: PCT}
for r in range(r0, rt + 1):
    for j in range(1, 18):
        c = ex.cell(r, j); c.border = BOR
        if j in fmt: c.number_format = fmt[j]
        if j == 17: c.alignment = Alignment(wrap_text=True, vertical="top")
        if r == rt: c.fill = TOT
rng = f"Q{r0}:Q{rl}"
ex.conditional_formatting.add(rng, FormulaRule(formula=[f'LEFT(Q{r0},10)="falta pedi"'], fill=ALERTA))
ex.conditional_formatting.add(rng, FormulaRule(formula=[f'LEFT(Q{r0},5)="a SES"'], fill=ALERTA))
ex.conditional_formatting.add(rng, FormulaRule(formula=[f'LEFT(Q{r0},7)="depende"'], fill=ATENCAO))
ex.conditional_formatting.add(rng, FormulaRule(formula=[f'Q{r0}="folgado"'], fill=OK))
ex.conditional_formatting.add(f"P{r0}:P{rl}", DataBarRule(start_type="num", start_value=0, end_type="num", end_value=1, color="F4B183"))
larg = [34, 15, 11, 11, 11, 15, 10, 10, 10, 9, 10, 9, 14, 12, 12, 11, 34]
for j, w in enumerate(larg, 1): ex.column_dimensions[ex.cell(H, j).column_letter].width = w
ex.freeze_panes = "B5"
notas = ["Vagas a agendar = meta ÷ (1 − falta na SES): os horários a marcar para chegar à meta se o projeto faltar como a SES.",
         "Pedidos que sobram para o projeto = fila de hoje + entradas em 8 meses − o que a SES agenda nas mesmas filas.",
         "Faltam pedidos: com toda falta reagendada no mesmo pedido, o projeto gasta a meta; sem nenhuma, gasta as vagas. "
         "A fonte não mostra o reagendamento.",
         "Parte da agenda da SES a encaminhar: o que falta (nenhuma reagendada) ÷ o que a SES agenda; 100% = não basta.",
         "A mesma conta, com mais colunas, está na planilha completa (abas Faltas e pedidos, Metas pela falta da SES e "
         "Encaminhamento SES)."]
for i, t in enumerate(notas, rt + 2):
    ex.cell(i, 1, t).font = fn(italic=True, size=9, color="595959")

# ---------- Por polo
po = wb.create_sheet("Por polo")
titulo(po, "Capacidade por polo: as 20 salas de ultrassom e os 5 tomógrafos em 8 meses",
       "Cada sala ou tomógrafo: 10 horas por dia útil, 8 de exame (as outras 2 para preparo e laudo), 21 dias úteis por "
       "mês. Uso acima de 100% = o polo não dá conta.")
po["A4"] = "Horas de exame por sala em 8 meses"; po["A4"].font = fn()
po["B4"] = "=8*21*Panorama!$C$7"; po["B4"].number_format = INT; po["B4"].font = fn()
cp = rv["capacidade"]
POLOS = list(cp["salas"])
cabecalho(po, 6, ["Polo", "Exames de ultrassom", "Horas de exame", "Salas", "Uso, faltas repostas por encaixe",
                  "Uso, 20% das faltas sem reposição", "Exames de TC", "Horas de TC", "Carga própria (tomógrafos)",
                  "Tem tomógrafo?"])
tem_tc = set(rv["premissas"]["polos_com_tomografo"])
for k, p in enumerate(POLOS):
    r = 7 + k
    vals = [p, cp["exames_us"][p], round(cp["horas_us"][p]), cp["salas"][p], f"=C{r}/(D{r}*$B$4)", f"=C{r}/0.8/(D{r}*$B$4)",
            cp["exames_tc"][p], round(cp["horas_tc"][p]), f"=H{r}/$B$4",
            "sim" if p in tem_tc else "não: vai à Central e Centro-Sul"]
    for j, v in enumerate(vals, 1):
        c = po.cell(r, j, v); c.border = BOR
        c.font = ENTRADA if j in (2, 3, 4, 7, 8) else fn()
        c.number_format = PCT if j in (5, 6) else ('0.00' if j == 9 else INT)
rt2 = 7 + len(POLOS)
po.cell(rt2, 1, "Total").font = fn(bold=True)
for j, L in ((2, "B"), (3, "C"), (4, "D"), (7, "G"), (8, "H")):
    po.cell(rt2, j, f"=SUM({L}7:{L}{rt2-1})").number_format = INT
po.cell(rt2, 5, f"=C{rt2}/(D{rt2}*$B$4)").number_format = PCT
po.cell(rt2, 6, f"=C{rt2}/0.8/(D{rt2}*$B$4)").number_format = PCT
po.cell(rt2, 9, f"=H{rt2}/$B$4").number_format = '0.00'
po.cell(rt2, 10, f'=COUNTIF(J7:J{rt2-1},"sim")&" tomógrafos"')
for j in range(1, 11):
    c = po.cell(rt2, j); c.fill = TOT; c.border = BOR; c.font = fn(bold=True)
po.conditional_formatting.add(f"E7:F{rt2}", FormulaRule(formula=["E7>1"], fill=ALERTA))
po.conditional_formatting.add(f"E7:F{rt2}", FormulaRule(formula=["AND(E7>0.9,E7<=1)"], fill=ATENCAO))
for j, w in enumerate([24, 12, 11, 8, 13, 13, 11, 10, 12, 30], 1):
    po.column_dimensions[po.cell(6, j).column_letter].width = w
for i, t in enumerate([
        "Carga 1 = um tomógrafo cheio. A Leste não tem tomógrafo e manda os exames à Central e Centro-Sul; o Sudoeste passa "
        "de um tomógrafo e divide com o Oeste (estudo de 20/10). Na rede, os 5 tomógrafos ficam em 71% com as faltas "
        "repostas e em 89% com 20% sem reposição.",
        "Na rede, as 20 salas aguentam até 11% de faltas sem reposição. Repor a falta por encaixe (publicar mais vagas do "
        "que cabe, sabendo que parte falta) é o que faz caber. Com 20% sem reposição, bastariam 25 salas.",
        "As salas e os tomógrafos das clínicas ainda não foram confirmados (L-006)."], rt2 + 2):
    po.cell(i, 1, t).font = fn(italic=True, size=9, color="595959")

# ---------- Pendências
pe = wb.create_sheet("Pendências e riscos")
titulo(pe, "O que a execução depende de resolver", "Ordem: o que trava primeiro. Controle interno.")
cabecalho(pe, 4, ["#", "Ponto", "Por que importa", "Com quem", "Situação"])
itens = [
    ("Encaminhamento da SES", "Sem ele, mesmo com toda falta reagendada, falta pedido em 8 exames (1.767 pedidos). A "
     "regulação precisa mandar ao projeto, exame a exame, a parte que falta, e reduzir a própria agenda na mesma medida.",
     "Regulação da SES", "a pactuar"),
    ("Reagendamento depois da falta", "Decide quantos pedidos o projeto gasta: de 79.533 (toda falta reagendada no mesmo "
     "pedido) a 120.712 (nenhuma, com a falta da SES). O acordo precisa dizer que o pedido de quem faltou volta ao "
     "projeto, e não à fila.", "Regulação da SES", "a pactuar; medir depois"),
    ("Confirmação e encaixe", "Baixar a falta abaixo da SES (34%) é o que fecha a mama e a bolsa escrotal, e o que faz as "
     "20 salas caberem (aguentam até 11% de faltas sem reposição).", "Operação do projeto", "a desenhar"),
    ("Parede abdominal (L-007)", "3.304 exames e R$ 388.253,04 da carteira dependem de a SES confirmar, por escrito, que a "
     "fila de parede é feita e faturada como abdômen total.", "SES", "aguardando"),
    ("IEV, um pedido, um plano (L-008)", "A US de articulação fica fora inteira, e 4.000 transvaginais ficam reservadas à "
     "OCI GIN1. Falta a resposta da regulação: os pedidos das filas de exame vão às OCI do IEV?", "Regulação da SES",
     "pergunta a refazer"),
    ("Parque instalado (L-006)", "As 20 salas e os 5 tomógrafos ainda não foram confirmados com as clínicas. Sudoeste e "
     "Sul ficam acima de 100% com 20% das faltas sem reposição.", "Clínicas", "a confirmar"),
    ("Fila perto do início", "A fila observada caiu cerca de 2.900 pedidos por mês desde 15/09; a TC e a mama caem "
     "rápido. Medir de novo quando houver data de início.", "Mapa Social", "medir depois"),
    ("Crianças", "1.463 exames de filas infantis: decidir se a rede das clínicas atende (a transfontanela saiu).", "Usuário",
     "a decidir"),
    ("Custos", "A sobra por exame usa premissas (sala, médico, insumo); a pélvica fica negativa com 20% das faltas sem "
     "reposição. A cotação fica para a etapa de custos.", "Etapa de custos", "depois"),
]
for k, (a, b, c, s) in enumerate(itens, 1):
    r = 4 + k
    for j, v in enumerate((k, a, b, c, s), 1):
        cc = pe.cell(r, j, v); cc.border = BOR; cc.font = fn(bold=(j == 2))
        cc.alignment = Alignment(wrap_text=True, vertical="top")
    pe.row_dimensions[r].height = 48
for j, w in enumerate([4, 30, 90, 18, 20], 1):
    pe.column_dimensions[pe.cell(4, j).column_letter].width = w

# ---------- Carteira 6
PE_ = "'Por exame'!"
k6 = next(k for k in d["cenarios"] if k.startswith("6"))
m6 = defaultdict(int)
for i in d["cenarios"][k6]:
    m6[i["codigo"]] += i["meta"]
c6 = wb.create_sheet("Carteira 6")
titulo(c6, "Carteira 6, com folga: a carteira 1 limitada aos pedidos que chegam, e o resto em TC",
       "Mesmos dados da aba Por exame. Amarelo = premissa que pode mudar; o resto recalcula. Estudo, seção 7.2.")
prem = [("Parte das faltas reagendada no mesmo pedido", 0.5), ("Parte da agenda da SES encaminhada ao projeto", 0.2)]
for k, (t, v) in enumerate(prem, 4):
    c6.cell(k, 1, t).font = fn()
    c = c6.cell(k, 3, v); c.font = ENTRADA; c.number_format = PCT; c.border = BOR
    c.fill = PatternFill("solid", fgColor="FFFF00")
H6 = 7
cabecalho(c6, H6, ["Exame", "Código", "Meta, carteira 1", "Meta, carteira 6", "Diferença", "Valor, carteira 6",
                   "Falta na SES", "Pedidos gastos, carteira 6", "Pedidos que chegam: SES mantém a agenda + o encaminhado",
                   "Faltam pedidos", "Sem encaminhamento: faltam", "Parte da agenda da SES a encaminhar"])
for k, c in enumerate(cods):
    r, rp = H6 + 1 + k, r0 + k
    vals = {1: f"={PE_}A{rp}", 2: f"={PE_}B{rp}", 3: f"={PE_}D{rp}", 4: m6[c], 5: f"=D{r}-C{r}",
            6: f"=D{r}*{PE_}E{rp}", 7: f"={PE_}J{rp}", 8: f"=D{r}*(1+(1/(1-G{r})-1)*(1-$C$4))",
            9: f"={PE_}M{rp}+$C$5*{PE_}I{rp}", 10: f"=MAX(0,H{r}-I{r})", 11: f"=MAX(0,H{r}-{PE_}M{rp})",
            12: f"=IF({PE_}I{rp}=0,0,MIN(1,K{r}/{PE_}I{rp}))"}
    for j, v in vals.items():
        cc = c6.cell(r, j, v); cc.border = BOR
        cc.font = ENTRADA if j == 4 else (fn(color="008000") if j in (1, 2, 3, 7) else fn())
        cc.number_format = {6: RS, 7: PCT, 12: PCT}.get(j, INT)
rl6 = H6 + len(cods); rt6 = rl6 + 1
c6.cell(rt6, 1, "Total").font = fn(bold=True)
for j in (3, 4, 5, 6, 8, 9, 10, 11):
    L = c6.cell(H6, j).column_letter
    c6.cell(rt6, j, f"=SUM({L}{H6+1}:{L}{rl6})").number_format = RS if j == 6 else INT
c6.cell(rt6, 12, f"=K{rt6}/{PE_}I{rt}").number_format = PCT
for j in range(1, 13):
    cc = c6.cell(rt6, j); cc.fill = TOT; cc.border = BOR; cc.font = fn(bold=True)
c6.conditional_formatting.add(f"E{H6+1}:E{rl6}", FormulaRule(formula=[f"E{H6+1}<0"], fill=ATENCAO))
c6.conditional_formatting.add(f"E{H6+1}:E{rl6}", FormulaRule(formula=[f"E{H6+1}>0"], fill=OK))
c6.conditional_formatting.add(f"J{H6+1}:J{rl6}", FormulaRule(formula=[f"J{H6+1}>0"], fill=ALERTA))
for j, w in enumerate([34, 15, 11, 11, 10, 15, 9, 12, 16, 10, 12, 12], 1):
    c6.column_dimensions[c6.cell(H6, j).column_letter].width = w
c6.freeze_panes = c6.cell(H6 + 1, 2)
for i, t in enumerate([
        "Meta da carteira 6 = a do estudo (azul). Verde = vem da aba Por exame. Pedidos gastos = meta × (1 + (1 ÷ (1 − falta) − 1) "
        "× (1 − parte reagendada)).",
        "Faltam pedidos = pedidos gastos − (o que sobra com a agenda da SES mantida + a parte encaminhada). Com as premissas "
        "de 50% e 20%, nenhum exame fica sem pedido.",
        "Sem encaminhamento: o que falta se a SES não passar nada. Mesmo na carteira 6, a regulação precisa encaminhar: a SES "
        "agenda nas mesmas filas mais do que a fila de hoje.",
        "Mudar as premissas recalcula os pedidos, mas não refaz a carteira: as metas da 6 saem do estudo com 50% e 20%."], rt6 + 2):
    c6.cell(i, 1, t).font = fn(italic=True, size=9, color="595959")

# ---------- Panorama
titulo(pan, "Plano 4 — panorama de execução da carteira 1",
       "Controle interno, 02/11/2026. Resumo do estudo das filas de imagem (estudo_filas_imagem_20261102). Ultrassom e "
       "tomografia ambulatoriais, preço da Tabela SUS Candanga. Nada daqui foi aplicado ao plano.")
PE = "'Por exame'!"
PP = "'Por polo'!"
blocos = [
    ("O que o plano entrega", [
        ("Exames realizados e laudados (meta)", f"={PE}D{rt}", INT, ""),
        ("Valor dos exames", f"={PE}F{rt}", RS, "o valor dos exames da v26 é R$ 10.636.542,52"),
        ("Prazo de produção (meses)", 8, INT, "premissa do estudo"),
        ("Procedimentos (códigos)", f"=COUNTA({PE}B{r0}:B{rl})", INT, ""),
        ("Exames por mês", f"=C5/C7", INT, ""),
    ]),
    ("Com que estrutura", [
        ("Salas de ultrassom", f"={PP}D{rt2}", INT, "20 salas em 6 polos"),
        ("Uso das salas, faltas repostas", f"={PP}E{rt2}", PCT, "aguentam até 11% de faltas sem reposição"),
        ("Uso das salas, 20% das faltas sem reposição", f"={PP}F{rt2}", PCT, "acima de 100%: não cabe"),
        ("Tomógrafos", 5, INT, "a Leste usa o da Central e Centro-Sul"),
        ("Carga dos tomógrafos (exames de TC ÷ capacidade)", f"={PP}I{rt2}/C15", PCT, ""),
    ]),
    ("Quanto agendar (com a falta da SES)", [
        ("Falta média na SES", f"={PE}J{rt}", PCT, "de 25% (Doppler, tireoide) a 44% (transvaginal)"),
        ("Vagas a agendar", f"={PE}K{rt}", INT, "meta ÷ (1 − falta), exame a exame"),
        ("Vagas por mês", f"={PE}L{rt}", INT, ""),
        ("Vagas por dia útil", "=C21/21", INT, "21 dias úteis por mês"),
    ]),
    ("De onde vêm os pedidos (filas do plano)", [
        ("Fila de hoje", f"={PE}G{rt}", INT, "pedidos esperando em 02/11"),
        ("Entradas em 8 meses", f"={PE}H{rt}", INT, "média dos 12 meses × 8"),
        ("O que a SES agenda nas mesmas filas em 8 meses", f"={PE}I{rt}", INT, "ela realiza só 56% do que agenda"),
        ("Pedidos que sobram para o projeto, se a SES mantém a agenda", f"={PE}M{rt}", INT, ""),
        ("Faltam pedidos, toda falta reagendada", f"={PE}N{rt}", INT, "a SES precisa encaminhar mesmo sem falta"),
        ("Faltam pedidos, nenhuma falta reagendada", f"={PE}O{rt}", INT, "o pior caso"),
        ("Parte da agenda da SES a encaminhar, no pior caso", f"={PE}P{rt}", PCT, ""),
    ]),
]
r = 4
for nome, linhas in blocos:
    pan.cell(r, 2, nome).font = fn(bold=True, size=12, color=AZUL_T); r += 1
    for rot, v, f, nota in linhas:
        pan.cell(r, 2, rot).font = fn()
        c = pan.cell(r, 3, v); c.number_format = f; c.border = BOR
        c.font = ENTRADA if not str(v).startswith("=") else fn(bold=True)
        pan.cell(r, 4, nota).font = fn(italic=True, size=9, color="595959")
        r += 1
    r += 1
# confere as posições usadas nas fórmulas acima
assert pan["B5"].value.startswith("Exames realizados") and pan["B7"].value.startswith("Prazo")
assert pan["B15"].value == "Tomógrafos" and pan["B21"].value == "Vagas por mês"
pan.cell(r, 2, "A carteira 6, com folga (aba Carteira 6)").font = fn(bold=True, size=12, color=AZUL_T); r += 1
C6 = "'Carteira 6'!"
for rot, v, f, nota in (("Exames, carteira 6", f"={C6}D{rt6}", INT, "a carteira 1 limitada aos pedidos que chegam; o resto em TC"),
                        ("Valor, carteira 6", f"={C6}F{rt6}", RS, ""),
                        ("Faltam pedidos, com as premissas da 6", f"={C6}J{rt6}", INT, "metade das faltas reagendada; 20% da agenda da SES"),
                        ("Sem encaminhamento da SES, faltam", f"={C6}K{rt6}", INT, "a regulação ainda precisa encaminhar"),
                        ("Parte da agenda da SES a encaminhar", f"={C6}L{rt6}", PCT, "")):
    pan.cell(r, 2, rot).font = fn()
    c = pan.cell(r, 3, v); c.number_format = f; c.border = BOR; c.font = fn(bold=True)
    pan.cell(r, 4, nota).font = fn(italic=True, size=9, color="595959")
    r += 1
r += 1
r_status = r
pan.cell(r, 2, "Os exames, um a um (carteira 1)").font = fn(bold=True, size=12, color=AZUL_T); r += 1
for rot, crit, fill in (("Folgados", '"folgado"', OK),
                        ("Dependem do reagendamento ou do encaminhamento", '"depende*"', ATENCAO),
                        ("Falta pedido mesmo sem faltas (a SES precisa encaminhar)", '"falta pedido mesmo sem*"', ATENCAO),
                        ("A SES teria de passar 70% ou mais da agenda", '"a SES*"', ALERTA),
                        ("Falta pedido mesmo se a SES parar", '"falta pedido mesmo se a SES*"', ALERTA)):
    pan.cell(r, 2, rot).font = fn()
    c = pan.cell(r, 3, f"=COUNTIF({PE}Q{r0}:Q{rl},{crit})"); c.font = fn(bold=True); c.border = BOR; c.fill = fill
    r += 1
r += 1
pan.cell(r, 2, "A leitura").font = fn(bold=True, size=12, color=AZUL_T); r += 1
for t in [
    "1. A estrutura dá conta se a falta for reposta por encaixe: as salas ficam em 89% e os tomógrafos em 71%. Sem "
    "reposição, Sudoeste e Sul passam de 100%.",
    "2. Para chegar a 79.533 exames com a falta da SES (34%), é preciso agendar cerca de 120 mil vagas: 15 mil por mês.",
    "3. O plano não se sustenta só com a fila: a SES agenda nas mesmas filas. Sem encaminhamento da regulação, falta "
    "pedido até com toda falta reagendada.",
    "4. O que decide o número de pedidos é o reagendamento: o pedido de quem faltou precisa voltar ao projeto.",
    "5. Mama e bolsa escrotal são as mais apertadas: sem reagendamento, falta pedido mesmo com a SES parando. A saída é "
    "baixar a falta ou remanejar a meta por termo aditivo.",
    "6. A TC tem folga de pedido (a SES agenda muito mais do que o projeto pede); o aperto está no ultrassom.",
    "As pendências estão na aba Pendências e riscos. O plano não traz taxa de faltas: é controle interno."]:
    c = pan.cell(r, 2, t); c.font = fn(); c.alignment = Alignment(wrap_text=True, vertical="top")
    pan.merge_cells(start_row=r, start_column=2, end_row=r, end_column=4); pan.row_dimensions[r].height = 30; r += 1
pan.column_dimensions["A"].width = 2; pan.column_dimensions["B"].width = 58
pan.column_dimensions["C"].width = 18; pan.column_dimensions["D"].width = 52
wb.save(dst)
