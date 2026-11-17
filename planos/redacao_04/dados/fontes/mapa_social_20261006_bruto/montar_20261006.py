# Monta ../mapa_social_20261006.xlsx a partir de coleta_20261006.json e dev_20261006.json,
# com a coleta de 05/10 (../mapa_social_20261005_bruto) como comparação.
import json, openpyxl
from openpyxl.styles import Font, PatternFill
H0='../mapa_social_20261005_bruto/'
j=json.load(open('coleta_20261006.json')); dv=json.load(open('dev_20261006.json'))
j5=json.load(open(H0+'coleta_20261005.json')); e5=json.load(open(H0+'entr_rows.json'))
norm=lambda s:' '.join(s.replace('\xa0',' ').split())
POLO={'Região Oeste':'Ceilândia','Região Sudoeste':'Ceilândia','Região Norte':'Sobradinho','Região Leste':'Sobradinho','Região Central':'Sobradinho','Região Sul':'Gama','Região Centro-Sul':'Gama'}
PLAN={'Mama bilateral':14608,'Transvaginal':10481,'Abdômen total':9959,'Doppler MMII':9793,'Carótidas':4608,'Aparelho urinário':3921,'Tireoide':3195,'Próstata':3185,'Parede abdominal':3121,'Abdômen superior':2249,
 'TC abdômen sup. c/contraste':4453,'TC pelve c/contraste':3808,'TC tórax c/contraste':3068,'Angiotomografia de coronárias':1397,'TC tórax s/contraste':726}
TCN=list(PLAN)[10:]
# ---- rateio na fila (método da 3.4)
cols=j['regioes_cols']
def dist(jj):
    c=jj['regioes_cols']; d={p:{} for p in PLAN}
    for row in jj['regioes']:
        for p in PLAN:
            cc=[p]+(['Parede abdominal (variante)'] if p=='Parede abdominal' else [])
            d[p][row[0]]=sum(row[1+c.index(x)] for x in cc)
    return d
def rateio(d):
    tot={'Ceilândia':0,'Sobradinho':0,'Gama':0}
    for p,qv in PLAN.items():
        s={k:0 for k in tot}
        for r,n in d[p].items():
            if r in POLO: s[POLO[r]]+=n
        S=sum(s.values())
        for k in tot: tot[k]+=qv*s[k]/S
    T=sum(tot.values()); return {k:(round(v/T*100,2),round(v)) for k,v in tot.items()}
R6=rateio(dist(j)); R5=rateio(dist(j5))
# ---- entrantes
O={norm(r[0]):r[1:] for r in j['open']}; A={norm(r[0]):r[1:] for r in j['ag']}
P={p['nome']:p for p in j['procedimentos']}
rows=[]
for x5 in e5:
    nome=x5['nome']; key=P['Partes moles (fora do objeto)' if nome.startswith('Partes') else nome]
    k=norm(key['nome_sisreg']); o=O[k]; a=A[k]
    f06=key['fila']+(P['Parede abdominal (variante)']['fila'] if nome=='Parede abdominal' else 0)
    p06=key['pessoas']+(P['Parede abdominal (variante)']['pessoas'] if nome=='Parede abdominal' else 0)
    e26=o[1]+a[1]; e25=o[0]+a[0]
    rows.append(dict(nome=nome,plan=x5['plan'],s15=x5['s15'],f05=x5['f05'],f06=f06,p05=x5['p05'],p06=p06,t15=x5['t15'],t05=x5['t05'],t06=o[1],ab25=o[0],ag26=a[1],ag25=a[0],e26=e26,e25=e25,e26_05=x5['e26'],e25_05=x5['e25'],
        m26=[o[3+i]+a[3+i] for i in range(9)],m25=[o[15+i]+a[15+i] for i in range(12)],real26=a[2],esp05=None,esp06=key['espera_fila']))
json.dump(rows,open('entr_rows_20261006.json','w'),ensure_ascii=False)
E5={p['nome']:p for p in j5['procedimentos']}
# ---- planilha
wb=openpyxl.Workbook(); wb.remove(wb.active); B=Font(bold=True); H=PatternFill('solid',fgColor='DDEBF7')
def sheet(t,data,heads=(),pct=None):
    ws=wb.create_sheet(t)
    for r in data: ws.append(list(r))
    for i in heads:
        for c in ws[i]: c.font=B; c.fill=H
    for col in ws.columns: ws.column_dimensions[col[0].column_letter].width=min(55,max(9,max(len(str(c.value or '')) for c in col)*0.9))
    return ws
