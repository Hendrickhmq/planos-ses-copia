# Monta coleta_20261026.json (o JSON da coleta no formato do método de 25/10/2026) e
# ../mapa_social_20261026.xlsx a partir de motor_20261026.json (saída do motor do painel Mapa Social
# da Saúde, base recarregada em 26/10/2026 16:32:44) e de anterior_20261015_resumo.json (a coleta
# de 15/10/2026, para a diferença).
# Uso: python3 ler_motor_20261026.py && python3 montar_20261026.py   (de qualquer pasta)
# O que este script calcula (e a planilha marca "calculado"): anos de estoque (fila ÷ agendadas em
# 12 meses), a parte da fila de antes da janela viva, as somas por grupo de CID da mamografia, os %
# de região e a diferença para 15/10. A decisão de cada fila é a função decidir(): regra escrita a
# partir das decisões do usuário de 15 a 20/10/2026 (dados/estudo_das_filas.md do redacao_07), não
# dado do motor. Só contagens agregadas: nenhum CNS, CPF, nome ou data de nascimento.
import json
import re
import unicodedata
from pathlib import Path

import openpyxl
from openpyxl.styles import Font, PatternFill

AQUI = Path(__file__).resolve().parent
m = json.loads((AQUI / 'motor_20261026.json').read_text(encoding='utf-8'))
ant = json.loads((AQUI / 'anterior_20261015_resumo.json').read_text(encoding='utf-8'))
comp = json.loads((AQUI / 'motor_complementar_20261026.json').read_text(encoding='utf-8'))

LIM_VELHA, LIM_ESTOQUE = 0.30, 3   # limites do método (propostos em 25/10/2026)


def sig(c):
    c = str(c)
    return f'0{c[0]}.{c[1:3]}.{c[3:5]}.{c[5:8]}-{c[8]}' if len(c) == 9 else c + ' (malformado)'


def norm(s):
    s = unicodedata.normalize('NFD', s or '').encode('ascii', 'ignore').decode()
    return re.sub(r'\s+', ' ', s.replace('\xa0', ' ')).strip().upper()


def vis(s):
    return s.replace('\xa0', '[NBSP]')


CARTEIRA = ['204030188', '204060028', '205020160', '205020070', '205020089', '205020178', '205020143', '205020151',
            '206010052', '206010079', '206010044', '206010060']
RESERVA = {'204030188', '204060028'}
VOLTAM = {  # saíram ou ficaram de fora em 15–20/10/2026 e podem voltar (pedido de 26/10/2026)
    '205010032': 'ecocardiografia transtorácica: fora em 15/10 (usuário), está na OCI de cardiologia do IEV (09.02.01.006-9)',
    '205020062': 'US de articulação: fora em 15 e 16/10 (usuário), está nas OCI de ortopedia do IEV',
    '205020119': 'US de próstata transretal: no rol, fila pequena (usuário, 20/10)',
    '205020135': 'US de tórax extracardíaca: no rol, fila pequena (usuário, 20/10)',
    '205010059': 'doppler de fluxo obstétrico: no rol, fila pequena (usuário, 20/10)',
    '205020224': 'elastografia hepática: no rol, sem fila',
    '206010010': 'TC de coluna cervical: entrou em 19/10 e saiu em 20/10 (OCI de ortopedia 09.03.01.003-8 do IEV)',
    '206010036': 'TC de coluna torácica: entrou em 19/10 e saiu em 20/10 (OCI de ortopedia do IEV)',
    '206010028': 'TC de coluna lombo-sacra: entrou em 19/10 e saiu em 20/10 (OCI de ortopedia do IEV)',
    '206020023': 'TC de segmentos apendiculares: entrou em 19/10 e saiu em 20/10 (OCI de ortopedia do IEV)',
    '206020015': 'TC de articulações de membro superior: fora em 15/10 (OCI de ortopedia do IEV)',
    '206030029': 'TC de articulações de membro inferior: fora em 15/10 (OCI de ortopedia do IEV)',
}
P4C = set(ant['plano4_codigos'])
P4N = set(ant['plano4_nomes_sisreg'])
# rol de imagem do Anexo I da Portaria SAES/MS 4.282/2026 (redacao_07, dados/valor_unitario.md)
ROL = set('''204030188 204060028 205010032 205010040 205010059 205020038 205020046 205020054 205020062 205020070
205020089 205020097 205020100 205020119 205020127 205020135 205020143 205020151 205020160 205020178 205020186
205020224 206010010 206010028 206010036 206010044 206010052 206010060 206010079 206020015 206020023 206020031
206030010 206030029 206030037 207010013 207010021 207010030 207010048 207010056 207010064 207010072 207020019
207020027 207020035 207020060 207030014 207030022 207030030 207030049 207030057'''.split())
DESTAQUE = CARTEIRA + list(VOLTAM) + sorted(c[0] for c in m['codigos'] if c[0].startswith('207') and c[2] > 0) + sorted(P4C)
GENERICA = re.compile(r'ECOCARDIOGRAFIA(?!.*(ESTRESSE|TRANSE))|^TORAX : PA E PERFIL$')

