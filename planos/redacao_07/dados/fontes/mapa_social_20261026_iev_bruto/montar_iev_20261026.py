# Monta, a partir de motor_iev_20261026.txt (o texto que o motor do painel Mapa Social da Saúde
# devolveu em 26/10/2026, base recarregada às 16:32:44), três arquivos:
#   motor_iev_20261026.json   o mesmo conteúdo, decodificado (o JSON do motor);
#   coleta_iev_20261026.json  o JSON da coleta no formato do método de 25/10/2026 (filas, ocis,
#                             janela viva, filtro_fila, nomes_internos, alarmes);
#   ../mapa_social_20261026_iev.xlsx  a planilha, uma aba por recorte, com "Leia-me".
# Uso: python3 montar_iev_20261026.py   (de qualquer pasta; precisa de openpyxl)
#
# O que este script CALCULA (e a planilha marca "calculado"): as somas por grupo (ortopedia,
# cardiologia, RM...) e por mês, a comparação com o contratado nos planos do IEV, as proporções,
# os anos de estoque (fila ÷ agendadas em 12 meses) e os alarmes. Tudo o mais é do motor.
# A identificação das unidades do IEV é julgamento da coleta (nome, tipo, data e o que agendam),
# não dado do painel: o painel não traz o convênio.
# Só contagens agregadas: nenhum CNS, CPF, nome ou data de nascimento.
import json
import re
import unicodedata
from pathlib import Path

import openpyxl
from openpyxl.styles import Font, PatternFill

AQUI = Path(__file__).resolve().parent
TXT = AQUI / 'motor_iev_20261026.txt'
TAM, HASH = 117748, 2141536843          # djb2 de 32 bits, calculado no navegador sobre o texto inteiro


def djb2(s):
    x = 5381
    for ch in s:
        x = ((x * 33) ^ ord(ch)) & 0xFFFFFFFF
    return x


T = TXT.read_text(encoding='utf-8')
if T.endswith('\n'):
    T = T[:-1]
assert len(T) == TAM and djb2(T) == HASH, f'texto do motor alterado: {len(T)} {djb2(T)}'
# na transcrição, as aspas viraram ~ e a barra invertida virou ^
m = json.loads(T.replace('~', '"').replace('^', '\\'))
(AQUI / 'motor_iev_20261026.json').write_text(json.dumps(m, ensure_ascii=False, indent=1), encoding='utf-8')

LIM_DOMINANTE, LIM_RARO, LIM_VELHA, LIM_ESTOQUE, LIM_CATEGORIAS = 0.30, 0.05, 0.30, 3, 20
IEV = {'0366986': 'Centro Clínico Samambaia', '3031543': 'Centro Clínico Sobradinho', '9180168': 'Centro de Imagens Gama'}
CERTEZA = {
    '0366986': 'alta: nome no SISREG "CENTRO CLINICO SAMAMBAIA" (o local do plano), tipo Privado, primeiro '
               'agendamento em 03/06/2026, só agenda consultas das especialidades do IEV',
    '3031543': 'alta para as consultas, de 21/05/2026 em diante: nome "CENTRO CLINICO E ECOGRAFICO" / '
               '"Centro Clinico Ecografico Sobrainho", tipo Privado; já agendava RM desde 18/09/2025 (antes do '
               'termo), e a RM não cresceu depois de 29/04/2026: a RM não se atribui ao convênio',
    '9180168': 'média-alta para as consultas de ortopedia, de 08/06/2026 em diante: "CIG CENTRO DE IMAGENS GAMA", '
               'tipo Contratado/Credenciado, agenda RM desde 29/08/2019 (credenciamento antigo); a consulta '
               'de ortopedia é nova e tem o mesmo desenho das outras duas',
}
OCIS = {
    '09.03.01.001-1': dict(k='001-1', exame=None, nome='radiologia', contratado=38594 + 14192),
    '09.03.01.002-0': dict(k='002-0', exame='us', nome='radiologia e ultrassonografia', contratado=12070 + 7000),
    '09.03.01.003-8': dict(k='003-8', exame='tc', nome='radiologia e tomografia', contratado=539),
    '09.03.01.004-6': dict(k='004-6', exame='rm', nome='radiologia e ressonância', contratado=16700 + 11430),
}
KS = ['001-1', '002-0', '003-8', '004-6']
COD = {v['k']: c for c, v in OCIS.items()}
ROT = {k: f'CID aceito {COD[k]}' for k in KS}
CONTRATADO_OUTROS = {
    'cardiologia 09.02.01.001-8': 4647, 'cardiologia 09.02.01.006-9': 1000, 'cardiologia 09.02.01.004-2': 900,
    'saúde da mulher 09.06.01.001-2': 3218, 'déficit auditivo 09.04.01.001-5': 6250,
    'déficit auditivo 09.04.01.002-3': 5340, 'próstata 09.01.01.004-9': 1015,
}


