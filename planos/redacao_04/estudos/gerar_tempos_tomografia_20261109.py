"""Tomografia e ultrassom: tempos e equipe (09/11/2026, pedido do usuário; revisto duas vezes no mesmo dia).

Gera duas planilhas:
- tempos_e_equipe_tomografia_ultrassom_20261109.xlsx: o formulário para as pessoas que ajudam o projeto na parte
  assistencial, com duas abas.
  - Tomografia: os minutos de cada etapa, sem e com contraste. A punção tem duas linhas, na mesa e antes, e cada
    etapa diz onde o paciente fica (cadeira ou maca no preparo e no repouso). Pergunta também a equipe para 10 horas
    e as pausas.
  - Ultrassom: os minutos de cada parte de 12 tipos de exame e a equipe de uma sala por 10 horas, com o auxiliar
    que fica com o médico o exame todo.
  Não traz tempo de referência, para não puxar a resposta, nem nada interno.
- estudo_tempos_tomografia_3_polos_20261109.xlsx: o estudo interno. Traz o fluxo da TC com os tempos de referência do
  estudo de 08/11, os exames por hora e as cadeiras, a conta dos 3 polos em 12 meses, o ultrassom por tipo de exame,
  a equipe de referência (v26, 4.15) e o lugar das respostas.

Tudo o que é conta é fórmula. Amarelo com fonte azul: premissa ou resposta. Verde: vem de outra aba.
Recalcular depois de gerar:
    python3.11 <skill xlsx>/scripts/recalc.py <arquivo>.xlsx 90
"""
import os

from openpyxl import Workbook
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter as L
from openpyxl.worksheet.datavalidation import DataValidation

AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA_FORM = os.path.join(AQUI, "tempos_e_equipe_tomografia_ultrassom_20261109.xlsx")
SAIDA_REF = os.path.join(AQUI, "tempos_e_equipe_tomografia_ultrassom_nossa_referencia_20261109.xlsx")
SAIDA_ESTUDO = os.path.join(AQUI, "estudo_tempos_tomografia_3_polos_20261109.xlsx")

# ------------------------------------------------------------------ estilo (o mesmo dos estudos de 05/11 a 08/11)
A = "Arial"
F = Font(name=A, size=10)
F_B = Font(name=A, size=10, bold=True)
F_T = Font(name=A, size=13, bold=True)
F_T14 = Font(name=A, size=14, bold=True)
F_S = Font(name=A, size=9, italic=True, color="555555")
F_EX = Font(name=A, size=10, italic=True, color="7F7F7F")
F_IN = Font(name=A, size=10, color="0000FF")
F_LK = Font(name=A, size=10, color="008000")
F_LKB = Font(name=A, size=10, bold=True, color="008000")
AMARELO = PatternFill("solid", fgColor="FFF2CC")
CAB = PatternFill("solid", fgColor="D9E1F2")
SEC = PatternFill("solid", fgColor="E2EFDA")
TOT = PatternFill("solid", fgColor="EDEDED")
VERDE_CF = PatternFill("solid", fgColor="C6EFCE")
VERMELHO_CF = PatternFill("solid", fgColor="FFC7CE")
F_VERDE_CF = Font(name=A, size=10, color="006100")
F_VERMELHO_CF = Font(name=A, size=10, color="9C0006")
BORDA = Border(*(Side(style="thin", color="BFBFBF"),) * 4)
TOPO = Alignment(vertical="top", wrap_text=True)
CENTRO = Alignment(horizontal="center", vertical="top", wrap_text=True)
NOWRAP = Alignment(vertical="top", wrap_text=False)
INT, DEC1, DEC2, PCT = "#,##0", "#,##0.0", "#,##0.00", "0%"

L_PAUSA = '"para,alguém cobre,depende"'
L_ESCALA = '"dois turnos de 5 horas,jornada cheia com revezamento nas pausas,outro (explique na Observação)"'
NAO_CONTAR = ("Não precisa contar: o médico de retaguarda e o responsável técnico do polo, a supervisão de polo, o "
              "agendamento e a confirmação (pré-exame), o registro no TrakCare (pós-exame) e o assistente "
              "administrativo. Essas funções já estão no projeto.")


def put(ws, ref, v, fmt=None, font=F, fill=None, borda=True, alin=TOPO):
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


def entrada(ws, ref, v=None, fmt=None, alin=TOPO):
    return put(ws, ref, v, fmt, F_IN, AMARELO, alin=alin)


def link(ws, ref, formula, fmt=None, bold=False):
    return put(ws, ref, formula, fmt, F_LKB if bold else F_LK)


def faixa(ws, r, c1, c2, v=None, font=F, fill=None, borda=True, altura=None, alin=TOPO):
    """Escreve v na primeira célula e junta c1:c2 da linha r (colunas em letra)."""
    put(ws, f"{c1}{r}", v, font=font, fill=fill, borda=borda, alin=alin)
    for col in range(ws[f"{c1}{r}"].column + 1, ws[f"{c2}{r}"].column + 1):
        cel = ws.cell(r, col)
        if borda:
            cel.border = BORDA
        if fill:
            cel.fill = fill
    if c1 != c2:
        ws.merge_cells(f"{c1}{r}:{c2}{r}")
    if altura:
        ws.row_dimensions[r].height = altura


def larguras(ws, ws_larg):
    for i, w in enumerate(ws_larg):
        ws.column_dimensions[L(i + 1)].width = w


def paisagem(ws):
    ws.page_setup.orientation = "landscape"
    ws.page_setup.paperSize = ws.PAPERSIZE_A4
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.print_options.horizontalCentered = True
    ws.page_margins.left = ws.page_margins.right = 0.4
    ws.page_margins.top = ws.page_margins.bottom = 0.5


def falta_ou_soma(celulas):
    """'—' se alguma célula estiver em branco; senão, a soma."""
    lista = ",".join(celulas)
    return f'=IF(COUNT({lista})<{len(celulas)},"—",SUM({lista}))'


# ------------------------------------------------------------------ cargos (v26, 4.15; quadro P2 de 07/11)
REC = "pessoal de recepção e preparo"
ENF = "enfermeiro ou técnico de enfermagem"
TRAD = "técnico em radiologia"

# ------------------------------------------------------------------ as etapas da TC (estudo de 08/11, aba 2)
# (chave, etapa, o que acontece, quem faz, onde o paciente fica, ocupa o tomógrafo, mín, central, máx, de onde vem)
SEM = [
    ("rec", "Recepção", "identificação, documento e pedido médico", REC, "recepção", "não", 3, 5, 8,
     "HC-UFMG: 3 min (Santos Junior, 2024)"),
    ("conf", "Conferência", "questionário de segurança; gestação, nas mulheres em idade fértil", ENF,
     "sala de triagem", "não", 3, 5, 8, "v26, 4.8"),
    ("roupa", "Troca de roupa", "tirar metais e vestir o avental", "paciente", "vestiário", "não", 3, 5, 10,
     "estimativa"),
    ("exame", "Exame", "posicionar o paciente, adquirir as imagens e sair da sala", TRAD, "sala do tomógrafo", "sim",
     8, 9, 13, "Erdfarb 2005: 8,6 min na sala (DP 4,2)"),
    ("troca", "Troca de paciente", "limpar a mesa e chamar o próximo", TRAD, "sala do tomógrafo", "sim", 1, 2, 4,
     "Stenson 2021: 3,6 min de sala vazia (mediana, com espera); POP HC-UFG: limpeza a cada exame"),
]
COM_MESA = [
    ("rec", "Recepção", "identificação, documento e pedido médico", REC, "recepção", "não", 3, 5, 8, "HC-UFMG"),
    ("triagem", "Triagem e termo", "alergia, doença renal, diabetes e metformina, gestação; leitura e assinatura do "
     "termo de consentimento", ENF, "sala de triagem", "não", 5, 10, 15,
     "HC-UFMG: o termo leva 15 min quando o usuário preenche sozinho"),
    ("roupa", "Troca de roupa", "tirar metais e vestir o avental", "paciente", "vestiário", "não", 3, 5, 10,
     "estimativa"),
    ("pmesa", "Punção na mesa", "acesso venoso e teste com soro, com o paciente já deitado no tomógrafo", ENF,
     "sala do tomógrafo", "sim", 5, 7, 15,
     "Kingston: cerca de 8 min por punção feita no serviço; AMC: tirar a punção da sala poupa 5 min"),
    ("exame", "Exame com contraste", "posicionar, ligar à bomba injetora, adquirir as fases, desligar e sair da sala",
     f"{TRAD} e enfermagem", "sala do tomógrafo", "sim", 9, 11, 15,
     "Erdfarb 2005: 17,1 min na sala no exame com contraste (DP 7,4), com a punção quando feita na sala"),
    ("troca", "Troca de paciente", "limpar a mesa e chamar o próximo", TRAD, "sala do tomógrafo", "sim", 1, 2, 4,
     "Stenson 2021"),
    ("repouso", "Repouso depois do contraste", "observação com o acesso mantido, antes da alta",
     f"{ENF}; radiologista na unidade", "sala de repouso, em maca ou cadeira", "não", 20, 30, 30,
     "ACR 2026: quase toda reação grave nos primeiros 20 min; bulas do contraste e ESUR: 30 min"),
    ("alta", "Alta", "retirar o acesso e orientar o paciente", ENF, "sala de repouso, em maca ou cadeira", "não",
     2, 3, 5, "estimativa"),
]
COM_ANTES = [
    ("rec", "Recepção", "o paciente chega cerca de 40 min antes do horário do tomógrafo", REC, "recepção", "não",
     3, 5, 8, "estudo de 07/11"),
    ("orient", "Orientação em grupo", "3 a 5 pacientes: o contraste, o calor na injeção, o repouso; leitura do termo",
     ENF, "sala de preparo, em cadeira", "não", 3, 4, 6, "uma sessão de 15 a 20 min dividida pelo grupo"),
    ("triagem", "Triagem e assinatura", "alergia, rim, metformina, gestação; assinatura do termo", ENF,
     "sala de triagem", "não", 3, 5, 8, "v26, 4.8"),
    ("roupa", "Troca de roupa", "tirar metais e vestir o avental", "paciente", "vestiário", "não", 3, 5, 10,
     "estimativa"),
    ("pantes", "Punção antes", "acesso venoso e teste com soro na sala de preparo; o paciente fica sentado", ENF,
     "sala de preparo, em cadeira", "não", 5, 7, 15, "Kingston: cerca de 8 min por punção"),
    ("espera", "Espera com o acesso feito", "um ou dois pacientes prontos, para o tomógrafo não parar", "paciente",
     "sala de preparo, em cadeira", "não", 5, 15, 30, "estudo de 07/11"),
    ("exame", "Exame com contraste", "posicionar, ligar à bomba, adquirir as fases, desligar e sair da sala", TRAD,
     "sala do tomógrafo", "sim", 10, 13, 15,
     "Stenson 2021: 12,1 min na sala (mediana); HC-UFMG: 15 min com o acesso feito antes"),
    ("troca", "Troca de paciente", "limpar a mesa e chamar o próximo", TRAD, "sala do tomógrafo", "sim", 1, 2, 4,
     "Stenson 2021"),
    ("repouso", "Repouso depois do contraste", "observação com o acesso mantido", f"{ENF}; radiologista na unidade",
     "sala de repouso, em maca ou cadeira", "não", 20, 30, 30, "ACR 2026; bulas do contraste; ESUR"),
    ("alta", "Alta", "retirar o acesso e orientar o paciente", ENF, "sala de repouso, em maca ou cadeira", "não",
     2, 3, 5, "estimativa"),
]
# o formulário: as duas punções na mesma tabela
FORM_COM = [
    COM_MESA[0], COM_MESA[1], COM_MESA[2], COM_MESA[3],
    ("pantes", "Punção antes", "acesso venoso e teste com soro numa sala de preparo, antes de entrar", ENF,
     "sala de preparo, em cadeira", "não"),
    ("espera", "Espera com o acesso feito", "só com a punção antes: o paciente espera pronto até ser chamado",
     "paciente", "sala de preparo, em cadeira", "não"),
    COM_MESA[4], COM_MESA[5], COM_MESA[6], COM_MESA[7],
]
# as contas das duas punções: (rótulo, etapas na mesa, etapas antes)
CONTAS_COM = [
    ("Minutos de tomógrafo por exame", ["pmesa", "exame", "troca"], ["exame", "troca"]),
    ("Exames por hora de tomógrafo", None, None),
    ("Minutos em cadeira ou maca (preparo e repouso)", ["repouso", "alta"], ["pantes", "espera", "repouso", "alta"]),
    ("Tempo do paciente na unidade", ["rec", "triagem", "roupa", "pmesa", "exame", "troca", "repouso", "alta"],
     ["rec", "triagem", "roupa", "pantes", "espera", "exame", "troca", "repouso", "alta"]),
]

