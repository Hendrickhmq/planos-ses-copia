# Monta ../mapa_social_20261015.xlsx a partir de coleta_20261015.json (saída da Qlik Engine API
# do painel Mapa Social da Saúde, base recarregada em 15/10/2026 19:32:31).
# Varredura das filas de exames de imagem (subgrupos SIGTAP 02.04 a 02.10) para escolher a fila
# de uma emenda nova, fora do plano 4. A comparação lê a coleta de 09/10/2026 do redacao_06:
#   planos/redacao_06/dados/fontes/mapa_social_20261009_bruto/coleta_20261009.json
# (raiz do repositório em $PLANOS_SES; padrão /Users/hendrick/Projetos/planos-ses).
# Uso: python3 montar_20261015.py   (de qualquer pasta)
# Só contagens agregadas: nenhum CNS, CPF, nome ou data de nascimento.
import json
import os
from pathlib import Path

import openpyxl
from openpyxl.styles import Font, PatternFill

AQUI = Path(__file__).resolve().parent
j = json.loads((AQUI / 'coleta_20261015.json').read_text(encoding='utf-8'))
RAIZ = Path(os.environ.get('PLANOS_SES', '/Users/hendrick/Projetos/planos-ses'))
ANT_JSON = RAIZ / 'planos/redacao_06/dados/fontes/mapa_social_20261009_bruto/coleta_20261009.json'
a = json.loads(ANT_JSON.read_text(encoding='utf-8')) if ANT_JSON.exists() else None

vis = lambda s: s.replace('\xa0', '[NBSP]') if s else s     # o nome exato, com o espaço não separável à vista
r1 = lambda x: None if x is None else round(x, 1)

MOD = {'204': 'radiologia', '205': 'ultrassonografia', '206': 'tomografia', '207': 'ressonância magnética',
       '208': 'medicina nuclear', '210': 'radiologia intervencionista'}
ORDEM_MOD = list(MOD)


def sig_fmt(c):
    if not c:
        return '(sem código)'
    c = str(c)
    if len(c) == 9:
        return f'0{c[0]}.{c[1:3]}.{c[3:5]}.{c[5:8]}-{c[8]}'
    return c + ' (malformado)'


def modalidade(c):
    if not c:
        return 'sem código'
    return MOD.get(str(c)[:3], 'fora dos subgrupos de imagem')


DESC = j['descricao_sigtap']
FC = {c: i for i, c in enumerate(j['filas_cols'])}
CC = {c: i for i, c in enumerate(j['por_codigo_cols'])}
AG = {r[0]: r for r in j['agendadas_jan_set_2026_por_codigo']}


def outro_tipo(c):
    c = str(c or '')
    if c.startswith('20101'):
        return 'punção ou biópsia guiada por imagem (02.01), não é exame de imagem'
    if c.startswith('2110602') or c.startswith('2110600'):
        return 'exame oftalmológico (02.11.06)'
    if c.startswith('21102'):
        return 'cateterismo cardíaco, hemodinâmica (02.11.02)'
    if not c:
        return 'sem código SIGTAP; grupo radiodiagnóstico do painel'
    return 'outro código'


def decidir(f):
    """A decisão de cada fila: regra escrita, não dado do motor (pedido da conversa principal, 15/10/2026)."""
    g = lambda c: f[FC[c]]
    cat, nome = g('categoria'), (g('nome_sisreg') or '').replace('\xa0', ' ').upper()
    sem_2026 = g('solicitacoes_2026_todos_status') == 0 and g('agendadas_2026_todos_meses') == 0
    if cat == 'plano4':
        return 'plano 4', 'enquadramento do plano 4: fora da soma, só referência'
    if cat == 'residuo' or (cat == 'mesmo_codigo_plano4' and sem_2026):
        extra = ' (mesmo código do plano 4)' if cat == 'mesmo_codigo_plano4' else ''
        return 'fica fora', 'resíduo: nenhuma solicitação nem agendamento em 2026' + extra
    if cat == 'mesmo_codigo_plano4':
        return 'a decidir', 'mesmo código do plano 4: risco de sobreposição com a execução do plano 4'
    notas = []
    if cat == 'outro_codigo_nome_de_imagem':
        notas.append('fora dos subgrupos de imagem: ' + outro_tipo(g('sigtap')))
    primeira = g('primeira_solicitacao_na_base') or ''
    if primeira.endswith('2026'):
        notas.append('fila aberta em 2026 (desde ' + primeira + ')')
    if 'EMERG' in nome:
        notas.append('fila de emergência')
    if 'INFANT' in nome:
        notas.append('faixa etária infantil')
    if g('fila_pedida_em_2026') == 0:
        notas.append('nada da fila pedido em 2026')
    return 'a decidir', 'candidata' + ('; ' + '; '.join(notas) if notas else '')


