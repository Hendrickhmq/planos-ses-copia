from pathlib import Path
import json,openpyxl
root=Path('/Users/hendrick/Projetos/planos-ses/estudos imagens')
candanga=openpyxl.load_workbook(root/'outputs/tabela-sus-candanga/Tabela SUS Candanga.xlsx',read_only=True,data_only=True)
portaria=openpyxl.load_workbook(root/'outputs/portaria-4282/Portaria 4282 exames de imagem.xlsx',read_only=True,data_only=True)
base=list(candanga['Imagens ambulatoriais'].iter_rows(min_row=7,values_only=True))
items=list(portaria['Procedimentos'].iter_rows(min_row=7,values_only=True))
assert len({r[0] for r in base})==len(base)
assert len({r[0] for r in items})==len(items)
p={r[0]:r for r in items}
rows=[]
for code,description,mode,price,page,category in base:
    assert mode=='SIA'
    match=p.get(code)
    status='Sim' if match else 'Não localizado'
    textstatus=('Idêntica' if description==match[2] else 'Texto diferente') if match else 'Não se aplica'
    rows.append([code,description,page,status,match[2] if match else None,textstatus,category])
assert len(rows)==223
assert sum(r[3]=='Sim' for r in rows)==91
assert sum(r[5]=='Idêntica' for r in rows)==76
assert sum(r[5]=='Texto diferente' for r in rows)==15
(root/'tmp/conversao/comparison-data.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
print('Prepared',len(rows),'records: 91 code matches, 132 absent; 76 identical descriptions, 15 different descriptions.')
