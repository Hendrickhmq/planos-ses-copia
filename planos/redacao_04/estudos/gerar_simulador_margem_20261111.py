"""Simulador de margem do plano 4 (11/11/2026): troque a quantidade de cada exame e veja a margem e se o valor fecha.

Gera simulador_margem_20261111.xlsx, com três abas:
  Simulador  - uma linha por exame de ultrassom e de tomografia: quantidade, preço da Tabela SUS Candanga, minutos
               de sala (os do meu estudo e os do estudo do Sebastião), valor que traz, custo pelas premissas do
               parceiro e margem, no melhor e no pior cenário do ultrassom. No alto, a parte da fila com contraste
               que é feita de fato com contraste. No rodapé: se o valor fecha, a margem do conjunto, o médico do
               ultrassom, as horas de sala pelos dois estudos e o quadro do contraste, de 100% a 50%.
  Salas por polo - a fila de cada exame repartida pelos 6 polos (Região de Saúde de quem pediu, coleta de 02/11), as
               horas e as salas que cada polo precisa, contra as salas da rede do ofício, em dois cenários: ideal (cada
               polo atende a própria Região) e real (uma matriz diz para qual polo vai a fila de cada Região).
  Premissas  - o valor a fechar e as premissas de custo do parceiro (rascunho de ofício do ISHP de 09/11/2026, as
               mesmas de planilha_custos_sebastião.xlsx).

Quantidades de partida: carteira_final_v3_20261111.xlsx, aba Escolhidos (fila de 02/11 mais os exames novos).
Preços: Tabela SUS Candanga. Minutos do meu estudo: estudo_readequacao_candanga_margem_20261109.xlsx (a articulação,
15 min, da v2). Minutos do estudo do Sebastião: 70 atendimentos de ultrassom em 9 horas (relato do usuário, 11/11).

Controle interno: não vai à SES nem ao parceiro. Tudo é fórmula; as células em azul são as premissas.
"""
import json
from pathlib import Path

from openpyxl import Workbook
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.datavalidation import DataValidation

SAIDA = Path(__file__).with_name("simulador_margem_20261111.xlsx")

FONTE = "Arial"
AZUL = Font(name=FONTE, size=10, color="0000FF")
PRETO = Font(name=FONTE, size=10)
VERDE = Font(name=FONTE, size=10, color="008000")
NEGRITO = Font(name=FONTE, size=10, bold=True)
VERMELHO = Font(name=FONTE, size=10, bold=True, color="C00000")
TITULO = Font(name=FONTE, size=14, bold=True)
SECAO = Font(name=FONTE, size=11, bold=True, color="FFFFFF")
NOTA = Font(name=FONTE, size=9, italic=True, color="555555")
F_SECAO = PatternFill("solid", fgColor="1F4E78")
F_CAB = PatternFill("solid", fgColor="D9E1F2")
F_TOTAL = PatternFill("solid", fgColor="F2F2F2")
F_ALERTA = PatternFill("solid", fgColor="FCE4D6")
F_BOM = PatternFill("solid", fgColor="E2EFDA")
FINA = Side(style="thin", color="BFBFBF")
BORDA = Border(left=FINA, right=FINA, top=FINA, bottom=FINA)

REAL = 'R$ #,##0.00'
REAL3 = 'R$ #,##0.000'
INT = '#,##0'
DEC = '#,##0.00'
PCT = '0.0%'

SEM_D, COM_D, COM_C, SEM_C = "sem Doppler", "com Doppler", "com contraste", "sem contraste"

# (exame, modalidade, código, tipo, quantidade de partida, preço Candanga, minutos de sala, observação)
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
    ("Doppler de carótidas e outros vasos", "Ultrassom", "02.05.01.004-0", COM_D, 5952, 115.61, 20, "4.727 da fila e 1.225 novos"),
    ("Doppler de membros (os dois lados)", "Ultrassom", "02.05.01.004-0", COM_D, 12034, 115.61, 40,
     "condição D-011: um exame por pedido na conta; 40 min de sala"),
    ("US de articulação, fora da ortopedia", "Ultrassom", "02.05.02.006-2", SEM_D, 4557, 70.97, 15,
     "minutos estimados (carteira v2); a ortopedia fica com o IEV (D-012)"),
    ("TC de abdômen superior com contraste", "Tomografia", "02.06.03.001-0", COM_C, 4116, 309.25, 20, ""),
    ("TC de abdômen superior sem contraste", "Tomografia", "02.06.03.001-0", SEM_C, 68, 309.25, 11, ""),
    ("TC de pelve com contraste", "Tomografia", "02.06.03.003-7", COM_C, 3634, 309.25, 20, ""),
    ("TC de pelve sem contraste", "Tomografia", "02.06.03.003-7", SEM_C, 56, 309.25, 11, ""),
    ("TC de tórax com contraste", "Tomografia", "02.06.02.003-1", COM_C, 2350, 309.25, 20, ""),
    ("TC de tórax sem contraste", "Tomografia", "02.06.02.003-1", SEM_C, 180, 309.25, 11, ""),
    ("TC de pescoço com contraste", "Tomografia", "02.06.01.005-2", COM_C, 479, 309.25, 20, ""),
    ("TC de crânio sem contraste", "Tomografia", "02.06.01.007-9", SEM_C, 44, 251.29, 11, ""),
]


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


def secao(ws, linha, texto, colunas):
    for col in colunas:
        ws[f"{col}{linha}"].fill = F_SECAO
    c = ws[f"A{linha}"]
    c.value = texto
    c.font = SECAO


def cabecalho(ws, linha, colunas, textos, altura=42):
    for col, t in zip(colunas, textos):
        celula(ws, f"{col}{linha}", t, NEGRITO, fill=F_CAB, wrap=True, alinh="center")
    ws.row_dimensions[linha].height = altura


def nota(ws, linha, texto):
    c = ws[f"A{linha}"]
    c.value = texto
    c.font = NOTA


FILAS = Path(__file__).with_name("estudo_filas_imagem_20261102.json")
POLOS = ["Oeste", "Sudoeste", "Norte", "Leste", "Central e Centro-Sul", "Sul"]
REGIAO_POLO = {"Região Oeste": "Oeste", "Região Sudoeste": "Sudoeste", "Região Norte": "Norte", "Região Leste": "Leste",
               "Região Central": "Central e Centro-Sul", "Região Centro-Sul": "Central e Centro-Sul", "Região Sul": "Sul"}
# rede de ultrassom do rascunho de ofício do ISHP de 09/11/2026: (unidades, salas)
REDE = {"Oeste": ("Clínica Brasília (1) e Carneiro de Mendonça (4), em Ceilândia", 5),
        "Sudoeste": ("Med Brasília (Samambaia)", 1), "Norte": ("Infinita (Sobradinho)", 1),
        "Leste": ("nenhuma unidade no ofício", 0), "Central e Centro-Sul": ("Infinita (Guará II)", 2),
        "Sul": ("PróVida (Gama)", 2)}
