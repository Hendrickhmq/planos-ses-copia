"""Custos e margens do plano 4: a planilha final, pela nossa conta ou pela conta do Sebastião.

    python3 gerar_custos_e_margens_nosso_20261111.py             -> final.xlsx (a nossa conta)
    python3 gerar_custos_e_margens_nosso_20261111.py sebastiao   -> final_sebastiao.xlsx (os valores do ofício do parceiro)

As duas têm as mesmas quatro abas e os mesmos exames (carteira v3), para comparar linha a linha:
  Simulador - uma linha por exame: troque a quantidade (e o tipo, o preço, os minutos e a parte da tomografia feita com
              contraste) e veja a margem de cada exame e do conjunto, se o valor fecha e se cabe nas salas.
              As quantidades moram aqui: as abas Custos e Volume vão atrás delas.
  Custos    - quantidades (vindas do Simulador), valores unitários, o custo dos exames na rede, a margem e o valor
              final por exame.
  Pessoas   - quantas pessoas a conta põe por sala e por polo, e o que fica sem preço.
  Volume    - o custo por exame do ultrassom conforme o volume, com as salas fixas e acompanhando o volume.
  Médico    - só na nossa conta (12/11): o médico do ultrassom pago pelo tempo do exame (valor da hora × minutos de
              sala), ao lado do pagamento por exame (R$ 35 e R$ 40); por exame, por médico e com outros valores da hora.
              A aba Custos escolhe qual dos dois entra na conta.

Nossa conta: a coluna "nosso" de custos_e_margens_sebastiao_x_nosso_20261111.xlsx, com as trocas do usuário de 11/11
(médico R$ 35 e R$ 40; auxiliar R$ 3.180; tomografia R$ 180 + R$ 50).
Conta do Sebastião: ../estudos/planilha_custos_sebastião.xlsx (rascunho de ofício do ISHP de 09/11/2026), com a
garantia mínima do médico por plantão, a gestão dentro do exame e o tempo do estudo dele (70 ultrassons em 9 horas).

Tudo é fórmula: azul = premissa que pode ser trocada. Controle interno.
Fontes: roteiro_reuniao_20261110.md (seção 4), estudo_tempos_tomografia_3_polos_20261109.md (seção 7),
estudo_12_meses_3_tomografos_20261107.md e carteira_final_v3_20261111.xlsx, em ../estudos/.
"""
import sys
from pathlib import Path

from openpyxl import Workbook
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

FONTE = "Arial"
AZUL = Font(name=FONTE, size=10, color="0000FF")
VERDE = Font(name=FONTE, size=10, color="008000")
PRETO = Font(name=FONTE, size=10)
NEGRITO = Font(name=FONTE, size=10, bold=True)
TITULO = Font(name=FONTE, size=14, bold=True)
SECAO = Font(name=FONTE, size=11, bold=True, color="FFFFFF")
NOTA = Font(name=FONTE, size=9, italic=True, color="555555")
VERMELHO = Font(name=FONTE, color="C00000", bold=True)
F_SECAO = PatternFill("solid", fgColor="1F4E78")
F_CAB = PatternFill("solid", fgColor="D9E1F2")
F_TOTAL = PatternFill("solid", fgColor="F2F2F2")
F_ALERTA = PatternFill("solid", fgColor="FCE4D6")
F_BOM = PatternFill("solid", fgColor="E2EFDA")
FINA = Side(style="thin", color="BFBFBF")
BORDA = Border(left=FINA, right=FINA, top=FINA, bottom=FINA)

REAL = 'R$ #,##0.00'
INT = '#,##0'
DEC = '#,##0.0'
PCT = '0.0%'

# ============================================================ PERFIS
# Cada premissa: (valor, observação). None = a linha não existe nesse perfil.
NOSSO = {
    "saida": "final.xlsx",
    "titulo": "Custos e margens do plano 4: a nossa conta",
    "fonte": "Estudos de 07/11 a 11/11 (roteiro da reunião, estudo de tempos e carteira v3), com os valores do usuário de 11/11 "
             "para médico, auxiliar de sala e tomografia.",
    "meses": (12, "estudo de 07/11 (o plano assinado tem 8)"),
    "dias": (21, "252 no ano, sem descontar feriados"),
    "salas": (14, "carteira v3"),
    "unid_rot": "Polos de ultrassom",
    "unid": (6, "um por Região"),
    "h_dia": (8, "sala aberta 10 h, com 80% das horas em exame"),
    "med_sem": (35, "usuário, 11/11"),
    "med_com": (40, "usuário, 11/11"),
    "med_hora": (100, "alternativa ao pagamento por exame: só entra na última coluna de margem por hora do Simulador. "
                      "A seleção do IgesDF paga R$ 174,30"),
    "med_h_rot": "R$ 100 por hora",
    # 12/11: o médico pago pelo tempo do exame (pedido do usuário: a tireoide paga menos que um exame que demora mais)
    "med_modo": ("pelo tempo", "pelo tempo: valor da hora (abaixo) × minutos de sala do exame, aba Médico; por exame: "
                               "R$ 35 sem Doppler e R$ 40 com Doppler, o mesmo para qualquer exame"),
    "med_tempo_h": (101.71, "mantém o gasto com médico de hoje na carteira v3 (R$ 2.749.335 em 27.031 h de sala); "
                            "R$ 1,70 por minuto. A aba Médico, seção 3, compara com R$ 100 e com R$ 174,30"),
    "med_dop_ad": (0, "pelo tempo, o Doppler já recebe mais por demorar mais; um adicional pagaria também a "
                      "especialização (com ele, a hora que mantém o gasto cai: aba Médico, seção 3)"),
    "garantia": None,
    "aux": (3180, "usuário, 11/11: posto com provisões"),
    "n_aux": (2, "fica com o médico o exame todo e digita o laudo; 2 para cobrir as 10 h"),
    "rec": (2959, "salário de recepcionista de consultório em Brasília, R$ 1.740,78 (salario.com.br, CBO 4221-10), "
                  "× 1,7 de encargos e benefícios (estudo de 20/10)"),
    "n_rec_rot": "Postos de recepção por polo",
    "n_rec": (2, "recepção e preparo; 2 para cobrir as 10 h"),
    "sala": (3000, ""),
    "apar": (2500, ""),
    "mat": (7, "R$ 7 ouvidos em reunião de 11/11 (relato do usuário); sem cotação"),
    "limp_s": (400, "estudo de 07/11, com energia, internet e água se o aluguel não incluir"),
    "limp_rede": None,
    "sist": (1500, "valor do ofício (usuário, 11/11); não sabemos se cobre o sistema de imagem"),
    "logi": (2600, "valor do ofício (usuário, 11/11)"),
    "gest": None,
    "fisc": (5.994, "hipótese do ofício, não é alíquota validada (usuário, 11/11), até alguém explicar que tributo é"),
    "tc_s": (180, "usuário, 11/11"),
    "tc_ad": (50, "usuário, 11/11"),
    "contraste": 1,
    "contraste_obs": "",
    "min_seb": None,
    "notas_valores": ["A gestão fica fora do exame: é a rubrica de apoio, R$ 956.160 no total (valor fixo, em 1 ou 20 meses).",
                      "Sem preço: responsável técnico do polo, médico de retaguarda e sistema de imagem (PACS)."],
    "rede": "na nossa rede",
    "conta": "a nossa conta",
    "medicos_sala": (2, "1.800 h por ano cada, ou dois turnos de 5 h"),
    "aux_obs": "fica com o médico o exame todo e digita o laudo; 2 para cobrir as 10 h",
    "rec_obs": "recepção e preparo; 2 para cobrir as 10 h",
    "pessoas_fonte": "Estudo de tempos de 09/11, seção 7 (sala aberta 10 h por dia útil; não conta férias nem faltas).",
    "pessoas_cab": "na nossa conta",
    "fora": [
        ("Enfermagem do ultrassom", "1 para cada 2 salas (7 em 14 salas)", "estimativa nossa, sem preço na conta"),
        ("Responsável técnico do polo", "1 por polo, sem preço", ""),
        ("Médico de retaguarda", "1 por dia útil por polo, sem preço", "previsto no plano assinado (4.15)"),
        ("Gestão e apoio", "22 postos e assessoria no plano assinado (8 meses); 16 postos e assessoria no quadro P2 (12 meses)",
         "rubrica de apoio, R$ 956.160 no total (valor fixo); a P2 de 07/11 dava R$ 978.120"),
        ("Tomografia: equipe do exame", "da clínica, dentro dos {tc}",
         "referência do que a clínica precisa por tomógrafo em 10 h: 3 técnicos em radiologia, 2 de enfermagem "
         "(3 com a punção antes), 1 radiologista no contraste e 2 de recepção: 8 ou 9 pessoas; 11 com dois turnos de 5 h"),
        ("Tomografia: agenda, lançamento e gestão", "na rubrica de apoio", ""),
    ],
    "pessoas_nota": None,
    "limite_medico": "- Médico do ultrassom: pago pelo tempo do exame (valor da hora × minutos de sala, aba Médico) ou por "
                     "exame (R$ 35 e R$ 40); a escolha está na aba Custos. Sem garantia mínima por plantão.",
}

