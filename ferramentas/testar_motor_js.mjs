// testar_motor_js.mjs - o kit do motor do Mapa Social (mapa_social/motor.js) sabe montar as
// expressoes, paginar, dividir a saida e parar quando deve?
//
// Roda o kit num contexto isolado, como no navegador, com um motor falso no lugar da Qlik
// Engine API. As funcoes que montam as expressoes de conjunto se testam pelo texto exato; a
// execucao inteira, pela forma da saida e pelas paradas (recarga no meio, campo que nao existe).
// So node, sem dependencias.
import assert from 'node:assert/strict';
import {execFileSync} from 'node:child_process';
import {test} from 'node:test';

import {ARQ_KIT as ARQ, FONTE, NBSP, SOL, carregar, djb2, esperar, motorFalso} from './mapa_social/motor_falso.mjs';

const puro = x => JSON.parse(JSON.stringify(x));
const desfazer = s => s.replace(/\{U\+([0-9A-F]{4})\}/g, (_, h) => String.fromCharCode(parseInt(h, 16)));

function comMotor(falso) {
  return carregar(FONTE, {__app: {model: {enigmaModel: falso.m}}});
}
const ORDEM = {
  contrato: '2026-10-27', tipo: 'medicao', plano: 'planos/redacao_99', saida: 'transcricao', janela_viva_meses: 24,
  dimensoes: ['regiao', 'idade', 'cid', 'entrantes', 'ano'],
  objetos: [
    {id: '09.02.01.006-9', tipo: 'oci', nome: 'insuficiencia cardiaca', ficha: 'dados/fontes/sigtap_0902010069_102026.md',
      codigos: ['02.11.02.003-6', '02.11.02.004-4', '03.01.01.007-2'], cid_aceito: 'codigo_cid_solicitado={"I*"}',
      cid_finalidade: 'codigo_cid_solicitado={"I50*"}', idade: {min: 18, max: 130}, sexo: 'ambos',
      filas: [{nome: 'CONSULTA EM CARDIOLOGIA - INSUFICIENCIA CARDIACA', papel: 'consulta', entrada: true},
        {nome: 'ELETROCARDIOGRAMA', papel: 'exame', obrigatorio: true}, {nome: 'HOLTER 24 HORAS', papel: 'exame', obrigatorio: true}]},
    {id: '02.04.03.018-8', tipo: 'exame', nome: 'mamografia', codigos: ['02.04.03.018-8'], sexo: 'feminino',
      filas: [{nome: 'MAMOGRAFIA BILATERAL PARA RASTREAMENTO'}], termos: ['MAMOGRAF']},
    {id: '02.06.01.007-9', tipo: 'exame', nome: 'angiotomografia', codigos: ['02.06.01.007-9'],
      filas: [{nome: 'ANGIOTOMOGRAFIA  DE CORONARIAS'}]}
  ]
};

// ------------------------------------------------------------- texto e expressoes
test('djb2 igual ao do python e ao da sondagem', () => {
  const K = carregar().__ms;
  assert.equal(K.djb2(''), 5381);
  assert.equal(K.djb2('a'), 177670);
  assert.equal(K.djb2('sondagem-ms|' + 'x'.repeat(50000) + '|ascii {U+00A0} fim 0123456789'), 1033203379);
});

test('ascii escapa o que a transcricao perderia, e so isso', () => {
  const K = carregar().__ms;
  assert.equal(K.ascii('A' + NBSP + 'B{\u00c9}\n'), 'A{U+00A0}B{U+007B}{U+00C9}}{U+000A}');
  assert.equal(desfazer(K.ascii('MAMA ' + NBSP + ' {x} \u2013 \u00c7')), 'MAMA ' + NBSP + ' {x} \u2013 \u00c7');
  assert.match(K.ascii('qualquer coisa \u00e9 \u00e7 \u2013 ' + NBSP), /^[\x20-\x7e]*$/);
});

