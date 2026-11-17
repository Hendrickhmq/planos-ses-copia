import json, re, sys
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter as L
from openpyxl.comments import Comment

P = sys.argv[1]; OUT = sys.argv[2]
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

EX = [  # código, nome, modalidade
    ('02.04.03.018-8', 'Mamografia bilateral (rastreamento)', 'radiologia'),
    ('02.05.02.016-0', 'US pélvica (ginecológica)', 'ultrassonografia'),
    ('02.05.02.007-0', 'US de bolsa escrotal', 'ultrassonografia'),
    ('02.05.02.008-9', 'US de globo ocular / órbita', 'ultrassonografia'),
    ('02.05.02.017-8', 'US transfontanela', 'ultrassonografia'),
    ('02.05.02.015-1', 'US obstétrica com doppler', 'ultrassonografia'),
    ('02.06.01.005-2', 'TC de pescoço', 'tomografia'),
    ('02.06.01.007-9', 'TC de crânio', 'tomografia'),
    ('02.06.01.004-4', 'TC de face / seios da face / ATM', 'tomografia'),
]
key = lambda c: c.replace('.', '').replace('-', '').lstrip('0')

F = 'Arial'
fn = lambda **k: Font(name=F, **k)
BLUE = '0000FF'; GREEN = '008000'
head_fill = PatternFill('solid', start_color='1F3864'); head_font = fn(bold=True, color='FFFFFF')
sub_fill = PatternFill('solid', start_color='D9E1F2'); yellow = PatternFill('solid', start_color='FFFF00')
tot_fill = PatternFill('solid', start_color='F2F2F2')
thin = Side(style='thin', color='BFBFBF'); box = Border(left=thin, right=thin, top=thin, bottom=thin)
BRL = '"R$" #,##0.00;("R$" #,##0.00);"-"'; INT = '#,##0;(#,##0);"-"'; PCT = '0%;(0%);"-"'

def cab(ws, row, nomes, larg=None):
    for j, t in enumerate(nomes, 1):
        c = ws.cell(row=row, column=j, value=t); c.font = head_font; c.fill = head_fill
        c.alignment = Alignment(wrap_text=True, vertical='center', horizontal='center'); c.border = box
    ws.row_dimensions[row].height = 45
    if larg:
        for j, w in enumerate(larg, 1): ws.column_dimensions[L(j)].width = w

def put(ws, ref, v, fmt=None, color=None, bold=False, fill=None):
    c = ws[ref]; c.value = v; c.font = fn(color=color, bold=bold) if (color or bold) else fn()
    if fmt: c.number_format = fmt
    if fill: c.fill = fill
    c.border = box
    return c

wb = Workbook()
# ---------- Premissas
ws = wb.active; ws.title = 'Premissas'
ws.column_dimensions['A'].width = 46; ws.column_dimensions['B'].width = 20; ws.column_dimensions['C'].width = 80
ws['A1'] = 'Emenda de imagem — cenários de aplicação (controle interno)'; ws['A1'].font = fn(bold=True, size=14)
ws['A2'] = 'Edite só as células em amarelo. Todo o resto é calculado.'; ws['A2'].font = fn(italic=True)
cab(ws, 4, ['Premissa', 'Valor', 'Fonte / nota'])
put(ws, 'A5', 'Recurso da emenda'); put(ws, 'B5', 1502687.00, BRL, BLUE, fill=yellow)
put(ws, 'C5', 'Bancada do DF 71080005, OGU 2025, proposta 36000722999202500 (federal) — a mesma emenda do redacao_05; estado.yaml')
put(ws, 'A6', 'Gestão e apoio — cenário "com apoio" (% do recurso)'); put(ws, 'B6', 0.10, PCT, BLUE, fill=yellow)
put(ws, 'C6', 'A decidir. 10% é o teto que o usuário fixou para a mesma emenda no otorrino (08/10/2026). Mude aqui e tudo recalcula.')
put(ws, 'A7', 'Para exames — sem apoio'); put(ws, 'B7', '=B5', BRL)
put(ws, 'C7', 'Todo o recurso em exames')
put(ws, 'A8', 'Para exames — com apoio'); put(ws, 'B8', '=ROUND(B5*(1-B6),2)', BRL)
put(ws, 'C8', 'Recurso menos gestão e apoio')
for r in range(5, 9): ws[f'C{r}'].alignment = Alignment(wrap_text=True)

