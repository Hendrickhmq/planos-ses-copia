import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const d=JSON.parse(await fs.readFile(path.join(root,'dados_plano_20_salas.json'),'utf8'));
const wb=Workbook.create();
const ns=['Plano em 20 salas','Exames e metas','Filas atendidas','Agenda e absenteismo','Encaminhamento SES'];
const S=Object.fromEntries(ns.map(n=>[n,wb.worksheets.add(n)]));
const blue='#203F64',ink='#233449';let id=0;
function col(n){let a='';while(n){n--;a=String.fromCharCode(65+n%26)+a;n=Math.floor(n/26);}return a;}
function val(n,c,v){S[n].getRange(c).values=[[v]];}
function form(n,c,f){S[n].getRange(c).formulas=[[f]];}
function merged(n,r,text,bold=false,fill){const q=S[n].getRange(r);q.merge();q.values=[[text]];q.format.wrapText=true;q.format.font={name:'Arial',size:11,bold,color:ink};if(fill)q.format.fill=fill;return q;}
function base(n,title,widths){const s=S[n];s.showGridLines=false;const end=col(widths.length);s.getRange(`A1:${end}6`).format.font={name:'Arial',size:11,color:ink};widths.forEach((w,i)=>s.getRangeByIndexes(0,i,1,1).format.columnWidth=w);merged(n,`A2:${end}2`,title,true).format.font.size=16;s.getRange(`A3:${end}3`).format.borders={bottom:{style:'thin',color:'#91A4BB'}};s.tabColor=n==='Plano em 20 salas'?blue:undefined;}
function table(n,row,heads,rows,widths,height=32){const s=S[n],last=row+rows.length,end=col(heads.length);s.getRange(`A${row}:${end}${last}`).values=[heads,...rows];s.getRange(`A${row}:${end}${last}`).format.font={name:'Arial',size:11,color:ink};s.getRange(`A${row}:${end}${last}`).format.verticalAlignment='center';s.getRange(`A${row}:${end}${last}`).format.rowHeight=height;s.getRange(`A${row}:${end}${row}`).format={fill:blue,font:{name:'Arial',size:10,bold:true,color:'#FFFFFF'},wrapText:true,rowHeight:62,horizontalAlignment:'center'};widths.forEach((w,i)=>s.getRangeByIndexes(row-1,i,1,1).format.columnWidth=w);const t=s.tables.add(`A${row}:${end}${last}`,true,`Plano20Tabela${++id}`);t.style='TableStyleLight9';s.freezePanes.freezeRows(row);return last;}
function fmt(n,r,f){S[n].getRange(r).setNumberFormat(f);}
function section(n,r,t,end){merged(n,`A${r}:${end}${r}`,t,true).format.borders={bottom:{style:'thin',color:'#91A4BB'}};}
const N=ns[0],E=ns[1],F=ns[2],A=ns[3],R=ns[4];
base(A,'Agenda e absenteísmo — metas operacionais',[43,20,111]);
table(A,5,['Parâmetro','Valor','Significado'],[
 ['Meses de produção',8,'Referência atual; alternativa de prazo exige decisão posterior.'],
 ['Dias úteis por mês',21,'Premissa de calendário. Sem sábados; feriados devem ser compensados dentro da jornada.'],
 ['Horas de funcionamento por dia',10,'Limite definido pelo usuário. Sem extensão de jornada no modelo.'],
 ['Parcela do tempo para agenda',.8,'8 das 10 horas para agendar exames; 2 horas de margem operacional. Tempos dos exames preservados.'],
 ['Faltas brutas no planejamento',.2,'Hipótese do projeto. Histórico SES é maior em vários exames. Não é taxa já alcançada.'],
 ['Tempo perdido recuperado: meta',.8,'Meta operacional a validar: recuperar 80% dos minutos das tentativas frustradas por substituições efetivamente realizadas.'],
 ['Perda líquida: meta proposta',null,'f × (1 − r) ÷ (1 − f × r). O tempo reutilizado ocupa uma única vaga física. Medir minutos, não apenas contatos.'],
],[43,20,111],43);
form(A,'B12','=B10*(1-B11)/(1-B10*B11)');fmt(A,'B9:B12','0.0%');
S[A].getRange('B6:B11').format.fill='#FFF1CC';
merged(A,'A15:C16','A meta de recuperar 80% do tempo perdido NÃO é capacidade comprovada. Sem essa recuperação, a carteira não cabe em 20 salas em oito meses. Contato ou reagendamento, por si só, não recuperam tempo de sala.',true,'#FFF1CC');
section(A,18,'O que muda quando a falta aumenta','C');
table(A,19,['Falta bruta','Perda líquida com recuperação-meta','Recuperação mínima para cumprir o polo mais carregado'],[.2,.25,.3,.4,.43].map(f=>[f,null,null]),[43,35,96]);
for(let r=20;r<=24;r++){
 form(A,`B${r}`,`=A${r}*(1-$B$11)/(1-A${r}*$B$11)`);
 form(A,`C${r}`,`=MAX(0,(1-($B$6*$B$7*$B$8*$B$9)*(1-A${r})/MAX('Plano em 20 salas'!$G$12:$G$17))/A${r})`);
}
fmt(A,'A20:C24','0.0%');
section(A,27,'Como operar as vagas — proposta a pactuar','C');
table(A,28,['Quando','Ação','Como comprovar'],[
 ['Antes de abrir a agenda','Receber pedidos da regulação','Conferir ID da solicitação, protocolo, elegibilidade e ausência de vínculo com outro convênio.'],
 ['Até 3 dias antes','Contato e orientação','Confirmar disponibilidade e transmitir o preparo indicado pela equipe; identificar cancelamentos antecipados.'],
 ['Na véspera','Confirmação e lista de reposição','Com autorização da regulação, convocar suplentes elegíveis do mesmo protocolo para vagas liberadas.'],
 ['No dia','Repor vaga somente se houver tempo','Realizar o exame completo no tempo previsto. Não sobrepor pacientes nem presumir chegada imediata do suplente.'],
 ['Após a falta','Registrar e pedir reagendamento','Vincular nova tentativa ao mesmo pedido. Destino e retorno dependem do fluxo acordado com a SES.'],
 ['Toda semana, por polo/protocolo','Medir faltas e minutos recuperados','Registrar faltas brutas, exames de reposição efetivamente feitos, perda líquida, realizados e laudos.'],
 ['Se a perda líquida passar de 5%','Revisar a agenda com a regulação','A folga é pequena. Se passar de 6,4% no polo limitante, rever o prazo; não manter promessa de produção sem capacidade.'],
],[29,49,96],56);
merged(A,'A38:C39','Pessoas únicas, pedidos, tentativas, faltas, reagendamentos e realizações são contagens diferentes. A meta é de exames realizados. Uma falta ou um reagendamento não cria um pedido novo; baixa administrativa não conta como resolução assistencial.');
section(A,41,'Histórico de faltas da SES — referência, não previsão do projeto','C');
table(A,42,['Exame','Faltas históricas SES','Uso na gestão'],d.codes.map(c=>[c.nome,c.faltas_codigo/(c.realizados_codigo+c.faltas_codigo),'Priorizar confirmação e acompanhamento. Taxa agregada por código, não pelo protocolo elegível.']),[53,25,96],43);
fmt(A,`B43:B${42+d.codes.length}`,'0.0%');