wb = openpyxl.Workbook()
wb.remove(wb.active)
B = Font(bold=True)
HF = PatternFill('solid', fgColor='DDEBF7')


def aba(titulo, linhas, cab=()):
    ws = wb.create_sheet(titulo)
    for r in linhas:
        ws.append(list(r))
    for i in cab:
        for c in ws[i]:
            c.font = B
            c.fill = HF
    for col in ws.columns:
        ws.column_dimensions[col[0].column_letter].width = min(70, max(9, max(len(str(c.value or '')) for c in col) * 0.9))
    return ws


# ---- 0 · Leia-me
aba('0 · Leia-me', [
    ['Mapa Social da Saúde — varredura das filas de exames de imagem (subgrupos SIGTAP 02.04 a 02.10), coleta de 15/10/2026'],
    ['Para quê', 'escolher a fila de uma emenda nova de exames de imagem (redacao_07), fora do plano 4. Não há objeto: é varredura para comparar candidatas'],
    ['Painel', 'Mapa Social da Saúde – Regulamentação (MPDFT) · Lista de Espera – Exames e Consultas'],
    ['Endereço', j['painel']],
    ['App Qlik', j['titulo_app'] + ' · ' + j['app']],
    ['Dados', 'SISREG/DATASUS'],
    ['Última recarga da base', j['recarga_brasilia'] + ' (Brasília) — qLastReloadTime ' + j['recarga_utc'] + '; conferida de novo no fim: ' + j['recarga_conferida_no_fim']],
    ['Consulta', j['consulta'] + ' a ' + j['consulta_fim'] + ' (relógio do motor, Brasília)'],
    ['Nota', j['nota_consulta']],
    ['Solicitação mais recente na base', j['max_data_solicitacao']],
    ['Via', 'Qlik Engine API do próprio painel (hipercubos de sessão e evaluateEx), no navegador embutido. Sem leitura de tela, sem exportação pelos ícones.'],
    ['Medida "fila"', 'Count(Distinct {1<' + j['filtro_fila'] + ', recorte>} contador_solicitacao) — os três status de fila'],
    ['Devolvidas', 'fora da fila, contadas à parte: ' + j['filtro_devolvidas']],
    ['Pessoas', 'Count(Distinct {mesmo conjunto da fila} cns_usuario_solicitacao) — só a contagem sai do motor'],
    ['Espera', 'Avg, Median e Max de tempo_espera_solicitacao, em dias, calculadas no motor sobre os registros do conjunto (não é média das linhas)'],
    ['Universo', j['universo']['por_codigo']],
    ['Busca por nome', j['universo']['por_nome']],
    ['Categorias', '; '.join(k + ': ' + v for k, v in j['categorias'].items())],
    ['Decisão', 'regra escrita no script montar_20261015.py, função decidir(): não é dado do motor'],
    ['[NBSP]', 'nas abas, o espaço não separável (U+00A0) do nome interno aparece como [NBSP]; o JSON guarda o caractere real'],
    ['Calculado', 'as colunas "agendadas/mês" (jan–set/2026 ÷ 9), os % e a aba 9 (diferença para 09/10) são calculados e dizem isso no título; o resto é do motor'],
    [],
    ['aba', 'conteúdo'],
    ['1', 'por código SIGTAP — candidatas (fora dos onze códigos do plano 4), sem os resíduos; tabela principal'],
    ['2', 'por modalidade — candidatas, mesmo código do plano 4, plano 4, resíduo, fora do plano 4'],
    ['3', 'mesmo código do plano 4 — por código, com e sem resíduo'],
    ['4', 'plano 4 — referência, por código'],
    ['5', 'varredura fila a fila: as 756 filas achadas, com o estudo e a decisão'],
    ['6', 'Região de Saúde — os quinze códigos candidatos de maior fila (fila e pessoas)'],
    ['7', 'Região de Saúde — conjuntos e modalidades'],
    ['8', 'outro código com nome de imagem; falsos positivos da busca por nome'],
    ['9', 'CALCULADO — diferença para a coleta de 09/10/2026 (mesmo código e plano 4)'],
], cab=(23,))

