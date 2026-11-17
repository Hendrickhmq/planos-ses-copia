import fs from 'node:fs/promises';
import {FileBlob,SpreadsheetFile} from '@oai/artifact-tool';
const root=process.cwd();
const d=JSON.parse(await fs.readFile('tmp/readequacao/data.json','utf8'));
const wb=await SpreadsheetFile.importXlsx(await FileBlob.load('outputs/plano4-mapeamento-20261102/Plano 4 - procedimentos filas e nomenclaturas.xlsx'));
const filas=wb.worksheets.add('Filas SUS Candanga');
const diff=wb.worksheets.add('Diferenças');
const cost=wb.worksheets.add('Metas e valores');
const ref=wb.worksheets.add('Referência Candanga');
const blue='#203F64',ink='#233449',muted='#56677C';
function setup(s,title,widths,rows=40){
 s.showGridLines=false;s.tabColor=blue;
 const all=s.getRangeByIndexes(0,0,rows,widths.length);
 all.format.font={name:'Arial',size:11,color:ink};all.format.rowHeight=24;all.format.verticalAlignment='center';
 widths.forEach((v,i)=>s.getRangeByIndexes(0,i,rows,1).format.columnWidth=v);
 s.getRange('A2').values=[[title]];s.getRange('A2').format.font={name:'Arial',size:16,bold:true,color:blue};s.getRange('A2').format.rowHeight=30;
 s.getRangeByIndexes(2,0,1,widths.length).format.borders={bottom:{style:'thin',color:'#91A4BB'}};
}
function table(s,row,heads,rows,name){
 const grid=s.getRangeByIndexes(row-1,0,rows.length+1,heads.length);grid.values=[heads,...rows];
 const t=s.tables.add(grid,true,name);t.style='TableStyleLight9';t.showFilterButton=true;
 const header=s.getRangeByIndexes(row-1,0,1,heads.length);header.format={fill:blue,font:{name:'Arial',size:11,bold:true,color:'#FFFFFF'},wrapText:true,rowHeight:48,horizontalAlignment:'center',verticalAlignment:'center'};
 for(let i=0;i<rows.length;i++){
  const r=s.getRangeByIndexes(row+i,0,1,heads.length);r.format.wrapText=true;r.format.fill=i%2===0?'#F0F4F8':'#FFFFFF';
  const height=Math.max(53,...rows[i].map((v,j)=>Math.ceil(String(v??'').length/Math.max(6,([9,45,19,58,28,14,14,14,16,64,60,18,17][j]||40)*0.87))*15+14));
  r.format.rowHeight=Math.min(180,height);
 }
 s.freezePanes.freezeRows(row);s.freezePanes.freezeColumns(2);
}
function note(s,cell,text){s.getRange(cell).values=[[text]];s.getRange(cell).format.font={name:'Arial',size:11,color:muted};}
function money(s,range){s.getRange(range).setNumberFormat('"R$ "#,##0.00');s.getRange(range).format.horizontalAlignment='right';}
function num(s,range){s.getRange(range).setNumberFormat('#,##0');s.getRange(range).format.horizontalAlignment='right';}

// Original data and formulas are retained. These three headings distinguish the historical basis.
const main=wb.worksheets.getItem('Plano 4');
main.getRange('A2').values=[['Plano 4 — base anterior à readequação SUS Candanga']];
main.getRange('A6').values=[['Readequação de 02/11/2026: consultar Filas SUS Candanga, Diferenças e Metas e valores. As quatro primeiras abas preservam a base anterior.']];
main.getRange('A7').values=[['Os 11 códigos existem em SIA. Parede abdominal e angiotomografia de coronárias têm enquadramento pendente; valores novos estão nas abas de readequação.']];

