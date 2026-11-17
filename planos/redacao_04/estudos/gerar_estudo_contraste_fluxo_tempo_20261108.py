"""Contraste na tomografia: tempo, fluxo e regras (08/11/2026, pedido do usuário).

Pesquisa sobre o exame com contraste (tempo de tomógrafo, fluxo do usuário, normas e diretrizes, segurança e
conversão para sem contraste) e análise com os números da v26 e da carteira 1.

Tudo o que é conta é fórmula. As células amarelas (fonte azul) são premissas que podem ser mudadas; a fonte verde
marca o que vem de outra aba. Recalcular depois de gerar:
    python3.11 <skill xlsx>/scripts/recalc.py estudo_contraste_fluxo_tempo_20261108.xlsx 90
"""
import os

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.datavalidation import DataValidation

AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(AQUI, "estudo_contraste_fluxo_tempo_20261108.xlsx")

# ------------------------------------------------------------------ estilo (o mesmo dos estudos de 05/11 e 07/11)
A = "Arial"
F = Font(name=A, size=10)
F_B = Font(name=A, size=10, bold=True)
F_T = Font(name=A, size=13, bold=True)
F_S = Font(name=A, size=9, italic=True, color="555555")
F_IN = Font(name=A, size=10, color="0000FF")
F_LK = Font(name=A, size=10, color="008000")
F_LKB = Font(name=A, size=10, color="008000", bold=True)
F_URL = Font(name=A, size=9, color="1F4E79")
AMARELO = PatternFill("solid", fgColor="FFF2CC")
CAB = PatternFill("solid", fgColor="D9E1F2")
SEC = PatternFill("solid", fgColor="E2EFDA")
TOT = PatternFill("solid", fgColor="EDEDED")
BORDA = Border(*(Side(style="thin", color="BFBFBF"),) * 4)
TOPO = Alignment(vertical="top", wrap_text=True)
INT, DEC1, DEC2, PCT, PCT2 = "#,##0", "#,##0.0", "#,##0.00", "0.0%", "0.00%"
MOEDA = '"R$" #,##0.00'

wb = Workbook()


def aba(nome, larguras):
    ws = wb.create_sheet(nome)
    ws.sheet_view.showGridLines = False
    for col, w in zip("ABCDEFGHIJKLMNOPQ", larguras):
        ws.column_dimensions[col].width = w
    return ws


def put(ws, ref, v, fmt=None, font=F, fill=None, borda=True):
    c = ws[ref]
    c.value = v
    c.font = font
    c.alignment = TOPO
    if borda:
        c.border = BORDA
    if fill:
        c.fill = fill
    if fmt:
        c.number_format = fmt
    return c


def entrada(ws, ref, v, fmt=None):
    return put(ws, ref, v, fmt, F_IN, AMARELO)


def link(ws, ref, formula, fmt=None, bold=False):
    return put(ws, ref, formula, fmt, F_LKB if bold else F_LK)


def titulo(ws, t, sub):
    put(ws, "A1", t, font=F_T, borda=False)
    put(ws, "A2", sub, font=F_S, borda=False)


def cab(ws, r, rotulos, col0="A"):
    for i, t in enumerate(rotulos):
        put(ws, f"{chr(ord(col0) + i)}{r}", t, font=F_B, fill=CAB)


def secao(ws, r, t, ncol):
    for i in range(ncol):
        put(ws, f"{chr(ord('A') + i)}{r}", t if i == 0 else None, font=F_B, fill=SEC)


def nota(ws, r, t, col="A"):
    put(ws, f"{col}{r}", t, font=F_S, borda=False)


# ================================================================== aba 2: fluxos (montada antes: as outras ligam nela)
FLUXOS = {
    "A": ("A. Tomografia sem contraste", [
        ("Recepção", "identificação, documento e pedido", "recepção", 3, 5, 8, "não",
         "HC-UFMG: 3 min (Santos Junior, 2024)"),
        ("Conferência", "questionário e gestação, nas usuárias", "enfermagem", 3, 5, 8, "não", "v26, 4.8"),
        ("Troca de roupa", "metais e avental", "usuário", 2, 3, 5, "não", "estimativa"),
        ("Exame na sala", "posicionar, adquirir as imagens e sair", "técnico em radiologia", 8, 9, 13, "sim",
         "Erdfarb 2005: 8,6 min na sala (DP 4,2)"),
        ("Troca de usuário", "limpar a mesa e chamar o próximo", "técnico em radiologia", 1, 2, 4, "sim",
         "Stenson 2021: 3,6 min de sala vazia (mediana, com espera); POP HC-UFG: limpeza a cada exame"),
    ]),
    "B": ("B. Com contraste em série: punção na mesa do tomógrafo (a conta da v26)", [
        ("Recepção", "identificação, documento e pedido", "recepção", 3, 5, 8, "não", "HC-UFMG"),
        ("Triagem e termo", "alergia, rim, metformina, gestação; termo lido e assinado", "enfermagem e médico",
         5, 10, 15, "não", "HC-UFMG: o termo leva 15 min quando o usuário preenche sozinho"),
        ("Troca de roupa", "metais e avental", "usuário", 2, 3, 5, "não", "estimativa"),
        ("Punção na mesa", "cateter 20G ou maior e teste com soro", "enfermagem", 5, 7, 15, "sim",
         "Kingston: cerca de 8 min por punção feita no serviço; AMC: tirar a punção da sala poupa 5 min"),
        ("Exame com contraste", "posicionar, conectar à bomba, adquirir as fases, desconectar e sair",
         "técnico em radiologia e enfermagem", 9, 11, 15, "sim",
         "Erdfarb 2005: 17,1 min na sala no exame com contraste (DP 7,4), com a punção quando feita na sala"),
        ("Troca de usuário", "limpar a mesa e chamar o próximo", "técnico em radiologia", 1, 2, 4, "sim",
         "Stenson 2021"),
        ("Observação", "repouso com o acesso venoso mantido", "enfermagem; médico no serviço", 20, 30, 30, "não",
         "ACR 2026: quase toda reação grave nos primeiros 20 min; bulas do contraste e ESUR v10: 30 min"),
        ("Alta", "retirada do acesso e orientação", "enfermagem", 2, 3, 5, "não", "estimativa"),
    ]),
    "C": ("C. Com contraste em linha: punção na sala de preparo, com o próximo usuário pronto", [
        ("Recepção", "o usuário chega cerca de 40 min antes do horário do tomógrafo", "recepção", 3, 5, 8, "não",
         "estudo de 07/11"),
        ("Orientação em grupo", "3 a 5 usuários: o contraste, o calor na injeção, o repouso; leitura do termo",
         "enfermagem", 3, 4, 6, "não", "uma sessão de 15 a 20 min dividida pelo grupo; a UFMG propõe entregar o "
         "termo antes do dia"),
        ("Triagem e assinatura", "alergia, rim, metformina, gestação; assinatura do termo", "enfermagem",
         3, 5, 8, "não", "v26, 4.8"),
        ("Troca de roupa", "metais e avental", "usuário", 2, 3, 5, "não", "estimativa"),
        ("Punção na sala de preparo", "cateter 20G ou maior e teste com soro; o usuário fica sentado e pronto",
         "enfermagem", 5, 7, 15, "não", "Kingston: cerca de 8 min por punção"),
        ("Espera pronto", "um ou dois usuários com acesso, para o tomógrafo não parar", "usuário", 5, 15, 30,
         "não", "estudo de 07/11"),
        ("Exame com contraste", "posicionar, conectar à bomba, adquirir as fases, desconectar e sair",
         "técnico em radiologia", 10, 13, 15, "sim",
         "Stenson 2021: 12,1 min na sala (mediana, PS); HC-UFMG: 15 min (média) com o acesso feito antes; 07/11: 13"),
        ("Troca de usuário", "limpar a mesa e chamar o próximo", "técnico em radiologia", 1, 2, 4, "sim",
         "Stenson 2021"),
        ("Observação", "repouso com o acesso venoso mantido", "enfermagem; médico no serviço", 20, 30, 30, "não",
         "ACR 2026; bulas do contraste; ESUR"),
        ("Alta", "retirada do acesso e orientação", "enfermagem", 2, 3, 5, "não", "estimativa"),
    ]),
    "D": ("D. Angiotomografia de coronárias (só na v26), com a frequência controlada fora da sala", [
        ("Recepção", "identificação, documento e pedido", "recepção", 3, 5, 8, "não", "HC-UFMG"),
        ("Triagem, termo e ECG", "frequência, ritmo, contraindicação ao betabloqueador e ao nitrato",
         "enfermagem e médico", 5, 10, 15, "não", "estimativa"),
        ("Controle da frequência", "betabloqueador oral cerca de 1 h antes, ou venoso na sala de preparo",
         "médico e enfermagem", 15, 45, 60, "não",
         "ensaio de 2011: 120 min no total com o oral, 35 com o venoso; fabricante: o oral soma cerca de 1 h"),
        ("Punção", "cateter 18G a 20G na dobra do cotovelo, para 4 mL/s ou mais", "enfermagem", 5, 7, 15, "não",
         "CBR 2021: 4 mL/s ou mais; ACR 2026: 20G ou maior a partir de 3 mL/s"),
        ("Exame na sala", "eletrodos, nitrato, teste do bolo, aquisição e saída", "técnico, enfermagem e médico",
         12, 18, 30, "sim", "aquisição de 7 a 12 min (mediana, resumo 13323)"),
        ("Troca de usuário", "limpar a mesa e chamar o próximo", "técnico em radiologia", 1, 2, 4, "sim",
         "Stenson 2021"),
        ("Observação", "repouso com o acesso venoso mantido", "enfermagem; médico no serviço", 20, 30, 30, "não",
         "ACR 2026; bulas do contraste; ESUR"),
        ("Alta", "retirada do acesso e orientação", "enfermagem", 2, 3, 5, "não", "estimativa"),
    ]),
    "E": ("E. Com contraste em linha, com as medidas que agilizam (aba 8)", [
        ("Recepção", "cadastro e documento conferidos na véspera (4.6); só a identificação", "recepção", 2, 3, 5,
         "não", "Temple: formulários consolidados; v26, 4.6"),
        ("Orientação em grupo", "o termo já foi lido no contato do pré-exame; aqui só as dúvidas", "enfermagem",
         2, 3, 5, "não", "HC-UFMG: o termo leva 15 min quando lido só no dia"),
        ("Triagem e assinatura", "questionário respondido por telefone no pré-exame; a enfermagem confirma",
         "enfermagem", 2, 3, 5, "não", "Temple: o pedido revisado 3 dias antes"),
        ("Troca de roupa", "metais e avental", "usuário", 2, 3, 5, "não", "estimativa"),
        ("Punção na sala de preparo", "enfermeiro na veia difícil, com ultrassom se preciso", "enfermagem",
         4, 6, 12, "não", "ultrassom: acerto na 1ª tentativa cerca de 3 vezes mais provável (meta-análise 2023)"),
        ("Espera pronto", "um ou dois usuários prontos na porta, já trocados e puncionados", "usuário",
         5, 10, 20, "não", "UMass: estação de punção ao lado do tomógrafo, espera 20% menor"),
        ("Exame com contraste", "bomba carregada antes de o usuário entrar; protocolo definido na véspera",
         "técnico em radiologia", 9, 11, 13, "sim",
         "Stenson 2021: 12,1 min (mediana, PS); fabricantes: bomba pronta poupa de 40 s a 3 min"),
        ("Troca de usuário", "o próximo já na porta", "técnico em radiologia", 1, 2, 3, "sim", "Stenson 2021"),
        ("Observação", "repouso com o acesso venoso mantido, fora da sala de preparo",
         "enfermagem; médico no serviço", 20, 30, 30, "não", "ACR 2026; bulas do contraste; ESUR"),
        ("Alta", "retirada do acesso; orientação escrita sobre reação tardia", "enfermagem", 2, 3, 5, "não",
         "estimativa"),
    ]),
}

