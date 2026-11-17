"""Readequação do plano 4 à Candanga: dois cenários (09/11/2026, pedido do usuário).

Cenário 1: a v26 como está (as mesmas metas), paga pela Candanga; só os R$ 245 mil que sobram são readequados.
Cenário 2: as filas escolhidas de novo, pela margem de cada exame (o que o convênio paga menos o que custa fazer),
pela complexidade e pela fila que existe (hoje e os pedidos novos dos 12 meses).

Fontes: estudo das filas de 02/11 (estudo_filas_imagem_20261102.json: filas, cobertura L-008, preços da Candanga,
minutos, demanda por código), estudo de 05/11 (a v26 pela Candanga e a sobra), custo v2 de 20/10 e estudo de 02/11
(custos: sala, médico, insumos, TC na clínica), formulário de 09/11 (auxiliar de sala do ultrassom).

Tudo o que é conta é fórmula. As quantidades escolhidas saem deste script (a ordem segue as premissas de hoje); se
mudar uma premissa, rodar de novo. Amarelo com fonte azul: premissa. Verde: vem de outra aba.
Recalcular depois de gerar:
    python3.11 <skill xlsx>/scripts/recalc.py estudo_readequacao_candanga_margem_20261109.xlsx 90
"""
import json
import math
import os

from openpyxl import Workbook
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter as L

AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.environ.get("SAIDA") or os.path.join(AQUI, "estudo_readequacao_candanga_margem_20261109.xlsx")
FILAS = json.load(open(os.path.join(AQUI, "estudo_filas_imagem_20261102.json"), encoding="utf-8"))

# ------------------------------------------------------------------ premissas (valores de partida)
P = {
    "envelope": 10636602.00,   # recurso 11.592.762 − apoio da v26 956.160 (estudo de 05/11, aba 3)
    "v26_candanga": 10390824.04,  # o mesmo mix da v26 pela Candanga (estudo de 05/11, aba 3)
    "medico_modo": os.environ.get("MEDICO_MODO", "hora"),  # "hora" ou "exame"
    "medico_h": 100.0,         # médico do ultrassom por hora (estudo de 02/11, custos)
    "medico_ex": 33.33,        # médico do ultrassom por exame (modelo do ISHP de 20/10: R$ 1.000 por 30 exames)
    "sala_mes": 5500.0,        # sala R$ 3.000 + aparelho R$ 2.500 por mês (custo v2 de 20/10)
    "aux_mes": 2 * 2959.0,     # 2 auxiliares de sala por sala em 10 h (formulário de 09/11); custo de recepcionista
    "horas_exame_mes": 168.0,  # 21 dias × 10 h × 80%
    "insumo": 3.0,             # insumos por exame de ultrassom (custo v2)
    "tc_sem": 175.0,           # TC na clínica, sem contraste (usuário, 09/11)
    "tc_contraste": 50.0,      # a mais por exame com contraste (usuário, 09/11)
    "meses": 12,
    "limiar": 0.15,            # margem mínima para o exame entrar no cenário 2
    "salas": 14,               # salas de ultrassom (estudo de 07/11: 13 a 15)
    "tomografos": 3,
    "horas_dia": 10,
    "uso": 0.8,
    "dias_ano": 252,
}

# ------------------------------------------------------------------ as linhas de exame (adultos, ambulatório)
# (chave, exame, mod., código, preço Candanga, minutos, fila de hoje, chave da demanda, complexidade, por quê)
DEM = {x["codigo"]: x for x in FILAS["revisao"]["demanda"]}
F = {f["nome"]: f for f in FILAS["filas"]}


def fila(*nomes):
    return sum(F[n]["fila"] for n in nomes)


