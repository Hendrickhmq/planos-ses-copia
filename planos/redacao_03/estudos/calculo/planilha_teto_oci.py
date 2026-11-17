"""Planilha do teto da OCI de câncer gástrico (09.01.01.007-3) para negociar com as clínicas.

Controle interno: não vai ao plano nem às clínicas.

Uso: python3 planilha_teto_oci.py <saida.xlsx>

Três formas de contratar a execução, sobre as mesmas premissas:
A. pacote na clínica: a clínica entrega a OCI inteira e recebe por OCI concluída;
B. por componente: consulta, exame com sedação, anatomopatológico e retorno, cada um com seu preço;
C. estrutura alugada e equipe própria: o desenho literal do plano (seções 10 e 11).

As células amarelas são premissas: mude e as outras abas se refazem. Depois de gerar, recalcular
com o recalc.py da skill xlsx (as fórmulas saem sem valor do openpyxl).
"""
import sys

from openpyxl import Workbook
from openpyxl.comments import Comment
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

ARIAL = "Arial"
F_TIT = Font(name=ARIAL, size=14, bold=True)
F_SUB = Font(name=ARIAL, size=10, italic=True, color="555555")
F_CAB = Font(name=ARIAL, size=10, bold=True, color="FFFFFF")
F_TXT = Font(name=ARIAL, size=10)
F_NEG = Font(name=ARIAL, size=10, bold=True)
F_IN = Font(name=ARIAL, size=10, color="0000FF")
F_LNK = Font(name=ARIAL, size=10, color="008000")
CAB = PatternFill("solid", fgColor="1F3864")
AMAR = PatternFill("solid", fgColor="FFFF00")
CINZA = PatternFill("solid", fgColor="EDEDED")
FINO = Side(style="thin", color="BFBFBF")
BORDA = Border(left=FINO, right=FINO, top=FINO, bottom=FINO)
R2 = 'R$ #,##0.00;[Red]-R$ #,##0.00;"-"'
R0 = 'R$ #,##0;[Red]-R$ #,##0;"-"'
N0 = '#,##0;[Red]-#,##0;"-"'
N2 = '#,##0.00'
PCT = '0.0%;[Red]-0.0%;"-"'
QUEBRA = Alignment(wrap_text=True, vertical="top")
CEN = Alignment(horizontal="center", vertical="center", wrap_text=True)


def c(ws, ref, valor, fonte=F_TXT, fmt=None, fill=None, al=None, borda=True):
    cel = ws[ref]
    cel.value = valor
    cel.font = fonte
    if fmt:
        cel.number_format = fmt
    if fill:
        cel.fill = fill
    cel.alignment = al or QUEBRA
    if borda:
        cel.border = BORDA
    return cel


def cab(ws, linha, nomes, col=1, h=30):
    for i, n in enumerate(nomes):
        c(ws, f"{get_column_letter(col + i)}{linha}", n, F_CAB, fill=CAB, al=CEN)
    ws.row_dimensions[linha].height = h


def titulo(ws, texto, sub):
    c(ws, "A1", texto, F_TIT, borda=False)
    c(ws, "A2", sub, F_SUB, borda=False)
    ws.merge_cells("A2:F2")
    ws.row_dimensions[2].height = 42


def larguras(ws, ls):
    for i, w in enumerate(ls, 1):
        ws.column_dimensions[get_column_letter(i)].width = w


wb = Workbook()
leia = wb.active
leia.title = "Leia"
pr = wb.create_sheet("Premissas")
pa = wb.create_sheet("A pacote")
pb = wb.create_sheet("B componentes")
pc = wb.create_sheet("C equipe própria")
vo = wb.create_sheet("Volume")
rf = wb.create_sheet("Referências")
P, B_ = "Premissas!", "'B componentes'!"

# ================================================================== Premissas
titulo(pr, "Premissas", "As células amarelas são premissas: mude e as outras abas se refazem. O que vem do plano "
       "assinado ou da Tabela do SUS tem fonte; o que diz 'hipótese' é para trocar pela cotação ou pela decisão.")
