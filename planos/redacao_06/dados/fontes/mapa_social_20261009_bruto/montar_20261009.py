# Monta ../mapa_social_20261009.xlsx a partir de coleta_20261009.json (saída da Qlik Engine API
# do painel Mapa Social da Saúde, base recarregada em 09/10/2026 11:32:55).
# A comparação lê a coleta de 06/10/2026 do plano 4 direto do JSON dela:
#   planos/redacao_04/dados/fontes/mapa_social_20261006_bruto/coleta_20261006.json
# (raiz do repositório em $PLANOS_SES; padrão /Users/hendrick/Projetos/planos-ses).
# Uso: python3 montar_20261009.py   (de qualquer pasta)
# Só contagens agregadas: nenhum CNS, CPF, nome ou data de nascimento.
import json
import os
from pathlib import Path

import openpyxl
from openpyxl.styles import Font, PatternFill

AQUI = Path(__file__).resolve().parent
j = json.loads((AQUI / 'coleta_20261009.json').read_text(encoding='utf-8'))
RAIZ = Path(os.environ.get('PLANOS_SES', '/Users/hendrick/Projetos/planos-ses'))
ANT_JSON = RAIZ / 'planos/redacao_04/dados/fontes/mapa_social_20261006_bruto/coleta_20261006.json'
a = json.loads(ANT_JSON.read_text(encoding='utf-8')) if ANT_JSON.exists() else None

vis = lambda s: s.replace('\xa0', '[NBSP]')          # o nome exato, com o espaço não separável à vista
r1 = lambda x: None if x is None else round(x, 1)


def sig_fmt(c):
    c = str(c)
    return f'{c[0:2]}.{c[2:4]}.{c[4:6]}.{c[6:9]}-{c[9:]}' if len(c) == 10 else (f'0{c[0]}.{c[1:3]}.{c[3:5]}.{c[5:8]}-{c[8]}' if len(c) == 9 else c)


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


C = j['conjuntos']
P = {p['nome']: p for p in j['procedimentos']}
ORDEM_US = [p['nome'] for p in j['procedimentos'] if p['grupo'] == 'US']
ORDEM_TC = [p['nome'] for p in j['procedimentos'] if p['grupo'] == 'TC']
CODS = [k[4:] for k in C if k.startswith('cod_')]

