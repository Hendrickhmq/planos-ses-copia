"""Destrincha o rascunho de ofício do parceiro (ISHP, 09/11/2026) em planilha.

Gera planilha_custos_sebastião.xlsx, com duas abas, só com o que o ofício traz:
  Ultrassom          - cada custo do ofício por mês, no período e por exame; o médico por produção
                       e com a garantia; o custo por exame em degraus.
  Tomografia         - o preço da clínica (R$ 175 + R$ 43), unidade a unidade.

Tudo é fórmula: as células em azul são as premissas.
"""
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

SAIDA = Path(__file__).with_name("planilha_custos_sebastião.xlsx")

FONTE = "Arial"
AZUL = Font(name=FONTE, size=10, color="0000FF")
PRETO = Font(name=FONTE, size=10)
VERDE = Font(name=FONTE, size=10, color="008000")
NEGRITO = Font(name=FONTE, size=10, bold=True)
TITULO = Font(name=FONTE, size=14, bold=True)
SECAO = Font(name=FONTE, size=11, bold=True, color="FFFFFF")
NOTA = Font(name=FONTE, size=9, italic=True, color="555555")
F_SECAO = PatternFill("solid", fgColor="1F4E78")
F_CAB = PatternFill("solid", fgColor="D9E1F2")
F_TOTAL = PatternFill("solid", fgColor="F2F2F2")
F_PLANO = PatternFill("solid", fgColor="E2EFDA")
F_ALERTA = PatternFill("solid", fgColor="FCE4D6")
FINA = Side(style="thin", color="BFBFBF")
BORDA = Border(left=FINA, right=FINA, top=FINA, bottom=FINA)

REAL = 'R$ #,##0.00'
INT = '#,##0'
DEC = '#,##0.00'
PCT = '0.0%'


def celula(ws, ref, valor, fonte=PRETO, fmt=None, fill=None, borda=True, wrap=False, alinh=None):
    c = ws[ref]
    c.value = valor
    c.font = fonte
    if fmt:
        c.number_format = fmt
    if fill:
        c.fill = fill
    if borda:
        c.border = BORDA
    c.alignment = Alignment(wrap_text=wrap, vertical="top", horizontal=alinh)
    return c


def secao(ws, linha, texto, ate="J"):
    for col in "ABCDEFGHIJ":
        ws[f"{col}{linha}"].fill = F_SECAO
        if col == ate:
            break
    c = ws[f"A{linha}"]
    c.value = texto
    c.font = SECAO


def cabecalho(ws, linha, textos):
    for col, t in zip("ABCDEFGHIJ", textos):
        celula(ws, f"{col}{linha}", t, NEGRITO, fill=F_CAB, wrap=True, alinh="center")
    ws.row_dimensions[linha].height = 30


def nota(ws, linha, texto):
    c = ws[f"A{linha}"]
    c.value = texto
    c.font = NOTA


def premissa(ws, linha, rotulo, valor, fmt, obs="", entrada=True):
    celula(ws, f"A{linha}", rotulo)
    celula(ws, f"B{linha}", valor, AZUL if entrada else PRETO, fmt)
    celula(ws, f"C{linha}", obs, NOTA, borda=False)


wb = Workbook()
us = wb.active
us.title = "Ultrassom"
tc = wb.create_sheet("Tomografia")

# ============================================================ ULTRASSOM
us["A1"].value = "Ultrassom: o que o ofício do parceiro calculou, custo a custo"
us["A1"].font = TITULO
nota(us, 2, "Fonte: rascunho ISHP_Oficio_12_Meses_USG_Unilateral_TC_Contraste.pdf, de 09/11/2026 (Anexos II e III). "
            "Azul = premissa que pode ser trocada; preto = fórmula; verde = vem de outra aba.")
nota(us, 3, "Só o que o ofício traz: o plano de trabalho não entra nesta planilha. Faixa laranja = ponto de atenção.")