# ---- 1 · por código, candidatas
res_cod = {r[0]: r for r in j['por_codigo']['res']}
cab = ['modalidade', 'SIGTAP', 'descrição SIGTAP', 'nomes com fila', 'fila', 'pessoas', 'devolvidas', 'espera média', 'mediana', 'máxima',
       'idade mediana', 'fila pedida em 2026', 'pessoas já na fila do plano 4', '1ª solicitação na base', 'agendadas jan–set/2026 (motor)',
       'agendadas/mês 2026 (CALCULADO)', 'resíduo do código: nomes', 'resíduo do código: fila']
lin = [['Por código SIGTAP — candidatas: códigos dos subgrupos de imagem fora dos onze do plano 4, sem as filas-resíduo. Motor, por código; não somar códigos como se fossem um objeto.'], [], cab]
cand = sorted(j['por_codigo']['cand'], key=lambda r: (ORDEM_MOD.index(str(r[0])[:3]), -r[CC['fila']]))
for r in cand:
    c = r[0]
    ag = AG.get(c, [c, 0, 0, 0])[1]
    rs = res_cod.get(c)
    lin.append([modalidade(c), sig_fmt(c), DESC.get(c), r[1], r[2], r[3], r[4], r1(r[5]), r1(r[6]), r1(r[7]), r[8], r[9], r[10], r[11],
                ag, round(ag / 9), rs[1] if rs else 0, rs[2] if rs else 0])
aba('1 · Por código (candidatas)', lin, cab=(3,))

# ---- 2 · por modalidade
PM = j['por_modalidade']
AGM = {r[0]: r for r in j['agendadas_jan_set_2026_por_modalidade']}
cab = ['conjunto', 'modalidade', 'nomes com fila', 'fila', 'pessoas', 'devolvidas', 'espera média', 'mediana', 'máxima', 'idade mediana',
       'fila pedida em 2026', 'pessoas já na fila do plano 4', 'agendadas jan–set/2026 (motor)', 'agendadas/mês (CALCULADO)']
lin = [['Por modalidade (prefixo do código SIGTAP) — motor. Pessoas distintas dentro de cada linha.'], [], cab]
ROT = {'cand': 'candidata', 'mesmo': 'mesmo código do plano 4 (com resíduo)', 'mesmo_semres': 'mesmo código do plano 4 (sem resíduo)',
       'p4': 'plano 4 (referência)', 'res': 'resíduo (outros códigos)', 'fora_p4': 'fora do plano 4 = candidata + mesmo código sem resíduo'}
AGI = {'cand': 1, 'mesmo_semres': 2, 'mesmo': 2, 'p4': 3}
for k in ('cand', 'mesmo_semres', 'mesmo', 'p4', 'res', 'fora_p4'):
    for r in sorted(PM[k], key=lambda r: r[0]):
        ag = None
        if k in AGI:
            ag = AGM.get(r[0], [0, 0, 0, 0])[AGI[k]]
        elif k == 'fora_p4':
            ag = AGM.get(r[0], [0, 0, 0, 0])[1] + AGM.get(r[0], [0, 0, 0, 0])[2]
        lin.append([ROT[k], MOD[r[0]], r[1], r[2], r[3], r[4], r1(r[5]), r1(r[6]), r1(r[7]), r[8], r[9], r[10], ag,
                    None if ag is None else round(ag / 9)])
lin += [[], ['totais do motor (todas as modalidades; universo, não é objeto)'], ['conjunto'] + j['totais_cols']]
for k, v in j['totais'].items():
    lin.append([k] + [r1(x) if isinstance(x, float) else x for x in v])
X = j['extra_motor']
lin += [[], ['outras medidas do motor (' + X['consulta'] + ')'],
        ['cintilografia de miocárdio, estresse ou repouso (02.08.01.002-5 e 02.08.01.003-3) — pessoas na fila', X['cintilografia_miocardio_estresse_ou_repouso_pessoas']],
        ['cintilografia de miocárdio — pessoas na fila das duas', X['cintilografia_miocardio_estresse_e_repouso_mesma_pessoa']]]
aba('2 · Por modalidade', lin, cab=(3,))

