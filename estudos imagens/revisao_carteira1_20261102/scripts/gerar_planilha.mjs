import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const d=JSON.parse(await fs.readFile(path.join(root,'dados_revisao.json'),'utf8'));
const wb=Workbook.create();
const names=['Resumo','Premissas','Salas por polo','Redistribuicao 20','Cenarios SES','Carteira 1','Protocolos','Rateio territorial','Demanda por codigo','Filas e exclusoes','Regioes na fonte','Series da fonte','Decisoes e fontes'];
const S=Object.fromEntries(names.map(n=>[n,wb.worksheets.add(n)]));
const blue='#203F64',ink='#233449';
const col=n=>{let s='';while(n){n--;s=String.fromCharCode(65+n%26)+s;n=Math.floor(n/26);}return s;};
function title(n,t,width=12){const s=S[n];s.showGridLines=false;s.getRangeByIndexes(0,0,5,width).format.font={name:'Arial',size:11,color:ink};s.getRange('A2').values=[[t]];s.getRange('A2').format.font={name:'Arial',size:16,bold:true,color:blue};s.getRange('A3:'+col(width)+'3').format.borders={bottom:{style:'thin',color:'#91A4BB'}};s.tabColor=n==='Resumo'?blue:undefined;}
let tableId=0;
function table(n,headers,rows,widths,row=6){const s=S[n];const end=row+rows.length;s.getRangeByIndexes(row-1,0,rows.length+1,headers.length).values=[headers,...rows.map(r=>r.map(x=>x??null))];const range=s.getRange(`A${row}:${col(headers.length)}${end}`);range.format.font={name:'Arial',size:11,color:ink};range.format.rowHeight=27;range.format.verticalAlignment='center';s.getRange(`A${row}:${col(headers.length)}${row}`).format={fill:blue,font:{name:'Arial',size:11,bold:true,color:'#FFFFFF'},wrapText:true,rowHeight:64,horizontalAlignment:'center',verticalAlignment:'center'};widths.forEach((w,i)=>s.getRangeByIndexes(row-1,i,rows.length+1,1).format.columnWidth=w);const t=s.tables.add(range,true,'RevisaoTabela'+(++tableId));t.style='TableStyleLight9';s.freezePanes.freezeRows(row);return end;}
const formula=(n,cell,f)=>{
 if(n==='Cenarios SES'){
  const row=cell.match(/\d+/)[0];
  f=f.replace(/Protocolos!([A-P])\d+/g,(_,c)=>`INDEX(Protocolos!$${c}$7:$${c}$${pe},MATCH(F${row},Protocolos!$Q$7:$Q$${pe},0))`);
 }
 S[n].getRange(cell).formulas=[[f]];
};
const value=(n,cell,v)=>S[n].getRange(cell).values=[[v]];
const fmt=(n,r,f)=>S[n].getRange(r).setNumberFormat(f);
const note=(n,row,text)=>{value(n,`A${row}`,text);S[n].getRange(`A${row}`).format.font={name:'Arial',size:11,color:'#56677C'};};
names.forEach(n=>title(n,n==='Resumo'?'Carteira 1 — revisão de capacidade e demanda':n));

// Premissas: uma origem para cada controle. Os três cenários e 7/8 meses são comparações expressamente solicitadas.
table('Premissas',['Parâmetro','Valor','Natureza e limite'],[
 ['Dias úteis por mês',21,'Premissa herdada. Sem calendário de feriados ou ramp-up confirmado.'],
 ['Horas por sala/dia',10,'Premissa herdada. Exige equipe e licenciamento.'],
 ['Disponibilidade de agenda',.8,'80% do tempo bruto para agenda. Absorve pausas, preparo e indisponibilidade operacional.'],
 ['Faltas do cenário principal',.2,'Hipótese. Separadas dos 80%; vaga perdida ocupa agenda. Não é taxa comprovada do projeto.'],
 ['Defasagem coleta/início (meses)',0,'Início não informado. Comparação adicional de 2 meses em Cenarios SES.'],
 ['Parte da produção histórica atribuível à SES',1,'Teto ilustrativo, não medido. O residual é prestadores/outros convênios não transferíveis.'],
 ['Transferência cenário a',0,'Oferta habitual mantida.'],
 ['Transferência cenário b',.5,'Encaminhamento de 50% da oferta eletiva selecionada da SES. Premissa, não decisão.'],
 ['Transferência cenário c',1,'Concentração integral desse recorte no projeto. Exige pactuação.'],
 ['Limite de salas US',20,'Possibilidade de planejamento. Capacidade instalada não confirmada.'],
 ['Vagas canceladas além das faltas',0,'Não medido. Zero só no cenário, sem inferir ausência real.'],
 ['Baixas administrativas líquidas/mês',0,'Não medidas. Sem presumir retorno ou exclusão de pedidos após falta.'],
], [58,19,115]);
S['Premissas'].getRange('B7:B18').format.fill='#FFF1CC';fmt('Premissas','B9:B10','0.0%');fmt('Premissas','B12:B15','0.0%');
S['Premissas'].getRange('B9:B10').dataValidation={rule:{type:'decimal',operator:'between',formula1:0,formula2:.99}};
S['Premissas'].getRange('B12:B15').dataValidation={rule:{type:'decimal',operator:'between',formula1:0,formula2:1}};
note('Premissas',21,'Amarelo = hipótese editável. Alterar participação SES exige medir prestadores e convênios no mesmo protocolo.');
note('Premissas',22,'Alternativa: 80% como eficiência final já com faltas. Use faltas adicionais = 0 apenas se a perda total couber nos 20%.');
note('Premissas',23,'Se faltas = 20%, eficiência final de 80% deixa zero margem para outras perdas. Com 30%, 80% final é incompatível sem reposição.');

