"""Planilha do quadro de gestao do plano 4 (20/10/2026): precificacao proposta e os tres cenarios.

Le o cenarios_quadro.json de cenarios_quadro.py e grava a planilha; recalcular depois com o recalc.py da skill xlsx.
Uso: python3 planilha_cenarios_quadro.py cenarios_quadro.json ../dados/quadro_gestao_cenarios_e_precificacao_20261020.xlsx
"""
import json, sys
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter as COL

R = json.load(open(sys.argv[1]))
SAIDA = sys.argv[2]

F = "Arial"
AZUL = Font(name=F, size=10, color="0000FF")
VERDE = Font(name=F, size=10, color="008000")
PRETO = Font(name=F, size=10)
NEG = Font(name=F, size=10, bold=True)
NEGV = Font(name=F, size=10, bold=True, color="008000")
TIT = Font(name=F, size=13, bold=True)
SUB = Font(name=F, size=10, italic=True, color="555555")
CAB = Font(name=F, size=10, bold=True, color="FFFFFF")
LINK = Font(name=F, size=9, color="0563C1", underline="single")
FUNDO_CAB = PatternFill("solid", fgColor="1F4E79")
FUNDO_TOT = PatternFill("solid", fgColor="DDEBF7")
FUNDO_PREM = PatternFill("solid", fgColor="FFF2CC")
FUNDO_PROP = PatternFill("solid", fgColor="E2EFDA")
FINA = Side(style="thin", color="BFBFBF")
BORDA = Border(left=FINA, right=FINA, top=FINA, bottom=FINA)
REAL = '#,##0.00;(#,##0.00);"-"'
INT = '#,##0;(#,##0);"-"'
PCT = '0.00%;(0.00%);"-"'
PCT0 = '0%'
DEC1 = '0.0'
QUEBRA = Alignment(wrap_text=True, vertical="center")
MEIO = Alignment(vertical="center")
CENTRO = Alignment(horizontal="center", vertical="center", wrap_text=True)

wb = Workbook()


def cel(ws, ref, v, font=PRETO, fmt=None, fill=None, al=None, borda=True):
    c = ws[ref]
    c.value = v
    c.font = font
    if fmt: c.number_format = fmt
    if fill: c.fill = fill
    c.alignment = al or MEIO
    if borda: c.border = BORDA
    return c


def cabecalho(ws, linha, textos, col0=1, altura=44):
    for i, t in enumerate(textos):
        cel(ws, f"{COL(col0 + i)}{linha}", t, CAB, fill=FUNDO_CAB, al=CENTRO)
    ws.row_dimensions[linha].height = altura


def texto(ws, linha, t, ate="K", neg=False, altura=None):
    cel(ws, f"A{linha}", t, NEG if neg else PRETO, al=QUEBRA, borda=False)
    ws.merge_cells(f"A{linha}:{ate}{linha}")
    if altura: ws.row_dimensions[linha].height = altura


NOMES_CEN = ["Cenário 1\n2 coordenações\n10 operadores", "Cenário 2\n3 coordenações\n6 operadores",
             "Cenário 3 (escolhido)\n3 coordenações\n8 operadores"]
pr = wb.active
pr.title = "Precificação proposta"
q = wb.create_sheet("Cenários do quadro")
p = wb.create_sheet("Cenários no plano")
m = wb.create_sheet("Mercado e aprovados")
s = wb.create_sheet("Premissas e fontes")
PR, QA, PA, MA = "'Precificação proposta'!", "'Cenários do quadro'!", "'Cenários no plano'!", "'Mercado e aprovados'!"