SEB_FONTE = "rascunho de ofício do ISHP de 09/11/2026 (planilha_custos_sebastião.xlsx)"
SEBASTIAO = dict(NOSSO, **{
    "saida": "final_sebastiao.xlsx",
    "titulo": "Custos e margens do plano 4: a conta do Sebastião",
    "fonte": f"Valores do {SEB_FONTE}. Exames: os mesmos da final (carteira v3), para comparar; o ofício usava "
             "54.589 ultrassons e 13.622 tomografias.",
    "meses": (12, "ofício: 10/12/2026 a 09/12/2027"),
    "dias": (21, "ofício, Anexo II: 252 dias, sem descontar feriados"),
    "salas": (11, "ofício: 11 salas em 6 unidades (5 em Ceilândia, nenhuma na Região Leste)"),
    "unid_rot": "Unidades de ultrassom",
    "unid": (6, "ofício: 1 posto de recepção por unidade"),
    "h_dia": (9, "plantão de 10 h com 1 h de almoço (usuário, 11/11)"),
    "med_sem": (35, "ofício, Anexo III"),
    "med_com": (40, "ofício, Anexo III"),
    "med_hora": None,
    "med_h_rot": "a garantia ÷ as horas do plantão",
    "garantia": (1500, "ofício: em cada plantão o médico recebe o maior entre a produção e a garantia"),
    "pl_dia": (1, "hipótese: toda sala abre todo dia útil com um médico"),
    "aux": (3180, "ofício: custo do posto com provisões, não é o salário"),
    "n_aux": (1, "ofício: 1 posto por sala"),
    "rec": (3500, "ofício: custo do posto com provisões, não é o salário"),
    "n_rec_rot": "Postos de recepção por unidade",
    "n_rec": (1, "ofício: 1 posto por unidade"),
    "sala": (1500, "ofício: alvo de negociação, não é cotação aceita"),
    "apar": (2500, "ofício: 1 aparelho por sala"),
    "mat": ("=177414/54589", "ofício: R$ 177.414 para 54.589 exames (R$ 3,25 por exame)"),
    "limp_s": None,
    "limp_rede": (2400, "ofício: a rede toda"),
    "sist": (1500, "ofício: a rede toda"),
    "logi": (2600, "ofício: a rede toda; não detalha"),
    "gest": (3500, "ofício: verba única para a rede, dentro do exame; não detalha"),
    "fisc": (5.994, "ofício: hipótese do modelo, não é alíquota validada"),
    "tc_s": (175, "ofício, Anexo IV; cobre tudo o que é do exame"),
    "tc_ad": (43, "ofício, Anexo IV; um por evento de contraste"),
    "contraste": 0.96,
    "contraste_obs": "96% da fila com contraste = 93% de toda a tomografia, a projeção do ofício. ",
    "min_seb": (70, "atendimentos de ultrassom em um plantão, no estudo do Sebastião (relato do usuário, 11/11)"),
    "notas_valores": ["A gestão de R$ 3.500 por mês está dentro do exame. O plano também tem a rubrica de apoio (R$ 956.160): "
                      "juntas, podem ser lidas como pagamento em dobro.",
                      "Sem preço no ofício: responsável técnico do polo, médico de retaguarda e sistema de imagem (PACS)."],
    "rede": "na rede do ofício",
    "conta": "a conta do Sebastião",
    "medicos_sala": (1, "ofício: 1 plantão de 10 h por sala"),
    "aux_obs": "ofício: 1 posto por sala; sem cobertura de almoço nem de falta nas 10 h",
    "rec_obs": "ofício: 1 posto por unidade",
    "pessoas_fonte": f"{SEB_FONTE[0].upper()}{SEB_FONTE[1:]}: o ofício dá postos, e não pessoas; médico = um plantão por sala "
                     "por dia útil.",
    "pessoas_cab": "no ofício",
    "fora": [
        ("Enfermagem do ultrassom", "não tem", ""),
        ("Responsável técnico do polo", "não tem", "falta também na nossa conta"),
        ("Médico de retaguarda", "não tem", "previsto no plano assinado (4.15)"),
        ("Gestão e apoio", "verba de R$ 3.500 por mês, sem pessoas, dentro do exame",
         "o plano tem também a rubrica de apoio, R$ 956.160 no total (valor fixo)"),
        ("Tomografia: equipe do exame", "da clínica, dentro dos {tc}", ""),
        ("Tomografia: agenda, lançamento e gestão", "o ofício não traz", ""),
    ],
    "pessoas_nota": "O ofício não diz quantos médicos cumprem os plantões: o mínimo é um médico por sala todo dia útil.",
    "limite_medico": "- Médico: o melhor cenário paga só a produção; o pior abre todas as salas todo dia útil e cobra a garantia "
                     "quando a produção do plantão fica abaixo dela (troque no alto da aba).",
})

for _k in ("med_modo", "med_tempo_h", "med_dop_ad"):      # o pagamento pelo tempo é só da nossa conta
    SEBASTIAO[_k] = None

P = SEBASTIAO if len(sys.argv) > 1 and sys.argv[1] == "sebastiao" else NOSSO
SEB = P is SEBASTIAO
SAIDA = Path(__file__).with_name(P["saida"])
pv = lambda k: P[k][0]
# A planilha do Sebastião pode ir ao parceiro (usuário, 12/11): sem o aviso de controle interno
AVISO = "" if SEB else " Controle interno."
AVISO_LONGO = "" if SEB else " Controle interno: não vai à SES nem ao parceiro."
po = lambda k: P[k][1]
TC_SEM, TC_ADIC = pv("tc_s"), pv("tc_ad")


def brl(v):
    return f"R$ {v:,.0f}".replace(",", ".")


def celula(ws, ref, valor, fonte=PRETO, fmt=None, fill=None, wrap=False, alinh=None):
    c = ws[ref]
    c.value = valor
    c.font = fonte
    if fmt:
        c.number_format = fmt
    if fill:
        c.fill = fill
    c.border = BORDA
    c.alignment = Alignment(wrap_text=wrap, vertical="top", horizontal=alinh)
    return c


def secao(ws, linha, texto, cols="ABC"):
    for col in cols:
        ws[f"{col}{linha}"].fill = F_SECAO
    ws[f"A{linha}"].value = texto
    ws[f"A{linha}"].font = SECAO


def cabecalho(ws, linha, textos):
    for i, t in enumerate(textos):
        celula(ws, f"{get_column_letter(i + 1)}{linha}", t, NEGRITO, fill=F_CAB, wrap=True, alinh="center")
    ws.row_dimensions[linha].height = 32


def nota(ws, linha, texto):
    ws[f"A{linha}"].value = texto
    ws[f"A{linha}"].font = NOTA


SEM_D, COM_D, COM_C, SEM_C = "sem Doppler", "com Doppler", "com contraste", "sem contraste"
# (exame, modalidade, código, tipo, quantidade de partida, preço Candanga, minutos de sala ou de tomógrafo, observação)
# Quantidades: carteira_final_v3_20261111.xlsx, aba Escolhidos. Minutos: estudo_readequacao_candanga_margem_20261109.xlsx.
EXAMES = [
    ("US de abdômen total (adulto)", "Ultrassom", "02.05.02.004-6", SEM_D, 13595, 117.51, 20, "9.895 da fila e 3.700 novos"),
    ("US de parede abdominal", "Ultrassom", "02.05.02.004-6", SEM_D, 3304, 117.51, 20, "a SES precisa confirmar o código (L-007)"),
    ("US de abdômen total (criança)", "Ultrassom", "02.05.02.004-6", SEM_D, 452, 117.51, 20, ""),
    ("US de abdômen superior", "Ultrassom", "02.05.02.003-8", SEM_D, 2505, 101.27, 15, "2.213 da fila e 292 novos"),
    ("US de aparelho urinário e rins (adulto)", "Ultrassom", "02.05.02.005-4", SEM_D, 4962, 90.53, 15, "3.749 da fila e 1.213 novos"),
    ("US de aparelho urinário (criança)", "Ultrassom", "02.05.02.005-4", SEM_D, 276, 90.53, 15, ""),
    ("US de bolsa escrotal (adulto)", "Ultrassom", "02.05.02.007-0", SEM_D, 1034, 100.00, 15, "700 da fila e 334 novos"),
    ("US de bolsa escrotal (criança)", "Ultrassom", "02.05.02.007-0", SEM_D, 234, 100.00, 15, ""),
    ("US de próstata (via abdominal)", "Ultrassom", "02.05.02.010-0", SEM_D, 3466, 74.19, 15, "2.969 da fila e 497 novos"),
    ("US de tireoide (adulto, com o Doppler de tireoide)", "Ultrassom", "02.05.02.012-7", SEM_D, 5308, 64.07, 15,
     "3.794 da fila e 1.514 novos; pago pelo código da tireoide"),
    ("US de tireoide (criança)", "Ultrassom", "02.05.02.012-7", SEM_D, 60, 64.07, 15, ""),
    ("US de mamas (as duas)", "Ultrassom", "02.05.02.009-7", SEM_D, 12950, 70.97, 20, ""),
    ("US transvaginal", "Ultrassom", "02.05.02.018-6", SEM_D, 5294, 83.77, 15, "sem os 4.000 reservados ao IEV (L-008)"),
    ("US de articulação, fora da ortopedia", "Ultrassom", "02.05.02.006-2", SEM_D, 4557, 70.97, 15,
     "minutos estimados (carteira v2); a ortopedia fica com o IEV (D-012)"),
    ("Doppler de carótidas e outros vasos", "Ultrassom", "02.05.01.004-0", COM_D, 5952, 115.61, 20, "4.727 da fila e 1.225 novos"),
    ("Doppler de membros (os dois lados)", "Ultrassom", "02.05.01.004-0", COM_D, 12034, 115.61, 40,
     "condição D-011: um exame por pedido na conta; 40 min de sala"),
    ("TC de abdômen superior com contraste", "Tomografia", "02.06.03.001-0", COM_C, 4116, 309.25, 20, ""),
    ("TC de abdômen superior sem contraste", "Tomografia", "02.06.03.001-0", SEM_C, 68, 309.25, 11, ""),
    ("TC de pelve com contraste", "Tomografia", "02.06.03.003-7", COM_C, 3634, 309.25, 20, ""),
    ("TC de pelve sem contraste", "Tomografia", "02.06.03.003-7", SEM_C, 56, 309.25, 11, ""),
    ("TC de tórax com contraste", "Tomografia", "02.06.02.003-1", COM_C, 2350, 309.25, 20, ""),
    ("TC de tórax sem contraste", "Tomografia", "02.06.02.003-1", SEM_C, 180, 309.25, 11, ""),
    ("TC de pescoço com contraste", "Tomografia", "02.06.01.005-2", COM_C, 479, 309.25, 20, ""),
    ("TC de crânio sem contraste", "Tomografia", "02.06.01.007-9", SEM_C, 44, 251.29, 11, ""),
]
# Linhas do Simulador (as abas Custos e Volume apontam para elas)
N_US = sum(1 for e in EXAMES if e[1] == "Ultrassom")
S_CAB = 5
U1, U2 = S_CAB + 1, S_CAB + N_US
S_US = U2 + 1
T1 = S_US + 1
T2 = T1 + len(EXAMES) - N_US - 1
S_TC = T2 + 1
S_TOT = S_TC + 1
SIM = lambda col, r: f"Simulador!${col}${r}"
# Linhas da aba Médico (só na nossa conta): uma por ultrassom, na mesma ordem do Simulador
M_CAB = 6
M1, M2 = M_CAB + 1, M_CAB + N_US
MT = M2 + 1
MED = lambda col, r: f"'Médico'!${col}${r}"
CENARIO = "Simulador!$E$3"        # só no perfil do Sebastião: "melhor" ou "pior"
PIOR = f'{CENARIO}="pior"'

