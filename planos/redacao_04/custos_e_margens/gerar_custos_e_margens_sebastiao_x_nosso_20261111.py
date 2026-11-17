"""Compara a conta do parceiro (planilha_custos_sebastião.xlsx, ofício de 09/11/2026) com a nossa.

Gera custos_e_margens_sebastiao_x_nosso_20261111.xlsx, com duas abas:
  Comparativo - quantidades, valores unitários e o custo dos mesmos exames pelas duas contas,
                na base dele (54.589 ultrassons, 11 salas) e na nossa (carteira v3, 14 salas).
  Pessoas     - quantas pessoas cada conta põe por sala e por unidade, e o total na rede.

Tudo é fórmula: azul = premissa que pode ser trocada. Controle interno.
Fontes do lado "nosso": roteiro_reuniao_20261110.md (seção 4), estudo_tempos_tomografia_3_polos_20261109.md
(seção 7), estudo_12_meses_3_tomografos_20261107.md e carteira_final_v3_20261111.xlsx.
"""
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

SAIDA = Path(__file__).with_name("custos_e_margens_sebastiao_x_nosso_20261111.xlsx")

FONTE = "Arial"
AZUL = Font(name=FONTE, size=10, color="0000FF")
PRETO = Font(name=FONTE, size=10)
NEGRITO = Font(name=FONTE, size=10, bold=True)
TITULO = Font(name=FONTE, size=14, bold=True)
SECAO = Font(name=FONTE, size=11, bold=True, color="FFFFFF")
NOTA = Font(name=FONTE, size=9, italic=True, color="555555")
F_SECAO = PatternFill("solid", fgColor="1F4E78")
F_CAB = PatternFill("solid", fgColor="D9E1F2")
F_TOTAL = PatternFill("solid", fgColor="F2F2F2")
F_ALERTA = PatternFill("solid", fgColor="FCE4D6")
FINA = Side(style="thin", color="BFBFBF")
BORDA = Border(left=FINA, right=FINA, top=FINA, bottom=FINA)

REAL = 'R$ #,##0.00'
INT = '#,##0'
DEC = '#,##0.0'
PCT = '0.0%'


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


def secao(ws, linha, texto, cols="ABCDE"):
    for col in cols:
        ws[f"{col}{linha}"].fill = F_SECAO
    ws[f"A{linha}"].value = texto
    ws[f"A{linha}"].font = SECAO


def cabecalho(ws, linha, textos):
    for col, t in zip("ABCDEFGH", textos):
        celula(ws, f"{col}{linha}", t, NEGRITO, fill=F_CAB, wrap=True, alinh="center")
    ws.row_dimensions[linha].height = 32


def nota(ws, linha, texto):
    ws[f"A{linha}"].value = texto
    ws[f"A{linha}"].font = NOTA


wb = Workbook()
ws = wb.active
ws.title = "Comparativo"
pe = wb.create_sheet("Pessoas")

ws["A1"].value = "Conta do Sebastião (ofício do parceiro) ao lado da nossa"
ws["A1"].font = TITULO
nota(ws, 2, "Sebastião = rascunho de ofício do ISHP de 09/11/2026, como está em planilha_custos_sebastião.xlsx. "
            "Nosso = estudos de 07/11 a 11/11 (roteiro da reunião, estudo de tempos e carteira v3).")
nota(ws, 3, "Azul = premissa que pode ser trocada; preto = fórmula. Faixa laranja = onde as contas mais se afastam. "
            "Controle interno: não vai à SES nem ao parceiro.")

R = {}          # chave -> linha
linha_atual = [5]


def lin(chave, rotulo, s, n, fmt, obs="", dif=True, alerta=False, total=False):
    """Uma linha: rótulo, Sebastião, nosso, diferença (nosso menos Sebastião) e observação."""
    r = linha_atual[0]
    R[chave] = r
    fill = F_ALERTA if alerta else (F_TOTAL if total else None)
    celula(ws, f"A{r}", rotulo, NEGRITO if total else PRETO, fill=fill, wrap=True)
    for col, v in (("B", s), ("C", n)):
        formula = isinstance(v, str) and v.startswith("=")
        texto = isinstance(v, str) and not formula
        celula(ws, f"{col}{r}", v, NEGRITO if total else (PRETO if formula or texto else AZUL),
               None if texto else fmt, fill, wrap=texto, alinh="right" if texto else None)
    numerico = not any(isinstance(v, str) and not v.startswith("=") for v in (s, n))
    celula(ws, f"D{r}", f"=C{r}-B{r}" if dif and numerico else "", NEGRITO if total else PRETO, fmt, fill)
    celula(ws, f"E{r}", obs, NOTA, fill=fill, wrap=True)
    linha_atual[0] += 1
    return r


def abre(titulo, cab=("item", "Sebastião", "nosso", "diferença (nosso − Sebastião)", "observação")):
    r = linha_atual[0] + 1
    secao(ws, r, titulo)
    cabecalho(ws, r + 1, cab)
    linha_atual[0] = r + 2


# ------------------------------------------------------------ 1. quantidades
abre("1. Quantidades: o que cada conta atende, e com quê")
lin("meses", "Meses de execução", 12, 12, INT, "ofício: 10/12/2026 a 09/12/2027. Nosso: estudo de 07/11 (o plano assinado tem 8)")
lin("dias", "Dias úteis por mês", 21, 21, INT, "252 no ano, sem descontar feriados, nas duas contas")
lin("us_sem", "Ultrassons sem Doppler", 40942, 57997, INT, "Sebastião: mistura de simulação, não extração da fila. Nosso: carteira v3 de 11/11")
lin("us_com", "Ultrassons com Doppler", 13647, 17986, INT, "nosso: 12.034 de membros (os dois lados, condição D-011) e 5.952 de carótidas e outros vasos")
lin("us", "Ultrassons no total", f"=B{R['us_sem']}+B{R['us_com']}", f"=C{R['us_sem']}+C{R['us_com']}", INT,
    "a carteira 1 de 02/11 tinha 65.132", total=True)
