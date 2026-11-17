"""Estudo interno sobre a v26 do plano 4 (05/11/2026), pedido do usuário em seis partes:

1. as 20 salas de ultrassom (e os tomógrafos) polo a polo;
2. a distribuição da demanda por Região de Saúde, de onde vem a fila;
3. o preço cotado (SIGTAP + incremento da Portaria SAES/MS 4.282) contra a Tabela SUS Candanga;
4. exames por hora de ultrassom e de tomografia (CBR 2017 e pesquisa);
5. duas adaptações com a diferença de preço: mais ultrassom ou mais tomografia;
6. o custo detalhado de cada procedimento (pessoal, estrutura, insumos), com as premissas em amarelo.

A base é a v26 (calculo_v19/calculo.py e calculo_v25/v25.json): as quantidades por fila, a origem por Região da
coleta de 15/09/2026 e os tempos de sala da v26. Tudo na planilha é fórmula sobre as células amarelas.
Recalcular depois de gerar: python3.11 <skill xlsx>/scripts/recalc.py <saída>.
"""
import json, os, sys

from openpyxl import Workbook
from openpyxl.comments import Comment
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter as L

AQUI = os.path.dirname(os.path.abspath(__file__))
PLANO = os.path.join(AQUI, "..")
sys.path.insert(0, os.path.join(PLANO, "calculo_v19"))
import calculo as K  # noqa: E402

V25 = json.load(open(os.path.join(PLANO, "calculo_v25", "v25.json"), encoding="utf-8"))
Q = V25["Q"]
SAIDA = os.path.join(AQUI, "estudo_v26_salas_precos_custos_20261105.xlsx")

# ---------------------------------------------------------------- dados da v26
FILAS = [  # chave, código, nome, modalidade
    ("mama", "02.05.02.009-7", "Ultrassonografia mamária bilateral", "US"),
    ("dop_mmii", "02.05.01.004-0", "Doppler venoso de membros inferiores (bilateral)", "US"),
    ("carotidas", "02.05.01.004-0", "Ecodoppler de carótidas", "US"),
    ("abd_total", "02.05.02.004-6", "Ultrassonografia de abdômen total", "US"),
    ("parede", "02.05.02.004-6", "Ultrassonografia de parede abdominal (código do abdômen total)", "US"),
    ("transvag", "02.05.02.018-6", "Ultrassonografia transvaginal", "US"),
    ("urinario", "02.05.02.005-4", "Ultrassonografia de aparelho urinário", "US"),
    ("tireoide", "02.05.02.012-7", "Ultrassonografia de tireoide", "US"),
    ("prostata", "02.05.02.010-0", "Ultrassonografia de próstata por via abdominal", "US"),
    ("abd_sup", "02.05.02.003-8", "Ultrassonografia de abdômen superior", "US"),
    ("tc_abd", "02.06.03.001-0", "TC de abdômen superior (com contraste)", "TC"),
    ("tc_pelve", "02.06.03.003-7", "TC de pelve, bacia e abdômen inferior (com contraste)", "TC"),
    ("tc_torax_c", "02.06.02.003-1", "TC de tórax com contraste", "TC"),
    ("coronarias", "02.06.02.003-1", "Angiotomografia de coronárias (código da TC de tórax)", "TC"),
    ("tc_torax_s", "02.06.02.003-1", "TC de tórax sem contraste", "TC"),
]
REG7 = ["Oeste", "Sudoeste", "Norte", "Leste", "Central", "Centro-Sul", "Sul"]
POLOS = ["Oeste", "Sudoeste", "Norte", "Leste", "Central e Centro-Sul", "Sul"]
SALAS_V26 = {"Oeste": 1, "Sudoeste": 6, "Norte": 2, "Leste": 3, "Central e Centro-Sul": 3, "Sul": 5}
CODIGOS = [  # código, nome, valor de tabela, incremento da 4.282, Candanga (Anexo Único, SIA)
    ("02.05.02.009-7", "Ultrassonografia mamária bilateral", 24.20, 3.13, 70.97),
    ("02.05.01.004-0", "Ultrassonografia doppler colorido de vasos", 39.60, 1.53, 115.61),
    ("02.05.02.004-6", "Ultrassonografia de abdômen total", 37.95, 1.64, 117.51),
    ("02.05.02.018-6", "Ultrassonografia transvaginal", 24.20, 3.13, 83.77),
    ("02.05.02.005-4", "Ultrassonografia de aparelho urinário", 24.20, 3.13, 90.53),
    ("02.05.02.012-7", "Ultrassonografia de tireoide", 24.20, 3.13, 64.07),
    ("02.05.02.010-0", "Ultrassonografia de próstata por via abdominal", 24.20, 3.13, 74.19),
    ("02.05.02.003-8", "Ultrassonografia de abdômen superior", 24.20, 3.13, 101.27),
    ("02.06.02.003-1", "Tomografia computadorizada de tórax", 136.41, 1.20, 309.25),
    ("02.06.03.001-0", "Tomografia computadorizada de abdômen superior", 138.63, 1.16, 309.25),
    ("02.06.03.003-7", "Tomografia computadorizada de pelve, bacia e abdômen inferior", 138.63, 1.16, 309.25),
]
# tempos (min): CBR 2017 (intervalo de agendamento, tempo com o paciente posicionado), premissa da v26, pesquisa
CBR = {"mama": (20, 15, "US - Mamas"),
       "dop_mmii": (40, 30, "Doppler venoso de membro inferior unilateral (20/15) × 2 membros"),
       "carotidas": (20, 15, "Doppler de vasos cervicais arteriais bilateral"),
       "abd_total": (20, 15, "US - Abdome total"),
       "parede": (15, 10, "US - Estruturas superficiais (parede)"),
       "transvag": (15, 10, "US - Transvaginal"),
       "urinario": (15, 10, "US - Aparelho urinário"),
       "tireoide": (15, 10, "US - Órgãos superficiais (tireoide)"),
       "prostata": (15, 10, "US - Próstata (via abdominal)"),
       "abd_sup": (15, 10, "US - Abdome superior")}
TC_PESQ = {"tc_abd": (17.1, 20, "Erdfarb 2005: exame com contraste, média de 17 min 5 s na sala"),
           "tc_pelve": (17.1, 20, "Erdfarb 2005: exame com contraste, média de 17 min 5 s na sala"),
           "tc_torax_c": (17.1, 20, "Erdfarb 2005: exame com contraste, média de 17 min 5 s na sala"),
           "coronarias": (None, 30, "sem medida publicada encontrada; ECG e controle da frequência cardíaca: premissa de 30 min"),
           "tc_torax_s": (8.6, 15, "Erdfarb 2005: exame sem contraste, média de 8 min 34 s na sala")}
V26_MIN = K.MIN

# ---------------------------------------------------------------- estilo
ARIAL = "Arial"
F_N = Font(name=ARIAL, size=10)
F_B = Font(name=ARIAL, size=10, bold=True)
F_T = Font(name=ARIAL, size=14, bold=True)
F_S = Font(name=ARIAL, size=11, bold=True, color="1F3864")
F_I = Font(name=ARIAL, size=9, italic=True, color="555555")
F_IN = Font(name=ARIAL, size=10, color="0000FF")
F_LK = Font(name=ARIAL, size=10, color="008000")
AMARELO = PatternFill("solid", fgColor="FFF2CC")
CAB = PatternFill("solid", fgColor="D9E1F2")
TOT = PatternFill("solid", fgColor="EDEDED")
FINA = Side(style="thin", color="BFBFBF")
BORDA = Border(left=FINA, right=FINA, top=FINA, bottom=FINA)
WRAP = Alignment(wrap_text=True, vertical="top")
MOEDA = '"R$" #,##0.00'
MOEDA0 = '"R$" #,##0'
INT = '#,##0'
DEC1 = '#,##0.0'
DEC2 = '#,##0.00'
DEC4 = '#,##0.0000'
PCT = '0.0%'

wb = Workbook()
wb.remove(wb.active)


def aba(nome, larguras):
    ws = wb.create_sheet(nome)
    for i, w in enumerate(larguras, 1):
        ws.column_dimensions[L(i)].width = w
    ws.sheet_view.showGridLines = False
    return ws


def ref(ws_nome, cel, abs_=True):
    if abs_:
        col = "".join(c for c in cel if c.isalpha())
        lin = "".join(c for c in cel if c.isdigit())
        cel = f"${col}${lin}"
    return f"'{ws_nome}'!{cel}"


def put(ws, r, c, v, fmt=None, font=None, fill=None, borda=True, wrap=False):
    cell = ws.cell(row=r, column=c, value=v)
    cell.font = font or F_N
    if fmt:
        cell.number_format = fmt
    if fill:
        cell.fill = fill
    if borda:
        cell.border = BORDA
    if wrap:
        cell.alignment = WRAP
    return cell


def entrada(ws, r, c, v, fmt=None, nota=None):
    cell = put(ws, r, c, v, fmt, F_IN, AMARELO)
    if nota:
        cell.comment = Comment(nota, "estudo")
    return cell


# a parte 6 sai em branco, só com a estrutura (pedido do usuário, 05/11/2026): cada campo a preencher fica amarelo e
# vazio, com a referência da pesquisa no comentário, e entra no contador de "faltam preencher" da aba
VAZIOS = {}
F_NA = Font(name=ARIAL, size=10, color="A6A6A6")


def vazio(ws, r, c, fmt=None, sugestao=None):
    cell = entrada(ws, r, c, None, fmt, sugestao)
    VAZIOS.setdefault(ws.title, []).append(cell.coordinate)
    return cell


def nao_usa(ws, r, c, fmt=None):
    return put(ws, r, c, 0, fmt, F_NA)


def contador(ws, r, abas):
    termos = [f"COUNTBLANK('{a}'!{x})" for a in abas for x in VAZIOS.get(a, [])]
    put(ws, r, 1, "Campos ainda vazios" + (" (esta aba e as premissas)" if len(abas) > 1 else ""), font=F_B,
        fill=AMARELO)
    put(ws, r, 2, "=" + ("+".join(termos) if termos else "0"), INT, F_B, AMARELO)


def link(ws, r, c, f, fmt=None):
    return put(ws, r, c, f, fmt, F_LK)


def titulo(ws, t, sub):
    ws.cell(row=1, column=1, value=t).font = F_T
    c = ws.cell(row=2, column=1, value=sub)
    c.font = F_I
    c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=10)
    ws.row_dimensions[2].height = 42


def secao(ws, r, t):
    ws.cell(row=r, column=1, value=t).font = F_S


def cabecalho(ws, r, nomes, c0=1):
    for i, n in enumerate(nomes):
        cell = put(ws, r, c0 + i, n, font=F_B, fill=CAB, wrap=True)
        cell.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
    ws.row_dimensions[r].height = 45