fx = aba("2 Fluxo", [24, 46, 24, 9, 10, 9, 11, 62])
titulo(fx, "Fluxo do usuário e tempo de tomógrafo, passo a passo",
       "Minutos por passo: mínimo, central (amarelo, pode mudar) e máximo. Só os passos marcados \"sim\" ocupam "
       "o tomógrafo. As fontes estão na aba 1 e na aba Fontes.")

TOM, USU, PASSO = {}, {}, {}
r = 13
for k, (nome, passos) in FLUXOS.items():
    secao(fx, r, nome, 8)
    cab(fx, r + 1, ["Passo", "O que acontece", "Quem faz", "Mínimo", "Central", "Máximo", "Ocupa o tomógrafo?",
                    "De onde vem"])
    a = r + 2
    for i, (p, o, q, mn, ce, mx, oc, fo) in enumerate(passos):
        l = a + i
        put(fx, f"A{l}", p)
        put(fx, f"B{l}", o)
        put(fx, f"C{l}", q)
        put(fx, f"D{l}", mn, INT)
        entrada(fx, f"E{l}", ce, INT)
        put(fx, f"F{l}", mx, INT)
        put(fx, f"G{l}", oc, font=F_B if oc == "sim" else F)
        put(fx, f"H{l}", fo, font=F_S)
        PASSO[(k, p)] = l
    b = a + len(passos) - 1
    t = b + 1
    put(fx, f"A{t}", "Minutos de tomógrafo por exame", font=F_B, fill=TOT)
    for c in "BC":
        put(fx, f"{c}{t}", None, fill=TOT)
    for c in "DEF":
        put(fx, f"{c}{t}", f'=SUMIF($G${a}:$G${b},"sim",{c}{a}:{c}{b})', INT, F_B, TOT)
    put(fx, f"A{t + 1}", "Exames por hora de tomógrafo", font=F_B)
    for c in "DEF":
        put(fx, f"{c}{t + 1}", f"=60/{c}{t}", DEC1, F_B)
    put(fx, f"A{t + 2}", "Tempo do usuário no polo (min)", font=F_B)
    for c in "DEF":
        put(fx, f"{c}{t + 2}", f"=SUM({c}{a}:{c}{b})", INT, F_B)
    TOM[k], USU[k] = t, t + 2
    r = t + 4

# resumo no topo da aba 2
cab(fx, 4, ["Fluxo", "", "", "Mínimo", "Central", "Máximo", "Exames/h", "Tempo do usuário no polo (central) e "
            "comparação com a v26"])
v26_txt = {"A": "a v26 conta 15 min", "B": "a v26 conta 20 min para todo exame com contraste",
           "C": "o estudo de 07/11 conta 13 min", "D": "a v26 conta 20 min; o estudo de 05/11, 30",
           "E": "a v26 conta 20 min"}
for i, k in enumerate("ABCDE"):
    l = 5 + i
    put(fx, f"A{l}", FLUXOS[k][0].split(":")[0].split(" (")[0], font=F_B)
    put(fx, f"B{l}", None)
    put(fx, f"C{l}", None)
    for c in "DEF":
        link(fx, f"{c}{l}", f"={c}{TOM[k]}", INT, bold=(c == "E"))
    link(fx, f"G{l}", f"=E{TOM[k] + 1}", DEC1)
    link(fx, f"H{l}", f'=TEXT(E{USU[k]},"0")&" min no polo; "&"{v26_txt[k]}"')
nota(fx, 10, "Os minutos de tomógrafo são os do exame na sala mais a troca de usuário. Observação, punção na sala de "
             "preparo e espera não ocupam o tomógrafo.")
nota(fx, 11, "O tempo do usuário no polo soma os passos; não conta a espera entre a chegada e a chamada, que depende "
             "da agenda (no HC-UFMG, cerca de 20 min).")

# ================================================================== aba 1: tempos medidos (evidência)
ev = aba("1 Tempos medidos", [30, 34, 34, 13, 13, 52, 22])
titulo(ev, "Quanto tempo o exame ocupa o tomógrafo: o que foi medido",
       "Pesquisa de 08/11/2026. Minutos por exame. Os links estão na aba Fontes.")
cab(ev, 4, ["Fonte", "Onde e quando", "O que mediu", "Com contraste (min)", "Sem contraste (min)",
            "Outros números", "Como foi lida"])
EVID = [
    ("Erdfarb, Forman e Tocino", "hospital universitário (Yale, EUA); RSNA 2005 e tese de 2006; 225 usuários, "
     "202 h de tomógrafo", "tempo na sala, da entrada à saída", 17.1, 8.6,
     "DP 7,4 (n 104) e 4,2 (n 114); média geral 12,6 = preparo 5,0 + aquisição 5,1 + saída 2,6. Tomógrafo ativo "
     "em 31% do tempo; 78% do tempo parado veio do fluxo de usuários", "resumos (congresso e tese)"),
    ("Stenson et al.", "pronto-socorro de Boston (BIDMC); Am J Emerg Med 2021", "tempo na sala e sala vazia",
     None, None, "12,1 min na sala (mediana, todos os exames) + 3,6 min de sala vazia; 3,2 exames/h observados, "
     "máximo teórico de 3,8", "resumo e trechos"),
    ("Santos Junior (dissertação)", "HC-UFMG, Belo Horizonte, 2023 e 2024; 2 tomógrafos", "fluxo do ambulatório, "
     "com o acesso venoso feito na sala de preparo", 15, None, "15 min na sala (média; 10 a 20). Capacidade "
     "calculada com 20 min (3/h, 12 h/dia, 72/dia). Termo: 15 min; espera: 20; preparo: 15 a 30; laudo: 30. "
     "Sem médico à noite, tudo é sem contraste", "texto completo"),
    ("Chang et al. (Kingston, Reino Unido)", "auditoria de 4 semanas, 1.458 TC", "punção feita pelo serviço", 8,
     None, "160 min em 20 punções. Vagas de 10 min (ambulatório) e 15 (internação e PS)", "notícia (AuntMinnie)"),
    ("Elkhuizen et al.", "AMC, Amsterdam; Health Care Manage Rev 2007", "punção tirada da sala para uma sala de "
     "preparo", None, None, "5 min a menos no tempo de atravessamento; uso do tomógrafo de 44% para 51%; espera "
     "pelo exame de 21 para menos de 5 dias", "resumo"),
    ("Zimmerman et al.", "7 serviços dos EUA; J Cardiovasc Comput Tomogr 2021; 54 usuários",
     "processo inteiro: preparo, exame, monitoração e imagem", 37, None,
     "angio de coronárias: 121 min (3,2 vezes a TC de tórax com contraste)", "resumo"),
    ("Resumo 13323 (angio de coronárias)", "serviço dos EUA", "angio coronária sem betabloqueador",
     None, None, "aquisição de 12 para 7 min (mediana); atendimento de 94 para 69 min", "resumo de congresso"),
    ("Ensaio oral × venoso (Radiología, 2011)", "Espanha, 40 usuários", "tempo total da angio coronária",
     None, None, "120 min com betabloqueador oral, 35 com venoso; tempo na sala igual", "resumo"),
    ("Watson Clinic (relato)", "EUA", "Lean na tomografia", None, None,
     "de 2,0 para 3,3 usuários por hora em cada tomógrafo", "relato de consultoria"),
    ("Manchester (UHSM)", "NHS, 2 tomógrafos", "produção por hora", None, None,
     "1,6 exame na primeira hora (8 às 9 h) contra 5,7 por hora no resto do dia, os dois juntos", "notícia"),
    ("CDA-AMC (Canadá)", "173 serviços, 2022 e 2023", "exames por hora aberta", None, None,
     "2,34 por hora (1,89 a 3,43 entre províncias); em 2007, 3,0", "relatório técnico"),
    ("CIHI 2007, citado pelo Ministério da Saúde", "hospitais do Canadá", "exames por hora de funcionamento",
     None, None, "3,1 (64 canais), 3,0 (16) e 3,2 (4 e 8): o preparo pesa mais que a máquina",
     "documento do MS (texto completo)"),
    ("Ministério da Saúde, Parâmetros SUS (NESCON/UFMG, 2013)", "Brasil", "capacidade por tomógrafo", None, None,
     "7.000 exames por ano por tomógrafo; no SUS em 2012, 2.569 exames por tomógrafo SUS", "texto completo"),
    ("Santos et al., Cad Saúde Pública 2014", "Brasil, 2009", "parâmetro de planejamento", 30, None,
     "2 exames por hora; uso de 14% dos tomógrafos públicos", "texto"),
    ("v26 (PT v1)", "plano enviado à SES", "premissa", 20, 15, "4.478 h de tomógrafo; carga de 3,33 tomógrafos de 6",
     "plano"),
    ("Estudo de 07/11", "interno", "hipótese do fluxo em linha", 13, 10, "o ganho da sala de preparo, a medir",
     "estudo"),
]
for i, (a_, b_, c_, d_, e_, f_, g_) in enumerate(EVID):
    l = 5 + i
    put(ev, f"A{l}", a_, font=F_B)
    put(ev, f"B{l}", b_)
    put(ev, f"C{l}", c_)
    put(ev, f"D{l}", d_, DEC1)
    put(ev, f"E{l}", e_, DEC1)
    put(ev, f"F{l}", f_)
    put(ev, f"G{l}", g_, font=F_S)