lin("tc_com", "Tomografias com contraste", "=ROUND(13622*0.93,0)", 10579, INT,
    "Sebastião: 93% de 13.622, projeção da coordenação. Nosso: como a fila pede (carteira v3)")
lin("tc_sem", "Tomografias sem contraste", f"=13622-B{R['tc_com']}", 348, INT)
lin("tc", "Tomografias no total", f"=B{R['tc_com']}+B{R['tc_sem']}", f"=C{R['tc_com']}+C{R['tc_sem']}", INT,
    "a carteira 1 tinha 14.401; a v3 trocou tomografia por ultrassom", total=True)
lin("ex", "Exames no total", f"=B{R['us']}+B{R['tc']}", f"=C{R['us']}+C{R['tc']}", INT, total=True)
lin("salas", "Salas de ultrassom", 11, 14, INT, "nosso: carteira v3, com 96% de uso em 12 meses", alerta=True)
lin("unid", "Unidades de ultrassom", 6, 6, INT,
    "Sebastião: 6 clínicas, duas em Ceilândia e nenhuma na Região Leste. Nosso: 6 polos, um por Região")
lin("unid_tc", "Unidades de tomografia", "5 (4 com tomógrafo)", "3 a 5, em estudo", None,
    "a Carneiro de Mendonça não tem tomógrafo (informação do usuário, 10/11)")
lin("h_dia", "Horas de exame por sala por dia", 9, 8, DEC,
    "Sebastião: plantão de 10 h com 1 h de almoço. Nosso: sala aberta 10 h, com 80% das horas em exame")
lin("min", "Minutos de sala por ultrassom, em média", "=9*60/70", "=27031*60/C" + str(R["us"]), DEC,
    "Sebastião: 70 atendimentos em 9 h, o mesmo tempo para todo exame (o ofício usa 20 min como sensibilidade). "
    "Nosso: agenda do CBR, de 15 a 40 min conforme o exame (27.031 h na carteira v3)", alerta=True)
lin("h_nec", "Horas de sala que os exames pedem", f"=B{R['us']}*B{R['min']}/60", f"=C{R['us']}*C{R['min']}/60", INT)
lin("h_disp", "Horas de sala disponíveis no período",
    f"=B{R['salas']}*B{R['dias']}*B{R['meses']}*B{R['h_dia']}", f"=C{R['salas']}*C{R['dias']}*C{R['meses']}*C{R['h_dia']}", INT)
lin("uso", "Uso das salas", f"=B{R['h_nec']}/B{R['h_disp']}", f"=C{R['h_nec']}/C{R['h_disp']}", PCT,
    "pelo tempo de cada um. A linha de baixo cruza os tempos")
lin("uso_x", "Uso das salas dele pelos nossos minutos, e das nossas pelos dele",
    f"=B{R['us']}*C{R['min']}/60/B{R['h_disp']}", f"=C{R['us']}*B{R['min']}/60/C{R['h_disp']}", PCT,
    "a diferença de salas vem toda do tempo por exame", dif=False)
lin("ex_sala", "Ultrassons por sala por dia útil", f"=B{R['us']}/(B{R['salas']}*B{R['dias']}*B{R['meses']})",
    f"=C{R['us']}/(C{R['salas']}*C{R['dias']}*C{R['meses']})", DEC)

# ------------------------------------------------------------ 2. valores unitários
abre("2. Valores unitários")
lin("med_sem", "Médico por ultrassom sem Doppler", 35, 33.33, REAL, "nosso: modelo do ISHP, R$ 1.000 por lote de 30 exames")
lin("med_com", "Médico por ultrassom com Doppler", 40, 33.33, REAL)
lin("garantia", "Garantia mínima do médico por plantão", 1500, 0, REAL,
    "o médico recebe o maior entre a produção do plantão e a garantia. Nós não temos garantia", alerta=True)
lin("med_hora", "Médico por hora de exame", f"=B{R['garantia']}/B{R['h_dia']}", 100, REAL,
    "Sebastião: a garantia do plantão dividida pelas horas úteis (R$ 150 por hora do plantão de 10 h). "
    "Nosso: alternativa ao pagamento por exame. A seleção do IgesDF paga R$ 174,30", alerta=True)
lin("aux", "Auxiliar de sala, custo do posto por mês", 3180, 2959, REAL,
    "Sebastião: posto com provisões. Nosso: R$ 5.918 por sala para 2 auxiliares")
lin("n_aux", "Auxiliares por sala", 1, 2, INT, "com 1 por sala não há cobertura de almoço nem de falta nas 10 h", alerta=True)
lin("rec", "Recepção, custo do posto por mês", 3500, 2959, REAL,
    "nosso: salário de recepcionista de consultório em Brasília, R$ 1.740,78 (salario.com.br, CBO 4221-10), × 1,7 de encargos e benefícios (estudo de 20/10)")
lin("n_rec", "Postos de recepção por unidade", 1, 2, INT, "", alerta=True)
lin("sala", "Aluguel da sala por mês", 1500, 3000, REAL, "Sebastião: alvo de negociação, não é cotação aceita", alerta=True)
lin("apar", "Aluguel do aparelho de ultrassom por mês", 2500, 2500, REAL)
lin("mat", "Materiais por exame", "=177414/54589", 7, REAL,
    "nosso: R$ 7 ouvidos em reunião de 11/11 (relato do usuário); antes usávamos R$ 3, hipótese. Nenhum dos dois tem cotação", alerta=True)
lin("limp", "Limpeza e resíduos: valor por mês para a rede toda", 2400, 0, REAL, "Sebastião: verba única para a rede")
lin("limp_s", "Limpeza e resíduos: valor por sala por mês", 0, 400, REAL,
    "nosso: R$ 400 por sala (estudo de 07/11, com energia, internet e água se o aluguel não incluir). É o mesmo serviço (usuário, 11/11)")
