# Monta coleta_20261025.json (formato do método de 25/10/2026: filas, ocis, janela viva) e
# ../mapa_social_20261025.xlsx a partir da saída do motor do painel Mapa Social da Saúde (MPDFT),
# gravada como veio em motor_20261025.json e motor_varredura_20261025.json.
# Não calcula número novo: reorganiza os do motor. As únicas contas são as razões dos alarmes
# (proporções e anos de agendamento) e a diferença para a coleta de 22/10/2026, ditas no título.
# Uso: python3 montar_20261025.py   (de dentro desta pasta)
import json
from datetime import date, timedelta
from pathlib import Path
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment

AQUI = Path(__file__).resolve().parent
M = json.loads((AQUI / 'motor_20261025.json').read_text(encoding='utf-8'))
VR = json.loads((AQUI / 'motor_varredura_20261025.json').read_text(encoding='utf-8'))
ANT = json.loads((AQUI.parent / 'mapa_social_20261022_bruto' / 'coleta_20261022.json').read_text(encoding='utf-8'))

dia = lambda s: None if s in (None, '') else (date(1899, 12, 30) + timedelta(days=int(s))).strftime('%d/%m/%Y')
r0 = lambda x: None if x is None else round(x)

ROT = {'NONE': 'sem recorte', 'I': 'I00-I99 (I*)', 'ISC': 'I20-I25', 'SCC': 'I20 e I25', 'IC': 'I50',
       'ICA': 'IC ampliada (I50, I110, I130, I132, I42, I43)', 'ZAV': 'Z136, Z848', 'ZPO': 'Z018, Z488, Z489'}
CUTS = ['NONE', 'I', 'ISC', 'SCC', 'IC', 'ICA', 'ZAV', 'ZPO']
F = M['F']
NOME = {v: k for k, v in F.items()}
GEN = {'ECG', 'RX', 'HOL', 'ECO', 'C_ADU'}          # regra 4 do enquadramento
PAPEL = {k: ('consulta' if k.startswith('C_') else 'exame') for k in F}
OCIS = list(M['OCI'])
NOME_OCI = {'09.02.01.001-8': 'avaliação de risco cirúrgico', '09.02.01.002-6': 'avaliação cardiológica',
            '09.02.01.003-4': 'SCC, avaliação inicial', '09.02.01.004-2': 'SCC, progressão I',
            '09.02.01.005-0': 'SCC, progressão II', '09.02.01.006-9': 'insuficiência cardíaca',
            '09.02.01.007-7': 'gestão do pré-operatório'}

# ---------------------------------------------------------------- filas
pc = M['pf_cols']
idx = {c: i for i, c in enumerate(pc)}
ag = {k: dict(zip(M['agF_cols'], v)) for k, v in M['agF'].items()}
filas = {}
for row in M['pf']:
    nome = row[0]; k = NOME[nome]
    g = lambda c: row[idx[c]]
    rec = {}
    for cut in CUTS:
        rec[ROT[cut]] = {'fila': g(f'{cut} fila'), 'fila_viva': g(f'{cut} fila_viva'),
                         'pessoas': g(f'{cut} pessoas'), 'pessoas_viva': g(f'{cut} pessoas_viva'),
                         'devolvidas': g(f'{cut} devolvidas'), 'espera_media': g(f'{cut} espera_media'),
                         'espera_mediana': g(f'{cut} espera_mediana'),
                         'cid_principais': M['top'][k][cut]}
    a = ag[k]
    filas[nome] = {
        'chave': k, 'papel': PAPEL[k], 'generica': k in GEN, 'codigo_sigtap': g('codigo_sigtap'),
        'fila': g('NONE fila'), 'fila_viva': g('NONE fila_viva'), 'fila_viva_12m': g('fila_viva12'),
        'fila_viva_36m': g('fila_viva36'), 'pessoas': g('NONE pessoas'), 'pessoas_viva': g('NONE pessoas_viva'),
        'devolvidas': g('NONE devolvidas'), 'espera_media': g('NONE espera_media'),
        'espera_mediana': g('NONE espera_mediana'), 'espera_max': g('espera_max'),
        'idade_mediana': g('idade_mediana'), 'fila_menor_18': g('fila_menor_18'),
        'mais_antiga': dia(g('mais_antiga')), 'fila_solicitada_2026': g('fila_2026'),
        'total_todos_status': g('total_todos_status'),
        'agendadas_12m': a['agendadas 12m'], 'agendadas_todos_os_anos': a['agendadas todos os anos'],
        'primeiro_agendamento': dia(a['primeiro agendamento']),
        'agendadas_12m_por_recorte': {ROT[c]: a[f'12m {c}'] for c in CUTS[1:]},
        'cid_principais_viva': M['top'][k]['VIVA'],
        'recortes': rec}