secao(us, 5, "1. Premissas")
premissa(us, 6, "Exames sem Doppler, no período", 40942, INT, "Anexo II: mistura de simulação, não extração da fila")
premissa(us, 7, "Exames com Doppler, no período", 13647, INT, "Anexo II")
premissa(us, 8, "Exames de ultrassom no total", "=B6+B7", INT, "", entrada=False)
premissa(us, 9, "Meses de execução", 12, INT, "10/12/2026 a 09/12/2027")
premissa(us, 10, "Dias úteis por mês", 21, INT, "Anexo II, item 3: 252 dias, sem descontar feriados")
premissa(us, 11, "Salas de ultrassom", "=B76", INT, "soma do quadro 3.4", entrada=False)
premissa(us, 12, "Unidades", "=COUNTA(A70:A75)", INT, "postos de recepção: 1 por unidade", entrada=False)
premissa(us, 13, "Honorário médico por exame sem Doppler", 35, REAL, "Anexo III")
premissa(us, 14, "Honorário médico por exame com Doppler", 40, REAL, "Anexo III")
premissa(us, 15, "Garantia mínima por médico por plantão", 1500, REAL, "o médico recebe o maior entre a garantia e a produção")
premissa(us, 16, "Duração do plantão, em horas", 10, INT, "definido pelo usuário em 11/11 (o ofício usa 480 min úteis)")
premissa(us, 17, "Almoço, em horas", 1, INT, "definido pelo usuário em 11/11")
premissa(us, 18, "Minutos úteis do plantão", "=(B16-B17)*60", INT, "", entrada=False)
premissa(us, 19, "Plantões por sala por dia útil", 1, INT, "hipótese: toda sala abre todo dia útil com um médico")
premissa(us, 20, "Teto de custo do ofício, sem Doppler", 55.87, REAL, "o ofício não diz a origem")
premissa(us, 21, "Teto de custo do ofício, com Doppler", 63.45, REAL, "o ofício não diz a origem")

secao(us, 23, "2. Custos não médicos, como o ofício calculou")
cabecalho(us, 24, ["item", "quantidade", "valor unitário", "por mês", "no período", "por exame", "tipo", "observação"])
fixos = [
    ("Auxiliar de sala", "=B11", 3180, "1 posto por sala; custo do posto com provisões, não é o salário"),
    ("Recepção", "=B12", 3500, "1 posto por unidade; custo do posto com provisões, não é o salário"),
    ("Aluguel da sala", "=B11", 1500, "alvo de negociação, não é cotação aceita"),
    ("Aluguel do aparelho de ultrassom", "=B11", 2500, "1 aparelho por sala"),
    ("Gestão e coordenação (verba do ofício)", 1, 3500, "verba única para a rede; o ofício não detalha"),
    ("Limpeza e resíduos", 1, 2400, "a rede toda"),
    ("Sistemas e comunicação", 1, 1500, "a rede toda"),
    ("Logística e contingência", 1, 2600, "a rede toda; o ofício não detalha"),
]
for i, (nome, qtd, unit, obs) in enumerate(fixos):
    r = 25 + i
    celula(us, f"A{r}", nome)
    celula(us, f"B{r}", qtd, PRETO if isinstance(qtd, str) else AZUL, INT)
    celula(us, f"C{r}", unit, AZUL, REAL)
    celula(us, f"D{r}", f"=B{r}*C{r}", fmt=REAL)
    celula(us, f"E{r}", f"=D{r}*$B$9", fmt=REAL)
    celula(us, f"F{r}", f"=E{r}/$B$8", fmt=REAL)
    celula(us, f"G{r}", "fixo por mês")
    celula(us, f"H{r}", obs, NOTA)
celula(us, "A29", fixos[4][0], fill=F_ALERTA)
celula(us, "A33", "Subtotal fixo", NEGRITO, fill=F_TOTAL)
for col in "BCGH":
    celula(us, f"{col}33", None, fill=F_TOTAL)
for col in "DEF":
    celula(us, f"{col}33", f"=SUM({col}25:{col}32)", NEGRITO, REAL, F_TOTAL)
variaveis = [
    (34, "Materiais", "=177414/54589", "o ofício dá R$ 177.414 para 54.589 exames; cresce com o volume"),
    (35, "Reserva fiscal", 5.994, "hipótese do modelo do ofício, não é alíquota validada"),
]
for r, nome, unit, obs in variaveis:
    celula(us, f"A{r}", nome)
    celula(us, f"B{r}", "=$B$8", fmt=INT)
    celula(us, f"C{r}", unit, AZUL, 'R$ #,##0.000')
    celula(us, f"E{r}", f"=B{r}*C{r}", fmt=REAL)
    celula(us, f"D{r}", f"=E{r}/$B$9", fmt=REAL)
    celula(us, f"F{r}", f"=E{r}/$B$8", fmt=REAL)
    celula(us, f"G{r}", "variável por exame")
    celula(us, f"H{r}", obs, NOTA)