l = 5 + len(EVID) + 1
put(ev, f"A{l}", "Leitura", font=F_B, borda=False)
for j, t in enumerate([
    "Sem contraste, o tomógrafo fica ocupado cerca de 9 a 11 min por exame. A v26 conta 15.",
    "Com contraste e punção na mesa, são 17 a 20 min. Os 20 min da v26 estão certos para esse fluxo.",
    "Com o acesso feito antes, ficam 12 a 15 min. Os 13 min do estudo de 07/11 são o piso, e 15 é o valor central.",
    "A produção boa é de cerca de 3 exames por hora por tomógrafo. O que trava é o fluxo, não a máquina: o "
    "tomógrafo de Yale ficou parado 69% do tempo, quase sempre por falha no fluxo de usuários.",
]):
    nota(ev, l + 1 + j, f"{j + 1}. {t}")

# ================================================================== aba 3: capacidade
cp = aba("3 Capacidade", [58, 15, 15, 15, 15, 15, 15])
titulo(cp, "Horas de tomógrafo com os tempos medidos",
       "Escolha a base em B4. Os minutos vêm da aba 2 (verde), salvo os da v26, que são os do plano (amarelo).")
put(cp, "A4", "Base de exames (v26 ou carteira 1)", font=F_B)
entrada(cp, "B4", "v26")
dv = DataValidation(type="list", formula1='"v26,carteira 1"', allow_blank=False)
cp.add_data_validation(dv)
dv.add("B4")
cab(cp, 6, ["Grupo de exames", "v26", "carteira 1", "Usada"])
GRUPOS = [
    ("Com contraste que podem ir sem contraste (abdômen, pelve, tórax; na carteira 1, também pescoço, face e "
     "crânio)", 11482, 11700),
    ("Angiotomografias (não vão sem contraste)", 0, 2353),
    ("Angiotomografia de coronárias", 1408, 0),
    ("Sem contraste", 728, 348),
]
for i, (n, v1, v2) in enumerate(GRUPOS):
    l = 7 + i
    put(cp, f"A{l}", n)
    entrada(cp, f"B{l}", v1, INT)
    entrada(cp, f"C{l}", v2, INT)
    put(cp, f"D{l}", f'=IF($B$4="carteira 1",C{l},B{l})', INT, F_B)
put(cp, "A11", "Total de tomografias", font=F_B, fill=TOT)
for c in "BCD":
    put(cp, f"{c}11", f"=SUM({c}7:{c}10)", INT, F_B, TOT)
nota(cp, 12, "v26: abdômen 4.516, pelve 3.862 e tórax 3.104 com contraste (tc_dados_basicos_v26_20261105.xlsx). "
             "Carteira 1: estudo das filas de 02/11, cenário 1.")

PREM = [("Tomógrafos", 6, INT), ("Meses", 8, INT), ("Dias úteis por mês", 21, INT),
        ("Horas abertas por dia", 10, INT), ("Parte das horas com exame", 0.8, PCT),
        ("Parte dos pedidos com contraste que o radiologista faz sem contraste", 0.10, PCT)]
cab(cp, 14, ["Premissa", "Valor"])
for i, (n, v, fm) in enumerate(PREM):
    put(cp, f"A{15 + i}", n)
    entrada(cp, f"B{15 + i}", v, fm)
# B15 tomógrafos, B16 meses, B17 dias, B18 horas, B19 aproveitamento, B20 conversão
H_MES = "$B$17*$B$18*$B$19"  # horas de exame por tomógrafo por mês

CEN = ["v26 como está", "Em série (central)", "Em linha (central)", "Em linha (melhor caso)",
       "Em série (pior caso)", "Em linha, com as medidas (aba 8)"]
cab(cp, 22, ["Cenário"] + CEN)
COLS = "BCDEFG"
t = {k: TOM[k] for k in "ABCDE"}
min_com = [20, f"='2 Fluxo'!E{t['B']}", f"='2 Fluxo'!E{t['C']}", f"='2 Fluxo'!D{t['C']}", f"='2 Fluxo'!F{t['B']}",
           f"='2 Fluxo'!E{t['E']}"]
min_cor = [20, 30, f"='2 Fluxo'!E{t['D']}", f"='2 Fluxo'!D{t['D']}", f"='2 Fluxo'!F{t['D']}",
           f"='2 Fluxo'!E{t['D']}"]
min_sem = [15, f"='2 Fluxo'!E{t['A']}", f"='2 Fluxo'!E{t['A']}", f"='2 Fluxo'!D{t['A']}", f"='2 Fluxo'!F{t['A']}",
           f"='2 Fluxo'!E{t['A']}"]
rotulos = {
    23: "Minutos de tomógrafo: exame com contraste",
    24: "Minutos de tomógrafo: angiotomografia",
    25: "Minutos de tomógrafo: angio de coronárias",
    26: "Minutos de tomógrafo: exame sem contraste",
    27: "Parte dos pedidos com contraste feita sem contraste",
    28: "Exames com contraste que podem ir sem, depois da conversão",
    29: "Angiotomografias",
    30: "Angio de coronárias",
    31: "Exames sem contraste",
    32: "Horas de tomógrafo",
    33: "Horas de exame disponíveis",
    34: "Uso dos tomógrafos",
    35: "Carga, em tomógrafos",
    36: "Exames por hora de tomógrafo",
    37: "Horas por dia de contraste em cada tomógrafo (o turno do radiologista)",
    38: "Exames com contraste por dia em cada tomógrafo",
}
for l, n in rotulos.items():
    put(cp, f"A{l}", n, font=F_B if l in (32, 34, 35, 37) else F)
for j, c in enumerate(COLS):
    for l, v in ((23, min_com[j]), (25, min_cor[j]), (26, min_sem[j])):
        if isinstance(v, str):
            link(cp, f"{c}{l}", v, INT)
        else:
            entrada(cp, f"{c}{l}", v, INT)
    put(cp, f"{c}24", f"={c}23", INT)
    if j == 0:
        entrada(cp, f"{c}27", 0, PCT)
    else:
        put(cp, f"{c}27", "=$B$20", PCT)
    put(cp, f"{c}28", f"=$D$7*(1-{c}27)", INT)
    put(cp, f"{c}29", "=$D$8", INT)
    put(cp, f"{c}30", "=$D$9", INT)
    put(cp, f"{c}31", f"=$D$10+$D$7*{c}27", INT)
    put(cp, f"{c}32", f"=({c}28*{c}23+{c}29*{c}24+{c}30*{c}25+{c}31*{c}26)/60", INT, F_B)
    put(cp, f"{c}33", f"=$B$15*$B$16*{H_MES}", INT)
    put(cp, f"{c}34", f"={c}32/{c}33", PCT, F_B)
    put(cp, f"{c}35", f"={c}32/($B$16*{H_MES})", DEC2, F_B)
    put(cp, f"{c}36", f"=$D$11/{c}32", DEC1)
    put(cp, f"{c}37", f"=({c}28*{c}23+{c}29*{c}24+{c}30*{c}25)/60/($B$16*$B$17)/$B$15", DEC1, F_B)
    put(cp, f"{c}38", f"=({c}28+{c}29+{c}30)/($B$16*$B$17)/$B$15", DEC1)
cab(cp, 40, ["Meses para fazer toda a tomografia com N tomógrafos"] + CEN)
for i, n in enumerate((3, 4, 5, 6)):
    l = 41 + i
    entrada(cp, f"A{l}", n, INT)
    for c in COLS:
        put(cp, f"{c}{l}", f"={c}$32/($A{l}*{H_MES})", DEC1)
for j, t_ in enumerate([
    "A coluna B repete a v26: 20 min para todo exame com contraste e 15 sem, nada convertido. Dá 4.478,7 h; o "
    "plano (7.3) escreve 4.478.",
    "Em série e em linha usam os minutos centrais da aba 2; o melhor e o pior caso, os mínimos e os máximos de "
    "cada passo. O pior caso soma todos os passos no máximo: punção difícil na mesa e exame demorado.",
    "Na coluna C, a coronária fica com 30 min, porque em série a frequência é controlada dentro da sala (estudo de "
    "05/11).",
    "A linha 37 é o tempo diário em que o radiologista precisa estar no polo (Parecer CFM 17/2019), mais a "
    "observação do último usuário.",
]):
    nota(cp, 46 + j, t_)

# ================================================================== aba 4: preparo, repouso e enfermagem
pr = aba("4 Poltronas e enfermagem", [62, 16, 16, 16, 56])
titulo(pr, "Poltronas de preparo e de repouso, e enfermagem no turno do contraste",
       "Por tomógrafo: em série, em linha e em linha com as medidas da aba 8. Conta pela lei de Little: usuários ao "
       "mesmo tempo = chegadas por hora × horas de permanência.")
cab(pr, 4, ["", "Em série", "Em linha", "Em linha, com as medidas", "De onde vem"])
P = PASSO


