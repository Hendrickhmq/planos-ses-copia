# Monta ../mapa_social_20261022.xlsx a partir de coleta_20261022.json (saída da Qlik Engine
# API do painel Mapa Social da Saúde, MPDFT). Primeira coleta do redacao_08 (OCI de
# Cardiologia): não há coleta anterior para comparar.
# Uso: python3 montar_20261022.py   (de dentro desta pasta)
import json
from datetime import date, timedelta
from pathlib import Path
import openpyxl
from openpyxl.styles import Font, PatternFill

AQUI = Path(__file__).resolve().parent
j = json.loads((AQUI / 'coleta_20261022.json').read_text(encoding='utf-8'))
dia = lambda s: '' if s in (None, '') else (date(1899, 12, 30) + timedelta(days=int(s))).strftime('%d/%m/%Y')
r0 = lambda x: None if x is None or x == '' else round(x)

CIDL = {'NONE': 'sem recorte', 'I': 'I00–I99 (I*)', 'ISC': 'I20–I25', 'ZAV': 'Z136, Z848',
        'ZPO': 'Z018, Z488, Z489', 'ZAMB': 'Z13, Z84, Z01, Z48 (só a categoria, 3 caracteres)'}
NOME = {v['nome_sisreg']: k for k, v in j['nomes_internos'].items() if v['nome_sisreg']}

wb = openpyxl.Workbook(); wb.remove(wb.active)
B = Font(bold=True); HF = PatternFill('solid', fgColor='DDEBF7')


def aba(titulo, linhas, cab=()):
    ws = wb.create_sheet(titulo)
    for r in linhas:
        ws.append([('' if c is None else c) for c in r])
    for i in cab:
        for c in ws[i]:
            c.font = B; c.fill = HF
    for col in ws.columns:
        ws.column_dimensions[col[0].column_letter].width = min(70, max(9, max(len(str(c.value or '')) for c in col) * 0.9))
    return ws


aba('0 · Leia-me', [
    ['Mapa Social da Saúde — fila das sete OCI de cardiologia (09.02.01), redacao_08 (Instituto Fazer o Bem, Faz Bem). Primeira coleta.'],
    ['Painel', 'Mapa Social da Saúde – Regulamentação (MPDFT) · Lista de Espera – Exames e Consultas'],
    ['Endereço', 'https://paineis-ext.mpdft.mp.br/extensions/mapasauderegulamentacao/mapasauderegulamentacao.html'],
    ['App Qlik', j['titulo_app'] + ' · ' + j['app']],
    ['Fonte declarada', 'SISREG/DATASUS'],
    ['Última recarga da base', '22/10/2026 08:32:12 (Brasília) — qLastReloadTime ' + j['recarga_utc']],
    ['Consulta', '22/10/2026, de 09:06 a ' + j['consulta'][11:16] + ' (relógio do motor)'],
    ['Solicitação mais recente na base', j['max_data_solicitacao']],
    ['Agendamento mais distante na base', j['max_data_agendamento']],
    ['Extração', 'Qlik Engine API do próprio painel (evaluateEx e hipercubos de sessão), pelo navegador embutido. Sem leitura de tela, sem exportar pelos ícones.'],
    ['Medida "fila"', 'Count(Distinct {1<' + j['filtro_fila'] + ', fila, CID>} contador_solicitacao). Devolvidas fora, contadas à parte.'],
    ['Devolvidas', j['filtro_devolvidas']],
    ['Pessoas', 'Count(Distinct {mesmo conjunto da fila} cns_usuario_solicitacao) — só a contagem sai do motor'],
    ['Recorte das OCI', 'CID da solicitação (codigo_cid_solicitado) contra a ficha do SIGTAP 10/2026: ' + '; '.join(f'{k}: {v}' for k, v in j['recorte_cid'].items())],
    ['Recorte nos agendamentos', '; '.join(f'{k}: {v}' for k, v in j['recorte_cid_agendamento'].items())],
    ['Recorte de tempo', 'fila: todos os anos. Agendadas: data do agendamento de 22/10/2025 a 21/10/2026 ("12 meses"); 29/04/2026 a 21/10/2026 (desde o início do convênio 030977/2026 do IEV); a partir de 22/10/2026 (já marcadas)'],
    ['Enquadramento', 'OCI → filas de exame da composição e filas de consulta que entram: ' + ' · '.join(f"{k}: exames {'+'.join(v['ex'])}, consultas {'+'.join(v['co'])}" for k, v in j['enquadramento'].items())],
    ['Grafia', 'CONSULTA  EM CARDIOLOGIA - PEDIATRIA e ANGIOTOMOGRAFIA  DAS ARTÉRIAS CORONARIAS têm espaço duplo; "TESTE DE ESFORCO OU TESTE ERGOMETRICO 2" termina em " 2"; as filas de eco começam pelo número ("1. ", "2. ", "5. "). O JSON guarda o texto exato.'],
    ['Regra', 'Todas as abas trazem números do motor, sem conta. Nenhuma soma de linhas foi feita aqui: os totais de conjunto e de união vêm do motor.'],
    ['Brutos e script', 'mapa_social_20261022_bruto/ (coleta_20261022.json, montar_20261022.py)'],
], [1])