celula(us, "A36", "Subtotal variável", NEGRITO, fill=F_TOTAL)
celula(us, "A37", "TOTAL NÃO MÉDICO", NEGRITO, fill=F_TOTAL)
for r in (36, 37):
    for col in "BCGH":
        celula(us, f"{col}{r}", None, fill=F_TOTAL)
for col in "DEF":
    celula(us, f"{col}36", f"=SUM({col}34:{col}35)", NEGRITO, REAL, F_TOTAL)
    celula(us, f"{col}37", f"={col}33+{col}36", NEGRITO, REAL, F_TOTAL)
celula(us, "H37", "ofício: R$ 1.824.380,47 e R$ 33,42 por exame", NOTA, fill=F_TOTAL)

secao(us, 39, "3. Médico: como a garantia funciona")
nota(us, 40, "Regra do ofício: em cada plantão o médico recebe o MAIOR entre a produção (exames x honorário) e a garantia. "
             "A garantia só custa a mais quando a produção do plantão fica abaixo dela.")
us["A41"].value = "3.1 A partir de quantos exames a garantia deixa de ser cobrada"
us["A41"].font = NEGRITO
linhas31 = [
    (42, "Exames sem Doppler no plantão para a produção alcançar a garantia", "=B15/B13", DEC),
    (43, "Exames com Doppler no plantão para a produção alcançar a garantia", "=B15/B14", DEC),
    (44, "Minutos por exame nesse ritmo, sem Doppler", "=B18/B42", DEC),
    (45, "Minutos por exame nesse ritmo, com Doppler", "=B18/B43", DEC),
    (46, "Mínimo que o médico de uma sala recebe por mês (garantia em todo plantão)", "=B15*B10*B19", REAL),
]
for r, rot, f, fmt in linhas31:
    celula(us, f"A{r}", rot)
    celula(us, f"B{r}", f, fmt=fmt)

us["A48"].value = "3.2 Quanto o médico recebe conforme a agenda do plantão (troque os exames em azul)"
us["A48"].font = NEGRITO
cabecalho(us, 49, ["exames no plantão", "minutos por exame", "produção, sem Doppler", "pago, sem Doppler",
                   "a garantia completa", "médico por exame, sem Doppler", "produção, com Doppler",
                   "pago, com Doppler", "a garantia completa", "médico por exame, com Doppler"])
for i, n in enumerate((10, 15, 20, 24, 27, 30, 36, 43, 50)):
    r = 50 + i
    celula(us, f"A{r}", n, AZUL, INT, alinh="center")
    celula(us, f"B{r}", f"=$B$18/A{r}", fmt=DEC)
    celula(us, f"C{r}", f"=A{r}*$B$13", fmt=REAL)
    celula(us, f"D{r}", f"=MAX($B$15,C{r})", fmt=REAL)
    celula(us, f"E{r}", f"=D{r}-C{r}", fmt=REAL)
    celula(us, f"F{r}", f"=D{r}/A{r}", NEGRITO, REAL)
    celula(us, f"G{r}", f"=A{r}*$B$14", fmt=REAL)
    celula(us, f"H{r}", f"=MAX($B$15,G{r})", fmt=REAL)
    celula(us, f"I{r}", f"=H{r}-G{r}", fmt=REAL)
    celula(us, f"J{r}", f"=H{r}/A{r}", NEGRITO, REAL)
nota(us, 59, "Quando 'a garantia completa' é zero, o médico custa só o honorário. Abaixo disso, cada exame que falta no plantão é pago do mesmo jeito.")

