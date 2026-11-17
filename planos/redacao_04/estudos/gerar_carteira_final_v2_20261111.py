"""Planilha da carteira final do plano 4, versão 2 (11/11/2026).

Muda em relação à v1 (carteira_final_20261111.xlsx), a pedido do usuário:
- uma coluna de fila só (a coleta de 02/11), sem a fila da SES;
- a US de articulação fora da ortopedia numa linha só, com o detalhe na aba Articulação;
- em Não escolhidos, o valor de cada grupo pela Candanga e o total que eles trariam ao plano;
- sem a aba Estudos; a v26 aparece como "versão enviada (PT v1)".

Fontes:
- estudo_readequacao_candanga_margem_20261109.xlsx, aba 1 (margem, fila e pedidos novos de cada candidato);
- dados/fontes/mapa_social_20261102_imagem_bruto/coleta_20261102.json (filas por nome e rumo por código);
- a Tabela SUS Candanga do main (biblioteca/precos/tabela_sus_candanga/tabela_sus_candanga.csv, modalidade SIA);
- pendencias.md, D-011 e D-012 (as decisões de 10 e 11/11).

Rodar da pasta planos/redacao_04:
    python3 estudos/gerar_carteira_final_v2_20261111.py
"""
import csv
import io
import json
import subprocess

import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

MARGEM = 'estudos/estudo_readequacao_candanga_margem_20261109.xlsx'
COLETA = 'dados/fontes/mapa_social_20261102_imagem_bruto/coleta_20261102.json'
SAIDA = 'estudos/carteira_final_v2_20261111.xlsx'
ALVO = 10636602  # valor dos exames: recurso menos o apoio (estudo de 05/11)
PRECO_ART = 70.97  # 02.05.02.006-2 pela Candanga

NEGRITO = Font(bold=True)
CAB = PatternFill('solid', fgColor='1F4E78')
CAB_FONTE = Font(bold=True, color='FFFFFF')
AMARELO = PatternFill('solid', fgColor='FFF2CC')
VERDE = PatternFill('solid', fgColor='E2EFDA')
VERMELHO = PatternFill('solid', fgColor='FCE4D6')
MOEDA = 'R$ #,##0.00'
INT = '#,##0'
PCT = '0%'
QUEBRA = Alignment(wrap_text=True, vertical='top')

CODIGO = {
    'TC de abdômen superior sem contraste': '02.06.03.001-0',
    'TC de pelve sem contraste': '02.06.03.003-7',
    'TC de tórax sem contraste': '02.06.02.003-1',
    'TC de crânio sem contraste': '02.06.01.007-9',
    'TC de abdômen superior com contraste': '02.06.03.001-0',
    'TC de pelve com contraste': '02.06.03.003-7',
    'TC de tórax com contraste': '02.06.02.003-1',
    'TC de pescoço com contraste': '02.06.01.005-2',
    'TC de crânio com contraste': '02.06.01.007-9',
    'TC de face e seios da face': '02.06.01.004-4',
    'Angiotomografias, sem as coronárias': 'vários',
    'Angiotomografia do crânio': '02.06.01.007-9',
    'US de abdômen superior': '02.05.02.003-8',
    'US de bolsa escrotal (adulto)': '02.05.02.007-0',
    'US de abdômen total (adulto)': '02.05.02.004-6',
    'US de parede abdominal': '02.05.02.004-6',
    'US de aparelho urinário e rins (adulto': '02.05.02.005-4',
    'Doppler de carótidas': '02.05.01.004-0',
    'US transvaginal': '02.05.02.018-6',
    'US de próstata': '02.05.02.010-0',
    'US de tireoide (com': '02.05.02.012-7',
    'US de mamas': '02.05.02.009-7',
    'US de abdômen total (criança)': '02.05.02.004-6',
    'US de aparelho urinário (criança)': '02.05.02.005-4',
    'US de bolsa escrotal (criança)': '02.05.02.007-0',
    'US de tireoide (criança)': '02.05.02.012-7',
    'Doppler de membros': '02.05.01.004-0',
}

DECISAO = {
    'TC de crânio com contraste': (False, 'margem de 10%; a SES agenda 1.909 por ano, a fila gira em 2 meses (11/11)'),
    'TC de face e seios da face': (False, 'margem de 13% e fila pequena (11/11)'),
    'Angiotomografias, sem as coronárias': (False, 'dá muito trabalho: injeção rápida, acesso calibroso, reconstrução (11/11)'),
    'Angiotomografia do crânio': (False, 'margem de 10% e a maior exigência (11/11)'),
    'Doppler de membros': (True, 'CONDICIONADO (D-011): só vale se contar como dois exames; está dentro da conta como um exame'),
    'TC de pescoço com contraste': (True, 'mesmo preço e custo das TC grandes; perfil oncológico (11/11)'),
}

# filas do código da articulação que não são ortopedia e entram (D-012, 11/11)
NAO_ORTO = ['ECOGRAFIA  DE PARTES MOLES', 'REGIAO INGUINAL', 'REGIÃO INGUINAL', 'PESCOCO', 'CERVICAL',
            'SUBMANDIBULARES', 'AXILA', 'COLUNA LOMBAR', 'USG QUADRIL', 'COXO-FEMURAL E INFANTIL',
            'COXO-FEMURAL D INFANTIL', 'REGIAO LOMBAR']  # joelho, punho, tornozelo e cotovelo infantis são ortopedia

TC_IEV = ('02.06.01.001-0', '02.06.01.002-8', '02.06.01.003-6', '02.06.02.001-5', '02.06.03.002-9', '02.06.02.002-3')


def chave(nome, tabela):
    return next((k for k in tabela if nome.startswith(k)), None)


def candanga():
    txt = subprocess.run(['git', 'show', 'main:biblioteca/precos/tabela_sus_candanga/tabela_sus_candanga.csv'],
                         capture_output=True, text=True, check=True).stdout
    return {r['codigo_sigtap']: float(r['valor']) for r in csv.DictReader(io.StringIO(txt))
            if r['modalidade'] == 'SIA' and r['valor']}


def cabecalho(ws, linha, titulos, larguras):
    for i, t in enumerate(titulos, 1):
        c = ws.cell(linha, i, t)
        c.fill, c.font, c.alignment = CAB, CAB_FONTE, QUEBRA
    for i, w in enumerate(larguras, 1):
        ws.column_dimensions[get_column_letter(i)].width = w


def titulo(ws, texto, sub=None):
    ws['A1'] = texto
    ws['A1'].font = Font(bold=True, size=14)
    if sub:
        ws['A2'] = sub