sheet('0 · Leia-me',[
 ['Mapa Social da Saúde — recoleta de 06/10/2026 dos procedimentos do plano 4 (ultrassonografia e tomografia)'],
 ['Painel','Mapa Social da Saúde – Regulamentação (MPDFT) · Lista de Espera – Exames e Consultas'],
 ['Endereço','https://paineis-ext.mpdft.mp.br/extensions/mapasauderegulamentacao/mapasauderegulamentacao.html'],
 ['App Qlik','D-PDDC - MAPA DA SAÚDE - REGULAÇÃO (M) · 7edb02fa-f1f5-4ea6-b348-049a4ac2d095'],
 ['Fonte declarada','SISREG/DATASUS'],
 ['Última recarga da base','06/10/2026 21:32:49 (BRT) — qLastReloadTime '+j['recarga_utc']],
 ['Data/hora da consulta',j['consulta']+' (relógio do motor)'],
 ['Solicitação mais recente na base',j['max_data_solicitacao']+' — o mesmo de 05/10: a recarga atualiza status, não traz solicitações de outubro'],
 ['Extração','Qlik Engine API do próprio painel (evaluateEx e hipercubos de sessão), pelo Claude no navegador embutido. Sem leitura de tela, sem exportação pelos ícones.'],
 ['Recorte','Todos os anos. Cada procedimento entra fixo na expressão de conjunto {1<descrição_procedimento_solicitacao={...}>}, que ignora a seleção da tela.'],
 ['Medida "fila"','Count(Distinct {1<'+j['filtro_fila']+'>} contador_solicitacao) — a medida "Solicitações" do cabeçalho do painel'],
 ['Medida "total"','Count(Distinct {1} contador_solicitacao) — a medida dos gráficos do painel, inclui as devolvidas'],
 ['Pessoas','Count(Distinct {mesmo conjunto da fila} cns_usuario_solicitacao)'],
 ['Entrantes','abertas (tabela Solicitacao, por Ano/Mês da solicitação) + agendadas (tabela de agendamentos, data da solicitação = data_agendamento − tempo_espera_agendamento). Piso: cancelada antes de agendar não consta.'],
 ['Regra','Abas 1 a 4, 6, 9 e 10: números do motor. Abas 5, 7, 8 e 11 somam ou ponderam números do motor e dizem isso no título.'],
 ['Grafia','Angiotomografia de coronárias: espaço não separável (U+00A0) seguido de espaço comum no nome interno.'],
 ['Mesmo método de','mapa_social_20261005.xlsx; brutos e script em mapa_social_20261006_bruto/'],
],[1])
hd=['grupo','procedimento','nome interno no SISREG','SIGTAP','descrição SIGTAP','pessoas na fila','fila (Solicitações)','devolvidas','total (gráficos)','espera média fila','mediana fila','espera máx. fila','espera média total']
d=[hd]+[[p['grupo'],p['nome'],norm(p['nome_sisreg']),str(p['sigtap']).zfill(10),p['desc_sigtap'],p['pessoas'],p['fila'],p['devolvidas'],p['total'],round(p['espera_fila'],1),round(p['mediana_fila'],1),round(p['max_fila'],1),round(p['espera_total'],1)] for p in j['procedimentos']]
d+=[[],['conjuntos (média recalculada pelo motor sobre os registros)']]
for k,lab in (('US_objeto','US do objeto — 10 nomes + variante de parede'),('US_com_partes_moles','US com partes moles'),('TC_objeto','TC do objeto — 5 nomes')):
    c=j['conjuntos'][k]; d.append(['',lab,'','','',c['pessoas'],c['fila'],c['devolvidas'],c['total'],round(c['espera_fila'],1),round(c['mediana_fila'],1),round(c['max_fila'],1),round(c['espera_total'],1)])