def f2(k, passo):
    return f"'2 Fluxo'!E{P[(k, passo)]}"


ROT4 = {
    5: ("Minutos de tomógrafo por exame com contraste", "aba 2"),
    6: ("Exames com contraste por hora", ""),
    7: ("Observação depois da injeção (min)", "aba 2: bula do contraste e ESUR, 30 min; ACR, 20 min"),
    8: ("Usuários em repouso ao mesmo tempo (média)", ""),
    9: ("Minutos na sala de preparo antes do exame (punção e espera)", "em série, a punção é na mesa"),
    10: ("Usuários na sala de preparo ao mesmo tempo (média)", ""),
    11: ("Poltronas por tomógrafo (repouso + preparo, com 1 de folga para os picos)", ""),
    12: ("Minutos de enfermagem por exame com contraste",
         "triagem, termo, punção e alta; a vigilância do repouso corre junto"),
    13: ("Enfermagem ocupada ao mesmo tempo (média)", ""),
    14: ("Pessoas de enfermagem no turno do contraste", ""),
    15: ("A v26 prevê de enfermagem por tomógrafo", "7.1 do PT v1: 2 por tomógrafo, para cobrir as 50 h da semana"),
}
for l, (n, fo_) in ROT4.items():
    put(pr, f"A{l}", n, font=F_B if l in (11, 14) else F)
    put(pr, f"E{l}", fo_, font=F_S)
for col, k in (("B", "B"), ("C", "C"), ("D", "E")):
    link(pr, f"{col}5", f"='2 Fluxo'!E{t[k]}", INT)
    put(pr, f"{col}6", f"=60/{col}5", DEC1)
    link(pr, f"{col}7", "=" + f2(k, "Observação"), INT)
    put(pr, f"{col}8", f"={col}6*{col}7/60", DEC1)
    if k == "B":
        put(pr, f"{col}9", 0, INT)
        enf = [f2(k, "Triagem e termo"), f2(k, "Punção na mesa"), f2(k, "Alta")]
    else:
        link(pr, f"{col}9", "=" + f2(k, "Punção na sala de preparo") + "+" + f2(k, "Espera pronto"), INT)
        enf = [f2(k, "Orientação em grupo"), f2(k, "Triagem e assinatura"), f2(k, "Punção na sala de preparo"),
               f2(k, "Alta")]
    put(pr, f"{col}10", f"={col}6*{col}9/60", DEC1)
    put(pr, f"{col}11", f"=ROUNDUP({col}8,0)+ROUNDUP({col}10,0)+1", INT, F_B)
    link(pr, f"{col}12", "=" + "+".join(enf), INT)
    put(pr, f"{col}13", f"={col}6*{col}12/60", DEC2)
    put(pr, f"{col}14", f"=ROUNDUP({col}13,0)", INT, F_B)
    entrada(pr, f"{col}15", 2, INT)
for j, t_ in enumerate([
    "Em linha, a enfermagem passa a ser o gargalo: com 4 exames por hora, são cerca de 1,3 pessoa ocupada o tempo "
    "todo. As 2 pessoas da v26 precisam estar juntas no turno do contraste, e não em turnos que se cobrem.",
    "O técnico em radiologia pode conectar a bomba ao acesso já feito, sob supervisão médica (Resolução CONTER "
    "nº 11, art. 6º, citada no Parecer CRM-MG 46/2020). A punção é sempre da enfermagem.",
    "Ler o termo no contato antes do exame e na orientação em grupo tira cerca de 10 min por usuário da triagem "
    "(no HC-UFMG, o termo leva 15 min quando o usuário preenche sozinho).",
]):
    nota(pr, 17 + j, t_)

# ================================================================== aba 5: segurança em números
sg = aba("5 Segurança", [52, 14, 14, 14, 14, 14, 44])
titulo(sg, "Reações e extravasamentos esperados",
       "Taxas do Manual de Contraste do ACR (2026), em amarelo. Exames com contraste da base escolhida na aba 3.")
cab(sg, 4, ["Taxa", "Valor", "", "", "", "", "De onde vem"])
TAXAS = [
    ("Reação de tipo alérgico, todas as gravidades", 0.006, "ACR 2026: 0,6% (a maioria leve)"),
    ("Reação grave", 0.0004, "ACR 2026: 0,04%, cerca de 4 em 10.000"),
    ("Reação tardia (pele, de horas a dias depois), mínimo", 0.005, "ACR 2026: 0,5% a 14%"),
    ("Reação tardia, máximo", 0.14, "ACR 2026"),
    ("Extravasamento, mínimo", 0.001, "ACR 2026: 0,1% a 1,2% das injeções de TC"),
    ("Extravasamento, central", 0.003, "ACR 2026: 0,3% numa série grande"),
    ("Extravasamento, máximo", 0.012, "ACR 2026"),
]
for i, (n, v, fo) in enumerate(TAXAS):
    put(sg, f"A{5 + i}", n)
    entrada(sg, f"B{5 + i}", v, PCT2)
    put(sg, f"G{5 + i}", fo, font=F_S)
# B5 alérgica, B6 grave, B7 tardia mín, B8 tardia máx, B9 extrav mín, B10 extrav central, B11 extrav máx
cab(sg, 13, ["Parte convertida para sem contraste", "", "", "", "", "", ""])
for c, v in zip("BCDEF", (0, 0.1, 0.2, 0.3, 0.5)):
    entrada(sg, f"{c}13", v, PCT)
EVENTOS = [
    (14, "Exames com contraste", "='3 Capacidade'!$D$7*(1-{c}13)+'3 Capacidade'!$D$8+'3 Capacidade'!$D$9", INT),
    (15, "Reações de tipo alérgico", "={c}14*$B$5", INT),
    (16, "Reações graves", "={c}14*$B$6", DEC1),
    (17, "Reações tardias, mínimo", "={c}14*$B$7", INT),
    (18, "Reações tardias, máximo", "={c}14*$B$8", INT),
    (19, "Extravasamentos, central", "={c}14*$B$10", INT),
    (20, "Extravasamentos, mínimo", "={c}14*$B$9", INT),
    (21, "Extravasamentos, máximo", "={c}14*$B$11", INT),
]
for l, n, f_, fm in EVENTOS:
    put(sg, f"A{l}", n, font=F_B if l in (14, 15, 16) else F)
    for c in "BCDEF":
        put(sg, f"{c}{l}", f_.format(c=c), fm, F_B if l in (15, 16) else F)
for j, t_ in enumerate([
    "Quase toda reação grave aparece nos primeiros 20 min (ACR 2026). É por isso que o repouso tem tempo mínimo e "
    "o acesso fica até a alta.",
    "No Brasil, o HCPA registrou 1% de reações leves com contraste não iônico e 2,2% de extravasamento, em "
    "internados (Juchem e Dall'Agnol, 2007).",
    "As reações tardias são quase todas de pele e acontecem em casa: a orientação de alta precisa dizer o que fazer "
    "e para onde ligar.",
]):
    nota(sg, 23 + j, t_)

# ================================================================== aba 6: conversão
cv = aba("6 Conversão", [40, 12, 9, 8, 9, 8, 9, 8, 9, 8, 9, 8, 14, 10, 12, 10])
titulo(cv, "Quanto do contraste dá para tirar: a fila, a evidência e o que rende",
       "A fila é do Mapa Social de 02/11/2026 (os 5 CIDs mais frequentes de cada fila; o painel não dá os outros).")
cab(cv, 4, ["Fila", "Pedidos", "1º CID", "", "2º", "", "3º", "", "4º", "", "5º", "", "Câncer (C) nos 5",
            "% da fila", "Dor abdominal (R10)", "% da fila"])
FILA_CID = [
    ("TC do abdômen superior com contraste", 4116, [("C50", 762), ("C18", 388), ("R10", 321), ("C20", 149),
                                                     ("C16", 147)]),
    ("TC de pelve com contraste", 3639, [("C50", 613), ("C18", 361), ("R10", 305), ("C16", 139), ("C20", 120)]),
    ("TC do tórax com contraste", 2350, [("C50", 557), ("C18", 247), ("C20", 123), ("C16", 93), ("C34", 76)]),
]
for i, (n, ped, cids) in enumerate(FILA_CID):
    l = 5 + i
    put(cv, f"A{l}", n)
    put(cv, f"B{l}", ped, INT)
    cols = "CDEFGHIJKL"
    canc, r10 = [], None
    for j, (cod, q) in enumerate(cids):
        put(cv, f"{cols[2 * j]}{l}", cod)
        put(cv, f"{cols[2 * j + 1]}{l}", q, INT)
        if cod.startswith("C"):
            canc.append(f"{cols[2 * j + 1]}{l}")
        if cod == "R10":
            r10 = f"{cols[2 * j + 1]}{l}"
    put(cv, f"M{l}", "=" + "+".join(canc), INT, F_B)
    put(cv, f"N{l}", f"=M{l}/B{l}", PCT, F_B)
    put(cv, f"O{l}", f"={r10}" if r10 else 0, INT)
    put(cv, f"P{l}", f"=O{l}/B{l}", PCT)
put(cv, "A8", "Três filas", font=F_B, fill=TOT)
put(cv, "B8", "=SUM(B5:B7)", INT, F_B, TOT)
put(cv, "M8", "=SUM(M5:M7)", INT, F_B, TOT)
put(cv, "N8", "=M8/B8", PCT, F_B, TOT)
put(cv, "O8", "=SUM(O5:O7)", INT, F_B, TOT)
put(cv, "P8", "=O8/B8", PCT, F_B, TOT)
nota(cv, 9, "C50 mama, C18 cólon, C20 reto, C16 estômago, C34 pulmão. Idade mediana de 59 a 61 anos. Pelo menos "
            "um terço de cada fila é estadiamento ou seguimento de câncer; o resto dos CIDs não aparece no painel.")
nota(cv, 10, "O protocolo do CBR (2021) faz a TC de tórax \"geralmente sem contraste\", mas pede no abdômen ao menos "
             "a fase portal: é ela que mostra metástase no fígado.")

