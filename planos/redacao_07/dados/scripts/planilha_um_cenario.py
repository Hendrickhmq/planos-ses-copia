"""Uma planilha por cenário, com 10% de gestão e apoio (usuário, 16/10/2026).
Uso, da raiz do repositório: python3 planos/redacao_07/dados/scripts/planilha_um_cenario.py planos/redacao_07
"""
import json, re, sys
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter as L

P = sys.argv[1]
d = json.load(open(f'{P}/dados/fontes/mapa_social_20261015_bruto/coleta_20261015.json'))
cols = d['por_codigo_cols']; cand = {r[0]: dict(zip(cols, r)) for r in d['por_codigo']['cand']}
ag = {r[0]: r[1] for r in d['agendadas_jan_set_2026_por_codigo']}
tab = {}
for l in open(f'{P}/dados/valor_unitario.md', encoding='utf-8'):
    m = re.match(r'\| (\d{2}\.\d{2}\.\d{2}\.\d{3}-\d) \| (.*?) \| .*? \| R\$ ([\d.,]+) \| (\d+)% \|', l)
    if m: tab[m.group(1)] = (float(m.group(3).replace('.', '').replace(',', '.')), int(m.group(4)) / 100)
merc = {}; sec = None
for l in open(f'{P}/dados/precos.md', encoding='utf-8'):
    if l.startswith('## '): sec = l[3]
    c = [x.strip() for x in l.strip().strip('|').split('|')]
    if sec == '5' and re.match(r'\d{2}\.\d{2}', c[0]) and c[1] == 'DF':
        num = lambda s: float(s.replace('R$', '').replace('.', '').replace(',', '.'))
        merc[c[0]] = (num(c[3]), num(c[4]))

MAMO = ('02.04.03.018-8', 'Mamografia bilateral (rastreamento)', 'radiologia')
OUTROS = [('02.05.02.016-0', 'US pélvica (ginecológica)', 'ultrassonografia'),
          ('02.05.02.007-0', 'US de bolsa escrotal', 'ultrassonografia'),
          ('02.05.02.008-9', 'US de globo ocular / órbita', 'ultrassonografia'),
          ('02.05.02.017-8', 'US transfontanela', 'ultrassonografia'),
          ('02.05.02.015-1', 'US obstétrica com doppler', 'ultrassonografia'),
          ('02.06.01.005-2', 'TC de pescoço', 'tomografia'),
          ('02.06.01.007-9', 'TC de crânio', 'tomografia'),
          ('02.06.01.004-4', 'TC de face / seios da face / ATM', 'tomografia')]
DENSI = ('02.04.06.002-8', 'Densitometria óssea (coluna e/ou fêmur)', 'radiologia')
key = lambda c: c.replace('.', '').replace('-', '').lstrip('0')

F = 'Arial'; BLUE = '0000FF'; GREEN = '008000'
fn = lambda **k: Font(name=F, **k)
HF = PatternFill('solid', start_color='1F3864'); YEL = PatternFill('solid', start_color='FFFF00')
TOT = PatternFill('solid', start_color='F2F2F2'); SUB = PatternFill('solid', start_color='D9E1F2')
thin = Side(style='thin', color='BFBFBF'); box = Border(left=thin, right=thin, top=thin, bottom=thin)
BRL = '"R$" #,##0.00;("R$" #,##0.00);"-"'; INT = '#,##0;(#,##0);"-"'; PCT = '0%;(0%);"-"'

def put(ws, ref, v, fmt=None, color=None, bold=False, fill=None, wrap=False):
    c = ws[ref]; c.value = v; c.font = fn(color=color, bold=bold); c.border = box
    if fmt: c.number_format = fmt
    if fill: c.fill = fill
    if wrap: c.alignment = Alignment(wrap_text=True, vertical='top')
    return c

def cab(ws, row, nomes, larg):
    for j, t in enumerate(nomes, 1):
        c = ws.cell(row=row, column=j, value=t); c.font = fn(bold=True, color='FFFFFF'); c.fill = HF; c.border = box
        c.alignment = Alignment(wrap_text=True, vertical='center', horizontal='center')
    ws.row_dimensions[row].height = 48
    for j, w in enumerate(larg, 1): ws.column_dimensions[L(j)].width = w