# ---------------------------------------------------------------- mercado (montado antes: as outras abas apontam para ela)
U = "https://www.salario.com.br/profissao/"
MER = [  # chave, rubrica, ocupacao, por que, salario, custo, referencia?, url
    ("dir", "Direção Executiva de Projeto", "Diretor Geral de Empresa e Organizações, CBO 1210-10",
     "Teto do mercado de direção", 18953.75, 32221, "não", U + "diretor-geral-de-empresa-e-organizacoes-exceto-de-interesse-publico-cbo-121010/brasilia-df/"),
    ("dir", "Direção Executiva de Projeto", "Diretor Administrativo, CBO 1231-05",
     "Direção de área, o mais próximo de dirigir um projeto", 15273.63, 25965, "sim", U + "diretor-administrativo-cbo-123105/brasilia-df/"),
    ("dir", "Direção Executiva de Projeto", "Coordenador Executivo, CBO 1311-15",
     "Piso: o projeto pede mais que uma coordenação executiva", 7323.54, 12450, "não", U + "coordenador-executivo-cbo-131115/brasilia-df"),
    ("assist", "Coordenação Assistencial", "Gerente de Serviços de Saúde, CBO 1312-10",
     "Gestão de serviço de saúde, com formação na área", 7301.09, 12412, "sim", U + "gerente-de-servicos-de-saude-cbo-131210/brasilia-df/"),
    ("admfin", "Coordenação Administrativa e Financeira", "Gerente Administrativo e Financeiro, CBO 1421-05",
     "A mesma função: orçamento, pagamentos, contratos, conformidade", 4924.39, 8371, "sim", U + "gerente-administrativo-e-financeiro-cbo-142105/brasilia-df/"),
    ("op", "Coordenação Operacional", "Gerente Administrativo e Financeiro, CBO 1421-05",
     "Nível gerencial: chefia os 3 supervisores e responde pelos 6 polos", 4924.39, 8371, "sim", U + "gerente-administrativo-e-financeiro-cbo-142105/brasilia-df/"),
    ("op", "Coordenação Operacional", "Coordenador Administrativo, CBO 4101-05",
     "Nível de supervisão: abaixo do que a função pede", 3960.67, 6733, "não", U + "coordenador-administrativo-cbo-410105/brasilia-df/"),
    ("sup", "Supervisão de Polo Assistencial", "Supervisor Administrativo, CBO 4101-05",
     "Supervisão presencial, sem chefia de equipe", 3960.67, 6733, "sim", U + "supervisor-administrativo-cbo-410105/brasilia-df/"),
    ("oper", "Operador de registro de sistemas", "Faturista, CBO 4131-15",
     "Registro e faturamento (BPA/APAC); a função pede também TrakCare e SISREG", 2206.94, 3752, "sim", U + "faturista-cbo-413115/brasilia-df"),
    ("asst", "Assistente Administrativo", "Operador de Telemarketing Ativo e Receptivo, CBO 4223-10",
     "Contato com o usuário, orientação e confirmação por telefone", 1856.35, 3156, "sim", U + "operador-de-telemarketing-ativo-e-receptivo-cbo-422310/brasilia-df/"),
    ("asst", "Assistente Administrativo", "Recepcionista de Consultório Médico ou Dentário, CBO 4221-10",
     "Agenda e confirmação em serviço de saúde", 1740.78, 2959, "não", U + "recepcionista-de-consultorio-medico-ou-dentario-cbo-422110/brasilia-df/"),
    ("asst", "Assistente Administrativo", "Assistente Administrativo, CBO 4110-10",
     "Função genérica, com suporte financeiro e documental (a do pt_ses_01)", 2981.04, 5068, "não", U + "assistente-administrativo-cbo-411010/brasilia-df/"),
    ("assess", "Assessoria de Prestação de Contas", "Contador, CBO 2522-10",
     "Tempo integral; a assessoria é serviço parcial de pessoa jurídica", 5406.75, 9191, "sim", U + "contador-cbo-252210/brasilia-df/"),
]
cel(m, "A1", "Referências de mercado no DF, por função", TIT, borda=False)
cel(m, "A2", "salario.com.br, página de Brasília/DF de cada ocupação (CBO): média do CAGED dos últimos 12 meses e o \"custo para a "
    "empresa\" que o site estima (cerca de 1,70 vez o salário). Acesso em 20/10/2026, de manhã; páginas atualizadas em 08/10/2026. "
    "Os preços dos aprovados também são custo total: o pt_ses_01 diz que incluem remuneração, benefícios e encargos.", SUB, borda=False)
m.merge_cells("A2:H2")
m.row_dimensions[2].height = 42
cabecalho(m, 4, ["Rubrica", "Ocupação comparada (CBO)", "Por que esta ocupação", "Salário médio em Brasília (R$)",
                 "Custo para a empresa em Brasília (R$)", "Usada na precificação?", "Preço proposto ÷ custo de mercado", "Fonte"])
MLIN = {}
for i, (k, rub, oc, pq, sal, custo, ref, url) in enumerate(MER):
    l = 5 + i
    if ref == "sim": MLIN[k] = l
    cel(m, f"A{l}", rub, al=QUEBRA)
    cel(m, f"B{l}", oc, al=QUEBRA)
    cel(m, f"C{l}", pq, al=QUEBRA)
    cel(m, f"D{l}", sal, AZUL, REAL)
    cel(m, f"E{l}", custo, AZUL, REAL)
    cel(m, f"F{l}", ref, NEG if ref == "sim" else PRETO, al=CENTRO, fill=FUNDO_PROP if ref == "sim" else None)
    c = cel(m, f"H{l}", url, LINK, al=QUEBRA)
    c.hyperlink = url
    m.row_dimensions[l].height = 44
ML_FIM = 5 + len(MER) - 1
for col, w in zip("ABCDEFGH", [28, 34, 40, 14, 14, 12, 14, 44]):
    m.column_dimensions[col].width = w
m.freeze_panes = "B5"

# ---------------------------------------------------------------- precificacao
cel(pr, "A1", "Plano 4 — Exames de imagem: precificação proposta do quadro de gestão e apoio", TIT, borda=False)
cel(pr, "A2", "Estudo interno de 20/10/2026. O usuário escolheu o cenário 3 com o preço proposto em 20/10/2026; o plano ainda não foi alterado. Azul = entrada; preto = fórmula; verde = vem de outra aba; "
    "fundo verde = preço proposto.", SUB, borda=False)
REGRAS = [
    ("A regra, aplicada igual a todas as rubricas", True, 16),
    ("1. Ponto de partida: o custo para a empresa, em Brasília, da ocupação que faz o mesmo trabalho que a rubrica faz neste "
     "plano, arredondado para a centena (aba \"Mercado e aprovados\").", False, 30),
    ("2. Limite: a faixa dos planos aprovados pela SES-DF para aquele nível de cargo. Se o mercado passa do maior aprovado, fica "
     "o maior aprovado: acima dele o preço perde a procedência. Se fica abaixo do menor, fica o menor aprovado, que é o "
     "preço que a SES-DF já aceitou para a mesma função.", False, 44),
    ("3. Conferência: quem chefia ganha pelo menos o que ganha quem responde a ele (coluna \"Responde a\").", False, 16),
]
for i, (t, neg, h) in enumerate(REGRAS):
    texto(pr, 4 + i, t, "N", neg, h)