# ---------- Filas
wf = wb.create_sheet('Filas')
wf['A1'] = 'As nove filas — Mapa Social (base de 15/10/2026 19:32), valor da emenda e mercado do DF'; wf['A1'].font = fn(bold=True, size=13)
H = ['Código SIGTAP', 'Exame', 'Modalidade', 'Fila (pedidos)', 'Pessoas', 'Espera média (dias)', 'Espera mediana (dias)',
     'Agendados por mês em 2026', 'Meses para a rede zerar sozinha', 'Valor SIGTAP (R$)', 'Incremento (Portaria 4.282)',
     'Valor pago por exame (R$)', 'Custo para zerar a fila (R$)', 'Mercado DF — menor preço (R$)', 'Mercado DF — mediana (R$)',
     'Cobertura (valor ÷ menor preço)']
cab(wf, 3, H, [16, 34, 16, 12, 11, 11, 11, 12, 12, 12, 13, 13, 16, 14, 14, 13])
R0 = 4
for i, (cod, nome, mod) in enumerate(EX):
    r = R0 + i; c = cand[key(cod)]; sig, inc = tab[cod]
    put(wf, f'A{r}', cod); put(wf, f'B{r}', nome); put(wf, f'C{r}', mod)
    put(wf, f'D{r}', c['fila'], INT, BLUE); put(wf, f'E{r}', c['pessoas'], INT, BLUE)
    put(wf, f'F{r}', round(c['espera_media']), INT, BLUE); put(wf, f'G{r}', round(c['espera_mediana']), INT, BLUE)
    put(wf, f'H{r}', round(ag.get(key(cod), 0) / 9), INT, BLUE)
    put(wf, f'I{r}', f'=IF(H{r}>0,D{r}/H{r},"-")', '0.0')
    put(wf, f'J{r}', sig, BRL, BLUE); put(wf, f'K{r}', inc, '0%', BLUE)
    put(wf, f'L{r}', f'=ROUNDDOWN(ROUND(J{r}*(1+K{r}),6),2)', BRL)
    put(wf, f'M{r}', f'=D{r}*L{r}', BRL)
    if cod in merc:
        put(wf, f'N{r}', merc[cod][0], BRL, BLUE); put(wf, f'O{r}', merc[cod][1], BRL, BLUE)
        put(wf, f'P{r}', f'=L{r}/N{r}', PCT)
    else:
        put(wf, f'N{r}', 'a pesquisar'); put(wf, f'O{r}', 'a pesquisar'); put(wf, f'P{r}', '-')
RN = R0 + len(EX) - 1; rt = RN + 1
put(wf, f'B{rt}', 'Total das nove filas', bold=True, fill=tot_fill)
for col in 'DM':
    put(wf, f'{col}{rt}', f'=SUM({col}{R0}:{col}{RN})', BRL if col == 'M' else INT, bold=True, fill=tot_fill)
put(wf, f'E{rt}', 'não se soma', fill=tot_fill)
wf[f'E{rt}'].comment = Comment('A mesma pessoa pode estar em mais de uma fila; somar pessoas de filas diferentes conta duas vezes.', 'planos-ses')
nota = rt + 2
for k, t in enumerate([
    'Fila, pessoas, espera e agendados: Mapa Social da Saúde (MPDFT), coleta do agente mapa-social, recarga de 15/10/2026 19:32 — planos/redacao_07/dados/fontes/mapa_social_20261015.md.',
    'Valor pago: valor SIGTAP × (1 + incremento do Anexo I da Portaria SAES/MS 4.282/2026), centavo truncado — a regra do plano 4 (dados/valor_unitario.md; fichas SIGTAP 10/2026).',
    'Mercado: menor preço e mediana do DF, Doctoralia e Medprev, 16/10/2026 — dados/precos.md. A mamografia ainda não foi pesquisada.',
    'Agendados por mês = agendamentos de jan. a set. de 2026 ÷ 9. "Meses para a rede zerar" ignora os pedidos novos que continuam entrando.',
    'Tomografias: nenhum anúncio diz se inclui contraste; a emenda paga o exame com o contraste dentro. Só 2 ou 3 preços no DF — depende de cotação.',
    'US obstétrica com doppler: nenhum preço achado abaixo do valor pago (cobertura de 64%).',
    'Mamografia (ficha SIGTAP 10/2026): o código 02.04.03.018-8 é de rastreamento — mulheres sem sintomas, sem nódulo, a partir de 35 anos. A fila inclui 187 pedidos da fila "diagnóstica" e casos de nódulo (CID N63), que a descrição do código não cobre. A mamografia diagnóstica (02.04.03.003-0, R$ 22,50) não tem incremento.',
    'Números em azul vêm das fontes; em preto, são calculados.']):
    wf.cell(row=nota + k, column=1, value=t).font = fn(italic=True, size=9)
