// md2docx.js — converte o plano de trabalho (markdown) em .docx
//
// Uso:
//   node ferramentas/md2docx.js planos/redacao_NN/plano.md planos/redacao_NN/plano.docx
//   node md2docx.js <plano.md> <saida.docx> --titulo "Nome do objeto"
//   npm run docx -- planos/redacao_NN/plano.md planos/redacao_NN/plano.docx
//
// O título vai no cabeçalho de todas as páginas e nas propriedades do arquivo.
// Sai de `titulo_documento` no estado.yaml ao lado do plano, ou de --titulo. Sem
// nenhum dos dois o script PARA: o título já esteve fixo aqui como "OCI Avaliação
// Cardiológica", e os planos de endoscopia e de imagem saíram com o cabeçalho do
// plano de cardiologia em todas as páginas.
const fs = require('fs');
const path = require('path');
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow, TableCell,
  WidthType, ShadingType, AlignmentType, BorderStyle, PageNumber, Footer, Header,
  TableOfContents, PageOrientation, PageBreak, TabStopType, TabStopPosition, VerticalAlign,
} = require('docx');

const args = process.argv.slice(2);
const iTitulo = args.indexOf('--titulo');
const TITULO_ARG = iTitulo >= 0 ? args.splice(iTitulo, 2)[1] : null;
const [SRC, OUT] = args;
if (!SRC || !OUT) {
  console.error('uso: node md2docx.js <plano.md> <saida.docx> [--titulo "Nome do objeto"]');
  process.exit(2);
}

function tituloDoEstado(plano) {
  const estado = path.join(path.dirname(plano), 'estado.yaml');
  if (!fs.existsSync(estado)) return null;
  const m = fs.readFileSync(estado, 'utf8').match(/^titulo_documento:\s*"([^"]+)"/m);
  return m ? m[1] : null;
}

const TITULO = TITULO_ARG || tituloDoEstado(SRC);
if (!TITULO) {
  console.error(`sem título: declare titulo_documento: "..." no estado.yaml ao lado de ${SRC}, ou use --titulo`);
  process.exit(2);
}

// CRLF vira LF: o arquivo pode ter vindo de um checkout no Windows.
const lines = fs.readFileSync(SRC, 'utf8').replace(/\r\n/g, '\n').split('\n');

// --- geometria (DXA: 1440 = 1 pol; 1 mm ≈ 56.7) -------------------------
const A4_W = 11906, A4_H = 16838, MARGIN = 1134; // 20 mm
const USABLE_P = A4_W - 2 * MARGIN;   // retrato
const USABLE_L = A4_H - 2 * MARGIN;   // paisagem

const GREY = 'F2F2F2', RULE = 'BFBFBF', INK = '1A1A1A', SOFT = '595959';

// --- inline: **negrito**, *itálico*, `código` ---------------------------
function runs(text, opts = {}) {
  const base = { size: opts.size || 20, font: 'Calibri', color: opts.color || INK };
  const out = [];
  const re = /(\*\*[^*]+\*\*|\*[^*\n]+\*|`[^`]+`)/g;
  let last = 0, m;
  const push = (t, extra) => { if (t) out.push(new TextRun({ ...base, ...extra, text: t })); };
  while ((m = re.exec(text)) !== null) {
    push(text.slice(last, m.index), { bold: opts.bold, italics: opts.italics });
    const tok = m[0];
    if (tok.startsWith('**')) push(tok.slice(2, -2), { bold: true, italics: opts.italics });
    else if (tok.startsWith('`')) push(tok.slice(1, -1), {
      font: 'Consolas', size: (opts.size || 20) - 2, color: '7A3E00', bold: opts.bold,
    });
    else push(tok.slice(1, -1), { italics: true, bold: opts.bold });
    last = m.index + tok.length;
  }
  push(text.slice(last), { bold: opts.bold, italics: opts.italics });
  return out.length ? out : [new TextRun({ ...base, text: '' })];
}

const P = (text, o = {}) => new Paragraph({
  children: runs(text, o),
  spacing: { after: o.after === undefined ? 140 : o.after, line: o.line || 276 },
  alignment: o.align || AlignmentType.JUSTIFIED,
  indent: o.indent,
  ...(o.bullet ? { bullet: { level: 0 } } : {}),
  ...(o.border ? { border: o.border } : {}),
  ...(o.shading ? { shading: o.shading } : {}),
  keepNext: o.keepNext,
});