def sig(c):
    c = str(c)
    return f'0{c[0]}.{c[1:3]}.{c[3:5]}.{c[5:8]}-{c[8]}' if len(c) == 9 else c


def norm(s):
    s = unicodedata.normalize('NFD', s or '').encode('ascii', 'ignore').decode()
    return re.sub(r'\s+', ' ', s.replace('\xa0', ' ')).strip().upper()


GENERICA = re.compile(r'^CONSULTA\b.*-\s*(?:ADULTO|GERAL)\s*$|^CONSULTA EM ORTOPEDIA E TRAUMATOLOGIA$')


def grupo(fila):
    f = norm(fila)
    if 'ORTOPEDIA' in f:
        return 'consultas de ortopedia'
    if 'RISCO CIRURGICO' in f:
        return 'cardiologia: risco cirúrgico'
    if 'CARDIOLOGIA - ADULTO' in f:
        return 'cardiologia: adulto'
    if 'GINECOLOGIA' in f:
        return 'ginecologia'
    if 'OTORRINO' in f:
        return 'otorrinolaringologia'
    if f.startswith('RM '):
        return 'ressonância (02.07)'
    return f


# ---------------------------------------------------------------- filas no formato do método
def ag_por_nome(lst):
    return {a[0]: a for a in lst}


filas, nomes_internos, colisoes = {}, {}, []


def add_fila(nome, entrada):
    if nome in filas:
        colisoes.append(nome)
        nome = f'{nome} [{entrada["codigo"]}]'
    filas[nome] = entrada
    return nome


compos = {k: [] for k in KS}
for s, papel, k in (('us', 'exame', '002-0'), ('tc', 'exame', '003-8'), ('rm', 'exame', '004-6')):
    ag = ag_por_nome(m[s]['ag'])
    nomes_internos[s] = [r[0] for r in m[s]['rows']]
    for r in m[s]['rows']:
        nome, cod, fila, viva, pess, dev, med, mdn, mx, ant, f26, fk, vk = r
        a = ag.get(nome)
        cp = m['cidprinc'].get(f'{s.upper()}|{k}|{nome}', [])
        e = dict(papel=papel, codigo=sig(cod), generica=bool(GENERICA.search(norm(nome))), fila=fila, fila_viva=viva,
                 pessoas=pess, devolvidas=dev, espera_media=med, espera_mediana=mdn, espera_max=mx,
                 pedido_mais_antigo=ant, fila_pedidos_2026=f26,
                 agendadas_12m=a[2] if a else 0, agendadas_12m_iev=a[3] if a else 0,
                 recortes={ROT[k]: dict(fila=fk, fila_viva=vk, cid_principais=cp)})
        compos[k].append(add_fila(nome, e))
ag = ag_por_nome(m['rx']['ag'])
nomes_internos['rx'] = [r[0] for r in m['rx']['rows']]
for r in m['rx']['rows']:
    nome, cod, fila, viva, pess, dev, med, mdn, mx, ant, f26 = r[:11]
    a = ag.get(nome)
    rec = {}
    for i, k in enumerate(KS):
        rec[ROT[k]] = dict(fila=r[11 + 2 * i], fila_viva=r[12 + 2 * i], cid_principais=m['cidprinc'].get(f'RX|{k}|{nome}', []))
    e = dict(papel='exame', codigo=sig(cod), generica=False, fila=fila, fila_viva=viva, pessoas=pess, devolvidas=dev,
             espera_media=med, espera_mediana=mdn, espera_max=mx, pedido_mais_antigo=ant, fila_pedidos_2026=f26,
             agendadas_12m=a[2] if a else 0, agendadas_12m_iev=a[3] if a else 0, recortes=rec)
    n = add_fila(nome, e)
    for k in KS:
        compos[k].append(n)
