"""Planilha da carteira final do plano 4 (11/11/2026).

Junta as decisões de 10 e 11/11 (pendencias.md, D-011 e D-012) com:
- a margem e as filas de cada candidato: estudo_readequacao_candanga_margem_20261109.xlsx, aba 1;
- as filas por nome e o rumo por código: dados/fontes/mapa_social_20261102_imagem_bruto/coleta_20261102.json;
- a fila que a SES mediu em 09/11: Despacho SEI 219528407 (CRDF, 10/11/2026).

Rodar da pasta planos/redacao_04:
    python3 estudos/gerar_carteira_final_20261111.py
"""
import json
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

AQUI = 'estudos/'
MARGEM = AQUI + 'estudo_readequacao_candanga_margem_20261109.xlsx'
COLETA = 'dados/fontes/mapa_social_20261102_imagem_bruto/coleta_20261102.json'
SAIDA = AQUI + 'carteira_final_20261111.xlsx'

ALVO = 10636602

NEGRITO = Font(bold=True)
CAB = PatternFill('solid', fgColor='1F4E78')
CAB_FONTE = Font(bold=True, color='FFFFFF')
AMARELO = PatternFill('solid', fgColor='FFF2CC')
VERDE = PatternFill('solid', fgColor='E2EFDA')
VERMELHO = PatternFill('solid', fgColor='FCE4D6')
MOEDA = 'R$ #,##0.00'
INT = '#,##0'
PCT = '0%'

# código e fila da SES (09/11) de cada candidato da aba 1
CODIGO = {
    'TC de abdômen superior sem contraste': ('02.06.03.001-0', 10),
    'TC de pelve sem contraste': ('02.06.03.003-7', 8),
    'TC de tórax sem contraste': ('02.06.02.003-1', 32),
    'TC de crânio sem contraste': ('02.06.01.007-9', None),
    'TC de abdômen superior com contraste': ('02.06.03.001-0', 3585),
    'TC de pelve com contraste': ('02.06.03.003-7', 3164),
    'TC de tórax com contraste': ('02.06.02.003-1', 1994),
    'TC de pescoço com contraste': ('02.06.01.005-2', None),
    'TC de crânio com contraste': ('02.06.01.007-9', None),
    'TC de face e seios da face': ('02.06.01.004-4', None),
    'Angiotomografias, sem as coronárias': ('vários', None),
    'Angiotomografia do crânio': ('02.06.01.007-9', None),
    'US de abdômen superior': ('02.05.02.003-8', 2217),
    'US de bolsa escrotal (adulto)': ('02.05.02.007-0', None),
    'US de abdômen total (adulto)': ('02.05.02.004-6', 9979),
    'US de parede abdominal': ('02.05.02.004-6', None),
    'US de aparelho urinário e rins (adulto': ('02.05.02.005-4', 3659),
    'Doppler de carótidas': ('02.05.01.004-0', None),
    'US transvaginal': ('02.05.02.018-6', 9220),
    'US de próstata': ('02.05.02.010-0', 2964),
    'US de tireoide (com': ('02.05.02.012-7', 3018),
    'US de mamas': ('02.05.02.009-7', 12807),
    'US de abdômen total (criança)': ('02.05.02.004-6', None),
    'US de aparelho urinário (criança)': ('02.05.02.005-4', 275),
    'US de bolsa escrotal (criança)': ('02.05.02.007-0', None),
    'US de tireoide (criança)': ('02.05.02.012-7', 62),
    'Doppler de membros': ('02.05.01.004-0', None),
}

DECISAO = {  # candidato → (entra?, motivo)
    'TC de crânio com contraste': (False, 'margem de 10%; a SES agenda 1.909 por ano, a fila gira em 2 meses (11/11)'),
    'TC de face e seios da face': (False, 'margem de 13% e fila pequena (11/11)'),
    'Angiotomografias, sem as coronárias': (False, 'dá muito trabalho: injeção rápida, acesso calibroso, reconstrução (11/11)'),
    'Angiotomografia do crânio': (False, 'margem de 10% e a maior exigência (11/11)'),
    'Doppler de membros': (True, 'CONDICIONADO (D-011): só vale se contar como dois exames; está dentro da conta como um exame'),
    'TC de pescoço com contraste': (True, 'mesmo preço e custo das TC grandes; perfil oncológico (11/11)'),
}