// --- tabela --------------------------------------------------------------
function buildTable(rows, usable) {
  const nCols = rows[0].length;
  const fs_ = nCols > 8 ? 13 : nCols > 5 ? 15 : 17; // meio-pontos
  // largura proporcional ao conteúdo, com piso
  const weight = new Array(nCols).fill(0);
  rows.forEach(r => r.forEach((c, i) => {
    const len = c.replace(/[*`]/g, '').length;
    if (len > weight[i]) weight[i] = Math.min(len, 60);
  }));
  const w = weight.map(x => Math.max(x, 4));
  const sum = w.reduce((a, b) => a + b, 0);
  let widths = w.map(x => Math.floor(usable * x / sum));
  // piso absoluto: nenhuma coluna abaixo de ~11 mm; o déficit sai das mais largas
  const MIN = Math.min(640, Math.floor(usable / nCols));
  let deficit = 0;
  widths = widths.map(x => { if (x < MIN) { deficit += MIN - x; return MIN; } return x; });
  while (deficit > 0) {
    const idx = widths.indexOf(Math.max(...widths));
    const take = Math.min(deficit, widths[idx] - MIN);
    if (take <= 0) break;
    widths[idx] -= take; deficit -= take;
  }
  widths[nCols - 1] += usable - widths.reduce((a, b) => a + b, 0);

  const cell = (txt, i, head) => new TableCell({
    width: { size: widths[i], type: WidthType.DXA },
    margins: { top: 60, bottom: 60, left: 90, right: 90 },
    shading: head ? { type: ShadingType.CLEAR, fill: GREY, color: 'auto' } : undefined,
    verticalAlign: VerticalAlign.CENTER,
    children: [new Paragraph({
      children: runs(txt, { size: fs_, bold: head }),
      spacing: { after: 0, line: 240 },
      alignment: AlignmentType.LEFT,
    })],
  });

  return new Table({
    columnWidths: widths,
    width: { size: usable, type: WidthType.DXA },
    borders: {
      top:   { style: BorderStyle.SINGLE, size: 4, color: RULE },
      bottom:{ style: BorderStyle.SINGLE, size: 4, color: RULE },
      left:  { style: BorderStyle.SINGLE, size: 4, color: RULE },
      right: { style: BorderStyle.SINGLE, size: 4, color: RULE },
      insideHorizontal: { style: BorderStyle.SINGLE, size: 2, color: RULE },
      insideVertical:   { style: BorderStyle.SINGLE, size: 2, color: RULE },
    },
    rows: rows.map((r, ri) => new TableRow({
      tableHeader: ri === 0,
      children: r.map((c, i) => cell(c, i, ri === 0)),
    })),
  });
}

const splitRow = l => l.replace(/^\||\|$/g, '').split('|').map(s => s.trim());
const isSep = l => /^\|[\s:|-]+\|?$/.test(l.trim()) && l.includes('-');

// --- varredura -----------------------------------------------------------
// A planilha (10 colunas, descritivo longo) sai em seção paisagem própria.
const LANDSCAPE_HEADS = [
  '| rubrica | item | descritivo |',
  '| # | item | passo |',
  '| id | risco |',
];
const isLandscapeHead = l => LANDSCAPE_HEADS.some(h => l.startsWith(h));

const sections = [];          // {landscape:bool, children:[]}
let cur = { landscape: false, children: [] };
const flush = () => { if (cur.children.length) sections.push(cur); };
const newSection = ls => { flush(); cur = { landscape: ls, children: [] }; };
let firstH2 = true, capa = [];
const add = el => (firstH2 ? capa : cur.children).push(el);

let i = 0;
while (i < lines.length) {
  const raw = lines[i];
  const l = raw.trimEnd();

  // bloco de código cercado
  if (l.trim().startsWith('```')) {
    i++;
    const buf = [];
    while (i < lines.length && !lines[i].trim().startsWith('```')) buf.push(lines[i]), i++;
    i++;
    buf.forEach((t, k) => add(new Paragraph({
      children: [new TextRun({ text: t || ' ', font: 'Consolas', size: 16, color: '333333' })],
      spacing: { after: k === buf.length - 1 ? 140 : 0, line: 240 },
      shading: { type: ShadingType.CLEAR, fill: 'F7F7F7', color: 'auto' },
      indent: { left: 200 },
    })));
    continue;
  }

  // tabela
  if (l.startsWith('|') && i + 1 < lines.length && isSep(lines[i + 1])) {
    const head = splitRow(l);
    const landscape = isLandscapeHead(l);
    const rows = [head];
    i += 2;
    while (i < lines.length && lines[i].trim().startsWith('|')) rows.push(splitRow(lines[i].trimEnd())), i++;
    if (landscape) {
      newSection(true);
      add(buildTable(rows, USABLE_L));
      add(P('', { after: 0 }));
      newSection(false);
    } else {
      add(buildTable(rows, cur.landscape ? USABLE_L : USABLE_P));
      add(P('', { after: 60 }));
    }
    continue;
  }

  // título 1 → capa
  if (l.startsWith('# ')) {
    capa.push(new Paragraph({
      children: runs(l.slice(2), { size: 40, bold: true }),
      spacing: { before: 2600, after: 200 }, alignment: AlignmentType.CENTER,
    }));
    i++;
    continue;
  }

  // transcricao normativa — texto corrente, recuado. Sem cor e sem moldura: a caixa
  // ambar de aviso, que era o estilo anterior, chamava atencao para a citacao como se
  // ela fosse alerta. Retirada em 05/09/2026 a pedido do usuario.
  if (l.startsWith('>')) {
    const buf = [];
    while (i < lines.length && lines[i].trimEnd().startsWith('>')) buf.push(lines[i].replace(/^>\s?/, '').trimEnd()), i++;
    const par = new Paragraph({
      children: runs(buf.join(' ').replace(/⚠️\s*/, ''), {}),
      spacing: { before: 160, after: 200, line: 276 },
      alignment: AlignmentType.BOTH,
      indent: { left: 340, right: 340 },
    });
    add(par);
    continue;
  }

  // títulos
  if (l.startsWith('#### ')) { add(new Paragraph({ children: runs(l.slice(5), { size: 20, bold: true }), spacing:{before:200,after:100}, keepNext:true })); i++; continue; }
  if (l.startsWith('### ')) {
    add(new Paragraph({ text: '', children: runs(l.slice(4), { size: 22, bold: true }), heading: HeadingLevel.HEADING_2, spacing: { before: 280, after: 120 }, keepNext: true }));
    i++; continue;
  }
  if (l.startsWith('## ')) {
    if (firstH2) {
      firstH2 = false;
      // capa + sumário antes da primeira seção
      cur.children = capa.concat([
        new Paragraph({ children: [new PageBreak()] }),
        new Paragraph({ children: runs('Sumário', { size: 28, bold: true }), spacing: { after: 240 } }),
        new TableOfContents('Sumário', { hyperlink: true, headingStyleRange: '1-2' }),
        new Paragraph({ children: [new PageBreak()] }),
      ]);
    } else {
      add(new Paragraph({ children: [new PageBreak()] }));
    }
    add(new Paragraph({
      text: '', children: runs(l.slice(3), { size: 30, bold: true }),
      heading: HeadingLevel.HEADING_1, spacing: { before: 0, after: 200 },
      border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: RULE, space: 6 } },
    }));
    i++; continue;
  }

  // régua
  if (/^-{3,}$/.test(l.trim())) { i++; continue; }

  // lista
  const li = l.match(/^\s*[-*]\s+(.*)$/);
  if (li) { add(P(li[1], { bullet: true, after: 60, align: AlignmentType.LEFT })); i++; continue; }
  const oli = l.match(/^\s*(\d+)\.\s+(.*)$/);
  if (oli) { add(P(oli[1] + '. ' + oli[2], { after: 60, align: AlignmentType.LEFT, indent: { left: 340, hanging: 340 } })); i++; continue; }

  // parágrafo (junta linhas até a linha em branco)
  if (l.trim() === '') { i++; continue; }
  const buf = [];
  while (i < lines.length) {
    const t = lines[i].trimEnd();
    if (t.trim() === '' || t.startsWith('#') || t.startsWith('|') || t.startsWith('>')
        || /^-{3,}$/.test(t.trim()) || /^\s*[-*]\s+/.test(t) || /^\s*\d+\.\s+/.test(t)
        || t.trim().startsWith('```')) break;
    buf.push(t.trim()); i++;
  }
  if (firstH2) add(P(buf.join(' '), { align: AlignmentType.CENTER, size: 24, color: '404040', after: 400 }));
  else add(P(buf.join(' ')));
}
flush();

// --- cabeçalho / rodapé --------------------------------------------------
const header = new Header({ children: [new Paragraph({
  children: [new TextRun({ text: `Plano de Trabalho · ${TITULO} · SES-DF`, size: 15, color: SOFT, font: 'Calibri' })],
  alignment: AlignmentType.RIGHT,
  border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: RULE, space: 4 } },
  spacing: { after: 120 },
})] });