wb = Workbook()
sim = wb.active
sim.title = "Simulador"
ws = wb.create_sheet("Custos")
pe = wb.create_sheet("Pessoas")

ws["A1"].value = P["titulo"]
ws["A1"].font = TITULO
nota(ws, 2, P["fonte"])
nota(ws, 3, "Azul = premissa que pode ser trocada; preto = fórmula; verde = vem da aba Simulador." + AVISO_LONGO)

R = {}          # chave -> linha
linha_atual = [5]


def lin(chave, rotulo, v, fmt, obs="", total=False):
    """Uma linha: rótulo, valor e observação."""
    r = linha_atual[0]
    R[chave] = r
    fill = F_TOTAL if total else None
    formula = isinstance(v, str) and v.startswith("=")
    texto = isinstance(v, str) and not formula
    celula(ws, f"A{r}", rotulo, NEGRITO if total else PRETO, fill=fill, wrap=True)
    do_sim = formula and "Simulador!" in v
    celula(ws, f"B{r}", v, NEGRITO if total else (VERDE if do_sim else (PRETO if formula or texto else AZUL)),
           None if texto else fmt, fill, wrap=texto, alinh="right" if texto else None)
    celula(ws, f"C{r}", obs, NOTA, fill=fill, wrap=True)
    linha_atual[0] += 1
    return r


def premissa(chave, rotulo, fmt):
    """Linha de premissa do perfil; não existe se o perfil não tem o valor."""
    if P.get(chave) is None:
        return None
    r = lin(chave, rotulo, pv(chave), fmt, po(chave))
    if isinstance(pv(chave), str):          # fórmula usada como premissa (ex.: materiais do ofício)
        ws[f"B{r}"].font = AZUL
    return r


def abre(titulo, cab=("item", "valor", "observação")):
    r = linha_atual[0] + 1
    secao(ws, r, titulo)
    cabecalho(ws, r + 1, cab)
    linha_atual[0] = r + 2


B = lambda k: f"B{R[k]}"
A_ = lambda k: f"$B${R[k]}"     # referência absoluta

# ------------------------------------------------------------ 1. quantidades
abre("1. Quantidades: o que a conta atende, e com quê")
celula(ws, f"A{linha_atual[0]}", "Para trocar a quantidade de exames: aba Simulador, coluna Quantidade (azul). "
       "As linhas em verde vêm de lá, e o resto da planilha recalcula sozinho.", NEGRITO, fill=F_BOM, wrap=True)
ws.merge_cells(f"A{linha_atual[0]}:C{linha_atual[0]}")
ws.row_dimensions[linha_atual[0]].height = 28
linha_atual[0] += 1
premissa("meses", "Meses de execução", INT)
premissa("dias", "Dias úteis por mês", INT)
D_US, E_US = f"Simulador!$D${U1}:$D${U2}", f"Simulador!$E${U1}:$E${U2}"
lin("us_sem", "Ultrassons sem Doppler", f'=SUMIF({D_US},"{SEM_D}",{E_US})', INT,
    "da aba Simulador (partida: carteira v3 de 11/11, 57.997)")
lin("us_com", "Ultrassons com Doppler", f'=SUMIF({D_US},"{COM_D}",{E_US})', INT,
    "da aba Simulador (partida: 12.034 de membros, os dois lados, condição D-011, e 5.952 de carótidas e outros vasos)")
lin("us", "Ultrassons no total", f"={B('us_sem')}+{B('us_com')}", INT, "a carteira 1 de 02/11 tinha 65.132", total=True)
lin("tc_com", "Tomografias feitas com contraste", f"={SIM('Q', S_TC)}", INT,
    "da aba Simulador: a fila com contraste vezes a parte feita de fato com contraste (partida: 100%, 10.579)")
lin("tc_sem", "Tomografias feitas sem contraste", f"={SIM('E', S_TC)}-{B('tc_com')}", INT, "da aba Simulador (partida: 348)")
lin("tc", "Tomografias no total", f"={B('tc_com')}+{B('tc_sem')}", INT,
    "a carteira 1 tinha 14.401; a v3 trocou tomografia por ultrassom", total=True)
lin("ex", "Exames no total", f"={B('us')}+{B('tc')}", INT, total=True)
lin("salas_in", "Salas de ultrassom, quando o número é fixo", pv("salas"), INT, po("salas"))
lin("salas_auto", "As salas acompanham os exames? (sim ou não)", "não", None,
    "não: usa o número fixo acima. sim: põe as salas que as horas de exame pedem, com o uso máximo abaixo "
    "(teste: mais exames por hora na aba Simulador, menos salas e menos custo fixo)")
ws[f"B{R['salas_auto']}"].font = AZUL
ws[f"B{R['salas_auto']}"].alignment = Alignment(horizontal="center", vertical="top")
dv_auto = DataValidation(type="list", formula1='"sim,não"', allow_blank=False)
ws.add_data_validation(dv_auto)
dv_auto.add(f"B{R['salas_auto']}")
lin("uso_max", "Uso máximo da sala, quando as salas acompanham os exames", 1, PCT,
    "100% = agenda cheia, sem folga; 90% deixa espaço para falta e aparelho parado")
premissa("unid", P["unid_rot"], INT)
lin("unid_tc", "Unidades de tomografia", "3 a 5, em estudo", None,
    "a Carneiro de Mendonça não tem tomógrafo (informação do usuário, 10/11)")
premissa("h_dia", "Horas de exame por sala por dia", DEC)
lin("min", "Minutos de sala por ultrassom, em média", f"=IF({B('us')}=0,0,{SIM('P', S_US)}*60/{B('us')})", DEC,
    "da aba Simulador: o tempo do estudo do Sebastião, o mesmo para todo ultrassom (troque na seção 2 ou exame a exame)" if SEB
    else "da aba Simulador: agenda do CBR, de 15 a 40 min conforme o exame (27.031 h na carteira v3)")
lin("h_nec", "Horas de sala que os exames pedem", f"={B('us')}*{B('min')}/60", INT)
lin("salas", "Salas de ultrassom na conta", f'=IF({B("salas_auto")}="sim",MAX(1,ROUNDUP({B("h_nec")}/'
    f'({B("dias")}*{B("meses")}*{B("h_dia")}*IF({B("uso_max")}=0,1,{B("uso_max")})),0)),{B("salas_in")})', INT,
    "as que entram no custo (auxiliares, aluguel, aparelhos, limpeza) e nas horas disponíveis", total=True)
lin("h_disp", "Horas de sala disponíveis no período", f"={B('salas')}*{B('dias')}*{B('meses')}*{B('h_dia')}", INT)
lin("uso", "Uso das salas", f"={B('h_nec')}/{B('h_disp')}", PCT, "acima de 100%, os exames não cabem nas salas")
lin("ex_sala", "Ultrassons por sala por dia útil", f"={B('us')}/({B('salas')}*{B('dias')}*{B('meses')})", DEC,
    "quantos exames cada sala faz por dia, em média: os ultrassons divididos por salas × dias úteis × meses. "
    f"Com {pv('h_dia')} h de exame por dia, dá um exame a cada 'Minutos de sala por ultrassom' (acima)")

# ------------------------------------------------------------ 2. valores unitários
abre("2. Valores unitários")
premissa("med_sem", "Médico por ultrassom sem Doppler", REAL)
premissa("med_com", "Médico por ultrassom com Doppler", REAL)
if not SEB:
    premissa("med_modo", "Como o médico do ultrassom é pago (pelo tempo ou por exame)", None)
    ws[f"B{R['med_modo']}"].alignment = Alignment(horizontal="center", vertical="top")
    dv_modo = DataValidation(type="list", formula1='"pelo tempo,por exame"', allow_blank=False)
    ws.add_data_validation(dv_modo)
    dv_modo.add(f"B{R['med_modo']}")
    premissa("med_tempo_h", "Médico pelo tempo: valor da hora de sala", REAL)
    premissa("med_dop_ad", "Médico pelo tempo: adicional por exame com Doppler", REAL)
premissa("med_hora", "Médico por hora de exame (alternativa, fora da conta)", REAL)
premissa("garantia", "Garantia mínima do médico por plantão", REAL)
premissa("pl_dia", "Plantões por sala por dia útil", INT)
if SEB:
    premissa("min_seb", "Ultrassons por plantão, no estudo do Sebastião", INT)
    lin("min_us_seb", "Minutos de sala por ultrassom, no estudo do Sebastião", f"={B('h_dia')}*60/{B('min_seb')}", DEC,
        "as horas de exame do plantão divididas pelos atendimentos; vale para todo ultrassom na aba Simulador")
premissa("aux", "Auxiliar de sala, custo do posto por mês", REAL)
premissa("n_aux", "Auxiliares por sala", INT)
premissa("rec", "Recepção, custo do posto por mês", REAL)
premissa("n_rec", P["n_rec_rot"], INT)
premissa("sala", "Aluguel da sala por mês", REAL)
premissa("apar", "Aluguel do aparelho de ultrassom por mês", REAL)
premissa("mat", "Materiais por exame", REAL)
premissa("limp_s", "Limpeza e resíduos por sala por mês", REAL)
premissa("limp_rede", "Limpeza e resíduos, a rede toda, por mês", REAL)
premissa("sist", "Sistemas e comunicação, a rede toda, por mês", REAL)
premissa("logi", "Logística e contingência, a rede toda, por mês", REAL)
premissa("gest", "Gestão e coordenação, a rede toda, por mês", REAL)
premissa("fisc", "Reserva fiscal por exame", REAL)
premissa("tc_s", "Tomografia na clínica, sem contraste", REAL)
premissa("tc_ad", "Adicional do contraste", REAL)
lin("tc_c", "Tomografia na clínica, com contraste", f"={B('tc_s')}+{B('tc_ad')}", REAL,
    "a Candanga paga R$ 309,25 na maior parte")
lin("tc_min_sem", "Minutos de tomógrafo do exame pedido com contraste e feito sem", 11, INT,
    "o mesmo tempo da tomografia sem contraste (estudo de 09/11); só mede o tomógrafo, não entra no custo")
for t in P["notas_valores"]:
    nota(ws, linha_atual[0], t)
    linha_atual[0] += 1

# ------------------------------------------------------------ 3. o custo dos exames
abre(f"3. O custo dos exames {P['rede']}")
p = A_
limp = (f"{p('limp_s')}*{p('salas')}" if P["limp_s"] else "") + ("+" if P["limp_s"] and P["limp_rede"] else "") + \
       (f"{p('limp_rede')}" if P["limp_rede"] else "")