wf.freeze_panes = 'C4'

# ---------- cenários
def cenario(nome, titulo, ordem, desc):
    w = wb.create_sheet(nome)
    w['A1'] = titulo; w['A1'].font = fn(bold=True, size=13)
    w['A2'] = desc; w['A2'].font = fn(italic=True)
    w['A3'] = 'Cada fila recebe o que sobra da anterior; quando uma zera, o saldo passa para a próxima.'; w['A3'].font = fn(italic=True, size=9)
    # bloco de cabeçalho em dois níveis
    w.merge_cells('I5:M5'); w.merge_cells('N5:R5')
    for ref, t in (('I5', 'SEM APOIO — todo o recurso em exames'), ('N5', 'COM APOIO — recurso menos gestão e apoio (Premissas)')):
        c = w[ref]; c.value = t; c.font = head_font; c.fill = PatternFill('solid', start_color='2F5597'); c.alignment = Alignment(horizontal='center')
    sub = ['Saldo antes (R$)', 'Exames atendidos', '% da fila atendida', 'Valor pago (R$)', 'Zera a fila?']
    cab(w, 6, ['Ordem', 'Código SIGTAP', 'Exame', 'Fila (pedidos)', 'Pessoas', 'Espera média (dias)', 'Valor pago por exame (R$)',
               'Custo para zerar (R$)'] + sub + sub,
        [7, 15, 32, 11, 10, 10, 12, 15, 15, 11, 10, 15, 9, 15, 11, 10, 15, 9])
    r0 = 7
    for i, cod in enumerate(ordem):
        r = r0 + i
        m = f'MATCH($B{r},Filas!$A${R0}:$A${RN},0)'
        put(w, f'A{r}', i + 1, '0'); put(w, f'B{r}', cod)
        for col, src, fmt in (('C', 'B', None), ('D', 'D', INT), ('E', 'E', INT), ('F', 'F', INT), ('G', 'L', BRL), ('H', 'M', BRL)):
            put(w, f'{col}{r}', f'=INDEX(Filas!${src}${R0}:${src}${RN},{m})', fmt, GREEN)
        for s0, rec in (('I', 'Premissas!$B$7'), ('N', 'Premissas!$B$8')):
            i0 = ord(s0) - 65
            S, E, Pc, V, Z = (L(i0 + 1 + k) for k in range(5))
            put(w, f'{S}{r}', f'={rec}' if i == 0 else f'={S}{r-1}-{V}{r-1}', BRL, GREEN if i == 0 else None)
            put(w, f'{E}{r}', f'=MIN(D{r},INT(ROUND({S}{r}/G{r},6)))', INT)
            put(w, f'{Pc}{r}', f'=IF(D{r}>0,{E}{r}/D{r},0)', PCT)
            put(w, f'{V}{r}', f'=ROUND({E}{r}*G{r},2)', BRL)
            put(w, f'{Z}{r}', f'=IF({E}{r}=D{r},"sim","não")')
            w[f'{Z}{r}'].alignment = Alignment(horizontal='center')
    rn = r0 + len(ordem) - 1; t = rn + 1
    put(w, f'C{t}', 'Total', bold=True, fill=tot_fill)
    put(w, f'D{t}', f'=SUM(D{r0}:D{rn})', INT, bold=True, fill=tot_fill)
    put(w, f'H{t}', f'=SUM(H{r0}:H{rn})', BRL, bold=True, fill=tot_fill)
    for s0 in ('I', 'N'):
        i0 = ord(s0) - 65; S, E, Pc, V, Z = (L(i0 + 1 + k) for k in range(5))
        put(w, f'{E}{t}', f'=SUM({E}{r0}:{E}{rn})', INT, bold=True, fill=tot_fill)
        put(w, f'{Pc}{t}', f'=IF(D{t}>0,{E}{t}/D{t},0)', PCT, bold=True, fill=tot_fill)
        put(w, f'{V}{t}', f'=SUM({V}{r0}:{V}{rn})', BRL, bold=True, fill=tot_fill)
        put(w, f'{Z}{t}', f'=COUNTIF({Z}{r0}:{Z}{rn},"sim")', '0 "zeradas"', bold=True, fill=tot_fill)
        put(w, f'{S}{t+1}', 'Sobra', bold=True)
        put(w, f'{V}{t+1}', f'={S}{rn}-{V}{rn}', BRL, bold=True)
    w.freeze_panes = 'D7'
    return w, r0, rn, t

