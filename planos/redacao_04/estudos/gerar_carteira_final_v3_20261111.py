"""Planilha da carteira final do plano 4, versão 3 (11/11/2026): a versão simples.

A pedido do usuário: cada exame com modalidade, código SIGTAP, fila, o que vamos atender, os exames novos e o preço;
todas as filas escolhidas destrinchadas pelo nome; a condição do Doppler de membros; as saídas, com a escolhida.
As abas Não escolhidos e Estudos das filas vêm da versão 2 sem mudança (o gerador da v2 roda primeiro).

Rodar da pasta planos/redacao_04:
    python3 estudos/gerar_carteira_final_v3_20261111.py
"""
import json
import os
import sys

import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

sys.path.insert(0, 'estudos')
import gerar_carteira_final_v2_20261111 as v2  # noqa: E402

SAIDA = 'estudos/carteira_final_v3_20261111.xlsx'
TEMP = 'estudos/_temp_v2_para_v3.xlsx'
FILAS = 'estudos/estudo_filas_imagem_20261102.json'
ALVO = 10636602
EXTRA = {'US de abdômen superior': 1}  # um exame a mais para chegar mais perto do valor pedido (usuário, 11/11)
PARTE_SES = 0.081  # parte do que a SES realiza nos 7 exames fáceis que a rede do plano assume (11/11)

NEGRITO = Font(bold=True)
CAB = PatternFill('solid', fgColor='1F4E78')
CAB_FONTE = Font(bold=True, color='FFFFFF')
SUB = PatternFill('solid', fgColor='DDEBF7')
AMARELO = PatternFill('solid', fgColor='FFF2CC')
VERDE = PatternFill('solid', fgColor='E2EFDA')
CINZA = PatternFill('solid', fgColor='EDEDED')
MOEDA = 'R$ #,##0.00'
INT = '#,##0'
PCT = '0%'
QUEBRA = Alignment(wrap_text=True, vertical='top')

US_DOP = '02.05.01.004-0'
MEMBROS = ['ULTRA-SONOGRAFIA DOPPLER VENOSO - MMII ( BILATERAL)', 'ULTRA-SONOGRAFIA DOPPLER ARTERIAL - MMII (BILATERAL)',
           'ULTRA-SONOGRAFIA DOPPLER VENOSO - MMSS ( BILATERAL)', 'ULTRA-SONOGRAFIA DOPPLER ARTERIAL - MMSS (BILATERAL)']
CAROTIDAS = ['10. ECODOPPLER DE CAROTIDAS', 'ULTRA-SONOGRAFIA  DOPPLER DE CAROTIDAS E VERTEBRAIS',
             'ULTRA-SONOGRAFIA DOPPLER COLORIDO DE VASOS', 'ECOGRAFIA TRANSVAGINAL COM DOPPLER',
             'ULTRASSONOGRAFIA COM DOPPLER COLORIDO DE ARTERIAS RENAIS']