cab(cv, 12, ["O que a evidência mostra", "Taxa", "", "", "", "", "", "", "", "", "", "", "Situação", "", "", ""])
EVC = [
    ("RSNA 2014: o radiologista mudou o uso do contraste (pôr ou tirar)", 0.085, "rotina; cerca de 220 mil pedidos"),
    ("Yale (RSNA 2018): pedidos de TC com contraste do PS mudados ou cancelados", 0.14, "rotina noturna"),
    ("Vermont (2022): TC de abdômen e pelve feita sem contraste, mínimo", 0.38, "falta de contraste; mais exames "
     "repetidos e internação mais longa"),
    ("Vermont (2022): idem, máximo", 0.55, "falta de contraste"),
    ("SPIE 2023: queda da TC de tórax com contraste", 0.607, "falta de contraste; um sistema dos EUA"),
    ("JAMA 2022: contraste poupado se a TC com contraste não essencial fosse sem", 0.78, "modelo; não mede o dano "
     "da perda de acurácia"),
]
for i, (n, v, s) in enumerate(EVC):
    l = 13 + i
    put(cv, f"A{l}", n)
    put(cv, f"B{l}", v, PCT)
    put(cv, f"M{l}", s, font=F_S)

cab(cv, 20, ["O que a conversão rende", "Rotina", "Ampliada", "Crise"])
for c, v in zip("BCD", (0.10, 0.20, 0.50)):
    entrada(cv, f"{c}21", v, PCT)
put(cv, "A21", "Parte convertida")
RENDE = [
    (22, "Exames convertidos (base da aba 3)", "='3 Capacidade'!$D$7*{c}21", INT),
    (23, "Minutos de tomógrafo poupados por exame, em série",
     f"='2 Fluxo'!$E${t['B']}-'2 Fluxo'!$E${t['A']}", INT),
    (24, "Minutos de tomógrafo poupados por exame, em linha",
     f"='2 Fluxo'!$E${t['C']}-'2 Fluxo'!$E${t['A']}", INT),
    (25, "Horas de tomógrafo poupadas, em série", "={c}22*{c}23/60", INT),
    (26, "Horas de tomógrafo poupadas, em linha", "={c}22*{c}24/60", INT),
    (27, "Parte das horas da tomografia (em série, central)", "={c}25/'3 Capacidade'!$C$32", PCT),
    (28, "Reações de tipo alérgico evitadas", "={c}22*'5 Segurança'!$B$5", DEC1),
    (29, "Reações graves evitadas", "={c}22*'5 Segurança'!$B$6", DEC2),
    (30, "Extravasamentos evitados (central)", "={c}22*'5 Segurança'!$B$10", DEC1),
    (31, "Margem da TC própria, teste de 05/11 (R$)", "=$B$35+$B$36*{c}21*$B$34", MOEDA),
]
for l, n, f_, fm in RENDE:
    put(cv, f"A{l}", n, font=F_B if l in (22, 31) else F)
    for c in "BCD":
        put(cv, f"{c}{l}", f_.format(c=c), fm, F_B if l in (22, 31) else F)
cab(cv, 33, ["Teste de 05/11 (valores sugeridos da planilha de custos)", "Valor"])
put(cv, "A34", "Economia por exame convertido (insumos e enfermagem), R$")
entrada(cv, "B34", 171.80, MOEDA)
put(cv, "A35", "Margem da TC própria com todos os convertíveis com contraste, R$")
entrada(cv, "B35", -1126877, MOEDA)
put(cv, "A36", "Convertíveis da v26 no teste")
entrada(cv, "B36", 11482, INT)
put(cv, "A37", "Conversão que zera a margem", font=F_B)
put(cv, "B37", "=-B35/(B36*B34)", PCT, F_B)
for j, t_ in enumerate([
    "O radiologista pode fazer sem contraste o pedido com contraste, desde que registre o motivo técnico; o "
    "solicitante não pode impor o contraste (Parecer CFM 17/2019).",
    "Para planejar, a evidência sustenta cerca de 10% (rotina: 8,5% a 14%). Taxas de 40% a 60% só apareceram na "
    "falta de contraste de 2022, com mais exames repetidos.",
    "No teste de 05/11, a TC própria só empata com 57% convertidos. A conversão poupa contraste, punção e reação, "
    "mas não fecha a conta: o custo tem de cair por outro lado.",
    "Troque o teste de 05/11 (B34 e B35) pelos valores da planilha de custos quando ela estiver preenchida.",
]):
    nota(cv, 39 + j, t_)

# ================================================================== aba 7: regras
rg = aba("7 Regras", [20, 30, 34, 34, 40, 32, 36])
titulo(rg, "As regras que mudam o fluxo: a v26 contra as diretrizes",
       "ACR = Manual de Contraste do American College of Radiology, 2026. ESUR = diretriz europeia, outubro de 2026. "
       "GEDIAG = Despacho SEI 218755566 sobre o PT v1.")
cab(rg, 4, ["Tema", "v26 (PT v1)", "ACR 2026", "ESUR 2026", "Brasil", "Efeito no fluxo",
            "Sugestão para a próxima versão (decisão do usuário e do RT)"])
REGRAS = [
    ("Jejum", "a orientação \"alcança jejum\", conforme o procedimento (4.7); não diz se a TC com contraste pede",
     "não é exigido antes de contraste venoso de rotina; só na sedação", "não é recomendado antes de contraste "
     "iodado não iônico", "ensaio do A.C.Camargo (AJR 2018, 3.206 usuários): sem diferença nos sintomas. O HC-UFG "
     "dispensa (2026); o POP do HC-UFG de 2021 e a FIDI ainda pedem 4 h",
     "sem jejum, o contraste não fica preso à manhã, e o diabético não corre risco de hipoglicemia",
     "escrever: sem jejum para TC com contraste venoso, salvo sedação"),
    ("Quem precisa de creatinina", "só quem tem doença ou agravo renal; consulta no TrakCare (4.8)",
     "doença renal (crônica, lesão aguda prévia, diálise, cirurgia ou ablação renal, albuminúria), metformina e, "
     "opcional, diabetes. Idade e hipertensão dão muitos falsos positivos",
     "todos, ou quem tem doença renal, cirurgia renal, proteinúria, hipertensão, ácido úrico alto ou diabetes",
     "Coser et al. (Radiol Bras 2021, 1.238 internados): nenhuma nefropatia atribuível ao contraste. GEDIAG (6.6) "
     "pede critério de função renal",
     "pelo ACR, a creatinina fica para uma minoria; pelo ESUR, para boa parte de uma fila de 60 anos",
     "adotar a lista do ACR 2026 e pôr a metformina; o RT decide se segue o ESUR"),
    ("Validade da creatinina", "\"dosagem válida\", sem prazo", "sem prazo acordado; muitos aceitam 30 dias no "
     "ambulatório", "3 meses; 7 dias se há doença aguda ou internação", "", "define quem colhe de novo",
     "90 dias para quem está estável e 7 dias para quem tem doença aguda"),
    ("Corte da função renal", "não fixa", "hidratação só com filtração abaixo de 30 ou lesão aguda; de 30 a 44, caso "
     "a caso", "abaixo de 30, no contraste venoso", "",
     "abaixo de 30: sem contraste, hidratação ou hospital", "o radiologista decide e registra; a devolução à "
     "regulação já está na 4.8"),
    ("Metformina", "todo usuário em metformina só a reinicia após 48 h e nova creatinina (4.8)",
     "filtração de 30 ou mais, sem lesão aguda: não suspende e não precisa de nova creatinina. Abaixo de 30 ou com "
     "lesão aguda: suspende por 48 h e reavalia", "igual: acima de 30, segue normalmente",
     "GEDIAG (6.7): rever, não aplicar a todos",
     "a regra da v26 manda todo diabético em metformina colher sangue depois do exame",
     "alinhar ao ACR e ao ESUR"),
    ("Observação depois da injeção", "\"não há tempo mínimo de permanência\" (4.8)",
     "quase toda reação grave nos primeiros 20 min; reação leve: observar 20 a 30 min",
     "reação leve: até sumir, no mínimo 30 min; quem já teve reação: 30 min com o acesso. A versão de 2018 pedia "
     "30 min para todos", "bulas do contraste: 30 min de observação. Parecer CFM 17/2019: médico no serviço até a "
     "liberação. HU-UFGD: 10 min. GEDIAG (6.8) pede critério de monitoramento e alta",
     "poltronas de repouso; não ocupa o tomógrafo",
     "30 min com o acesso mantido, e mais para quem já teve reação"),
    ("Médico presente", "\"sob supervisão médica, conforme a Resolução CFM nº 2.147/2016\" (4.8)",
     "supervisão direta no local (nos EUA, médico ou profissional habilitado)", "equipe treinada, carrinho de "
     "emergência e protocolo", "Parecer CFM 17/2019: o médico do serviço de radiologia fica no espaço físico durante "
     "todo o exame contrastado, até a liberação. Resolução CFM 2.107/2014, art. 8º: TC exige médico especialista "
     "local. A 2.147/2016 trata do diretor técnico",
     "o contraste só roda com o radiologista no polo; no HC-UFMG, à noite, sem médico, tudo é sem contraste",
     "citar o Parecer 17/2019 e a 2.107/2014; o turno do contraste é o turno do radiologista"),
    ("Quem decide o contraste", "o radiologista decide entre fazer sem contraste e devolver, quando há "
     "contraindicação (4.8)", "", "avaliar risco, benefício e alternativas", "Parecer CFM 17/2019: indicação, dose, "
     "via e prescrição são do radiologista; fazer sem contraste não é infração, desde que se registre o motivo",
     "é a base da conversão caso a caso", "registrar o motivo de cada conversão e acompanhar como indicador"),
    ("Punção e injeção", "enfermeiro ou técnico de enfermagem, sob supervisão médica (4.8)",
     "pessoal treinado para reconhecer e tratar reação", "", "enfermagem punciona e injeta com prescrição "
     "(COREN-BA, 2018); punção difícil pelo enfermeiro (COREN-SP). O técnico em radiologia pode administrar pelo "
     "acesso já feito, mas não punciona (CONTER nº 11, art. 6º). O técnico de enfermagem só fica na sala com o "
     "tomógrafo parado (COREN-RJ 009/2023)", "a punção é sempre da enfermagem; a conexão à bomba pode ser do técnico "
     "em radiologia", "manter; prever enfermeiro para a punção difícil"),
    ("Cateter e fluxo", "não trata", "20G ou maior a partir de 3 mL/s; extravasamento em 0,1% a 1,2%", "",
     "CBR 2021: 2 a 4 mL/s no corpo, 4 mL/s ou mais nas coronárias; 1 a 2 mL/kg",
     "fila oncológica: veia difícil depois da quimioterapia e braço da mama operada sem punção",
     "POP de acesso difícil e de cateter implantado (só o próprio para bomba)"),
    ("Contraste oral", "preparo \"conforme o procedimento\"", "", "", "CBR 2021: no abdômen, \"preferência do "
     "serviço\"", "o contraste oral pede de 60 a 90 min de ingestão; no PS, tirá-lo encurtou a permanência em 97 min "
     "(Levenson, 2012)", "o RT define; se usar, a espera fica na sala de preparo, não no tomógrafo"),
    ("Reação anterior", "\"alergia prévia\" como fator de risco (4.8)", "pré-medicação oral começando 12 h antes, "
     "ou venosa de ao menos 4 a 5 h (2 h ou menos não funciona); reação de escape em 2,1% de quem já reagiu", "identificar o contraste, trocar de produto, observar "
     "30 min com acesso; agendar de dia, de preferência em hospital", "GEDIAG (6.6) pede a conduta",
     "agenda especial ou devolução", "escrever a conduta: sem contraste, pré-medicação pelo protocolo do RT ou "
     "devolução para hospital"),
    ("Termo de consentimento", "colhido antes do contraste (4.8)", "", "", "HC-UFMG: o termo leva 15 min quando o "
     "usuário preenche sozinho; muitos não leem", "15 min por usuário dentro do polo",
     "ler o termo no contato antes do exame e na orientação em grupo; assinar na triagem"),
    ("Tomógrafo da coronária", "1.408 angio de coronárias na v26", "", "", "SCCT 2016: no mínimo 64 canais. O "
     "tomógrafo de Sobradinho tem 4 canais (rascunho do Anexo)", "a coronária só vai a tomógrafo de 64 canais ou "
     "mais", "na carteira 1 não há coronária; nas angiotomografias, parecer do radiologista sobre cada aparelho"),
]
for i, linha_ in enumerate(REGRAS):
    l = 5 + i
    for j, v in enumerate(linha_):
        put(rg, f"{'ABCDEFG'[j]}{l}", v, font=F_B if j == 0 else F)
    rg.row_dimensions[l].height = 105