ag = ag_por_nome(m['orto']['ag'])
nomes_internos['consultas'] = [r[0] for r in m['orto']['rows']]
for r in m['orto']['rows']:
    nome, fila, viva, pess, pessv, dev, med, mdn, mx, ant, f26 = r[:11]
    a = ag.get(nome)
    rec = {}
    for i, k in enumerate(KS):
        rec[ROT[k]] = dict(fila=r[11 + 4 * i], fila_viva=r[12 + 4 * i], pessoas=r[13 + 4 * i], pessoas_viva=r[14 + 4 * i],
                           cid_principais=m['cidprinc'].get(f'OR|{k}|{nome}', []))
    e = dict(papel='consulta', codigo='03.01.01.007-2', generica=bool(GENERICA.search(norm(nome))), fila=fila,
             fila_viva=viva, pessoas=pess, pessoas_viva=pessv, devolvidas=dev, espera_media=med, espera_mediana=mdn,
             espera_max=mx, pedido_mais_antigo=ant, fila_pedidos_2026=f26,
             agendadas_12m=a[2] if a else 0, agendadas_12m_iev=a[3] if a else 0,
             agendadas_desde_29abr2026=a[4] if a else 0, agendadas_desde_29abr2026_iev=a[5] if a else 0,
             marcadas_de_26out2026=a[6] if a else 0, marcadas_de_26out2026_iev=a[7] if a else 0,
             agendadas_29abr2025_a_28abr2026=a[9] if a else 0, recortes=rec)
    n = add_fila(nome, e)
    if fila:
        for k in KS:
            compos[k].append(n)

ocis = {}
for cod, o in OCIS.items():
    k = o['k']
    q = m['ocis'][k]
    exame = {'us': 'US de articulação 02.05.02.006-2', 'tc': 'tomografia', 'rm': 'ressonância'}.get(o['exame'])
    if 'exame_pessoas' in q and q['exame_pessoas'] > q['cons_pessoas']:
        nuc = dict(pessoas=q['exame_pessoas'], pessoas_viva=q['exame_pessoas_viva'],
                   como=f'exame obrigatório ({exame}) com o CID da ficha; a consulta de entrada tem {q["cons_pessoas"]}')
    else:
        extra = f'; o exame ({exame}) com o CID tem {q["exame_pessoas"]}' if 'exame_pessoas' in q else ''
        nuc = dict(pessoas=q['cons_pessoas'], pessoas_viva=q['cons_pessoas_viva'],
                   como=f'consulta de entrada (consultas de ortopedia) com o CID da ficha{extra}')
    teto = dict(pessoas=q['teto_pessoas'], pessoas_viva=q['teto_pessoas_viva'], fila=q['teto_fila'],
                fila_viva=q['teto_fila_viva'], espera_media=q['teto_espera_media'],
                espera_mediana=q['teto_espera_mediana'], pessoas_menores_18=q['teto_menores18'])
    ocis[cod] = dict(
        nome=f'OCI avaliação diagnóstica em ortopedia com recursos de {o["nome"]}',
        cid_aceito=m['meta']['filtros']['K'][k], cid_finalidade=m['meta']['filtros']['K'][k],
        nota_finalidade='a ficha não separa o CID da finalidade: finalidade = teto. Recorte mais estreito é decisão do usuário',
        recorte_teto=ROT[k], recorte_finalidade=ROT[k], filas=compos[k],
        teto=teto, finalidade=dict(teto), nucleo=nuc,
        sem_recorte_de_cid=dict(pessoas=q['sem_cid_pessoas'], fila=q['sem_cid_fila']),
        contratado_iev=o['contratado'])