C_MED_EX = f"{p('us_sem')}*{p('med_sem')}+{p('us_com')}*{p('med_com')}"       # médico por exame (R$ 35 e R$ 40)
if SEB:
    lin("c_med", "Médico, pela produção", f"={C_MED_EX}", REAL)
else:
    TEMPO = f'{p("med_modo")}="pelo tempo"'
    lin("c_med", "Médico, pela produção", f"=IF({TEMPO},{MED('K', MT)},{C_MED_EX})", REAL,
        "pelo tempo ou por exame, conforme a seção 2; a aba Médico mostra os dois")
if SEB:
    lin("c_gar", "Médico: o que a garantia acrescenta (só no pior cenário)",
        f"=IF({PIOR},MAX(0,{p('salas')}*{p('dias')}*{p('meses')}*{p('pl_dia')}*{p('garantia')}-{B('c_med')}),0)", REAL,
        "pior cenário: todas as salas abertas todo dia útil, e o plantão pago pela garantia quando a produção média fica "
        "abaixo dela. Troque o cenário no alto da aba Simulador")
lin("c_aux", "Auxiliares de sala", f"={p('salas')}*{p('n_aux')}*{p('aux')}*{p('meses')}", REAL)
lin("c_rec", "Recepção", f"={p('unid')}*{p('n_rec')}*{p('rec')}*{p('meses')}", REAL)
lin("c_sala", "Aluguel das salas", f"={p('salas')}*{p('sala')}*{p('meses')}", REAL)
lin("c_apar", "Aluguel dos aparelhos", f"={p('salas')}*{p('apar')}*{p('meses')}", REAL)
lin("c_mat", "Materiais", f"={p('us')}*{p('mat')}", REAL)
lin("c_limp", "Limpeza e resíduos", f"=({limp})*{p('meses')}" if SEB else f"={limp}*{p('meses')}", REAL)
if SEB:
    lin("c_rede", "Sistemas, logística e gestão da rede", f"=({p('sist')}+{p('logi')}+{p('gest')})*{p('meses')}", REAL)
else:
    lin("c_rede", "Sistemas e logística da rede", f"=({p('sist')}+{p('logi')})*{p('meses')}", REAL)
lin("c_fisc", "Reserva fiscal", f"={p('us')}*{p('fisc')}", REAL)
lin("nmed", "Ultrassom: tudo menos o médico", f"=SUM(B{R['c_aux']}:B{R['c_fisc']})", REAL, total=True)
lin("nmed_ex", "  por exame", f"=IF({p('us')}=0,0,{B('nmed')}/{p('us')})", REAL)
GAR = f"+{B('c_gar')}" if SEB else ""
lin("us_t", "ULTRASSOM", f"={B('c_med')}{GAR}+{B('nmed')}", REAL, total=True)
lin("us_t_ex", "  por exame", f"=IF({p('us')}=0,0,{B('us_t')}/{p('us')})", REAL)
lin("tc_t", "TOMOGRAFIA, paga à clínica", f"={p('tc_com')}*{p('tc_c')}+{p('tc_sem')}*{p('tc_s')}", REAL, total=True)
lin("tc_t_ex", "  por exame", f"=IF({p('tc')}=0,0,{B('tc_t')}/{p('tc')})", REAL)
lin("tot", "CONJUNTO DOS EXAMES: o custo de fazer", f"={B('us_t')}+{B('tc_t')}", REAL, total=True)
lin("valor", "O que os exames trazem pela Tabela SUS Candanga", f"={SIM('H', S_TOT)}", REAL,
    "quantidade × preço de cada exame, na aba Simulador")
lin("marg", "Margem: o que os exames trazem menos o custo de fazer", f"={B('valor')}-{B('tot')}", REAL,
    "a conta é a do lucro bruto (receita menos custo direto), mas não é lucro: é a folga que paga o que a conta não tem "
    "(responsável técnico, retaguarda, PACS, enfermagem, faltas, férias, aparelho parado) e o imprevisto. O apoio fica fora",
    total=True)
lin("marg_p", "  em proporção do que os exames trazem", f"=IF({B('valor')}=0,0,{B('marg')}/{B('valor')})", PCT)
lin("teto", "Valor dos exames a fechar", 10636602, REAL,
    "recurso de R$ 11.592.762 menos o apoio (plano.md: envelope de produção assistencial)")
lin("apoio", "Apoio e gestão (custo acessório), fora da conta dos exames", 956160, REAL,
    "valor fixo no total, em qualquer prazo: não multiplicar por meses")
lin("dif", "Diferença: valor a fechar menos o que os exames trazem", f"={B('teto')}-{B('valor')}", REAL,
    "negativa = as quantidades passam do valor; ver a aba Simulador, seção 1")

if not SEB:
    D_M, E_M, K_M = (f"'Médico'!${c}${M1}:${c}${M2}" for c in "BCK")
    lin("med_sem_ef", "  médico por ultrassom sem Doppler, em média",
        f'=IF(AND({TEMPO},{p("us_sem")}>0),SUMIF({D_M},"{SEM_D}",{K_M})/{p("us_sem")},{p("med_sem")})', REAL,
        "pelo tempo, a média do que o médico recebe nos exames sem Doppler (de 15 a 20 min)")
    lin("med_com_ef", "  médico por ultrassom com Doppler, em média",
        f'=IF(AND({TEMPO},{p("us_com")}>0),SUMIF({D_M},"{COM_D}",{K_M})/{p("us_com")},{p("med_com")})', REAL,
        "pelo tempo, a média do que o médico recebe nos Dopplers (carótidas 20 min, membros 40 min)")
MS, MC = ("med_sem", "med_com") if SEB else ("med_sem_ef", "med_com_ef")

# ------------------------------------------------------------ 4. valor final por exame
abre("4. Valor final por exame: quanto custa fazer cada tipo", ("exame", "custo por exame", "observação"))
GAR_EX = f"+IF({p('us')}=0,0,{B('c_gar')}/{p('us')})" if SEB else ""
lin("f_us", "Ultrassom sem Doppler", f"={B(MS)}{GAR_EX}+{B('nmed_ex')}", REAL,
    f"honorário do médico{'' if SEB else ' (em média, se pago pelo tempo)'} mais o rateio igual de tudo o que não é médico. "
    "A Candanga paga de R$ 64,07 a R$ 117,51"
    + ("; no pior cenário, mais o rateio igual da garantia" if SEB else ""), total=True)
lin("f_dop", "Ultrassom com Doppler", f"={B(MC)}{GAR_EX}+{B('nmed_ex')}", REAL, "a Candanga paga R$ 115,61", total=True)
lin("f_tcs", "Tomografia sem contraste", f"={B('tc_s')}", REAL,
    "preço pago à clínica. A Candanga paga R$ 309,25 (crânio R$ 251,29)", total=True)
lin("f_tcc", "Tomografia com contraste", f"={B('tc_c')}", REAL,
    "preço pago à clínica, com o adicional do contraste. A Candanga paga R$ 309,25", total=True)
nota(ws, linha_atual[0], "O custo do ultrassom cai com mais exames na mesma rede, porque o fixo (salas, auxiliares, recepção) "
                         "é dividido por mais exames: ver a aba Volume.")

ws.column_dimensions["A"].width = 58
ws.column_dimensions["B"].width = 21
ws.column_dimensions["C"].width = 100
ws.freeze_panes = "B5"

C = lambda k: f"Custos!$B${R[k]}"

# ============================================================ PESSOAS
pe["A1"].value = "Quantas pessoas a conta põe"
pe["A1"].font = TITULO
nota(pe, 2, P["pessoas_fonte"])
nota(pe, 3, "Azul = premissa que pode ser trocada; preto = fórmula. Salas e polos vêm da aba Custos.")
secao(pe, 5, "1. Ultrassom: quem está na conta do exame", "ABCD")
cabecalho(pe, 6, ["função", "por sala ou polo", "pessoas na rede", "observação"])
funcoes = [
    ("Médico ultrassonografista, por sala", pv("medicos_sala"), "s", po("medicos_sala")),
    ("Auxiliar de sala, por sala", f"={C('n_aux')}", "s", P["aux_obs"]),
    ("Recepção, por polo" if not SEB else "Recepção, por unidade", f"={C('n_rec')}", "u", P["rec_obs"]),
]
for i, (nome, v, por, obs) in enumerate(funcoes):
    r = 7 + i
    celula(pe, f"A{r}", nome)
    celula(pe, f"B{r}", v, PRETO if isinstance(v, str) else AZUL, INT)
    celula(pe, f"C{r}", f"=B{r}*{C('salas') if por == 's' else C('unid')}", fmt=INT)
    celula(pe, f"D{r}", obs, NOTA, wrap=True)
celula(pe, "A10", "Pessoas no ultrassom", NEGRITO, fill=F_TOTAL)
celula(pe, "B10", "", fill=F_TOTAL)
celula(pe, "C10", "=SUM(C7:C9)", NEGRITO, INT, F_TOTAL)
celula(pe, "D10", "", NOTA, fill=F_TOTAL)
celula(pe, "A11", "  das quais, auxiliares e recepção (pagos por mês)")
celula(pe, "B11", "")
celula(pe, "C11", "=C8+C9", fmt=INT)
celula(pe, "D11", "", NOTA)

secao(pe, 13, "2. O que fica fora da conta do exame, ou não tem preço", "ABCD")
cabecalho(pe, 14, ["função", P["pessoas_cab"], "", "observação"])
for i, (nome, v, obs) in enumerate(P["fora"]):
    r = 15 + i
    celula(pe, f"A{r}", nome, wrap=True)
    pe.merge_cells(f"B{r}:C{r}")
    celula(pe, f"B{r}", v.format(tc=f"{brl(TC_SEM)} + {brl(TC_ADIC)}"), wrap=True)
    celula(pe, f"D{r}", obs, NOTA, wrap=True)
    pe.row_dimensions[r].height = 42
if P["pessoas_nota"]:
    nota(pe, 15 + len(P["fora"]) + 1, P["pessoas_nota"])

pe.column_dimensions["A"].width = 46
for col in "BC":
    pe.column_dimensions[col].width = 22
pe.column_dimensions["D"].width = 90
pe.freeze_panes = "B7"

# ============================================================ VOLUME
vo = wb.create_sheet("Volume")
vo["A1"].value = "Como o volume de ultrassons muda o custo por exame"
vo["A1"].font = TITULO
nota(vo, 2, "O custo fixo (salas, aparelhos, auxiliares, recepção, limpeza e verbas da rede) é dividido pelos exames: "
            "mais exames, menos fixo em cada um. Preços e pessoas por sala vêm da aba Custos.")