cabecalho(pr, 9, ["Rubrica", "Nível", "Responde a", "O que faz neste plano", "O que a função exige (proposta)",
                  "Ocupação de mercado usada", "Custo de mercado no DF (R$)", "Faixa nos aprovados (plano: R$ por mês)",
                  "Menor aprovado (R$)", "Maior aprovado (R$)", "Preço de hoje (R$)", "Preço proposto (R$)",
                  "Proposto ÷ mercado", "Como a regra resultou"], altura=58)
PREC = [  # chave, rubrica, nivel, responde, faz, exige, faixa, min, max, hoje, resultado
    ("dir", "Direção Executiva de Projeto", "Direção", "Diretoria do ISHP",
     "Responde pelo projeto inteiro perante a SES-DF: metas, cronograma, indicadores, alinhamento das coordenações e "
     "interlocução institucional.", "Gestão de projeto de saúde ou de convênio público; 44 h, dedicação ao projeto.",
     "pt_ses_01 (ISHP): 14.500 · pt_ses_02 (IEV): 10.200", 10200, 14500, 14500,
     "O mercado de direção (R$ 26 mil) passa do maior aprovado: fica o maior aprovado."),
    ("assist", "Coordenação Assistencial", "Coordenação", "Direção Executiva",
     "Coordena a execução assistencial nos 6 polos: protocolos, fluxo regulado, segurança do contraste, qualidade e prazo "
     "do laudo, articulação com os responsáveis técnicos dos polos.", "Graduação em saúde e experiência em serviço de "
     "diagnóstico por imagem; 44 h.", "pt_ses_01 (ISHP): 10.500 · faixa de coordenação nos aprovados: 6.000 a 10.500",
     6000, 10500, 10500, "O mercado (R$ 12.400) passa do maior aprovado: fica o maior aprovado."),
    ("admfin", "Coordenação Administrativa e Financeira", "Coordenação", "Direção Executiva",
     "Execução orçamentária, pagamentos, contratações, guarda da documentação comprobatória e prestação de contas, com a "
     "assessoria.", "Administração ou ciências contábeis, experiência em convênio público; 44 h.",
     "pt_ses_01 (ISHP): 10.500 · pt_ses_02 (IEV): 6.000", 6000, 10500, 10500,
     "O mercado (R$ 8.400) cabe na faixa: fica o mercado."),
    ("op", "Coordenação Operacional", "Coordenação", "Direção Executiva",
     "Funcionamento dos 6 polos e das agendas, redistribuição de agenda entre polos, chefia dos 3 supervisores e da rotina "
     "dos operadores e assistentes.", "Gestão de operação de serviço de saúde; 44 h.",
     "pt_ses_01 (ISHP): 9.500 · faixa de coordenação nos aprovados: 6.000 a 10.500", 6000, 10500, 9500,
     "O mercado de nível gerencial (R$ 8.400) cabe na faixa: fica o mercado, no mesmo nível da Adm. e Financeira."),
    ("sup", "Supervisão de Polo Assistencial", "Supervisão", "Coordenação Operacional",
     "Presença em 2 polos: condições de funcionamento, fluxo de usuários, agendas no local e registro de ocorrências. Sem "
     "coordenação nem gestão de equipe.", "Experiência em rotina de serviço de saúde; 44 h, presencial nos polos.",
     "pt_ses_01 (ISHP): 6.155", 6155, 6155, 6155,
     "O mercado (R$ 6.700) passa do único aprovado: fica o aprovado."),
    ("oper", "Operador de registro de sistemas", "Execução", "Coordenação Operacional",
     "Pós-exame: registro do atendimento e do laudo no TrakCare, BPA/APAC, crítica dos registros e reapresentação dos "
     "rejeitados.", "Faturamento SUS (SIA/SUS, BPA e APAC), TrakCare e SISREG; 44 h.",
     "pt_ses_02, 03 e 04 (IEV): 4.300", 4300, 4300, 4300,
     "O faturista médio (R$ 3.800) fica abaixo do único aprovado: fica o aprovado, que é o preço da mesma função."),
    ("asst", "Assistente Administrativo", "Execução", "Coordenação Operacional",
     "Pré-exame: liberação da agenda no SISREG, contato com o usuário agendado pela regulação, orientação de preparo, "
     "confirmação na véspera, busca ativa e reagendamento.", "Atendimento ao público e SISREG; 44 h.",
     "pt_ses_02, 03 e 04 (IEV): 3.200 · pt_ses_01 e 05 (ISHP): 4.549,94", 3200, 4549.94, 3200,
     "O mercado da função (R$ 3.200) cabe na faixa: fica o mercado."),
    ("assess", "Assessoria de Prestação de Contas", "Serviço (PJ)", "Coordenação Adm. e Financeira",
     "Serviço parcial: organização da documentação, consolidação financeira e relatórios da prestação de contas.",
     "Contabilidade de convênio público; pessoa jurídica.",
     "pt_ses_01 (ISHP): 5.455 · pt_ses_05 (ISHP): 3.700", 3700, 5455, 5455,
     "Um contador em tempo integral (R$ 9.200) passa do maior aprovado: fica o maior aprovado."),
]
PLIN = {}
for i, (k, rub, niv, resp, faz, exige, faixa, mn, mx, hoje, como) in enumerate(PREC):
    l = 10 + i
    PLIN[k] = l
    cel(pr, f"A{l}", rub, NEG, al=QUEBRA)
    cel(pr, f"B{l}", niv, al=CENTRO)
    cel(pr, f"C{l}", resp, al=QUEBRA)
    cel(pr, f"D{l}", faz, al=QUEBRA)
    cel(pr, f"E{l}", exige, al=QUEBRA)
    cel(pr, f"F{l}", f"={MA}B{MLIN[k]}", VERDE, al=QUEBRA)
    cel(pr, f"G{l}", f"={MA}E{MLIN[k]}", VERDE, REAL)
    cel(pr, f"H{l}", faixa, al=QUEBRA)
    cel(pr, f"I{l}", mn, AZUL, REAL)
    cel(pr, f"J{l}", mx, AZUL, REAL)
    cel(pr, f"K{l}", hoje, AZUL, REAL)
    cel(pr, f"L{l}", f"=MIN(MAX(ROUND(G{l}/100,0)*100,I{l}),J{l})", NEG, REAL, FUNDO_PROP)
    cel(pr, f"M{l}", f"=L{l}/G{l}", PRETO, PCT0, al=CENTRO)
    cel(pr, f"N{l}", como, al=QUEBRA)
    pr.row_dimensions[l].height = 72