# ---------------------------------------------------------------- ocis
ocis = {}
for cod in OCIS:
    o = M['OCI'][cod]; v = M['oci'][cod]
    todas = o['ex'] + o['co']
    nb = v.get('nuc_b_pessoas')
    if nb is not None and nb > v['nuc_a_pessoas']:
        nuc = {'pessoas': nb, 'pessoas_viva': v['nuc_b_pessoas_viva'],
               'como': 'exames obrigatórios com fila ao mesmo tempo (' + ' + '.join(o['obr']) + ')'}
    else:
        nuc = {'pessoas': v['nuc_a_pessoas'], 'pessoas_viva': v['nuc_a_pessoas_viva'],
               'como': 'consulta de entrada (' + ' + '.join(o['co']) + ')'}
    nuc['a_consultas'] = {'filas': [F[x] for x in o['co']], 'pessoas': v['nuc_a_pessoas'], 'pessoas_viva': v['nuc_a_pessoas_viva']}
    nuc['a_so_a_consulta_especifica'] = {'fila': F[o['ent']], 'pessoas': v['nuc_a_ent_pessoas'], 'pessoas_viva': v['nuc_a_ent_pessoas_viva']}
    nuc['b_exames_obrigatorios'] = ({'filas': [F[x] for x in o['obr']], 'pessoas': nb, 'pessoas_viva': v['nuc_b_pessoas_viva']}
                                    if nb is not None else {'filas': [], 'nota': 'a 007-7 não tem componente obrigatório'})
    def bloco(p):
        return {k[len(p) + 1:]: val for k, val in v.items() if k.startswith(p + '_')}
    fin = bloco('fin')
    fin['pessoas_18_ou_mais'] = M['fin18'][cod]
    fin['mais_antiga'] = dia(fin['mais_antiga'])
    var = {}
    for x in o['var']:
        var[ROT[x]] = dict(bloco('var_' + x), cid=M['CID'][x])
    ocis[cod] = {
        'nome': NOME_OCI[cod],
        'cid_aceito': M['CID'][o['teto']], 'cid_finalidade': M['CID'][o['fin']],
        'finalidade_igual_ao_teto': o['teto'] == o['fin'],
        'recorte_teto': ROT[o['teto']], 'recorte_finalidade': ROT[o['fin']],
        'filas': [F[x] for x in todas], 'exames': [F[x] for x in o['ex']], 'consultas': [F[x] for x in o['co']],
        'obrigatorios_com_fila': [F[x] for x in o['obr']],
        'filas_genericas': [F[x] for x in todas if x in GEN],
        'teto': bloco('teto'), 'finalidade': fin, 'variantes': var, 'nucleo': nuc,
        'finalidade_sem_genericas': dict(M['fin_sem_genericas'][cod], filas=[F[x] for x in M['fin_sem_genericas'][cod]['filas']]),
    }
rc = M['risco_cirurgico_sem_recorte']
ocis['09.02.01.001-8']['a_decidir'] = {'CONSULTA EM CARDIOLOGIA - RISCO CIRURGICO sem recorte de CID (P-08)': rc}
ocis['09.02.01.007-7']['a_decidir'] = {'CONSULTA EM CARDIOLOGIA - RISCO CIRURGICO sem recorte de CID (a mesma da 001-8)': rc}