# ---- 3 · mesmo código do plano 4
cab = ['SIGTAP', 'descrição SIGTAP', 'conjunto', 'nomes com fila', 'fila', 'pessoas', 'devolvidas', 'espera média', 'mediana', 'máxima',
       'idade mediana', 'fila pedida em 2026', 'pessoas já na fila do plano 4', 'pessoas fora da fila do plano 4 (CALCULADO)',
       'agendadas jan–set/2026 fora dos nomes do plano 4 (motor)']
lin = [['Mesmo código do plano 4 — as filas dos onze códigos fora dos dezesseis nomes do enquadramento. A decidir: risco de sobreposição com a execução do plano 4.'], [], cab]
for k, rot in (('mesmo', 'com resíduo (comparável a 09/10)'), ('mesmo_semres', 'sem resíduo')):
    for r in sorted(j['por_codigo'][k], key=lambda r: -r[2]):
        lin.append([sig_fmt(r[0]), DESC.get(r[0]), rot, r[1], r[2], r[3], r[4], r1(r[5]), r1(r[6]), r1(r[7]), r[8], r[9], r[10], r[3] - r[10],
                    AG.get(r[0], [0, 0])[1]])
    t = j['totais'][k if k == 'mesmo' else 'mesmo_semres']
    lin.append(['total (motor)', '', rot] + [r1(x) if isinstance(x, float) else x for x in t[:10]] + [t[2] - t[9], ''])
aba('3 · Mesmo código do plano 4', lin, cab=(3,))

# ---- 4 · plano 4, referência
cab = ['SIGTAP', 'descrição SIGTAP', 'nomes', 'fila', 'pessoas', 'devolvidas', 'espera média', 'mediana', 'máxima', 'idade mediana',
       'fila pedida em 2026', 'agendadas jan–set/2026 nos nomes do plano 4 (motor)']
lin = [['Plano 4 — os dezesseis nomes do enquadramento, por código. Fora da soma: só referência e base do cruzamento de pessoas.'], [], cab]
for r in sorted(j['por_codigo']['p4'], key=lambda r: -r[2]):
    lin.append([sig_fmt(r[0]), DESC.get(r[0]), r[1], r[2], r[3], r[4], r1(r[5]), r1(r[6]), r1(r[7]), r[8], r[9], AG.get(r[0], [0, 0, 0])[2]])
t = j['totais']['p4']
lin.append(['total (motor)', '', t[0], t[1], t[2], t[3], r1(t[4]), r1(t[5]), r1(t[6]), t[7], t[8], ''])
aba('4 · Plano 4 (referência)', lin, cab=(3,))

# ---- 5 · varredura fila a fila
cab = ['decisão', 'motivo / nota', 'categoria', 'modalidade', 'SIGTAP', 'nome interno no SISREG (exato)', 'fila', 'pessoas', 'devolvidas',
       'espera média', 'mediana', 'máxima', 'idade mediana', '1ª solicitação na base', 'fila pedida em 2026', 'solicitações 2026 (todos os status)',
       'agendadas jan–set/2026', 'agendadas/mês 2026 (CALCULADO)', 'agendadas 2026 (todos os meses)', 'pessoas já na fila do plano 4',
       'CIDs principais na fila']
lin = [['Varredura das filas: toda fila de imagem achada (fila > 0), com o estudo e a decisão. Só "a decidir" pode virar objeto; plano 4 e resíduo ficam fora da soma.'],
       ['Agendadas = contador_agendamento pela data marcada (data_agendamento). A coluna por mês é jan–set/2026 ÷ 9 (CALCULADO).'], [], cab]
ORD = {'plano4': 0, 'mesmo_codigo_plano4': 1, 'candidata': 2, 'outro_codigo_nome_de_imagem': 3, 'residuo': 4}
for f in sorted(j['filas'], key=lambda f: (ORD[f[2]], f[1] or '', -f[3])):
    d, nota = decidir(f)
    g = lambda c: f[FC[c]]
    lin.append([d, nota, g('categoria'), modalidade(g('sigtap')), sig_fmt(g('sigtap')), vis(g('nome_sisreg')), g('fila'), g('pessoas'), g('devolvidas'),
                r1(g('espera_media')), r1(g('espera_mediana')), r1(g('espera_max')), g('idade_mediana'), g('primeira_solicitacao_na_base'),
                g('fila_pedida_em_2026'), g('solicitacoes_2026_todos_status'), g('agendadas_2026_jan_set'), round(g('agendadas_2026_jan_set') / 9),
                g('agendadas_2026_todos_meses'), g('pessoas_ja_na_fila_plano4'), g('cid_top3_na_fila')])