lin("limp_11", "Limpeza e resíduos por mês, nas 11 salas dele", f"=B{R['limp']}+B{R['limp_s']}*$B${R['salas']}",
    f"=C{R['limp']}+C{R['limp_s']}*$B${R['salas']}", REAL, "o mesmo serviço: R$ 2.400 contra R$ 4.400", alerta=True)
lin("sist", "Sistemas e comunicação, a rede toda, por mês", 1500, 1500, REAL, "nosso: copiado do ofício (usuário, 11/11); não sabemos se cobre o sistema de imagem")
lin("logi", "Logística e contingência, a rede toda, por mês", 2600, 2600, REAL, "o ofício não detalha. Nosso: copiado do ofício (usuário, 11/11)")
lin("gest", "Gestão e coordenação dentro do exame, por mês", 3500, 0, REAL,
    "nosso: a gestão é a rubrica de apoio (R$ 956.160 no total, valor fixo). Dentro do exame e na rubrica pode ser lida como pagamento em dobro")
lin("fisc", "Reserva fiscal por exame", 5.994, 5.994, REAL,
    "hipótese do ofício, não é alíquota validada. Nosso: copiado do ofício (usuário, 11/11), até alguém explicar que tributo é")
lin("tc_s", "Tomografia na clínica, sem contraste", 175, 175, REAL)
lin("tc_ad", "Adicional do contraste", 43, 43, REAL, "nosso: igual ao do ofício (usuário, 11/11); em 09/11 a referência era R$ 50")
lin("tc_c", "Tomografia na clínica, com contraste", f"=B{R['tc_s']}+B{R['tc_ad']}", f"=C{R['tc_s']}+C{R['tc_ad']}", REAL,
    "a Candanga paga R$ 309,25 na maior parte")
nota(ws, linha_atual[0], "Sem preço nas duas contas: responsável técnico do polo, médico de retaguarda e sistema de imagem (PACS).")
linha_atual[0] += 1


# ------------------------------------------------------------ 3 e 4. o custo dos mesmos exames
def bloco(titulo, q, prefixo):
    """q = coluna de onde vêm as quantidades (B = base dele, C = a nossa). Os preços: B dele, C nossos."""
    abre(titulo, ("item", "pela conta do Sebastião", "pela nossa conta", "diferença (nossa − Sebastião)", "observação"))
    g = lambda k: f"${q}${R[k]}"           # quantidade da base
    k_ = lambda nome: prefixo + nome
    meses, salas, unid, us = g("meses"), g("salas"), g("unid"), g("us")

    def custo(chave, rotulo, f, obs="", **kw):
        """f(p) devolve a fórmula com os preços da coluna p."""
        return lin(k_(chave), rotulo, "=" + f("B"), "=" + f("C"), REAL, obs, **kw)

    p = lambda col, k: f"${col}${R[k]}"
    custo("med", "Médico, só pela produção",
          lambda c: f"{g('us_sem')}*{p(c,'med_sem')}+{g('us_com')}*{p(c,'med_com')}")
    custo("gar", "O que a garantia acrescenta, com todas as salas abertas todo dia útil",
          lambda c: f"IF({p(c,'garantia')}=0,0,MAX(0,{salas}*{g('dias')}*{meses}*{p(c,'garantia')}"
                    f"-({g('us_sem')}*{p(c,'med_sem')}+{g('us_com')}*{p(c,'med_com')})))",
          "pior cenário: um plantão por sala por dia útil, pago pelo mínimo quando a produção média fica abaixo", alerta=True)
    custo("aux", "Auxiliares de sala", lambda c: f"{salas}*{p(c,'n_aux')}*{p(c,'aux')}*{meses}")
    custo("rec", "Recepção", lambda c: f"{unid}*{p(c,'n_rec')}*{p(c,'rec')}*{meses}")
    custo("sala", "Aluguel das salas", lambda c: f"{salas}*{p(c,'sala')}*{meses}")
    custo("apar", "Aluguel dos aparelhos", lambda c: f"{salas}*{p(c,'apar')}*{meses}")
    custo("mat", "Materiais", lambda c: f"{us}*{p(c,'mat')}")
    custo("limp", "Limpeza e resíduos", lambda c: f"({p(c,'limp')}+{p(c,'limp_s')}*{salas})*{meses}")
    custo("rede", "Sistemas e logística da rede", lambda c: f"({p(c,'sist')}+{p(c,'logi')})*{meses}")
    custo("gest", "Gestão e coordenação dentro do exame", lambda c: f"{p(c,'gest')}*{meses}")
    custo("fisc", "Reserva fiscal", lambda c: f"{us}*{p(c,'fisc')}")
    ini, fim = R[k_("aux")], R[k_("fisc")]
    lin(k_("nmed"), "Ultrassom: tudo menos o médico", f"=SUM(B{ini}:B{fim})", f"=SUM(C{ini}:C{fim})", REAL, total=True)
    lin(k_("nmed_ex"), "  por exame", f"=B{R[k_('nmed')]}/{us}", f"=C{R[k_('nmed')]}/{us}", REAL)
    lin(k_("us_a"), "ULTRASSOM, melhor cenário (sem a garantia)", f"=B{R[k_('med')]}+B{R[k_('nmed')]}",
        f"=C{R[k_('med')]}+C{R[k_('nmed')]}", REAL, total=True)
    lin(k_("us_a_ex"), "  por exame", f"=B{R[k_('us_a')]}/{us}", f"=C{R[k_('us_a')]}/{us}", REAL)
    lin(k_("us_b"), "ULTRASSOM, pior cenário (com a garantia)", f"=B{R[k_('us_a')]}+B{R[k_('gar')]}",
        f"=C{R[k_('us_a')]}+C{R[k_('gar')]}", REAL, "na nossa conta não há garantia: é igual ao melhor", total=True)
    lin(k_("us_b_ex"), "  por exame", f"=B{R[k_('us_b')]}/{us}", f"=C{R[k_('us_b')]}/{us}", REAL)
    custo("tc", "TOMOGRAFIA, paga à clínica",
          lambda c: f"{g('tc_com')}*{p(c,'tc_c')}+{g('tc_sem')}*{p(c,'tc_s')}", total=True)
    lin(k_("tc_ex"), "  por exame", f"=B{R[k_('tc')]}/{g('tc')}", f"=C{R[k_('tc')]}/{g('tc')}", REAL)
    lin(k_("tot_a"), "CONJUNTO, melhor cenário", f"=B{R[k_('us_a')]}+B{R[k_('tc')]}", f"=C{R[k_('us_a')]}+C{R[k_('tc')]}",
        REAL, total=True)
    lin(k_("tot_b"), "CONJUNTO, pior cenário", f"=B{R[k_('us_b')]}+B{R[k_('tc')]}", f"=C{R[k_('us_b')]}+C{R[k_('tc')]}",
        REAL, total=True)


