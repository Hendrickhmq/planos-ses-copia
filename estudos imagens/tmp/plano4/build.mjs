import fs from 'node:fs/promises';
import { Workbook, SpreadsheetFile } from '@oai/artifact-tool';
const here='/Users/hendrick/Projetos/planos-ses/estudos imagens';
const d=JSON.parse(await fs.readFile(`${here}/tmp/plano4/data.json`,'utf8'));
const out=`${here}/outputs/plano4-mapeamento-20261102`;
const wb=Workbook.create();
const main=wb.worksheets.add('Plano 4');
const filas=wb.worksheets.add('Filas escolhidas');
const nomes=wb.worksheets.add('Nomes no Mapa');
const fontes=wb.worksheets.add('Fontes e ressalvas');
const ink='#233449',blue='#203F64',muted='#56677C';
function base(s,end,cols,widths,title){
 s.showGridLines=false;
 const r=s.getRangeByIndexes(0,0,end,cols);
 r.format.font={name:'Arial',size:11,color:ink};
 r.format.verticalAlignment='center';r.format.rowHeight=24;
 widths.forEach((w,i)=>s.getRangeByIndexes(0,i,end,1).format.columnWidth=w);
 s.getRange('A2').values=[[title]];
 s.getRange('A2').format.font={name:'Arial',size:16,bold:true,color:blue};
 s.getRange('A2').format.rowHeight=30;
 s.getRangeByIndexes(2,0,1,cols).format.borders={bottom:{style:'thin',color:'#91A4BB'}};
}
function table(s,row,headers,rows,name,heights=60){
 const end=row+rows.length;
 s.getRangeByIndexes(row-1,0,rows.length+1,headers.length).values=[headers,...rows];
 const t=s.tables.add(s.getRangeByIndexes(row-1,0,rows.length+1,headers.length),true,name);
 t.style='TableStyleLight9';t.showFilterButton=true;
 s.getRangeByIndexes(row-1,0,1,headers.length).format={fill:blue,font:{name:'Arial',size:11,bold:true,color:'#FFFFFF'},wrapText:true,rowHeight:42,horizontalAlignment:'center',verticalAlignment:'center'};
 s.getRangeByIndexes(row,0,rows.length,headers.length).format.wrapText=true;
 s.getRangeByIndexes(row,0,rows.length,headers.length).format.rowHeight=heights;
 for(let i=0;i<rows.length;i++)s.getRangeByIndexes(row+i,0,1,headers.length).format.fill=i%2===0?'#F0F4F8':'#FFFFFF';
 s.freezePanes.freezeRows(row);s.freezePanes.freezeColumns(2);
 return end;
}
base(main,35,12,[19,59,13,13,13,12,53,13,13,66,13,13],'Plano 4 — procedimentos e filas de origem');
main.tabColor=blue;
main.getRange('A4').values=[['Meta de exames']];main.getRange('C4').formulas=[['=SUM(C10:C20)']];
main.getRange('D4').values=[['Códigos']];main.getRange('E4').formulas=[['=COUNTA(A10:A20)']];
main.getRange('F4').values=[['Filas de origem']];main.getRange('H4').formulas=[["=COUNTA('Filas escolhidas'!A8:A22)"]];
main.getRange('C4').setNumberFormat('#,##0');
main.getRange('A5').values=[['Valor global (R$)']];main.getRange('B5').values=[[11592702.52]];main.getRange('B5').setNumberFormat('"R$ "#,##0.00');
main.getRange('A6').values=[['Base: plano vigente v26, de 21/10/2026, conferido no DOCX e no Markdown. Quantidades são exames, não pessoas.']];
main.getRange('A7').values=[['Os 11 códigos têm mais de um nome no catálogo. Somente 15 filas compõem a origem do objeto; parede abdominal tem duas grafias.']];
main.getRange('A6:L7').format.font={name:'Arial',size:11,color:muted};
const mrows=d.procs.map(p=>[p.code,p.name,p.target,null,null,null,p.filas.join('\n'),null,null,p.relation,p.state,null]);
table(main,9,['Código SIGTAP','Procedimento no plano','Meta vigente (exames)','Fila base 10/09','Acréscimo à base','Filas escolhidas (nº)','Filas de origem selecionadas','Nomes no catálogo 29/10','Com fila > 0 em 29/10 (nomes)','Relação entre os nomes','Qtd. em estado.yaml','Estado menos plano'],mrows,'ProcedimentosPlano4',53);
for(let i=10;i<=20;i++){
 main.getRange(`D${i}`).formulas=[[`=SUMIF('Filas escolhidas'!$D$8:$D$22,A${i},'Filas escolhidas'!$E$8:$E$22)`]];
 main.getRange(`E${i}`).formulas=[[`=C${i}-D${i}`]];
 main.getRange(`F${i}`).formulas=[[`=COUNTIF('Filas escolhidas'!$D$8:$D$22,A${i})`]];
 main.getRange(`H${i}`).formulas=[[`=COUNTIF('Nomes no Mapa'!$A$8:$A$235,A${i})`]];
 main.getRange(`I${i}`).formulas=[[`=COUNTIFS('Nomes no Mapa'!$A$8:$A$235,A${i},'Nomes no Mapa'!$E$8:$E$235,">0")`]];
 main.getRange(`L${i}`).formulas=[[`=K${i}-C${i}`]];
}
main.getRange('A22').values=[['Total']];
for(const c of ['C','D','E','F','H','I','K','L'])main.getRange(`${c}22`).formulas=[[`=SUM(${c}10:${c}20)`]];
main.getRange('A22:L22').format.font={name:'Arial',size:11,bold:true,color:blue};
main.getRange('A22:L22').format.borders={top:{style:'thin',color:'#91A4BB'}};
main.getRange('A24').values=[['Principais agrupamentos documentados']];main.getRange('A24').format.font={name:'Arial',size:13,bold:true,color:blue};
main.getRange('A26:B29').values=[
 ['02.05.01.004-0','Doppler venoso bilateral de MMII e ecodoppler de carótidas → Doppler colorido de vasos.'],
 ['02.05.02.004-6','Abdômen total e parede abdominal → Ultrassonografia de abdômen total.'],
 ['02.06.02.003-1','Tórax com contraste, tórax sem contraste e angiotomografia de coronárias → TC de tórax.'],
 ['Divergência','estado.yaml mantém 8 exames a mais. As metas desta planilha seguem plano.docx, subseções 2.2 e 8.2.']
];
main.getRange('B26:B29').format.wrapText=true;main.getRange('A26:B29').format.rowHeight=60;
main.getRange('L10:L20').conditionalFormats.add('cellIs',{operator:'notEqual',formula:0,format:{fill:'#FFF1CC',font:{color:'#805500'}}});
for(const c of ['C','D','E','F','H','I','K','L']){main.getRange(`${c}10:${c}22`).setNumberFormat('#,##0');main.getRange(`${c}10:${c}22`).format.horizontalAlignment='right';}