const codes=[...d.codes].sort((a,b)=>a.codigo.localeCompare(b.codigo));
base(E,'Quais exames faremos e quanto precisamos produzir',[22,68,20,22,24,19,18,20,19,21]);
merged(E,'A4:J4','Carteira 1 mantida. Quantidades são exames realizados; TC usa rede específica e não ocupa as 20 salas de US.');
const ee=table(E,6,['Código','Exame / recorte','Modalidade','Fila total do código','Fila elegível estimada','Meta de exames','Média por mês','Tentativas com 20% faltas','Meta acima do estoque','Procedimentos (R$)'],codes.map(c=>[c.codigo,c.nome,c.modalidade,c.estoque_codigo,c.estoque,c.meta,null,null,null,c.valor]),[22,68,20,22,24,19,18,24,23,23],44);
for(let r=7;r<=ee;r++){
 form(E,`G${r}`,`=F${r}/'Agenda e absenteismo'!$B$6`);
 form(E,`H${r}`,`=ROUNDUP(F${r}/(1-'Agenda e absenteismo'!$B$10),0)`);
 form(E,`I${r}`,`=MAX(0,F${r}-E${r})`);
}
const et=ee+1;val(E,`B${et}`,'TOTAL');for(const c of ['D','E','F','G','H','I','J'])form(E,`${c}${et}`,`=SUM(${c}7:${c}${ee})`);
S[E].getRange(`A${et}:J${et}`).format.fill='#DEE8F2';S[E].getRange(`A${et}:J${et}`).format.font.bold=true;
fmt(E,`D7:F${et}`,'#,##0.0');fmt(E,`F7:F${et}`,'#,##0');fmt(E,`G7:G${et}`,'#,##0.0');fmt(E,`H7:H${et}`,'#,##0');fmt(E,`I7:I${et}`,'#,##0.0');fmt(E,`J7:J${et}`,'"R$ "#,##0.00');S[E].getRange(`B7:B${ee}`).format.wrapText=true;
merged(E,`A${et+3}:J${et+4}`,'Fila total inclui protocolos excluídos. A fila elegível desconta emergência, sedação, angio e reservas conforme o estudo completo. São pedidos da coleta de 02/11/2026, com solicitações até 28/10. Não é estoque garantido para o início.');
merged(E,`A${et+6}:J${et+7}`,'Meta acima do estoque mostra o complemento mínimo entre códigos; ainda é preciso descontar atendimento da rede e pactuar encaminhamento. Não são pedidos novos por absenteísmo. Somar tetos por código pode gerar mais tentativas que arredondar só o total.');
merged(E,`A${et+9}:J${et+10}`,'Parede abdominal: 3.304 exames mantidos, com confirmação de enquadramento e faturamento pela SES. Articulação excluída e 4.000 transvaginais reservadas ao IEV. Valores preservados, sem revisão de custos.');