for k, l in MLIN.items():
    cel(m, f"G{l}", f"={PR}L{PLIN[k]}/E{l}", NEG, PCT0, al=CENTRO)
# conferencia da hierarquia
LH = 10 + len(PREC) + 1
texto(pr, LH, "Conferência da hierarquia (VERDADEIRO = quem chefia ganha pelo menos o que ganha quem responde a ele)", "N", True, 16)
HIER = [("Direção ≥ cada coordenação", f"=AND(L{PLIN['dir']}>=L{PLIN['assist']},L{PLIN['dir']}>=L{PLIN['admfin']},L{PLIN['dir']}>=L{PLIN['op']})"),
        ("Coordenação Operacional ≥ Supervisão de Polo", f"=L{PLIN['op']}>=L{PLIN['sup']}"),
        ("Supervisão de Polo ≥ Operador e Assistente", f"=AND(L{PLIN['sup']}>=L{PLIN['oper']},L{PLIN['sup']}>=L{PLIN['asst']})")]
for i, (rot, f) in enumerate(HIER):
    l = LH + 1 + i
    cel(pr, f"A{l}", rot)
    pr.merge_cells(f"A{l}:C{l}")
    cel(pr, f"D{l}", f, NEG, al=CENTRO)
NOTAS_PR = [
    "O que muda em relação ao preço de hoje",
    "• Só as duas coordenações administrativas mudam: a Administrativa e Financeira vai de R$ 10.500 a R$ 8.400 e a Operacional "
    "de R$ 9.500 a R$ 8.400. Eram as duas acima do mercado (125% e 113%). As outras seis ficam como estão: quatro já estão no "
    "maior aprovado, abaixo do mercado, e o operador e o assistente estão no mercado da função.",
    "• O assistente: R$ 3.200 está no mercado de quem faz contato, orientação e confirmação por telefone (R$ 3.156). A comparação "
    "com o assistente administrativo genérico (R$ 5.068) só vale se o assistente fizer suporte financeiro e documental, como no "
    "pt_ses_01; nesse caso o preço seria o do ISHP, R$ 4.549,94.",
    "• O preço segue a função, não o nome. Se parte dos operadores fizer o pré-exame (contato e confirmação), essa parte se "
    "compara ao assistente, não ao faturista.",
    "• A Coordenação Assistencial coordena; quem executa e responde tecnicamente em cada polo é o responsável técnico, pago "
    "pelo valor do exame. A descrição precisa dizer isso, para a rubrica não ser lida como custo assistencial em duplicidade (LI-018).",
]
for i, t in enumerate(NOTAS_PR):
    texto(pr, LH + 5 + i, t, "N", i == 0, 16 if i == 0 else 32)
for col, w in zip("ABCDEFGHIJKLMN", [24, 14, 16, 40, 28, 26, 12, 26, 11, 11, 11, 12, 10, 30]):
    pr.column_dimensions[col].width = w
pr.freeze_panes = "B10"

# ---------------------------------------------------------------- cenarios do quadro
cel(q, "A1", "Os três cenários do quadro, com o preço proposto", TIT, borda=False)
cel(q, "A2", "Estudo interno de 20/10/2026 sobre a v9 final da equipe (a v23 do repositório). Não altera o plano.", SUB, borda=False)
cabecalho(q, 4, ["Parâmetro", "", "Valor", "De onde vem"], col0=2, altura=20)
q.merge_cells("B4:C4")
PARAM = [
    ("Meses de vigência e de execução", 8, INT, "Estado do plano 4, v22 (decisão do usuário, 07/10/2026)"),
    ("Recurso da proposta 36000720055202500 (R$)", 11592762.00, REAL, "Ofício 40/2026 da Bancada do DF"),
    ("Teto interno do apoio hoje", 0.08, PCT, "D-002, decisão do usuário de 15/09/2026 (não é norma)"),
    ("Limite de cima da faixa do critério LI-038", 0.085, PCT, "metodo/criterios.md, LI-038: 8% a 8,5% nos planos de procedimento que paga bem"),
    ("Apoio da v9 final (R$)", 919640.00, REAL, "v9 final, planilha 8.2 (R$ 114.955 por mês × 8)"),
    ("Dias úteis no período", 168, INT, "21 dias úteis × 8 meses, como no cálculo do plano"),
    ("Minutos de trabalho por dia", 528, INT, "44 h semanais ÷ 5 dias = 8,8 h"),
]
for i, (n, v, fmt, fonte) in enumerate(PARAM):
    l = 5 + i
    cel(q, f"B{l}", n, al=QUEBRA)
    q.merge_cells(f"B{l}:C{l}")
    cel(q, f"D{l}", v, AZUL, fmt, fill=FUNDO_PREM)
    cel(q, f"E{l}", fonte, al=QUEBRA)