nota(vo, 3, "Azul = pode trocar (volumes, salas, parte com Doppler, uso máximo). Laranja = não cabe nas salas." + AVISO)
COLS_V = "ABCDEFG"
secao(vo, 5, "Premissas", COLS_V)
prem = [
    (6, "Salas de ultrassom", f"={C('salas')}", INT, "aba Custos; troque aqui para testar"),
    (7, "Parte dos ultrassons com Doppler", f"={C('us_com')}/{C('us')}", PCT, "a da carteira v3"),
    (8, "Uso máximo da sala para dizer quantas salas o volume pede", 1, PCT,
     "100% = sem folga; 90% deixa espaço para falta e aparelho parado"),
]
for r, rot, v, fmt, obs in prem:
    celula(vo, f"A{r}", rot)
    celula(vo, f"B{r}", v, AZUL, fmt)
    celula(vo, f"C{r}", obs, NOTA)
SALAS, DOP, USO = "$B$6", "$B$7", "$B$8"
VOLUMES = [30000, 40000, 54589, 65000, 75983, 90000, 100000, 113518]
HORAS_SALA = f"({C('dias')}*{C('meses')}*{C('h_dia')})"
VAR = f"({C('mat')}+{C('fisc')})"


def fixo(salas):
    """Custo fixo do período com esse número de salas."""
    por_sala = f"{C('n_aux')}*{C('aux')}+{C('sala')}+{C('apar')}" + (f"+{C('limp_s')}" if P["limp_s"] else "")
    rede = f"+{C('sist')}+{C('logi')}" + (f"+{C('limp_rede')}+{C('gest')}" if SEB else "")
    return f"(({salas})*({por_sala})+{C('unid')}*{C('n_rec')}*{C('rec')}{rede})*{C('meses')}"


def gar_v(salas, V):
    """No perfil do Sebastião: o que a garantia acrescenta por exame, no pior cenário."""
    if not SEB:
        return ""
    prod = f"{V}*((1-{DOP})*{C('med_sem')}+{DOP}*{C('med_com')})"
    return (f"+IF({PIOR},MAX(0,({salas})*{C('dias')}*{C('meses')}*{C('pl_dia')}*{C('garantia')}-{prod})/{V},0)")


# ---- 1. rede fixa
secao(vo, 10, "1. Com as salas fixas, e o volume mudando", COLS_V)
cabecalho(vo, 11, ["ultrassons no período", "fixo por exame", "ultrassom sem Doppler", "ultrassom com Doppler",
                   "média, com a parte de Doppler", "uso das salas"])
vo.row_dimensions[11].height = 44
for i, v in enumerate(VOLUMES):
    r = 12 + i
    V = f"$A{r}"
    celula(vo, f"A{r}", v, AZUL, INT)
    celula(vo, f"B{r}", f"={fixo(SALAS)}/{V}", fmt=REAL)
    celula(vo, f"C{r}", f"={C(MS)}+{VAR}+B{r}{gar_v(SALAS, V)}", fmt=REAL)
    celula(vo, f"D{r}", f"={C(MC)}+{VAR}+B{r}{gar_v(SALAS, V)}", fmt=REAL)
    celula(vo, f"E{r}", f"=(1-{DOP})*C{r}+{DOP}*D{r}", fmt=REAL)
    celula(vo, f"F{r}", f"={V}*{C('min')}/60/({SALAS}*{HORAS_SALA})", fmt=PCT)
fim1 = 12 + len(VOLUMES) - 1
vo.conditional_formatting.add(f"F12:F{fim1}", CellIsRule(operator="greaterThan", formula=["1"], fill=F_ALERTA))
nota(vo, fim1 + 1, "Uso acima de 100% (laranja): o volume não cabe nessas salas, e o custo da linha não vale; ver a seção 2.")

# ---- 2. salas acompanham o volume
t2 = fim1 + 3
secao(vo, t2, "2. Com as salas acompanhando o volume: quantas salas cada volume pede, e o custo com elas", COLS_V)
cabecalho(vo, t2 + 1, ["ultrassons no período", "salas que o volume pede", "fixo por exame", "ultrassom sem Doppler",
                       "ultrassom com Doppler", "média, com a parte de Doppler"])
vo.row_dimensions[t2 + 1].height = 44
for i in range(len(VOLUMES)):
    r = t2 + 2 + i
    V = f"$A{r}"
    celula(vo, f"A{r}", f"=A{12 + i}", fmt=INT)
    celula(vo, f"B{r}", f"=ROUNDUP({V}*{C('min')}/60/({HORAS_SALA}*{USO}),0)", fmt=INT)
    celula(vo, f"C{r}", f"={fixo(f'$B{r}')}/{V}", fmt=REAL)
    celula(vo, f"D{r}", f"={C(MS)}+{VAR}+C{r}{gar_v(f'$B{r}', V)}", fmt=REAL)
    celula(vo, f"E{r}", f"={C(MC)}+{VAR}+C{r}{gar_v(f'$B{r}', V)}", fmt=REAL)
    celula(vo, f"F{r}", f"=(1-{DOP})*D{r}+{DOP}*E{r}", fmt=REAL)
fim2 = t2 + 2 + len(VOLUMES) - 1
nota(vo, fim2 + 1, f"As salas usam {pv('h_dia')} h de exame por dia. O volume segue o da seção 1.")
nota(vo, fim2 + 2, "Quando as salas acompanham o volume, o custo por exame quase não cai: só a recepção e as verbas da rede se diluem.")
nota(vo, fim2 + 3, f"Tomografia: é paga à clínica por exame ({brl(TC_SEM)}, ou {brl(TC_SEM + TC_ADIC)} com contraste), e o volume "
                   "não muda o preço, salvo se a clínica der desconto por volume ou pedir mínimo mensal.")
if SEB:
    nota(vo, fim2 + 4, "Médico: o cenário escolhido no alto da aba Simulador vale aqui também. No pior, a garantia é cobrada nas "
                       "salas abertas todo dia útil quando a produção fica abaixo dela.")

vo.column_dimensions["A"].width = 50
for col in "BCDEF":
    vo.column_dimensions[col].width = 18
vo.freeze_panes = "B5"