aba('5 · Varredura fila a fila', lin, cab=(4,))

# ---- 6 · Região, top 15 candidatos
REGS = ['Região Central', 'Região Centro-Sul', 'Região Leste', 'Região Norte', 'Região Oeste', 'Região Sudoeste', 'Região Sul', 'URD',
        'Contratado/Credenciado', 'Serviços Centralizados', 'Público - Não SES', None]
rot_reg = lambda r: '(sem região informada)' if r is None else r
top = []
for r in j['regiao_top15_codigos_candidatos']:
    if r[0] not in top:
        top.append(r[0])
RC = {(r[0], r[1]): r for r in j['regiao_top15_codigos_candidatos']}
FIL = {r[0]: r for r in j['por_codigo']['cand']}
lin = [['Região de Saúde da unidade solicitante, medida fila — os quinze códigos candidatos de maior fila. URD, Contratado/Credenciado, Serviços Centralizados e Público - Não SES não são Região de Saúde. Nenhuma linha foi rateada.'], [],
       ['Região'] + [sig_fmt(c) for c in top]]
lin.append(['(descrição)'] + [DESC.get(c) for c in top])
for reg in REGS:
    lin.append([rot_reg(reg)] + [RC.get((c, reg), [0, 0, 0, 0])[2] for c in top])
lin.append(['total (motor)'] + [FIL[c][2] for c in top])
lin.append(['URD + Contratado/Credenciado — % da fila (CALCULADO)'] +
           [round((RC.get((c, 'URD'), [0, 0, 0])[2] + RC.get((c, 'Contratado/Credenciado'), [0, 0, 0])[2]) / FIL[c][2] * 100, 1) for c in top])
lin += [[], ['pessoas por Região (não somam o total: quem tem solicitação vinda de duas Regiões conta nas duas)'], ['Região'] + [sig_fmt(c) for c in top]]
for reg in REGS:
    lin.append([rot_reg(reg)] + [RC.get((c, reg), [0, 0, 0, 0])[3] for c in top])
lin.append(['total (motor)'] + [FIL[c][3] for c in top])
aba('6 · Região, 15 códigos', lin, cab=(3, len(REGS) + 8))

# ---- 7 · Região, conjuntos e modalidades
lin = [['Região de Saúde, medida fila — conjuntos (motor). A linha sem região é o campo vazio no painel.'], [],
       ['Região'] + j['regiao_conjuntos_cols'][1:]]
RJ = {r[0]: r for r in j['regiao_conjuntos']}
for reg in REGS:
    lin.append([rot_reg(reg)] + list(RJ.get(reg, [reg, 0, 0, 0, 0])[1:]))
lin.append(['total (motor)', j['totais']['cand'][1], j['totais']['mesmo'][1], j['totais']['p4'][1], j['totais']['extra'][1]])
RM = {(r[0], r[1]): r[2] for r in j['regiao_por_modalidade_candidata']}
lin += [[], ['candidatas por modalidade (motor)'], ['Região'] + [MOD[m] for m in ORDEM_MOD]]
for reg in REGS:
    lin.append([rot_reg(reg)] + [RM.get((m, reg), 0) for m in ORDEM_MOD])
PMC = {r[0]: r for r in PM['cand']}
lin.append(['total (motor)'] + [PMC[m][2] if m in PMC else 0 for m in ORDEM_MOD])
aba('7 · Região, conjuntos', lin, cab=(3, len(REGS) + 7))

# ---- 8 · outro código e falsos positivos
lin = [['Filas com nome ou código de imagem fora dos subgrupos 02.04 a 02.10 (motor). A decidir, à parte: não são exame de imagem pelo SIGTAP.'], [],
       ['SIGTAP', 'descrição SIGTAP', 'nomes com fila', 'fila', 'pessoas', 'devolvidas', 'espera média', 'mediana', 'máxima', 'idade mediana',
        'fila pedida em 2026', 'pessoas já na fila do plano 4', 'agendadas jan–set/2026 (motor)', 'tipo']]
for r in sorted(j['por_codigo']['extra'], key=lambda r: -r[2]):
    lin.append([sig_fmt(r[0]), DESC.get(r[0]) if r[0] else None, r[1], r[2], r[3], r[4], r1(r[5]), r1(r[6]), r1(r[7]), r[8], r[9], r[10],
                AG.get(r[0], [0, 0])[1] if r[0] else 0, outro_tipo(r[0])])