larguras(pr, [52, 16, 70])
cab(pr, 4, ["Premissa", "Valor", "De onde vem"])
PREM = [
    ("V", "Valor da OCI 09.01.01.007-3 (R$)", 600.11, R2,
     "SIGTAP 10/2026 (arquivo oficial TabelaUnificada_202610, DATASUS); valor da Portaria SAES/MS 4.653/2026, "
     "desde 08/2026. É o item 2.1.1 do plano assinado."),
    ("N", "OCIs da meta", 13012, N0, "Plano assinado, Meta 02 (seções 15 e 19.2)."),
    ("POL", "Polos", 2, N0, "Plano assinado, seção 9: Polo 1 Taguatinga e Polo 2 CONIC."),
    ("DU", "Dias úteis de produção", 167, N0, "Plano assinado, seção 16.3 (dez/2026 a jul/2027)."),
    ("MV", "Meses de vigência (equipe e estrutura pagas)", 9, N0,
     "Plano assinado, seção 16.1: mês 1 de implantação e 8 de produção."),
    ("BIO", "EDAs com biópsia (anatomopatológico)", 0.70, PCT,
     "Hipótese. O plano (13.1) biopsia lesão suspeita ou pelo protocolo de Sydney modificado; com Sydney de rotina, "
     "chega perto de 100%. Pedir à clínica a taxa dela em EDA diagnóstica."),
    ("AP", "Anatomopatológico por paciente (R$)", 60.00, R2,
     "Hipótese, entre o SIGTAP (R$ 40,78) e o varejo por amostra (R$ 91,00, dr.consulta). Negociar por paciente, "
     "não por frasco: a OCI paga um anatomopatológico só."),
    ("TELE", "Retornos por teleconsulta", 0.50, PCT,
     "Hipótese. O plano admite retorno presencial ou teleconsulta (seção 7.1, etapa 7)."),
    ("CONC", "OCIs iniciadas que concluem", 0.95, PCT,
     "Plano assinado, seção 15: retornos realizados ≥ 95% das OCIs com EDA. A OCI que não conclui não conta "
     "para a meta (7.2)."),
    ("RES", "Reserva de risco do ISHP sobre o valor da OCI", 0.05, PCT,
     "Decisão de vocês. Cobre glosa, nova coleta sem ônus (13.5), intercorrência e atraso de laudo."),
    ("RET", "Custos que ficam com o ISHP dentro da OCI (R$ por OCI)", 10.00, R2,
     "Hipótese. Itens que o plano põe no unitário (19.3) e que a clínica pode não trazer: seguro de "
     "responsabilidade civil, prontuário, plataforma de teleconsulta."),
]
REF = {}
for i, (k, rot, val, fmt, fonte) in enumerate(PREM, 5):
    c(pr, f"A{i}", rot)
    c(pr, f"B{i}", val, F_IN, fmt, AMAR)
    c(pr, f"C{i}", fonte)
    REF[k] = f"{P}$B${i}"
lin = 5 + len(PREM) + 1
c(pr, f"A{lin}", "Derivados", F_NEG, borda=False)
lin += 1
cab(pr, lin, ["Conta", "Valor", "Como se calcula"])
DER = [
    ("T", "Teto técnico por OCI concluída (R$)", f"=({REF['V']}-{REF['RET']})*(1-{REF['RES']})", R2,
     "(valor da OCI − custos do ISHP) × (1 − reserva). É o máximo que se paga pela OCI inteira sem tirar "
     "dinheiro da gestão, que o plano paga à parte (Metas 01 e 03)."),
    ("EDA", "EDAs realizadas para concluir a meta", f"={REF['N']}/{REF['CONC']}", N0,
     "OCIs da meta ÷ conclusão: as OCIs que não concluem também fazem consulta e exame."),
    ("REC", "O convênio paga pela Meta 02 (R$)", f"={REF['V']}*{REF['N']}", R2, "valor da OCI × OCIs da meta"),
]
for k, rot, form, fmt, como in DER:
    lin += 1
    c(pr, f"A{lin}", rot)
    c(pr, f"B{lin}", form, F_NEG, fmt)
    c(pr, f"C{lin}", como)
    REF[k] = f"{P}$B${lin}"
V, N, T, CONC, BIO, TELE, RET, RES, AP, POL, DU, MV = (REF[k] for k in
    ("V", "N", "T", "CONC", "BIO", "TELE", "RET", "RES", "AP", "POL", "DU", "MV"))

# ================================================================== A. pacote na clínica
titulo(pa, "A. Pacote na clínica: a OCI inteira por um preço",
       "A clínica entrega consulta, EDA com sedação por anestesiologista, anatomopatológico, retorno, enfermagem, SRPA, "
       "reprocessamento, insumos e estrutura. O ISHP faz a recepção, o agendamento e o registro, que o plano paga na Meta 01.")