bloco("3. Os exames e a rede do Sebastião (coluna B da seção 1), pelas duas contas", "B", "a_")
nota(ws, linha_atual[0], "Mesmos exames, mesmas salas e mesmas unidades; muda só o preço e quantas pessoas cada conta põe.")
linha_atual[0] += 1
bloco("4. Os nossos exames e a nossa rede (coluna C da seção 1), pelas duas contas", "C", "b_")
nota(ws, linha_atual[0], "Para comparar: o valor dos exames a fechar é R$ 10.636.602 (recurso menos o custo acessório de R$ 956.160, que é valor fixo).")
linha_atual[0] += 1
nota(ws, linha_atual[0], "A nossa conta não tem preço para responsável técnico, médico de retaguarda e sistema de imagem; a dele também não.")
linha_atual[0] += 1

# ------------------------------------------------------------ 5. valor final por exame
abre("5. Valor final por exame: quanto custa fazer cada tipo",
     ("exame", "pela conta do Sebastião", "pela nossa conta", "diferença (nossa − Sebastião)", "observação"))


def finais(rotulo, q, prefixo):
    r = linha_atual[0]
    celula(ws, f"A{r}", rotulo, NEGRITO, fill=F_CAB)
    for col in "BCDE":
        celula(ws, f"{col}{r}", "", fill=F_CAB)
    linha_atual[0] += 1
    nm = R[prefixo + "nmed_ex"]
    us = f"${q}${R['us']}"
    med = lambda c: f"({c}{R[prefixo + 'med']}+{c}{R[prefixo + 'gar']})/{us}"
    lin(prefixo + "f_us", "Ultrassom sem Doppler", f"=B{R['med_sem']}+B{nm}", f"=C{R['med_sem']}+C{nm}", REAL,
        "honorário do médico mais o rateio igual de tudo o que não é médico", total=True)
    lin(prefixo + "f_dop", "Ultrassom com Doppler", f"=B{R['med_com']}+B{nm}", f"=C{R['med_com']}+C{nm}", REAL,
        "na nossa conta o médico recebe o mesmo com e sem Doppler", total=True)
    lin(prefixo + "f_gar", "Ultrassom, com ou sem Doppler, se a garantia for cobrada em todo plantão",
        f"={med('B')}+B{nm}", f"={med('C')}+C{nm}", REAL,
        "pior cenário: o plantão é pago pelo mínimo, e o médico por exame fica igual nos dois tipos. Na nossa conta "
        "é a média dos dois, porque não há garantia", alerta=True)
    lin(prefixo + "f_tcs", "Tomografia sem contraste", f"=B{R['tc_s']}", f"=C{R['tc_s']}", REAL,
        "preço pago à clínica; não muda com a rede", total=True)
    lin(prefixo + "f_tcc", "Tomografia com contraste", f"=B{R['tc_c']}", f"=C{R['tc_c']}", REAL,
        "preço pago à clínica, com o adicional do contraste", total=True)


finais("Nos exames e na rede do Sebastião (54.589 ultrassons, 11 salas)", "B", "a_")
finais("Nos nossos exames e na nossa rede (carteira v3, 14 salas)", "C", "b_")
nota(ws, linha_atual[0], "O ultrassom muda de uma rede para a outra porque o custo fixo (salas, auxiliares, recepção) é dividido por mais ou menos exames.")
linha_atual[0] += 1
nota(ws, linha_atual[0], "Para comparar, a Candanga paga: ultrassom sem Doppler de R$ 64,07 a R$ 117,51; Doppler R$ 115,61; tomografia R$ 309,25 (crânio R$ 251,29).")

ws.column_dimensions["A"].width = 58
for col in "BCD":
    ws.column_dimensions[col].width = 21
ws.column_dimensions["E"].width = 90
ws.freeze_panes = "B5"

# ============================================================ PESSOAS
pe["A1"].value = "Quantas pessoas cada conta põe"
pe["A1"].font = TITULO
nota(pe, 2, "Sebastião: o ofício dá postos, e não pessoas; médico = um plantão por sala por dia útil. "
            "Nosso: estudo de tempos de 09/11, seção 7 (sala aberta 10 h por dia útil; não conta férias nem faltas).")
nota(pe, 3, "Azul = premissa que pode ser trocada; preto = fórmula. Salas e unidades vêm da aba Comparativo.")
secao(pe, 5, "1. Ultrassom: quem está na conta do exame", "ABCDEFG")
cabecalho(pe, 6, ["função", "Sebastião: por sala ou unidade", "Sebastião: pessoas na rede dele",
                  "nosso: por sala ou polo", "nosso: pessoas na nossa rede", "nosso critério na rede dele", "observação"])
