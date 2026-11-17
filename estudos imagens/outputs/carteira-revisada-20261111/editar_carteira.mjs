import fs from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { FileBlob, SpreadsheetFile } from '@oai/artifact-tool';
const dir = fileURLToPath(new URL('.', import.meta.url));
const original = '/Users/hendrick/Projetos/planos-ses/planos/redacao_04/estudos/carteira_final_v2_20261111.xlsx';
const readPath = process.argv.includes('--verificar-salvo')?dir+'carteira_final_v3_revisada_20261111.xlsx':original;
const wb = await SpreadsheetFile.importXlsx(await FileBlob.load(readPath));
if(process.argv.includes('--verificar-salvo')){
  console.log((await wb.inspect({kind:'table',range:'Resumo!A4:B16',tableMaxRows:13,tableMaxCols:2,maxChars:4000})).ndjson);
  for(const [sheetName,range,file] of [['Resumo','A1:D25','resumo_final'],['Saídas','A4:C14','premissas_finais']]){
    const img=await wb.render({sheetName,range,scale:1,format:'png'});await fs.writeFile(dir+file+'.png',new Uint8Array(await img.arrayBuffer()));
  }
  process.exit(0);
}
if (process.argv.includes('--inspecionar')) {
  console.log((await wb.inspect({kind:'sheet',include:'id,name',maxChars:4000})).ndjson);
  const img = await wb.render({sheetName:'Escolhidos',range:'A4:M12',scale:1,format:'png'});
  await fs.writeFile(dir+'original.png',new Uint8Array(await img.arrayBuffer()));
  process.exit(0);
}
const data = JSON.parse(await fs.readFile(dir+'dados_modelo.json','utf8'));
const originalHash=(await import('node:crypto')).createHash('sha256').update(await fs.readFile(original)).digest('hex');
if(originalHash!==data.metadata.original_sha256)throw Error('O original mudou desde a extração.');
const sheets={};
for(const name of ['Resumo','Escolhidos','Articulação','Não escolhidos','Estudos das filas','Saídas','Da sobra à falta','Conferência']){
  sheets[name]=wb.worksheets.getItem(name);
  sheets[name].getUsedRange().clear({applyTo:'contents'});
}
for(const name of ['Demanda por fila','Doppler'])sheets[name]=wb.worksheets.add(name);
const money='"R$ "#,##0.00';
function v(s,a,x){sheets[s].getRange(a).values=[[x]];}
function f(s,a,x){sheets[s].getRange(a).formulas=[[x]];}
function title(s,text,sub,last='J'){
  const w=sheets[s];w.showGridLines=false;
  w.getRange(`A1:${last}3`).format.font={name:'Arial',size:10};
  v(s,'A1',text);w.getRange('A1').format.font={name:'Arial',size:14,bold:true};
  w.getRange(`A2:${last}2`).merge();v(s,'A2',sub);
  w.getRange(`A2:${last}2`).format.wrapText=true;w.getRange('A2').format.rowHeight=42;
}
function headers(s,heads,widths){
 const w=sheets[s];w.getRangeByIndexes(3,0,1,heads.length).values=[heads];
 const r=w.getRangeByIndexes(3,0,1,heads.length);r.format={fill:'#1F4E78',font:{name:'Arial',size:10,bold:true,color:'#FFFFFF'},wrapText:true,rowHeight:45,verticalAlignment:'center'};
 widths.forEach((x,i)=>w.getRangeByIndexes(0,i,1,1).format.columnWidth=x);
 w.freezePanes.freezeRows(4);
}
function body(s,rows,cols){
 const r=sheets[s].getRangeByIndexes(4,0,rows,cols);r.format.font={name:'Arial',size:10};r.format.rowHeight=22;r.format.verticalAlignment='center';
}
const nC=data.candidates.length,lastC=nC+4,nF=data.filas.length,lastF=nF+4,nCode=data.codes.length,lastCode=nCode+4;
const codeRow=new Map(data.codes.map((c,i)=>[c.code,i+5]));
const candInput=new Map(data.candidates.map((c,i)=>[c.id,i+5]));
const byId=new Map(data.candidates.map(c=>[c.id,c]));