setup(ref,'SUS Candanga — referência SIA e fontes',[19,83,14,20,13,17],85);
note(ref,'A4','Fonte local: Tabela SUS Candanga.xlsx. SEI 212117347. Somente SIA; SIH não participa das buscas.');
note(ref,'A5','Recorte: códigos do plano e itens de ultrassonografia/tomografia para conferir alternativas. Descrições publicadas preservadas.');
table(ref,7,['Código (10 dígitos)','Descrição publicada','Modalidade','Valor Candanga (R$)','Página PDF','Linha na fonte'],d.reference.map(r=>[r.code,r.name,r.mod,r.price,r.page,r.row]),'ReferenciaCandangaSIA');
const re=d.reference.length+7;
ref.getRange(`A8:A${re}`).setNumberFormat('@');money(ref,`D8:D${re}`);num(ref,`E8:F${re}`);
// Set heights using the actual widths for this source view.
d.reference.forEach((r,i)=>ref.getRange(`A${i+8}:F${i+8}`).format.rowHeight=Math.max(42,Math.ceil(r.name.length/68)*16+12));
const sourceRow=re+4;
const sources=[
 ['SC1 — tabela de preços',`${root}/Tabela SUS Candanga.xlsx — Tabela SUS Candanga, linhas 7–2962. Fonte declarada: TABELA SUS CANGANGA OFICIAL.pdf, SEI 212117347. A vigência do anexo local não foi certificada por nova cópia do PDF.`],
 ['SC2 — base do mapeamento',`${root}/outputs/plano4-mapeamento-20261102/Plano 4 - procedimentos filas e nomenclaturas.xlsx. Plano 4!A10:L20 e Filas escolhidas!A8:K22. As abas originais mantêm suas evidências S1–S8.`],
 ['SC3 — preço anterior',`${root}/../planos/redacao_04/plano.md, 8.1 e 8.2. Unitários conferidos com estado.yaml; quantidades seguem o plano vigente, não as quantidades divergentes do controle.`],
 ['SC4 — comparação federal',`${root}/outputs/portaria-4282/Portaria 4282 exames de imagem.xlsx. A extração é da publicação original; diferenças financeiras usam o preço efetivamente adotado no plano, sem apresentar esta versão como consolidação normativa atual.`],
 ['SC5 — Lei 7.897/2026','https://www.sinj.df.gov.br/sinj/Norma/cb7aa4f1e15e4be9ba631f9fccf17a1f/Lei_7897_2026.html — arts. 4º e 6º. Consulta em 02/11/2026. Remuneração combina SIGTAP e complementação distrital; o valor Candanga não recebe novamente o incremento federal do plano.'],
 ['SC6 — Deliberação 46/2026','https://www.sinj.df.gov.br/sinj/Norma/08cdc67f1b9a46158271100a13d7d382/ses_cg_dlb_46_2026.html — arts. 2º–5º e 12. Consulta em 02/11/2026. A tabela mantém regras SIGTAP. Contratos vigentes exigem adequação formal. O valor aplicável é o vigente na realização.'],
 ['Critério de vinculação','Chave: código SIGTAP de 10 dígitos + modalidade SIA. Retirou-se apenas pontuação para cruzar códigos. Um código no painel comprova o vínculo administrativo histórico, mas não resolve sozinho equivalência clínica ou faturamento.'],
 ['Tratamento das filas','A base SES de 10/09/2026 é contagem de exames. O Mapa de 29/10/2026 é contagem de pedidos, em fotografia separada. Não foram atualizadas as filas nem estimadas pessoas únicas. Nenhum dos outros 212 nomes foi incluído automaticamente.'],
 ['Tratamento das metas','79.144 exames foram mantidos para isolar o efeito de preço. Os 572 exames adicionais têm meta apenas por código; não houve rateio por fila. Os cálculos que incluem F09 e F14 são condicionais ao enquadramento.'],
 ['Contraste e apoio','Não há item 0206030045 localizado na tabela local. Nenhum adicional de R$ 60 foi lançado. Mantidos R$ 956.160 de apoio apenas para comparação aritmética; admissibilidade, eventual duplicidade e pactuação dos custos exigem análise própria.'],
 ['Escopo da entrega','Readequação da planilha e relação de mudanças a incorporar no plano. Nenhum DOCX, Markdown ou instrumento jurídico foi alterado. O relatório não valida atributos SIGTAP, habilitações ou faturamento individual.']
];
ref.getRangeByIndexes(sourceRow-1,0,sources.length,2).values=sources;
ref.getRangeByIndexes(sourceRow-1,0,sources.length,1).format.font={name:'Arial',size:11,bold:true,color:blue};
ref.getRangeByIndexes(sourceRow-1,0,sources.length,2).format.wrapText=true;
sources.forEach((r,i)=>ref.getRange(`A${sourceRow+i}:B${sourceRow+i}`).format.rowHeight=Math.max(60,Math.ceil(r[1].length/68)*16+12));