# 1 · Filas, fila a fila, em cada recorte
hd = ['recorte CID', 'chave', 'fila no SISREG (nome interno)', 'fila', 'pessoas', 'devolvidas', 'espera média', 'mediana', 'máxima',
      'idade mediana', 'idade mín.', 'idade máx.', 'fila < 18 anos', 'pessoas 18+', 'solicitação mais antiga', 'fila solicitada em 2026',
      'total (todos os status)']
d = [hd]
for cut in ['NONE', 'I', 'ISC', 'ZAV', 'ZPO', 'ZAMB']:
    for x in sorted(j['filas'][cut], key=lambda r: -r[1]):
        d.append([CIDL[cut], NOME.get(x[0], ''), x[0], x[1], x[2], x[3], r0(x[4]), r0(x[5]), r0(x[6]), x[7], x[8], x[9], x[10], x[11],
                  dia(x[12]), x[13], x[14]])
aba('1 · Filas', d, [1])

# 2 · Conjuntos por OCI
cc = j['conjuntos_cols']
d = [['OCI', 'conjunto', 'recorte CID', 'filas'] + cc]
for x in j['conjuntos']:
    v = x['vals']
    d.append([x['oci'], x['tipo'], CIDL[x['cut']], ' + '.join(x['filas']), v[0], v[1], v[2], r0(v[3]), r0(v[4]), r0(v[5]), v[6], v[7], v[8], v[9]])
aba('2 · Conjuntos por OCI', d, [1])

# 3 · Região de Saúde
cols = j['regioes']['cols']
d = [['Região de Saúde da unidade solicitante, medida FILA. "(sem região informada)" em linha própria, sem rateio. As linhas de pessoas não somam o total: quem tem solicitação vinda de duas regiões conta nas duas.'],
     ['Região de Saúde'] + cols]
d += [['(sem região informada)' if r[0] is None else r[0]] + r[1:] for r in j['regioes']['rows']]
aba('3 · Região de Saúde', d, [2])

# 4 · Pessoas em mais de uma OCI
ov = j['sobreposicao_ocis']
d = [['Pessoas (CNS distintos) por número de OCI em que se enquadram — conjunto "exames + consultas" de cada OCI, do motor (Sum(Aggr(...), cns_usuario_solicitacao))'],
     ['nº de OCI', 'pessoas']] + [[k, v] for k, v in ov['dist_ex_co'].items()]
d += [[], ['pessoas em 2 ou mais OCI (exames + consultas)', ov['ge2_ex_co']], ['pessoas em 2 ou mais OCI (só exames)', ov['ge2_ex']],
      ['pessoas nas sete OCI, união (exames + consultas)', ov['uniao_ex_co']], ['fila nas sete OCI, união (exames + consultas)', ov['uniao_fila_ex_co']],
      ['pessoas nas sete OCI, união (só exames)', ov['uniao_ex']], ['fila nas sete OCI, união (só exames)', ov['uniao_fila_ex']],
      [], ['par de OCI', 'pessoas nas duas (exames + consultas)', 'pessoas nas duas (só exames)']]
d += [[k, ov['pares_ex_co'][k], ov['pares_ex'][k]] for k in ov['pares_ex_co']]
e = j['extra']
d += [[], ['pessoas que esperam cintilografia de estresse e de repouso (I20–I25)', e['cintilografia_pessoas_nas_duas']],
      ['idem, sem recorte de CID', e['cintilografia_pessoas_nas_duas_semcid']],
      ['pessoas que esperam teste ergométrico e Holter (I*)', e['ergometrico_e_holter_I']]]
aba('4 · Pessoas em mais de uma OCI', d, [2, len(ov['dist_ex_co']) + 11])