FC = {c: i for i, c in enumerate(m['filas_cols'])}
CC = {c: i for i, c in enumerate(m['codigos_cols'])}
GC = {c: i for i, c in enumerate(m['grupos_cols'])}
cod = {r[0]: r for r in m['codigos']}


def decidir(nome, c, f):
    """A decisão de cada fila: regra escrita a partir das decisões do usuário de 15 a 20/10/2026."""
    n = norm(nome)
    residuo = f[FC['solicitacoes_2026_todos_status']] == 0 and f[FC['agendadas_2026']] == 0
    if nome in P4N:
        return 'fica fora', 'enquadramento do plano 4 (ISHP, R$ 11,5 mi): só marca a sobreposição'
    if residuo:
        return 'fica fora', 'resíduo: nenhum pedido nem agendamento em 2026'
    if c in P4C:
        sub = 'emergência' if 'EMERG' in n else 'angiotomografia' if 'ANGIOTOMO' in n else 'outro nome'
        return 'fica fora', f'mesmo código do plano 4, fora do enquadramento ({sub}): risco de sobreposição (usuário, 16/10/2026)'
    if c in CARTEIRA:
        if 'EMERG' in n:
            return 'a decidir', 'fila de emergência (pronto-atendimento) com o código da carteira'
        if 'ANGIOTOMO' in n:
            return 'a decidir', 'angiotomografia registrada no código da carteira'
        if 'CONE BEAN' in n:
            return 'a decidir', 'tomografia cone beam (odontológica) registrada no código da TC de face'
        if 'DIAGNOSTICA' in n and c == '204030188':
            return 'a decidir', 'mamografia diagnóstica pedida no código de rastreamento'
        if c in RESERVA:
            return 'entra', 'carteira do pré-plano, reserva (usuário, 20/10/2026)'
        return 'entra', 'carteira do pré-plano (usuário, 16, 19 e 20/10/2026)'
    if c in VOLTAM:
        return 'a decidir', 'reaberta em 26/10/2026; antes, ' + VOLTAM[c]
    if c.startswith('207'):
        return 'a decidir', 'ressonância na tabela de destaque de 26/10/2026; em 16/10: fora, a rede já cuida (usuário)'
    if c.startswith('208'):
        return 'fica fora', 'cintilografia: complexa de executar, CNEN e radiofármaco (usuário, 16/10/2026)'
    if c not in ROL:
        return 'fica fora', 'fora do rol da Portaria 4.282: sem incremento, paga só a Tabela (estudo, 15/10/2026)'
    return 'a decidir', 'no rol da Portaria 4.282, fora da carteira'


def estoque(fila, ag):
    if not fila:
        return None
    return None if not ag else round(fila / ag, 2)


def alarmes_de(nome, fila, viva, ag, mais_antiga):
    out = []
    if fila and (ag == 0 or (ag and fila / ag > LIM_ESTOQUE)):
        out.append(['estoque', f'{fila} na fila, ' + ('sem agendamento em 12 meses' if ag == 0 else f'{fila / ag:.1f} anos de agendamentos ({ag} em 12 meses)')])
    if fila and viva is not None and (fila - viva) / fila > LIM_VELHA:
        out.append(['fila velha', f'{fila - viva} de {fila} pedidos ({(fila - viva) / fila:.0%}) de antes de 26/10/2024; o mais antigo é de {mais_antiga}'])
    return out