us["A61"].value = "3.3 Melhor cenário: todo plantão com agenda cheia (a garantia nunca é cobrada)"
us["A61"].font = NEGRITO
cabecalho(us, 62, ["item", "exames", "honorário", "por mês", "no período", "por exame", "plantões cheios necessários"])
for r, nome, q, h, pt in ((63, "Sem Doppler", "=B6", "=B13", "$B$42"), (64, "Com Doppler", "=B7", "=B14", "$B$43")):
    celula(us, f"A{r}", nome)
    celula(us, f"B{r}", q, fmt=INT)
    celula(us, f"C{r}", h, fmt=REAL)
    celula(us, f"E{r}", f"=B{r}*C{r}", fmt=REAL)
    celula(us, f"D{r}", f"=E{r}/$B$9", fmt=REAL)
    celula(us, f"F{r}", f"=C{r}", fmt=REAL)
    celula(us, f"G{r}", f"=B{r}/{pt}", fmt=INT)
celula(us, "A65", "Médico só por produção", NEGRITO, fill=F_TOTAL)
celula(us, "B65", "=B8", NEGRITO, INT, F_TOTAL)
celula(us, "C65", None, fill=F_TOTAL)
celula(us, "D65", "=SUM(D63:D64)", NEGRITO, REAL, F_TOTAL)
celula(us, "E65", "=SUM(E63:E64)", NEGRITO, REAL, F_TOTAL)
celula(us, "F65", "=E65/B65", NEGRITO, REAL, F_TOTAL)
celula(us, "G65", "=SUM(G63:G64)", NEGRITO, INT, F_TOTAL)
celula(us, "A66", "Salas abertas por dia útil, em média, nesse caso")
celula(us, "B66", "=G65/(B10*B9)", fmt=DEC)
celula(us, "C66", "de 11 salas da rede", NOTA, borda=False)

us["A68"].value = "3.4 Pior cenário: os exames do ofício espalhados nas 11 salas, abertas todo dia útil"
us["A68"].font = NEGRITO
cabecalho(us, 69, ["unidade", "salas", "exames no período", "plantões no período", "exames por plantão",
                   "minutos por exame", "produção por plantão", "pago por plantão", "médico no período",
                   "médico por exame"])
unidades = [
    ("Clínica Brasília (Ceilândia)", 1, 3540),
    ("Med Brasília (Samambaia)", 1, 5376),
    ("Carneiro de Mendonça (Ceilândia)", 4, 19493),
    ("Infinita (Sobradinho)", 1, 4676),
    ("Infinita (Guará II)", 2, 10752),
    ("PróVida (Gama)", 2, 10752),
]
for i, (nome, salas, exames) in enumerate(unidades):
    r = 70 + i
    celula(us, f"A{r}", nome)
    celula(us, f"B{r}", salas, AZUL, INT)
    celula(us, f"C{r}", exames, AZUL, INT)
    celula(us, f"D{r}", f"=B{r}*$B$10*$B$9*$B$19", fmt=INT)
    celula(us, f"E{r}", f"=C{r}/D{r}", fmt=DEC)
    celula(us, f"F{r}", f"=$B$18/E{r}", fmt=DEC)
    celula(us, f"G{r}", f"=E{r}*$F$65", fmt=REAL)
    celula(us, f"H{r}", f"=MAX($B$15,G{r})", fmt=REAL)
    celula(us, f"I{r}", f"=H{r}*D{r}", fmt=REAL)
    celula(us, f"J{r}", f"=I{r}/C{r}", fmt=REAL)
celula(us, "A76", "Rede", NEGRITO, fill=F_TOTAL)
celula(us, "B76", "=SUM(B70:B75)", NEGRITO, INT, F_TOTAL)
celula(us, "C76", "=SUM(C70:C75)", NEGRITO, INT, F_TOTAL)
celula(us, "D76", "=SUM(D70:D75)", NEGRITO, INT, F_TOTAL)
celula(us, "E76", "=C76/D76", NEGRITO, DEC, F_TOTAL)
celula(us, "F76", "=$B$18/E76", NEGRITO, DEC, F_TOTAL)
celula(us, "G76", "=E76*$F$65", NEGRITO, REAL, F_TOTAL)
celula(us, "H76", "=I76/D76", NEGRITO, REAL, F_TOTAL)
celula(us, "I76", "=SUM(I70:I75)", NEGRITO, REAL, F_TOTAL)
celula(us, "J76", "=I76/C76", NEGRITO, REAL, F_TOTAL)
celula(us, "A77", "Médico por mês, nesse caso")
celula(us, "B77", "=I76/B9", fmt=REAL)
celula(us, "A78", "Quanto a garantia acrescenta ao melhor cenário, no período", fill=F_ALERTA)
celula(us, "B78", "=I76-E65", fmt=REAL)
celula(us, "A79", "Conferência: exames das unidades menos a mistura (deve dar 0)")
celula(us, "B79", "=C76-B8", fmt=INT)
nota(us, 80, "A produção por plantão usa o honorário médio da rede (3.3), porque o ofício não dá a mistura com e sem Doppler por unidade.")