larguras(pa, [44, 18, 18, 18, 20, 16])
cab(pa, 4, ["", "Valor"])
LA = [
    ("O convênio paga por OCI concluída", f"={V}", R2),
    ("Teto técnico, pagando a clínica por OCI concluída", f"={T}", R2),
    ("Teto técnico, pagando a clínica por OCI iniciada (na EDA)", f"={T}*{CONC}", R2),
    ("O convênio paga pela Meta 02, no total", f"={REF['REC']}", R0),
    ("Por polo", f"={REF['REC']}/{POL}", R0),
]
for i, (rot, form, fmt) in enumerate(LA, 5):
    c(pa, f"A{i}", rot)
    c(pa, f"B{i}", form, F_LNK if "!" in form else F_NEG, fmt)
c(pa, "A11", "Pagar por OCI concluída passa à clínica o risco do retorno e do laudo atrasado. Pagar na EDA deixa o "
  "risco com o ISHP, e o teto cai na proporção das OCIs que não concluem.", F_SUB, borda=False)
pa.merge_cells("A11:F11")
pa.row_dimensions[11].height = 30
cab(pa, 13, ["Oferta, em % do valor da OCI", "Preço por OCI (R$)", "Fica com o ISHP por OCI (R$)",
             "Fica com o ISHP no total (R$)", "Fica com o ISHP, % do valor", "Cabe no teto?"], h=44)
for j, pct in enumerate([0.50, 0.60, 0.70, 0.80, 0.85, 0.90, 0.95], 14):
    c(pa, f"A{j}", pct, F_IN, PCT, AMAR)
    c(pa, f"B{j}", f"={V}*A{j}", F_TXT, R2)
    c(pa, f"C{j}", f"={V}-B{j}", F_TXT, R2)
    c(pa, f"D{j}", f"=C{j}*{N}", F_TXT, R0)
    c(pa, f"E{j}", f"=C{j}/{V}", F_TXT, PCT)
    c(pa, f"F{j}", f'=IF(B{j}<={T},"sim","não")', F_TXT, al=CEN)
c(pa, "A22", "\"Fica com o ISHP\" é antes dos custos do ISHP dentro da OCI e da reserva (aba Premissas). A gestão, a "
  "recepção e a prestação de contas já estão pagas à parte, nas Metas 01 e 03 (R$ 596.696,76).", F_SUB, borda=False)
pa.merge_cells("A22:F22")
pa.row_dimensions[22].height = 30

# ================================================================== B. por componente
titulo(pb, "B. Por componente: quanto sobra para o exame",
       "Cada peça com seu preço. As células amarelas são a cotação da clínica (os valores de agora são exemplo). "
       "A OCI que não conclui paga consulta, exame e biópsia e não recebe: por isso essas peças se dividem pela conclusão.")
larguras(pb, [50, 16, 16, 16, 16, 60])
cab(pb, 4, ["Componente", "Preço (R$)", "Vezes por OCI concluída", "Por OCI concluída (R$)", "", "Nota"])
COMP = [
    ("C1", "Consulta inicial com gastroenterologista", 80.00, f"=1/{CONC}",
     "Exemplo: um quinto da mediana do varejo do DF (R$ 400,00); preço de volume a cotar."),
    ("E", "EDA com sedação por anestesiologista (o exame)", 400.00, f"=1/{CONC}",
     "Exemplo, entre o que a SES-DF paga pela EDA na Tabela Regionalizada (R$ 335,00) e o que o Ministério paga "
     "por EDA e sedação no Agora Tem Especialistas (R$ 500,11). Deve incluir sala, enfermagem, SRPA, "
     "reprocessamento e insumos."),
    ("S", "Sedação cobrada à parte (se a clínica separar)", 0.00, f"=1/{CONC}",
     "Muitas clínicas cobram o anestesiologista à parte. Zero se estiver no exame."),
    ("APc", "Anatomopatológico por paciente", f"={AP}", f"={BIO}/{CONC}",
     "Vem da aba Premissas. Por paciente, não por frasco."),
    ("IB", "Pinça, frasco e formol cobrados à parte", 0.00, f"={BIO}/{CONC}",
     "Zero se estiver no exame. Pinça descartável custava menos de US$ 40 num estudo de 2000 (PubMed 10699769)."),
    ("RP", "Retorno presencial", 60.00, f"=1-{TELE}", "Exemplo; o varejo do DF não publica retorno."),
    ("TC", "Retorno por teleconsulta", 50.00, f"={TELE}", "Exemplo."),
]
RB = {}
for i, (k, rot, preco, vezes, nota) in enumerate(COMP, 5):
    c(pb, f"A{i}", rot)
    eh_link = isinstance(preco, str)
    c(pb, f"B{i}", preco, F_LNK if eh_link else F_IN, R2, None if eh_link else AMAR)
    c(pb, f"C{i}", vezes, F_TXT, '0.000')
    c(pb, f"D{i}", f"=B{i}*C{i}", F_TXT, R2)
    c(pb, f"F{i}", nota)
    RB[k] = i