setup(filas,'Plano 4 — filas vinculadas à SUS Candanga',[9,48,19,62,29,15,15,15,19,68,68,17],29);
note(filas,'A4','15 filas: 13 com correspondência compatível; 2 com código candidato que exige confirmação técnica da SES-DF (F09 e F14).');
note(filas,'A5','Os códigos são os publicados na tabela. Os protocolos da fila permanecem identificados; preços não autorizam cobrança por vaso ou lado.');
note(filas,'A6','A base SES é de 10/09/2026. O Mapa de 29/10/2026 é outra fotografia. Os totais não representam pessoas únicas.');
const fr=d.filas.map(f=>[f.id,f.original,f.code,null,f.status,null,null,null,null,f.protocol,f.names.join('\n'),null]);
table(filas,8,['ID','Fila de origem preservada','Código Candanga / candidato','Descrição exata SUS Candanga (SIA)','Resultado do enquadramento','Base SES 10/09 (exames)','Mapa 29/10 (pedidos)','Preço anterior (R$)','Candanga SIA (R$)','Diferença e ação necessária','Nome exato no Mapa Social','Linha tabela local'],fr,'ReadequacaoFilasCandanga');
for(let i=0;i<15;i++){
 const r=i+9,s=i+8,c=d.filas[i].cand;
 filas.getRange(`D${r}`).formulas=[[`=INDEX('Referência Candanga'!$B$8:$B$${re},MATCH(SUBSTITUTE(SUBSTITUTE(C${r},".",""),"-",""),'Referência Candanga'!$A$8:$A$${re},0))`]];
 filas.getRange(`F${r}`).formulas=[[`='Filas escolhidas'!E${s}`]];filas.getRange(`G${r}`).formulas=[[`='Filas escolhidas'!G${s}`]];
 filas.getRange(`H${r}`).values=[[d.filas[i].old_price]];
 filas.getRange(`I${r}`).formulas=[[`=INDEX('Referência Candanga'!$D$8:$D$${re},MATCH(SUBSTITUTE(SUBSTITUTE(C${r},".",""),"-",""),'Referência Candanga'!$A$8:$A$${re},0))`]];
 filas.getRange(`L${r}`).values=[[c.row]];
 filas.getRange(`A${r}:L${r}`).format.rowHeight=d.filas[i].pending?104:80;
}
num(filas,'F9:G25');money(filas,'H9:I23');
filas.getRange('A25').values=[['Total']];filas.getRange('F25:G25').formulas=[['=SUM(F9:F23)','=SUM(G9:G23)']];
filas.getRange('A26').values=[['Base SES nas duas filas a validar']];filas.getRange('F26').formulas=[['=SUMIF(E9:E23,"Validar enquadramento",F9:F23)']];num(filas,'F26');
note(filas,'A28','F09: candidato abdômen total. F14: candidato TC de tórax. Ambos constam na tabela, mas o nome da fila não é um item específico publicado.');
filas.getRange('E9:E23').conditionalFormats.add('containsText',{text:'Validar',format:{fill:'#FFF1CC',font:{color:'#805500',bold:true}}});