base(filas,25,11,[9,53,84,19,14,14,14,28,70,54,43],'Filas escolhidas — nomes originais e enquadramento');
filas.getRange('A4').values=[['15 filas de origem. A fila de parede abdominal reúne duas grafias verificadas, sem duplicar os 3.121 exames da base.']];
filas.getRange('A5').values=[['Fila base é a extração SES de 10/09. Mapa Social de 15/09 e de 29/10 aparece como fotografia separada. Fontes S1 a S4 na última aba.']];
const frows=d.filas.map(f=>[f.id,f.original,f.names.join('\n'),f.code,f.base,f.fila15,f.fila29,f.kind,f.relation,f.source_original+'\n'+f.source_mapping,f.source_catalog]);
table(filas,7,['ID','Nome na planilha de origem (10/09)','Nome exato no Mapa Social / SISREG (catálogo 29/10)','Código SIGTAP','Base SES 10/09 (exames)','Fila Mapa 15/09 (pedidos)','Fila Mapa 29/10 (pedidos)','Tipo de correspondência','Como o exame foi enquadrado no plano','Localização na origem e no vínculo de código','Localização no catálogo'],frows,'FilasEscolhidasPlano4',76);
filas.getRange('A24').values=[['Total de exames da base']];for(const c of ['E','F','G'])filas.getRange(`${c}24`).formulas=[[`=SUM(${c}8:${c}22)`]];
filas.getRange('A24:K24').format.font={name:'Arial',size:11,bold:true,color:blue};
filas.getRange('E8:G24').setNumberFormat('#,##0');filas.getRange('E8:G24').format.horizontalAlignment='right';

