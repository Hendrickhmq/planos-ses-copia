import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
const out=path.dirname(fileURLToPath(import.meta.url));
const d=JSON.parse(await fs.readFile(path.join(out,'dados_estudo.json'),'utf8'));
const w=Workbook.create();const names=['Decisao','Modelo','Demanda','Precos','Fontes'];
const S=Object.fromEntries(names.map(n=>[n,w.worksheets.add(n)]));
const navy='#203F64',ink='#203044',amber='#FFF0C2';
const currency='"R$ "#,##0.00;("R$ "#,##0.00);"-"';
function val(s,c,v){S[s].getRange(c).values=[[v]];}
function formula(s,c,f){S[s].getRange(c).formulas=[[f]];S[s].getRange(c).format.font.color=f.includes("'Precos'")||f.includes("'Demanda'")||f.includes("'Modelo'")?'#217346':ink;}
function base(s,title,widths,endrow){const q=S[s];q.showGridLines=false;q.getRangeByIndexes(0,0,endrow,widths.length).format.font={name:'Arial',size:11,color:ink};q.getRangeByIndexes(0,0,endrow,widths.length).format.verticalAlignment='center';widths.forEach((v,i)=>q.getRangeByIndexes(0,i,1,1).format.columnWidth=v);val(s,'A2',title);q.getRange('A2').format.font={name:'Arial',size:16,bold:true,color:navy};q.getRange('A2').format.rowHeight=29;}
let tid=0;
function tab(s,row,headers,rows){const n=headers.length,range=S[s].getRangeByIndexes(row-1,0,rows.length+1,n);range.values=[headers,...rows];range.format.rowHeight=36;range.format.wrapText=true;const h=S[s].getRangeByIndexes(row-1,0,1,n);h.format={fill:navy,font:{name:'Arial',size:11,bold:true,color:'#FFFFFF'},rowHeight:58,wrapText:true,horizontalAlignment:'center'};const t=S[s].tables.add(range,true,'EstudoTabela'+(++tid));t.style='TableStyleLight9';S[s].freezePanes.freezeRows(row);}
function fmt(s,c,f){S[s].getRange(c).setNumberFormat(f);}
const N=d.records.length,last=6+N;
base('Precos','Remuneracao e referencias para cotar',[19,38,17,16,19,20,19,65,19,19,19,20],last+4);
val('Precos','A3','10/2026. Incremento e Candanga sao referencias distintas. Cotacoes integrais ainda pendentes.');
tab('Precos',6,['SIGTAP','Procedimento','Base SA','Incremento 38.01','Candanga oficial','Preco publicado','Qualidade/local','Fonte de mercado','Base + incremento','Limite base ilustrativo','Limite incr. ilustrativo','Fontes da tarifa'],d.records.map(r=>[r.code_fmt,r.name,r.base,r.increment,r.candanga,r.retail,r.retail_quality,r.retail_url,null,null,null,'S4 e S5; p. '+r.page]));
for(let i=0;i<N;i++){const r=i+7;formula('Precos',`I${r}`,`=IF(ISNUMBER(D${r}),ROUND(C${r}*100*(100+D${r}*100)/100,0)/100,C${r})`);formula('Precos',`J${r}`,`=C${r}*(1-'Modelo'!$B$12)`);formula('Precos',`K${r}`,`=I${r}*(1-'Modelo'!$B$12)`);}
fmt('Precos',`C7:C${last}`,currency);fmt('Precos',`D7:D${last}`,'0.0%');fmt('Precos',`E7:F${last}`,currency);fmt('Precos',`I7:K${last}`,currency);
S.Precos.getRange(`G7:H${last}`).format.rowHeight=78;
base('Demanda','Fila e rede regulada: outubro/2025 a setembro/2026',[19,38,15,17,15,18,18,18,16,16,18,18,20],last+7);
val('Demanda','A3','Recarga 02/11/2026. Realizados incluem a rede registrada; nao isolam a oferta propria da SES.');
tab('Demanda',6,['SIGTAP','Procedimento','Estoque codigo','Estoque do recorte','Reserva inicial','Entradas 12m','Agendados 12m','Realizados 12m','Faltas 12m','Faltas / encerrados','Entradas - real. / mes','Saldo rateado ao recorte','Disponibilidade proxy'],d.records.map(r=>[r.code_fmt,r.name,r.stock,r.code==='0205010032'?13236:r.stock,r.reserve,r.entries,r.scheduled,r.performed,r.absent,null,null,null,null]));
for(let i=0;i<N;i++){const r=i+7;formula('Demanda',`J${r}`,`=IF(H${r}+I${r}>0,I${r}/(H${r}+I${r}),"Sem base")`);formula('Demanda',`K${r}`,`=(F${r}-H${r})/12`);formula('Demanda',`L${r}`,`=IF(C${r}>0,K${r}*D${r}/C${r},0)`);formula('Demanda',`M${r}`,`=D${r}-E${r}+L${r}*'Modelo'!$B$6`);}
fmt('Demanda',`C7:I${last}`,'#,##0');fmt('Demanda',`J7:J${last}`,'0.0%');fmt('Demanda',`K7:M${last}`,'#,##0.0');
val('Demanda',`A${last+2}`,'Proxy = recorte - reserva + saldo rateado x meses. Nao prova pedidos unicos, acesso ou fluxo mensal.');
val('Demanda',`A${last+3}`,'Eco: recorte adulto 13.236; reserva hipotetica de 1.000 ao IEV. Rateio do fluxo pela fracao do estoque.');
val('Demanda',`A${last+4}`,'Fontes S1-S3. Nao somar estoque, agendamentos e realizados. Falta nao equivale a novo pedido.');
base('Modelo','Emenda federal de bancada: modelo editavel',[36,39,15,18,18,20,21,20,22,17,19,23,34],41);
const params=[['Orcamento',1500000],['Apoio hipotetico',150000],['Meses de execucao',8],['Falta planejada',.2],['Tarifa solicitada','Base'],['Reconhecimento SES e CNES','Nao'],['Norma cobre o periodo real','Nao'],['Tarifa ativa',null],['Retencao ilustrativa por exame',.1]];
S.Modelo.getRange('A4:B12').values=params;S.Modelo.getRange('A4:B12').format.rowHeight=27;
S.Modelo.getRange('B4:B10').format.fill=amber;S.Modelo.getRange('B12').format.fill=amber;
S.Modelo.getRange('B4:B10').format.font.color='#1459A6';
S.Modelo.getRange('B8').dataValidation={rule:{type:'list',values:['Base','Incremento']}};
S.Modelo.getRange('B9:B10').dataValidation={rule:{type:'list',values:['Nao','Sim']}};
formula('Modelo','B11','=IF(B8="Base","Base",IF(AND(B9="Sim",B10="Sim"),"Incremento","PENDENTE"))');
fmt('Modelo','B4:B5',currency);fmt('Modelo','B7','0.0%');fmt('Modelo','B12','0.0%');
val('Modelo','D4','Use Base enquanto nao houver reconhecimento especifico.');
val('Modelo','D5','Apoio e reserva hipotetica, nao custo cotado nem rubrica aprovada.');
val('Modelo','D6','Incremento: habilitacao, via no convenio e validade no periodo precisam ser confirmadas.');
val('Modelo','D7','A norma ambulatorial consultada tem efeitos ate 31/12/2026.');
val('Modelo','D8','Cotacao = preco integral por exame entregue, incluindo itens ja precificados pelo executor.');
val('Modelo','D9','Celulas amarelas: hipoteses. Nao ha cotacao contratada neste estudo.');
val('Modelo','D12','Retencao apenas para comparar limites na aba Precos; nao soma despesa ao apoio.');
for(let r=4;r<=12;r++){S.Modelo.getRange(`D${r}`).format.wrapText=false;}
const mr=19,ml=mr+N-1;
tab('Modelo',18,['SIGTAP','Procedimento','Meta proposta','Tarifa ativa','Unitario ativo','Valor assistencial','Cotacao integral / un.','Custo executor','Contribuicao antes apoio','Realizados / mes','Tentativas / mes','Demanda proxy','Condicao da linha'],d.records.map(r=>[r.code_fmt,r.name,r.code==='0208050035'?1200:r.code==='0204060028'?1900:0,null,null,null,null,null,null,null,null,null,null]));
S.Modelo.getRange(`C${mr}:C${ml}`).format.fill=amber;S.Modelo.getRange(`G${mr}:G${ml}`).format.fill=amber;
S.Modelo.getRange(`C${mr}:C${ml}`).format.font.color='#1459A6';S.Modelo.getRange(`G${mr}:G${ml}`).format.font.color='#1459A6';
for(let i=0;i<N;i++){const r=mr+i,p=i+7;formula('Modelo',`D${r}`,'=$B$11');formula('Modelo',`E${r}`,`=IF(D${r}="Base",'Precos'!C${p},IF(D${r}="Incremento",'Precos'!I${p},"Pendente"))`);formula('Modelo',`F${r}`,`=IF(C${r}=0,0,IF(ISNUMBER(E${r}),C${r}*E${r},"Tarifa pendente"))`);formula('Modelo',`H${r}`,`=IF(C${r}=0,0,IF(ISNUMBER(G${r}),C${r}*G${r},"Cotacao pendente"))`);formula('Modelo',`I${r}`,`=IF(AND(ISNUMBER(F${r}),ISNUMBER(H${r})),F${r}-H${r},"Pendente")`);formula('Modelo',`J${r}`,`=C${r}/$B$6`);formula('Modelo',`K${r}`,`=ROUNDUP(J${r}/(1-$B$7),0)`);formula('Modelo',`L${r}`,`='Demanda'!M${p}`);formula('Modelo',`M${r}`,`=IF(C${r}=0,"Nao selecionado",IF(C${r}>L${r},"Meta acima da proxy",IF(NOT(ISNUMBER(F${r})),"Confirmar tarifa",IF(NOT(ISNUMBER(H${r})),"Obter cotacao integral","Confirmar encaminhamento SES"))))`);}
val('Modelo','A13','Valor assistencial');formula('Modelo','B13',`=IF(COUNT(F${mr}:F${ml})=${N},SUM(F${mr}:F${ml}),"Tarifa pendente")`);
val('Modelo','A14','Assistencia + apoio');formula('Modelo','B14','=IF(ISNUMBER(B13),B13+B5,"Tarifa pendente")');
val('Modelo','A15','Saldo nao alocado');formula('Modelo','B15','=IF(ISNUMBER(B14),B4-B14,"Tarifa pendente")');
val('Modelo','A16','Saldo apos custos cotados e apoio');formula('Modelo','B16',`=IF(AND(ISNUMBER(B13),COUNT(H${mr}:H${ml})=${N}),B13-SUM(H${mr}:H${ml})-B5,"Cotacoes pendentes")`);
fmt('Modelo','B13:B16',currency);fmt('Modelo',`C${mr}:C${ml}`,'#,##0');fmt('Modelo',`E${mr}:I${ml}`,currency);fmt('Modelo',`J${mr}:L${ml}`,'#,##0.0');
S.Modelo.getRange('B15:B16').conditionalFormats.add('cellIs',{operator:'lessThan',formula:0,format:{fill:'#FCE5E3',font:{color:'#A12622'}}});
S.Modelo.getRange(`I${mr}:I${ml}`).conditionalFormats.add('cellIs',{operator:'lessThan',formula:0,format:{fill:'#FCE5E3',font:{color:'#A12622'}}});
S.Modelo.getRange(`A${ml+2}`).values=[['Quantidade nao e compromisso. Eco e ECG reservados a emenda de R$ 2 milhoes de cardiologia.']];
base('Decisao','Estudo da emenda de R$ 1,5 milhao',[34,25,23,25,23,23,60],31);
val('Decisao','A3','Federal de bancada | 03/11/2026 | Contratacao de exames de imagem');
S.Decisao.getRange('A5:C10').values=[['Referencia do modelo','Valor','Condicao'],['Tarifa ativa',null,'Base ate reconhecimento'],['Metas de exames',null,'Hipotese para comparar'],['Assistencia + apoio',null,'Apoio hipotetico de R$ 150 mil'],['Saldo nao alocado',null,'Nao criar despesa para fechar o envelope'],['Resultado com custos cotados',null,'Sem cotacoes, viabilidade pendente']];
formula('Decisao','B6',"='Modelo'!B11");formula('Decisao','B7',`=SUM('Modelo'!C${mr}:C${ml})`);formula('Decisao','B8',"='Modelo'!B14");formula('Decisao','B9',"='Modelo'!B15");formula('Decisao','B10',"='Modelo'!B16");fmt('Decisao','B8:B10',currency);
S.Decisao.getRange('A5:C5').format={fill:navy,font:{name:'Arial',size:11,bold:true,color:'#FFFFFF'},rowHeight:30};S.Decisao.getRange('A6:C10').format.rowHeight=32;
S.Decisao.getRange('C6:C10').format.wrapText=true;
tab('Decisao',13,['Prioridade','Opcao','Estoque codigo','SIGTAP base','Com incr. 38.01','Candanga','Motivo e condicao'],[
 ['1 - cotar','Cintilografia ossea',null,null,null,null,'Gargalo registrado; incremento e custo DF precisam ser reconhecidos e cotados.'],
 ['Reservado - cardiologia','Ecocardiograma adulto',null,null,null,null,'Meta zero aqui. Eco e ECG reservados a emenda de R$ 2 milhoes de cardiologia.'],
 ['1 - cotar','Densitometria',null,null,null,null,'Boa comparacao com anuncio local sob incremento; rede ja atende.'],
 ['3 - alternativa','RM nao ortopedica',null,null,null,null,'Separar protocolo e contraste; crânio como referencia; evitar RM coberta pelo IEV.'],
 ['Nao priorizar','Mamografia',null,null,null,null,'Preco publico supera base e incremento; relevancia exige recorte e proposta propria.'],
 ['Somente com proposta','PET-CT',null,null,null,null,'Sem incremento localizado; tarifa alta nao prova margem; confirmar FDG.']
]);
const id=[0,1,2,4,3,13];for(let i=0;i<id.length;i++){const r=i+14,p=id[i]+7;formula('Decisao',`C${r}`,`='Demanda'!C${p}`);formula('Decisao',`D${r}`,`='Precos'!C${p}`);formula('Decisao',`E${r}`,`='Precos'!I${p}`);formula('Decisao',`F${r}`,`='Precos'!E${p}`);}
fmt('Decisao','C14:C19','#,##0');fmt('Decisao','D14:F19',currency);S.Decisao.getRange('A14:G19').format.rowHeight=64;
S.Decisao.getRange('B6:B10').format.font.color=ink;S.Decisao.getRange('C14:F19').format.font.color=ink;
val('Decisao','A22','Carteira A para testar');val('Decisao','B22','1.200 cintilografias osseas + 1.900 densitometrias');
val('Decisao','A23','Carteira B alternativa');val('Decisao','B23','1.000 cintilografias osseas + 1.150 RM de cranio');
val('Decisao','A25','As duas dependem de incremento reconhecido ou de cotacao compativel com a base.');
val('Decisao','A26','Candanga nao e receita automatica desta emenda. Nao acumular Candanga e incremento.');
val('Decisao','A27','Norma ambulatorial consultada ate 31/12/2026; continuidade em 2027 nao comprovada.');
val('Decisao','A28','Fonte de conclusoes: estudo escrito, Precos, Demanda e fontes preservadas.');
base('Fontes','Fontes e limites de interpretacao',[14,87,106],d.sources.length+20);
tab('Fontes',5,['ID','Fonte e recorte','Caminho ou URL'],d.sources);
S.Fontes.getRange(`A6:C${5+d.sources.length}`).format.rowHeight=72;
const notes=[['Recorte assistencial','Nao e inventario exaustivo de todos os contratos vigentes da SES. Acervo aprovado mapeado; confirmar atualizacoes.'],['Fila e pessoas','Pedidos e pessoas sao medidas distintas; nao somar pessoas entre exames nem estresse/repouso como pacientes distintos.'],['Serie','Outubro/2025 a setembro/2026; estoque em 02/11. Datas e janelas diferentes estao preservadas.'],['Incremento','Parametros da habilitacao 38.01. Nao somar com Candanga e nao presumir cabimento no convenio.'],['Preco de mercado','Anuncio nao e proposta. Referencias sem cidade confirmada nao comprovam custo DF.'],['Apoio','R$ 150 mil e hipotese; decompor por quantidades e precos. Nao duplicar componente ja incluido na proposta.']];
const start=23;S.Fontes.getRange(`A${start}:B${start+notes.length-1}`).values=notes;S.Fontes.getRange(`A${start}:B${start+notes.length-1}`).format.wrapText=true;S.Fontes.getRange(`A${start}:B${start+notes.length-1}`).format.rowHeight=65;
S.Decisao.freezePanes.unfreeze();S.Modelo.freezePanes.unfreeze();S.Modelo.freezePanes.freezeColumns(2);
w.recalculate();
const checks={};
function read(s,c){return S[s].getRange(c).values[0][0];}
function expect(s,c,n){let v=read(s,c);if(typeof n==='number'?Math.abs(v-n)>.011:v!==n)throw new Error(`${s}!${c}: ${v}, esperado ${n}`);}
expect('Modelo','B13',333878);expect('Modelo','B15',1016122);expect('Modelo','B16','Cotacoes pendentes');
for(let i=0;i<N;i++)expect('Precos',`I${i+7}`,d.records[i].with_increment);
val('Modelo','B8','Incremento');expect('Modelo','B11','PENDENTE');expect('Modelo','B13','Tarifa pendente');
val('Modelo','B9','Sim');expect('Modelo','B11','PENDENTE');val('Modelo','B10','Sim');expect('Modelo','B13',1335512);expect('Modelo','B15',14488);
val('Modelo','C19',1201);expect('Modelo','B13',1336275.96);val('Modelo','C19',1200);
val('Modelo','G19',800);expect('Modelo','I19',-43248);val('Modelo','G21',100);expect('Modelo','B16',35512);
val('Modelo','B7',.3);expect('Modelo','K21',340);val('Modelo','B7',.2);
val('Modelo','B5',170000);expect('Modelo','B15',-5512);val('Modelo','B5',150000);
for(const cell of ['G19','G21'])S.Modelo.getRange(cell).clear({applyTo:'contents'});
val('Modelo','B8','Base');val('Modelo','B9','Nao');val('Modelo','B10','Nao');w.recalculate();
expect('Modelo','B13',333878);expect('Modelo','B16','Cotacoes pendentes');
checks.tests='Base, gates incrementais, quantidade, cotacao negativa, falta, apoio, restauracao';
checks.final={active:read('Modelo','B11'),assistance:read('Modelo','B13'),budgetTotal:read('Modelo','B14'),unallocated:read('Modelo','B15'),costStatus:read('Modelo','B16')};
await fs.writeFile(path.join(out,'verificacao_modelo.json'),JSON.stringify(checks,null,2));
const inspect=await w.inspect({kind:'table',range:'Modelo!A13:B16',include:'values,formulas',tableMaxRows:4,tableMaxCols:2});
await fs.writeFile(path.join(out,'inspecao.ndjson'),inspect.ndjson);
const errors=await w.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:50},summary:'Erros finais'});
await fs.writeFile(path.join(out,'erros.ndjson'),errors.ndjson);
await (await SpreadsheetFile.exportXlsx(w)).save(path.join(out,'Estudo emenda imagem 1,5 milhao.xlsx'));
for(const [s,r] of [['Decisao','A13:G19'],['Modelo','A13:F21'],['Demanda','A6:G11'],['Precos','A6:F11'],['Fontes','A5:C9']]){
 const b=await w.render({sheetName:s,range:r,scale:1,format:'png'});await fs.writeFile(path.join(out,`previa_${s}.png`),new Uint8Array(await b.arrayBuffer()));
}
console.log(JSON.stringify(checks));console.log(errors.ndjson);