base(F,'Quais filas vamos atender — 47 filas com meta',[22,93,21,25,19,24,15,24,24]);
merged(F,'A4:I4','Nomes exatos do Mapa Social. A meta reúne o estoque escolhido e os complementos planejados da mesma fila.');
const pr=[...d.protocols].sort((a,b)=>a.codigo.localeCompare(b.codigo)||b.meta-a.meta);
const fe=table(F,6,['Código','Nome exato da fila','Pedidos na coleta','Elegíveis estimados','Meta realizada','Meta acima do estoque','Min/exame','Tentativas com 20% faltas','Devolvidas separadas'],pr.map(p=>[p.codigo,p.nome,p.fila_bruta,p.estoque,p.meta,null,p.minutos,null,p.devolvidas]),[22,93,21,25,19,24,15,26,25],48);
for(let r=7;r<=fe;r++){form(F,`F${r}`,`=MAX(0,E${r}-D${r})`);form(F,`H${r}`,`=ROUNDUP(E${r}/(1-'Agenda e absenteismo'!$B$10),0)`);}
S[F].getRange(`B7:B${fe}`).format.wrapText=true;fmt(F,`C7:D${fe}`,'#,##0.0');fmt(F,`E7:E${fe}`,'#,##0');fmt(F,`F7:F${fe}`,'#,##0.0');fmt(F,`H7:I${fe}`,'#,##0');
val(F,`B${fe+1}`,'TOTAL DAS METAS');form(F,`E${fe+1}`,`=SUM(E7:E${fe})`);form(F,`H${fe+1}`,`=SUM(H7:H${fe})`);
merged(F,`A${fe+3}:I${fe+4}`,'Coleta: 02/11/2026 às 10h31. Última solicitação: 28/10. Devolvidas não são subtraídas da fila. Elegibilidade da pelve e distribuição proporcional da reserva transvaginal são aproximações explícitas do estudo.');
merged(F,`A${fe+6}:I${fe+7}`,'Outros nomes elegíveis sem meta específica ficam apenas como reserva para eventual remanejamento regulado. O total elegível por código pode, por isso, ser maior que o estoque destas 47 filas. Não somar pessoas como se fossem únicas.');