// Um só conjunto de premissas; os custos unitários são os da versão recebida.
title('Saídas','Premissas da carteira e alternativas de faturamento','Amarelo: entradas editáveis. Custos e tempos herdados da v2; dimensionamento por polo não reavaliado.','W');
const settings=[
 ['Horizonte de execução (meses)',12],
 ['Ritmo da SES a repetir','3 meses'],
 ['Descontar da demanda','agendamentos'],
 ['Valor máximo dos exames',10636602],
 ['Margem mínima (% do preço)',0.15],
 ['SES confirmou duas unidades por bilateral?','não'],
 ['Incluir bilaterais se a condição for atendida?','sim'],
 ['Unidades por pedido no cenário bilateral',2],
 ['Fonte do enquadramento da parede','DF 16/2025: 02.05.02.006-2'],
 ['Data do histórico de fluxos','02/11/2026'],
 ['Atualização do estoque','26 filas em 11/11; restantes em 02/11'],
];
sheets['Saídas'].getRange(`A4:B${settings.length+3}`).values=settings;
sheets['Saídas'].getRange('A4:C14').format={fill:'#FFFFFF',font:{name:'Arial',size:10,bold:false,color:'#111111'},rowHeight:26};
sheets['Saídas'].getRange('A4:A14').format.columnWidth=50;
sheets['Saídas'].getRange('B4:B14').format.columnWidth=43;
sheets['Saídas'].getRange('B4:B11').format.fill='#FFF2CC';
sheets['Saídas'].getRange('B7').setNumberFormat(money);sheets['Saídas'].getRange('B8').setNumberFormat('0.0%');
for(const [a,vals] of [['B5',['3 meses','12 meses']],['B6',['agendamentos','realizados']],['B9',['não','sim']],['B10',['não','sim']]])sheets['Saídas'].getRange(a).dataValidation={rule:{type:'list',values:vals}};
sheets['Saídas'].getRange('B4').dataValidation={rule:{type:'whole',operator:'between',formula1:1,formula2:24}};
sheets['Saídas'].getRange('B11').dataValidation={rule:{type:'whole',operator:'between',formula1:1,formula2:2}};
const inputHeads=['ID','Exame','Mod.','Código faturamento','Preço por unidade','Custo por pedido','Minutos por pedido','Condição','Margem ativa','Ordem por margem','Unidades por pedido','Elegibilidade','Motivo'];
sheets['Saídas'].getRange(`D4:P4`).values=[inputHeads];
sheets['Saídas'].getRange('D4:P4').format={fill:'#1F4E78',font:{name:'Arial',size:10,bold:true,color:'#FFFFFF'},wrapText:true,rowHeight:45};
for(let i=0;i<nC;i++){
 const c=data.candidates[i],r=i+5;
 sheets['Saídas'].getRange(`D${r}:K${r}`).values=[[c.id,c.name,c.mod,c.code,c.price,c.cost,c.minutes,c.condition]];
 f('Saídas',`N${r}`,`=IF(K${r}="bilateral",IF(AND($B$9="sim",$B$10="sim"),$B$11,1),1)`);
 f('Saídas',`L${r}`,`=(H${r}*N${r}-I${r})/(H${r}*N${r})`);
 f('Saídas',`M${r}`,`=COUNTIF(L$5:L$${lastC},">"&L${r})+COUNTIF(L$5:L${r},L${r})`);
 f('Saídas',`O${r}`,`=IF(AND(K${r}="bilateral",OR($B$9<>"sim",$B$10<>"sim",$B$11<>2)),"condicionado",IF(L${r}<$B$8,"margem abaixo do mínimo","sim"))`);
 v('Saídas',`P${r}`,c.note);
}
for(const [col,width] of Object.entries({D:15,E:55,F:8,G:18,H:16,I:16,J:14,K:15,L:14,M:12,N:14,O:24,P:80}))sheets['Saídas'].getRange(`${col}1`).format.columnWidth=width;
sheets['Saídas'].getRange(`H5:I${lastC}`).setNumberFormat(money);sheets['Saídas'].getRange(`L5:L${lastC}`).setNumberFormat('0.0%');
sheets['Saídas'].getRange(`D5:P${lastC}`).format.font={name:'Arial',size:10,bold:false,color:'#111111'};
sheets['Saídas'].getRange(`D5:P${lastC}`).format.wrapText=false;
sheets['Saídas'].getRange(`D5:P${lastC}`).format.rowHeight=24;
sheets['Saídas'].getRange(`H5:K${lastC}`).format.fill='#FFF2CC';
const notes=[
 ['Método da demanda','Estoque + entradas estimadas do período − produção/oferta prevista da SES − reservas. Nunca soma o crescimento líquido a entradas brutas novamente.'],
 ['Rateio por fila','Entradas e produção mensal foram medidas por código. Distribuição por nome: participação nos agendamentos históricos. Agenda não informada tem peso zero; código inteiro sem agenda usa estoque. É hipótese, não medição de futuras solicitações por fila.'],
 ['Cenário inicial','Desconta agendamentos ao ritmo dos últimos 3 meses fechados, para evitar prometer demanda já absorvida em agendas da SES. Realizados mostra hipótese mais ampla; faltas/cancelamentos podem mudar o retorno à fila.'],
 ['Datas e atualização','Fluxos: out/2025 a set/2026; últimos três: jul a set/2026. Pesos por nome: janela da coleta de 02/11. Estoques de 26 filas: leitura pública de 11/11; demais: 02/11. Não houve nova coleta completa.'],
 ['Reserva do IEV','Mantidos 4.000 transvaginais e os seis recortes históricos de pelve. São premissas herdadas; não foram atualizados por CID/contrato.'],
 ['Faturamento do Doppler','Mesmo código vascular 02.05.01.004-0 para membros, carótidas, renal e aorta. Mudar a indicação do exame não é alternativa de faturamento. Duas unidades por membro dependem de aceitação aplicável ao DF/instrumento.'],
 ['Correção do parecer anterior','A descrição sobre vasos não basta para proibir duas unidades bilaterais. Material SES-SP, 2019, p. 136, orienta unidade por membro e distingue o registro de vasos. É fundamento para consulta, não autorização do DF.'],
 ['Parede abdominal','Planejamento corrigido para 02.05.02.006-2, R$ 70,97: enquadramento explícito na tabela regionalizada DF 16/2025. O código original do cadastro SISREG foi preservado na Demanda por fila. Confirmar aplicação no instrumento.'],
 ['Preços regionais diferentes','A DF 16/2025 diferencia descrições sob o mesmo código. Seus R$ 134,25 para membros não substituem automaticamente os R$ 115,61 da Candanga; não foram aplicados à receita principal.'],
 ['Doppler bilateral','A ativação da hipótese pode mudar a classificação por margem. O custo de 40 minutos por pedido bilateral é mantido; não se duplica o custo ao duplicar unidades de faturamento.'],
 ['Pendência assistencial','Quadril e coluna infantis ficam separados até comprovar o escopo da OCI. Displasia do quadril é ortopedia; não foi afirmada ausência de sobreposição apenas pelo nome da fila.'],
 ['Custos e capacidade','Custos e tempos da v2 preservados, inclusive a referência já usada para Doppler extra membros. Não houve cotação nem revisão por polo. Valores são cenários de planejamento.'],
 ['Fonte de preços','Anexo oficial Candanga SEI 212117347, SIA, CSV do main, commit 6673d50cdd0c5a0cbbdc8afb5452d771b8c4fb04.'],
 ['Mapa Social','https://paineis-ext.mpdft.mp.br/extensions/mapasauderegulamentacao/mapasauderegulamentacao.html'],
 ['Deliberação DF 16/2025','https://www.sinj.df.gov.br/sinj/Norma/482f67237e0a4bd1a7e9dd40dfe9b158/ses_cg_dlb_16_2025.html'],
 ['Deliberação DF 46/2026','https://www.sinj.df.gov.br/sinj/Norma/08cdc67f1b9a46158271100a13d7d382/ses_cg_dlb_46_2026.html'],
 ['Auditoria SES-SP, p. 136','https://saude.sp.gov.br/resources/ses/perfil/gestor/homepage/auditoria/cursos/curso-auditoria-e-regulacao-no-sistema-unico-de-saude-sus-sp-2019/auditoria_ambulatorial_-_dr_vanderlei_soares_moya_2v.pdf'],
 ['Referência SIGTAP','Ficha local 02.05.01.004-0, competência 10/2026; não foi extraído o pacote de novembro. Não há código especial de Doppler de pernas identificado nesta revisão.'],
 ['Original preservado',original],
];
for(let i=0;i<notes.length;i++){
 const r=i+17;v('Saídas',`A${r}`,notes[i][0]);sheets['Saídas'].getRange(`B${r}:C${r}`).merge();v('Saídas',`B${r}`,notes[i][1]);
 sheets['Saídas'].getRange(`B${r}:C${r}`).format.wrapText=true;sheets['Saídas'].getRange(`A${r}:C${r}`).format.rowHeight=64;
}
sheets['Saídas'].getRange('C1').format.columnWidth=45;

