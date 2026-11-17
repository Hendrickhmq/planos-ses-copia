import fs from 'node:fs/promises';
import {FileBlob,SpreadsheetFile} from '@oai/artifact-tool';
const w=await SpreadsheetFile.importXlsx(await FileBlob.load('outputs/plano4-mapeamento-20261102/Plano 4 - procedimentos filas e nomenclaturas.xlsx'));
console.log((await w.inspect({kind:'workbook,sheet,table',maxChars:3500,tableMaxRows:2,tableMaxCols:4})).ndjson);
for(const [s,r,n] of [['Plano 4','A9:F13','antes-plano'],['Filas escolhidas','A7:E10','antes-filas']]) {
 const p=await w.render({sheetName:s,range:r,scale:1.3});await fs.writeFile(`tmp/readequacao/${n}.png`,new Uint8Array(await p.arrayBuffer()));
}