# ---------------------------------------------------------------- alarmes (os limites do método; contas ditas)
LIM_DOM, LIM_RARO, LIM_VELHA, LIM_EST = 0.30, 0.05, 0.30, 3
alarmes = []
for cod in OCIS:
    o = M['OCI'][cod]; oc = ocis[cod]
    comp = o['ex'] + o['co']
    if o['teto'] == 'I':
        alarmes.append(['CID largo', cod, None, 'o CID aceito é o capítulo I inteiro (I*, 77 categorias na ficha)'])
    tot = sum(filas[F[x]]['fila'] for x in comp)
    nf = sum(filas[F[x]]['recortes'][ROT[o['fin']]]['fila'] for x in comp)
    if tot and nf / tot < LIM_RARO:
        alarmes.append(['CID raro', cod, None, f'a finalidade pega {nf} de {tot} solicitações das filas da composição ({nf / tot:.1%})'])
    p, pv = oc['finalidade']['pessoas'], oc['finalidade']['pessoas_viva']
    if p and (p - pv) / p > LIM_VELHA:
        alarmes.append(['fila velha', cod, None, f'{p - pv} de {p} pessoas da finalidade ({(p - pv) / p:.1%}) só têm pedido de antes de 25/10/2024; o pedido mais antigo é de {oc["finalidade"]["mais_antiga"]}'])
    if o['teto'] != o['fin']:
        for x in comp:
            r = filas[F[x]]['recortes'][ROT[o['teto']]]
            for cid, q in r['cid_principais']:
                if r['fila'] and q / r['fila'] > LIM_DOM and not cid.startswith(tuple(t.strip('"*') for t in M['CID'][o['fin']].split('{')[1].strip('}').split(','))):
                    alarmes.append(['CID dominante', cod, F[x], f'{cid} em {q / r["fila"]:.0%} de {F[x]} no teto ({q} de {r["fila"]})'])
    for x in comp:
        if x in GEN:
            alarmes.append(['fila genérica', cod, F[x], f'{F[x]} na composição da {cod}'])
for x in sorted({x for c in OCIS for x in M['OCI'][c]['ex'] + M['OCI'][c]['co']}):
    d = filas[F[x]]
    if d['agendadas_12m'] == 0 or d['fila'] / d['agendadas_12m'] > LIM_EST:
        alarmes.append(['estoque', None, F[x], f'{d["fila"]} na fila e {d["agendadas_12m"]} agendadas em 12 meses: {d["fila"] / d["agendadas_12m"]:.1f} anos de agendamentos (viva: {d["fila_viva"] / d["agendadas_12m"]:.1f})'])

# ---------------------------------------------------------------- diferença para 22/10
ant_oci = {x['oci']: x['vals'][1] for x in ANT['conjuntos'] if x['tipo'] == 'exames + consultas'}
ant_fila = {r[0]: r for r in ANT['filas']['NONE']}
diferenca = {
    'nota': 'coleta de 22/10/2026 (recarga 08:32, método anterior): pessoas "exames + consultas" com o CID aceito, o mesmo conjunto do teto de agora',
    'ocis': {c: {'22/10 exames + consultas': ant_oci.get(c), '25/10 teto': ocis[c]['teto']['pessoas'],
                 'diferenca_teto': ocis[c]['teto']['pessoas'] - ant_oci.get(c, 0),
                 '25/10 finalidade': ocis[c]['finalidade']['pessoas'],
                 '25/10 finalidade viva': ocis[c]['finalidade']['pessoas_viva']} for c in OCIS},
    'uniao': {'22/10 exames + consultas': ANT['sobreposicao_ocis']['uniao_ex_co'], '25/10 teto': M['sobreposicao']['teto_uniao_pessoas'],
              '25/10 teto viva': M['sobreposicao']['teto_uniao_pessoas_viva'],
              '25/10 finalidade': M['sobreposicao']['uniao_pessoas'], '25/10 finalidade viva': M['sobreposicao']['uniao_pessoas_viva']},
    'filas': {n: {'22/10 fila': ant_fila[n][1] if n in ant_fila else None, '25/10 fila': filas[n]['fila'],
                  '22/10 pessoas': ant_fila[n][2] if n in ant_fila else None, '25/10 pessoas': filas[n]['pessoas']} for n in filas},
}