SB, SC = f"Comparativo!$B${R['salas']}", f"Comparativo!$C${R['salas']}"
UB, UC = f"Comparativo!$B${R['unid']}", f"Comparativo!$C${R['unid']}"
funcoes = [
    ("Médico ultrassonografista, por sala", 1, 2, "s",
     "Sebastião: 1 plantão de 10 h por sala. Nosso: 2 por sala (1.800 h por ano cada, ou dois turnos de 5 h)"),
    ("Auxiliar de sala, por sala", f"=Comparativo!B{R['n_aux']}", f"=Comparativo!C{R['n_aux']}", "s",
     "nosso: fica com o médico o exame todo e digita o laudo; 2 para cobrir as 10 h"),
    ("Recepção, por unidade", f"=Comparativo!B{R['n_rec']}", f"=Comparativo!C{R['n_rec']}", "u",
     "nosso: recepção e preparo; 2 para cobrir as 10 h"),
]
for i, (nome, s, n, por, obs) in enumerate(funcoes):
    r = 7 + i
    qb, qc = (SB, SC) if por == "s" else (UB, UC)
    celula(pe, f"A{r}", nome)
    celula(pe, f"B{r}", s, PRETO if isinstance(s, str) else AZUL, INT)
    celula(pe, f"C{r}", f"=B{r}*{qb}", fmt=INT)
    celula(pe, f"D{r}", n, PRETO if isinstance(n, str) else AZUL, INT)
    celula(pe, f"E{r}", f"=D{r}*{qc}", fmt=INT)
    celula(pe, f"F{r}", f"=D{r}*{qb}", fmt=INT)
    celula(pe, f"G{r}", obs, NOTA, wrap=True)
r = 10
celula(pe, f"A{r}", "Pessoas no ultrassom", NEGRITO, fill=F_TOTAL)
celula(pe, f"B{r}", "", fill=F_TOTAL)
celula(pe, f"C{r}", "=SUM(C7:C9)", NEGRITO, INT, F_TOTAL)
celula(pe, f"D{r}", "", fill=F_TOTAL)
celula(pe, f"E{r}", "=SUM(E7:E9)", NEGRITO, INT, F_TOTAL)
celula(pe, f"F{r}", "=SUM(F7:F9)", NEGRITO, INT, F_TOTAL)
celula(pe, f"G{r}", "a diferença na mesma rede (coluna F menos C) é só o critério de cobertura das 10 h", NOTA, fill=F_TOTAL, wrap=True)
celula(pe, "A11", "  das quais, auxiliares e recepção (pagos por mês)")
celula(pe, "B11", "")
celula(pe, "C11", "=C8+C9", fmt=INT)
celula(pe, "D11", "")
celula(pe, "E11", "=E8+E9", fmt=INT)
celula(pe, "F11", "=F8+F9", fmt=INT)
celula(pe, "G11", "", NOTA)

secao(pe, 13, "2. O que fica fora da conta do exame, ou não tem preço", "ABCDEFG")
cabecalho(pe, 14, ["função", "Sebastião", "", "nosso", "", "", "observação"])
fora = [
    ("Enfermagem do ultrassom", "não tem", "1 para cada 2 salas (7 em 14 salas)", "estimativa nossa, sem preço na conta"),
    ("Responsável técnico do polo", "não tem", "1 por polo, sem preço", "falta nas duas contas"),
    ("Médico de retaguarda", "não tem", "1 por dia útil por polo, sem preço", "previsto no plano assinado (4.15)"),
    ("Gestão e apoio", "verba de R$ 3.500 por mês, sem pessoas",
     "22 postos e assessoria no plano assinado (8 meses); 16 postos e assessoria no quadro P2 (12 meses)",
     "nosso: rubrica de apoio, R$ 956.160 no total (valor fixo); a P2 de 07/11 dava R$ 978.120"),
    ("Tomografia: equipe do exame", "da clínica, dentro dos R$ 175 + R$ 43", "da clínica, dentro dos R$ 175 + R$ 43",
     "referência nossa do que a clínica precisa por tomógrafo em 10 h: 3 técnicos em radiologia, 2 de enfermagem "
     "(3 com a punção antes), 1 radiologista no contraste e 2 de recepção: 8 ou 9 pessoas; 11 com dois turnos de 5 h"),
    ("Tomografia: agenda, lançamento e gestão", "o ofício não traz", "na rubrica de apoio", ""),
]
for i, (nome, s, n, obs) in enumerate(fora):
    r = 15 + i
    celula(pe, f"A{r}", nome, wrap=True)
    pe.merge_cells(f"B{r}:C{r}")
    pe.merge_cells(f"D{r}:F{r}")
    celula(pe, f"B{r}", s, wrap=True)
    celula(pe, f"D{r}", n, wrap=True)
    celula(pe, f"G{r}", obs, NOTA, wrap=True)
    pe.row_dimensions[r].height = 42
nota(pe, 22, "O ofício não diz quantos médicos cumprem os plantões: 11 é o mínimo, com um médico por sala todo dia útil.")

pe.column_dimensions["A"].width = 46
for col in "BCDEF":
    pe.column_dimensions[col].width = 19
pe.column_dimensions["G"].width = 80
pe.freeze_panes = "B7"

# ============================================================ VOLUME
vo = wb.create_sheet("Volume")
vo["A1"].value = "Como o volume de ultrassons muda o custo por exame"
vo["A1"].font = TITULO
nota(vo, 2, "O custo fixo (salas, aparelhos, auxiliares, recepção e verbas da rede) é dividido pelos exames: mais exames, menos fixo em cada um. "
            "Preços e quantas pessoas por sala vêm da aba Comparativo.")
nota(vo, 3, "Azul = pode trocar (volumes, salas, parte com Doppler, uso máximo). Laranja = não cabe nas salas. Controle interno.")
CB = lambda k: f"Comparativo!$B${R[k]}"
CC = lambda k: f"Comparativo!$C${R[k]}"
CMP = {"B": CB, "C": CC}

secao(vo, 5, "Premissas", "ABCDEFGHIJK")
prem = [
    (6, "Salas de ultrassom na rede do Sebastião", f"={CB('salas')}", INT, "aba Comparativo; troque aqui para testar"),
    (7, "Salas de ultrassom na nossa rede", f"={CC('salas')}", INT, ""),
    (8, "Parte dos ultrassons com Doppler", f"={CB('us_com')}/{CB('us')}", PCT, "a do ofício; na nossa carteira é 23,7%"),
    (9, "Uso máximo da sala para dizer quantas salas o volume pede", 1, PCT, "100% = sem folga; 90% deixa espaço para falta e aparelho parado"),
]
for r, rot, v, fmt, obs in prem:
    celula(vo, f"A{r}", rot)
    celula(vo, f"B{r}", v, AZUL, fmt)
    celula(vo, f"C{r}", obs, NOTA)