def monta(arquivo, titulo, desc, ordem):
    wb = Workbook()
    # ---- Resumo
    wr = wb.active; wr.title = 'Resumo'
    for col, w in zip('ABC', (44, 20, 70)): wr.column_dimensions[col].width = w
    wr['A1'] = titulo; wr['A1'].font = fn(bold=True, size=14)
    wr['A2'] = desc; wr['A2'].font = fn(italic=True)
    cab(wr, 4, ['Item', 'Valor', 'Fonte / nota'], [44, 20, 70])
    put(wr, 'A5', 'Recurso da emenda'); put(wr, 'B5', 1502687.00, BRL, BLUE)
    put(wr, 'C5', 'Emenda de Bancada do DF 71080005, OGU 2025, proposta 36000722999202500 (federal)', wrap=True)
    put(wr, 'A6', 'Gestão e apoio (% do recurso)'); put(wr, 'B6', 0.10, PCT, BLUE, fill=YEL)
    put(wr, 'C6', '10% por decisão do usuário em 16/10/2026. Mude aqui e a planilha recalcula.', wrap=True)
    put(wr, 'A7', 'Gestão e apoio (R$)'); put(wr, 'B7', '=ROUND(B5*B6,2)', BRL)
    put(wr, 'A8', 'Para exames (R$)', bold=True); put(wr, 'B8', '=B5-B7', BRL, bold=True)
    # ---- Detalhe
    wd = wb.create_sheet('Detalhe por fila')
    wd['A1'] = f'{titulo} — detalhe por fila'; wd['A1'].font = fn(bold=True, size=13)
    wd['A2'] = 'Cada fila recebe o saldo da anterior; quando zera, o que sobra passa para a próxima. Exames atendidos = o menor entre a fila e o que o saldo compra.'
    wd['A2'].font = fn(italic=True, size=9)
    H = ['Ordem', 'Código SIGTAP', 'Exame', 'Modalidade', 'Fila (pedidos)', 'Pessoas na fila', 'Espera média (dias)',
         'Espera mediana (dias)', 'Agendados por mês em 2026 (rede SES)', 'Valor SIGTAP (R$)', 'Incremento (Portaria 4.282)',
         'Valor pago por exame (R$)', 'Custo para zerar a fila (R$)', 'Saldo antes (R$)', 'Atendimentos (exames)',
         '% da fila atendida', 'Pedidos que ficam na fila', 'Valor pago (R$)', 'Zera a fila?', 'Saldo depois (R$)',
         '% do recurso para exames', 'Mercado DF — menor preço (R$)', 'Mercado DF — mediana (R$)', 'Cobertura (valor ÷ menor preço)']
    cab(wd, 4, H, [7, 15, 32, 15, 11, 11, 10, 10, 12, 11, 12, 12, 15, 15, 12, 10, 12, 15, 9, 15, 11, 13, 13, 12])
    r0 = 5
    for i, (cod, nome, mod) in enumerate(ordem):
        r = r0 + i; c = cand[key(cod)]; sig, inc = tab[cod]
        put(wd, f'A{r}', i + 1, '0'); put(wd, f'B{r}', cod); put(wd, f'C{r}', nome); put(wd, f'D{r}', mod)
        put(wd, f'E{r}', c['fila'], INT, BLUE); put(wd, f'F{r}', c['pessoas'], INT, BLUE)
        put(wd, f'G{r}', round(c['espera_media']), INT, BLUE); put(wd, f'H{r}', round(c['espera_mediana']), INT, BLUE)
        put(wd, f'I{r}', round(ag.get(key(cod), 0) / 9), INT, BLUE)
        put(wd, f'J{r}', sig, BRL, BLUE); put(wd, f'K{r}', inc, '0%', BLUE)
        put(wd, f'L{r}', f'=ROUNDDOWN(ROUND(J{r}*(1+K{r}),6),2)', BRL)
        put(wd, f'M{r}', f'=E{r}*L{r}', BRL)
        put(wd, f'N{r}', '=Resumo!$B$8' if i == 0 else f'=T{r-1}', BRL, GREEN if i == 0 else None)
        put(wd, f'O{r}', f'=MIN(E{r},INT(ROUND(N{r}/L{r},6)))', INT, bold=True)
        put(wd, f'P{r}', f'=IF(E{r}>0,O{r}/E{r},0)', PCT)
        put(wd, f'Q{r}', f'=E{r}-O{r}', INT)
        put(wd, f'R{r}', f'=ROUND(O{r}*L{r},2)', BRL, bold=True)
        put(wd, f'S{r}', f'=IF(O{r}=E{r},"sim","não")'); wd[f'S{r}'].alignment = Alignment(horizontal='center')
        put(wd, f'T{r}', f'=N{r}-R{r}', BRL)
        put(wd, f'U{r}', f'=R{r}/Resumo!$B$8', PCT)
        if cod in merc:
            put(wd, f'V{r}', merc[cod][0], BRL, BLUE); put(wd, f'W{r}', merc[cod][1], BRL, BLUE); put(wd, f'X{r}', f'=L{r}/V{r}', PCT)
        else:
            put(wd, f'V{r}', 'não pesquisado'); put(wd, f'W{r}', 'não pesquisado'); put(wd, f'X{r}', '-')
    rn = r0 + len(ordem) - 1; t = rn + 1
    put(wd, f'C{t}', 'Total', bold=True, fill=TOT)
    for col, fmt in (('E', INT), ('M', BRL), ('O', INT), ('Q', INT), ('R', BRL), ('U', PCT)):
        put(wd, f'{col}{t}', f'=SUM({col}{r0}:{col}{rn})', fmt, bold=True, fill=TOT)
    put(wd, f'P{t}', f'=O{t}/E{t}', PCT, bold=True, fill=TOT)
    put(wd, f'S{t}', f'=COUNTIF(S{r0}:S{rn},"sim")', '0 "zeradas"', bold=True, fill=TOT)
    put(wd, f'F{t}', 'não se soma', fill=TOT)
    wd.freeze_panes = 'D5'
    # resumo: totais
    linhas = [('Atendimentos (exames)', f"='Detalhe por fila'!O{t}", INT),
              (f'Pedidos nas {len(ordem)} filas', f"='Detalhe por fila'!E{t}", INT),
              ('% dos pedidos atendidos', f"='Detalhe por fila'!P{t}", PCT),
              (f'Filas zeradas (de {len(ordem)})', f"='Detalhe por fila'!S{t}", '0'),
              ('Valor pago em exames (R$)', f"='Detalhe por fila'!R{t}", BRL),
              ('Sobra não aplicada (R$)', f"=B8-'Detalhe por fila'!R{t}", BRL),
              ('Valor total programado — exames + gestão e apoio (R$)', f"='Detalhe por fila'!R{t}+B7", BRL)]
    for k, (rot, f, fmt) in enumerate(linhas):
        r = 10 + k; put(wr, f'A{r}', rot, bold=True); put(wr, f'B{r}', f, fmt, GREEN)
    put(wr, 'C15', 'Menor que o valor de um exame; fica sem aplicar', wrap=True)
    r = 18
    put(wr, f'A{r}', 'Por fila', bold=True, fill=SUB); put(wr, f'B{r}', 'Atendimentos', bold=True, fill=SUB)
    put(wr, f'C{r}', 'Valor pago (R$)', bold=True, fill=SUB); put(wr, f'D{r}', '% da fila', bold=True, fill=SUB); wr.column_dimensions['D'].width = 12
    for i in range(len(ordem)):
        rr = r + 1 + i; src = r0 + i
        put(wr, f'A{rr}', f"='Detalhe por fila'!C{src}", None, GREEN)
        put(wr, f'B{rr}', f"='Detalhe por fila'!O{src}", INT, GREEN)
        put(wr, f'C{rr}', f"='Detalhe por fila'!R{src}", BRL, GREEN)
        put(wr, f'D{rr}', f"='Detalhe por fila'!P{src}", PCT, GREEN)
    # ---- Notas
    wn = wb.create_sheet('Fontes e notas'); wn.column_dimensions['A'].width = 140
    wn['A1'] = 'Fontes e notas'; wn['A1'].font = fn(bold=True, size=13)
    for k, txt in enumerate([
        'FILA: Mapa Social da Saúde (MPDFT), base recarregada em 15/10/2026 19:32 — coleta do agente mapa-social (planos/redacao_07/dados/fontes/mapa_social_20261015.md). Fila = pedidos pendentes de regulação (três status); devolvidas ficam fora.',
        'PESSOAS: CNS distintos em cada fila. Não se somam entre filas: a mesma pessoa pode esperar mais de um exame.',
        'AGENDADOS POR MÊS: agendamentos de janeiro a setembro de 2026 ÷ 9, todas as unidades da rede.',
        'VALOR PAGO POR EXAME: valor SIGTAP × (1 + incremento do Anexo I da Portaria SAES/MS 4.282/2026), com o centavo truncado — a regra do plano 4. Fichas SIGTAP de 10/2026 em dados/fontes/.',
        'ZERAR: atender todos os pedidos da fila medida em 15/10/2026. Pedidos novos continuam entrando depois.',
        'GESTÃO E APOIO: 10% do recurso, por decisão do usuário em 16/10/2026.',
        'MERCADO DF: menor preço e mediana de Doctoralia e Medprev, pesquisa de 16/10/2026 (dados/precos.md). Controle interno — não vai ao documento. Mamografia: 5 preços no DF, incluídos em 16/10/2026.',
        'TOMOGRAFIAS: a emenda paga o exame com o contraste dentro (o contraste não gera pagamento à parte). Nenhum anúncio do DF diz se inclui contraste; só 2 ou 3 preços — depende de cotação.',
        'US OBSTÉTRICA COM DOPPLER: nenhum preço achado abaixo do valor pago (cobertura de 64%).',
        'MAMOGRAFIA: o código 02.04.03.018-8 é de rastreamento (sem sintomas, sem nódulo, a partir de 35 anos). A fila inclui 187 pedidos da fila "diagnóstica" e casos de nódulo (CID N63), que a descrição do código não cobre. A diagnóstica (02.04.03.003-0, R$ 22,50) não tem incremento.',
        'CORES: azul = número das fontes; preto = calculado; verde = vem de outra aba; amarelo = premissa que se pode mudar.']):
        c = wn.cell(row=3 + k, column=1, value=txt); c.font = fn(); c.alignment = Alignment(wrap_text=True, vertical='top')
    wb.save(arquivo); print('ok', arquivo)