base(nomes,237,10,[19,58,89,30,14,14,46,40,67,12],'Nomes no Mapa — catálogo dos 11 códigos');
nomes.getRange('A4').values=[['228 pares de nome × código encontrados em 29/10/2026: 16 correspondem às 15 filas selecionadas; 212 são outros nomes sob os mesmos códigos.']];
nomes.getRange('A5').values=[['103 pares têm fila > 0. Célula vazia de estoque significa somente agendamentos, sem estoque informado por esse par; não equivale a zero.']];
const nrows=d.catalog.map(c=>[c.codigo_formatado,d.procs.find(p=>p.code===c.codigo_formatado).name,c.nome,c.selected,c.fila,c.devolvidas,c.presenca,c.space_note,c.interpretation,c.source_row]);
table(nomes,7,['Código SIGTAP','Procedimento correspondente no plano','Nome exato no catálogo do Mapa Social','Vínculo com as filas escolhidas','Fila 29/10 (pedidos)','Devolvidas 29/10 (pedidos)','Presença nas tabelas da fonte','Particularidade da grafia','Interpretação do vínculo de código','Linha CSV (S4)'],nrows,'CatalogoNomesPlano4',50);
nomes.getRange('E8:F235').setNumberFormat('#,##0');nomes.getRange('E8:F235').format.horizontalAlignment='right';
nomes.getRange('J8:J235').setNumberFormat('0');
nomes.getRange('D8:D235').conditionalFormats.add('containsText',{text:'Fila escolhida',format:{fill:'#E5EEF8',font:{bold:true,color:blue}}});

