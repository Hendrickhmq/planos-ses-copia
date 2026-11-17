"""Estudo interno do plano 4 (07/11/2026): o que muda, em custo e no plano, se a execução passar a 12 meses, com 6 polos
de ultrassom e a tomografia em 3 polos (pedido da equipe, trazido pelo usuário).

Base: a carteira 1 escolhida em 02/11 (sem a transfontanela, 03/11), pela Candanga, em
estudo_filas_imagem_20261102.json — 79.533 exames, 20 salas e 5 tomógrafos em 8 meses. O quadro de gestão é o da
v26 assinada (D-007, R$ 119.520 por mês). Os custos de execução são os da planilha de custo v2 (20/10) e da pesquisa
de 05/11 (estudo_v26_salas_precos_custos), em amarelo para mudar.

Tudo na planilha é fórmula sobre as células amarelas. Recalcular depois de gerar:
python3.11 <skill xlsx>/scripts/recalc.py estudo_12_meses_3_tomografos_20261107.xlsx
"""
import json
import os
import re

from openpyxl import Workbook
from openpyxl.comments import Comment
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter as L
from openpyxl.worksheet.datavalidation import DataValidation

AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(AQUI, "estudo_12_meses_3_tomografos_20261107.xlsx")
EST = json.load(open(os.path.join(AQUI, "estudo_filas_imagem_20261102.json"), encoding="utf-8"))

# ------------------------------------------------------------------ carteira 1 (base)
CHAVE = next(k for k in EST["cenarios"] if k.startswith("1 "))
CART = EST["cenarios"][CHAVE]
US = [i for i in CART if i["modalidade"] == "Ultrassom"]
TC = [i for i in CART if i["modalidade"] == "Tomografia"]
SEM = re.compile(r"S/\s*CONTR")
EX_US = sum(i["meta"] for i in US)
EX_TC_SEM = sum(i["meta"] for i in TC if SEM.search(i["nome"]))
EX_TC_COM = sum(i["meta"] for i in TC) - EX_TC_SEM
V_US = round(sum(i["valor"] for i in US), 2)
V_TC = round(sum(i["valor"] for i in TC), 2)
INCERTOS = [i for i in CART if "esperados" in i["nome"] or "encaminhados" in i["nome"]]
EX_INC, V_INC = sum(i["meta"] for i in INCERTOS), round(sum(i["valor"] for i in INCERTOS), 2)
CAP = EST["revisao"]["capacidade"]
POLOS = ["Oeste", "Sudoeste", "Norte", "Leste", "Central e Centro-Sul", "Sul"]
assert EX_US == sum(CAP["exames_us"].values()) and EX_TC_COM + EX_TC_SEM == sum(CAP["exames_tc"].values())

# ------------------------------------------------------------------ estilo (o mesmo dos estudos de 02/11 e 05/11)
A = "Arial"
F_N = Font(name=A, size=10)
F_B = Font(name=A, size=10, bold=True)
F_T = Font(name=A, size=14, bold=True, color="1F3864")
F_S = Font(name=A, size=11, bold=True, color="1F3864")
F_I = Font(name=A, size=9, italic=True, color="555555")
F_IN = Font(name=A, size=10, color="0000FF")
F_LK = Font(name=A, size=10, color="008000")
F_G = Font(name=A, size=11, bold=True)
AMARELO = PatternFill("solid", fgColor="FFF2CC")
CAB = PatternFill("solid", fgColor="D9E1F2")
TOT = PatternFill("solid", fgColor="EDEDED")
AZUL = PatternFill("solid", fgColor="DDEBF7")
VERDE = PatternFill("solid", fgColor="E2EFDA")
VERM = PatternFill("solid", fgColor="F8CBAD")
FINA = Side(style="thin", color="BFBFBF")
BORDA = Border(left=FINA, right=FINA, top=FINA, bottom=FINA)
WRAP = Alignment(wrap_text=True, vertical="top")
CEN = Alignment(horizontal="center", vertical="center", wrap_text=True)
MOEDA = '"R$" #,##0.00;-"R$" #,##0.00;"-"'
MOEDA0 = '"R$" #,##0;-"R$" #,##0;"-"'
INT = '#,##0;-#,##0;"-"'
DEC1 = '#,##0.0'
DEC2 = '#,##0.00'
PCT = '0.0%'

wb = Workbook()
wb.remove(wb.active)


def aba(nome, larguras):
    ws = wb.create_sheet(nome)
    for i, w in enumerate(larguras, 1):
        ws.column_dimensions[L(i)].width = w
    ws.sheet_view.showGridLines = False
    return ws


def put(ws, cel, v, fmt=None, font=None, fill=None, borda=True, al=None):
    c = ws[cel]
    c.value = v
    c.font = font or F_N
    if fmt:
        c.number_format = fmt
    if fill:
        c.fill = fill
    if borda:
        c.border = BORDA
    if al:
        c.alignment = al
    return c


def entrada(ws, cel, v, fmt=None, nota=None):
    c = put(ws, cel, v, fmt, F_IN, AMARELO)
    if nota:
        c.comment = Comment(nota, "estudo 07/11")
    return c


def titulo(ws, t, sub, ate="J"):
    put(ws, "A1", t, font=F_T, borda=False)
    put(ws, "A2", sub, font=F_I, borda=False, al=WRAP)
    ws.merge_cells(f"A2:{ate}2")
    ws.row_dimensions[2].height = 44


def secao(ws, r, t):
    put(ws, f"A{r}", t, font=F_S, borda=False)


def cab(ws, r, nomes, c0=1, h=40):
    for i, n in enumerate(nomes):
        put(ws, f"{L(c0 + i)}{r}", n, font=F_B, fill=CAB, al=CEN)
    ws.row_dimensions[r].height = h