const ci=6+d.items.length;
table('Carteira 1',['ID','Código','Modalidade','Nome exato / origem da meta','Meta realizada','R$/exame','R$ procedimentos','Minutos','Horas assistenciais','Origem da quantidade','Base do tempo'],d.items.map((i,j)=>[j+1,i.codigo,i.modalidade,i.nome,i.meta,i.preco,null,i.minutos,null,i.cobertura==='crescimento da fila'?'Complemento da meta, demanda a pactuar':'Estoque na carteira anterior',i.base_tempo]),[8,21,19,90,16,16,22,13,20,50,45]);
for(let r=7;r<=ci;r++){formula('Carteira 1',`G${r}`,`=E${r}*F${r}`);formula('Carteira 1',`I${r}`,`=E${r}*H${r}/60`);}
fmt('Carteira 1',`E7:E${ci}`,'#,##0');fmt('Carteira 1',`F7:G${ci}`,'"R$ "#,##0.00');fmt('Carteira 1',`I7:I${ci}`,'#,##0.0');
note('Carteira 1',ci+3,'Parede: 3.304 exames mantidos. Código e faturamento dependem da confirmação expressa da SES. Custos não revistos.');

const ri=6+d.regional.length;
table('Rateio territorial',['Item','Região de origem aproximada','Polo US proposto','Meta alocada','Minutos','Horas','Modalidade','Participação proxy','Família da proxy','Data e origem da distribuição'],d.regional.map(r=>[r.item,r.regiao,r.polo,r.meta,null,null,null,r.share,r.familia,r.nota]),[10,30,25,18,14,16,20,20,32,98]);
for(let r=7;r<=ri;r++){formula('Rateio territorial',`E${r}`,`=INDEX('Carteira 1'!$H$7:$H$${ci},MATCH(A${r},'Carteira 1'!$A$7:$A$${ci},0))`);formula('Rateio territorial',`F${r}`,`=D${r}*E${r}/60`);formula('Rateio territorial',`G${r}`,`=INDEX('Carteira 1'!$C$7:$C$${ci},MATCH(A${r},'Carteira 1'!$A$7:$A$${ci},0))`);}
fmt('Rateio territorial',`H7:H${ri}`,'0.0%');fmt('Rateio territorial',`F7:F${ri}`,'#,##0.0');
note('Rateio territorial',ri+3,'Participações de 15/09 reaplicadas à meta de 02/11 por família. Novos protocolos usam mix antigo da modalidade. Não é coleta regional atual elegível.');
note('Rateio territorial',ri+4,'Região do registro não foi validada como residência. Plano separa origem aproximada de polo de execução proposto.');