setup(cost,'Plano 4 — comparação de metas e preços',[19,62,15,20,20,19,16,22,22,22,63],40);
note(cost,'A4','Mesmas metas do plano vigente: 79.144 exames. Preço anterior = plano 8.1; preço novo = item SIA da tabela local, sem novo incremento.');
note(cost,'A5','Simulação condicional: abdômen total contém parede abdominal, e TC de tórax contém angiotomografia de coronárias.');
note(cost,'A6','A meta não foi redistribuída por fila, região ou mês. Validar F09/F14 antes de fechar o orçamento e atualizar o plano.');
table(cost,8,['Código SIGTAP','Descrição SUS Candanga','Meta mantida (exames)','Preço anterior (R$)','Preço Candanga (R$)','Variação unitária (R$)','Variação (%)','Total anterior (R$)','Total Candanga (R$)','Diferença total (R$)','Efeito no enquadramento'],d.procs.map(p=>[p.code,null,null,p.old_price,null,null,null,null,null,null,p.code==='02.05.02.004-6'?'Inclui F09 (parede abdominal). Total condicional.':p.code==='02.06.02.003-1'?'Inclui F14 (angiotomografia coronária). Total condicional.':'Mesmo código SIA. Preservar protocolo e demais regras de registro.']),'ComparacaoValoresCandanga');
for(let i=0;i<11;i++){
 const r=i+9,old=i+10;
 cost.getRange(`B${r}`).formulas=[[`=INDEX('Referência Candanga'!$B$8:$B$${re},MATCH(SUBSTITUTE(SUBSTITUTE(A${r},".",""),"-",""),'Referência Candanga'!$A$8:$A$${re},0))`]];
 cost.getRange(`C${r}`).formulas=[[`='Plano 4'!C${old}`]];
 cost.getRange(`E${r}`).formulas=[[`=INDEX('Referência Candanga'!$D$8:$D$${re},MATCH(SUBSTITUTE(SUBSTITUTE(A${r},".",""),"-",""),'Referência Candanga'!$A$8:$A$${re},0))`]];
 for(const [col,f] of Object.entries({F:`=ROUND(E${r}-D${r},2)`,G:`=F${r}/D${r}`,H:`=ROUND(C${r}*D${r},2)`,I:`=ROUND(C${r}*E${r},2)`,J:`=ROUND(I${r}-H${r},2)`}))cost.getRange(`${col}${r}`).formulas=[[f]];
 cost.getRange(`A${r}:K${r}`).format.rowHeight=68;
}
cost.getRange('A21').values=[['Total assistencial']];
for(const c of ['C','H','I','J'])cost.getRange(`${c}21`).formulas=[[`=SUM(${c}9:${c}19)`]];
cost.getRange('A21:K21').format.font={name:'Arial',size:11,bold:true,color:blue};
num(cost,'C9:C21');money(cost,'D9:F19');money(cost,'H9:J21');cost.getRange('G9:G19').setNumberFormat('0.0%');
cost.getRange('A24:C31').values=[
 ['Comparação global','Anterior (R$)','Candanga (R$)'],
 ['Produção assistencial',null,null],
 ['Apoio mantido para comparação',956160,956160],
 ['Total simulado',null,null],
 ['Diferença novo menos anterior',null,null],
 ['Recurso indicado no plano',11592762,11592762],
 ['Saldo aritmético frente ao recurso',null,null],
 ['Variação assistencial (%)',null,null]
];
cost.getRange('B25:C25').formulas=[['=H21','=I21']];
cost.getRange('B27:C27').formulas=[['=SUM(B25:B26)','=SUM(C25:C26)']];
cost.getRange('C28').formulas=[['=ROUND(C27-B27,2)']];
cost.getRange('B30:C30').formulas=[['=ROUND(B29-B27,2)','=ROUND(C29-C27,2)']];
cost.getRange('C31').formulas=[['=J21/H21']];
cost.getRange('A24:C31').format.rowHeight=40;cost.getRange('A24:A31').format.wrapText=true;
cost.getRange('A24:C24').format={fill:blue,font:{name:'Arial',size:11,bold:true,color:'#FFFFFF'},wrapText:true,rowHeight:44};
money(cost,'B25:C30');cost.getRange('C31').setNumberFormat('0.0%');
note(cost,'A33','O total Candanga inclui os candidatos F09/F14 e apoio inalterado. É comparação de preços, não orçamento final homologado.');
note(cost,'A34','Contraste: nenhum adicional presumido. O código 02.06.03.004-5 não foi localizado na tabela local.');
note(cost,'A35','Confirmar o enquadramento e a composição do apoio antes de recalcular metas por período, capacidade, repasses e plano de aplicação.');