def nota(ws, r, t, ate=10):
    c = ws.cell(row=r, column=1, value=t)
    c.font = F_I
    c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=ate)
    ws.row_dimensions[r].height = max(15, 13 * (len(t) // 150 + 1))


N_SALAS = "1 Salas"
N_DEM = "2 Demanda por Região"
N_PRE = "3 Preços"
N_TEM = "4 Exames por hora"
N_ADA = "5 Adaptações"
N_PC = "6 Premissas de custo"
N_CUS = "6 Custo ultrassom"
N_CTC = "6 Custo tomografia"
N_CCS = "6 Custo TC com e sem contraste"
N_CEN = "6 Cenários sem contraste"

# ================================================================ Leia
ws = aba("Leia", [30, 110])
titulo(ws, "Plano 4 (v26) — salas, demanda, preços, exames por hora e custo por procedimento",
       "Controle interno do ISHP, 05/11/2026. Base: a v26 enviada à SES (79.144 exames, 20 salas de ultrassom e 6 "
       "tomógrafos em 6 polos, 8 meses). Nada daqui vai ao plano sem decisão do usuário.")
linhas = [
    ("Como mexer", "Células amarelas com número azul são premissas: mude e o resto se refaz. Número verde vem de "
                   "outra aba. Número preto é conta. Passe o mouse nas células com triângulo vermelho para ver a fonte."),
    (N_SALAS, "Parte 1. As 20 salas de ultrassom e os 6 tomógrafos da v26, polo a polo: horas de exame, uso das "
              "salas com e sem faltas, salas que bastariam e vagas por dia."),
    (N_DEM, "Parte 2. De onde vem a fila: os pedidos de cada fila por Região de Saúde (coleta de 15/09/2026, a base "
            "da v26), a % de cada Região e os exames da v26 repartidos pelos polos."),
    (N_PRE, "Parte 3. O preço que cotamos (valor da Tabela SIGTAP mais o incremento da Portaria SAES/MS 4.282/2026) "
            "contra a Tabela SUS Candanga, código a código e no total."),
    (N_TEM, "Parte 4. Quantos exames cabem em uma hora de sala, por procedimento: a recomendação do CBR (2017) para "
            "o ultrassom e a pesquisa para a tomografia; e quanto rende uma hora de sala nos dois preços."),
    (N_ADA, "Parte 5. A diferença entre o envelope da v26 e o mesmo mix pela Candanga, gasta de duas formas: "
            "A, mais ultrassom; B, mais tomografia. Com a conferência de salas e tomógrafos."),
    (N_PC, "Parte 6. As premissas do custo: pessoal (salário, encargos, jornada, custo por hora), estrutura "
           "(aluguel, aparelho, tomógrafo, energia) e o preço de cada insumo."),
    (N_CUS, "Parte 6. O custo de cada exame de ultrassom, item a item: médico, recepção, assistente de sala, "
            "higienização, RT, retaguarda, sala, aparelho, sistema e cada insumo, com a margem nos dois preços."),
    (N_CTC, "Parte 6. O mesmo para a tomografia: técnico, enfermagem, radiologista, contraste, seringa da bomba, "
            "cateter, soro e o resto, com a comparação com o preço da clínica parceira."),
    (N_CCS, "Parte 6. Só a tomografia, em duas contas: o exame com contraste e o exame sem contraste, com o mesmo "
            "pessoal, estrutura e insumos, para preencher."),
    (N_CEN, "Parte 6. Cenários de enquadramento: de 100% a 0% dos exames convertíveis feitos com contraste, "
            "com o contraste usado, o custo, a economia, as horas de tomógrafo e a margem."),
    ("Fontes", "As fontes de cada número, com o link."),
    ("Atenção", "A parte 6 está em branco, só com a estrutura: preencha as células amarelas vazias (preços, salários, "
                "encargos e consumo por exame) e o custo final sai sozinho. Cada aba diz quantos campos faltam. O "
                "comentário de cada célula traz o que a pesquisa de 05/11 encontrou, só para conferir. A equipe de gestão (R$ 956.160,00) é "
                "paga pelo apoio do convênio e fica fora do custo do exame. A sobra no convênio não é receita: volta "
                "como saldo ou vira mais exames por termo aditivo."),
]
for i, (a, b) in enumerate(linhas, 4):
    put(ws, i, 1, a, font=F_B, wrap=True)
    put(ws, i, 2, b, wrap=True)
    ws.row_dimensions[i].height = 32
put(ws, 17, 1, "Legenda", font=F_B)
entrada(ws, 18, 1, "premissa (preencha ou mude)")
link(ws, 19, 1, "vem de outra aba")
put(ws, 20, 1, "conta")

# ================================================================ 2 Demanda por Região
ws = aba(N_DEM, [15, 44, 6, 10] + [9] * 7 + [10] + [8] * 7 + [10] * 6)
titulo(ws, "Parte 2 — de onde vem a fila: a demanda por Região de Saúde",
       "Pedidos de cada fila pela Região de Saúde da unidade que pediu o exame (Mapa Social, coleta de 15/09/2026; "
       "ultrassom pela medida fila, tomografia pelo total de solicitações). É a origem que a v26 usou para repartir os "
       "exames (subseção 3.4). Os pedidos sem Região (URD e contratados) não entram na %.")
R0 = 5
cabecalho(ws, R0, ["Código", "Fila (procedimento)", "Mod.", "Exames na v26"] + [f"Pedidos — {r}" for r in REG7] +
          ["Pedidos com Região"] + [f"% {r}" for r in REG7] + [f"Exames v26 — polo {p}" for p in POLOS])
DEM = {}
for i, (k, cod, nome, mod) in enumerate(FILAS):
    r = R0 + 1 + i
    DEM[k] = r
    put(ws, r, 1, cod)
    put(ws, r, 2, nome, wrap=True)
    put(ws, r, 3, mod)
    entrada(ws, r, 4, Q[k], INT, "Quantidade da fila na v26 (calculo_v25/v25.json, Q)")
    for j, reg in enumerate(REG7):
        entrada(ws, r, 5 + j, K.R[k].get("Região " + reg, 0), INT)
    put(ws, r, 12, f"=SUM(E{r}:K{r})", INT)
    for j in range(7):
        put(ws, r, 13 + j, f"=IF($L{r}=0,0,{L(5 + j)}{r}/$L{r})", PCT)
    # polos: Oeste E, Sudoeste F, Norte G, Leste H, Central I + Centro-Sul J, Sul K
    for j, expr in enumerate([f"E{r}", f"F{r}", f"G{r}", f"H{r}", f"(I{r}+J{r})", f"K{r}"]):
        put(ws, r, 20 + j, f"=IF($L{r}=0,0,$D{r}*{expr}/$L{r})", INT)
RF1, RF2 = R0 + 1, R0 + len(FILAS)
RT = RF2 + 1
put(ws, RT, 2, "Total", font=F_B, fill=TOT)
for c in [4] + list(range(5, 13)) + list(range(20, 26)):
    put(ws, RT, c, f"=SUM({L(c)}{RF1}:{L(c)}{RF2})", INT, F_B, TOT)
for j in range(7):
    put(ws, RT, 13 + j, f"=IF($L{RT}=0,0,{L(5 + j)}{RT}/$L{RT})", PCT, F_B, TOT)
for nm, mod, rr in [("Ultrassom", "US", RT + 1), ("Tomografia", "TC", RT + 2)]:
    put(ws, rr, 2, nm, font=F_B, fill=TOT)
    for c in [4] + list(range(5, 13)) + list(range(20, 26)):
        put(ws, rr, c, f'=SUMIF($C${RF1}:$C${RF2},"{mod}",{L(c)}{RF1}:{L(c)}{RF2})', INT, F_B, TOT)
    for j in range(7):
        put(ws, rr, 13 + j, f"=IF($L{rr}=0,0,{L(5 + j)}{rr}/$L{rr})", PCT, F_B, TOT)
nota(ws, RT + 3, "Os exames por polo têm fração porque cada fila se reparte na proporção da sua origem; a v26 "
                 "arredondou pelos maiores restos (4.595, 26.818, 6.699, 12.300, 12.436 e 16.296).", 20)

# resumo por polo
RS = RT + 5
secao(ws, RS, "Resumo por polo: a % da demanda de cada Região")
cabecalho(ws, RS + 1, ["Polo", "Regiões", "", "Pedidos com Região", "% dos pedidos", "Exames v26", "% dos exames",
                       "de ultrassom", "de tomografia", "% do ultrassom", "% da tomografia"])
REGS_P = {"Oeste": ["E"], "Sudoeste": ["F"], "Norte": ["G"], "Leste": ["H"], "Central e Centro-Sul": ["I", "J"], "Sul": ["K"]}
NOME_REG = {"Central e Centro-Sul": "Central e Centro-Sul"}
for i, p in enumerate(POLOS):
    r = RS + 2 + i
    cp = L(20 + i)
    put(ws, r, 1, p, font=F_B)
    put(ws, r, 2, NOME_REG.get(p, p))
    put(ws, r, 4, "=" + "+".join(f"{c}{RT}" for c in REGS_P[p]), INT)
    put(ws, r, 5, f"=D{r}/L{RT}", PCT)
    put(ws, r, 6, f"={cp}{RT}", INT)
    put(ws, r, 7, f"=F{r}/D{RT}", PCT)
    put(ws, r, 8, f"={cp}{RT + 1}", INT)
    put(ws, r, 9, f"={cp}{RT + 2}", INT)
    put(ws, r, 10, f"=H{r}/D{RT + 1}", PCT)
    put(ws, r, 11, f"=I{r}/D{RT + 2}", PCT)
r = RS + 8
put(ws, r, 1, "Total", font=F_B, fill=TOT)
for c in [4, 5, 6, 7, 8, 9, 10, 11]:
    put(ws, r, c, f"=SUM({L(c)}{RS + 2}:{L(c)}{RS + 7})", PCT if c in (5, 7, 10, 11) else INT, F_B, TOT)
DEM_POLO_R0 = RS + 2
nota(ws, RS + 9, "A coluna % dos exames é a participação da subseção 3.4 da v26 (5,81%, 33,89%, 8,46%, 15,54%, "
                 "15,71% e 20,59%). A % dos pedidos é a da fila crua; as duas diferem porque cada procedimento tem "
                 "origem própria e pesa pelo número de exames dele na v26.", 11)
ws.freeze_panes = "C6"

# ================================================================ 1 Salas (parâmetros primeiro, as tabelas depois)
wsS = aba(N_SALAS, [26, 12, 13, 13, 10, 13, 12, 12, 12, 12, 13, 12, 12])
# ================================================================ 4 Exames por hora
ws = aba(N_TEM, [15, 44, 6, 11, 11, 11, 11, 11, 10, 11, 12, 11, 11, 12, 12, 48])
titulo(ws, "Parte 4 — exames por hora de sala, por procedimento",
       "Ultrassom: Recomendação do Colégio Brasileiro de Radiologia (CBR), 14/11/2017 — intervalo mínimo de "
       "agendamento e tempo médio do exame com o paciente posicionado. Tomografia: o CBR não publica tempo; ficam a "
       "medida de Erdfarb e outros (RSNA 2005, 218 exames) e a premissa da v26. O tempo adotado (amarelo) é o que "
       "vale nas abas 1, 5 e 6.")
T0 = 5
cabecalho(ws, T0, ["Código", "Fila (procedimento)", "Mod.", "CBR: intervalo de agendamento (min)",
                   "CBR: tempo médio do exame (min)", "Premissa da v26 (min)", "Pesquisa: tempo medido na sala (min)",
                   "Tempo adotado por exame (min)", "Exames por hora", "Exames por dia por sala (horas úteis)",
                   "Exames por sala no período", "Preço v26 (R$)", "Preço Candanga (R$)",
                   "R$ por hora de sala — v26", "R$ por hora de sala — Candanga", "De onde vem o tempo"])
TEM = {}
for i, (k, cod, nome, mod) in enumerate(FILAS):
    r = T0 + 1 + i
    TEM[k] = r
    put(ws, r, 1, cod)
    put(ws, r, 2, nome, wrap=True)
    put(ws, r, 3, mod)
    if k in CBR:
        a, b, txt = CBR[k]
        put(ws, r, 4, a, INT, F_IN)
        put(ws, r, 5, b, INT, F_IN)
        put(ws, r, 7, None)
        entrada(ws, r, 8, f"=D{r}", DEC1, "Padrão: o intervalo de agendamento do CBR. Mude se o polo praticar outro.")
        put(ws, r, 16, "CBR 2017: " + txt, wrap=True)
    else:
        pesq, adot, txt = TC_PESQ[k]
        put(ws, r, 4, "—")
        put(ws, r, 5, "—")
        put(ws, r, 7, pesq, DEC1, F_IN) if pesq else put(ws, r, 7, "—")
        entrada(ws, r, 8, adot, DEC1, "Tomografia: a premissa da v26 (20 min com contraste, 15 sem); angio "
                                      "coronária 30 min por premissa. Mude se o tomógrafo praticar outro.")
        put(ws, r, 16, txt, wrap=True)
    put(ws, r, 6, V26_MIN[k], INT, F_IN)
    put(ws, r, 9, f"=60/H{r}", DEC1)
    put(ws, r, 10, f"=ROUNDDOWN(I{r}*{ref(N_SALAS, 'B4')}*{ref(N_SALAS, 'B6')},0)", INT)
    put(ws, r, 11, f"=ROUNDDOWN(I{r}*{ref(N_SALAS, 'B7')},0)", INT)
    put(ws, r, 12, f"=INDEX('{N_PRE}'!$F$6:$F$16,MATCH(A{r},'{N_PRE}'!$A$6:$A$16,0))", MOEDA, F_LK)
    put(ws, r, 13, f"=INDEX('{N_PRE}'!$G$6:$G$16,MATCH(A{r},'{N_PRE}'!$A$6:$A$16,0))", MOEDA, F_LK)
    put(ws, r, 14, f"=I{r}*L{r}", MOEDA)
    put(ws, r, 15, f"=I{r}*M{r}", MOEDA)
TF1, TF2 = T0 + 1, T0 + len(FILAS)
r = TF2 + 1
put(ws, r, 2, "Ultrassom — média ponderada pelos exames da v26", font=F_B, fill=TOT, wrap=True)
for c, col in [(6, "F"), (8, "H")]:
    put(ws, r, c, f"=SUMPRODUCT(('{N_DEM}'!$C${RF1}:$C${RF2}=\"US\")*'{N_DEM}'!$D${RF1}:$D${RF2}*{col}{TF1}:{col}{TF2})"
                  f"/'{N_DEM}'!$D${RT + 1}", DEC1, F_B, TOT)
put(ws, r, 9, f"=60/H{r}", DEC1, F_B, TOT)
r += 1
put(ws, r, 2, "Tomografia — média ponderada pelos exames da v26", font=F_B, fill=TOT, wrap=True)
for c, col in [(6, "F"), (8, "H")]:
    put(ws, r, c, f"=SUMPRODUCT(('{N_DEM}'!$C${RF1}:$C${RF2}=\"TC\")*'{N_DEM}'!$D${RF1}:$D${RF2}*{col}{TF1}:{col}{TF2})"
                  f"/'{N_DEM}'!$D${RT + 2}", DEC1, F_B, TOT)
put(ws, r, 9, f"=60/H{r}", DEC1, F_B, TOT)
TEM_MED_US, TEM_MED_TC = TF2 + 1, TF2 + 2
r = TF2 + 4
secao(ws, r, "Como ler")
for t in [
    "Exames por hora = 60 ÷ tempo adotado. O tempo é o da sala ocupada por um paciente: o intervalo do CBR já inclui "
    "entrar, posicionar, examinar, limpar o transdutor e sair; o tempo médio do CBR é só o exame com o paciente "
    "posicionado. Por isso o adotado é o intervalo.",
    "Exames por dia por sala usa as horas úteis da aba 1 (10 h abertas × 80% de aproveitamento = 8 h): o resto é "
    "preparo, intervalo, atraso e manutenção. O CBR manda acrescentar 50% ao tempo em serviço com residente — não é o "
    "caso aqui.",
    "O doppler venoso de membros inferiores da fila é bilateral: o CBR dá 20 min por membro, e a conta usa 40. Na "
    "v26 a premissa era 30. É o exame que mais pesa nas horas de sala.",
    "Na v26 o ultrassom estava a 20 min (doppler a 30). Pelo CBR a mama e o abdômen total ficam em 20 e os exames de "
    "órgão isolado (tireoide, próstata, urinário, transvaginal, abdômen superior, parede) caem para 15: as horas de "
    "ultrassom baixam (aba 1).",
    "Tomografia: a medida da RSNA 2005 (dois tomógrafos, 202 horas observadas) deu 17 min com contraste e 8,6 min sem; "
    "a mesma série mostrou que a agenda de 30 min deixava o aparelho ocioso. Um estudo de 2007 mediu 12, 9,7 e 8 "
    "minutos de sala com 1, 2 e 3 técnicos. A v26 usou 20 e 15, com folga sobre a medida.",
    "R$ por hora de sala = exames por hora × preço. Mostra qual exame paga melhor a hora: o mesmo valor no doppler "
    "bilateral rende menos por hora do que na tireoide, porque ocupa a sala por mais tempo.",
]:
    r += 1
    nota(ws, r, "• " + t, 16)
ws.freeze_panes = "C6"

# ================================================================ 1 Salas
ws = wsS
titulo(ws, "Parte 1 — as 20 salas de ultrassom e os tomógrafos, polo a polo (v26)",
       "Exames de cada polo pela origem da fila (aba 2) × tempo de cada exame (aba 4). Cada sala dá as horas úteis do "
       "período (10 h abertas por dia útil × 168 dias × 80%). As salas por polo são as da v26: uma no mínimo e cada "
       "sala a mais ao polo mais carregado.")
secao(ws, 3, "Parâmetros")
for r, (nm, v, f, nt) in enumerate([
        ("Horas abertas por dia útil", 10, INT, "v26, 7.3: 10 horas por dia útil"),
        ("Dias úteis no período", 168, INT, "v26: 8 meses × 21 dias úteis"),
        ("Aproveitamento das horas abertas", 0.8, PCT, "v26: regra dos 80% (o resto é preparo, intervalo, manutenção)"),
        (None, None, None, None),
        ("Faltas sem reposição — cenário 1", 0.10, PCT, "parte dos horários fica vazia: a sala precisa de agenda maior"),
        ("Faltas sem reposição — cenário 2", 0.20, PCT, "20% a 30% de faltas: estudo de 02/11 (controle interno)")], 4):
    if nm is None:
        put(ws, 7, 1, "Horas úteis por sala no período", font=F_B)
        put(ws, 7, 2, "=B4*B5*B6", INT, F_B)
        put(ws, 7, 3, "10 × 168 × 80% (1.344 h na v26)", borda=False, font=F_I)
        continue
    put(ws, r, 1, nm, font=F_B)
    entrada(ws, r, 2, v, f, nt)
H0 = 11
secao(ws, H0 - 1, "Ultrassom — 20 salas")
cabecalho(ws, H0, ["Polo", "Exames de ultrassom", "Horas pela premissa da v26", "Horas pelo tempo adotado (aba 4)",
                   "Salas", "Horas úteis das salas", "Uso — premissa da v26", "Uso — tempo adotado",
                   "Uso com faltas — cenário 1", "Uso com faltas — cenário 2", "Salas que bastariam no cenário 2",
                   "Vagas por dia útil (faltas do cenário 2)", "Exames por sala por dia útil"])
DCOL = {p: L(20 + i) for i, p in enumerate(POLOS)}
dm = lambda c: f"'{N_DEM}'!${c}${RF1}:${c}${RF2}"
tm = lambda c: f"'{N_TEM}'!${c}${TF1}:${c}${TF2}"
for i, p in enumerate(POLOS):
    r = H0 + 1 + i
    dc = DCOL[p]
    put(ws, r, 1, p, font=F_B)
    link(ws, r, 2, f'=SUMIF({dm("C")},"US",{dm(dc)})', INT)
    link(ws, r, 3, f'=SUMPRODUCT(({dm("C")}="US")*{dm(dc)}*{tm("F")})/60', INT)
    link(ws, r, 4, f'=SUMPRODUCT(({dm("C")}="US")*{dm(dc)}*{tm("H")})/60', INT)
    entrada(ws, r, 5, SALAS_V26[p], INT, "Salas da v26 (calculo_v25/v25.json). Mude para testar outra divisão.")
    put(ws, r, 6, f"=E{r}*$B$7", INT)
    put(ws, r, 7, f"=C{r}/F{r}", PCT)
    put(ws, r, 8, f"=D{r}/F{r}", PCT)
    put(ws, r, 9, f"=D{r}/(1-$B$8)/F{r}", PCT)
    put(ws, r, 10, f"=D{r}/(1-$B$9)/F{r}", PCT)
    put(ws, r, 11, f"=ROUNDUP(D{r}/(1-$B$9)/$B$7,0)", INT)
    put(ws, r, 12, f"=ROUNDUP(B{r}/(1-$B$9)/$B$5,0)", INT)
    put(ws, r, 13, f"=B{r}/$B$5/E{r}", DEC1)
HT = H0 + 7
put(ws, HT, 1, "Rede", font=F_B, fill=TOT)
for c in (2, 3, 4, 5, 6, 11, 12):
    put(ws, HT, c, f"=SUM({L(c)}{H0 + 1}:{L(c)}{H0 + 6})", INT, F_B, TOT)
for c, num in [(7, "C"), (8, "D")]:
    put(ws, HT, c, f"={num}{HT}/F{HT}", PCT, F_B, TOT)
put(ws, HT, 9, f"=D{HT}/(1-$B$8)/F{HT}", PCT, F_B, TOT)
put(ws, HT, 10, f"=D{HT}/(1-$B$9)/F{HT}", PCT, F_B, TOT)
put(ws, HT, 13, f"=B{HT}/$B$5/E{HT}", DEC1, F_B, TOT)
put(ws, HT + 1, 1, "Faltas que a rede aguenta sem reposição", font=F_B)
put(ws, HT + 1, 2, f"=MAX(0,1-D{HT}/F{HT})", PCT, F_B)
put(ws, HT + 1, 3, "acima disso a rede passa de 100% e precisa de encaixe (repor a falta com outro paciente)",
    borda=False, font=F_I)
nota(ws, HT + 2, "Uso acima de 100% num polo quer dizer que as salas dele não dão conta naquele cenário: ou o polo "
                 "repõe as faltas com encaixe (publicar mais vagas do que cabe, sabendo que parte falta), ou manda "
                 "pacientes ao vizinho, ou ganha sala. A v26 já diz que o número de salas é conferido no mês 1.", 13)

C0 = HT + 5
secao(ws, C0 - 1, "Tomografia — 6 tomógrafos na v26 (um por polo)")
cabecalho(ws, C0, ["Polo", "Exames de tomografia", "Horas pela premissa da v26", "Horas pelo tempo adotado (aba 4)",
                   "Tomógrafos", "Horas úteis dos tomógrafos", "Carga própria (tomógrafos cheios)", "Uso — tempo adotado",
                   "Uso com faltas — cenário 2", "Exames por dia útil", "Vagas por dia útil (faltas do cenário 2)"])
for i, p in enumerate(POLOS):
    r = C0 + 1 + i
    dc = DCOL[p]
    put(ws, r, 1, p, font=F_B)
    link(ws, r, 2, f'=SUMIF({dm("C")},"TC",{dm(dc)})', INT)
    link(ws, r, 3, f'=SUMPRODUCT(({dm("C")}="TC")*{dm(dc)}*{tm("F")})/60', INT)
    link(ws, r, 4, f'=SUMPRODUCT(({dm("C")}="TC")*{dm(dc)}*{tm("H")})/60', INT)
    entrada(ws, r, 5, 1, INT, "v26: um tomógrafo por polo. Ponha 0 para testar o cenário de 5 (a Leste sem).")
    put(ws, r, 6, f"=E{r}*$B$7", INT)
    put(ws, r, 7, f"=D{r}/$B$7", DEC2)
    put(ws, r, 8, f'=IF(E{r}=0,"vai ao vizinho",D{r}/F{r})', PCT)
    put(ws, r, 9, f'=IF(E{r}=0,"vai ao vizinho",D{r}/(1-$B$9)/F{r})', PCT)
    put(ws, r, 10, f"=ROUNDUP(B{r}/$B$5,0)", INT)
    put(ws, r, 11, f"=ROUNDUP(B{r}/(1-$B$9)/$B$5,0)", INT)
CT = C0 + 7
put(ws, CT, 1, "Rede", font=F_B, fill=TOT)
for c in (2, 3, 4, 5, 6, 10, 11):
    put(ws, CT, c, f"=SUM({L(c)}{C0 + 1}:{L(c)}{C0 + 6})", INT, F_B, TOT)
put(ws, CT, 7, f"=D{CT}/$B$7", DEC2, F_B, TOT)
put(ws, CT, 8, f"=D{CT}/F{CT}", PCT, F_B, TOT)
put(ws, CT, 9, f"=D{CT}/(1-$B$9)/F{CT}", PCT, F_B, TOT)
nota(ws, CT + 1, "Carga 1 = um tomógrafo cheio. A Sudoeste passa de um tomógrafo e manda o excedente à Oeste, como "
                 "diz a v26 (4.2 e 7.3). A linha Rede mostra o uso do conjunto: com 6 tomógrafos para uma carga de "
                 "pouco mais de 3, sobra folga para manutenção e para levar exame de um polo a outro.", 11)
SAL = {"us_horas": f"'{N_SALAS}'!$D${HT}", "us_salas": f"'{N_SALAS}'!$E${HT}",
       "tc_horas": f"'{N_SALAS}'!$D${CT}", "tc_tomo": f"'{N_SALAS}'!$E${CT}"}
ws.freeze_panes = "B4"

# ================================================================ 3 Preços
ws = aba(N_PRE, [15, 44, 11, 12, 11, 13, 13, 13, 11, 15, 15, 15, 14])
titulo(ws, "Parte 3 — o preço cotado (SIGTAP + incremento) contra a Tabela SUS Candanga",
       "Preço da v26: valor do Serviço Ambulatorial da Tabela SIGTAP acrescido do incremento do Anexo I da Portaria "
       "SAES/MS 4.282/2026, truncado no centavo (8.1 da v26). Candanga: Anexo Único da Deliberação CG-SES-DF 46/2026 "
       "(DODF 178, 24/09/2026), modalidade SIA.")
cabecalho(ws, 5, ["Código", "Procedimento", "Exames na v26", "Valor SIGTAP (R$)", "Incremento da 4.282",
                  "Preço da v26 (R$)", "Tabela SUS Candanga (R$)", "Candanga − v26 (R$)", "Candanga ÷ v26 − 1",
                  "Total na v26 (R$)", "Mesmo mix na Candanga (R$)", "Diferença no total (R$)", "Qual paga mais"])
for i, (cod, nome, tab, inc, cand) in enumerate(CODIGOS):
    r = 6 + i
    put(ws, r, 1, cod)
    put(ws, r, 2, nome, wrap=True)
    link(ws, r, 3, f"=SUMIF('{N_DEM}'!$A${RF1}:$A${RF2},A{r},'{N_DEM}'!$D${RF1}:$D${RF2})", INT)
    entrada(ws, r, 4, tab, MOEDA, "SIGTAP, valor SA (8.1 da v26)")
    entrada(ws, r, 5, inc, '0%', "Portaria SAES/MS 4.282/2026, Anexo I (8.1 da v26)")
    put(ws, r, 6, f"=TRUNC(D{r}*(1+E{r}),2)", MOEDA)
    entrada(ws, r, 7, cand, MOEDA, "Tabela SUS Candanga, Anexo Único (SEI 212117347), SIA")
    put(ws, r, 8, f"=G{r}-F{r}", MOEDA)
    put(ws, r, 9, f"=G{r}/F{r}-1", PCT)
    put(ws, r, 10, f"=C{r}*F{r}", MOEDA)
    put(ws, r, 11, f"=C{r}*G{r}", MOEDA)
    put(ws, r, 12, f"=K{r}-J{r}", MOEDA)
    put(ws, r, 13, f'=IF(G{r}>F{r},"Candanga",IF(G{r}<F{r},"v26","igual"))')
r = 17
put(ws, r, 2, "Total", font=F_B, fill=TOT)
for c in (3, 10, 11, 12):
    put(ws, r, c, f"=SUM({L(c)}6:{L(c)}16)", INT if c == 3 else MOEDA, F_B, TOT)
put(ws, r, 9, "=K17/J17-1", PCT, F_B, TOT)
for nm, crit, rr in [("Ultrassom", "02.05*", 18), ("Tomografia", "02.06*", 19)]:
    put(ws, rr, 2, nm, font=F_B, fill=TOT)
    for c in (3, 10, 11, 12):
        put(ws, rr, c, f'=SUMIF($A$6:$A$16,"{crit}",{L(c)}6:{L(c)}16)', INT if c == 3 else MOEDA, F_B, TOT)
    put(ws, rr, 6, f"=J{rr}/C{rr}", MOEDA, F_B, TOT)
    put(ws, rr, 7, f"=K{rr}/C{rr}", MOEDA, F_B, TOT)
    put(ws, rr, 9, f"=K{rr}/J{rr}-1", PCT, F_B, TOT)
put(ws, 18, 1, "média →", font=F_I, borda=False)
secao(ws, 21, "O envelope e a diferença")
for r, (nm, f, fmt, nt) in enumerate([
        ("Recurso da emenda", 11592762.00, MOEDA, "Ofício 40/2026; v26, 3.1"),
        ("Planejamento, gestão e prestação de contas (apoio)", 956160.00, MOEDA, "v26, seção 8"),
        ("Envelope de produção assistencial", "=B22-B23", MOEDA, None),
        ("Produção na v26 (preço cotado)", "=J17", MOEDA, None),
        ("Mesmo mix pela Candanga", "=K17", MOEDA, None),
        ("Diferença: envelope − mix na Candanga", "=B24-B26", MOEDA, None),
        ("Diferença em % do envelope", "=B27/B24", PCT, None)], 22):
    put(ws, r, 1, nm, font=F_B, wrap=True)
    if isinstance(f, float):
        entrada(ws, r, 2, f, fmt, nt)
    else:
        put(ws, r, 2, f, fmt, F_B if r == 27 else F_N)
nota(ws, 30, "• A Candanga paga mais no doppler, no abdômen total, no abdômen superior e nas três tomografias; paga "
             "menos na mama, na transvaginal, no aparelho urinário, na tireoide e na próstata. Como a mama e a "
             "transvaginal são um terço da v26, o mesmo mix fica mais barato na Candanga, e sobra a diferença da linha "
             "27 — é ela que a aba 5 gasta.", 13)
nota(ws, 31, "• Regra do projeto desde 01/11/2026 (LI-002): o valor é o da Candanga também com recurso federal, salvo "
             "quando o SIGTAP vigente é igual ou maior, ou quando o código está fora do Anexo. Aqui o SIGTAP puro (coluna "
             "D) é sempre menor; o incremento da 4.282 não é SIGTAP vigente. A v26 já assinada ficou com o preço cotado.",
     13)
ws.column_dimensions["A"].width = 30
ws.freeze_panes = "C6"
PRE_DIF = f"'{N_PRE}'!$B$27"
PRE_ENV = f"'{N_PRE}'!$B$24"

# ================================================================ 5 Adaptações
ws = aba(N_ADA, [15, 40, 6, 10, 11, 10, 10, 10, 11, 14, 10, 10, 11, 14])
titulo(ws, "Parte 5 — duas adaptações com a diferença: mais ultrassom (A) ou mais tomografia (B)",
       "Preço da Candanga em tudo. Ponto de partida: os 79.144 exames da v26. A diferença entre o envelope e esse mix "
       "(aba 3) vira exames a mais, repartidos na proporção dos pesos (amarelo; padrão = exames da v26 de cada código). "
       "Cada código recebe um número inteiro de exames; o que não forma exame fica como sobra.")
put(ws, 4, 1, "Diferença a gastar", font=F_B)
link(ws, 4, 2, f"={PRE_DIF}", MOEDA)
put(ws, 5, 1, "Envelope de produção", font=F_B)
link(ws, 5, 2, f"={PRE_ENV}", MOEDA)
A0 = 8
put(ws, A0 - 1, 6, "A — mais ultrassom", font=F_S, borda=False)
put(ws, A0 - 1, 11, "B — mais tomografia", font=F_S, borda=False)
cabecalho(ws, A0, ["Código", "Procedimento", "Mod.", "Exames na v26", "Preço Candanga (R$)",
                   "Peso A", "Exames a mais A", "Exames A", "Valor A (R$)", "Tempo médio do código (min)",
                   "Peso B", "Exames a mais B", "Exames B", "Valor B (R$)"])
for i, (cod, nome, *_r) in enumerate(CODIGOS):
    r = A0 + 1 + i
    mod = "US" if cod.startswith("02.05") else "TC"
    put(ws, r, 1, cod)
    put(ws, r, 2, nome, wrap=True)
    put(ws, r, 3, mod)
    link(ws, r, 4, f"='{N_PRE}'!C{6 + i}", INT)
    link(ws, r, 5, f"='{N_PRE}'!G{6 + i}", MOEDA)
    entrada(ws, r, 6, f"=D{r}" if mod == "US" else 0, INT, "Peso da repartição em A (padrão: exames da v26 no ultrassom, "
                                                          "zero na tomografia). Ponha zero no código cuja fila acabou.")
    put(ws, r, 7, f"=IF(F{r}=0,0,INT($B$4*F{r}/SUMPRODUCT($F${A0 + 1}:$F${A0 + 11},$E${A0 + 1}:$E${A0 + 11})))", INT)
    put(ws, r, 8, f"=D{r}+G{r}", INT)
    put(ws, r, 9, f"=H{r}*E{r}", MOEDA)
    put(ws, r, 10, f"=SUMPRODUCT(({dm('A')}=A{r})*{dm('D')}*{tm('H')})/D{r}", DEC1, F_LK)
    entrada(ws, r, 11, f"=D{r}" if mod == "TC" else 0, INT, "Peso da repartição em B (padrão: exames da v26 na "
                                                           "tomografia, zero no ultrassom).")
    put(ws, r, 12, f"=IF(K{r}=0,0,INT($B$4*K{r}/SUMPRODUCT($K${A0 + 1}:$K${A0 + 11},$E${A0 + 1}:$E${A0 + 11})))", INT)
    put(ws, r, 13, f"=D{r}+L{r}", INT)
    put(ws, r, 14, f"=M{r}*E{r}", MOEDA)
AF1, AF2 = A0 + 1, A0 + 11
r = AF2 + 1
put(ws, r, 2, "Total", font=F_B, fill=TOT)
for c in (4, 7, 8, 12, 13):
    put(ws, r, c, f"=SUM({L(c)}{AF1}:{L(c)}{AF2})", INT, F_B, TOT)
for c in (9, 14):
    put(ws, r, c, f"=SUM({L(c)}{AF1}:{L(c)}{AF2})", MOEDA, F_B, TOT)
ATOT = r
R2 = ATOT + 2
secao(ws, R2, "Comparação")
cabecalho(ws, R2 + 1, ["", "Indicador", "", "v26 na Candanga", "A — mais ultrassom", "B — mais tomografia"])
hus = lambda col: f'SUMPRODUCT(($C${AF1}:$C${AF2}="US")*{col}{AF1}:{col}{AF2}*$J${AF1}:$J${AF2})/60'
htc = lambda col: f'SUMPRODUCT(($C${AF1}:$C${AF2}="TC")*{col}{AF1}:{col}{AF2}*$J${AF1}:$J${AF2})/60'
ind = [
    ("Exames", "=D{t}", "=H{t}", "=M{t}", INT),
    ("de ultrassom", f'=SUMIF($C${AF1}:$C${AF2},"US",D{AF1}:D{AF2})', f'=SUMIF($C${AF1}:$C${AF2},"US",H{AF1}:H{AF2})',
     f'=SUMIF($C${AF1}:$C${AF2},"US",M{AF1}:M{AF2})', INT),
    ("de tomografia", f'=SUMIF($C${AF1}:$C${AF2},"TC",D{AF1}:D{AF2})', f'=SUMIF($C${AF1}:$C${AF2},"TC",H{AF1}:H{AF2})',
     f'=SUMIF($C${AF1}:$C${AF2},"TC",M{AF1}:M{AF2})', INT),
    ("Valor dos exames (R$)", f"=SUMPRODUCT(D{AF1}:D{AF2},E{AF1}:E{AF2})", "=I{t}", "=N{t}", MOEDA),
    ("Sobra no envelope (R$)", "=$B$5-D{v}", "=$B$5-E{v}", "=$B$5-F{v}", MOEDA),
    ("Horas de ultrassom (tempo adotado)", "=" + hus("D"), "=" + hus("H"), "=" + hus("M"), INT),
    ("Uso das salas de ultrassom", "=D{hu}/({us}*{cap})", "=E{hu}/({us}*{cap})", "=F{hu}/({us}*{cap})", PCT),
    ("Horas de tomógrafo (tempo adotado)", "=" + htc("D"), "=" + htc("H"), "=" + htc("M"), INT),
    ("Uso dos tomógrafos", "=D{ht}/({tc}*{cap})", "=E{ht}/({tc}*{cap})", "=F{ht}/({tc}*{cap})", PCT),
]
base = R2 + 2
pos = {"t": ATOT, "v": base + 3, "hu": base + 5, "ht": base + 7,
       "us": SAL["us_salas"], "tc": SAL["tc_tomo"], "cap": ref(N_SALAS, "B7")}
for j, (nm, a, b, c, fmt) in enumerate(ind):
    r = base + j
    put(ws, r, 2, nm, font=F_B)
    for col, f in zip((4, 5, 6), (a, b, c)):
        put(ws, r, col, f.format(**pos), fmt)
nota(ws, base + len(ind) + 1,
     "• A diferença é o que sobra do envelope quando o mesmo mix da v26 é pago pela Candanga. A gasta tudo em "
     "ultrassom, na proporção da v26; a B gasta tudo em tomografia. Para outra proporção, mude os pesos (amarelo): "
     "por exemplo, zero na mama para não aumentar uma fila que o mutirão já atendeu.", 14)
nota(ws, base + len(ind) + 2,
     "• A fila de cada código é o limite: a v26 já atende a fila inteira da extração de 10/09 e mais 572. Antes de "
     "escolher, conferir no estudo das filas de 02/11 (aba Filas) se há pedido para os exames a mais de cada código.",
     14)
nota(ws, base + len(ind) + 3,
     "• As salas e os tomógrafos são os da aba 1. A sobra que fica depois do arredondamento ainda paga alguns exames: "
     "some-os à mão no código que preferir (ou mude um peso).", 14)
ws.freeze_panes = "C9"

# ================================================================ 6 Premissas de custo
ws = aba(N_PC, [44, 16, 13, 11, 11, 11, 14, 13, 60])
titulo(ws, "Parte 6 — premissas do custo por procedimento (para preencher)",
       "Preencha as células amarelas vazias: as abas de custo se refazem sozinhas. A coluna de referência e o "
       "comentário de cada célula trazem o que a pesquisa de 05/11/2026 encontrou, só para conferir.")
secao(ws, 4, "Gerais")
GER = {}
for r, (k, nm, v, fmt, nt) in enumerate([
        ("meses", "Meses de execução", 8, INT, "v26"),
        ("dias_mes", "Dias úteis por mês", 21, INT, "v26: 168 dias em 8 meses"),
        ("horas_dia", "Horas abertas por dia útil", f"={ref(N_SALAS, 'B4')}", INT, "aba 1"),
        ("semanas", "Semanas por mês", 4.33, DEC2, "52 semanas ÷ 12 meses"),
        ("encargos", "Encargos sociais e trabalhistas sobre o salário (CLT)", 0.70, PCT,
         "premissa — a confirmar: INSS patronal, FGTS, RAT, terceiros, 13º, férias e provisões; o estudo de 20/10 usou "
         "1,7. Se o ISHP tiver CEBAS (isenção da cota patronal), cai para cerca de 40%"),
        ("beneficios", "Benefícios por empregado CLT por mês (vale-transporte e alimentação) (R$)", 600.00, MOEDA,
         "premissa — a confirmar"),
        ("tributos", "Tributos sobre o valor recebido", 0.0, PCT,
         "premissa: entidade sem fins lucrativos; o médico PJ já tem o imposto dele no preço"),
        ("polos", "Polos", 6, INT, "v26"),
        ("aux_salas", "Salas que um auxiliar de higienização atende", 3, INT, "premissa — a confirmar"),
        ("rec_polo", "Recepcionistas por polo", 2, INT, "v26, 4.15: polo aberto 50 h por semana"),
], 5):
    GER[k] = f"'{N_PC}'!$B${r}"
    put(ws, r, 1, nm, font=F_B, wrap=True)
    if isinstance(v, str):
        link(ws, r, 2, v, fmt)
    elif k in ("encargos", "beneficios", "tributos"):
        vazio(ws, r, 2, fmt, f"pesquisa de 05/11: {v:.0%}" if fmt == PCT else f"pesquisa de 05/11: R$ {v:,.2f}")
    else:
        entrada(ws, r, 2, v, fmt)
    put(ws, r, 3, nt, font=F_I, wrap=True)
    ws.merge_cells(start_row=r, start_column=3, end_row=r, end_column=9)
put(ws, 15, 1, "Horas abertas por mês", font=F_B)
put(ws, 15, 2, f"={GER['dias_mes']}*{GER['horas_dia']}", INT, F_B)
GER["horas_mes"] = f"'{N_PC}'!$B$15"
put(ws, 16, 1, "Aproveitamento das horas pagas — ultrassom", font=F_B, wrap=True)
link(ws, 16, 2, f"={SAL['us_horas']}/({SAL['us_salas']}*{ref(N_SALAS, 'B4')}*{ref(N_SALAS, 'B5')})", PCT)
put(ws, 16, 3, "horas de exame ÷ horas abertas das 20 salas (aba 1): o tempo pago e parado entra no custo de cada exame",
    font=F_I, wrap=True)
ws.merge_cells("C16:I16")
put(ws, 17, 1, "Aproveitamento das horas pagas — tomografia", font=F_B, wrap=True)
link(ws, 17, 2, f"={SAL['tc_horas']}/({SAL['tc_tomo']}*{ref(N_SALAS, 'B4')}*{ref(N_SALAS, 'B5')})", PCT)
put(ws, 17, 3, "horas de exame ÷ horas abertas dos tomógrafos (aba 1)", font=F_I, wrap=True)
ws.merge_cells("C17:I17")
GER["apr_us"], GER["apr_tc"] = f"'{N_PC}'!$B$16", f"'{N_PC}'!$B$17"
put(ws, 18, 1, "Exames da v26 (para ratear o que é por polo)", font=F_B, wrap=True)
link(ws, 18, 2, f"='{N_DEM}'!$D${RT}", INT)
GER["exames"] = f"'{N_PC}'!$B$18"

secao(ws, 20, "Pessoal")
cabecalho(ws, 21, ["Função", "Vínculo", "Salário ou valor (R$)", "Adicional (% do salário)", "Jornada semanal (h)",
                   "Horas por mês", "Custo por mês (R$)", "Custo por hora (R$)", "Referência (pesquisa de 05/11)"])
PES = {}
pessoal = [
    ("med_us_exame", "Médico de ultrassom — por exame", "PJ por exame", 33.33, None, None,
     "modelo do ISHP: R$ 1.000 por lote de 30 exames (estudo de custo de 20/10/2026)"),
    ("med_us_hora", "Médico de ultrassom — por hora", "PJ por hora", 174.30, None, None,
     "IgesDF, seleção de ultrassonografista: R$ 18.115,68 por 24 h semanais ÷ 104 h = R$ 174,30 por hora "
     "(soubrasilia.com, out/2026)"),
    ("rad_laudo", "Radiologista — por laudo de tomografia", "PJ por exame", 35.00, None, None,
     "premissa — a confirmar com cotação de telelaudo ou dos radiologistas"),
    ("rad_hora", "Radiologista — por hora presencial", "PJ por hora", 174.30, None, None,
     "premissa: a mesma hora do ultrassonografista do IgesDF"),
    ("tec_rad", "Técnico em radiologia", "CLT", 2795.00, 0.40, 24,
     "salário: CAGED DF via salario.com.br (425 vínculos, 24 h semanais); adicional de 40%: Lei 7.394/1985, art. 16; "
     "jornada de 24 h: Lei 7.394/1985, art. 14"),
    ("tec_enf", "Técnico de enfermagem", "CLT", 3124.00, 0.10, 44,
     "salário: mediana do CAGED no DF, mar/2026 (numerando.com.br); insalubridade como % do salário: premissa"),
    ("recep", "Recepcionista", "CLT", 1750.00, 0.0, 44,
     "estudo de custo de 20/10/2026: R$ 2.959 de custo por mês (salario.com.br, Brasília, × 1,7)"),
    ("assist", "Assistente de sala (auxiliar do exame)", "CLT", 1900.00, 0.20, 44,
     "premissa — a confirmar: quem acompanha o exame, troca o lençol e limpa o transdutor"),
    ("higien", "Auxiliar de higienização", "CLT", 1650.00, 0.20, 44, "premissa — a confirmar"),
    ("rt", "Responsável técnico médico do polo (por mês)", "PJ por mês", 5000.00, None, None,
     "premissa — a confirmar (v26, 4.15: um por polo, pago pelo valor do exame)"),
    ("retag", "Médico de retaguarda (por dia útil, por polo)", "PJ por dia", 500.00, None, None,
     "premissa — a confirmar (v26, 4.15 e R-09: um por dia útil em cada polo)"),
]
for i, (k, nm, vin, v, adic, jor, fonte) in enumerate(pessoal):
    r = 22 + i
    PES[k] = r
    put(ws, r, 1, nm, font=F_B, wrap=True)
    put(ws, r, 2, vin)
    vazio(ws, r, 3, MOEDA, f"pesquisa de 05/11: R$ {v:,.2f}")
    if vin == "CLT":
        if k == "tec_rad":
            entrada(ws, r, 4, adic, PCT, "40%: Lei 7.394/1985, art. 16")
        else:
            vazio(ws, r, 4, PCT, f"pesquisa de 05/11: {adic:.0%}")
        entrada(ws, r, 5, jor, INT)
        put(ws, r, 6, f"=E{r}*{GER['semanas']}", DEC1)
        put(ws, r, 7, f"=C{r}*(1+D{r})*(1+{GER['encargos']})+{GER['beneficios']}", MOEDA)
        put(ws, r, 8, f"=G{r}/F{r}", MOEDA)
    else:
        for c in (4, 5, 6, 7, 8):
            put(ws, r, c, "—")
    put(ws, r, 9, fonte, font=F_I, wrap=True)
    ws.row_dimensions[r].height = 30
pc = lambda k, col="H": f"'{N_PC}'!${col}${PES[k]}"

r = 22 + len(pessoal) + 1
put(ws, r, 1, "Como pagar o médico do ultrassom", font=F_B)
entrada(ws, r, 2, "por hora", None, "Escreva 'por exame' ou 'por hora'. Por hora: decisão do usuário, 05/11/2026.")
put(ws, r, 3, "escreva por exame ou por hora", font=F_I, borda=False)
MODO_US = f"'{N_PC}'!$B${r}"
r += 1
put(ws, r, 1, "Como pagar o radiologista da tomografia", font=F_B)
entrada(ws, r, 2, "por exame", None, "Escreva 'por exame' (laudo) ou 'por hora' (presencial, supervisiona e lauda).")
put(ws, r, 3, "escreva por exame ou por hora", font=F_I, borda=False)
MODO_TC = f"'{N_PC}'!$B${r}"

r += 2
secao(ws, r, "Estrutura")
r += 1
cabecalho(ws, r, ["Item", "Unidade", "Valor (R$)", "", "", "", "", "", "Referência (pesquisa de 05/11)"])
EST = {}
estrutura = [
    ("sala_us", "Aluguel de uma sala de ultrassom", "por sala por mês", 3000.00,
     "rede do ISHP: R$ 6.000 por polo com 2 salas, recepção e guichê (estudo de 20/10/2026)"),
    ("aparelho_us", "Aparelho de ultrassom com doppler (aluguel com manutenção)", "por sala por mês", 2500.00,
     "rede do ISHP: opção mapeada em Samambaia (estudo de 20/10/2026)"),
    ("fixos_sala", "Outros custos fixos da sala (internet, água, telefone, limpeza)", "por sala por mês", 400.00,
     "premissa — a confirmar se já vêm no aluguel"),
    ("energia_us", "Energia da sala de ultrassom (aparelho, luz, ar-condicionado)", "por hora de exame", 1.50,
     "premissa: cerca de 1,7 kW × R$ 0,90 por kWh"),
    ("tomo", "Tomógrafo e sala de tomografia (aluguel)", "por tomógrafo por mês", 30000.00,
     "anúncio de locação de tomógrafo Canon de 16 canais, R$ 30.000 (mfrural.com.br; não diz se é mensal) — premissa"),
    ("manut_tomo", "Manutenção do tomógrafo (se o aluguel não incluir)", "por tomógrafo por mês", 0.00,
     "zero: a conta supõe aluguel com manutenção. Se não incluir, referência: Prefeitura de Belo Horizonte, Philips "
     "Brilliance 16, manutenção com peças, 2018: R$ 24.418,93 por mês"),
    ("energia_tc", "Energia do tomógrafo e da sala", "por hora de exame", 15.00,
     "premissa: cerca de 17 kW médios × R$ 0,90 por kWh"),
    ("fisica", "Física médica, dosimetria e testes de constância", "por tomógrafo por mês", 1500.00,
     "premissa — a confirmar (v26, 4.16: RDC Anvisa 611/2022 e IN 93/2021)"),
    ("pacs", "Sistema de imagem (RIS/PACS) e armazenamento", "por exame", 2.00, "premissa — a confirmar"),
    ("clinica_tc", "Referência: preço médio da tomografia na clínica parceira", "por exame", 171.44,
     "estudo de custo de 20/10/2026: média das clínicas da rede (R$ 165 a R$ 175)"),
]
for i, (k, nm, un, v, fonte) in enumerate(estrutura):
    rr = r + 1 + i
    EST[k] = f"'{N_PC}'!$C${rr}"
    put(ws, rr, 1, nm, font=F_B, wrap=True)
    put(ws, rr, 2, un, wrap=True)
    vazio(ws, rr, 3, MOEDA, f"pesquisa de 05/11: R$ {v:,.2f}")
    put(ws, rr, 9, fonte, font=F_I, wrap=True)
    ws.row_dimensions[rr].height = 30
r = r + 1 + len(estrutura) + 1
secao(ws, r, "Insumos")
r += 1
cabecalho(ws, r, ["Insumo", "Embalagem", "Preço da embalagem (R$)", "Unidades na embalagem", "Unidade de consumo",
                  "Preço por unidade (R$)", "", "", "Referência (pesquisa de 05/11)"])
INS = {}
insumos = [
    ("gel", "Gel para ultrassom", "galão de 5 kg", 41.82, 5000, "g",
     "Gel condutor Mercur 5 kg, Pague Menos, via cliquefarma.com.br"),
    ("lencol", "Lençol de papel 70 cm × 50 m", "rolo", 25.29, 50, "m", "Kinsan 70 cm × 50 m, Pague Menos"),
    ("toalha", "Papel toalha interfolhado (o paciente limpa o gel)", "pacote de 1.000 folhas", 22.00, 1000, "folha",
     "premissa — a cotar"),
    ("capa", "Capa do transdutor endocavitário (sem lubrificante)", "caixa de 144", 139.90, 144, "unidade",
     "Protetor de sonda para ultrassom, caixa com 144, Droga Raia"),
    ("luva", "Luva de procedimento", "caixa de 100 luvas", 30.00, 50, "par", "premissa — a cotar"),
    ("lenco", "Lenço desinfetante para o transdutor", "pote de 100", 45.00, 100, "unidade", "premissa — a cotar"),
    ("dan", "Desinfecção de alto nível do transdutor endocavitário", "ciclo", 3.00, 1, "ciclo",
     "premissa — a cotar (produto ou equipamento de desinfecção)"),
    ("avental", "Avental descartável do paciente", "pacote de 10", 15.00, 10, "unidade", "premissa — a cotar"),
    ("alcool_gel", "Álcool em gel para as mãos", "frasco de 500 mL", 15.00, 500, "mL", "premissa — a cotar"),
    ("laudo", "Impressão do laudo (folha A4 e toner)", "folha", 0.25, 1, "folha",
     "premissa; o laudo vai ao TrakCare, a folha é a via do usuário"),
    ("contraste", "Contraste iodado não iônico 300 mgI/mL", "frasco de 100 mL", 110.00, 100, "mL",
     "premissa — a cotar. Referência: Sergipe, CTR 125/2025, ioexol 300 de 50 mL a R$ 121,89 (compra emergencial); a "
     "v22 do plano previa R$ 60 de contraste por exame"),
    ("seringa_inj", "Seringa da bomba injetora (200 mL)", "unidade", 45.00, 1, "unidade", "premissa — a cotar"),
    ("extensor", "Extensor (linha do paciente) da bomba injetora", "unidade", 8.00, 1, "unidade", "premissa — a cotar"),
    ("cateter", "Cateter intravenoso periférico 20G", "unidade", 1.50, 1, "unidade", "premissa — a cotar"),
    ("soro", "Soro fisiológico 0,9% 100 mL (empurra o contraste)", "unidade", 3.50, 1, "unidade", "premissa — a cotar"),
    ("seringa10", "Seringa de 10 mL", "unidade", 0.60, 1, "unidade", "premissa — a cotar"),
    ("swab", "Algodão e álcool 70% para a punção", "uso", 0.30, 1, "uso", "premissa — a cotar"),
    ("curativo", "Curativo adesivo pós-punção", "unidade", 0.25, 1, "unidade", "premissa — a cotar"),
    ("kit_emerg", "Kit de reação ao contraste (adrenalina, anti-histamínico, corticoide), amortizado", "por exame com "
     "contraste", 1.00, 1, "exame", "premissa — a confirmar (v26, 4.8: meios de atendimento à reação no polo)"),
]
for i, (k, nm, emb, preco, n, un, fonte) in enumerate(insumos):
    rr = r + 1 + i
    INS[k] = f"'{N_PC}'!$F${rr}"
    put(ws, rr, 1, nm, font=F_B, wrap=True)
    put(ws, rr, 2, emb, wrap=True)
    vazio(ws, rr, 3, MOEDA, f"pesquisa de 05/11: R$ {preco:,.2f} ({emb})")
    entrada(ws, rr, 4, n, INT, "unidades da embalagem da coluna B; mude se a embalagem cotada for outra")
    put(ws, rr, 5, un)
    put(ws, rr, 6, f"=IFERROR(C{rr}/D{rr},0)", DEC4)
    put(ws, rr, 9, fonte, font=F_I, wrap=True)
    ws.row_dimensions[rr].height = 30
contador(ws, 3, [N_PC])
ws.freeze_panes = "B4"


# ================================================================ abas de custo
FIXOS = {"t_recep", "f_assist", "tecnicos"}  # decisões de estrutura, não valores: ficam preenchidas
TOPO_FILA = [("Código", lambda k: f"='{N_DEM}'!A{DEM[k]}", None),
             ("Exames na v26", lambda k: f"='{N_DEM}'!D{DEM[k]}", INT),
             ("Preço da v26 (R$)", lambda k: f"='{N_TEM}'!L{TEM[k]}", MOEDA),
             ("Preço Candanga (R$)", lambda k: f"='{N_TEM}'!M{TEM[k]}", MOEDA)]


def aba_custo(nome, mod, chaves, consumo, linhas_custo, titulo_, sub, nomes=None, topo=TOPO_FILA, tempo=None):
    """tempo: None liga o tempo de sala à aba 4; um dict {chave: sugestão} deixa o tempo em branco para preencher."""
    ws = aba(nome, [46] + [14] * len(chaves) + [44])
    titulo(ws, titulo_, sub)
    nc = len(chaves)
    nomes = nomes or [next(n for kk, _, n, _ in FILAS if kk == k) for k in chaves]
    cabecalho(ws, 4, ["Item"] + nomes + ["Como se calcula"])
    ws.row_dimensions[4].height = 60
    R = {}
    r = 5
    for lab, f, fmt in topo:
        put(ws, r, 1, lab, font=F_B)
        for j, k in enumerate(chaves):
            link(ws, r, 2 + j, f(k), fmt)
        R[lab] = r
        r += 1
    r += 1
    secao(ws, r, "Tempo e consumo por exame (amarelo vazio: preencha; cinza: o exame não usa)")
    r += 1
    put(ws, r, 1, "Tempo de sala (min)", font=F_B)
    for j, k in enumerate(chaves):
        if tempo is None:
            link(ws, r, 2 + j, f"='{N_TEM}'!H{TEM[k]}", DEC1)
        else:
            vazio(ws, r, 2 + j, DEC1, f"sugestão de 05/11: {tempo[k]:g} min (aba 4)")
    put(ws, r, 2 + nc, "aba 4, tempo adotado" if tempo is None else "tempo da sala ocupada por um paciente",
        font=F_I)
    R["tempo"] = r
    for key, lab, vals, fmt, how in consumo:
        r += 1
        put(ws, r, 1, lab, font=F_B, wrap=True)
        for j, k in enumerate(chaves):
            v = vals[k] if isinstance(vals, dict) else vals
            if key in FIXOS:
                entrada(ws, r, 2 + j, v, fmt)
            elif v == 0:
                nao_usa(ws, r, 2 + j, fmt)
            else:
                vazio(ws, r, 2 + j, fmt, f"sugestão de 05/11: {v:g}")
        put(ws, r, 2 + nc, how, font=F_I, wrap=True)
        R[key] = r
    r += 2
    secao(ws, r, "Custo por exame (R$)")
    grupos = {}
    for grupo, itens in linhas_custo:
        r += 1
        put(ws, r, 1, grupo, font=F_S, borda=False)
        ini = r + 1
        for lab, fn, how in itens:
            r += 1
            put(ws, r, 1, lab, wrap=True)
            R["item:" + lab] = r
            for j, k in enumerate(chaves):
                c = L(2 + j)
                put(ws, r, 2 + j, fn(c, R), MOEDA)
            put(ws, r, 2 + nc, how, font=F_I, wrap=True)
        r += 1
        put(ws, r, 1, "Subtotal — " + grupo.lower(), font=F_B, fill=TOT)
        for j in range(nc):
            c = L(2 + j)
            put(ws, r, 2 + j, f"=SUM({c}{ini}:{c}{r - 1})", MOEDA, F_B, TOT)
        grupos[grupo] = r
        R["sub:" + grupo] = r
    r += 2
    put(ws, r, 1, "Custo do exame, antes dos tributos", font=F_B, fill=CAB)
    for j in range(nc):
        c = L(2 + j)
        put(ws, r, 2 + j, "=" + "+".join(f"{c}{g}" for g in grupos.values()), MOEDA, F_B, CAB)
    R["custo0"] = r
    r += 1
    put(ws, r, 1, "Tributos sobre o valor recebido (preço da v26)")
    for j in range(nc):
        c = L(2 + j)
        put(ws, r, 2 + j, f"={c}{R['Preço da v26 (R$)']}*{GER['tributos']}", MOEDA)
    r += 1
    put(ws, r, 1, "Custo total do exame", font=F_B, fill=CAB)
    for j in range(nc):
        c = L(2 + j)
        put(ws, r, 2 + j, f"={c}{R['custo0']}+{c}{r - 1}", MOEDA, F_B, CAB)
    R["custo"] = r
    for lab, pr in [("v26", "Preço da v26 (R$)"), ("Candanga", "Preço Candanga (R$)")]:
        r += 1
        put(ws, r, 1, f"Margem no preço {lab} (R$)", font=F_B)
        for j in range(nc):
            c = L(2 + j)
            put(ws, r, 2 + j, f"={c}{R[pr]}-{c}{R['custo']}", MOEDA, F_B)
        r += 1
        put(ws, r, 1, f"Custo ÷ preço {lab}")
        for j in range(nc):
            c = L(2 + j)
            put(ws, r, 2 + j, f"={c}{R['custo']}/{c}{R[pr]}", PCT)
    r += 2
    secao(ws, r, "No período (exames da v26)")
    for lab, f in [("Custo total (R$)", lambda c: f"={c}{R['custo']}*{c}{R['Exames na v26']}"),
                   ("Recebido no preço da v26 (R$)", lambda c: f"={c}{R['Preço da v26 (R$)']}*{c}{R['Exames na v26']}"),
                   ("Recebido no preço Candanga (R$)",
                    lambda c: f"={c}{R['Preço Candanga (R$)']}*{c}{R['Exames na v26']}")]:
        r += 1
        put(ws, r, 1, lab, font=F_B)
        for j in range(nc):
            put(ws, r, 2 + j, f(L(2 + j)), MOEDA)
        put(ws, r, 2 + nc, f"=SUM(B{r}:{L(1 + nc)}{r})", MOEDA, F_B, TOT)
        R[lab] = r
    put(ws, R["Custo total (R$)"] - 1, 2 + nc, "Total", font=F_B, fill=TOT)
    ws.freeze_panes = "B5"
    return ws, R


hora = lambda custo_h, apr: f"{custo_h}/60/{apr}"  # custo de um minuto de sala, com o tempo parado
rateio_polo = (f"({pc('rt', 'C')}*{GER['polos']}*{GER['meses']}"
               f"+{pc('retag', 'C')}*{GER['polos']}*{GER['dias_mes']}*{GER['meses']})/{GER['exames']}")

rateio_recep = f"{GER['rec_polo']}*{GER['polos']}*{pc('recep', 'G')}*{GER['meses']}/{GER['exames']}"

US_K = [k for k, _, _, m in FILAS if m == "US"]
TC_K = [k for k, _, _, m in FILAS if m == "TC"]
consumo_us = [
    ("t_recep", "Tempo de recepção por exame (min)", 5, DEC1,
     "identificação, documentos e preparo (v26, 4.7); só informa: o custo da recepção é o quadro pago, abaixo"),
    ("f_assist", "Presença do assistente de sala (% do tempo de sala)", 1.0, PCT,
     "100% = um assistente por sala o tempo todo (decisão do usuário, 05/11/2026); 50% = um para duas salas"),
    ("gel", "Gel (g)", {"mama": 25, "dop_mmii": 40, "carotidas": 15, "abd_total": 25, "parede": 15, "transvag": 5,
                        "urinario": 20, "tireoide": 10, "prostata": 15, "abd_sup": 20}, INT, "premissa — a confirmar"),
    ("lencol", "Lençol de papel (m)", 1.0, DEC1, "um pedaço de maca por paciente"),
    ("toalha", "Papel toalha (folhas)", {k: (2 if k == "transvag" else 4) for k in US_K}, INT, "o paciente limpa o gel"),
    ("capa", "Capa do transdutor endocavitário (unidades)", {k: (1 if k == "transvag" else 0) for k in US_K}, INT,
     "só a transvaginal"),
    ("luva", "Luvas (pares)", {k: (2 if k == "transvag" else 1) for k in US_K}, INT, ""),
    ("lenco", "Lenço desinfetante do transdutor (unidades)", 1, INT, "limpeza entre um paciente e outro"),
    ("dan", "Desinfecção de alto nível (ciclos)", {k: (1 if k == "transvag" else 0) for k in US_K}, INT,
     "transdutor endocavitário, entre um paciente e outro"),
    ("avental", "Avental descartável (unidades)", {k: (1 if k in ("transvag", "mama") else 0) for k in US_K}, INT, ""),
    ("alcool_gel", "Álcool em gel (mL)", 3, INT, "higiene das mãos"),
    ("laudo", "Folhas de laudo impresso", 1, INT, "via do usuário"),
]
mod_med_us = (lambda c, R: f'=IF({MODO_US}="por hora",{c}{R["tempo"]}*{hora(pc("med_us_hora", "C"), GER["apr_us"])},'
                           f'{pc("med_us_exame", "C")})')
custo_us = [
    ("Pessoal", [
        ("Médico de ultrassom (executa e lauda)", mod_med_us,
         "por exame: valor por exame; por hora: tempo de sala × hora do médico ÷ aproveitamento (aba 6 Premissas)"),
        ("Recepcionista", lambda c, R: "=" + rateio_recep,
         "recepcionistas por polo × polos × custo por mês × meses ÷ todos os exames da v26 (o que se paga de fato)"),
        ("Assistente de sala", lambda c, R: f"={c}{R['tempo']}*{c}{R['f_assist']}*{hora(pc('assist'), GER['apr_us'])}",
         "tempo de sala × presença × custo por hora ÷ aproveitamento"),
        ("Auxiliar de higienização", lambda c, R: f"={c}{R['tempo']}*{hora(pc('higien'), GER['apr_us'])}/{GER['aux_salas']}",
         "tempo de sala × custo por hora ÷ salas por auxiliar ÷ aproveitamento"),
        ("Responsável técnico e médico de retaguarda (rateio)", lambda c, R: "=" + rateio_polo,
         "(RT por mês × polos × meses + retaguarda por dia × polos × dias) ÷ todos os exames da v26"),
    ]),
    ("Estrutura", [
        ("Sala (aluguel)", lambda c, R: f"={c}{R['tempo']}*{hora(EST['sala_us'] + '/' + GER['horas_mes'], GER['apr_us'])}",
         "aluguel por mês ÷ horas abertas por mês × tempo de sala ÷ aproveitamento"),
        ("Aparelho de ultrassom", lambda c, R: f"={c}{R['tempo']}*{hora(EST['aparelho_us'] + '/' + GER['horas_mes'], GER['apr_us'])}",
         "idem"),
        ("Outros custos fixos da sala", lambda c, R: f"={c}{R['tempo']}*{hora(EST['fixos_sala'] + '/' + GER['horas_mes'], GER['apr_us'])}",
         "idem"),
        ("Energia", lambda c, R: f"={c}{R['tempo']}/60*{EST['energia_us']}", "tempo de sala × energia por hora"),
        ("Sistema de imagem (RIS/PACS)", lambda c, R: f"={EST['pacs']}", "por exame"),
    ]),
    ("Insumos", [
        ("Gel", lambda c, R: f"={c}{R['gel']}*{INS['gel']}", "consumo × preço por unidade"),
        ("Lençol de papel", lambda c, R: f"={c}{R['lencol']}*{INS['lencol']}", ""),
        ("Papel toalha", lambda c, R: f"={c}{R['toalha']}*{INS['toalha']}", ""),
        ("Capa do transdutor", lambda c, R: f"={c}{R['capa']}*{INS['capa']}", ""),
        ("Luvas", lambda c, R: f"={c}{R['luva']}*{INS['luva']}", ""),
        ("Lenço desinfetante", lambda c, R: f"={c}{R['lenco']}*{INS['lenco']}", ""),
        ("Desinfecção de alto nível", lambda c, R: f"={c}{R['dan']}*{INS['dan']}", ""),
        ("Avental descartável", lambda c, R: f"={c}{R['avental']}*{INS['avental']}", ""),
        ("Álcool em gel", lambda c, R: f"={c}{R['alcool_gel']}*{INS['alcool_gel']}", ""),
        ("Impressão do laudo", lambda c, R: f"={c}{R['laudo']}*{INS['laudo']}", ""),
    ]),
]
wsU, RU = aba_custo(N_CUS, "US", US_K, consumo_us, custo_us,
                    "Parte 6 — custo de cada exame de ultrassom, item a item",
                    "Execução própria nos polos: sala e aparelho alugados, médico, recepção, assistente e higienização. "
                    "O tempo parado das salas entra no custo pelo aproveitamento (aba 6 Premissas). A gestão do convênio "
                    "fica fora (é paga pelo apoio).")

com = {k: (0 if k == "tc_torax_s" else 1) for k in TC_K}
consumo_tc = [
    ("t_recep", "Tempo de recepção por exame (min)", 5, DEC1, "identificação, documentos, termo de consentimento"),
    ("t_enf", "Tempo de enfermagem por exame (min)", {k: 10 * com[k] for k in TC_K}, DEC1,
     "triagem pré-contraste, acesso venoso e injeção (v26, 4.8)"),
    ("tecnicos", "Técnicos na sala durante o exame", 1, INT, "v26: 3 técnicos por tomógrafo para cobrir 50 h semanais"),
    ("contraste", "Contraste iodado (mL)", {"tc_abd": 90, "tc_pelve": 90, "tc_torax_c": 70, "coronarias": 80,
                                           "tc_torax_s": 0}, INT, "premissa — a confirmar com o protocolo do radiologista"),
    ("seringa_inj", "Seringa da bomba injetora (unidades)", com, INT, ""),
    ("extensor", "Extensor da bomba (unidades)", com, INT, ""),
    ("cateter", "Cateter intravenoso (unidades)", com, INT, ""),
    ("soro", "Soro fisiológico 100 mL (unidades)", com, INT, ""),
    ("seringa10", "Seringa de 10 mL (unidades)", com, INT, "teste de permeabilidade da veia"),
    ("swab", "Algodão e álcool (usos)", com, INT, ""),
    ("curativo", "Curativo pós-punção (unidades)", com, INT, ""),
    ("kit_emerg", "Kit de reação ao contraste (exames)", com, INT, ""),
    ("luva", "Luvas (pares)", {k: 1 + com[k] for k in TC_K}, INT, ""),
    ("lencol", "Lençol de papel (m)", 1.8, DEC1, "a mesa do tomógrafo é mais longa"),
    ("avental", "Avental descartável (unidades)", 1, INT, ""),
    ("alcool_gel", "Álcool em gel (mL)", 3, INT, ""),
    ("laudo", "Folhas de laudo impresso", 1, INT, ""),
]
mod_rad = (lambda c, R: f'=IF({MODO_TC}="por hora",{c}{R["tempo"]}*{hora(pc("rad_hora", "C"), GER["apr_tc"])},'
                        f'{pc("rad_laudo", "C")})')
mensal_tc = f"({EST['tomo']}+{EST['manut_tomo']}+{EST['fisica']}+{EST['fixos_sala']})"
custo_tc = [
    ("Pessoal", [
        ("Técnico em radiologia", lambda c, R: f"={c}{R['tempo']}*{c}{R['tecnicos']}*{hora(pc('tec_rad'), GER['apr_tc'])}",
         "tempo de sala × técnicos × custo por hora ÷ aproveitamento"),
        ("Enfermagem (contraste)", lambda c, R: f"={c}{R['t_enf']}*{hora(pc('tec_enf'), GER['apr_tc'])}",
         "tempo de enfermagem × custo por hora ÷ aproveitamento"),
        ("Radiologista (laudo e supervisão)", mod_rad, "por exame: valor do laudo; por hora: tempo de sala × hora ÷ "
                                                       "aproveitamento"),
        ("Recepcionista", lambda c, R: "=" + rateio_recep, "o mesmo do ultrassom"),
        ("Auxiliar de higienização", lambda c, R: f"={c}{R['tempo']}*{hora(pc('higien'), GER['apr_tc'])}/{GER['aux_salas']}",
         ""),
        ("Responsável técnico e médico de retaguarda (rateio)", lambda c, R: "=" + rateio_polo, "o mesmo do ultrassom"),
    ]),
    ("Estrutura", [
        ("Tomógrafo, sala, manutenção, física médica e fixos",
         lambda c, R: f"={c}{R['tempo']}*{hora(mensal_tc + '/' + GER['horas_mes'], GER['apr_tc'])}",
         "custos por mês ÷ horas abertas por mês × tempo de sala ÷ aproveitamento"),
        ("Energia", lambda c, R: f"={c}{R['tempo']}/60*{EST['energia_tc']}", ""),
        ("Sistema de imagem (RIS/PACS)", lambda c, R: f"={EST['pacs']}", ""),
    ]),
    ("Insumos", [(nm, (lambda key: (lambda c, R: f"={c}{R[key]}*{INS[key]}"))(key), "")
                 for key, nm in [("contraste", "Contraste iodado"), ("seringa_inj", "Seringa da bomba injetora"),
                                 ("extensor", "Extensor"), ("cateter", "Cateter intravenoso"),
                                 ("soro", "Soro fisiológico"), ("seringa10", "Seringa de 10 mL"),
                                 ("swab", "Algodão e álcool"), ("curativo", "Curativo"),
                                 ("kit_emerg", "Kit de reação ao contraste"), ("luva", "Luvas"),
                                 ("lencol", "Lençol de papel"), ("avental", "Avental descartável"),
                                 ("alcool_gel", "Álcool em gel"), ("laudo", "Impressão do laudo")]]),
]
wsT, RTC = aba_custo(N_CTC, "TC", TC_K, consumo_tc, custo_tc,
                     "Parte 6 — custo de cada exame de tomografia, item a item",
                     "Execução própria com tomógrafo alugado, para comparar com o preço da clínica parceira. O tempo "
                     "parado dos 6 tomógrafos (carga de pouco mais de 3) entra pelo aproveitamento e pesa muito.")
contador(wsU, 3, [N_CUS, N_PC])
contador(wsT, 3, [N_CTC, N_PC])
r = RTC["Recebido no preço Candanga (R$)"] + 2
put(wsT, r, 1, "Referência: preço da clínica parceira (R$)", font=F_B)
for j in range(len(TC_K)):
    link(wsT, r, 2 + j, f"={EST['clinica_tc']}", MOEDA)
put(wsT, r, 2 + len(TC_K), "estudo de custo de 20/10/2026; a clínica traz tomógrafo, equipe e laudo", font=F_I,
    wrap=True)
put(wsT, r + 1, 1, "Custo próprio − preço da clínica (R$)", font=F_B)
for j in range(len(TC_K)):
    c = L(2 + j)
    put(wsT, r + 1, 2 + j, f"={c}{RTC['custo']}-{c}{r}", MOEDA, F_B)

# ---------------------------------------------------------------- só tomografia: com contraste e sem contraste
# pedido do usuário (05/11/2026): uma aba com duas contas, a TC com contraste e a TC sem contraste, em branco para
# preencher; os preços dos insumos e do pessoal vêm das premissas, e o resto é igual à aba por procedimento
GRUPO_TC = {"com": ["tc_abd", "tc_pelve", "tc_torax_c", "coronarias"], "sem": ["tc_torax_s"]}
BASE_TC = {"com": "tc_abd", "sem": "tc_torax_s"}  # de onde vem a sugestão de consumo


def media_tc(k, col):
    soma = "+".join(f"'{N_DEM}'!$D${DEM[f]}*'{N_TEM}'!${col}${TEM[f]}" for f in GRUPO_TC[k])
    return f"=({soma})/({'+'.join(f'{chr(39)}{N_DEM}{chr(39)}!$D${DEM[f]}' for f in GRUPO_TC[k])})"


topo_cs = [("Código", lambda k: " · ".join(sorted({c for kk, c, _, _ in FILAS if kk in GRUPO_TC[k]})), None),
           ("Exames na v26", lambda k: "=" + "+".join(f"'{N_DEM}'!$D${DEM[f]}" for f in GRUPO_TC[k]), INT),
           ("Preço da v26 (R$)", lambda k: media_tc(k, "L"), MOEDA),
           ("Preço Candanga (R$)", lambda k: media_tc(k, "M"), MOEDA)]
consumo_cs = [(key, lab, ({k: vals[b] for k, b in BASE_TC.items()} if isinstance(vals, dict) else vals), fmt, how)
              for key, lab, vals, fmt, how in consumo_tc]
wsC, RCS = aba_custo(N_CCS, "TC", ["com", "sem"], consumo_cs, custo_tc,
                     "Parte 6 — tomografia: custo do exame com contraste e sem contraste",
                     "Duas contas só de tomografia. Com contraste: TC de abdômen superior, de pelve, de tórax com "
                     "contraste e angio coronária da v26; sem contraste: TC de tórax sem contraste. Preencha o amarelo "
                     "vazio desta aba e das premissas; o preço de cada insumo e do pessoal vem das premissas.",
                     nomes=["TC com contraste", "TC sem contraste"], topo=topo_cs,
                     tempo={"com": 20, "sem": 15})
contador(wsC, 3, [N_CCS, N_PC])
r = RCS["Recebido no preço Candanga (R$)"] + 2
put(wsC, r, 1, "Referência: preço da clínica parceira (R$)", font=F_B)
for j in range(2):
    link(wsC, r, 2 + j, f"={EST['clinica_tc']}", MOEDA)
put(wsC, r, 4, "estudo de custo de 20/10/2026; a clínica traz tomógrafo, equipe e laudo", font=F_I, wrap=True)
put(wsC, r + 1, 1, "Custo próprio − preço da clínica (R$)", font=F_B)
for j in range(2):
    c = L(2 + j)
    put(wsC, r + 1, 2 + j, f"={c}{RCS['custo']}-{c}{r}", MOEDA, F_B)
r += 3
secao(wsC, r, "Tomografia inteira (média ponderada pelos exames da v26)")
ex = f"B{RCS['Exames na v26']}:C{RCS['Exames na v26']}"
for i, (lab, row) in enumerate([("Custo por exame (R$)", RCS["custo"]), ("Preço da v26 (R$)", RCS["Preço da v26 (R$)"]),
                                 ("Preço Candanga (R$)", RCS["Preço Candanga (R$)"])]):
    put(wsC, r + 1 + i, 1, lab, font=F_B)
    put(wsC, r + 1 + i, 2, f"=SUMPRODUCT({ex},B{row}:C{row})/SUM({ex})", MOEDA, F_B)
wsC.column_dimensions["B"].width = wsC.column_dimensions["C"].width = 18

# ---------------------------------------------------------------- cenários: parte da TC com contraste feita sem
# pedido do usuário (07/11/2026): o radiologista enquadra caso a caso, e parte dos exames pedidos com contraste é feita
# sem contraste. A angiotomografia de coronárias não existe sem contraste e fica de fora da conversão.
ws = aba(N_CEN, [16, 14, 13, 13, 12, 12, 14, 15, 15, 13, 12, 13, 15, 15])
titulo(ws, "Parte 6 — cenários: exames pedidos com contraste e feitos sem contraste",
       "O enquadramento médico, caso a caso, decide se o exame precisa de contraste. Cada linha supõe uma parte dos "
       "exames convertíveis feita com contraste (amarelo: mude os passos). O preço não muda: o código da Tabela SUS "
       "é o mesmo com e sem contraste. Custo, consumo e tempo vêm da aba " + N_CCS + ".")
cc = lambda lin, col="B": f"'{N_CCS}'!${col}${lin}"
put(ws, 4, 1, "Convertíveis", font=F_B)
link(ws, 4, 2, "=" + "+".join(f"'{N_DEM}'!$D${DEM[f]}" for f in ("tc_abd", "tc_pelve", "tc_torax_c")), INT)
put(ws, 4, 3, "TC de abdômen superior, de pelve e de tórax com contraste da v26", font=F_I, borda=False)
put(ws, 5, 1, "Sempre com contraste", font=F_B)
link(ws, 5, 2, f"='{N_DEM}'!$D${DEM['coronarias']}", INT)
put(ws, 5, 3, "angiotomografia de coronárias: sem contraste não há exame", font=F_I, borda=False)
put(ws, 6, 1, "Já sem contraste", font=F_B)
link(ws, 6, 2, f"='{N_DEM}'!$D${DEM['tc_torax_s']}", INT)
put(ws, 6, 3, "TC de tórax sem contraste da v26", font=F_I, borda=False)
put(ws, 7, 1, "Economia por exame convertido (R$)", font=F_B)
put(ws, 7, 2, f"=({cc(RCS['sub:Insumos'])}-{cc(RCS['sub:Insumos'], 'C')})"
              f"+({cc(RCS['item:Enfermagem (contraste)'])}-{cc(RCS['item:Enfermagem (contraste)'], 'C')})", MOEDA, F_B)
put(ws, 7, 3, "insumos e enfermagem do exame com contraste menos os do exame sem (aba " + N_CCS + "); o tomógrafo, "
              "os técnicos e a sala são pagos de qualquer forma", font=F_I, borda=False)
put(ws, 8, 1, "Minutos liberados por exame convertido", font=F_B)
put(ws, 8, 2, f"={cc(RCS['tempo'])}-{cc(RCS['tempo'], 'C')}", DEC1, F_B)
put(ws, 8, 3, "tempo de sala com contraste menos o sem contraste", font=F_I, borda=False)
cabecalho(ws, 10, ["Convertíveis feitos com contraste", "Convertidos para sem contraste", "Exames com contraste",
                   "Exames sem contraste", "% com contraste no total", "Contraste usado (litros)",
                   "Frascos de contraste", "Custo dos exames (R$)", "Economia sobre 100% com contraste (R$)",
                   "Custo médio por exame (R$)", "Horas de tomógrafo", "Uso dos tomógrafos",
                   "Recebido no preço da v26 (R$)", "Margem no preço da v26 (R$)"])
ml = cc(RCS["contraste"])
frasco = INS["contraste"].replace("$F$", "$D$")
for i, pct in enumerate([1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0]):
    r = 11 + i
    entrada(ws, r, 1, pct, '0%', "parte dos convertíveis que o radiologista mantém com contraste")
    put(ws, r, 2, f"=1-A{r}", '0%')
    put(ws, r, 3, f"=$B$5+ROUND($B$4*A{r},0)", INT)
    put(ws, r, 4, f"=$B$6+$B$4-ROUND($B$4*A{r},0)", INT)
    put(ws, r, 5, f"=C{r}/(C{r}+D{r})", '0%')
    put(ws, r, 6, f"=C{r}*{ml}/1000", DEC1)
    put(ws, r, 7, f"=IFERROR(ROUNDUP(C{r}*{ml}/{frasco},0),0)", INT)
    put(ws, r, 8, f"=$C$11*{cc(RCS['custo'])}+$D$11*{cc(RCS['custo'], 'C')}-(D{r}-$D$11)*$B$7", MOEDA)
    put(ws, r, 9, f"=$H$11-H{r}", MOEDA)
    put(ws, r, 10, f"=H{r}/(C{r}+D{r})", MOEDA)
    put(ws, r, 11, f"=(C{r}*{cc(RCS['tempo'])}+D{r}*{cc(RCS['tempo'], 'C')})/60", INT)
    put(ws, r, 12, f"=K{r}/({SAL['tc_tomo']}*{ref(N_SALAS, 'B7')})", '0%')
    put(ws, r, 13, f"={cc(RCS['Recebido no preço da v26 (R$)'], 'D')}", MOEDA)
    put(ws, r, 14, f"=M{r}-H{r}", MOEDA)
nota(ws, 23, "• A linha de 100% é a v26 como está: todo exame pedido com contraste é feito com contraste. Cada linha "
             "abaixo converte mais 10% dos convertíveis. A angio coronária fica sempre com contraste.", 14)
nota(ws, 24, "• O custo cai só no que o exame sem contraste não usa: contraste, seringa da bomba, extensor, cateter, "
             "soro, kit de reação e o tempo de enfermagem. O tomógrafo, os técnicos, a sala e o radiologista (por exame) "
             "seguem iguais; o tempo que sobra aparece nas horas de tomógrafo, como folga para mais exames.", 14)
nota(ws, 25, "• O recebido não muda: a Tabela SUS paga o mesmo código com e sem contraste. A conta só sai com a aba "
             + N_CCS + " e as premissas preenchidas (contraste em mL, preços, tempos).", 14)
ws.freeze_panes = "B11"

# resumo no fim da aba de ultrassom: o ultrassom inteiro
r = RU["Recebido no preço Candanga (R$)"] + 2
secao(wsU, r, "Ultrassom inteiro (média ponderada pelos exames da v26)")
nc = len(US_K)
lst = f"B{RU['Exames na v26']}:{L(1 + nc)}{RU['Exames na v26']}"
for i, (lab, row) in enumerate([("Custo por exame (R$)", RU["custo"]), ("Preço da v26 (R$)", RU["Preço da v26 (R$)"]),
                                 ("Preço Candanga (R$)", RU["Preço Candanga (R$)"])]):
    put(wsU, r + 1 + i, 1, lab, font=F_B)
    put(wsU, r + 1 + i, 2, f"=SUMPRODUCT({lst},B{row}:{L(1 + nc)}{row})/SUM({lst})", MOEDA, F_B)
rm = RU["item:Médico de ultrassom (executa e lauda)"]
put(wsU, r + 4, 1, "Médico por exame, em média (R$)", font=F_B)
put(wsU, r + 4, 2, f"=SUMPRODUCT({lst},B{rm}:{L(1 + nc)}{rm})/SUM({lst})", MOEDA, F_B)
put(wsU, r + 5, 1, "Tempo de sala por exame, em média (min)", font=F_B)
link(wsU, r + 5, 2, f"='{N_TEM}'!$H${TEM_MED_US}", DEC1)
for i, (lab, lin) in enumerate([("v26", r + 2), ("Candanga", r + 3)]):
    rr = r + 6 + i
    put(wsU, rr, 1, f"Hora do médico que empata o custo com o preço {lab} (R$)", font=F_B, wrap=True)
    put(wsU, rr, 2, f"=(B{lin}-(B{r + 1}-B{r + 4}))*60*{GER['apr_us']}/B{r + 5}", MOEDA, F_B, CAB)
put(wsU, r + 6, 3, "com o aproveitamento das salas da aba 6 Premissas: acima disso, o ultrassom pago por hora custa mais "
                   "do que recebe. O modelo por exame (R$ 33,33) equivale a R$ 100 por hora de exame (3 exames por hora).",
    font=F_I, borda=False)

# ================================================================ Fontes
ws = aba("Fontes", [50, 100])
titulo(ws, "Fontes", "Onde cada número foi buscado. As premissas sem fonte estão marcadas nas abas.")
fontes = [
    ("Plano v26 (quantidades, polos, salas, tempos, preço)", "planos/redacao_04/versoes/plano_v26_20261021.md; "
     "calculo_v25/v25.json; calculo_v19/calculo.py (origem por Região de 15/09/2026 e tempos de sala)"),
    ("CBR — tempos de ultrassom", "Recomendação do Colégio Brasileiro de Radiologia sobre o intervalo de tempo mínimo "
     "para o agendamento e o tempo médio dos exames de ultrassonografia, 14/11/2017 (output/cbr_agendamento_"
     "ultrassonografia_20171114.pdf)"),
    ("Tempo de sala da tomografia (contraste × sem)", "Erdfarb et al., RSNA 2005, https://archive.rsna.org/2005/4407929.html "
     "(também Yale, https://elischolar.library.yale.edu/ymtdl/239)"),
    ("Tempo de sala da tomografia por número de técnicos", "Marchione et al., RSNA 2007, "
     "https://archive.rsna.org/2007/5009730.html"),
    ("Duração do exame de tomografia para o paciente", "Rede D'Or, https://www.rededorsaoluiz.com.br/hospital/sao-luiz-"
     "itaim/exames-e-procedimentos/tomografia-computadorizada (5 a 20 minutos)"),
    ("Tabela SUS Candanga", "Anexo Único da Deliberação CG-SES-DF 46/2026, SEI 212117347 (biblioteca/precos/"
     "tabela_sus_candanga/ no main)"),
    ("Preço da v26", "SIGTAP (valor SA) + Portaria SAES/MS 4.282/2026, Anexo I (8.1 da v26)"),
    ("Médico de ultrassom por hora", "IgesDF, seleção de ultrassonografista, R$ 18.115,68 por 24 h semanais: "
     "https://soubrasilia.com/igesdf-selecao-ultrassonografista-salario-18-mil/"),
    ("Médico de ultrassom por exame; aluguel de sala e aparelho; recepcionista; TC na clínica",
     "estudos/custo_por_exame_v2_20261020.xlsx (rede do ISHP, 20/10/2026)"),
    ("Técnico em radiologia", "https://www.salario.com.br/profissao/tecnico-em-radiologia-cbo-324115/df/; "
     "Lei 7.394/1985, arts. 14 e 16"),
    ("Técnico de enfermagem", "https://numerando.com.br/salarios/tecnico-em-enfermagem/distrito-federal"),
    ("Gel para ultrassom", "https://www.cliquefarma.com.br/hospitalar/equipamentos-e-acessorios/equipamentos/gel-"
     "condutor-mercur-5-kg-galao"),
    ("Lençol de papel", "https://www.paguemenos.com.br/lencol-de-papel-em-rolo-kinsan-70cmx50m-unidade-"
     "16qr9845250l0630/p"),
    ("Capa do transdutor", "https://www.drogaraia.com.br/protetor-de-sonda-para-ultrassom-sem-lubrificante-cixa-com-"
     "144-und-1247972.html"),
    ("Contraste iodado (referência)", "Governo de Sergipe, CTR 125/2025: https://saude.se.gov.br/wp-content/uploads/"
     "2026/01/CTR-125.2025-UNIAO-FARMA-IOEXOL.pdf"),
    ("Locação de tomógrafo (referência fraca)", "https://www.mfrural.com.br/busca/canais/categoria/26-maquinas--"
     "equipamentos/estado/rio-de-janeiro (anúncio)"),
    ("Manutenção de tomógrafo", "Prefeitura de Belo Horizonte, HMOB, serviço contínuo 2018-0205: "
     "https://prefeitura.pbh.gov.br/contratos/hmob-servico-continuo-2018-0205"),
]
cabecalho(ws, 4, ["Número", "Fonte"])
for i, (a, b) in enumerate(fontes, 5):
    put(ws, i, 1, a, font=F_B, wrap=True)
    put(ws, i, 2, b, wrap=True)
    ws.row_dimensions[i].height = 30

# ordem das abas
ordem = ["Leia", N_SALAS, N_DEM, N_PRE, N_TEM, N_ADA, N_PC, N_CUS, N_CTC, N_CCS, N_CEN, "Fontes"]
wb._sheets = [wb[n] for n in ordem]
wb.save(SAIDA)
print(SAIDA)