test('codigo sem o zero da frente, com curinga', () => {
  const K = carregar().__ms;
  assert.equal(K.codigo('02.04.03.018-8'), '204030188');
  assert.equal(K.codigo('0301010072'), '301010072');
  assert.equal(K.codigo('204030188'), '204030188');
  assert.equal(K.codigo('02.05*'), '205*');
  assert.equal(K.codigo('03.01.01*'), '30101*');
  assert.ok(K.casa_codigo('205020097', '205*'));
  assert.ok(!K.casa_codigo('204030188', '205*'));
});

test('literal com aspa simples e lista de nomes', () => {
  const K = carregar().__ms;
  assert.equal(K.lit("D'AGUA"), "'D''AGUA'");
  assert.equal(K.mod_nomes(['A', "B'C"]), "descri\u00e7\u00e3o_procedimento_solicitacao={'A','B''C'}");
  assert.equal(K.conj([]), '{1}');
  assert.equal(K.conj(['a', '', 'b']), '{1<a, b>}');
});

test('o CID da ficha na tabela de agendamentos ganha o curinga', () => {
  const K = carregar().__ms;
  assert.equal(K.cid_ag('codigo_cid_solicitado={"I50*","Z136"}'), 'CID_agendamento={"I50*","Z136*"}');
  assert.equal(K.cid_ag(''), '');
});

test('os campos da expressao de CID', () => {
  const K = carregar().__ms;
  assert.deepEqual(puro(K.campos_da_expressao('codigo_cid_solicitado={"J3*"}')), ['codigo_cid_solicitado']);
  assert.deepEqual(puro(K.campos_da_expressao('cid_errado={"J3*"}, idade_solicitacao={">=18<=130"}')), ['cid_errado', 'idade_solicitacao']);
});

test('idade e sexo da ficha', () => {
  const K = carregar().__ms;
  assert.equal(K.mod_idade({min: 18, max: 130}), 'idade_solicitacao={">=18<=130"}');
  assert.equal(K.mod_idade({min: 40}), 'idade_solicitacao={">=40<=130"}');
  assert.equal(K.mod_idade(null), '');
  // exclui o sexo oposto: quem nao tem sexo ligado continua
  assert.equal(K.mod_sexo('feminino'), "cns_usuario_solicitacao=E({1<sexo_usuario={'MASCULINO'}>} cns_usuario_solicitacao)");
  assert.equal(K.mod_sexo('masculino'), "cns_usuario_solicitacao=E({1<sexo_usuario={'FEMININO'}>} cns_usuario_solicitacao)");
  assert.equal(K.mod_sexo('ambos'), '');
});

test('janelas contadas da solicitacao mais recente', () => {
  const K = carregar().__ms;
  assert.equal(K.data_br(46321), '26/10/2026');
  const j = puro(K.janelas(46321, 24));
  assert.equal(j.viva, 'data_solicitacao={">=26/10/2024"}');
  assert.equal(j.agendadas_12m, 'data_agendamento={">=26/10/2025<=25/10/2026"}');
  assert.equal(j.entrantes_sol, 'data_solicitacao={">=01/10/2024"}');
  assert.equal(j.entrantes_ag, 'Ano_Agendamento={">=2024"}');
  assert.equal(j.entrantes_desde, '2024-10');
  assert.equal(j.oferta, 'data_agendamento={">=01/10/2024"}');
  // o fim do mes nao transborda
  const s31 = K.menos_meses(46112, 0);            // 31/03/2026
  assert.equal(K.data_br(s31), '31/03/2026');
  assert.equal(K.data_br(K.menos_meses(46112, 1)), '28/02/2026');
  assert.equal(K.data_br(K.menos_meses(46112, 13)), '28/02/2025');
});