# filas não-ortopedia do código da articulação que entram (D-012, 11/11)
NAO_ORTO = ['ECOGRAFIA  DE PARTES MOLES', 'REGIAO INGUINAL', 'REGIÃO INGUINAL', 'PESCOCO', 'CERVICAL',
            'SUBMANDIBULARES', 'AXILA', 'COLUNA LOMBAR', 'USG QUADRIL', 'INFANTIL', 'REGIAO LOMBAR']


def chave(nome, tabela):
    for k in tabela:
        if nome.startswith(k):
            return k
    return None


def cabecalho(ws, linha, titulos, larguras=None):
    for i, t in enumerate(titulos, 1):
        c = ws.cell(linha, i, t)
        c.fill, c.font = CAB, CAB_FONTE
        c.alignment = Alignment(wrap_text=True, vertical='top')
    if larguras:
        for i, w in enumerate(larguras, 1):
            ws.column_dimensions[get_column_letter(i)].width = w


def titulo(ws, texto, sub=None):
    ws['A1'] = texto
    ws['A1'].font = Font(bold=True, size=14)
    if sub:
        ws['A2'] = sub
        ws['A2'].alignment = Alignment(wrap_text=False)


def main():
    m = openpyxl.load_workbook(MARGEM, data_only=True)['1 Margem por exame']
    cand = []
    for r in m.iter_rows(min_row=4, values_only=True):
        if r[1] in ('US', 'TC'):
            cand.append(dict(nome=r[0], mod=r[1], preco=r[2], minutos=r[3], custo=r[4], margem=r[6],
                             fila=r[10], novos=r[11], complex=r[9], porque=r[14]))
    coleta = json.load(open(COLETA))
    us = coleta['panorama']['ultrassonografia']['filas']
    tc = coleta['panorama']['tomografia']['filas']
    rumo = {r['codigo']: r for r in coleta['rumo']}

    wb = openpyxl.Workbook()

    # ---------- Resumo ----------
    ws = wb.active
    ws.title = 'Resumo'
    titulo(ws, 'Plano 4 — carteira final pela Tabela SUS Candanga',
           'Controle interno, 11/11/2026. Filas da coleta do Mapa Social de 02/11; preço da Candanga (SIA). '
           'Amarelo é premissa que pode mudar. Tudo é fórmula sobre as outras abas.')
    linhas = [
        ('Valor dos exames pedido (recurso menos o apoio)', ALVO, MOEDA, True),
        ('Carteira escolhida (aba Escolhidos)', "=Escolhidos!J{tot}", MOEDA, False),
        ('Falta para fechar', '=B4-B5', MOEDA, False),
        ('Exames na carteira', "=Escolhidos!I{tot}", INT, False),
        ('O Doppler de membros está dentro, como um exame por pedido', "=Escolhidos!J{dop}", MOEDA, False),
        ('Falta, se o Doppler de membros ficar fora', '=B6+B8', MOEDA, False),
        ('Falta, se o Doppler contar como dois exames (D-011)', '=B6-B8', MOEDA, False),
        ('Pedidos novos de 12 meses dos exames escolhidos (valor)', "=Escolhidos!L{tot}", MOEDA, False),
        ('Valores não escolhidos, cabem no aparelho (aba Não escolhidos)', "=SUMIFS('Não escolhidos'!F:F,'Não escolhidos'!H:H,\"sim\")", MOEDA, False),
    ]
    ws.append([])
    resumo_pos = []
    for i, (rot, val, fmt, amarelo) in enumerate(linhas, 4):
        ws.cell(i, 1, rot)
        c = ws.cell(i, 2, val)
        c.number_format = fmt
        if amarelo:
            c.fill = AMARELO
        resumo_pos.append(c)
    ws['B6'].font = Font(bold=True, color='C00000')
    ws.cell(14, 1, 'Como ler').font = NEGRITO
    notas = [
        'Escolhidos: os exames que entram, com a fila de hoje, a fila da SES de 09/11, o preço e o valor.',
        'Não escolhidos: o que ficou fora, com o valor pela Candanga e o motivo. A coluna "cabe no aparelho" diz se poderia fechar a falta.',
        'Estudos das filas: o rumo de cada código (entradas, oferta, faltas, meses para zerar) e cada fila pelo nome.',
        'Saídas: as formas de chegar ao valor pedido, com quanto cada uma traz e o que pesa contra.',
        'Da sobra à falta: como se sai de faltar R$ 245 mil (v26 pela Candanga) para a falta de hoje, exame a exame.',
        'Estudos: os arquivos de onde vem cada número e cada decisão.',
    ]
    for i, n in enumerate(notas, 15):
        ws.cell(i, 1, '- ' + n)
    ws.column_dimensions['A'].width = 70
    ws.column_dimensions['B'].width = 20

    # ---------- Escolhidos ----------
    e = wb.create_sheet('Escolhidos')
    titulo(e, 'Exames escolhidos',
           'Quantidade = fila de hoje (02/11). Valor = quantidade × preço da Candanga. A quantidade em amarelo pode ser mudada.')
    cab = ['Exame', 'Mod.', 'Código SIGTAP', 'Fila nossa (02/11)', 'Fila SES (09/11)', 'Preço Candanga',
           'Minutos', 'Margem (% do preço)', 'Quantidade na carteira', 'Valor', 'Pedidos novos em 12 meses',
           'Valor dos pedidos novos', 'Motivo / observação']
    cabecalho(e, 4, cab, [44, 6, 16, 12, 12, 13, 9, 11, 12, 16, 12, 16, 70])
    lin = 5
    dop_linha = None
    for c in cand:
        k = chave(c['nome'], DECISAO)
        entra, motivo = DECISAO.get(k, (True, c['porque']))
        if not entra:
            continue
        cod, ses = CODIGO[chave(c['nome'], CODIGO)]
        e.append([c['nome'], c['mod'], cod, c['fila'], ses, c['preco'], c['minutos'], c['margem'],
                  c['fila'], f'=I{lin}*F{lin}', c['novos'], f'=K{lin}*F{lin}', motivo])
        e.cell(lin, 9).fill = AMARELO
        if c['nome'].startswith('Doppler de membros'):
            dop_linha = lin
            for col in range(1, 14):
                e.cell(lin, col).fill = AMARELO
        lin += 1
    # articulação não-ortopedia, fila a fila
    custo15 = next(c['custo'] for c in cand if c['nome'].startswith('US de abdômen superior'))
    for f in us:
        if f['codigo'] == '02.05.02.006-2' and any(k in f['nome'] for k in NAO_ORTO):
            e.append([f"Articulação, não ortopedia: {f['nome'].strip()}", 'US', '02.05.02.006-2', f['fila'], None,
                      70.97, 15, (70.97 - custo15) / 70.97, f['fila'], f'=I{lin}*F{lin}', 0, f'=K{lin}*F{lin}',
                      'fora da OCI de ortopedia do IEV (D-012, 11/11); margem estimada com o custo do exame de 15 min'])
            e.cell(lin, 9).fill = AMARELO
            lin += 1
    tot = lin
    e.cell(tot, 1, 'Total').font = NEGRITO
    for col, L in ((4, 'D'), (9, 'I'), (10, 'J'), (11, 'K'), (12, 'L')):
        e.cell(tot, col, f'=SUM({L}5:{L}{tot - 1})').font = NEGRITO
    e.cell(tot, 5, 'a SES mediu só os códigos da v26').font = Font(italic=True)
    for r in range(5, tot + 1):
        for col, fmt in ((4, INT), (5, INT), (6, MOEDA), (8, PCT), (9, INT), (10, MOEDA), (11, INT), (12, MOEDA)):
            e.cell(r, col).number_format = fmt
    e.freeze_panes = 'B5'
    e.cell(tot + 2, 1, 'Fila SES (09/11): a SES dá um número por código e não separa adulto e criança nem carótidas e membros '
                       '(Doppler 12.664; urinário e tireoide infantis 275 e 62). Na TC, ela separa com e sem contraste.')
    e.cell(tot + 3, 1, 'Na tomografia, as três filas grandes têm 1.357 pedidos a menos pela SES que pela nossa coleta, cerca de R$ 420 mil.')

    # preencher fórmulas do resumo
    for c in resumo_pos:
        if isinstance(c.value, str):
            c.value = c.value.format(tot=tot, dop=dop_linha)

    # ---------- Não escolhidos ----------
    n = wb.create_sheet('Não escolhidos')
    titulo(n, 'O que ficou fora, com o valor pela Candanga',
           '"Cabe no aparelho" = sim quando o exame usa o ultrassom ou o tomógrafo do plano e poderia fechar a falta.')
    cabecalho(n, 4, ['Fila', 'Código SIGTAP', 'Grupo', 'Pedidos (02/11)', 'Preço Candanga', 'Valor', 'Motivo',
                     'Cabe no aparelho', 'Margem (% do preço)'], [52, 16, 22, 12, 13, 16, 80, 10, 11])
    fora = []
    for c in cand:
        k = chave(c['nome'], DECISAO)
        if k and not DECISAO[k][0]:
            fora.append([c['nome'], CODIGO[chave(c['nome'], CODIGO)][0], 'decisão desta revisão', c['fila'], c['preco'],
                         DECISAO[k][1], 'sim', c['margem']])
    art = sum(f['fila'] for f in us if f['codigo'] == '02.05.02.006-2' and f['fila'] >= 1
              and not any(k in f['nome'] for k in NAO_ORTO))
    fora += [
        ['US pélvica ginecológica, adulto e infantil', '02.05.02.016-0', 'decisão desta revisão', 1014, 43.41,
         'cada exame dá prejuízo: paga R$ 43,41 e custa R$ 44,99 (09/11 e 11/11)', 'sim', (43.41 - custo15) / 43.41],
        ['US de articulação de adulto (ombro, punho, joelho, tornozelo, cotovelo, mão, pé)', '02.05.02.006-2', 'IEV',
         art, 70.97, 'OCI de ortopedia com ultrassom do IEV (19.070 contratadas); volta se a regulação disser por escrito '
         'que não manda esses pedidos ao IEV (L-008)', 'sim', (70.97 - custo15) / 70.97],
        ['US transvaginal, reserva do IEV', '02.05.02.018-6', 'IEV', 4000, 83.77,
         'OCI de ginecologia (GIN1) do IEV, 3.218 contratadas; a reserva vale até o fim da vigência, por volta de 05/2027',
         'sim', 0.46],
        ['TC de coluna, articulações e segmentos', 'vários', 'IEV', 522, None,
         'compatíveis com a OCI de ortopedia com tomografia do IEV (L-008)', 'não', None],
        ['Angiotomografia de coronárias', '02.06.02.003-1', 'regra do plano', 1532, 309.25,
         '30 min, betabloqueador e ECG pelo preço da TC de tórax; a clínica provavelmente não cobre (02/11)', 'sim', None],
        ['Filas de emergência (todas com "EMERG")', 'vários', 'regra do plano', 4697, None, 'só ambulatório (D-009)', 'não', None],
        ['US transfontanela', '02.05.02.017-8', 'regra do plano', 270, None, 'saiu em 03/11, a pedido do usuário', 'não', None],
        ['TC com sedação', 'vários', 'regra do plano', 10, None, 'precisa de anestesia', 'não', None],
        ['Ecocardiografia', '02.05.01.003-2', 'outra equipe ou aparelho', 14669, None, 'outra equipe (cardiologia)', 'não', None],
        ['US de globo ocular', '02.05.02.008-9', 'outra equipe ou aparelho', 1316, None, 'outra equipe (oftalmologia)', 'não', None],
        ['US obstétricas', 'vários', 'outra equipe ou aparelho', 561, None, 'outra equipe', 'não', None],
        ['PET-CT', '—', 'outra equipe ou aparelho', 379, None, 'outro aparelho', 'não', None],
        ['TC cone beam', '—', 'outra equipe ou aparelho', 195, None, 'outro aparelho (odontologia)', 'não', None],
        ['Paquimetria', '—', 'outra equipe ou aparelho', 144, None, 'outro aparelho', 'não', None],
        ['Radiologia (mamografia 6.448, densitometria e outras)', '02.04*', 'outra equipe ou aparelho', 14093, None,
         'outro aparelho; fora do objeto', 'não', None],
        ['Ressonância', '02.07*', 'outra equipe ou aparelho', 10149, None, 'outro aparelho; fora do objeto', 'não', None],
        ['Medicina nuclear', '02.08*', 'outra equipe ou aparelho', 5663, None, 'outro aparelho; fora do objeto', 'não', None],
    ]
    lin = 5
    for row in fora:
        nome, cod, grupo, ped, preco, motivo, cabe, marg = row
        n.append([nome, cod, grupo, ped, preco, f'=IF(E{lin}="","",D{lin}*E{lin})', motivo, cabe, marg])
        n.cell(lin, 4).number_format = INT
        n.cell(lin, 5).number_format = MOEDA
        n.cell(lin, 6).number_format = MOEDA
        n.cell(lin, 9).number_format = PCT
        n.cell(lin, 8).fill = VERDE if cabe == 'sim' else VERMELHO
        lin += 1
    n.cell(lin, 1, 'Total que cabe no aparelho').font = NEGRITO
    n.cell(lin, 6, f'=SUMIFS(F5:F{lin - 1},H5:H{lin - 1},"sim")').number_format = MOEDA
    n.cell(lin, 6).font = NEGRITO
    n.freeze_panes = 'B5'

    # ---------- Estudos das filas ----------
    s = wb.create_sheet('Estudos das filas')
    titulo(s, 'O rumo de cada código e cada fila pelo nome (coleta de 02/11/2026)',
           'Meses para zerar = fila ÷ (oferta − entradas) por mês, no ritmo dos 3 últimos meses. É projeção, não previsão.')
    cabecalho(s, 4, ['Código', 'Fila maior do código', 'Fila do código', 'Fila de menos de 24 meses', 'Devolvidas',
                     'Entram por mês (12 m)', 'Oferta por mês (12 m)', 'Oferta por mês (3 últimos)', 'Realizados em 12 m',
                     'Faltas em 12 m', 'Falta (% dos agendados)', 'Saldo por mês (entra − sai)', 'Meses para zerar (3 últimos)',
                     'Pico da oferta'], [16, 50, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 12, 16])
    codigos = ['02.05.02.009-7', '02.05.01.004-0', '02.05.02.004-6', '02.05.02.018-6', '02.05.02.005-4', '02.05.02.012-7',
               '02.05.02.010-0', '02.05.02.003-8', '02.05.02.007-0', '02.05.02.006-2', '02.05.02.016-0', '02.06.03.001-0',
               '02.06.03.003-7', '02.06.02.003-1', '02.06.01.005-2', '02.06.01.007-9', '02.06.01.004-4']
    lin = 5
    for cd in codigos:
        r = rumo[cd]
        s.append([cd, r['fila_maior'], r['fila'], r['fila_viva'], r['devolvidas'], round(r['entrantes_12m'] / 12),
                  round(r['oferta_12m'] / 12), round(r['oferta_media_3m']), r['realizados_12m'], r['faltas_12m'],
                  r['falta_12m'],
                  f'=F{lin}-H{lin}',
                  f'=IF(H{lin}>F{lin},C{lin}/(H{lin}-F{lin}),"não zera")',
                  f"{r['pico_oferta_mes']} ({r['pico_oferta']})"])
        for col in (3, 4, 5, 6, 7, 8, 9, 10, 12):
            s.cell(lin, col).number_format = INT
        s.cell(lin, 11).number_format = PCT
        s.cell(lin, 13).number_format = '0.0'
        lin += 1
    lin += 2
    s.cell(lin, 1, 'Cada fila pelo nome, nos códigos acima (filas com 30 pedidos ou mais)').font = Font(bold=True, size=12)
    lin += 1
    cols = ['Código', 'Fila', 'Na carteira?', 'Pedidos', 'Menos de 24 meses', 'Devolvidas', 'Espera mediana (dias)',
            'Idade mediana', 'Agendadas em 12 m', 'Motivos mais pedidos (CID)']
    for i, t in enumerate(cols, 1):
        c = s.cell(lin, i, t)
        c.fill, c.font = CAB, CAB_FONTE
        c.alignment = Alignment(wrap_text=True)
    lin += 1

    def na_carteira(f):
        nm = f['nome'].upper()
        cd = f['codigo']
        if 'EMERG' in nm:
            return 'não: emergência'
        if 'C/SEDACAO' in nm or 'C/ SEDACAO' in nm:
            return 'não: sedação'
        if 'CORONARIA' in nm:
            return 'não: coronária'
        if 'ANGIO' in nm:
            return 'não: angiotomografia'
        if cd == '02.05.02.006-2':
            return 'sim: não ortopedia' if any(k in f['nome'] for k in NAO_ORTO) else 'não: IEV (ortopedia)'
        if cd == '02.05.02.016-0':
            return 'não: prejuízo'
        if cd == '02.06.01.004-4':
            return 'não: margem baixa'
        if cd == '02.06.01.007-9':
            return 'não: margem baixa' if 'C/CONTRASTE' in nm else 'sim'
        if cd == '02.05.02.018-6':
            return 'sim, menos 4.000 do IEV'
        return 'sim'

    for f in sorted(us + tc, key=lambda x: (x['codigo'], -x['fila'])):
        if f['codigo'] in codigos and f['fila'] >= 30:
            dec = na_carteira(f)
            s.append([f['codigo'], f['nome'].strip(), dec, f['fila'], f['fila_viva'], f['devolvidas'],
                      round(f['espera_mediana']), f['idade_mediana'], f['agendadas_12m'],
                      ', '.join(f'{a} ({b})' for a, b in f['cid_principais'])])
            s.cell(lin, 3).fill = VERDE if dec.startswith('sim') else VERMELHO
            for col in (4, 5, 6, 7, 9):
                s.cell(lin, col).number_format = INT
            lin += 1
    s.cell(lin + 1, 1, 'A coluna "Na carteira?" é pelo nome da fila, como aproximação. Os totais oficiais estão em Escolhidos, '
                       'que vêm da planilha de 09/11 (fila elegível, já sem a reserva do IEV e as filas pequenas).')
    s.column_dimensions['J'].width = 60
    s.freeze_panes = 'C5'

    # ---------- Saídas ----------
    o = wb.create_sheet('Saídas')
    titulo(o, 'As saídas para chegar ao valor pedido',
           'Marque "sim" na coluna Usar para somar. A conta parte da falta da aba Resumo.')
    cabecalho(o, 4, ['#', 'Saída', 'Quanto traz', 'Usar', 'A favor', 'Contra', 'Depende de'],
              [4, 44, 16, 8, 60, 60, 40])
    saidas = [
        (1, 'Doppler de membros como dois exames por pedido', "=Escolhidos!J{dop}", 'não',
         'fecha sozinha; o exame passa de 0,5% a cerca de 50% de margem',
         'a ficha do SIGTAP diz que é um exame só ("independe da quantidade de vasos")',
         'a SES autorizar por escrito (D-011)'),
        (2, 'Contar os pedidos novos dos 12 meses dos exames escolhidos', "=Escolhidos!L{tot}", 'não',
         'os mesmos exames; a regulação disse que a fila é dinâmica e aceita ajuste por aditivo (Despacho 219528407, item 4)',
         'metas acima da fila de hoje, o que a regulação já apontou; um mutirão da SES leva os pedidos; '
         'inclui 2.624 Doppler de membros',
         'escrever no plano que a meta conta com os pedidos novos; meta como teto'),
        (3, 'Resto da US de articulação (adulto)', "='Não escolhidos'!F{art}", 'não',
         'fila grande, que cresce cerca de 280 por mês; o IEV não tirou nenhum pedido dela',
         'conflita com a regra de 02/11 (L-008); margem de cerca de 37%',
         'a regulação dizer que não manda esses pedidos ao IEV'),
        (4, 'Transvaginal reservada ao IEV, depois da vigência', "='Não escolhidos'!F{tv}", 'não',
         'o IEV fez 20 consultas de ginecologia em seis meses',
         'só depois de maio de 2027; é o exame com mais faltas (43%) e mais trabalho',
         'execução que passe de maio de 2027'),
        (5, 'Voltar as angiotomografias (sem coronárias e sem crânio)', "='Não escolhidos'!F{angio}", 'não',
         'fila real, com espera de 3 a 6 meses; margem de 27%',
         'dá muito trabalho (decisão de 11/11); a clínica precisa confirmar o preço de R$ 225',
         'clínica com bomba injetora e protocolo vascular'),
        (6, 'Angiotomografia de coronárias', "='Não escolhidos'!F{cor}", 'não',
         'a maior fila de TC fora do plano, espera mediana de 265 dias',
         '30 min, betabloqueador e ECG pelo preço da TC de tórax; provavelmente não cobre a clínica',
         'cotação própria'),
        (7, 'Plano menor: metas e valor abaixo do recurso', 0, 'não',
         'nada sem fila nem exame difícil',
         'o recurso que sobra não é usado; a gestão é valor fixo, e o percentual dela sobe (8,44% hoje, teto de 8,5%)',
         'aceite do parlamentar e da SES'),
    ]
    idx = {o_[0]: i for i, o_ in enumerate(fora, 5)}
    art_l = 5 + next(i for i, x in enumerate(fora) if x[0].startswith('US de articulação de adulto'))
    tv_l = 5 + next(i for i, x in enumerate(fora) if x[0].startswith('US transvaginal, reserva'))
    angio_l = 5 + next(i for i, x in enumerate(fora) if x[0].startswith('Angiotomografias'))
    cor_l = 5 + next(i for i, x in enumerate(fora) if x[0].startswith('Angiotomografia de coronárias'))
    lin = 5
    for sd in saidas:
        num, nome, val, usar, fav, contra, dep = sd
        if isinstance(val, str):
            val = val.format(dop=dop_linha, tot=tot, art=art_l, tv=tv_l, angio=angio_l, cor=cor_l)
        o.append([num, nome, val, usar, fav, contra, dep])
        o.cell(lin, 3).number_format = MOEDA
        o.cell(lin, 4).fill = AMARELO
        for col in (2, 5, 6, 7):
            o.cell(lin, col).alignment = Alignment(wrap_text=True, vertical='top')
        lin += 1
    o.cell(lin + 1, 2, 'Falta hoje').font = NEGRITO
    o.cell(lin + 1, 3, '=Resumo!B6').number_format = MOEDA
    o.cell(lin + 2, 2, 'Soma das saídas marcadas').font = NEGRITO
    o.cell(lin + 2, 3, f'=SUMIFS(C5:C{lin - 1},D5:D{lin - 1},"sim")').number_format = MOEDA
    o.cell(lin + 3, 2, 'Falta depois das saídas (negativo = passa do valor)').font = NEGRITO
    o.cell(lin + 3, 3, f'=C{lin + 1}-C{lin + 2}').number_format = MOEDA
    o.cell(lin + 3, 3).font = Font(bold=True, color='C00000')
    o.cell(lin + 5, 2, 'Recomendação (conversa de 11/11): a 2 como base, com a 1 pedida à SES no mesmo pedido da parede '
                       'abdominal; a 3 de reserva, para a resposta da regulação sobre o IEV.')
    o.cell(lin + 6, 2, 'Se o Doppler de membros sair (condição da D-011 não atendida), a falta sobe pelo valor dele, '
                       'e a 2 perde os 2.624 pedidos novos dele: ver Resumo, B9.')

    # ---------- Da sobra à falta ----------
    p = wb.create_sheet('Da sobra à falta')
    titulo(p, 'De faltar R$ 245 mil para a falta de hoje',
           'A v26 pela Candanga (as metas assinadas, 09/11) contra a carteira escolhida, exame a exame.')
    cabecalho(p, 4, ['Exame', 'v26: quantidade', 'v26: valor pela Candanga', 'Hoje: quantidade', 'Hoje: valor',
                     'Diferença', 'Por quê'], [36, 12, 18, 12, 16, 16, 90])
    ponte = [
        ('US de mamas', 14689, 70.97, 12950, 'a meta da v26 passava da fila; ficou a fila de hoje (a SES fez mutirões)'),
        ('US transvaginal', 10541, 83.77, 5294, 'a meta passava da fila, e 4.000 ficaram reservados ao IEV'),
        ('Doppler de membros', 9834, 115.61, 12043, 'entrou toda a fila de hoje (condicionado à D-011)'),
        ('Doppler de carótidas', 4674, 115.61, 4727, 'a fila de hoje'),
        ('US de abdômen total, adulto e criança', 10028, 117.51, 10347, 'a fila de hoje; as crianças entraram (D-010)'),
        ('US de parede abdominal', 3138, 117.51, 3304, 'a fila de hoje (L-007)'),
        ('US de aparelho urinário, adulto e criança', 3944, 90.53, 4025, 'a fila de hoje; as crianças entraram'),
        ('US de tireoide, adulto e criança', 3216, 64.07, 3854, 'a fila de hoje; as crianças entraram'),
        ('US de próstata', 3201, 74.19, 2969, 'a meta passava da fila'),
        ('US de abdômen superior', 2261, 101.27, 2213, 'a meta passava da fila'),
        ('TC de abdômen superior', 4516, 309.25, 4184, 'a meta passava da fila'),
        ('TC de pelve', 3862, 309.25, 3690, 'a meta passava da fila'),
        ('TC de tórax', 3104, 309.25, 2530, 'a meta passava da fila'),
        ('Angiotomografia de coronárias', 1408, 309.25, 0, 'saiu: 30 min e ECG pelo preço da TC de tórax (02/11)'),
        ('TC de tórax de emergência', 728, 309.25, 0, 'saiu: só ambulatório (D-009)'),
        ('US de bolsa escrotal', 0, 100.00, 934, 'entrou: liberada em 02/11'),
        ('TC de pescoço', 0, 309.25, 479, 'entrou (11/11)'),
        ('TC de crânio sem contraste', 0, 251.29, 44, 'entrou'),
        ('Articulação, não ortopedia', 0, 70.97, 4610, 'entrou (11/11): partes moles, inguinal, pescoço, axila e infantis'),
    ]
    lin = 5
    for nome, q26, pr, qh, porque in ponte:
        p.append([nome, q26, f'=B{lin}*{pr}', qh, f'=D{lin}*{pr}', f'=E{lin}-C{lin}', porque])
        for col, fmt in ((2, INT), (3, MOEDA), (4, INT), (5, MOEDA), (6, MOEDA)):
            p.cell(lin, col).number_format = fmt
        lin += 1
    p.cell(lin, 1, 'Total').font = NEGRITO
    for col, L in ((2, 'B'), (3, 'C'), (4, 'D'), (5, 'E'), (6, 'F')):
        c = p.cell(lin, col, f'=SUM({L}5:{L}{lin - 1})')
        c.font = NEGRITO
        c.number_format = INT if col in (2, 4) else MOEDA
    p.cell(lin + 2, 1, 'Valor dos exames pedido')
    p.cell(lin + 2, 3, ALVO).number_format = MOEDA
    p.cell(lin + 3, 1, 'Faltava na v26 pela Candanga')
    p.cell(lin + 3, 3, f'=C{lin + 2}-C{lin}').number_format = MOEDA
    p.cell(lin + 4, 1, 'Falta hoje')
    p.cell(lin + 4, 3, f'=C{lin + 2}-E{lin}').number_format = MOEDA
    p.cell(lin + 4, 3).font = Font(bold=True, color='C00000')
    p.cell(lin + 6, 1, 'A diferença: os R$ 245 mil supunham que a v26 tinha pedido para todas as metas. Não tinha: '
                       'R$ 1,14 mi estava em exames sem fila ou já descartados (transvaginal, coronária, emergência, mama), '
                       'e as outras metas passavam um pouco da fila. Limitar cada exame à fila de hoje e tirar o que '
                       'foi decidido fora derrubou mais do que os exames novos repuseram.')
    p.cell(lin + 7, 1, 'A Candanga não mudou nada nessa conta: os dois lados usam o mesmo preço. A Candanga já tinha '
                       'feito a v26 cair de R$ 10,64 mi (Portaria) para R$ 10,39 mi.')
    p.cell(lin + 8, 1, 'A carteira de hoje (Escolhidos) usa a fila elegível da planilha de 09/11; as quantidades desta aba '
                       'somam a mesma coisa por exame.')

    # ---------- Estudos ----------
    t = wb.create_sheet('Estudos')
    titulo(t, 'Os estudos e as decisões por trás desta planilha')
    cabecalho(t, 3, ['Data', 'Arquivo', 'O que traz'], [11, 70, 90])
    est = [
        ('21/10', 'versoes/plano_v26_20261021.md', 'a carteira assinada: 79.144 exames em 11 códigos'),
        ('01/11', 'output/estudo_imagem_candanga_20261101.md', 'os quatro critérios de escolha: aparelho compartilhado, receita por hora, custo e fila'),
        ('01/11', 'output/plano4_mais_tc_ambulatorio_20261101.md', 'os mutirões da SES na mama e na transvaginal, por unidade'),
        ('02/11', 'estudos/estudo_filas_imagem_20261102.md', 'a carteira 1, o inventário de 656 filas e o rumo de cada código'),
        ('02/11', 'estudos/estudo_outros_planos_imagem_20261102.md', 'o que o IEV contratou; a reserva da transvaginal; o método de sobreposição'),
        ('08/11', 'estudos/analise_despacho_gediag_20261108.md', 'o parecer da GEDIAG; a seção 8.1 trata do risco da fila'),
        ('09/11', 'estudos/estudo_readequacao_candanga_margem_20261109.md', 'a margem de cada exame; cenários 1 (sobra de R$ 245 mil) e 2'),
        ('10/11', 'Despacho SEI 219528407 (CRDF), em Downloads', 'a fila da SES de 09/11 contra as metas da v26; pede idade mínima expressa'),
        ('10 e 11/11', 'pendencias.md, D-011 e D-012', 'as decisões exame a exame desta revisão'),
        ('—', 'dados/fontes/sigtap_0205010040_102026.md', 'a ficha do Doppler: o bilateral é um exame só'),
        ('02/11', 'dados/fontes/mapa_social_20261102_imagem.md', 'a coleta de onde vêm as filas desta planilha'),
    ]
    for row in est:
        t.append(list(row))
    t.cell(16, 1, 'Gerada por estudos/gerar_carteira_final_20261111.py.')

    wb.save(SAIDA)
    print('salvo', SAIDA, 'total na linha', tot, 'doppler na linha', dop_linha)


if __name__ == '__main__':
    main()