fim = 5 + len(COMP) - 1
L = fim + 2
c(pb, f"A{L}", "Custo por OCI concluída", F_NEG)
c(pb, f"D{L}", f"=SUM(D5:D{fim})", F_NEG, R2)
c(pb, f"A{L+1}", "Teto técnico por OCI concluída (aba Premissas)")
c(pb, f"D{L+1}", f"={T}", F_LNK, R2)
c(pb, f"A{L+2}", "Folga sobre o teto por OCI (negativo: a cotação não cabe)", F_NEG)
c(pb, f"D{L+2}", f"=D{L+1}-D{L}", F_NEG, R2)
c(pb, f"A{L+3}", "Folga sobre o teto no total da meta")
c(pb, f"D{L+3}", f"=D{L+2}*{N}", F_TXT, R0)
e = lambda k: f"B{RB[k]}"
TETO_E = (f"=({T}-{TELE}*{e('TC')}-(1-{TELE})*{e('RP')})*{CONC}-{e('C1')}-{e('S')}"
          f"-{BIO}*({e('APc')}+{e('IB')})")
c(pb, f"A{L+5}", "Até quanto se paga pelo exame (EDA com sedação), com os outros preços desta aba", F_NEG)
c(pb, f"D{L+5}", TETO_E, F_NEG, R2, CINZA)
c(pb, f"F{L+5}", "(teto − retorno médio) × conclusão − consulta inicial − sedação à parte − biópsia × (anatomopatológico "
  "+ pinça). É o número para levar à negociação do exame.")
c(pb, f"A{L+6}", "O mesmo, em % do valor da OCI")
c(pb, f"D{L+6}", f"=D{L+5}/{V}", F_TXT, PCT)

# o estudo de 20/10: exame, retorno e biópsia
L2 = L + 8
c(pb, f"A{L2}", "As três peças do estudo de 20/10 (exame, retorno e biópsia) e o que ficava de fora", F_NEG, borda=False)
cab(pb, L2 + 1, ["", "R$ por OCI concluída"])
TRES = [
    ("Exame, sem dividir pela conclusão", f"={e('E')}"),
    ("Retorno médio (presencial e teleconsulta)", f"={TELE}*{e('TC')}+(1-{TELE})*{e('RP')}"),
    ("Biópsia, sem dividir pela conclusão", f"={BIO}*{e('APc')}"),
    ("As três peças", f"=SUM(B{L2+2}:B{L2+4})"),
    ("Custo completo desta aba", f"=D{L}"),
    ("Ficava de fora: consulta inicial, sedação e pinça à parte, e as OCIs que não concluem", f"=B{L2+6}-B{L2+5}"),
]
for j, (rot, form) in enumerate(TRES, L2 + 2):
    c(pb, f"A{j}", rot, F_NEG if j >= L2 + 5 else F_TXT)
    c(pb, f"B{j}", form, F_NEG if j >= L2 + 5 else F_TXT, R2)

# sensibilidade: teto do exame por taxa de biópsia e preço do anatomopatológico
L3 = L2 + 10
c(pb, f"A{L3}", "Até quanto se paga pelo exame, pela taxa de biópsia (linhas) e pelo preço do anatomopatológico por "
  "paciente (colunas)", F_NEG, borda=False)
pb.merge_cells(f"A{L3}:F{L3}")
APS = [40.78, 60, 91, 130]
cab(pb, L3 + 1, ["Taxa de biópsia"] + [f"AP R$ {a:.2f}".replace(".", ",") for a in APS])
for j, b in enumerate([0.40, 0.55, 0.70, 0.85, 1.00], L3 + 2):
    c(pb, f"A{j}", b, F_IN, PCT, AMAR)
    for k, a in enumerate(APS):
        col = get_column_letter(2 + k)
        form = (f"=({T}-{TELE}*{e('TC')}-(1-{TELE})*{e('RP')})*{CONC}-{e('C1')}-{e('S')}"
                f"-$A{j}*({a}+{e('IB')})")
        c(pb, f"{col}{j}", form, F_TXT, R2)
c(pb, f"A{L3+8}", "As outras peças (consulta, sedação e pinça à parte, retorno) e as premissas ficam como estão acima. "
  "R$ 40,78 é o SIGTAP; R$ 91,00 e R$ 130,00, o varejo por amostra (dr.consulta, com e sem cartão).", F_SUB, borda=False)
