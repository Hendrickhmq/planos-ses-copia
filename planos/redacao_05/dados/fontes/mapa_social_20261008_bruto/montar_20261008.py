# Monta ../mapa_social_20261008.xlsx a partir de coleta_20261008.json (saída da Qlik Engine
# API do painel). As coletas anteriores entram como comparação, com os números copiados dos
# resumos: ../../fila.md (base de 08/10/2026 07:32) e
# registros/fontes/mapa_social_oci_otorrino_20261007.md (base de 07/10/2026 19:32).
# Uso: python3 montar_20261008.py   (de dentro desta pasta)
import json
from datetime import date, timedelta
from pathlib import Path
import openpyxl
from openpyxl.styles import Font, PatternFill

AQUI = Path(__file__).resolve().parent
j = json.loads((AQUI / 'coleta_20261008.json').read_text(encoding='utf-8'))
norm = lambda s: ' '.join(str(s).replace('\xa0', ' ').split())
dia = lambda serial: (date(1899, 12, 30) + timedelta(days=int(serial))).strftime('%d/%m/%Y')
r0 = lambda x: None if x is None else round(x)

# ---- coletas anteriores (copiadas dos resumos; "" = não medido naquela coleta)
# chave: (nome da fila, recorte) -> (fila 07/10, fila 08/10 07:32, pessoas 08/10 07:32)
ANT = {
    ('AUDIOMETRIA E IMITANCIOMETRIA – ATÉ 7 ANOS', 'H'): (749, '', ''),
    ('AUDIOMETRIA E IMITANCIOMETRIA – 8 A 64 ANOS', 'H'): (2233, '', ''),
    ('AUDIOMETRIA E IMITANCIOMETRIA – ACIMA DE 65 ANOS', 'H'): (1252, '', ''),
    ('CONSULTA EM ATENCAO A SAUDE AUDITIVA - MEDIA E ALTA COMPLEXIDADE', 'H'): (5552, '', ''),
    ('CONSULTA EM OTORRINOLARINGOLOGIA - GERAL', 'H'): (1960, '', ''),
    ('CONSULTA EM OTONEUROLOGIA', 'H'): (85, '', ''),
    ('VIDEOENDOSCOPIA NASAL FLEXIVEL', 'J'): (2933, 2930, 2924),
    ('VIDEOENDOSCOPIA NASAL RIGIDA', 'J'): (520, 507, 506),
    ('VIDEOLARINGOSCOPIA', 'J'): (60, 60, 60),
    ('CONSULTA EM OTORRINOLARINGOLOGIA - GERAL', 'J'): (1981, 1983, 1983),
    ('VIDEOENDOSCOPIA DA DEGLUTICAO ( VED)', 'J'): (11, '', ''),
}
# conjunto -> (fila 07/10, pessoas 07/10, fila 08/10 07:32, pessoas 08/10 07:32, espera média 08/10 07:32)
ANTC = {
    '001-5 exames (audiometria)': (4234, 4234, '', 4255, 120),
    '002-3 exames (BERA)': ('', '', '', 1810, 457),
    'auditivas consultas': (7512, 7472, '', 7468, 353),
    '001-5 exames + consultas': (11746, 11329, '', '', ''),
    '003-1 exames': (3513, 3493, 3497, 3477, 518),
    '003-1 consulta': (1981, 1981, 1983, 1983, 149),
    '003-1 exames + consulta': (5494, 5430, 5480, 5416, 322),
}
# Região -> pessoas 08/10 07:32 na 003-1: (exames + consulta, só exames)
ANTR = {'Região Sudoeste': (1447, 958), 'Região Centro-Sul': (717, 530), 'Região Norte': (631, 506),
        'Região Oeste': (446, 152), 'Região Leste': (437, 157), 'Região Central': (413, 178),
        'Região Sul': (410, 113), 'URD': (764, 764), 'Contratado/Credenciado': (119, 119), '-': (48, 3)}

wb = openpyxl.Workbook(); wb.remove(wb.active)
B = Font(bold=True); HF = PatternFill('solid', fgColor='DDEBF7')