# cenário real, partida: para qual polo vai a fila de cada Região (hipótese, editável na planilha)
ROTA = {"Sudoeste": {"Sudoeste": 0.25, "Oeste": 0.75}, "Leste": {"Norte": 0.5, "Central e Centro-Sul": 0.5}}
# exame do simulador -> grupo da coleta de Região de 02/11 (estudo das filas, revisao.participacoes)
ORIGEM = {
    "US de abdômen total (adulto)": "abdomen_total", "US de abdômen total (criança)": "abdomen_total",
    "US de parede abdominal": "parede", "US de abdômen superior": "abdomen_superior",
    "US de aparelho urinário e rins (adulto)": "urinario", "US de aparelho urinário (criança)": "urinario",
    "US de bolsa escrotal (adulto)": "bolsa_escrotal", "US de bolsa escrotal (criança)": "bolsa_escrotal",
    "US de próstata (via abdominal)": "prostata", "US de tireoide (adulto, com o Doppler de tireoide)": "tireoide",
    "US de tireoide (criança)": "tireoide", "US de mamas (as duas)": "mama", "US transvaginal": "transvaginal",
    "Doppler de carótidas e outros vasos": "doppler_outros", "Doppler de membros (os dois lados)": "doppler_membros",
}


def partes_por_polo():
    """Parte de cada polo na fila de cada grupo de ultrassom. Pedidos sem Região (URD, contratado, sem registro)
    se repartem na mesma proporção. Devolve também a média de todos os grupos, para o exame sem coleta de Região."""
    part = json.load(open(FILAS, encoding="utf-8"))["revisao"]["participacoes"]
    partes, soma = {}, dict.fromkeys(POLOS, 0)
    for chave in set(ORIGEM.values()):
        n = dict.fromkeys(POLOS, 0)
        for regiao, q in part[chave]["por_regiao"].items():
            if regiao in REGIAO_POLO:
                n[REGIAO_POLO[regiao]] += q
                soma[REGIAO_POLO[regiao]] += q
        partes[chave] = [n[p] / sum(n.values()) for p in POLOS]
    partes[None] = [soma[p] / sum(soma.values()) for p in POLOS]
    return partes