secao(us, 82, "4. Custo por exame: melhor e pior cenário para os mesmos 54.589 exames")
cabecalho(us, 83, ["degrau", "sem Doppler", "com Doppler", "média", "no período", "por mês"])


def degrau(r, rot, b, c, d, e, f, fonte=PRETO, fill=None):
    celula(us, f"A{r}", rot, fonte, fill=fill)
    for col, v in zip("BCDEF", (b, c, d, e, f)):
        celula(us, f"{col}{r}", v, fonte, REAL, fill)


degrau(84, "Médico só por produção", "=B13", "=B14", "=F65", "=E65", "=D65")
degrau(85, "Não médico do ofício", "=F37", "=F37", "=F37", "=E37", "=D37")
degrau(86, "A. MELHOR CENÁRIO: agenda cheia, garantia nunca cobrada (é a conta do ofício)", "=B84+B85", "=C84+C85", "=D84+D85", "=E84+E85", "=F84+F85", NEGRITO, F_TOTAL)
degrau(87, "Teto de custo do ofício", "=B20", "=B21", "=(B20*B6+B21*B7)/B8", "=D87*B8", "=E87/B9")
degrau(88, "Quanto A passa do teto", "=B86-B87", "=C86-C87", "=D86-D87", "=E86-E87", "=F86-F87")
degrau(90, "Médico com a garantia cobrada em todo plantão", "=J76", "=J76", "=J76", "=I76", "=B77")
degrau(91, "Não médico do ofício", "=F37", "=F37", "=F37", "=E37", "=D37")
degrau(92, "B. PIOR CENÁRIO: 11 salas abertas todo dia, garantia sempre cobrada", "=B90+B91", "=C90+C91", "=D90+D91", "=E90+E91", "=F90+F91", NEGRITO, F_ALERTA)
degrau(93, "Quanto B passa do teto", "=B92-B87", "=C92-C87", "=D92-D87", "=E92-E87", "=F92-F87")
nota(us, 94, "No pior cenário o plantão é pago pelo mínimo em todas as unidades; por isso o médico por exame é o mesmo com e sem Doppler.")
nota(us, 95, "O custo real fica entre A e B, conforme quantos plantões a rede abrir para os mesmos exames.")

secao(us, 97, "5. A conta dos tetos, como o ofício fez (sem a garantia)")
tetos = [
    (98, "Sobra para o não médico, sem Doppler (teto menos honorário)", "=B20-B13", REAL),
    (99, "Sobra para o não médico, com Doppler", "=B21-B14", REAL),
    (100, "Limite comum para o não médico", "=MIN(B98,B99)", REAL),
    (101, "Variável não médico por exame (materiais e reserva fiscal)", "=F36", REAL),
    (102, "Sobra por exame para pagar o fixo", "=B100-B101", REAL),
    (103, "Exames necessários no período para caber nos tetos", "=E33/B102", INT),
    (104, "Exames por sala por dia nesse volume", "=B103/(B11*B10*B9)", DEC),
    (105, "Minutos por exame nesse volume", "=B18/B104", DEC),
    (106, "Fixo mensal máximo, mantidos os exames do ofício", "=B102*B8/B9", REAL),
    (107, "Corte necessário no fixo mensal", "=D33-B106", REAL),
]
for r, rot, f, fmt in tetos:
    celula(us, f"A{r}", rot)
    celula(us, f"B{r}", f, fmt=fmt)
nota(us, 108, "Ofício: 113.518 exames, 40,95 por sala por dia, fixo máximo de R$ 52.887,66 e corte de R$ 57.092,34.")