P = {"meses": "$D$5", "recurso": "$D$6", "teto": "$D$7", "faixa": "$D$8", "v9": "$D$9", "dias": "$D$10", "min": "$D$11"}
L0 = 14
cel(q, f"G{L0 - 1}", "Postos em cada cenário", NEG, al=CENTRO)
q.merge_cells(f"G{L0 - 1}:I{L0 - 1}")
cel(q, f"J{L0 - 1}", "Total em 8 meses, preço proposto (R$)", NEG, al=CENTRO)
q.merge_cells(f"J{L0 - 1}:L{L0 - 1}")
cabecalho(q, L0, ["Item", "Rubrica", "Meta", "R$ por mês hoje", "R$ por mês proposto", "Origem do preço proposto"]
          + NOMES_CEN + NOMES_CEN)
O01 = "pt_ses_01 — Convênio 030989/2026, ISHP, \"Visão Além do Alcance\" (OCI em oftalmologia), item "
OIEV = "pt_ses_02, 03 e 04 — Convênios 030975, 030976 e 030977/2026, IEV (Projetos DOA, DOAR e Fila Zero), "
RUB = [
    ("1.1.1", "dir", 1, O01 + "1.1.1", (1, 1, 1)),
    ("1.1.2", "op", 1, "Mercado (gerente, CBO 1421-05), dentro da faixa de coordenação dos aprovados (pt_ses_02 a pt_ses_01)", (1, 1, 1)),
    ("1.1.3", "assist", 1, O01 + "1.1.3", (0, 1, 1)),
    ("1.1.4", "sup", 1, O01 + "1.1.11 (2 supervisores para 4 polos)", (3, 3, 3)),
    ("2.1.1", "asst", 2, OIEV + "itens 1.1.5, 1.1.2 e 1.1.2; é também o mercado da função", (6, 6, 6)),
    ("3.1.1", "oper", 3, OIEV + "item 1.3.3", (10, 6, 8)),
    ("6.1.1", "admfin", 6, "Mercado (gerente administrativo e financeiro, CBO 1421-05), dentro da faixa: 6.000 (pt_ses_02) a 10.500 (pt_ses_01)", (1, 1, 1)),
    ("6.1.2", "assess", 6, O01 + "3.1.1", (1, 1, 1)),
]
QLIN = {}
for i, (it, k, meta, orig, qtd) in enumerate(RUB):
    l = L0 + 1 + i
    QLIN[k] = l
    cel(q, f"A{l}", it, al=CENTRO)
    cel(q, f"B{l}", f"={PR}A{PLIN[k]}", VERDE, al=QUEBRA)
    cel(q, f"C{l}", meta, AZUL, INT, al=CENTRO)
    cel(q, f"D{l}", f"={PR}K{PLIN[k]}", VERDE, REAL)
    cel(q, f"E{l}", f"={PR}L{PLIN[k]}", NEGV, REAL, FUNDO_PROP)
    cel(q, f"F{l}", orig, al=QUEBRA)
    for j, n in enumerate(qtd):
        cq = COL(7 + j)
        cel(q, f"{cq}{l}", n, AZUL, INT, al=CENTRO)
        cel(q, f"{COL(10 + j)}{l}", f"={cq}{l}*$E{l}*{P['meses']}", PRETO, REAL)
    q.row_dimensions[l].height = 30
LA, LB = L0 + 1, L0 + len(RUB)
LT = LB + 1
LINHAS_TOT = ["qtd", "mes", "tot", "pct_rec", "pct_glob", "folga8", "folga85", "dif", "hoje", "economia"]
ROT = {"qtd": "Postos (pessoas e serviço)", "mes": "Custo por mês, preço proposto (R$)", "tot": "Total em 8 meses, preço proposto (R$)",
       "pct_rec": "% do recurso", "pct_glob": "% do valor global do plano", "folga8": "Folga até o teto de 8% (R$; negativo = passa)",
       "folga85": "Folga até 8,5% (R$; negativo = passa)", "dif": "Diferença sobre o apoio da v9 (R$)",
       "hoje": "Total em 8 meses com o preço de hoje (R$)", "economia": "Diferença do preço proposto sobre o de hoje (R$)"}
TOT = {}
for k, chave in enumerate(LINHAS_TOT):
    l = LT + k
    TOT[chave] = l
    cel(q, f"A{l}", ROT[chave], NEG, fill=FUNDO_TOT)
    q.merge_cells(f"A{l}:F{l}")
    for j in range(3):
        cq, ct = COL(7 + j), COL(10 + j)
        if chave == "qtd":
            cel(q, f"{cq}{l}", f"=SUM({cq}{LA}:{cq}{LB})", NEG, INT, FUNDO_TOT, CENTRO)
            continue
        f = {"mes": f"=SUMPRODUCT({cq}{LA}:{cq}{LB},$E{LA}:$E{LB})",
             "tot": f"=SUM({ct}{LA}:{ct}{LB})",
             "pct_rec": f"={ct}{LT + 2}/{P['recurso']}",
             "pct_glob": f"={ct}{LT + 2}/{PA}{COL(6 + j)}$26",
             "folga8": f"={P['recurso']}*{P['teto']}-{ct}{LT + 2}",
             "folga85": f"={P['recurso']}*{P['faixa']}-{ct}{LT + 2}",
             "dif": f"={ct}{LT + 2}-{P['v9']}",
             "hoje": f"=SUMPRODUCT({cq}{LA}:{cq}{LB},$D{LA}:$D{LB})*{P['meses']}",
             "economia": f"={ct}{LT + 2}-{ct}{LT + 8}"}[chave]
        fmt = PCT if chave.startswith("pct") else REAL
        cel(q, f"{ct}{l}", f, VERDE if chave == "pct_glob" else NEG, fmt, FUNDO_TOT)