# ============================================================ MÉDICO (só na nossa conta)
if not SEB:
    md = wb.create_sheet("Médico")
    md["A1"].value = "Médico do ultrassom: pago pelo tempo do exame"
    md["A1"].font = TITULO
    nota(md, 2, "O médico fica na sala o exame todo (entrada, exame com o transdutor e laudo), então o tempo dele é o minuto de "
                "sala da aba Simulador. Pelo tempo: valor da hora × minutos ÷ 60. Exame mais demorado paga mais, e a hora do "
                "médico vale o mesmo em qualquer exame.")
    nota(md, 3, "Azul = premissa; verde = vem do Simulador ou da aba Custos; preto = fórmula. Para trocar o valor da hora ou "
                "voltar ao pagamento por exame: aba Custos, seção 2. Para trocar os minutos: aba Simulador, exames por hora."
         + AVISO)
    MCOLS = "ABCDEFGHIJKLM"
    secao(md, 5, "1. Quanto o médico recebe por exame: hoje (por exame) e pelo tempo", MCOLS)
    cabecalho(md, M_CAB, ["Exame", "Tipo", "Quantidade", "Minutos de sala", "Hoje: por exame",
                          "Hoje: vale por hora de sala", "Pelo tempo: por exame", "Pelo tempo: vale por hora de sala",
                          "Diferença por exame", "Hoje: total no período", "Pelo tempo: total no período",
                          "Diferença no período", "Horas de sala"])
    md.row_dimensions[M_CAB].height = 44
    HORA, AD = C("med_tempo_h"), C("med_dop_ad")
    for i in range(N_US):
        r, rs = M1 + i, U1 + i
        celula(md, f"A{r}", f"=Simulador!A{rs}", VERDE)
        celula(md, f"B{r}", f"=Simulador!D{rs}", VERDE, alinh="center")
        celula(md, f"C{r}", f"=Simulador!E{rs}", VERDE, INT)
        celula(md, f"D{r}", f"=Simulador!G{rs}", VERDE, DEC, alinh="center")
        celula(md, f"E{r}", f'=IF(B{r}="{COM_D}",{C("med_com")},{C("med_sem")})', fmt=REAL)
        celula(md, f"F{r}", f"=IF(D{r}=0,0,E{r}*60/D{r})", fmt=REAL)
        celula(md, f"G{r}", f'=ROUND({HORA}*D{r}/60+IF(B{r}="{COM_D}",{AD},0),2)', fmt=REAL)
        celula(md, f"H{r}", f"=IF(D{r}=0,0,G{r}*60/D{r})", fmt=REAL)
        celula(md, f"I{r}", f"=G{r}-E{r}", fmt=REAL)
        celula(md, f"J{r}", f"=C{r}*E{r}", fmt=REAL)
        celula(md, f"K{r}", f"=C{r}*G{r}", fmt=REAL)
        celula(md, f"L{r}", f"=K{r}-J{r}", fmt=REAL)
        celula(md, f"M{r}", f"=C{r}*D{r}/60", fmt=INT)
    celula(md, f"A{MT}", "Ultrassom", NEGRITO, fill=F_TOTAL)
    celula(md, f"B{MT}", None, fill=F_TOTAL)
    for col, fmt in zip("CJKLM", (INT, REAL, REAL, REAL, INT)):
        celula(md, f"{col}{MT}", f"=SUM({col}{M1}:{col}{M2})", NEGRITO, fmt, F_TOTAL)
    celula(md, f"D{MT}", f"=IF(C{MT}=0,0,M{MT}*60/C{MT})", NEGRITO, DEC, F_TOTAL)
    celula(md, f"E{MT}", f"=IF(C{MT}=0,0,J{MT}/C{MT})", NEGRITO, REAL, F_TOTAL)
    celula(md, f"F{MT}", f"=IF(M{MT}=0,0,J{MT}/M{MT})", NEGRITO, REAL, F_TOTAL)
    celula(md, f"G{MT}", f"=IF(C{MT}=0,0,K{MT}/C{MT})", NEGRITO, REAL, F_TOTAL)
    celula(md, f"H{MT}", f"=IF(M{MT}=0,0,K{MT}/M{MT})", NEGRITO, REAL, F_TOTAL)
    celula(md, f"I{MT}", f"=G{MT}-E{MT}", NEGRITO, REAL, F_TOTAL)
    for col in "FH":
        md.conditional_formatting.add(f"{col}{M1}:{col}{M2}", FormulaRule(
            formula=[f"{col}{M1}=MAX(${col}${M1}:${col}${M2})"], fill=F_BOM))
        md.conditional_formatting.add(f"{col}{M1}:{col}{M2}", FormulaRule(
            formula=[f"{col}{M1}=MIN(${col}${M1}:${col}${M2})"], fill=F_ALERTA))
    nota(md, MT + 1, "Na linha Ultrassom, os minutos e os valores por exame e por hora são médias. Verde = a hora que mais paga; "
                     "laranja = a que menos paga. Hoje a hora do médico muda conforme o exame; pelo tempo, fica igual.")
    nota(md, MT + 2, "O que entra na conta (aba Custos, Simulador e Volume) é o modo escolhido na aba Custos: "
                     "a coluna 'Pelo tempo' se for 'pelo tempo', a coluna 'Hoje' se for 'por exame'.")

    # ---- 2. por médico
    r0 = MT + 4
    secao(md, r0, "2. Por médico", MCOLS)
    for col, t in zip("ACDE", ["", "hoje (por exame)", "pelo tempo", "observação"]):
        celula(md, f"{col}{r0 + 1}", t, NEGRITO, fill=F_CAB, wrap=True, alinh="center")
    celula(md, f"B{r0 + 1}", None, fill=F_CAB)
    md.merge_cells(f"A{r0 + 1}:B{r0 + 1}")
    MEDS = "Pessoas!$C$7"
    TURNO = f"({C('h_dia')}/2)"
    linhas2 = [
        ("Médicos ultrassonografistas na rede", f"={MEDS}", f"={MEDS}", INT, "aba Pessoas: médicos por sala × salas"),
        ("Horas de sala com exame, por médico, por mês", f"=IF({MEDS}=0,0,$M${MT}/{MEDS}/{C('meses')})",
         f"=IF({MEDS}=0,0,$M${MT}/{MEDS}/{C('meses')})", DEC, "as horas do período divididas igual pelos médicos"),
        ("Recebe por mês, em média", f"=IF({MEDS}=0,0,$J${MT}/{MEDS}/{C('meses')})",
         f"=IF({MEDS}=0,0,$K${MT}/{MEDS}/{C('meses')})", REAL,
         "supõe a produção dividida igual; cada médico recebe pelo que faz"),
        ("Um turno de 5 h (metade das horas de exame do dia), só com o exame que menos paga por hora",
         f"=MIN($F${M1}:$F${M2})*{TURNO}", f"=MIN($H${M1}:$H${M2})*{TURNO}", REAL,
         "hoje é o Doppler de membros (40 min a R$ 40): o médico perde por pegar o exame demorado"),
        ("O mesmo turno, só com o exame que mais paga por hora",
         f"=MAX($F${M1}:$F${M2})*{TURNO}", f"=MAX($H${M1}:$H${M2})*{TURNO}", REAL,
         "hoje são os de 15 min (tireoide, próstata, rins...): 4 por hora a R$ 35"),
        ("Diferença entre o melhor e o pior turno", f"=C{r0 + 6}-C{r0 + 5}", f"=D{r0 + 6}-D{r0 + 5}", REAL,
         "pelo tempo, a agenda deixa de pesar no bolso do médico (só o adicional do Doppler, se houver)"),
    ]
    for i, (rot, hoje, tempo, fmt, obs) in enumerate(linhas2):
        q = r0 + 2 + i
        celula(md, f"A{q}", rot, wrap=True)
        celula(md, f"B{q}", None)
        md.merge_cells(f"A{q}:B{q}")
        celula(md, f"C{q}", hoje, fmt=fmt)
        celula(md, f"D{q}", tempo, fmt=fmt)
        md[f"E{q}"].value = obs
        md[f"E{q}"].font = NOTA
        md.row_dimensions[q].height = 28

    # ---- 3. outros valores da hora
    r3 = r0 + 2 + len(linhas2) + 1
    secao(md, r3, "3. Pelo tempo, com outros valores da hora", MCOLS)
    cab3 = ["valor da hora (troque os azuis)", "", "valor da hora", "exame de 15 min", "exame de 20 min", "exame de 40 min",
            "gasto com médico no período", "diferença contra hoje (por exame)", "margem do conjunto", "margem %"]
    for i, t in enumerate(cab3):
        celula(md, f"{get_column_letter(i + 1)}{r3 + 1}", t, NEGRITO, fill=F_CAB, wrap=True, alinh="center")
    md.merge_cells(f"A{r3 + 1}:B{r3 + 1}")
    md.row_dimensions[r3 + 1].height = 44
    DOP_Q = f'SUMIF($B${M1}:$B${M2},"{COM_D}",$C${M1}:$C${M2})'
    opcoes = [
        ("a da aba Custos (a que está na conta, se for pelo tempo)", f"={HORA}", VERDE),
        ("a que mantém o gasto de hoje (R$ 35 e R$ 40 por exame), com o adicional do Doppler da aba Custos",
         f"=IF($M${MT}=0,0,($J${MT}-{AD}*{DOP_Q})/$M${MT})", PRETO),
        ("a alternativa da aba Custos", f"={C('med_hora')}", VERDE),
        ("a da seleção do IgesDF", 174.30, AZUL),
        ("outra", 90, AZUL),
    ]
    for i, (rot, v, fonte) in enumerate(opcoes):
        q = r3 + 2 + i
        celula(md, f"A{q}", rot, wrap=True)
        celula(md, f"B{q}", None)
        md.merge_cells(f"A{q}:B{q}")
        celula(md, f"C{q}", v, fonte, REAL)
        for col, mins in zip("DEF", (15, 20, 40)):
            celula(md, f"{col}{q}", f"=ROUND($C{q}*{mins}/60,2)", fmt=REAL)
        celula(md, f"G{q}", f'=SUMPRODUCT($C${M1}:$C${M2},ROUND($C{q}*$D${M1}:$D${M2}/60+($B${M1}:$B${M2}="{COM_D}")*{AD},2))',
               fmt=REAL)
        celula(md, f"H{q}", f"=G{q}-$J${MT}", fmt=REAL)
        celula(md, f"I{q}", f"={C('marg')}+{C('c_med')}-G{q}", fmt=REAL)
        celula(md, f"J{q}", f"=IF({C('valor')}=0,0,I{q}/{C('valor')})", fmt=PCT)
        md.row_dimensions[q].height = 28
    fim3 = r3 + 2 + len(opcoes) - 1
    md.conditional_formatting.add(f"H{r3 + 2}:I{fim3}", CellIsRule(operator="lessThan", formula=["0"], font=VERMELHO))
    nota(md, fim3 + 1, "Os exames de 15, 20 e 40 min não têm o adicional do Doppler. Diferença positiva = gasta mais com médico "
                       "que hoje; a margem do conjunto troca só o médico (o resto da conta fica como na aba Custos).")
    nota(md, fim3 + 2, "Hoje (R$ 35 e R$ 40 por exame) o médico ganha R$ 140 por hora num exame de 15 min e R$ 60 num Doppler "
                       "de membros de 40 min; o pagamento pelo tempo corrige isso sem mudar o gasto, se usar a hora que o mantém.")
    nota(md, fim3 + 3, "Limite: os minutos são a agenda do CBR (aba Simulador), não o tempo medido. Quando o formulário de tempos "
                       "de 09/11 voltar, troque os exames por hora no Simulador, e o pagamento acompanha.")

    md.column_dimensions["A"].width = 46
    for col, w in zip(MCOLS[1:], (13, 12, 11, 13, 14, 14, 14, 13, 16, 16, 14, 11)):
        md.column_dimensions[col].width = w
    md.freeze_panes = f"B{M_CAB + 1}"
    md.sheet_view.showGridLines = False


# ============================================================ SIMULADOR
sim["A1"].value = "Simulador: troque as quantidades e veja a margem, se o valor fecha e se cabe nas salas"
sim["A1"].font = TITULO
nota(sim, 2, "Azul = pode trocar (tipo, quantidade, preço, exames por hora no ultrassom, minutos na tomografia e a parte com contraste); preto = fórmula. Preço = Tabela SUS "
             f"Candanga. Custo = {P['conta']} (aba Custos). As abas Custos e Volume vão atrás destas quantidades." + AVISO)
if SEB:
    celula(sim, "A3", "Cenário do médico: melhor (só a produção) ou pior (garantia em todo plantão, com todas as salas abertas)",
           NEGRITO, fill=F_BOM)
    for col in "BCD":
        celula(sim, f"{col}3", None, fill=F_BOM)
    celula(sim, "E3", "melhor", Font(name=FONTE, size=11, bold=True, color="0000FF"), None, F_BOM, alinh="center")
    dv_c = DataValidation(type="list", formula1='"melhor,pior"', allow_blank=False)
    sim.add_data_validation(dv_c)
    dv_c.add("E3")
    sim["F3"].value = ("o custo real fica entre os dois, conforme quantos plantões a rede abrir. Margem é a folga para executar, e "
                       "não lucro; o apoio (R$ 956.160) fica fora.")
    sim["F3"].font = NOTA
else:
    nota(sim, 3, "Margem é a folga para executar, e não lucro; o apoio (R$ 956.160) fica fora. 'Pelo tempo' reparte o fixo do "
                 "ultrassom pelos minutos de sala, em vez de dividir igual por exame.")
celula(sim, "A4", "Parte da fila com contraste que é feita de fato com contraste (tomografia)", NEGRITO, fill=F_BOM)
for col in "BCD":
    celula(sim, f"{col}4", None, fill=F_BOM)
celula(sim, "E4", P["contraste"], Font(name=FONTE, size=11, bold=True, color="0000FF"), '0%', F_BOM, alinh="center")
sim["F4"].value = (f"{P['contraste_obs']}o resto é feito sem contraste: custa {brl(TC_ADIC)} a menos na clínica, ocupa menos o "
                   "tomógrafo e a Candanga paga o mesmo. A seção 4 mostra de 100% a 50%.")
sim["F4"].font = NOTA
PCT_C = "$E$4"

SCOLS = "ABCDEFGHIJKLMNOPQRSTUVWX"
cabecalho(sim, S_CAB, [
    "Exame", "Modalidade", "Código", "Tipo", "Quantidade", "Preço Candanga", "Minutos de sala", "Valor que traz",
    "Custo por exame", "Custo", "Margem", "Margem %",
    "Pelo tempo: custo por exame", "Pelo tempo: margem", "Pelo tempo: margem %",
    "Horas de sala", "Feitos com contraste", "Quantidade de partida",
    "Exames por hora (no ultrassom, troque aqui)", "Margem por hora de sala",
    f"Margem por hora, médico pago por hora ({P['med_h_rot']})",
    "Exames por hora para empatar (médico por exame)" if SEB else "Exames por hora para empatar (médico como na aba Custos)",
    "Exames por hora para empatar (médico pago por hora)", "Observação"])