test('o nome digitado sem o espaco nao separavel acha o nome exato', () => {
  const K = carregar().__ms, nomes = SOL.map(p => p[0]);
  assert.deepEqual(puro(K.resolver('ANGIOTOMOGRAFIA  DE CORONARIAS', nomes)), ['ANGIOTOMOGRAFIA' + NBSP + ' DE CORONARIAS']);
  assert.deepEqual(puro(K.resolver('angiotomografia de coronarias', nomes)), ['ANGIOTOMOGRAFIA' + NBSP + ' DE CORONARIAS']);
  assert.deepEqual(puro(K.resolver('NAO EXISTE', nomes)), []);
  // as duas grafias da mesma fila, o exato primeiro
  assert.deepEqual(puro(K.resolver('VIDEOENDOSCOPIA NASAL FLEXIVEL', ['VIDEOENDOSCOPIA  NASAL  FLEXIVEL', 'X', 'VIDEOENDOSCOPIA NASAL FLEXIVEL'])),
    ['VIDEOENDOSCOPIA NASAL FLEXIVEL', 'VIDEOENDOSCOPIA  NASAL  FLEXIVEL']);
  assert.ok(K.tem_termo('MAMOGRAFIA BILATERAL PARA RASTREAMENTO', 'mamograf'));
  // o termo casa pelo comeco da palavra: RINOLOGIA nao acha ENDOCRINOLOGIA (prova de 26/10/2026)
  assert.ok(K.tem_termo('CONSULTA EM  RINOLOGIA', 'RINOLOGIA'));
  assert.ok(!K.tem_termo('CONSULTA EM ENDOCRINOLOGIA - GERAL', 'RINOLOGIA'));
  assert.ok(K.tem_termo('031. TC DE CRANIO ADULTO C/CONTRASTE', 'tc cranio'));
  assert.ok(K.parecido('MAMOGRAFIA BILATERAL PARA RASTREAMENTO - ACIMA DE 70', 'MAMOGRAFIA BILATERAL PARA RASTREAMENTO'));
  assert.ok(!K.parecido('ECOGRAFIA DE MAMAS - BILATERAL', 'MAMOGRAFIA BILATERAL PARA RASTREAMENTO'));
});