# ---- 0 · Leia-me
aba('0 · Leia-me', [
    ['Mapa Social da Saúde — fila dos onze procedimentos de imagem (ultrassonografia e tomografia), coleta de 09/10/2026'],
    ['Painel', 'Mapa Social da Saúde – Regulamentação (MPDFT) · Lista de Espera – Exames e Consultas'],
    ['Endereço', j['painel']],
    ['App Qlik', j['titulo_app'] + ' · ' + j['app']],
    ['Dados', 'SISREG/DATASUS'],
    ['Última recarga da base', '09/10/2026 11:32:55 (Brasília) — qLastReloadTime ' + j['recarga_utc']],
    ['Consulta', j['consulta'] + ' (relógio do motor, Brasília); a recarga foi conferida de novo às 11:53:57 e não mudou'],
    ['Solicitação mais recente na base', j['max_data_solicitacao']],
    ['Via', 'Qlik Engine API do próprio painel (hipercubos de sessão e evaluateEx), no navegador embutido. Sem leitura de tela, sem exportação pelos ícones.'],
    ['Medida "fila"', 'Count(Distinct {1<' + j['filtro_fila'] + ', nomes da fila>} contador_solicitacao) — os três status de fila'],
    ['Devolvidas', 'fora da fila, contadas à parte: ' + j['filtro_devolvidas']],
    ['Pessoas', 'Count(Distinct {mesmo conjunto da fila} cns_usuario_solicitacao) — só a contagem sai do motor'],
    ['Espera', 'Avg, Median e Max de tempo_espera_solicitacao, em dias, calculadas no motor sobre os registros do conjunto (não é média das linhas)'],
    ['Recorte', 'todos os anos; cada nome de fila fixo na expressão de conjunto ({1<...>}), sem depender da tela'],
    ['Objeto', '11 códigos SIGTAP em 16 nomes de fila; partes moles (02.05.02.006-2) fora do objeto desde 22/09/2026, coletada à parte, fora da soma'],
    ['Enquadramento', 'o de planos/redacao_04/dados/fontes/mapa_social_20261006_bruto/coleta_20261006.json (procedimentos[].nome_sisreg); os 17 nomes responderam com a grafia exata'],
    ['[NBSP]', 'nas abas, o espaço não separável (U+00A0) do nome interno aparece como [NBSP]; o JSON guarda o caractere real'],
    ['Abas calculadas', 'só a 8 (diferença para 06/10), a coluna de % da aba 5 e a de agendadas por mês da aba 6; dizem isso no título'],
    ['Decisão (aba 6)', 'regra escrita no script montar_20261009.py, função decidir(): não é dado do motor'],
    [],
    ['aba', 'conteúdo'],
    ['1', 'fila por nome de fila (17 nomes: 16 do objeto e partes moles)'],
    ['2', 'fila por código SIGTAP do objeto (11 códigos, só os nomes do enquadramento)'],
    ['3', 'conjuntos: ultrassonografia, tomografia, objeto, ultrassonografia com partes moles'],
    ['4', 'Região de Saúde — fila por nome de fila'],
    ['5', 'Região de Saúde — fila por código e nos conjuntos; pessoas nos conjuntos'],
    ['6', 'varredura das filas: as 119 filas achadas (enquadramento, mesmo código, nome parecido) com estudo e decisão; subtotais do mesmo código'],
    ['7', 'contexto: outros códigos dos subgrupos 02.05.01, 02.05.02, 02.06.02, 02.06.03 (fora da soma)'],
    ['8', 'CALCULADO — diferença para a coleta de 06/10/2026 do plano 4'],
    ['9', 'filas de nome parecido em outras modalidades (ressonância, radiografia, cintilografia, punção, consulta): só registro'],
], cab=(21,))

# ---- 1 · por nome
cab = ['grupo', 'fila (nome curto)', 'nome interno no SISREG (exato)', 'SIGTAP', 'descrição SIGTAP', 'fila', 'pessoas', 'devolvidas',
       'total (com devolvidas)', 'espera média (dias)', 'mediana', 'máxima']
lin = [cab]
for p in j['procedimentos']:
    lin.append([p['grupo'], p['nome'], vis(p['nome_sisreg']), sig_fmt(p['sigtap']), p['desc_sigtap'], p['fila'], p['pessoas'], p['devolvidas'],
                p['total'], r1(p['espera_media']), r1(p['espera_mediana']), r1(p['espera_max'])])
aba('1 · Por nome de fila', lin, cab=(1,))

# ---- 2 · por código
cab = ['SIGTAP', 'descrição SIGTAP', 'nomes de fila', 'fila', 'pessoas', 'devolvidas', 'pessoas com devolvida', 'total', 'espera média', 'mediana',
       'máxima', 'solicitação mais antiga na fila', 'mais recente']
desc = {p['sigtap']: p['desc_sigtap'] for p in j['procedimentos']}
lin = [cab]
for c in CODS:
    v = C['cod_' + c]
    lin.append([sig_fmt(c), desc[c], v['nomes'], v['fila'], v['pessoas'], v['devolvidas'], v['pessoas_devolvidas'], v['total'],
                r1(v['espera_media']), r1(v['espera_mediana']), r1(v['espera_max']), v['mais_antiga'], v['mais_recente']])
aba('2 · Por código SIGTAP', lin, cab=(1,))

# ---- 3 · conjuntos
cab = ['conjunto', 'nomes de fila', 'fila', 'pessoas', 'devolvidas', 'pessoas com devolvida', 'total', 'espera média', 'mediana', 'máxima',
       'mais antiga', 'mais recente']