// Histórico de fluxos por código. As decisões finais não alteram o dado medido.
title('Estudos das filas','Fluxos históricos por código SIGTAP','Fonte: coleta bruta 02/11/2026. Entradas e produção observadas por código; rateios por fila são hipóteses na aba Demanda por fila.','L');
headers('Estudos das filas',['Código','Maior fila do código','Estoque 02/11','Entradas em 12 meses','Agendamentos em 12 meses','Agendamentos 3m anualizados','Realizados em 12 meses','Realizados 3m anualizados','Soma dos pesos de estoque','Agendadas por nomes (janela fonte)','Preço Candanga SIA','SES anual no cenário ativo'],[18,55,16,17,19,20,19,20,18,21,18,20]);
body('Estudos das filas',nCode,12);
for(let i=0;i<nCode;i++){
 const c=data.codes[i],r=i+5;
 sheets['Estudos das filas'].getRange(`A${r}:K${r}`).values=[[c.code,c.name,c.stock,c.entries,c.offer12,c.offer3annual,c.real12,c.real3annual,c.weight_stock,c.weight_offer,c.price]];
 f('Estudos das filas',`L${r}`,`=IF('Saídas'!$B$6="realizados",IF('Saídas'!$B$5="3 meses",H${r},G${r}),IF('Saídas'!$B$5="3 meses",F${r},E${r}))`);
}
sheets['Estudos das filas'].getRange(`C5:J${lastCode}`).setNumberFormat('#,##0.0');sheets['Estudos das filas'].getRange(`K5:K${lastCode}`).setNumberFormat(money);