us.column_dimensions["A"].width = 62
for col, w in zip("BCDEFGHIJ", (16, 16, 18, 18, 16, 20, 18, 18, 16)):
    us.column_dimensions[col].width = w
us.column_dimensions["H"].width = 22
us.freeze_panes = "B5"

# ============================================================ TOMOGRAFIA
tc["A1"].value = "Tomografia: o que o ofício do parceiro calculou"
tc["A1"].font = TITULO
nota(tc, 2, "Fonte: rascunho do ofício do ISHP de 09/11/2026 (Anexos II e IV). Os R$ 175 + R$ 43 cobrem tudo o que é do exame "
            "(equipe, aparelho, contraste e laudo), conforme o usuário em 11/11.")
nota(tc, 3, "Azul = premissa; preto = fórmula. Só o que o ofício traz.")

secao(tc, 5, "1. Premissas", "H")
premissa(tc, 6, "Preço da clínica por exame, sem contraste", 175, REAL, "Anexo IV")
premissa(tc, 7, "Adicional quando o contraste é administrado", 43, REAL, "Anexo IV; um por evento de contraste, não por segmento")
premissa(tc, 8, "Preço da clínica por exame, com contraste", "=B6+B7", REAL, "", entrada=False)
premissa(tc, 9, "Parte dos exames com contraste", 0.93, PCT, "informada pela coordenação; é projeção, não obrigação")
premissa(tc, 10, "Meses de execução", 12, INT, "10/12/2026 a 09/12/2027")

secao(tc, 12, "2. O que se paga à clínica, unidade a unidade", "H")
cabecalho(tc, 13, ["unidade", "exames no período", "com contraste", "sem contraste", "custo no período", "por mês",
                   "por exame", "observação"])
tcs = [
    ("Clínica Brasília (Ceilândia)", 3105, ""),
    ("Carneiro de Mendonça (Ceilândia)", 2825, "não tem tomógrafo (usuário, 10/11); a conferir"),
    ("Infinita (Sobradinho)", 2315, ""),
    ("Infinita (Guará II)", 3523, ""),
    ("CIG (Gama)", 1854, ""),
]
for i, (nome, exames, obs) in enumerate(tcs):
    r = 14 + i
    celula(tc, f"A{r}", nome)
    celula(tc, f"B{r}", exames, AZUL, INT)
    celula(tc, f"C{r}", f"=ROUND(B{r}*$B$9,0)", fmt=INT)
    celula(tc, f"D{r}", f"=B{r}-C{r}", fmt=INT)
    celula(tc, f"E{r}", f"=C{r}*$B$8+D{r}*$B$6", fmt=REAL)
    celula(tc, f"F{r}", f"=E{r}/$B$10", fmt=REAL)
    celula(tc, f"G{r}", f"=E{r}/B{r}", fmt=REAL)
    celula(tc, f"H{r}", obs, NOTA)
celula(tc, "A19", "Rede", NEGRITO, fill=F_TOTAL)
for col in "BCD":
    celula(tc, f"{col}19", f"=SUM({col}14:{col}18)", NEGRITO, INT, F_TOTAL)
for col in "EF":
    celula(tc, f"{col}19", f"=SUM({col}14:{col}18)", NEGRITO, REAL, F_TOTAL)
celula(tc, "G19", "=E19/B19", NEGRITO, REAL, F_TOTAL)
celula(tc, "H19", "ofício: R$ 2.928.574,00 e R$ 214,99 por exame", NOTA, fill=F_TOTAL)
celula(tc, "A20", "Se o contraste for usado em 100% dos exames")
celula(tc, "E20", "=B19*B8", fmt=REAL)
nota(tc, 21, "Pagamento por produção. O ofício avisa que garantias mínimas pedidas pelas clínicas não estão incluídas.")

nota(tc, 22, "O ofício não traz custo de agendamento, lançamento ou gestão para a tomografia: só o preço pago à clínica.")

tc.column_dimensions["A"].width = 72
for col, w in zip("BCDEFGH", (18, 20, 16, 18, 16, 14, 44)):
    tc.column_dimensions[col].width = w
tc.freeze_panes = "B5"

for ws in (us, tc):
    ws.sheet_view.showGridLines = False

wb.save(SAIDA)
print(SAIDA)