lin = [cab]
for k, rot in (('US_objeto', 'ultrassonografia (8 códigos, 11 nomes)'), ('TC_objeto', 'tomografia (3 códigos, 5 nomes)'),
               ('objeto', 'objeto (11 códigos, 16 nomes)'), ('US_com_partes_moles', 'ultrassonografia + partes moles (fora do objeto)'),
               ('nome_Partes moles (fora do objeto)', 'partes moles sozinha (fora do objeto)')):
    v = C[k]
    lin.append([rot, v['nomes'], v['fila'], v['pessoas'], v['devolvidas'], v['pessoas_devolvidas'], v['total'], r1(v['espera_media']),
                r1(v['espera_mediana']), r1(v['espera_max']), v['mais_antiga'], v['mais_recente']])
lin += [[], ['outras medidas do motor'],
        ['pessoas que esperam TC de abdômen superior e TC de pelve ao mesmo tempo', j['extra']['combo_abdsup_e_pelve_mesma_pessoa']],
        ['pessoas da fila de partes moles que também estão na fila de ultrassonografia do objeto', j['extra']['partes_moles_pessoas_ja_na_fila_US_objeto']],
        ['grupos 4 e 5 de tomografia do painel, inteiros — fila', j['grupoTC']['fila']],
        ['grupos 4 e 5 de tomografia do painel, inteiros — pessoas', j['grupoTC']['pessoas']],
        ['grupos 4 e 5 de tomografia do painel, inteiros — espera média', r1(j['grupoTC']['espera'])]]
aba('3 · Conjuntos', lin, cab=(1,))

# ---- 4 e 5 · Região
cols = j['regioes_cols']
ix = {c: i + 1 for i, c in enumerate(cols)}
REG = j['regioes']
cab = ['Região de Saúde da unidade solicitante'] + [n for n in ORDEM_US] + ['Partes moles (fora do objeto)'] + ORDEM_TC
lin = [cab]
for r in REG:
    lin.append([r[0]] + [r[ix['fila_nome_' + n]] for n in ORDEM_US + ['Partes moles (fora do objeto)'] + ORDEM_TC])
lin.append(['total (motor)'] + [P[n]['fila'] for n in ORDEM_US + ['Partes moles (fora do objeto)'] + ORDEM_TC])
aba('4 · Região por nome (fila)', lin, cab=(1,))

cab = ['Região de Saúde'] + [sig_fmt(c) for c in CODS] + ['ultrassonografia — fila', 'tomografia — fila', 'objeto — fila',
                                                       'ultrassonografia — pessoas', 'tomografia — pessoas', 'objeto — pessoas',
                                                       'objeto — % da fila (CALCULADO)']
lin = [cab]
tot_obj = C['objeto']['fila']
for r in REG:
    lin.append([r[0]] + [r[ix['fila_cod_' + c]] for c in CODS] + [r[ix['fila_US_objeto']], r[ix['fila_TC_objeto']], r[ix['fila_objeto']],
                                                               r[ix['pessoas_US_objeto']], r[ix['pessoas_TC_objeto']], r[ix['pessoas_objeto']],
                                                               round(r[ix['fila_objeto']] / tot_obj * 100, 2)])
lin.append(['total (motor)'] + [C['cod_' + c]['fila'] for c in CODS] + [C['US_objeto']['fila'], C['TC_objeto']['fila'], C['objeto']['fila'],
                                                                      C['US_objeto']['pessoas'], C['TC_objeto']['pessoas'], C['objeto']['pessoas'], 100])
lin += [[], ['As pessoas por Região não somam o total: quem tem solicitação vinda de duas Regiões conta nas duas.'],
        ['"(sem região: nulo)" é o campo regiao_saude_solicitante vazio; URD, Contratado/Credenciado e Público - Não SES não são Região de Saúde. Nenhuma linha foi rateada.']]