SALAS_S, SALAS_N, DOP, USO = "$B$6", "$B$7", "$B$8", "$B$9"
VOLUMES = [30000, 40000, 54589, 65000, 75983, 90000, 100000, 113518]


def fixo(c, salas):
    """Custo fixo do período pela conta c (B = Sebastião, C = nossa), com esse número de salas."""
    k = CMP[c]
    return (f"(({salas})*({k('n_aux')}*{k('aux')}+{k('sala')}+{k('apar')}+{k('limp_s')})"
            f"+{k('unid')}*{k('n_rec')}*{k('rec')}+{k('limp')}+{k('sist')}+{k('logi')}+{k('gest')})*{k('meses')}")


def var(c):
    return f"({CMP[c]('mat')}+{CMP[c]('fisc')})"


def med_gar(c, salas, v):
    """Médico por exame com a garantia cobrada quando a produção média do plantão fica abaixo dela."""
    k = CMP[c]
    prod = f"{v}*((1-{DOP})*{k('med_sem')}+{DOP}*{k('med_com')})"
    return f"MAX({prod},({salas})*{k('dias')}*{k('meses')}*{k('garantia')})/{v}"


def horas_sala(c):
    k = CMP[c]
    return f"({k('dias')}*{k('meses')}*{k('h_dia')})"


def uso(v, c_min, c_rede, salas):
    return f"={v}*{CMP[c_min]('min')}/60/(({salas})*{horas_sala(c_rede)})"


def pinta_uso(ref):
    from openpyxl.formatting.rule import CellIsRule
    vo.conditional_formatting.add(ref, CellIsRule(operator="greaterThan", formula=["1"], fill=F_ALERTA))


# ---- 1. rede fixa
secao(vo, 11, "1. Com as salas fixas: a rede de cada um, e o volume mudando", "ABCDEFGHIJK")
cabecalho(vo, 12, ["ultrassons no período", "Sebastião: fixo por exame", "Sebastião: sem Doppler", "Sebastião: com Doppler",
                   "Sebastião: com a garantia em todo plantão", "Sebastião: uso das salas, pelo tempo dele",
                   "Sebastião: uso das salas, pelo nosso tempo", "nosso: fixo por exame"])
for col, t in zip("IJK", ["nosso: ultrassom, com ou sem Doppler", "nosso: uso das salas, pelo nosso tempo", "nosso menos Sebastião (sem Doppler)"]):
    celula(vo, f"{col}12", t, NEGRITO, fill=F_CAB, wrap=True, alinh="center")
vo.row_dimensions[12].height = 58
for i, v in enumerate(VOLUMES):
    r = 13 + i
    V = f"$A{r}"
    celula(vo, f"A{r}", v, AZUL, INT)
    celula(vo, f"B{r}", f"={fixo('B', SALAS_S)}/{V}", fmt=REAL)
    celula(vo, f"C{r}", f"={CB('med_sem')}+{var('B')}+B{r}", fmt=REAL)
    celula(vo, f"D{r}", f"={CB('med_com')}+{var('B')}+B{r}", fmt=REAL)
    celula(vo, f"E{r}", f"={med_gar('B', SALAS_S, V)}+{var('B')}+B{r}", fmt=REAL)
    celula(vo, f"F{r}", uso(V, "B", "B", SALAS_S), fmt=PCT)
    celula(vo, f"G{r}", uso(V, "C", "B", SALAS_S), fmt=PCT)
    celula(vo, f"H{r}", f"={fixo('C', SALAS_N)}/{V}", fmt=REAL)
    celula(vo, f"I{r}", f"={CC('med_sem')}+{var('C')}+H{r}", fmt=REAL)
    celula(vo, f"J{r}", uso(V, "C", "C", SALAS_N), fmt=PCT)
    celula(vo, f"K{r}", f"=I{r}-C{r}", fmt=REAL)
fim1 = 13 + len(VOLUMES) - 1
pinta_uso(f"F13:G{fim1}")
pinta_uso(f"J13:J{fim1}")
nota(vo, fim1 + 1, "Uso acima de 100% (laranja): o volume não cabe nessas salas, e o custo da linha não vale; ver a seção 2.")
nota(vo, fim1 + 2, "Com a garantia: o médico recebe o maior entre a produção e R$ 1.500 por plantão, com todas as salas abertas todo dia útil. "
                   "Quando a produção passa da garantia, a coluna E fica entre a C e a D.")

# ---- 2. salas acompanham o volume
t2 = fim1 + 4
secao(vo, t2, "2. Com as salas acompanhando o volume: quantas salas cada volume pede, e o custo com elas", "ABCDEFGHIJK")
cabecalho(vo, t2 + 1, ["ultrassons no período", "salas, pelo tempo do Sebastião", "salas, pelo nosso tempo",
                       "Sebastião, salas pelo tempo dele: sem Doppler", "Sebastião, salas pelo tempo dele: com a garantia",
                       "Sebastião, salas pelo nosso tempo: sem Doppler", "Sebastião, salas pelo nosso tempo: com a garantia",
                       "nosso, salas pelo nosso tempo: ultrassom"])
