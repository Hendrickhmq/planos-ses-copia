# Lê a saída do motor transcrita (motor_*.txt, cada parte conferida por hash djb2 contra o texto
# do motor) e grava motor_20261026.json, com os nomes de fila exatos e as datas em DD/MM/AAAA.
# Mapa Social da Saúde (MPDFT), app Qlik 7edb02fa-f1f5-4ea6-b348-049a4ac2d095, base recarregada
# em 26/10/2026 16:32:44 (Brasília). Só contagens agregadas: nenhum CNS, CPF, nome ou data de
# nascimento.
# Uso: python3 ler_motor_20261026.py   (de qualquer pasta)
import json
import re
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

AQUI = Path(__file__).resolve().parent
BASE = date(1899, 12, 30)


def djb2(s):
    h = 5381
    for ch in s:
        h = ((h << 5) + h + ord(ch)) & 0xFFFFFFFF
    return h


def ler(nome, tamanho, hash_):
    t = (AQUI / nome).read_text(encoding='utf-8').rstrip('\n')
    assert len(t) == tamanho and djb2(t) == hash_, f'{nome}: o texto não bate com o hash do motor'
    return t


def nome_exato(s):
    # o motor devolveu o espaço não separável e os caracteres fora do Latin-1 como {U+XXXX}
    return re.sub(r'\{U\+([0-9A-F]{4})\}', lambda m: chr(int(m.group(1), 16)), s)


def num(v):
    if v == '':
        return None
    f = float(v)
    return int(f) if f.is_integer() else f


def data(v):
    return None if v in ('', None) else (BASE + timedelta(days=int(float(v)))).strftime('%d/%m/%Y')


def hora(serial):
    d = datetime(1899, 12, 30) + timedelta(days=serial)
    return d.strftime('%d/%m/%Y %H:%M:%S')


# hashes da transcrição (texto do motor, calculados no navegador)
FILAS = ler('motor_filas_20261026.txt', 109303, 1068364975)
CODIGOS = ler('motor_codigos_20261026.txt', 20382, 2206795101)
AGREG = ler('motor_agregados_20261026.txt', 28324, 3777938657)

filas_cols = ['indice', 'nome_sisreg', 'codigo_sigtap', 'fila', 'fila_viva', 'pessoas', 'pessoas_viva', 'devolvidas',
              'espera_media', 'espera_mediana', 'espera_max', 'mais_antiga', 'fila_solicitada_2026', 'idade_mediana',
              'total_todos_status', 'solicitacoes_2026_todos_status', 'primeira_solicitacao_na_base', 'agendadas_12m',
              'agendadas_todos_os_anos', 'agendadas_2026', 'primeiro_agendamento', 'agendadas_a_partir_de_26_10_2026',
              'cid_principais']
filas = []
for l in FILAS.split('\n'):
    f = l.split('|')
    assert len(f) == 23, l
    r = [int(f[0]), nome_exato(f[1]), f[2]] + [num(x) for x in f[3:22]] + [f[22]]
    for i in (11, 16, 20):
        r[i] = data(r[i])
    r[22] = [[c.split(' ')[0], int(c.split(' ')[1])] for c in f[22].split(';') if c]
    filas.append(r)

codigos_cols = ['codigo_sigtap', 'descricao_sigtap', 'fila', 'fila_viva', 'pessoas', 'pessoas_viva', 'devolvidas',
                'espera_media', 'espera_mediana', 'espera_max', 'mais_antiga', 'fila_solicitada_2026', 'idade_mediana',
                'total_todos_status', 'solicitacoes_2026_todos_status', 'primeira_solicitacao_na_base',
                'nomes_com_fila', 'espera_media_viva', 'agendadas_12m', 'agendadas_2026', 'agendadas_todos_os_anos']
codigos = []
for l in CODIGOS.split('\n'):
    f = l.split('|')
    assert len(f) == 21, l
    r = [f[0], nome_exato(f[1])] + [num(x) for x in f[2:]]
    r[10] = data(r[10])
    r[15] = data(r[15])
    codigos.append(r)

