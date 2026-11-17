// motor_falso.mjs - um motor falso no lugar da Qlik Engine API, para testar o kit sem o painel.
//
// Responde a qualquer cubo com linhas fixas e numeros que saem do hash da expressao: nao imita
// o SISREG, so da ao kit (motor.js) algo deterministico para medir. Os testes do kit
// (testar_motor_js.mjs) e os do ler_motor e do montador (que chamam este arquivo pelo node)
// usam o mesmo motor.
//
//   node motor_falso.mjs <ordem.json> <pasta> [tamanho] [--recarga-no-meio]
// roda o kit sobre a ordem e grava as partes motor_parte_N.txt na pasta, como o navegador.
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import {fileURLToPath} from 'node:url';

export const ARQ_KIT = new URL('./motor.js', import.meta.url);
export const FONTE = fs.readFileSync(ARQ_KIT, 'utf8');
export const NBSP = '\u00a0';
export const SOL = [['ELETROCARDIOGRAMA', '211020036'], ['HOLTER 24 HORAS', '211020044'],
  ['CONSULTA EM CARDIOLOGIA - INSUFICIENCIA CARDIACA', '301010072'], ['MAMOGRAFIA BILATERAL PARA RASTREAMENTO', '204030188'],
  ['ANGIOTOMOGRAFIA' + NBSP + ' DE CORONARIAS', '206010079'], ['ECOGRAFIA DE MAMAS - BILATERAL', '205020097']];
export const AG = SOL.map(([n, c]) => [n, c]).concat([['MAMOGRAFIA DE RASTREAMENTO', '204030188']]);
export const MESES = ['2024-09', '2024-10', '2025-06', '2026-10'];
export const SITUACOES = ['PROCEDIMENTO REALIZADO', 'PROCEDIMENTO NÃO REALIZADO POR FALTA DO PACIENTE', 'PROCEDIMENTO CANCELADO PELA REGULAÇÃO'];

export const djb2 = s => { let h = 5381; for (let i = 0; i < s.length; i++) h = ((h << 5) + h + s.charCodeAt(i)) >>> 0; return h; };

export function carregar(fonte = FONTE, extra = {}) {
  const ctx = {console, setTimeout, Promise, Date, Math, JSON, ...extra};
  ctx.window = ctx;
  vm.createContext(ctx);
  vm.runInContext(fonte, ctx);
  return ctx;
}

export function motorFalso({recargas = ['2026-10-26T19:32:44.246Z'], campos = null, linhas = null, largura_max = 10000, sem_ag = []} = {}) {
  const pedidos = [], paginas = [], dims_pedidas = [];
  let nLayout = 0;
  const c = carregar().__ms.campos();
  const lista = campos || Object.values(c);
  const valor = (e, k) => (djb2(e + '|' + k) % 900) + 100;
  function gerar(def) {
    const dims = def.qDimensions.map(d => d.qDef.qFieldDefs[0]), meds = def.qMeasures.map(x => x.qDef.qDef);
    meds.forEach(e => pedidos.push(e));
    dims.forEach(d => dims_pedidas.push(d));
    let chaves;
    if (!dims.length) chaves = [[]];
    else if (linhas) chaves = linhas(dims);
    else if (dims[0] === c.nome_sol && dims[1] === c.cod_sol && dims.length === 2) chaves = SOL;
    else if (dims[0] === c.nome_sol && dims[1] === c.cod_sol) chaves = SOL.flatMap(p => [p.concat('I50'), p.concat('I10')]);
    else if (dims[0] === c.nome_ag) chaves = AG.filter(r => !sem_ag.includes(r[0]));
    else if (dims[0] === c.nome_sol && dims.length === 2) chaves = SOL.flatMap(p => [[p[0], 'I50'], [p[0], 'I10'], [p[0], 'Z12']]);
    else if (dims[0] === c.nome_sol) chaves = SOL.map(p => [p[0]]);
    else if ((dims[0] === c.cod_sol || dims[0] === c.cod_ag) && dims.length === 2)
      chaves = ['204030188', '205020097'].flatMap(k => (dims[1] === c.situacao_ag ? SITUACOES : MESES).map(x => [k, x]));
    else if (dims[0] === c.situacao_ag) chaves = SITUACOES.map(x => [x]);
    else if (dims[0] === c.regiao) chaves = [['Regi\u00e3o Oeste'], ['Regi\u00e3o Sul'], ['URD']];
    else if (dims[0] === c.ano) chaves = [['2024'], ['2025'], ['2026']];
    else if (dims[0].startsWith('=Date(MonthStart')) chaves = MESES.map(x => [x]);
    else chaves = [['0'], ['10'], ['20']];
    return chaves.map(k => k.map(t => ({qText: t, qNum: 'NaN'})).concat(meds.map(e => {
      const v = e === 'Now()' ? 46321.958 : e.startsWith('Max({1} data_solicitacao') ? 46321 :
        e.startsWith('Max({1} data_agendamento') ? 46414 : e.startsWith('Min(') ? 41000 : valor(e, k.join('|'));
      return {qText: String(v), qNum: v};
    })));
  }
  const m = {
    async getAppLayout() { return {qLastReloadTime: recargas[Math.min(nLayout++, recargas.length - 1)], qTitle: 'APP FALSO'}; },
    async createSessionObject(def) {
      if (def.qInfo.qType === 'FieldList') return {id: 'fl', getLayout: async () => ({qFieldList: {qItems: lista.map(n => ({qName: n}))}})};
      const todas = gerar(def.qHyperCubeDef), f = def.qHyperCubeDef.qInitialDataFetch[0];
      const pagina = (topo, larg, alt) => {
        paginas.push(larg * alt);
        if (larg * alt > largura_max) throw new Error('Result too large');
        return {qMatrix: todas.slice(topo, topo + alt)};
      };
      return {id: 'cubo', getLayout: async () => ({qHyperCube: {qSize: {qcx: f.qWidth, qcy: todas.length}, qDataPages: [pagina(0, f.qWidth, f.qHeight)]}}),
        getHyperCubeData: async (_, p) => [pagina(p[0].qTop, p[0].qWidth, p[0].qHeight)]};
    },
    async destroySessionObject() {}
  };
  return {m, pedidos, paginas, dims: dims_pedidas};
}

export async function esperar(ctx) {
  for (let i = 0; i < 400; i++) {
    const e = ctx.__ms.estado();
    if (e.feito || e.erro) return JSON.parse(JSON.stringify(e));
    await new Promise(r => setTimeout(r, 5));
  }
  throw new Error('o kit nao terminou');
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const [ordemArq, pasta, tamanho] = process.argv.slice(2).filter(a => !a.startsWith('--'));
  const meio = process.argv.includes('--recarga-no-meio');
  const f = motorFalso(meio ? {recargas: ['2026-10-26T17:36:46.000Z', '2026-10-26T17:36:46.000Z', '2026-10-26T19:32:44.246Z']} : {});
  const ctx = carregar(FONTE, {__app: {model: {enigmaModel: f.m}}});
  ctx.__ms.rodar(JSON.parse(fs.readFileSync(ordemArq, 'utf8')));
  const e = await esperar(ctx);
  if (e.erro) { console.error(e.erro); process.exit(1); }
  ctx.__ms.preparar(Number(tamanho || 300000));
  for (let i = 1; ctx.__ms.parte(i); i++) fs.writeFileSync(path.join(pasta, 'motor_parte_' + i + '.txt'), ctx.__ms.parte(i));
}
