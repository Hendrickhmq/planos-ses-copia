import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
const out=path.dirname(fileURLToPath(import.meta.url));const d=JSON.parse(await fs.readFile(path.join(out,'dados_ampliados.json'),'utf8'));const w=Workbook.create();
const navy='#203F64',ink='#203044';let tn=0;
function sheet(name,title,headers,rows,widths){const s=w.worksheets.add(name);s.showGridLines=false;s.getRangeByIndexes(0,0,rows.length+8,headers.length).format.font={name:'Arial',size:11,color:ink};s.getRange('A2').values=[[title]];s.getRange('A2').format.font={name:'Arial',size:16,bold:true,color:navy};widths.forEach((v,i)=>s.getRangeByIndexes(0,i,1,1).format.columnWidth=v);const r=s.getRangeByIndexes(5,0,rows.length+1,headers.length);r.values=[headers,...rows];r.format.rowHeight=44;r.format.wrapText=true;r.format.verticalAlignment='center';s.tables.add(r,true,'Pesquisa'+(++tn)).style='TableStyleLight9';s.getRangeByIndexes(5,0,1,headers.length).format={fill:navy,font:{name:'Arial',size:11,bold:true,color:'#FFFFFF'},wrapText:true,rowHeight:52,horizontalAlignment:'center'};s.freezePanes.freezeRows(6);return s;}
const dec=sheet('Decisao','Carteira de imagem | pesquisa ampliada', ['Frente','Encaminhamento','Motivo','Condição para contratar'],[
['Densitometria','Cotar primeiro','Menor complexidade operacional relativa; 2.178 pedidos na base','Preço integral, regulação e tarifa formal'],
['RM não ortopédica','Cotar crânio, abdômen e protocolos residuais','Amplia opções além da medicina nuclear','Separar contraste/sedação e a bacia ortopédica do IEV'],
['Óssea + DMSA + paratireoide','Cotar pacote com serviço já instalado','Demanda residual e autorizações privadas localizadas','Capacidade por mês, radiofármaco e tarifa formal'],
['Miocárdio','Cotar repouso + estresse como pacote','Duas etapas podem pertencer à mesma pessoa','Decidir se entra na emenda de imagem ou de cardiologia'],
['PET-CT','Cotação exploratória; prioridade condicionada','Oferta privada localizada, custo integral não confirmado','Indicação SUS, traçador e preço fechado'],
['Mamografia','Alternativa de escala','Fila grande; remuneração não prova margem','Fluxo de investigação dos achados e custo integral'],
['Eco e ECG','Reservados aos R$ 2 milhões de cardiologia','Decisão do usuário','Não incluídos nesta carteira'],
['Mapa Social | Cintilografia','HUB: 5.328 agendamentos; 1 executor','Grupo completo consultado, todos os anos disponíveis','Painel atualizado 03/11/2026 14:32:34'],
['Mapa Social | PET-CT','HBDF: 4.983 agendamentos; 1 executor','Nome exato consultado, todos os anos disponíveis','Ausência de privado no recorte não comprova ausência de contrato'],
['Viabilidade econômica','Ainda não demonstrada','Nenhuma cotação vinculante de prestador foi obtida','Não usar Candanga/incremento como valor automaticamente autorizado']
],[29,54,64,62]);dec.getRange('A3').values=[['Federal de bancada: R$ 1.500.000. Pesquisa em 03/11/2026. Propostas condicionais.']];
const p=sheet('Procedimentos','34 procedimentos | demanda e referências', ['SIGTAP','Nome oficial','Modalidade','Fila em 02/11','Realizados 12m','Base SA R$','Incremento 38.01','Com incremento R$','Candanga R$','Encaminhamento','Sobreposição / cuidado','Entrantes 12m','Agendados 12m','Faltas 12m'],d.procedures.map(x=>[x.code,x.name,x.family,x.stock,x.performed,x.base,x.inc,null,x.candanga,x.decision,x.overlap,x.entries,x.scheduled,x.absent]),[19,65,24,17,18,18,20,21,20,63,67,20,20,20]);
p.getRange('A3').values=[['Produção: out/2025–set/2026. Incremento e Candanga são cenários de referência; não somar.']];
p.getRange('A4').values=[['Fila = pedidos, não pessoas únicas. Entrantes = solicitações abertas + agendadas no método original; não é demanda nova líquida.']];
for(let i=0;i<d.procedures.length;i++){const r=i+7;p.getRange(`H${r}`).formulas=[[`=IF(G${r}="",F${r},ROUND(F${r}*100*(100+G${r}*100)/100,0)/100)`]];}
p.getRange('A7:A40').setNumberFormat('0000000000');p.getRange('F7:F40').setNumberFormat('"R$ "#,##0.00');p.getRange('H7:I40').setNumberFormat('"R$ "#,##0.00');p.getRange('G7:G40').setNumberFormat('0%');p.getRange('H7:H40').format.font.color='#203044';
const pre=sheet('Prestadores','19 perfis | oferta, evidência e limites',['Prestador / perfil','Evidência','Procedimentos publicados','Autorização','Local','Contato público','SES / Mapa Social','Fonte do portfólio','Pendente'],d.providers,[43,42,73,66,62,42,65,85,82]);pre.getRange('A3').values=[['Perfis incluem públicos e pistas não confirmadas. Filiais e operadores hospitalares podem pertencer ao mesmo grupo.']];pre.getRange('A7:I25').format.rowHeight=84;
const lic=sheet('Autorizacoes','23 instalações DF | medicina nuclear',['Matrícula','Razão / designação na base','Cidade','Validade declarada','Área','Fonte'],d.licenses.map(x=>[x['Matrícula'],x['Designação'],x.Cidade,x.Validade,x['Área de atuação'],d.sources[3][2]]),[19,95,25,25,30,105]);lic.getRange('A3').values=[['CSV ANSN/CNEN disponível em 03/11/2026. Autorização não comprova portfólio, vaga SUS ou contrato SES.']];
const src=sheet('Fontes','Fontes e limites de interpretação',['Assunto','Escopo','Fonte / caminho'],d.sources,[28,110,140]);src.getRange('A3').values=[['Fontes comerciais por prestador estão na aba Prestadores; CSV original e manifesto preservados na pasta fontes.']];src.getRange('A7:C15').format.rowHeight=70;
w.recalculate();for(let i=0;i<d.procedures.length;i++){let v=p.getRange(`H${i+7}`).values[0][0];if(Math.abs(v-d.procedures[i].incremental)>.001)throw Error('Preço divergente '+i+' '+v);}
const errors=await w.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!',options:{useRegex:true,maxResults:20},summary:'Erros'});await fs.writeFile(path.join(out,'verificacao.ndjson'),errors.ndjson);
await (await SpreadsheetFile.exportXlsx(w)).save(path.join(out,'Pesquisa ampliada de imagem.xlsx'));
for(const [s,r] of [['Decisao','A6:D10'],['Procedimentos','A6:E12'],['Prestadores','A6:C10'],['Autorizacoes','A6:E12'],['Fontes','A6:C9']]){const b=await w.render({sheetName:s,range:r,scale:1,format:'png'});await fs.writeFile(path.join(out,`previa_${s}.png`),new Uint8Array(await b.arrayBuffer()));}
console.log('34 preços reconciliados; 5 abas exportadas.');console.log(errors.ndjson);
