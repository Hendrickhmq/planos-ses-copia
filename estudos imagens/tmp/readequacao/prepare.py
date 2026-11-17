import json,re
from pathlib import Path
from decimal import Decimal
import openpyxl
root=Path.cwd()
src=root/'outputs/plano4-mapeamento-20261102/Plano 4 - procedimentos filas e nomenclaturas.xlsx'
w=openpyxl.load_workbook(src,data_only=True)
d=json.loads((root/'tmp/plano4/data.json').read_text())
assert [(r[0],r[1],r[2]) for r in list(w['Plano 4'].values)[9:20]]==[(p['code'],p['name'],p['target']) for p in d['procs']]
assert [(r[0],r[1],r[3],r[4]) for r in list(w['Filas escolhidas'].values)[7:22]]==[(f['id'],f['original'],f['code'],f['base']) for f in d['filas']]
cand=openpyxl.load_workbook(root/'Tabela SUS Candanga.xlsx',data_only=True).active
rows=[dict(code=str(r[0]),name=r[1],mod=r[2],price=r[3],page=r[4],row=i) for i,r in enumerate(cand.values,1) if i>6]
def norm(c):return re.sub(r'\D','',c)
state=(root/'../planos/redacao_04/estado.yaml').read_text()
for p in d['procs']:
 matches=[r for r in rows if r['code']==norm(p['code']) and r['mod']=='SIA'];assert len(matches)==1
 p['cand']=matches[0]
 p['old_price']=float(re.search('"'+re.escape(p['code'])+'"[^\n]+unitario: ([0-9.]+)',state).group(1))
for f in d['filas']:
 f['pending']=f['id'] in ['F09','F14']
 p=next(p for p in d['procs'] if p['code']==f['code']);f['cand']=p['cand'];f['old_price']=p['old_price']
 f['status']='Validar enquadramento' if f['pending'] else 'Correspondência compatível'
 f['protocol']='Preservar nome e protocolo da fila na agenda e no laudo.'
 if f['id']=='F09':f['protocol']='Parede abdominal não tem item específico localizado na tabela. Código de abdômen total é candidato herdado do painel; requer confirmação SES-DF antes de contratar/faturar. Não substituir por articulação por semelhança.'
 if f['id']=='F14':f['protocol']='Angiotomografia de coronárias não tem item específico localizado na tabela. TC de tórax é candidato herdado do painel; requer confirmação SES-DF do protocolo e enquadramento antes de contratar/faturar.'
 if f['id'] in ['F04','F05']:f['protocol']='Manter território vascular e bilateralidade no subitem da agenda. O item publicado é genérico. Não multiplicar unidades por vaso/lado sem regra de registro validada.'
 if f['id'] in ['F11','F12','F13','F15']:f['protocol']='Preservar adulto, uso ou ausência de contraste e ausência de sedação. A descrição publicada não separa estes protocolos. Nenhum adicional foi presumido.'
codes={norm(p['code']) for p in d['procs']}
d['reference']=[r for r in rows if r['mod']=='SIA' and (r['code'] in codes or r['code'].startswith(('020501','020502','020601','020602','020603')))]
old=sum(Decimal(str(p['old_price']))*p['target'] for p in d['procs'])
new=sum(Decimal(str(p['cand']['price']))*p['target'] for p in d['procs'])
assert old==Decimal('10636542.52')
d['totals']=dict(old=float(old),new=float(new),delta=float(new-old),pending_base=sum(f['base'] for f in d['filas'] if f['pending']),pending_29=sum(f['fila29'] for f in d['filas'] if f['pending']))
(root/'tmp/readequacao/data.json').write_text(json.dumps(d,ensure_ascii=False,indent=2))
print(d['totals'])