sim.row_dimensions[S_CAB].height = 58

hon_ex = lambda r: f'IF(D{r}="{COM_D}",{C("med_com")},{C("med_sem")})'
# na nossa conta, o médico pode ser pago pelo tempo: o valor da linha vem da aba Médico
hon = hon_ex if SEB else (lambda r: f'IF({C("med_modo")}="pelo tempo",{MED("G", M1 + r - U1)},{hon_ex(r)})')
GAR_US = f"+IF({C('us')}=0,0,{C('c_gar')}/{C('us')})" if SEB else ""
FIXO_US = f"({C('nmed')}-{C('c_mat')}-{C('c_fisc')})"          # o fixo do ultrassom, sem materiais e reserva fiscal
MIN_US = f"SUMPRODUCT($E${U1}:$E${U2},$G${U1}:$G${U2})"
MED_H = f"({C('garantia')}/{C('h_dia')})" if SEB else C("med_hora")   # o médico pago por hora
FIXO_H = f"IF({MIN_US}=0,0,{FIXO_US}*60/{MIN_US})"                       # o fixo por hora de sala usada, como hoje


def linha_base(r, e):
    nome, mod, cod, tipo, qtd, preco, mins, obs = e
    celula(sim, f"A{r}", nome)
    celula(sim, f"B{r}", mod)
    celula(sim, f"C{r}", cod, alinh="center")
    celula(sim, f"D{r}", tipo, AZUL, alinh="center")
    celula(sim, f"E{r}", qtd, AZUL, INT)
    celula(sim, f"F{r}", preco, AZUL, REAL)
    celula(sim, f"G{r}", mins, AZUL, INT, alinh="center")
    celula(sim, f"H{r}", f"=E{r}*F{r}", fmt=REAL)
    celula(sim, f"J{r}", f"=E{r}*I{r}", fmt=REAL)
    celula(sim, f"K{r}", f"=H{r}-J{r}", fmt=REAL)
    celula(sim, f"L{r}", f"=IF(H{r}=0,0,K{r}/H{r})", fmt=PCT)
    celula(sim, f"N{r}", f"=H{r}-E{r}*M{r}", fmt=REAL)
    celula(sim, f"O{r}", f"=IF(H{r}=0,0,N{r}/H{r})", fmt=PCT)
    celula(sim, f"R{r}", qtd, fmt=INT)
    celula(sim, f"S{r}", f"=IF(P{r}=0,0,E{r}/P{r})", fmt=DEC)
    celula(sim, f"T{r}", f"=IF(P{r}=0,0,N{r}/P{r})", fmt=REAL)
    celula(sim, f"X{r}", obs, NOTA)


for i, e in enumerate(EXAMES[:N_US]):
    r = U1 + i
    linha_base(r, e)
    if SEB:                     # o tempo do estudo do Sebastião, o mesmo para todo ultrassom (pode trocar exame a exame)
        celula(sim, f"S{r}", f"=60/{C('min_us_seb')}", VERDE, DEC)
    else:
        celula(sim, f"S{r}", round(60 / e[6], 2), AZUL, DEC)
    celula(sim, f"G{r}", f"=IF(S{r}=0,0,60/S{r})", fmt=DEC, alinh="center")
    # o médico da linha (pelo tempo ou por exame) mais o rateio igual do que não é médico
    celula(sim, f"I{r}", f"={hon(r)}{GAR_US}+{C('nmed_ex')}", fmt=REAL)
    celula(sim, f"M{r}", f"={hon(r)}{GAR_US}+{C('mat')}+{C('fisc')}+IF({MIN_US}=0,0,{FIXO_US}*G{r}/{MIN_US})", fmt=REAL)
    celula(sim, f"P{r}", f"=E{r}*G{r}/60", fmt=INT)
    celula(sim, f"Q{r}", None)
    # médico pago por hora de exame no lugar do pagamento por exame (e da garantia); o resto como no "pelo tempo"
    celula(sim, f"U{r}", f"=IF(G{r}=0,0,(F{r}-({MED_H}*G{r}/60+{C('mat')}+{C('fisc')}"
                         f"+IF({MIN_US}=0,0,{FIXO_US}*G{r}/{MIN_US})))*60/G{r})", fmt=REAL)
    sobra_ex = f"(F{r}-{hon(r)}{GAR_US}-{C('mat')}-{C('fisc')})"      # o que o exame deixa antes do fixo, médico por exame
    sobra_h = f"(F{r}-{C('mat')}-{C('fisc')})"                         # idem, médico pago por hora
    celula(sim, f"V{r}", f'=IF({sobra_ex}<=0,"não empata",{FIXO_H}/{sobra_ex})', fmt=DEC, alinh="right")
    celula(sim, f"W{r}", f'=IF({sobra_h}<=0,"não empata",({MED_H}+{FIXO_H})/{sobra_h})', fmt=DEC, alinh="right")
for i, e in enumerate(EXAMES[N_US:]):
    r = T1 + i
    linha_base(r, e)
    celula(sim, f"Q{r}", f'=IF(D{r}="{COM_C}",ROUND(E{r}*{PCT_C},0),0)', fmt=INT)
    celula(sim, f"I{r}", f'=IF(E{r}=0,{C("tc_s")}+IF(D{r}="{COM_C}",{PCT_C},0)*{C("tc_ad")},(E{r}*{C("tc_s")}+Q{r}*{C("tc_ad")})/E{r})',
           fmt=REAL)
    celula(sim, f"M{r}", f"=I{r}", fmt=REAL)
    celula(sim, f"P{r}", f'=IF(D{r}="{COM_C}",(Q{r}*G{r}+(E{r}-Q{r})*{C("tc_min_sem")})/60,E{r}*G{r}/60)', fmt=INT)
    celula(sim, f"U{r}", f"=T{r}", fmt=REAL)
    celula(sim, f"V{r}", "pago por exame", NOTA, alinh="center")
    celula(sim, f"W{r}", "pago por exame", NOTA, alinh="center")


def subtotal(r, rotulo, faixas, contraste=True):
    celula(sim, f"A{r}", rotulo, NEGRITO, fill=F_TOTAL)
    for col in "BCDVWX":
        celula(sim, f"{col}{r}", None, fill=F_TOTAL)
    for col in "EHJKNPQR":
        soma = "+".join(f"SUM({col}{a}:{col}{b})" if a != b else f"{col}{a}" for a, b in faixas)
        celula(sim, f"{col}{r}", f"={soma}", NEGRITO, REAL if col in "HJKN" else INT, F_TOTAL)
    if not contraste:
        celula(sim, f"Q{r}", None, fill=F_TOTAL)
    celula(sim, f"F{r}", f"=IF(E{r}=0,0,H{r}/E{r})", NEGRITO, REAL, F_TOTAL)
    celula(sim, f"G{r}", f"=IF(E{r}=0,0,P{r}*60/E{r})", NEGRITO, DEC, F_TOTAL)
    celula(sim, f"I{r}", f"=IF(E{r}=0,0,J{r}/E{r})", NEGRITO, REAL, F_TOTAL)
    celula(sim, f"L{r}", f"=IF(H{r}=0,0,K{r}/H{r})", NEGRITO, PCT, F_TOTAL)
    celula(sim, f"M{r}", f"=IF(E{r}=0,0,(H{r}-N{r})/E{r})", NEGRITO, REAL, F_TOTAL)
    celula(sim, f"O{r}", f"=IF(H{r}=0,0,N{r}/H{r})", NEGRITO, PCT, F_TOTAL)
    celula(sim, f"S{r}", f"=IF(P{r}=0,0,E{r}/P{r})", NEGRITO, DEC, F_TOTAL)
    celula(sim, f"T{r}", f"=IF(P{r}=0,0,N{r}/P{r})", NEGRITO, REAL, F_TOTAL)
    soma_u = "+".join(f"SUMPRODUCT(U{a}:U{b},P{a}:P{b})" for a, b in faixas)
    celula(sim, f"U{r}", f"=IF(P{r}=0,0,({soma_u})/P{r})", NEGRITO, REAL, F_TOTAL)


subtotal(S_US, "Ultrassom", [(U1, U2)], contraste=False)
subtotal(S_TC, "Tomografia", [(T1, T2)])
subtotal(S_TOT, "Total dos exames", [(S_US, S_US), (S_TC, S_TC)], contraste=False)
nota(sim, S_TOT + 1, "Nas linhas Ultrassom, Tomografia e Total, o preço, os minutos e o custo por exame são médias. Na tomografia, "
                     "os minutos já contam os exames que passam a sem contraste.")

dv_us = DataValidation(type="list", formula1=f'"{SEM_D},{COM_D}"', allow_blank=False)
dv_tc = DataValidation(type="list", formula1=f'"{COM_C},{SEM_C}"', allow_blank=False)
sim.add_data_validation(dv_us)
sim.add_data_validation(dv_tc)
dv_us.add(f"D{U1}:D{U2}")
dv_tc.add(f"D{T1}:D{T2}")
for col in "KLNOTU":
    sim.conditional_formatting.add(f"{col}{U1}:{col}{S_TOT}", CellIsRule(operator="lessThan", formula=["0"], font=VERMELHO))
for col in "VW":
    sim.conditional_formatting.add(f"{col}{U1}:{col}{U2}", FormulaRule(
        formula=[f'OR({col}{U1}="não empata",AND(ISNUMBER({col}{U1}),$S{U1}<{col}{U1}))'], font=VERMELHO, fill=F_ALERTA))


def par(r, rotulo, formula, fmt, fonte=PRETO, fill=None, obs=""):
    celula(sim, f"A{r}", rotulo, fonte, fill=fill)
    celula(sim, f"H{r}", formula, fonte, fmt, fill)
    if obs:
        sim[f"I{r}"].value = obs
        sim[f"I{r}"].font = NOTA