NOTAS_Q = [
    "Notas",
    "• A meta de cada rubrica segue a v9 (Meta 1 estrutura, 2 fila, 3 registro, 6 prestação de contas). A meta da Coordenação "
    "Assistencial e dos supervisores é proposta e falta decidir.",
    "• Os 6 polos não mudam estas contas: a equipe dos polos (médicos, técnicos, recepção) é paga pelo valor unitário do exame.",
    "• O % do valor global vem da aba \"Cenários no plano\", que guarda o resultado do cálculo do plano rodado com o preço "
    "proposto. Se mudar uma quantidade ou um preço, o apoio e o % do recurso se atualizam, mas os exames só mudam rodando o cálculo de novo.",
]
for k, t in enumerate(NOTAS_Q):
    texto(q, LT + len(LINHAS_TOT) + 1 + k, t, "L", k == 0, 15 if k == 0 else 30)
for col, w in zip("ABCDEFGHIJKL", [9, 30, 7, 12, 12, 44, 13, 13, 13, 15, 15, 15]):
    q.column_dimensions[col].width = w
q.freeze_panes = f"A{L0 + 1}"

# ---------------------------------------------------------------- cenarios no plano
cel(p, "A1", "O que cada cenário faz com o plano, com o preço proposto", TIT, borda=False)
cel(p, "A2", "Os exames por código (em azul) são o resultado do cálculo do próprio plano (calculo_v22.py, ramo plano-04-ultrassom-"
    "tomografia), rodado com o apoio de cada cenário em 20/10/2026. As demais linhas são fórmula.", SUB, borda=False)
p.merge_cells("A2:H2")
p.row_dimensions[2].height = 28
cabecalho(p, 4, ["Código", "Procedimento", "Valor unitário (R$)", "Fila extraída em 10/09/2026", "v9 atual"] + NOMES_CEN)
PROC = [
    ("02.05.02.009-7", "Ultrassonografia mamária bilateral", 99.94),
    ("02.05.01.004-0", "Ultrassonografia doppler colorido de vasos", 100.18),
    ("02.05.02.004-6", "Ultrassonografia de abdômen total", 100.18),
    ("02.05.02.018-6", "Ultrassonografia transvaginal", 99.94),
    ("02.05.02.005-4", "Ultrassonografia de aparelho urinário", 99.94),
    ("02.05.02.012-7", "Ultrassonografia de tireoide", 99.94),
    ("02.05.02.010-0", "Ultrassonografia de próstata por via abdominal", 99.94),
    ("02.05.02.003-8", "Ultrassonografia de abdômen superior", 99.94),
    ("02.06.02.003-1", "Tomografia computadorizada de tórax", 300.10),
    ("02.06.03.001-0", "Tomografia computadorizada de abdômen superior", 299.44),
    ("02.06.03.003-7", "Tomografia computadorizada de pelve, bacia e abdômen inferior", 299.44),
]
V9 = {"02.05.02.009-7": 14721, "02.05.02.018-6": 10565, "02.05.02.004-6": 13200, "02.05.01.004-0": 14550,
      "02.05.02.005-4": 3953, "02.05.02.012-7": 3224, "02.05.02.010-0": 3208, "02.05.02.003-8": 2266,
      "02.06.03.001-0": 4541, "02.06.03.003-7": 3885, "02.06.02.003-1": 5260}
CK = ["1p", "2p", "3p"]
for i, (c, n, u) in enumerate(PROC):
    l = 5 + i
    cel(p, f"A{l}", c, al=CENTRO)
    cel(p, f"B{l}", n, al=QUEBRA)
    cel(p, f"C{l}", u, AZUL, REAL)
    cel(p, f"D{l}", R["fila"][c], AZUL, INT)
    cel(p, f"E{l}", V9[c], AZUL, INT)
    for j, k in enumerate(CK):
        cel(p, f"{COL(6 + j)}{l}", R[k]["qc"][c], AZUL, INT)
for l, rot, f in [(16, "Total de exames", "=SUM({c}5:{c}15)"), (17, "Ultrassonografia", "=SUM({c}5:{c}12)"),
                  (18, "Tomografia computadorizada", "=SUM({c}13:{c}15)"),
                  (19, "Produção assistencial (R$)", "=SUMPRODUCT($C$5:$C$15,{c}5:{c}15)")]:
    cel(p, f"A{l}", rot, NEG, fill=FUNDO_TOT)
    p.merge_cells(f"A{l}:C{l}")
    for c in "DEFGH":
        cel(p, f"{c}{l}", f.format(c=c), NEG, REAL if l == 19 else INT, FUNDO_TOT)