lin += [[], ['falsos positivos da busca por nome (não entram)'], ['nomes', 'código', 'motivo']]
for r in j['falsos_positivos_da_busca_por_nome']:
    lin.append(r)
aba('8 · Outro código', lin, cab=(3,))

# ---- 9 · diferença para 09/10 (CALCULADO)
if a:
    V = a['varredura']['conjuntos']
    lin = [['CALCULADO — diferença entre esta coleta (base de 15/10/2026 19:32) e a de 09/10/2026 (base de 09/10/2026 11:32, redacao_06)'], [],
           ['mesmo código do plano 4, por código', 'nomes 09/10', 'nomes 15/10', 'fila 09/10', 'fila 15/10', 'Δ fila', 'pessoas 09/10',
            'pessoas 15/10', 'Δ pessoas', 'devolvidas 09/10', 'devolvidas 15/10', 'espera média 09/10', 'espera média 15/10',
            'pessoas já no plano 4 09/10', 'pessoas já no plano 4 15/10']]
    M = {r[0]: r for r in j['por_codigo']['mesmo']}
    for c in sorted(set(M) | {k[4:] for k in V if k.startswith('cod_')}, key=lambda c: -(M.get(c, [0, 0, 0])[2])):
        p = V.get('cod_' + c, {})
        q = M.get(c, [c, 0, 0, 0, 0, None, None, None, None, 0, 0])
        lin.append([sig_fmt(c), p.get('nomes_com_fila'), q[1], p.get('fila'), q[2], q[2] - (p.get('fila') or 0), p.get('pessoas'), q[3],
                    q[3] - (p.get('pessoas') or 0), p.get('devolvidas'), q[4], r1(p.get('espera_media')), r1(q[5]), p.get('pessoas_ja_no_objeto'), q[10]])
    p, t = V['varredura_total'], j['totais']['mesmo']
    lin.append(['total (motor)', p['nomes_com_fila'], t[0], p['fila'], t[1], t[1] - p['fila'], p['pessoas'], t[2], t[2] - p['pessoas'],
                p['devolvidas'], t[3], r1(p['espera_media']), r1(t[4]), p['pessoas_ja_no_objeto'], t[9]])
    # por nome, mesmo código
    VF = {r[0]: r for r in a['varredura']['filas']}
    NF = {f[0]: f for f in j['filas'] if f[2] == 'mesmo_codigo_plano4'}
    lin += [[], ['mesmo código do plano 4, por nome', 'SIGTAP', 'fila 09/10', 'fila 15/10', 'Δ fila', 'espera média 09/10', 'espera média 15/10']]
    for n in sorted(set(VF) | set(NF), key=lambda n: -(NF[n][3] if n in NF else 0)):
        p, q = VF.get(n), NF.get(n)
        lin.append([vis(n), sig_fmt((q or p)[1]), p[2] if p else None, q[3] if q else None, (q[3] if q else 0) - (p[2] if p else 0),
                    r1(p[5]) if p else None, r1(q[FC['espera_media']]) if q else None])
    # plano 4
    AP = {p['nome_sisreg']: p for p in a['procedimentos']}
    lin += [[], ['plano 4, por nome', 'SIGTAP', 'fila 09/10', 'fila 15/10', 'Δ fila', 'pessoas 09/10', 'pessoas 15/10', 'espera média 09/10',
                 'espera média 15/10']]
    for f in sorted((f for f in j['filas'] if f[2] == 'plano4'), key=lambda f: -f[3]):
        p = AP[f[0]]
        lin.append([vis(f[0]), sig_fmt(f[1]), p['fila'], f[3], f[3] - p['fila'], p['pessoas'], f[4], r1(p['espera_media']), r1(f[6])])
    c9, t = a['conjuntos']['objeto'], j['totais']['p4']
    lin.append(['plano 4 — total (motor)', '', c9['fila'], t[1], t[1] - c9['fila'], c9['pessoas'], t[2], r1(c9['espera_media']), r1(t[4])])
    lin += [[], ['solicitação mais recente na base', a['max_data_solicitacao'], j['max_data_solicitacao']]]
    aba('9 · Δ 09-10 (CALCULADO)', lin, cab=(3,))

wb._sheets.sort(key=lambda ws: int(ws.title.split(' ')[0]))   # abas na ordem do número
saida = AQUI.parent / 'mapa_social_20261015.xlsx'
wb.save(saida)
print('gravado', saida)
