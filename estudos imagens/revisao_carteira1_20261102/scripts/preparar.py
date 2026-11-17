"""Extrai fontes preservadas, sem executar geradores antigos nem alterar o plano.
Uso: python3 scripts/preparar.py. Requer fontes_preservadas e versao_anterior.
"""
from pathlib import Path
import ast, json, math, hashlib, shutil
from collections import defaultdict
from openpyxl import load_workbook

ROOT=Path(__file__).resolve().parents[1]
ORIG=Path('/Users/hendrick/Projetos/planos-ses/planos/redacao_04')
F=ROOT/'fontes_preservadas'
V=ROOT/'versao_anterior'
# Copiar só na primeira execução. Manifesto torna a revisão reprodutível e rastreável.
if not (ROOT/'manifesto_fontes.json').exists():
    paths=list((ORIG/'estudos').glob('*20261102*'))+[ORIG/'estudos/README.md',ORIG/'estudos/estudo_polos_rede_capacidade_20261020.md',ORIG/'estudos/salas_ultrassom_metricas_20261020.xlsx',ORIG/'calculo_v19/calculo.py',ORIG/'calculo_v24/polos_capacidade.py',ORIG/'calculo_v24/polos_capacidade.json']
    paths+=list((ORIG/'dados/fontes').glob('mapa_social_20261102*'))+list((ORIG/'dados/fontes').glob('mapa_social_20261005*'))
    paths += [ORIG/'dados/fontes/sigtap_0205010040_102026.md',ORIG/'dados/conferencia_procedimentos.md']
    manifest=[]
    for src in paths:
        if not src.exists(): continue
        dest=(V/src.name) if src.parent.name=='estudos' and '20261102' in src.name else F/src.relative_to(ORIG)
        if src.is_dir(): shutil.copytree(src,dest,dirs_exist_ok=True)
        else:
            dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dest)
        for a in src.rglob('*') if src.is_dir() else [src]:
            if a.is_file():
                b=dest/a.relative_to(src) if src.is_dir() else dest
                manifest.append({'origem':str(a),'copia':str(b.relative_to(ROOT)),'sha256':hashlib.sha256(a.read_bytes()).hexdigest()})
    (ROOT/'manifesto_fontes.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))

old=json.loads((V/'estudo_filas_imagem_20261102.json').read_text())
raw=json.loads((F/'dados/fontes/mapa_social_20261102_imagem_bruto/coleta_20261102.json').read_text())
items=next(iter(old['cenarios'].values()))
# Ler todas as células da versão organizada, preservando o conteúdo para conferência.
w=load_workbook(V/'estudo_filas_imagem_20261102_organizada.xlsx',data_only=False)
(ROOT/'verificacao/leitura_planilha_anterior.json').write_text(json.dumps({s.title:list(s.values) for s in w},ensure_ascii=False,default=str))
tree=ast.parse((F/'calculo_v19/calculo.py').read_text())
R=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='R' for t in n.targets))
polos=json.loads((F/'calculo_v24/polos_capacidade.json').read_text())
regs=['Central','Centro-Sul','Leste','Norte','Oeste','Sudoeste','Sul']
def regional_key(i):
    c,n=i['codigo'],i['nome']
    if c=='02.05.01.004-0': return 'dop_mmii' if any(s in n for s in ['MMII','MMSS','MEMBRO']) else 'carotidas'
    keys={'02.05.02.004-6':'parede' if 'PAREDE' in n else 'abd_total','02.05.02.009-7':'mama','02.05.02.018-6':'transvag','02.05.02.005-4':'urinario','02.05.02.012-7':'tireoide','02.05.02.010-0':'prostata','02.05.02.003-8':'abd_sup','02.06.03.001-0':'tc_abd','02.06.03.003-7':'tc_pelve','02.06.02.003-1':'tc_torax_s' if i['minutos']==15 else 'tc_torax_c'}
    return keys.get(c)
def alloc(q,shares):
    a={r:math.floor(q*shares[r]) for r in regs}
    for r in sorted(regs,key=lambda r:q*shares[r]-a[r],reverse=True)[:q-sum(a.values())]: a[r]+=1
    return a
regional=[]
for j,i in enumerate(items):
    k=regional_key(i)
    if k:
        counts={r:R[k].get('Região '+r,0) for r in regs}; note='15/09/2026, fila US; total de solicitações TC. Proxy por família.'
    else:
        counts={r:polos['R']['us' if i['modalidade']=='Ultrassom' else 'tc'][r] for r in regs};note='Sem regional por protocolo. Proxy do mix antigo de 20/10 (base 15/09).'
    shares={r:counts[r]/sum(counts.values()) for r in regs}
    a=alloc(i['meta'],shares)
    for r in regs:
        regional.append({'item':j+1,'regiao':r,'polo': 'Asa Sul' if r in ['Central','Centro-Sul'] else {'Sudoeste':'Samambaia','Sul':'Gama','Leste':'São Sebastião','Norte':'Sobradinho','Oeste':'Ceilândia'}[r], 'meta':a[r],'share':shares[r],'familia':k or 'mix antigo da modalidade','nota':note})