aba('5 · Região por código', lin, cab=(1,))

# ---- 6 · varredura: estudo e decisão de cada fila
# A decisão segue o método (metodo/coleta/mapa_social.md, varredura, regra de 09/10/2026):
#   objeto ............................ entra (enquadramento do plano 4, objeto informado por quem chamou)
#   partes moles ...................... fica fora (fora do objeto desde 22/09/2026)
#   outro código SIGTAP ............... fica fora (o objeto são onze códigos; só entra se o objeto mudar)
#   mesmo código, fora do enquadramento a decidir (fila nova não entra na soma sem decisão), com a nota do tipo de fila
V = j['varredura']
E = V['estudo']
ec = {c: i for i, c in enumerate(E['cols'])}


def decidir(r):
    g = lambda c: r[ec[c]]
    classe, nome = g('classe'), g('nome_sisreg').replace('\xa0', ' ').upper()
    if classe == 'objeto':
        return 'entra', 'enquadramento do plano 4'
    if classe == 'fora_22_09':
        return 'fica fora', 'fora do objeto desde 22/09/2026'
    if classe == 'nome_parecido_outro_codigo':
        return 'fica fora', 'código SIGTAP fora dos onze do objeto; só entra se o objeto mudar'
    sem_2026 = g('fila_solicitada_em_2026') == 0 and g('agendadas_2026_jan_set') == 0
    primeira = g('primeira_solicitacao_na_base') or ''
    pag = g('primeiro_agendamento') or ''
    if sem_2026 and g('fila') <= 10:
        nota = 'resíduo: nome antigo, sem solicitação nem agendamento em 2026'
    elif sem_2026:
        nota = 'fila parada: sem solicitação nova nem agendamento em 2026'
    elif primeira.endswith('2026') and (not pag or pag.endswith('2026')):
        nota = 'fila aberta em 2026 (desde ' + primeira + ')'
    elif 'EMERG' in nome:
        nota = 'fila de emergência, mesmo código'
    elif 'INFANT' in nome:
        nota = 'faixa etária infantil, mesmo código'
    elif nome.startswith('ANGIOTOMOGRAFIA'):
        nota = 'angiotomografia, mesmo código'
    elif 'DOPPLER' in nome:
        nota = 'outro doppler com o mesmo código'
    elif g('sigtap') == '205010040':
        nota = 'outro exame com o código de doppler'
    elif 'C/SEDACAO' in nome or 'S/CONTRASTE' in nome:
        nota = 'variante de contraste ou sedação, mesmo código'
    else:
        nota = 'variante de nome, mesmo código'
    return 'a decidir', nota


ROT = {'objeto': 'objeto', 'fora_22_09': 'partes moles', 'mesmo_codigo': 'mesmo código', 'nome_parecido_outro_codigo': 'nome parecido, outro código'}
cab = ['decisão', 'motivo / nota', 'classe', 'nome interno no SISREG (exato)', 'SIGTAP', 'fila', 'pessoas', 'devolvidas', 'espera média', 'mediana',
       'idade mediana', 'idade mín.', 'idade máx.', '1ª solicitação na base', 'mais antiga na fila', 'fila solicitada em 2026', 'CIDs principais na fila',
       'agendadas 2025', 'agendadas 2026 (jan–set)', 'agendadas/mês 2026 (CALCULADO)', 'agendadas set/2026', 'agendadas out/2026 (parcial)',
       'agendadas depois de out/2026', '1º agendamento', 'último agendamento']
lin = [['Varredura das filas: toda fila achada, com o estudo e a decisão (regra do método de 09/10/2026). O que não é "entra" fica FORA DA SOMA.'],
       ['Agendadas = contador_agendamento por mês de data_agendamento (a data marcada). A coluna por mês é a de jan–set/2026 dividida por 9 (CALCULADO).'], [], cab]