pb.merge_cells(f"A{L3+8}:F{L3+8}")
pb.row_dimensions[L3 + 8].height = 30

# ================================================================== C. estrutura e equipe própria
titulo(pc, "C. Estrutura alugada e equipe própria (o desenho do plano)",
       "A equipe da seção 10.2 do plano, com os médicos pagos por hora de posto e a enfermagem pelos 9 meses; os "
       "insumos e o anatomopatológico por EDA; o equipamento e a estrutura por mês. Ordem de grandeza: quase tudo é "
       "hipótese a cotar.")
larguras(pc, [46, 15, 13, 13, 13, 16, 18, 52])
c(pc, "A4", "Horas por dia de posto", F_TXT)
c(pc, "B4", 10, F_IN, N0, AMAR)
c(pc, "H4", "Plano, seção 10.2: 10 h por dia, segunda a sexta.")
HD = "$B$4"
cab(pc, 6, ["Médicos (por hora de posto)", "Custo por mês (R$)", "Jornada (h/semana)", "R$ por hora",
            "Postos por polo", "Horas no período", "Custo no período (R$)", "Fonte"], h=40)
MED = [
    ("Gastroenterologista (consulta inicial e retorno)", 14777, 20, 3,
     "salario.com.br, CBO 2251-65, Brasil (sem amostra no DF), custo para a empresa, 21/10/2026. Postos: plano 10.2."),
    ("Endoscopista", 15516, 21, 2, "salario.com.br, CBO 2253-10, Brasil (sem amostra no DF), custo para a empresa, 21/10/2026."),
    ("Anestesiologista (um por sala)", 21354, 24, 2, "salario.com.br, CBO 2251-51, Brasília/DF, custo para a empresa, 21/10/2026."),
]
for i, (rot, custo, jor, postos, fonte) in enumerate(MED, 7):
    c(pc, f"A{i}", rot)
    c(pc, f"B{i}", custo, F_IN, R0, AMAR)
    c(pc, f"C{i}", jor, F_IN, N0, AMAR)
    c(pc, f"D{i}", f"=B{i}/(C{i}*52/12)", F_TXT, R2)
    c(pc, f"E{i}", postos, F_IN, N0, AMAR)
    c(pc, f"F{i}", f"=E{i}*{HD}*{DU}*{POL}", F_TXT, N0)
    c(pc, f"G{i}", f"=D{i}*F{i}", F_TXT, R0)
    c(pc, f"H{i}", fonte)
cab(pc, 11, ["Enfermagem e reprocessamento (CLT)", "Custo por mês (R$)", "", "", "Pessoas por polo",
             "Meses pagos", "Custo no período (R$)", "Fonte"], h=40)
ENF = [
    ("Enfermeiro", 10186, 3, "salario.com.br, CBO 2235-05, Brasília/DF, custo para a empresa, 21/10/2026."),
    ("Técnico de enfermagem", 4945, 6, "salario.com.br, CBO 3222-05, Brasília/DF, custo para a empresa, 21/10/2026."),
    ("Técnico de reprocessamento", 3748, 3,
     "salario.com.br, auxiliar de enfermagem (CBO 3222-30), Brasília/DF, como aproximação; custo para a empresa, 21/10/2026."),
]
for i, (rot, custo, pessoas, fonte) in enumerate(ENF, 12):
    c(pc, f"A{i}", rot)
    c(pc, f"B{i}", custo, F_IN, R0, AMAR)
    c(pc, f"E{i}", pessoas, F_IN, N0, AMAR)
    c(pc, f"F{i}", f"={MV}", F_LNK, N0)
    c(pc, f"G{i}", f"=B{i}*E{i}*{POL}*F{i}", F_TXT, R0)
    c(pc, f"H{i}", fonte)
cab(pc, 16, ["Por EDA, equipamento e estrutura", "Preço (R$)", "", "", "Quantidade", "Vezes", "Custo no período (R$)",
             "Fonte"], h=40)