def aba(titulo, linhas, cab=()):
    ws = wb.create_sheet(titulo)
    for r in linhas:
        ws.append(list(r))
    for i in cab:
        for c in ws[i]:
            c.font = B; c.fill = HF
    for col in ws.columns:
        ws.column_dimensions[col[0].column_letter].width = min(60, max(9, max(len(str(c.value or '')) for c in col) * 0.9))
    return ws


rec_utc = j['recarga_utc']
aba('0 · Leia-me', [
    ['Mapa Social da Saúde — coleta piloto de 08/10/2026 da fila das três OCIs de otorrinolaringologia (redacao_05, ISHP)'],
    ['Painel', 'Mapa Social da Saúde – Regulamentação (MPDFT) · Lista de Espera – Exames e Consultas'],
    ['Endereço', 'https://paineis-ext.mpdft.mp.br/extensions/mapasauderegulamentacao/mapasauderegulamentacao.html'],
    ['App Qlik', j['titulo_app'] + ' · ' + j['app']],
    ['Fonte declarada', 'SISREG/DATASUS'],
    ['Última recarga da base', '08/10/2026 21:32:58 (BRT) — qLastReloadTime ' + rec_utc],
    ['Data/hora da consulta', j['consulta'] + ' (relógio do motor)'],
    ['Solicitação mais recente na base', j['max_data_solicitacao']],
    ['Extração', 'Qlik Engine API do próprio painel (evaluateEx e hipercubos de sessão), pelo navegador embutido. Sem leitura de tela, sem exportação pelos ícones.'],
    ['Medida "fila"', 'Count(Distinct {1<' + j['filtro_fila'] + ', fila, CID>} contador_solicitacao). Devolvidas fora, contadas à parte.'],
    ['Devolvidas', j['filtro_devolvidas']],
    ['Pessoas', 'Count(Distinct {mesmo conjunto da fila} cns_usuario_solicitacao) — só a contagem sai do motor'],
    ['Recorte OCI', 'CID da solicitação contra a ficha do SIGTAP. H60–H95: ' + j['recorte_cid']['H60_H95'] + ' · J30–J39: ' + j['recorte_cid']['J30_J39']],
    ['Recorte de tempo', 'todos os anos'],
    ['Entrantes', 'abertas (solicitações na base, todos os status, por Ano_Solicitacao/Mes_Solicitacao) + agendadas (contador_agendamento por mês de data_agendamento − tempo_espera_agendamento, CID_agendamento no mesmo recorte). Piso: cancelada antes de agendar não consta.'],
    ['Grafia', 'VIDEOENDOSCOPIA  NASAL  FLEXIVEL tem dois espaços comuns entre as palavras e não tem acento; VIDEOENDOSCOPIA DA DEGLUTICAO  ( VED) e CONSULTA EM  RINOLOGIA também têm espaço duplo. As filas de audiometria e BERA usam travessão (U+2013) e "ATÉ" com acento.'],
    ['Regra', 'Abas 1, 2, 3, 4 e 6: números do motor. Abas 5, 7 e 8 somam números do motor ou comparam com coletas anteriores e dizem isso no título.'],
    ['Comparação', '08/10/2026 07:32 = planos/redacao_05/dados/fila.md · 07/10/2026 19:32 = registros/fontes/mapa_social_oci_otorrino_20261007.md'],
    ['Brutos e script', 'mapa_social_20261008_bruto/ (coleta_20261008.json, montar_20261008.py)'],
], [1])

hd = ['OCI', 'papel', 'fila no SISREG', 'recorte CID', 'SIGTAP da fila', 'fila', 'pessoas', 'devolvidas', 'total (fila + devolvidas + outros)',
      'fila sem recorte de CID', 'devolvidas sem recorte', 'espera média', 'mediana', 'máxima', 'idade mediana', 'idade mín.', 'idade máx.',
      'fila solicitada em 2026', 'solicitação mais antiga na fila']