TC_A, TC_P, TC_T = "02.06.03.001-0", "02.06.03.003-7", "02.06.02.003-1"
US_DOP, US_ABT, US_MAMA = "02.05.01.004-0", "02.05.02.004-6", "02.05.02.009-7"
LINHAS = [
    # tomografia: na clínica, por exame
    ("tc_abd_s", "TC de abdômen superior sem contraste", "TC", TC_A, 309.25, 11, 68, None, 1, "sem punção nem repouso"),
    ("tc_pel_s", "TC de pelve sem contraste (sem os CID da OCI do IEV)", "TC", TC_P, 309.25, 11, 56, None, 1,
     "sem punção nem repouso"),
    ("tc_tor_s", "TC de tórax sem contraste", "TC", TC_T, 309.25, 11, 180, None, 1, "sem punção nem repouso"),
    ("tc_cra_s", "TC de crânio sem contraste", "TC", "02.06.01.007-9", 251.29, 11, 44, None, 1,
     "sem punção; fila do código encolhe (a SES agenda mais do que entra)"),
    ("tc_abd_c", "TC de abdômen superior com contraste", "TC", TC_A, 309.25, 20, 4116, TC_A, 3,
     "contraste: punção, repouso, radiologista presente; fila oncológica"),
    ("tc_pel_c", "TC de pelve com contraste (sem os CID da OCI do IEV)", "TC", TC_P, 309.25, 20, 3634, TC_P, 3,
     "contraste; fila oncológica"),
    ("tc_tor_c", "TC de tórax com contraste", "TC", TC_T, 309.25, 20, 2350, TC_T, 3, "contraste; fila oncológica"),
    ("tc_pes_c", "TC de pescoço com contraste", "TC", "02.06.01.005-2", 309.25, 20, 479, None, 3, "contraste"),
    ("tc_cra_c", "TC de crânio com contraste", "TC", "02.06.01.007-9", 251.29, 20, 372, None, 3,
     "contraste; fila do código encolhe"),
    ("tc_fac_c", "TC de face e seios da face com contraste", "TC", "02.06.01.004-4", 260.09, 20, 139, None, 3,
     "contraste; fila pequena e que encolhe"),
    ("tc_ang", "Angiotomografias, sem as coronárias (aorta, carótidas, pescoço, tórax, abdômen, pelve, renais)", "TC",
     "vários", 309.25, 20, 1962, None, 3,
     "contraste com injeção rápida: cateter calibroso e disparo pelo contraste; sem medicação nem controle de "
     "frequência (só a coronária pede)"),
    ("tc_ang_cra", "Angiotomografia do crânio", "TC", "02.06.01.007-9", 251.29, 20, 385, None, 3,
     "contraste com injeção rápida; preço do código do crânio"),
    # ultrassom: feito por nós (sala, aparelho, médico por hora, auxiliar de sala)
    ("us_abs", "US de abdômen superior", "US", "02.05.02.003-8", 101.27, 15, 2213, "02.05.02.003-8", 1,
     "jejum: agenda de manhã"),
    ("us_esc", "US de bolsa escrotal (adulto)", "US", "02.05.02.007-0", 100.00, 15, 700, "02.05.02.007-0", 2,
     "acompanhante"),
    ("us_abt", "US de abdômen total (adulto)", "US", US_ABT, 117.51, 20, 9895, US_ABT, 1,
     "jejum e bexiga cheia: agenda de manhã"),
    ("us_par", "US de parede abdominal (código do abdômen total)", "US", US_ABT, 117.51, 20, 3304, None, 1,
     "depende de a SES aceitar o código (L-007)"),
    ("us_uri", "US de aparelho urinário e rins (adulto)", "US", "02.05.02.005-4", 90.53, 15, 3749,
     "02.05.02.005-4", 1, "bexiga cheia: espera de cerca de 1 h"),
    ("us_dca", "Doppler de carótidas e outros vasos", "US", US_DOP, 115.61, 20, 4727, US_DOP, 2,
     "médico com prática vascular"),
    ("us_tv", "US transvaginal (sem a reserva de 4.000 da GIN1)", "US", "02.05.02.018-6", 83.77, 15, 5294, None, 2,
     "acompanhante, transdutor com desinfecção; fila do código encolhe"),
    ("us_pro", "US de próstata (via abdominal)", "US", "02.05.02.010-0", 74.19, 15, 2969, "02.05.02.010-0", 2,
     "bexiga cheia; acompanhante"),
    ("us_tir", "US de tireoide (com o Doppler de tireoide)", "US", "02.05.02.012-7", 64.07, 15, 3794,
     "02.05.02.012-7", 1, "sem preparo"),
    ("us_mam", "US de mamas (as duas)", "US", US_MAMA, 70.97, 20, 12950, US_MAMA, 1,
     "sem preparo; a fila caiu com mutirões da SES (01/11)"),
    ("us_abt_i", "US de abdômen total (criança)", "US", US_ABT, 117.51, 20, 452, None, 2,
     "criança: acompanhante e mais cuidado para posicionar"),
    ("us_uri_i", "US de aparelho urinário (criança)", "US", "02.05.02.005-4", 90.53, 15, 276, None, 2,
     "criança: acompanhante; bexiga cheia"),
    ("us_esc_i", "US de bolsa escrotal (criança)", "US", "02.05.02.007-0", 100.00, 15, 234, None, 2,
     "criança: acompanhante"),
    ("us_tir_i", "US de tireoide (criança)", "US", "02.05.02.012-7", 64.07, 15, 60, None, 2, "criança: acompanhante"),
    ("us_dmi", "Doppler de membros (os dois lados)", "US", US_DOP, 115.61, 40, 12043, US_DOP, 2,
     "40 min por exame; médico com prática vascular"),
]
FORA = [
    ("Angiotomografia de coronárias", 1532, "decisão do usuário de 02/11: não atender (betabloqueador, controle de "
     "frequência e ECG)"),
    ("Transfontanela", 270, "saiu em 03/11, a pedido do usuário"),
    ("US pélvica ginecológica (adulto e criança)", 1014, "fora da conta (usuário, 09/11): paga R$ 43,41, menos que o "
     "custo"),
    ("Filas de emergência", None, "D-009: só ambulatório"),
    ("Partes moles, articulação, OCI do IEV e a reserva de 4.000 transvaginais", None, "L-008: um pedido, um plano"),
]

# pedidos novos que a SES não absorve, em 12 meses: o saldo mensal do código × 12, só quando positivo.
# No Doppler, o saldo do código se reparte entre carótidas e membros pela fila de cada um.
dop_total = 4727 + 12043


def novos(chave, cod_dem):
    if cod_dem is None:
        return 0
    saldo = DEM[cod_dem]["saldo_elegivel_mes"]
    if saldo <= 0:
        return 0
    n = saldo * P["meses"]
    if cod_dem == US_DOP:
        n *= (4727 if chave == "us_dca" else 12043) / dop_total
    return int(n)


# a v26 (as metas assinadas) e o espaço que cada código ainda tem na fila de 12 meses
V26 = [  # (linha da v26, código, meta, preço Candanga, minutos, linha de margem equivalente)
    ("US de mamas", US_MAMA, 14689, 70.97, 20, "us_mam"),
    ("Doppler venoso de membros", US_DOP, 9834, 115.61, 40, "us_dmi"),
    ("Doppler de carótidas", US_DOP, 4674, 115.61, 20, "us_dca"),
    ("US de abdômen total", US_ABT, 10028, 117.51, 20, "us_abt"),
    ("US de parede abdominal (código do abdômen total)", US_ABT, 3138, 117.51, 20, "us_par"),
    ("US transvaginal", "02.05.02.018-6", 10541, 83.77, 15, "us_tv"),
    ("US de aparelho urinário", "02.05.02.005-4", 3944, 90.53, 15, "us_uri"),
    ("US de tireoide", "02.05.02.012-7", 3216, 64.07, 15, "us_tir"),
    ("US de próstata", "02.05.02.010-0", 3201, 74.19, 15, "us_pro"),
    ("US de abdômen superior", "02.05.02.003-8", 2261, 101.27, 15, "us_abs"),
    ("TC de abdômen superior com contraste", TC_A, 4516, 309.25, 20, "tc_abd_c"),
    ("TC de pelve com contraste", TC_P, 3862, 309.25, 20, "tc_pel_c"),
    ("TC de tórax com contraste", TC_T, 3104, 309.25, 20, "tc_tor_c"),
    ("Angiotomografia de coronárias (código da TC de tórax)", TC_T, 1408, 309.25, 30, "tc_tor_c"),
    ("TC de tórax sem contraste, emergência", TC_T, 728, 309.25, 11, "tc_tor_s"),
]


def margem(ch):
    l = next(x for x in LINHAS if x[0] == ch)
    preco, mins = l[4], l[5]
    if l[2] == "TC":
        return preco - P["tc_sem"] - (P["tc_contraste"] if mins >= 20 else 0)
    med_h = P["medico_h"] if P["medico_modo"] == "hora" else 0
    med_ex = P["medico_ex"] if P["medico_modo"] == "exame" else 0
    h = (med_h + P["sala_mes"] / P["horas_exame_mes"] + P["aux_mes"] / P["horas_exame_mes"])
    return preco - h * mins / 60 - P["insumo"] - med_ex


# ---------------------------------------------------------------- cenário 1: a sobra vai aos códigos da v26 com espaço
def espaco_codigo(cod):
    d = DEM[cod]
    fila12 = d["fila_elegivel"] + max(0, d["saldo_elegivel_mes"]) * P["meses"]
    if cod == TC_T:  # a fila elegível não tem coronária nem emergência: compara com a meta ambulatorial
        meta = 3104
    else:
        meta = sum(m for _, c, m, *_ in V26 if c == cod)
    return int(fila12 - meta)