# ---- filas (formato do método)
filas, nomes_internos, alarmes = {}, {}, []
grupo_de = {}
for g in m['grupos']:
    for n in g[GC['nomes_sisreg']]:
        grupo_de[(n, g[GC['codigo_sigtap']])] = g[GC['grupo']]
for f in m['filas']:
    nome, c = f[FC['nome_sisreg']], f[FC['codigo_sigtap']]
    chave = nome if nome not in filas else f'{nome} [{sig(c)}]'
    dec, motivo = decidir(nome, c, f)
    fila, viva, ag = f[FC['fila']], f[FC['fila_viva']], f[FC['agendadas_12m']]
    al = alarmes_de(nome, fila, viva, ag, f[FC['mais_antiga']])
    for t, txt in al:
        alarmes.append({'tipo': t, 'fila': chave, 'codigo_sigtap': sig(c), 'texto': f'{chave} ({sig(c)}): {txt}', 'destaque': c in DESTAQUE})
    filas[chave] = {
        'papel': 'exame', 'generica': bool(GENERICA.search(norm(nome))), 'codigo_sigtap': sig(c),
        'grupo': grupo_de.get((nome, c)),
        'fila': fila, 'fila_viva': viva, 'pessoas': f[FC['pessoas']], 'pessoas_viva': f[FC['pessoas_viva']],
        'devolvidas': f[FC['devolvidas']], 'espera_media': f[FC['espera_media']], 'espera_mediana': f[FC['espera_mediana']],
        'espera_max': f[FC['espera_max']], 'mais_antiga': f[FC['mais_antiga']], 'fila_solicitada_2026': f[FC['fila_solicitada_2026']],
        'idade_mediana': f[FC['idade_mediana']], 'total_todos_status': f[FC['total_todos_status']],
        'primeira_solicitacao_na_base': f[FC['primeira_solicitacao_na_base']],
        'agendadas_12m': ag, 'agendadas_2026': f[FC['agendadas_2026']], 'agendadas_todos_os_anos': f[FC['agendadas_todos_os_anos']],
        'anos_estoque_calculado': estoque(fila, ag),
        'decisao': dec, 'motivo': motivo, 'alarmes': [a[0] for a in al],
        'recortes': {'sem recorte': {'fila': fila, 'fila_viva': viva, 'pessoas': f[FC['pessoas']],
                                     'cid_principais': f[FC['cid_principais']]}},
    }
    nomes_internos[chave] = {'nome_sisreg': nome, 'nome_sisreg_agendamento': nome, 'codigo_sigtap': sig(c)}

# ---- por código e por grupo
reg = m['regiao_codigos']
FORA_REG = {'URD', 'Contratado/Credenciado', 'Serviços Centralizados', 'Público - Não SES', '-'}


def resumo_regiao(lista):
    tot = sum(x[1] for x in lista)
    sem = sum(x[1] for x in lista if x[0] == '-')
    ref = sum(x[1] for x in lista if x[0] in ('URD', 'Contratado/Credenciado'))
    return tot, sem, ref


por_codigo = {}
for r in m['codigos']:
    c = r[0]
    if not (r[CC['fila']] or r[CC['agendadas_12m']]):
        continue
    fila, viva, ag = r[CC['fila']], r[CC['fila_viva']], r[CC['agendadas_12m']]
    por_codigo[sig(c)] = {
        'descricao_sigtap': r[CC['descricao_sigtap']], 'nomes_com_fila': r[CC['nomes_com_fila']],
        'fila': fila, 'fila_viva': viva, 'pessoas': r[CC['pessoas']], 'pessoas_viva': r[CC['pessoas_viva']],
        'devolvidas': r[CC['devolvidas']], 'espera_media': r[CC['espera_media']], 'espera_mediana': r[CC['espera_mediana']],
        'espera_max': r[CC['espera_max']], 'mais_antiga': r[CC['mais_antiga']], 'fila_solicitada_2026': r[CC['fila_solicitada_2026']],
        'idade_mediana': r[CC['idade_mediana']], 'agendadas_12m': ag, 'agendadas_2026': r[CC['agendadas_2026']],
        'anos_estoque_calculado': estoque(fila, ag), 'regiao': reg.get(c, []),
        'destaque': c in DESTAQUE, 'alarmes': [a[0] for a in alarmes_de(c, fila, viva, ag, r[CC['mais_antiga']])],
    }
