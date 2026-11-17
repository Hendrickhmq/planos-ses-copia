import json
SP='/private/tmp/claude-501/-Users-hendrick-Projetos-planos-ses/1b35c3e0-b578-4271-a344-be72490288ae/scratchpad/'
SP0='/private/tmp/claude-501/-Users-hendrick-Projetos-planos-ses/6e5ec242-e139-480f-b774-8edbf56d8f37/scratchpad/'
j=json.load(open(SP+'entrantes_20261005.json')); c0=json.load(open(SP0+'coleta_20261005.json'))
norm=lambda s:' '.join(s.replace('\xa0',' ').split())
O={norm(r[0]):r[1:] for r in j['open']}; A={norm(r[0]):r[1:] for r in j['ag']}
# ordem, nome curto, planilha 10/09, 15/09 solic, 15/09 pessoas, 15/09 Total Ano=2026 (só TC)
L=[('Mama bilateral',14608,14396,14370,None),('Transvaginal',10481,10383,10382,None),('Abdômen total',9959,9912,9908,None),('Doppler MMII',9793,9824,9822,None),('Carótidas',4608,4537,4537,None),('Aparelho urinário',3921,3914,3914,None),('Tireoide',3195,3216,3216,None),('Próstata',3185,3243,3237,None),('Parede abdominal',3121,3143,3143,None),('Abdômen superior',2249,2276,2274,None),
   ('TC abdômen sup. c/contraste',4453,4467,4465,4447),('TC pelve c/contraste',3808,3836,3835,3723),('TC tórax c/contraste',3068,2987,2984,2873),('Angiotomografia de coronárias',1397,1409,1409,723),('TC tórax s/contraste',726,426,426,522),('Partes moles (fora)',2974,2992,2991,None)]
P={p['nome']:p for p in c0['procedimentos']}
P['Partes moles (fora)']=P['Partes moles (fora do objeto)']
rows=[]
for nome,plan,s15,p15,t15 in L:
    p=P[nome]; key=norm(p['nome_sisreg'])
    o=O[key]; a=A[key]
    f05=p['fila']+(P['Parede abdominal (variante)']['fila'] if nome=='Parede abdominal' else 0)
    pe05=p['pessoas']+(1 if nome=='Parede abdominal' else 0)
    e26=o[1]+a[1]; e25=o[0]+a[0]
    m26=[o[3+i]+a[3+i] for i in range(9)]; m25=[o[15+i]+a[15+i] for i in range(12)]
    rows.append(dict(nome=nome,plan=plan,s15=s15,f05=f05,p15=p15,p05=pe05,t15=t15,t05=o[1],ab25=o[0],ag26=a[1],ag25=a[0],e26=e26,e25=e25,mm26=e26/9,mm25=e25/12,m26=m26,m25=m25,real26=a[2]))
json.dump(rows,open(SP+'entr_rows.json','w'),ensure_ascii=False)
f=lambda x:f'{x:,.0f}'.replace(',','.')
print('nome | plan | 15/09 fila | 05/10 fila | pess15 | pess05 | T2026 15/09 | T2026 05/10 | entr26 | /mes26 | entr25 | /mes25 | ag26 realiz')
for r in rows: print(r['nome'],'|',f(r['plan']),'|',f(r['s15']),'|',f(r['f05']),'|',f(r['p15']),'|',f(r['p05']),'|',r['t15'],'|',f(r['t05']),'|',f(r['e26']),'|',f(r['mm26']),'|',f(r['e25']),'|',f(r['mm25']),'|',r['real26'])
for g,sl in (('US',slice(0,10)),('TC',slice(10,15)),('OBJ',slice(0,15))):
    R=rows[sl]; print(g,{k:sum(r[k] for r in R) for k in ('plan','s15','f05','t05','e26','e25')}, 'mm26',round(sum(r['e26'] for r in R)/9),'mm25',round(sum(r['e25'] for r in R)/12))
print('meses 2026 objeto:',[sum(r['m26'][i] for r in rows[:15]) for i in range(9)])
print('meses 2025 objeto:',[sum(r['m25'][i] for r in rows[:15]) for i in range(12)])
print('meses 2026 TC tórax s/c:',rows[14]['m26'])