title('Demanda por fila','Demanda por nome de fila, com desconto da SES','Estoque observado + entradas estimadas − SES prevista − reserva. Uma linha por par nome/código da coleta. Datas de estoques explícitas. Pesos de fluxo estimados.','W');
headers('Demanda por fila',['Código no cadastro','Fila exata','Estoque 02/11','Estoque lido 11/11','Data do estoque usado','Estoque usado','Reserva histórica','Preço código nativo','ID candidato','Classificação / motivo','Peso no estoque do código','Entradas anuais do código','Entradas estimadas da fila/ano','Agenda histórica pelo nome','Peso estimado nos fluxos','SES anual do código (ativa)','SES prevista no período','Entradas estimadas no período','Disponível após SES/reserva','Código para planejamento','Alocado à carteira (pedidos)','Disponível não alocado','Qualidade do estoque'],[18,65,16,17,18,16,17,18,16,54,18,20,20,20,20,20,20,20,20,20,20,20,30]);
body('Demanda por fila',nF,23);
for(let i=0;i<nF;i++){
 const x=data.filas[i],r=i+5,k=codeRow.get(x.codigo),c=byId.get(x.candidate);
 sheets['Demanda por fila'].getRange(`A${r}:E${r}`).values=[[x.codigo,x.nome,x.fila,x.current,x.source_date]];
 f('Demanda por fila',`F${r}`,`=IF(D${r}="",C${r},D${r})`);
 sheets['Demanda por fila'].getRange(`G${r}:J${r}`).values=[[x.reserve,x.native_price,x.candidate,x.reason]];
 f('Demanda por fila',`K${r}`,`=IF('Estudos das filas'!I${k}=0,0,C${r}/'Estudos das filas'!I${k})`);
 f('Demanda por fila',`L${r}`,`='Estudos das filas'!D${k}`);
 f('Demanda por fila',`M${r}`,`=O${r}*L${r}`);
 v('Demanda por fila',`N${r}`,x.agendadas_12m);
 f('Demanda por fila',`O${r}`,`=IF('Estudos das filas'!J${k}=0,K${r},IF(N${r}="",0,N${r}/'Estudos das filas'!J${k}))`);
 f('Demanda por fila',`P${r}`,`='Estudos das filas'!L${k}`);
 f('Demanda por fila',`Q${r}`,`=O${r}*P${r}*'Saídas'!$B$4/12`);
 f('Demanda por fila',`R${r}`,`=M${r}*'Saídas'!$B$4/12`);
 f('Demanda por fila',`S${r}`,`=MAX(0,ROUNDDOWN(F${r}+R${r}-Q${r}-G${r}+0.000000001,0))`);
 v('Demanda por fila',`T${r}`,c?c.code:x.codigo);
 const lookup=`INDEX(Escolhidos!$H$5:$H$${lastC},MATCH(I${r},Escolhidos!$P$5:$P$${lastC},0))`;
 f('Demanda por fila',`U${r}`,x.candidate?`=MIN(S${r},MAX(0,${lookup}-${r===5?'0':`SUMIF(I$5:I${r-1},I${r},U$5:U${r-1})`}))`:'=0');
 f('Demanda por fila',`V${r}`,`=S${r}-U${r}`);
 v('Demanda por fila',`W${r}`,(x.current===null?'histórico de 02/11':'leitura parcial de 11/11')+(x.agendadas_12m===null?'; agenda não informada':''));
}
sheets['Demanda por fila'].getRange(`C5:D${lastF}`).setNumberFormat('#,##0');sheets['Demanda por fila'].getRange(`F5:G${lastF}`).setNumberFormat('#,##0');
sheets['Demanda por fila'].getRange(`K5:K${lastF}`).setNumberFormat('0.00%');sheets['Demanda por fila'].getRange(`O5:O${lastF}`).setNumberFormat('0.00%');
sheets['Demanda por fila'].getRange(`L5:R${lastF}`).setNumberFormat('#,##0.0');sheets['Demanda por fila'].getRange(`S5:V${lastF}`).setNumberFormat('#,##0');sheets['Demanda por fila'].getRange(`H5:H${lastF}`).setNumberFormat(money);
sheets['Demanda por fila'].getRange(`D5:D${lastF}`).format.fill='#FFF2CC';

