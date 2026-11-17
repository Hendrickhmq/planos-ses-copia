import fs from 'node:fs/promises';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
const root='/Users/hendrick/Projetos/planos-ses/estudos imagens';
const data=JSON.parse(await fs.readFile(`${root}/tmp/conversao/portaria-records.json`,'utf8'));
const source='https://www.conass.org.br/conass-informa-n-115-2026-publicada-a-portaria-saes-n-4-282-que-inclui-e-altera-procedimentos-de-apoio-diagnostico-e-terapeutico-por-imagem-e-inclui-incremento-financeiro-na-tabela-de-proc/';
const official='https://www.in.gov.br/web/dou/-/portaria-saes/ms-n-4282-de-19-de-junho-de-2026-713606720';
const wb=Workbook.create();
const s=wb.worksheets.add('Procedimentos');
const ref=wb.worksheets.add('Referências');
const rows=data.map(r=>[r.code.replace(/\D/g,''),r.code,r.name,r.base,r.increment,r.newValue,r.annexes.includes('I')?'Anexo I':'Anexo II']);
const end=rows.length+6;
s.showGridLines=false;
s.getRange(`A1:G${end}`).format.font={name:'Arial',size:10,color:'#202D3A'};
s.getRange(`A1:G${end}`).format.verticalAlignment='center';
s.getRange('A1').values=[['Portaria 4282 exames de imagem']];
s.getRange('A1').format.font={name:'Arial',size:16,bold:true,color:'#17365D'};
s.getRange('A1:G1').format.rowHeight=30;
s.getRange('A2').values=[['Portaria SAES/MS nº 4.282, de 19/06/2026. Publicação original reproduzida pelo Conass em 22/06/2026.']];
s.getRange('A3').values=[['103 procedimentos: 101 no Anexo I e 2 contrastes no Anexo II. Fontes e critérios na aba Referências.']];
s.getRange('A4').values=[['Os percentuais e valores foram transcritos, sem cálculo de valor final. N/A foi mantido como na fonte.']];
s.getRange('A2:G4').format.font={name:'Arial',size:10,color:'#536477'};
s.getRange('A2:G4').format.rowHeight=21;
const headers=['Código SIGTAP','Código publicado','Procedimento/Exame','Valor SIGTAP (R$)','Incremento S.A.','Valor ambulatorial Anexo II (R$)','Origem dos valores'];
s.getRange(`A6:G${end}`).values=[headers,...rows];
s.getRange(`A7:B${end}`).setNumberFormat('@');
s.getRange(`D7:D${end}`).setNumberFormat('"R$" #,##0.00');
s.getRange(`F7:F${end}`).setNumberFormat('"R$" #,##0.00');
s.getRange(`E7:E${end}`).setNumberFormat('0%');
s.getRange(`A7:C${end}`).format.horizontalAlignment='left';
s.getRange(`D7:F${end}`).format.horizontalAlignment='right';
s.getRange(`G7:G${end}`).format.horizontalAlignment='left';
s.getRange(`A7:G${end}`).format.rowHeight=30;
s.getRange(`C7:C${end}`).format.wrapText=true;
for(const [i,width] of [17,21,100,21,20,28,22].entries())s.getRange(`${String.fromCharCode(65+i)}1:${String.fromCharCode(65+i)}${end}`).format.columnWidth=width;
for(let i=0;i<rows.length;i++)if(rows[i][2].length>85)s.getRange(`A${i+7}:G${i+7}`).format.rowHeight=Math.ceil(rows[i][2].length/80)*16+8;
const t=s.tables.add(`A6:G${end}`,true,'ProcedimentosPortaria4282');t.style='TableStyleMedium2';t.showFilterButton=true;
s.getRange('A6:G6').format={fill:'#17365D',font:{name:'Arial',size:10,bold:true,color:'#FFFFFF'},rowHeight:40,wrapText:true,horizontalAlignment:'center',verticalAlignment:'center'};
s.freezePanes.freezeRows(6);