const footer = new Footer({ children: [new Paragraph({
  alignment: AlignmentType.CENTER,
  children: [new TextRun({ children: ['Página ', PageNumber.CURRENT, ' de ', PageNumber.TOTAL_PAGES], size: 15, color: SOFT, font: 'Calibri' })],
})] });

const doc = new Document({
  creator: 'Plano de trabalho — documento de exercício',
  title: `Plano de Trabalho — ${TITULO}`,
  styles: { default: { document: { run: { font: 'Calibri', size: 20, color: INK } } } },
  features: { updateFields: true },
  sections: sections.map((s, idx) => ({
    properties: {
      page: {
        size: s.landscape
          ? { width: A4_W, height: A4_H, orientation: PageOrientation.LANDSCAPE }
          : { width: A4_W, height: A4_H, orientation: PageOrientation.PORTRAIT },
        margin: { top: MARGIN, bottom: MARGIN, left: MARGIN, right: MARGIN },
      },
      titlePage: idx === 0,
    },
    headers: { default: header },
    footers: { default: footer },
    children: s.children,
  })),
});

Packer.toBuffer(doc).then(b => {
  fs.writeFileSync(OUT, b);
  console.log('gravado:', OUT, (b.length / 1024).toFixed(0) + ' KB');
  console.log('seções:', sections.length, '| paisagem:', sections.filter(s => s.landscape).length);
});