FILAS_OUTROS = [c for c, _, _ in EX[1:]]
w1 = cenario('Mamografia primeiro', 'Cenário 1 — mamografia primeiro', [EX[0][0]] + FILAS_OUTROS,
             'Zera a mamografia; o saldo vai para os cinco ultrassons e depois para as tomografias (escolha do usuário em 16/10/2026).')
w2 = cenario('Outros primeiro', 'Cenário 2 — ultrassons e tomografias primeiro, mamografia por último', FILAS_OUTROS + [EX[0][0]],
             'Zera os cinco ultrassons e as três tomografias; o saldo vai para a mamografia (variante A3).')

# ---------- Comparativo
wc = wb.create_sheet('Comparativo', 1)
wc['A1'] = 'Comparativo dos dois cenários'; wc['A1'].font = fn(bold=True, size=13)
wc['A2'] = 'Tudo vem das abas dos cenários; mude o recurso ou o apoio em Premissas.'; wc['A2'].font = fn(italic=True)
cab(wc, 4, ['', 'Mamografia primeiro — sem apoio', 'Mamografia primeiro — com apoio', 'Outros primeiro — sem apoio', 'Outros primeiro — com apoio'],
    [34, 20, 20, 20, 20])
refs = []
for (w, r0, rn, t), nm in ((w1, 'Mamografia primeiro'), (w2, 'Outros primeiro')):
    for s0 in ('I', 'N'):
        i0 = ord(s0) - 65; refs.append((nm, t, *(L(i0 + 1 + k) for k in range(5))))
linhas = [('Exames atendidos', lambda q: f"='{q[0]}'!{q[3]}{q[1]}", INT),
          ('% dos pedidos das nove filas', lambda q: f"='{q[0]}'!{q[4]}{q[1]}", PCT),
          ('Filas zeradas (de 9)', lambda q: f"='{q[0]}'!{q[6]}{q[1]}", '0'),
          ('Valor aplicado em exames (R$)', lambda q: f"='{q[0]}'!{q[5]}{q[1]}", BRL),
          ('Sobra (R$)', lambda q: f"='{q[0]}'!{q[5]}{q[1]+1}", BRL)]
for k, (rot, f, fmt) in enumerate(linhas):
    r = 5 + k; put(wc, f'A{r}', rot, bold=True)
    for j, q in enumerate(refs): put(wc, f'{L(j+2)}{r}', f(q), fmt, GREEN)
r = 11
put(wc, f'A{r}', 'Exames atendidos por fila', bold=True, fill=sub_fill)
for j in range(4): put(wc, f'{L(j+2)}{r}', '', fill=sub_fill)
for i, (cod, nome, _) in enumerate(EX):
    rr = r + 1 + i; put(wc, f'A{rr}', nome)
    for j, (nm, t, S, E, Pc, V, Z) in enumerate(refs):
        r0 = 7; rn = t - 1
        put(wc, f'{L(j+2)}{rr}', f"=INDEX('{nm}'!{E}{r0}:{E}{rn},MATCH(\"{cod}\",'{nm}'!B{r0}:B{rn},0))", INT, GREEN)
rr = r + len(EX) + 1
put(wc, f'A{rr}', '% da fila de cada exame', bold=True, fill=sub_fill)
for j in range(4): put(wc, f'{L(j+2)}{rr}', '', fill=sub_fill)
for i, (cod, nome, _) in enumerate(EX):
    q = rr + 1 + i; put(wc, f'A{q}', nome)
    for j, (nm, t, S, E, Pc, V, Z) in enumerate(refs):
        r0 = 7; rn = t - 1
        put(wc, f'{L(j+2)}{q}', f"=INDEX('{nm}'!{Pc}{r0}:{Pc}{rn},MATCH(\"{cod}\",'{nm}'!B{r0}:B{rn},0))", PCT, GREEN)

for w in wb.worksheets:
    for row in w.iter_rows():
        for c in row:
            if c.font is None or c.font.name != F:
                c.font = Font(name=F, bold=c.font.bold if c.font else False, italic=c.font.italic if c.font else False,
                              size=c.font.size if c.font else 11, color=c.font.color if c.font else None)
wb.save(OUT); print('ok', OUT)