for r in E['rows']:
    d, nota = decidir(r)
    g = lambda c: r[ec[c]]
    lin.append([d, nota, ROT[g('classe')], vis(g('nome_sisreg')), sig_fmt(g('sigtap')), g('fila'), g('pessoas'), g('devolvidas'), r1(g('espera_media')),
                r1(g('espera_mediana')), g('idade_mediana'), g('idade_min'), g('idade_max'), g('primeira_solicitacao_na_base'), g('mais_antiga_na_fila'),
                g('fila_solicitada_em_2026'), g('cid_top3_na_fila'), g('agendadas_2025'), g('agendadas_2026_jan_set'), round(g('agendadas_2026_jan_set') / 9),
                g('agendadas_2026_09'), g('agendadas_2026_10'), g('agendadas_depois_de_10_2026'), g('primeiro_agendamento'), g('ultimo_agendamento')])
n_sub = len(lin) + 2
lin += [[], ['subtotais do motor — mesmo código, fora do enquadramento', 'nomes com fila', 'fila', 'pessoas', 'devolvidas', 'espera média', 'mediana',
             'pessoas já na fila do objeto', 'pessoas fora da fila do objeto', 'fila dessas pessoas']]
for k, v in V['conjuntos'].items():
    rot = sig_fmt(k[4:]) if k.startswith('cod_') else k
    lin.append([rot, v['nomes_com_fila'], v['fila'], v['pessoas'], v['devolvidas'], r1(v['espera_media']), r1(v['espera_mediana']),
                v['pessoas_ja_no_objeto'], v['pessoas_fora_do_objeto'], v['fila_de_pessoas_fora_do_objeto']])
aba('6 · Varredura das filas', lin, cab=(4, n_sub))

# ---- 9 · nome parecido em outras modalidades (só registro)
X9 = V['nome_parecido_outras_modalidades']
lin = [['Filas com nome parecido ao de um exame do objeto, fora dos códigos 02.05 e 02.06 (outra modalidade ou não é exame). Ficam fora: não são ultrassom nem tomografia.'],
       [], ['nome interno no SISREG (exato)', 'SIGTAP', 'fila']]
for r in X9['rows']:
    lin.append([vis(r[0]), sig_fmt(r[1]) if r[1] != '-' else '-', r[2]])
aba('9 · Parecido, outra modalid.', lin, cab=(3,))

# ---- 7 · contexto
X = j['contexto_subgrupos']
lin = [['Outros códigos dos subgrupos SIGTAP 02.05.01, 02.05.02, 02.06.02 e 02.06.03 (fora do enquadramento e fora da soma). Só contexto.'], [],
       ['SIGTAP', 'descrição SIGTAP', 'fila', 'pessoas', 'devolvidas', 'espera média', 'mediana', 'nomes com fila']]
for r in X['por_codigo']:
    lin.append([sig_fmt(r[0]), r[1], r[2], r[3], r[4], r1(r[5]), r1(r[6]), r[7]])
n0 = len(lin) + 2
lin += [[], ['nomes de fila com 100 ou mais na fila'], ['nome interno no SISREG (exato)', 'SIGTAP', 'fila', 'pessoas', 'devolvidas', 'espera média', 'mediana']]
for r in X['nomes_fila_100_ou_mais']:
    lin.append([vis(r[0]), sig_fmt(r[1]), r[2], r[3], r[4], r1(r[5]), r1(r[6])])
ws = aba('7 · Contexto subgrupos', lin, cab=(3, n0 + 1))

