import fs from 'node:fs/promises';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
const root='/Users/hendrick/Projetos/planos-ses/estudos imagens';
const rows=JSON.parse(await fs.readFile(`${root}/tmp/conversao/comparison-data.json`,'utf8'));
const wb=Workbook.create();
const s=wb.worksheets.add('Comparação');
const ref=wb.worksheets.add('Referências');
const first=9,end=rows.length+8;
s.showGridLines=false;
s.getRange(`A1:G${end}`).format.font={name:'Arial',size:10,color:'#202D3A'};
s.getRange(`A1:G${end}`).format.verticalAlignment='center';
s.getRange('A1').values=[['Comparação SUS Candanga Portaria 4282']];
s.getRange('A1').format.font={name:'Arial',size:16,bold:true,color:'#17365D'};
s.getRange('A1:G1').format.rowHeight=30;
s.getRange('A2').values=[['Base: 223 itens da aba Imagens ambulatoriais (SIA). Correspondência exata pelo código SIGTAP de 10 dígitos.']];
s.getRange('A3').values=[['Descrições comparadas literalmente, incluindo acentuação, espaços, maiúsculas e pontuação. Textos originais preservados lado a lado.']];
s.getRange('A4').values=[['Portaria: 103 itens da publicação original reproduzida pelo Conass. Não localizado refere-se à planilha dessa versão. Ver Referências.']];
s.getRange('A2:G4').format.font={name:'Arial',size:10,color:'#536477'};
s.getRange('A2:G4').format.rowHeight=21;
s.getRange('A5').values=[['Presentes na portaria']];
s.getRange('C5').formulas=[[`=COUNTIFS(D${first}:D${end},"Sim")`]];
s.getRange('D5').values=[['Descrições idênticas']];
s.getRange('F5').formulas=[[`=COUNTIFS(F${first}:F${end},"Idêntica")`]];
s.getRange('A6').values=[['Não localizados']];
s.getRange('C6').formulas=[[`=COUNTIFS(D${first}:D${end},"Não localizado")`]];
s.getRange('D6').values=[['Textos diferentes']];
s.getRange('F6').formulas=[[`=COUNTIFS(F${first}:F${end},"Texto diferente")`]];
s.getRange('A5:G6').format.rowHeight=24;
s.getRange('A5:A6').format.font={name:'Arial',size:10,bold:true,color:'#17365D'};
s.getRange('D5:D6').format.font={name:'Arial',size:10,bold:true,color:'#17365D'};
s.getRange('C5:C6').setNumberFormat('0');s.getRange('F5:F6').setNumberFormat('0');
const headers=['Código SIGTAP','Procedimento/Exame SUS Candanga','Página do PDF','Mesmo código na portaria?','Procedimento/Exame Portaria 4282','Comparação das descrições','Categoria SUS Candanga'];
s.getRange(`A8:G${end}`).values=[headers,...rows];
s.getRange(`A9:A${end}`).setNumberFormat('@');
s.getRange(`C9:C${end}`).setNumberFormat('0');
s.getRange(`A9:G${end}`).format.horizontalAlignment='left';
s.getRange(`C9:C${end}`).format.horizontalAlignment='right';
s.getRange(`A9:G${end}`).format.rowHeight=42;
for(const c of ['B','D','E','F','G'])s.getRange(`${c}9:${c}${end}`).format.wrapText=true;
for(const [i,width] of [18,87,15,26,87,28,38].entries())s.getRange(`${String.fromCharCode(65+i)}1:${String.fromCharCode(65+i)}${end}`).format.columnWidth=width;
for(let i=0;i<rows.length;i++){
 const lines=Math.max(Math.ceil(rows[i][1].length/70),Math.ceil((rows[i][4]||'').length/70));
 s.getRange(`A${i+9}:G${i+9}`).format.rowHeight=Math.max(42,lines*16+10);
}
const table=s.tables.add(`A8:G${end}`,true,'ComparacaoCandangaPortaria');table.style='TableStyleMedium2';table.showFilterButton=true;
s.getRange('A8:G8').format={fill:'#17365D',font:{name:'Arial',size:10,bold:true,color:'#FFFFFF'},rowHeight:40,wrapText:true,horizontalAlignment:'center',verticalAlignment:'center'};
s.getRange(`D9:D${end}`).conditionalFormats.add('containsText',{text:'Não localizado',format:{fill:'#F0F2F5',font:{color:'#536477'}}});
s.getRange(`F9:F${end}`).conditionalFormats.add('containsText',{text:'Texto diferente',format:{fill:'#FFF1CC',font:{color:'#7A5100',bold:true}}});
s.freezePanes.freezeRows(8);
s.freezePanes.freezeColumns(1);
const references=[
 ['Arquivo SUS Candanga',`${root}/outputs/tabela-sus-candanga/Tabela SUS Candanga.xlsx`],
 ['Escopo da base','Somente a aba Imagens ambulatoriais, com 223 registros SIA. A aba completa da SUS Candanga não foi usada neste recorte.'],
 ['Fonte original SUS Candanga','TABELA SUS CANGANGA OFICIAL.pdf. SES/DF. Documento SEI 212117347. A coluna Página do PDF permite localizar cada item.'],
 ['Arquivo Portaria 4282',`${root}/outputs/portaria-4282/Portaria 4282 exames de imagem.xlsx`],
 ['Escopo da portaria','Aba Procedimentos: 101 itens do Anexo I e 2 contrastes do Anexo II. Publicação original de 22/06/2026, sem consolidar a republicação ou retificações posteriores.'],
 ['Link informado pelo usuário','https://www.in.gov.br/web/dou/-/portaria-saes/ms-n-4282-de-19-de-junho-de-2026-713606720'],
 ['Fonte usada na extração da portaria','https://www.conass.org.br/conass-informa-n-115-2026-publicada-a-portaria-saes-n-4-282-que-inclui-e-altera-procedimentos-de-apoio-diagnostico-e-terapeutico-por-imagem-e-inclui-incremento-financeiro-na-tabela-de-proc/'],
 ['Critério de correspondência','Igualdade exata do código SIGTAP de 10 dígitos, armazenado como texto. A pontuação da apresentação dos códigos não interfere na correspondência. Não foi usado pareamento por semelhança de nomes.'],
 ['Critério das descrições','Comparação literal dos textos presentes nas duas planilhas. Acentos, maiúsculas, espaços e pontuação podem produzir Texto diferente mesmo quando o código é igual. As descrições não foram corrigidas.'],
 ['Leitura do resultado','Sim significa que o mesmo código existe na planilha da portaria. Idêntica exige também descrição literalmente igual. Texto diferente destaca o mesmo código com redações distintas, para conferência.'],
 ['Não localizado','Código ausente entre os 103 itens da planilha da portaria utilizada. Não é uma conclusão sobre outras versões da norma ou sobre cobertura assistencial.'],
 ['Campos vazios','A descrição da portaria fica em branco quando o código não foi localizado; a comparação das descrições recebe Não se aplica.'],
 ['Categorias','Copiadas da aba Imagens ambulatoriais da SUS Candanga. São a classificação de trabalho criada nessa aba, não uma categoria publicada pela portaria.'],
 ['Atualização','Comparação dos arquivos locais em 02/11/2026. O resultado registra essa versão dos dados.'],
];
ref.showGridLines=false;
ref.getRange('A1:B16').format.font={name:'Arial',size:10,color:'#202D3A'};
ref.getRange('A1').values=[['Fontes e critérios da comparação']];
ref.getRange('A1').format.font={name:'Arial',size:16,bold:true,color:'#17365D'};
ref.getRange('A1:B1').format.rowHeight=30;
ref.getRange('A3:B16').values=references;
ref.getRange('A3:A16').format.font={name:'Arial',size:10,bold:true,color:'#17365D'};
ref.getRange('A1:A16').format.columnWidth=34;
ref.getRange('B1:B16').format.columnWidth=145;
ref.getRange('A3:B16').format.wrapText=true;
ref.getRange('A3:B16').format.verticalAlignment='center';
for(let i=0;i<references.length;i++)ref.getRange(`A${i+3}:B${i+3}`).format.rowHeight=Math.max(38,Math.ceil(references[i][1].length/115)*16+12);
wb.recalculate();
console.log((await wb.inspect({kind:'table',range:'Comparação!A5:G6',include:'values,formulas',tableMaxRows:2,tableMaxCols:7,maxChars:1800})).ndjson);
console.log((await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!|#NULL!',options:{useRegex:true,maxResults:10},maxChars:500})).ndjson);
for(const [name,range,file] of [['Comparação','A1:G15','comparison-preview'],['Referências','A1:B16','comparison-references']]){
 const img=await wb.render({sheetName:name,range,scale:1,format:'png'});
 await fs.writeFile(`${root}/tmp/conversao/${file}.png`,new Uint8Array(await img.arrayBuffer()));
}
const outdir=`${root}/outputs/comparacao-sus-candanga-portaria-4282`;
await fs.mkdir(outdir,{recursive:true});
const output=await SpreadsheetFile.exportXlsx(wb);
await output.save(`${outdir}/Comparação SUS Candanga Portaria 4282.xlsx`);
console.log('SAVED',rows.length);
