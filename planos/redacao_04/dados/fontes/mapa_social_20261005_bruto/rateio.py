import json, openpyxl
SP='/private/tmp/claude-501/-Users-hendrick-Projetos-planos-ses/6e5ec242-e139-480f-b774-8edbf56d8f37/scratchpad/'
POLO={'Região Oeste':'Ceilândia','Região Sudoeste':'Ceilândia','Região Norte':'Sobradinho','Região Leste':'Sobradinho','Região Central':'Sobradinho','Região Sul':'Gama','Região Centro-Sul':'Gama'}
PLAN={'Mama bilateral':14608,'Transvaginal':10481,'Abdômen total':9959,'Doppler MMII':9793,'Carótidas':4608,'Aparelho urinário':3921,'Tireoide':3195,'Próstata':3185,'Parede abdominal':3121,'Abdômen superior':2249,
 'TC abdômen sup. c/contraste':4453,'TC pelve c/contraste':3808,'TC tórax c/contraste':3068,'Angiotomografia de coronárias':1397,'TC tórax s/contraste':726}
assert sum(PLAN.values())==78572
def rateio(dist):  # dist: proc -> {regiao: n}
    tot={'Ceilândia':0,'Sobradinho':0,'Gama':0}; per={}
    for p,q in PLAN.items():
        d={k:0 for k in tot}
        for r,n in dist[p].items():
            if r in POLO: d[POLO[r]]+=n
        s=sum(d.values()); per[p]={k:(d[k]/s if s else 0) for k in d}
        for k in tot: tot[k]+=q*per[p][k]
    T=sum(tot.values()); return {k:(round(v/T*100,2), round(v)) for k,v in tot.items()}, per
# --- antigo (15/09)
wb=openpyxl.load_workbook('dados/fontes/validacao_ultrassom_20260915.xlsx',data_only=True)
mapnome={'ECOGRAFIA DE MAMAS - BILATERAL':'Mama bilateral','ECOGRAFIA TRANSVAGINAL':'Transvaginal','ECOGRAFIA DE ABDOMEN TOTAL ADULTO':'Abdômen total','ULTRA-SONOGRAFIA DOPPLER VENOSO - MMII ( BILATERAL)':'Doppler MMII','10. ECODOPPLER DE CAROTIDAS':'Carótidas','ECOGRAFIA DO APARELHO URINARIO (RINS, BEXIGA) ADULTO':'Aparelho urinário','ECOGRAFIA DE TIREOIDE ADULTO':'Tireoide','ECOGRAFIA DE PROSTATA ( VIA ABDOMINAL )':'Próstata','ULTRASONOGRAFIA DE PAREDE ABDOMINAL':'Parede abdominal','ULTRA-SONOGRAFIA DE PAREDE ABDOMINAL':'Parede abdominal','ECOGRAFIA DE ABDOMEN SUPERIOR ADULTO':'Abdômen superior'}
old={p:{} for p in PLAN}
for r in wb['2 · Região de Saúde'].iter_rows(min_row=3,values_only=True):
    if r[0] in mapnome and isinstance(r[2],(int,float)):
        d=old[mapnome[r[0]]]; d[r[1]]=d.get(r[1],0)+r[2]
wb2=openpyxl.load_workbook('dados/fontes/mapa_social_tomografia_20260915.xlsx',data_only=True)
tcn=['TC abdômen sup. c/contraste','TC pelve c/contraste','TC tórax c/contraste','Angiotomografia de coronárias','TC tórax s/contraste']
for r in wb2['4-Regiao'].iter_rows(min_row=3,values_only=True):
    if r[0] and isinstance(r[1],(int,float)):
        for i,p in enumerate(tcn): old[p][r[0]]=r[1+i]
print('ANTIGO (15/09, TC em Total de Solicitações):', rateio(old)[0])
# --- novo (05/10)
j=json.load(open(SP+'coleta_20261005.json'))
cols=j['regioes_cols']
def dist(colmap):
    d={p:{} for p in PLAN}
    for row in j['regioes']:
        reg=row[0]
        for p,c in colmap.items():
            for cc in c: d[p][reg]=d[p].get(reg,0)+row[1+cols.index(cc)]
    return d
base={p:[p] for p in PLAN}; base['Parede abdominal']=['Parede abdominal','Parede abdominal (variante)']
novo_fila=dist(base)
novo_total=dist({**base, **{p:['TOTAL '+p] for p in tcn}})
rf,perf=rateio(novo_fila); rt,pert=rateio(novo_total)
print('NOVO 05/10, TC em Total (mesmo método antigo):', rt)
print('NOVO 05/10, tudo em fila:', rf)
print('\nTC por procedimento, fila vs total (Ceil/Sobr/Gama):')
for p in tcn: print(p, {k:round(v*100,1) for k,v in perf[p].items()}, {k:round(v*100,1) for k,v in pert[p].items()})
# TC only rateio
tcq=sum(PLAN[p] for p in tcn)
for lab,per in (('fila',perf),('total',pert)):
    t={k:sum(PLAN[p]*per[p][k] for p in tcn) for k in ('Ceilândia','Sobradinho','Gama')}
    print('TC só,',lab,{k:(round(v/tcq*100,2),round(v)) for k,v in t.items()})
json.dump({'fila':rf,'total':rt},open(SP+'rateio_out.json','w'),ensure_ascii=False)