# Cada par nome/código recebe um recorte explícito, inclusive os excluídos.
codes=sorted({i['codigo'] for i in items})
invent=[]
for f in old['filas']:
    eligible=0
    reason=f['motivo']
    if f['codigo'] in codes and f['cobertura'] in ['livre','parcial'] and 'angio coronária' not in f['protocolo']:
        eligible=f['fila']
        if f['codigo']=='02.05.02.018-6': eligible=f['fila']*(1-4000/9295);reason='Reserva fixa total de 4.000 transvaginais. Rateio proporcional entre nomes só para modelar.'
        elif f['codigo']=='02.06.03.003-7': eligible=f['fila']*(1-7/5944);reason='Desconto legado de 7/5.944 por CID, aproximação pendente. Não é fronteira de elegibilidade.'
        else: reason='Elegível no estudo. Enquadramento da parede pendente.' if 'PAREDE' in f['nome'] else 'Elegível no estudo.'
    invent.append({**f,'elegivel':eligible,'regra':reason or 'Fora do recorte da carteira 1.'})

rumo={r['codigo']:r for r in raw['rumo']}
flows=[]
for c in codes:
    fs=[f for f in invent if f['codigo']==c]
    rr=rumo[c]; stock=sum(f['elegivel'] for f in fs);allstock=sum(f['fila'] for f in fs)
    agenda=sum(f['agendadas_12m'] or 0 for f in fs if f['elegivel']>0)
    # Reserva do IEV não é desconto permanente do fluxo. Fração aplicada aqui é premissa explícita.
    agenda_adj=sum((f['agendadas_12m'] or 0)*(f['elegivel']/f['fila'] if f['fila'] else 0) for f in fs)
    flows.append({'codigo':c,'estoque':stock,'estoque_codigo':allstock,'entrantes_codigo':rr['entrantes_12m'],'agendados_codigo':rr['oferta_12m'],'realizados_codigo':rr['realizados_12m'],'faltas_codigo':rr['faltas_12m'],'agenda_nomes':agenda_adj,'fracao_estoque':stock/allstock if allstock else 0,'meta':sum(i['meta'] for i in items if i['codigo']==c)})

# Cenários independentes por protocolo, como solicitado. Rateios são hipóteses, não séries medidas.
protocols=[]
for f in invent:
    if f['elegivel']<=0: continue
    matches=[i for i in items if i['codigo']==f['codigo'] and i['nome'].split(' — pedidos novos')[0]==f['nome']]
    rr=rumo[f['codigo']]; fl=next(x for x in flows if x['codigo']==f['codigo'])
    protocols.append({'codigo':f['codigo'],'nome':f['nome'],'estoque':f['elegivel'],'meta':sum(i['meta'] for i in matches),'minutos':f['minutos'],'fracao_entrada':f['elegivel']/fl['estoque_codigo'],'entrada_mes':rr['entrantes_12m']/12*f['elegivel']/fl['estoque_codigo'],'producao_mes':(f['agendadas_12m'] or 0)/12*(f['elegivel']/f['fila'] if f['fila'] else 0)*rr['realizados_12m']/rr['oferta_12m'] if rr['oferta_12m'] else 0,'agenda_12m':f['agendadas_12m'],'real_ag_cod':rr['realizados_12m']/rr['oferta_12m'] if rr['oferta_12m'] else 0})
assert sum(x['meta'] for x in protocols)==79219
assert sum(x['meta'] for x in items)==79219
assert round(sum(x['valor'] for x in items),2)==10636506.41
assert not any('angio coronária' in i['protocolo'] for i in items)
assert not any(i['codigo']=='02.05.02.006-2' for i in items)
data={'items':items,'regional':regional,'flows':flows,'protocols':protocols,'invent':invent,'raw_region':{k:v['dimensoes'].get('regiao') for k,v in raw['panorama'].items() if k in ['ultrassonografia','tomografia']},'series':raw['por_codigo'],'dates':raw['datas'],'source_manifest':json.loads((ROOT/'manifesto_fontes.json').read_text())}
(ROOT/'dados_revisao.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
print('Itens:',len(items),'Protocolos elegíveis:',len(protocols),'Estoque elegível:',round(sum(x['estoque'] for x in flows),2))
for months in [8,7]:
    hs=defaultdict(float)
    for r in regional:
        i=items[r['item']-1]
        if i['modalidade']=='Ultrassom': hs[r['polo']]+=r['meta']*i['minutos']/60
    for f in [0,.2,.3]:
        print(months,'meses, faltas',f,{p:math.ceil(h/(months*21*10*.8*(1-f))) for p,h in hs.items()},'total',sum(math.ceil(h/(months*21*10*.8*(1-f))) for h in hs.values()))