setup(diff,'Plano 4 — diferenças encontradas',[20,49,69,69,69,22],40);
note(diff,'A4','Comparação da base anterior com os itens publicados na SUS Candanga. Filas sem mudança de código mantêm seus qualificadores.');
const changes=[
 ['F01, F02, F06, F07, F08, F10','Seis filas de ultrassom','Ecografia, abreviações ou qualificadores de idade no nome da fila.','Nome publicado SUS Candanga pelo mesmo código SIA.','Adotar a descrição publicada na contratação e preservar a identificação original na regulação.','Nomenclatura'],
 ['F03','Abdômen total','Meta do código também contém parede abdominal.','Item publicado: ULTRASSONOGRAFIA DE ABDOMEN TOTAL.','A fila de abdômen total é compatível. Manter F09 separada até confirmar seu enquadramento.','Separar fila F09'],
 ['F04 e F05','Doppler MMII e carótidas','Duas filas e territórios diferentes sob 02.05.01.004-0.','A tabela mantém ULTRASSONOGRAFIA DOPPLER COLORIDO DE VASOS, R$ 115,61. Não há desdobramento publicado por esses territórios no recorte.','Manter subitens por território e bilateralidade. Não fundir filas nem multiplicar a remuneração automaticamente.','Código mantido'],
 ['F09','Parede abdominal','3.121 exames da base vinculados a 02.05.02.004-6 no painel.','Não localizado item específico de ultrassonografia de parede abdominal. Abdômen total permanece apenas candidato.','Solicitar confirmação formal SES-DF do código e da regra assistencial. Não apresentar a fila como abdômen total validado.','Validar enquadramento'],
 ['F11 e F12','TC abdômen superior e pelve','Adulto com contraste e sem sedação, sob dois códigos.','Mesmos códigos, ambos R$ 309,25. A nomenclatura de pelve usa barras.','Preservar protocolo. Trocar referência de preço e nome publicado, sem presumir pagamento adicional de contraste.','Protocolo mantido'],
 ['F13 e F15','TC tórax com e sem contraste','Filas distintas sob o mesmo código 02.06.02.003-1.','Mesmo item TC de tórax, R$ 309,25. O nome não distingue esses protocolos.','Manter filas separadas na agenda, com um mesmo item de remuneração, sujeito às regras SIGTAP.','Código mantido'],
 ['F14','Angiotomografia coronária','1.397 exames da base vinculados a TC de tórax no painel.','Não localizado item específico de angiotomografia de coronárias. TC de tórax permanece apenas candidato.','Confirmar com SES-DF o código, protocolo e possibilidade de remuneração antes de contratar ou faturar.','Validar enquadramento'],
 ['11 códigos','Referência de preço','O plano aplica valor SIGTAP com incremento da Portaria 4.282 e truncamento.','Valor SUS Candanga publicado por código e modalidade SIA.','Substituir o preço final. Não aplicar novamente o percentual da portaria ao valor Candanga. Valores lado a lado em Metas e valores.','Alterar 11 preços'],
 ['79.144 exames','Impacto financeiro','R$ 10.636.542,52 de produção assistencial.','R$ 10.390.824,04 com as mesmas metas, incluindo F09/F14 de modo condicional. Redução de R$ 245.718,48.','Recalcular o plano de aplicação após confirmar os candidatos e o apoio. Não converter a diferença em exames extras sem definir o novo mix.','Simulação condicional'],
 ['02.06.03.004-5','Contraste','Referência acessória de R$ 60 citada no controle, fora da planilha assistencial.','Código não localizado na tabela SUS Candanga local.','Não inserir cobrança autônoma por analogia. Confirmar com SES-DF o tratamento remuneratório e preservar a necessidade assistencial do insumo.','Sem adicional presumido'],
 ['Meta e fila','Unidades e fotografias','78.572 exames na base SES; meta 79.144. O Mapa usa pedidos e outras datas.','Preços e nomenclatura alterados, sem mudar as fotografias nem repartir os 572 adicionais por fila.','Não usar o saldo de preço como fila nova, nem somar fotografias para estimar pessoas.','Quantidades preservadas'],
 ['Cadastro e faturamento','Validação do código','O painel registra o código de solicitação; isso não comprova toda a regra de produção.','Existência na tabela é conferida por código + SIA. Os atributos SIGTAP continuam aplicáveis.','Validar compatibilidades e registro. A equivalência clínica de F09/F14 permanece aberta.','Validação técnica'],
 ['Documento vigente','Trechos a readequar','O plano usa a referência federal nas seções 3.3 e 8.1, preços em 8.2, risco R-14 e quantitativos em várias seções.','Descrição e valor Candanga nos itens, com protocolo da fila preservado.','Atualizar 2.2, 3.1, 3.3, 4.8, 6, 7 (R-04/R-14), 8 e 9 conforme a decisão de metas e enquadramento. DOCX/MD permanecem sem alteração nesta entrega.','Revisão documental'],
 ['Controle anterior','Divergência de 8 exames','estado.yaml soma 79.152; plano e planilha-base somam 79.144.','Simulação mantém as metas publicadas no plano.','Sincronizar o controle ao revisar o plano. Não usar as 8 unidades divergentes no orçamento comparativo.','Diferença preexistente'],
 ['Outros nomes do Mapa','Limite do objeto','228 nomes × código, sendo 16 grafias selecionadas para 15 filas.','Os outros 212 pares permanecem como catálogo histórico.','Não incluí-los por compartilhar código. Parede abdominal conserva duas grafias sem duplicar a base.','Escopo preservado'],
 ['Apoio administrativo','Comparação global','Apoio de R$ 956.160,00 no plano anterior.','Mantido apenas no cenário comparativo.','Revisar admissibilidade e evitar duplicação de componentes já cobertos pelo procedimento antes da pactuação final.','Revisar composição']
];
table(diff,7,['Fila / referência','Tema','Situação anterior','SUS Candanga / diferença','Alteração ou providência','Situação'],changes,'DiferencasPlanoCandanga');
changes.forEach((r,i)=>diff.getRange(`A${i+8}:F${i+8}`).format.rowHeight=104);
diff.getRange(`F8:F${changes.length+7}`).conditionalFormats.add('containsText',{text:'Validar',format:{fill:'#FFF1CC',font:{color:'#805500',bold:true}}});
note(diff,'A26','Fontes dos preços, códigos, regras e critérios estão em Referência Candanga. As quatro abas originais permitem conferir a base anterior.');

