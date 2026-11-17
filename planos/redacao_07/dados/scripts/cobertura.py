"""A cobertura das filas de imagem fora do plano 4 pela emenda de R$ 1.502.687,00.

Lê a coleta do agente mapa-social (dados/fontes/mapa_social_20261015_bruto/coleta_20261015.json)
e o valor de referência (dados/valor_unitario.md); escreve dados/cobertura.md.
Uso, a partir da pasta do plano: python3 -I dados/scripts/cobertura.py > dados/cobertura.md
"""
import json, re
from decimal import Decimal as D, ROUND_FLOOR

COLETA = 'dados/fontes/mapa_social_20261015_bruto/coleta_20261015.json'
R = D('1502687.00')                       # estado.yaml, recurso.valor
CEN = [('sem apoio', R), ('com 10% de apoio', (R * D('0.9')).quantize(D('0.01')))]
MOD = {'204': 'radiologia', '205': 'ultrassonografia', '206': 'tomografia', '207': 'ressonância',
       '208': 'medicina nuclear', '210': 'intervencionista'}

# Decisão do usuário, 15/10/2026: "retire Ecocardiografia transtorácica e todos os outros de articulações".
ECO = '205010032'
ARTIC_COD = {'206030029', '206020015', '207010021', '204060087', '204060060', '204040035',
             '204040027', '204060079', '204040043', '204010055'}   # descrição SIGTAP com "articulação"
US_ARTIC = '205020062'   # o código da US de articulação: sai a fila de articulação; o resto do código fica
ARTIC_NOME = re.compile(r'ARTICULA|OMBRO|PUNHO|JOELHO|TORNOZELO|COTOVELO|QUADRIL|COXO|\bMAO\b|\bPE\b|DEDO|TENDAO|CALCANEO')
# Decisão do usuário, 16/10/2026: "retire todos de cintilografia". Sai a medicina nuclear inteira (02.08), que no
# SIGTAP é toda cintilográfica, inclusive o estudo renal dinâmico e o de fluxo sanguíneo cerebral. O PET-CT
# (02.06.01.009-5) fica: é tomografia por emissão de pósitrons, fora do rol da 4.282, sem valor aqui.
NUCLEAR = '208'

d = json.load(open(COLETA))
valor = {}
for l in open('dados/valor_unitario.md', encoding='utf-8'):
    m = re.match(r'\| (\d{2}\.\d{2}\.\d{2}\.\d{3}-\d) \|.*\*\*R\$ ([\d.,]+)\*\*', l)
    if m: valor[m.group(1).replace('.', '').replace('-', '').lstrip('0')] = D(m.group(2).replace('.', '').replace(',', '.'))
ag = {r[0]: r[1] for r in d['agendadas_jan_set_2026_por_codigo']}
fmt = lambda c: f'0{c[0]}.{c[1:3]}.{c[3:5]}.{c[5:8]}-{c[8]}' if len(c) == 9 else c   # há dois códigos malformados, de 8 dígitos
br = lambda v: 'R$ ' + f'{v:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
n = lambda v: f'{v:,}'.replace(',', '.')