d.append(['','Grupos 4 + 5 de tomografia inteiros','','','','',j['grupoTC']['fila'],'','',round(j['grupoTC']['espera'],1)])
sheet('1 · Procedimentos',d,[1])
sheet('2 · Região de Saúde',[['Região de Saúde da unidade solicitante × procedimento. Sem prefixo: medida FILA. "TOTAL ...": medida dos gráficos, com devolvidas (só TC).'],['Região']+cols]+[[('(sem região informada)' if r[0]=='-' else r[0])]+r[1:] for r in j['regioes']],[2])
sheet('3 · Idade',[['idade na solicitação','US do objeto (fila)','TC do objeto (fila)']]+[[int(a),b,c] for a,b,c in sorted(j['idade'],key=lambda x:int(x[0]))],[1])
sheet('4 · Risco',[['classificação de risco','US do objeto (fila)','TC do objeto (fila)']]+sorted(j['risco']),[1])
REG={'Ceilândia':'Oeste e Sudoeste','Sobradinho':'Norte, Leste e Central','Gama':'Sul e Centro-Sul'}
old={'Ceilândia':(39.69,31183),'Sobradinho':(29.94,23527),'Gama':(30.37,23862)}
d=[['CALCULADO — rateio entre polos na medida da fila, procedimento a procedimento, aplicado às quantidades da planilha de 10/09/2026 (78.572). Método da seção 3.4.'],['polo','Regiões','06/10','exames','05/10','exames','plano v18 (15/09)','exames']]
for k in REG: d.append([k,REG[k],R6[k][0]/100,R6[k][1],R5[k][0]/100,R5[k][1],old[k][0]/100,old[k][1]])
ws=sheet('5 · Rateio (calculado)',d,[2])
for r in ws.iter_rows(min_row=3,max_row=5):
    for c in (r[2],r[4],r[6]): c.number_format='0.00%'
obj=rows[:15]; o=j['pess']['out']
d=[['Fila e pessoas por nome de fila — medida FILA. Parede abdominal soma as duas grafias.'],['procedimento','planilha 10/09','fila 15/09','fila 05/10','fila 06/10','pessoas 05/10','pessoas 06/10']]
d+=[[r['nome'],r['plan'],r['s15'],r['f05'],r['f06'],r['p05'],r['p06']] for r in rows]
d+=[[],['pessoas distintas nos conjuntos'],['conjunto','solicitações','pessoas','com 1 exame','com 2','com 3','com 4 ou mais']]
for k,lab in (('US','ultrassonografia do objeto'),('TC','tomografia do objeto'),('US_TC','objeto inteiro')):
    x=o[k]; d.append([lab,x['solic'],x['pessoas'],x['k1'],x['k2'],x['k3'],x['k4mais']])
d+=[[],['pessoas com TC de abdômen superior E TC de pelve na fila',j['pess']['combo_abdsup_e_pelve_mesma_pessoa']]]
sheet('6 · Fila e pessoas',d,[2,len(rows)+5])
M26=['jan','fev','mar','abr','mai','jun','jul','ago','set']; M25=M26+['out','nov','dez']
d=[['CALCULADO — entrantes 2026 (jan–set) = abertas + agendadas, por mês da solicitação.'],['procedimento','Total Ano=2026 (abertas) 05/10','Total Ano=2026 (abertas) 06/10','agendadas com solicitação em 2026','já realizadas','entrantes 2026','média mensal (÷9)','entrantes 2026 em 05/10']+M26]
d+=[[r['nome'],r['t05'],r['t06'],r['ag26'],r['real26'],r['e26'],round(r['e26']/9,1),r['e26_05']]+r['m26'] for r in rows]
d.append(['objeto (15 nomes)',sum(r['t05'] for r in obj),sum(r['t06'] for r in obj),sum(r['ag26'] for r in obj),sum(r['real26'] for r in obj),sum(r['e26'] for r in obj),round(sum(r['e26'] for r in obj)/9,1),sum(r['e26_05'] for r in obj)]+[sum(r['m26'][i] for r in obj) for i in range(9)])
sheet('7 · Entrantes 2026',d,[2])
d=[['CALCULADO — entrantes 2025 = abertas + agendadas, por mês da solicitação.'],['procedimento','abertas com solicitação em 2025','agendadas com solicitação em 2025','entrantes 2025','média mensal (÷12)','entrantes 2025 em 05/10']+M25]
d+=[[r['nome'],r['ab25'],r['ag25'],r['e25'],round(r['e25']/12,1),r['e25_05']]+r['m25'] for r in rows]
d.append(['objeto (15 nomes)',sum(r['ab25'] for r in obj),sum(r['ag25'] for r in obj),sum(r['e25'] for r in obj),round(sum(r['e25'] for r in obj)/12,1),sum(r['e25_05'] for r in obj)]+[sum(r['m25'][i] for r in obj) for i in range(12)])
sheet('8 · Entrantes 2025',d,[2])
pc=j['pess']['porCod']
fmt=lambda k:(lambda z:f'{z[:2]}.{z[2:4]}.{z[4:6]}.{z[6:9]}-{z[9]}')(str(k).zfill(10))
sheet('9 · Pessoas por código',[['código SIGTAP','nomes de fila','solicitações na fila','pessoas distintas']]+[[fmt(k),v['nomes'],v['solic'],v['pessoas']] for k,v in pc.items()],[1])
c=dv['cols']; R=dv['rows']
d=[['Devolvidas para complementação, por nome de fila. "por ano de solicitação" = Ano_Solicitacao; "devolvidas em" = Year(data_devolucao). "pessoas também na fila" = CNS com devolvida E solicitação em fila no MESMO nome.'],
   ['procedimento','fila','devolvidas','pessoas com devolvida','pessoas também na fila','espera média devolvidas','espera mediana devolvidas','devolvidas solicitadas em 2025','devolvidas solicitadas em 2026','fila solicitada em 2025','fila solicitada em 2026','devolvidas em 2026','devolvidas até 2023']]