// Capacidade de agenda e atendimento separadas: faltas consomem tempo de vaga, não horas assistenciais.
const polos=['Asa Sul','São Sebastião','Sobradinho','Ceilândia','Samambaia','Gama'];
const origens=['Central + Centro-Sul','Leste','Norte','Oeste','Sudoeste','Sul'];
const caprows=[];
for(const m of [8,7])for(const f of [0,.2,.3])for(let p=0;p<6;p++)caprows.push([origens[p],polos[p],m,f,null,null,null,null,null,null,null,null,null,null,null,null,null]);
const ce=table('Salas por polo',['Origem aproximada','Polo US','Meses','Faltas adicionais','Exames US','Horas assistenciais','Horas de agenda','Horas perdidas em faltas','Vagas necessárias','Horas agenda/sala','Salas inteiras','Utilização agenda','Salas no teto 20','Déficit de horas no teto','Exames TC (origem)','Horas TC (origem)','Tomógrafos locais mínimos'],caprows,[30,24,12,18,17,20,20,20,20,20,17,20,20,22,20,20,22]);
for(let r=7;r<=ce;r++){
 formula('Salas por polo',`E${r}`,`=SUMIFS('Rateio territorial'!$D$7:$D$${ri},'Rateio territorial'!$C$7:$C$${ri},B${r},'Rateio territorial'!$G$7:$G$${ri},"Ultrassom")`);
 formula('Salas por polo',`F${r}`,`=SUMIFS('Rateio territorial'!$F$7:$F$${ri},'Rateio territorial'!$C$7:$C$${ri},B${r},'Rateio territorial'!$G$7:$G$${ri},"Ultrassom")`);
 formula('Salas por polo',`G${r}`,`=F${r}/((1-D${r})*(1-Premissas!$B$17))`);formula('Salas por polo',`H${r}`,`=G${r}-F${r}`);
 formula('Salas por polo',`I${r}`,`=ROUNDUP(E${r}/((1-D${r})*(1-Premissas!$B$17)),0)`);
 formula('Salas por polo',`J${r}`,`=C${r}*Premissas!$B$7*Premissas!$B$8*Premissas!$B$9`);
 formula('Salas por polo',`K${r}`,`=ROUNDUP(G${r}/J${r},0)`);formula('Salas por polo',`L${r}`,`=G${r}/(J${r}*K${r})`);
 // Mesmo arranjo de 20 em todos os cenários: teste territorial, não declaração de capacidade instalada.
 value('Salas por polo',`M${r}`,[3,3,3,1,6,4][(r-7)%6]);
 formula('Salas por polo',`N${r}`,`=MAX(0,G${r}-J${r}*M${r})`);
 for(const [target,source] of [['O','D'],['P','F']])formula('Salas por polo',`${target}${r}`,`=SUMIFS('Rateio territorial'!$${source}$7:$${source}$${ri},'Rateio territorial'!$C$7:$C$${ri},B${r},'Rateio territorial'!$G$7:$G$${ri},"Tomografia")`);
 formula('Salas por polo',`Q${r}`,`=ROUNDUP(P${r}/((1-D${r})*(1-Premissas!$B$17))/J${r},0)`);
}
for(const c of ['D','L'])fmt('Salas por polo',`${c}7:${c}${ce}`,'0.0%');fmt('Salas por polo',`F7:H${ce}`,'#,##0.0');fmt('Salas por polo',`N7:N${ce}`,'#,##0.0');
S['Salas por polo'].getRange(`N7:N${ce}`).conditionalFormats.add('cellIs',{operator:'greaterThan',formula:0,format:{fill:'#FDE9E7',font:{color:'#A12622'}}});
note('Salas por polo',ce+3,'TC: colunas O:Q são carga por origem no arranjo local de seis polos. Tomógrafos e unidades não confirmados. Não presumir o roteamento antigo.');
note('Salas por polo',ce+4,'Faltas 0% também representa a hipótese otimista de perdas já integralmente absorvidas nos 80%, a confirmar operacionalmente.');

table('Redistribuicao 20',['Origem habitual','Execução proposta','Salas','Horas originais','Horas recebidas','Horas transferidas','Horas após remanejo','Capacidade 8 meses','Uso da capacidade','Déficit (h)'],polos.map((p,j)=>[origens[j],p,[3,3,3,1,6,4][j],null,null,null,null,null,null,null]),[30,27,16,23,23,23,25,25,24,22]);
table('Redistribuicao 20',['Origem','Execução','Exames transferidos','Minutos/exame','Horas','Protocolo'],[
 ['Sul','Asa Sul',915,40,null,'Doppler venoso bilateral de MMII'],
 ['Sul','Ceilândia',456,40,null,'Doppler venoso bilateral de MMII']
],[30,27,25,23,23,70],18);
for(let r=19;r<=20;r++)formula('Redistribuicao 20',`E${r}`,`=C${r}*D${r}/60`);
for(let r=7;r<=12;r++){
 formula('Redistribuicao 20',`D${r}`,`='Salas por polo'!F${r}`);
 formula('Redistribuicao 20',`E${r}`,`=SUMIFS($E$19:$E$20,$B$19:$B$20,B${r})`);
 formula('Redistribuicao 20',`F${r}`,`=IF(A${r}="Sul",SUM($E$19:$E$20),0)`);
 formula('Redistribuicao 20',`G${r}`,`=D${r}+E${r}-F${r}`);
 formula('Redistribuicao 20',`H${r}`,`=C${r}*8*Premissas!$B$7*Premissas!$B$8*Premissas!$B$9*(1-Premissas!$B$17)`);
 formula('Redistribuicao 20',`I${r}`,`=G${r}/H${r}`);formula('Redistribuicao 20',`J${r}`,`=MAX(0,G${r}-H${r})`);
}
fmt('Redistribuicao 20','D7:H12','#,##0.0');fmt('Redistribuicao 20','I7:I12','0.00%');fmt('Redistribuicao 20','J7:J12','#,##0.0');
note('Redistribuicao 20',14,'Teste matemático otimista: sem perdas adicionais por faltas. Requer confirmação de transporte, agenda e polos receptores.');
note('Redistribuicao 20',15,'Sul mantém origem. 1.371 Dopplers bilaterais passam de Gama para Asa Sul (915) e Ceilândia (456), sem reduzir os 40 minutos.');
note('Redistribuicao 20',16,'Gama e Asa Sul ficam praticamente no limite dos 80% do tempo bruto. Em sete meses ou com faltas adicionais este arranjo não cabe.');