def conta(fila, v, rec):
    k = int((rec / v).to_integral_value(rounding=ROUND_FLOOR)); at = min(k, fila)
    return at, int(100 * at // fila), rec - at * v

def linhas(chave):
    cols = d['por_codigo_cols']; out = []
    for r in d['por_codigo'][chave]:
        r = dict(zip(cols, r)); c = r['sigtap']
        r.update(cod=fmt(c), desc=(d['descricao_sigtap'].get(c) or '(sem descrição)').capitalize(),
                 mod=MOD.get(c[:3], '?'), v=valor.get(c), ag=ag.get(c, 0) / 9, med=f"{r['espera_mediana']:.0f}")
        out.append(r)
    return out

# as filas do código da US de articulação, uma a uma (só as candidatas: o resíduo já está fora)
fc = d['filas_cols']
filas_us = [dict(zip(fc, r)) for r in d['filas'] if r[1] == US_ARTIC and r[2] == 'candidata']
artic = [f for f in filas_us if ARTIC_NOME.search(f['nome_sisreg'])]
resto = [f for f in filas_us if not ARTIC_NOME.search(f['nome_sisreg'])]

def agrega(fs, desc):
    fila = sum(f['fila'] for f in fs)
    return dict(sigtap=US_ARTIC, cod=fmt(US_ARTIC) + ' *', desc=desc, mod='ultrassonografia', v=valor[US_ARTIC],
                fila=fila, pessoas=sum(f['pessoas'] for f in fs), med='—',
                espera_media=sum(f['fila'] * f['espera_media'] for f in fs) / fila,
                ag=sum(f['agendadas_2026_jan_set'] for f in fs) / 9)

todas = linhas('cand')
fora = [r for r in todas if r['sigtap'] == ECO or r['sigtap'] in ARTIC_COD or r['sigtap'].startswith(NUCLEAR)]
cand = [r for r in todas if r not in fora and r['sigtap'] != US_ARTIC]
# Decisão do usuário, 16/10/2026: "tire partes moles" — sai o resto do código 02.05.02.006-2 (partes moles e outras regiões).
pm = agrega(resto, 'US de partes moles e outras regiões (o resto do código da articulação)')
cand.sort(key=lambda r: -r['fila'])
art = agrega(artic, 'US de articulação (as filas de articulação, mão, pé, quadril, tendão)')

print('''# A cobertura das filas de imagem fora do plano 4 — emenda de R$ 1.502.687,00

**Controle interno: tem valor em reais; não vai ao documento.**

| | |
|---|---|
| recurso | R$ 1.502.687,00, federal — a mesma emenda do redacao_05 (`estado.yaml`) |
| gestão e apoio | a decidir (trava F-08). Dois cenários: **sem apoio**, e **10%** (R$ 1.352.418,30 para exames), o teto que o usuário fixou para a mesma emenda no redacao_05 |
| fila | Mapa Social, recarga de 15/10/2026 19:32, coleta do agente `mapa-social` (`fontes/mapa_social_20261015.md`, 7/7). **Fila = solicitações (exames), não pessoas** |
| valor | `valor_unitario.md` (Anexo I da Portaria SAES/MS 4.282/2026, a regra do plano 4). Código fora do rol fica sem valor aqui |
| fora por decisão do usuário | ecocardiografia transtorácica e as filas de articulação (15/10/2026); todas as cintilografias (16/10/2026) — seção 0 |
| montado em | 16/10/2026, por `scripts/cobertura.py` |

Tudo abaixo é **CALCULADO**:
- **custo para zerar** = fila × valor de referência; **% do recurso** = custo ÷ R$ 1.502.687,00;
- **atende** = piso(recurso ÷ valor), limitado à fila; o percentual é truncado, e "zera" só quando
  atende a fila inteira;
- **meses para a rede zerar** = fila ÷ agendadas por mês em 2026 (jan–set ÷ 9). Mede o ritmo de
  agendamento de hoje sem contar os pedidos novos: quanto maior, menos a rede dá conta sozinha;
- **zerar** é zerar a fila medida em 15/10/2026. Pedido novo continua entrando.
- **\\*** = parte das filas de um código, somada linha a linha: as pessoas podem contar duas vezes,
  a espera média é ponderada pela fila e a mediana não se calcula.
''')

print('## 0. Fora por decisão do usuário\n')
print('- 15/10/2026: "Retire Ecocardiografia transtorácica e todos os outros de articulações."')
print('- 16/10/2026: "Retire todos de cintilografia." Sai a medicina nuclear inteira (02.08), inclusive o estudo '
      'renal dinâmico e o de fluxo sanguíneo cerebral, que também são cintilográficos. O PET-CT fica: é tomografia.\n')
print('| código | procedimento | fila | pessoas | custo para zerar |')
print('|---|---|---|---|---|')
for r in sorted(fora + [art, pm], key=lambda r: -r['fila']):
    print(f"| {r['cod']} | {r['desc']} | {n(r['fila'])} | {n(r['pessoas'])} | {br(r['fila'] * r['v']) if r['v'] else 'fora do rol'} |")
print('\nFica, com nota: a **TC de face / seios da face / ATM** (02.06.01.004-4, 500 na fila), que é '
      'exame de face e seios e só cita a articulação temporo-mandibular no nome.\n')
print('- 16/10/2026: "Tire partes moles." Sai o resto do código 02.05.02.006-2: partes moles e as outras regiões abaixo.\n')
print('As filas do código 02.05.02.006-2 que saíram em 16/10/2026 (partes moles e outras regiões):\n')
print('| fila no SISREG | fila | espera média |')
print('|---|---|---|')
for f in sorted(resto, key=lambda f: -f['fila']):
    print(f"| {f['nome_sisreg']} | {n(f['fila'])} | {f['espera_media']:.0f} |")

print('\n## 1. As filas candidatas, código a código (fila de 100 ou mais)\n')
print('| modalidade | código | procedimento | fila | pessoas | espera média / mediana (dias) | agendadas/mês 2026 | meses para a rede zerar | valor ref. | custo para zerar | % do recurso | sem apoio | com 10% de apoio |')
print('|---|---|---|---|---|---|---|---|---|---|---|---|---|')
for r in cand:
    if r['fila'] < 100: continue
    r['meses'] = r['fila'] / r['ag'] if r['ag'] else None
    mo = f"{r['meses']:.1f}".replace('.', ',') if r['meses'] else '—'
    base = f"| {r['mod']} | {r['cod']} | {r['desc']} | {n(r['fila'])} | {n(r['pessoas'])} | {r['espera_media']:.0f} / {r['med']} | {n(round(r['ag']))} | {mo} | "
    if r['v'] is None:
        print(base + 'fora do rol | | | | |'); continue
    cel = []
    for _, rec in CEN:
        at, p, _ = conta(r['fila'], r['v'], rec)
        cel.append('zera' if at == r['fila'] else f'{n(at)} ({p}%)')
    print(base + f"{br(r['v'])} | {br(r['fila'] * r['v'])} | {r['fila'] * r['v'] / R:.0%} | {cel[0]} | {cel[1]} |")
pequenas = [r for r in cand if r['fila'] < 100]
print(f"\nMais {len(pequenas)} códigos com menos de 100 na fila ({n(sum(r['fila'] for r in pequenas))} no total), na planilha da coleta.")

rm = [r for r in cand if r['mod'] == 'ressonância']
print('\n## 1a. A ressonância, código a código (todas as filas)\n')
print('| código | procedimento | fila | pessoas | espera média / mediana (dias) | agendadas/mês 2026 | meses para a rede zerar | custo para zerar |')
print('|---|---|---|---|---|---|---|---|')
for r in rm:
    mo = f"{r['fila'] / r['ag']:.1f}".replace('.', ',') if r['ag'] else '—'
    print(f"| {r['cod']} | {r['desc']} | {n(r['fila'])} | {n(r['pessoas'])} | {r['espera_media']:.0f} / {r['med']} | {n(round(r['ag']))} | {mo} | {br(r['fila'] * r['v'])} |")
fr = sum(r['fila'] for r in rm); cr = sum(r['fila'] * r['v'] for r in rm); ar = sum(r['ag'] for r in rm)
er = sum(r['fila'] * r['espera_media'] for r in rm) / fr
mo = f"{fr / ar:.1f}".replace('.', ',')
print(f"| **ressonância, soma das linhas** | {len(rm)} códigos | **{n(fr)}** | | {er:.0f} (ponderada) | {n(round(ar))} | {mo} | **{br(cr)}** |")
vr = valor['207010064']
for rot, rec in CEN:
    k = int((rec / vr).to_integral_value(rounding=ROUND_FLOOR))
    print(f"\n- {rot}: o recurso compra {n(k)} ressonâncias a {br(vr)}, {int(100 * k // fr)}% da fila de ressonância."
          if rot == 'sem apoio' else f"- {rot}: {n(k)} ressonâncias, {int(100 * k // fr)}% da fila.")
print('\nA ressonância de ATM (02.07.01.002-1, 127 na fila) saiu com as articulações (seção 0).')

print('\n## 2. Mesmo código do plano 4, sem resíduo\n')
print('| código | procedimento | fila | pessoas | espera média / mediana | valor ref. | custo para zerar |')
print('|---|---|---|---|---|---|---|')
tot = D(0); mesmo = sorted(linhas('mesmo_semres'), key=lambda r: -r['fila'])
for r in mesmo:
    tot += r['fila'] * r['v']
    print(f"| {r['cod']} | {r['desc']} | {n(r['fila'])} | {n(r['pessoas'])} | {r['espera_media']:.0f} / {r['med']} | {br(r['v'])} | {br(r['fila'] * r['v'])} |")
t = d['totais']['mesmo_semres']; tc = d['totais_cols']
print(f"| **total** | {t[0]} filas | **{n(t[tc.index('fila')])}** | {n(t[tc.index('pessoas')])} | {t[tc.index('espera_media')]:.0f} / {t[tc.index('espera_mediana')]:.0f} | | **{br(tot)}** |")

por = {r['cod']: r for r in cand}
for r in mesmo:
    por[r['cod'] + ' (p4)'] = r
CURTO = {'02.05.02.016-0': 'US pélvica', '02.05.02.007-0': 'US de bolsa escrotal', '02.05.02.006-2 *': 'US de partes moles e outras regiões',
         '02.05.02.008-9': 'US de globo ocular', '02.05.02.017-8': 'US transfontanela', '02.05.02.015-1': 'US obstétrica com doppler',
         '02.06.01.005-2': 'TC de pescoço', '02.06.01.007-9': 'TC de crânio', '02.06.01.004-4': 'TC de face/seios',
         '02.04.03.018-8': 'mamografia', '02.04.06.002-8': 'densitometria', '02.07.01.006-4': 'RM de crânio',
         '02.07.01.004-8': 'RM de coluna lombo-sacra'}
US_LONGA = ['02.05.02.016-0', '02.05.02.007-0', '02.05.02.008-9', '02.05.02.017-8', '02.05.02.015-1']
US_P4 = [r['cod'] + ' (p4)' for r in mesmo if r['mod'] == 'ultrassonografia']
for c in US_P4:
    CURTO[c] = 'US ' + {'02.05.01.004-0': 'doppler', '02.05.02.012-7': 'de tireoide', '02.05.02.004-6': 'de abdômen total',
                        '02.05.02.005-4': 'de aparelho urinário', '02.05.02.003-8': 'de abdômen superior'}[c[:14]] + ' (mesmo código do plano 4)'
base_us = sum(por[c]['fila'] * por[c]['v'] for c in US_LONGA)
COMBOS = [
    ('A. Ultrassom de espera longa, o resto em tomografia: TC de pescoço → TC de crânio → TC de face/seios',
     US_LONGA + ['02.06.01.005-2', '02.06.01.007-9', '02.06.01.004-4']),
    ('B. Ultrassom de espera longa, o resto em mamografia → densitometria',
     US_LONGA + ['02.04.03.018-8', '02.04.06.002-8']),
    ('C. Ultrassom de espera longa, o resto em ressonância: RM de crânio → RM de coluna lombo-sacra',
     US_LONGA + ['02.07.01.006-4', '02.07.01.004-8']),
    ('D. Só ultrassom: os de espera longa e os do mesmo código do plano 4 fora das filas dele, o resto em TC de pescoço → TC de crânio',
     US_LONGA + US_P4 + ['02.06.01.005-2', '02.06.01.007-9']),
]
print('\n## 3. Combinações (cada fila na ordem; quando uma zera, passa-se à próxima)\n')
print(f"Os cinco ultrassons de espera longa (pélvica, bolsa escrotal, globo ocular, "
      f"transfontanela, obstétrica com doppler) custam {br(base_us)} para zerar, {base_us / R:.0%} do recurso. "
      f"Toda combinação começa por eles; o que muda é onde vai o resto.")
print()
print('| combinação | cenário | o que atende | filas zeradas | exames | sobra |')
print('|---|---|---|---|---|---|')
for nome, cods in COMBOS:
    for rot, rec in CEN:
        partes = []; ex = 0; z = 0
        for c in cods:
            r = por[c]; at, p, rec = conta(r['fila'], r['v'], rec); ex += at
            if at == r['fila']: z += 1
            partes.append(f"{CURTO.get(c, r['desc'])}: " + ('zera' if at == r['fila'] else f"{n(at)} de {n(r['fila'])} ({p}%)"))
            if at < r['fila']: break
        print(f"| {nome} | {rot} | {'; '.join(partes)} | {z} | {n(ex)} | {br(rec)} |")
print('\nNa D, as filas do mesmo código do plano 4 trazem o risco de sobreposição: são os procedimentos que o plano 4 já paga ao ISHP.')

# 4. A combinação escolhida pelo usuário (A, 16/10/2026), com o preço de mercado de dados/precos.md
ESCOLHA = US_LONGA + ['02.06.01.005-2', '02.06.01.007-9', '02.06.01.004-4']
MAMO = '02.04.03.018-8'
ESCOLHA_A3 = ESCOLHA + [MAMO]   # usuário, 16/10/2026: "acho bom focarmos em mamografia"
FINAL = [MAMO] + ESCOLHA        # usuário, 16/10/2026: "mamografia primeiro: zera a mamografia e depois os ultrassons e as tomografias"
mercado = {}; npre = {}
sec = None
for l in open('dados/precos.md', encoding='utf-8'):
    if l.startswith('## '): sec = l[3]
    cel = [c.strip() for c in l.strip().strip('|').split('|')]
    if not re.match(r'\d{2}\.\d{2}\.\d{2}\.\d{3}-\d$', cel[0]): continue
    if sec == '4' and cel[2] == 'DF': npre[cel[0]] = int(cel[4])
    if sec == '5' and cel[1] == 'DF':
        num = lambda s: D(s.replace('R$', '').replace('.', '').replace(',', '.').strip())
        mercado[cel[0]] = (num(cel[3]), num(cel[4]), cel[5])
print('\n## 4. A combinação escolhida — mamografia primeiro, depois a combinação A, com o preço de mercado\n')
print('Escolhas do usuário em 16/10/2026 (`estado.yaml`). Mercado do DF e cobertura de `precos.md` (16/10/2026); '
      '"valor ÷ mediana" é CALCULADO aqui.\n')
print('| ordem | exame | fila | espera média | a rede zera em | valor | custo para zerar | mercado DF: mínimo / mediana (preços) | cobertura | valor ÷ mediana |')
print('|---|---|---|---|---|---|---|---|---|---|')
for i, c in enumerate(FINAL, 1):
    r = por[c]
    m = round(r['fila'] / r['ag']) if r['ag'] else None
    mo = '—' if m is None else ('1 mês' if m <= 1 else f'{m} meses')
    base = f"| {i} | {CURTO[c]} | {n(r['fila'])} | {r['espera_media']:.0f} dias | {mo} | {br(r['v'])} | {br(r['fila'] * r['v'])} | "
    if c[:14] not in mercado:
        print(base + 'a pesquisar | | |'); continue
    mn, md, cob = mercado[c[:14]]
    print(base + f"{br(mn)} / {br(md)} ({npre[c[:14]]}) | {cob} | {r['v'] / md:.0%} |")
def roda(cods, rec):
    partes = []; ex = 0; z = 0
    for c in cods:
        r = por[c]; at, p, rec = conta(r['fila'], r['v'], rec); ex += at
        if at == r['fila']: z += 1
        partes.append(f"{CURTO[c]}: " + ('zera' if at == r['fila'] else f"{n(at)} de {n(r['fila'])} ({p}%)"))
        if at < r['fila']: break
    return partes, z, ex, rec
OUTRAS_TC = [r['cod'] for r in sorted([r for r in cand if r['mod'] == 'tomografia' and r['v'] and r['cod'] not in ESCOLHA],
                                       key=lambda r: -r['espera_media'])]
for c in OUTRAS_TC: CURTO.setdefault(c, por[c]['desc'])
CURTO['02.05.02.014-3'] = 'US obstétrica'
custo_a = sum(por[c]['fila'] * por[c]['v'] for c in ESCOLHA)
custo_m = por[MAMO]['fila'] * por[MAMO]['v']
print(f"\nA mamografia vem primeiro e custa {br(custo_m)} para zerar ({custo_m / R:.0%} do recurso). O resto segue a ordem da "
      f"combinação A: os cinco ultrassons, depois TC de pescoço, de crânio e de face/seios. As outras variantes ficam como registro.")
print('\n| variante | cenário | filas zeradas | exames | onde para | sobra |')
print('|---|---|---|---|---|---|')
for nome, cods in [('**a escolhida: mamografia primeiro, depois a A**', FINAL),
                   ('A3. A → mamografia', ESCOLHA_A3),
                   ('A, sem a sobra', ESCOLHA),
                   ('A1. A + as outras tomografias (segmentos apendiculares, colunas, sela túrcica) → US obstétrica → mamografia',
                    ESCOLHA + OUTRAS_TC + ['02.05.02.014-3', '02.04.03.018-8']),
                   ('A2. A + os ultrassons do mesmo código do plano 4, fora das filas dele (doppler → tireoide → abdômen total → aparelho urinário)',
                    ESCOLHA + US_P4),
                   ]:
    for rot, rec in CEN:
        partes, z, ex, sobra = roda(cods, rec)
        print(f"| {nome} | {rot} | {z} | {n(ex)} | {partes[-1]} | {br(sobra)} |")
print('\nNa A2, as filas do mesmo código do plano 4 trazem o risco de sobreposição. As filas das variantes, fora da A, '
      'ainda não têm ficha nem preço.')