test('as partes se juntam, e cada uma diz tamanho e hash', () => {
  const K = carregar().__ms, texto = 'x'.repeat(25) + '{U+00A0}' + 'y'.repeat(10);
  const partes = puro(K.dividir(texto, 10));
  assert.equal(partes.length, 5);
  let junto = '';
  partes.forEach((p, i) => {
    const [cab, corpo] = [p.slice(0, p.indexOf('\n')), p.slice(p.indexOf('\n') + 1)];
    const m = cab.match(/^#ms-parte (\d+)\/(\d+) tamanho=(\d+) hash=(\d+) total=(\d+) total_hash=(\d+)$/);
    assert.ok(m, cab);
    assert.equal(Number(m[1]), i + 1);
    assert.equal(Number(m[3]), corpo.length);
    assert.equal(Number(m[4]), djb2(corpo));
    assert.equal(Number(m[6]), djb2(texto));
    junto += corpo;
  });
  assert.equal(junto, texto);
});

test('a assinatura sobrevive ao javascript_tool, que troca o \\u pelo caractere', () => {
  const decodificado = FONTE.replace(/\\u([0-9a-fA-F]{4})/g, (_, h) => String.fromCharCode(parseInt(h, 16)));
  assert.notEqual(decodificado, FONTE);
  assert.equal(carregar(decodificado).__ms.assinatura(), carregar().__ms.assinatura());
  // o escape do arquivo vai em minusculas, como o K.fonte_ascii escreve; e o arquivo e ASCII
  assert.equal(FONTE.match(/\\u[0-9a-f]*[A-F][0-9a-fA-F]*/g), null);
  assert.match(FONTE, /^[\x00-\x7e]*$/);
});

test('a assinatura nao depende dos comentarios: o agente pode cola-los ou nao', () => {
  const sem = FONTE.split('\n').filter(l => !/^\s*\/\//.test(l)).join('\n');
  assert.notEqual(sem, FONTE);
  assert.equal(carregar(sem).__ms.assinatura(), carregar().__ms.assinatura());
});

test('a assinatura muda quando uma funcao muda', () => {
  const a = carregar().__ms.assinatura(), b = carregar().__ms.assinatura();
  assert.equal(a, b);
  const outra = carregar(FONTE.replace("K.versao = () => '2026-10-27';", "K.versao = () => '2026-10-28';")).__ms.assinatura();
  assert.notEqual(a, outra);
  assert.equal(String(a), execFileSync('node', [ARQ.pathname, '--assinatura'], {encoding: 'utf8'}).trim());
});

// --------------------------------------------------------------------- o motor
test('o cubo pagina sem passar de 10.000 celulas', async () => {
  const muitas = Array.from({length: 1577}, (_, i) => ['FILA ' + i, String(200000000 + i)]);
  const f = motorFalso({linhas: () => muitas}), K = comMotor(f).__ms;
  const r = await K.cubo(f.m, ['a', 'b'], Array.from({length: 11}, (_, i) => 'Sum(' + i + ')'));
  assert.equal(r.length, 1577);
  assert.ok(Math.max(...f.paginas) <= 10000);
  assert.equal(r[1576][0], 'FILA 1576');
});

test('a medicao inteira: forma da saida, nomes exatos e lacunas', async () => {
  const f = motorFalso(), ctx = comMotor(f), K = ctx.__ms;
  K.rodar(ORDEM);
  const e = await esperar(ctx);
  assert.equal(e.erro, null);
  const out = JSON.parse(desfazer(ctx.__out));
  assert.equal(out.kit.assinatura, K.assinatura());
  assert.equal(out.ordem_hash, K.djb2(K.ascii(JSON.stringify(ORDEM))));
  assert.equal(out.datas.inicio.solicitacao_max, 46321);
  assert.deepEqual(Object.keys(out.objetos), ORDEM.objetos.map(o => o.id));
  const ic = out.objetos['09.02.01.006-9'];
  for (const k of ['teto.pessoas', 'teto.pessoas_viva', 'finalidade.pessoas', 'finalidade.pessoas_viva',
    'nucleo_entrada.pessoas', 'nucleo_obrigatorios.pessoas', 'nucleo_obrigatorios.pessoas_viva']) {
    assert.equal(typeof ic.valores[k], 'number', k);
  }
  assert.deepEqual(Object.keys(ic.dimensoes).sort(), ['ano', 'cid', 'entrantes', 'idade', 'regiao']);
  assert.ok('sem_regiao' in ic.dimensoes.regiao);
  assert.deepEqual(ic.nomes['ANGIOTOMOGRAFIA  DE CORONARIAS'], undefined);
  assert.deepEqual(out.objetos['02.06.01.007-9'].nomes['ANGIOTOMOGRAFIA  DE CORONARIAS'], ['ANGIOTOMOGRAFIA' + NBSP + ' DE CORONARIAS']);
  // a varredura acha, pelo codigo, pelo nome e pelo CID; a fila so de agendamento tambem
  const v = out.varredura, i = n => v.cols.indexOf(n);
  assert.ok(v.linhas.some(l => l[i('tabela')] === 'ag' && l[i('nome')] === 'MAMOGRAFIA DE RASTREAMENTO'));
  assert.ok(v.linhas.some(l => l[i('nome')] === 'ELETROCARDIOGRAMA' && l[i('por')].includes('cid_aceito')));
  // as expressoes: o sexo exclui o oposto; a idade da ficha; o nucleo pelos obrigatorios ao mesmo tempo
  assert.ok(f.pedidos.some(x => x.includes("E({1<sexo_usuario={'MASCULINO'}>} cns_usuario_solicitacao)")));
  assert.ok(f.pedidos.some(x => x.includes('idade_solicitacao={">=18<=130"}')));
  assert.ok(f.pedidos.some(x => x.startsWith('Sum({1} Aggr({1} If(') && x.includes('HOLTER 24 HORAS')));
  assert.ok(f.pedidos.some(x => x.includes('CID_agendamento={"I50*"}')));
  // nenhum CNS sai: o campo nunca e dimensao nem vai para uma funcao que devolve texto
  assert.ok(!f.dims.some(d => /cns|no_usuario|telefone/.test(d)));
  assert.ok(!f.pedidos.some(x => /(Concat|Only|MaxString|MinString|FirstSortedValue)\s*\(/.test(x)));
});

test('panorama: toda fila do universo, com as agendadas pelo par', async () => {
  const f = motorFalso(), ctx = comMotor(f), K = ctx.__ms;
  K.rodar({contrato: '2026-10-27', tipo: 'panorama', plano: 'planos/redacao_99', saida: 'transcricao', janela_viva_meses: 24,
    universo: [{rotulo: 'imagem', codigos: ['02.04*', '02.05*', '02.06*']}, {rotulo: 'cardiologia', termos: ['CARDI']}],
    dimensoes: ['regiao']});
  const e = await esperar(ctx);
  assert.equal(e.erro, null);
  const out = JSON.parse(desfazer(ctx.__out)), img = out.panorama.imagem.filas;
  assert.deepEqual(img.linhas.map(l => l[0]).sort(), ['ANGIOTOMOGRAFIA' + NBSP + ' DE CORONARIAS', 'ECOGRAFIA DE MAMAS - BILATERAL',
    'MAMOGRAFIA BILATERAL PARA RASTREAMENTO']);
  assert.deepEqual(out.panorama.cardiologia.filas.linhas.map(l => l[0]), ['CONSULTA EM CARDIOLOGIA - INSUFICIENCIA CARDIACA']);
  assert.ok(out.panorama.imagem.dimensoes.regiao);
  assert.ok(img.cols.includes('agendadas_12m') && img.cols.includes('cid_principais'));
});

test('a oferta pelo mes do agendamento, com realizados e faltas, e a situacao em 12 meses', async () => {
  const f = motorFalso(), ctx = comMotor(f), K = ctx.__ms;
  const ordem = puro(ORDEM);
  ordem.dimensoes = ['oferta', 'situacao'];
  K.rodar(ordem);
  const e = await esperar(ctx);
  assert.equal(e.erro, null);
  const out = JSON.parse(desfazer(ctx.__out)), mam = out.objetos['02.04.03.018-8'].dimensoes;
  assert.deepEqual(mam.oferta.cols, ['mes', 'agendamentos', 'realizados', 'faltas']);
  assert.deepEqual(mam.oferta.linhas.map(l => l[0]), ['2024-09', '2024-10', '2025-06', '2026-10']);
  assert.deepEqual(mam.situacao.cols, ['situacao', 'agendamentos']);
  assert.ok(mam.situacao.linhas.some(l => l[0] === 'PROCEDIMENTO REALIZADO'));
  // pelo mes do agendamento (nao do pedido), na janela de 24 meses, e a falta pelo nome exato
  assert.ok(f.dims.includes("=Date(MonthStart(data_agendamento),'YYYY-MM')"));
  assert.ok(f.pedidos.some(x => x.includes('data_agendamento={">=01/10/2024"}')
    && x.includes("status_solicitacao_agendamento_alias={'PROCEDIMENTO NÃO REALIZADO POR FALTA DO PACIENTE'}")));
  assert.ok(f.pedidos.some(x => x.includes('data_agendamento={">=26/10/2025<=25/10/2026"}') && x.startsWith('Count(Distinct {1<descri')));
});

test('a oferta sem fila na tabela de agendamentos vira lacuna, e nao a base inteira', async () => {
  const f = motorFalso({sem_ag: ['HOLTER 24 HORAS']}), ctx = comMotor(f), K = ctx.__ms;
  K.rodar({contrato: '2026-10-27', tipo: 'medicao', plano: 'planos/redacao_99', saida: 'transcricao', janela_viva_meses: 24,
    dimensoes: ['oferta'], objetos: [{id: '02.11.02.004-4', tipo: 'exame', nome: 'holter', codigos: ['02.11.02.004-4'],
      filas: [{nome: 'HOLTER 24 HORAS'}]}]});
  const e = await esperar(ctx);
  assert.equal(e.erro, null);
  const out = JSON.parse(desfazer(ctx.__out));
  assert.equal(out.objetos['02.11.02.004-4'].dimensoes.oferta, undefined);
  assert.ok(out.lacunas.some(l => l.onde === '02.11.02.004-4 oferta' && /base inteira/.test(l.motivo)));
});

test('panorama por codigo: entrantes, oferta e situacao de cada codigo das filas do universo', async () => {
  const f = motorFalso(), ctx = comMotor(f), K = ctx.__ms;
  K.rodar({contrato: '2026-10-27', tipo: 'panorama', plano: 'planos/redacao_99', saida: 'transcricao', janela_viva_meses: 24,
    universo: [{rotulo: 'imagem', codigos: ['02.04*', '02.05*', '02.06*']}], por_codigo: ['entrantes', 'oferta', 'situacao']});
  const e = await esperar(ctx);
  assert.equal(e.erro, null);
  const pc = JSON.parse(desfazer(ctx.__out)).por_codigo;
  assert.deepEqual(pc.entrantes.cols, ['codigo', 'mes', 'abertas', 'agendadas']);
  assert.deepEqual(pc.oferta.cols, ['codigo', 'mes', 'agendamentos', 'realizados', 'faltas']);
  assert.deepEqual(pc.situacao.cols, ['codigo', 'situacao', 'agendamentos']);
  // os entrantes so da janela de 24 meses; tudo ordenado por codigo e mes
  assert.ok(pc.entrantes.linhas.every(l => l[1] >= '2024-10'));
  assert.deepEqual(pc.oferta.linhas.map(l => l[0] + '|' + l[1]), [...pc.oferta.linhas.map(l => l[0] + '|' + l[1])].sort());
  // os codigos sao os das filas do universo, por busca exata
  assert.ok(f.pedidos.some(x => x.includes('codigo_sigtap_agendamento={"204030188","205020097","206010079"}')));
});

test('recarga no meio: para, sem saida', async () => {
  const f = motorFalso({recargas: ['2026-10-26T17:36:46.000Z', '2026-10-26T17:36:46.000Z', '2026-10-26T19:32:44.246Z']});
  const ctx = comMotor(f);
  ctx.__ms.rodar(ORDEM);
  const e = await esperar(ctx);
  assert.match(e.erro, /recarga no meio/);
  assert.equal(ctx.__out, null);
});

test('campo que nao existe: para e lista os campos, em vez de medir errado', async () => {
  const f = motorFalso(), ctx = comMotor(f);
  const ordem = puro(ORDEM);
  ordem.objetos[0].cid_finalidade = 'cid_que_nao_existe={"I50*"}';
  ctx.__ms.rodar(ordem);
  const e = await esperar(ctx);
  assert.match(e.erro, /campo que nao responde: cid_que_nao_existe/);
  assert.match(e.erro, /campos do app: /);
});

test('as partes da saida e o botao', async () => {
  const f = motorFalso(), elementos = [];
  const documento = {
    getElementById: id => elementos.find(x => x.id === id) || null,
    createElement: () => ({style: {}, setAttribute() {}, select() {}, remove() {}}),
    body: {appendChild: x => elementos.push(x)},
    execCommand: () => true
  };
  const ctx = carregar(FONTE, {__app: {model: {enigmaModel: f.m}}, document: documento});
  ctx.__ms.rodar(ORDEM);
  await esperar(ctx);
  const cab = puro(ctx.__ms.preparar(5000));
  assert.ok(cab.length > 1);
  assert.equal(cab.map((_, i) => ctx.__ms.parte(i + 1).split('\n').slice(1).join('\n')).join(''), ctx.__out);
  assert.equal(ctx.__ms.botao(2), 'copiar parte 2/' + cab.length);
  elementos[0].onclick();
  assert.equal(elementos[0].textContent, 'copiada a parte 2/' + cab.length);
});