# (exame, modalidade, código, preço, filas pelo nome, ajuste da fila, dem: código da demanda ou None, condição)
# ajuste: pedidos que saem de uma fila (nome → quantos), com o motivo
EXAMES = [
    ('US de abdômen total (adulto)', 'Ultrassom', '02.05.02.004-6', 117.51, ['ECOGRAFIA DE ABDOMEN TOTAL ADULTO'], {}, '02.05.02.004-6', ''),
    ('US de parede abdominal', 'Ultrassom', '02.05.02.004-6', 117.51, ['ULTRASONOGRAFIA DE PAREDE ABDOMINAL'], {}, None,
     'a SES ainda precisa confirmar por escrito o código do abdômen total (L-007)'),
    ('US de abdômen total (criança)', 'Ultrassom', '02.05.02.004-6', 117.51, ['ECOGRAFIA DE ABDOMEN TOTAL INFANTIL'], {}, None, ''),
    ('US de abdômen superior', 'Ultrassom', '02.05.02.003-8', 101.27, ['ECOGRAFIA DE ABDOMEN SUPERIOR ADULTO'], {}, '02.05.02.003-8', ''),
    ('US de aparelho urinário e rins (adulto)', 'Ultrassom', '02.05.02.005-4', 90.53,
     ['ECOGRAFIA DO APARELHO URINARIO (RINS, BEXIGA) ADULTO', 'ULTRASSONOGRAFIA RENAL'], {}, '02.05.02.005-4', ''),
    ('US de aparelho urinário (criança)', 'Ultrassom', '02.05.02.005-4', 90.53,
     ['ECOGRAFIA DO APARELHO URINARIO (RINS, BEXIGA) INFANTIL'], {}, None, ''),
    ('US de bolsa escrotal (adulto)', 'Ultrassom', '02.05.02.007-0', 100.00, ['ECOGRAFIA DE BOLSA ESCROTAL ADULTO'], {}, '02.05.02.007-0', ''),
    ('US de bolsa escrotal (criança)', 'Ultrassom', '02.05.02.007-0', 100.00, ['ECOGRAFIA DE BOLSA ESCROTAL INFANTIL'], {}, None, ''),
    ('US de próstata (via abdominal)', 'Ultrassom', '02.05.02.010-0', 74.19, ['ECOGRAFIA DE PROSTATA ( VIA ABDOMINAL )'], {}, '02.05.02.010-0', ''),
    ('US de tireoide (adulto, com o Doppler de tireoide)', 'Ultrassom', '02.05.02.012-7', 64.07,
     ['ECOGRAFIA DE TIREOIDE ADULTO', 'ULTRA-SONOGRAFIA DOPPLER DE TIREOIDE'], {}, '02.05.02.012-7', ''),
    ('US de tireoide (criança)', 'Ultrassom', '02.05.02.012-7', 64.07, ['ECOGRAFIA DE TIREOIDE INFANTIL'], {}, None, ''),
    ('US de mamas (as duas)', 'Ultrassom', '02.05.02.009-7', 70.97, ['ECOGRAFIA DE MAMAS - BILATERAL'], {}, None, ''),
    ('US transvaginal', 'Ultrassom', '02.05.02.018-6', 83.77, ['ECOGRAFIA TRANSVAGINAL'],
     {'ECOGRAFIA TRANSVAGINAL': (4000, '4.000 reservados à OCI de ginecologia do IEV (L-008)')}, None, ''),
    ('Doppler de carótidas e outros vasos', 'Ultrassom', US_DOP, 115.61, CAROTIDAS, {}, US_DOP, ''),
    ('Doppler de membros (os dois lados)', 'Ultrassom', US_DOP, 115.61, MEMBROS,
     {'ULTRA-SONOGRAFIA DOPPLER VENOSO - MMII ( BILATERAL)': (9, 'ajuste para o valor dos exames não passar do valor '
                                                               'pedido (usuário, 11/11)')}, None,
     'CONDIÇÃO (D-011): só fica se a SES aceitar registrar o pedido dos dois lados como dois exames. '
     'Está na conta como um exame; se a condição não for atendida, sai, e faltam R$ 1,39 mi (ver Saídas)'),
    ('US de articulação, fora da ortopedia', 'Ultrassom', '02.05.02.006-2', 70.97, 'ARTICULACAO', {}, None,
     'partes moles, região inguinal, pescoço, axila e quadril e coluna de bebê; a ortopedia fica com o IEV (D-012)'),
    ('TC de abdômen superior com contraste', 'Tomografia', '02.06.03.001-0', 309.25,
     ['063. TC DO ABDOMEN SUPERIOR ADULTO C/CONTRASTE S/SEDACAO'], {}, None, ''),
    ('TC de abdômen superior sem contraste', 'Tomografia', '02.06.03.001-0', 309.25,
     ['061. TC DO ABDOMEN SUPERIOR ADULTO S/CONTRASTE S/SEDACAO'], {}, None, ''),
    ('TC de pelve com contraste', 'Tomografia', '02.06.03.003-7', 309.25,
     ['111. TC DE PELVE OU BACIA ADULTO C/CONTRASTE S/SEDACAO'],
     {'111. TC DE PELVE OU BACIA ADULTO C/CONTRASTE S/SEDACAO': (5, 'pedidos com CID da OCI de ortopedia do IEV')}, None, ''),
    ('TC de pelve sem contraste', 'Tomografia', '02.06.03.003-7', 309.25,
     ['109. TC DE PELVE OU BACIA ADULTO S/CONTRASTE  S/SEDACAO'],
     {'109. TC DE PELVE OU BACIA ADULTO S/CONTRASTE  S/SEDACAO': (1, 'pedido com CID da OCI de ortopedia do IEV')}, None, ''),
    ('TC de tórax com contraste', 'Tomografia', '02.06.02.003-1', 309.25, ['055. TC DO TORAX ADULTO C/CONTRASTE S/SEDACAO'], {}, None, ''),
    ('TC de tórax sem contraste', 'Tomografia', '02.06.02.003-1', 309.25, ['053. TC DO TORAX  ADULTO S/CONTRASTE S/SEDACAO'], {}, None, ''),
    ('TC de pescoço com contraste', 'Tomografia', '02.06.01.005-2', 309.25, ['119. TC DE PESCOCO ADULTO C/CONTRASTE S/SEDACAO'], {}, None, ''),
    ('TC de crânio sem contraste', 'Tomografia', '02.06.01.007-9', 251.29, ['029. TC DE CRANIO ADULTO S/CONTRASTE S/SEDACAO'], {}, None, ''),
]