def gerar(saida=SAIDA, exames=EXAMES, pct_contraste=1.0):
    wb = Workbook()
    sim = wb.active
    sim.title = "Simulador"
    sp = wb.create_sheet("Salas por polo")
    pr = wb.create_sheet("Premissas")
    R_REDE = 10 + len(POLOS)  # linha "Rede" do resumo da aba Salas por polo

    # ============================================================ PREMISSAS
    P = {}  # nome -> referência absoluta na aba Premissas

    def premissa(linha, chave, rotulo, valor, fmt, obs="", entrada=True):
        celula(pr, f"A{linha}", rotulo)
        celula(pr, f"B{linha}", valor, AZUL if entrada else PRETO, fmt)
        celula(pr, f"C{linha}", obs, NOTA, borda=False)
        P[chave] = f"Premissas!$B${linha}"

    pr["A1"].value = "Premissas: o valor a fechar e o custo pelas contas do parceiro"
    pr["A1"].font = TITULO
    nota(pr, 2, "Custos: rascunho de ofício do ISHP de 09/11/2026 (os mesmos de planilha_custos_sebastião.xlsx). "
                "Azul = premissa que pode ser trocada; preto = fórmula.")
    nota(pr, 3, "Controle interno: não vai à SES nem ao parceiro.")

    secao(pr, 5, "1. Valor a fechar", "ABCDE")
    premissa(6, "global", "Valor global do plano", 11592702.52, REAL, "")
    premissa(7, "acessorio", "Custo acessório (apoio e gestão)", 956160, REAL,
             "valor fixo no total, em qualquer prazo: não multiplicar por meses nem ratear por mês")
    premissa(8, "alvo", "Valor a fechar com os exames", "=B6-B7", REAL,
             "o que as quantidades precisam somar; pode ser trocado por um número", entrada=False)
    pr["B8"].font = NEGRITO

    secao(pr, 10, "2. Ultrassom: rede e plantão", "ABCDE")
    premissa(11, "meses", "Meses de execução", 12, INT, "ofício: 10/12/2026 a 09/12/2027")
    premissa(12, "dias", "Dias úteis por mês", 21, INT, "ofício: 252 dias, sem descontar feriados")
    premissa(13, "salas", "Salas de ultrassom", f"='Salas por polo'!$C${R_REDE}", INT,
             "soma das salas de cada polo: troque na aba Salas por polo (ofício: 11 salas em 6 unidades)", entrada=False)
    premissa(14, "unidades", "Unidades (postos de recepção)", 6, INT, "1 posto por unidade")
    premissa(15, "h_plantao", "Duração do plantão, em horas", 10, INT, "definido pelo usuário em 11/11")
    premissa(16, "h_almoco", "Almoço, em horas", 1, INT, "definido pelo usuário em 11/11")
    premissa(17, "min_uteis", "Minutos úteis do plantão, no meu estudo", "=(B15-B16)*60", INT, "", entrada=False)
    premissa(18, "min_seb", "Minutos úteis do plantão, no estudo do Sebastião", "=B51*60", INT, "as horas do estudo dele (seção 6)",
             entrada=False)
    premissa(19, "pl_dia", "Plantões por sala por dia útil", 1, INT, "")
    premissa(20, "plantoes", "Plantões no período, com todas as salas abertas todo dia útil", "=B13*B12*B11*B19", INT,
             "é o pior cenário", entrada=False)

    secao(pr, 22, "3. Ultrassom: médico", "ABCDE")
    premissa(23, "hon_sem", "Honorário médico por exame sem Doppler", 35, REAL, "ofício, Anexo III")
    premissa(24, "hon_com", "Honorário médico por exame com Doppler", 40, REAL, "ofício, Anexo III")
    premissa(25, "garantia", "Garantia mínima do médico por plantão", 1500, REAL,
             "o médico recebe o maior entre a produção do plantão e a garantia")

    secao(pr, 27, "4. Ultrassom: custos não médicos", "ABCDE")
    cabecalho(pr, 28, "ABCDE", ["item", "quantidade", "valor unitário", "por mês", "no período"], 30)
    fixos = [
        ("Auxiliar de sala", "=B13", 3180),
        ("Recepção", "=B14", 3500),
        ("Aluguel da sala", "=B13", 1500),
        ("Aluguel do aparelho de ultrassom", "=B13", 2500),
        ("Gestão e coordenação (verba do ofício)", 1, 3500),
        ("Limpeza e resíduos", 1, 2400),
        ("Sistemas e comunicação", 1, 1500),
        ("Logística e contingência", 1, 2600),
    ]
    for i, (nome, qtd, unit) in enumerate(fixos):
        r = 29 + i
        celula(pr, f"A{r}", nome)
        celula(pr, f"B{r}", qtd, PRETO if isinstance(qtd, str) else AZUL, INT)
        celula(pr, f"C{r}", unit, AZUL, REAL)
        celula(pr, f"D{r}", f"=B{r}*C{r}", fmt=REAL)
        celula(pr, f"E{r}", f"=D{r}*$B$11", fmt=REAL)
    celula(pr, "A37", "Fixo do ultrassom", NEGRITO, fill=F_TOTAL)
    celula(pr, "B37", None, fill=F_TOTAL)
    celula(pr, "C37", None, fill=F_TOTAL)
    celula(pr, "D37", "=SUM(D29:D36)", NEGRITO, REAL, F_TOTAL)
    celula(pr, "E37", "=SUM(E29:E36)", NEGRITO, REAL, F_TOTAL)
    P["fixo"] = "Premissas!$E$37"
    nota(pr, 38, "O fixo é rateado igualmente por exame de ultrassom, como o parceiro faz: menos exames, mais fixo em cada um.")
    premissa(39, "materiais", "Materiais, por exame", "=177414/54589", REAL3, "ofício: R$ 177.414 para 54.589 exames (R$ 3,25)")
    pr["B39"].font = AZUL
    premissa(40, "fiscal", "Reserva fiscal, por exame", 5.994, REAL3, "hipótese do ofício, não é alíquota validada")

    secao(pr, 42, "5. Tomografia", "ABCDE")
    premissa(43, "tc_sem", "Preço da clínica por exame, sem contraste", 175, REAL, "ofício, Anexo IV; cobre tudo do exame")
    premissa(44, "tc_adic", "Adicional quando o contraste é usado", 43, REAL, "ofício, Anexo IV; a Candanga não paga o contraste à parte")
    premissa(45, "tc_com", "Preço da clínica por exame, com contraste", "=B43+B44", REAL, "", entrada=False)
    premissa(46, "tc_min_sem", "Minutos de tomógrafo do exame pedido com contraste e feito sem", 11, INT,
             "o mesmo tempo da tomografia sem contraste (estudo de 09/11)")
    nota(pr, 47, "A parte da fila com contraste que é feita de fato com contraste fica na aba Simulador, no alto (o ofício projeta 93% "
                 "de toda a tomografia).")

    secao(pr, 49, "6. Estudo do Sebastião: tempo do ultrassom", "ABCDE")
    premissa(50, "seb_atend", "Atendimentos de ultrassom no estudo", 70, INT, "apresentado pelo Sebastião ao usuário (relato de 11/11)")
    premissa(51, "seb_horas", "Horas do estudo", 9, INT, "")
    premissa(52, "seb_min", "Minutos por exame", "=B51*60/B50", DEC,
             "vale para todo ultrassom na coluna do Sebastião da aba Simulador; lá dá para trocar exame a exame", entrada=False)
    nota(pr, 53, "Não sei se os 70 atendimentos foram numa sala só, com um médico, nem que exames eram. O ofício de 09/11 usa outra "
                 "conta: 20 minutos por exame e 480 minutos úteis, como sensibilidade.")

    pr.column_dimensions["A"].width = 60
    for col, w in zip("BCDE", (18, 16, 16, 18)):
        pr.column_dimensions[col].width = w
    pr.freeze_panes = "B5"

    # ============================================================ SIMULADOR
    sim["A1"].value = "Simulador de margem: troque as quantidades e veja a margem e se o valor fecha"
    sim["A1"].font = TITULO
    nota(sim, 2, "Azul = pode trocar (quantidade, tipo, preço, minutos e a parte com contraste); preto = fórmula. Preço = Tabela SUS "
                 "Candanga. Custo = contas do parceiro (aba Premissas). Controle interno: não vai à SES nem ao parceiro.")
    nota(sim, 3, "Melhor cenário do ultrassom: médico só por produção (a garantia nunca é cobrada). Pior: todas as salas "
                 "abertas todo dia útil, com a garantia cobrada quando a produção média do plantão fica abaixo dela.")
    celula(sim, "A4", "Parte da fila com contraste que é feita de fato com contraste (tomografia)", NEGRITO, fill=F_BOM)
    for col in "BCD":
        celula(sim, f"{col}4", None, fill=F_BOM)
    celula(sim, "E4", pct_contraste, Font(name=FONTE, size=11, bold=True, color="0000FF"), '0%', F_BOM, alinh="center")
    celula(sim, "F4", "o resto é feito sem contraste: custa R$ 43 a menos na clínica, ocupa menos o tomógrafo e a Candanga paga "
                      "o mesmo. O quadro da seção 5 mostra de 100% a 50%.", NOTA, borda=False)
    PCT_C = "$E$4"

    CAB = 5
    cols = "ABCDEFGHIJKLMNOPQRSTUV"
    cabecalho(sim, CAB, cols, [
        "Exame", "Modalidade", "Código", "Tipo", "Quantidade", "Preço Candanga",
        "Minutos, meu estudo", "Minutos, estudo do Sebastião", "Valor que traz",
        "Custo por exame, melhor", "Custo, melhor", "Margem, melhor", "Margem %, melhor",
        "Custo por exame, pior", "Custo, pior", "Margem, pior", "Margem %, pior",
        "Horas de sala, meu estudo", "Horas de sala, estudo do Sebastião", "Feitos com contraste",
        "Quantidade de partida", "Observação"], 56)

    us = [e for e in exames if e[1] == "Ultrassom"]
    tc = [e for e in exames if e[1] == "Tomografia"]
    u1 = CAB + 1
    u2 = u1 + len(us) - 1
    SUB_US = u2 + 1
    t1 = SUB_US + 1
    t2 = t1 + len(tc) - 1
    SUB_TC = t2 + 1
    TOT = SUB_TC + 1

    # linhas do rodapé (definidas antes porque as linhas dos exames apontam para elas)
    R_FECHA = TOT + 2          # seção 1
    R_MARG = R_FECHA + 8       # seção 2
    R_MED = R_MARG + 13        # seção 3
    R_SALA = R_MED + 16        # seção 4
    R_CONT = R_SALA + 12       # seção 5
    n_us = f"$E${SUB_US}"
    prod = f"$I${R_MED + 2}"
    falta_gar = f"$I${R_MED + 5}"   # produção média do plantão abaixo da garantia? (1 = sim)
    med_pior = f"$I${R_MED + 7}"

    def linha_base(r, e, min_seb):
        nome, mod, cod, tipo, qtd, preco, mins, obs = e
        celula(sim, f"A{r}", nome)
        celula(sim, f"B{r}", mod)
        celula(sim, f"C{r}", cod, alinh="center")
        celula(sim, f"D{r}", tipo, AZUL, alinh="center")
        celula(sim, f"E{r}", qtd, AZUL, INT)
        celula(sim, f"F{r}", preco, AZUL, REAL)
        celula(sim, f"G{r}", mins, AZUL, INT, alinh="center")
        celula(sim, f"H{r}", min_seb, AZUL, INT, alinh="center")
        celula(sim, f"I{r}", f"=E{r}*F{r}", fmt=REAL)
        celula(sim, f"L{r}", f"=I{r}-K{r}", fmt=REAL)
        celula(sim, f"M{r}", f"=IF(I{r}=0,0,L{r}/I{r})", fmt=PCT)
        celula(sim, f"P{r}", f"=I{r}-O{r}", fmt=REAL)
        celula(sim, f"Q{r}", f"=IF(I{r}=0,0,P{r}/I{r})", fmt=PCT)
        celula(sim, f"U{r}", qtd, fmt=INT)
        celula(sim, f"V{r}", obs, NOTA)

    nao_med = f"(IF({n_us}=0,0,{P['fixo']}/{n_us})+{P['materiais']}+{P['fiscal']})"
    for i, e in enumerate(us):
        r = u1 + i
        linha_base(r, e, f"={P['seb_min']}")
        sim[f"H{r}"].font = PRETO
        sim[f"H{r}"].number_format = '0.0'
        hon = f'IF(D{r}="{COM_D}",{P["hon_com"]},{P["hon_sem"]})'
        celula(sim, f"J{r}", f"={nao_med}+{hon}", fmt=REAL)
        celula(sim, f"K{r}", f"=E{r}*J{r}", fmt=REAL)
        celula(sim, f"N{r}", f"={nao_med}+IF({falta_gar}=1,{med_pior}/{n_us},{hon})", fmt=REAL)
        celula(sim, f"O{r}", f"=E{r}*N{r}", fmt=REAL)
        celula(sim, f"R{r}", f"=E{r}*G{r}/60", fmt=INT)
        celula(sim, f"S{r}", f"=E{r}*H{r}/60", fmt=INT)
        celula(sim, f"T{r}", None)
    for i, e in enumerate(tc):
        r = t1 + i
        linha_base(r, e, e[6])
        celula(sim, f"T{r}", f'=IF(D{r}="{COM_C}",ROUND(E{r}*{PCT_C},0),0)', fmt=INT)
        celula(sim, f"J{r}", f"=IF(E{r}=0,{P['tc_sem']}+IF(D{r}=\"{COM_C}\",{PCT_C},0)*{P['tc_adic']},K{r}/E{r})", fmt=REAL)
        celula(sim, f"K{r}", f"=E{r}*{P['tc_sem']}+T{r}*{P['tc_adic']}", fmt=REAL)
        celula(sim, f"N{r}", f"=J{r}", fmt=REAL)
        celula(sim, f"O{r}", f"=K{r}", fmt=REAL)
        for col, m in (("R", "G"), ("S", "H")):
            celula(sim, f"{col}{r}", f'=IF(D{r}="{COM_C}",(T{r}*{m}{r}+(E{r}-T{r})*{P["tc_min_sem"]})/60,E{r}*{m}{r}/60)', fmt=INT)

    def subtotal(r, rotulo, faixas, contraste=True):
        celula(sim, f"A{r}", rotulo, NEGRITO, fill=F_TOTAL)
        for col in "BCDV":
            celula(sim, f"{col}{r}", None, fill=F_TOTAL)
        for col in "EIKLOPRSTU":
            soma = "+".join(f"SUM({col}{a}:{col}{b})" if a != b else f"{col}{a}" for a, b in faixas)
            celula(sim, f"{col}{r}", f"={soma}", NEGRITO, REAL if col in "IKLOP" else INT, F_TOTAL)
        if not contraste:
            celula(sim, f"T{r}", None, fill=F_TOTAL)
        celula(sim, f"F{r}", f"=IF(E{r}=0,0,I{r}/E{r})", NEGRITO, REAL, F_TOTAL)
        celula(sim, f"G{r}", f"=IF(E{r}=0,0,R{r}*60/E{r})", NEGRITO, DEC, F_TOTAL)
        celula(sim, f"H{r}", f"=IF(E{r}=0,0,S{r}*60/E{r})", NEGRITO, DEC, F_TOTAL)
        celula(sim, f"J{r}", f"=IF(E{r}=0,0,K{r}/E{r})", NEGRITO, REAL, F_TOTAL)
        celula(sim, f"N{r}", f"=IF(E{r}=0,0,O{r}/E{r})", NEGRITO, REAL, F_TOTAL)
        celula(sim, f"M{r}", f"=IF(I{r}=0,0,L{r}/I{r})", NEGRITO, PCT, F_TOTAL)
        celula(sim, f"Q{r}", f"=IF(I{r}=0,0,P{r}/I{r})", NEGRITO, PCT, F_TOTAL)

    subtotal(SUB_US, "Ultrassom", [(u1, u2)], contraste=False)
    subtotal(SUB_TC, "Tomografia", [(t1, t2)])
    subtotal(TOT, "Total dos exames", [(SUB_US, SUB_US), (SUB_TC, SUB_TC)], contraste=False)
    nota(sim, TOT + 1, "Nas linhas Ultrassom, Tomografia e Total, o preço, os minutos e o custo por exame são médias. Na tomografia, "
                       "os minutos médios já contam os exames que passam a sem contraste.")

    dv_us = DataValidation(type="list", formula1=f'"{SEM_D},{COM_D}"', allow_blank=False)
    dv_tc = DataValidation(type="list", formula1=f'"{COM_C},{SEM_C}"', allow_blank=False)
    sim.add_data_validation(dv_us)
    sim.add_data_validation(dv_tc)
    dv_us.add(f"D{u1}:D{u2}")
    dv_tc.add(f"D{t1}:D{t2}")
    vermelho = Font(name=FONTE, color="C00000", bold=True)
    for col in "LMPQ":
        sim.conditional_formatting.add(f"{col}{u1}:{col}{TOT}", CellIsRule(operator="lessThan", formula=["0"], font=vermelho))

    def par(r, rotulo, formula, fmt, fonte=PRETO, fill=None, obs=""):
        celula(sim, f"A{r}", rotulo, fonte, fill=fill)
        celula(sim, f"I{r}", formula, fonte, fmt, fill)
        if obs:
            celula(sim, f"J{r}", obs, NOTA, borda=False)

    def direita(ref):
        sim[ref].alignment = Alignment(horizontal="right", vertical="top")

    # ---------- 1. O valor fecha?
    r = R_FECHA
    secao(sim, r, "1. O valor fecha?", cols)
    par(r + 1, "Total que as quantidades trazem", f"=I{TOT}", REAL, NEGRITO)
    par(r + 2, "Valor a fechar com os exames", f"={P['alvo']}", REAL, obs="aba Premissas: valor global menos o custo acessório")
    par(r + 3, "Diferença: valor a fechar menos o total (negativa = passa do valor)", f"=ROUND(I{r + 2}-I{r + 1},2)", REAL, NEGRITO)
    par(r + 4, "Situação", f'=IF(I{r + 3}<0,"PASSA do valor a fechar",IF(I{r + 3}=0,"fecha exato","cabe: sobra a diferença acima"))',
        None, NEGRITO)
    direita(f"I{r + 4}")
    par(r + 5, "Custo acessório (informativo: valor fixo no total, fora da margem dos exames)", f"={P['acessorio']}", REAL)
    par(r + 6, "Valor global com estas quantidades (exames mais o custo acessório)", f"=I{r + 1}+I{r + 5}", REAL,
        obs="para comparar com o valor global do plano, na aba Premissas")
    sim.conditional_formatting.add(f"I{r + 3}:I{r + 4}", FormulaRule(formula=[f"$I${r + 3}<0"], font=vermelho, fill=F_ALERTA))

    # ---------- 2. Margem do conjunto
    r = R_MARG
    secao(sim, r, "2. Margem do conjunto", cols)
    cabecalho(sim, r + 1, "AIJKLM", ["cenário", "valor que traz", "custo", "margem", "margem %", "custo por exame"], 30)
    for col in "BCDEFGH":
        celula(sim, f"{col}{r + 1}", None, fill=F_CAB)
    T_MIN = R_MED + 10  # quadro "pelos minutos": colunas I (meu estudo) e J (Sebastião); o médico fica 3 linhas abaixo
    nm_us = f"({P['fixo']}+({P['materiais']}+{P['fiscal']})*{n_us})"
    quadro = [
        ("Ultrassom, melhor cenário (médico só por produção)", f"=I{SUB_US}", f"=K{SUB_US}", f"E{SUB_US}", PRETO, None),
        ("Ultrassom, pelos minutos do meu estudo (só os plantões necessários)", f"=I{SUB_US}",
         f"=IF({n_us}=0,0,{nm_us}+$I${T_MIN + 4})", f"E{SUB_US}", PRETO, None),
        ("Ultrassom, pelos minutos do estudo do Sebastião (só os plantões necessários)", f"=I{SUB_US}",
         f"=IF({n_us}=0,0,{nm_us}+$J${T_MIN + 4})", f"E{SUB_US}", PRETO, None),
        ("Ultrassom, pior cenário (todas as salas abertas todo dia útil)", f"=I{SUB_US}", f"=O{SUB_US}", f"E{SUB_US}", PRETO, None),
        ("Tomografia", f"=I{SUB_TC}", f"=K{SUB_TC}", f"E{SUB_TC}", PRETO, None),
        ("CONJUNTO, melhor cenário", f"=I{r + 2}+I{r + 6}", f"=J{r + 2}+J{r + 6}", f"E{TOT}", NEGRITO, F_BOM),
        ("CONJUNTO, pelos minutos do meu estudo", f"=I{r + 3}+I{r + 6}", f"=J{r + 3}+J{r + 6}", f"E{TOT}", NEGRITO, F_TOTAL),
        ("CONJUNTO, pelos minutos do estudo do Sebastião", f"=I{r + 4}+I{r + 6}", f"=J{r + 4}+J{r + 6}", f"E{TOT}", NEGRITO, F_TOTAL),
        ("CONJUNTO, pior cenário", f"=I{r + 5}+I{r + 6}", f"=J{r + 5}+J{r + 6}", f"E{TOT}", NEGRITO, F_ALERTA),
    ]
    for i, (rot, valor, custo, qtd, fonte, fill) in enumerate(quadro):
        q = r + 2 + i
        celula(sim, f"A{q}", rot, fonte, fill=fill)
        celula(sim, f"I{q}", valor, fonte, REAL, fill)
        celula(sim, f"J{q}", custo, fonte, REAL, fill)
        celula(sim, f"K{q}", f"=I{q}-J{q}", fonte, REAL, fill)
        celula(sim, f"L{q}", f"=IF(I{q}=0,0,K{q}/I{q})", fonte, PCT, fill)
        celula(sim, f"M{q}", f"=IF({qtd}=0,0,J{q}/{qtd})", fonte, REAL, fill)
    sim.conditional_formatting.add(f"K{r + 2}:L{r + 10}", CellIsRule(operator="lessThan", formula=["0"], font=vermelho))
    nota(sim, r + 11, "A margem é a folga para executar, e não lucro. O custo acessório fica fora dela. As linhas 'pelos minutos' "
                      "não estão nas contas do parceiro: usam os minutos de sala desta aba (ver seção 3).")

    # ---------- 3. Médico do ultrassom
    r = R_MED
    secao(sim, r, "3. Médico do ultrassom: como a conta saiu", cols)
    par(r + 1, "Exames de ultrassom", f"=E{SUB_US}", INT)
    par(r + 2, "Produção: exames × honorário (é o médico do melhor cenário)",
        f'=SUMIF(D{u1}:D{u2},"{COM_D}",E{u1}:E{u2})*{P["hon_com"]}+(E{SUB_US}-SUMIF(D{u1}:D{u2},"{COM_D}",E{u1}:E{u2}))*{P["hon_sem"]}',
        REAL)
    par(r + 3, "Pior cenário: plantões no período, com todas as salas abertas", f"={P['plantoes']}", INT)
    par(r + 4, "Pior cenário: produção média por plantão", f"=IF(I{r + 3}=0,0,{prod}/I{r + 3})", REAL)
    par(r + 5, "Pior cenário: a produção média fica abaixo da garantia? (1 = sim, a garantia é cobrada)",
        f"=IF(I{r + 4}<{P['garantia']},1,0)", INT)
    par(r + 6, "Pior cenário: pago ao médico por plantão", f"=MAX({P['garantia']},I{r + 4})", REAL)
    par(r + 7, "Pior cenário: médico no período", f"=I{r + 6}*I{r + 3}", REAL, NEGRITO)
    par(r + 8, "Exames por plantão para a produção alcançar a garantia, sem Doppler", f"={P['garantia']}/{P['hon_sem']}", DEC,
        obs="um exame a cada 12,6 minutos, num plantão de 540 minutos úteis")
    sim[f"J{r + 8}"].value = None
    celula(sim, f"J{r + 8}", f"={P['min_uteis']}/I{r + 8}", fmt=DEC)
    celula(sim, f"K{r + 8}", "minutos por exame nesse ritmo, no plantão do meu estudo", NOTA, borda=False)
    q = T_MIN
    cabecalho(sim, q, "AIJ", ["pelos minutos: só os plantões necessários, com a agenda cheia", "meu estudo", "estudo do Sebastião"], 30)
    for col in "BCDEFGH":
        celula(sim, f"{col}{q}", None, fill=F_CAB)
    for i, (rot, fi, fj, fmt, fonte) in enumerate([
        ("Minutos úteis do plantão", f"={P['min_uteis']}", f"={P['min_seb']}", INT, PRETO),
        ("Plantões necessários (horas de sala usadas ÷ minutos úteis)", f"=ROUNDUP(R{SUB_US}*60/I{q + 1},0)",
         f"=ROUNDUP(S{SUB_US}*60/J{q + 1},0)", INT, PRETO),
        ("Produção média por plantão cheio (abaixo da garantia, nem a agenda cheia livra dela)",
         f"=IF(I{q + 2}=0,0,{prod}/I{q + 2})", f"=IF(J{q + 2}=0,0,{prod}/J{q + 2})", REAL, PRETO),
        ("Médico no período", f"=MAX({prod},{P['garantia']}*I{q + 2})", f"=MAX({prod},{P['garantia']}*J{q + 2})", REAL, NEGRITO),
    ]):
        celula(sim, f"A{q + 1 + i}", rot, fonte)
        celula(sim, f"I{q + 1 + i}", fi, fonte, fmt)
        celula(sim, f"J{q + 1 + i}", fj, fonte, fmt)

    # ---------- 4. Horas de sala
    r = R_SALA
    secao(sim, r, "4. Cabe nas salas de ultrassom?", cols)
    cabecalho(sim, r + 1, "AIJ", ["", "meu estudo", "estudo do Sebastião"], 30)
    for col in "BCDEFGH":
        celula(sim, f"{col}{r + 1}", None, fill=F_CAB)
    for i, (rot, fmt, fonte, f) in enumerate([
        ("Horas de sala de ultrassom usadas", INT, NEGRITO, lambda c, h, m: f"={h}{SUB_US}"),
        ("Horas de sala disponíveis no período (salas × dias úteis × meses × minutos úteis)", INT, PRETO,
         lambda c, h, m: f"={P['plantoes']}*{m}/60"),
        ("Uso das salas", PCT, NEGRITO, lambda c, h, m: f"=IF({c}{r + 3}=0,0,{c}{r + 2}/{c}{r + 3})"),
        ("Salas necessárias para estas quantidades", DEC, PRETO,
         lambda c, h, m: f"=IF({c}{r + 3}=0,0,{c}{r + 2}/({c}{r + 3}/{P['salas']}))"),
        ("Aviso", None, NEGRITO, lambda c, h, m: f'=IF({c}{r + 2}>{c}{r + 3},"NÃO CABE nas salas","cabe")'),
        ("Horas que faltam (negativo = folga)", INT, PRETO, lambda c, h, m: f"={c}{r + 2}-{c}{r + 3}"),
        ("Tomografia: horas de tomógrafo usadas (informativo)", INT, PRETO, lambda c, h, m: f"={h}{SUB_TC}"),
    ]):
        q = r + 2 + i
        celula(sim, f"A{q}", rot, fonte)
        for c, h, m in (("I", "R", P["min_uteis"]), ("J", "S", P["min_seb"])):
            celula(sim, f"{c}{q}", f(c, h, m), fonte, fmt)
            if rot == "Aviso":
                direita(f"{c}{q}")
    for c in "IJ":
        sim.conditional_formatting.add(f"{c}{r + 4}:{c}{r + 7}",
                                       FormulaRule(formula=[f"{c}${r + 2}>{c}${r + 3}"], font=vermelho, fill=F_ALERTA))
    nota(sim, r + 9, "Polo a polo, com as salas que faltam em cada um: aba Salas por polo. Estudo do Sebastião: 70 atendimentos de "
                     "ultrassom em 9 horas (aba Premissas, seção 6), o mesmo tempo para todo exame. Na tomografia, repeti os do meu estudo.")

    # ---------- 5. Contraste
    r = R_CONT
    secao(sim, r, "5. Tomografia: e se menos exames da fila com contraste forem feitos com contraste?", cols)
    cabecalho(sim, r + 1, "AHIJKLMNOPQR", [
        "cenário (troque as porcentagens em azul)", "feita com contraste", "feitos com contraste", "passam a sem contraste",
        "custo da tomografia", "margem da tomografia", "margem % da tomografia", "ganho contra 100%",
        "margem do conjunto, melhor", "margem do conjunto, pior", "horas de tomógrafo, meu estudo",
        "parte de toda a tomografia com contraste"], 56)
    for col in "BCDEFG":
        celula(sim, f"{col}{r + 1}", None, fill=F_CAB)
    D_, E_, G_ = (f"${c}${t1}:${c}${t2}" for c in "DEG")
    com = f'({D_}="{COM_C}")'
    q0 = r + 2
    for i, p in enumerate(("=$E$4", 1, 0.9, 0.8, 0.7, 0.6, 0.5)):
        q = q0 + i
        atual = i == 0
        fill = F_BOM if atual else None
        celula(sim, f"A{q}", "a escolhida no alto da aba" if atual else None, NEGRITO if atual else PRETO, fill=fill)
        celula(sim, f"H{q}", p, NEGRITO if atual else AZUL, '0%', fill, alinh="center")
        celula(sim, f"I{q}", f"=SUMPRODUCT(ROUND({com}*{E_}*$H{q},0))", fmt=INT, fill=fill)
        celula(sim, f"J{q}", f"=SUMPRODUCT({com}*{E_})-I{q}", fmt=INT, fill=fill)
        celula(sim, f"K{q}", f"=$E${SUB_TC}*{P['tc_sem']}+I{q}*{P['tc_adic']}", fmt=REAL, fill=fill)
        celula(sim, f"L{q}", f"=$I${SUB_TC}-K{q}", fmt=REAL, fill=fill)
        celula(sim, f"M{q}", f"=IF($I${SUB_TC}=0,0,L{q}/$I${SUB_TC})", fmt=PCT, fill=fill)
        celula(sim, f"N{q}", f"=L{q}-($I${SUB_TC}-$E${SUB_TC}*{P['tc_sem']}-SUMPRODUCT({com}*{E_})*{P['tc_adic']})", fmt=REAL, fill=fill)
        celula(sim, f"O{q}", f"=$I${SUB_US}-$K${SUB_US}+L{q}", fmt=REAL, fill=fill)
        celula(sim, f"P{q}", f"=$I${SUB_US}-$O${SUB_US}+L{q}", fmt=REAL, fill=fill)
        celula(sim, f"Q{q}", f"=(SUMPRODUCT(ROUND({com}*{E_}*$H{q},0)*({G_}-{P['tc_min_sem']}))+SUMPRODUCT({com}*{E_})*{P['tc_min_sem']}"
                             f"+SUMPRODUCT((1-{com})*{E_}*{G_}))/60", fmt=INT, fill=fill)
        celula(sim, f"R{q}", f"=IF($E${SUB_TC}=0,0,I{q}/$E${SUB_TC})", fmt=PCT, fill=fill)
    nota(sim, q0 + 7, "Cada exame que passa a sem contraste custa R$ 43 a menos na clínica e a Candanga paga o mesmo. A decisão de usar "
                      "ou não o contraste é do radiologista, exame a exame: a porcentagem é uma hipótese de quanto a readequação alcança.")

    r = q0 + 9
    for i, t in enumerate([
        "Limites da conta:",
        "- O fixo e, no pior cenário, o médico do ultrassom são rateados igualmente por exame, como o parceiro faz: um exame "
        "de 40 minutos pesa o mesmo que um de 15. O tempo de cada exame só aparece nas horas de sala e nas linhas 'pelos minutos'.",
        "- Por isso a margem de cada linha de ultrassom muda quando muda a quantidade de qualquer outra linha de ultrassom.",
        "- O fixo do ultrassom não cresce com as quantidades: se elas não couberem nas salas das Premissas, é preciso mais "
        "salas, e o fixo sobe (troque as salas na aba Premissas). Nesse caso o pior cenário fica otimista: o médico pelos "
        "minutos passa dele.",
        "- O custo real do ultrassom fica entre o melhor e o pior cenário, conforme quantos plantões a rede abrir.",
        "- Tomografia: R$ 175 e R$ 43 de contraste são o preço que o parceiro informou; garantias mínimas das clínicas e "
        "custo de agendamento não estão incluídos. Os minutos de tomógrafo não entram no custo.",
    ]):
        nota(sim, r + i, t)
    sim[f"A{r}"].font = NEGRITO

    sim.column_dimensions["A"].width = 62
    for col, w in zip(cols[1:], (11, 15, 14, 11, 13, 10, 11, 16, 13, 16, 16, 11, 13, 16, 16, 11, 12, 12, 11, 11, 52)):
        sim.column_dimensions[col].width = w
    sim.freeze_panes = f"B{CAB + 1}"

    # ============================================================ SALAS POR POLO
    partes = partes_por_polo()
    C_P = "CDEFGH"  # uma coluna por polo nas seções 2 e 3
    n = len(us)
    m1 = R_REDE + 6          # primeira linha da seção 2 (quem atende quem)
    q0 = m1 + 9              # topo da seção 3 (cenário real)
    p1 = q0 + 2 + len(POLOS) + 6   # primeira linha da seção 4 (partes)
    p2 = p1 + n - 1
    e1 = p2 + 5              # primeira linha da seção 5 (exames por Região)
    e2 = e1 + n - 1
    sp["A1"].value = "Salas de ultrassom por polo: onde a fila está e quantas salas cada polo precisa"
    sp["A1"].font = TITULO
    nota(sp, 2, "As quantidades e os minutos vêm da aba Simulador. A fila de cada exame é repartida pela Região de Saúde da unidade que "
                "pediu (Mapa Social, coleta de 02/11/2026). Azul = pode trocar: as salas de cada polo, quem atende quem e a parte de cada Região.")
    nota(sp, 3, "Salas da rede = rascunho de ofício do ISHP de 09/11/2026. A soma delas é o número de salas da aba Premissas: pôr uma "
                "sala aqui aumenta o fixo do ultrassom.")
    celula(sp, "A5", "Horas de uma sala no período, meu estudo")
    celula(sp, "C5", f"={P['dias']}*{P['meses']}*{P['pl_dia']}*{P['min_uteis']}/60", fmt=INT)
    celula(sp, "A6", "Horas de uma sala no período, estudo do Sebastião")
    celula(sp, "C6", f"={P['dias']}*{P['meses']}*{P['pl_dia']}*{P['min_seb']}/60", fmt=INT)

    E_S, G_S, H_S = (f"Simulador!${c}${u1}:${c}${u2}" for c in "EGH")
    TODAS = "ABCDEFGHIJKLMNO"

    def situacao(nec, tem):
        return (f'=IF({nec}>{tem},"faltam "&({nec}-{tem})&" sala(s)",IF({nec}<{tem},"sobram "&({tem}-{nec})&" sala(s)","justo"))')

    def quadro_polos(topo, titulo, fonte_de, salas, obs_rede):
        """Quadro de um cenário: uma linha por polo e a linha Rede. fonte_de(i, col) dá a fórmula de exames e de horas."""
        secao(sp, topo, titulo, TODAS)
        cabecalho(sp, topo + 1, TODAS, [
            "Polo", "Unidades no ofício", "Salas na rede", "Exames no período",
            "Horas de sala, meu estudo", "Salas necessárias, meu estudo", "Salas inteiras", "Uso das salas da rede",
            "Salas que faltam", "Situação, meu estudo",
            "Horas de sala, estudo do Sebastião", "Salas necessárias, estudo do Sebastião", "Salas inteiras", "Salas que faltam",
            "Situação, estudo do Sebastião"], 56)
        a = topo + 2
        for i, polo in enumerate(POLOS):
            r = a + i
            celula(sp, f"A{r}", polo, NEGRITO)
            celula(sp, f"B{r}", REDE[polo][0], NOTA, wrap=True)
            v = salas(i)
            celula(sp, f"C{r}", v, PRETO if isinstance(v, str) else AZUL, INT, alinh="center")
            celula(sp, f"D{r}", fonte_de(i, "D"), fmt=INT)
            celula(sp, f"E{r}", fonte_de(i, "E"), fmt=INT)
            celula(sp, f"F{r}", f"=IF($C$5=0,0,E{r}/$C$5)", fmt=DEC)
            celula(sp, f"G{r}", f"=ROUNDUP(ROUND(F{r},2),0)", NEGRITO, INT, alinh="center")
            celula(sp, f"H{r}", f'=IF(C{r}=0,"sem sala",E{r}/(C{r}*$C$5))', fmt=PCT, alinh="right")
            celula(sp, f"I{r}", f"=MAX(0,G{r}-C{r})", NEGRITO, INT, alinh="center")
            celula(sp, f"J{r}", situacao(f"G{r}", f"C{r}"), alinh="center")
            celula(sp, f"K{r}", fonte_de(i, "K"), fmt=INT)
            celula(sp, f"L{r}", f"=IF($C$6=0,0,K{r}/$C$6)", fmt=DEC)
            celula(sp, f"M{r}", f"=ROUNDUP(ROUND(L{r},2),0)", NEGRITO, INT, alinh="center")
            celula(sp, f"N{r}", f"=MAX(0,M{r}-C{r})", NEGRITO, INT, alinh="center")
            celula(sp, f"O{r}", situacao(f"M{r}", f"C{r}"), alinh="center")
        r = a + len(POLOS)
        celula(sp, f"A{r}", "Rede", NEGRITO, fill=F_TOTAL)
        celula(sp, f"B{r}", obs_rede, NOTA, fill=F_TOTAL, wrap=True)
        for col in "CDEFGIKLMN":
            celula(sp, f"{col}{r}", f"=SUM({col}{a}:{col}{r - 1})", NEGRITO, DEC if col in "FL" else INT, F_TOTAL,
                   alinh="center" if col in "CGIMN" else None)
        celula(sp, f"H{r}", f"=IF(C{r}=0,0,E{r}/(C{r}*$C$5))", NEGRITO, PCT, F_TOTAL)
        celula(sp, f"J{r}", f'=IF(I{r}>0,"faltam "&I{r}&" sala(s) nos polos","cabe em todos os polos")', NEGRITO, fill=F_TOTAL, alinh="center")
        celula(sp, f"O{r}", f'=IF(N{r}>0,"faltam "&N{r}&" sala(s) nos polos","cabe em todos os polos")', NEGRITO, fill=F_TOTAL, alinh="center")
        for col in "IJNO":
            sp.conditional_formatting.add(f"{col}{a}:{col}{r}", FormulaRule(
                formula=[f"${'I' if col in 'IJ' else 'N'}{a}>0"], font=vermelho, fill=F_ALERTA))
        return r

    # ---------- 1. cenário ideal
    def ideal(i, col):
        c = C_P[i]
        if col == "D":
            return f"=SUM({c}{e1}:{c}{e2})"
        return f"=SUMPRODUCT({E_S},{G_S if col == 'E' else H_S},${c}${p1}:${c}${p2})/60"

    r = quadro_polos(8, "1. Cenário ideal: cada polo atende só a fila da própria Região", ideal, lambda i: REDE[POLOS[i]][1],
                     "salas inteiras e salas que faltam: soma dos polos")
    assert r == R_REDE
    nota(sp, r + 1, "Salas necessárias = horas de sala ÷ horas de uma sala no período, com a agenda cheia: sem faltas, sem aparelho parado "
                    "e sem rampa de início. Salas inteiras arredonda para cima, polo a polo: por isso a soma dos polos passa da conta da rede.")
    nota(sp, r + 2, "Aqui nenhum paciente sai da própria Região: a sala vaga de um polo não ajuda o polo vizinho.")

    # ---------- 2. quem atende quem
    secao(sp, m1 - 2, "2. Quem atende quem: para qual polo vai a fila de cada Região (troque em azul)", TODAS)
    cabecalho(sp, m1 - 1, "ABCDEFGHI", ["Região de onde vem a fila", "Horas de sala que a Região gera, meu estudo",
                                        *[f"vai ao polo {p}" for p in POLOS], "Soma"], 44)
    for i, polo in enumerate(POLOS):
        r = m1 + i
        celula(sp, f"A{r}", polo, NEGRITO)
        celula(sp, f"B{r}", f"=E{10 + i}", fmt=INT)
        for k, c in enumerate(C_P):
            celula(sp, f"{c}{r}", ROTA.get(polo, {polo: 1}).get(POLOS[k], 0), AZUL, '0%', alinh="center")
        celula(sp, f"I{r}", f"=SUM(C{r}:H{r})", fmt='0%', alinh="center")
    sp.conditional_formatting.add(f"I{m1}:I{m1 + 5}", FormulaRule(formula=[f"ABS(I{m1}-1)>0.001"], font=vermelho, fill=F_ALERTA))
    sp.conditional_formatting.add(f"C{m1}:H{m1 + 5}", CellIsRule(operator="greaterThan", formula=["0"], fill=F_BOM))
    nota(sp, m1 + 6, "Cada linha tem de somar 100%. A partida é hipótese minha, para trocar: a Sudoeste manda 75% a Ceilândia (polo Oeste, "
                     "onde sobram salas) e a Leste, que não tem unidade no ofício, se divide entre Sobradinho (Norte) e Guará II (Central).")

    # ---------- 3. cenário real
    def real(i, col):
        c = C_P[i]
        return f"=SUMPRODUCT(${col}$10:${col}${R_REDE - 1},${c}${m1}:${c}${m1 + 5})"

    r = quadro_polos(q0, "3. Cenário real: cada polo atende a fila que a seção 2 manda para ele", real, lambda i: f"=C{10 + i}",
                     "as salas vêm da seção 1")
    nota(sp, r + 1, "Para fechar: mude a seção 2 (quem atende quem) ou as salas na seção 1, até não faltar sala em nenhum polo. "
                    "O que a planilha não mede: distância, transporte e se a regulação aceita mandar o paciente a outra Região.")

    secao(sp, p1 - 2, "4. De onde vem a fila de cada exame: parte de cada Região", "ABCDEFGHIJKLMNO")
    cabecalho(sp, p1 - 1, "ABCDEFGHIJ", ["Exame", "Quantidade (aba Simulador)", *POLOS, "Soma", "Origem da parte"], 44)
    secao(sp, e1 - 2, "5. Exames por Região de origem (quantidade × parte)", "ABCDEFGHIJKLMNO")
    cabecalho(sp, e1 - 1, "ABCDEFGHI", ["Exame", "Minutos, meu estudo", *POLOS, "Soma"], 44)
    for i, e in enumerate(us):
        a, b = p1 + i, e1 + i
        chave = ORIGEM.get(e[0])
        celula(sp, f"A{a}", f"=Simulador!A{u1 + i}")
        celula(sp, f"B{a}", f"=Simulador!E{u1 + i}", fmt=INT)
        for c, v in zip(C_P, partes[chave]):
            celula(sp, f"{c}{a}", v, AZUL, PCT)
            celula(sp, f"{c}{b}", f"=$B{a}*{c}{a}", fmt=INT)
        celula(sp, f"I{a}", f"=SUM(C{a}:H{a})", fmt=PCT)
        celula(sp, f"J{a}", "coleta de Região de 02/11" if chave else "sem coleta de Região: média dos outros exames de ultrassom", NOTA)
        celula(sp, f"A{b}", f"=Simulador!A{u1 + i}")
        celula(sp, f"B{b}", f"=Simulador!G{u1 + i}", fmt=INT, alinh="center")
        celula(sp, f"I{b}", f"=SUM(C{b}:H{b})", fmt=INT)
    sp.conditional_formatting.add(f"I{p1}:I{p2}", FormulaRule(formula=[f"ABS(I{p1}-1)>0.001"], font=vermelho, fill=F_ALERTA))
    nota(sp, p2 + 1, "Pedidos sem Região (URD, contratado e sem registro) se repartem na mesma proporção. Os exames novos seguem a parte "
                     "da fila de hoje. A soma de cada linha tem de dar 100%.")
    celula(sp, f"A{e2 + 1}", "Total", NEGRITO, fill=F_TOTAL)
    celula(sp, f"B{e2 + 1}", None, fill=F_TOTAL)
    for c in C_P + "I":
        celula(sp, f"{c}{e2 + 1}", f"=SUM({c}{e1}:{c}{e2})", NEGRITO, INT, F_TOTAL)

    sp.column_dimensions["A"].width = 48
    sp.column_dimensions["B"].width = 34
    for col, w in zip("CDEFGHIJKLMNO", (11, 12, 12, 13, 11, 13, 11, 20, 13, 13, 11, 11, 20)):
        sp.column_dimensions[col].width = w
    sp.freeze_panes = "B10"

    for ws in (sim, sp, pr):
        ws.sheet_view.showGridLines = False
    wb.save(saida)
    return saida


if __name__ == "__main__":
    print(gerar())