# ---------------------------------------------------------------- o JSON da coleta
coleta = {
    'metodo': '2026-10-25', 'janela_viva_meses': 24,
    'app': M['app'], 'titulo_app': M['titulo_app'], 'recarga_utc': M['reload'], 'recarga_brasilia': '25/10/2026 14:31:55',
    'consulta': M['consulta_inicio'] + ' a ' + M['consulta_fim'][11:], 'max_data_solicitacao': M['max_data_solicitacao'],
    'max_data_agendamento': M['max_data_agendamento'],
    'filtro_fila': M['S'], 'filtro_devolvidas': M['DEV'],
    'janelas': {'viva 24 meses': M['V']['24'], 'viva 12 meses': M['V']['12'], 'viva 36 meses': M['V']['36'],
                'agendadas 12 meses': M['A12']},
    'recortes_cid': {ROT[c]: M['CID'][c] for c in CUTS}, 'recortes_cid_agendamento': {ROT[c]: M['CIDAG'][c] for c in CUTS[1:]},
    'nomes_internos': {k: {'nome_sisreg': v, 'nome_sisreg_agendamento': v} for k, v in F.items()},
    'enquadramento': {c: {'teto': ROT[o['teto']], 'finalidade': ROT[o['fin']], 'variantes': [ROT[x] for x in o['var']],
                          'ex': o['ex'], 'co': o['co'], 'obr': o['obr'], 'consulta_especifica': o['ent'],
                          'genericas': [x for x in o['ex'] + o['co'] if x in GEN]} for c, o in M['OCI'].items()},
    'filas': filas, 'ocis': ocis,
    'regiao_finalidade': M['reg'], 'sobreposicao_finalidade': M['sobreposicao'], 'pessoas_por_ano': M['anos'],
    'cid_so_categoria_Z13_Z84_Z01_Z48': M['zamb'], 'alarmes': alarmes, 'diferenca_20261022': diferenca,
    'varredura': {'nota': VR['nota'], 'solicitacoes_cols': VR['varr_cols'], 'solicitacoes': VR['vs'],
                  'agendamentos_cols': VR['varag_cols'], 'agendamentos': VR['va'],
                  'laboratorio': {'nota': VR['laboratorio_nota'], 'solicitacoes': VR['laboratorio_solicitacoes'],
                                  'agendamentos': VR['laboratorio_agendamentos']}},
    'conferencias': {'viva_ecg_por_ano': M['conferencia_viva_ecg'],
                     'P_contra_Aggr': [M['sobreposicao']['conferencia_P_erg_hol_I'], M['sobreposicao']['conferencia_Aggr_erg_hol_I']]},
}
(AQUI / 'coleta_20261025.json').write_text(json.dumps(coleta, ensure_ascii=False, indent=1), encoding='utf-8')

# ---------------------------------------------------------------- a planilha
wb = openpyxl.Workbook(); wb.remove(wb.active)
B = Font(bold=True); HF = PatternFill('solid', fgColor='DDEBF7')


def aba(titulo, linhas, cab=(1,)):
    ws = wb.create_sheet(titulo[:31])
    for r in linhas:
        ws.append([('' if c is None else c) for c in r])
    for i in cab:
        for c in ws[i]:
            c.font = B; c.fill = HF; c.alignment = Alignment(wrap_text=True, vertical='top')
    for col in ws.columns:
        ws.column_dimensions[col[0].column_letter].width = min(60, max(9, max(len(str(c.value or '')) for c in col[1:] or col) * 0.9))
    return ws