const pe=table('Protocolos',['Código','Protocolo elegível (nome exato)','Estoque elegível','Meta realizada','Minutos','Entradas elegíveis/mês (proxy)','Produção habitual/mês (proxy)','Agendamentos nome, 12m','Realizados/agendados código','Participação elegível do estoque','SES/mês (premissa)','Outros prestadores/mês (premissa)','Saldo mensal sem projeto','Meses para zerar (condicional)','Transferência mínima SES 8m','Transferência mínima SES 7m','ID protocolo'],d.protocols.map((p,j)=>[p.codigo,p.nome,p.estoque,p.meta,p.minutos,p.entrada_mes,p.producao_mes,p.agenda_12m,p.real_ag_cod,p.fracao_entrada,null,null,null,null,null,null,j+7]),[22,92,21,19,14,25,26,26,26,28,25,27,24,28,29,29,18]);
for(let r=7;r<=pe;r++){
 formula('Protocolos',`K${r}`,`=G${r}*Premissas!$B$12`);formula('Protocolos',`L${r}`,`=G${r}-K${r}`);formula('Protocolos',`M${r}`,`=F${r}-G${r}-Premissas!$B$18`);formula('Protocolos',`N${r}`,`=IF(M${r}<0,C${r}/(-M${r}),"não zera")`);
}
fmt('Protocolos',`C7:N${pe}`,'#,##0.0');fmt('Protocolos',`D7:D${pe}`,'#,##0');fmt('Protocolos',`I7:J${pe}`,'0.0%');
note('Protocolos',pe+3,'Entradas: fluxo do código × participação do estoque elegível do nome. Rateio hipotético, sem série histórica por protocolo.');
note('Protocolos',pe+4,'Produção: agenda anual do nome × realizado/agendado do código ÷ 12 × fração elegível do nome. Janelas e mix não idênticos.');
note('Protocolos',pe+5,'SES versus outros prestadores não é identificado no mesmo recorte. B12 de Premissas = 100% é teto de transferibilidade, não fato.');
value('Protocolos','O6','Transferência mínima SES 8m');value('Protocolos','P6','Transferência mínima SES 7m');
S['Protocolos'].getRange('O6:P6').format={fill:blue,font:{name:'Arial',size:11,bold:true,color:'#FFFFFF'},wrapText:true,rowHeight:64,horizontalAlignment:'center'};
S['Protocolos'].getRange(`O6:P${pe}`).format.columnWidth=29;
for(let r=7;r<=pe;r++)for(const [c,m] of [['O',8],['P',7]])formula('Protocolos',`${c}${r}`,`=IF(K${r}=0,IF(D${r}<=MAX(0,C${r}+F${r}*${m}-L${r}*${m}),0,"sem SES transferível"),MAX(0,(D${r}-C${r}-F${r}*${m}+G${r}*${m})/(K${r}*${m})))`);
fmt('Protocolos',`O7:P${pe}`,'0.0%');
note('Protocolos',pe+6,'Transferência mínima: início na coleta e sem baixas. Acima de 100% indica insuficiência mesmo suspendendo a parcela SES estimada.');