legenda, grupos, reg_grupo, reg_codigo, idade, mamo, carteira, fora, por_ano, tot, so_ag = {}, [], {}, {}, [], [], {}, [], [], None, []
idx_nome = {r[0]: r[1] for r in filas}
for l in AGREG.split('\n'):
    f = l.split('|')
    t = f[0]
    if t == 'REGIOES':
        for p in f[1].split(';'):
            k, v = p.split('=', 1)
            legenda[k] = nome_exato(v)
    elif t == 'G':
        nomes = [idx_nome[int(i)] for i in f[4].split(',')]
        v = [num(x) for x in f[5:]]
        v[8] = data(v[8])
        grupos.append([int(f[1]), f[2], nome_exato(f[3]), nomes] + v)
    elif t == 'GR':
        reg_grupo[int(f[1])] = [[legenda[p.split(':')[0]], int(p.split(':')[1])] for p in f[2].split(';') if p]
    elif t == 'CR':
        reg_codigo[f[1]] = [[legenda[p.split(':')[0]], int(p.split(':')[1]), int(p.split(':')[2])] for p in f[2].split(';') if p]
    elif t == 'ID':
        idade.append([f[1], int(f[2]), int(f[3]), nome_exato(f[4])] + [num(x) for x in f[5:]])
    elif t == 'MC':
        mamo.append([nome_exato(f[1]), f[2], int(f[3]), int(f[4])])
    elif t == 'CA':
        carteira[f[1]] = [num(x) for x in f[2:]]
    elif t == 'FO':
        fora.append([nome_exato(f[1]), f[2]] + [num(x) for x in f[3:]])
    elif t == 'ANO':
        por_ano = sorted([[int(a), int(b), int(c)] for a, b, c in (p.split(':') for p in f[1].split(';'))])
    elif t == 'TOT':
        tot = f[1:]
    elif t == 'AO':
        so_ag.append([f[1], int(f[2]), int(f[3])])