base(R,'Como a SES precisa encaminhar a demanda',[22,67,21,23,25,26,25,25,25]);
merged(R,'A4:I5','Cenários de oito meses a partir da coleta, por protocolo, consolidados por código. Fluxos elegíveis são rateios, não séries medidas por protocolo. A parte da oferta atribuível à SES ainda precisa ser confirmada.');
const re=table(R,7,['Código','Exame','Meta','Estoque elegível','Entradas elegíveis 8m (proxy)','Déficit: oferta habitual','Déficit: encaminhar 50%','Déficit: concentrar recorte','Providência'],codes.map(c=>[c.codigo,c.nome,c.meta,c.estoque,codes.find(x=>x.codigo===c.codigo).entrantes_codigo/12*c.fracao_estoque*8,...c.deficits,'Pactuar quantidade mensal e oferta que permanece na rede.']),[22,67,21,23,25,26,25,25,73],46);
S[R].getRange(`B8:B${re}`).format.wrapText=true;S[R].getRange(`I8:I${re}`).format.wrapText=true;fmt(R,`C8:H${re}`,'#,##0.0');
for(const c of ['C','D','E','F','G','H'])form(R,`${c}${re+1}`,`=SUM(${c}8:${c}${re})`);val(R,`B${re+1}`,'TOTAL');
merged(R,`A${re+3}:I${re+4}`,'Transferir oferta SES não cria demanda adicional. Déficit é insuficiência de exames no protocolo sob aquela divisão da oferta, não necessidade comprovada de pedidos novos. A concentração integral só sustenta o mix nas hipóteses usadas.');
merged(R,`A${re+6}:I${re+7}`,'Na hipótese inicial, 100% da produção habitual elegível é tratada como transferível: é um teto, não fato medido. Preservar oferta de outros convênios e recalcular quando a SES informar sua parcela real. Emergências não entram na transferência.');
merged(R,`A${re+9}:I${re+10}`,'Antes de iniciar: recoletar estoque por protocolo; confirmar parede; separar oferta própria de outros convênios; aprovar lista de reposição, reagendamentos e não sobreposição com IEV; pactuar encaminhamento mensal e remanejamentos.');

base(N,'Carteira 1 — execução em até 20 salas',[28,23,12,18,18,18,23,24,24]);
merged(N,'A4:I4','Somente dias úteis, 10 horas/dia e sem sábados. As 20 salas são de US; tomógrafos devem ser confirmados em rede específica.',true);
merged(N,'A6:C6','Meta realizada: 79.219 exames',true,'#EEF3F8');merged(N,'D6:F6','64.915 US + 14.304 TC',true,'#EEF3F8');merged(N,'G6:I6','Procedimentos: R$ 10.636.506,41',true,'#EEF3F8');
merged(N,'A8:I9','O melhor arranjo de salas está abaixo. Cumprir a carteira em oito meses depende de recuperar tempo perdido em vagas: falta bruta de 20% exige recuperar pelo menos 72,7% dessa perda no polo limitante. A meta operacional proposta é 80%, ainda não medida.',true,'#FFF1CC');
const regions=['Central + Centro-Sul','Leste','Norte','Oeste','Sudoeste','Sul'];
const nr=d.polos.map((p,j)=>{const rs=d.records.filter(r=>r.polo===p);return [regions[j],p,d.salas[j],rs.reduce((a,r)=>a+r.meta,0),null,null,rs.reduce((a,r)=>a+r.horas,0)/d.salas[j],null,null];});
table(N,11,['Origem aproximada','Executar em','Salas US','Exames US','Realizados/dia','Tentativas/dia','Horas assistenciais por sala','Carga sem repor faltas','Carga com reposição-meta'],nr,[28,23,12,18,18,18,23,24,24],32);
for(let r=12;r<=17;r++){
 form(N,`E${r}`,`=D${r}/('Agenda e absenteismo'!$B$6*'Agenda e absenteismo'!$B$7)`);
 form(N,`F${r}`,`=ROUNDUP(E${r}/(1-'Agenda e absenteismo'!$B$10),0)`);
 form(N,`H${r}`,`=G${r}/('Agenda e absenteismo'!$B$6*'Agenda e absenteismo'!$B$7*'Agenda e absenteismo'!$B$8*'Agenda e absenteismo'!$B$9*(1-'Agenda e absenteismo'!$B$10))`);
 form(N,`I${r}`,`=G${r}/('Agenda e absenteismo'!$B$6*'Agenda e absenteismo'!$B$7*'Agenda e absenteismo'!$B$8*'Agenda e absenteismo'!$B$9*(1-'Agenda e absenteismo'!$B$12))`);
}
val(N,'B18','TOTAL');for(const c of ['C','D','E','F'])form(N,`${c}18`,`=SUM(${c}12:${c}17)`);S[N].getRange('A18:I18').format.fill='#DEE8F2';S[N].getRange('A18:I18').format.font.bold=true;
fmt(N,'D12:D18','#,##0');fmt(N,'E12:E18','#,##0.0');fmt(N,'G12:G17','#,##0.0');fmt(N,'H12:I17','0.0%');
S[N].getRange('H12:I17').conditionalFormats.add('cellIs',{operator:'greaterThan',formula:1,format:{fill:'#FDE9E7',font:{color:'#A12622'}}});
merged(N,'A20:I21','Remanejo proposto: 504 Dopplers venosos bilaterais de MMII da região Norte serão atendidos na Asa Sul, mantendo 40 min/exame. A origem continua sendo Norte. Validar deslocamento com a regulação.');
section(N,23,'Prazo e absenteísmo — o que realmente cabe','I');
table(N,24,['Cenário','Meses','Falta bruta','Recuperação de tempo','Perda líquida','Carga do polo limitante','Exames US da meta','Situação','Condição'],[
 ['Sem reposição',8,.2,0,null,null,64915,null,'Capacidade insuficiente'],
 ['Meta de reposição',8,.2,.8,null,null,64915,null,'Repor minutos de sala, não só remarcar pedidos'],
 ['Prazo alternativo',10,.2,0,null,null,64915,null,'Exige decisão sobre extensão do prazo'],
 ['Sete meses efetivos',7,.2,.8,null,null,64915,null,'A meta de reposição proposta não basta'],
],[28,23,12,18,18,18,23,24,52],42);
for(let r=25;r<=28;r++){
 form(N,`E${r}`,`=C${r}*(1-D${r})/(1-C${r}*D${r})`);
 form(N,`F${r}`,`=MAX($G$12:$G$17)/(B${r}*'Agenda e absenteismo'!$B$7*'Agenda e absenteismo'!$B$8*'Agenda e absenteismo'!$B$9*(1-E${r}))`);
 form(N,`H${r}`,`=IF(F${r}<=1,"Cabe nas premissas","Não cabe")`);
}
fmt(N,'C25:F28','0.0%');fmt(N,'B25:B28','0');fmt(N,'G25:G28','#,##0');S[N].getRange('H25:I28').format.wrapText=true;
merged(N,'A30:I31','Oito meses sem reposição têm déficit mínimo de 2.402 horas assistenciais de US, antes da distribuição territorial. Não reduzir tempos nem contar reagendamento como produção. Se a recuperação não se comprovar, o caminho dentro de 20 salas é rever o prazo.');
merged(N,'A33:I34','Arranjo escolhido entre 11.628 distribuições: menor carga máxima por sala antes do remanejo; depois, equilíbrio Norte/Central. A distribuição territorial usa participações antigas (15/09) e exige validação antes de contratar a execução.');
merged(N,'A36:I37','Parede abdominal mantida, com confirmação de faturamento pela SES. Angio coronária e articulação excluídas; 4.000 transvaginais reservadas ao IEV. As abas Exames e metas e Filas atendidas mostram o estoque e a meta de cada exame.');
merged(N,'A39:I40','A SES precisa encaminhar demanda suficiente por protocolo. Os dados de fila são da recarga de 02/11/2026, com solicitações até 28/10. Não são garantia de estoque no início. A planilha completa e o plano oficial foram preservados.');