// User follow-up: show considered requests, returned requests and the non-returned queue.
filas.getRange('M8:O8').values=[['Solicitações 29/10 (pedidos)','Devolvidos 29/10 (pedidos)','Fila válida 29/10 (solicitações − devolvidos)']];
filas.getRange('M8:O8').format={fill:blue,font:{name:'Arial',size:11,bold:true,color:'#FFFFFF'},wrapText:true,horizontalAlignment:'center',verticalAlignment:'center'};
filas.getRange('M8:O26').format.columnWidth=24;
filas.getRange('M9:O26').format.font={name:'Arial',size:11,color:ink};
filas.getRange('M9:O26').format.verticalAlignment='center';
for(let i=0;i<15;i++){
 const f=d.filas[i],r=i+9;
 const selected=d.catalog.map((c,j)=>({c,row:j+8})).filter(({c})=>c.codigo_formatado===f.code&&f.names.includes(c.nome));
 if(selected.length!==f.names.length||selected.some(({c})=>typeof c.devolvidas!=='number'))throw new Error(`Returned count unavailable: ${f.id}`);
 filas.getRange(`N${r}`).formulas=[[`=SUM(${selected.map(({row})=>`'Nomes no Mapa'!F${row}`).join(',')})`]];
 filas.getRange(`M${r}`).formulas=[[`=G${r}`]];
 filas.getRange(`O${r}`).formulas=[[`=M${r}-N${r}`]];
 filas.getRange(`M${r}:O${r}`).format.fill=i%2===0?'#F0F4F8':'#FFFFFF';
}
for(const c of ['M','N','O'])filas.getRange(`${c}25`).formulas=[[`=SUM(${c}9:${c}23)`]];
filas.getRange('O26').formulas=[['=SUMIF(E9:E23,"Validar enquadramento",O9:O23)']];
num(filas,'M9:O26');
filas.tables.items.find(t=>t.name==='ReadequacaoFilasCandanga').delete();
const ft=filas.tables.add('A8:O23',true,'ReadequacaoFilasCandanga');ft.style='TableStyleLight9';ft.showFilterButton=true;
note(filas,'A29','Correção do critério: Fila válida = Solicitações − Devolvidos. Solicitações corresponde ao valor original do Mapa 29/10, sem somar os devolvidos.');
note(filas,'A30','Critério informado pelo usuário: as solicitações incluem os devolvidos. A leitura anterior que somava os devolvidos foi descartada.');
note(filas,'A31','Resultado negativo indica devolvidos maiores que solicitações na base transcrita. Conferir mesma data, filtro e universo; valores não foram zerados.');
filas.getRange('O9:O23').conditionalFormats.add('cellIs',{operator:'lessThan',formula:0,format:{fill:'#FDE8E7',font:{color:'#A12622',bold:true}}});