grupos = []
for g in m['grupos']:
    fila, viva, ag = g[GC['fila']], g[GC['fila_viva']], g[GC['agendadas_12m_pelos_nomes']]
    grupos.append({
        'codigo_sigtap': sig(g[GC['codigo_sigtap']]), 'grupo': g[GC['grupo']], 'nomes_sisreg': g[GC['nomes_sisreg']],
        'fila': fila, 'fila_viva': viva, 'pessoas': g[GC['pessoas']], 'pessoas_viva': g[GC['pessoas_viva']],
        'devolvidas': g[GC['devolvidas']], 'espera_media': g[GC['espera_media']], 'espera_mediana': g[GC['espera_mediana']],
        'espera_max': g[GC['espera_max']], 'mais_antiga': g[GC['mais_antiga']], 'fila_solicitada_2026': g[GC['fila_solicitada_2026']],
        'idade_mediana': g[GC['idade_mediana']], 'agendadas_12m_pelos_nomes': ag, 'anos_estoque_calculado': estoque(fila, ag),
        'regiao': m['regiao_grupos'].get(str(g[GC['indice']]), []),
        'alarmes': [a[0] for a in alarmes_de(g[GC['grupo']], fila, viva, ag, g[GC['mais_antiga']])],
    })

# ---- mamografia: CID por grupo (calculado)
def grupo_cid(cid):
    c = cid.upper()
    if c.startswith('Z12'):
        return 'rastreamento de neoplasia (Z12)'
    if c[:3] in ('Z00', 'Z01', 'Z10', 'Z13'):
        return 'exame geral ou de rotina (Z00, Z01, Z10, Z13)'
    if c[:3] in ('Z80', 'Z85', 'Z08'):
        return 'história de câncer ou seguimento (Z80, Z85, Z08)'
    if c[:3] in ('N60', 'N61', 'N62', 'N63', 'N64', 'R92', 'D24', 'D48', 'N65'):
        return 'queixa ou achado mamário (N60–N64, R92, D24, D48)'
    if c[:3] in ('C50', 'D05'):
        return 'câncer de mama (C50, D05)'
    if c[:3] == 'N95':
        return 'climatério (N95)'
    return 'outros'


mamo = {}
for nome, cid, fila, viva in m['mamografia_cid']:
    k = (nome, grupo_cid(cid))
    a = mamo.setdefault(k, [0, 0])
    a[0] += fila
    a[1] += viva

# ---- diferença para 15/10/2026 (calculado)
AF = {c: i for i, c in enumerate(ant['filas_15_10_cols'])}
old_cod, old_nome = {}, {}
for f in ant['filas_15_10']:
    c = f[AF['codigo_sigtap']]
    a = old_cod.setdefault(c, [0, 0.0, 0])
    a[0] += f[AF['fila']]
    a[1] += f[AF['fila']] * (f[AF['espera_media']] or 0)
    a[2] += 1
    old_nome[(f[AF['nome_sisreg']], c)] = f
diferenca = {'nota': ('fila e espera média por código e por recorte, 15/10/2026 (recarga 19:32:31) e 26/10/2026 (recarga 16:32:44). '
                      'A espera média de 15/10 por código é a média das filas do código ponderada pela fila (exata: cada pedido '
                      'tem um nome de fila só); a de 26/10 sai do motor. CALCULADO.'), 'codigos': {}, 'recortes': {}}