OUT = [
    ("Insumos por EDA: sedativos, bocal, lidocaína, luvas, oxigênio, saneante da DAN", 50, f"=1", f"={REF['EDA']}",
     "Hipótese a cotar."),
    ("Pinça, frasco e formol por EDA com biópsia", 80, f"={BIO}", f"={REF['EDA']}",
     "Hipótese a cotar; descartável abaixo de US$ 40 num estudo de 2000 (PubMed 10699769)."),
    ("Anatomopatológico por paciente, laboratório contratado", f"={AP}", f"={BIO}", f"={REF['EDA']}",
     "Aba Premissas."),
    ("Conjunto de videoendoscopia por sala por mês (torre, endoscópios, manutenção)", 15000, f"=4", f"={MV}",
     "Hipótese a cotar. Plano, seção 11: 4 salas, 12 videoendoscópios, 6 torres."),
    ("Lavadora automática (DAN) por mês", 3000, f"=4", f"={MV}", "Hipótese a cotar. Plano, seção 11: 4 lavadoras."),
    ("Estrutura por polo por mês: salas, consultórios, SRPA, reprocessamento, recepção", 20000, f"={POL}", f"={MV}",
     "Hipótese a cotar: é o aluguel que se negocia."),
    ("Outros por OCI: energia, limpeza, TI, seguro, teleconsulta", 15, f"=1", f"={N}", "Hipótese a cotar."),
]
for i, (rot, preco, qtd, vezes, fonte) in enumerate(OUT, 17):
    c(pc, f"A{i}", rot)
    eh_link = isinstance(preco, str)
    c(pc, f"B{i}", preco, F_LNK if eh_link else F_IN, R2, None if eh_link else AMAR)
    c(pc, f"E{i}", qtd, F_LNK if "!" in qtd else F_TXT, '0.00')
    c(pc, f"F{i}", vezes, F_LNK, N0)
    c(pc, f"G{i}", f"=B{i}*E{i}*F{i}", F_TXT, R0)
    c(pc, f"H{i}", fonte)
EST = 22  # linha da estrutura
L = 25
RES_C = [
    ("Médicos", "=SUM(G7:G9)"),
    ("Enfermagem e reprocessamento", "=SUM(G12:G14)"),
    ("Insumos, biópsia e anatomopatológico", "=SUM(G17:G19)"),
    ("Equipamento", "=SUM(G20:G21)"),
    ("Estrutura", f"=G{EST}"),
    ("Outros", "=G23"),
]
cab(pc, L - 1, ["Resumo", "", "", "", "", "", "Custo no período (R$)", "Por OCI concluída (R$)"], h=30)
for j, (rot, form) in enumerate(RES_C, L):
    c(pc, f"A{j}", rot)
    c(pc, f"G{j}", form, F_TXT, R0)
    c(pc, f"H{j}", f"=G{j}/{N}", F_TXT, R2)
tot = L + len(RES_C)
c(pc, f"A{tot}", "Custo total", F_NEG)
c(pc, f"G{tot}", f"=SUM(G{L}:G{tot-1})", F_NEG, R0)
c(pc, f"H{tot}", f"=G{tot}/{N}", F_NEG, R2)
c(pc, f"A{tot+1}", "Teto técnico por OCI concluída (aba Premissas)")
c(pc, f"H{tot+1}", f"={T}", F_LNK, R2)
c(pc, f"A{tot+2}", "Folga sobre o teto por OCI (negativo: não cabe)", F_NEG)
c(pc, f"H{tot+2}", f"=H{tot+1}-H{tot}", F_NEG, R2)
c(pc, f"A{tot+3}", "Aluguel máximo da estrutura por polo por mês, com o resto como está", F_NEG)
c(pc, f"H{tot+3}", f"=({T}*{N}-(G{tot}-G{EST}))/({POL}*{MV})", F_NEG, R0, CINZA)
c(pc, f"A{tot+5}", "O que mais pesa é o médico pago por hora de posto: o anestesiologista fica na sala as 10 horas, e o "
  "gastroenterologista tem 3 postos para consultas que ocupam 78% deles (plano, 10.2). Pagar médico por produção, "
  "ou ter a equipe da própria clínica, tira o custo ocioso.", F_SUB, borda=False)
pc.merge_cells(f"A{tot+5}:H{tot+5}")
pc.row_dimensions[tot + 5].height = 44

# ================================================================== Volume
titulo(vo, "Volume e dinheiro por mês", "Plano assinado, seção 16.3. Por polo é a metade: a divisão real segue a "
       "regulação (seção 9.1).")
larguras(vo, [12, 14, 12, 14, 14, 18, 18])
cab(vo, 4, ["Mês", "Período", "Dias úteis", "OCIs", "OCIs por polo", "OCIs por polo por dia útil",
            "O convênio paga (R$)"], h=40)