# ------------------------------------------------------------------ ultrassom (estudo de 07/11, seção 2.1; CBR 2017)
# (chave, exame, preparo, agenda do CBR = minutos de sala, posicionado do CBR = exame, exames da carteira 1)
EXAMES_US = [
    ("mama", "Mamas (as duas)", "sem preparo; troca de roupa", 20, 15, 12950),
    ("dmi", "Doppler de membros (os dois lados)", "tirar meias e a roupa do membro", 40, 30, 12345),
    ("dvas", "Doppler de carótidas e outros vasos", "sem preparo; artérias renais e aorta: jejum", 20, 15, 4727),
    ("par", "Parede abdominal", "sem preparo", 20, 15, 3304),
    ("abt", "Abdômen total", "jejum e bexiga cheia; água na espera", 20, 15, 10347),
    ("abs", "Abdômen superior", "jejum", 15, 10, 2327),
    ("uri", "Aparelho urinário e rins", "bexiga cheia; água cerca de 1 hora antes", 15, 10, 4657),
    ("pro", "Próstata (via abdominal)", "bexiga cheia; água na espera", 15, 10, 3052),
    ("pel", "Pélvica (ginecológica)", "bexiga cheia; água na espera", 15, 10, 1014),
    ("tv", "Transvaginal", "esvaziar a bexiga e trocar de roupa", 15, 10, 5294),
    ("tir", "Tireoide", "sem preparo", 15, 10, 3979),
    ("esc", "Bolsa escrotal", "troca de roupa", 15, 10, 1136),
]
PARTES_US = ["Preparo fora da sala", "Entrada e posicionamento", "Exame com o transdutor", "Fechar o laudo",
             "Saída e limpeza do transdutor"]

# ------------------------------------------------------------------ equipe: (chave, função, o que faz)
EQUIPE_TC = [
    ("tc_radiol", "Médico radiologista", "laudo; presente na unidade durante os exames com contraste, até a alta"),
    ("tc_tecrad", "Técnico em radiologia", "posiciona o paciente e adquire as imagens"),
    ("tc_enf", "Enfermeiro ou técnico de enfermagem", "triagem, punção, repouso, alta e intercorrências"),
    ("tc_rec", "Pessoal de recepção e preparo", "identificação, cadastro, orientação e troca de roupa"),
]
EQUIPE_US = [
    ("us_med", "Médico ultrassonografista", "realiza o exame e assina o laudo"),
    ("us_aux", "Auxiliar de sala do ultrassom", "fica com o médico o exame todo: digita o laudo, ajuda o paciente, "
     "acompanha o transvaginal e o de próstata, limpa o transdutor"),
    ("us_rec", "Pessoal de recepção e preparo", "identificação, cadastro, orientação e preparo (água, troca de roupa)"),
]


# ------------------------------------------------------------------ a versão preenchida: a nossa referência, com a fonte
NOSSA = "estimativa nossa"
IDOSOS = "estimativa nossa: a fila tem idade mediana de 59 a 61 anos, com muitos idosos"
REF_TC = {
    "sem": {
        "rec": (5, "HC-UFMG (Santos Junior, 2024): 3 min medidos; 5 com folga"),
        "conf": (5, NOSSA),
        "roupa": (5, IDOSOS),
        "exame": (9, "Erdfarb et al., RSNA 2005 (Yale): 8,6 min na sala"),
        "troca": (2, "Stenson et al., 2021: 3,6 min de sala vazia entre pacientes, com espera"),
    },
    "com": {
        "rec": (5, "HC-UFMG (Santos Junior, 2024): 3 min medidos; 5 com folga"),
        "triagem": (10, "HC-UFMG (Santos Junior, 2024): o termo leva 15 min quando o paciente lê sozinho"),
        "roupa": (5, IDOSOS),
        "pmesa": (7, "auditoria de Kingston (Reino Unido): cerca de 8 min por punção feita na sala"),
        "pantes": (7, "o mesmo tempo de punção, feita fora da sala"),
        "espera": (15, NOSSA + ": um ou dois pacientes prontos, para o tomógrafo não parar"),
        "exame": (11, "Erdfarb et al., RSNA 2005: 17,1 min na sala com a punção; com a punção antes, 12 a 15 min "
                      "medidos (Stenson et al., 2021; HC-UFMG)"),
        "troca": (2, "Stenson et al., 2021"),
        "repouso": (30, "bulas dos contrastes e ESUR 2026: 30 min; ACR 2026: quase toda reação grave nos primeiros "
                        "20 min"),
        "alta": (3, NOSSA),
    },
}
REF_EQUIPE = {
    "tc_radiol": (2, "um por turno de 5 h com contraste (Parecer CFM 17/2019: presente durante o contraste); 1, se o "
                     "contraste couber num turno"),
    "tc_tecrad": (3, "turnos de 5 h; até 24 h semanais por pessoa (Lei 7.394/1985, art. 14): 10 turnos por semana ÷ 4 "
                     "= 3"),
    "tc_enf": (4, "turnos de 5 h: 2 no dia todo; com a punção antes, mais 2 para a 2ª pessoa no horário do contraste"),
    "tc_rec": (2, "turnos de 5 h: um de manhã e um à tarde, por polo"),
    "us_med": (2, "turnos de 5 h: um de manhã e um à tarde"),
    "us_aux": (2, "turnos de 5 h: um de manhã e um à tarde"),
    "us_rec": (2, "turnos de 5 h, por polo; o mesmo da tomografia, se houver"),
}
# ultrassom: preparo fora da sala (min, fonte); na sala, o CBR 2017 com a diferença entre agenda e exame dividida
REF_PREPARO_US = {
    "mama": (5, "troca de roupa, " + IDOSOS), "dmi": (5, "tirar meias e roupa, " + IDOSOS), "dvas": (0, "sem preparo"),
    "par": (0, "sem preparo"), "abt": (60, "bexiga cheia: água cerca de 1 hora antes; o jejum é em casa"),
    "abs": (0, "o jejum é em casa"), "uri": (60, "bexiga cheia: água cerca de 1 hora antes"),
    "pro": (60, "bexiga cheia: água cerca de 1 hora antes"), "pel": (60, "bexiga cheia: água cerca de 1 hora antes"),
    "tv": (7, "esvaziar a bexiga e trocar de roupa, " + IDOSOS), "tir": (0, "sem preparo"),
    "esc": (5, "troca de roupa, " + IDOSOS),
}