for c in DESTAQUE:
    o = old_cod.get(c)
    r = cod.get(c)
    nf = r[CC['fila']] if r else 0
    ne = r[CC['espera_media']] if r else None
    of = o[0] if o else 0
    oe = round(o[1] / o[0], 1) if o and o[0] else None
    diferenca['codigos'][sig(c)] = {'fila_15_10': of, 'fila_26_10': nf, 'delta': nf - of,
                                    'espera_media_15_10': oe, 'espera_media_26_10': ne,
                                    'delta_espera': None if oe is None or ne is None else round(ne - oe, 1)}
for g in grupos:
    c = g['codigo_sigtap'].replace('.', '').replace('-', '').lstrip('0')
    of, oe = 0, 0.0
    for n in g['nomes_sisreg']:
        o = old_nome.get((n, c))
        if o:
            of += o[AF['fila']]
            oe += o[AF['fila']] * (o[AF['espera_media']] or 0)
    diferenca['recortes'][f"{g['codigo_sigtap']} | {g['grupo']}"] = {
        'fila_15_10': of, 'fila_26_10': g['fila'], 'delta': g['fila'] - of,
        'espera_media_15_10': round(oe / of, 1) if of else None, 'espera_media_26_10': g['espera_media']}

# ---- varredura: contagem por decisão
varr = {}
for k, v in filas.items():
    a = varr.setdefault(v['decisao'], [0, 0])
    a[0] += 1
    a[1] += v['fila']

coleta = {
    'metodo': '2026-10-25', 'janela_viva_meses': 24,
    'objeto': ('exames de imagem avulsos (não OCI) do pré-plano redacao_07, Emenda de Bancada 71080005, ISHP: sem recorte de CID; '
               'a fila do exame inteira e a fila viva ao lado'),
    **{k: m[k] for k in ('app', 'titulo_app', 'painel', 'recarga_utc', 'recarga_brasilia', 'recarga_conferida_no_fim',
                         'consulta_inicio', 'consulta_fim', 'max_data_solicitacao', 'max_data_agendamento',
                         'min_data_solicitacao', 'leitura_descartada', 'filtro_fila', 'filtro_devolvidas', 'janelas',
                         'universo', 'nota_medidas')},
    'limites_alarmes': {'fila velha': 'mais de 30% da fila com pedido de antes da janela viva',
                        'estoque': 'fila ÷ agendadas em 12 meses > 3, ou nenhuma agendada em 12 meses'},
    'nomes_internos': nomes_internos,
    'filas': filas,
    'ocis': {},
    'carteira': CARTEIRA, 'reabertura': VOLTAM, 'plano4_codigos': sorted(P4C), 'plano4_nomes_sisreg': sorted(P4N),
    'destaque_codigos': [sig(c) for c in DESTAQUE],
    'por_codigo': por_codigo,
    'recortes_por_nome': grupos,
    'idade_cols': m['idade_cols'], 'idade': m['idade'],
    'mamografia_cid_por_grupo_calculado': [[n, g, v[0], v[1]] for (n, g), v in sorted(mamo.items(), key=lambda x: (x[0][0], -x[1][0]))],
    'mamografia_cid': m['mamografia_cid'],
    'carteira_uniao': m['carteira'], 'carteira_uniao_cols': m['carteira_cols'],
    'fora_dos_subgrupos': m['fora_dos_subgrupos'], 'fora_dos_subgrupos_cols': m['fora_dos_subgrupos_cols'],
    'fora_dos_subgrupos_complementar': comp,
    'so_agendamento_por_codigo': m['so_agendamento_por_codigo'],
    'por_ano': m['por_ano'], 'totais': m['totais'],
    'varredura': {'nota': 'decisão de cada fila pela função decidir() do montar_20261026.py', 'por_decisao': varr},
    'alarmes': alarmes,
    'diferenca_20261015': diferenca,
}
(AQUI / 'coleta_20261026.json').write_text(json.dumps(coleta, ensure_ascii=False, indent=1), encoding='utf-8')

# ---- planilha
wb = openpyxl.Workbook()
wb.remove(wb.active)
B = Font(bold=True)
HF = PatternFill('solid', fgColor='DDEBF7')


