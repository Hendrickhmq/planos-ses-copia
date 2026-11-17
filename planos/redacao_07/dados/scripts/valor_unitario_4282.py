"""Lê o Anexo I da Portaria SAES/MS 4.282/2026 (código, nome, valor SIGTAP, incremento) do texto do PDF.

Uso: pdftotext -layout "biblioteca/normas/SAES 4282-2026 rol imagem e incremento.pdf" p4282.txt
     python3 -I valor_unitario_4282.py p4282.txt anexo1.json
Gerou, em 15/10/2026, a tabela de dados/valor_unitario.md (101 procedimentos; conferida nos onze do plano 4).
"""
import sys, re, json
txt = open(sys.argv[1], encoding='utf-8').read().split('\n')
ini = next(i for i,l in enumerate(txt) if l.strip()=='ANEXO I')
fim = next(i for i,l in enumerate(txt) if l.strip()=='ANEXO II')
ents = []
for l in txt[ini:fim]:
    s = l.strip()
    if not s: continue
    m = re.match(r'(\d{2}\.\d{2}\.\d{2}\.\d{3}-)(\d)?(\s+.*)?$', s)
    if m:
        ents.append({'cod': m.group(1) + (m.group(2) or ''), 'txt': [(m.group(3) or '').strip()]})
        continue
    md = re.match(r'(\d)(\s+(.*))?$', s)
    if md and ents and len(ents[-1]['cod']) == 13:
        ents[-1]['cod'] += md.group(1); s = (md.group(3) or '')
    if ents: ents[-1]['txt'].append(s)
out = []
for e in ents:
    t = ' '.join(e['txt'])
    v = re.search(r'(\d{1,3}(?:\.\d{3})*,\d{2})', t); p = re.search(r'(\d+%|N/A)', t)
    nome = re.sub(r'R\$|\d{1,3}(?:\.\d{3})*,\d{2}|\d+%|N/A', '', t); nome = re.sub(r'\s+', ' ', nome).strip()
    out.append({'codigo': e['cod'], 'nome': nome, 'valor_tabela': float(v.group(1).replace('.','').replace(',','.')) if v else None, 'incremento': p.group(1) if p else None})
json.dump(out, open(sys.argv[2], 'w'), ensure_ascii=False, indent=1)
bad = [o for o in out if len(o['codigo']) != 14 or o['valor_tabela'] is None or o['incremento'] is None]
print('entradas', len(out), 'problemas', len(bad))
for o in bad: print(o)