# ================================================================== aba 8: o que agiliza
ag = aba("8 Agilizar", [34, 40, 24, 24, 56, 24, 30])
titulo(ag, "O que agiliza o fluxo com contraste",
       "O resumo liga nas abas 2, 3 e 4 (base e premissas da aba 3). Abaixo, cada medida, o ganho e de onde vem.")
cab(ag, 4, ["", "Em série (a conta da v26)", "Em linha", "Em linha, com as medidas"])
TP = "'4 Poltronas e enfermagem'"
RESUMO = [
    (5, "Minutos de tomógrafo por exame com contraste",
     [f"='2 Fluxo'!E{t['B']}", f"='2 Fluxo'!E{t['C']}", f"='2 Fluxo'!E{t['E']}"], INT),
    (6, "Exames com contraste por hora de tomógrafo", ["=60/B5", "=60/C5", "=60/D5"], DEC1),
    (7, "Exames com contraste por dia, por tomógrafo (horas e aproveitamento da aba 3)",
     [f"={c}6*'3 Capacidade'!$B$18*'3 Capacidade'!$B$19" for c in "BCD"], DEC1),
    (8, "Tempo do usuário no polo (min)",
     [f"='2 Fluxo'!E{USU['B']}", f"='2 Fluxo'!E{USU['C']}", f"='2 Fluxo'!E{USU['E']}"], INT),
    (9, "Carga da base da aba 3, em tomógrafos",
     ["='3 Capacidade'!C35", "='3 Capacidade'!D35", "='3 Capacidade'!G35"], DEC2),
    (10, "Meses para fazer toda a TC com 3 tomógrafos",
     ["='3 Capacidade'!C41", "='3 Capacidade'!D41", "='3 Capacidade'!G41"], DEC1),
    (11, "Poltronas por tomógrafo", [f"={TP}!B11", f"={TP}!C11", f"={TP}!D11"], INT),
    (12, "Enfermagem ocupada ao mesmo tempo, por tomógrafo", [f"={TP}!B13", f"={TP}!C13", f"={TP}!D13"], DEC2),
]
for l, n, fs, fm in RESUMO:
    put(ag, f"A{l}", n, font=F_B if l in (5, 6, 8) else F)
    for c, f_ in zip("BCD", fs):
        link(ag, f"{c}{l}", f_, fm, bold=(l in (5, 6)))
cab(ag, 14, ["Medida", "O que muda no fluxo", "Ganho no tomógrafo", "Ganho para o usuário", "De onde vem",
             "Quem faz", "Na v26"])
MEDIDAS = [
    ("1. Punção fora da sala", "a punção sai da mesa do tomógrafo e vai para a sala de preparo",
     "−5 min por exame: de 20 para 15 (de 3 para 4 exames por hora)", "fica de 10 a 15 min a mais no polo, à espera "
     "pronto", "AMC Amsterdam: −5 min, uso de 44% para 51%, espera pelo exame de 21 para menos de 5 dias. Kingston: "
     "cerca de 8 min por punção feita na sala. UMass: espera 20% menor", "enfermagem",
     "não: a v26 conta 20 min, em série"),
    ("2. Usuário pronto na porta e bomba carregada", "o próximo usuário já está trocado e puncionado; a seringa da "
     "bomba é preparada antes de ele entrar", "−2 min: de 15 para 13 (4,6 exames por hora)", "",
     "Stenson: o máximo de exames por hora só sai com um usuário pronto a cada intervalo. Yale: 78% do tempo parado "
     "veio do fluxo. Fabricantes: a bomba pronta poupa de 40 s a 3 min", "técnico em radiologia e enfermagem", "não"),
    ("3. Pedido revisado antes do dia", "o radiologista define o protocolo (com ou sem contraste, fases, contraste "
     "oral) na véspera; pedido, creatinina e documento conferidos", "evita tomógrafo parado e exame remarcado",
     "−15 a −30 min: no HC-UFMG, o usuário esperava de 15 a 30 min a decisão do médico",
     "Temple (JACR): revisão dos pedidos 3 dias antes, formulários juntados e agenda refeita; da chegada ao exame, "
     "de 3,1 h para 1,1 h, e 19% mais exames por dia", "radiologista e técnico, com o pré-exame",
     "em parte: a creatinina é consultada no TrakCare (4.8)"),
    ("4. Termo e questionário antes do dia", "o termo é lido e o questionário respondido no contato depois do "
     "agendamento e na véspera; no polo, só a assinatura", "", "−7 a −10 min",
     "HC-UFMG: o termo leva 15 min no dia, e muitos usuários não leem; a dissertação propõe entregá-lo no "
     "agendamento", "operador do pré-exame; a enfermagem confirma", "não: o contato existe (4.5 e 4.6), sem o termo"),
    ("5. Sem jejum", "o exame com contraste pode ir para qualquer horário", "agenda mais flexível",
     "sem fome e sem hipoglicemia no diabético; menos exame perdido por preparo errado",
     "ACR 2026 e ESUR 2026; A.C.Camargo (AJR 2018, 3.206 usuários): sem diferença nos sintomas",
     "RT, na orientação de preparo", "não: a 4.5 fala em jejum conforme o procedimento"),
    ("6. Creatinina só para quem tem risco; metformina sem exame depois", "menos usuários dependem de exame de "
     "sangue antes e depois", "menos devolução por falta de exame", "não precisa ir ao laboratório",
     "ACR 2026: doença renal e metformina, diabetes opcional. ACR e ESUR: a metformina segue com filtração de 30 ou "
     "mais", "RT; o pré-exame consulta o TrakCare",
     "em parte: a 4.8 já limita ao renal, mas a metformina pede creatinina depois"),
    ("7. Primeiro horário pronto", "a sala de preparo abre de 30 a 40 min antes do tomógrafo, com os dois primeiros "
     "usuários puncionados", "recupera a primeira hora do dia", "",
     "Manchester: 1,6 exame na primeira hora contra 5,7 por hora no resto do dia (dois tomógrafos). Num serviço dos "
     "EUA, o início no horário passou de 11% para 82%", "enfermagem e supervisor do polo", "não"),
    ("8. Agenda em blocos e chegadas escalonadas", "contraste no turno do radiologista; sem contraste nos intervalos "
     "e fora do turno; com contraste chega 40 min antes, sem contraste 15", "menos tempo parado",
     "menos fila na recepção", "Parecer CFM 17/2019 (médico presente). HC-UFMG: a agenda de 5 em 5 min enchia a "
     "recepção; a proposta é de 15 em 15", "coordenação assistencial e supervisor do polo", "não"),
    ("9. Duas pessoas de enfermagem juntas no turno do contraste", "uma na triagem e na punção; outra na injeção, "
     "no repouso e na alta", "sustenta de 4 a 4,6 exames por hora", "", "aba 4: de 1,2 a 1,3 pessoa ocupada o "
     "tempo todo, em linha", "enfermagem", "em parte: 2 por tomógrafo, mas em turnos que se cobrem (7.1)"),
    ("10. Veia difícil com enfermeiro e ultrassom", "a primeira tentativa dá certo mais vezes",
     "em série, a mesa não fica parada", "menos picadas", "meta-análise de 2023: acerto na 1ª tentativa cerca de 3 "
     "vezes mais provável com ultrassom; revisão de 2021: 77% contra 63%. Até um terço dos adultos tem veia difícil, "
     "e a fila é oncológica", "enfermeiro", "não"),
    ("11. Técnico em radiologia conecta a bomba", "a enfermagem não precisa entrar na sala na injeção", "",
     "", "CONTER nº 11, art. 6º, citada no Parecer CRM-MG 46/2020: o técnico administra pelo acesso já feito, sob "
     "supervisão, e não punciona", "técnico em radiologia", "não: a 4.8 põe a injeção na enfermagem"),
    ("12. Contraste oral só quando o radiologista pedir", "sem 60 a 90 min de ingestão antes do exame", "",
     "−60 a −90 min no polo", "Levenson 2012: −97 min de permanência no PS. CBR 2021: no abdômen, preferência do "
     "serviço", "RT", "não trata"),
    ("13. Repouso com poltronas suficientes", "o repouso de 30 min não ocupa a poltrona de quem vai ser puncionado",
     "evita que o preparo trave", "", "aba 4: de 5 a 6 poltronas por tomógrafo, em linha", "enfermagem",
     "não: a v26 não tem tempo mínimo"),
    ("14. Medir desde o mês 1", "tempo na sala, troca, punção difícil, conversões, reações e tempo no polo",
     "confirma ou corrige os minutos", "", "Lean na TC: de 2,0 para 3,3 usuários por hora (Watson Clinic); revisão "
     "de 17 estudos com ganho de produção", "coordenação assistencial", "em parte: relatório mensal"),
]
for i, linha_ in enumerate(MEDIDAS):
    l = 15 + i
    for j, v in enumerate(linha_):
        put(ag, f"{'ABCDEFG'[j]}{l}", v, font=F_B if j == 0 else F)
    ag.row_dimensions[l].height = 64