def aba(titulo, linhas, cab=(1,)):
    ws = wb.create_sheet(titulo[:31])
    for r in linhas:
        ws.append([vis(x) if isinstance(x, str) else x for x in r])
    for i in cab:
        for c in ws[i]:
            c.font = B
            c.fill = HF
    for col in ws.columns:
        ws.column_dimensions[col[0].column_letter].width = min(70, max(9, max(len(str(c.value or '')) for c in col) * 0.9))
    ws.freeze_panes = 'A2' if cab == (1,) else None
    return ws


aba('0 · Leia-me', [
    ['Mapa Social da Saúde — filas de exames de imagem (subgrupos SIGTAP 02.04 a 02.08 e 02.10), coleta de 26/10/2026'],
    ['Para quê', 'reabrir a carteira de exames de imagem do pré-plano redacao_07 (Emenda de Bancada 71080005, ISHP, R$ 1.502.687,00)'],
    ['Painel', 'Mapa Social da Saúde – Regulamentação (MPDFT) · Lista de Espera – Exames e Consultas'],
    ['Endereço', m['painel']],
    ['App Qlik', m['titulo_app'] + ' · ' + m['app']],
    ['Dados', 'SISREG/DATASUS'],
    ['Última recarga da base', m['recarga_brasilia'] + ' (Brasília) — qLastReloadTime ' + m['recarga_utc'] + ', conferida no fim: ' + m['recarga_conferida_no_fim']],
    ['Consulta', m['consulta_inicio'] + ' a ' + m['consulta_fim'] + ' (relógio do motor)'],
    ['Leitura descartada', m['leitura_descartada']],
    ['Solicitação mais recente na base', m['max_data_solicitacao'] + ' (agendamento mais distante: ' + m['max_data_agendamento'] + ')'],
    ['Medida', 'fila = os três status (pendente de regulação, corrigida e reenviada para regulação, pendente de regulação por fila de espera); devolvidas fora, contadas à parte'],
    ['Fila viva', m['janelas']['viva 24 meses'] + ' — só os pedidos dos últimos 24 meses, contados da solicitação mais recente'],
    ['Agendadas 12 meses', m['janelas']['agendadas 12 meses'] + ' — data do atendimento agendado, todos os status do agendamento'],
    ['Anos de estoque', 'fila ÷ agendadas em 12 meses (CALCULADO)'],
    ['Universo', m['universo']],
    ['Medidas', m['nota_medidas']],
    ['Decisão', 'regra escrita (decidir() em montar_20261026.py) a partir das decisões do usuário de 15 a 20/10/2026; não é dado do motor'],
    ['Privacidade', 'só contagens agregadas; nenhum CNS, CPF, nome ou data de nascimento'],
    [],
    ['Aba', 'Conteúdo'],
    ['1 · Destaque', 'os códigos da tabela de destaque, um por linha, com a decisão e os alarmes'],
    ['2 · Recortes', 'dentro do código, por nome de fila: eco adulto e infantil, articulação por região, plano 4 enquadramento e fora, TC eletiva, emergência e angiotomografia, mamografia'],
    ['3 · Mamografia CID', 'mamografia 02.04.03.018-8: CID por nome de fila, um a um e somados por grupo (grupo CALCULADO)'],
    ['4 · Idade', 'as fichas que restringem a idade: mamografia 35+, transfontanela 0–4, obstétricas 8–60'],
    ['5 · Região por código', 'Região de Saúde da unidade solicitante, fila e pessoas, todos os códigos com fila'],
    ['6 · Região por recorte', 'Região de Saúde, fila, por recorte'],
    ['7 · Varredura', 'as 684 filas (nome × código) com gente esperando, o estudo e a decisão'],
    ['8 · Por código', 'todos os códigos do universo, com fila ou agendamento'],
    ['9 · Alarmes', 'estoque e fila velha, fila a fila (limites do método)'],
    ['10 · Diferença 15-10', 'fila e espera média, 15/10 e 26/10, por código e por recorte (CALCULADO)'],
    ['11 · Fora dos subgrupos', 'filas com nome de imagem e código fora de 02.04 a 02.10'],
    ['12 · Só agendamento', 'nomes de fila que só aparecem na tabela de agendamentos, por código'],
], cab=(1, 20))