// A ordenação se recalcula pela margem ativa; orçamento é consumido de cima para baixo.
title('Escolhidos','Carteira recomendada por margem e demanda após SES','Ordem dinâmica por margem percentual; quantidades inteiras limitadas à demanda estimada e ao orçamento. Bilaterais condicionados não entram no cenário inicial.','S');
headers('Escolhidos',['Exame','Mod.','Código faturamento','Estoque usado','Preço por unidade','Minutos/pedido','Margem ativa','Pedidos escolhidos','Valor dos exames','Margem em R$','Entradas estimadas no período','SES descontada no período','Reserva histórica','Disponível após SES','Unidades/pedido','ID candidato','Condição no cenário','Observação','Unidades faturáveis'],[56,8,18,17,18,17,16,19,20,20,21,21,18,21,17,16,30,80,19]);
body('Escolhidos',nC+4,19);
for(let r=5;r<=lastC;r++){
 const ix=`MATCH(ROW()-4,'Saídas'!$M$5:$M$${lastC},0)`;
 const src=col=>`INDEX('Saídas'!$${col}$5:$${col}$${lastC},${ix})`;
 for(const [dest,col] of [['A','E'],['B','F'],['C','G'],['E','H'],['F','J'],['G','L'],['O','N'],['P','D'],['Q','O'],['R','P']])f('Escolhidos',`${dest}${r}`,`=${src(col)}`);
 for(const [dest,col] of [['D','F'],['K','R'],['L','Q'],['M','G'],['N','S']])f('Escolhidos',`${dest}${r}`,`=SUMIF('Demanda por fila'!$I$5:$I$${lastF},P${r},'Demanda por fila'!$${col}$5:$${col}$${lastF})`);
 f('Escolhidos',`H${r}`,`=IF(Q${r}="sim",MIN(N${r},MAX(0,ROUNDDOWN(('Saídas'!$B$7-SUM(I$4:I${r-1})+0.0000001)/(E${r}*O${r}),0))),0)`);
 f('Escolhidos',`S${r}`,`=H${r}*O${r}`);
 f('Escolhidos',`I${r}`,`=S${r}*E${r}`);
 f('Escolhidos',`J${r}`,`=I${r}*G${r}`);
}
const total=lastC+1;v('Escolhidos',`A${total}`,'Total');
for(const col of ['D','H','I','J','K','L','M','N','S'])f('Escolhidos',`${col}${total}`,`=SUM(${col}5:${col}${lastC})`);
f('Escolhidos',`G${total}`,`=IF(I${total}=0,0,J${total}/I${total})`);
for(const [idx,label] of [[1,'US'],[2,'TC']]){
 const r=total+idx;v('Escolhidos',`A${r}`,label==='US'?'Ultrassom':'Tomografia');
 for(const col of ['D','H','I','J','K','L','M','N','S'])f('Escolhidos',`${col}${r}`,`=SUMIF(B$5:B$${lastC},"${label}",${col}$5:${col}$${lastC})`);
 f('Escolhidos',`G${r}`,`=IF(I${r}=0,0,J${r}/I${r})`);
}
sheets['Escolhidos'].getRange(`E5:E${total+2}`).setNumberFormat(money);sheets['Escolhidos'].getRange(`G5:G${total+2}`).setNumberFormat('0.0%');sheets['Escolhidos'].getRange(`I5:J${total+2}`).setNumberFormat(money);sheets['Escolhidos'].getRange(`D5:D${total+2}`).setNumberFormat('#,##0');sheets['Escolhidos'].getRange(`H5:H${total+2}`).setNumberFormat('#,##0');sheets['Escolhidos'].getRange(`K5:N${total+2}`).setNumberFormat('#,##0');sheets['Escolhidos'].getRange(`S5:S${total+2}`).setNumberFormat('#,##0');
sheets['Escolhidos'].getRange(`A${total}:S${total}`).format.font={name:'Arial',size:10,bold:true};
sheets['Escolhidos'].getRange(`G5:G${lastC}`).conditionalFormats.add('colorScale',{colors:['#FCE4D6','#FFFFFF','#E2EFDA'],thresholds:['min',{type:'percentile',value:50},'max']});

title('Resumo','Carteira revisada: melhores margens após desconto da SES','Cópia de planejamento. Fluxos históricos por código; 26 estoques atualizados em 11/11 e demais em 02/11. Premissas e fontes na aba Saídas.','D');
const summary=[
 ['Valor máximo dos exames',"='Saídas'!B7",money],
 ['Valor da carteira recomendada',`=Escolhidos!I${total}`,money],
 ['Recurso sem alocação',"=B4-B5",money],
 ['Pedidos escolhidos',`=Escolhidos!H${total}`,'#,##0'],
 ['Unidades faturáveis estimadas',`=Escolhidos!S${total}`,'#,##0'],
 ['Margem estimada da carteira',`=Escolhidos!J${total}`,money],
 ['Margem percentual',`=Escolhidos!G${total}`,'0.0%'],
 ['Critério de desconto da SES',"='Saídas'!B6",null],
 ['Histórico da SES repetido',"='Saídas'!B5",null],
 ['Horizonte (meses)',"='Saídas'!B4",'0'],
 ['Duas unidades por bilateral confirmadas?',"='Saídas'!B9",null],
 ['Margem mínima aceita',"='Saídas'!B8",'0.0%'],
 ['Demanda dos candidatos antes do limite de orçamento',`=Escolhidos!N${total}`,'#,##0'],
];
summary.forEach(([label,formula,fmt],i)=>{v('Resumo',`A${i+4}`,label);f('Resumo',`B${i+4}`,formula);if(fmt)sheets['Resumo'].getRange(`B${i+4}`).setNumberFormat(fmt);});
sheets['Resumo'].getRange('A4:A16').format.columnWidth=56;sheets['Resumo'].getRange('B4:B16').format.columnWidth=28;sheets['Resumo'].getRange('A4:B16').format.rowHeight=26;sheets['Resumo'].getRange('B5:B6').format.font={name:'Arial',size:12,bold:true};
const overview=[
 'Como ler: Escolhidos ordena as margens e limita a quantidade pela demanda após SES e pelo recurso.',
 'Doppler: 11.845 pedidos de MMII e 198 de MMSS formavam o grupo antigo de 12.043; não é uma única fila.',
 'Há fundamento público para estudar unidade por membro. A receita bilateral segue condicionada à aplicação no DF.',
 'Parede abdominal: planejamento a R$ 70,97 no 02.05.02.006-2; o cadastro de origem permanece visível.',
 'A projeção futura usa rateio histórico por nome, não novas solicitações observadas. Trocar para realizados amplia o cenário.',
 'Não há obrigação de gastar todo o recurso. A diferença fica explícita, sem preencher com exames sem enquadramento.',
 'Custos e capacidade por polo não foram reavaliados nesta cópia. Confirmar demanda, regulação e faturamento antes de executar.',
];
overview.forEach((t,i)=>{let r=i+19;sheets['Resumo'].getRange(`A${r}:D${r}`).merge();v('Resumo',`A${r}`,t);sheets['Resumo'].getRange(`A${r}:D${r}`).format.wrapText=true;sheets['Resumo'].getRange(`A${r}:D${r}`).format.rowHeight=36;});