def main():
    m = openpyxl.load_workbook(MARGEM, data_only=True)['1 Margem por exame']
    cand = [dict(nome=r[0], mod=r[1], preco=r[2], minutos=r[3], custo=r[4], margem=r[6], fila=r[10], novos=r[11],
                 porque=r[14]) for r in m.iter_rows(min_row=4, values_only=True) if r[1] in ('US', 'TC')]
    coleta = json.load(open(COLETA))
    pano = coleta['panorama']
    us, tc = pano['ultrassonografia']['filas'], pano['tomografia']['filas']
    todas = [f for mod in pano.values() for f in mod['filas']]
    rumo = {r['codigo']: r for r in coleta['rumo']}
    preco = candanga()
    custo15 = next(c['custo'] for c in cand if c['nome'].startswith('US de abdômen superior'))
    art = [f for f in us if f['codigo'] == '02.05.02.006-2' and any(k in f['nome'] for k in NAO_ORTO)]

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Resumo'

    # ---------- Articulação (detalhe) ----------
    a = wb.create_sheet('Articulação')
    titulo(a, 'US de articulação: as filas que não são ortopedia (entram na carteira)',
           'Código 02.05.02.006-2, preço da Candanga R$ 70,97. Decisão de 11/11 (D-012): a OCI do IEV é de ortopedia, '
           'e estas filas não são. As de adulto (ombro, punho, joelho, tornozelo, cotovelo, mão, pé) ficam fora.')
    cabecalho(a, 4, ['Fila', 'Grupo', 'Pedidos (02/11)', 'Menos de 24 meses', 'Espera mediana (dias)', 'Idade mediana',
                     'Motivos mais pedidos (CID)', 'Preço Candanga', 'Valor'], [50, 22, 11, 11, 11, 10, 60, 13, 15])

    def grupo(nm):
        if 'PARTES MOLES' in nm:
            return 'partes moles'
        if 'INGUINAL' in nm:
            return 'região inguinal'
        if 'AXILA' in nm:
            return 'axila'
        if any(k in nm for k in ('PESCOCO', 'CERVICAL', 'SUBMANDIBULARES')):
            return 'pescoço e cervical'
        return 'infantil (quadril e coluna)'

    lin = 5
    for f in sorted(art, key=lambda x: (grupo(x['nome']), -x['fila'])):
        a.append([f['nome'].strip(), grupo(f['nome']), f['fila'], f['fila_viva'], round(f['espera_mediana']),
                  f['idade_mediana'], ', '.join(f'{x} ({y})' for x, y in f['cid_principais']), PRECO_ART,
                  f'=C{lin}*H{lin}'])
        for col, fmt in ((3, INT), (4, INT), (5, INT), (8, MOEDA), (9, MOEDA)):
            a.cell(lin, col).number_format = fmt
        lin += 1
    art_tot = lin
    a.cell(art_tot, 1, 'Total').font = NEGRITO
    for col, L, fmt in ((3, 'C', INT), (4, 'D', INT), (9, 'I', MOEDA)):
        c = a.cell(art_tot, col, f'=SUM({L}5:{L}{art_tot - 1})')
        c.font, c.number_format = NEGRITO, fmt
    a.cell(art_tot + 2, 1, 'Por grupo').font = NEGRITO
    for i, g in enumerate(['partes moles', 'região inguinal', 'pescoço e cervical', 'axila', 'infantil (quadril e coluna)']):
        r = art_tot + 3 + i
        a.cell(r, 1, g)
        a.cell(r, 3, f'=SUMIFS(C5:C{art_tot - 1},B5:B{art_tot - 1},A{r})').number_format = INT
        a.cell(r, 9, f'=SUMIFS(I5:I{art_tot - 1},B5:B{art_tot - 1},A{r})').number_format = MOEDA
    a.cell(art_tot + 9, 1, 'Cuidado: o código é o mesmo da articulação de ortopedia. Na lista de filas do plano, a regulação '
                           'precisa ver pelo nome que só estas entram. Partes moles tem fila velha: 1.246 pedidos com mais de '
                           '24 meses.')
    a.freeze_panes = 'B5'

    # ---------- Escolhidos ----------
    e = wb.create_sheet('Escolhidos', 1)
    titulo(e, 'Exames escolhidos',
           'Fila = coleta do Mapa Social de 02/11. Quantidade = a fila. Valor = quantidade × preço da Candanga. '
           'A quantidade em amarelo pode ser mudada.')
    cabecalho(e, 4, ['Exame', 'Mod.', 'Código SIGTAP', 'Fila (02/11)', 'Preço Candanga', 'Minutos',
                     'Margem (% do preço)', 'Quantidade na carteira', 'Valor', 'Margem em R$', 'Pedidos novos em 12 meses',
                     'Valor dos pedidos novos', 'Motivo / observação'],
              [44, 6, 16, 12, 13, 9, 11, 12, 16, 15, 12, 16, 70])
    lin, dop = 5, None
    linhas = []
    linha_de = {}
    for c in cand:
        entra, motivo = DECISAO.get(chave(c['nome'], DECISAO), (True, c['porque']))
        if entra:
            linhas.append([c['nome'], c['mod'], CODIGO[chave(c['nome'], CODIGO)], c['fila'], c['preco'], c['minutos'],
                           c['margem'], c['fila'], None, None, c['novos'], None, motivo])
    linhas.append(['US de articulação, só o que não é ortopedia (detalhe na aba Articulação)', 'US', '02.05.02.006-2',
                   f"=Articulação!C{art_tot}", PRECO_ART, 15, (PRECO_ART - custo15) / PRECO_ART, f'=D{{lin}}', None, None, 0,
                   None, 'partes moles, inguinal, pescoço, axila e infantis; fora da OCI de ortopedia do IEV (D-012, 11/11); '
                         'margem estimada com o custo do exame de 15 min'])
    for row in linhas:
        row = [x.format(lin=lin) if isinstance(x, str) and '{lin}' in x else x for x in row]
        row[8] = f'=H{lin}*E{lin}'
        row[9] = f'=I{lin}*G{lin}'
        row[11] = f'=K{lin}*E{lin}'
        e.append(row)
        linha_de[row[0]] = lin
        e.cell(lin, 8).fill = AMARELO
        if row[0].startswith('Doppler de membros'):
            dop = lin
            for col in range(1, 14):
                e.cell(lin, col).fill = AMARELO
        for col, fmt in ((4, INT), (5, MOEDA), (7, PCT), (8, INT), (9, MOEDA), (10, MOEDA), (11, INT), (12, MOEDA)):
            e.cell(lin, col).number_format = fmt
        lin += 1
    tot = lin
    e.cell(tot, 1, 'Total').font = NEGRITO
    cols_tot = ((4, 'D', INT), (8, 'H', INT), (9, 'I', MOEDA), (10, 'J', MOEDA), (11, 'K', INT), (12, 'L', MOEDA))
    for col, L, fmt in cols_tot:
        c = e.cell(tot, col, f'=SUM({L}5:{L}{tot - 1})')
        c.font, c.number_format = NEGRITO, fmt
    e.cell(tot, 7, f'=J{tot}/I{tot}').number_format = PCT
    # subtotais por modalidade e sem o Doppler de membros
    for i, (rot, crit) in enumerate([('  Ultrassom', 'US'), ('  Tomografia', 'TC')]):
        r = tot + 1 + i
        e.cell(r, 1, rot)
        for col, L, fmt in cols_tot:
            e.cell(r, col, f'=SUMIFS({L}5:{L}{tot - 1},B5:B{tot - 1},"{crit}")').number_format = fmt
        e.cell(r, 7, f'=J{r}/I{r}').number_format = PCT
    r = tot + 3
    e.cell(r, 1, 'Total sem o Doppler de membros (se a D-011 não for atendida)').font = NEGRITO
    for col, L, fmt in cols_tot:
        e.cell(r, col, f'={L}{tot}-{L}{dop}').number_format = fmt
    e.cell(r, 7, f'=J{r}/I{r}').number_format = PCT
    e.cell(tot + 5, 1, 'Margem em R$ = valor × margem %, com o médico do ultrassom pago por hora (planilha de 09/11). '
                       'É a folga para executar, e não lucro. Na articulação, a margem é estimada com o custo do exame de 15 min.')
    e.freeze_panes = 'B5'

    # ---------- Resumo ----------
    titulo(ws, 'Plano 4 — carteira final pela Tabela SUS Candanga',
           'Controle interno, 11/11/2026. Filas da coleta do Mapa Social de 02/11; preço da Candanga (SIA). '
           'Amarelo é premissa que pode mudar. Tudo é fórmula sobre as outras abas.')
    res = [
        ('Valor dos exames pedido (recurso menos o apoio)', ALVO, MOEDA),
        ('Carteira escolhida (aba Escolhidos)', f'=Escolhidos!I{tot}', MOEDA),
        ('Falta para fechar', '=B4-B5', MOEDA),
        ('Exames na carteira', f'=Escolhidos!H{tot}', INT),
        ('O Doppler de membros está dentro, como um exame por pedido', f'=Escolhidos!I{dop}', MOEDA),
        ('Falta, se o Doppler de membros ficar fora', '=B6+B8', MOEDA),
        ('Sobra (negativo) ou falta, se o Doppler contar como dois exames (D-011)', '=B6-B8', MOEDA),
        ('Pedidos novos de 12 meses dos exames escolhidos (valor)', f'=Escolhidos!L{tot}', MOEDA),
        ('Valor dos não escolhidos que cabem no aparelho do plano', "='Não escolhidos'!G{cabe}", MOEDA),
    ]
    res += [
        ('Margem da carteira em R$ (folga para executar)', f'=Escolhidos!J{tot}', MOEDA),
        ('Margem da carteira, em % do valor', f'=Escolhidos!G{tot}', PCT),
        ('Exames de ultrassom / de tomografia', f'=TEXT(Escolhidos!H{tot + 1},"#,##0")&" / "&TEXT(Escolhidos!H{tot + 2},"#,##0")', None),
    ]
    for i, (rot, val, fmt) in enumerate(res, 4):
        ws.cell(i, 1, rot)
        if fmt:
            ws.cell(i, 2, val).number_format = fmt
        else:
            ws.cell(i, 2, val)
    ws['B4'].fill = AMARELO
    ws['B6'].font = Font(bold=True, color='C00000')
    ws.cell(17, 1, 'Como ler').font = NEGRITO
    for i, t in enumerate([
        'Escolhidos: os exames que entram, com a fila, o preço da Candanga, a margem e o valor.',
        'Articulação: as filas do código da articulação que não são ortopedia, uma a uma.',
        'Não escolhidos: o que ficou fora, com o valor que traria ao plano e o motivo.',
        'Estudos das filas: o rumo de cada código e cada fila pelo nome.',
        'Saídas: as formas de chegar ao valor pedido; marque "sim" para somar.',
        'Da sobra à falta: como se sai de faltar R$ 245 mil (versão enviada pela Candanga) para a falta de hoje.',
        'Agenda da SES: quem entra na fila por mês e quanto da agenda da SES a rede do plano assume nos exames fáceis.',
        'Na tomografia, a fila que a SES mediu em 09/11 (Despacho SEI 219528407) tem cerca de 1.357 pedidos a menos '
        'que a coleta de 02/11, cerca de R$ 420 mil.',
    ], 18):
        ws.cell(i, 1, '- ' + t)
    ws.column_dimensions['A'].width = 70
    ws.column_dimensions['B'].width = 20

    # ---------- Não escolhidos ----------
    n = wb.create_sheet('Não escolhidos', 3)
    titulo(n, 'O que ficou fora, e o valor que traria ao plano',
           'Valor = pedidos de cada fila × preço do código na Candanga, somado fila a fila. '
           '"Cabe no aparelho" = sim quando usa o ultrassom ou o tomógrafo do plano e poderia fechar a falta.')
    cabecalho(n, 4, ['Fila', 'Código SIGTAP', 'Grupo', 'Pedidos (02/11)', 'Preço Candanga', 'Filas sem preço',
                     'Valor que traria', 'Cabe no aparelho', 'Margem (% do preço)', 'Motivo'],
              [52, 16, 22, 12, 13, 10, 16, 10, 11, 80])

    def soma(filtro):
        sel = [f for f in todas if filtro(f)]
        ped = sum(f['fila'] for f in sel)
        val = sum(f['fila'] * preco[f['codigo']] for f in sel if f['codigo'] in preco)
        sem = sum(1 for f in sel if f['codigo'] not in preco)
        return ped, val, sem

    emerg = lambda f: 'EMERG' in f['nome'].upper()
    fora = []
    for c in cand:
        k = chave(c['nome'], DECISAO)
        if k and not DECISAO[k][0]:
            fora.append([c['nome'], CODIGO[chave(c['nome'], CODIGO)], 'decisão desta revisão', c['fila'], c['preco'], 0,
                         c['fila'] * c['preco'], 'sim', c['margem'], DECISAO[k][1]])
    ped_art = sum(f['fila'] for f in us if f['codigo'] == '02.05.02.006-2' and not any(k in f['nome'] for k in NAO_ORTO))
    grupos = [
        ('US pélvica ginecológica, adulto e infantil', '02.05.02.016-0', 'decisão desta revisão',
         soma(lambda f: f['codigo'] == '02.05.02.016-0' and not emerg(f)),
         43.41, 'sim', (43.41 - custo15) / 43.41, 'cada exame dá prejuízo: paga R$ 43,41 e custa R$ 44,99 (09/11 e 11/11)'),
        ('US de articulação de ortopedia (ombro, punho, joelho, tornozelo, cotovelo, mão, pé; adulto e criança)', '02.05.02.006-2', 'IEV',
         (ped_art, ped_art * PRECO_ART, 0), PRECO_ART, 'sim', (PRECO_ART - custo15) / PRECO_ART,
         'OCI de ortopedia com ultrassom do IEV (19.070 contratadas); volta se a regulação disser por escrito que não '
         'manda esses pedidos ao IEV (L-008)'),
        ('US transvaginal, reserva do IEV', '02.05.02.018-6', 'IEV', (4000, 4000 * 83.77, 0), 83.77, 'sim',
         next(c['margem'] for c in cand if c['nome'].startswith('US transvaginal')),
         'OCI de ginecologia (GIN1) do IEV, 3.218 contratadas; a reserva vale até o fim da vigência, por volta de 05/2027'),
        ('TC de coluna, articulações e segmentos', 'vários', 'IEV',
         soma(lambda f: f['codigo'] in TC_IEV and not emerg(f)), None, 'sim', None,
         'compatíveis com a OCI de ortopedia com tomografia do IEV (L-008)'),
        ('Angiotomografia de coronárias', '02.06.02.003-1', 'regra do plano', (1532, 1532 * 309.25, 0), 309.25, 'sim',
         None, '30 min, betabloqueador e ECG pelo preço da TC de tórax; a clínica provavelmente não cobre (02/11)'),
        ('Filas de emergência (todas com "EMERG", qualquer modalidade)', 'vários', 'regra do plano', soma(emerg), None,
         'não', None, 'só ambulatório (D-009)'),
        ('US transfontanela', '02.05.02.017-8', 'regra do plano',
         soma(lambda f: f['codigo'] == '02.05.02.017-8' and not emerg(f)), None, 'sim', None,
         'saiu em 03/11, a pedido do usuário'),
        ('TC com sedação', 'vários', 'regra do plano',
         soma(lambda f: f in tc and 'C/SEDACAO' in f['nome'].upper() and not emerg(f)), None, 'não', None,
         'precisa de anestesia'),
        ('Ecocardiografia', '02.05.01.00x', 'outra equipe ou aparelho',
         soma(lambda f: f in us and 'ECOCARDIO' in f['nome'].upper() and not emerg(f)), None, 'não', None,
         'outra equipe (cardiologia)'),
        ('US de globo ocular', '02.05.02.008-9', 'outra equipe ou aparelho',
         soma(lambda f: f['codigo'] == '02.05.02.008-9' and not emerg(f)), None, 'não', None, 'outra equipe (oftalmologia)'),
        ('US obstétricas', '02.05.02.014-3 e 015-1', 'outra equipe ou aparelho',
         soma(lambda f: f['codigo'] in ('02.05.02.014-3', '02.05.02.015-1') and not emerg(f)), None, 'não', None,
         'outra equipe'),
        ('Radiologia (mamografia, densitometria e outras)', '02.04*', 'outra equipe ou aparelho',
         soma(lambda f: f in pano['radiologia']['filas'] and not emerg(f)), None, 'não', None,
         'outro aparelho; fora do objeto'),
        ('Ressonância', '02.07*', 'outra equipe ou aparelho',
         soma(lambda f: f in pano['ressonância magnética']['filas'] and not emerg(f)), None, 'não', None,
         'outro aparelho; fora do objeto'),
        ('Medicina nuclear', '02.08*', 'outra equipe ou aparelho',
         soma(lambda f: f in pano['medicina nuclear']['filas'] and not emerg(f)), None, 'não', None,
         'outro aparelho; fora do objeto'),
    ]
    for nome, cod, grp, (ped, val, sem), pr, cabe, marg, motivo in grupos:
        fora.append([nome, cod, grp, ped, pr, sem, val, cabe, marg, motivo])
    lin = 5
    pos = {}
    for row in fora:
        n.append(row)
        pos[row[0]] = lin
        for col, fmt in ((4, INT), (5, MOEDA), (6, INT), (7, MOEDA), (9, PCT)):
            n.cell(lin, col).number_format = fmt
        n.cell(lin, 8).fill = VERDE if row[7] == 'sim' else VERMELHO
        n.cell(lin, 10).alignment = QUEBRA
        lin += 1
    ult = lin - 1
    for i, (rot, form) in enumerate([
        ('Total que cabe no aparelho do plano', f'=SUMIFS(G5:G{ult},H5:H{ult},"sim")'),
        ('Total que precisa de outra equipe ou aparelho', f'=SUMIFS(G5:G{ult},H5:H{ult},"não")'),
        ('Total de tudo o que ficou fora', f'=SUM(G5:G{ult})'),
    ]):
        r = lin + 1 + i
        n.cell(r, 1, rot).font = NEGRITO
        c = n.cell(r, 7, form)
        c.font, c.number_format = NEGRITO, MOEDA
        n.cell(r, 4, f'=SUMIFS(D5:D{ult},H5:H{ult},"{["sim", "não"][i]}")' if i < 2 else f'=SUM(D5:D{ult})').number_format = INT
    cabe_l = lin + 1
    n.cell(lin + 5, 1, 'Os grupos de emergência, radiologia, ressonância e medicina nuclear somam várias filas e códigos; '
                       '"Filas sem preço" conta as filas cujo código não está na Candanga (SIA) e por isso não entram no valor.')
    n.freeze_panes = 'B5'
    ws['B12'] = f"='Não escolhidos'!G{cabe_l}"

    # ---------- Estudos das filas ----------
    s = wb.create_sheet('Estudos das filas')
    titulo(s, 'O rumo de cada código e cada fila pelo nome (coleta de 02/11/2026)',
           'Saldo = entradas − oferta por mês (negativo: a fila cai). Meses para zerar = fila ÷ queda por mês, nas duas janelas: '
           'os 12 meses mostram o ritmo normal, os 3 últimos pegam mutirões. É projeção, não previsão. '
           'A fila do código inclui emergência e filas fora do plano: ver a aba Conferência.')
    cabecalho(s, 4, ['Código', 'Fila maior do código', 'Fila do código', 'Fila de menos de 24 meses', 'Devolvidas',
                     'Entram por mês (12 m)', 'Oferta por mês (12 m)', 'Oferta por mês (3 últimos)', 'Realizados em 12 m',
                     'Faltas em 12 m', 'Falta (% dos agendados)', 'Saldo por mês, 12 m (entra − oferta)',
                     'Saldo por mês, 3 últimos', 'Meses para zerar, 12 m', 'Meses para zerar, 3 últimos', 'Pico da oferta'],
              [16, 50, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 12, 12, 16])
    codigos = ['02.05.02.009-7', '02.05.01.004-0', '02.05.02.004-6', '02.05.02.018-6', '02.05.02.005-4', '02.05.02.012-7',
               '02.05.02.010-0', '02.05.02.003-8', '02.05.02.007-0', '02.05.02.006-2', '02.05.02.016-0', '02.06.03.001-0',
               '02.06.03.003-7', '02.06.02.003-1', '02.06.01.005-2', '02.06.01.007-9', '02.06.01.004-4']
    lin = 5
    for cd in codigos:
        r = rumo[cd]
        s.append([cd, r['fila_maior'], r['fila'], r['fila_viva'], r['devolvidas'], round(r['entrantes_12m'] / 12),
                  round(r['oferta_12m'] / 12), round(r['oferta_media_3m']), r['realizados_12m'], r['faltas_12m'],
                  r['falta_12m'], f'=F{lin}-G{lin}', f'=F{lin}-H{lin}',
                  f'=IF(L{lin}<0,C{lin}/-L{lin},"não zera")', f'=IF(M{lin}<0,C{lin}/-M{lin},"não zera")',
                  f"{r['pico_oferta_mes']} ({r['pico_oferta']})"])
        for col in (3, 4, 5, 6, 7, 8, 9, 10, 12, 13):
            s.cell(lin, col).number_format = INT
        s.cell(lin, 11).number_format = PCT
        s.cell(lin, 14).number_format = '0.0'
        s.cell(lin, 15).number_format = '0.0'
        lin += 1
    lin += 2
    s.cell(lin, 1, 'Cada fila pelo nome, nos códigos acima (filas com 30 pedidos ou mais)').font = Font(bold=True, size=12)
    lin += 1
    for i, t in enumerate(['Código', 'Fila', 'Na carteira?', 'Pedidos', 'Menos de 24 meses', 'Devolvidas',
                           'Espera mediana (dias)', 'Idade mediana', 'Agendadas em 12 m', 'Motivos mais pedidos (CID)'], 1):
        c = s.cell(lin, i, t)
        c.fill, c.font, c.alignment = CAB, CAB_FONTE, QUEBRA
    lin += 1

    def na_carteira(f):
        nm, cd = f['nome'].upper(), f['codigo']
        if 'EMERG' in nm:
            return 'não: emergência'
        if 'C/SEDACAO' in nm:
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
                      ', '.join(f'{x} ({y})' for x, y in f['cid_principais'])])
            s.cell(lin, 3).fill = VERDE if dec.startswith('sim') else VERMELHO
            for col in (4, 5, 6, 7, 9):
                s.cell(lin, col).number_format = INT
            lin += 1
    s.cell(lin + 1, 1, 'A coluna "Na carteira?" é pelo nome da fila, como aproximação. Os totais oficiais estão em '
                       'Escolhidos, que vêm da planilha de 09/11 (fila elegível, já sem a reserva do IEV e as filas pequenas).')
    s.column_dimensions['J'].width = 60
    s.freeze_panes = 'C5'

    # ---------- Agenda da SES ----------
    g = wb.create_sheet('Agenda da SES')
    titulo(g, 'Fechar a falta com os exames fáceis: pedidos novos e parte da agenda da SES',
           'Quem entra na fila por mês, quanto a SES agenda e realiza (12 meses, filas do plano, estudo de 02/11), e quanto '
           'a rede do plano assume. Cada exame assumido libera a vaga na agenda da SES para outro atendimento.')
    g['A3'] = 'Parte do que a SES realiza que a rede do plano assume (12 meses)'
    g['F3'] = 0.081  # fecha a falta com o Doppler de membros dentro (11/11)
    g['F3'].fill, g['F3'].number_format = AMARELO, PCT
    g['H3'] = 'Contar os pedidos novos destes exames?'
    g['K3'] = 'sim'
    g['K3'].fill = AMARELO
    cabecalho(g, 5, ['Exame', 'Código', 'Complexidade (1 fácil a 3)', 'Margem (% do preço)', 'Preço Candanga', 'Minutos',
                     'Entram na fila por mês', 'Entram em 12 meses', 'SES agenda por mês', 'SES realiza por mês',
                     'SES realiza em 12 meses', 'Falta na SES', 'Usar', 'Pedidos novos em 12 meses (Escolhidos)',
                     'Exames assumidos da SES', 'Exames a mais na carteira', 'Valor a mais', 'Margem a mais',
                     'Horas de sala a mais', 'Vagas que a SES libera', 'Horas de sala que a SES libera'],
              [34, 15, 11, 10, 12, 8, 10, 11, 10, 10, 11, 9, 7, 12, 11, 11, 15, 14, 11, 11, 11])
    dem = {x['codigo']: x for x in json.load(open('estudos/estudo_filas_imagem_20261102.json'))['revisao']['demanda']}
    cplx = {r[0]: r[9] for r in m.iter_rows(min_row=4, values_only=True) if r[1] in ('US', 'TC')}
    fila_dop = dem['02.05.01.004-0']['fila_elegivel']
    faceis = [  # (prefixo em Escolhidos, código, parte do fluxo do código, usar)
        ('US de abdômen superior', '02.05.02.003-8', 1, 'sim'),
        ('US de abdômen total (adulto)', '02.05.02.004-6', 1, 'sim'),
        ('US de aparelho urinário e rins', '02.05.02.005-4', 1, 'sim'),
        ('Doppler de carótidas', '02.05.01.004-0', None, 'sim'),
        ('US de bolsa escrotal (adulto)', '02.05.02.007-0', 1, 'sim'),
        ('US de próstata', '02.05.02.010-0', 1, 'sim'),
        ('US de tireoide (com', '02.05.02.012-7', 1, 'sim'),
        ('TC de abdômen superior com contraste', '02.06.03.001-0', 1, 'não'),
        ('TC de pelve com contraste', '02.06.03.003-7', 1, 'não'),
        ('TC de tórax com contraste', '02.06.02.003-1', 1, 'não'),
    ]
    lin = 6
    for pref, cd, parte, usar in faceis:
        nome = next(k for k in linha_de if k.startswith(pref))
        el = linha_de[nome]
        x = dem[cd]
        if parte is None:  # carótidas: a parte delas no fluxo do código do Doppler, pela fila
            parte = e.cell(el, 4).value / fila_dop
        g.append([nome, cd, cplx.get(nome), f'=Escolhidos!G{el}', f'=Escolhidos!E{el}', f'=Escolhidos!F{el}',
                  round(x['entram_elegivel_mes'] * parte), f'=G{lin}*12', round(x['ses_agenda_elegivel_mes'] * parte),
                  round(x['ses_realiza_elegivel_mes'] * parte), f'=J{lin}*12', x['falta_ses'], usar,
                  f'=Escolhidos!K{el}',
                  f'=IF(M{lin}="sim",ROUND(K{lin}*$F$3,0),0)',
                  f'=IF(M{lin}="sim",O{lin}+IF($K$3="sim",N{lin},0),0)',
                  f'=P{lin}*E{lin}', f'=Q{lin}*D{lin}',
                  f'=IF(B{lin}<"02.06",P{lin}*F{lin}/60,0)',
                  f'=ROUND(O{lin}/(1-L{lin}),0)', f'=T{lin}*F{lin}/60'])
        g.cell(lin, 13).fill = AMARELO
        for col, fmt in ((4, PCT), (5, MOEDA), (7, INT), (8, INT), (9, INT), (10, INT), (11, INT), (12, PCT),
                         (14, INT), (15, INT), (16, INT), (17, MOEDA), (18, MOEDA), (19, INT), (20, INT), (21, INT)):
            g.cell(lin, col).number_format = fmt
        lin += 1
    tot_ag = lin
    g.cell(tot_ag, 1, 'Total').font = NEGRITO
    for col in (7, 8, 9, 10, 11, 14, 15, 16, 17, 18, 19, 20, 21):
        L = get_column_letter(col)
        c = g.cell(tot_ag, col, f'=SUM({L}6:{L}{tot_ag - 1})')
        c.font = NEGRITO
        c.number_format = MOEDA if col in (17, 18) else INT
    r0 = tot_ag + 2
    conta = [
        ('Falta hoje (Resumo)', '=Resumo!B6', MOEDA),
        ('Valor a mais com os exames marcados', f'=Q{tot_ag}', MOEDA),
        ('Falta depois (negativo = passa do valor)', f'=F{r0}-F{r0 + 1}', MOEDA),
        ('Parte que fecha a falta exata, com os pedidos novos (só os exames marcados)',
         f'=IF(SUMIFS(K6:K{tot_ag - 1},M6:M{tot_ag - 1},"sim")=0,"",'
         f'MAX(0,F{r0}-IF(K3="sim",SUMPRODUCT((M6:M{tot_ag - 1}="sim")*N6:N{tot_ag - 1}*E6:E{tot_ag - 1}),0))'
         f'/SUMPRODUCT((M6:M{tot_ag - 1}="sim")*K6:K{tot_ag - 1}*E6:E{tot_ag - 1}))', PCT),
        ('Horas de ultrassom da carteira (Escolhidos)',
         f'=SUMPRODUCT((Escolhidos!B5:B{tot - 1}="US")*Escolhidos!H5:H{tot - 1}*Escolhidos!F5:F{tot - 1})/60', INT),
        ('Horas de ultrassom a mais', f'=S{tot_ag}', INT),
        ('Salas de ultrassom', 14, INT),
        ('Horas de exame por sala em 12 meses (168 por mês)', 168 * 12, INT),
        ('Uso das salas', f'=(F{r0 + 4}+F{r0 + 5})/(F{r0 + 6}*F{r0 + 7})', PCT),
        ('Uso das salas sem o Doppler de membros',
         f'=(F{r0 + 4}+F{r0 + 5}-Escolhidos!H{dop}*Escolhidos!F{dop}/60)/(F{r0 + 6}*F{r0 + 7})', PCT),
    ]
    for i, (rot, form, fmt) in enumerate(conta):
        g.cell(r0 + i, 1, rot).font = NEGRITO if i in (2, 3, 8) else Font()
        c = g.cell(r0 + i, 6, form)
        c.number_format = fmt
    g.cell(r0 + 6, 6).fill = AMARELO
    g.cell(r0 + 7, 6).fill = AMARELO
    g.cell(r0 + 2, 6).font = Font(bold=True, color='C00000')
    notas = [
        'Como ler: "Entram na fila" é quem a atenção primária e os ambulatórios põem na fila por mês. Hoje a SES agenda '
        'a maior parte e realiza cerca de 60%; o resto falta.',
        'Os pedidos novos são a parte que a SES não dá conta e que faz a fila crescer: assumi-los não tira nada da SES. '
        'Eles já estão na saída 2 (aba Saídas), e não somam de novo.',
        'Os exames assumidos da SES são a parte do que ela realiza que passa à rede do plano. A conta usa o que a SES '
        'realiza, e não o que agenda, para não contar falta como exame.',
        'A vaga liberada é a da agenda da SES (realizado ÷ (1 − falta)): a SES pode usá-la em outra fila do mesmo '
        'aparelho, como o Doppler de membros, a articulação de ortopedia ou o paciente internado.',
        'Depende da regulação: o ultrassom está nos panoramas 1 e 2, sob gestão das Regiões de Saúde (Despacho 219528407, '
        'item 5). A transferência precisa ser pactuada por Região e escrita no plano (o pedido novo e a parte da agenda vão '
        'ao projeto).',
        'Complexidade e margem vêm da planilha de 09/11 (médico pago por hora). Carótidas: a parte delas no fluxo do '
        'código do Doppler é a parte da fila (28%). As TC ficam marcadas "não": margem de 27% e contraste.',
    ]
    for i, t in enumerate(notas):
        g.cell(r0 + len(conta) + 1 + i, 1, '- ' + t)
    g.freeze_panes = 'B6'

    # ---------- Saídas ----------
    o = wb.create_sheet('Saídas')
    titulo(o, 'As saídas para chegar ao valor pedido', 'Marque "sim" na coluna Usar para somar. A conta parte da falta do Resumo.')
    cabecalho(o, 4, ['Nº', 'Saída', 'Quanto traz', 'Usar', 'A favor', 'Contra', 'Depende de'], [5, 44, 16, 8, 60, 60, 40])
    nf = lambda nome: f"='Não escolhidos'!G{pos[nome]}"
    saidas = [
        (1, 'Doppler de membros como dois exames por pedido', f'=Escolhidos!I{dop}',
         'fecha sozinha; o exame passa de 0,5% a cerca de 50% de margem',
         'a ficha do SIGTAP diz que é um exame só ("independe da quantidade de vasos")',
         'a SES autorizar por escrito (D-011)'),
        (2, 'Contar os pedidos novos dos 12 meses dos exames escolhidos, sem o Doppler de membros',
         f'=Escolhidos!L{tot}-Escolhidos!L{dop}',
         'os mesmos exames; a regulação disse que a fila é dinâmica e aceita ajuste por aditivo (Despacho 219528407, item 4)',
         'metas acima da fila de hoje, o que a regulação já apontou; um mutirão da SES leva os pedidos',
         'escrever no plano que a meta conta com os pedidos novos; meta como teto'),
        ('2b', 'Pedidos novos dos 12 meses do Doppler de membros (2.624)', f'=Escolhidos!L{dop}',
         'mesma lógica da 2', 'só vale se o Doppler de membros ficar na carteira; se a 1 for usada, dobra',
         'a D-011'),
        (3, 'Resto da US de articulação (ortopedia)',
         nf('US de articulação de ortopedia (ombro, punho, joelho, tornozelo, cotovelo, mão, pé; adulto e criança)'),
         'fila grande, que cresce cerca de 280 por mês; o IEV não tirou nenhum pedido dela',
         'conflita com a regra de 02/11 (L-008)', 'a regulação dizer que não manda esses pedidos ao IEV'),
        (4, 'Transvaginal reservada ao IEV, depois da vigência', nf('US transvaginal, reserva do IEV'),
         'o IEV fez 20 consultas de ginecologia em seis meses',
         'só depois de maio de 2027; é o exame com mais faltas (43%) e mais trabalho', 'execução que passe de maio de 2027'),
        (5, 'Voltar as angiotomografias (sem coronárias e sem crânio)', nf(next(k for k in pos if k.startswith('Angiotomografias'))),
         'fila real, com espera de 3 a 6 meses; margem de 27%',
         'dá muito trabalho (decisão de 11/11); a clínica precisa confirmar o preço de R$ 225',
         'clínica com bomba injetora e protocolo vascular'),
        (6, 'Angiotomografia de coronárias', nf('Angiotomografia de coronárias'),
         'a maior fila de TC fora do plano, espera mediana de 265 dias',
         '30 min, betabloqueador e ECG pelo preço da TC de tórax; provavelmente não cobre a clínica', 'cotação própria'),
        (7, 'Plano menor: metas e valor abaixo do recurso', 0, 'nada sem fila nem exame difícil',
         'o recurso que sobra não é usado; a gestão é valor fixo, e o percentual dela sobe (8,44% hoje, teto de 8,5%)',
         'aceite do parlamentar e da SES'),
        (8, 'Assumir parte do que a SES realiza nos exames fáceis (aba Agenda da SES; só a transferência)',
         f"=SUMPRODUCT('Agenda da SES'!O6:O{tot_ag - 1},'Agenda da SES'!E6:E{tot_ag - 1})",
         'exames de 15 a 20 min, sem contraste, com margem de 30% a 56%; a SES fica com a vaga para outro atendimento',
         'a SES precisa abrir mão da agenda por Região; tira exame de quem já faz',
         'pactuar com a regulação e as Regiões; escrever no plano'),
    ]
    lin = 5
    for num, nome, val, fav, contra, dep in saidas:
        o.append([num, nome, val, 'não', fav, contra, dep])
        o.cell(lin, 3).number_format = MOEDA
        o.cell(lin, 4).fill = AMARELO
        for col in (2, 5, 6, 7):
            o.cell(lin, col).alignment = QUEBRA
        lin += 1
    for i, (rot, form) in enumerate([
        ('Falta hoje', '=Resumo!B6'),
        ('Soma das saídas marcadas', f'=SUMIFS(C5:C{lin - 1},D5:D{lin - 1},"sim")'),
        ('Falta depois das saídas (negativo = passa do valor)', f'=C{lin + 1}-C{lin + 2}'),
    ]):
        o.cell(lin + 1 + i, 2, rot).font = NEGRITO
        o.cell(lin + 1 + i, 3, form).number_format = MOEDA
    o.cell(lin + 3, 3).font = Font(bold=True, color='C00000')
    o.cell(lin + 5, 2, 'Recomendação (conversa de 11/11): a 2 como base, com a 1 pedida à SES no mesmo pedido da parede '
                       'abdominal; a 3 de reserva, para a resposta da regulação sobre o IEV.')
    o.cell(lin + 6, 2, 'Se o Doppler de membros sair (condição da D-011 não atendida), a falta sobe pelo valor dele, e a 2 '
                       'perde os 2.624 pedidos novos dele (a 2b): ver Resumo, B9. Não marque a 2b sem o Doppler na carteira.')

    # ---------- Da sobra à falta ----------
    p = wb.create_sheet('Da sobra à falta')
    titulo(p, 'De faltar R$ 245 mil para a falta de hoje',
           'A versão enviada (PT v1) pela Candanga, com as mesmas metas, contra a carteira escolhida, exame a exame.')
    cabecalho(p, 4, ['Exame', 'Versão enviada: quantidade', 'Versão enviada: valor pela Candanga', 'Hoje: quantidade',
                     'Hoje: valor', 'Diferença', 'Por quê'], [36, 12, 18, 12, 16, 16, 90])
    L = lambda *nomes: '=' + '+'.join(f'Escolhidos!H{linha_de[k]}' for k in linha_de if k.startswith(nomes))
    ponte = [
        ('US de mamas', 14689, 70.97, L('US de mamas'), 'a meta passava da fila; ficou a fila de hoje (a SES fez mutirões)'),
        ('US transvaginal', 10541, 83.77, L('US transvaginal'), 'a meta passava da fila, e 4.000 ficaram reservados ao IEV'),
        ('Doppler de membros', 9834, 115.61, L('Doppler de membros'), 'entrou toda a fila de hoje (condicionado à D-011)'),
        ('Doppler de carótidas', 4674, 115.61, L('Doppler de carótidas'), 'a fila de hoje'),
        ('US de abdômen total, adulto e criança', 10028, 117.51, L('US de abdômen total'), 'a fila de hoje; as crianças entraram (D-010)'),
        ('US de parede abdominal', 3138, 117.51, L('US de parede'), 'a fila de hoje (L-007)'),
        ('US de aparelho urinário, adulto e criança', 3944, 90.53, L('US de aparelho urinário'), 'a fila de hoje; as crianças entraram'),
        ('US de tireoide, adulto e criança', 3216, 64.07, L('US de tireoide'), 'a fila de hoje; as crianças entraram'),
        ('US de próstata', 3201, 74.19, L('US de próstata'), 'a meta passava da fila'),
        ('US de abdômen superior', 2261, 101.27, L('US de abdômen superior'), 'a meta passava da fila'),
        ('TC de abdômen superior', 4516, 309.25, L('TC de abdômen superior'), 'a meta passava da fila'),
        ('TC de pelve', 3862, 309.25, L('TC de pelve'), 'a meta passava da fila'),
        ('TC de tórax', 3104, 309.25, L('TC de tórax'), 'a meta passava da fila'),
        ('Angiotomografia de coronárias', 1408, 309.25, 0, 'saiu: 30 min e ECG pelo preço da TC de tórax (02/11)'),
        ('TC de tórax de emergência', 728, 309.25, 0, 'saiu: só ambulatório (D-009)'),
        ('US de bolsa escrotal', 0, 100.00, L('US de bolsa escrotal'), 'entrou: liberada em 02/11'),
        ('TC de pescoço', 0, 309.25, L('TC de pescoço'), 'entrou (11/11)'),
        ('TC de crânio sem contraste', 0, 251.29, L('TC de crânio sem contraste'), 'entrou'),
        ('US de articulação, não ortopedia', 0, PRECO_ART, L('US de articulação'),
         'entrou (11/11): partes moles, inguinal, pescoço, axila e infantis'),
    ]
    lin = 5
    for nome, q1, pr, qh, porque in ponte:
        p.append([nome, q1, f'=B{lin}*{pr}', qh, f'=D{lin}*{pr}', f'=E{lin}-C{lin}', porque])
        for col, fmt in ((2, INT), (3, MOEDA), (4, INT), (5, MOEDA), (6, MOEDA)):
            p.cell(lin, col).number_format = fmt
        lin += 1
    p.cell(lin, 1, 'Total').font = NEGRITO
    for col, L in ((2, 'B'), (3, 'C'), (4, 'D'), (5, 'E'), (6, 'F')):
        c = p.cell(lin, col, f'=SUM({L}5:{L}{lin - 1})')
        c.font, c.number_format = NEGRITO, (INT if col in (2, 4) else MOEDA)
    for i, (rot, form) in enumerate([('Valor dos exames pedido', ALVO),
                                     ('Faltava na versão enviada pela Candanga', f'=C{lin + 2}-C{lin}'),
                                     ('Falta hoje', f'=C{lin + 2}-E{lin}'),
                                     ('Conferência: a carteira de hoje é igual à de Escolhidos?',
                                      f'=IF(ABS(E{lin}-Escolhidos!I{tot})<0.01,"sim","NÃO")')]):
        p.cell(lin + 2 + i, 1, rot)
        p.cell(lin + 2 + i, 3, form).number_format = MOEDA
    p.cell(lin + 4, 3).font = Font(bold=True, color='C00000')
    for i, t in enumerate([
        'A diferença: os R$ 245 mil supunham que a versão enviada tinha pedido para todas as metas. Não tinha: R$ 1,14 mi '
        'estava em exames sem fila ou já descartados (transvaginal, coronária, emergência, mama), e as outras metas passavam '
        'um pouco da fila. Limitar cada exame à fila de hoje e tirar o que foi decidido fora derrubou mais do que os exames '
        'novos repuseram.',
        'A Candanga não muda nada nessa diferença: os dois lados usam o mesmo preço. Ela já tinha feito a versão enviada '
        'cair de R$ 10,64 mi (Portaria) para R$ 10,39 mi.',
    ]):
        p.cell(lin + 6 + i, 1, t)

    # ---------- Conferência ----------
    k = wb.create_sheet('Conferência')
    titulo(k, 'Conferência: a fila de cada código, o que entra e o que fica fora',
           'Fila do código = soma de todas as filas da coleta de 02/11 naquele código. O que fica fora é separado pelo nome '
           'da fila. A última coluna é o que nenhuma regra explica: filas pequenas e a diferença de recorte da planilha de 09/11.')
    cats = ['não: emergência', 'não: sedação', 'não: coronária', 'não: angiotomografia', 'IEV', 'decisão desta revisão']
    cabecalho(k, 4, ['Código', 'Exame', 'Fila do código (02/11)', 'Na carteira (Escolhidos)', 'Fora: emergência',
                     'Fora: sedação', 'Fora: coronária', 'Fora: angiotomografia', 'Fora: IEV',
                     'Fora: decisão desta revisão', 'Sem explicação (filas pequenas, recorte)'],
              [16, 40, 12, 12, 11, 11, 11, 12, 11, 12, 14])
    lin = 5
    for cd in codigos:
        filas = [f for f in us + tc if f['codigo'] == cd]
        conta = dict.fromkeys(cats, 0)
        for f in filas:
            d = na_carteira(f)
            if d in conta:
                conta[d] += f['fila']
            elif d.startswith('não: IEV'):
                conta['IEV'] += f['fila']
            elif d.startswith('não:'):
                conta['decisão desta revisão'] += f['fila']
        if cd == '02.05.02.018-6':
            conta['IEV'] += 4000
        k.append([cd, rumo[cd]['fila_maior'], sum(f['fila'] for f in filas),
                  f'=SUMIFS(Escolhidos!H$5:H${tot - 1},Escolhidos!C$5:C${tot - 1},A{lin})']
                 + [conta[c] for c in cats] + [f'=C{lin}-SUM(D{lin}:J{lin})'])
        for col in range(3, 12):
            k.cell(lin, col).number_format = INT
        lin += 1
    k.cell(lin, 1, 'Total').font = NEGRITO
    for col in range(3, 12):
        L = get_column_letter(col)
        c = k.cell(lin, col, f'=SUM({L}5:{L}{lin - 1})')
        c.font, c.number_format = NEGRITO, INT
    k.cell(lin + 1, 1, 'Conferência: o total "Na carteira" é igual ao de Escolhidos?')
    k.cell(lin + 1, 4, f'=IF(D{lin}=Escolhidos!H{tot},"sim","NÃO")')
    k.cell(lin + 3, 1, 'Negativo na última coluna: a carteira tem mais do que a soma das filas daquele código pelo nome '
                       '(acontece quando a planilha de 09/11 juntou filas de outro código no mesmo exame).')
    k.freeze_panes = 'C5'
    ws.cell(17 + 10, 1, '- Conferência: para cada código, a fila inteira, o que entra e o que fica fora, por motivo.')

    wb.save(SAIDA)
    print('salvo', SAIDA)


if __name__ == '__main__':
    main()