ST = "status_solicitacao_alias={'SOLICITAÇÃO PENDENTE DE REGULAÇÃO','SOLICITAÇÃO CORRIGIDA E REENVIADA PARA REGULAÇÃO','SOLICITAÇÃO PENDENTE DE REGULAÇÃO POR FILA DE ESPERA'}"
recarga_utc = '2026-10-26T19:32:44.246Z'
rec = datetime.strptime(recarga_utc, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=timezone.utc) - timedelta(hours=3)
motor = {
    'app': '7edb02fa-f1f5-4ea6-b348-049a4ac2d095',
    'titulo_app': 'D-PDDC - MAPA DA SAÚDE - REGULAÇÃO (M)',
    'painel': 'https://paineis-ext.mpdft.mp.br/extensions/mapasauderegulamentacao/mapasauderegulamentacao.html',
    'recarga_utc': recarga_utc,
    'recarga_brasilia': rec.strftime('%d/%m/%Y %H:%M:%S'),
    'recarga_conferida_no_fim': tot[5],
    'consulta_inicio': hora(46321.69912037037),
    'consulta_fim': hora(46321.70038194444),
    'max_data_solicitacao': data(tot[8]),
    'max_data_agendamento': data(tot[9]),
    'min_data_solicitacao': data(tot[10]),
    'leitura_descartada': ('O painel foi aberto às 16:24:21 com a base recarregada em 26/10/2026 14:36:46 '
                           '(qLastReloadTime 2026-10-26T17:36:46Z); a base recarregou às 16:32:44 durante a coleta. '
                           'Tudo o que está neste JSON saiu de uma ida só, de 16:46:44 a 16:48:33, com a recarga das '
                           '16:32:44 conferida no início e no fim; o que foi lido antes dela foi descartado.'),
    'filtro_fila': ST,
    'filtro_devolvidas': "status_solicitacao_alias={'SOLICITAÇÃO DEVOLVIDA PARA COMPLEMENTAÇÃO PELO SOLICITANTE'}",
    'janelas': {'viva 24 meses': 'data_solicitacao={">=26/10/2024"}',
                'agendadas 12 meses': 'data_agendamento={">=26/10/2025<=25/10/2026"}'},
    'universo': ('codigo_sigtap_solicitacao={"204*","205*","206*","207*","208*","210*"} (subgrupos 02.04 a 02.08 e 02.10; '
                 'o 02.09, endoscopia, fica fora: não é exame de imagem; tinha 54.445 na fila). Agendamentos: '
                 'codigo_sigtap_agendamento com os mesmos curingas.'),
    'nota_medidas': ('fila = Count(Distinct {1<universo, filtro_fila>} contador_solicitacao); viva = a mesma com a janela de 24 meses; '
                     'pessoas = Count(Distinct ... cns_usuario_solicitacao), só a contagem; devolvidas = filtro_devolvidas; '
                     'espera = Avg/Median/Max(tempo_espera_solicitacao) no conjunto da fila, em dias; mais antiga = Min(data_solicitacao) na fila; '
                     'fila solicitada em 2026 = fila com Ano_Solicitacao={2026}; idade = Median(idade_solicitacao) na fila; '
                     'agendadas 12 meses = Count(Distinct contador_agendamento) com data_agendamento de 26/10/2025 a 25/10/2026, todos os status, '
                     'pelo par descrição_procedimento_agendamento × codigo_sigtap_agendamento (fila) ou pelo código; todos os anos na fila.'),
    'filas_cols': filas_cols, 'filas': filas,
    'codigos_cols': codigos_cols, 'codigos': codigos,
    'grupos_cols': ['indice', 'codigo_sigtap', 'grupo', 'nomes_sisreg', 'fila', 'fila_viva', 'pessoas', 'pessoas_viva',
                    'devolvidas', 'espera_media', 'espera_mediana', 'espera_max', 'mais_antiga', 'fila_solicitada_2026',
                    'idade_mediana', 'agendadas_12m_pelos_nomes'],
    'grupos': grupos,
    'regiao_grupos_nota': 'fila (solicitações) por regiao_saude_solicitante, soma dos nomes do grupo; "-" é o campo vazio',
    'regiao_grupos': {str(k): v for k, v in reg_grupo.items()},
    'regiao_codigos_cols': ['regiao_saude_solicitante', 'fila', 'pessoas'],
    'regiao_codigos': reg_codigo,
    'idade_cols': ['codigo_sigtap', 'idade_min_ficha', 'idade_max_ficha', 'nome_sisreg', 'fila', 'fila_na_idade',
                   'fila_abaixo', 'fila_acima', 'pessoas_na_idade', 'fila_viva_na_idade', 'fila_50_a_69', 'fila_40_a_49', 'fila_70_ou_mais'],
    'idade': idade,
    'mamografia_cid_cols': ['nome_sisreg', 'codigo_cid_solicitado', 'fila', 'fila_viva'],
    'mamografia_cid': mamo,
    'carteira_cols': ['fila', 'fila_viva', 'pessoas', 'pessoas_viva', 'pessoas_tambem_na_fila_do_plano4', 'espera_media',
                      'fila_solicitada_2026', 'agendadas_12m'],
    'carteira': {'12 codigos': carteira['12'], '10 codigos sem mamografia e densitometria': carteira['10']},
    'fora_dos_subgrupos_cols': ['nome_sisreg', 'codigo_sigtap', 'fila', 'fila_viva', 'pessoas', 'devolvidas', 'espera_media',
                                'espera_mediana', 'agendadas_12m_nao_medida'],
    'fora_dos_subgrupos': fora,
    'por_ano_cols': ['Ano_Solicitacao', 'fila', 'fila_viva'], 'por_ano': por_ano,
    'totais': {'fila': int(tot[0]), 'fila_viva': int(tot[1]), 'pessoas': int(tot[2]), 'fila_0209_endoscopia_fora': int(tot[3])},
    'so_agendamento_por_codigo_cols': ['codigo_sigtap', 'nomes_so_na_tabela_de_agendamentos', 'agendadas_12m_nesses_nomes'],
    'so_agendamento_por_codigo': so_ag,
    'transcricao': {
        'nota': ('o motor devolveu as tabelas em texto (campos separados por |; o espaço não separável e os caracteres fora do '
                 'Latin-1 como {U+XXXX}; na tabela de filas, o nome que já estava na leitura descartada veio como #índice dela, '
                 'e foi trocado pelo nome conferido). Cada parte foi transcrita e conferida por hash djb2 de 32 bits contra o texto '
                 'do motor; o texto inteiro também'),
        'motor_filas_20261026.txt': [109303, 1068364975],
        'motor_codigos_20261026.txt': [20382, 2206795101],
        'motor_agregados_20261026.txt': [28324, 3777938657]},
}
(AQUI / 'motor_20261026.json').write_text(json.dumps(motor, ensure_ascii=False, indent=1), encoding='utf-8')
print('filas', len(filas), 'codigos', len(codigos), 'grupos', len(grupos), 'recarga', motor['recarga_brasilia'],
      'consulta', motor['consulta_inicio'], '-', motor['consulta_fim'])