monta(f'{P}/cenario_1_mamografia_primeiro.xlsx', 'Cenário 1 — mamografia primeiro',
      'Zera a mamografia; o saldo vai para os cinco ultrassons e depois para as tomografias. 10% de gestão e apoio.', [MAMO] + OUTROS)
monta(f'{P}/cenario_2_outros_primeiro.xlsx', 'Cenário 2 — ultrassons e tomografias primeiro, mamografia por último',
      'Zera os cinco ultrassons e as três tomografias; o saldo vai para a mamografia. 10% de gestão e apoio.', OUTROS + [MAMO])
monta(f'{P}/cenario_3_mamografia_ultrassom_densitometria.xlsx', 'Cenário 3 — mamografia, ultrassons e densitometria, sem tomografia',
      'Zera a mamografia e os cinco ultrassons; o saldo vai para a densitometria óssea. Sem tomografia. 10% de gestão e apoio.',
      [MAMO] + OUTROS[:5] + [DENSI])

# Usuário, 20/10/2026: as dez filas de espera longa primeiro, na ordem da espera; mamografia e densitometria de reserva.
OBST = ('02.05.02.014-3', 'US obstétrica', 'ultrassonografia')
SELA = ('02.06.01.006-0', 'TC de sela túrcica', 'tomografia')
POR_ESPERA = [OUTROS[0], OUTROS[1], OUTROS[3], OUTROS[2], OUTROS[6], OUTROS[4], SELA, OBST, OUTROS[5], OUTROS[7]]
monta(f'{P}/cenario_4_espera_longa_com_reserva.xlsx',
      'Cenário 4 — as dez filas de espera longa, com mamografia e densitometria de reserva',
      'Zera as dez filas na ordem da espera média; o saldo vai para a mamografia e, depois, para a densitometria, que ficam de reserva porque a rede já dá conta delas. 10% de gestão e apoio.',
      POR_ESPERA + [MAMO, DENSI])