cabecalho(p, 22, ["Indicador", "", "", "", "v9 atual"] + NOMES_CEN)
p.merge_cells("A22:D22")
TT = TOT["tot"]
IND = [
    (23, "Apoio: gestão e apoio (R$)", [f"={QA}D9", f"={QA}J{TT}", f"={QA}K{TT}", f"={QA}L{TT}"], REAL, VERDE),
    (24, "Envelope de produção: recurso menos apoio (R$)", f"={QA}$D$6-{{c}}23", REAL, PRETO),
    (25, "Produção assistencial (R$)", "={c}19", REAL, PRETO),
    (26, "Valor global: produção mais apoio (R$)", "={c}25+{c}23", REAL, NEG),
    (27, "Sobra não aplicada: recurso menos valor global (R$)", f"={QA}$D$6-{{c}}26", REAL, PRETO),
    (28, "% do apoio no valor global", "={c}23/{c}26", PCT, NEG),
    (29, "Exames", "={c}16", INT, NEG),
    (30, "Acréscimo sobre a fila extraída (exames)", "={c}16-$D$16", INT, PRETO),
    (31, "Diferença de exames sobre a v9", "={c}29-$E$29", INT, NEG),
    (32, "Operadores de registro de sistemas", [10, f"={QA}G{QLIN['oper']}", f"={QA}H{QLIN['oper']}", f"={QA}I{QLIN['oper']}"], INT, VERDE),
    (33, "Registros por operador por dia útil", f"={{c}}29/{QA}$D$10/{{c}}32", DEC1, PRETO),
    (34, "Minutos por registro", f"={QA}$D$11/{{c}}33", DEC1, PRETO),
    (35, "Assistentes administrativos", [10, f"={QA}G{QLIN['asst']}", f"={QA}H{QLIN['asst']}", f"={QA}I{QLIN['asst']}"], INT, VERDE),
    (36, "Contatos por assistente por dia útil (2 por exame: depois do agendamento e na véspera)", f"=2*{{c}}29/{QA}$D$10/{{c}}35", DEC1, PRETO),
    (37, "Minutos por contato", f"={QA}$D$11/{{c}}36", DEC1, PRETO),
]
for l, rot, f, fmt, fonte in IND:
    cel(p, f"A{l}", rot, al=QUEBRA)
    p.merge_cells(f"A{l}:D{l}")
    for j, c in enumerate("EFGH"):
        v = f[j] if isinstance(f, list) else f.format(c=c)
        fo = AZUL if (isinstance(f, list) and j == 0 and not str(v).startswith("=")) else fonte
        cel(p, f"{c}{l}", v, fo, fmt)
p.row_dimensions[36].height = 28
cabecalho(p, 39, ["Curva e parcelas", "", "", "", "v9 atual"] + NOMES_CEN)
p.merge_cells("A39:D39")
V9_CURVA, V9_PROD = [29760, 29764, 19849], [4001448.36, 4002247.12, 2669330.74]
PER = [("meses 1 a 3", 3), ("meses 4 a 6", 3), ("meses 7 e 8", 2)]
for i, (rot, mm) in enumerate(PER):
    l = 40 + i
    cel(p, f"A{l}", f"Exames, {rot}")
    p.merge_cells(f"A{l}:D{l}")
    cel(p, f"E{l}", V9_CURVA[i], AZUL, INT)
    for j, k in enumerate(CK):
        cel(p, f"{COL(6 + j)}{l}", R[k]["curva"][i], AZUL, INT)
cel(p, "A43", "Exames no período (confere com o total)", NEG, fill=FUNDO_TOT)
p.merge_cells("A43:D43")
for c in "EFGH":
    cel(p, f"{c}43", f"=SUM({c}40:{c}42)", NEG, INT, FUNDO_TOT)
for i, (rot, mm) in enumerate(PER):
    l = 44 + i
    cel(p, f"A{l}", f"Produção assistencial, {rot} (R$)")
    p.merge_cells(f"A{l}:D{l}")
    cel(p, f"E{l}", V9_PROD[i], AZUL, REAL)
    for j, k in enumerate(CK):
        cel(p, f"{COL(6 + j)}{l}", float(R[k]["prod_p"][i]), AZUL, REAL)
for i, (rot, mm) in enumerate(PER):
    l = 47 + i
    cel(p, f"A{l}", f"Parcela {i + 1}, {rot}: produção mais {mm}/8 do apoio (R$)")
    p.merge_cells(f"A{l}:D{l}")
    for c in "EFGH":
        cel(p, f"{c}{l}", f"={c}{44 + i}+{c}$23*{mm}/{QA}$D$5", PRETO, REAL)
cel(p, "A50", "Soma das parcelas (confere com o valor global)", NEG, fill=FUNDO_TOT)
p.merge_cells("A50:D50")
for c in "EFGH":
    cel(p, f"{c}50", f"=SUM({c}47:{c}49)", NEG, REAL, FUNDO_TOT)
cabecalho(p, 52, ["Comparação: os mesmos cenários com o preço de hoje", "", "", "", ""] + NOMES_CEN)
p.merge_cells("A52:E52")
COMP = [
    (53, "Apoio com o preço de hoje (R$)", "={q}{c2}{hoje}", REAL, VERDE),
    (54, "Valor global com o preço de hoje (R$), do cálculo do plano", None, REAL, AZUL),
    (55, "% do apoio no valor global, preço de hoje", "={c}53/{c}54", PCT, NEG),
    (56, "Exames com o preço de hoje, do cálculo do plano", None, INT, AZUL),
    (57, "Exames a mais com o preço proposto", "={c}29-{c}56", INT, NEG),
]
for l, rot, f, fmt, fonte in COMP:
    cel(p, f"A{l}", rot, al=QUEBRA)
    p.merge_cells(f"A{l}:E{l}")
    for j, (c, k) in enumerate(zip("FGH", ["1", "2", "3"])):
        if f is None:
            v = float(R[k]["global"]) if l == 54 else R[k]["total"]
        else:
            v = f.format(c=c, q=QA, c2=COL(10 + j), hoje=TOT["hoje"])
        cel(p, f"{c}{l}", v, fonte, fmt)
