import fs from 'node:fs/promises';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';

const root='/Users/hendrick/Projetos/planos-ses/estudos imagens';
const data=JSON.parse(await fs.readFile(`${root}/tmp/conversao/data.json`,'utf8'));
const wb=Workbook.create();
const sheet=wb.worksheets.add('Tabela SUS Candanga');
sheet.showGridLines=false;
const end=data.rows.length+6;
sheet.getRange(`A1:E${end}`).format.font={name:'Arial',size:10,color:'#202D3A'};
sheet.getRange(`A1:E${end}`).format.verticalAlignment='center';
sheet.getRange('A1').values=[['Tabela SUS Candanga']];
sheet.getRange('A1').format.font={name:'Arial',size:16,bold:true,color:'#17365D'};
sheet.getRange('A1:E1').format.rowHeight=30;
sheet.getRange('A2').values=[['Fonte: TABELA SUS CANGANGA OFICIAL.pdf. SES/DF. Documento SEI 212117347. 57 páginas.']];
sheet.getRange('A3').values=[['Pesquise com Ctrl+F ou Cmd+F. Nas setas dos cabeçalhos, filtre por código, descrição, modalidade ou valor.']];
sheet.getRange('A4').values=[[`${data.rows.length.toLocaleString('pt-BR')} registros. Descrições e modalidades preservadas. A coluna de página indica a localização no PDF.`]];
sheet.getRange('A2:E4').format.font={name:'Arial',size:10,color:'#536477'};
sheet.getRange('A2:E4').format.rowHeight=21;
const headers=['Código','Procedimento/Item','Modalidade','Valor SUS Candanga (R$)','Página do PDF'];
sheet.getRange(`A6:E${end}`).values=[headers,...data.rows];
sheet.getRange(`A7:A${end}`).setNumberFormat('@');
sheet.getRange(`D7:D${end}`).setNumberFormat('"R$" #,##0.00');
sheet.getRange(`E7:E${end}`).setNumberFormat('0');
sheet.getRange(`A7:C${end}`).format.horizontalAlignment='left';
sheet.getRange(`D7:E${end}`).format.horizontalAlignment='right';
sheet.getRange(`A7:E${end}`).format.rowHeight=30;
sheet.getRange(`B7:B${end}`).format.wrapText=true;
const widths=[17,102,20,27,17];
for(let i=0;i<5;i++)sheet.getRange(`${String.fromCharCode(65+i)}1:${String.fromCharCode(65+i)}${end}`).format.columnWidth=widths[i];
for(let i=0;i<data.rows.length;i++){
  const length=data.rows[i][1].length;
  // Allow generous line spacing for long descriptions without reducing font size.
  if(length>90)sheet.getRange(`A${i+7}:E${i+7}`).format.rowHeight=Math.ceil(length/85)*16+8;
}
const table=sheet.tables.add(`A6:E${end}`,true,'TabelaSUSCandanga');
table.style='TableStyleMedium2';
table.showFilterButton=true;
sheet.getRange('A6:E6').format={fill:'#17365D',font:{name:'Arial',size:10,bold:true,color:'#FFFFFF'},rowHeight:34,wrapText:true,horizontalAlignment:'center',verticalAlignment:'center'};
sheet.freezePanes.freezeRows(6);
wb.recalculate();
console.log((await wb.inspect({kind:'table',range:'Tabela SUS Candanga!A6:E10',include:'values',tableMaxRows:5,tableMaxCols:5,maxChars:2500})).ndjson);
console.log((await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!|#NULL!',options:{useRegex:true,maxResults:10},maxChars:1000})).ndjson);
const preview=await wb.render({sheetName:sheet.name,range:'A1:E15',scale:1.5,format:'png'});
await fs.writeFile(`${root}/tmp/conversao/preview.png`,new Uint8Array(await preview.arrayBuffer()));
const output=await SpreadsheetFile.exportXlsx(wb);
await output.save(`${root}/outputs/tabela-sus-candanga/Tabela SUS Candanga.xlsx`);
console.log('SAVED',data.rows.length);