// Inventário exaustivo por motivo, inclusive PET-CT, cone beam e órbitas/sela.
title('Não escolhidos','Universo das filas e o que não foi alocado','Inventário completo das 656 linhas da coleta, separado entre alocado e não alocado. Procedimentos/pedidos por par nome/código; não são pacientes únicos. Detalhe em Demanda por fila.','G');
headers('Não escolhidos',['Motivo ou situação','Estoque histórico 02/11','Estoque usado (datas mistas)','Disponível estimado no período','Pedidos alocados','Disponível não alocado','Número de filas'],[65,24,26,28,24,26,20]);
const reasons=[...new Set(data.filas.map(x=>x.reason))].sort();
for(let i=0;i<reasons.length;i++){
 const r=i+5;v('Não escolhidos',`A${r}`,reasons[i]);
 for(const [dest,col] of [['B','C'],['C','F'],['D','S'],['E','U'],['F','V']])f('Não escolhidos',`${dest}${r}`,`=SUMIF('Demanda por fila'!$J$5:$J$${lastF},A${r},'Demanda por fila'!$${col}$5:$${col}$${lastF})`);
 f('Não escolhidos',`G${r}`,`=COUNTIF('Demanda por fila'!$J$5:$J$${lastF},A${r})`);
}
const nr=reasons.length+5;v('Não escolhidos',`A${nr}`,'Total dos pares nome/código');
for(const c of 'BCDEFG')f('Não escolhidos',`${c}${nr}`,`=SUM(${c}5:${c}${nr-1})`);
body('Não escolhidos',reasons.length+1,7);sheets['Não escolhidos'].getRange(`B5:G${nr}`).setNumberFormat('#,##0');

// Detalhe original de articulação, com correção de classificação e vínculo às filas fonte.
title('Articulação','Estruturas superficiais e filas infantis: enquadramento separado','As contagens originais foram preservadas. Quadril/coluna infantil não são declarados fora da ortopedia pelo nome; confirmar CID e escopo do IEV.','K');
headers('Articulação',['Fila','Grupo histórico','Pedidos 02/11','Menos de 24 meses (fonte)','Espera mediana (dias)','Idade mediana','CID principais (fonte)','Preço de planejamento','Valor histórico de referência','Situação revisada','Disponível no cenário'],[60,25,20,25,20,18,75,22,25,60,24]);
const oldArt=data.original.find(s=>s.sheet==='Articulação');
for(let rr=5;rr<=20;rr++){
 const row=oldArt.rows.find(row=>row[0]?.cell===`A${rr}`);const old=Object.fromEntries(row.map(c=>[c.cell.replace(/\d/g,''),c.value]));
 const pos=data.filas.findIndex(x=>x.codigo==='02.05.02.006-2'&&x.nome.trim()===old.A.trim());const src=pos+5;
 sheets['Articulação'].getRange(`A${rr}:H${rr}`).values=[[old.A,old.B,Number(old.C),Number(old.D),Number(old.E),Number(old.F),old.G,70.97]];
 f('Articulação',`I${rr}`,`=C${rr}*H${rr}`);v('Articulação',`J${rr}`,data.filas[pos].reason);f('Articulação',`K${rr}`,`='Demanda por fila'!S${src}`);
}
v('Articulação','A21','Total histórico detalhado');for(const c of ['C','D','I','K'])f('Articulação',`${c}21`,`=SUM(${c}5:${c}20)`);
body('Articulação',17,11);sheets['Articulação'].getRange('H5:I21').setNumberFormat(money);sheets['Articulação'].getRange('A23:K30').clear({applyTo:'contents'});

// Reunião de todas as filas vasculares do código e de outros Dopplers, sem trocar indicações.
const dop=data.filas.filter(x=>x.codigo==='02.05.01.004-0'||/DOPPLER/.test(x.nome));
title('Doppler','Doppler: filas, indicação e possibilidade de faturamento','Fila regulatória não é código de faturamento. Mesmo código vascular reúne anatomias diferentes. Estudo detalhado e fontes na aba Saídas.','J');
headers('Doppler',['Fila exata','Código no cadastro','Pedidos 02/11','Estoque usado','Grupo / destino','Código para planejamento','Unidades por pedido','Situação de faturamento','Disponível após SES','Pedidos escolhidos'],[80,20,20,20,57,23,23,80,24,24]);
for(let i=0;i<dop.length;i++){
 const x=dop[i],r=i+5,src=data.filas.indexOf(x)+5,c=byId.get(x.candidate),cr=candInput.get(x.candidate);
 sheets['Doppler'].getRange(`A${r}:F${r}`).values=[[x.nome,x.codigo,x.fila,null,c?c.name:x.reason,c?c.code:x.codigo]];
 f('Doppler',`D${r}`,`='Demanda por fila'!F${src}`);
 if(c)f('Doppler',`G${r}`,`='Saídas'!N${cr}`);else v('Doppler',`G${r}`,null);
 const txt=x.codigo==='02.05.01.004-0'?(c?.condition==='bilateral'?'Estudar unidade por membro com SES; não remapear venoso para arterial ou carótidas.':c?'Mesmo código vascular; indicação e laudo próprios.':x.reason):'Outro procedimento/indicação: não substitui Doppler vascular de membros.';
 v('Doppler',`H${r}`,txt);f('Doppler',`I${r}`,`='Demanda por fila'!S${src}`);f('Doppler',`J${r}`,`='Demanda por fila'!U${src}`);
}
body('Doppler',dop.length,10);sheets['Doppler'].getRange(`C5:D${dop.length+4}`).setNumberFormat('#,##0');