celula(vo, f"I{t2+1}", "nosso menos Sebastião, as duas com as salas pelo nosso tempo", NEGRITO, fill=F_CAB, wrap=True, alinh="center")
vo.row_dimensions[t2 + 1].height = 58
for i in range(len(VOLUMES)):
    r = t2 + 2 + i
    V = f"$A{r}"
    celula(vo, f"A{r}", f"=A{13+i}", fmt=INT)
    celula(vo, f"B{r}", f"=ROUNDUP({V}*{CB('min')}/60/({horas_sala('B')}*{USO}),0)", fmt=INT)
    celula(vo, f"C{r}", f"=ROUNDUP({V}*{CC('min')}/60/({horas_sala('C')}*{USO}),0)", fmt=INT)
    celula(vo, f"D{r}", f"={CB('med_sem')}+{var('B')}+{fixo('B', f'$B{r}')}/{V}", fmt=REAL)
    celula(vo, f"E{r}", f"={med_gar('B', f'$B{r}', V)}+{var('B')}+{fixo('B', f'$B{r}')}/{V}", fmt=REAL)
    celula(vo, f"F{r}", f"={CB('med_sem')}+{var('B')}+{fixo('B', f'$C{r}')}/{V}", fmt=REAL)
    celula(vo, f"G{r}", f"={med_gar('B', f'$C{r}', V)}+{var('B')}+{fixo('B', f'$C{r}')}/{V}", fmt=REAL)
    celula(vo, f"H{r}", f"={CC('med_sem')}+{var('C')}+{fixo('C', f'$C{r}')}/{V}", fmt=REAL)
    celula(vo, f"I{r}", f"=H{r}-F{r}", fmt=REAL)
fim2 = t2 + 2 + len(VOLUMES) - 1
nota(vo, fim2 + 1, "As salas pelo nosso tempo usam a sala de 8 h de exame por dia; pelo tempo dele, a de 9 h. O volume segue os da seção 1.")
nota(vo, fim2 + 2, "Quando as salas acompanham o volume, o custo por exame quase não cai: só a recepção e as verbas da rede se diluem.")
nota(vo, fim2 + 3, "Tomografia: é paga à clínica por exame (R$ 175, ou R$ 218 com contraste), e o volume não muda o preço, salvo se a clínica der desconto por volume ou pedir mínimo mensal.")

vo.column_dimensions["A"].width = 50
for col in "BCDEFGHIJK":
    vo.column_dimensions[col].width = 17
vo.freeze_panes = "B5"

# ============================================================ MARGENS
from openpyxl.formatting.rule import CellIsRule
from openpyxl.utils import get_column_letter

mg = wb.create_sheet("Margens")
mg["A1"].value = "Margem por procedimento: preço da Candanga menos o custo de fazer"
mg["A1"].font = TITULO
nota(mg, 2, "Exames e quantidades da carteira v3 de 11/11, na nossa rede (14 salas). Custos da aba Comparativo, seção 5. "
            "Margem é a folga para executar, e não lucro; o custo acessório (R$ 956.160) fica fora.")
nota(mg, 3, "Azul = pode trocar (quantidade, preço e minutos). Laranja = o exame custa mais do que a Candanga paga. Controle interno.")
EXAMES = [  # nome, tipo, quantidade, preço Candanga, minutos de sala ou de tomógrafo
    ("US de abdômen total (adulto)", "us", 13595, 117.51, 20),
    ("US de parede abdominal", "us", 3304, 117.51, 20),
    ("US de abdômen total (criança)", "us", 452, 117.51, 20),
    ("US de abdômen superior", "us", 2505, 101.27, 15),
    ("US de aparelho urinário e rins (adulto)", "us", 4962, 90.53, 15),
    ("US de aparelho urinário (criança)", "us", 276, 90.53, 15),
    ("US de bolsa escrotal (adulto)", "us", 1034, 100.00, 15),
    ("US de bolsa escrotal (criança)", "us", 234, 100.00, 15),
    ("US de próstata (via abdominal)", "us", 3466, 74.19, 15),
    ("US de tireoide (adulto)", "us", 5308, 64.07, 15),
    ("US de tireoide (criança)", "us", 60, 64.07, 15),
    ("US de mamas (as duas)", "us", 12950, 70.97, 20),
    ("US transvaginal", "us", 5294, 83.77, 15),
    ("US de articulação, fora da ortopedia", "us", 4557, 70.97, 15),
    ("Doppler de carótidas e outros vasos", "dop", 5952, 115.61, 20),
    ("Doppler de membros (os dois lados)", "dop", 12034, 115.61, 40),
    ("TC de abdômen superior com contraste", "tcc", 4116, 309.25, 20),
    ("TC de abdômen superior sem contraste", "tcs", 68, 309.25, 11),
    ("TC de pelve com contraste", "tcc", 3634, 309.25, 20),
    ("TC de pelve sem contraste", "tcs", 56, 309.25, 11),
    ("TC de tórax com contraste", "tcc", 2350, 309.25, 20),
    ("TC de tórax sem contraste", "tcs", 180, 309.25, 11),
    ("TC de pescoço com contraste", "tcc", 479, 309.25, 20),
    ("TC de crânio sem contraste", "tcs", 44, 251.29, 11),
]
ROT = {"us": "ultrassom sem Doppler", "dop": "ultrassom com Doppler", "tcc": "tomografia com contraste", "tcs": "tomografia sem contraste"}
CAB = ["exame", "tipo", "quantidade", "preço Candanga", "minutos", "valor que traz",
       "Sebastião: custo", "Sebastião: margem por exame", "Sebastião: margem %", "Sebastião: margem no total",
       "Sebastião com a garantia: custo", "com a garantia: margem %", "com a garantia: margem no total",
       "nosso: custo", "nosso: margem por exame", "nosso: margem %", "nosso: margem no total",
       "nosso, fixo rateado pelo tempo: custo", "pelo tempo: margem %", "pelo tempo: margem no total"]
L0 = 6
secao(mg, 5, "1. Procedimento a procedimento", [get_column_letter(i + 1) for i in range(len(CAB))])
for i, t in enumerate(CAB):
    celula(mg, f"{get_column_letter(i+1)}{L0}", t, NEGRITO, fill=F_CAB, wrap=True, alinh="center")