# 5 · Fila por ano da solicitação
d = [j['fila_por_ano_cols']] + sorted(j['fila_por_ano'], key=lambda r: (r[0], r[1]))
aba('5 · Fila por ano', d, [1])

# 6 · Agendadas por executante (sobreposição)
ac = j['agendamentos_12m_cols']
d = [['Agendamentos por tipo de unidade executante (regiao_saude_executante). "Privado" e "Contratado/Credenciado" são classificações do próprio painel. O painel não traz o convênio da unidade.'], ac]
d += sorted(j['agendamentos_12m_por_regiao_executante'], key=lambda r: (r[0], -r[2]))
d += [[], ['por unidade executante'], ['fila (agendamento)', 'unidade executante', 'tipo'] + ac[2:]]
d += sorted(j['agendamentos_12m_por_unidade_executante'], key=lambda r: (r[0], -r[3]))
aba('6 · Agendadas por executante', d, [2, len(j['agendamentos_12m_por_regiao_executante']) + 5])

# 7 · Unidades privadas: mês a mês, status, CID, código
d = [['As duas unidades "Privado" que agendam consultas de cardiologia: agendamentos por mês do agendamento (filas de cardiologia do enquadramento)'],
     ['unidade', 'fila'] + e['privado_mes_cols']] + e['privado_mes']
d += [[], ['status dos agendamentos (todas as datas)'], ['fila', 'status', 'agendamentos']] + e['privado_status']
d += [[], ['CID mais frequentes na consulta de risco cirúrgico agendada nessas unidades'], ['CID', 'agendamentos']] + e['privado_cid_risco']
d += [[], ['unidade', 'código da unidade no painel', 'primeiro agendamento (qualquer fila)', 'primeiro agendamento (filas de cardiologia)']] + e['privado_primeiro_agendamento']
aba('7 · Unidades privadas', d, [2])

# 8 · Oferta por OCI (agendadas 12 meses)
d = [e['oferta_oci_cols']] + e['oferta_oci']
aba('8 · Agendadas por OCI', d, [1])

# 9 · CIDs principais
d = [['CID mais frequentes (codigo_cid_solicitado) na fila de cada nome, sem recorte — mostra o peso de cada CID e o que fica fora da ficha'], ['fila no SISREG', 'CID', 'fila']]
for nome, lst in j['cid_principais_na_fila_sem_recorte'].items():
    for cid, n in lst:
        d.append([nome, cid, n])
aba('9 · CID principais', d, [2])

# 10 e 11 · Varredura
d = [j['varredura_solicitacoes_cols']] + sorted(j['varredura_solicitacoes'], key=lambda r: -r[2])
aba('10 · Varredura solicitações', d, [1])
d = [j['varredura_agendamentos_cols']] + sorted(j['varredura_agendamentos'], key=lambda r: -r[3])
aba('11 · Varredura agendamentos', d, [1])

# 12 · Cirurgias eletivas (tabela CE do painel)
d = [['Tabela de cirurgias eletivas (CE) do painel: fila e CID de pré-operatório'], ['medida', 'valor'],
     ['fila CE (três status)', e['ce_fila_total']], ['pessoas na fila CE', e['ce_fila_pessoas']],
     ['fila CE com Z018/Z488/Z489', e['ce_fila_ZPO']], ['fila CE com Z136/Z848', e['ce_fila_ZAV']],
     [], ['CID mais frequentes na fila CE', '']] + e['ce_cid_amostra']
d += [[], ['hipertensão nas filas de exame das OCI de capítulo I'],
      ['003-4: fila com I10', e['09.02.01.003-4_exames_fila_I10']], ['003-4: pessoas com I10 ou I15', e['09.02.01.003-4_exames_pessoas_so_I10_I15']],
      ['006-9: fila com I10', e['09.02.01.006-9_exames_fila_I10']], ['006-9: pessoas com I10 ou I15', e['09.02.01.006-9_exames_pessoas_so_I10_I15']]]
d += [[], ['CONSULTA EM CARDIOLOGIA - RISCO CIRURGICO, sem recorte de CID, por Região de Saúde (medida fila)'], e['risco_cirurgico_sem_recorte_regiao_cols']]
d += [['(sem região informada)' if r[0] is None else r[0]] + r[1:] for r in e['risco_cirurgico_sem_recorte_regiao']]
aba('12 · CE, I10 e risco cirúrgico', d, [2])

saida = AQUI.parent / 'mapa_social_20261022.xlsx'
wb.save(saida)
print('gravado', saida)