MESES = [("Mês 1", "nov/2026", 18, 0), ("Mês 2", "dez/2026", 22, 1320), ("Mês 3", "jan/2027", 20, 1613),
         ("Mês 4", "fev/2027", 18, 1451), ("Mês 5", "mar/2027", 22, 1774), ("Mês 6", "abr/2027", 21, 1693),
         ("Mês 7", "mai/2027", 20, 1613), ("Mês 8", "jun/2027", 22, 1774), ("Mês 9", "jul/2027", 22, 1774)]
for i, (m, per, du, oci) in enumerate(MESES, 5):
    c(vo, f"A{i}", m)
    c(vo, f"B{i}", per)
    c(vo, f"C{i}", du, F_TXT, N0)
    c(vo, f"D{i}", oci, F_TXT, N0)
    c(vo, f"E{i}", f"=D{i}/{POL}", F_TXT, N0)
    c(vo, f"F{i}", f"=IF(D{i}=0,0,E{i}/C{i})", F_TXT, '0.0;-0.0;"-"')
    c(vo, f"G{i}", f"=D{i}*{V}", F_TXT, R0)
c(vo, "A14", "Total", F_NEG)
for col in "CDEG":
    c(vo, f"{col}14", f"=SUM({col}5:{col}13)", F_NEG, R0 if col == "G" else N0)
c(vo, "A16", "A capacidade é de 48 EDAs por polo por dia (2 salas × 24); o pico previsto é 40,3 (seção 10.2). O mês "
  "1 não produz: a equipe e a estrutura já correm.", F_SUB, borda=False)
vo.merge_cells("A16:G16")
vo.row_dimensions[16].height = 30

# ================================================================== Referências
titulo(rf, "Referências", "Valores com fonte, para a conversa com a clínica. Não mudam as contas.")
larguras(rf, [16, 46, 16, 16, 16, 60])
cab(rf, 4, ["Código", "O que paga o SUS por cada peça", "SIGTAP (R$)", "Incremento", "Com incremento (R$)", "Fonte"],
    h=40)
SUS = [
    ("09.01.01.007-3", "OCI Avaliação Diagnóstica de Câncer Gástrico", 600.11, None,
     "SIGTAP 10/2026, arquivo oficial do DATASUS."),
    ("02.09.01.003-7", "Esofagogastroduodenoscopia (obrigatória na OCI, 1)", 48.16, 6.27,
     "Incremento: Portaria SAES/MS 4.282/2026, Anexo I (Agora Tem Especialistas, créditos financeiros, "
     "habilitação 38.05); na Tabela de 10/2026, também na 38.01 (PMAE)."),
    ("04.17.01.006-0", "Sedação (compatível na OCI, 1)", 15.15, 8.90, "Incremento: Portaria SAES/MS 4.282/2026, Anexo I."),
    ("02.03.02.003-0", "Anatomopatológico por biópsia (compatível na OCI, 1)", 40.78, None, "SIGTAP 10/2026."),
    ("03.01.01.007-2", "Consulta em atenção especializada (compatível, até 2)", 10.00, None, "SIGTAP 10/2026."),
    ("03.01.01.030-7", "Teleconsulta em atenção especializada (compatível, até 2)", 10.00, None, "SIGTAP 10/2026."),
]
for i, (cod, nome, val, inc, fonte) in enumerate(SUS, 5):
    c(rf, f"A{i}", cod)
    c(rf, f"B{i}", nome)
    c(rf, f"C{i}", val, F_TXT, R2)
    c(rf, f"D{i}", inc if inc is not None else "", F_TXT, '0%' if inc is not None else None)
    c(rf, f"E{i}", f"=ROUND(C{i}*(1+D{i}),2)" if inc is not None else f"=C{i}", F_TXT, R2)
    c(rf, f"F{i}", fonte)
c(rf, "A12", "Leitura", F_NEG, borda=False)
c(rf, "B12", "EDA com incremento + sedação com incremento + R$ 100,00 = R$ 600,11, exatos. A Tabela não diz que a OCI "
  "foi composta assim, mas a soma serve de régua: o Ministério paga R$ 500,11 pelo exame com sedação no programa "
  "federal, e sobram R$ 100,00 para as duas consultas e o anatomopatológico.", F_TXT, borda=False)