mg.row_dimensions[L0].height = 58
cB, cC = (lambda k: f"Comparativo!$B${R[k]}"), (lambda k: f"Comparativo!$C${R[k]}")
# nosso, pelo tempo: médico e variável iguais; o fixo vai na proporção dos minutos de sala
FIXO_N = f"({cC('b_nmed')}-{cC('b_mat')}-{cC('b_fisc')})"
ini = L0 + 1
fim_us = ini + sum(1 for e in EXAMES if e[1] in ("us", "dop")) - 1
fim = ini + len(EXAMES) - 1
MIN_US = f"SUMPRODUCT($C${ini}:$C${fim_us},$E${ini}:$E${fim_us})"
for i, (nome, tipo, qtd, preco, minutos) in enumerate(EXAMES):
    r = ini + i
    celula(mg, f"A{r}", nome)
    celula(mg, f"B{r}", ROT[tipo], NOTA)
    celula(mg, f"C{r}", qtd, AZUL, INT)
    celula(mg, f"D{r}", preco, AZUL, REAL)
    celula(mg, f"E{r}", minutos, AZUL, INT)
    celula(mg, f"F{r}", f"=C{r}*D{r}", fmt=REAL)
    if tipo in ("us", "dop"):
        seb = cB("b_f_us") if tipo == "us" else cB("b_f_dop")
        gar, nos = cB("b_f_gar"), (cC("b_f_us") if tipo == "us" else cC("b_f_dop"))
        tempo = f"={cC('med_sem' if tipo == 'us' else 'med_com')}+{cC('mat')}+{cC('fisc')}+{FIXO_N}*E{r}/{MIN_US}"
    else:
        k = "tc_c" if tipo == "tcc" else "tc_s"
        seb, gar, nos, tempo = cB(k), cB(k), cC(k), f"={cC(k)}"
    for col, custo in (("G", f"={seb}"), ("K", f"={gar}"), ("N", f"={nos}"), ("R", tempo)):
        celula(mg, f"{col}{r}", custo, fmt=REAL)
    celula(mg, f"H{r}", f"=D{r}-G{r}", fmt=REAL)
    celula(mg, f"I{r}", f"=H{r}/D{r}", fmt=PCT)
    celula(mg, f"J{r}", f"=H{r}*C{r}", fmt=REAL)
    celula(mg, f"L{r}", f"=(D{r}-K{r})/D{r}", fmt=PCT)
    celula(mg, f"M{r}", f"=(D{r}-K{r})*C{r}", fmt=REAL)
    celula(mg, f"O{r}", f"=D{r}-N{r}", fmt=REAL)
    celula(mg, f"P{r}", f"=O{r}/D{r}", fmt=PCT)
    celula(mg, f"Q{r}", f"=O{r}*C{r}", fmt=REAL)
    celula(mg, f"S{r}", f"=(D{r}-R{r})/D{r}", fmt=PCT)
    celula(mg, f"T{r}", f"=(D{r}-R{r})*C{r}", fmt=REAL)
for col in "ILPS":
    mg.conditional_formatting.add(f"{col}{ini}:{col}{fim+3}", CellIsRule(operator="lessThan", formula=["0"], fill=F_ALERTA))


def total(r, rot, a, b):
    celula(mg, f"A{r}", rot, NEGRITO, fill=F_TOTAL)
    celula(mg, f"B{r}", "", fill=F_TOTAL)
    celula(mg, f"C{r}", f"=SUM(C{a}:C{b})", NEGRITO, INT, F_TOTAL)
    celula(mg, f"D{r}", f"=F{r}/C{r}", NEGRITO, REAL, F_TOTAL)
    celula(mg, f"E{r}", f"=SUMPRODUCT(C{a}:C{b},E{a}:E{b})/C{r}", NEGRITO, DEC, F_TOTAL)
    celula(mg, f"F{r}", f"=SUM(F{a}:F{b})", NEGRITO, REAL, F_TOTAL)
    for custo, porex, pct, tot in (("G", "H", "I", "J"), ("K", None, "L", "M"), ("N", "O", "P", "Q"), ("R", None, "S", "T")):
        celula(mg, f"{tot}{r}", f"=SUM({tot}{a}:{tot}{b})", NEGRITO, REAL, F_TOTAL)
        celula(mg, f"{custo}{r}", f"=(F{r}-{tot}{r})/C{r}", NEGRITO, REAL, F_TOTAL)
        celula(mg, f"{pct}{r}", f"={tot}{r}/F{r}", NEGRITO, PCT, F_TOTAL)
        if porex:
            celula(mg, f"{porex}{r}", f"={tot}{r}/C{r}", NEGRITO, REAL, F_TOTAL)


total(fim + 1, "ULTRASSOM", ini, fim_us)
total(fim + 2, "TOMOGRAFIA", fim_us + 1, fim)
total(fim + 3, "TOTAL DOS EXAMES", ini, fim)
n = fim + 5
nota(mg, n, "Nos totais, preço, minutos e custo são médias por exame.")
nota(mg, n + 1, "Sebastião e nosso: o fixo é dividido igual por exame, como o ofício faz. Com a garantia: cobrada em todo plantão, nas 14 salas, todo dia útil (pior cenário).")
nota(mg, n + 2, "Pelo tempo: o mesmo custo total da nossa conta, mas o fixo (sala, aparelho, auxiliares, recepção e verbas) vai para cada exame na proporção dos minutos de sala. "
                "Mostra quem de fato ocupa a sala: o total do ultrassom não muda.")
celula(mg, f"A{n+4}", "Conferência: ultrassons desta aba menos os da aba Comparativo (deve dar 0)")
celula(mg, f"B{n+4}", f"=C{fim+1}-{cC('us')}", fmt=INT)
celula(mg, f"A{n+5}", "Conferência: tomografias desta aba menos as da aba Comparativo (deve dar 0)")
celula(mg, f"B{n+5}", f"=C{fim+2}-{cC('tc')}", fmt=INT)
mg.column_dimensions["A"].width = 44
mg.column_dimensions["B"].width = 24
for i in range(3, len(CAB) + 1):
    mg.column_dimensions[get_column_letter(i)].width = 16
mg.freeze_panes = f"B{ini}"

wb.save(SAIDA)
print("gravado:", SAIDA.name)