const records=[
 ['S1 — plano vigente','Versão v26, 21/10/2026. Meta de 79.144 exames e valor global de R$ 11.592.702,52. DOCX conferido contra plano.md. Quantidades e nomenclatura do documento prevalecem sobre o arquivo de controle.',`${d.plan}/plano.docx — 1.4, 2.2 e 8.2\n${d.plan}/plano.md — linhas 173–183 e 797–810`],
 ['S2 — fila base SES','Extração de 10/09/2026, recebida em 15/09/2026. As 15 linhas escolhidas somam 78.572 exames. O cabeçalho original inclui partes moles em ultrassom, removida do objeto em 22/09.',`${d.fontes}/filas_ultrassom_tomografia_20260915.xlsx — Exames de imagem, A4:B14 e A34:B38`],
 ['S3 — vínculo fila/código','Recoleta de 06/10 confirma os códigos e os nomes das filas selecionadas. Não substitui a fila base da SES. Vínculo pelo campo codigo_sigtap_solicitacao, não por semelhança de nomes.',`${d.fontes}/mapa_social_20261006.xlsx — 1 · Procedimentos, A1:E18; 6 · Fila e pessoas, A2:E17`],
 ['S4 — catálogo completo','Inventário de 29/10/2026. Catálogo inclui pares presentes em solicitações, agendamentos ou em ambos. Cruzamento exato dos 11 códigos identifica 228 pares; 103 têm estoque positivo. O número de nomes varia conforme a data e o universo.',`${d.root}/registros/mapa_social/imagem/catalogo_20261029.csv\n${d.root}/registros/mapa_social/imagem/dados/fontes/mapa_social_20261029_inventario_bruto/README.md`],
 ['S5 — validação US','Coleta de 15/09. Confirma os códigos de Doppler, parede abdominal e a variante de grafia. Os totais do Mapa Social desta data não foram usados para recalcular a meta vigente.',`${d.fontes}/validacao_ultrassom_20260915.xlsx — 1 · SIGTAP (L-001), linhas 3–14\n${d.fontes}/validacao_ultrassom.md`],
 ['S6 — validação TC','Coleta de 15/09. Confirma TC de tórax com e sem contraste e angiotomografia de coronárias no código 02.06.02.003-1.',`${d.fontes}/mapa_social_tomografia_20260915.xlsx — 1-Cinco procedimentos\n${d.fontes}/mapa_social_tomografia.md — seção 2`],
 ['S7 — conferência de nomes','Registra a correspondência das três camadas de nomes: planilha original, SISREG e Tabela do SUS. A redação deste material menciona faturamento, mas a evidência usada aqui é o código registrado no painel.',`${d.plan}/dados/conferencia_procedimentos.md`],
 ['S8 — arquivo de controle','estado.yaml tem quantidades que somam 79.152, enquanto o plano vigente tem 79.144. Divergências: mama +1, abdômen total +1, transvaginal +1, TC tórax +1, TC abdômen superior +1, TC pelve +2 e próstata +1. Fontes originais preservadas.',`${d.plan}/estado.yaml — parametros.valor_unitario.por_codigo`],
 ['Método','O nome exato do catálogo e o código foram preservados. Espaços consecutivos e U+00A0 foram normalizados apenas para localizar a correspondência dos nomes entre fontes; os registros do catálogo não foram fundidos. Parede abdominal mantém as duas grafias em uma fila de origem.', 'Análise dos arquivos locais em 02/11/2026; sem nova consulta ao painel nesta tarefa.'],
 ['Escopo das alternativas','Os 228 pares não são 228 exames selecionados nem 228 sinônimos clínicos. Os outros 212 pares compartilham código, mas sua inclusão no objeto não está documentada. O catálogo contém outros territórios, protocolos, faixas etárias e urgências.','Aba Nomes no Mapa: filtrar Vínculo com as filas escolhidas.'],
 ['Medidas e contagem','Fila = pendente de regulação, corrigida e reenviada e pendente por fila de espera. Devolvidas estão separadas. Somar filas não produz pessoas únicas; somas de pares nome × código também podem conter sobreposição de pedidos. Não foi calculado um total geral de pessoas.',`${d.root}/registros/mapa_social/imagem/README.md`],
 ['Enquadramento documental','Código compartilhado comprova o vínculo no painel. Não comprova, isoladamente, faturamento realizado, equivalência clínica integral ou possibilidade de trocar o exame solicitado. Qualificadores como contraste, sedação e território continuam relevantes para identificar a fila.', 'Plano, 2.2; coletas S3, S5 e S6.'],
 ['Exclusão — partes moles','Ecografia de partes moles não integra o plano desde 22/09/2026. Na coleta de 15/09 aparecia sob 02.05.02.006-2 (ultrassonografia de articulação), mas esse código não está entre os 11 escolhidos. Os 2.974 exames da base foram excluídos dos totais.',`${d.plan}/dados/conferencia_procedimentos.md — revisão de 22/09/2026`],
 ['Contraste acessório','O código 02.06.03.004-5 é mencionado no controle como secundário de contraste e está fora da planilha assistencial. Não é um 12º procedimento escolhido. O plano, 4.8, estima 12.890 TC com contraste dentro das 13.618 TC.',`${d.plan}/estado.yaml — secundario_contraste\n${d.plan}/plano.docx — 4.8 e 8.2`],
 ['Composição da meta','79.144 exames = 78.572 da base + 572 de acréscimo planejado. Ultrassom: 65.526. Tomografia: 13.618. O plano publica a meta por código; não foi inventado rateio do acréscimo por nome de fila.',`${d.plan}/plano.docx — 2.2 e 3.1`],
 ['Data das fotografias','As colunas de fila do Mapa Social usam datas explícitas, sem misturá-las com a meta. A recoleta de 01/11 disponível localmente cobre apenas mama e transvaginal e não foi usada para substituir parcialmente o inventário geral de 29/10.',`${d.fontes}/mapa_social_20261101_executante.md`],
 ['Painel de origem','Mapa Social da Saúde, MPDFT. Dados SISREG/DATASUS. Recarga do inventário: 29/10/2026 18:32:39. Solicitação mais recente da base: 27/10/2026. Os caminhos locais e as linhas permitem rastrear as evidências.', 'https://paineis-ext.mpdft.mp.br/extensions/mapasauderegulamentacao/mapasauderegulamentacao.html'],
];
base(fontes,records.length+8,3,[28,123,111],'Fontes, critérios e diferenças encontradas');
fontes.getRange('A4').values=[['S1 a S8 identificam as evidências usadas. Os dados originais foram somente lidos.']];
table(fontes,6,['Fonte / tema','O que foi usado e como interpretar','Arquivo e localização'],records,'FontesMapeamentoPlano4',82);
fontes.freezePanes.freezeColumns(1);
wb.recalculate();
const inspection=await wb.inspect({kind:'table',range:"'Plano 4'!A9:L22",include:'values,formulas',tableMaxRows:14,tableMaxCols:12,maxChars:18000});
await fs.writeFile(`${here}/tmp/plano4/inspect.ndjson`,inspection.ndjson);
const errors=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:50},summary:'Erros de fórmula'});
console.log(errors.ndjson);
console.log(JSON.stringify({totals:main.getRange('C22:L22').values,selected:filas.getRange('E24:G24').values}));
await fs.mkdir(out,{recursive:true});
const xlsx=await SpreadsheetFile.exportXlsx(wb);await xlsx.save(`${out}/Plano 4 - procedimentos filas e nomenclaturas.xlsx`);
for(const [s,range,file] of [[main,'A2:J20','plano'],[filas,'A7:I12','filas'],[nomes,'A7:I13','nomes'],[fontes,'A6:C10','fontes']]){
 const png=await wb.render({sheetName:s.name,range,scale:1,format:'png'});
 await fs.writeFile(`${here}/tmp/plano4/${file}.png`,new Uint8Array(await png.arrayBuffer()));
}
console.log('Exportado e renderizado.');