# ---------------------------------------------------------------- alarmes (a lógica da conferência)
def tokens(expr):
    return [t.upper() for t in re.findall(r'["\']([A-Za-z0-9*]+)["\']', expr or '')]


alarmes = []
for cod, o in ocis.items():
    nt = len(tokens(o['cid_aceito']))
    cats = len({t[:3] for t in tokens(o['cid_aceito'])})
    if nt > LIM_CATEGORIAS:
        alarmes.append(dict(tipo='CID largo', oci=cod, texto=f'{nt} códigos em {cats} categorias'))
    tot = sum(filas[f]['fila'] for f in o['filas'])
    fin = sum(filas[f]['recortes'][o['recorte_finalidade']]['fila'] for f in o['filas'])
    if tot and fin / tot < LIM_RARO:
        alarmes.append(dict(tipo='CID raro', oci=cod, texto=f'{fin} de {tot} solicitações ({fin / tot:.1%})'))
    p, pv = o['finalidade']['pessoas'], o['finalidade']['pessoas_viva']
    if p and (p - pv) / p > LIM_VELHA:
        alarmes.append(dict(tipo='fila velha', oci=cod, texto=f'{p - pv} de {p}'))
    for f in o['filas']:
        if filas[f]['generica']:
            alarmes.append(dict(tipo='fila genérica', oci=cod, fila=f, texto=f'{f} na composição da {cod}'))
for f in sorted({f for o in ocis.values() for f in o['filas']}):
    d = filas[f]
    if d['fila'] and (d['agendadas_12m'] == 0 or d['fila'] / d['agendadas_12m'] > LIM_ESTOQUE):
        anos = 'sem agendamento em 12 meses' if d['agendadas_12m'] == 0 else f"{d['fila'] / d['agendadas_12m']:.1f} anos"
        alarmes.append(dict(tipo='estoque', oci=None, fila=f, texto=f"{d['fila']} na fila, {anos}"))

coleta = dict(
    metodo='2026-10-25', janela_viva_meses=24, janela_viva_desde='26/10/2024',
    fonte='Mapa Social da Saúde (MPDFT), app Qlik 7edb02fa-f1f5-4ea6-b348-049a4ac2d095',
    recarga=m['meta']['reload'], consulta=[m['meta']['inicio'], m['meta']['fim']],
    solicitacao_mais_recente=m['meta']['sol_max'], agendamento_mais_distante=m['meta']['ag_max'],
    filtro_fila=m['meta']['filtros']['FS'], filtro_devolvidas=m['meta']['filtros']['DEV'],
    filtro_viva=m['meta']['filtros']['VIVA'], filtro_agendadas_12m=m['meta']['filtros']['AG12'],
    unidades_iev=dict(filtro=m['meta']['filtros']['IEV'], unidades=IEV, certeza=CERTEZA),
    nomes_internos=nomes_internos, colisoes_de_nome=colisoes,
    filas=filas, ocis=ocis, alarmes=alarmes)
(AQUI / 'coleta_iev_20261026.json').write_text(json.dumps(coleta, ensure_ascii=False, indent=1), encoding='utf-8')

# ---------------------------------------------------------------- planilha
wb = openpyxl.Workbook()
B = Font(bold=True)
CALC = PatternFill('solid', fgColor='FFF2CC')


def aba(nome, cab, linhas, calc=False, nota=None):
    ws = wb.create_sheet(nome[:31])
    r0 = 1
    if nota:
        ws.cell(1, 1, nota).font = Font(italic=True)
        r0 = 3
    for j, c in enumerate(cab, 1):
        x = ws.cell(r0, j, c)
        x.font = B
        if calc:
            x.fill = CALC
    for i, l in enumerate(linhas, r0 + 1):
        for j, v in enumerate(l, 1):
            ws.cell(i, j, v)
    ws.freeze_panes = ws.cell(r0 + 1, 1)
    return ws