// Comparação com as metas enviadas: base histórica mantida, cenário atual por ID estável.
title('Da sobra à falta','Versão enviada e carteira revisada','As metas enviadas são históricas. A carteira atual inclui demanda futura estimada e desconta a SES; comparação financeira, não queda observada da fila.','G');
headers('Da sobra à falta',['Grupo de exame','Metas enviadas','Valor enviado pela Candanga','Pedidos na revisão','Valor na revisão','Diferença de valor','Observação'],[60,22,27,24,24,24,80]);
const groupIds={5:['V2-22'],6:['V2-19'],7:['D-MMII-V','D-MMII-A','D-MMSS-V','D-MMSS-A'],8:['D-CAR','D-REN','D-AOR'],9:['V2-15','V2-23'],10:['V2-16'],11:['V2-17','V2-24'],12:['V2-21','V2-26'],13:['V2-20'],14:['V2-13'],15:['V2-5','V2-9'],16:['V2-6','V2-10'],17:['V2-7','V2-11'],18:[],19:[],20:['V2-14','V2-25'],21:['V2-12'],22:['V2-8'],23:['V2-28']};
const oldBridge=data.original.find(s=>s.sheet==='Da sobra à falta');
for(let r=5;r<=23;r++){
 const old=Object.fromEntries(oldBridge.rows.find(row=>row[0]?.cell===`A${r}`).map(c=>[c.cell.replace(/\d/g,''),c]));
 v('Da sobra à falta',`A${r}`,r===8?'Doppler extra membros: carótidas, renal e aorta':old.A.value);v('Da sobra à falta',`B${r}`,Number(old.B.value));f('Da sobra à falta',`C${r}`,'='+old.C.formula);
 for(const [dest,col] of [['D','H'],['E','I']])f('Da sobra à falta',`${dest}${r}`,groupIds[r].length?'='+groupIds[r].map(id=>`SUMIF(Escolhidos!$P$5:$P$${lastC},"${id}",Escolhidos!$${col}$5:$${col}$${lastC})`).join('+'):'=0');
 f('Da sobra à falta',`F${r}`,`=E${r}-C${r}`);v('Da sobra à falta',`G${r}`,r===10?'Preço de planejamento da parede corrigido para R$ 70,97.':'Carteira limitada pela demanda estimada após SES e pela ordem de margem.');
}
v('Da sobra à falta','A24','Total');for(const c of 'BCDEF')f('Da sobra à falta',`${c}24`,`=SUM(${c}5:${c}23)`);
v('Da sobra à falta','A26','Valor máximo dos exames');f('Da sobra à falta','C26',"='Saídas'!B7");v('Da sobra à falta','A27','Recurso não alocado na carteira revisada');f('Da sobra à falta','C27','=C26-E24');
body('Da sobra à falta',23,7);for(const c of ['C','E','F'])sheets['Da sobra à falta'].getRange(`${c}5:${c}27`).setNumberFormat(money);

// Conferências terminais: não alimentam quantidades, preços nem classificação.
title('Conferência','Reconciliação completa da demanda e da alocação','A demanda após SES se separa entre pedidos escolhidos e saldo não alocado. As categorias incluem todos os pares de filas; não são contagens de pacientes únicos.','J');
headers('Conferência',['Código no cadastro','Estoque histórico','Estoque usado','Reserva','Entradas estimadas','SES descontada','Disponível após SES','Alocado','Não alocado','Diferença'],[20,22,22,20,24,24,24,22,22,20]);
sheets['Conferência'].getRange('A1').format.columnWidth=60;
for(let i=0;i<nCode;i++){
 const cd=data.codes[i].code,r=i+5;v('Conferência',`A${r}`,cd);
 for(const [dest,col] of [['B','C'],['C','F'],['D','G'],['E','R'],['F','Q'],['G','S'],['H','U'],['I','V']])f('Conferência',`${dest}${r}`,`=SUMIF('Demanda por fila'!$A$5:$A$${lastF},A${r},'Demanda por fila'!$${col}$5:$${col}$${lastF})`);
 f('Conferência',`J${r}`,`=G${r}-H${r}-I${r}`);
}
const checks=lastCode+3;
v('Conferência',`A${checks}`,'Filas no inventário');f('Conferência',`B${checks}`,`=COUNTA('Demanda por fila'!B5:B${lastF})`);
v('Conferência',`A${checks+1}`,'Filas sem classificação');f('Conferência',`B${checks+1}`,`=COUNTBLANK('Demanda por fila'!J5:J${lastF})`);
v('Conferência',`A${checks+2}`,'Pedidos: fonte versus carteira');f('Conferência',`B${checks+2}`,`=SUM(H5:H${lastCode})-Escolhidos!H${total}`);
v('Conferência',`A${checks+3}`,'Valor: ponte versus carteira');f('Conferência',`B${checks+3}`,`='Da sobra à falta'!E24-Escolhidos!I${total}`);
v('Conferência',`A${checks+4}`,'Recurso excedido (zero esperado)');f('Conferência',`B${checks+4}`,`=MAX(0,Escolhidos!I${total}-'Saídas'!B7)`);
body('Conferência',nCode+8,10);sheets['Conferência'].getRange(`B5:J${lastCode}`).setNumberFormat('#,##0.0');sheets['Conferência'].getRange(`J5:J${lastCode}`).conditionalFormats.add('cellIs',{operator:'notEqual',formula:0,format:{fill:'#FCE4D6',font:{color:'#C00000'}}});

