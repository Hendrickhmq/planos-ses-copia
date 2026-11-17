"""O estudo das filas de imagem do redacao_07: cada código levantado, a decisão e o motivo.

Lê a coleta de 15/10/2026 (dados/fontes/mapa_social_20261015_bruto/coleta_20261015.json), o
valor de referência (dados/valor_unitario.md) e o estado.yaml; escreve
dados/estudo_das_filas.xlsx e devolve as linhas para o .md. Uso, da pasta do plano:
python3 -I dados/scripts/estudo_filas.py
"""
import json, re
from decimal import Decimal as D

d = json.load(open('dados/fontes/mapa_social_20261015_bruto/coleta_20261015.json'))
cols = d['por_codigo_cols']
val = {}
for l in open('dados/valor_unitario.md', encoding='utf-8'):
    m = re.match(r'\| (\d{2}\.\d{2}\.\d{2}\.\d{3}-\d) \|.*\*\*R\$ ([\d.,]+)\*\*', l)
    if m: val[m.group(1).replace('.', '').replace('-', '').lstrip('0')] = D(m.group(2).replace('.', '').replace(',', '.'))
# agendadas jan-set/2026 por código: fora dos 16 nomes do plano 4 e dentro deles (colunas da coleta)
ag = {r[0]: r[1] / 9 for r in d['agendadas_jan_set_2026_por_codigo']}
ag_p4 = {r[0]: r[2] / 9 for r in d['agendadas_jan_set_2026_por_codigo']}
fmt = lambda c: f'0{c[0]}.{c[1:3]}.{c[3:5]}.{c[5:8]}-{c[8]}' if c and len(c) == 9 else (c or '(sem código)')
MOD = {'204': 'radiologia', '205': 'ultrassonografia', '206': 'tomografia', '207': 'ressonância',
       '208': 'medicina nuclear', '210': 'intervencionista'}

CARTEIRA = {'204030188', '204060028', '205020160', '205020070', '205020089', '205020178', '205020143', '205020151',
            '206010052', '206010079', '206010044', '206010060'}
IEV_TC = {'206010010', '206010036', '206010028', '206020023'}
ARTIC = {'206030029', '206020015', '207010021', '204060087', '204060060', '204040035', '204040027', '204060079',
         '204040043', '204010055'}

# (grupo, motivo, quem decidiu e quando) — a ordem das regras é a ordem do estudo
def decide(c, cat, r):
    if cat == 'p4':
        return ('1. Plano 4', 'já é objeto do plano 4 (R$ 11,5 mi): os dezesseis nomes de fila do enquadramento', 'plano 4')
    if cat == 'mesmo':
        return ('2. Mesmo código do plano 4', 'outro projeto: os mesmos códigos do plano 4, fora das filas dele; risco de pagar duas vezes o mesmo objeto ao ISHP. O usuário escolheu a combinação A, e não a D, que as usava', 'usuário, 16/10/2026')
    if cat == 'extra':
        return ('9. Fora dos subgrupos de imagem', 'código fora de 02.04 a 02.10 (OCT, punção e biópsia guiadas, biometria, cateterismo): não é exame de imagem do rol da Portaria 4.282', 'estudo, 15/10/2026')
    if c in CARTEIRA:
        return ('0. Entra na carteira', 'no rol da Portaria 4.282, fora do plano 4 e escolhido pelo usuário', 'usuário, 16 e 19/10/2026')
    if c in IEV_TC:
        return ('4. Articulações e partes moles — IEV', 'outro projeto: compatível com a OCI de ortopedia 09.03.01.003-8, que o Fila Zero do IEV executa com tomografia de articulações ou segmentos anatômicos. Entrou na carteira em 19/10 e saiu em 20/10', 'usuário, 20/10/2026')
    if c == '205010032':
        return ('3. Ecocardiografia — IEV', 'outro projeto: está nas OCI de cardiologia do IEV (Convênio 030977/2026, Fila Zero: OCI 09.02.01.006-9, com ecocardiografia transtorácica, e 09.02.01.004-2, com a de estresse). Além disso, espera de 135 dias e custo de 174% do recurso', 'usuário, 15/10/2026; motivo dito em 20/10/2026')
    if c == '205020062':
        return ('4. Articulações e partes moles — IEV', 'outro projeto: as OCI de ortopedia do IEV (Convênios 030975 e 030976/2026; no Fila Zero, a OCI 09.03.01.002-0 com ultrassom de partes moles). No plano 4, partes moles saiu em 22/09 para "outra OCI" (D-007). Articulações retiradas em 15/10, partes moles em 16/10', 'usuário, 15 e 16/10/2026')
    if c in ARTIC:
        return ('4. Articulações e partes moles — IEV', 'outro projeto: as OCI de ortopedia do IEV (no Fila Zero, a OCI 09.03.01.003-8 com tomografia de articulações ou segmentos anatômicos)', 'usuário, 15/10/2026')
    if c.startswith('208'):
        return ('5. Cintilografia (medicina nuclear)', 'complexa de executar (confirmado em 20/10): Autorização de Operação da CNEN e licença da vigilância (RDC 38/2008), médico nuclear e supervisor certificado pela CNEN (NN 3.05), radiofármaco do IPEN, fornecedor único; 62% a 71% dos pedidos vêm de unidades de referência e contratados. A de miocárdio está na OCI de cardiologia 09.02.01.005-0', 'usuário, 16/10/2026')
    if c.startswith('207'):
        return ('6. Ressonância', 'a rede já cuida: espera média de 19 a 63 dias e a rede agenda por mês o tamanho da fila (zera em cerca de 1 mês). Também há o convênio de ressonância em ortopedia do IEV (OCI 09.03.01.004-6)', 'usuário, 16/10/2026')
    if val.get(c) is None:
        return ('7. Fora do rol da Portaria 4.282', 'paga mal (confirmado no SIGTAP em 20/10): sem incremento, só a Tabela — radiografias de R$ 6,30 a R$ 10,96, mamografia diagnóstica R$ 22,50, paquimetria R$ 14,81; a bite-wing foi revogada em 2020. Exceções de alta complexidade: PET-CT R$ 2.107,22 (serviço raro, três indicações) e eco de estresse R$ 330,00 (está no IEV)', 'estudo, 15/10/2026')
    return ('8. No rol, fila pequena', 'fila pequena: não vale a pena incluir (usuário)', 'estudo, 16/10/2026')