ws = wb.active
ws.title = 'Leia-me'
leia = [
    'Mapa Social da Saúde (MPDFT) — sobreposição com o IEV (Instituto Esporte e Vida), coleta de 26/10/2026',
    f'Recarga da base: 26/10/2026 16:32:44 (qLastReloadTime {m["meta"]["reload"]}); consulta: {m["meta"]["inicio"]} a {m["meta"]["fim"]}',
    f'Solicitação mais recente: {m["meta"]["sol_max"]}; agendamento mais distante: {m["meta"]["ag_max"]}',
    'Fila = três status (pendente de regulação, corrigida e reenviada, pendente por fila de espera); devolvidas à parte.',
    'Fila viva = pedidos de 26/10/2024 em diante. Agendadas 12 m = data_agendamento de 26/10/2025 a 25/10/2026.',
    'Unidades do IEV (identificação da coleta, não do painel): 0366986 Samambaia, 3031543 Sobradinho, 9180168 CIG Gama.',
    'Agendamentos "desde 29/04/2026" = data_agendamento de 29/04/2026 em diante (inclui o que está marcado até 26/11/2026).',
    'Abas com cabeçalho amarelo: números CALCULADOS (somas, proporções, comparação com o contratado), não do motor.',
    'Só contagens agregadas: nenhum CNS, CPF, nome ou data de nascimento.',
    'Fonte de cada aba: motor_iev_20261026.json (pasta mapa_social_20261026_iev_bruto/).',
]
for i, t in enumerate(leia, 1):
    ws.cell(i, 1, t)

aba('1 Unidades', ['código', 'nome no painel', 'nome no SISREG', 'tipo', 'agendamentos (todos)', 'primeiro', 'último',
                   'desde 29/04/2026', 'de 26/10/2026 em diante', 'nomes de fila', 'IEV?', 'certeza'],
    [u + ['sim' if u[0] in IEV else 'não', CERTEZA.get(u[0], '')] for u in m['unidades']])
aba('2 IEV por fila', ['unidade', 'fila (RM por código)', 'desde 29/04/2026', 'de 26/10/2026 em diante', 'antes de 29/04/2026',
                       'primeiro', 'último', 'nomes'], m['iev_filas'])
aba('3 IEV por mês', ['unidade', 'fila'] + m['iev_mes']['meses'], m['iev_mes']['linhas'])
# grupos × mês (calculado)
gm = {}
for l in m['iev_mes']['linhas']:
    g = grupo(l[1])
    gm.setdefault(g, [0] * len(m['iev_mes']['meses']))
    for i, v in enumerate(l[2:]):
        gm[g][i] += v
fut = {}
for l in m['iev_filas']:
    g = grupo(l[1])
    fut.setdefault(g, [0, 0])
    fut[g][0] += l[2]
    fut[g][1] += l[3]
aba('4 IEV grupo x mês (calc)', ['grupo'] + m['iev_mes']['meses'] + ['total desde 29/04', 'de 26/10 em diante'],
    [[g] + v + fut[g] for g, v in sorted(gm.items())], calc=True)
aba('5 IEV status', ['unidade', 'grupo', 'status do agendamento', 'agendamentos desde 29/04/2026'], m['iev_status'])
lin = []
for f, (tot, l) in m['iev_cid'].items():
    for c, n in l:
        lin.append([f, tot, c, n])
aba('6 IEV CID', ['fila', 'agendamentos desde 29/04/2026', 'categoria do CID_agendamento', 'agendamentos'], lin)
aba('7 IEV x lista da OCI', ['lista de CID', 'consultas de ortopedia no IEV com CID da lista', 'das quais realizadas'],
    [[k, *v] for k, v in m['iev_orto_cid_oci'].items()])
# contratado × agendado (calculado)
st = {}
for u, g, s, n in m['iev_status']:
    st.setdefault(g, {}).setdefault(s, 0)
    st[g][s] += n