# ---- 8 · diferença para 06/10 (CALCULADO)
if a:
    AP = {p['nome']: p for p in a['procedimentos']}
    cab = ['fila', 'fila 06/10', 'fila 09/10', 'Δ fila', 'pessoas 06/10', 'pessoas 09/10', 'Δ pessoas', 'devolvidas 06/10', 'devolvidas 09/10',
           'espera média 06/10', 'espera média 09/10', 'Δ espera']
    lin = [['CALCULADO — diferença entre esta coleta (base de 09/10/2026 11:32) e a de 06/10/2026 (base de 06/10/2026 21:32, plano 4)'], [], cab]
    for n in ORDEM_US + ['Partes moles (fora do objeto)'] + ORDEM_TC:
        p, q = AP[n], P[n]
        lin.append([n, p['fila'], q['fila'], q['fila'] - p['fila'], p['pessoas'], q['pessoas'], q['pessoas'] - p['pessoas'], p['devolvidas'],
                    q['devolvidas'], r1(p['espera_fila']), r1(q['espera_media']), r1(q['espera_media'] - p['espera_fila'])])
    AC = a['conjuntos']
    for k, rot in (('US_objeto', 'ultrassonografia'), ('TC_objeto', 'tomografia')):
        p, q = AC[k], C[k]
        lin.append([rot, p['fila'], q['fila'], q['fila'] - p['fila'], p['pessoas'], q['pessoas'], q['pessoas'] - p['pessoas'], p['devolvidas'],
                    q['devolvidas'], r1(p['espera_fila']), r1(q['espera_media']), r1(q['espera_media'] - p['espera_fila'])])
    po = a['pess']['out']['US_TC']
    lin.append(['objeto', po['solic'], C['objeto']['fila'], C['objeto']['fila'] - po['solic'], po['pessoas'], C['objeto']['pessoas'],
                C['objeto']['pessoas'] - po['pessoas'], AC['US_objeto']['devolvidas'] + AC['TC_objeto']['devolvidas'], C['objeto']['devolvidas'],
                '', r1(C['objeto']['espera_media']), ''])
    lin.append(['(objeto: devolvidas de 06/10 = soma dos dois conjuntos; a espera do objeto inteiro não foi medida em 06/10)'])
    lin += [[], ['por código', 'fila 06/10', 'fila 09/10', 'Δ fila', 'pessoas 06/10', 'pessoas 09/10', 'Δ pessoas']]
    for c in CODS:
        p, q = a['pess']['porCod'][c], C['cod_' + c]
        lin.append([sig_fmt(c), p['solic'], q['fila'], q['fila'] - p['solic'], p['pessoas'], q['pessoas'], q['pessoas'] - p['pessoas']])
    # Região: em 06/10 a fila por Região foi gravada por nome; a soma dos nomes é cálculo desta aba
    acols = a['regioes_cols']
    us_i = [acols.index(n) + 1 for n in ORDEM_US]
    tc_i = [acols.index(n) + 1 for n in ORDEM_TC]
    areg = {('(sem região: nulo)' if r[0] == '-' else r[0]): (sum(r[i] for i in us_i), sum(r[i] for i in tc_i)) for r in a['regioes']}
    lin += [[], ['Região (06/10 = soma dos nomes, CALCULADO)', 'US 06/10', 'US 09/10', 'Δ US', 'TC 06/10', 'TC 09/10', 'Δ TC']]
    for r in REG:
        u0, t0 = areg.get(r[0], (0, 0))
        u1, t1 = r[ix['fila_US_objeto']], r[ix['fila_TC_objeto']]
        lin.append([r[0], u0, u1, u1 - u0, t0, t1, t1 - t0])
    lin += [[], ['solicitação mais recente na base', a['max_data_solicitacao'], j['max_data_solicitacao']],
            ['pessoas com TC de abdômen superior e de pelve', a['pess']['combo_abdsup_e_pelve_mesma_pessoa'], j['extra']['combo_abdsup_e_pelve_mesma_pessoa']],
            ['grupos 4 e 5 de tomografia — fila', a['grupoTC']['fila'], j['grupoTC']['fila']]]
    aba('8 · Δ 06-10 (CALCULADO)', lin, cab=(3,))

wb._sheets.sort(key=lambda ws: int(ws.title.split(' ')[0]))   # abas na ordem do número
saida = AQUI.parent / 'mapa_social_20261009.xlsx'
wb.save(saida)
print('gravado', saida)