for col, w in zip("ABCDEFGH", [16, 44, 13, 15, 15, 16, 16, 16]):
    p.column_dimensions[col].width = w
p.freeze_panes = "A5"

# ---------------------------------------------------------------- premissas
cel(s, "A1", "Premissas, método e fontes", TIT, borda=False)
acr = [R[k]["total"] - 78572 for k in CK]
TXT = [
    ("De onde vêm os exames, e o que muda entre os cenários", True, 16),
    ("Nada da fila foi retirado. Os 78.572 exames da extração de 10/09/2026 estão inteiros em todos os cenários. O cálculo do "
     "plano cobre a fila inteira e põe o que sobra do envelope (recurso menos apoio) em exames além da fila, repartidos pelos "
     "onze códigos na proporção das solicitações que entraram em 2026. Esse acréscimo é de 801 exames na v9 e, com o preço "
     f"proposto, de {acr[0]} no cenário 1, {acr[1]} no cenário 2 e {acr[2]} no cenário 3. Um apoio maior só diminui o acréscimo; "
     "a sobra, sempre menor que um exame, fica sem aplicar.", False, 72),
    ("A precificação", True, 16),
    ("A regra está na aba \"Precificação proposta\": custo de mercado em Brasília da ocupação que faz o mesmo trabalho, limitado "
     "à faixa dos aprovados para o nível do cargo, e conferência da hierarquia. As referências de mercado e as fontes estão na "
     "aba \"Mercado e aprovados\". O teto do apoio, 8%, é decisão de 15/09/2026 (D-002), não norma; o critério LI-038 põe os "
     "planos de procedimento que paga bem entre 8% e 8,5%.", False, 58),
    ("O quadro", True, 16),
    ("Supervisores: 1 para 2 polos, como o pt_ses_01 fez (2 supervisores para 4 polos). Operadores no pós-exame (TrakCare, BPA/APAC) "
     "e assistentes no pré-exame (agenda no SISREG, contato, preparo, confirmação, busca ativa). Quem agenda é a regulação da SES-DF; "
     "o polo libera a agenda no SISREG.", False, 44),
    ("Os planos aprovados citados", True, 16),
]
l = 3
for t, neg, h in TXT:
    texto(s, l, t, "H", neg, h)
    l += 1
cabecalho(s, l, ["Plano", "Convênio", "Proponente", "Projeto e objeto", "Valor da planilha (R$)", "Meses",
                 "Assinatura", "Controle externo (registros/acervo.csv)"])
APR = [
    ("pt_ses_01", "030989/2026", "ISHP", "Visão Além do Alcance — OCI em oftalmologia", 8532671.65, 9, "29/04/2026",
     "Representação 28/2026 do MPCDF pede a suspensão cautelar; a Decisão TCDF 1500/2026 mandou a SES-DF esclarecer; "
     "em pauta em 28/09/2026 (CT-001, CT-003)"),
    ("pt_ses_02", "030975/2026", "IEV", "Projeto DOA — OCI em ortopedia", 16671550.00, 16, "29/04/2026",
     "Representação 31/2026 do MPCDF sobre os três convênios do IEV; Decisão TCDF 1501/2026 (CT-002, CT-005). "
     "O MPCDF apontou que só 63% a 69% do valor ia ao atendimento (LI-017)"),
    ("pt_ses_03", "030976/2026", "IEV", "Projeto DOAR — OCI em ortopedia", 5998920.00, 12, "29/04/2026", "Idem"),
    ("pt_ses_04", "030977/2026", "IEV", "Projeto Fila Zero — OCI em várias especialidades", 8998131.20, 12, "29/04/2026", "Idem"),
    ("pt_ses_05", "031061/2026", "ISHP", "Visão Além do Alcance — consultas em oftalmologia", 2000000.00, 8, "09/07/2026",
     "Nenhum registrado"),
]
for row in APR:
    l += 1
    for j, v in enumerate(row):
        cel(s, f"{COL(1 + j)}{l}", v, AZUL if j in (4, 5) else PRETO, REAL if j == 4 else (INT if j == 5 else None), al=QUEBRA)
    s.row_dimensions[l].height = 44
l += 2
for t, neg, h in [
    ("Onde estão as contas", True, 16),
    ("Cálculo: planos/redacao_04/calculo_v22/calculo_v22.py, no ramo plano-04-ultrassom-tomografia, com o quadro de cada cenário "
     "no lugar do da v22 (o resto igual: 8 meses, 168 dias úteis, valor unitário da Portaria SAES/MS 4.282/2026). A rodada "
     "reproduz a v9 exatamente (79.373 exames, R$ 10.673.026,22). Preços do acervo: biblioteca/precos/cargos_no_acervo.md.", False, 44),
]:
    texto(s, l, t, "H", neg, h)
    l += 1
for col, w in zip("ABCDEFGH", [11, 13, 11, 34, 15, 7, 12, 60]):
    s.column_dimensions[col].width = w

for ws in wb.worksheets:
    ws.sheet_view.showGridLines = False
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
wb.save(SAIDA)
print("ok", SAIDA)