g=lambda r,k:r[1+c.index(k)]
for r in R: d.append([r[0],g(r,'fila'),g(r,'dev'),g(r,'dev_pessoas'),g(r,'ov'),g(r,'dev_esp_media'),g(r,'dev_esp_mediana'),g(r,'dev2025'),g(r,'dev2026'),g(r,'fila2025'),g(r,'fila2026'),g(r,'dev_em_2026'),g(r,'dev_ate_2023')])
S=lambda k:sum(g(r,k) for r in R)
d.append(['objeto (15 nomes)',S('fila'),S('dev'),dv['devPessObj'],f"{dv['ovObj']:,} em qualquer fila do objeto".replace(',','.'),'','',S('dev2025'),S('dev2026'),S('fila2025'),S('fila2026'),S('dev_em_2026'),S('dev_ate_2023')])
sheet('10 · Devolvidas',d,[2])
# ---- comparação
d=[['CALCULADO — 06/10 contra 05/10 (recarga das 13:32) e contra a planilha de 10/09.'],['procedimento','planilha 10/09','fila 05/10','fila 06/10','Δ fila','pessoas 05/10','pessoas 06/10','espera 05/10','espera 06/10','entrantes 2026 em 05/10','entrantes 2026 em 06/10','Δ entrantes']]
for r in rows:
    k='Partes moles (fora do objeto)' if r['nome'].startswith('Partes') else r['nome']
    d.append([r['nome'],r['plan'],r['f05'],r['f06'],r['f06']-r['f05'],r['p05'],r['p06'],round(E5[k]['espera_fila'],1),round(P[k]['espera_fila'],1),r['e26_05'],r['e26'],r['e26']-r['e26_05']])
for lab,sl in (('ultrassonografia',slice(0,10)),('tomografia',slice(10,15)),('objeto',slice(0,15))):
    X=rows[sl]; d.append([lab]+[sum(x[k] for x in X) for k in ('plan','f05','f06')]+[sum(x['f06']-x['f05'] for x in X),'','','','',sum(x['e26_05'] for x in X),sum(x['e26'] for x in X),sum(x['e26']-x['e26_05'] for x in X)])
sheet('11 · Comparação (calculado)',d,[2])
wb.save('../mapa_social_20261006.xlsx')
print('rateio 06/10',R6,'\nrateio 05/10',R5)
for lab,sl in (('US',slice(0,10)),('TC',slice(10,15)),('OBJ',slice(0,15))):
    X=rows[sl]; print(lab,{k:sum(x[k] for x in X) for k in ('plan','f05','f06','p05','p06','t05','t06','e26_05','e26','e25_05','e25')})
print('meses26',[sum(r['m26'][i] for r in obj) for i in range(9)])
print('dev',S('fila'),S('dev'),dv['devPessObj'],dv['ovObj'])
print(wb.sheetnames)