aba('0 · Leia-me', [
    ['Mapa Social da Saúde — fila das sete OCI de cardiologia (09.02.01), redacao_08. Recoleta pelo método de 25/10/2026 (teto, finalidade, núcleo; fila viva de 24 meses; alarmes).'],
    ['Painel', 'Mapa Social da Saúde – Regulamentação (MPDFT) · Lista de Espera – Exames e Consultas'],
    ['Endereço', 'https://paineis-ext.mpdft.mp.br/extensions/mapasauderegulamentacao/mapasauderegulamentacao.html'],
    ['App Qlik', M['titulo_app'] + ' · ' + M['app'] + ' · dados SISREG/DATASUS'],
    ['Última recarga da base', '25/10/2026 14:31:55 (Brasília) — qLastReloadTime ' + M['reload']],
    ['Consulta', coleta['consulta'] + ' (relógio do motor)'],
    ['Solicitação mais recente na base', M['max_data_solicitacao']],
    ['Medida "fila"', 'Count(Distinct {1<' + M['S'] + ', fila, CID>} contador_solicitacao). Devolvidas fora, contadas à parte: ' + M['DEV']],
    ['Pessoas', 'Count(Distinct {o conjunto da fila} cns_usuario_solicitacao): só a contagem sai do motor'],
    ['Fila viva', 'a fila só com as solicitações de 25/10/2024 em diante (24 meses contados da solicitação mais recente): ' + M['V']['24'] + '. Também 12 e 36 meses para a finalidade.'],
    ['Teto', 'o CID aceito pela ficha do SIGTAP, na união das filas da composição. Referência, nunca a fila do dossiê.'],
    ['Finalidade', 'o CID da finalidade (proposta para o usuário escolher), na união das filas da composição: a fila da OCI.'],
    ['Núcleo', 'o maior entre (a) as consultas da OCI com o CID da finalidade e (b) quem espera todos os exames obrigatórios com fila ao mesmo tempo, com o CID da finalidade.'],
    ['Recortes de CID', '; '.join(f'{ROT[c]}: {M["CID"][c] or "nenhum"}' for c in CUTS)],
    ['Filas genéricas (regra 4)', 'ELETROCARDIOGRAMA, TORAX : PA E PERFIL, HOLTER 24 HORAS, 1. ECOCARDIOGRAFIA ... ADULTO, CONSULTA EM CARDIOLOGIA - ADULTO: no teto aparecem marcadas; na finalidade, só com o CID da finalidade; decisão "a decidir".'],
    ['Regra', 'Números do motor, sem conta. As abas com conta dizem no título: "2 · Alarmes (razões calculadas)" e "11 · Diferença 22-10 (calc.)".'],
    ['Brutos e script', 'mapa_social_20261025_bruto/ (motor_20261025.json, motor_varredura_20261025.json, coleta_20261025.json, montar_20261025.py)'],
], [1])

# 1 · os três números
d = [['OCI', 'nome', 'CID aceito', 'CID da finalidade', 'teto', 'teto viva', 'finalidade', 'finalidade viva 12 m', 'finalidade viva 24 m',
      'finalidade viva 36 m', 'variante (recorte)', 'variante pessoas', 'variante viva', 'núcleo', 'núcleo viva', 'núcleo: como',
      '(a) consultas', '(a) viva', '(a) só a consulta específica', '(b) obrigatórios juntos', '(b) viva',
      'espera média (fin.)', 'mediana (fin.)', 'máxima (fin.)', 'espera média viva (fin.)', 'mediana viva (fin.)',
      'devolvidas (fin.)', 'pessoas 18+ (fin.)', 'pedido mais antigo (fin.)', 'finalidade sem genéricas', 'sem genéricas viva']]
