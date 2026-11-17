import json, openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
SP='/private/tmp/claude-501/-Users-hendrick-Projetos-planos-ses/6e5ec242-e139-480f-b774-8edbf56d8f37/scratchpad/'
j=json.load(open(SP+'coleta_20261005.json')); rt=json.load(open(SP+'rateio_out.json'))
wb=openpyxl.Workbook(); B=Font(bold=True); H=PatternFill('solid',fgColor='DDEBF7')
def sheet(title,rows,head_rows=()):
    ws=wb.create_sheet(title)
    for r in rows: ws.append(list(r))
    for i in head_rows:
        for c in ws[i]: c.font=B; c.fill=H
    for col in ws.columns:
        ws.column_dimensions[col[0].column_letter].width=min(60,max(10,max(len(str(c.value or '')) for c in col)*0.9))
    return ws
wb.remove(wb.active)
sheet('0 · Leia-me',[
 ['Mapa Social da Saúde — recoleta dos procedimentos do plano 4 (ultrassonografia e tomografia)'],
 ['Painel','Mapa Social da Saúde – Regulamentação (MPDFT) · Lista de Espera – Exames e Consultas'],
 ['Endereço','https://paineis-ext.mpdft.mp.br/extensions/mapasauderegulamentacao/mapasauderegulamentacao.html'],
 ['App Qlik',j['app']+' · 7edb02fa-f1f5-4ea6-b348-049a4ac2d095'],
 ['Fonte declarada','SISREG/DATASUS'],
 ['Última recarga da base','05/10/2026 13:32:34 (BRT) — qLastReloadTime '+j['recarga_utc']],
 ['Data/hora da consulta',j['consulta']+' (relógio do motor)'],
 ['Extração','Qlik Engine API do próprio painel (evaluateEx e hipercubos de sessão), feita pelo Claude no navegador embutido. Sem leitura de tela, sem exportação pelos ícones.'],
 ['Recorte','Todos os anos. Cada procedimento entra fixo na expressão de conjunto {1<descrição_procedimento_solicitacao={...}>}, que ignora a seleção da tela.'],
 ['Medida "fila"','Count(Distinct {1<'+j['filtro_fila']+'>} contador_solicitacao) — a medida "Solicitações" do cabeçalho do painel'],
 ['Medida "total"','Count(Distinct {1} contador_solicitacao) — a medida dos gráficos do painel, inclui as devolvidas'],
 ['Pessoas','Count(Distinct {mesmo conjunto da fila} cns_usuario_solicitacao)'],
 ['Espera','Avg / Median / Max de tempo_espera_solicitacao, em dias, no conjunto indicado'],
 ['Regra','Abas 1 a 4: nenhum número calculado, todos saíram do motor. Aba 5 é CALCULADA a partir da aba 2 e das quantidades da planilha de 10/09/2026, e diz isso no título.'],
 ['Grafia','O nome interno da angiotomografia de coronárias tem um espaço não separável (U+00A0) seguido de espaço comum: "ANGIOTOMOGRAFIA\\u00a0 DAS ARTÉRIAS...". Busca com dois espaços comuns não acha.'],
],[1])
hd=['grupo','procedimento','nome interno no SISREG','SIGTAP','descrição SIGTAP','pessoas na fila','fila (Solicitações)','devolvidas','total (gráficos)','espera média fila','mediana fila','espera máx. fila','espera média total']
rows=[hd]+[[p['grupo'],p['nome'],p['nome_sisreg'],str(p['sigtap']).zfill(10),p['desc_sigtap'],p['pessoas'],p['fila'],p['devolvidas'],p['total'],round(p['espera_fila'],1),round(p['mediana_fila'],1),round(p['max_fila'],1),round(p['espera_total'],1)] for p in j['procedimentos']]
rows+=[[],['conjuntos (Avg recalculada pelo motor sobre os registros, não média das linhas)']]
for k,lab in (('US_objeto','US do objeto — 10 nomes + variante de parede'),('US_com_partes_moles','US com partes moles'),('TC_objeto','TC do objeto — 5 nomes')):
    c=j['conjuntos'][k]; rows.append(['',lab,'','','',c['pessoas'],c['fila'],c['devolvidas'],c['total'],round(c['espera_fila'],1),round(c['mediana_fila'],1),round(c['max_fila'],1),round(c['espera_total'],1)])
rows.append(['','Grupos 4 + 5 de tomografia inteiros','','','','',j['grupoTC']['fila'],'','',round(j['grupoTC']['espera'],1)])
sheet('1 · Procedimentos',rows,[1])
cols=j['regioes_cols']
sheet('2 · Região de Saúde',[['Região de Saúde da unidade solicitante × procedimento. Colunas sem prefixo: medida FILA. Colunas "TOTAL ...": medida dos gráficos, com devolvidas (só TC, para comparar com a coleta de 15/09).'],['Região']+cols]+[[ ('(sem região informada)' if r[0]=='-' else r[0]) ]+r[1:] for r in j['regioes']],[2])
idade=sorted(j['idade'],key=lambda x:int(x[0]))
sheet('3 · Idade',[['idade na solicitação','US do objeto (fila)','TC do objeto (fila)']]+[[int(a),b,c] for a,b,c in idade],[1])
sheet('4 · Risco',[['classificação de risco','US do objeto (fila)','TC do objeto (fila)']]+sorted(j['risco']),[1])
r5=[['CALCULADO — rateio entre polos, procedimento a procedimento: participação de cada polo entre as solicitações com Região de Saúde nomeada, aplicada à quantidade da planilha de 10/09/2026 (78.572), e somada. Mesmo método da seção 3.4; reproduz 39,69/29,94/30,37 com os dados de 15/09.'],
    ['polo','Regiões','tudo em fila (05/10)','exames','TC em total, como em 15/09 (05/10)','exames','plano v18 (15/09)','exames']]
old={'Ceilândia':(39.69,31183),'Sobradinho':(29.94,23527),'Gama':(30.37,23862)}
REG={'Ceilândia':'Oeste e Sudoeste','Sobradinho':'Norte, Leste e Central','Gama':'Sul e Centro-Sul'}
for k in ('Ceilândia','Sobradinho','Gama'): r5.append([k,REG[k],rt['fila'][k][0]/100,rt['fila'][k][1],rt['total'][k][0]/100,rt['total'][k][1],old[k][0]/100,old[k][1]])
ws=sheet('5 · Rateio (calculado)',r5,[2])
for row in ws.iter_rows(min_row=3,max_row=5):
    for c in (row[2],row[4],row[6]): c.number_format='0.00%'
wb.save('dados/fontes/mapa_social_20261005.xlsx'); print('ok')