cost.getRange('L8:N8').values=[['Solicitações 29/10 (pedidos)','Devolvidos 29/10 (pedidos)','Fila válida 29/10 (solicitações − devolvidos)']];
cost.getRange('L8:N8').format={fill:blue,font:{name:'Arial',size:11,bold:true,color:'#FFFFFF'},wrapText:true,horizontalAlignment:'center',verticalAlignment:'center'};
cost.getRange('L8:N21').format.columnWidth=24;
cost.getRange('L9:N21').format.font={name:'Arial',size:11,color:ink};
cost.getRange('L9:N21').format.verticalAlignment='center';
for(let i=0;i<11;i++){
 const r=i+9;
 for(const [dest,src] of [['L','M'],['M','N'],['N','O']])cost.getRange(`${dest}${r}`).formulas=[[`=SUMIF('Filas SUS Candanga'!$C$9:$C$23,A${r},'Filas SUS Candanga'!$${src}$9:$${src}$23)`]];
 cost.getRange(`L${r}:N${r}`).format.fill=i%2===0?'#F0F4F8':'#FFFFFF';
}
for(const c of ['L','M','N'])cost.getRange(`${c}21`).formulas=[[`=SUM(${c}9:${c}19)`]];
num(cost,'L9:N21');
cost.tables.items.find(t=>t.name==='ComparacaoValoresCandanga').delete();
const ct=cost.tables.add('A8:N19',true,'ComparacaoValoresCandanga');ct.style='TableStyleLight9';ct.showFilterButton=true;
note(cost,'A36','Fila válida = Solicitações − Devolvidos, conforme correção do usuário. Solicitações sem acréscimo. Valores negativos por fila exigem conferência da base.');