for c in OCIS:
    oc = ocis[c]; t = oc['teto']; f = oc['finalidade']; n = oc['nucleo']
    vv = list(oc['variantes'].items())
    d.append([c, oc['nome'], oc['recorte_teto'], oc['recorte_finalidade'], t['pessoas'], t['pessoas_viva'], f['pessoas'],
              f['pessoas_viva12'], f['pessoas_viva'], f['pessoas_viva36'],
              vv[0][0] if vv else '', vv[0][1]['pessoas'] if vv else '', vv[0][1]['pessoas_viva'] if vv else '',
              n['pessoas'], n['pessoas_viva'], n['como'], n['a_consultas']['pessoas'], n['a_consultas']['pessoas_viva'],
              n['a_so_a_consulta_especifica']['pessoas'], n['b_exames_obrigatorios'].get('pessoas', 'sem obrigatório'),
              n['b_exames_obrigatorios'].get('pessoas_viva', ''), r0(f['espera_media']), r0(f['espera_mediana']),
              r0(f['espera_max']), r0(f['espera_media_viva']), r0(f['espera_mediana_viva']), f['devolvidas'],
              f['pessoas_18_ou_mais'], f['mais_antiga'], oc['finalidade_sem_genericas']['pessoas'],
              oc['finalidade_sem_genericas']['pessoas_viva']])
d.append([]); d.append(['a decidir (001-8 e 007-7): CONSULTA EM CARDIOLOGIA - RISCO CIRURGICO sem recorte de CID', '', '', '', '', '',
                        rc['pessoas'], rc['pessoas_viva12'], rc['pessoas_viva'], rc['pessoas_viva36'], '', '', '', '', '', '', '', '', '', '', '',
                        r0(rc['espera_media']), rc['espera_mediana'], rc['espera_max']])
d.append(['união das sete', '', '', '', M['sobreposicao']['teto_uniao_pessoas'], M['sobreposicao']['teto_uniao_pessoas_viva'],
          M['sobreposicao']['uniao_pessoas'], '', M['sobreposicao']['uniao_pessoas_viva']])
aba('1 · Três números', d)

# 2 · alarmes
aba('2 · Alarmes (razões calculadas)', [['alarme', 'OCI', 'fila', 'o número que dispara']] + alarmes)

# 3 · filas da composição, por recorte
d = [['fila no SISREG (nome interno)', 'chave', 'papel', 'genérica', 'recorte CID', 'fila', 'fila viva', 'pessoas', 'pessoas viva',
      'devolvidas', 'espera média', 'mediana', 'agendadas 12 m (mesmo recorte)']]
for n, x in filas.items():
    for rot, r in x['recortes'].items():
        agr = x['agendadas_12m'] if rot == 'sem recorte' else x['agendadas_12m_por_recorte'].get(rot)
        d.append([n, x['chave'], x['papel'], 'sim' if x['generica'] else '', rot, r['fila'], r['fila_viva'], r['pessoas'],
                  r['pessoas_viva'], r['devolvidas'], r0(r['espera_media']), r0(r['espera_mediana']), agr])
aba('3 · Filas por recorte', d)

# 4 · fila a fila, sem recorte
d = [['fila no SISREG (nome interno)', 'chave', 'SIGTAP da fila', 'fila', 'fila viva 24 m', 'fila viva 12 m', 'fila viva 36 m', 'pessoas',
      'pessoas viva', 'devolvidas', 'espera média', 'mediana', 'máxima', 'idade mediana', 'fila < 18 anos', 'pedido mais antigo',
      'solicitadas em 2026', 'total (todos os status)', 'agendadas 12 m', 'agendadas, todos os anos', 'primeiro agendamento']]
for n, x in filas.items():
    d.append([n, x['chave'], x['codigo_sigtap'], x['fila'], x['fila_viva'], x['fila_viva_12m'], x['fila_viva_36m'], x['pessoas'],
              x['pessoas_viva'], x['devolvidas'], r0(x['espera_media']), r0(x['espera_mediana']), r0(x['espera_max']),
              x['idade_mediana'], x['fila_menor_18'], x['mais_antiga'], x['fila_solicitada_2026'], x['total_todos_status'],
              x['agendadas_12m'], x['agendadas_todos_os_anos'], x['primeiro_agendamento']])