CAND1 = [  # códigos da v26 que podem receber exames a mais, na linha de margem que representa o código
    ("US de abdômen superior", "02.05.02.003-8", "us_abs"),
    ("US de aparelho urinário", "02.05.02.005-4", "us_uri"),
    ("US de abdômen total", US_ABT, "us_abt"),
    ("Doppler de carótidas", US_DOP, "us_dca"),
    ("US de tireoide", "02.05.02.012-7", "us_tir"),
    ("US de próstata", "02.05.02.010-0", "us_pro"),
    ("TC de abdômen superior com contraste", TC_A, "tc_abd_c"),
    ("TC de pelve com contraste", TC_P, "tc_pel_c"),
    ("TC de tórax com contraste", TC_T, "tc_tor_c"),
]


def cenario1():
    sobra = P["envelope"] - P["v26_candanga"]
    preco = {x[0]: x[4] for x in LINHAS}
    ordem = sorted(CAND1, key=lambda c: -margem(c[2]) / preco[c[2]])
    escolha = []
    for rot, cod, ch in ordem:
        esp = max(0, espaco_codigo(cod))
        q = min(esp, int(sobra // preco[ch]))
        escolha.append((rot, cod, ch, esp, q))
        sobra -= q * preco[ch]
    return escolha


# ---------------------------------------------------------------- cenário 2: escolher de novo, pela margem
def cenario2():
    preco = {x[0]: x[4] for x in LINHAS}
    blocos = []
    for l in LINHAS:
        ch = l[0]
        m = margem(ch) / preco[ch]
        if m <= 0:  # não paga o próprio custo: fica fora
            continue
        baixa = 2 if m < P["limiar"] else 0  # margem baixa: só entra no fim, para fechar o valor
        blocos.append((1 + baixa, -m, ch, "fila de hoje", l[6]))
        n = novos(ch, l[7])
        if n:
            blocos.append((2 + baixa, -m, ch, "pedidos novos em 12 meses", n))
    blocos.sort()
    resto = P["envelope"]
    escolha = {}
    for passo, mneg, ch, tipo, qtd in blocos:
        q = min(qtd, int(resto // preco[ch]))
        escolha.setdefault(ch, {})[tipo] = escolha.get(ch, {}).get(tipo, 0) + q
        resto -= q * preco[ch]
    return escolha


# ================================================================== a planilha
A = "Arial"
FN = Font(name=A, size=10)
FB = Font(name=A, size=10, bold=True)
FT = Font(name=A, size=13, bold=True)
FS = Font(name=A, size=9, italic=True, color="555555")
FIN = Font(name=A, size=10, color="0000FF")
FLK = Font(name=A, size=10, color="008000")
AMA = PatternFill("solid", fgColor="FFF2CC")
CAB = PatternFill("solid", fgColor="D9E1F2")
SEC = PatternFill("solid", fgColor="E2EFDA")
TOT = PatternFill("solid", fgColor="EDEDED")
VERDE = PatternFill("solid", fgColor="C6EFCE")
VERM = PatternFill("solid", fgColor="FFC7CE")
BORDA = Border(*(Side(style="thin", color="BFBFBF"),) * 4)
TOPO = Alignment(vertical="top", wrap_text=True)
CEN = Alignment(horizontal="center", vertical="top", wrap_text=True)
NOW = Alignment(vertical="top", wrap_text=False)
INT, DEC1, DEC2, PCT, PCT1, BRL = "#,##0", "#,##0.0", "#,##0.00", "0%", "0.0%", '"R$" #,##0.00'
BRL0 = '"R$" #,##0'

wb = Workbook()
wb.remove(wb.active)


def aba(nome, larg):
    ws = wb.create_sheet(nome)
    ws.sheet_view.showGridLines = False
    for i, w in enumerate(larg):
        ws.column_dimensions[L(i + 1)].width = w
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    return ws


def put(ws, ref, v, fmt=None, font=FN, fill=None, borda=True, alin=TOPO):
    c = ws[ref]
    c.value = v
    c.font = font
    c.alignment = alin
    if borda:
        c.border = BORDA
    if fill:
        c.fill = fill
    if fmt:
        c.number_format = fmt
    return c


def ent(ws, ref, v, fmt=None, alin=TOPO):
    return put(ws, ref, v, fmt, FIN, AMA, alin=alin)


def lk(ws, ref, f, fmt=None, bold=False):
    return put(ws, ref, f, fmt, Font(name=A, size=10, color="008000", bold=bold))


def titulo(ws, t, sub):
    put(ws, "A1", t, font=FT, borda=False, alin=NOW)
    put(ws, "A2", sub, font=FS, borda=False, alin=NOW)


def cab(ws, r, rot, altura=40):
    for i, t in enumerate(rot):
        put(ws, f"{L(i + 1)}{r}", t, font=FB, fill=CAB)
    ws.row_dimensions[r].height = altura


def secao(ws, r, t, n):
    for i in range(n):
        put(ws, f"{L(i + 1)}{r}", t if i == 0 else None, font=FB, fill=SEC, alin=NOW)


def nota(ws, r, t):
    put(ws, f"A{r}", t, font=FS, borda=False, alin=NOW)


leia = aba("Leia", [130])
pr = aba("Premissas", [64, 16, 70])
mg = aba("1 Margem por exame", [46, 6, 10, 9, 10, 10, 10, 10, 10, 11, 10, 9, 9, 11, 46])
c1 = aba("2 Cenário 1", [50, 15, 10, 11, 11, 10, 14, 14, 12, 40])
c2 = aba("3 Cenário 2", [46, 6, 11, 10, 11, 11, 11, 14, 14, 12, 40])
cp = aba("4 Comparação", [62, 18, 18, 18])
ct = aba("5 Contraste", [40, 14, 16, 14, 14, 14, 16, 14, 14])
pe = aba("6 Exame a exame", [58, 12, 12, 12, 16, 16, 16, 15, 15, 15, 52])

# ---------------------------------------------------------------- premissas
titulo(pr, "Premissas", "Amarelo com fonte azul: pode mudar. As quantidades dos cenários saem do script com estes "
                        "valores; mudou, rodar de novo.")
cab(pr, 4, ["Premissa", "Valor", "De onde vem"], 18)
prem = [
    ("envelope", "Valor dos exames (recurso menos o apoio da v26)", BRL, "estudo de 05/11, aba 3: 11.592.762 − "
     "956.160. Com o quadro P2 de 12 meses (978.120), cai para 10.614.642"),
    ("v26_candanga", "As metas da v26 pagas pela Candanga", BRL, "estudo de 05/11, aba 3 (79.144 exames)"),
    ("medico_modo", "Como se paga o médico do ultrassom (hora ou exame)", None, "escreva hora ou exame; as "
     "quantidades dos cenários mudam: rodar o script com MEDICO_MODO=exame"),
    ("medico_h", "Médico do ultrassom, por hora", BRL, "estudo das filas de 02/11 (custos)"),
    ("medico_ex", "Médico do ultrassom, por exame", BRL, "modelo do ISHP de 20/10: R$ 1.000 por lote de 30 exames"),
    ("sala_mes", "Sala e aparelho de ultrassom, por sala por mês", BRL, "custo v2 de 20/10: sala R$ 3.000 + "
     "aparelho R$ 2.500"),
    ("aux_mes", "Auxiliar de sala do ultrassom, por sala por mês (2 pessoas em 10 h)", BRL,
     "formulário de 09/11 (uma pessoa com o médico o exame todo); custo de recepcionista em Brasília, R$ 2.959"),
    ("horas_exame_mes", "Horas de exame por sala por mês", DEC1, "21 dias × 10 h × 80%"),
    ("insumo", "Insumos por exame de ultrassom", BRL, "custo v2 de 20/10 (hipótese)"),
    ("tc_sem", "Tomografia na clínica, por exame, sem contraste", BRL, "usuário, 09/11"),
    ("tc_contraste", "A mais por exame com contraste", BRL, "usuário, 09/11"),
    ("meses", "Meses de execução", INT, "pedido da equipe, 07/11"),
    ("limiar", "Margem mínima: abaixo dela, o exame só entra no fim do cenário 2, para fechar o valor", PCT,
     "escolha deste estudo: abaixo disso o exame quase não paga o próprio custo"),
    ("salas", "Salas de ultrassom", INT, "estudo de 07/11: 13 a 15 em 12 meses"),
    ("tomografos", "Tomógrafos", INT, "3 polos de tomografia"),
    ("horas_dia", "Horas abertas por dia", INT, "v26, 7.3"),
    ("uso", "Parte das horas com exame", PCT, "estudos de 07/11 e 08/11"),
    ("dias_ano", "Dias úteis em 12 meses", INT, "21 × 12"),
]
PR = {}
for i, (k, rot, fmt, fonte) in enumerate(prem):
    r = 5 + i
    PR[k] = f"Premissas!$B${r}"
    put(pr, f"A{r}", rot)
    ent(pr, f"B{r}", P[k], fmt)
    put(pr, f"C{r}", fonte, font=FS)
r += 1
PR["custo_h"] = f"Premissas!$B${r}"
put(pr, f"A{r}", "Custo da hora de exame no ultrassom (médico + sala + auxiliar)", font=FB)
put(pr, f"B{r}", f"=IF({PR['medico_modo']}=\"hora\",{PR['medico_h']},0)+{PR['sala_mes']}/{PR['horas_exame_mes']}+"
                 f"{PR['aux_mes']}/{PR['horas_exame_mes']}", BRL, FB)
put(pr, f"C{r}", "a recepção é do polo e não muda com o tipo de exame: fica fora", font=FS)
r += 1
PR["sobra"] = f"Premissas!$B${r}"
put(pr, f"A{r}", "Sobra: valor dos exames menos as metas da v26 pela Candanga", font=FB)
put(pr, f"B{r}", f"={PR['envelope']}-{PR['v26_candanga']}", BRL, FB)

# ---------------------------------------------------------------- margem por exame
titulo(mg, "Margem de cada exame: o que o convênio paga menos o que custa fazer",
       "Ultrassom feito por nós (médico por hora, sala, aparelho, auxiliar e insumos); tomografia na clínica, por "
       "exame. A margem não é lucro: no convênio, o que não se gasta volta como saldo ou vira mais exames.")
cab(mg, 4, ["Exame", "Mod.", "Preço Candanga", "Minutos", "Custo por exame", "Margem por exame", "Margem (% do "
            "preço)", "Exames por hora", "Margem por hora", "Complexidade (1 a 3)", "Fila de hoje", "Pedidos novos "
            "em 12 meses", "Fila em 12 meses", "Ordem pela margem", "Por que a complexidade"], 52)
MG = {}
for i, (ch, ex, mod, cod, preco, mins, fh, cdem, cx, porque) in enumerate(LINHAS):
    r = 5 + i
    MG[ch] = r
    put(mg, f"A{r}", ex, font=FB)
    put(mg, f"B{r}", mod, alin=CEN)
    ent(mg, f"C{r}", preco, BRL)
    ent(mg, f"D{r}", mins, INT, alin=CEN)
    if mod == "TC":
        put(mg, f"E{r}", f"={PR['tc_sem']}+IF(D{r}>=20,{PR['tc_contraste']},0)", BRL)
    else:
        put(mg, f"E{r}", f"={PR['custo_h']}*D{r}/60+{PR['insumo']}+IF({PR['medico_modo']}=\"exame\","
                         f"{PR['medico_ex']},0)", BRL)
    put(mg, f"F{r}", f"=C{r}-E{r}", BRL, FB)
    put(mg, f"G{r}", f"=F{r}/C{r}", PCT1, FB)
    put(mg, f"H{r}", f"=60/D{r}", DEC1)
    put(mg, f"I{r}", f"=F{r}*H{r}", BRL, FB)
    ent(mg, f"J{r}", cx, INT, alin=CEN)
    ent(mg, f"K{r}", fh, INT)
    ent(mg, f"L{r}", novos(ch, cdem), INT)
    put(mg, f"M{r}", f"=K{r}+L{r}", INT)
    put(mg, f"O{r}", porque, font=FS)
u = 5 + len(LINHAS) - 1
for r in range(5, u + 1):
    put(mg, f"N{r}", f"=RANK(G{r},$G$5:$G${u})", INT, alin=CEN)
mg.conditional_formatting.add(f"G5:G{u}", CellIsRule(operator="lessThan", formula=[PR["limiar"]], fill=VERM))
mg.conditional_formatting.add(f"G5:G{u}", CellIsRule(operator="greaterThanOrEqual", formula=["0.45"], fill=VERDE))
nota(mg, u + 2, "Pedidos novos em 12 meses: o que entra por mês e a SES não agenda (estudo de 02/11), × 12; só quando "
                "positivo. No Doppler, o saldo do código se reparte entre carótidas e membros pela fila.")
nota(mg, u + 3, "Complexidade: 1 = sem preparo especial ou só jejum; 2 = acompanhante, médico com prática específica "
                "ou exame longo; 3 = contraste na veia (punção, repouso, radiologista presente, risco de reação).")
nota(mg, u + 4, "Vermelho: abaixo da margem mínima das premissas. Verde: 45% ou mais.")
r = u + 6
secao(mg, r, "O que ficou fora das duas contas", 15)
for rot, q, porque in FORA:
    r += 1
    put(mg, f"A{r}", rot)
    put(mg, f"B{r}", q, INT) if q else put(mg, f"B{r}", None)
    put(mg, f"C{r}", porque, font=FS, borda=False, alin=NOW)

# ---------------------------------------------------------------- cenário 1
e1 = cenario1()
titulo(c2 if False else c1, "Cenário 1: a v26 como está, e só a sobra readequada",
       "As metas assinadas não mudam; pagas pela Candanga, sobram cerca de R$ 245 mil. A sobra vai aos códigos da v26 "
       "que ainda têm fila, na ordem da margem (% do preço).")
cab(c1, 4, ["Linha da v26", "Código", "Meta", "Preço Candanga", "Minutos", "Margem por exame", "Valor", "Margem",
            "Horas de aparelho", "Observação"], 40)
r = 4
p1 = r + 1
R1 = {}
for rot, cod, meta, preco, mins, chm in V26:
    r += 1
    R1[rot] = r
    put(c1, f"A{r}", rot)
    put(c1, f"B{r}", cod)
    put(c1, f"C{r}", meta, INT)
    put(c1, f"D{r}", preco, BRL)
    put(c1, f"E{r}", mins, INT)
    lk(c1, f"F{r}", f"='1 Margem por exame'!F{MG[chm]}", BRL)
    put(c1, f"G{r}", f"=C{r}*D{r}", BRL)
    put(c1, f"H{r}", f"=C{r}*F{r}", BRL)
    put(c1, f"I{r}", f"=C{r}*E{r}/60", INT)
    obs = {"US de mamas": "meta acima da fila de hoje (12.950); a fila caiu com mutirões",
           "US transvaginal": "meta acima da fila sem a reserva da GIN1 (5.294)",
           "Angiotomografia de coronárias (código da TC de tórax)": "fica na v26 como está; fora das prioridades "
           "do usuário (02/11)",
           "TC de tórax sem contraste, emergência": "fica na v26 como está; D-009 a tiraria (+R$ 225 mil de sobra)"}
    put(c1, f"J{r}", obs.get(rot), font=FS)
u1 = r
r += 1
put(c1, f"A{r}", "Metas da v26", font=FB, fill=TOT)
for col in "BDEF":
    put(c1, f"{col}{r}", None, fill=TOT)
put(c1, f"C{r}", f"=SUM(C{p1}:C{u1})", INT, FB, TOT)
for col in "GHI":
    put(c1, f"{col}{r}", f"=SUM({col}{p1}:{col}{u1})", BRL if col != "I" else INT, FB, TOT)
put(c1, f"J{r}", None, fill=TOT)
rv26 = r
r += 2
secao(c1, r, "A sobra: onde entra", 10)
r += 1
cab(c1, r, ["Código que recebe", "Código", "Espaço na fila de 12 meses", "Preço Candanga", "Minutos",
            "Margem por exame", "Valor", "Margem", "Horas de aparelho", "Exames a mais"], 40)
p2 = r + 1
R1s = {}
for rot, cod, ch, esp, q in e1:
    r += 1
    R1s[ch] = r
    put(c1, f"A{r}", rot)
    put(c1, f"B{r}", cod)
    put(c1, f"C{r}", esp, INT)
    lk(c1, f"D{r}", f"='1 Margem por exame'!C{MG[ch]}", BRL)
    lk(c1, f"E{r}", f"='1 Margem por exame'!D{MG[ch]}", INT)
    lk(c1, f"F{r}", f"='1 Margem por exame'!F{MG[ch]}", BRL)
    put(c1, f"G{r}", f"=J{r}*D{r}", BRL)
    put(c1, f"H{r}", f"=J{r}*F{r}", BRL)
    put(c1, f"I{r}", f"=J{r}*E{r}/60", INT)
    ent(c1, f"J{r}", q, INT)
u2 = r
r += 1
put(c1, f"A{r}", "A sobra readequada", font=FB, fill=TOT)
for col in "BCDEF":
    put(c1, f"{col}{r}", None, fill=TOT)
for col in "GHI":
    put(c1, f"{col}{r}", f"=SUM({col}{p2}:{col}{u2})", BRL if col != "I" else INT, FB, TOT)
put(c1, f"J{r}", f"=SUM(J{p2}:J{u2})", INT, FB, TOT)
rsob = r
r += 2
C1 = {}
for k, rot, f, fmt in [
    ("ex", "Exames do cenário 1", f"=C{rv26}+J{rsob}", INT),
    ("val", "Valor dos exames", f"=G{rv26}+G{rsob}", BRL),
    ("res", "Não gasto do valor dos exames", f"={PR['envelope']}-G{rv26}-G{rsob}", BRL),
    ("mar", "Margem total", f"=H{rv26}+H{rsob}", BRL),
    ("marp", "Margem total, em % do valor", f"=(H{rv26}+H{rsob})/(G{rv26}+G{rsob})", PCT1),
]:
    C1[k] = f"'2 Cenário 1'!$B${r}"
    put(c1, f"A{r}", rot, font=FB)
    put(c1, f"B{r}", f, fmt, FB)
    r += 1
nota(c1, r + 1, "Espaço na fila de 12 meses: a fila elegível de hoje mais os pedidos novos de 12 meses, menos a meta "
                "da v26 no código. A ordem é a da margem em % do preço: com o dinheiro fixo, é ela que deixa mais folga.")
nota(c1, r + 2, "A TC entraria depois: a margem por exame é maior, mas a % do preço é menor, e a hora do tomógrafo é o "
                "recurso mais apertado com 3 polos.")

# ---------------------------------------------------------------- cenário 2
e2 = cenario2()
titulo(c2, "Cenário 2: as filas escolhidas de novo, pela margem e pela complexidade",
       "Primeiro a fila de hoje, depois os pedidos novos dos 12 meses, da maior para a menor margem (% do preço). O que "
       "fica abaixo da margem mínima entra por último, só para fechar o valor.")
cab(c2, 4, ["Exame", "Mod.", "Fila de hoje (escolhida)", "Pedidos novos (escolhidos)", "Exames", "Margem (%)",
            "Complexidade", "Valor", "Margem", "Horas de aparelho", "O que ficou de fora e por quê"], 52)
r = 4
p3 = r + 1
R2 = {}
for ch, ex, mod, *_ in LINHAS:
    r += 1
    R2[ch] = r
    m = MG[ch]
    hoje = e2.get(ch, {}).get("fila de hoje", 0)
    nov = e2.get(ch, {}).get("pedidos novos em 12 meses", 0)
    put(c2, f"A{r}", ex, font=FB)
    put(c2, f"B{r}", mod, alin=CEN)
    ent(c2, f"C{r}", hoje, INT)
    ent(c2, f"D{r}", nov, INT)
    put(c2, f"E{r}", f"=C{r}+D{r}", INT, FB)
    lk(c2, f"F{r}", f"='1 Margem por exame'!G{m}", PCT1)
    lk(c2, f"G{r}", f"='1 Margem por exame'!J{m}", INT)
    put(c2, f"H{r}", f"=E{r}*'1 Margem por exame'!C{m}", BRL)
    put(c2, f"I{r}", f"=E{r}*'1 Margem por exame'!F{m}", BRL)
    put(c2, f"J{r}", f"=E{r}*'1 Margem por exame'!D{m}/60", INT)
    put(c2, f"K{r}", f"=IF(E{r}<'1 Margem por exame'!M{m},TEXT('1 Margem por exame'!M{m}-E{r},\"#,##0\")&\" fora\"&"
                     f"IF(F{r}<=0,\": não paga o próprio custo\",IF(F{r}<{PR['limiar']},\": margem abaixo da mínima, entrou por último\",\": não coube no valor\")),"
                     f"IF(F{r}<{PR['limiar']},\"margem abaixo da mínima: entrou por último, para fechar o valor\",\"\"))",
    font=FS)
u3 = r
r += 1
put(c2, f"A{r}", "Total", font=FB, fill=TOT)
put(c2, f"B{r}", None, fill=TOT)
for col in "CDE":
    put(c2, f"{col}{r}", f"=SUM({col}{p3}:{col}{u3})", INT, FB, TOT)
put(c2, f"F{r}", f"=I{r}/H{r}", PCT1, FB, TOT)
put(c2, f"G{r}", None, fill=TOT)
for col in "HI":
    put(c2, f"{col}{r}", f"=SUM({col}{p3}:{col}{u3})", BRL, FB, TOT)
put(c2, f"J{r}", f"=SUM(J{p3}:J{u3})", INT, FB, TOT)
put(c2, f"K{r}", None, fill=TOT)
rt2 = r
r += 2
C2 = {}
for k, rot, f, fmt in [
    ("ex", "Exames do cenário 2", f"=E{rt2}", INT),
    ("val", "Valor dos exames", f"=H{rt2}", BRL),
    ("res", "Não gasto do valor dos exames", f"={PR['envelope']}-H{rt2}", BRL),
    ("mar", "Margem total", f"=I{rt2}", BRL),
    ("marp", "Margem total, em % do valor", f"=F{rt2}", PCT1),
    ("hus", "Horas de ultrassom", f'=SUMIF(B{p3}:B{u3},"US",J{p3}:J{u3})', INT),
    ("htc", "Horas de tomógrafo", f'=SUMIF(B{p3}:B{u3},"TC",J{p3}:J{u3})', INT),
    ("nov", "Exames que dependem de pedidos novos", f"=D{rt2}", INT),
]:
    C2[k] = f"'3 Cenário 2'!$B${r}"
    put(c2, f"A{r}", rot, font=FB)
    put(c2, f"B{r}", f, fmt, FB)
    r += 1

# ---------------------------------------------------------------- comparação (com a carteira 1 de hoje)
c1rows = FILAS["cenarios"][[k for k in FILAS["cenarios"] if k.startswith("1")][0]]
cart = {"ex": sum(x["meta"] for x in c1rows), "val": sum(x["valor"] for x in c1rows)}
ch_mod = {}
for x in c1rows:
    mod = "TC" if x["modalidade"] == "Tomografia" else "US"
    mins = x["minutos"]
    preco = x["valor"] / x["meta"] if x["meta"] else 0
    if mod == "TC":
        m = preco - P["tc_sem"] - (P["tc_contraste"] if mins >= 20 else 0)
    else:
        med_h = P["medico_h"] if P["medico_modo"] == "hora" else 0
        med_ex = P["medico_ex"] if P["medico_modo"] == "exame" else 0
        m = preco - (med_h + P["sala_mes"] / P["horas_exame_mes"] + P["aux_mes"] / P["horas_exame_mes"]) * \
            mins / 60 - P["insumo"] - med_ex
    cart["mar"] = cart.get("mar", 0) + m * x["meta"]
    cart["h" + mod] = cart.get("h" + mod, 0) + x["meta"] * mins / 60
titulo(cp, "Os dois cenários lado a lado, com a carteira 1 de hoje",
       "A carteira 1 (02/11 e 03/11) é a escolha em vigor; a margem dela usa as mesmas premissas (valor fixo, "
       "calculado pelo script).")
cab(cp, 4, ["", "Cenário 1: a v26 e a sobra", "Cenário 2: escolher de novo", "Carteira 1 (em vigor)"], 30)
cap_us = f"{PR['salas']}*{PR['dias_ano']}*{PR['horas_dia']}*{PR['uso']}"
cap_tc = f"{PR['tomografos']}*{PR['dias_ano']}*{PR['horas_dia']}*{PR['uso']}"
linhas_cp = [
    ("Exames", f"={C1['ex']}", f"={C2['ex']}", cart["ex"], INT),
    ("Valor dos exames", f"={C1['val']}", f"={C2['val']}", cart["val"], BRL),
    ("Não gasto do valor dos exames", f"={C1['res']}", f"={C2['res']}", f"={PR['envelope']}-D6", BRL),
    ("Margem total (folga para executar)", f"={C1['mar']}", f"={C2['mar']}", round(cart["mar"], 2), BRL),
    ("Margem, em % do valor", "=B8/B6", "=C8/C6", "=D8/D6", PCT1),
    ("Horas de ultrassom", f"=SUMIF('2 Cenário 1'!B{p1}:B{u1},\"02.05*\",'2 Cenário 1'!I{p1}:I{u1})+SUMIF("
                           f"'2 Cenário 1'!B{p2}:B{u2},\"02.05*\",'2 Cenário 1'!I{p2}:I{u2})", f"={C2['hus']}",
     round(cart["hUS"]), INT),
    ("Uso das salas de ultrassom", f"=B10/({cap_us})", f"=C10/({cap_us})", f"=D10/({cap_us})", PCT),
    ("Horas de tomógrafo (20 min com contraste, 11 sem)", f"=SUMIF('2 Cenário 1'!B{p1}:B{u1},\"02.06*\",'2 Cenário "
     f"1'!I{p1}:I{u1})+SUMIF('2 Cenário 1'!B{p2}:B{u2},\"02.06*\",'2 Cenário 1'!I{p2}:I{u2})", f"={C2['htc']}",
     round(cart["hTC"]), INT),
    ("Uso dos 3 tomógrafos", f"=B12/({cap_tc})", f"=C12/({cap_tc})", f"=D12/({cap_tc})", PCT),
]
for i, (rot, b, c, d, fmt) in enumerate(linhas_cp):
    r = 5 + i
    put(cp, f"A{r}", rot, font=FB)
    put(cp, f"B{r}", b, fmt)
    put(cp, f"C{r}", c, fmt)
    put(cp, f"D{r}", d, fmt)
nota(cp, 15, "Horas de tomógrafo da carteira 1 com os minutos do estudo de 02/11 (20 com contraste e angio, 15 sem); "
             "as do cenário 1 incluem a angio de coronárias a 30 min.")
nota(cp, 16, "Uso: horas ÷ (aparelhos × 252 dias × 10 h × 80%). Acima de 100%, não cabe.")
for col in "BCD":
    cp.conditional_formatting.add(f"{col}11", CellIsRule(operator="greaterThan", formula=["1"], fill=VERM))
    cp.conditional_formatting.add(f"{col}13", CellIsRule(operator="greaterThan", formula=["1"], fill=VERM))

# ---------------------------------------------------------------- contraste: quanto dos pedidos é feito com contraste
titulo(ct, "E se nem todo pedido com contraste for feito com contraste?",
       "O radiologista readequa os pedidos (a fila está muito \"suja\"). Cada exame feito sem contraste custa R$ 50 a "
       "menos na clínica, ocupa o tomógrafo 11 min em vez de 20 e paga o mesmo (o código é o mesmo).")
put(ct, "A4", "Minutos de tomógrafo: com contraste")
ent(ct, "B4", 20, INT)
put(ct, "A5", "Minutos de tomógrafo: sem contraste")
ent(ct, "B5", 11, INT)
put(ct, "C4", "estudo de 08/11: em série 20; sem contraste 11", font=FS, borda=False, alin=NOW)
conv1 = "+".join(f"'2 Cenário 1'!C{R1[k]}" for k in ("TC de abdômen superior com contraste", "TC de pelve com contraste",
                                                      "TC de tórax com contraste"))
conv2 = "+".join(f"'3 Cenário 2'!E{R2[k]}" for k in ("tc_abd_c", "tc_pel_c", "tc_tor_c", "tc_pes_c", "tc_cra_c",
                                                      "tc_fac_c"))
put(ct, "A6", "Pedidos com contraste que podem ir sem: cenário 1", font=FB)
put(ct, "B6", f"={conv1}", INT, FB)
put(ct, "A7", "Pedidos com contraste que podem ir sem: cenário 2", font=FB)
put(ct, "B7", f"={conv2}", INT, FB)
put(ct, "C6", "abdômen, pelve e tórax com contraste da v26; a angio de coronárias e as angiotomografias não vão sem "
              "contraste", font=FS, borda=False, alin=NOW)
put(ct, "C7", "abdômen, pelve, tórax, pescoço, crânio e face com contraste", font=FS, borda=False, alin=NOW)
for bloco, (rot, linha_conv, mar, val, htc) in enumerate([
        ("Cenário 1: a v26 e a sobra", "$B$6", C1["mar"], C1["val"], "'4 Comparação'!$B$12"),
        ("Cenário 2: escolher de novo", "$B$7", C2["mar"], C2["val"], "'4 Comparação'!$C$12")]):
    r0 = 9 + bloco * 11
    secao(ct, r0, rot, 9)
    cab(ct, r0 + 1, ["Parte feita com contraste", "Exames feitos sem contraste", "Margem total", "Margem (% do valor)",
                     "Margem a mais", "Horas de tomógrafo", "Uso dos 3 tomógrafos", "Horas poupadas",
                     "Horas de contraste por dia, por tomógrafo"], 40)
    for i, parte in enumerate([1.0, 0.9, 0.8, 0.7, 0.6, 0.5]):
        r = r0 + 2 + i
        ent(ct, f"A{r}", parte, PCT, alin=CEN)
        put(ct, f"B{r}", f"=ROUND({linha_conv}*(1-A{r}),0)", INT)
        put(ct, f"C{r}", f"={mar}+B{r}*{PR['tc_contraste']}", BRL, FB)
        put(ct, f"D{r}", f"=C{r}/{val}", PCT1, FB)
        put(ct, f"E{r}", f"=C{r}-$C${r0 + 2}", BRL)
        put(ct, f"F{r}", f"={htc}-B{r}*($B$4-$B$5)/60", INT)
        put(ct, f"G{r}", f"=F{r}/({cap_tc})", PCT, FB)
        put(ct, f"H{r}", f"=$F${r0 + 2}-F{r}", INT)
        put(ct, f"I{r}", f"=({linha_conv}*A{r})*$B$4/60/({PR['tomografos']}*{PR['dias_ano']})/{PR['uso']}", DEC1)
nota(ct, 31, "A linha de 100% é a conta das abas 2 e 3. As quantidades não mudam: o preço é o mesmo com ou sem "
             "contraste. Só mudam o custo na clínica, as horas de tomógrafo e as horas de radiologista.")
nota(ct, 32, "Horas de contraste por dia: só os exames convertíveis feitos com contraste; as angiotomografias somam por "
             "cima no cenário 2 e a angio de coronárias no cenário 1. É o turno em que o radiologista precisa estar.")
nota(ct, 33, "Referência (estudo de 08/11): na rotina, o radiologista muda o contraste de 8,5% a 14% dos pedidos; 38% a "
             "61% só na falta de contraste de 2022. A fila é cerca de 37% câncer, que pede fase com contraste.")

# ---------------------------------------------------------------- exame a exame: cenário 2 no formato do cenário 1
titulo(pe, "Exame a exame: o cenário 2 ao lado do cenário 1",
       "Cenário 1: as metas da v26 mais a sobra. Cenário 2: a escolha pela margem. Tudo liga nas abas 2 e 3 (médico do "
       "ultrassom pago por hora).")
cab(pe, 4, ["Exame", "Cenário 1: exames", "Cenário 2: exames", "Diferença de exames", "Cenário 1: valor",
            "Cenário 2: valor", "Diferença de valor", "Cenário 1: margem", "Cenário 2: margem", "Diferença de margem",
            "Por que muda"], 40)
V26CH = {"US de mamas": "us_mam", "Doppler venoso de membros": "us_dmi", "Doppler de carótidas": "us_dca",
         "US de abdômen total": "us_abt", "US de parede abdominal (código do abdômen total)": "us_par",
         "US transvaginal": "us_tv", "US de aparelho urinário": "us_uri", "US de tireoide": "us_tir",
         "US de próstata": "us_pro", "US de abdômen superior": "us_abs",
         "TC de abdômen superior com contraste": "tc_abd_c", "TC de pelve com contraste": "tc_pel_c",
         "TC de tórax com contraste": "tc_tor_c"}
POR_QUE = {
    "us_mam": "a v26 passa da fila de 12 meses (14.134)",
    "us_dmi": "médico por hora: o Doppler de membros quase não se paga e entra por último (por exame, entra a fila toda)",
    "us_dca": "o cenário 2 usa a fila de hoje e os pedidos novos",
    "us_abt": "o cenário 2 usa a fila de hoje e os pedidos novos; o cenário 1 recebe parte da sobra",
    "us_tv": "a v26 passa da fila sem a reserva de 4.000 da GIN1 (5.294)",
    "us_uri": "o cenário 1 recebe parte da sobra",
    "us_abs": "o cenário 1 recebe parte da sobra",
    "us_tir": "o cenário 2 usa os pedidos novos",
    "tc_abd_c": "o cenário 2 limita à fila de hoje e aos pedidos novos",
    "tc_tor_c": "a v26 tinha 3.104; a fila de 12 meses tem 2.510",
    "coron": "fora no cenário 2 (decisão de 02/11)",
    "emerg": "fora no cenário 2 (D-009)",
}
linhas_pe = [(ch, ex) for ch, ex, *_ in LINHAS] + [("coron", "Angiotomografia de coronárias"),
                                                   ("emerg", "TC de tórax sem contraste, emergência")]
EXTRA = {"coron": "Angiotomografia de coronárias (código da TC de tórax)",
         "emerg": "TC de tórax sem contraste, emergência"}
r = 4
p6 = r + 1
for ch, ex in linhas_pe:
    r += 1
    rv = [R1[k] for k, v in V26CH.items() if v == ch]
    if ch in EXTRA:
        rv = [R1[EXTRA[ch]]]
    def soma1(col_v26, col_sob):
        partes = [f"'2 Cenário 1'!{col_v26}{x}" for x in rv]
        if ch in R1s:
            partes.append(f"'2 Cenário 1'!{col_sob}{R1s[ch]}")
        return "=" + ("+".join(partes) if partes else "0")
    put(pe, f"A{r}", ex, font=FB)
    lk(pe, f"B{r}", soma1("C", "J"), INT)
    lk(pe, f"C{r}", f"='3 Cenário 2'!E{R2[ch]}" if ch in R2 else "=0", INT)
    put(pe, f"D{r}", f"=C{r}-B{r}", '+#,##0;-#,##0;0', FB)
    lk(pe, f"E{r}", soma1("G", "G"), BRL0)
    lk(pe, f"F{r}", f"='3 Cenário 2'!H{R2[ch]}" if ch in R2 else "=0", BRL0)
    put(pe, f"G{r}", f"=F{r}-E{r}", '+"R$" #,##0;-"R$" #,##0;0', FB)
    lk(pe, f"H{r}", soma1("H", "H"), BRL0)
    lk(pe, f"I{r}", f"='3 Cenário 2'!I{R2[ch]}" if ch in R2 else "=0", BRL0)
    put(pe, f"J{r}", f"=I{r}-H{r}", '+"R$" #,##0;-"R$" #,##0;0', FB)
    porque = POR_QUE.get(ch)
    if not porque and not rv and ch not in R1s:
        porque = "não está na v26: entra só no cenário 2"
    put(pe, f"K{r}", porque, font=FS)
u6 = r
r += 1
put(pe, f"A{r}", "Total", font=FB, fill=TOT)
for col in "BCDEFGHIJ":
    fmt = INT if col in "BCD" else BRL0
    put(pe, f"{col}{r}", f"=SUM({col}{p6}:{col}{u6})", fmt, FB, TOT)
put(pe, f"K{r}", None, fill=TOT)
for col in "DGJ":
    pe.conditional_formatting.add(f"{col}{p6}:{col}{u6}", CellIsRule(operator="lessThan", formula=["0"], fill=VERM))
    pe.conditional_formatting.add(f"{col}{p6}:{col}{u6}", CellIsRule(operator="greaterThan", formula=["0"],
                                                                      fill=VERDE))
nota(pe, r + 2, "Verde: o cenário 2 tem mais; vermelho: tem menos. O total de exames muda, mas o valor fica quase igual: "
                "a troca é entre exames de preços diferentes.")

# ---------------------------------------------------------------- Leia
for i, (t, fnt) in enumerate([
    ("Readequação do plano 4 à Candanga: dois cenários", FT),
    ("Estudo interno de 09/11/2026, a pedido do usuário. Controle interno: a margem não vai ao plano.", FS),
    ("", FN),
    ("Premissas: os custos, o valor dos exames, as salas e os tomógrafos. Amarelo pode mudar.", FN),
    ("1 Margem por exame: o que cada exame paga, o que custa, a margem por exame, por hora e em % do preço, a "
     "complexidade e a fila de hoje e de 12 meses.", FN),
    ("2 Cenário 1: as metas da v26 pela Candanga, e a sobra de cerca de R$ 245 mil nos códigos que ainda têm fila.", FN),
    ("3 Cenário 2: as filas escolhidas de novo, pela margem e pela complexidade, até o valor dos exames.", FN),
    ("4 Comparação: os dois cenários e a carteira 1 em vigor.", FN),
    ("5 Contraste: os dois cenários com 100%, 90%, 80%, 70%, 60% e 50% dos pedidos com contraste feitos com contraste.",
     FN),
    ("6 Exame a exame: o cenário 2 no formato do cenário 1, com a diferença de exames, de valor e de margem de cada "
     "exame.", FN),
    ("", FN),
    ("O resumo e a recomendação estão em estudo_readequacao_candanga_margem_20261109.md. Gerado por "
     "gerar_readequacao_candanga_margem_20261109.py.", FS),
]):
    put(leia, f"A{i + 1}", t, font=fnt, borda=False)

wb.save(SAIDA)
print(SAIDA)
print("cenário 1:", [(x[0], x[4]) for x in e1])
print("cenário 2:", {k: v for k, v in e2.items()})
print("carteira 1:", {k: round(v) for k, v in cart.items()})
for l in LINHAS:
    print(l[0], round(margem(l[0]), 2), f"{margem(l[0]) / l[4]:.1%}", "novos", novos(l[0], l[7]))