diff.getRange('E10').values=[['Separar MMII e carótidas em itens assistenciais com o mesmo código. Não localizado código SIA específico distinto para cada fila. Ecodoppler transcraniano e Doppler obstétrico têm outros alvos; não são substitutos.']];
diff.getRange('E11').values=[['Manter parede abdominal em item separado de abdômen total. Não localizado código SIA específico para a parede. O código herdado continua candidato, pendente de confirmação SES-DF.']];
diff.getRange('E13').values=[['Separar tórax com e sem contraste em itens de agenda. A tabela local publica um mesmo código SIA de TC de tórax; não foram encontrados dois códigos específicos que permitam desdobrar por contraste.']];
diff.getRange('E14').values=[['Separar angiotomografia em item assistencial próprio, mantendo código pendente. Não localizado código SIA específico para angiotomografia coronária na tabela local. Não substituir por exame de técnica diferente.']];
note(diff,'A27','É possível separar filas e protocolos em itens assistenciais. Códigos de remuneração distintos exigem correspondência específica na tabela e nas regras SIGTAP.');
note(diff,'A28','Conta corrigida: 73.217 solicitações − 55.944 devolvidos = 17.273 (saldo aritmético). Há quatro filas com saldo negativo; conferir antes de usar no planejamento.');
const additionalSource=sourceRow+sources.length;
ref.getRange(`A${additionalSource}:B${additionalSource+1}`).values=[
 ['Fila válida — definição e fonte','Critério corrigido pelo usuário: Solicitações inclui devolvidos. Fila válida = Solicitações − Devolvidos. Solicitações usa o valor original da coluna Mapa 29/10. Devolvidos usa Nomes no Mapa!F8:F235, com o mesmo par nome × código. Não se soma devolvidos a solicitações.'],
 ['Fila válida — conferência','A descrição metodológica anterior foi substituída pelo critério informado pelo usuário. Quatro pares da base têm devolvidos maiores que solicitações: F03, F11, F12 e F15. O resultado negativo foi preservado e destacado. Conferir a extração e os filtros antes de fixar metas.']
];
ref.getRange(`A${additionalSource}:A${additionalSource+1}`).format.font={name:'Arial',size:11,bold:true,color:blue};
ref.getRange(`A${additionalSource}:B${additionalSource+1}`).format.wrapText=true;
ref.getRange(`A${additionalSource}:B${additionalSource+1}`).format.rowHeight=94;

wb.recalculate();
for(const r of ['Filas SUS Candanga!A25:I26','Metas e valores!A21:J21','Metas e valores!A24:C31'])console.log((await wb.inspect({kind:'table',range:r,include:'values,formulas',tableMaxRows:10,tableMaxCols:11,maxChars:3500})).ndjson);
console.log((await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:30},maxChars:2000})).ndjson);
// Verify changed input affects the calculated production value, then restore it.
const targetRow=d.reference.findIndex(r=>r.code==='0205020097')+8;
const priceCell=ref.getRange(`D${targetRow}`);const price=priceCell.values[0][0];
const before=cost.getRange('I21').values[0][0];priceCell.values=[[price+1]];
if(Math.abs(cost.getRange('I21').values[0][0]-before-14689)>0.001)throw new Error('Price sensitivity failed');
priceCell.values=[[price]];wb.recalculate();
if(Math.abs(cost.getRange('I21').values[0][0]-d.totals.new)>0.001)throw new Error('Restored total differs');
if(filas.getRange('O25').values[0][0]!==17273||filas.getRange('N25').values[0][0]!==55944||filas.getRange('M25').values[0][0]!==73217)throw new Error('Queue totals mismatch');
for(let r=9;r<=23;r++)if(filas.getRange(`O${r}`).values[0][0]!==filas.getRange(`G${r}`).values[0][0]-filas.getRange(`N${r}`).values[0][0])throw new Error('Queue subtraction differs');
console.log((await wb.inspect({kind:'table',range:'Filas SUS Candanga!M8:O12',include:'values,formulas',tableMaxRows:5,tableMaxCols:3,maxChars:2000})).ndjson);
const previews=[['Filas SUS Candanga','M8:O13','fila-valida'],['Metas e valores','L8:N13','fila-por-codigo'],['Diferenças','D10:F14','desdobramentos'],['Referência Candanga',`A${additionalSource}:B${additionalSource+1}`,'fonte-fila-valida']];
for(const [sheetName,range,file] of previews){const img=await wb.render({sheetName,range,scale:1,format:'png'});await fs.writeFile(`tmp/readequacao/${file}.png`,new Uint8Array(await img.arrayBuffer()));}
const outdir='outputs/plano4-sus-candanga-20261102';await fs.mkdir(outdir,{recursive:true});
const output=await SpreadsheetFile.exportXlsx(wb);await output.save(`${outdir}/Plano 4 - readequação SUS Candanga.xlsx`);
console.log('SAVED',d.totals, 'reference rows',d.reference.length);