rf.merge_cells("B12:F12")
rf.row_dimensions[12].height = 44
c(rf, "B13", "=E6+E7", F_TXT, R2)
c(rf, "C13", "=C5-B13", F_TXT, R2)
c(rf, "D13", "exame com sedação e o que sobra", F_SUB, borda=False)
cab(rf, 15, ["Código", "O que a SES-DF paga", "Valor (R$)", "", "", "Fonte"], h=30)
c(rf, "A16", "02.09.01.003-7")
c(rf, "B16", "Esofagogastroduodenoscopia, valor regionalizado")
c(rf, "C16", 335.00, F_TXT, R2)
c(rf, "F16", "Tabela Regionalizada SUS/DF, Anexo Único da Deliberação CG-SES 24/2024, republicado pela Deliberação "
  "CG-SES 16/2025, item IV (SADT), Endoscopia. É a tabela da contratação complementar de terapia intensiva, não de "
  "ambulatório. SINJ: https://www.sinj.df.gov.br/sinj/Norma/482f67237e0a4bd1a7e9dd40dfe9b158/x.html")
rf.row_dimensions[16].height = 56
cab(rf, 18, ["Componente", "Mercado privado (varejo)", "Preços", "Mínimo (R$)", "Mediana (R$)", "Máximo (R$) e fonte"],
    h=30)
MER = [
    ("Consulta", "Consulta de gastroenterologia, DF", 35, 100, 400, "R$ 1.000,00. Doctoralia, 21/10/2026."),
    ("EDA", "Endoscopia digestiva alta, DF", 2, 500, 800, "R$ 1.100,00. Doctoralia, 21/10/2026; o DF quase não publica."),
    ("EDA", "Endoscopia digestiva alta, fora do DF (SP, BH, Goiânia)", 8, 240, 520, "R$ 980,00. Doctoralia, 21/10/2026."),
    ("AP", "Anatomopatológico por amostra, fora do DF", 1, 91, 91, "R$ 91,00 (R$ 130,00 sem o cartão). dr.consulta, 21/10/2026."),
]
for i, (comp, nome, n, mn, md, mx) in enumerate(MER, 19):
    c(rf, f"A{i}", comp)
    c(rf, f"B{i}", nome)
    c(rf, f"C{i}", n, F_TXT, N0)
    c(rf, f"D{i}", mn, F_TXT, R2)
    c(rf, f"E{i}", md, F_TXT, R2)
    c(rf, f"F{i}", mx)
c(rf, "A24", "O detalhe, linha a linha, está em dados/precos.md. Preço de varejo é teto de referência, não piso: o "
  "volume de 6.500 OCIs por polo é o argumento para baixar.", F_SUB, borda=False)
rf.merge_cells("A24:F24")
rf.row_dimensions[24].height = 30

# ================================================================== Leia
c(leia, "A1", "Teto da OCI de câncer gástrico: o que dá para pagar às clínicas", F_TIT, borda=False)
TXT = [
    "Controle interno do ISHP: não vai ao plano nem às clínicas.",
    "Objeto: OCI 09.01.01.007-3, Avaliação Diagnóstica de Câncer Gástrico, 13.012 OCIs a R$ 600,11 em 2 polos "
    "(Taguatinga e CONIC), dez/2026 a jul/2027. Plano assinado em 01/10/2026 (processo SEI 00060-00367596/2026-59).",
    "Células amarelas com número azul são premissas ou cotação: mude e o resto se refaz. Número verde vem de outra aba. "
    "Cinza é o resultado para levar à negociação.",
    "Premissas: o valor da OCI, a meta, a taxa de biópsia, o retorno por teleconsulta, a conclusão, a reserva do ISHP.",
    "A pacote: a clínica entrega a OCI inteira. Teto técnico e a tabela de ofertas em % do valor.",
    "B componentes: preço de cada peça (consulta, exame com sedação, anatomopatológico, retorno). Diz até quanto se paga "
    "pelo exame, com a sensibilidade à taxa de biópsia e ao preço do anatomopatológico.",
    "C equipe própria: o desenho do plano, com estrutura alugada e equipe contratada. Diz até quanto se paga de aluguel.",
    "Volume: as OCIs e o dinheiro de cada mês.",
    "Referências: o que o SUS e a SES-DF pagam por cada peça e o varejo.",
    "O estudo completo está em estudos/precificacao_oci_20261021.md; os preços linha a linha, em dados/precos.md.",
]
for i, t in enumerate(TXT, 3):
    c(leia, f"A{i}", t, F_TXT, borda=False)
leia.column_dimensions["A"].width = 120
for i in range(3, 3 + len(TXT)):
    leia.row_dimensions[i].height = 30
pr["B5"].comment = Comment("Exemplo do formato: R$ 600,11 é o valor da tabela em 10/2026.", "estudo")

for ws in wb.worksheets:
    ws.sheet_view.showGridLines = False
    ws.freeze_panes = None

wb.save(sys.argv[1])
print("gravado", sys.argv[1])