l = 15 + len(MEDIDAS) + 1
for j, t_ in enumerate([
    "As medidas 1, 2, 7 e 9 mexem no tempo de tomógrafo. As 3, 4, 5, 6, 8 e 12, no tempo do usuário e no exame "
    "perdido. As 10, 11 e 13 sustentam o ritmo.",
    "Nenhuma delas pede equipamento novo. Pedem sala de preparo com poltronas, escala de enfermagem no turno do "
    "contraste e o pré-exame fazendo mais do que confirmar a presença.",
]):
    nota(ag, l + j, t_)

# ================================================================== fontes
fo = aba("Fontes", [5, 70, 20, 90])
titulo(fo, "Fontes", "Consultadas em 08/11/2026. \"Texto completo\" quer dizer que o documento foi lido inteiro; "
                     "\"resumo\", que só o resumo ou trechos.")
cab(fo, 4, ["Nº", "Fonte", "Como foi lida", "Link"])
FONTES = [
    ("ACR Manual on Contrast Media, 2026", "texto completo",
     "https://www.acr.org/Clinical-Resources/Clinical-Tools-and-Reference/Contrast-Manual"),
    ("ACR, Supervision of Contrast Material Administration (atualizada em 24/12/2025)", "texto completo",
     "https://www.acr.org/Clinical-Resources/Clinical-Tools-and-Reference/Contrast-Manual/supervision-of-contrast-material-administration"),
    ("ESUR Contrast Media Safety Committee Guidelines 2026 (outubro de 2026)", "texto completo",
     "https://www.esur.org/esur-guidelines-2026/"),
    ("ESUR Guidelines on Contrast Agents v10.0 (2018)", "texto completo",
     "https://www.esur.org/wp-content/uploads/2022/03/ESUR-Guidelines-10_0-Final-Version.pdf"),
    ("CFM, Parecer nº 17/2019 (indicação e prescrição de contraste)", "texto completo",
     "https://cbr.org.br/wp-content/uploads/2023/08/Parecer-CFM-de-2019-no-17_Uso-de-contraste.pdf"),
    ("CBR, parecer jurídico sobre a prescrição de contraste (22/08/2025; cita a Resolução CFM 2.107/2014, art. 8º)",
     "texto completo",
     "https://cbr.org.br/wp-content/uploads/2026/04/Parecer-sobre-Responsabilidade-pela-Prescricao-de-Meios-de-Contraste-para-Exames-de-Imagem.pdf"),
    ("Resolução CFM nº 2.147/2016 (diretores técnicos e clínicos)", "ementa",
     "https://sistemas.cfm.org.br/normas/arquivos/resolucoes/BR/2016/2147_2016.pdf"),
    ("CRM-MG, Parecer nº 46/2020 (técnico em radiologia e contraste; cita a Resolução CONTER nº 11)", "trechos",
     "https://sistemas.cfm.org.br/normas/arquivos/pareceres/MG/2020/46_2020.pdf"),
    ("COREN-RJ, Parecer nº 009/2023 (técnico de enfermagem na tomografia)", "trechos",
     "https://coren-rj.org.br/wp-content/uploads/2023/11/PARECER-009.2023-CT-Gest%C3%A3o-de-Investimentos-e-Tecnologia-em-Sa%C3%BAde-papel-do-t%C3%A9cnico.pdf"),
    ("COREN-BA, Parecer Técnico nº 001/2018 (administração de contraste)", "trechos",
     "https://www.coren-ba.gov.br/wp-content/uploads/2018/06/PT-001-2018-ADMINISTRA%C3%87%C3%83O-DE-MEIO-DE-CONTRASTE-Aprovado-ROP-08-06-18.pdf"),
    ("CBR, Protocolos iniciais de tomografia computadorizada (dezembro de 2021)", "texto completo",
     "https://cbr.org.br/wp-content/uploads/2022/03/Protocolos-de-Tomografia-Computadorizada-1.pdf"),
    ("HC-UFG/Ebserh, POP.UDI.007, atividades nos exames de TC (2021)", "texto completo",
     "https://www.gov.br/hubrasil/pt-br/hospitais-universitarios/regiao-centro-oeste/hc-ufg/governanca/pops-e-protocolos/gerencia-de-atencao-a-saude/divisao-de-apoio-diagnostico-e-terapeutico/POP.UDI.007.DescriodasatividadesemexamesdeTomografiaComputadorizada.pdf"),
    ("HC-UFG/Ebserh, preparo de TC e RM (2026), sem jejum", "texto completo (estudo de 07/11)",
     "https://www.gov.br/hubrasil/pt-br/hospitais-universitarios/regiao-centro-oeste/hc-ufg/saude/exames/PREPAROEXAMESDETCERM.26.pdf"),
    ("Santos Junior E. Lean no setor de TC de um hospital universitário. Dissertação, UFMG, 2024", "texto completo",
     "https://repositorio.ufmg.br/handle/1843/81992"),
    ("Erdfarb AJ, Forman HP, Tocino I. RSNA 2005 (SSE22-01); tese de Erdfarb, Yale, 2006", "resumos",
     "https://archive.rsna.org/2005/4407929.html"),
    ("Stenson BA et al. Am J Emerg Med 2021;40:159-161", "resumo e trechos",
     "https://research.bidmc.org/radiology-research/publications/estimating-maximum-patient-throughput-ed-scanner-three-patients-hour-magic-number"),
    ("Elkhuizen SG et al. Health Care Manage Rev 2007;32(1):37-45 (AMC, Amsterdam)", "resumo",
     "https://research.utwente.nl/en/publications/applying-the-variety-reduction-principle-to-management-of-ancilla/"),
    ("Chang L et al., auditoria de punção na TC, Kingston (AuntMinnie Europe)", "notícia",
     "https://www.auntminnieeurope.com/subspecialties/musculoskeletal-radiology/body-imaging/article/15655073/lack-of-iv-access-contributes-to-ct-scanner-downtime"),
    ("Royal College of Radiologists, auditoria \"Inpatient cannulation in CT\"", "modelo de auditoria",
     "https://www.rcr.ac.uk/career-development/audit-quality-improvement/auditlive-radiology-templates/inpatient-cannulation-in-ct-how-much-scanner-time-is-lost/"),
    ("Zimmerman ME et al. J Cardiovasc Comput Tomogr 2021;15(6):477-483", "resumo",
     "https://scholars.duke.edu/individual/pub1488054"),
    ("Resumo 13323: angio coronária sistólica, sem betabloqueador", "resumo",
     "https://www.citedrive.com/en/discovery/abstract-13323-impact-of-an-institutional-process-change-adopting-end-systolic-coronary-cta-acquisition-on-patient-throughput-and-image-quality"),
    ("Betabloqueador oral × venoso na angio coronária (Radiología, 2011)", "resumo",
     "https://www.elsevier.es/en-revista-radiologia-english-edition--419-articulo-oral-versus-intravenous-beta-blockers-for-S2173510711700155"),
    ("SCCT 2016, diretriz de realização da angio coronária (mínimo de 64 canais)", "trechos",
     "https://cdn-corpweb.heartflow.com/assets/docs/SCCT_guidelines_for_the_perf/SCCT_guidelines_for_the_perf.html"),
    ("CDA-AMC. Hourly CT Exam Volumes Across Canada in 2022–2023. Can J Health Technol 2025;5(7)", "texto completo",
     "https://canjhealthtechnol.ca/index.php/cjht/article/view/CM0028"),
    ("Ministério da Saúde, Parâmetros SUS, Seção D: equipamentos de apoio diagnóstico (NESCON/UFMG)",
     "texto completo",
     "https://www.gov.br/saude/pt-br/acesso-a-informacao/gestao-do-sus/programacao-regulacao-controle-e-financiamento-da-mac/programacao-assistencial/arquivos/se-o-d-equipamentos.pdf"),
    ("Santos DL et al. Cad Saúde Pública 2014;30(6):1293-1304", "texto",
     "https://www.scielo.br/j/csp/a/bJRMxq6ycWRDvFvKTrqGbXt/"),
    ("Manchester (UHSM): produção da TC das 8 às 9 h (AuntMinnie Europe)", "notícia",
     "https://www.auntminnieeurope.com/imaging-informatics/article/15651212/low-ct-productivity-from-8-to-9-am-needs-attention"),
    ("Relatos iSixSigma de Lean na tomografia (Watson Clinic e outros)", "relato",
     "https://www.isixsigma.com/case-studies/removing-bottlenecks-improving-flow-radiology/"),
    ("Barbosa PNVP et al. AJR 2018;210(5):941-947 (jejum, A.C.Camargo)", "resumo",
     "https://doi.org/10.2214/AJR.17.19061"),
    ("Juchem BC, Dall'Agnol CM. Rev Latino-Am Enfermagem 2007 (reações no HCPA)", "resumo",
     "https://www.scielo.br/j/rlae/a/XCrRdWMYwVByHCjkwKW7wdR/?lang=pt"),
    ("Coser et al. Radiol Bras 2021;54(2):77-82 (contraste e lesão renal, 1.238 internados)", "resumo",
     "https://www.scielo.br/j/rb/a/3jKDntc59srhJjTshYX9jVP/?lang=en"),
    ("Bula do Omnipaque (GE Healthcare, Reino Unido): 30 min de observação", "trechos",
     "https://gehealthcare.co.uk/Omnipaque-PI/uk"),
    ("Bula do Iopamiron (Brasil): pelo menos 30 min de observação", "trechos",
     "https://drconsulta.com/conteudo/iopamiron-bula/"),
    ("HU-UFGD/Ebserh, POP UDI 008, enfermagem na TC (10 min de observação)", "trechos",
     "https://www.gov.br/hubrasil/pt-br/hospitais-universitarios/regiao-centro-oeste/hu-ufgd/acesso-a-informacao/pops-protocolos-e-processos/gad/pop-udi-008-assistencia-de-enfermagem-nos-exames-de-tomografia-computadorizada-v-1.pdf"),
    ("Davenport MS et al. JAMA 2022;328(5):476-478 (estratégias na falta de contraste)", "texto completo",
     "https://jamanetwork.com/journals/jama/fullarticle/2793384"),
    ("Falta de contraste de 2022 em Vermont (van den Broek-Altenburg; Radiology Business)", "trechos",
     "https://radiologybusiness.com/topics/healthcare-management/healthcare-economics/2022-contrast-shortage-changed-ct-patterns-driving-higher-costs-and-longer-stays"),
    ("Queda da TC de tórax com contraste na falta de 2022 (SPIE Medical Imaging 2023)", "trechos",
     "https://nanophotonics.spiedigitallibrary.org/conference-proceedings-of-spie/12468/124680X/Tracking-the-impact-of-global-iodinated-contrast-agent-shortage-on/10.1117/12.2654552.full"),
    ("RSNA 2014: o radiologista muda o exame e o contraste do pedido", "resumo",
     "https://archive.rsna.org/2014/14016581.html"),
    ("Yale, RSNA 2018: consulta ao radiologista nos pedidos do PS", "notícia",
     "https://appliedradiology.com/articles/rsna-2018-radiologists-provide-positive-impact-to-exam-orders-from-emergency-department"),
    ("Contraste oral e permanência no PS (Hopkins et al., West J Emerg Med 2012; cita Levenson 2012)", "resumo",
     "https://westjem.com/original-research/does-limiting-oral-contrast-decrease-emergency-department-length-of-stay.html"),
    ("Dako F et al. (Temple), fluxo da TC ambulatorial, J Am Coll Radiol (relatado por AuntMinnie e Health Imaging)",
     "notícia",
     "https://www.auntminnie.com/clinical-news/ct/article/15618262/simple-interventions-reduce-outpatient-ct-wait-times"),
    ("UMass Chan: estação de punção ao lado do tomógrafo (prêmio de 2023)", "notícia",
     "https://umassmed.edu/radiology/radnews/2024/spring2024/innovators-of-the-year-award-university-ct-team"),
    ("Meta-análise: ultrassom na punção de veia difícil (Eur J Emerg Med 2023)", "resumo",
     "https://www.pubmed.gov/36727865/"),
    ("AAFP 2021: ultrassom contra palpação na punção periférica", "resumo",
     "https://www.aafp.org/pubs/afp/issues/2021/1000/od2.pdf"),
    ("Início no horário do primeiro exame de TC (Emory; DOTmed)", "trechos", "https://www.dotmed.com/news/story/51999"),
    ("Mapa Social da Saúde, coleta de 02/11/2026 (filas de imagem)", "dado do projeto",
     "../dados/fontes/mapa_social_20261102_imagem.md"),
    ("PT v1 (v26), seções 4.8 e 7.1 a 7.3", "plano", "../versoes/plano_v26_20261021.md"),
    ("Análise do Despacho GEDIAG 218755566 (08/11/2026)", "estudo interno", "analise_despacho_gediag_20261108.md"),
    ("Estudos de 05/11 (custos) e 07/11 (12 meses e 3 tomógrafos)", "estudos internos",
     "estudo_v26_salas_precos_custos_20261105.xlsx; estudo_12_meses_3_tomografos_20261107.md"),
]
for i, (n, como, url) in enumerate(FONTES):
    l = 5 + i
    put(fo, f"A{l}", i + 1, INT)
    put(fo, f"B{l}", n)
    put(fo, f"C{l}", como, font=F_S)
    put(fo, f"D{l}", url, font=F_URL)