// Um registro por protocolo, cenário e horizonte. O mesmo cálculo é aplicado em todas as linhas.
const cr=[];
for(const m of [8,7])for(const lag of [0,2])for(const scenario of ['a','b','c'])for(let j=0;j<d.protocols.length;j++)cr.push([scenario,m,lag,d.protocols[j].codigo,d.protocols[j].nome,j+7,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null]);
const se=table('Cenarios SES',['Cenário','Meses execução','Espera antes início (meses)','Código','Protocolo','Linha fonte','Estoque na coleta','Entradas antes início','Produção rede antes início','Estoque inicial','Entradas na execução','SES habitual potencial','Outros convênios / prestadores','Fração encaminhada SES','Oferta SES reduzida','SES remanescente atendida','Disponível ao projeto','Meta projeto','Projeto realizável','Déficit de demanda','Estoque final','Transferência absorvida pelo projeto','Aumento líquido na rede','Vagas do projeto (meta)','Horas assistenciais (meta)','Horas de agenda (meta)','Baixas administrativas'],cr,[12,17,24,22,90,16,22,23,24,22,23,24,27,25,24,26,25,21,23,24,23,30,27,26,27,26,25]);
for(let r=7;r<=se;r++){
 const p=cr[r-7][5];const scenario=cr[r-7][0];
 formula('Cenarios SES',`G${r}`,`=Protocolos!C${p}`);formula('Cenarios SES',`H${r}`,`=Protocolos!F${p}*(C${r}+Premissas!$B$11)`);
 formula('Cenarios SES',`I${r}`,`=MIN(G${r}+H${r},Protocolos!G${p}*(C${r}+Premissas!$B$11))`);
 formula('Cenarios SES',`J${r}`,`=MAX(0,G${r}+H${r}-I${r}-Premissas!$B$18*(C${r}+Premissas!$B$11))`);
 formula('Cenarios SES',`K${r}`,`=Protocolos!F${p}*B${r}`);formula('Cenarios SES',`L${r}`,`=Protocolos!K${p}*B${r}`);
 formula('Cenarios SES',`M${r}`,`=MIN(J${r}+K${r},Protocolos!L${p}*B${r})`);
 formula('Cenarios SES',`N${r}`,`=IF(Protocolos!D${p}>0,Premissas!$B$${{a:13,b:14,c:15}[scenario]},0)`);formula('Cenarios SES',`O${r}`,`=L${r}*N${r}`);
 formula('Cenarios SES',`P${r}`,`=MIN(MAX(0,J${r}+K${r}-M${r}),L${r}-O${r})`);
 formula('Cenarios SES',`AA${r}`,`=MIN(MAX(0,J${r}+K${r}-M${r}-P${r}),Premissas!$B$18*B${r})`);
 formula('Cenarios SES',`Q${r}`,`=MAX(0,J${r}+K${r}-M${r}-P${r}-AA${r})`);formula('Cenarios SES',`R${r}`,`=Protocolos!D${p}`);
 formula('Cenarios SES',`S${r}`,`=MIN(Q${r},R${r})`);formula('Cenarios SES',`T${r}`,`=R${r}-S${r}`);formula('Cenarios SES',`U${r}`,`=Q${r}-S${r}`);
 formula('Cenarios SES',`V${r}`,`=MIN(S${r},O${r})`);
 formula('Cenarios SES',`W${r}`,`=P${r}+M${r}+S${r}-MIN(J${r}+K${r},Protocolos!G${p}*B${r})`);
 formula('Cenarios SES',`X${r}`,`=ROUNDUP(R${r}/((1-Premissas!$B$10)*(1-Premissas!$B$17)),0)`);formula('Cenarios SES',`Y${r}`,`=R${r}*Protocolos!E${p}/60`);formula('Cenarios SES',`Z${r}`,`=Y${r}/((1-Premissas!$B$10)*(1-Premissas!$B$17))`);
}
fmt('Cenarios SES',`G7:AA${se}`,'#,##0.0');fmt('Cenarios SES',`N7:N${se}`,'0.0%');
S['Cenarios SES'].getRange(`T7:T${se}`).conditionalFormats.add('cellIs',{operator:'greaterThan',formula:.001,format:{fill:'#FDE9E7',font:{color:'#A12622'}}});
note('Cenarios SES',se+3,'a mantém oferta. b transfere parte. c concentra recorte eletivo selecionado. Regulação ainda não pactuou. Emergência, angio e sedação excluídas antes do cálculo.');
note('Cenarios SES',se+4,'Oferta reduzida é potencial histórico, não demanda adicional. Transferência absorvida = mínimo(projeto, oferta reduzida). Aumento líquido pode ser negativo.');
note('Cenarios SES',se+5,'Balanço acumulado não garante encaminhamento mensal suficiente nem identifica pessoas únicas. Revalidar estoque e coortes antes de iniciar.');

const de=table('Demanda por codigo',['Código','Estoque do código','Estoque elegível','Entradas código 12m','Agendamentos código 12m','Realizados código 12m','Faltas código 12m','Agenda dos nomes elegíveis (proxy)','Fração elegível (estoque)','Meta','Entrada elegível/mês (proxy)','Produção elegível/mês (proxy)'],d.flows.map(f=>[f.codigo,f.estoque_codigo,f.estoque,f.entrantes_codigo,f.agendados_codigo,f.realizados_codigo,f.faltas_codigo,f.agenda_nomes,f.fracao_estoque,f.meta,null,null]),[22,23,23,26,28,25,25,32,26,20,29,29]);
for(let r=7;r<=de;r++){formula('Demanda por codigo',`K${r}`,`=D${r}/12*I${r}`);formula('Demanda por codigo',`L${r}`,`=H${r}/12*F${r}/E${r}`);}
fmt('Demanda por codigo',`B7:L${de}`,'#,##0.0');fmt('Demanda por codigo',`I7:I${de}`,'0.0%');
note('Demanda por codigo',de+3,'Entradas integrais dos códigos não são acessíveis ao plano. A proxy usa participação do estoque, sem atribuir a ela caráter de medição.');
note('Demanda por codigo',de+4,'Reserva transvaginal = 4.000 no estoque. Aplicar sua fração ao fluxo é hipótese, não nova reserva contratual. Pelve mantém desconto legado 7/5.944 sujeito à regulação.');

const fe=table('Filas e exclusoes',['Código','Nome exato','Modalidade','Pedidos pendentes','Pessoas no par (não somar)','Devolvidas (separadas)','Elegível no cenário','Excluído / reservado','Protocolo','Regra aplicada','Agendamentos nome 12m'],d.invent.map(f=>[f.codigo,f.nome,f.modalidade,f.fila,f.pessoas,f.devolvidas,f.elegivel,null,f.protocolo,f.regra,f.agendadas_12m]),[22,96,20,23,28,28,25,26,30,115,30]);
for(let r=7;r<=fe;r++)formula('Filas e exclusoes',`H${r}`,`=D${r}-G${r}`);fmt('Filas e exclusoes',`D7:H${fe}`,'#,##0.0');