const references=[
 ['Documento','Portaria SAES/MS nº 4.282, de 19 de junho de 2026.'],
 ['Versão utilizada','Publicação original, reproduzida no Conass em 22/06/2026. Não é uma consolidação da republicação de 24/07/2026 ou das retificações posteriores.'],
 ['Link informado pelo usuário',official],
 ['Fonte efetivamente extraída',source],
 ['Acesso ao DOU','O endereço informado não pôde ser carregado nesta sessão. A extração foi feita da reprodução do texto integral no Conass.'],
 ['Consulta','02/11/2026'],
 ['Abrangência','Lista integral dos 101 itens do Anexo I e dos 2 procedimentos incluídos no Anexo II, sem filtrar por especialidade.'],
 ['Anexo III','Os 101 códigos listados no Anexo III já constam no Anexo I. Foram mantidos uma única vez na aba Procedimentos.'],
 ['Anexo IV','Relaciona procedimentos principais e contrastes já presentes na lista. Não foi usado para criar novos códigos de procedimento.'],
 ['Grafias do Anexo IV','A reprodução traz os códigos 02.06.03.0033-7 e 02.074.03.004-9. Na lista de procedimentos foram preservados os códigos publicados nos Anexos I e II, sem tratar essas grafias do Anexo IV como procedimentos adicionais.'],
 ['Códigos','Código SIGTAP contém os 10 dígitos como texto, incluindo zeros iniciais. Código publicado mantém a pontuação da fonte.'],
 ['Valores do Anexo I','Valor SIGTAP e percentual de incremento S.A. transcritos da publicação original. N/A é o texto da fonte e não foi convertido em zero.'],
 ['Valores do Anexo II','Valores do Serviço Ambulatorial dos contrastes: R$ 60,00 para tomografia e R$ 100,00 para ressonância. São valores de referência para composição de créditos financeiros, conforme o Anexo II.'],
 ['Campos em branco','Os contrastes não têm Valor SIGTAP no Anexo I. A coluna de valor do Anexo II aplica-se apenas aos 2 contrastes. Nenhum valor ausente foi estimado.'],
 ['Condições do art. 1º','A publicação vincula os incrementos à modalidade ambulatorial, ao Componente Créditos Financeiros do Programa Agora Tem Especialistas e à habilitação 38.05.'],
 ['Pesquisa','Use Ctrl+F ou Cmd+F. As setas dos cabeçalhos permitem filtrar e ordenar a lista.'],
];
ref.showGridLines=false;
ref.getRange('A1:B20').format.font={name:'Arial',size:10,color:'#202D3A'};
ref.getRange('A1').values=[['Fontes e critérios da extração']];
ref.getRange('A1').format.font={name:'Arial',size:16,bold:true,color:'#17365D'};
ref.getRange('A1:B1').format.rowHeight=30;
ref.getRange('A3:B18').values=references;
ref.getRange('A3:A18').format.font={name:'Arial',size:10,bold:true,color:'#17365D'};
ref.getRange('A1:A18').format.columnWidth=32;
ref.getRange('B1:B18').format.columnWidth=145;
ref.getRange('A3:B18').format.wrapText=true;
ref.getRange('A3:B18').format.verticalAlignment='center';
for(let i=0;i<references.length;i++)ref.getRange(`A${i+3}:B${i+3}`).format.rowHeight=Math.max(32,Math.ceil(references[i][1].length/120)*16+12);
wb.recalculate();
console.log((await wb.inspect({kind:'table',range:'Procedimentos!A6:G10',include:'values',tableMaxRows:5,tableMaxCols:7,maxChars:2500})).ndjson);
console.log((await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!|#NULL!',options:{useRegex:true,maxResults:10},maxChars:500})).ndjson);
for(const [name,range,file] of [['Procedimentos','A1:G14','portaria-preview'],['Referências','A1:B18','portaria-references']]){
 const img=await wb.render({sheetName:name,range,scale:1,format:'png'});
 await fs.writeFile(`${root}/tmp/conversao/${file}.png`,new Uint8Array(await img.arrayBuffer()));
}
const outdir=`${root}/outputs/portaria-4282`;
await fs.mkdir(outdir,{recursive:true});
const out=await SpreadsheetFile.exportXlsx(wb);
await out.save(`${outdir}/Portaria 4282 exames de imagem.xlsx`);
console.log('SAVED',rows.length);
