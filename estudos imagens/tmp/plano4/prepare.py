import csv, json, re
from pathlib import Path
from collections import Counter
import openpyxl
from docx import Document

root=Path('/Users/hendrick/Projetos/planos-ses')
p=root/'planos/redacao_04'
f=p/'dados/fontes'
dest=Path(__file__).parent
def norm(s): return ' '.join(str(s).split())
def integer(s): return int(str(s).replace('.',''))
doc=Document(p/'plano.docx')
t=next(t for t in doc.tables if [c.text for c in t.rows[0].cells]==['código','procedimento','exames'])
procs=[dict(code=r.cells[0].text,name=r.cells[1].text,target=integer(r.cells[2].text)) for r in t.rows[1:] if r.cells[0].text]
codes={r['code'] for r in procs}
catalog=list(csv.DictReader((root/'registros/mapa_social/imagem/catalogo_20261029.csv').open(encoding='utf-8-sig'),delimiter=';'))
catalog=[dict(r,source_row=i) for i,r in enumerate(catalog,2) if r['codigo_formatado'] in codes]
wb=openpyxl.load_workbook(f/'mapa_social_20261006.xlsx',data_only=True)
base=list(wb['6 · Fila e pessoas'].values)[2:17]
details=list(wb['1 · Procedimentos'].values)[1:18]
original=list(openpyxl.load_workbook(f/'filas_ultrassom_tomografia_20260915.xlsx',data_only=True)['Exames de imagem'].values)
orig_by_qty={int(r[1]):(r[0],i) for i,r in enumerate(original,1) if isinstance(r[1],(int,float)) and r[0]}
orig_by_qty.pop(68094,None)
source_rows={r[1]:i for i,r in enumerate(wb['1 · Procedimentos'].values,1) if r[1]}
filas=[]
for i,r in enumerate(base,1):
    ds=[d for d in details if d[1]==r[0] or (r[0]=='Parede abdominal' and d[1]=='Parede abdominal (variante)')]
    assert ds
    rawcode=ds[0][3]
    code=f'{rawcode[:2]}.{rawcode[2:4]}.{rawcode[4:6]}.{rawcode[6:9]}-{rawcode[9]}'
    matches=[c for c in catalog if c['codigo_formatado']==code and norm(c['nome']) in {norm(d[2]) for d in ds}]
    assert len(matches)==len(ds),(r[0],len(matches),len(ds))
    original_name,original_row=orig_by_qty[int(r[1])]
    relation='Variação de redação entre fila e procedimento do plano.'
    kind='Redação / qualificadores'
    if r[0]=='Doppler MMII':
        kind='Enquadramento em nome genérico'; relation='Doppler venoso bilateral de membros inferiores sob Doppler colorido de vasos; compartilha código com carótidas. Exames de territórios diferentes.'
    elif r[0]=='Carótidas':
        kind='Enquadramento em nome genérico'; relation='Ecodoppler de carótidas sob Doppler colorido de vasos; compartilha código com Doppler venoso de MMII. Não são sinônimos clínicos.'
    elif r[0]=='Parede abdominal':
        kind='Enquadramento em outra denominação'; relation='Parede abdominal vinculada ao código de abdômen total no painel. Duas grafias na fonte; a base de 10/09 não separa o quantitativo por grafia.'
    elif r[0]=='Abdômen total':
        kind='Código compartilhado'; relation='Adulto consta da fila; o mesmo código também agrega a parede abdominal escolhida no plano.'
    elif r[0]=='Angiotomografia de coronárias':
        kind='Enquadramento em outra denominação'; relation='Angiotomografia de artérias coronárias vinculada no painel ao código de TC de tórax; protocolo específico preservado no nome da fila.'
    elif r[0].startswith('TC tórax'):
        kind='Protocolos sob o mesmo código'; relation='Tórax com e sem contraste e angiotomografia de coronárias compartilham código; contraste e sedação não aparecem na denominação do plano.'
    elif r[0].startswith('TC '):
        kind='Redação / protocolo'; relation='Fila explicita adulto, com contraste e sem sedação. O plano usa denominação do procedimento por código.'
    filas.append(dict(id=f'F{i:02}',short=r[0],original=original_name,code=code,base=int(r[1]),fila15=r[2],fila6=r[4],fila29=sum(int(c['fila']) for c in matches),names=[c['nome'] for c in matches],kind=kind,relation=relation,source_original=f'S2: Exames de imagem!A{original_row}:B{original_row}',source_mapping='S3: 1 · Procedimentos, linhas '+', '.join(str(source_rows[d[1]]) for d in ds),source_catalog='S4: CSV, linhas '+', '.join(str(c['source_row']) for c in matches)))
selected={(c['code'],n) for c in filas for n in c['names']}
for c in catalog:
    c['selected']='Fila escolhida' if (c['codigo_formatado'],c['nome']) in selected else 'Outro nome do mesmo código'
    c['fila']=int(c['fila']) if c['fila']!='' else None
    c['devolvidas']=int(c['devolvidas']) if c['devolvidas']!='' else None
    c['space_note']=''
    if '\u00a0' in c['nome']: c['space_note']='Contém espaço não separável U+00A0.'
    elif '  ' in c['nome']: c['space_note']='Contém espaços duplos.'
    if c['selected']!='Fila escolhida':
        c['interpretation']='Mesmo código, sem inclusão automática no plano. Pode haver outro território, idade ou protocolo.'
    elif c['nome']=='ULTRA-SONOGRAFIA DE PAREDE ABDOMINAL': c['interpretation']='Variante de grafia de parede abdominal confirmada nas coletas.'
    else: c['interpretation']='Nome correspondente a uma das 15 filas de origem selecionadas.'
catalog.sort(key=lambda r:(next(i for i,p in enumerate(procs) if p['code']==r['codigo_formatado']),r['selected']!='Fila escolhida',-(r['fila'] or 0),r['nome']))
for r in procs:
    fs=[x for x in filas if x['code']==r['code']]
    cs=[x for x in catalog if x['codigo_formatado']==r['code']]
    r.update(base=sum(x['base'] for x in fs),filas=[x['short'] for x in fs],aliases=len(cs),active=sum((x['fila'] or 0)>0 for x in cs))
    if len(fs)>1: r['relation']='Agrupa '+str(len(fs))+' filas de origem distintas.'
    else: r['relation']='Uma fila selecionada; há outros nomes cadastrados no mesmo código.'
    r['state']=int(re.search('"'+re.escape(r['code'])+'"[^\n]+exames: (\\d+)',(p/'estado.yaml').read_text()).group(1))
assert len(procs)==11 and len(filas)==15 and len(catalog)==228 and len(selected)==16
assert sum(r['target'] for r in procs)==79144
assert sum(r['base'] for r in filas)==78572
assert sum(r['target']-r['base'] for r in procs)==572
assert len({(r['nome'],r['codigo_formatado']) for r in catalog})==228
out=dict(procs=procs,filas=filas,catalog=catalog,root=str(root),plan=str(p),fontes=str(f),selected_pairs=len(selected))
(dest/'data.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
print(json.dumps(dict(procedimentos=len(procs),filas=len(filas),pares_escolhidos=len(selected),catalogo=len(catalog),com_fila=sum((r['fila'] or 0)>0 for r in catalog),meta=sum(r['target'] for r in procs),base=sum(r['base'] for r in filas),fila29=sum(r['fila29'] for r in filas),estado_soma=sum(r['state'] for r in procs)),ensure_ascii=False))