const regrows=[];for(const [mod,t] of Object.entries(d.raw_region)){for(const a of t.linhas)regrows.push([mod,...a,'02/11/2026 10:31','Modalidade inteira; não é carteira elegível nem residência validada.']);regrows.push([mod,'Sem região',t.sem_regiao.fila,t.sem_regiao.pessoas,'02/11/2026 10:31','Não redistribuído silenciosamente.']);}
table('Regioes na fonte',['Modalidade','Região/categoria na fonte','Pedidos','Pessoas na categoria','Recarga','Limitação'],regrows,[25,38,18,27,28,95]);
const sr=[];for(const [kind,t] of Object.entries(d.series))for(const row of t.linhas)if(d.flows.some(f=>f.codigo===row[0]))sr.push([kind,...row,...Array(Math.max(0,5-row.length)).fill(null)]);
table('Series da fonte',['Tabela','Código','Mês ou situação','Abertas / agendamentos (ver tabela)','Agendadas / realizados (ver tabela)','Faltas (oferta)'],sr,[20,23,95,40,42,28]);
note('Series da fonte',sr.length+9,'entrantes: abertas por mês de solicitação, agendadas por mês de agenda. oferta: agendamentos, realizados, faltas. situacao: contagens por status.');

const notes=[
 ['Decisão','Carteira 1 escolhida','79.219 exames e R$ 10.636.506,41. Mantida sem nova otimização de custos.','Solicitação do usuário e versão anterior JSON.'],
 ['Decisão','Parede abdominal mantida','3.304 exames essenciais. Obstáculo exige decisão sobre escopo e metas, sem troca automática por angio.','Usuário. Confirmação de enquadramento e faturamento pela SES pendente.'],
 ['Decisão','Sobreposição IEV','Articulação excluída inteira e 4.000 transvaginais reservadas. CID não define sozinho a fronteira.','estudo_outros_planos_imagem_20261102.md, seção 7, versão preservada.'],
 ['Superada','12.884 a 27.004 pedidos adicionais','Meta/(1-faltas) estima tentativas de agenda. Pedidos novos não demonstrados.','Relatório anterior, seção 3.2.'],
 ['Superada','Faltas não mudam salas','Vaga perdida reduz produção se não houver reposição no mesmo tempo. Só não há desconto adicional se a perda já estiver nos 80%.','estudo_polos_rede_capacidade_20261020.md, seção 5.'],
 ['Superada','Crescimento só positivo','Saldos negativos permanecem e reduzem o estoque antes e durante execução. Agendamento não equivale a exame feito.','Estudo anterior: crescimento e faltas.'],
 ['Superada','Alternativa principal sem parede/com angio','Carteira 1 é a decisão. Outras carteiras ficam apenas no arquivo anterior.','Solicitação atual prevalece.'],
 ['Diferença de conciliação','Estoque elegível de modelagem','77.981,35 pedidos equivalentes, contra 77.976 antes. Agora inclui filas pequenas e evita truncamento por nome; não equivale a pessoas nem estoque confirmado para execução.','Filas e exclusoes e regra legada de pelve.'],
 ['Medir','Pessoas únicas','A fonte tem contagens por par e modalidade. Não permite somar e deduplicar pessoas da carteira.','Coleta agregada, sem CPF/CNS/ID da solicitação.'],
 ['Medir','Solicitações e transições','Faltam IDs e datas de cada agendamento, falta, retorno, reagendamento, cancelamento, baixa e realização. Não há regra comprovada de retorno à fila.','por_codigo.situacao e por_codigo.oferta são agregados, sem vínculo longitudinal.'],
 ['Definição','Reagendamento','Nova tentativa da mesma solicitação. Não cria entrada nem outra realização.','Regra contábil do modelo.'],
 ['Definição','Baixa administrativa','Pode reduzir pendência sem resolver necessidade clínica. Não contar como produção assistencial.','Modelagem. Sem taxa medida.'],
 ['Cenário','Faltas com retorno','Com reapresentação do mesmo pedido, 79.219 realizações podem exigir 99.024 tentativas a 20% ou 113.170 a 30%.','Arredondamento no total. Por protocolo a soma de tetos é maior.'],
 ['Cenário','Faltas sem retorno no prazo','Meta de produção pode não ser atingida mesmo com estoque suficiente. Pedidos novos só são necessários se houver perda definitiva medida e insuficiência após reapresentações.','Não presumir regra operacional da SES.'],
 ['Cenário','Cancelamentos e outras baixas','Baixas líquidas são hipótese zero editável. Agendas canceladas podem consumir ou liberar vagas conforme prazo, ainda não medido.','Taxas e destino precisam de extração longitudinal.'],
 ['Pendente SES','Transferência pactuada','Definir protocolos eletivos, fração SES transferível, oferta mantida de outros convênios, vigência e volume mensal encaminhado.','Cenarios SES. Não inclui emergência.'],
 ['Pendente SES','Produção e faturamento Doppler','Confirmar unidade de exame bilateral versus pedido/procedimento faturável, mantendo 40 min para a quantidade atual até decisão expressa.','Tempos herdados no script anterior.'],
 ['Pendente operação','Salas e polos','Confirmar salas licenciadas, aparelhos, equipe e horários em cada polo. Até 20 é hipótese.','Rede de 20/10 é registro histórico, não capacidade atual confirmada.'],
 ['Proposta posterior','Meta verificável','Realizar 79.219 exames elegíveis regulados, por código e prazo, com laudo e registro individual únicos. Validar remanejamentos previamente.','Não aplicado ao plano oficial.'],
 ['Proposta posterior','Espera e regulação','Monitorar encaminhados, agendados, faltas, reapresentações, realizados, laudos, mediana e P90 de espera por protocolo. Definir metas de redução após medir linha de base.','Evita promessa de zerar extração sem controlar encaminhamento ou rede.'],
 ['Fonte','Mapa Social','Recarga 02/11/2026 10:31:47; solicitação mais recente 28/10. Séries com diferentes janelas conforme coleta.','fontes_preservadas/dados/fontes/mapa_social_20261102_imagem_bruto/coleta_20261102.json'],
 ['Fonte','Distribuição territorial','15/09, fila US e total de solicitações TC; aproximação por família. Novos protocolos usam mix antigo de 20/10.','fontes_preservadas/calculo_v19/calculo.py e calculo_v24/polos_capacidade.json'],
 ['Fonte','Tempos','Tempos herdados atribuídos pelo gerador ao CBR 2017 e intervalos TC do plano. São premissas de planejamento, sem validação clínica nova nesta revisão.','versao_anterior/estudo_filas_imagem_20261102.py, função minutos.'],
 ['Preservação','Fontes e versão anterior','Cópias e hashes em manifesto_fontes.json. Arquivos oficiais e documentos de outros planos não alterados.','Sem commit e sem envio externo.'],
];
table('Decisoes e fontes',['Natureza','Tema','Decisão / correção / limitação','Origem e confirmação necessária'],notes,[23,44,120,110]);
S['Decisoes e fontes'].getRange(`B7:D${notes.length+6}`).format.wrapText=true;S['Decisoes e fontes'].getRange(`A7:D${notes.length+6}`).format.rowHeight=68;