wb.recalculate();
const metrics={salas:S[N].getRange('C18').values[0][0],US:S[N].getRange('D18').values[0][0],exames:S[E].getRange(`F${et}`).values[0][0],valor:S[E].getRange(`J${et}`).values[0][0],filas:pr.length,cenarios:S[N].getRange('E25:H28').values,recuperacao_minima:S[A].getRange('C20').values[0][0]};
if(metrics.salas!==20||metrics.US!==64915||metrics.exames!==79219||Math.abs(metrics.valor-10636506.41)>.01)throw new Error('Conciliação falhou');
const errors=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!',options:{useRegex:true,maxResults:100}});
await fs.writeFile(path.join(root,'verificacao/plano20_resultados.json'),JSON.stringify(metrics,null,2));await fs.writeFile(path.join(root,'verificacao/plano20_erros.ndjson'),errors.ndjson);
await (await SpreadsheetFile.exportXlsx(wb)).save(path.join(root,'Carteira 1 - plano em 20 salas.xlsx'));
for(const [n,range,file] of [[N,'A11:I18','plano20_salas'],[N,'A23:I31','plano20_cenarios'],[E,'A6:J13','plano20_exames'],[F,'A6:I11','plano20_filas']]){
 const pic=await wb.render({sheetName:n,range,scale:1.1,format:'png'});await fs.writeFile(path.join(root,`verificacao/${file}.png`),new Uint8Array(await pic.arrayBuffer()));
}
console.log(JSON.stringify(metrics,null,2));console.log(errors.ndjson);