# ---------- 1. O valor fecha?
r = S_TOT + 3
secao(sim, r, "1. O valor fecha?", SCOLS)
par(r + 1, "O que as quantidades trazem", f"=H{S_TOT}", REAL, NEGRITO)
par(r + 2, "Valor a fechar com os exames", f"={C('teto')}", REAL, obs="aba Custos: o recurso menos o apoio")
par(r + 3, "Diferença: valor a fechar menos o que trazem (negativa = passa do valor)", f"=ROUND(H{r + 2}-H{r + 1},2)", REAL, NEGRITO)
par(r + 4, "Situação", f'=IF(H{r + 3}<0,"PASSA do valor a fechar",IF(H{r + 3}=0,"fecha exato","cabe: sobra a diferença acima"))',
    None, NEGRITO)
sim[f"H{r + 4}"].alignment = Alignment(horizontal="right", vertical="top")
par(r + 5, "Valor global com estas quantidades (exames mais o apoio)", f"=H{r + 1}+{C('apoio')}", REAL,
    obs="o plano assinado tem R$ 11.592.702,52; o recurso é R$ 11.592.762,00")
sim.conditional_formatting.add(f"H{r + 3}:H{r + 4}", FormulaRule(formula=[f"$H${r + 3}<0"], font=VERMELHO, fill=F_ALERTA))

# ---------- 2. Margem do conjunto
r = r + 7
secao(sim, r, "2. Margem do conjunto", SCOLS)
for col, t in zip("AHIJKL", ["", "valor que traz", "custo por exame", "custo", "margem", "margem %"]):
    celula(sim, f"{col}{r + 1}", t, NEGRITO, fill=F_CAB, wrap=True, alinh="center")
for col in "BCDEFG":
    celula(sim, f"{col}{r + 1}", None, fill=F_CAB)
for i, (rot, lin_s, fonte, fill) in enumerate([("Ultrassom", S_US, PRETO, None), ("Tomografia", S_TC, PRETO, None),
                                               ("CONJUNTO", S_TOT, NEGRITO, F_BOM)]):
    q = r + 2 + i
    celula(sim, f"A{q}", rot, fonte, fill=fill)
    for col, fmt in zip("HIJKL", (REAL, REAL, REAL, REAL, PCT)):
        celula(sim, f"{col}{q}", f"={col}{lin_s}", fonte, fmt, fill)
sim.conditional_formatting.add(f"K{r + 2}:L{r + 4}", CellIsRule(operator="lessThan", formula=["0"], font=VERMELHO))
nota(sim, r + 5, "A conta é a do lucro bruto (o que traz menos o custo direto), mas a margem não é lucro: paga o que a conta não tem "
                 "preço (responsável técnico, retaguarda, PACS, enfermagem, faltas, férias) e o imprevisto.")

# ---------- 3. Cabe nas salas?
r = r + 7
secao(sim, r, "3. Cabe nas salas de ultrassom?", SCOLS)
par(r + 1, "Horas de sala de ultrassom usadas", f"=P{S_US}", INT, NEGRITO)
par(r + 2, "Horas de sala disponíveis no período (salas × dias úteis × meses × horas de exame)", f"={C('h_disp')}", INT,
    obs="aba Custos, seção 1: troque lá as salas (fixas ou acompanhando os exames), os meses ou as horas de exame")
par(r + 3, "Uso das salas", f"=IF(H{r + 2}=0,0,H{r + 1}/H{r + 2})", PCT, NEGRITO)
par(r + 4, "Salas necessárias para estas quantidades", f"=IF(H{r + 2}=0,0,H{r + 1}/(H{r + 2}/{C('salas')}))", DEC,
    obs="com a agenda cheia: sem faltas, sem aparelho parado e sem rampa de início")
par(r + 5, "Aviso", f'=IF(H{r + 1}>H{r + 2},"NÃO CABE nas salas","cabe")', None, NEGRITO)
sim[f"H{r + 5}"].alignment = Alignment(horizontal="right", vertical="top")
par(r + 6, "Horas que faltam (negativo = folga)", f"=H{r + 1}-H{r + 2}", INT)
par(r + 7, "Ultrassons por sala por dia útil", f"=IF({C('salas')}=0,0,E{S_US}/({C('salas')}*{C('dias')}*{C('meses')}))", DEC,
    obs="quantos exames cada sala faz por dia, em média")
par(r + 8, "Tomografia: horas de tomógrafo usadas (informativo)", f"=P{S_TC}", INT)
sim.conditional_formatting.add(f"H{r + 3}:H{r + 6}", FormulaRule(formula=[f"$H${r + 1}>$H${r + 2}"], font=VERMELHO, fill=F_ALERTA))

# ---------- 4. Contraste
r = r + 10
secao(sim, r, "4. Tomografia: e se menos exames da fila com contraste forem feitos com contraste?", SCOLS)
cab4 = {"A": "cenário (troque as porcentagens em azul)", "H": "feita com contraste", "I": "feitos com contraste",
        "J": "passam a sem contraste", "K": "custo da tomografia", "L": "margem da tomografia", "M": "margem % da tomografia",
        "N": "ganho contra 100%", "O": "margem do conjunto", "P": "horas de tomógrafo",
        "Q": "parte de toda a tomografia com contraste"}
for col in SCOLS[:17]:
    celula(sim, f"{col}{r + 1}", cab4.get(col), NEGRITO, fill=F_CAB, wrap=True, alinh="center")
sim.row_dimensions[r + 1].height = 44
D_, E_, G_ = (f"${c}${T1}:${c}${T2}" for c in "DEG")
com = f'({D_}="{COM_C}")'
q0 = r + 2
for i, pc in enumerate(("=$E$4", 1, 0.9, 0.8, 0.7, 0.6, 0.5)):
    q = q0 + i
    atual = i == 0
    fill = F_BOM if atual else None
    celula(sim, f"A{q}", "a escolhida no alto da aba" if atual else None, NEGRITO if atual else PRETO, fill=fill)
    celula(sim, f"H{q}", pc, NEGRITO if atual else AZUL, '0%', fill, alinh="center")
    celula(sim, f"I{q}", f"=SUMPRODUCT(ROUND({com}*{E_}*$H{q},0))", fmt=INT, fill=fill)
    celula(sim, f"J{q}", f"=SUMPRODUCT({com}*{E_})-I{q}", fmt=INT, fill=fill)
    celula(sim, f"K{q}", f"=$E${S_TC}*{C('tc_s')}+I{q}*{C('tc_ad')}", fmt=REAL, fill=fill)
    celula(sim, f"L{q}", f"=$H${S_TC}-K{q}", fmt=REAL, fill=fill)
    celula(sim, f"M{q}", f"=IF($H${S_TC}=0,0,L{q}/$H${S_TC})", fmt=PCT, fill=fill)
    celula(sim, f"N{q}", f"=L{q}-($H${S_TC}-$E${S_TC}*{C('tc_s')}-SUMPRODUCT({com}*{E_})*{C('tc_ad')})", fmt=REAL, fill=fill)
    celula(sim, f"O{q}", f"=$K${S_US}+L{q}", fmt=REAL, fill=fill)
    celula(sim, f"P{q}", f"=(SUMPRODUCT(ROUND({com}*{E_}*$H{q},0)*({G_}-{C('tc_min_sem')}))+SUMPRODUCT({com}*{E_})*{C('tc_min_sem')}"
                         f"+SUMPRODUCT((1-{com})*{E_}*{G_}))/60", fmt=INT, fill=fill)
    celula(sim, f"Q{q}", f"=IF($E${S_TC}=0,0,I{q}/$E${S_TC})", fmt=PCT, fill=fill)
nota(sim, q0 + 7, f"Cada exame que passa a sem contraste custa {brl(TC_ADIC)} a menos na clínica e a Candanga paga o mesmo. A decisão "
                  "de usar o contraste é do radiologista, exame a exame: a porcentagem é uma hipótese.")

r = q0 + 9
for i, t in enumerate([
    "Limites da conta:",
    "- Custo por exame: o fixo do ultrassom (salas, aparelhos, auxiliares, recepção, limpeza e verbas da rede) é dividido igual "
    "por exame. Pelo tempo: o mesmo total, repartido pelos minutos de sala; um exame de 40 minutos pesa mais que um de 15.",
    "- Por isso a margem de cada linha de ultrassom muda quando muda a quantidade de qualquer outra linha de ultrassom.",
    "- O fixo não cresce com as quantidades: se elas não couberem nas salas (seção 3), é preciso pôr mais salas na aba Custos, "
    "e o fixo sobe.",
    P["limite_medico"],
    f"- Tomografia: {brl(TC_SEM)} e {brl(TC_ADIC)} de contraste por exame, pagos à clínica; garantia mínima da clínica e custo "
    "de agendamento não estão incluídos. Os minutos de tomógrafo não entram no custo.",
    "- Sem preço: responsável técnico do polo, médico de retaguarda e sistema de imagem (PACS).",
    "- Margem por hora: a margem pelo tempo vezes os exames que cabem numa hora (60 ÷ minutos), como no estudo de readequação "
    "de 09/11. No ultrassom é a hora de sala; na tomografia, a hora de tomógrafo da clínica. Mostra o que mais rende quando a "
    "sala é o que falta. A coluna seguinte troca o médico por exame pelo médico pago por hora de exame; na tomografia não muda.",
    "- Exames por hora para empatar: quantos exames por hora o ultrassom precisa fazer para a margem por hora dele chegar a "
    "zero, com o custo da hora de sala de hoje. Em vermelho, quando o ritmo da coluna 'Exames por hora' fica abaixo dele. "
    "Troque os exames por hora (azul) para ver a margem mudar; com as salas acompanhando os exames (aba Custos), o fixo cai junto.",
]):
    nota(sim, r + i, t)
sim[f"A{r}"].font = NEGRITO
r_conf = r + len(range(9)) + 1
celula(sim, f"A{r_conf}", "Conferência: custo do conjunto aqui menos o da aba Custos (deve dar 0)")
celula(sim, f"H{r_conf}", f"=ROUND(J{S_TOT}-{C('tot')},2)", fmt=REAL)
celula(sim, f"A{r_conf + 1}", "Conferência: o custo pelo tempo do ultrassom menos o dividido igual (deve dar 0)")
celula(sim, f"H{r_conf + 1}", f"=ROUND(N{S_US}-K{S_US},2)", fmt=REAL)

sim.column_dimensions["A"].width = 62
for col, w in zip(SCOLS[1:], (11, 15, 14, 11, 13, 10, 16, 13, 16, 16, 11, 13, 16, 11, 12, 12, 11, 13, 14, 18, 16, 16, 52)):
    sim.column_dimensions[col].width = w
sim.freeze_panes = f"B{S_CAB + 1}"
sim.sheet_view.showGridLines = False

wb.save(SAIDA)
print("gravado:", SAIDA.name)