def cab(ws, linha, titulos, larguras):
    for i, t in enumerate(titulos, 1):
        c = ws.cell(linha, i, t)
        c.fill, c.font, c.alignment = CAB, CAB_FONTE, QUEBRA
    for i, w in enumerate(larguras, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.row_dimensions[linha].height = 32


def titulo(ws, t, sub):
    ws['A1'] = t
    ws['A1'].font = Font(bold=True, size=14)
    ws['A2'] = sub


def fmt(ws, lin, formatos):
    for col, f in formatos:
        ws.cell(lin, col).number_format = f


def main():
    # 1. a v2 gera Não escolhidos e Estudos das filas
    v2.SAIDA = TEMP
    v2.main()
    wb = openpyxl.load_workbook(TEMP)
    os.remove(TEMP)
    for nome in ('Resumo', 'Escolhidos', 'Articulação', 'Agenda da SES', 'Saídas', 'Da sobra à falta', 'Conferência'):
        del wb[nome]

    F = {f['nome']: f for f in json.load(open(FILAS))['filas']}
    dem = {x['codigo']: x for x in json.load(open(FILAS))['revisao']['demanda']}
    marg = openpyxl.load_workbook(v2.MARGEM, data_only=True)['1 Margem por exame']
    novos_09 = {r[0]: r[11] for r in marg.iter_rows(min_row=4, values_only=True) if r[1] in ('US', 'TC')}
    art = [f for f in F.values() if f['codigo'] == '02.05.02.006-2' and any(k in f['nome'] for k in v2.NAO_ORTO)
           and 'EMERG' not in f['nome']]
    fila_dop = sum(F[n]['fila'] for n in MEMBROS + CAROTIDAS)

    def novos_do(exame, cod_dem):
        """pedidos novos de 12 meses que a SES não absorve + a parte do que ela realiza (só os 7 exames fáceis)."""
        if cod_dem is None:
            return 0, 0
        chave = {'US de abdômen total (adulto)': 'US de abdômen total (adulto)', 'US de abdômen superior': 'US de abdômen superior',
                 'US de aparelho urinário e rins (adulto)': 'US de aparelho urinário e rins', 'US de bolsa escrotal (adulto)': 'US de bolsa escrotal (adulto)',
                 'US de próstata (via abdominal)': 'US de próstata', 'US de tireoide (adulto, com o Doppler de tireoide)': 'US de tireoide (com',
                 'Doppler de carótidas e outros vasos': 'Doppler de carótidas'}[exame]
        nov = next(v for k, v in novos_09.items() if k.startswith(chave))
        parte = sum(F[n]['fila'] for n in CAROTIDAS) / fila_dop if cod_dem == US_DOP else 1
        ses = round(dem[cod_dem]['ses_realiza_elegivel_mes'] * parte * 12 * PARTE_SES)
        return nov, ses

    # ---------- Filas escolhidas (o detalhe) ----------
    d = wb.create_sheet('Filas escolhidas', 0)
    titulo(d, 'Todas as filas escolhidas, pelo nome do SISREG',
           'Coleta do Mapa Social de 02/11/2026. Cada exame da aba Escolhidos é a soma das suas filas. '
           '"Vamos atender" = a fila menos o que é de outro plano.')
    cab(d, 4, ['Exame', 'Modalidade', 'Código SIGTAP', 'Fila no SISREG', 'Pedidos na fila', 'Vamos atender',
               'Por que não atendemos todos', 'Pedidos de menos de 24 meses', 'Espera mediana (dias)', 'Motivos mais pedidos (CID)',
               'Preço Candanga', 'Valor'], [34, 11, 15, 52, 10, 10, 30, 11, 10, 46, 12, 15])
    lin = 5
    sub_de = {}
    for exame, mod, cod, preco, filas, ajuste, _, _ in EXAMES:
        lista = art if filas == 'ARTICULACAO' else [F[n] for n in filas]
        ini = lin
        for f in sorted(lista, key=lambda x: -x['fila']):
            tira, porque = ajuste.get(f['nome'], (0, ''))
            cid = f.get('cid') or ''
            d.append([exame, mod, cod, f['nome'].strip(), f['fila'], f'=E{lin}-{tira}' if tira else f'=E{lin}', porque,
                      f['fila_viva'], round(f['espera_mediana']), cid.replace(';', ','), preco, f'=F{lin}*K{lin}'])
            fmt(d, lin, ((5, INT), (6, INT), (8, INT), (9, INT), (11, MOEDA), (12, MOEDA)))
            lin += 1
        d.append([f'Subtotal: {exame}', None, None, None, f'=SUM(E{ini}:E{lin - 1})', f'=SUM(F{ini}:F{lin - 1})', None,
                  f'=SUM(H{ini}:H{lin - 1})', None, None, None, f'=SUM(L{ini}:L{lin - 1})'])
        for col in range(1, 13):
            d.cell(lin, col).fill = SUB
            d.cell(lin, col).font = NEGRITO
        fmt(d, lin, ((5, INT), (6, INT), (8, INT), (12, MOEDA)))
        sub_de[exame] = lin
        lin += 1
    d_tot = lin
    d.cell(d_tot, 1, 'Total das filas escolhidas').font = NEGRITO
    for col, L, f_ in ((5, 'E', INT), (6, 'F', INT), (8, 'H', INT), (12, 'L', MOEDA)):
        subs = ','.join(f'{L}{r}' for r in sub_de.values())
        c = d.cell(d_tot, col, f'=SUM({subs})')
        c.font, c.number_format = NEGRITO, f_
    d.cell(d_tot + 2, 1, 'Filas com menos de 30 pedidos de outros nomes do mesmo código ficam de fora (planilha de 09/11), menos '
                         'na articulação, onde entram todas as que não são ortopedia.')
    d.freeze_panes = 'E5'

    # ---------- Escolhidos ----------
    e = wb.create_sheet('Escolhidos', 0)
    titulo(e, 'Os exames do plano',
           'Fila de hoje = coleta de 02/11 (detalhe na aba Filas escolhidas). Exames novos = o que entra na fila em 12 '
           'meses e a rede do plano assume. Preço = Tabela SUS Candanga.')
    cab(e, 4, ['Exame', 'Modalidade', 'Código SIGTAP', 'Fila de hoje (vamos atender)', 'Exames novos em 12 meses',
               'Total de exames', 'Preço Candanga', 'Valor', 'Condição / observação'],
        [40, 11, 15, 13, 13, 12, 13, 16, 70])
    lin = 5
    linha_ex = {}
    for exame, mod, cod, preco, _, _, cod_dem, cond in EXAMES:
        nov, ses = novos_do(exame, cod_dem)
        obs = cond
        if nov or ses:
            br = lambda n: f'{n:,}'.replace(',', '.')
            pct = f'{PARTE_SES:.1%}'.replace('.', ',')
            obs = (f'exames novos: {br(nov)} pedidos que entram e a SES não dá conta, mais {br(ses)} do que a SES '
                   f'realiza ({pct} em 12 meses), que passam ao plano')
            if EXTRA.get(exame):
                obs += f', mais {EXTRA[exame]} para chegar mais perto do valor pedido'
        e.append([exame, mod, cod, f"='Filas escolhidas'!F{sub_de[exame]}", nov + ses + EXTRA.get(exame, 0), f'=D{lin}+E{lin}', preco,
                  f'=F{lin}*G{lin}', obs])
        fmt(e, lin, ((4, INT), (5, INT), (6, INT), (7, MOEDA), (8, MOEDA)))
        e.cell(lin, 9).alignment = QUEBRA
        if exame.startswith('Doppler de membros'):
            for col in range(1, 10):
                e.cell(lin, col).fill = AMARELO
        linha_ex[exame] = lin
        lin += 1
    tot = lin
    e.cell(tot, 1, 'Total').font = NEGRITO
    for col, L, f_ in ((4, 'D', INT), (5, 'E', INT), (6, 'F', INT), (8, 'H', MOEDA)):
        c = e.cell(tot, col, f'=SUM({L}5:{L}{tot - 1})')
        c.font, c.number_format = NEGRITO, f_
    for i, mod in enumerate(('Ultrassom', 'Tomografia')):
        r = tot + 1 + i
        e.cell(r, 1, f'  {mod}')
        for col, L, f_ in ((4, 'D', INT), (5, 'E', INT), (6, 'F', INT), (8, 'H', MOEDA)):
            e.cell(r, col, f'=SUMIFS({L}5:{L}{tot - 1},B5:B{tot - 1},"{mod}")').number_format = f_
    e.freeze_panes = 'B5'
    dop = linha_ex['Doppler de membros (os dois lados)']

    # ---------- Resumo ----------
    r = wb.create_sheet('Resumo', 0)
    titulo(r, 'Plano 4 — os exames pela Tabela SUS Candanga',
           'Controle interno, 11/11/2026. Fila do Mapa Social de 02/11; preço da Candanga (SIA).')
    linhas = [
        ('Valor dos exames pedido (recurso menos o apoio)', ALVO, MOEDA),
        ('Valor dos exames escolhidos', f'=Escolhidos!H{tot}', MOEDA),
        ('Sobra: valor pedido menos o valor escolhido (não pode ser negativa)', '=B4-B5', MOEDA),
        (None, None, None),
        ('Exames da fila de hoje', f'=Escolhidos!D{tot}', INT),
        ('Exames novos em 12 meses', f'=Escolhidos!E{tot}', INT),
        ('Total de exames', f'=Escolhidos!F{tot}', INT),
        ('  de ultrassom', f'=Escolhidos!F{tot + 1}', INT),
        ('  de tomografia', f'=Escolhidos!F{tot + 2}', INT),
        (None, None, None),
        ('Condição do Doppler de membros (os dois lados)', 'só fica se a SES aceitar dois exames por pedido (D-011)', None),
        ('Valor do Doppler de membros na conta (um exame por pedido)', f'=Escolhidos!H{dop}', MOEDA),
        ('Se a condição não for atendida e ele sair: falta', f'=B4-(B5-B15)', MOEDA),
        ('Se a SES aceitar dois exames por pedido: passa do valor em', f'=B15-B6', MOEDA),
    ]
    for i, (rot, val, f_) in enumerate(linhas, 4):
        if rot:
            r.cell(i, 1, rot)
            c = r.cell(i, 2, val)
            if f_:
                c.number_format = f_
    r['B6'].font = Font(bold=True, color='006100')
    r['B16'].font = Font(bold=True, color='C00000')
    r['A14'].font = NEGRITO
    notas = [
        'Como fechamos o valor: os exames da fila de hoje, mais os exames novos de 7 exames fáceis de ultrassom '
        '(abdômen total, abdômen superior, urinário, carótidas, bolsa escrotal, próstata e tireoide). Os novos são os '
        'pedidos que entram e a SES não dá conta, mais 8,1% do que a SES realiza neles. Ver Saídas, 1 e 2.',
        'A regulação e as Regiões precisam aceitar mandar esses pedidos ao plano: o ultrassom está sob gestão das Regiões '
        '(Despacho SEI 219528407, item 5).',
        'As 14 salas de ultrassom ficam em cerca de 96% de uso em 12 meses, sem folga. Sem o Doppler de membros, cerca de 67%.',
        'Abas: Escolhidos (os exames), Filas escolhidas (cada fila pelo nome), Saídas (como fechar o valor e o que fazer '
        'se o Doppler sair), Não escolhidos e Estudos das filas.',
    ]
    for i, t in enumerate(notas, 19):
        r.cell(i, 1, '- ' + t).alignment = Alignment(wrap_text=True, vertical='top')
        r.merge_cells(start_row=i, start_column=1, end_row=i, end_column=4)
        r.row_dimensions[i].height = 45
    r.column_dimensions['A'].width = 62
    r.column_dimensions['B'].width = 30

    # ---------- Saídas ----------
    s = wb.create_sheet('Saídas', 3)
    titulo(s, 'As saídas para fechar o valor',
           'Verde = escolhida e já na carteira. Amarelo = de reserva, se o Doppler de membros sair (faltam R$ 1,39 mi). '
           'Cinza = descartada. Marque "sim" em Usar para somar as de reserva.')
    cab(s, 4, ['Nº', 'Saída', 'Situação', 'Exames', 'Quanto traz', 'Usar', 'Por quê', 'Depende de'],
        [5, 50, 12, 10, 16, 7, 70, 45])
    nl = {x[0]: x for x in EXAMES}
    fac = [x for x in EXAMES if x[6]]
    nov_t = sum(novos_do(x[0], x[6])[0] for x in fac)
    nov_v = sum(novos_do(x[0], x[6])[0] * x[3] for x in fac)
    ses_t = sum(novos_do(x[0], x[6])[1] for x in fac)
    ses_v = sum(novos_do(x[0], x[6])[1] * x[3] for x in fac)
    tc = ['02.06.03.001-0', '02.06.03.003-7', '02.06.02.003-1']
    tc_nov = sum(novos_09[k] for k in novos_09 if k.startswith(('TC de abdômen superior com', 'TC de pelve com', 'TC de tórax com')))
    tc_real = sum(dem[c]['ses_realiza_elegivel_mes'] * 12 for c in tc)
    s['B3'] = 'Parte do que a SES realiza na TC com contraste que o plano assumiria (saída 4)'
    s['E3'] = 0.12
    s['E3'].fill, s['E3'].number_format = AMARELO, PCT
    saidas = [
        ('1', 'Pedidos novos de 7 exames fáceis de ultrassom', 'escolhida', nov_t, round(nov_v, 2), '',
         'é o que entra na fila e a SES não dá conta: a fila cresce. Exames de 15 a 20 min, sem contraste, margem de 30% a 56%',
         'escrever no plano que a meta conta com os pedidos novos'),
        ('2', f'{PARTE_SES:.1%} do que a SES realiza nesses 7 exames passa ao plano'.replace('.', ','), 'escolhida', ses_t,
         round(ses_v, 2), '',
         'cerca de 128 exames por mês na rede toda; a SES fica com a vaga para outro atendimento do mesmo aparelho',
         'pactuar com a regulação e as Regiões'),
        ('3', 'Doppler de membros contado como dois exames por pedido', 'reserva', f'=Escolhidos!F{dop}',
         f'=Escolhidos!H{dop}', 'não', 'é a própria condição: se a SES aceitar, além de ficar, ele passa do valor em R$ 1,39 mi',
         'a SES autorizar por escrito (D-011); a ficha do SIGTAP diz que é um exame só'),
        ('4', 'TC com contraste: pedidos novos e parte do que a SES realiza', 'reserva',
         f'=ROUND({tc_nov}+{tc_real}*E3,0)', f'=ROUND({tc_nov}+{tc_real}*E3,0)*309.25', 'não',
         f'a SES realiza {tc_real:,.0f} TC com contraste de abdômen, pelve e tórax por ano; com 12%, fecha a falta sem o '
         'Doppler. Feita na clínica; margem de 27%'.replace(',', '.'),
         'os 3 tomógrafos (cerca de 79% de uso hoje); pactuar com a regulação (panorama 3, central)'),
        ('5', 'Mais da agenda da SES nos 7 exames fáceis', 'reserva', None, None, 'não',
         'sem o Doppler, as salas ficam com 67% de uso e há espaço; mas fechar só por aqui pede cerca de 83% do que a '
         'SES realiza neles, o que é demais', 'regulação e Regiões'),
        ('6', 'Resto da US de articulação (ortopedia)', 'reserva', "=SUMIFS('Não escolhidos'!D:D,'Não escolhidos'!A:A,\"US de articulação de ortopedia*\")",
         "=SUMIFS('Não escolhidos'!G:G,'Não escolhidos'!A:A,\"US de articulação de ortopedia*\")", 'não',
         'fila grande que cresce; o IEV não tirou nenhum pedido dela', 'a regulação dizer que não manda esses pedidos ao IEV (L-008)'),
        ('7', 'Transvaginal reservada ao IEV, depois de maio de 2027', 'reserva', 4000,
         "=SUMIFS('Não escolhidos'!G:G,'Não escolhidos'!A:A,\"US transvaginal, reserva*\")", 'não',
         'o IEV quase não executa a OCI de ginecologia', 'execução que passe do fim da vigência do IEV'),
        ('8', 'Plano menor: metas e valor abaixo do recurso', 'reserva', None, 0, 'não',
         'nada sem fila nem exame difícil; mas o recurso não é usado e o percentual da gestão sobe (perto do teto de 8,5%)',
         'aceite do parlamentar e da SES'),
        ('9', 'Pedidos novos de mama e transvaginal', 'descartada', None, None, '',
         'mama: margem de 17% e a SES faz mutirões; transvaginal: a SES agenda mais do que entra, não há pedido novo', ''),
        ('10', 'Angiotomografias (sem coronárias e sem crânio)', 'descartada', None,
         "=SUMIFS('Não escolhidos'!G:G,'Não escolhidos'!A:A,\"Angiotomografias*\")", '', 'dão muito trabalho (decisão de 11/11)', ''),
        ('11', 'Angiotomografia de coronárias', 'descartada', 1532, 1532 * 309.25, '',
         '30 min, betabloqueador e ECG pelo preço da TC de tórax', ''),
        ('12', 'TC de face e de crânio com contraste, angio do crânio', 'descartada', None, None, '',
         'margem de 10% a 13% e a SES já dá conta', ''),
        ('13', 'US pélvica ginecológica', 'descartada', 1016, 1016 * 43.41, '', 'cada exame dá prejuízo', ''),
    ]
    lin = 5
    for row in saidas:
        s.append(list(row))
        cor = {'escolhida': VERDE, 'reserva': AMARELO, 'descartada': CINZA}[row[2]]
        for col in range(1, 9):
            s.cell(lin, col).fill = cor
            s.cell(lin, col).alignment = QUEBRA
        fmt(s, lin, ((4, INT), (5, MOEDA)))
        lin += 1
    ult = lin - 1
    contas = [
        ('Escolhidas (1 e 2): já estão na carteira', f'=SUMIFS(E5:E{ult},C5:C{ult},"escolhida")'),
        ('Falta se o Doppler de membros sair', '=Resumo!B16'),
        ('Reservas marcadas com "sim"', f'=SUMIFS(E5:E{ult},F5:F{ult},"sim")'),
        ('Falta depois das reservas marcadas (negativo = passa)', f'=E{lin + 2}-E{lin + 3}'),
    ]
    for i, (rot, form) in enumerate(contas):
        s.cell(lin + 1 + i, 2, rot).font = NEGRITO
        s.cell(lin + 1 + i, 5, form).number_format = MOEDA
    s.cell(lin + 4, 5).font = Font(bold=True, color='C00000')
    s.freeze_panes = 'C5'

    wb.move_sheet('Não escolhidos', offset=10)
    wb.move_sheet('Estudos das filas', offset=10)
    wb.active = 0
    wb.save(SAIDA)
    print('salvo', SAIDA, 'sheets', wb.sheetnames)


if __name__ == '__main__':
    main()