CIDL = {'H': 'H60–H95', 'J': 'J30–J39'}
d = [hd]
for x in j['linhas']:
    d.append([x['oci'], x['papel'], x['nome'], CIDL[x['cid']], str(x['sigtap_na_fila']), x['fila'], x['pessoas'], x['devolvidas'], x['total'],
              x['fila_sem_recorte_cid'], x['devolvidas_sem_recorte_cid'], r0(x['espera_media']), r0(x['espera_mediana']), r0(x['espera_max']),
              x['idade_mediana'], x['idade_min'], x['idade_max'], x['fila_solicitada_2026'], dia(x['solicitacao_mais_antiga'])])
aba('1 · Filas', d, [1])

d = [['conjunto', 'recorte CID', 'filas'] + hd[5:]]
for x in j['conjuntos']:
    d.append([x['conjunto'], CIDL[x['cid']], ' + '.join(x['filas']), x['fila'], x['pessoas'], x['devolvidas'], x['total'], x['fila_sem_recorte_cid'],
              x['devolvidas_sem_recorte_cid'], r0(x['espera_media']), r0(x['espera_mediana']), r0(x['espera_max']), x['idade_mediana'],
              x['idade_min'], x['idade_max'], x['fila_solicitada_2026'], dia(x['solicitacao_mais_antiga'])])
e = j['extra']
d += [[], ['as três OCIs (união no motor)'],
      ['exames das três OCIs', '', 'audiometria + BERA (H60–H95) + videoendoscopias e videolaringoscopia (J30–J39)', e['tres_ocis_exames_fila'], e['tres_ocis_exames_pessoas'], '', '', '', '', r0(e['tres_ocis_exames_espera_media']), r0(e['tres_ocis_exames_espera_mediana'])],
      ['exames + consultas das três OCIs', '', 'idem + consultas com CID compatível', e['tres_ocis_exames_consultas_fila'], e['tres_ocis_exames_consultas_pessoas']],
      ['pessoas com audiometria e BERA ao mesmo tempo', '', '', '', e['pessoas_audiometria_e_bera']],
      ['pessoas nas duas famílias (auditiva e nasofaringe, exames + consultas)', '', '', '', e['pessoas_nas_duas_familias']]]
aba('2 · Conjuntos por OCI', d, [1, len(j['conjuntos']) + 3])

cols = j['regioes']['cols']
d = [['Região de Saúde da unidade solicitante, medida FILA. "-" = sem região informada (linha própria, sem rateio). As linhas de pessoas não somam o total: quem tem solicitação vinda de duas regiões conta nas duas.'],
     ['Região de Saúde'] + cols]
d += [['(sem região informada)' if r[0] == '-' else r[0]] + r[1:] for r in j['regioes']['rows']]
aba('3 · Região de Saúde', d, [2])

ic = j['idade']['cols']
d = [['idade na solicitação'] + [c + ' (fila)' for c in ic]]
d += [[int(r[0])] + r[1:] for r in sorted(j['idade']['rows'], key=lambda r: int(r[0]))]
aba('4 · Idade', d, [1])

FX = [(0, 4), (5, 9), (10, 14), (15, 19), (20, 39), (40, 59), (60, 64), (65, 200)]
d = [['CALCULADO — faixas etárias somadas a partir da aba 4 (medida fila)'], ['faixa'] + ic]
for a, b in FX:
    d.append([f'{a}–{b}' if b < 200 else f'{a} ou mais'] + [sum(r[1 + i] for r in j['idade']['rows'] if a <= int(r[0]) <= b) for i in range(len(ic))])
aba('5 · Faixas etárias (calculado)', d, [2])

ac = j['abertas_por_mes']['cols']
d = [['solicitações na base (todos os status) por mês da solicitação, no recorte de CID'], ['ano', 'mês'] + ac]
MES = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']
d += sorted(j['abertas_por_mes']['rows'], key=lambda r: (r[0], MES.index(r[1])))
d += [[], ['agendadas por mês da solicitação (data_agendamento − tempo_espera_agendamento), no recorte de CID'], ['ano-mês', ''] + ac]
d += [[r[0], ''] + r[1:] for r in j['agendadas_por_mes_da_solicitacao']['rows']]
aba('6 · Abertas e agendadas', d, [2, len(j['abertas_por_mes']['rows']) + 5])