// Resumo compacto; resultados ligados aos cálculos, comparações territoriais e de encaminhamento.
const su=S.Resumo;su.tabColor=blue;
su.getRange('A4:D8').values=[['Meta de exames',null,'Procedimentos (R$)',null],['Salas confirmadas?','Pendente','Parede aprovada?','Pendente'],['Escopo','US e TC ambulatoriais','Angio coronária','Excluída'],['Reserva IEV (TV)',4000,'US articulação','Excluída'],['Rateio territorial','Proxy de 15/09','Coleta do estoque','02/11/2026']];
formula('Resumo','B4',`=SUM('Carteira 1'!E7:E${ci})`);formula('Resumo','D4',`=SUM('Carteira 1'!G7:G${ci})`);fmt('Resumo','B4','#,##0');fmt('Resumo','D4','"R$ "#,##0.00');
su.getRange('A4:D8').format.font={name:'Arial',size:11,color:ink};su.getRange('A4:D8').format.rowHeight=29;
table('Resumo',['Meses','Faltas adicionais','Horas US realizadas','Horas US de agenda','Salas sem mover origem','Mínimo agregado US','Déficit global com 20 (h)'],[8,7].flatMap(m=>[0,.2,.3].map(f=>[m,f,null,null,null,null,null])),[19,25,26,27,28,27,32],11);
for(let r=12;r<=17;r++){
 formula('Resumo',`C${r}`,`=SUMIFS('Carteira 1'!$I$7:$I$${ci},'Carteira 1'!$C$7:$C$${ci},"Ultrassom")`);formula('Resumo',`D${r}`,`=C${r}/((1-B${r})*(1-Premissas!$B$17))`);
 formula('Resumo',`E${r}`,`=SUMIFS('Salas por polo'!$K$7:$K$${ce},'Salas por polo'!$C$7:$C$${ce},A${r},'Salas por polo'!$D$7:$D$${ce},B${r})`);
 formula('Resumo',`F${r}`,`=ROUNDUP(D${r}/(A${r}*Premissas!$B$7*Premissas!$B$8*Premissas!$B$9),0)`);
 formula('Resumo',`G${r}`,`=MAX(0,D${r}-Premissas!$B$16*A${r}*Premissas!$B$7*Premissas!$B$8*Premissas!$B$9)`);
}
fmt('Resumo','B12:B17','0%');fmt('Resumo','C12:D17','#,##0.0');fmt('Resumo','G12:G17','#,##0.0');
note('Resumo',19,'20 salas: só há encaixe em 8 meses se as faltas já couberem nos 80% e houver redistribuição entre polos.');
note('Resumo',20,'Com 20% de faltas adicionais, são 24 salas em 8 meses e 29 em 7 meses. Sem remanejamento, até a hipótese otimista pede 21 e 23.');
const summaries=[];for(const m of [8,7])for(const lag of [0,2])for(const c of ['a','b','c'])summaries.push([c,m,lag,null,null,null,null,null,null,null,null]);
table('Resumo',['SES cenário','Meses','Espera inicial (meses)','Estoque inicial','Entradas elegíveis','SES atendida','Outros atendidos','Projeto possível','Déficit para meta','Estoque final','Aumento líquido rede'],summaries,[19,25,26,27,28,27,32,25,26,26,27],23);
const targets={D:'J',E:'K',F:'P',G:'M',H:'S',I:'T',J:'U',K:'W'};
for(let r=24;r<=35;r++)for(const [to,from] of Object.entries(targets))formula('Resumo',`${to}${r}`,`=SUMIFS('Cenarios SES'!$${from}$7:$${from}$${se},'Cenarios SES'!$A$7:$A$${se},A${r},'Cenarios SES'!$B$7:$B$${se},B${r},'Cenarios SES'!$C$7:$C$${se},C${r})`);
fmt('Resumo','D24:K35','#,##0.0');
note('Resumo',37,'a = mantém oferta; b = encaminha 50%; c = concentra 100% do recorte SES selecionado. Valores são cenários condicionados aos rateios.');
note('Resumo',38,'Atribuição à SES de 100% da produção habitual é um teto de transferência editável. Não foi comprovada separação por convênio/protocolo.');
note('Resumo',39,'Transferir oferta não cria novos pedidos. Aumento líquido compara produção total com a rede habitual e pode ser menor que a produção do projeto.');
note('Resumo',40,'Faltas geram tentativas e perdas de agenda. Não há prova de necessidade de 12.884 a 27.004 pedidos novos.');
note('Resumo',41,'Detalhes, limites e conclusões superadas: Decisoes e fontes. Versão anterior e fontes brutas ficam preservadas nesta pasta.');
for(const [n,c,last] of [['Carteira 1','D',ci],['Protocolos','B',pe],['Cenarios SES','E',se],['Filas e exclusoes','B',fe],['Filas e exclusoes','J',fe]]){
 S[n].getRange(`${c}7:${c}${last}`).format.wrapText=true;
 S[n].getRange(`A7:A${last}`).format.rowHeight=46;
}
note('Premissas',24,'Somente hipóteses deste painel são controles de cenário. Alterar o mix de metas ou fontes requer regenerar dados e rateio.');

