import pdfplumber, re, json
from pathlib import Path
from collections import Counter

root=Path('/Users/hendrick/Projetos/planos-ses/estudos imagens')
rows=[]
audit=[]
with pdfplumber.open('/Users/hendrick/Downloads/TABELA SUS CANGANGA OFICIAL.pdf') as pdf:
    for n,page in enumerate(pdf.pages,1):
        tables=page.extract_tables()
        current=[]
        for table in tables:
            for cells in table:
                cells=[re.sub(r'\s+',' ',c or '').strip() for c in cells]
                if cells[0]=='Código': continue
                if len(cells)!=4 or not re.fullmatch(r'\d{10}',cells[0]):
                    raise ValueError((n,cells))
                code,desc,mode,value=cells
                assert desc and mode and re.fullmatch(r'R\$ [\d.]+,\d{2}',value),(n,cells)
                current.append([code,desc,mode,float(value.replace('R$ ','').replace('.','').replace(',','.')),n])
        text=page.extract_text()
        codes=re.findall(r'(?<!\d)\d{10}(?!\d)',text)
        assert Counter(codes)==Counter(r[0] for r in current),(n,len(codes),len(current))
        money=re.findall(r'R\$\s*([\d.]+,\d{2})',text)
        assert Counter(round(float(v.replace('.','').replace(',','.'))*100) for v in money)==Counter(round(r[3]*100) for r in current),n
        rows.extend(current)
        audit.append({'page':n,'records':len(current)})
        print(n,len(current),flush=True)
data={'rows':rows,'audit':audit,'modalities':dict(Counter(r[2] for r in rows))}
(root/'tmp/conversao/data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
print('TOTAL',len(rows),'MODALITIES',data['modalities'],'DUPLICATE CODES',[(c,n) for c,n in Counter(r[0] for r in rows).items() if n>1])
