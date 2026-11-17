from html.parser import HTMLParser
from pathlib import Path
import re,json

class Tables(HTMLParser):
    def __init__(self):
        super().__init__(); self.tables=[]; self.table=None; self.row=None; self.cell=None
    def handle_starttag(self,tag,attrs):
        if tag=='table': self.table=[]
        if tag=='tr' and self.table is not None:self.row=[]
        if tag in ('td','th') and self.row is not None:self.cell=[]
        if tag in ('br','p') and self.cell is not None:self.cell.append(' ')
    def handle_data(self,data):
        if self.cell is not None:self.cell.append(data)
    def handle_endtag(self,tag):
        if tag in ('td','th') and self.cell is not None:
            self.row.append(re.sub(r'\s+',' ',''.join(self.cell)).strip());self.cell=None
        if tag=='tr' and self.row is not None:self.table.append(self.row);self.row=None
        if tag=='table' and self.table is not None:self.tables.append(self.table);self.table=None

root=Path('/Users/hendrick/Projetos/planos-ses/estudos imagens/tmp/conversao')
p=Tables();p.feed((root/'conass4282.html').read_text())
tables=p.tables[:8]
for i,t in enumerate(tables):print('TABLE',i,'ROWS',len(t),'FIRST',t[:1])
(root/'portaria-tables.json').write_text(json.dumps(tables,ensure_ascii=False,indent=2))
records={}
for row in tables[0][1:]+tables[1]:
    code,name,val,inc=row
    assert re.fullmatch(r'\d{2}\.\d{2}\.\d{2}\.\d{3}-\d',code),row
    assert code not in records,code
    records[code]={'code':code,'name':name,'base':float(val.replace('R$','').replace('.','').replace(',','.').strip()),'increment':float(inc[:-1])/100 if inc.endswith('%') else inc,'newValue':None,'annexes':['I']}
for table in tables[2:4]:
    code,name=table[0][1].split(' – ',1)
    value=next(r[1] for r in table if r[0]=='Valor do Serviço Ambulatorial')
    records[code]={'code':code,'name':name,'base':None,'increment':'Não informado','newValue':float(value.replace('R$','').replace('.','').replace(',','.').strip()),'annexes':['II']}
for row in tables[4]+tables[5]+tables[6]:
    if row[0] in ('CÓDIGO',''):continue
    code,name,*_=row
    assert code in records,(code,name)
    if 'III' not in records[code]['annexes']:records[code]['annexes'].append('III')
print('UNIQUE',len(records),'I',sum('I' in r['annexes'] for r in records.values()),'II',sum('II' in r['annexes'] for r in records.values()),'III',sum('III' in r['annexes'] for r in records.values()))
# Annex IV repeats principal and contrast procedures, with two malformed codes in the original.
# Preserve those source rows verbatim for traceability rather than inventing extra procedures.
(root/'portaria-records.json').write_text(json.dumps(list(records.values()),ensure_ascii=False,indent=2))
