import fs from 'node:fs/promises';
import {FileBlob,SpreadsheetFile} from '@oai/artifact-tool';
const wb=await SpreadsheetFile.importXlsx(await FileBlob.load('/Users/hendrick/Projetos/planos-ses/planos/redacao_04/estudos/estudo_filas_imagem_20261102_organizada.xlsx'));
console.log((await wb.inspect({kind:'sheet',include:'id,name',maxChars:4000})).ndjson);
const pic=await wb.render({sheetName:'Faltas e pedidos',range:'A19:G38',scale:1.3,format:'png'});
await fs.writeFile(new URL('antes.png',import.meta.url),new Uint8Array(await pic.arrayBuffer()));