// Testes de alteração real de premissas, com restauração antes da exportação.
value('Premissas','B12',.5);wb.recalculate();
const shortageHalf=S.Resumo.getRange('I26').values[0][0];
if(Math.abs(shortageHalf-348)>.001)throw new Error('Falha na sensibilidade SES: '+shortageHalf);
value('Premissas','B12',1);value('Premissas','B10',.3);wb.recalculate();
const slotTest=S['Cenarios SES'].getRange('X7').values[0][0];
if(slotTest!==Math.ceil(d.protocols[0].meta/.7))throw new Error('Falha na sensibilidade de vagas');
value('Premissas','B10',.2);wb.recalculate();
await fs.writeFile(path.join(root,'verificacao/sensibilidades.json'),JSON.stringify({SES_50pct_deficit_c:shortageHalf,faltas_30pct_vagas_protocolo1:slotTest,premissas_restauradas:true},null,2));
const report=await wb.inspect({kind:'table',range:'Resumo!A11:K35',include:'values,formulas',tableMaxRows:30,tableMaxCols:11,maxChars:15000});
await fs.writeFile(path.join(root,'verificacao/resumo.inspect.ndjson'),report.ndjson);
const errs=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:100},summary:'Erros finais'});
await fs.writeFile(path.join(root,'verificacao/erros.inspect.ndjson'),errs.ndjson);
const output=await SpreadsheetFile.exportXlsx(wb);await output.save(path.join(root,'estudo_filas_imagem_20261102_organizada_revisada.xlsx'));
const preview=await wb.render({sheetName:'Resumo',range:'A11:G20',scale:1.3,format:'png'});await fs.writeFile(path.join(root,'verificacao/resumo.png'),new Uint8Array(await preview.arrayBuffer()));
for(const [name,range,file] of [['Resumo','A2:D8','abertura'],['Redistribuicao 20','A6:J12','redistribuicao20'],['Salas por polo','A6:L12','salas']]){
 const pic=await wb.render({sheetName:name,range,scale:1,format:'png'});
 await fs.writeFile(path.join(root,`verificacao/${file}.png`),new Uint8Array(await pic.arrayBuffer()));
}
console.log(report.ndjson.slice(0,7000));console.log(errs.ndjson);console.log('Planilha exportada.');