cab = ['código', 'procedimento (SIGTAP)', 'papel na coleta', 'nomes com fila', 'fila', 'fila viva', 'pessoas', 'pessoas viva',
       'devolvidas', 'espera média', 'mediana', 'máxima', 'pedido mais antigo', 'pedidos de 2026 na fila', 'agendadas 12 m',
       'anos de estoque (calc.)', 'alarmes', 'sem região', 'URD + contratado', 'idade mediana']
lin = [cab]
for c in DESTAQUE:
    p = por_codigo.get(sig(c))
    papel = 'carteira' if c in CARTEIRA else 'pode voltar' if c in VOLTAM else 'plano 4 (sobreposição)' if c in P4C else 'ressonância'
    if not p:
        lin.append([sig(c), '(sem fila nem agendamento na base)', papel])
        continue
    t, sem, ref = resumo_regiao([[x[0], x[1]] for x in p['regiao']])
    lin.append([sig(c), p['descricao_sigtap'], papel, p['nomes_com_fila'], p['fila'], p['fila_viva'], p['pessoas'], p['pessoas_viva'],
                p['devolvidas'], p['espera_media'], p['espera_mediana'], p['espera_max'], p['mais_antiga'], p['fila_solicitada_2026'],
                p['agendadas_12m'], p['anos_estoque_calculado'], ', '.join(p['alarmes']), sem, ref, p['idade_mediana']])
aba('1 · Destaque', lin)

lin = [['código', 'recorte', 'nomes de fila', 'fila', 'fila viva', 'pessoas', 'pessoas viva', 'devolvidas', 'espera média', 'mediana',
        'máxima', 'pedido mais antigo', 'pedidos de 2026', 'idade mediana', 'agendadas 12 m (pelos nomes)', 'anos de estoque (calc.)', 'alarmes']]
for g in grupos:
    lin.append([g['codigo_sigtap'], g['grupo'], ' · '.join(g['nomes_sisreg']), g['fila'], g['fila_viva'], g['pessoas'], g['pessoas_viva'],
                g['devolvidas'], g['espera_media'], g['espera_mediana'], g['espera_max'], g['mais_antiga'], g['fila_solicitada_2026'],
                g['idade_mediana'], g['agendadas_12m_pelos_nomes'], g['anos_estoque_calculado'], ', '.join(g['alarmes'])])
aba('2 · Recortes', lin)

lin = [['nome de fila', 'CID solicitado', 'fila', 'fila viva', 'grupo de CID (calculado)']]
for nome, cid, fila, viva in sorted(m['mamografia_cid'], key=lambda x: (x[0], -x[2])):
    lin.append([nome, cid, fila, viva, grupo_cid(cid)])
lin += [[], ['nome de fila', 'grupo de CID (calculado)', 'fila', 'fila viva']]
for n, g, f, v in coleta['mamografia_cid_por_grupo_calculado']:
    lin.append([n, g, f, v])
aba('3 · Mamografia CID', lin)

lin = [['código', 'idade mínima da ficha', 'idade máxima', 'nome de fila', 'fila', 'na idade da ficha', 'abaixo', 'acima',
        'pessoas na idade', 'fila viva na idade', '50 a 69 anos', '40 a 49', '70 ou mais']]
for r in m['idade']:
    lin.append([sig(r[0])] + r[1:])
aba('4 · Idade', lin)

lin = [['código', 'procedimento', 'Região de Saúde (unidade solicitante)', 'fila', 'pessoas']]
for c in sorted(reg):
    for rr in reg[c]:
        lin.append([sig(c), cod[c][1] if c in cod else '', rr[0] if rr[0] != '-' else '(sem região informada)', rr[1], rr[2]])
aba('5 · Região por código', lin)

lin = [['código', 'recorte', 'Região de Saúde', 'fila']]
for g in grupos:
    for rr in g['regiao']:
        lin.append([g['codigo_sigtap'], g['grupo'], rr[0] if rr[0] != '-' else '(sem região informada)', rr[1]])
aba('6 · Região por recorte', lin)