def nota(ws, r, t, ate="J", h=None):
    put(ws, f"A{r}", t, font=F_I, borda=False, al=WRAP)
    ws.merge_cells(f"A{r}:{ate}{r}")
    ws.row_dimensions[r].height = h or max(15, 13 * (len(t) // 140 + 1))


def R(ws_nome, cel):
    col = "".join(ch for ch in cel if ch.isalpha())
    lin = "".join(ch for ch in cel if ch.isdigit())
    return f"'{ws_nome}'!${col}${lin}"


# ================================================================== Premissas
N_PR = "Premissas"
pr = aba(N_PR, [64, 18, 18, 90])
titulo(pr, "Premissas", "Amarelo = premissa: mude e as outras abas se refazem. Azul = número que veio de fonte ou do "
       "usuário; o comentário da célula diz de onde. Coluna B: hoje (carteira 1, 8 meses, 5 tomógrafos). Coluna C: a "
       "proposta da equipe (12 meses, 6 polos de ultrassom, 3 de tomografia).", "D")
P = {}  # nome -> referência absoluta
r = 4
secao(pr, r, "O que muda entre os dois arranjos")
r += 1
cab(pr, r, ["Premissa", "Hoje", "Proposta", "De onde vem"], h=24)
DUAS = [
    ("meses", "Meses de execução", 8, 12, INT, "hoje: v26 e carteira 1; proposta: pedido da equipe (07/11/2026)"),
    ("polos_us", "Polos de ultrassom", 6, 6, INT, "v26, 4.2; a proposta mantém os 6"),
    ("tomografos", "Tomógrafos (um por polo com tomografia)", 5, 3, INT,
     "hoje: 5, decisão do usuário de 02/11 (a v26 assinada tem 6); proposta: 3 polos de tomografia"),
    ("database", "Mês da vigência em que cai a data-base dos salários", 7, 7, INT,
     "premissa — a confirmar: depende do mês de início e da convenção coletiva de cada cargo"),
]
for k, rot, a, b, fmt, fonte in DUAS:
    r += 1
    put(pr, f"A{r}", rot)
    entrada(pr, f"B{r}", a, fmt)
    entrada(pr, f"C{r}", b, fmt)
    put(pr, f"D{r}", fonte, font=F_I, al=WRAP)
    P[k + "_h"], P[k + "_p"] = R(N_PR, f"B{r}"), R(N_PR, f"C{r}")
r += 2
secao(pr, r, "Valem para os dois arranjos")
r += 1
cab(pr, r, ["Premissa", "Valor", "", "De onde vem"], h=24)
UMA = [
    ("Funcionamento", None),
    ("dias", "Dias úteis por mês", 21, INT, "v26, 7.3: 8 meses de 21 dias úteis, de segunda a sexta-feira"),
    ("horas_dia", "Horas de funcionamento por dia útil (sala e tomógrafo)", 10, INT, "v26, 7.3"),
    ("ocupacao", "Parte das horas com exame (o resto absorve atraso, encaixe e manutenção)", 0.8, PCT,
     "estudo das filas de 02/11: 8 h de exame em 10 h abertas"),
    ("falta", "Faltas que deixam a vaga parada (sem reposição)", 0.0, PCT,
     "controle interno, fora do plano (absenteísmo é tratamento interno): 0% = toda falta reposta"),
    ("Tomografia: tempo e contraste", None),
    ("min_com", "Minutos de tomógrafo por exame com contraste", 20, DEC1,
     "v26 e estudo de 02/11: 20 min. A RSNA 2005 mediu 17 min na sala; com fases tardias, mais. É o ponto que a "
     "clínica levantou: confirmar por escrito"),
    ("min_sem", "Minutos de tomógrafo por exame sem contraste", 15, DEC1, "v26: 15 min (RSNA 2005 mediu 8,6 min)"),
    ("horas_tc", "Horas por dia útil em que o tomógrafo atende o plano", 10, DEC1,
     "v26, 7.3: 10 h. Se a clínica abrir 12 h, ponha 12"),
    ("dias_tc", "Dias por mês em que o tomógrafo atende o plano", 21, INT,
     "21 = dias úteis. Com sábados, cerca de 25"),
    ("janela", "Horas por dia em que a clínica faz exame com contraste", 10, DEC1,
     "10 = o dia inteiro. Se o contraste só correr com médico presente ou com jejum de manhã, ponha as horas da janela"),
    ("Tomografia: conversão e fluxo em linha", None),
    ("conv", "Parte dos pedidos com contraste que o radiologista faz sem contraste", 0.10, PCT,
     "hipótese do estudo, a medir no mês 1: o radiologista readequa o protocolo (v26, 4.8). O código SUS é o mesmo com "
     "ou sem contraste e paga o mesmo"),
    ("min_linha_com", "Minutos de tomógrafo por exame com contraste, com o acesso venoso feito fora da sala", 13, DEC1,
     "hipótese a medir no mês 1: 8,6 min do exame sem contraste (RSNA 2005) + cerca de 4 min de conexão à bomba, "
     "injeção e fases"),
    ("min_linha_sem", "Minutos de tomógrafo por exame sem contraste, com o paciente já pronto", 10, DEC1,
     "RSNA 2005: 8,6 min na sala, arredondado para 10"),
    ("Fluxo: tempos fora da sala (premissas a medir no mês 1)", None),
    ("t_recep", "Recepção pela secretaria: identificação, documentos, CPF e conferência do preparo (min)", 5, DEC1,
     "premissa"),
    ("t_grupo", "Orientação em grupo sobre o contraste (min por grupo)", 5, DEC1, "premissa"),
    ("n_grupo", "Pacientes por grupo de orientação", 4, INT, "premissa"),
    ("t_triagem", "Triagem individual: alergia, doença renal, metformina, gestação e termo (min)", 5, DEC1,
     "v26, 4.8: a creatinina só é exigida de quem tem doença renal, e é consultada no TrakCare"),
    ("t_troca", "Troca de roupa e retirada de metais, no vestiário (min)", 3, DEC1, "premissa"),
    ("t_puncao", "Punção venosa na sala de preparo: cateter, teste com soro e curativo (min de enfermagem)", 8, DEC1,
     "premissa"),
    ("pulmao", "Pacientes prontos, com acesso, à espera do tomógrafo", 2, INT,
     "premissa: dois bastam para o tomógrafo não esperar; mais que isso deixa paciente com acesso parado se o "
     "equipamento parar"),
    ("t_repouso", "Repouso observado depois do contraste, fora da sala (min)", 15, DEC1,
     "v26, 4.8: não há tempo mínimo, o usuário sai quando se sentir em condições; 15 min é premissa de planejamento"),
    ("t_alta", "Retirada do acesso, orientação da metformina e alta (min de enfermagem)", 3, DEC1, "premissa"),
    ("troca_us", "Ultrassom: minutos entre um paciente e o próximo, com o próximo já pronto", 2, DEC1,
     "premissa: com vestiário, bexiga cheia na espera e chamada antecipada, a sala só perde a entrada e a saída"),
    ("A carteira (carteira 1, escolhida em 02/11; sem a transfontanela, 03/11)", None),
    ("ex_us", "Exames de ultrassom", EX_US, INT, "estudo_filas_imagem_20261102.json, carteira 1"),
    ("ex_tc_com", "Exames de tomografia com contraste (inclui as angiotomografias)", EX_TC_COM, INT,
     "carteira 1: toda fila de TC sem \"S/CONTRASTE\" no nome"),
    ("ex_tc_sem", "Exames de tomografia sem contraste", EX_TC_SEM, INT, "carteira 1: abdômen, pelve, tórax e crânio"),
    ("v_us", "Valor do ultrassom da carteira 1 (R$)", V_US, MOEDA, "carteira 1, pela Tabela SUS Candanga"),
    ("v_tc", "Valor da tomografia da carteira 1 (R$)", V_TC, MOEDA, "carteira 1, pela Tabela SUS Candanga"),
    ("ex_inc", "Exames das linhas de pedidos novos e encaminhados da carteira 1", EX_INC, INT,
     "as linhas \"pedidos novos esperados\" e \"encaminhados pela SES\" (em 8 meses)"),
    ("v_inc", "Valor dessas linhas (R$)", V_INC, MOEDA, "idem"),
    ("O convênio", None),
    ("global", "Valor global do convênio (R$)", 11592762.00, MOEDA, "Emenda 202571080005, Ofício 40/2026"),
    ("teto", "Teto interno do apoio (parte do valor global)", 0.085, PCT,
     "D-005 (20/10/2026), faixa de 8% a 8,5% da LI-038; decisão interna, não vai ao plano"),
    ("reajuste", "Reajuste da data-base sobre os salários", 0.05, PCT,
     "premissa — a confirmar na convenção coletiva de cada cargo"),
    ("Execução: ultrassom feito por nós (dentro do valor do exame)", None),
    ("sala", "Aluguel de uma sala por mês (R$)", 3000.00, MOEDA,
     "rede do ISHP: R$ 6.000 por polo com 2 salas (custo v2, 20/10/2026)"),
    ("aparelho", "Aluguel de um aparelho de ultrassom por mês, com manutenção (R$)", 2500.00, MOEDA,
     "opção mapeada em Samambaia (custo v2, 20/10/2026)"),
    ("parte_ap", "Parte das salas com aparelho alugado", 1.0, PCT, "100% = alugamos o aparelho de toda sala"),
    ("fixos_sala", "Outros custos fixos da sala por mês: internet, água, telefone, limpeza (R$)", 400.00, MOEDA,
     "pesquisa de 05/11 — premissa, a confirmar se já vêm no aluguel"),
    ("energia", "Energia da sala de ultrassom por hora de exame (R$)", 1.50, MOEDA, "pesquisa de 05/11 — premissa"),
    ("n_recep", "Recepcionistas por polo", 2, INT, "v26, 4.15: polo aberto 50 h por semana ÷ 44 h"),
    ("recep", "Custo de um recepcionista por mês, com encargos (R$)", 2959.00, MOEDA,
     "salario.com.br, recepcionista de consultório, Brasília (custo v2)"),
    ("rt", "Responsável técnico médico do polo, por mês (R$)", 0.00, MOEDA,
     "SEM PREÇO — a preencher (v26, 4.15: um por polo)"),
    ("retaguarda", "Médico de retaguarda presencial, por dia útil e polo (R$)", 0.00, MOEDA,
     "SEM PREÇO — a preencher (v26, 4.15: um por dia útil em cada polo). Se for pago por plantão, é o item que "
     "mais sobe com 12 meses"),
    ("outros_polo", "Outros custos de cada polo por mês: contabilidade, sistema, seguro, licença (R$)", 0.00, MOEDA,
     "SEM PREÇO — a preencher"),
    ("medico_us", "Médico de ultrassom, por exame (R$)", 33.33, MOEDA,
     "modelo do ISHP: R$ 1.000 por lote de 30 exames (custo v2)"),
    ("insumo_us", "Insumos do ultrassom, por exame (R$)", 3.00, MOEDA, "hipótese do custo v2"),
    ("pacs", "Sistema de imagem (RIS/PACS), por exame de ultrassom (R$)", 2.00, MOEDA, "pesquisa de 05/11 — premissa"),
    ("Execução: tomografia na clínica parceira (por exame)", None),
    ("tc_hoje", "Preço da tomografia na clínica, hoje, com contraste incluído (R$)", 171.44, MOEDA,
     "custo v2: média da rede de TC do ISHP, R$ 165 a R$ 175"),
    ("tc_prop", "Preço da tomografia com 3 polos, negociado por volume (R$)", 171.44, MOEDA,
     "A NEGOCIAR — mude quando a clínica responder"),
    ("contraste", "Contraste cobrado à parte, por exame com contraste (R$)", 0.00, MOEDA,
     "0 = incluído no preço. Se a clínica cobrar à parte, o custo v2 estimou cerca de R$ 57"),
]
for item in UMA:
    r += 1
    if item[1] is None:
        secao(pr, r, item[0])
        continue
    k, rot, v, fmt, fonte = item
    put(pr, f"A{r}", rot)
    entrada(pr, f"B{r}", v, fmt)
    put(pr, f"D{r}", fonte, font=F_I, al=WRAP)
    P[k] = R(N_PR, f"B{r}")
    if "SEM PREÇO" in fonte or "A NEGOCIAR" in fonte:
        pr[f"D{r}"].font = Font(name=A, size=9, italic=True, color="C00000")
r += 2
secao(pr, r, "Contas que as outras abas usam")
r += 1
CALC = [
    ("ex_tc", "Exames de tomografia", f"={P['ex_tc_com']}+{P['ex_tc_sem']}", INT),
    ("tc_com_ef", "Exames de tomografia com contraste, depois da conversão", f"={P['ex_tc_com']}*(1-{P['conv']})", INT),
    ("tc_sem_ef", "Exames de tomografia sem contraste, depois da conversão",
     f"={P['ex_tc_sem']}+{P['ex_tc_com']}*{P['conv']}", INT),
    ("ex_tot", "Exames da carteira 1", f"={P['ex_us']}+{P['ex_tc_com']}+{P['ex_tc_sem']}", INT),
    ("v_ex", "Valor dos exames da carteira 1 (R$)", f"={P['v_us']}+{P['v_tc']}", MOEDA),
    ("med_tot", "Valor médio por exame (R$)", f"=({P['v_us']}+{P['v_tc']})/({P['ex_us']}+{P['ex_tc_com']}+{P['ex_tc_sem']})",
     MOEDA),
    ("med_us", "Valor médio do ultrassom (R$)", f"={P['v_us']}/{P['ex_us']}", MOEDA),
    ("med_tc", "Valor médio da tomografia (R$)", f"={P['v_tc']}/({P['ex_tc_com']}+{P['ex_tc_sem']})", MOEDA),
    ("dias_h", "Dias úteis no período, hoje", f"={P['dias']}*{P['meses_h']}", INT),
    ("dias_p", "Dias úteis no período, proposta", f"={P['dias']}*{P['meses_p']}", INT),
    ("cap_h", "Horas de exame de uma sala ou um tomógrafo no período, hoje",
     f"={P['horas_dia']}*{P['ocupacao']}*{P['dias']}*{P['meses_h']}", INT),
    ("cap_p", "Horas de exame de uma sala no período, proposta",
     f"={P['horas_dia']}*{P['ocupacao']}*{P['dias']}*{P['meses_p']}", INT),
    ("cap_tc_p", "Horas de exame de um tomógrafo no período, proposta",
     f"={P['horas_tc']}*{P['ocupacao']}*{P['dias_tc']}*{P['meses_p']}", INT),
    ("dias_tc_p", "Dias de tomógrafo no período, proposta", f"={P['dias_tc']}*{P['meses_p']}", INT),
]
for k, rot, f, fmt in CALC:
    r += 1
    put(pr, f"A{r}", rot)
    put(pr, f"B{r}", f, fmt)
    P[k] = R(N_PR, f"B{r}")
pr.freeze_panes = "B6"

# ================================================================== Gestão (o apoio do convênio)
N_GE = "Gestão"
ge = aba(N_GE, [46, 11, 11, 11, 36] + [7, 11, 13] * 5)
titulo(ge, "Equipe de gestão e apoio em 12 meses: readequar para caber no teto", "O valor global não muda: todo real a "
       "mais no apoio sai dos exames. Regra do usuário (07/11): o apoio em 12 meses fica no valor de hoje, ou sobe "
       "pouco, até 8,5% do global. Preços = custo total por mês, com encargos. Amarelo: quantidades e preços para "
       "testar. Laranja: preço abaixo do custo de mercado no DF.", "T")
LARANJA = PatternFill("solid", fgColor="FCE4D6")
CARGOS = [  # cargo, preço hoje, mercado DF, menor aprovado, origem, qtd (hoje, A, P1, P2, P3), preço P2, preço P3
    ("Direção Executiva de Projeto", 14500, 25965, 10200,
     "pt_ses_02 — Convênio 030975/2026, IEV, Direção Executiva (16 meses)", [1, 1, 1, 1, 1], 10200, None),
    ("Coordenação Assistencial", 10500, 12412, 6000,
     "pt_ses_02 e 04 — Convênios 030975 e 030977/2026, IEV: coordenações a R$ 6.000", [1, 1, 1, 1, 1], 8400, None),
    ("Coordenação Administrativa e Financeira", 8400, 8371, 6000,
     "pt_ses_02 — Convênio 030975/2026, IEV, Coordenação Administrativa-Financeira", [1, 1, 1, 1, 1], 8400, None),
    ("Supervisão de Polo Assistencial", 6155, 6733, 6155,
     "pt_ses_01 — Convênio 030989/2026, ISHP (o único aprovado; 2 para 4 polos)", [3, 3, 3, 2, 2], 6155, None),
    ("Operador de registro — pré-exame: agenda, contato, confirmação e busca ativa", 4300, 3156, 3200,
     "pt_ses_02, 03 e 04 — IEV, Assistente Administrativo: o preço da função de contato (estudo de 20/10)",
     [5, 5, 5, 4, 3], 3200, None),
    ("Operador de registro — pós-exame: TrakCare e APAC", 4300, 3752, 4300,
     "pt_ses_02 e 04 — Convênios 030975 e 030977/2026, IEV, Operador de registro de sistemas", [5, 5, 5, 3, 2], 4300,
     None),
    ("Assistente Administrativo: documentação do atendimento e da prestação de contas", 3200, 5068, 3200,
     "pt_ses_02, 03 e 04 — Convênios 030975, 030976 e 030977/2026, IEV", [6, 6, 6, 4, 3], 3200, None),
    ("Assessoria de Prestação de Contas (serviço de pessoa jurídica)", 5455, None, 3700,
     "pt_ses_05 — Convênio 031061/2026, ISHP (leitura por OCR)", [1, 1, 1, 1, 1], 3700, 3700),
]
CEN_GE = [("hoje", "Hoje: v26, 8 meses", "h"), ("A", "A. 12 meses sem readequar", "p"),
          ("P1", "P1. 12 meses: o mesmo quadro, salários cortados por igual até 8,5%", "p"),
          ("P2", "P2. 12 meses: quadro pelo volume e preços dos aprovados (recomendada)", "p"),
          ("P3", "P3. 12 meses: salários de hoje, menos postos", "p")]
GC = {k: (L(6 + 3 * j), L(7 + 3 * j), L(8 + 3 * j)) for j, (k, _n, _m) in enumerate(CEN_GE)}
put(ge, "A4", "Cenário", font=F_B, fill=CAB)
for c_ in "BCDE":
    put(ge, f"{c_}4", "", fill=CAB)
put(ge, "A5", "Meses", font=F_B)
for c_ in "BCDE":
    put(ge, f"{c_}5", "")
for k, nome, hp in CEN_GE:
    q, p_, t_ = GC[k]
    put(ge, f"{q}4", nome, font=F_B, fill=CAB, al=CEN)
    ge.merge_cells(f"{q}4:{t_}4")
    put(ge, f"{q}5", f"={P['meses_' + hp]}", INT, F_LK, al=CEN)
    ge.merge_cells(f"{q}5:{t_}5")
ge.row_dimensions[4].height = 58
cab(ge, 6, ["Cargo", "Preço de hoje (v26)", "Custo de mercado no DF", "Menor preço aprovado",
            "Origem do menor preço aprovado"] + ["Qtd.", "Preço por mês", "No período"] * 5, h=44)
L0 = 7
LF = L0 + len(CARGOS) - 1
LCLT = LF - 1
FATOR = f"$B${LF + 2}"
for i, (cargo, hoje, merc, menor, origem, qtds, p2, p3) in enumerate(CARGOS):
    l = L0 + i
    put(ge, f"A{l}", cargo, al=WRAP)
    entrada(ge, f"B{l}", hoje, MOEDA0, "v26, 8.2 (D-005 e D-007)")
    if merc is None:
        put(ge, f"C{l}", "não se compara", font=F_I, al=CEN)
    else:
        entrada(ge, f"C{l}", merc, MOEDA0, "salario.com.br, custo para a empresa em Brasília (20/10/2026); "
                "dados/quadro_gestao_cenarios_e_precificacao_20261020.xlsx, aba Mercado e aprovados")
    entrada(ge, f"D{l}", menor, MOEDA0, "biblioteca/precos/cargos_no_acervo.md")
    put(ge, f"E{l}", origem, font=F_I, al=WRAP)
    for j, (k, _n, _m) in enumerate(CEN_GE):
        q, p_, t_ = GC[k]
        entrada(ge, f"{q}{l}", qtds[j], INT)
        if k in ("hoje", "A"):
            put(ge, f"{p_}{l}", f"=$B{l}", MOEDA0)
        elif k == "P1":
            put(ge, f"{p_}{l}", f"=ROUND($B{l}*{FATOR},2)", MOEDA0)
        elif k == "P2":
            entrada(ge, f"{p_}{l}", p2, MOEDA0)
        else:
            if p3 is None:
                put(ge, f"{p_}{l}", f"=$B{l}", MOEDA0)
            else:
                entrada(ge, f"{p_}{l}", p3, MOEDA0)
        put(ge, f"{t_}{l}", f"={q}{l}*{p_}{l}*{q}$5", MOEDA0)
    ge.row_dimensions[l].height = 40
qh, ph, th = GC["hoje"]
put(ge, f"A{LF + 2}", "P1: fator do corte igual (o teto de 8,5% ÷ 12 meses ÷ o custo por mês de hoje)", font=F_B,
    al=WRAP)
put(ge, f"B{LF + 2}", f"={P['teto']}*{P['global']}/({P['meses_p']}*SUMPRODUCT({qh}{L0}:{qh}{LF},$B${L0}:$B${LF}))",
    '0.0000', F_B)
ge.row_dimensions[LF + 2].height = 28
R0G = LF + 4
LINHAS_GE = [
    ("Postos (sem a assessoria)", "q", lambda q, p_, t_: f"=SUM({q}{L0}:{q}{LCLT})", INT),
    ("Custo por mês (R$)", "t", lambda q, p_, t_: f"=SUMPRODUCT({q}{L0}:{q}{LF},{p_}{L0}:{p_}{LF})", MOEDA0),
    ("Apoio no período (R$)", "t", lambda q, p_, t_: f"=SUM({t_}{L0}:{t_}{LF})", MOEDA0),
    ("Parte do valor global", "t", lambda q, p_, t_: f"={t_}{R0G + 2}/{P['global']}", '0.00%'),
    ("Cabe no teto interno (8,5%)?", "t",
     lambda q, p_, t_: f'=IF({t_}{R0G + 3}<={P["teto"]}+0.00001,"sim","não")', None),
    ("Diferença para o apoio de hoje (R$)", "t", lambda q, p_, t_: f"={t_}{R0G + 2}-${th}${R0G + 2}",
     '+"R$" #,##0;-"R$" #,##0;"-"'),
    ("Diferença para o apoio de hoje (%)", "t", lambda q, p_, t_: f"={t_}{R0G + 2}/${th}${R0G + 2}-1",
     '+0.0%;-0.0%;"0"'),
    ("Custo por mês contra hoje (%)", "t", lambda q, p_, t_: f"={t_}{R0G + 1}/${th}${R0G + 1}-1", '+0.0%;-0.0%;"0"'),
    ("Sobra para os exames (R$)", "t", lambda q, p_, t_: f"={P['global']}-{t_}{R0G + 2}", MOEDA0),
    ("Diferença para o valor dos exames da carteira 1 (R$)", "t",
     lambda q, p_, t_: f"={t_}{R0G + 8}-{P['v_ex']}", '+"R$" #,##0;-"R$" #,##0;"-"'),
    ("Exames a mais (+) ou a menos (−), no valor médio", "t",
     lambda q, p_, t_: f"=ROUNDDOWN({t_}{R0G + 9}/{P['med_tot']},0)", '+#,##0;-#,##0;"0"'),
    ("Exames por operador de registro por mês (carga)", "t",
     lambda q, p_, t_: f"=ROUND({P['ex_tot']}/(({q}{L0 + 4}+{q}{L0 + 5})*{q}$5),0)", INT),
    ("Cargos abaixo do custo de mercado no DF", "t",
     lambda q, p_, t_: f"=SUMPRODUCT(({q}{L0}:{q}{LCLT}>0)*({p_}{L0}:{p_}{LCLT}<$C${L0}:$C${LCLT}))", INT),
    ("Cargos abaixo do menor preço aprovado", "t",
     lambda q, p_, t_: f"=SUMPRODUCT(({q}{L0}:{q}{LF}>0)*({p_}{L0}:{p_}{LF}<$D${L0}:$D${LF}-0.005))", INT),
    ("Reajuste da data-base no período, fora do convênio (R$)", "t", None, MOEDA0),
]
G_ROW = {}
for i, (rot, onde, fn, fmt) in enumerate(LINHAS_GE):
    l = R0G + i
    G_ROW[rot] = l
    put(ge, f"A{l}", rot, font=F_B, fill=TOT, al=WRAP)
    for c_ in "BCDE":
        put(ge, f"{c_}{l}", "", fill=TOT)
    ge.merge_cells(f"A{l}:E{l}")
    for k, _n, hp in CEN_GE:
        q, p_, t_ = GC[k]
        if fn is None:
            f = (f"=SUMPRODUCT({q}{L0}:{q}{LCLT},{p_}{L0}:{p_}{LCLT})*{P['reajuste']}"
                 f"*MAX(0,{q}$5-{P['database_' + hp]}+1)")
        else:
            f = fn(q, p_, t_)
        alvo = q if onde == "q" else t_
        put(ge, f"{alvo}{l}", f, fmt, F_B, TOT, al=CEN if fmt is None else None)
        for c_ in (q, p_, t_):
            if c_ != alvo:
                put(ge, f"{c_}{l}", "", fill=TOT)
    ge.row_dimensions[l].height = 24
RTETO = G_ROW["Cabe no teto interno (8,5%)?"]
ge.conditional_formatting.add(f"F{RTETO}:T{RTETO}", CellIsRule(operator="equal", formula=['"não"'], fill=VERM))
ge.conditional_formatting.add(f"F{RTETO}:T{RTETO}", CellIsRule(operator="equal", formula=['"sim"'], fill=VERDE))
faixas = " ".join(f"{GC[k][1]}{L0}:{GC[k][1]}{LCLT}" for k, _n, _m in CEN_GE)
ge.conditional_formatting.add(faixas, CellIsRule(operator="lessThan", formula=[f"$C{L0}"], fill=LARANJA))

# a resposta em porcentagem
r = R0G + len(LINHAS_GE) + 1
secao(ge, r, "Os 4 meses a mais, em porcentagem")
r += 1
cab(ge, r, ["", "Valor", "%", "", "Como ler"], h=22)
qa, pa, ta = GC["A"]
q2, p2_, t2 = GC["P2"]
RESP = [
    ("Meses a mais", f"={P['meses_p']}-{P['meses_h']}", INT, f"={P['meses_p']}/{P['meses_h']}-1",
     "a vigência fica 50% mais longa"),
    ("Apoio de hoje, 8 meses (R$)", f"={th}{G_ROW['Apoio no período (R$)']}", MOEDA0,
     f"={th}{G_ROW['Parte do valor global']}", "% do valor global"),
    ("O mesmo quadro e os mesmos salários por 12 meses (R$)", f"={ta}{G_ROW['Apoio no período (R$)']}", MOEDA0,
     f"={ta}{G_ROW['Diferença para o apoio de hoje (%)']}", "a mais sobre o apoio de hoje, se nada for readequado"),
    ("Custo por mês de hoje (R$)", f"={th}{G_ROW['Custo por mês (R$)']}", MOEDA0, None, ""),
    ("Custo por mês que mantém o apoio de hoje em 12 meses (R$)",
     f"={th}{G_ROW['Apoio no período (R$)']}/{P['meses_p']}", MOEDA0,
     f"=1-({th}{G_ROW['Apoio no período (R$)']}/{P['meses_p']})/{th}{G_ROW['Custo por mês (R$)']}",
     "quanto o custo por mês precisa cair para o apoio ficar igual ao de hoje"),
    ("Custo por mês no teto de 8,5%, em 12 meses (R$)", f"={P['teto']}*{P['global']}/{P['meses_p']}", MOEDA0,
     f"=1-({P['teto']}*{P['global']}/{P['meses_p']})/{th}{G_ROW['Custo por mês (R$)']}",
     "quanto o custo por mês precisa cair para caber no teto"),
    ("O teto permite a mais sobre o apoio de hoje (R$)",
     f"={P['teto']}*{P['global']}-{th}{G_ROW['Apoio no período (R$)']}", MOEDA0,
     f"=({P['teto']}*{P['global']})/{th}{G_ROW['Apoio no período (R$)']}-1", "a folga até 8,5%"),
    ("P2: o custo por mês cai (R$ e %)", f"={t2}{G_ROW['Custo por mês (R$)']}", MOEDA0,
     f"={t2}{G_ROW['Custo por mês contra hoje (%)']}", "contra o custo por mês de hoje"),
    ("… por ter menos postos (o quadro da P2 com os preços de hoje)",
     f"=SUMPRODUCT({q2}{L0}:{q2}{LF},$B${L0}:$B${LF})", MOEDA0,
     f"=SUMPRODUCT({q2}{L0}:{q2}{LF},$B${L0}:$B${LF})/{th}{G_ROW['Custo por mês (R$)']}-1",
     "o efeito dos postos a menos"),
    ("… por readequar os salários", "", None,
     f"={t2}{G_ROW['Custo por mês (R$)']}/SUMPRODUCT({q2}{L0}:{q2}{LF},$B${L0}:$B${LF})-1",
     "o efeito dos preços, sobre o quadro já menor"),
]
for rot, v, fmtv, pct, como in RESP:
    r += 1
    put(ge, f"A{r}", rot, font=F_B, al=WRAP)
    put(ge, f"B{r}", v, fmtv, F_B)
    put(ge, f"C{r}", pct if pct else "", '+0.0%;-0.0%;"0"' if pct else None, F_B)
    put(ge, f"D{r}", "")
    put(ge, f"E{r}", como, font=F_I, al=WRAP)
    ge.row_dimensions[r].height = 28
G_RESP_FIM = r
r += 2
for t in [
    "Os preços que caem na P2: a Direção vai ao preço do IEV (R$ 10.200, convênio de 16 meses); a Coordenação "
    "Assistencial iguala a Administrativa e Financeira (R$ 8.400, o custo de mercado de um gerente) para a direção "
    "continuar acima das coordenações; o pré-exame é pago pela função (contato, orientação e confirmação), como o "
    "assistente do IEV (R$ 3.200) — na P2 o posto passa a se chamar assistente de agendamento, confirmação e busca "
    "ativa; a assessoria vai ao preço do pt_ses_05 (R$ 3.700), que em 12 meses dá o mesmo total da v26, porque o "
    "trabalho dela é por prestação de contas, e não por mês.",
    "Os postos que caem na P2 seguem o volume: os mesmos exames em 12 meses dão 2/3 do trabalho por mês. 10 "
    "operadores × 8 meses = 80 operador-mês viram 7 × 12 = 84; 6 assistentes × 8 = 48 viram 4 × 12 = 48. Os "
    "supervisores passam a 1 para 3 polos (o pt_ses_01 tem 1 para 2). Direção e coordenações ficam.",
    "P1 mostra por que só cortar salário não serve: todos os cargos caem 31% e quase todos ficam abaixo do mercado ou "
    "do menor preço aprovado. P3 mostra o outro extremo: mantém os salários de hoje e corta postos, e a carga por "
    "operador sobe a cerca de 1.300 exames por mês.",
]:
    nota(ge, r, t, "T", 44)
    r += 1
ge.freeze_panes = "F7"

# ================================================================== Fluxo de atendimento
N_FX = "Fluxo"
fx = aba(N_FX, [30, 34, 40, 10, 11, 12, 12, 11, 12])
titulo(fx, "Fluxo de atendimento: o que acontece fora da sala para a sala render mais", "Parte 1: ultrassom, por "
       "grupo de exame. Parte 2: tomografia sem contraste, com contraste em série (como a v26 conta) e com contraste "
       "em linha, com o preparo de vários pacientes em paralelo. Minutos em amarelo nas Premissas: são para medir no "
       "mês 1.", "I")
# ---- parte 1: ultrassom
GRUPOS_US = [
    ("Mama", lambda c, n: c == "02.05.02.009-7", "sem preparo",
     "troca de roupa no vestiário (avental) antes de ser chamada"),
    ("Doppler de membros (venoso e arterial)", lambda c, n: c == "02.05.01.004-0" and re.search(r"MMII|MMSS", n),
     "sem preparo", "tirar meias e a roupa do membro no vestiário"),
    ("Doppler de carótidas e outros vasos", lambda c, n: c == "02.05.01.004-0", "sem preparo; artérias renais e "
     "aorta: jejum", "—"),
    ("Parede abdominal", lambda c, n: "PAREDE" in n, "sem preparo", "—"),
    ("Abdômen total", lambda c, n: c == "02.05.02.004-6", "jejum e bexiga cheia",
     "água na espera para encher a bexiga; agenda de manhã, por causa do jejum"),
    ("Abdômen superior", lambda c, n: c == "02.05.02.003-8", "jejum", "agenda de manhã, por causa do jejum"),
    ("Aparelho urinário e rins", lambda c, n: c == "02.05.02.005-4", "bexiga cheia",
     "água na espera, cerca de 1 hora antes, sem ocupar a sala"),
    ("Próstata (via abdominal)", lambda c, n: c == "02.05.02.010-0", "bexiga cheia", "água na espera, cerca de 1 hora antes"),
    ("Pélvica (ginecológica)", lambda c, n: c == "02.05.02.016-0", "bexiga cheia", "água na espera, cerca de 1 hora antes"),
    ("Transvaginal", lambda c, n: c == "02.05.02.018-6", "bexiga vazia; acompanhante (v26, 4.16 g)",
     "esvaziar a bexiga e trocar de roupa no vestiário; transdutor desinfetado e capa pronta"),
    ("Tireoide", lambda c, n: c == "02.05.02.012-7", "sem preparo", "—"),
    ("Bolsa escrotal", lambda c, n: c == "02.05.02.007-0", "sem preparo; acompanhante", "troca de roupa no vestiário"),
]
agg = {g[0]: [0, 0.0, 0.0] for g in GRUPOS_US}  # exames, minutos de agenda × exames, minutos posicionado × exames
for it in US:
    nome_up = it["nome"].upper()
    g = next(g for g in GRUPOS_US if g[1](it["codigo"], nome_up))
    m = it["minutos"]
    pos = 30 if m >= 40 else m - 5
    agg[g[0]][0] += it["meta"]
    agg[g[0]][1] += it["meta"] * m
    agg[g[0]][2] += it["meta"] * pos
assert sum(v[0] for v in agg.values()) == EX_US
secao(fx, 4, "Parte 1. Ultrassom: o preparo do paciente fica fora da sala")
cab(fx, 5, ["Grupo de exame", "Preparo do paciente (usual; o responsável técnico do polo valida)",
            "O que se faz fora da sala, em paralelo", "Exames (carteira 1)", "Minutos de agenda (CBR 2017)",
            "Minutos com o paciente posicionado (CBR 2017)", "Minutos de sala com o preparo em paralelo",
            "Horas de agenda", "Horas com o preparo em paralelo"], h=58)
r = 6
FX_US0 = r
for nome, _f, prep, fora in GRUPOS_US:
    ex_, mag, mpos = agg[nome]
    put(fx, f"A{r}", nome, font=F_B, al=WRAP)
    put(fx, f"B{r}", prep, al=WRAP)
    put(fx, f"C{r}", fora, al=WRAP)
    entrada(fx, f"D{r}", ex_, INT, "carteira 1 (estudo das filas de 02/11)")
    entrada(fx, f"E{r}", round(mag / ex_, 1), DEC1, "média da carteira: o intervalo de agendamento do CBR 2017")
    entrada(fx, f"F{r}", round(mpos / ex_, 1), DEC1, "CBR 2017: tempo com o paciente posicionado (5 min a menos que "
            "o intervalo; doppler de membros 30 em vez de 40)")
    put(fx, f"G{r}", f"=F{r}+{P['troca_us']}", DEC1)
    put(fx, f"H{r}", f"=D{r}*E{r}/60", INT)
    put(fx, f"I{r}", f"=D{r}*G{r}/60", INT)
    fx.row_dimensions[r].height = 30
    r += 1
FX_US1 = r - 1
put(fx, f"A{r}", "Ultrassom", font=F_G, fill=TOT)
for c_ in "BCEFG":
    put(fx, f"{c_}{r}", "", fill=TOT)
for c_ in "DHI":
    put(fx, f"{c_}{r}", f"=SUM({c_}{FX_US0}:{c_}{FX_US1})", INT, F_G, TOT)
FX_UST = r
r += 1
put(fx, f"A{r}", "Horas de sala com o preparo em paralelo ÷ horas de agenda", font=F_B, al=WRAP)
fx.merge_cells(f"A{r}:G{r}")
put(fx, f"H{r}", "")
put(fx, f"I{r}", f"=I{FX_UST}/H{FX_UST}", PCT, F_B)
FX_RAZAO = R(N_FX, f"I{r}")
r += 1
put(fx, f"A{r}", "Salas da rede em 12 meses (sem o arredondamento por polo): na agenda do CBR · com o preparo em "
    "paralelo", font=F_B, al=WRAP)
fx.merge_cells(f"A{r}:G{r}")
put(fx, f"H{r}", f"=ROUNDUP(H{FX_UST}/(1-{P['falta']})/{P['cap_p']},0)", INT, F_B)
put(fx, f"I{r}", f"=ROUNDUP(I{FX_UST}/(1-{P['falta']})/{P['cap_p']},0)", INT, F_B)
fx.row_dimensions[r].height = 28
r += 1
nota(fx, r, "O CBR 2017 separa o intervalo de agendamento do tempo com o paciente posicionado. A diferença (5 min por "
     "exame) é a entrada, a troca de roupa, a explicação e a saída. Com o próximo paciente pronto (vestiário, bexiga "
     "cheia na espera, chamada antecipada), a sala só perde a entrada e a saída. A aba Salas mostra, polo a polo, "
     "quantas salas bastam assim.", "I", 44)
r += 2

# ---- parte 2: tomografia
secao(fx, r, "Parte 2. Tomografia: três fluxos")
r += 1
FX_TC = {}


def fluxo(r, titulo_, passos, chave):
    secao(fx, r, titulo_)
    r += 1
    cab(fx, r, ["Passo", "O que acontece", "Quem faz e onde", "Minutos", "Ocupa o tomógrafo?"], h=30)
    r += 1
    ini = r
    for nome, oque, quem, minutos, ocupa in passos:
        put(fx, f"A{r}", nome, font=F_B, al=WRAP)
        put(fx, f"B{r}", oque, al=WRAP)
        put(fx, f"C{r}", quem, al=WRAP)
        put(fx, f"D{r}", minutos, DEC1, F_LK if str(minutos).startswith("=") else F_N)
        put(fx, f"E{r}", "sim" if ocupa else "não", font=F_B if ocupa else F_N, al=CEN,
            fill=AZUL if ocupa else None)
        fx.row_dimensions[r].height = 40
        r += 1
    put(fx, f"A{r}", "Minutos de tomógrafo por exame", font=F_B, fill=TOT)
    for c_ in "BC":
        put(fx, f"{c_}{r}", "", fill=TOT)
    put(fx, f"D{r}", f'=SUMIF(E{ini}:E{r - 1},"sim",D{ini}:D{r - 1})', DEC1, F_B, TOT)
    put(fx, f"E{r}", "", fill=TOT)
    FX_TC[chave] = R(N_FX, f"D{r}")
    r += 1
    put(fx, f"A{r}", "Tempo do paciente no polo (soma dos passos)", font=F_B)
    put(fx, f"D{r}", f"=SUM(D{ini}:D{r - 2})", DEC1, F_B)
    return r + 2


r = fluxo(r, "A. Tomografia sem contraste", [
    ("1. Recepção", "identificação, documentos, CPF, conferência da solicitação", "secretaria, na recepção",
     f"={P['t_recep']}", False),
    ("2. Conferência", "gestação, nas usuárias, e termo de consentimento", "enfermagem, na triagem",
     f"={P['t_triagem']}", False),
    ("3. Troca de roupa", "retirada de metais e avental", "o paciente, no vestiário", f"={P['t_troca']}", False),
    ("4. Exame", "posicionar, adquirir e sair", "técnico em radiologia, na sala", f"={P['min_linha_sem']}", True),
], "sem")
r = fluxo(r, "B. Tomografia com contraste em série (a conta da v26: tudo na sala)", [
    ("1. Recepção", "identificação, documentos, CPF", "secretaria, na recepção", f"={P['t_recep']}", False),
    ("2. Triagem", "alergia, doença renal, metformina, gestação; termo", "enfermagem, na triagem",
     f"={P['t_triagem']}", False),
    ("3. Troca de roupa", "retirada de metais e avental", "o paciente, no vestiário", f"={P['t_troca']}", False),
    ("4. Punção e exame na sala", "punção venosa na mesa, conexão à bomba, aquisição com fases, desconexão",
     "enfermagem e técnico em radiologia, na sala", f"={P['min_com']}", True),
    ("5. Repouso", "observação depois do contraste", "enfermagem, na sala de repouso", f"={P['t_repouso']}", False),
    ("6. Alta", "retirada do acesso, orientação da metformina", "enfermagem", f"={P['t_alta']}", False),
], "serie")
r = fluxo(r, "C. Tomografia com contraste em linha: o preparo de vários pacientes em paralelo", [
    ("1. Recepção", "identificação, documentos, CPF; o paciente chega cerca de 40 min antes do horário do "
     "tomógrafo", "secretaria, na recepção", f"={P['t_recep']}", False),
    ("2. Orientação em grupo", "3 a 5 pacientes juntos: o que é o contraste, o calor na injeção, o repouso e o que "
     "avisar", "enfermagem, na sala de espera", f"={P['t_grupo']}", False),
    ("3. Triagem individual", "alergia, doença renal (creatinina no TrakCare só para o renal), metformina, gestação; "
     "termo", "enfermagem, na triagem", f"={P['t_triagem']}", False),
    ("4. Troca de roupa", "retirada de metais e avental", "o paciente, no vestiário", f"={P['t_troca']}", False),
    ("5. Punção na sala de preparo", "cateter venoso, teste com soro e curativo; o paciente fica pronto, sentado",
     "enfermagem, na sala de preparo", f"={P['t_puncao']}", False),
    ("6. Espera pronto", "dois pacientes com acesso à espera, para o tomógrafo nunca parar",
     "o paciente, na sala de preparo", f"={P['pulmao']}*{P['min_linha_com']}", False),
    ("7. Exame", "posicionar, conectar à bomba, adquirir com fases, desconectar", "técnico em radiologia, na sala",
     f"={P['min_linha_com']}", True),
    ("8. Repouso", "observação, sem tempo mínimo (v26, 4.8)", "enfermagem, na sala de repouso",
     f"={P['t_repouso']}", False),
    ("9. Alta", "retirada do acesso, orientação da metformina", "enfermagem", f"={P['t_alta']}", False),
], "linha")
# resumo do fluxo em linha
secao(fx, r, "O que o fluxo em linha pede e o que ele rende, por tomógrafo")
r += 1
cab(fx, r, ["", "Valor", "Como se calcula"], h=22)
RES_FX = [
    ("Minutos de tomógrafo por exame com contraste: em série · em linha", f"={FX_TC['serie']}",
     f"={FX_TC['linha']}", "aba Fluxo, B e C"),
    ("Tomógrafo poupado por exame com contraste", f"=1-{FX_TC['linha']}/{FX_TC['serie']}", None, "em linha ÷ em série"),
    ("Exames com contraste por dia de tomógrafo: em série · em linha",
     f"={P['horas_tc']}*{P['ocupacao']}*60/{FX_TC['serie']}", f"={P['horas_tc']}*{P['ocupacao']}*60/{FX_TC['linha']}",
     "horas por dia × parte com exame × 60 ÷ minutos por exame"),
    ("Punções por hora que o tomógrafo pede", f"=60/{FX_TC['linha']}", None, "60 ÷ minutos por exame"),
    ("Enfermagem ocupada no preparo e na alta, por tomógrafo (pessoas)",
     f"=60/{FX_TC['linha']}*({P['t_puncao']}+{P['t_alta']})/60", None,
     "punções por hora × (punção + alta) ÷ 60; a v26 tem 2 de enfermagem por tomógrafo"),
    ("Poltronas na sala de preparo e repouso",
     f"=ROUNDUP({P['pulmao']}+60/{FX_TC['linha']}*({P['t_puncao']}+{P['t_repouso']})/60,0)", None,
     "pacientes prontos + (punções por hora × minutos de punção e repouso ÷ 60)"),
    ("Grupos de orientação por hora", f"=60/{FX_TC['linha']}/{P['n_grupo']}", None,
     "punções por hora ÷ pacientes por grupo"),
]
for rot, v1, v2, como in RES_FX:
    r += 1
    put(fx, f"A{r}", rot, font=F_B, al=WRAP)
    fx.merge_cells(f"A{r}:B{r}")
    if v2 is None:
        put(fx, f"C{r}", v1, PCT if "poupado" in rot else DEC1, F_B)
    else:
        put(fx, f"C{r}", v1, DEC1, F_B)
        put(fx, f"D{r}", v2, DEC1, F_B)
    put(fx, f"E{r}", como, font=F_I, al=WRAP)
    fx.merge_cells(f"E{r}:I{r}")
    fx.row_dimensions[r].height = 30
r += 2
for t in [
    "Jejum: o HC-UFG (Ebserh, 2026) dispensa jejum para tomografia, mesmo com contraste venoso, e cita o Colégio "
    "Americano de Radiologia. Sem jejum, o contraste não fica preso à manhã, e a agenda pode correr o dia inteiro. "
    "A clínica precisa confirmar se segue essa orientação.",
    "O que a clínica precisa ter para o fluxo em linha: uma sala de preparo com poltronas (a conta acima), uma pessoa "
    "de enfermagem dedicada à punção e à alta por tomógrafo, a bomba injetora com a seringa pronta antes de o paciente "
    "entrar e o radiologista no serviço durante as injeções.",
    "O que muda na agenda: o paciente com contraste é marcado para chegar cerca de 40 minutos antes do horário do "
    "tomógrafo; os exames sem contraste entram nos intervalos; na espera, cada paciente com contraste tem um tempo "
    "previsto, e o próximo é puncionado quando o anterior entra na sala.",
]:
    nota(fx, r, t, "I", 44)
    r += 1
fx.freeze_panes = "B4"

# ================================================================== Salas de ultrassom
N_SA = "Salas"
sa = aba(N_SA, [24, 13, 11, 11, 12, 12, 11, 11, 11, 12, 13, 40, 13, 11])
titulo(sa, "Salas de ultrassom por polo: 8 meses contra 12", "As horas de exame do polo são as mesmas nos dois "
       "arranjos (os mesmos exames); em 12 meses cada sala tem 50% mais horas, e o polo precisa de menos salas. O que "
       "sobe é o tempo de aluguel. Mude as salas adotadas (amarelo) para testar.", "N")
cab(sa, 4, ["Polo", "Horas de exame no período (carteira 1)", "Salas hoje (02/11)", "Uso hoje",
            "Salas necessárias em 12 meses", "Salas adotadas em 12 meses", "Uso em 12 meses", "Salas-mês hoje",
            "Salas-mês em 12 meses", "Salas nos contratos (20/10)", "Diferença: adotadas − contratos", "Unidade dos contratos",
            "Salas em 12 meses com o preparo em paralelo (aba Fluxo)", "Uso com o preparo em paralelo"],
    h=58)
SALAS_HOJE = CAP["salas"]
CONTRATOS = {"Oeste": (3, "Ceilândia (Clínica Brasília) — recebe também Taguatinga e Vicente Pires"),
             "Sudoeste": (2, "Samambaia (MedBrasília)"), "Norte": (2, "Sobradinho (Clínica Padrão)"),
             "Leste": (2, "São Sebastião (Hpaes)"), "Central e Centro-Sul": (3, "Asa Sul (DaVida)"),
             "Sul": (1, "Gama (Provida)")}
for i, p in enumerate(POLOS):
    l = 5 + i
    put(sa, f"A{l}", p, font=F_B)
    entrada(sa, f"B{l}", CAP["horas_us"][p], INT, "estudo_filas_imagem_20261102.json, capacidade da carteira 1 "
            "(tempos do CBR 2017)")
    entrada(sa, f"C{l}", SALAS_HOJE[p], INT, "estudo das filas de 02/11: as 20 salas repartidas pela carga")
    put(sa, f"D{l}", f"=B{l}/(1-{P['falta']})/(C{l}*{P['cap_h']})", PCT)
    put(sa, f"E{l}", f"=MAX(1,ROUNDUP(B{l}/(1-{P['falta']})/{P['cap_p']}-0.000001,0))", INT, F_B)
    entrada(sa, f"F{l}", f"=E{l}", INT, "começa igual às necessárias; ponha um número para testar")
    put(sa, f"G{l}", f"=B{l}/(1-{P['falta']})/(F{l}*{P['cap_p']})", PCT)
    put(sa, f"H{l}", f"=C{l}*{P['meses_h']}", INT)
    put(sa, f"I{l}", f"=F{l}*{P['meses_p']}", INT)
    entrada(sa, f"J{l}", CONTRATOS[p][0], INT, "salas_ultrassom_metricas_20261020.xlsx, aba Por unidade (documento "
            "da equipe de 20/10, Projeto Zero Fila | USG)")
    put(sa, f"K{l}", f"=F{l}-J{l}", '+#,##0;-#,##0;"0"')
    put(sa, f"L{l}", CONTRATOS[p][1], font=F_I, al=WRAP)
    put(sa, f"M{l}", f"=MAX(1,ROUNDUP(B{l}*{FX_RAZAO}/(1-{P['falta']})/{P['cap_p']}-0.000001,0))", INT, F_B)
    put(sa, f"N{l}", f"=B{l}*{FX_RAZAO}/(1-{P['falta']})/(M{l}*{P['cap_p']})", PCT)
    sa.row_dimensions[l].height = 28
LT_SA = 11
put(sa, f"A{LT_SA}", "Rede", font=F_G, fill=TOT)
for col in "BCEFHIJK":
    put(sa, f"{col}{LT_SA}", f"=SUM({col}5:{col}10)", INT if col != "K" else '+#,##0;-#,##0;"0"', F_G, TOT)
put(sa, f"D{LT_SA}", f"=B{LT_SA}/(1-{P['falta']})/(C{LT_SA}*{P['cap_h']})", PCT, F_G, TOT)
put(sa, f"G{LT_SA}", f"=B{LT_SA}/(1-{P['falta']})/(F{LT_SA}*{P['cap_p']})", PCT, F_G, TOT)
put(sa, f"L{LT_SA}", "", fill=TOT)
put(sa, f"M{LT_SA}", f"=SUM(M5:M10)", INT, F_G, TOT)
put(sa, f"N{LT_SA}", f"=B{LT_SA}*{FX_RAZAO}/(1-{P['falta']})/(M{LT_SA}*{P['cap_p']})", PCT, F_G, TOT)
for c_ in ("D", "G"):
    sa.conditional_formatting.add(f"{c_}5:{c_}11", CellIsRule(operator="greaterThan", formula=["1"], fill=VERM))
sa.conditional_formatting.add("K5:K10", CellIsRule(operator="greaterThan", formula=["0"], fill=VERM))
nota(sa, 13, "Salas-mês = salas × meses: é o que se paga de aluguel. Em 12 meses a rede inteira usaria menos salas "
     "(as horas cabem em cerca de 12), mas cada polo arredonda para cima e tem no mínimo uma sala: é esse "
     "arredondamento que faz as salas-mês subirem. O Oeste, por exemplo, usa meia sala e paga uma inteira por mais "
     "quatro meses. Sala por turno, em vez de sala inteira, reduz essa perda.", "L", 42)
nota(sa, 14, "Contratos: o documento da equipe de 20/10 reparte as Regiões de outro jeito (Ceilândia recebe Taguatinga "
     "e Vicente Pires, que são da Sudoeste); por isso olhe Oeste e Sudoeste juntos. O que não fecha em 12 meses é o "
     "Sul: o Gama tem 1 sala para a 2ª maior carga da rede.", "L", 30)
sa.freeze_panes = "B5"

# ================================================================== Tomografia
N_TC = "Tomografia"
tc = aba(N_TC, [56, 15, 15, 15, 15, 15, 30])
titulo(tc, "Tomografia: 3 tomógrafos em 12 meses, e o tempo do contraste", "97% da tomografia da carteira 1 é com "
       "contraste, antes de o radiologista converter parte para sem contraste. Aqui o exame é feito em série, com o "
       "acesso venoso na mesa (v26); o fluxo em linha está nas abas Fluxo e Meses e tomógrafos.", "G")
cab(tc, 4, ["", "Hoje", "Proposta", "Diferença"], h=24)
put(tc, "A5", "Meses")
put(tc, "B5", f"={P['meses_h']}", INT, F_LK)
put(tc, "C5", f"={P['meses_p']}", INT, F_LK)
put(tc, "A6", "Tomógrafos")
put(tc, "B6", f"={P['tomografos_h']}", INT, F_LK)
put(tc, "C6", f"={P['tomografos_p']}", INT, F_LK)
LINHAS_TC = [
    ("Tomógrafo-mês (tomógrafos × meses)", "={c}6*{c}5", INT),
    ("Horas de tomógrafo que a carteira pede",
     f"=({P['tc_com_ef']}*{P['min_com']}+{P['tc_sem_ef']}*{P['min_sem']})/60", INT),
    ("… delas, com contraste", f"={P['tc_com_ef']}*{P['min_com']}/60", INT),
    ("Horas de exame de um tomógrafo no período",
     f"={P['horas_tc']}*{P['ocupacao']}*{P['dias_tc']}*{{c}}5", INT),
    ("Horas de exame da rede no período", "={c}10*{c}6", INT),
    ("Uso da rede", "={c}8/{c}11", PCT),
    ("Horas de contraste da rede (na janela do contraste)",
     f"=MIN({P['janela']},{P['horas_tc']})*{P['ocupacao']}*{P['dias_tc']}*{{c}}5*{{c}}6", INT),
    ("Uso da janela do contraste", "={c}9/{c}13", PCT),
    ("Tomógrafos necessários",
     f"=ROUNDUP(MAX({{c}}8/{{c}}10,{{c}}9/(MIN({P['janela']},{P['horas_tc']})*{P['ocupacao']}*{P['dias_tc']}*{{c}}5))"
     f"-0.000001,0)", INT),
    ("Minutos máximos por exame com contraste que os tomógrafos aguentam",
     f"=MIN(({{c}}11-{P['tc_sem_ef']}*{P['min_sem']}/60)*60/{P['tc_com_ef']},{{c}}13*60/{P['tc_com_ef']})", DEC1),
    ("Exames de tomografia por tomógrafo por mês", f"=({P['tc_com_ef']}+{P['tc_sem_ef']})/{{c}}6/{{c}}5", INT),
    ("Exames de tomografia por tomógrafo por dia de atendimento",
     f"=({P['tc_com_ef']}+{P['tc_sem_ef']})/{{c}}6/{{c}}5/{P['dias_tc']}", DEC1),
]
for i, (rot, f, fmt) in enumerate(LINHAS_TC):
    l = 7 + i
    put(tc, f"A{l}", rot, al=WRAP)
    for c_ in "BC":
        put(tc, f"{c_}{l}", f.replace("{c}", c_), fmt, F_B if rot.startswith(("Uso", "Tomógrafos nec", "Minutos")) else F_N)
    put(tc, f"D{l}", f"=C{l}-B{l}", fmt if fmt != PCT else '+0.0%;-0.0%;"0"')
    tc.row_dimensions[l].height = 26
for c_ in ("B12:C12", "B14:C14"):
    tc.conditional_formatting.add(c_, CellIsRule(operator="greaterThan", formula=["1"], fill=VERM))
tc.conditional_formatting.add("B15:C15", CellIsRule(operator="greaterThan", formula=["B6"], fill=VERM))
nota(tc, 20, "Ler assim: com 12 meses e 3 tomógrafos, a rede tem 36 tomógrafo-mês, contra 40 de hoje (5 × 8). A "
     "proposta tem menos capacidade de tomografia que a de hoje, e não mais. O que a salva é a folga: com 20 min por "
     "exame com contraste e o dia inteiro de contraste, ela fica em cerca de 79%. Acima de uns 25 min por exame, ou "
     "com o contraste restrito a uma janela curta, 3 tomógrafos não fecham.", "G", 56)

# grades de sensibilidade
MINS = [15, 20, 25, 30, 35, 40]
JAN = [10, 8, 6, 5]


def grade(r0, meses_ref, titulo_):
    secao(tc, r0, titulo_)
    cab(tc, r0 + 1, ["Minutos por exame com contraste ↓ · horas de contraste por dia →"] + [f"{j} h" for j in JAN], h=30)
    for i, m in enumerate(MINS):
        l = r0 + 2 + i
        entrada(tc, f"A{l}", m, INT)
        for j, w in enumerate(JAN):
            col = L(2 + j)
            if i == 0:
                entrada(tc, f"{col}{r0 + 1}", w, '0" h"')
            hora = f"{P['horas_tc']}*{P['ocupacao']}*{P['dias_tc']}*{meses_ref}"
            janela = f"MIN({col}${r0 + 1},{P['horas_tc']})*{P['ocupacao']}*{P['dias_tc']}*{meses_ref}"
            f = (f"=ROUNDUP(MAX(({P['tc_com_ef']}*$A{l}+{P['tc_sem_ef']}*{P['min_sem']})/60/({hora}),"
                 f"{P['tc_com_ef']}*$A{l}/60/({janela}))-0.000001,0)")
            put(tc, f"{col}{l}", f, INT, al=CEN)
    return r0 + 2, r0 + 1 + len(MINS)


a1, b1 = grade(22, P["meses_p"], "Tomógrafos necessários em 12 meses (proposta)")
tc.conditional_formatting.add(f"B{a1}:E{b1}", CellIsRule(operator="lessThanOrEqual", formula=[P["tomografos_p"]],
                                                         fill=VERDE))
tc.conditional_formatting.add(f"B{a1}:E{b1}", CellIsRule(operator="greaterThan", formula=[P["tomografos_p"]],
                                                         fill=VERM))
a2, b2 = grade(b1 + 2, P["meses_h"], "Tomógrafos necessários em 8 meses (hoje)")
tc.conditional_formatting.add(f"B{a2}:E{b2}", CellIsRule(operator="lessThanOrEqual", formula=[P["tomografos_h"]],
                                                         fill=VERDE))
tc.conditional_formatting.add(f"B{a2}:E{b2}", CellIsRule(operator="greaterThan", formula=[P["tomografos_h"]],
                                                         fill=VERM))
nota(tc, b2 + 1, "Verde: cabe nos tomógrafos do arranjo (3 na proposta, 5 hoje). Vermelho: não cabe. A janela é o tempo "
     "do dia em que a clínica aceita exame com contraste (por exemplo, só com o radiologista presente, ou só de manhã "
     "por causa do jejum). Os exames sem contraste (2%) entram no resto do dia.", "G", 30)

# arranjo dos 3 polos de tomografia
r0 = b2 + 3
secao(tc, r0, "Os 3 polos de tomografia: para onde vai cada Região (mude na coluna D)")
cab(tc, r0 + 1, ["Região de Saúde (polo do ultrassom)", "Exames de TC no período", "Parte da Região",
                 "Vai para o polo de TC", "Exames que leva", "Horas que leva", "Observação"], h=36)
LIN_REG = [("Oeste", 1.0, 1, ""),
           ("Sudoeste — Samambaia e Recanto das Emas", 0.5, 1, "a parte da Sudoeste em amarelo; o resto na linha de baixo"),
           ("Sudoeste — Taguatinga, Águas Claras, Vicente Pires e Arniqueira", None, 2, ""),
           ("Norte", 1.0, 3, ""), ("Leste", 1.0, 3, ""), ("Central e Centro-Sul", 1.0, 3, ""), ("Sul", 1.0, 2, "")]
dv = DataValidation(type="list", formula1='"1,2,3"', allow_blank=False)
tc.add_data_validation(dv)
RA = r0 + 2
for i, (reg, parte, polo, obs) in enumerate(LIN_REG):
    l = RA + i
    base = "Sudoeste" if reg.startswith("Sudoeste") else reg
    put(tc, f"A{l}", reg, al=WRAP)
    entrada(tc, f"B{l}", CAP["exames_tc"][base], INT, "carteira 1, exames de TC pela origem da Região (estudo de 02/11)")
    if parte is None:
        put(tc, f"C{l}", f"=1-C{l - 1}", PCT)
    else:
        entrada(tc, f"C{l}", parte, PCT)
    entrada(tc, f"D{l}", polo, INT)
    dv.add(f"D{l}")
    put(tc, f"E{l}", f"=B{l}*C{l}", INT)
    put(tc, f"F{l}", f"=E{l}*({P['tc_com_ef']}*{P['min_com']}+{P['tc_sem_ef']}*{P['min_sem']})"
                     f"/({P['tc_com_ef']}+{P['tc_sem_ef']})/60", INT)
    put(tc, f"G{l}", obs, font=F_I, al=WRAP)
    tc.row_dimensions[l].height = 28
RZ = RA + len(LIN_REG) - 1
r1 = RZ + 2
cab(tc, r1, ["Polo de tomografia (nome em amarelo)", "Exames no período", "Exames por mês", "Exames por dia útil",
             "Horas no período", "Uso do tomógrafo", "Regiões que recebe"], h=36)
NOMES_TC = ["1 — oeste (ex.: Ceilândia)", "2 — sudoeste e sul (ex.: Taguatinga)", "3 — centro e norte (ex.: Plano Piloto)"]
for k in range(3):
    l = r1 + 1 + k
    entrada(tc, f"A{l}", NOMES_TC[k], None, "o nome é livre; o número na frente é o que a coluna D usa")
    put(tc, f"B{l}", f"=SUMIF($D${RA}:$D${RZ},{k + 1},$E${RA}:$E${RZ})", INT)
    put(tc, f"C{l}", f"=B{l}/{P['meses_p']}", INT)
    put(tc, f"D{l}", f"=B{l}/{P['dias_tc_p']}", DEC1)
    put(tc, f"E{l}", f"=SUMIF($D${RA}:$D${RZ},{k + 1},$F${RA}:$F${RZ})", INT)
    put(tc, f"F{l}", f"=E{l}/{P['cap_tc_p']}", PCT, F_B)
    lista = "&".join(f'IF($D${x}={k + 1},", "&$A${x},"")' for x in range(RA, RZ + 1))
    put(tc, f"G{l}", f"=MID({lista},3,400)", font=F_I, al=WRAP)
    tc.row_dimensions[l].height = 40
tc.conditional_formatting.add(f"F{r1 + 1}:F{r1 + 3}", CellIsRule(operator="greaterThan", formula=["1"], fill=VERM))
nota(tc, r1 + 5, "O arranjo de exemplo equilibra os três em cerca de 79%: Ceilândia com a Oeste e metade da Sudoeste; "
     "Taguatinga com a outra metade e o Sul; o Plano Piloto com a Central, a Centro-Sul, a Leste e a Norte. Pôr o "
     "terceiro no Gama ou em Sobradinho, no lugar do Plano Piloto, desequilibra (teste na coluna D). Quem decide a "
     "Região de cada solicitação é a regulação (v26, 4.2).", "G", 44)
tc.freeze_panes = "B5"
TC_ROW = {"uso": 12, "nec": 15, "maxmin": 16, "porMes": 17}

# ================================================================== Meses e tomógrafos
N_ME = "Meses e tomógrafos"
me = aba(N_ME, [46, 15, 15, 15, 17, 40])
titulo(me, "Quantos meses a tomografia leva com 3, 4 ou 5 tomógrafos", "Os meses que cada número de tomógrafos "
       "leva para fazer toda a tomografia da carteira 1, no fluxo em série (a conta da v26, com 20, 25 ou 30 min por "
       "exame com contraste) e no fluxo em linha (aba Fluxo). Já desconta a parte que o radiologista converte para sem "
       "contraste (Premissas). Verde: cabe nos meses da proposta.", "F")
cab(me, 4, ["", "Em série, 20 min (v26)", "Em série, 25 min", "Em série, 30 min", "Em linha (acesso fora da sala)",
            "De onde vem"], h=40)
put(me, "A5", "Minutos de tomógrafo por exame com contraste", font=F_B)
put(me, "B5", f"={P['min_com']}", DEC1, F_LK)
entrada(me, "C5", 25, DEC1)
entrada(me, "D5", 30, DEC1)
put(me, "E5", f"={FX_TC['linha']}", DEC1, F_LK)
put(me, "F5", "Premissas e aba Fluxo", font=F_I)
put(me, "A6", "Minutos de tomógrafo por exame sem contraste", font=F_B)
for c_ in "BCD":
    put(me, f"{c_}6", f"={P['min_sem']}", DEC1, F_LK)
put(me, "E6", f"={FX_TC['sem']}", DEC1, F_LK)
put(me, "F6", "Premissas e aba Fluxo", font=F_I)
put(me, "A7", "Horas de tomógrafo que a carteira pede", font=F_B)
for c_ in "BCDE":
    put(me, f"{c_}7", f"=({P['tc_com_ef']}*{c_}5+{P['tc_sem_ef']}*{c_}6)/60", INT, F_B)
put(me, "F7", "exames com e sem contraste depois da conversão × minutos ÷ 60", font=F_I, al=WRAP)
put(me, "A8", "Horas de exame de um tomógrafo por mês", font=F_B)
put(me, "B8", f"={P['horas_tc']}*{P['ocupacao']}*{P['dias_tc']}", INT, F_B)
put(me, "F8", "horas por dia × parte com exame × dias por mês (Premissas)", font=F_I, al=WRAP)
TC_MES = "$B$8"
secao(me, 10, "Meses para fazer toda a tomografia")
cab(me, 11, ["Tomógrafos", "Em série, 20 min (v26)", "Em série, 25 min", "Em série, 30 min",
             "Em linha (acesso fora da sala)", ""], h=40)
for i, n in enumerate([3, 4, 5]):
    l = 12 + i
    entrada(me, f"A{l}", n, INT)
    for c_ in "BCDE":
        put(me, f"{c_}{l}", f"={c_}$7/($A{l}*{TC_MES})", DEC1, F_B, al=CEN)
me.conditional_formatting.add("B12:E14", CellIsRule(operator="lessThanOrEqual", formula=[P["meses_p"]], fill=VERDE))
me.conditional_formatting.add("B12:E14", CellIsRule(operator="greaterThan", formula=[P["meses_p"]], fill=VERM))
secao(me, 16, "Horas por dia que cada tomógrafo precisa abrir para o plano, para fechar em 12 meses")
cab(me, 17, ["Tomógrafos", "Em série, 20 min (v26)", "Em série, 25 min", "Em série, 30 min",
             "Em linha (acesso fora da sala)", ""], h=40)
for i in range(3):
    l = 18 + i
    put(me, f"A{l}", f"=A{12 + i}", INT, F_LK)
    for c_ in "BCDE":
        put(me, f"{c_}{l}", f"={c_}$7/($A{l}*{P['ocupacao']}*{P['dias_tc']}*{P['meses_p']})", DEC1, al=CEN)
me.conditional_formatting.add("B18:E20", CellIsRule(operator="greaterThan", formula=[P["horas_tc"]], fill=VERM))
nota(me, 21, "Vermelho: precisa de mais horas por dia do que as Premissas dão ao tomógrafo. Um turno de 6 horas com o "
     "radiologista presente cabe onde a conta der até 6.", "F", 28)
secao(me, 23, "A conversão para sem contraste muda pouco: meses com 3 tomógrafos (mude o número em amarelo)")
put(me, "A24", "Tomógrafos", font=F_B)
entrada(me, "B24", 3, INT)
cab(me, 25, ["Parte convertida para sem contraste", "Em série, 20 min (v26)", "Em linha", "", "", ""], h=30)
for i, c in enumerate([0, 0.1, 0.2, 0.3]):
    l = 26 + i
    entrada(me, f"A{l}", c, PCT)
    put(me, f"B{l}", f"=({P['ex_tc_com']}*(1-$A{l})*$B$5+({P['ex_tc_sem']}+{P['ex_tc_com']}*$A{l})*$B$6)/60"
                     f"/($B$24*{TC_MES})", DEC1, al=CEN)
    put(me, f"C{l}", f"=({P['ex_tc_com']}*(1-$A{l})*$E$5+({P['ex_tc_sem']}+{P['ex_tc_com']}*$A{l})*$E$6)/60"
                     f"/($B$24*{TC_MES})", DEC1, al=CEN)
me.conditional_formatting.add("B26:C29", CellIsRule(operator="lessThanOrEqual", formula=[P["meses_p"]], fill=VERDE))
me.conditional_formatting.add("B26:C29", CellIsRule(operator="greaterThan", formula=[P["meses_p"]], fill=VERM))
nota(me, 30, "A conversão poupa pouco tempo de tomógrafo porque, no fluxo em série, o exame sem contraste leva 15 min "
     "contra 20; no fluxo em linha, 10 contra 13. O ganho maior da conversão é outro: menos contraste, menos punção e "
     "menos risco de reação. O código SUS é o mesmo e paga o mesmo.", "F", 42)
secao(me, 32, "Exames por tomógrafo por mês, se a tomografia correr os 12 meses")
for i in range(3):
    l = 33 + i
    put(me, f"A{l}", f'=A{12 + i}&" tomógrafos"', font=F_B)
    put(me, f"B{l}", f"={P['ex_tc']}/(A{12 + i}*{P['meses_p']})", INT, F_B)
nota(me, 36, "É o volume que dá para oferecer à clínica parceira por tomógrafo. Com o fluxo em linha, 3 tomógrafos "
     "fecham a tomografia antes dos 12 meses: dá para usar só um turno por dia de cada um, ou terminar a tomografia "
     "antes e deixar o fim da vigência para o ultrassom e as remarcações.", "F", 42)
ME_LINHA3 = R(N_ME, "E12")
ME_SERIE3 = R(N_ME, "B12")
ME_HORAS3_LINHA = R(N_ME, "E18")
ME_HORAS3_SERIE = R(N_ME, "B18")
me.freeze_panes = "B5"

# ================================================================== Execução (custo dentro do valor do exame)
N_EX = "Execução"
ex = aba(N_EX, [46, 44, 14, 12, 15, 12, 15, 15, 40])
titulo(ex, "Quanto custa executar: hoje contra 12 meses (controle interno)", "Ultrassom feito por nós (sala e aparelho "
       "alugados, médico por exame) e tomografia na clínica parceira, por exame. É o custo que precisa caber no valor "
       "do exame; não é rubrica do convênio. Os itens SEM PREÇO estão em zero nas Premissas: preencha.", "I")
cab(ex, 4, ["Item", "Como se calcula", "Valor unitário (R$)", "Qtd. hoje", "Custo hoje (R$)", "Qtd. em 12 meses",
            "Custo em 12 meses (R$)", "Diferença (R$)", "O que muda"], h=36)
SA_T = f"'{N_SA}'!$C${LT_SA}"
SA_P = f"'{N_SA}'!$F${LT_SA}"
ITENS = [
    ("Por sala: sobe com os meses, cai com as salas", None),
    ("Aluguel das salas de ultrassom", "salas × meses", P["sala"], f"={SA_T}*{P['meses_h']}",
     f"={SA_P}*{P['meses_p']}", "menos salas, mais meses: pesa o arredondamento por polo"),
    ("Aluguel dos aparelhos de ultrassom", "salas × meses × parte alugada", P["aparelho"],
     f"={SA_T}*{P['meses_h']}*{P['parte_ap']}", f"={SA_P}*{P['meses_p']}*{P['parte_ap']}", "idem"),
    ("Outros custos fixos da sala", "salas × meses", P["fixos_sala"], f"={SA_T}*{P['meses_h']}",
     f"={SA_P}*{P['meses_p']}", "idem"),
    ("Por polo: sobe 50% com os meses", None),
    ("Recepção", "recepcionistas × polos × meses", P["recep"], f"={P['n_recep']}*{P['polos_us_h']}*{P['meses_h']}",
     f"={P['n_recep']}*{P['polos_us_p']}*{P['meses_p']}", "4 meses a mais dos 12 recepcionistas"),
    ("Responsável técnico médico do polo", "polos × meses", P["rt"], f"={P['polos_us_h']}*{P['meses_h']}",
     f"={P['polos_us_p']}*{P['meses_p']}", "SEM PREÇO: cada R$ 1.000 por mês custa R$ 24.000 a mais"),
    ("Médico de retaguarda presencial", "polos × dias úteis", P["retaguarda"], f"={P['polos_us_h']}*{P['dias_h']}",
     f"={P['polos_us_p']}*{P['dias_p']}", "SEM PREÇO: 504 dias-polo a mais; cada R$ 100 por dia custa R$ 50.400"),
    ("Outros custos do polo", "polos × meses", P["outros_polo"], f"={P['polos_us_h']}*{P['meses_h']}",
     f"={P['polos_us_p']}*{P['meses_p']}", "SEM PREÇO"),
    ("Por exame ou por hora: não muda com os meses", None),
    ("Médico de ultrassom", "exames de ultrassom", P["medico_us"], f"={P['ex_us']}", f"={P['ex_us']}",
     "o mesmo por exame; cada médico faz 1/3 menos por mês"),
    ("Insumos do ultrassom", "exames de ultrassom", P["insumo_us"], f"={P['ex_us']}", f"={P['ex_us']}", ""),
    ("Sistema de imagem (RIS/PACS)", "exames de ultrassom", P["pacs"], f"={P['ex_us']}", f"={P['ex_us']}", ""),
    ("Energia do ultrassom", "horas de exame", P["energia"], f"='{N_SA}'!$B${LT_SA}", f"='{N_SA}'!$B${LT_SA}", ""),
    ("Tomografia na clínica", "exames de tomografia", None, f"={P['ex_tc']}", f"={P['ex_tc']}",
     "o preço com 3 polos está nas Premissas: cada R$ 10 a menos por exame poupa cerca de R$ 144 mil"),
    ("Contraste cobrado à parte", "exames com contraste", P["contraste"], f"={P['ex_tc_com']}", f"={P['ex_tc_com']}",
     "zero se vier no preço; condição a pôr no contrato"),
]
l = 5
PRIM = l
for it in ITENS:
    if it[1] is None:
        secao(ex, l, it[0])
        l += 1
        continue
    nome, como, vu, qh, qp, obs = it
    put(ex, f"A{l}", nome, al=WRAP)
    put(ex, f"B{l}", como, font=F_I, al=WRAP)
    if nome == "Tomografia na clínica":
        put(ex, f"C{l}", f"={P['tc_hoje']}", MOEDA, F_LK)
        put(ex, f"E{l}", f"=D{l}*{P['tc_hoje']}", MOEDA0)
        put(ex, f"G{l}", f"=F{l}*{P['tc_prop']}", MOEDA0)
    else:
        put(ex, f"C{l}", f"={vu}", MOEDA, F_LK)
        put(ex, f"E{l}", f"=D{l}*C{l}", MOEDA0)
        put(ex, f"G{l}", f"=F{l}*C{l}", MOEDA0)
    put(ex, f"D{l}", qh, INT)
    put(ex, f"F{l}", qp, INT)
    put(ex, f"H{l}", f"=G{l}-E{l}", '+"R$" #,##0;-"R$" #,##0;"-"', F_B)
    put(ex, f"I{l}", obs, font=F_I, al=WRAP)
    if "SEM PREÇO" in obs:
        ex[f"I{l}"].font = Font(name=A, size=9, italic=True, color="C00000")
    ex.row_dimensions[l].height = 28
    l += 1
ULT = l - 1
LT_EX = l + 1
put(ex, f"A{LT_EX}", "Custo de executar", font=F_G, fill=TOT)
put(ex, f"B{LT_EX}", "", fill=TOT)
for c_ in "CDF":
    put(ex, f"{c_}{LT_EX}", "", fill=TOT)
put(ex, f"E{LT_EX}", f"=SUM(E{PRIM}:E{ULT})", MOEDA0, F_G, TOT)
put(ex, f"G{LT_EX}", f"=SUM(G{PRIM}:G{ULT})", MOEDA0, F_G, TOT)
put(ex, f"H{LT_EX}", f"=G{LT_EX}-E{LT_EX}", '+"R$" #,##0;-"R$" #,##0;"-"', F_G, TOT)
put(ex, f"I{LT_EX}", "", fill=TOT)
put(ex, f"A{LT_EX + 1}", "Custo por exame", font=F_B)
put(ex, f"E{LT_EX + 1}", f"=E{LT_EX}/{P['ex_tot']}", MOEDA, F_B)
put(ex, f"G{LT_EX + 1}", f"=G{LT_EX}/{P['ex_tot']}", MOEDA, F_B)
put(ex, f"A{LT_EX + 2}", "Valor dos exames da carteira 1 (o que o convênio paga pela produção)", font=F_B, al=WRAP)
put(ex, f"E{LT_EX + 2}", f"={P['v_ex']}", MOEDA0, F_LK)
put(ex, f"G{LT_EX + 2}", f"={P['v_ex']}", MOEDA0, F_LK)
put(ex, f"A{LT_EX + 3}", "Folga: valor dos exames − custo de executar", font=F_B, al=WRAP)
put(ex, f"E{LT_EX + 3}", f"=E{LT_EX + 2}-E{LT_EX}", MOEDA0, F_B)
put(ex, f"G{LT_EX + 3}", f"=G{LT_EX + 2}-G{LT_EX}", MOEDA0, F_B)
put(ex, f"H{LT_EX + 3}", f"=G{LT_EX + 3}-E{LT_EX + 3}", '+"R$" #,##0;-"R$" #,##0;"-"', F_B)
for rr in (LT_EX + 2, LT_EX + 3):
    ex.row_dimensions[rr].height = 28
nota(ex, LT_EX + 5, "A folga não é lucro: no convênio, o que não se gasta volta como saldo ou vira mais exames por "
     "aditivo (estudo de custo de 20/10). Ela mostra que o custo a mais dos 12 meses cabe no valor do exame — desde "
     "que os itens SEM PREÇO não sejam grandes. A coluna de 12 meses usa os mesmos exames; se a gestão a mais sair dos "
     "exames (aba Gestão, A e B), o custo variável cai um pouco.", "I", 44)
ex.freeze_panes = "B5"

# ================================================================== Mapa do que muda
N_MA = "Mapa"
ma = aba(N_MA, [6, 26, 44, 50, 40, 16, 30])
titulo(ma, "Mapa: tudo o que muda com 12 meses, 6 polos de ultrassom e 3 de tomografia", "Uma linha por item. "
       "Frente: Convênio (o plano de trabalho que vai à SES), Execução (contratos e custo do ISHP, dentro do valor do "
       "exame) e Fila (demanda, controle interno). A coluna F traz o número das outras abas e muda com as premissas.",
       "G")
cab(ma, 4, ["#", "Frente e item", "Hoje (v26 assinada / carteira 1)", "Com a mudança", "Efeito",
            "Número (das outras abas)", "Onde (seção do plano ou contrato)"], h=36)
GA = lambda rot, k: f"='{N_GE}'!{GC[k][2]}{G_ROW[rot]}"  # noqa: E731
DIF = '+"R$" #,##0;-"R$" #,##0;"-"'
MAPA = [
    ("Convênio", None),
    ("Vigência", "8 meses", "12 meses", "todo item mensal da planilha custa 50% a mais se nada mudar", None, None,
     "1.9; 5.1; 7.1"),
    ("Gestão e apoio sem readequar", "22 postos + assessoria, R$ 119.520 por mês, 8,25% do global",
     "o mesmo quadro e os mesmos salários por 12 meses", "a mais no apoio",
     GA("Diferença para o apoio de hoje (R$)", "A"), DIF, "4.13; 8.2; 8.3"),
    ("Gestão e apoio readequada (P2, recomendada)", "—",
     "quadro pelo volume (16 postos + assessoria) e preços dos aprovados: Direção a R$ 10.200, Coordenação "
     "Assistencial a R$ 8.400, pré-exame a R$ 3.200, assessoria a R$ 3.700",
     "a mais no apoio, dentro de 8,5%", GA("Diferença para o apoio de hoje (R$)", "P2"), DIF, "4.13; 8.2; 8.3"),
    ("Quantidade de exames", "79.533 exames (carteira 1)", "o valor global não muda: o apoio a mais sai dos exames",
     "exames a mais ou a menos na P2", GA("Exames a mais (+) ou a menos (−), no valor médio", "P2"),
     '+#,##0;-#,##0;"0"', "2.2; 3.1; 6.1 (Metas 2 a 5); 8.2"),
    ("Parcelas", "3 parcelas: 3 + 3 + 2 meses", "4 trimestrais (ou 3 quadrimestrais), cada uma menor",
     "uma prestação de contas parcial a mais", None, None, "7.4; 7.5; 7.6"),
    ("Curva de produção", "3/8, 3/8 e 2/8 do quantitativo", "1/4 por trimestre", "—", None, None, "7.2"),
    ("Capacidade", "168 dias úteis; 20 salas; 5 tomógrafos (6 na v26)",
     "252 dias úteis; 2/3 dos exames por dia; salas da aba Salas; 3 tomógrafos", "ver Execução", None, None,
     "7.3 (reescrever o parágrafo dos \"seis equipamentos para carga de 3,33\")"),
    ("Local de execução da tomografia", "um tomógrafo por polo; a TC de um polo pode ir a outro",
     "TC em 3 polos; cada Região sem tomógrafo tem polo de referência (aba Tomografia)",
     "nenhum direto; risco de mais faltas pela distância", None, None, "3.4; 4.2; 7.3"),
    ("Preparo e triagem do contraste", "triagem no dia e acesso venoso, sem dizer onde (4.8)",
     "acesso venoso na sala de preparo, antes de o paciente entrar na sala do tomógrafo; orientação em grupo; "
     "sem jejum", "minutos de tomógrafo por exame com contraste, em linha", f"={FX_TC['linha']}", DEC1, "4.3; 4.8"),
    ("Equipe assistencial (quadro do plano)", "24 médicos de US; 7 radiologistas; 18 técnicos; 12 de enfermagem; "
     "retaguarda 6 por dia útil; 6 RT; 12 recepção",
     "médicos de US pela regra de 1.800 h por ano: 16; radiologistas: no mínimo 3; técnicos: 9; enfermagem: 6; "
     "retaguarda por 252 dias; RT e recepção iguais",
     "no valor do exame; o que é por dia ou por mês sobe 50%", None, None, "4.15"),
    ("Proteção radiológica", "blindagem e levantamento radiométrico nos polos com TC; testes de cada tomógrafo",
     "só nos 3 polos com TC", "menos documentos na formalização", None, None, "4.16 (b) e (d)"),
    ("Metas e relatórios", "Meta 1: 6 polos por 8 meses; Meta 6: 8 relatórios mensais",
     "6 polos por 12 meses; 12 relatórios mensais", "—", None, None, "5.2; 6.1; 6.2"),
    ("Riscos", "R-01 fala em seis tomógrafos e oito meses",
     "R-01 com 3 tomógrafos e o tempo do contraste; R-14 (preço muda na vigência) fica mais provável; risco novo: "
     "deslocamento às Regiões com TC", "—", None, None, "7.8; 7.9"),
    ("Documento assinado", "PT v1 assinado (23/10 e 27/10) com 8 meses",
     "nova versão (v27), nova assinatura e reenvio à SES; juntar com a troca de preço para a Candanga",
     "—", None, None, "versoes/; recebidos/"),
    ("Execução", None),
    ("Aluguel de salas e aparelhos de US", "20 salas × 8 meses = 160 salas-mês",
     "menos salas por mais meses (aba Salas): as salas-mês sobem pelo arredondamento por polo",
     "a mais em sala, aparelho e fixos da sala", f"='{N_EX}'!H6+'{N_EX}'!H7+'{N_EX}'!H8", DIF, "contratos de locação"),
    ("Salas com o preparo em paralelo", "—", "vestiário, bexiga cheia na espera e chamada antecipada",
     "salas em 12 meses, polo a polo", f"='{N_SA}'!M11", INT, "contratos de locação; aba Fluxo"),
    ("Contratos de locação das salas", "13 salas negociadas (20/10), prazo de 8 meses",
     "prazo de 12 meses; faltam salas no Sul (Gama tem 1) e sobra na Asa Sul (aba Salas)",
     "salas adotadas menos as dos contratos", f"='{N_SA}'!K11", '+#,##0;-#,##0;"0"', "contratos"),
    ("Recepção", "12 recepcionistas × 8 meses", "12 × 12 meses", "a mais", f"='{N_EX}'!H10", DIF,
     "contratos de trabalho"),
    ("RT, retaguarda médica e custos do polo", "sem preço", "50% a mais (504 dias-polo a mais de retaguarda)",
     "a mais (zero enquanto não houver preço)", f"='{N_EX}'!H11+'{N_EX}'!H12+'{N_EX}'!H13", DIF, "contratos médicos"),
    ("Médicos de ultrassom", "por exame (R$ 1.000 por 30 exames)", "o mesmo por exame, 1/3 menos exames por mês",
     "nenhum direto; risco de o médico pedir mínimo por turno", None, None, "contratos médicos"),
    ("Tomografia na clínica", "5 tomógrafos, cerca de 360 exames por mês cada",
     "3 tomógrafos, com mais exames por mês cada (número ao lado)", "exames por mês por tomógrafo",
     f"='{N_TC}'!C17", INT, "contrato com a clínica parceira"),
    ("Preço da tomografia com volume", "R$ 165 a R$ 175, contraste incluído", "a negociar (Premissas)",
     "diferença no custo da tomografia", f"='{N_EX}'!H19", DIF, "contrato com a clínica parceira"),
    ("Meses de tomografia com 3 tomógrafos", "—", "em série (20 min) e em linha (aba Meses e tomógrafos)",
     "meses no fluxo em linha", f"={ME_LINHA3}", DEC1, "contrato com a clínica; R-01"),
    ("Sala de preparo do contraste na clínica", "não pedida", "poltronas, enfermagem dedicada, bomba pronta, "
     "radiologista no serviço durante as injeções", "poltronas por tomógrafo (aba Fluxo)", None, None,
     "contrato com a clínica parceira"),
    ("Reajuste de salários (data-base)", "pode cair nos 8 meses", "mais provável em 12 meses, e com mais meses depois",
     "reserva na P2, fora do convênio", GA("Reajuste da data-base no período, fora do convênio (R$)", "P2"),
     MOEDA0, "convenção coletiva de cada cargo"),
    ("Contratos de trabalho", "prazo determinado de 8 meses", "prazo determinado de 12 meses",
     "férias e 13º proporcionais já estão no custo com encargos", None, None, "contratos de trabalho"),
    ("Fila", None),
    ("Ritmo", "cerca de 9.900 exames por mês", "cerca de 6.600 exames por mês",
     "—", None, None, "a fila cai mais devagar; as entradas continuam"),
    ("Pedidos novos", "1.490 pedidos novos esperados em 8 meses (carteira 1)", "cerca de 1,5 vez mais em 12 meses",
     "as linhas de pedidos novos ficam mais seguras", None, None, "estudo das filas, seções 3 e 7"),
    ("Conversão para sem contraste", "a fila diz com contraste", "parte o radiologista faz sem contraste",
     "parte convertida (Premissas)", f"={P['conv']}", PCT, "4.8; Meta 5 não muda (mesmo código)"),
    ("Faltas", "agenda apertada para repor as faltas", "mais pacientes na fila para cada vaga do mês",
     "reposição mais fácil", None, None, "controle interno"),
]
l = 5
n = 0
for it in MAPA:
    if it[1] is None:
        put(ma, f"A{l}", "", fill=CAB)
        put(ma, f"B{l}", it[0], font=F_S, fill=CAB)
        for c_ in "CDEFG":
            put(ma, f"{c_}{l}", "", fill=CAB)
        l += 1
        continue
    n += 1
    item, hoje, prop, efeito, num, fmt, onde = it
    put(ma, f"A{l}", n, INT, al=CEN)
    put(ma, f"B{l}", item, font=F_B, al=WRAP)
    put(ma, f"C{l}", hoje, al=WRAP)
    put(ma, f"D{l}", prop, al=WRAP)
    put(ma, f"E{l}", efeito, al=WRAP)
    put(ma, f"F{l}", num if num else "", fmt, F_LK if num else F_N)
    put(ma, f"G{l}", onde, font=F_I, al=WRAP)
    ma.row_dimensions[l].height = 58
    l += 1
ma.freeze_panes = "C5"

# ================================================================== Decisões
N_DE = "Decisões"
de = aba(N_DE, [6, 44, 62, 52])
titulo(de, "O que precisa ser decidido", "Na ordem em que travam o resto. A coluna da direita é a recomendação do "
       "estudo; a decisão é do usuário e da equipe.", "D")
cab(de, 4, ["#", "Decisão", "Opções", "Recomendação"], h=24)
DEC = [
    ("O quadro de gestão em 12 meses, dentro de 8,5%", "P1 (o mesmo quadro, salários cortados por igual), P2 (quadro "
     "pelo volume e preços dos aprovados), P3 (salários de hoje, menos postos)",
     "P2: fica em 8,44%, nenhum preço abaixo do menor aprovado, e a carga por operador fica abaixo da de hoje"),
    ("O fluxo da tomografia com contraste na clínica", "em série (tudo na sala) ou em linha (acesso venoso na sala de "
     "preparo, pacientes prontos à espera)", "em linha: é o que faz 3 tomógrafos sobrarem em 12 meses; pôr no "
     "contrato a sala de preparo, a enfermagem e o radiologista durante as injeções"),
    ("O tempo real do contraste na clínica", "minutos de tomógrafo por exame em série e em linha; janela do contraste; "
     "jejum; creatinina; repouso", "medir no mês 1, por escrito, e ajustar as Premissas"),
    ("Quais 3 polos de tomografia e para onde vai cada Região", "o arranjo de exemplo (Ceilândia, Taguatinga, Plano "
     "Piloto) fica em cerca de 79% cada no fluxo em série", "escolher pela rede da clínica parceira e testar na aba "
     "Tomografia"),
    ("Quanto tempo a tomografia corre", "os 12 meses inteiros, em um turno por dia, ou menos meses no dia inteiro",
     "os 12 meses em um turno com radiologista presente: dá folga para remarcação e falha de equipamento"),
    ("Salas de ultrassom", "as necessárias por polo, com ou sem o preparo em paralelo, ou as 13 dos contratos com "
     "ajuste no Sul", "contratar por 12 meses as da aba Salas com o preparo em paralelo, e negociar sala por turno "
     "onde a carga não enche uma sala"),
    ("Parcelas", "4 trimestrais ou 3 quadrimestrais", "4 trimestrais, na lógica da v26"),
    ("Mês de início e data-base", "a data-base de cada cargo e o mês provável da celebração",
     "levantar para pôr a reserva de reajuste no custo interno"),
    ("Preço da tomografia com volume", "o preço por exame com 3 polos, com o contraste incluído",
     "pôr no contrato o contraste incluído e o prazo do laudo"),
]
for i, (d, o, rec) in enumerate(DEC):
    l = 5 + i
    put(de, f"A{l}", i + 1, INT, al=CEN)
    put(de, f"B{l}", d, font=F_B, al=WRAP)
    put(de, f"C{l}", o, al=WRAP)
    put(de, f"D{l}", rec, al=WRAP)
    de.row_dimensions[l].height = 58

# ================================================================== Leia (primeira aba)
N_LE = "Leia"
le = aba(N_LE, [70, 18, 18, 56])
titulo(le, "Plano 4: 12 meses, 6 polos de ultrassom e 3 de tomografia", "Estudo interno de 07/11/2026, sobre a "
       "carteira 1 (Candanga, 79.533 exames) e o quadro da v26. Responde: o que muda em custo, como readequar a gestão "
       "para caber no teto, como o fluxo de atendimento rende mais e quantos meses a tomografia leva. Nada daqui vai "
       "ao plano sem decisão do usuário.", "D")
cab(le, 4, ["Resposta curta", "Hoje", "Proposta", "Onde ver"], h=24)
GG = lambda rot, k: f"='{N_GE}'!{GC[k][2]}{G_ROW[rot]}"  # noqa: E731
LEIA = [
    ("Apoio da gestão (R$): hoje · 12 meses sem readequar", GG("Apoio no período (R$)", "hoje"),
     GG("Apoio no período (R$)", "A"), MOEDA0, "Gestão"),
    ("… parte do valor global", GG("Parte do valor global", "hoje"), GG("Parte do valor global", "A"), '0.00%', ""),
    ("Apoio da gestão readequada, P2 (R$)", GG("Apoio no período (R$)", "hoje"), GG("Apoio no período (R$)", "P2"),
     MOEDA0, "Gestão, P2 (recomendada)"),
    ("… parte do valor global", GG("Parte do valor global", "hoje"), GG("Parte do valor global", "P2"), '0.00%', ""),
    ("… a mais sobre o apoio de hoje (%)", "", GG("Diferença para o apoio de hoje (%)", "P2"), '+0.0%;-0.0%;"0"', ""),
    ("Custo por mês da gestão: quanto precisa cair para ficar igual a hoje · para caber em 8,5%",
     f"='{N_GE}'!C{G_RESP_FIM - 5}", f"='{N_GE}'!C{G_RESP_FIM - 4}", '0.0%', "Gestão, os 4 meses em %"),
    ("Salas de ultrassom em 12 meses: na agenda do CBR · com o preparo em paralelo", f"='{N_SA}'!F11",
     f"='{N_SA}'!M11", INT, "Salas e Fluxo"),
    ("Minutos de tomógrafo por exame com contraste: em série · em linha", f"={FX_TC['serie']}", f"={FX_TC['linha']}",
     DEC1, "Fluxo"),
    ("Meses para toda a tomografia com 3 tomógrafos: em série · em linha", f"={ME_SERIE3}", f"={ME_LINHA3}", DEC1,
     "Meses e tomógrafos"),
    ("Horas por dia de cada tomógrafo para fechar em 12 meses: em série · em linha", f"={ME_HORAS3_SERIE}",
     f"={ME_HORAS3_LINHA}", DEC1, "Meses e tomógrafos"),
    ("Tomógrafos necessários em 12 meses, em série (Tomografia)", f"='{N_TC}'!C15", "", INT, "Tomografia"),
    ("Custo de executar a mais em 12 meses (R$)", "", f"='{N_EX}'!H{LT_EX}", MOEDA0,
     "Execução (sem os itens SEM PREÇO)"),
]
for i, (rot, fh, fp, fmt, onde) in enumerate(LEIA):
    l = 5 + i
    put(le, f"A{l}", rot, font=F_B if not rot.startswith("…") else F_N, al=WRAP)
    put(le, f"B{l}", fh, fmt, F_LK)
    put(le, f"C{l}", fp, fmt, F_LK)
    put(le, f"D{l}", onde, font=F_I)
    le.row_dimensions[l].height = 28
l = 5 + len(LEIA) + 1
secao(le, l, "As abas")
for nome, t in [
    ("Premissas", "tudo que dá para mudar, com a fonte; os itens SEM PREÇO estão em vermelho"),
    ("Gestão", "o quadro em cinco cenários, os preços de mercado e dos aprovados, e os 4 meses a mais em %"),
    ("Salas", "salas de ultrassom por polo, 8 contra 12 meses, com e sem o preparo em paralelo"),
    ("Tomografia", "a carga dos 3 tomógrafos em série, as grades do tempo do contraste e o arranjo dos 3 polos"),
    ("Fluxo", "o atendimento de cada grupo de ultrassom e os três fluxos da tomografia"),
    ("Meses e tomógrafos", "quantos meses a tomografia leva com 3, 4 ou 5 tomógrafos, e a conversão"),
    ("Execução", "o custo de executar item a item: o que sobe com os meses e o que não muda"),
    ("Mapa", "tudo que muda, frente a frente, com a seção do plano"),
    ("Decisões", "o que falta decidir, na ordem"),
]:
    l += 1
    put(le, f"A{l}", nome, font=F_B)
    put(le, f"B{l}", t, font=F_I, borda=False)
l += 2
nota(le, l, "Legenda: amarelo com número azul = premissa (mude); verde = vem de outra aba; preto = conta. Fonte da "
     "carteira: estudos/estudo_filas_imagem_20261102.json. Gerada por estudos/gerar_estudo_12_meses_3_tomografos_"
     "20261107.py.", "D", 30)

ORDEM = [N_LE, N_PR, N_GE, N_SA, N_TC, N_FX, N_ME, N_EX, N_MA, N_DE]
wb._sheets = [wb[n] for n in ORDEM]
wb.active = 0
wb.save(SAIDA)
print(SAIDA)
