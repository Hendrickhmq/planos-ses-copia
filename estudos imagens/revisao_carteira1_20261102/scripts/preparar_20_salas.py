"""Rearranjo da carteira mantida em 20 salas de US; não altera estudos anteriores."""
from pathlib import Path
from collections import defaultdict
import json,math,itertools
P=Path(__file__).resolve().parents[1]
d=json.loads((P/'dados_revisao.json').read_text())
polos=['Asa Sul','São Sebastião','Sobradinho','Ceilândia','Samambaia','Gama']
hours={p:sum(r['meta']*d['items'][r['item']-1]['minutos']/60 for r in d['regional'] if r['polo']==p and d['items'][r['item']-1]['modalidade']=='Ultrassom') for p in polos}
cap=8*21*10*.8*(1-.2)/(1-.2*.8)
bestload=float('inf');best=[]
for cuts in itertools.combinations(range(1,20),5):
    a=[y-x for x,y in zip((0,)+cuts,cuts+(20,))]
    load=max(hours[p]/n for p,n in zip(polos,a))
    if load<bestload-1e-8:bestload=load;best=[a]
    elif abs(load-bestload)<1e-8:best.append(a)
assert best==[[3,3,2,1,6,5]]
# Distribuição minimiza o maior número de horas assistenciais por sala antes de remanejar.
# Em seguida, o remanejo equilibra a carga por sala de Norte e Central.
balance=(3*hours['Sobradinho']-2*hours['Asa Sul'])/5
move=round(balance/(40/60));assert move==504
records=[]
for r in d['regional']:
    i=d['items'][r['item']-1]
    if i['modalidade']!='Ultrassom':continue
    nr={**r,'codigo':i['codigo'],'nome':i['nome'],'minutos':i['minutos'],'horas':r['meta']*i['minutos']/60}
    if r['regiao']=='Norte' and i['nome']=='ULTRA-SONOGRAFIA DOPPLER VENOSO - MMII ( BILATERAL)':
        assert r['meta']>=move
        nr['meta']-=move;nr['horas']=nr['meta']*i['minutos']/60
        records.append({**nr,'polo':'Asa Sul','meta':move,'horas':move*40/60,'remanejo':True})
    records.append(nr)
codes=[]
for f in d['flows']:
    items=[i for i in d['items'] if i['codigo']==f['codigo']]
    ps=[p for p in d['protocols'] if p['codigo']==f['codigo']]
    name=items[0]['descricao_candanga']
    if f['codigo']=='02.05.01.004-0':name='Doppler: carótidas, membros e outros territórios selecionados'
    if f['codigo']=='02.05.02.004-6':name='Abdômen total, incluindo parede abdominal'
    if f['codigo']=='02.06.02.003-1':name='TC de tórax, sem angio coronária'
    deficits=[]
    for t in [0,.5,1]:
        deficits.append(sum(max(0,p['meta']-max(0,p['estoque']+p['entrada_mes']*8-p['producao_mes']*8*(1-t))) for p in ps))
    codes.append({**f,'nome':name,'modalidade':items[0]['modalidade'],'valor':sum(i['valor'] for i in items),'horas':sum(i['meta']*i['minutos']/60 for i in items),'deficits':deficits,'filas':sum(p['meta']>0 for p in ps)})
protocols=[]
for p in d['protocols']:
    if not p['meta']:continue
    f=next(f for f in d['invent'] if f['codigo']==p['codigo'] and f['nome']==p['nome'])
    protocols.append({**p,'fila_bruta':f['fila'],'fila_viva':f['fila_viva'],'devolvidas':f['devolvidas'],'espera_mediana':f['espera_mediana'],'regra':f['regra']})
out={'polos':polos,'salas':best[0],'horas_origem':hours,'records':records,'codes':codes,'protocols':protocols,'maior_carga_sala_antes_remanejo':bestload,'dopplers_remanejados':move,'arranjos_comparados':math.comb(19,5),'data_coleta':d['dates']['recarga'],'data_ultima_solicitacao':d['dates']['solicitacao_mais_recente']}
(P/'dados_plano_20_salas.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
print('Arranjos comparados:',out['arranjos_comparados'],'salas:',best,'remanejo proposto (exames):',move)
for p,n in zip(polos,best[0]):
    h=sum(r['horas'] for r in records if r['polo']==p)
    q=sum(r['meta'] for r in records if r['polo']==p)
    print(p,n,q,round(h,2),'utilização',round(h/(n*cap)*100,2))
assert sum(p['meta'] for p in protocols)==79219
assert sum(r['meta'] for r in records)==64915
assert math.isclose(sum(r['horas'] for r in records),23906.166666666668)