def altura_para(pares):
    """Altura da linha para caber o texto mais longo: (texto, largura da coluna em caracteres)."""
    linhas = max((len(t or "") // max(w - 4, 1)) + 1 for t, w in pares)
    return max(15, 13 * linhas + 2)


def ref_us(chave, agenda, posic):
    """(preparo, entrada, exame, laudo, saída, fonte) da versão preenchida."""
    dif = agenda - posic
    prep, fonte_prep = REF_PREPARO_US[chave]
    fonte = (f"CBR 2017: {posic} min de exame e {agenda} de agenda; entrada e saída divididas por nós; laudo "
             f"digitado durante o exame. Preparo: {fonte_prep}")
    return prep, round(dif * 0.6), posic, 0, dif - round(dif * 0.6), fonte


# ================================================================== 1. o formulário
AVISO_REF = ("Esta planilha traz a nossa referência: os tempos vêm de estudos publicados e de outros serviços, com a "
             "fonte de cada número na Observação. Serve para comparar; para responder, usem a planilha em branco.")


def formulario(saida, ref=False):
    """ref=True: a versão preenchida com a nossa referência e as fontes."""
    wb = Workbook()
    tc = wb.active
    tc.title = "Tomografia"
    us = wb.create_sheet("Ultrassom")
    for ws in (tc, us):
        ws.sheet_view.showGridLines = False
        paisagem(ws)

    def validacoes(ws):
        dv_min = DataValidation(type="decimal", operator="between", formula1="0", formula2="600", allow_blank=True,
                                showErrorMessage=True, errorTitle="Minutos",
                                error="Digite só o número de minutos (por exemplo, 5).")
        dv_num = DataValidation(type="decimal", operator="between", formula1="0", formula2="600", allow_blank=True,
                                showErrorMessage=True, errorTitle="Número", error="Digite só o número.")
        dv_pausa = DataValidation(type="list", formula1=L_PAUSA, allow_blank=True)
        dv_escala = DataValidation(type="list", formula1=L_ESCALA, allow_blank=True)
        for dv in (dv_min, dv_num, dv_pausa, dv_escala):
            ws.add_data_validation(dv)
        ws._dv_escala = dv_escala
        return dv_min, dv_num, dv_pausa

    def cabeca(ws, titulo, sub, c2):
        put(ws, "A1", titulo, font=F_T14, borda=False, alin=NOWRAP)
        put(ws, "A2", sub, font=F_S, borda=False, alin=NOWRAP)
        put(ws, "A4", "Nome de quem preencheu", font=F_B)
        faixa(ws, 4, "B", c2, "Referência do projeto" if ref else None, font=F_IN, fill=AMARELO)

    def equipe(ws, r, linhas, c_oque2, c_qtd, c_jor1, c_jor2, dv_num):
        """Tabela de equipe a partir da linha r (cabeçalho). Devolve a última linha."""
        put(ws, f"A{r}", "Função", font=F_B, fill=CAB)
        faixa(ws, r, "B", c_oque2, "O que faz", font=F_B, fill=CAB)
        put(ws, f"{c_qtd}{r}", "Quantas pessoas", font=F_B, fill=CAB, alin=CENTRO)
        faixa(ws, r, c_jor1, c_jor2, "Jornada ou escala de cada uma (ex.: 6 h por dia; 12x36)", font=F_B, fill=CAB)
        for chave, funcao, oque in linhas + [(None, "Outra função (qual?)", None)]:
            r += 1
            put(ws, f"A{r}", funcao, font=F_B)
            if oque is None:
                faixa(ws, r, "B", c_oque2, None, font=F_IN, fill=AMARELO)
            else:
                faixa(ws, r, "B", c_oque2, oque)
            qtd, jor = REF_EQUIPE.get(chave, (None, None)) if ref else (None, None)
            entrada(ws, f"{c_qtd}{r}", qtd, "0", alin=CENTRO)
            dv_num.add(f"{c_qtd}{r}")
            faixa(ws, r, c_jor1, c_jor2, jor, font=F_IN, fill=AMARELO)
            if (oque and len(oque) > 70) or (jor and len(jor) > 60):
                ws.row_dimensions[r].height = 28
        return r

    # ---------------------------------------------------------------- aba Tomografia
    ws = tc
    larguras(ws, [30, 44, 28, 26, 11, 12, 12, 60 if ref else 30])
    dv_min, dv_num, dv_pausa = validacoes(ws)
    cabeca(ws, "Tomografia: tempos e equipe",
           "Para dimensionar a tomografia do projeto. Cada pessoa preenche a sua. O ultrassom está na outra aba.", "D")
    faixa(ws, 7, "A", "H", "Como preencher", font=F_B, fill=SEC)
    faixa(ws, 8, "A", "H", "Digite só nas células amarelas. Vale número aproximado, da experiência de vocês. Se não "
          "souber, deixe em branco.", altura=18)
    faixa(ws, 9, "A", "H", 'As etapas com "sim" em "Ocupa o tomógrafo?" prendem o aparelho e decidem quantos exames '
          "cabem por hora. As contas aparecem sozinhas embaixo de cada tabela.", altura=18)
    faixa(ws, 10, "A", "H", "Se alguma etapa é feita por outra pessoa, ou em outro lugar, escreva na Observação.",
          altura=18)
    if ref:
        faixa(ws, 11, "A", "H", AVISO_REF, font=F_B, altura=28)
    put(ws, "A11", "Exemplo de linha preenchida:", font=F_S, borda=False, alin=NOWRAP) if not ref else None
    exemplo = ["Recepção", "identificação, documento e pedido médico", REC, "recepção", "não", 6,
               "às segundas demora mais"]
    for i, v in enumerate(exemplo if not ref else []):
        col = L(i + 1)
        if col == "G":
            faixa(ws, 12, "G", "H", v, font=F_EX)
        else:
            put(ws, f"{col}12", v, font=F_EX, alin=CENTRO if col in "EF" else TOPO)

    cab_tc = ["Etapa", "O que acontece", "Quem faz", "Onde o paciente fica", "Ocupa o tomógrafo?", "Minutos"]

    def tabela_tc(r, etapas, valores):
        for i, t in enumerate(cab_tc):
            put(ws, f"{L(i + 1)}{r}", t, font=F_B, fill=CAB, alin=CENTRO if i in (4, 5) else TOPO)
        faixa(ws, r, "G", "H", "Observação", font=F_B, fill=CAB)
        linhas = {}
        for chave, etapa, oque, quem, onde, ocupa, *_ in etapas:
            r += 1
            linhas[chave] = r
            put(ws, f"A{r}", etapa, font=F_B)
            put(ws, f"B{r}", oque)
            put(ws, f"C{r}", quem)
            put(ws, f"D{r}", onde)
            put(ws, f"E{r}", ocupa, alin=CENTRO)
            v, fonte = valores[chave] if ref else (None, None)
            entrada(ws, f"F{r}", v, alin=CENTRO)
            dv_min.add(f"F{r}")
            faixa(ws, r, "G", "H", fonte, font=F_IN, fill=AMARELO)
            if fonte:
                ws.row_dimensions[r].height = altura_para([(oque, 44), (quem, 28), (onde, 26), (fonte, 66)])
        return r, linhas

    def linha_conta(r, rot, expl, formulas, fmt="General"):
        put(ws, f"A{r}", rot, font=F_B, fill=TOT)
        faixa(ws, r, "B", "E", expl, font=F_S, fill=TOT)
        for col, f in zip("FG", formulas):
            put(ws, f"{col}{r}", f, fmt, F_B, TOT, alin=CENTRO)
        if len(formulas) == 1:
            faixa(ws, r, "G", "H", None, fill=TOT)
        else:
            put(ws, f"H{r}", None, fill=TOT)

    # 1. sem contraste
    faixa(ws, 14, "A", "H", "1. Tomografia SEM contraste", font=F_B, fill=SEC)
    r, ls = tabela_tc(15, SEM, REF_TC["sem"])
    cel = [f"F{ls[k]}" for k in ("exame", "troca")]
    r += 1
    linha_conta(r, "Minutos de tomógrafo por exame", 'soma das etapas com "sim"', [falta_ou_soma(cel)])
    r += 1
    linha_conta(r, "Exames por hora de tomógrafo", "60 ÷ minutos de tomógrafo",
                [f'=IF(ISNUMBER(F{r - 1}),IF(F{r - 1}>0,60/F{r - 1},"—"),"—")'], "0.0")
    r += 1
    linha_conta(r, "Tempo do paciente na unidade", "soma de todas as etapas, em minutos",
                [falta_ou_soma([f"F{ls[k]}" for k, *_ in SEM])])

    # 2. com contraste
    r += 2
    faixa(ws, r, "A", "H", "2. Tomografia COM contraste (na veia)", font=F_B, fill=SEC)
    textos = [
        "A punção (o acesso venoso) pode ser feita de dois jeitos, e cada um tem a sua linha na tabela. Se souberem, "
        "preencham as duas.",
        "Punção na mesa: o paciente deita no tomógrafo e a enfermagem faz o acesso ali. O aparelho fica parado "
        "enquanto isso.",
        "Punção antes: o acesso é feito numa sala de preparo, com o paciente sentado. Ele espera pronto e entra no "
        "tomógrafo só para o exame.",
    ]
    for t in textos:
        r += 1
        faixa(ws, r, "A", "H", t, altura=18)
    r, ls = tabela_tc(r + 1, FORM_COM, REF_TC["com"])
    r += 1
    put(ws, f"A{r}", "Contas", font=F_B, fill=CAB)
    faixa(ws, r, "B", "E", None, fill=CAB)
    put(ws, f"F{r}", "Punção na mesa", font=F_B, fill=CAB, alin=CENTRO)
    put(ws, f"G{r}", "Punção antes", font=F_B, fill=CAB, alin=CENTRO)
    put(ws, f"H{r}", None, fill=CAB)
    expl = {"Minutos de tomógrafo por exame": 'soma das etapas com "sim" de cada jeito',
            "Exames por hora de tomógrafo": "60 ÷ minutos de tomógrafo",
            "Minutos em cadeira ou maca (preparo e repouso)": "o tempo que o paciente ocupa uma cadeira ou maca",
            "Tempo do paciente na unidade": "soma das etapas de cada jeito, em minutos"}
    for rot, mesa, antes in CONTAS_COM:
        r += 1
        if mesa is None:
            fs = [f'=IF(ISNUMBER({c}{r - 1}),IF({c}{r - 1}>0,60/{c}{r - 1},"—"),"—")' for c in "FG"]
            linha_conta(r, rot, expl[rot], fs, "0.0")
        else:
            fs = [falta_ou_soma([f"F{ls[k]}" for k in ks]) for ks in (mesa, antes)]
            linha_conta(r, rot, expl[rot], fs)

    # 3. equipe
    r += 2
    faixa(ws, r, "A", "H", "3. Equipe para um tomógrafo funcionar 10 horas por dia útil", font=F_B, fill=SEC)
    r += 1
    faixa(ws, r, "A", "H", "Se vocês fossem montar o time, quantas pessoas de cada função? Contem as pessoas para "
          "cobrir as 10 horas, com as pausas.", altura=18)
    r = equipe(ws, r + 1, EQUIPE_TC, "E", "F", "G", "H", dv_num)
    r += 1
    faixa(ws, r, "A", "H", NAO_CONTAR, font=F_S, altura=28)
    for texto, dv, fmt, v in [
        ("Para cobrir as 10 horas, como vocês organizariam a equipe?", ws._dv_escala, None, "dois turnos de 5 horas"),
        ("Pausas: quantos minutos de pausa cada pessoa faz num dia de trabalho (almoço e descanso)?", dv_num, "0", 15),
        ("Nas pausas, o tomógrafo para ou alguém cobre?", dv_pausa, None, "para"),
    ]:
        r += 1
        faixa(ws, r, "A", "E", texto)
        faixa(ws, r, "F", "H", v if ref else None, font=F_IN, fill=AMARELO, alin=TOPO)
        if fmt:
            ws[f"F{r}"].number_format = fmt
        dv.add(f"F{r}")
    if ref:
        r += 1
        faixa(ws, r, "A", "H", "Turno de 5 h: pela CLT (art. 71, § 1º), o trabalho de 4 a 6 h tem pausa de 15 min, e não de "
              "1 h. Com dois turnos, o tomógrafo para 30 min por dia, 5% do dia.", font=F_S, altura=18)
    r += 2
    faixa(ws, r, "A", "H", "4. Observações", font=F_B, fill=SEC)
    r += 1
    faixa(ws, r, "A", "C", "Alguma etapa que não está aqui, ou que vocês fazem de outro jeito?")
    faixa(ws, r, "D", "H", None, font=F_IN, fill=AMARELO, altura=45)

    # ---------------------------------------------------------------- aba Ultrassom
    ws = us
    larguras(ws, [32, 34, 12, 15, 12, 12, 13, 11, 10, 70 if ref else 28])
    dv_min, dv_num, _ = validacoes(ws)
    cabeca(ws, "Ultrassom: tempos e equipe", "Para dimensionar o ultrassom do projeto. Cada pessoa preenche a sua.",
           "D")
    faixa(ws, 7, "A", "J", "Como preencher", font=F_B, fill=SEC)
    instr = [
        "Para cada exame, os minutos de cada parte. Vale número aproximado, da experiência de vocês. Se não souber um "
        "exame, deixe a linha em branco.",
        "Preparo fora da sala: o tempo que o paciente passa se preparando antes de entrar (por exemplo, a bexiga "
        "enchendo). Não ocupa a sala.",
        "As outras quatro partes acontecem na sala, com o médico e a pessoa que fica com ele. Se o paciente troca de "
        "roupa na sala, contem em Entrada e posicionamento.",
        "Se o preparo for diferente do que está escrito, corrijam na Observação.",
    ]
    for i, t in enumerate(instr):
        faixa(ws, 8 + i, "A", "J", t, altura=18)
    if ref:
        faixa(ws, 12, "A", "J", AVISO_REF, font=F_B, altura=28)
    else:
        put(ws, "A12", "Exemplo de linha preenchida:", font=F_S, borda=False, alin=NOWRAP)
    for i, v in enumerate([] if ref else ["Tireoide", "sem preparo", 0, 2, 8, 2, 1, 13, 4.6, "nódulo leva mais"]):
        put(ws, f"{L(i + 1)}13", v, "0.0" if i == 8 else None, font=F_EX, alin=CENTRO if 2 <= i <= 8 else TOPO)

    faixa(ws, 15, "A", "J", "1. Minutos de cada exame", font=F_B, fill=SEC)
    cab_us = ["Exame", "Preparo antes da sala"] + PARTES_US + ["Minutos de sala", "Exames por hora", "Observação"]
    for i, t in enumerate(cab_us):
        put(ws, f"{L(i + 1)}16", t, font=F_B, fill=CAB, alin=CENTRO if 2 <= i <= 8 else TOPO)
    ws.row_dimensions[16].height = 40
    r = 16
    for chave, exame, preparo, agenda, posic, _qtd in EXAMES_US:
        r += 1
        put(ws, f"A{r}", exame, font=F_B)
        put(ws, f"B{r}", preparo)
        vals = ref_us(chave, agenda, posic) if ref else [None] * 6
        for col, v in zip("CDEFG", vals[:5]):
            entrada(ws, f"{col}{r}", v, alin=CENTRO)
            dv_min.add(f"{col}{r}")
        put(ws, f"H{r}", falta_ou_soma([f"{c}{r}" for c in "DEFG"]), "General", F_B, TOT, alin=CENTRO)
        put(ws, f"I{r}", f'=IF(ISNUMBER(H{r}),IF(H{r}>0,60/H{r},"—"),"—")', "0.0", F_B, TOT, alin=CENTRO)
        entrada(ws, f"J{r}", vals[5])
        if ref:
            ws.row_dimensions[r].height = altura_para([(vals[5], 72), (preparo, 34)])
    r += 1
    faixa(ws, r, "A", "J", "Minutos de sala = entrada e posicionamento + exame + fechar o laudo + saída e limpeza. O "
          "preparo fora da sala não entra.", font=F_S, borda=False)

    r += 2
    faixa(ws, r, "A", "J", "2. Equipe para uma sala de ultrassom funcionar 10 horas por dia útil", font=F_B,
          fill=SEC)
    r += 1
    faixa(ws, r, "A", "J", "Se vocês fossem montar o time, quantas pessoas de cada função? Contem as pessoas para "
          "cobrir as 10 horas, com as pausas.", altura=18)
    r = equipe(ws, r + 1, EQUIPE_US, "F", "G", "H", "J", dv_num)
    r += 1
    faixa(ws, r, "A", "J", NAO_CONTAR, font=F_S, altura=28)
    r += 1
    faixa(ws, r, "A", "F", "Para cobrir as 10 horas, como vocês organizariam a equipe?")
    faixa(ws, r, "G", "J", "dois turnos de 5 horas" if ref else None, font=F_IN, fill=AMARELO)
    ws._dv_escala.add(f"G{r}")
    r += 1
    faixa(ws, r, "A", "F", "Que formação vocês pedem para o auxiliar de sala (por exemplo, técnico de enfermagem)?")
    faixa(ws, r, "G", "J", "técnico de enfermagem (sugestão nossa: pode acompanhar o transvaginal e o de próstata)"
          if ref else None, font=F_IN, fill=AMARELO)
    r += 2
    faixa(ws, r, "A", "J", "3. Observações", font=F_B, fill=SEC)
    r += 1
    faixa(ws, r, "A", "D", "Algum exame ou etapa que não está aqui, ou que vocês fazem de outro jeito?")
    faixa(ws, r, "E", "J", None, font=F_IN, fill=AMARELO, altura=45)
    r += 2
    put(ws, f"A{r}", "Obrigado! Pode devolver a planilha pelo grupo.", font=F_S, borda=False, alin=NOWRAP)
    wb.save(saida)


# ================================================================== 2. o estudo interno
def estudo():
    wb = Workbook()
    wb.remove(wb.active)

    def aba(nome, larg):
        ws = wb.create_sheet(nome)
        ws.sheet_view.showGridLines = False
        larguras(ws, larg)
        paisagem(ws)
        return ws

    def titulo(ws, t, sub):
        put(ws, "A1", t, font=F_T, borda=False, alin=NOWRAP)
        put(ws, "A2", sub, font=F_S, borda=False, alin=NOWRAP)

    def secao(ws, r, t, ncol):
        for i in range(ncol):
            put(ws, f"{L(i + 1)}{r}", t if i == 0 else None, font=F_B, fill=SEC, alin=NOWRAP)

    def cab(ws, r, rotulos, col0=1, altura=None):
        for i, t in enumerate(rotulos):
            put(ws, f"{L(col0 + i)}{r}", t, font=F_B, fill=CAB)
        if altura:
            ws.row_dimensions[r].height = altura

    def nota(ws, r, t, col="A"):
        put(ws, f"{col}{r}", t, font=F_S, borda=False, alin=NOWRAP)

    leia = aba("Leia", [130])
    fl = aba("1 Fluxo TC", [30, 44, 30, 28, 11, 8, 8, 8, 60])
    ph = aba("2 Por hora", [50, 13, 13, 13, 13, 13, 13, 13, 13])
    tp = aba("3 Três polos", [62, 16, 16, 16, 16, 16])
    ul = aba("4 Ultrassom", [34, 12, 34, 12, 12, 12, 12, 12, 12, 12, 12])
    eq = aba("5 Equipe", [56, 12, 12, 12, 12, 12, 12, 12, 12, 12, 70])
    rs = aba("6 Respostas", [64, 30, 30, 30])
    RESP = ["Resposta 1", "Resposta 2", "Resposta 3"]

    # ---------------------------------------------------------------- aba 6: respostas (as outras ligam nela)
    titulo(rs, "Respostas da equipe assistencial, uma coluna por pessoa",
           "Copiar aqui as respostas do formulário (tempos_e_equipe_tomografia_ultrassom_20261109.xlsx). Os minutos "
           "da TC vão na aba 1 (bloco D) e os do ultrassom na aba 4 (seção 2).")
    cab(rs, 4, ["Pergunta"] + RESP)
    perguntas = [("nome", "Nome de quem respondeu", None)]
    perguntas += [(k, f"Equipe da TC: {f.lower()}", "0") for k, f, _ in EQUIPE_TC]
    perguntas += [("tc_outro", "Equipe da TC: outra função (quantas pessoas)", "0"),
                  ("tc_outro_qual", "Equipe da TC: qual outra função", None),
                  ("tc_jornadas", "Equipe da TC: jornadas e escalas", None),
                  ("tc_escala", "TC: como cobrir as 10 horas", None),
                  ("pausa_min", "Pausa por pessoa num dia de trabalho, em minutos", "0"),
                  ("pausa_cobre", "Nas pausas, o tomógrafo para ou alguém cobre", None),
                  ("tc_obs", "TC: observações", None)]
    perguntas += [(k, f"Equipe do ultrassom: {f.lower()}", "0") for k, f, _ in EQUIPE_US]
    perguntas += [("us_outro", "Equipe do ultrassom: outra função (quantas pessoas)", "0"),
                  ("us_outro_qual", "Equipe do ultrassom: qual outra função", None),
                  ("us_jornadas", "Equipe do ultrassom: jornadas e escalas", None),
                  ("us_escala", "Ultrassom: como cobrir as 10 horas", None),
                  ("us_formacao", "Formação do auxiliar de sala do ultrassom", None),
                  ("us_obs", "Ultrassom: observações", None)]
    LR = {}
    for i, (k, rot, fmt) in enumerate(perguntas):
        r = 5 + i
        LR[k] = r
        put(rs, f"A{r}", rot)
        for col in "BCD":
            entrada(rs, f"{col}{r}", None, fmt)
    dv = DataValidation(type="list", formula1=L_PAUSA, allow_blank=True)
    rs.add_data_validation(dv)
    dv.add(f"B{LR['pausa_cobre']}:D{LR['pausa_cobre']}")
    CR = ["B", "C", "D"]  # coluna de cada resposta na aba 6

    def nome_resp(i):
        c = CR[i]
        return f"=IF('6 Respostas'!{c}${LR['nome']}=\"\",\"{RESP[i]}\",'6 Respostas'!{c}${LR['nome']})"

    # ---------------------------------------------------------------- aba 1: fluxo da TC
    titulo(fl, "Fluxo da tomografia, passo a passo: o tempo de cada etapa e onde o paciente fica",
           "Referência: minutos mínimo, central e máximo do estudo de 08/11 (aba 2), com a fonte. As respostas da "
           "equipe assistencial entram no bloco D. Só as etapas com \"sim\" ocupam o tomógrafo.")
    cab_fl = ["Etapa", "O que acontece", "Quem faz", "Onde o paciente fica", "Ocupa o tomógrafo?", "Mín",
              "Central", "Máx", "De onde vem"]
    TOTS = {}

    def bloco(r0, nome, t, etapas, cadeira):
        secao(fl, r0, t, 9)
        r = r0 + 1
        cab(fl, r, cab_fl, altura=28)
        p = r + 1
        lin = {}
        for chave, etapa, oque, quem, onde, ocupa, mn, ce, mx, fonte in etapas:
            r += 1
            lin[chave] = r
            put(fl, f"A{r}", etapa, font=F_B)
            put(fl, f"B{r}", oque)
            put(fl, f"C{r}", quem)
            put(fl, f"D{r}", onde)
            put(fl, f"E{r}", ocupa, alin=CENTRO)
            put(fl, f"F{r}", mn, "0", alin=CENTRO)
            put(fl, f"G{r}", ce, "0", F_B, alin=CENTRO)
            put(fl, f"H{r}", mx, "0", alin=CENTRO)
            put(fl, f"I{r}", fonte, font=F_S)
        u = r
        contas = [
            ("tom", "Minutos de tomógrafo por exame", lambda c: f'=SUMIF($E${p}:$E${u},"sim",{c}{p}:{c}{u})'),
            ("porh", "Exames por hora de tomógrafo", None),
            ("cad", "Minutos em cadeira ou maca (preparo e repouso)",
             lambda c: "=" + ("+".join(f"{c}{lin[k]}" for k in cadeira) if cadeira else "0")),
            ("pac", "Tempo do paciente na unidade (min)", lambda c: f"=SUM({c}{p}:{c}{u})"),
        ]
        TOTS[nome] = {}
        for k, rot, fn in contas:
            r += 1
            TOTS[nome][k] = r
            put(fl, f"A{r}", rot, font=F_B, fill=TOT)
            for col in "BCDE":
                put(fl, f"{col}{r}", None, fill=TOT)
            for col in "FGH":
                f = fn(col) if fn else f'=IF(N({col}{r - 1})>0,60/{col}{r - 1},"")'
                put(fl, f"{col}{r}", f, "0.0" if k == "porh" else "0", F_B, TOT, alin=CENTRO)
            put(fl, f"I{r}", None, fill=TOT)
        return r

    fim = bloco(4, "A", "A. Sem contraste", SEM, [])
    fim = bloco(fim + 2, "B", "B. Com contraste e a punção na mesa (a conta da v26)", COM_MESA, ["repouso", "alta"])
    fim = bloco(fim + 2, "C", "C. Com contraste e a punção antes, numa sala de preparo (em linha)", COM_ANTES,
                ["orient", "pantes", "espera", "repouso", "alta"])

    # bloco D: as respostas, como no formulário
    r = fim + 2
    secao(fl, r, "D. As respostas da equipe assistencial (as linhas do formulário)", 9)
    r += 1
    cab(fl, r, ["Etapa", "Onde o paciente fica", "Ocupa o tomógrafo?", "Referência (central)"] + RESP)
    for i in range(3):
        link(fl, f"{L(5 + i)}{r}", nome_resp(i), bold=True)
        fl[f"{L(5 + i)}{r}"].fill = CAB
    RD = {"sem": {}, "com": {}}

    def linhas_resp(r, titulo_sub, etapas, ref, grupo):
        r += 1
        put(fl, f"A{r}", titulo_sub, font=F_B, fill=SEC)
        for col in "BCDEFG":
            put(fl, f"{col}{r}", None, fill=SEC)
        for chave, etapa, _oque, _quem, onde, ocupa, *_ in etapas:
            r += 1
            RD[grupo][chave] = r
            put(fl, f"A{r}", etapa, font=F_B)
            put(fl, f"B{r}", onde)
            put(fl, f"C{r}", ocupa, alin=CENTRO)
            link(fl, f"D{r}", f"=G{ref[chave]}", "0")
            for i in range(3):
                entrada(fl, f"{L(5 + i)}{r}", None, alin=CENTRO)
        return r

    # linha de cada etapa nos blocos A, B e C: as etapas terminam logo antes da linha dos minutos de tomógrafo
    linA, linB, linC = {}, {}, {}
    for nome, etapas, alvo in (("A", SEM, linA), ("B", COM_MESA, linB), ("C", COM_ANTES, linC)):
        p = TOTS[nome]["tom"] - len(etapas)
        for i, e in enumerate(etapas):
            alvo[e[0]] = p + i
    ref_com = dict(linB)
    ref_com["pantes"] = linC["pantes"]
    ref_com["espera"] = linC["espera"]
    r = linhas_resp(r, "Sem contraste", SEM, linA, "sem")
    r += 1
    put(fl, f"A{r}", "Minutos de tomógrafo por exame", font=F_B, fill=TOT)
    for col in "BC":
        put(fl, f"{col}{r}", None, fill=TOT)
    link(fl, f"D{r}", f"=G{TOTS['A']['tom']}", "0")
    RD["sem_tom"] = r
    for i in range(3):
        c = L(5 + i)
        put(fl, f"{c}{r}", falta_ou_soma([f"{c}{RD['sem'][k]}" for k in ("exame", "troca")]).replace('"—"', '""'),
            "General", F_B, TOT, alin=CENTRO)
    r += 1
    put(fl, f"A{r}", "Exames por hora de tomógrafo", font=F_B, fill=TOT)
    for col in "BC":
        put(fl, f"{col}{r}", None, fill=TOT)
    for col in "DEFG":
        put(fl, f"{col}{r}", f'=IF(N({col}{r - 1})>0,60/{col}{r - 1},"")', "0.0", F_B, TOT, alin=CENTRO)
    r = linhas_resp(r, "Com contraste (as duas punções)", FORM_COM, ref_com, "com")
    for rot, mesa, antes in CONTAS_COM:
        for jeito, ks, tot_ref in (("na mesa", mesa, "B"), ("antes", antes, "C")):
            r += 1
            put(fl, f"A{r}", f"{rot}: punção {jeito}", font=F_B, fill=TOT)
            for col in "BC":
                put(fl, f"{col}{r}", None, fill=TOT)
            chave = {"Minutos de tomógrafo por exame": "tom", "Exames por hora de tomógrafo": "porh",
                     "Minutos em cadeira ou maca (preparo e repouso)": "cad",
                     "Tempo do paciente na unidade": "pac"}[rot]
            RD[f"{chave}_{'mesa' if jeito == 'na mesa' else 'antes'}"] = r
            link(fl, f"D{r}", f"=G{TOTS[tot_ref][chave]}", "0.0" if chave == "porh" else "0")
            for i in range(3):
                c = L(5 + i)
                if ks is None:
                    alvo = RD[f"tom_{'mesa' if jeito == 'na mesa' else 'antes'}"]
                    f = f'=IF(N({c}{alvo})>0,60/{c}{alvo},"")'
                    fmt = "0.0"
                else:
                    f = falta_ou_soma([f"{c}{RD['com'][k]}" for k in ks]).replace('"—"', '""')
                    fmt = "General"
                put(fl, f"{c}{r}", f, fmt, F_B, TOT, alin=CENTRO)
    r += 2
    nota(fl, r, "Na referência, o exame com contraste leva 11 min com a punção na mesa e 13 com ela antes (estudo de "
                "08/11), e o bloco C tem a orientação em grupo; por isso a coluna D das contas liga nos blocos B e C, "
                "e não na soma da coluna.")
    nota(fl, r + 1, "Quem decide o contraste: o pedido médico indica; o radiologista confirma (Parecer CFM 17/2019), "
                    "de preferência na véspera, ao rever o pedido, e de novo na triagem do dia.")
    nota(fl, r + 2, "As fontes completas, com os 16 tempos medidos e a lista de 49 fontes, estão no estudo de 08/11 "
                    "(abas 1 e Fontes).")
    fl.freeze_panes = "B4"

    # ---------------------------------------------------------------- aba 3: premissas da carteira (no topo)
    titulo(tp, "3 polos em 12 meses, contra 5 e 6 polos em 8: o que cada tomógrafo precisa fazer",
           "Carteira 1 (14.401 TC). Os minutos vêm da aba 1 (central). As células amarelas são premissas.")
    secao(tp, 4, "Premissas: a tomografia da carteira 1", 2)
    prem = [
        ("com", "TC com contraste", 14053, INT, "estudo de 08/11, aba 3 (11.700 + 2.353)"),
        ("conv", "   dos quais podem ir sem contraste (abdômen, pelve, tórax, pescoço, face e crânio)", 11700, INT,
         "estudo de 08/11, aba 3"),
        ("sem0", "TC sem contraste", 348, INT, "estudo de 08/11, aba 3"),
        ("p", "Parte dos que podem ir sem contraste que o radiologista faz sem", 0.10, PCT,
         "premissa de planejamento (08/11, seção 7)"),
        ("dias", "Dias úteis por mês", 21, INT, "v26, 7.3"),
    ]
    LT = {}
    r = 5
    for k, rot, v, fmt, fonte in prem:
        LT[k] = r
        put(tp, f"A{r}", rot)
        entrada(tp, f"B{r}", v, fmt)
        put(tp, f"C{r}", fonte, font=F_S, borda=False, alin=NOWRAP)
        r += 1
    LT["util"] = r
    put(tp, f"A{r}", "Parte das horas abertas com exame")
    link(tp, f"B{r}", "='2 Por hora'!B5", PCT)
    put(tp, f"C{r}", "aba 2", font=F_S, borda=False, alin=NOWRAP)
    for k, rot, f in [("c", "Exames com contraste, depois da conversão", "=B{com}-B{conv}*B{p}"),
                      ("s", "Exames sem contraste, depois da conversão", "=B{sem0}+B{conv}*B{p}")]:
        r += 1
        LT[k] = r
        put(tp, f"A{r}", rot)
        put(tp, f"B{r}", f.format(**LT), INT)
    r += 1
    LT["tot"] = r
    put(tp, f"A{r}", "Total de TC", font=F_B, fill=TOT)
    put(tp, f"B{r}", f"=B{LT['c']}+B{LT['s']}", INT, F_B, TOT)
    r += 1
    LT["pc"] = r
    put(tp, f"A{r}", "Parte com contraste")
    put(tp, f"B{r}", f"=B{LT['c']}/B{LT['tot']}", PCT)
    C_, S_, TOTc = (f"'3 Três polos'!$B${LT[k]}" for k in ("c", "s", "tot"))
    c_, s_, tot_, dias_, util_ = (f"$B${LT[k]}" for k in ("c", "s", "tot", "dias", "util"))

    # ---------------------------------------------------------------- aba 2: por hora
    titulo(ph, "Quantos exames cada tomógrafo faz por hora, e quantas cadeiras ou macas o fluxo pede",
           "Por hora de exame (o aparelho trabalhando) e por hora aberta (descontadas as horas sem exame: atrasos, "
           "encaixes, limpeza e pausas).")
    secao(ph, 4, "Premissas", 3)
    prem2 = [
        ("Parte das horas abertas com exame", 0.8, PCT,
         "estudo de 08/11, aba 3; no Canadá, 2,34 exames por hora aberta (CDA-AMC 2025). Inclui as pausas (aba 5)"),
        ("Horas abertas por dia", 10, INT, "v26, 7.3"),
        ("Horas de um turno", 4, INT, "para comparar por turno"),
        ("Minutos de tomógrafo com contraste: punção antes e as medidas que agilizam", 13, INT,
         "estudo de 08/11, aba 8 e fluxo E da aba 2"),
    ]
    for i, (rot, v, fmt, fonte) in enumerate(prem2):
        put(ph, f"A{5 + i}", rot)
        entrada(ph, f"B{5 + i}", v, fmt)
        put(ph, f"C{5 + i}", fonte, font=F_S, borda=False, alin=NOWRAP)

    secao(ph, 10, "1. Por fluxo, com os tempos de referência (aba 1)", 9)
    cab(ph, 11, ["Fluxo", "Minutos de tomógrafo", "Por hora de exame", "Por hora aberta", "Por dia (10 h)",
                 "Pior caso, por hora", "Melhor caso, por hora", "Minutos em cadeira ou maca",
                 "Cadeiras ou macas ao mesmo tempo, com 1 de folga"], altura=52)
    fluxos = [("Sem contraste", "A"), ("Com contraste, punção na mesa (em série)", "B"),
              ("Com contraste, punção antes (em linha)", "C"),
              ("Com contraste, punção antes e as medidas que agilizam", None)]
    LP = {}
    for i, (rot, b) in enumerate(fluxos):
        r = 12 + i
        LP[i] = r
        put(ph, f"A{r}", rot, font=F_B)
        if b:
            t = TOTS[b]
            link(ph, f"B{r}", f"='1 Fluxo TC'!G{t['tom']}", "0")
            link(ph, f"F{r}", f"=60/'1 Fluxo TC'!H{t['tom']}", "0.0")
            link(ph, f"G{r}", f"=60/'1 Fluxo TC'!F{t['tom']}", "0.0")
            link(ph, f"H{r}", f"='1 Fluxo TC'!G{t['cad']}", "0")
            put(ph, f"I{r}", f'=IF(H{r}>0,ROUNDUP(C{r}*H{r}/60,0)+1,0)', INT, F_B)
        else:
            put(ph, f"B{r}", "=$B$8", "0")
            for col in "FGHI":
                put(ph, f"{col}{r}", None)
        put(ph, f"C{r}", f"=60/B{r}", "0.0", F_B)
        put(ph, f"D{r}", f"=C{r}*$B$5", "0.0")
        put(ph, f"E{r}", f"=D{r}*$B$6", "0")
    nota(ph, 16, "Cadeiras ou macas: exames por hora × minutos em cadeira ou maca ÷ 60, arredondado para cima, mais "
                 "1 de folga (como no estudo de 08/11, aba 4). Contam o preparo com a punção antes e o repouso.")

    secao(ph, 18, "2. Na carteira 1, que mistura exames com e sem contraste (aba 3)", 9)
    cab(ph, 19, ["Fluxo do exame com contraste", "Minutos médios por exame", "Por hora de exame",
                 "Por hora aberta", "Por dia (10 h)", "Por turno (4 h)"], altura=40)
    for i, (rot, lr) in enumerate([("Punção na mesa (em série)", LP[1]), ("Punção antes (em linha)", LP[2]),
                                   ("Punção antes e as medidas que agilizam", LP[3])]):
        r = 20 + i
        put(ph, f"A{r}", rot, font=F_B)
        put(ph, f"B{r}", f"=({C_}*B{lr}+{S_}*$B${LP[0]})/{TOTc}", "0.0")
        put(ph, f"C{r}", f"=60/B{r}", "0.0", F_B)
        put(ph, f"D{r}", f"=C{r}*$B$5", "0.0")
        put(ph, f"E{r}", f"=D{r}*$B$6", "0")
        put(ph, f"F{r}", f"=D{r}*$B$7", "0")
    put(ph, "A23", f"=\"Com \"&TEXT('3 Três polos'!B{LT['p']}*100,\"0\")&\"% dos que podem ir sem contraste "
                   f"convertidos, \"&TEXT('3 Três polos'!B{LT['pc']}*100,\"0\")&\"% da TC da carteira 1 fica com "
                   f"contraste.\"", font=F_S, borda=False, alin=NOWRAP)

    secao(ph, 25, "3. Por resposta da equipe assistencial (aba 1, bloco D)", 9)
    cab(ph, 26, ["Resposta", "Sem contraste: minutos", "Sem contraste: por hora", "Punção na mesa: minutos",
                 "Punção na mesa: por hora", "Punção antes: minutos", "Punção antes: por hora",
                 "Punção antes: minutos em cadeira ou maca", "Punção antes: cadeiras ou macas"], altura=52)
    for i in range(3):
        r = 27 + i
        c = L(5 + i)
        link(ph, f"A{r}", nome_resp(i))
        link(ph, f"B{r}", f"='1 Fluxo TC'!{c}{RD['sem_tom']}", "General")
        put(ph, f"C{r}", f'=IF(N(B{r})>0,60/B{r},"")', "0.0", F_B)
        link(ph, f"D{r}", f"='1 Fluxo TC'!{c}{RD['tom_mesa']}", "General")
        put(ph, f"E{r}", f'=IF(N(D{r})>0,60/D{r},"")', "0.0", F_B)
        link(ph, f"F{r}", f"='1 Fluxo TC'!{c}{RD['tom_antes']}", "General")
        put(ph, f"G{r}", f'=IF(N(F{r})>0,60/F{r},"")', "0.0", F_B)
        link(ph, f"H{r}", f"='1 Fluxo TC'!{c}{RD['cad_antes']}", "General")
        put(ph, f"I{r}", f'=IF(AND(N(G{r})>0,N(H{r})>0),ROUNDUP(G{r}*H{r}/60,0)+1,"")', INT, F_B)

    # ---------------------------------------------------------------- aba 3: o resto
    r = LT["pc"] + 2
    secao(tp, r, "1. Os três arranjos", 4)
    r += 1
    cab(tp, r, ["", "6 polos, 8 meses", "5 polos, 8 meses", "3 polos, 12 meses"])
    r += 1
    LA = {"n": r, "m": r + 1}
    put(tp, f"A{r}", "Tomógrafos (um por polo)")
    for col, v in zip("BCD", (6, 5, 3)):
        entrada(tp, f"{col}{r}", v, INT)
    r += 1
    put(tp, f"A{r}", "Meses de execução")
    for col, v in zip("BCD", (8, 8, 12)):
        entrada(tp, f"{col}{r}", v, INT)
    linhas = [
        ("tm", "Tomógrafo-mês", lambda c: f"={c}{LA['n']}*{c}{LA['m']}", INT, False),
        ("dtm", "Diferença sobre 6 polos em 8 meses", lambda c: f"={c}{{tm}}/$B${{tm}}-1", PCT, False),
        ("pm", "TC por tomógrafo, por mês", lambda c: f"={tot_}/{c}{{tm}}", INT, True),
        ("pd", "TC por tomógrafo, por dia útil", lambda c: f"={tot_}/({c}{{tm}}*{dias_})", DEC1, True),
        ("dpm", "Exames a mais por tomógrafo, sobre 6 polos", lambda c: f"={c}{{pm}}/$B${{pm}}-1", PCT, False),
    ]
    for k, rot, fn, fmt, negrito in linhas:
        r += 1
        LA[k] = r
        put(tp, f"A{r}", rot, font=F_B if negrito else F)
        for col in "BCD":
            put(tp, f"{col}{r}", fn(col).format(**LA), fmt, F_B if negrito else F)
    r += 1
    put(tp, f"A{r}", "Horas por dia útil que cada tomógrafo precisa ficar aberto para o projeto", font=F_B, fill=TOT)
    for col in "BCD":
        put(tp, f"{col}{r}", None, fill=TOT)
    sem_min = f"'2 Por hora'!$B${LP[0]}"
    for k, rot, tc in [("h_mesa", "com contraste, punção na mesa", f"'2 Por hora'!$B${LP[1]}"),
                       ("h_antes", "com contraste, punção antes", f"'2 Por hora'!$B${LP[2]}"),
                       ("h_med", "com contraste, punção antes e as medidas que agilizam", f"'2 Por hora'!$B${LP[3]}")]:
        r += 1
        LA[k] = r
        put(tp, f"A{r}", "   " + rot)
        for col in "BCD":
            put(tp, f"{col}{r}", f"=({c_}*{tc}+{s_}*{sem_min})/60/({col}${LA['tm']}*{dias_})/{util_}", DEC1, F_B)
    r += 1
    put(tp, f"A{r}", "Horas por dia com radiologista na unidade (só o contraste)", font=F_B, fill=TOT)
    for col in "BCD":
        put(tp, f"{col}{r}", None, fill=TOT)
    for k, rot, tc in [("r_mesa", "punção na mesa", f"'2 Por hora'!$B${LP[1]}"),
                       ("r_antes", "punção antes", f"'2 Por hora'!$B${LP[2]}")]:
        r += 1
        LA[k] = r
        put(tp, f"A{r}", "   " + rot)
        for col in "BCD":
            put(tp, f"{col}{r}", f"=({c_}*{tc})/60/({col}${LA['tm']}*{dias_})/{util_}", DEC1)
    r += 1
    nota(tp, r, "O radiologista precisa estar na unidade durante todo exame com contraste, até a alta (Parecer CFM "
                "17/2019). As horas por dia já contam as horas abertas sem exame.")
    r += 2
    secao(tp, r, "2. O limite com 3 tomógrafos em 12 meses: até quantos minutos por exame com contraste cabem", 4)
    r += 1
    cab(tp, r, ["Horas por dia útil que cada tomógrafo fica para o projeto", "Minutos por exame com contraste, no "
                "máximo", "Cabe com punção na mesa?", "Cabe com punção antes?"], altura=40)
    n3, m3 = f"$D${LA['n']}", f"$D${LA['m']}"
    lim0 = r + 1
    for h in range(4, 11):
        r += 1
        entrada(tp, f"A{r}", h, INT, alin=CENTRO)
        put(tp, f"B{r}", f"=({n3}*{m3}*{dias_}*A{r}*60*{util_}-{s_}*{sem_min})/{c_}", DEC1, F_B, alin=CENTRO)
        put(tp, f"C{r}", f"=IF(B{r}>='2 Por hora'!$B${LP[1]},\"sim\",\"não\")", alin=CENTRO)
        put(tp, f"D{r}", f"=IF(B{r}>='2 Por hora'!$B${LP[2]},\"sim\",\"não\")", alin=CENTRO)
    rng = f"C{lim0}:D{r}"
    tp.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=['"sim"'], fill=VERDE_CF,
                                                  font=F_VERDE_CF))
    tp.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=['"não"'], fill=VERMELHO_CF,
                                                  font=F_VERMELHO_CF))
    r += 1
    nota(tp, r, "O exame sem contraste fica com o tempo central da aba 1. A carteira se divide igual pelos 3 "
                "tomógrafos.")
    r += 2
    secao(tp, r, "3. Meses para fazer toda a TC da carteira com 3 tomógrafos", 6)
    r += 1
    put(tp, f"A{r}", "Horas por dia (linhas) × minutos por exame com contraste (colunas)", font=F_B, fill=CAB)
    for col, v in zip("BCDEF", (13, 15, 17, 20, 25)):
        entrada(tp, f"{col}{r}", v, INT, alin=CENTRO)
    hm = r
    m0 = r + 1
    for h in range(4, 11):
        r += 1
        entrada(tp, f"A{r}", h, INT, alin=CENTRO)
        for col in "BCDEF":
            put(tp, f"{col}{r}", f"=({c_}*{col}${hm}+{s_}*{sem_min})/60/({n3}*{dias_}*$A{r}*{util_})", DEC1,
                alin=CENTRO)
    tp.conditional_formatting.add(f"B{m0}:F{r}", CellIsRule(operator="lessThanOrEqual", formula=[m3],
                                                            fill=VERDE_CF, font=F_VERDE_CF))
    tp.conditional_formatting.add(f"B{m0}:F{r}", CellIsRule(operator="greaterThan", formula=[m3],
                                                            fill=VERMELHO_CF, font=F_VERMELHO_CF))
    r += 1
    nota(tp, r, "Verde: cabe nos meses do arranjo de 3 polos (célula D da seção 1). 13 min é a punção antes com as "
                "medidas; 15, a punção antes; 20, a punção na mesa; 25, a punção difícil.")

    # ---------------------------------------------------------------- aba 4: ultrassom
    titulo(ul, "Ultrassom por tipo de exame: minutos de sala, exames por hora e salas",
           "Referência: o CBR 2017 (agenda = minutos de sala; posicionado = exame), como no estudo de 07/11, seção "
           "2.1. As respostas entram na seção 2; a seção 1 compara pela média delas.")
    secao(ul, 4, "Premissas", 3)
    put(ul, "A5", "Dias úteis em 12 meses")
    link(ul, "B5", f"='3 Três polos'!B{LT['dias']}*12", INT)
    put(ul, "C5", "aba 3: dias úteis por mês × 12", font=F_S, borda=False, alin=NOWRAP)
    put(ul, "A6", "Horas abertas por dia")
    link(ul, "B6", "='2 Por hora'!B6", INT)
    put(ul, "A7", "Parte das horas abertas com exame")
    link(ul, "B7", "='2 Por hora'!B5", PCT)
    put(ul, "C7", "aba 2", font=F_S, borda=False, alin=NOWRAP)

    secao(ul, 9, "1. Referência e média das respostas, por exame", 11)
    cab(ul, 10, ["Exame", "Exames (carteira 1)", "Preparo fora da sala", "Sala, CBR (agenda)", "Exame, CBR "
                 "(posicionado)", "Por hora (CBR)", "Horas de sala (CBR)", "Sala, respostas (média)",
                 "Por hora (respostas)", "Horas de sala (respostas)", "Diferença de horas"], altura=40)
    LU = {}
    secao_resp_inicio = 10 + len(EXAMES_US) + 5  # onde começa a seção 2
    BL = []  # primeira linha de exame de cada bloco de resposta
    for i in range(3):
        BL.append(secao_resp_inicio + 2 + i * (len(EXAMES_US) + 3))
    for j, (k, exame, preparo, agenda, posic, qtd) in enumerate(EXAMES_US):
        r = 11 + j
        LU[k] = r
        put(ul, f"A{r}", exame, font=F_B)
        entrada(ul, f"B{r}", qtd, INT)
        put(ul, f"C{r}", preparo)
        entrada(ul, f"D{r}", agenda, "0", alin=CENTRO)
        entrada(ul, f"E{r}", posic, "0", alin=CENTRO)
        put(ul, f"F{r}", f"=60/D{r}", "0.0", F_B)
        put(ul, f"G{r}", f"=B{r}*D{r}/60", INT)
        salas = ",".join(f"J{BL[i] + j}" for i in range(3))
        put(ul, f"H{r}", f'=IF(COUNT({salas})=0,"",AVERAGE({salas}))', "0.0", F_B)
        put(ul, f"I{r}", f'=IF(N(H{r})>0,60/H{r},"")', "0.0")
        put(ul, f"J{r}", f'=IF(N(H{r})>0,B{r}*H{r}/60,"")', INT)
        put(ul, f"K{r}", f'=IF(N(J{r})>0,J{r}-G{r},"")', INT)
    r = 11 + len(EXAMES_US)
    u0, u1 = 11, r - 1
    put(ul, f"A{r}", "Total", font=F_B, fill=TOT)
    put(ul, f"B{r}", f"=SUM(B{u0}:B{u1})", INT, F_B, TOT)
    for col in "CDEF":
        put(ul, f"{col}{r}", None, fill=TOT)
    put(ul, f"G{r}", f"=SUM(G{u0}:G{u1})", INT, F_B, TOT)
    put(ul, f"H{r}", None, fill=TOT)
    put(ul, f"I{r}", None, fill=TOT)
    put(ul, f"J{r}", f'=IF(COUNT(J{u0}:J{u1})<{len(EXAMES_US)},"",SUM(J{u0}:J{u1}))', INT, F_B, TOT)
    put(ul, f"K{r}", f'=IF(N(J{r})>0,J{r}-G{r},"")', INT, F_B, TOT)
    r += 1
    put(ul, f"A{r}", "Salas na rede em 12 meses, sem arredondar por polo", font=F_B)
    put(ul, f"G{r}", f"=G{r - 1}/($B$5*$B$6*$B$7)", DEC1, F_B)
    put(ul, f"J{r}", f'=IF(N(J{r - 1})>0,J{r - 1}/($B$5*$B$6*$B$7),"")', DEC1, F_B)
    r += 1
    nota(ul, r, "Arredondando polo a polo, o estudo de 07/11 achou 15 salas pela agenda do CBR e 13 com o preparo fora "
                "da sala. A média das respostas só fecha o total quando os 12 exames tiverem resposta.")

    secao(ul, secao_resp_inicio, "2. As respostas, uma tabela por pessoa (minutos de cada parte, como no "
                                  "formulário)", 11)
    for i in range(3):
        r0 = BL[i] - 1
        link(ul, f"A{r0}", nome_resp(i), bold=True)
        ul[f"A{r0}"].fill = CAB
        cab(ul, r0, PARTES_US + ["Minutos de sala", "Por hora"], col0=3)
        put(ul, f"B{r0}", None, fill=CAB)
        ul.row_dimensions[r0].height = 40
        for j, (k, exame, *_) in enumerate(EXAMES_US):
            rr = BL[i] + j
            put(ul, f"A{rr}", exame)
            put(ul, f"B{rr}", None)
            for col in "CDEFG":
                entrada(ul, f"{col}{rr}", None, alin=CENTRO)
            put(ul, f"H{rr}", None)
            put(ul, f"I{rr}", None)
            # minutos de sala = as quatro partes na sala (colunas D a G)
            put(ul, f"J{rr}", falta_ou_soma([f"{c}{rr}" for c in "DEFG"]).replace('"—"', '""'), "General", F_B,
                alin=CENTRO)
            put(ul, f"K{rr}", f'=IF(N(J{rr})>0,60/J{rr},"")', "0.0", alin=CENTRO)
    # cabeçalho das respostas: as partes vão de C a G, sala em J e por hora em K
    for i in range(3):
        r0 = BL[i] - 1
        for col, t in zip("CDEFG", PARTES_US):
            put(ul, f"{col}{r0}", t, font=F_B, fill=CAB)
        put(ul, f"H{r0}", None, fill=CAB)
        put(ul, f"I{r0}", None, fill=CAB)
        put(ul, f"J{r0}", "Minutos de sala", font=F_B, fill=CAB)
        put(ul, f"K{r0}", "Por hora", font=F_B, fill=CAB)
    ul.freeze_panes = "B4"

    # ---------------------------------------------------------------- aba 5: equipe
    titulo(eq, "Equipe para 10 horas por dia útil: um tomógrafo e uma sala de ultrassom",
           "Referência: o quadro da v26 (4.15), as jornadas e o auxiliar de sala do ultrassom. Pessoas = pessoas ao "
           "mesmo tempo × horas por dia × dias por semana ÷ jornada semanal, antes de férias e faltas.")
    secao(eq, 4, "Premissas", 3)
    prem4 = [
        ("horas", "Horas abertas por dia", "='2 Por hora'!B6", INT, "aba 2", True),
        ("dias", "Dias úteis por semana", 5, INT, "v26, 7.3", False),
        ("j_rad", "Jornada semanal do técnico em radiologia (horas)", 24, INT, "Lei 7.394/1985, art. 14", False),
        ("j_clt", "Jornada semanal da enfermagem, do auxiliar e da recepção (horas)", 44, INT, "v26, 4.15 (CLT)",
         False),
        ("med_ano", "Horas por ano de cada médico", 1800, INT, "v26, 4.15", False),
    ]
    LE = {}
    r = 5
    for k, rot, v, fmt, fonte, eh_link in prem4:
        LE[k] = r
        put(eq, f"A{r}", rot)
        (link if eh_link else entrada)(eq, f"B{r}", v, fmt)
        put(eq, f"C{r}", fonte, font=F_S, borda=False, alin=NOWRAP)
        r += 1
    LE["j_med"] = r
    put(eq, f"A{r}", "Jornada semanal de cada médico (horas)")
    put(eq, f"B{r}", f"=B{LE['med_ano']}/52", DEC1)
    put(eq, f"C{r}", "horas por ano ÷ 52 semanas", font=F_S, borda=False, alin=NOWRAP)
    horas_, dias_e = f"=$B${LE['horas']}", f"$B${LE['dias']}"
    j = {k: f"$B${LE[k]}" for k in ("j_rad", "j_clt", "j_med")}
    cab_eq = ["Função", "Pessoas ao mesmo tempo", "Horas por dia com essa presença", "Jornada semanal",
              "Horas por semana", "Pessoas (conta)", "Pessoas (arredondado)"] + RESP + ["De onde vem"]

    ROWEQ = {}

    def tabela_equipe(r, titulo_sec, linhas, total_rot):
        secao(eq, r, titulo_sec, 11)
        r += 1
        cab(eq, r, cab_eq, altura=40)
        for i in range(3):
            link(eq, f"{L(8 + i)}{r}", nome_resp(i), bold=True)
            eq[f"{L(8 + i)}{r}"].fill = CAB
        p = r + 1
        for rot, simul, horas_dia, jornada, resp, fonte in linhas:
            r += 1
            ROWEQ[rot] = r
            put(eq, f"A{r}", rot, font=F_B)
            entrada(eq, f"B{r}", simul, "0.0", alin=CENTRO)
            link(eq, f"C{r}", horas_dia, DEC1)
            link(eq, f"D{r}", f"={jornada}", DEC1)
            put(eq, f"E{r}", f"=B{r}*C{r}*{dias_e}", DEC1)
            put(eq, f"F{r}", f"=E{r}/D{r}", DEC2)
            put(eq, f"G{r}", f"=ROUNDUP(F{r},0)", INT, F_B)
            for i in range(3):
                col, cr = L(8 + i), CR[i]
                if resp:
                    link(eq, f"{col}{r}", f"=IF('6 Respostas'!{cr}{LR[resp]}=\"\",\"\",'6 Respostas'!{cr}{LR[resp]})",
                         INT)
                else:
                    put(eq, f"{col}{r}", None)
            put(eq, f"K{r}", fonte, font=F_S)
        u = r
        r += 1
        put(eq, f"A{r}", total_rot, font=F_B, fill=TOT)
        for col in "BCDEF":
            put(eq, f"{col}{r}", None, fill=TOT)
        put(eq, f"G{r}", f"=SUM(G{p}:G{u})", INT, F_B, TOT)
        for i in range(3):
            col = L(8 + i)
            put(eq, f"{col}{r}", f'=IF(COUNT({col}{p}:{col}{u})=0,"",SUM({col}{p}:{col}{u}))', INT, F_B, TOT)
        put(eq, f"K{r}", None, fill=TOT)
        return r

    h_contraste = f"='3 Três polos'!D{LA['r_antes']}"
    linhas_tc = [
        ("Técnico em radiologia", 1, horas_, j["j_rad"], "tc_tecrad",
         "Lei 7.394/1985, art. 14: 24 h semanais; v26, 4.15: 50 ÷ 24 = 2,08, arredondado para 3"),
        ("Enfermeiro ou técnico de enfermagem: 1ª pessoa, o dia todo", 1, horas_, j["j_clt"], "tc_enf",
         "v26, 4.15: 50 ÷ 44 = 1,14, arredondado para 2; com a punção na mesa, 1,0 pessoa ocupada (08/11, aba 4). "
         "A resposta traz o total de enfermagem"),
        ("Enfermeiro ou técnico de enfermagem: 2ª pessoa, no horário do contraste (só com a punção antes)", 1,
         h_contraste, j["j_clt"], None,
         "com a punção antes, 1,3 pessoa ocupada: 2 juntas no horário do contraste (08/11, aba 4); horas da aba 3"),
        ("Médico radiologista, presente no horário do contraste", 1, h_contraste, j["j_med"], "tc_radiol",
         "Parecer CFM 17/2019; horas da aba 3 (3 polos, punção antes; na mesa, 7,1 h). v26, 4.15: no mínimo 1 por "
         "tomógrafo, mais o médico de retaguarda"),
        ("Pessoal de recepção e preparo (por polo)", 1, horas_, j["j_clt"], "tc_rec",
         "v26, 4.15: 50 ÷ 44 = 1,14, arredondado para 2"),
        ("Outra função", 0, horas_, j["j_clt"], "tc_outro", "aba 6"),
    ]
    r = tabela_equipe(r + 2, "1. Um tomógrafo, 10 horas por dia útil", linhas_tc, "Total do tomógrafo")
    linhas_us = [
        ("Médico ultrassonografista", 1, horas_, j["j_med"], "us_med",
         "v26, 4.15: um médico por sala durante o exame; 1.800 h anuais por médico"),
        ("Auxiliar de sala do ultrassom (com o médico o exame todo)", 1, horas_, j["j_clt"], "us_aux",
         "função nova (pedido do usuário, 09/11): digita o laudo, ajuda o paciente, acompanha o transvaginal e o de "
         "próstata (v26, 4.16, g) e limpa o transdutor"),
        ("Pessoal de recepção e preparo (por polo; o mesmo da tomografia, se houver)", 1, horas_, j["j_clt"],
         "us_rec", "v26, 4.15: 50 ÷ 44 = 1,14, arredondado para 2"),
        ("Outra função", 0, horas_, j["j_clt"], "us_outro", "aba 6"),
    ]
    r = tabela_equipe(r + 2, "2. Uma sala de ultrassom, 10 horas por dia útil", linhas_us, "Total da sala")
    r += 1
    nota(eq, r, "Já no projeto e fora da conta: médico de retaguarda presencial e responsável técnico médico (1 por "
                "polo, v26, 4.15); supervisão de polo, assistente de agendamento, confirmação e busca ativa "
                "(pré-exame), operador de registro do pós-exame e assistente administrativo (quadro P2, estudo de "
                "07/11).")

    r += 2
    secao(eq, r, "3. Pausas", 11)
    r += 1
    cab(eq, r, ["", "Referência"])
    for i in range(3):
        link(eq, f"{L(8 + i)}{r}", nome_resp(i), bold=True)
        eq[f"{L(8 + i)}{r}"].fill = CAB
    put(eq, f"K{r}", "De onde vem", font=F_B, fill=CAB)
    r += 1
    lpm = r
    put(eq, f"A{r}", "Minutos de pausa por pessoa, num dia de trabalho")
    entrada(eq, f"B{r}", 60, INT, alin=CENTRO)
    for i in range(3):
        cr = CR[i]
        link(eq, f"{L(8 + i)}{r}", f"=IF('6 Respostas'!{cr}{LR['pausa_min']}=\"\",\"\","
                                   f"'6 Respostas'!{cr}{LR['pausa_min']})", INT)
    put(eq, f"K{r}", "CLT, art. 71: jornada acima de 6 h, intervalo de 1 a 2 h; de 4 a 6 h, 15 min", font=F_S)
    r += 1
    lpc = r
    put(eq, f"A{r}", "Nas pausas, o aparelho para ou alguém cobre?")
    entrada(eq, f"B{r}", "alguém cobre", alin=CENTRO)
    for i in range(3):
        cr = CR[i]
        link(eq, f"{L(8 + i)}{r}", f"=IF('6 Respostas'!{cr}{LR['pausa_cobre']}=\"\",\"\","
                                   f"'6 Respostas'!{cr}{LR['pausa_cobre']})")
    put(eq, f"K{r}", "a escala com 3 técnicos e 2 de enfermagem permite revezar", font=F_S)
    r += 1
    put(eq, f"A{r}", "Parte do dia de 10 h com o aparelho parado nas pausas", font=F_B)
    put(eq, f"B{r}", f'=IF(B{lpc}="para",B{lpm}/60/$B${LE["horas"]},0)', PCT, F_B, alin=CENTRO)
    for i in range(3):
        col = L(8 + i)
        put(eq, f"{col}{r}", f'=IF({col}{lpm}="","",IF({col}{lpc}="para",{col}{lpm}/60/$B${LE["horas"]},0))', PCT,
            F_B)
    put(eq, f"K{r}", "compara com os 20% de horas sem exame da aba 2, que já incluem as pausas", font=F_S)

    # turnos de 5 horas
    r += 2
    secao(eq, r, "4. Dois turnos de 5 horas no lugar da jornada cheia com revezamento", 11)
    r += 1
    lt = r
    put(eq, f"A{r}", "Duração do turno (horas)")
    entrada(eq, f"B{r}", 5, INT, alin=CENTRO)
    put(eq, f"C{r}", "pedido do usuário, 09/11", font=F_S, borda=False, alin=NOWRAP)
    r += 1
    lpt = r
    put(eq, f"A{r}", "Pausa por turno (minutos)")
    entrada(eq, f"B{r}", 15, INT, alin=CENTRO)
    put(eq, f"C{r}", "CLT, art. 71, § 1º: de 4 a 6 h de trabalho, 15 min", font=F_S, borda=False, alin=NOWRAP)
    r += 1
    put(eq, f"A{r}", "Parte do dia com o aparelho parado, se ele para em cada pausa", font=F_B)
    put(eq, f"B{r}", f"=ROUNDUP($B${LE['horas']}/B{lt},0)*B{lpt}/($B${LE['horas']}*60)", PCT, F_B, alin=CENTRO)
    put(eq, f"C{r}", "com jornada cheia e 1 h de almoço sem cobertura, seriam 10%", font=F_S, borda=False,
        alin=NOWRAP)
    r += 2
    cab(eq, r, ["Função", "Pessoas ao mesmo tempo", "Turnos por dia", "Turnos por semana", "Jornada semanal",
                "Turnos por pessoa por semana", "Pessoas", "Horas por pessoa por semana", "Pessoas na jornada cheia",
                "Diferença", "Como lê"], altura=40)
    turnos = [
        ("Técnico em radiologia", 1, "dia", j["j_rad"], "a lei limita a 24 h: 4 turnos de 5 h por pessoa"),
        ("Enfermeiro ou técnico de enfermagem: 1ª pessoa, o dia todo", 1, "dia", j["j_clt"],
         "um turno por dia por pessoa"),
        ("Enfermeiro ou técnico de enfermagem: 2ª pessoa, no horário do contraste (só com a punção antes)", 1,
         "contraste", j["j_clt"], "o contraste passa de 5 h e ocupa os dois turnos"),
        ("Médico radiologista, presente no horário do contraste", 1, "contraste", j["j_med"],
         "o contraste passa de 5 h: um radiologista por turno; se couber num turno, 1"),
        ("Pessoal de recepção e preparo (por polo)", 1, "dia", j["j_clt"], "um de manhã e um à tarde"),
        ("Médico ultrassonografista", 1, "dia", j["j_med"], "um de manhã e um à tarde"),
        ("Auxiliar de sala do ultrassom (com o médico o exame todo)", 1, "dia", j["j_clt"],
         "um de manhã e um à tarde"),
    ]
    p = r + 1
    for rot, simul, tipo, jornada, como in turnos:
        r += 1
        put(eq, f"A{r}", rot, font=F_B)
        entrada(eq, f"B{r}", simul, "0", alin=CENTRO)
        horas_tipo = f"$B${LE['horas']}" if tipo == "dia" else f"'3 Três polos'!$D${LA['r_antes']}"
        put(eq, f"C{r}", f"=ROUNDUP({horas_tipo}/$B${lt},0)", INT, alin=CENTRO)
        put(eq, f"D{r}", f"=C{r}*{dias_e}", INT, alin=CENTRO)
        link(eq, f"E{r}", f"={jornada}", DEC1)
        put(eq, f"F{r}", f"=MIN({dias_e},INT(E{r}/$B${lt}))", INT, alin=CENTRO)
        put(eq, f"G{r}", f"=ROUNDUP(B{r}*D{r}/F{r},0)", INT, F_B, alin=CENTRO)
        put(eq, f"H{r}", f"=B{r}*D{r}*$B${lt}/G{r}", DEC1, alin=CENTRO)
        link(eq, f"I{r}", f"=G{ROWEQ[rot]}", INT)
        put(eq, f"J{r}", f"=G{r}-I{r}", '+0;-0;0', F_B, alin=CENTRO)
        put(eq, f"K{r}", como, font=F_S)
    tc_u = p + 4
    r += 1
    put(eq, f"A{r}", "Total do tomógrafo (5 primeiras linhas)", font=F_B, fill=TOT)
    for col in "BCDEF":
        put(eq, f"{col}{r}", None, fill=TOT)
    for col in "GI":
        put(eq, f"{col}{r}", f"=SUM({col}{p}:{col}{tc_u})", INT, F_B, TOT)
    put(eq, f"H{r}", None, fill=TOT)
    put(eq, f"J{r}", f"=G{r}-I{r}", '+0;-0;0', F_B, TOT)
    put(eq, f"K{r}", None, fill=TOT)
    r += 1
    nota(eq, r, "Com turnos de 5 h, as pessoas trabalham menos horas cada (25 h por semana na CLT). O número só cresce "
                "onde o contraste ocupa os dois turnos: o radiologista e a 2ª pessoa de enfermagem.")
    r += 1
    nota(eq, r, "Se o contraste couber num turno de 5 h (com a punção antes e as medidas que agilizam, são 4,6 h por "
                "dia), o radiologista e a 2ª de enfermagem voltam a 1 cada.")

    # ---------------------------------------------------------------- Leia
    linhas_leia = [
        ("Tomografia em 3 polos e 12 meses e ultrassom por exame: tempo, exames por hora e equipe", F_T),
        ("Estudo interno de 09/11/2026, a pedido do usuário. Base: carteira 1 (14.401 TC e 65.132 US). Os tempos são "
         "os de referência (estudos de 07/11 e 08/11) até a equipe assistencial responder.", F_S),
        ("", F),
        ("O que tem em cada aba", F_B),
        ("1 Fluxo TC: o passo a passo sem contraste, com a punção na mesa e com a punção antes: minutos, quem faz, "
         "onde o paciente fica, se ocupa o tomógrafo e a fonte. O bloco D recebe as respostas, com as duas punções.", F),
        ("2 Por hora: exames por hora de cada tomógrafo e as cadeiras ou macas do preparo e do repouso; a mistura da "
         "carteira 1; e cada resposta.", F),
        ("3 Três polos: 6 polos em 8 meses, 5 em 8 e 3 em 12; as horas por dia de cada tomógrafo; o limite de "
         "minutos por exame com contraste; os meses em cada combinação.", F),
        ("4 Ultrassom: os 12 tipos de exame da carteira, com o tempo de sala do CBR, as horas de sala e as salas na "
         "rede; e uma tabela por resposta.", F),
        ("5 Equipe: a equipe de referência para 10 horas de um tomógrafo e de uma sala de ultrassom, com os cargos do "
         "plano e o auxiliar de sala; a de cada resposta ao lado; e as pausas.", F),
        ("6 Respostas: equipe, pausas e observações de cada pessoa.", F),
        ("", F),
        ("Quando as respostas chegarem", F_B),
        ("1. Os minutos da TC vão na aba 1, bloco D (colunas E a G).", F),
        ("2. Os minutos do ultrassom vão na aba 4, seção 2, uma tabela por pessoa.", F),
        ("3. A equipe, as pausas e as observações vão na aba 6.", F),
        ("", F),
        ("Cores", F_B),
        ("Amarelo com fonte azul: premissa ou resposta, pode mudar. Verde: vem de outra aba. Preto: conta.", F),
        ("", F),
        ("Fontes e arquivos ligados", F_B),
        ("Estudo de 08/11 (estudo_contraste_fluxo_tempo_20261108): os tempos de cada etapa da TC, a carteira 1, a "
         "enfermagem e as cadeiras do repouso e as medidas que agilizam.", F),
        ("Estudo de 07/11 (estudo_12_meses_3_tomografos_20261107): os 12 meses, os 3 polos, o fluxo em linha, o "
         "ultrassom por grupo de exame (CBR 2017) e o quadro P2.", F),
        ("Plano v26 (PT v1), 4.15: a equipe assistencial e as jornadas; 4.16 (g): o acompanhante no transvaginal e "
         "no de próstata.", F),
        ("O formulário enviado ao grupo: tempos_e_equipe_tomografia_ultrassom_20261109.xlsx. O texto da mensagem "
         "está no .md deste estudo.", F),
        ("Gerado por gerar_tempos_tomografia_20261109.py.", F_S),
    ]
    for i, (t, fnt) in enumerate(linhas_leia):
        put(leia, f"A{i + 1}", t, font=fnt, borda=False)

    wb.save(SAIDA_ESTUDO)
    return {"TOTS": TOTS, "RD": RD, "LT": LT, "LA": LA, "LP": LP, "LU": LU, "BL": BL, "LR": LR, "LE": LE}


if __name__ == "__main__":
    formulario(SAIDA_FORM)
    formulario(SAIDA_REF, ref=True)
    pos = estudo()
    print(SAIDA_FORM)
    print(SAIDA_REF)
    print(SAIDA_ESTUDO)
    print(pos)