aba('4 · Fila a fila', d)

# 5 · CID principais
d = [['fila', 'recorte', 'posição', 'CID (categoria)', 'solicitações na fila']]
for n, x in filas.items():
    for rot, r in list(x['recortes'].items()) + [('sem recorte, só a fila viva', {'cid_principais': x['cid_principais_viva']})]:
        for i, (cid, q) in enumerate(r['cid_principais'], 1):
            d.append([n, rot, i, cid, q])
aba('5 · CID principais', d)

# 6 · Região de Saúde (finalidade)
rg = M['reg']
d = [['Região de Saúde da unidade solicitante, medida FILA, finalidade principal de cada OCI. "sem região informada" em linha própria, sem rateio. As linhas de pessoas não somam o total: quem tem pedido de duas regiões conta nas duas.'],
     ['Região'] + rg['cols']]
for row in rg['rows']:
    d.append(['sem região informada' if row[0] == '-' else row[0]] + row[1:])
aba('6 · Região (finalidade)', d, [2])

# 7 · sobreposição
s = M['sobreposicao']
d = [['pessoas em', 'finalidade principal']] + [[f'{k} OCI', v] for k, v in s['distribuicao'].items()] + \
    [['união das sete', s['uniao_pessoas']], ['união das sete, viva', s['uniao_pessoas_viva']],
     ['união dos sete tetos', s['teto_uniao_pessoas']], ['união dos sete tetos, viva', s['teto_uniao_pessoas_viva']],
     ['união com as variantes (IC ampliada, I20-I25 na 003-4)', s['var_uniao_pessoas']], [], ['par', 'pessoas nas duas']] + \
    [[k, v] for k, v in sorted(s['pares'].items(), key=lambda x: -x[1])]
aba('7 · Mais de uma OCI', d)

# 8 · por ano
d = [['Ano da solicitação'] + M['anos']['cols']] + M['anos']['rows']
aba('8 · Pessoas por ano', d)

# 9 e 10 · varredura
aba('9 · Varredura solicitações', [[VR['nota']], VR['varr_cols']] + sorted(VR['vs'], key=lambda r: -(r[2] or 0)), [2])
aba('10 · Varredura agendamentos', [[VR['nota']], VR['varag_cols']] + [r[:-1] + [dia(r[-1])] for r in sorted(VR['va'], key=lambda r: -(r[3] or 0))], [2])

# 11 · diferença
d = [['OCI', '22/10: exames + consultas (CID aceito)', '25/10: teto', 'diferença do teto', '25/10: finalidade', '25/10: finalidade viva']]
for c, v in diferenca['ocis'].items():
    d.append([c, v['22/10 exames + consultas'], v['25/10 teto'], v['diferenca_teto'], v['25/10 finalidade'], v['25/10 finalidade viva']])
u = diferenca['uniao']
d.append(['união das sete', u['22/10 exames + consultas'], u['25/10 teto'], u['25/10 teto'] - u['22/10 exames + consultas'], u['25/10 finalidade'], u['25/10 finalidade viva']])
d += [[], ['fila', '22/10 fila', '25/10 fila', 'diferença', '22/10 pessoas', '25/10 pessoas']]
for n, v in diferenca['filas'].items():
    d.append([n, v['22/10 fila'], v['25/10 fila'], v['25/10 fila'] - (v['22/10 fila'] or 0), v['22/10 pessoas'], v['25/10 pessoas']])
aba('11 · Diferença 22-10 (calc.)', d)

wb.save(AQUI.parent / 'mapa_social_20261025.xlsx')
print('coleta_20261025.json e ../mapa_social_20261025.xlsx gravados;', len(alarmes), 'alarmes')
for a in alarmes:
    print(' ', a)