# ================================================================== leia
le = wb.active
le.title = "Leia"
le.sheet_view.showGridLines = False
le.column_dimensions["A"].width = 130
titulo(le, "Contraste na tomografia: tempo, fluxo e regras",
       "Pesquisa e análise de 08/11/2026, com os números da v26 (PT v1) e da carteira 1. Controle interno: nada "
       "daqui vai ao plano sem decisão do usuário.")
TEXTO = [
    ("Como ler", True),
    ("Células amarelas com fonte azul: premissas que podem ser mudadas. Fonte verde: vem de outra aba. O resto é "
     "fórmula.", False),
    ("A aba 3 escolhe a base (v26 ou carteira 1) na célula B4.", False),
    ("", False),
    ("Abas", True),
    ("1 Tempos medidos: o que a literatura e os serviços brasileiros mediram de tempo de tomógrafo.", False),
    ("2 Fluxo: o passo a passo do usuário em quatro fluxos (sem contraste; com contraste em série; em linha; angio "
     "coronária), com mínimo, central e máximo.", False),
    ("3 Capacidade: horas de tomógrafo, uso, carga e meses com esses tempos, e o turno diário do radiologista.",
     False),
    ("4 Poltronas e enfermagem: quantas poltronas e quantas pessoas de enfermagem o contraste pede por tomógrafo.",
     False),
    ("5 Segurança: reações e extravasamentos esperados, pelas taxas do ACR.", False),
    ("6 Conversão: os CIDs da fila, o que a evidência mostra de conversão e o que cada nível rende.", False),
    ("7 Regras: a v26 contra o ACR 2026, o ESUR 2026 e as normas brasileiras, com o efeito no fluxo.", False),
    ("8 Agilizar: as medidas que aceleram o fluxo com contraste, o ganho de cada uma e de onde vem.", False),
    ("Fontes: os links, e como cada documento foi lido.", False),
    ("", False),
    ("O que a pesquisa mostra", True),
    ("1. Os 20 min da v26 estão certos para o exame com contraste com punção na mesa (medidos: 17 a 20). Com o "
     "acesso feito antes, ficam 12 a 15; os 13 min do estudo de 07/11 são o piso. Sem contraste, são 9 a 11, e não 15.",
     False),
    ("2. O que trava é o fluxo, não a máquina: num hospital de Yale, o tomógrafo ficou parado 69% do tempo, quase "
     "sempre por falha no fluxo de usuários. Em Amsterdam, tirar a punção da sala encurtou em 5 min o tempo de "
     "atravessamento e levou o uso de 44% a 51%.", False),
    ("3. Três regras da 4.8 da v26 estão fora das diretrizes atuais e foram contestadas pela GEDIAG: a metformina "
     "para todos, o repouso sem tempo mínimo e a triagem renal sem lista nem prazo. A norma citada para a supervisão "
     "(CFM 2.147/2016) trata do diretor técnico; as que tratam do contraste são o Parecer CFM 17/2019 e a "
     "Resolução CFM 2.107/2014.", False),
    ("4. O ACR 2026 é mais estreito do que se pensava: pede creatinina de quem tem doença renal ou toma "
     "metformina, e diz que idade e hipertensão geram falso positivo. O ESUR 2026 é mais largo. A escolha muda "
     "quantos usuários precisam de exame de sangue.", False),
    ("5. Com 30 min de repouso (a bula do contraste), cada tomógrafo em linha pede cerca de 5 poltronas e 2 pessoas "
     "de enfermagem juntas no turno do contraste.", False),
    ("6. O radiologista precisa estar no polo enquanto houver contraste (Parecer CFM 17/2019). Na v26, isso dá "
     "cerca de 3 a 4 h por dia em cada tomógrafo.", False),
    ("7. Nas 12.890 TC com contraste da v26, esperam-se cerca de 77 reações de tipo alérgico (quase todas leves), "
     "5 graves e de 13 a 155 extravasamentos.", False),
    ("8. Conversão: pelo menos um terço das filas com contraste é câncer, e o abdômen pede fase portal. A rotina "
     "converte de 8,5% a 14%. No teste de 05/11, a TC própria só empata com 57% convertidos: a conversão não fecha a "
     "conta.", False),
    ("9. Com as medidas da aba 8, o exame com contraste ocupa o tomógrafo 13 min, e não 20: são 4,6 exames por "
     "hora, 54% a mais que em série, e o usuário fica cerca de 74 min no polo. Nenhuma medida pede equipamento novo.",
     False),
]
for i, (t_, negrito) in enumerate(TEXTO):
    put(le, f"A{4 + i}", t_, font=F_B if negrito else F, borda=False)

ordem = ["Leia", "1 Tempos medidos", "2 Fluxo", "3 Capacidade", "4 Poltronas e enfermagem", "5 Segurança",
         "6 Conversão", "7 Regras", "8 Agilizar", "Fontes"]
wb._sheets = [wb[n] for n in ordem]
for ws in wb.worksheets:
    ws.sheet_view.zoomScale = 110
wb.save(SAIDA)
print(SAIDA)