lin = [['nome interno (exato; [NBSP] = U+00A0)', 'código', 'recorte', 'decisão', 'motivo', 'fila', 'fila viva', 'pessoas', 'devolvidas',
        'espera média', 'mediana', 'máxima', 'pedido mais antigo', 'pedidos de 2026', 'idade mediana', 'agendadas 12 m',
        'anos de estoque (calc.)', 'alarmes', 'genérica', '1ª solicitação na base', 'CID principais (categoria)']]
for k, v in sorted(filas.items(), key=lambda x: (x[1]['codigo_sigtap'], -x[1]['fila'])):
    lin.append([k, v['codigo_sigtap'], v['grupo'], v['decisao'], v['motivo'], v['fila'], v['fila_viva'], v['pessoas'], v['devolvidas'],
                v['espera_media'], v['espera_mediana'], v['espera_max'], v['mais_antiga'], v['fila_solicitada_2026'], v['idade_mediana'],
                v['agendadas_12m'], v['anos_estoque_calculado'], ', '.join(v['alarmes']), 'sim' if v['generica'] else '',
                v['primeira_solicitacao_na_base'], '; '.join(f'{a} {b}' for a, b in v['recortes']['sem recorte']['cid_principais'])])
aba('7 · Varredura', lin)

lin = [['código', 'procedimento (SIGTAP)', 'nomes com fila', 'fila', 'fila viva', 'pessoas', 'pessoas viva', 'devolvidas', 'espera média',
        'mediana', 'máxima', 'pedido mais antigo', 'pedidos de 2026', 'idade mediana', 'agendadas 12 m', 'agendadas 2026',
        'anos de estoque (calc.)', 'destaque', 'alarmes']]
for k, p in sorted(por_codigo.items()):
    lin.append([k, p['descricao_sigtap'], p['nomes_com_fila'], p['fila'], p['fila_viva'], p['pessoas'], p['pessoas_viva'], p['devolvidas'],
                p['espera_media'], p['espera_mediana'], p['espera_max'], p['mais_antiga'], p['fila_solicitada_2026'], p['idade_mediana'],
                p['agendadas_12m'], p['agendadas_2026'], p['anos_estoque_calculado'], 'sim' if p['destaque'] else '', ', '.join(p['alarmes'])])
aba('8 · Por código', lin)

lin = [['alarme', 'fila (nome interno)', 'código', 'na tabela de destaque', 'texto']]
for a in alarmes:
    lin.append([a['tipo'], a['fila'], a['codigo_sigtap'], 'sim' if a['destaque'] else '', a['texto']])
aba('9 · Alarmes', lin)

lin = [['código', 'recorte', 'fila 15/10', 'fila 26/10', 'Δ fila (calc.)', 'espera média 15/10 (calc.)', 'espera média 26/10', 'Δ espera (calc.)']]
for k, v in diferenca['codigos'].items():
    lin.append([k, '(código inteiro)', v['fila_15_10'], v['fila_26_10'], v['delta'], v['espera_media_15_10'], v['espera_media_26_10'], v['delta_espera']])
for k, v in diferenca['recortes'].items():
    c, g = k.split(' | ')
    de = None if v['espera_media_15_10'] is None or v['espera_media_26_10'] is None else round(v['espera_media_26_10'] - v['espera_media_15_10'], 1)
    lin.append([c, g, v['fila_15_10'], v['fila_26_10'], v['delta'], v['espera_media_15_10'], v['espera_media_26_10'], de])
aba('10 · Diferença 15-10', lin)

lin = [m['fora_dos_subgrupos_cols']]
for r in m['fora_dos_subgrupos']:
    lin.append(r)
lin += [[], ['medida complementar: ' + comp['nota']], comp['cols']]
for r in comp['filas']:
    lin.append(r)
aba('11 · Fora dos subgrupos', lin)

lin = [m['so_agendamento_por_codigo_cols']]
for r in m['so_agendamento_por_codigo']:
    lin.append([sig(r[0])] + r[1:])
aba('12 · Só agendamento', lin)

saida = AQUI.parent / 'mapa_social_20261026.xlsx'
wb.save(saida)
print('filas', len(filas), '| alarmes', len(alarmes), '| destaque', len(DESTAQUE), '| por decisão', varr, '|', saida.name)