real = {g: v.get('PROCEDIMENTO REALIZADO', 0) for g, v in st.items()}
cmp_ = [
    ['ortopedia (4 OCI, 2 convênios)', sum(o['contratado'] for o in OCIS.values()), fut['consultas de ortopedia'][0],
     fut['consultas de ortopedia'][1], real.get('ortopedia', 0)],
    ['cardiologia (3 OCI)', 4647 + 1000 + 900,
     fut['cardiologia: risco cirúrgico'][0] + fut['cardiologia: adulto'][0],
     fut['cardiologia: risco cirúrgico'][1] + fut['cardiologia: adulto'][1],
     real.get('cardio risco cirurgico', 0) + real.get('cardio adulto', 0)],
    ['saúde da mulher 09.06.01.001-2', 3218, fut['ginecologia'][0], fut['ginecologia'][1], real.get('ginecologia', 0)],
    ['déficit auditivo 09.04.01.001-5 + 002-3', 6250 + 5340, fut['otorrinolaringologia'][0], fut['otorrinolaringologia'][1],
     real.get('otorrino', 0)],
    ['próstata 09.01.01.004-9', 1015, 0, 0, 0],
]
aba('8 Contratado x agendado (calc)', ['objeto', 'contratado (OCI)', 'consultas agendadas no IEV desde 29/04',
                                       'das quais de 26/10 em diante', 'realizadas'], cmp_, calc=True,
    nota='Contratado: planos aprovados (soma dos dois convênios de ortopedia). Agendado: consultas de entrada no SISREG; '
         'os exames da OCI não aparecem como agendamento regulado.')
aba('9 Cardiologia', ['fila', 'mês', 'todas as unidades', 'unidades do IEV'], m['mes_total']['cardio'])
aba('10 Orto todas x IEV', ['mês', 'consultas de ortopedia, todas as unidades', 'unidades do IEV', '% IEV (calc)'],
    [[a, b, c, round(c / b, 3) if b else None] for a, b, c in m['mes_total']['orto']])
aba('11 Outros privados', ['unidade', 'fila'] + m['privado_outros_mes']['meses'], m['privado_outros_mes']['linhas'])
cab_e = ['nome interno', 'código', 'fila', 'fila viva', 'pessoas', 'devolvidas', 'espera média', 'mediana', 'máxima',
         'pedido mais antigo', 'pedidos de 2026 na fila', 'fila no CID da OCI', 'viva no CID', 'agendadas 12 m', 'anos de estoque (calc)']


def com_ag(s):
    ag = ag_por_nome(m[s]['ag'])
    out = []
    for r in m[s]['rows']:
        a = ag.get(r[0])
        n = a[2] if a else 0
        out.append(list(r) + [n, round(r[2] / n, 1) if n else None])
    return out


aba('12 US articulação', cab_e, com_ag('us'), nota='02.05.02.006-2, todos os nomes; CID = lista da 09.03.01.002-0')
aba('13 US CID fora', ['categoria', 'fila', 'fila viva', 'fila no CID 002-0', 'pessoas'], m['us']['cats'])
aba('14 US grupos', ['grupo de CID', 'fila', 'fila viva', 'pessoas', 'fila no CID 002-0'],
    [[g, *v] for g, v in m['us']['grupos'].items()])
cab_c = ['código', 'fila', 'fila viva', 'pessoas', 'pessoas viva', 'devolvidas', 'espera média', 'mediana', 'máxima',
         'mais antigo', 'fila no CID', 'viva no CID', 'pessoas no CID', 'pessoas viva no CID', 'média no CID',
         'mediana no CID', 'pedidos de 2026']
aba('15 RM por código', cab_c, m['rm']['porCodigo'], nota='RM compatíveis com a 09.03.01.004-6; CID = lista da 004-6')
aba('16 RM por nome', cab_e, com_ag('rm'))
aba('17 TC por código', cab_c, m['tc']['porCodigo'], nota='TC compatíveis com a 09.03.01.003-8; CID = lista da 003-8')
aba('18 TC por nome', cab_e, com_ag('tc'))
aba('19 RX por código', ['código', 'fila', 'viva', 'pessoas', 'pessoas viva', 'devolvidas', 'média', 'mediana', 'máxima',
                         'mais antigo', '2026', 'fila 001-1', 'viva 001-1', 'fila 002-0', 'viva 002-0', 'fila 003-8',
                         'viva 003-8', 'fila 004-6', 'viva 004-6'], m['rx']['porCodigo'])