ab = {(r[0], MES.index(r[1]) + 1): r[2:] for r in j['abertas_por_mes']['rows']}
ag = {(r[0][:4], int(r[0][5:])): r[1:] for r in j['agendadas_por_mes_da_solicitacao']['rows']}
d = [['CALCULADO — entrantes = abertas + agendadas, por mês da solicitação (abas 6). Outubro/2026 incompleto (base até 02/10).'], ['ano-mês'] + ac]
tot = {'2025': [0] * len(ac), '2026': [0] * len(ac)}
for ano, ult in (('2025', 12), ('2026', 9)):
    for m in range(1, ult + 1):
        v = [ab.get((ano, m), [0] * len(ac))[i] + ag.get((ano, m), [0] * len(ac))[i] for i in range(len(ac))]
        tot[ano] = [tot[ano][i] + v[i] for i in range(len(ac))]
        d.append([f'{ano}-{m:02d}'] + v)
d += [['2025, doze meses'] + tot['2025'], ['2025, média mensal'] + [round(x / 12, 1) for x in tot['2025']],
      ['2026, jan–set'] + tot['2026'], ['2026, média mensal (÷9)'] + [round(x / 9, 1) for x in tot['2026']]]
aba('7 · Entrantes (calculado)', d, [2])

d = [['CID mais frequentes (3 caracteres) na fila inteira de cada nome, sem recorte — mostra o que fica fora da ficha'], ['fila no SISREG', 'CID', 'fila']]
for nome, lst in j['cid_principais_na_fila_sem_recorte'].items():
    for cid, n in lst:
        d.append([nome, cid, n])
aba('8 · CID na fila (motor)', d, [2])

d = [['CALCULADO — comparação com as coletas anteriores (números copiados de fila.md e do resumo de 07/10)'],
     ['fila no SISREG', 'recorte', 'fila 07/10 19:32', 'fila 08/10 07:32', 'pessoas 08/10 07:32', 'fila 08/10 21:32', 'pessoas 08/10 21:32', 'Δ fila vs 08/10 07:32', 'Δ fila vs 07/10']]
for x in j['linhas']:
    a = ANT.get((x['nome'], x['cid']), ('', '', ''))
    d.append([x['nome'], CIDL[x['cid']], a[0], a[1], a[2], x['fila'], x['pessoas'],
              x['fila'] - a[1] if a[1] != '' else '', x['fila'] - a[0] if a[0] != '' else ''])
d += [[], ['conjunto', 'recorte', 'fila 07/10', 'pessoas 07/10', 'fila 08/10 07:32', 'pessoas 08/10 07:32', 'espera média 08/10 07:32', 'fila 08/10 21:32', 'pessoas 08/10 21:32', 'espera média 08/10 21:32', 'Δ pessoas vs 08/10 07:32']]
for x in j['conjuntos']:
    a = ANTC.get(x['conjunto'])
    if not a:
        continue
    d.append([x['conjunto'], CIDL[x['cid']], *a, x['fila'], x['pessoas'], r0(x['espera_media']), x['pessoas'] - a[3] if a[3] != '' else ''])
n1 = len(j['linhas']) + 2
d += [[], ['Região de Saúde — 003-1', 'pessoas exames + consulta 08/10 07:32', 'pessoas exames + consulta 08/10 21:32', 'Δ', 'pessoas só exames 08/10 07:32', 'pessoas só exames 08/10 21:32', 'Δ']]
ci = {c: i + 1 for i, c in enumerate(cols)}
for r in j['regioes']['rows']:
    a = ANTR.get(r[0])
    if not a:
        continue
    pe = r[ci['003-1 exames + consulta · pessoas']]; px = r[ci['003-1 exames · pessoas']]
    d.append(['(sem região informada)' if r[0] == '-' else r[0], a[0], pe, pe - a[0], a[1], px, px - a[1]])
aba('9 · Comparação (calculado)', d, [2, n1 + 2, n1 + 2 + len(ANTC) + 2])

saida = AQUI.parent / 'mapa_social_20261008.xlsx'
wb.save(saida)
print('gravado', saida.name, wb.sheetnames)
print('entrantes 2025', dict(zip(ac, tot['2025'])))
print('entrantes 2026 jan-set', dict(zip(ac, tot['2026'])))