wb.recalculate();
console.log((await wb.inspect({kind:'table',range:'Resumo!A4:B16',include:'values,formulas',tableMaxRows:13,tableMaxCols:2,maxChars:5000})).ndjson);
console.log((await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:30},maxChars:5000})).ndjson);
console.log((await wb.inspect({kind:'table',range:`Conferência!A${checks}:B${checks+4}`,include:'values,formulas',tableMaxRows:5,tableMaxCols:2,maxChars:3000})).ndjson);
const checksValues=sheets['Conferência'].getRange(`B${checks}:B${checks+4}`).values.flat();
if(checksValues[0]!==656||checksValues.slice(1).some(x=>Math.abs(x)>0.005))throw Error('Controles da carteira não reconciliam: '+JSON.stringify(checksValues));
// Sensibilidade relevante em cópia temporária do estado: unidades e autorização alteram a mesma carteira.
const baseTotal=sheets['Resumo'].getRange('B5').values[0][0];
sheets['Saídas'].getRange('B9').values=[['sim']];wb.recalculate();
const enabledTotal=sheets['Resumo'].getRange('B5').values[0][0];
const enabledUnits=sheets['Saídas'].getRange(`N5:N${lastC}`).values.flat();
if(!enabledUnits.includes(2))throw Error('O cenário bilateral não atualizou as unidades.');
sheets['Saídas'].getRange('B9').values=[['não']];
sheets['Saídas'].getRange('B6').values=[['realizados']];wb.recalculate();
const actualsTotal=sheets['Resumo'].getRange('B5').values[0][0];
if(actualsTotal===baseTotal)throw Error('O seletor de produção não mudou a carteira.');
sheets['Saídas'].getRange('B6').values=[['agendamentos']];wb.recalculate();
if(Math.abs(sheets['Resumo'].getRange('B5').values[0][0]-baseTotal)>0.005)throw Error('A restauração do cenário falhou.');
const savedBudget=sheets['Saídas'].getRange('B7').values[0][0];
sheets['Saídas'].getRange('B7').values=[[0]];wb.recalculate();
if(sheets['Resumo'].getRange('B5').values[0][0]!==0)throw Error('O orçamento zero não zerou a carteira.');
sheets['Saídas'].getRange('B7').values=[[savedBudget]];
const savedMargin=sheets['Saídas'].getRange('B8').values[0][0];
sheets['Saídas'].getRange('B8').values=[[0.6]];wb.recalculate();
if(sheets['Resumo'].getRange('B5').values[0][0]!==0)throw Error('O limiar de margem não retirou os candidatos.');
sheets['Saídas'].getRange('B8').values=[[savedMargin]];wb.recalculate();
if(Math.abs(sheets['Resumo'].getRange('B5').values[0][0]-baseTotal)>0.005)throw Error('A restauração das premissas falhou.');
console.log(JSON.stringify({baseTotal,enabledTotal,actualsTotal,originalHash}));
for(const [name,range,file] of [['Resumo','A1:D25','resumo'],['Escolhidos','A4:J16','escolhidos'],['Escolhidos',`K4:S${Math.min(lastC,12)}`,'demanda_escolhidos'],['Doppler','A4:J12','doppler'],['Articulação','A4:K10','articulacao'],['Não escolhidos','A4:G15','nao_escolhidos'],['Estudos das filas','A4:L10','estudos'],['Saídas','A4:C14','premissas'],['Saídas','D4:O10','parametros_exames'],['Da sobra à falta','A4:F12','comparacao'],['Conferência',`A${checks}:B${checks+4}`,'conferencia'],['Demanda por fila','A4:J10','fontes']]){
 const img=await wb.render({sheetName:name,range,scale:1,format:'png'});await fs.writeFile(dir+file+'.png',new Uint8Array(await img.arrayBuffer()));
}
const out=await SpreadsheetFile.exportXlsx(wb);
await out.save(dir+'carteira_final_v3_revisada_20261111.xlsx');
const hashAfter=(await import('node:crypto')).createHash('sha256').update(await fs.readFile(original)).digest('hex');
if(hashAfter!==originalHash)throw Error('O arquivo original foi alterado.');
await fs.writeFile(dir+'verificacao.json',JSON.stringify({checksValues,baseTotal,enabledTotal,actualsTotal,originalHash,output:dir+'carteira_final_v3_revisada_20261111.xlsx'},null,2));
