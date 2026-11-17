import json, openpyxl
from openpyxl.styles import Font, PatternFill
SP='/private/tmp/claude-501/-Users-hendrick-Projetos-planos-ses/1b35c3e0-b578-4271-a344-be72490288ae/scratchpad/'
rows=json.load(open(SP+'entr_rows.json')); j=json.load(open(SP+'entrantes_20261005.json'))
f='dados/fontes/mapa_social_20261005.xlsx'; wb=openpyxl.load_workbook(f)
for s in ['6 · Fila e pessoas','7 · Entrantes 2026','8 · Entrantes 2025','9 · Pessoas por código']:
    if s in wb.sheetnames: del wb[s]
B=Font(bold=True); H=PatternFill('solid',fgColor='DDEBF7')
def sheet(t,data,heads):
    ws=wb.create_sheet(t)
    for r in data: ws.append(list(r))
    for i in heads:
        for c in ws[i]: c.font=B; c.fill=H
    for col in ws.columns: ws.column_dimensions[col[0].column_letter].width=min(45,max(9,max(len(str(c.value or '')) for c in col)*0.9))
obj=rows[:15]
d=[['Fila e pessoas por nome de fila — medida FILA (3 status). Planilha = extração da SES-DF de 10/09/2026; 15/09 = coletas anteriores; 05/10 = esta coleta. Parede abdominal soma as duas grafias.'],
   ['procedimento','planilha 10/09','fila 15/09','fila 05/10','pessoas 15/09','pessoas 05/10']]
d+=[[r['nome'],r['plan'],r['s15'],r['f05'],r['p15'],r['p05']] for r in rows]
o=j['pess']['out']
d+=[[],['pessoas distintas nos conjuntos (CNS distintos, o motor desconta quem está em mais de uma fila)'],['conjunto','solicitações','pessoas','com 1 exame','com 2','com 3','com 4 ou mais']]
for k,lab in (('US','ultrassonografia do objeto'),('TC','tomografia do objeto'),('US_TC','objeto inteiro')):
    x=o[k]; d.append([lab,x['solic'],x['pessoas'],x['k1'],x['k2'],x['k3'],x['k4mais']])
d+=[[],['pessoas com TC de abdômen superior E TC de pelve na fila',j['pess']['combo_abdsup_e_pelve_mesma_pessoa']]]
sheet('6 · Fila e pessoas',d,[2,len(rows)+5])
pc=j['pess']['porCod']
sheet('9 · Pessoas por código',[['código SIGTAP','nomes de fila','solicitações na fila','pessoas distintas']]+[[k[:2]+'.'+k[2:4]+'.'+k[4:6]+'.'+k[6:9]+'-'+k[9] if len(k)==10 else ('0'+k)[:2]+'.'+('0'+k)[2:4]+'.'+('0'+k)[4:6]+'.'+('0'+k)[6:9]+'-'+('0'+k)[9],v['nomes'],v['solic'],v['pessoas']] for k,v in pc.items()],[1])
M26=['jan','fev','mar','abr','mai','jun','jul','ago','set']; M25=M26+['out','nov','dez']
nota='Entrantes = solicitações ainda abertas na tabela Solicitacao (pendentes + devolvidas) + solicitações que já saíram dela por agendamento (tabela de agendamentos), pela data da solicitação. Data da solicitação do agendado = data_agendamento − tempo_espera_agendamento, igual a Calendar.Data_Solicitacao. Solicitação cancelada antes de agendar não consta da base: é piso. Base com solicitações até 30/09/2026.'
d=[[ 'Entrantes 2026 (jan–set) por mês da solicitação. '+nota],['procedimento','Total de Solicitações Ano=2026 em 15/09 (só TC)','Total de Solicitações Ano=2026 hoje (abertas)','agendadas com solicitação em 2026','já realizadas','entrantes 2026','média mensal (÷9)']+M26]
d+=[[r['nome'],r['t15'],r['t05'],r['ag26'],r['real26'],r['e26'],round(r['mm26'],1)]+r['m26'] for r in rows]
d.append(['objeto (15 nomes)','',sum(r['t05'] for r in obj),sum(r['ag26'] for r in obj),sum(r['real26'] for r in obj),sum(r['e26'] for r in obj),round(sum(r['e26'] for r in obj)/9,1)]+[sum(r['m26'][i] for r in obj) for i in range(9)])
sheet('7 · Entrantes 2026',d,[2])
d=[['Entrantes 2025 (12 meses) por mês da solicitação. '+nota],['procedimento','abertas com solicitação em 2025','agendadas com solicitação em 2025','entrantes 2025','média mensal (÷12)']+M25]
d+=[[r['nome'],r['ab25'],r['ag25'],r['e25'],round(r['mm25'],1)]+r['m25'] for r in rows]
d.append(['objeto (15 nomes)',sum(r['ab25'] for r in obj),sum(r['ag25'] for r in obj),sum(r['e25'] for r in obj),round(sum(r['e25'] for r in obj)/12,1)]+[sum(r['m25'][i] for r in obj) for i in range(12)])
sheet('8 · Entrantes 2025',d,[2])
ws=wb['0 · Leia-me']
ws.append(['Abas 6 a 9','Acrescentadas na mesma sessão, consulta de 05/10/2026 14:58, mesma recarga da base. Entrantes somam duas tabelas do modelo; a soma é a única operação feita fora do motor.'])
wb.save(f); print(wb.sheetnames)