cab_o = ['nome interno', 'fila', 'viva', 'pessoas', 'pessoas viva', 'devolvidas', 'média', 'mediana', 'máxima', 'mais antigo',
         '2026'] + [f'{x} {k}' for k in KS for x in ('fila', 'viva', 'pessoas', 'pessoas viva')]
aba('20 Consultas orto', cab_o, m['orto']['rows'])
aba('21 Consultas orto agenda', ['nome', 'código', 'agendadas 12 m', 'no IEV', 'desde 29/04/2026', 'no IEV',
                                 'de 26/10 em diante', 'no IEV', 'outros privados', '29/04/2025 a 28/04/2026'], m['orto']['ag'])
aba('22 Três números', ['OCI', 'teto pessoas', 'teto viva', 'finalidade', 'finalidade viva', 'núcleo', 'núcleo viva',
                        'como', 'espera média', 'mediana', 'menores de 18', 'sem recorte de CID (pessoas)', 'contratado IEV'],
    [[c, o['teto']['pessoas'], o['teto']['pessoas_viva'], o['finalidade']['pessoas'], o['finalidade']['pessoas_viva'],
      o['nucleo']['pessoas'], o['nucleo']['pessoas_viva'], o['nucleo']['como'], o['teto']['espera_media'],
      o['teto']['espera_mediana'], o['teto']['pessoas_menores_18'], o['sem_recorte_de_cid']['pessoas'], o['contratado_iev']]
     for c, o in ocis.items()])
aba('23 Região', ['Região de Saúde', 'pessoas US', 'US no CID 002-0', 'pessoas consultas', 'consultas no CID 001-1',
                  'pessoas RM', 'RM no CID 004-6', 'pessoas TC', 'TC no CID 003-8', 'união dos tetos', 'fila US',
                  'fila consultas'], [[r[0] or '(sem região)', *r[1:]] for r in m['regiao']])
lin = []
for k, v in m['varredura'].items():
    for n, c, fk, f in v['top']:
        lin.append([COD[k], v['nfilas'], v['total'], n, sig(c), fk, f])
aba('24 Varredura', ['OCI', 'filas com o CID', 'solicitações com o CID', 'fila', 'código', 'fila no CID', 'fila inteira'], lin)
aba('25 RM no IEV antes x depois', ['unidade', 'mês', 'RM', 'outras filas'], m['iev_rm_mes'])
aba('26 Alarmes (calc)', ['tipo', 'OCI', 'fila', 'texto'],
    [[a['tipo'], a.get('oci') or '', a.get('fila') or '', a['texto']] for a in alarmes], calc=True)
wb.save(AQUI.parent / 'mapa_social_20261026_iev.xlsx')

# ---------------------------------------------------------------- resumo no terminal (para o .md)
if __name__ == '__main__':
    print('colisões de nome:', colisoes)
    print('alarmes por tipo:', {t: sum(1 for a in alarmes if a['tipo'] == t) for t in sorted({a['tipo'] for a in alarmes})})
    for a in alarmes:
        if a['tipo'] != 'estoque':
            print('  ', a['tipo'], a.get('oci'), a.get('fila', ''), a['texto'])
    print('estoque (fila >= 50):')
    for a in alarmes:
        if a['tipo'] == 'estoque' and filas[a['fila']]['fila'] >= 50:
            print('  ', a['fila'], a['texto'])
    print('grupo × mês:', m['iev_mes']['meses'])
    for g, v in sorted(gm.items()):
        print('  ', g, v, fut[g])
    print('contratado × agendado:')
    for l in cmp_:
        print('  ', l)
    print('status:', {g: v for g, v in st.items()})
    for c, o in ocis.items():
        tot = sum(filas[f]['fila'] for f in o['filas'])
        fin = sum(filas[f]['recortes'][o['recorte_finalidade']]['fila'] for f in o['filas'])
        print(c, 'teto', o['teto'], 'núcleo', o['nucleo'], 'filas', len(o['filas']), 'fila comp', tot, 'no CID', fin)