linhas = []
for cat in ('p4', 'mesmo', 'cand', 'res', 'extra'):
    for r in d['por_codigo'][cat]:
        r = dict(zip(cols, r)); c = r['sigtap']
        if cat == 'res':
            g = ('10. Resíduo', 'fila sem nenhuma solicitação nem agendamento em 2026 (nomes antigos do SISREG)', 'estudo, 15/10/2026')
        else:
            g = decide(c, cat, r)
        a = (ag_p4 if cat == 'p4' else ag).get(c, 0)
        linhas.append(dict(grupo=g[0], motivo=g[1], quem=g[2], codigo=fmt(c),
                           desc=(d['descricao_sigtap'].get(c) or '(sem descrição)').capitalize(),
                           mod=MOD.get((c or '')[:3], 'outro grupo'), filas=r['nomes_com_fila'], fila=r['fila'],
                           pessoas=r['pessoas'], espera=round(r['espera_media']), mediana=round(r['espera_mediana']),
                           ag=round(a), meses=(round(r['fila'] / a, 1) if a else None),
                           valor=(float(val[c]) if c and c in val else None),
                           custo=(float(val[c] * r['fila']) if c and c in val else None), cat=cat))
linhas.sort(key=lambda x: (int(x['grupo'].split('.')[0]), -x['fila']))

if __name__ == '__main__':
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment
    wb = Workbook(); ws = wb.active; ws.title = 'Códigos'
    H = ['grupo', 'código SIGTAP', 'procedimento', 'modalidade', 'nomes de fila', 'fila (pedidos)', 'pessoas',
         'espera média (dias)', 'espera mediana (dias)', 'agendados/mês 2026', 'meses para a rede zerar',
         'valor de referência (R$)', 'custo para zerar (R$)', 'decisão e motivo', 'quem decidiu']
    ws.append(H)
    for x in linhas:
        ws.append([x['grupo'], x['codigo'], x['desc'], x['mod'], x['filas'], x['fila'], x['pessoas'], x['espera'],
                   x['mediana'], x['ag'], x['meses'], x['valor'], x['custo'], x['motivo'], x['quem']])
    for c in ws[1]:
        c.font = Font(name='Arial', bold=True, color='FFFFFF'); c.fill = PatternFill('solid', start_color='1F3864')
        c.alignment = Alignment(wrap_text=True, vertical='center')
    for row in ws.iter_rows(min_row=2):
        for c in row: c.font = Font(name='Arial')
        row[11].number_format = row[12].number_format = '"R$" #,##0.00'
        for k in (5, 6, 9): row[k].number_format = '#,##0'
    for i, w in enumerate([30, 15, 50, 16, 9, 11, 10, 10, 10, 11, 11, 13, 15, 90, 20], 1):
        ws.column_dimensions[ws.cell(1, i).column_letter].width = w
    ws.freeze_panes = 'D2'; ws.auto_filter.ref = ws.dimensions
    wb.save('dados/estudo_das_filas.xlsx')
    from collections import OrderedDict
    g = OrderedDict()
    for x in linhas:
        s = g.setdefault(x['grupo'], [0, 0, 0, x['quem']]); s[0] += 1; s[1] += x['filas']; s[2] += x['fila']
    for k, (n, f, p, q) in g.items(): print(f'{k} | {n} códigos | {f} nomes | {p} pedidos | {q}')
    print('total', sum(v[2] for v in g.values()), 'códigos', len(linhas))
    for x in linhas:
        if x['grupo'].startswith('8.'): print('   8:', x['codigo'], x['desc'][:50], x['fila'])
