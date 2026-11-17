// motor.js - o kit do motor do Mapa Social da Saude (metodo/coleta/mapa_social.md, "O kit do motor").
//
// Cola-se inteiro no javascript_tool do navegador embutido, na pagina do painel, e fica em
// window.__ms. Monta as expressoes de conjunto, pergunta ao motor (Qlik Engine API) e deixa a
// saida em window.__out, em partes com tamanho e hash djb2. Nao decide nada: so mede o que a
// ordem de coleta pede. So contagens agregadas: nenhum CNS, CPF, nome ou data de nascimento.
//
// No painel:
//   __ms.abrir()                  abre o app (a chamada seguinte ja pode medir)
//   __ms.assinatura()             tem de ser igual a `node ferramentas/mapa_social/motor.js --assinatura`
//   __ms.rodar(<ordem>)           mede em segundo plano; acompanhar com __ms.estado()
//   __ms.preparar(tamanho)        divide a saida em partes; __ms.parte(i) ou __ms.botao(i)
//
// No node (testes e conferencia):
//   node motor.js --assinatura
//   node motor.js --hash-ordem <ordem.json>
//   node motor.js --partes <saida.json> <pasta> [tamanho]
//
// O arquivo e ASCII: os acentos dos nomes de campo e dos status vao como \u.

(function (raiz) {
  'use strict';
  const K = {};

  K.versao = () => '2026-10-27';
  K.app = () => '7edb02fa-f1f5-4ea6-b348-049a4ac2d095';

  // os campos que o kit usa; cada um se confere contra a lista do app antes de medir, porque
  // o motor ignora em silencio o campo que nao existe (sondagem de 26/10/2026)
  K.campos = () => ({
    nome_sol: 'descri\u00e7\u00e3o_procedimento_solicitacao', cod_sol: 'codigo_sigtap_solicitacao',
    nome_ag: 'descri\u00e7\u00e3o_procedimento_agendamento', cod_ag: 'codigo_sigtap_agendamento',
    status: 'status_solicitacao_alias', contador: 'contador_solicitacao', cns: 'cns_usuario_solicitacao',
    espera: 'tempo_espera_solicitacao', data: 'data_solicitacao', idade: 'idade_solicitacao',
    ano: 'Ano_Solicitacao', regiao: 'regiao_saude_solicitante', cid: 'codigo_cid_solicitado',
    sexo: 'sexo_usuario', contador_ag: 'contador_agendamento', data_ag: 'data_agendamento',
    espera_ag: 'tempo_espera_agendamento', ano_ag: 'Ano_Agendamento', cid_ag: 'CID_agendamento',
    situacao_ag: 'status_solicitacao_agendamento_alias'
  });
  K.st_fila = () => ['SOLICITA\u00c7\u00c3O PENDENTE DE REGULA\u00c7\u00c3O',
    'SOLICITA\u00c7\u00c3O CORRIGIDA E REENVIADA PARA REGULA\u00c7\u00c3O',
    'SOLICITA\u00c7\u00c3O PENDENTE DE REGULA\u00c7\u00c3O POR FILA DE ESPERA'];
  K.st_devolvidas = () => 'SOLICITA\u00c7\u00c3O DEVOLVIDA PARA COMPLEMENTA\u00c7\u00c3O PELO SOLICITANTE';
  // a situacao do agendamento: o realizado e a falta, como o motor escreve (coleta do IEV, 26/10/2026)
  K.st_realizado = () => 'PROCEDIMENTO REALIZADO';
  K.st_falta = () => 'PROCEDIMENTO N\u00c3O REALIZADO POR FALTA DO PACIENTE';

  // ---------------------------------------------------------------- texto e hash
  K.djb2 = function (s) {
    let h = 5381;
    for (let i = 0; i < s.length; i++) h = ((h << 5) + h + s.charCodeAt(i)) >>> 0;
    return h;
  };
  // tudo fora do ASCII visivel (e a chave) vira {U+XXXX}: o espaco nao separavel nao se perde
  // na transcricao, e o ler_motor.py restaura
  K.ascii = function (s) {
    return s.replace(/[^\x20-\x7e]|[{]/g, c => '{U+' + c.charCodeAt(0).toString(16).toUpperCase().padStart(4, '0') + '}');
  };
  K.norm = function (s) {
    return String(s == null ? '' : s).normalize('NFD').replace(/[\u0300-\u036f]/g, '')
      .replace(/\u00a0/g, ' ').replace(/\s+/g, ' ').trim().toUpperCase();
  };
  // a fonte de cada funcao em ASCII: o javascript_tool troca o \u do texto pelo caractere antes
  // de rodar, e a assinatura tem de sair igual no navegador e no node (prova de 26/10/2026)
  K.fonte_ascii = s => s.replace(/[^\x00-\x7f]/g, c => '\\u' + c.charCodeAt(0).toString(16).padStart(4, '0'));
  K.assinatura = function () {
    return K.djb2(Object.keys(K).sort().map(k => k + '=' + K.fonte_ascii(String(K[k]))).join('\n'));
  };
  K.dividir = function (texto, tamanho) {
    const n = Math.max(1, Math.ceil(texto.length / tamanho)), total = K.djb2(texto), partes = [];
    for (let i = 0; i < n; i++) {
      const pedaco = texto.slice(i * tamanho, (i + 1) * tamanho);
      partes.push('#ms-parte ' + (i + 1) + '/' + n + ' tamanho=' + pedaco.length + ' hash=' + K.djb2(pedaco) +
        ' total=' + texto.length + ' total_hash=' + total + '\n' + pedaco);
    }
    return partes;
  };

  // ------------------------------------------------------- expressoes de conjunto
  K.lit = v => "'" + String(v).replace(/'/g, "''") + "'";
  K.em = (campo, valores) => campo + '={' + valores.map(K.lit).join(',') + '}';
  K.busca = (campo, padroes) => campo + '={' + padroes.map(p => '"' + p + '"').join(',') + '}';
  K.conj = mods => {
    const m = mods.filter(Boolean);
    return m.length ? '{1<' + m.join(', ') + '>}' : '{1}';
  };
  // '02.04.03.018-8' -> '204030188'; '02.05*' -> '205*': o motor guarda o codigo sem o zero da frente
  K.codigo = function (c) {
    const s = String(c).trim(), curinga = s.endsWith('*');
    let d = s.replace(/\D/g, '');
    if (d.length === 10 || (curinga && d.startsWith('0'))) d = d.replace(/^0/, '');
    return d + (curinga ? '*' : '');
  };
  K.casa_codigo = (cod, padrao) => padrao.endsWith('*') ? String(cod).startsWith(padrao.slice(0, -1)) : String(cod) === padrao;
  // o CID da ficha na tabela de agendamentos: o campo vem com o nome ("H91 - ..."), entao todo
  // valor ganha o curinga
  K.cid_ag = function (expr) {
    if (!expr) return '';
    return expr.replace(/codigo_cid_solicitado\s*=/g, K.campos().cid_ag + '=').replace(/"([A-Za-z0-9.]+?)\*?"/g, '"$1*"');
  };
  K.campos_da_expressao = expr => (String(expr || '').match(/[A-Za-z_\u00c0-\u00ff][\w\u00c0-\u00ff.]*(?=\s*[-+*/]?=\s*[{E])/g) || []);
  K.mod_fila = () => K.em(K.campos().status, K.st_fila());
  K.mod_dev = () => K.em(K.campos().status, [K.st_devolvidas()]);
  K.mod_nomes = nomes => K.em(K.campos().nome_sol, nomes);
  K.mod_nomes_ag = nomes => K.em(K.campos().nome_ag, nomes);
  K.mod_idade = function (i) {
    if (!i || (i.min == null && i.max == null)) return '';
    return K.campos().idade + '={">=' + (i.min == null ? 0 : i.min) + '<=' + (i.max == null ? 130 : i.max) + '"}';
  };
  // o sexo da ficha exclui o sexo oposto, e nao seleciona o da ficha: cerca de 11% da fila nao
  // tem sexo ligado, e a selecao os perderia (sondagem de 26/10/2026)
  K.mod_sexo = function (s) {
    const oposto = {feminino: 'MASCULINO', masculino: 'FEMININO'}[String(s || 'ambos').toLowerCase()];
    if (!oposto) return '';
    const c = K.campos();
    return c.cns + '=E({1<' + c.sexo + "={'" + oposto + "'}>} " + c.cns + ')';
  };

  // ----------------------------------------------------------------------- datas
  K.dia = serial => new Date(Date.UTC(1899, 11, 30) + Math.round(serial) * 86400000);
  K.data_br = function (serial) {
    const d = K.dia(serial);
    return String(d.getUTCDate()).padStart(2, '0') + '/' + String(d.getUTCMonth() + 1).padStart(2, '0') + '/' + d.getUTCFullYear();
  };
  K.mes = serial => { const d = K.dia(serial); return d.getUTCFullYear() + '-' + String(d.getUTCMonth() + 1).padStart(2, '0'); };
  K.menos_meses = function (serial, meses) {
    const d = K.dia(serial), y = d.getUTCFullYear(), m = d.getUTCMonth() - meses;
    const ultimo = new Date(Date.UTC(y, m + 1, 0)).getUTCDate();
    return Math.round((Date.UTC(y, m, Math.min(d.getUTCDate(), ultimo)) - Date.UTC(1899, 11, 30)) / 86400000);
  };
  // a fila viva conta da solicitacao mais recente da base; as agendadas em 12 meses vao ate a
  // vespera dela; os entrantes e a oferta, 24 meses de calendario (a oferta inclui o ja marcado
  // para depois de hoje)
  K.janelas = function (max_sol, meses_viva) {
    const c = K.campos(), viva = K.menos_meses(max_sol, meses_viva), ag = K.menos_meses(max_sol, 12);
    const ent = K.menos_meses(max_sol, 24), ent_ini = ent - K.dia(ent).getUTCDate() + 1;
    return {
      meses_viva: meses_viva,
      viva: c.data + '={">=' + K.data_br(viva) + '"}',
      agendadas_12m: c.data_ag + '={">=' + K.data_br(ag) + '<=' + K.data_br(max_sol - 1) + '"}',
      entrantes_sol: c.data + '={">=' + K.data_br(ent_ini) + '"}',
      entrantes_ag: c.ano_ag + '={">=' + K.dia(ent_ini).getUTCFullYear() + '"}',
      entrantes_desde: K.mes(ent_ini),
      oferta: c.data_ag + '={">=' + K.data_br(ent_ini) + '"}'
    };
  };

  // ---------------------------------------------------------------------- medidas
  K.medidas_fila = function (mods, viva) {
    const c = K.campos(), S = [K.mod_fila()].concat(mods), V = S.concat([viva]);
    return [
      ['fila', 'Count(Distinct ' + K.conj(S) + ' ' + c.contador + ')'],
      ['fila_viva', 'Count(Distinct ' + K.conj(V) + ' ' + c.contador + ')'],
      ['pessoas', 'Count(Distinct ' + K.conj(S) + ' ' + c.cns + ')'],
      ['pessoas_viva', 'Count(Distinct ' + K.conj(V) + ' ' + c.cns + ')'],
      ['devolvidas', 'Count(Distinct ' + K.conj([K.mod_dev()].concat(mods)) + ' ' + c.contador + ')'],
      ['espera_media', 'Avg(' + K.conj(S) + ' ' + c.espera + ')'],
      ['espera_mediana', 'Median(' + K.conj(S) + ' ' + c.espera + ')'],
      ['espera_max', 'Max(' + K.conj(S) + ' ' + c.espera + ')'],
      ['mais_antiga', 'Min(' + K.conj(S) + ' ' + c.data + ')'],
      ['idade_mediana', 'Median(' + K.conj(S) + ' ' + c.idade + ')'],
      ['total', 'Count(Distinct ' + K.conj(mods) + ' ' + c.contador + ')']
    ];
  };
  // a oferta pelo mes em que o agendamento acontece (nao pelo mes do pedido): o total, os realizados
  // e as faltas, no conjunto da tabela de agendamentos
  K.mes_ag = () => "=Date(MonthStart(" + K.campos().data_ag + "),'YYYY-MM')";
  K.medidas_oferta = function (mods) {
    const c = K.campos(), cont = extra => 'Count(Distinct ' + K.conj(mods.concat(extra)) + ' ' + c.contador_ag + ')';
    return [cont([]), cont([K.em(c.situacao_ag, [K.st_realizado()])]), cont([K.em(c.situacao_ag, [K.st_falta()])])];
  };
  // pessoas que esperam em todas as filas ao mesmo tempo, sem expor o CNS
  K.todas_ao_mesmo_tempo = function (grupos, mods) {
    const c = K.campos(), cond = grupos.map(g => 'Count(' + K.conj([K.mod_fila(), K.mod_nomes(g)].concat(mods)) + ' ' + c.contador + ')>0');
    return 'Sum({1} Aggr({1} If(' + cond.join(' and ') + ', 1, 0), ' + c.cns + '))';
  };

  // ------------------------------------------------------------------------ motor
  K.abrir = function () {
    raiz.require(['js/qlik'], qlik => {
      raiz.__app = qlik.openApp(K.app(), {host: raiz.location.hostname, prefix: '/', port: 443, isSecure: true});
    });
    return 'abrindo: na chamada seguinte o motor responde';
  };
  K.modelo = async function () {
    for (let i = 0; i < 40; i++) {
      const m = raiz.__app && raiz.__app.model && raiz.__app.model.enigmaModel;
      if (m) return m;
      await new Promise(r => setTimeout(r, 500));
    }
    throw new Error('o app nao abriu: chame __ms.abrir() e espere');
  };
  K.cubo = async function (m, dims, medidas, sem_zero) {
    const larg = dims.length + medidas.length, alt = Math.max(1, Math.floor(10000 / larg));
    const o = await m.createSessionObject({qInfo: {qType: 'cube'}, qHyperCubeDef: {
      qDimensions: dims.map(d => ({qDef: {qFieldDefs: [d]}, qNullSuppression: true})),
      qMeasures: medidas.map(e => ({qDef: {qDef: e}})),
      qSuppressZero: sem_zero !== false,
      qInitialDataFetch: [{qTop: 0, qLeft: 0, qWidth: larg, qHeight: alt}]}});
    try {
      const hc = (await o.getLayout()).qHyperCube;
      if (hc.qError) throw new Error('o motor recusou o cubo: ' + JSON.stringify(hc.qError));
      let linhas = hc.qDataPages[0] ? hc.qDataPages[0].qMatrix : [];
      for (let topo = alt; topo < hc.qSize.qcy; topo += alt) {
        const p = await o.getHyperCubeData('/qHyperCubeDef', [{qTop: topo, qLeft: 0, qWidth: larg, qHeight: alt}]);
        linhas = linhas.concat(p[0].qMatrix);
      }
      return linhas.map(r => r.map((c, i) => i < dims.length ? c.qText :
        (typeof c.qNum === 'number' && isFinite(c.qNum) ? c.qNum : null)));
    } finally {
      await m.destroySessionObject(o.id);
    }
  };
  K.valores = async function (m, pares) {
    const r = await K.cubo(m, [], pares.map(p => p[1]), false), out = {};
    pares.forEach((p, i) => { out[p[0]] = r[0] ? r[0][i] : null; });
    return out;
  };
  K.lista_campos = async function (m) {
    const o = await m.createSessionObject({qInfo: {qType: 'FieldList'}, qFieldListDef: {qShowSrcTables: true}});
    try {
      return (await o.getLayout()).qFieldList.qItems.map(f => f.qName);
    } finally {
      await m.destroySessionObject(o.id);
    }
  };
  K.conferir_campos = async function (m, ordem) {
    const existem = new Set(await K.lista_campos(m)), usados = new Set(Object.values(K.campos()));
    (ordem.objetos || []).forEach(o => {
      [o.cid_aceito, o.cid_finalidade].concat((o.recortes || []).map(r => r.cid)).forEach(e => K.campos_da_expressao(e).forEach(f => usados.add(f)));
    });
    const faltam = [...usados].filter(f => !existem.has(f));
    if (faltam.length) throw new Error('campo que nao responde: ' + faltam.join(', ') + ' | campos do app: ' + [...existem].join(', '));
  };
  K.datas = async function (m) {
    const lay = await m.getAppLayout(), c = K.campos();
    const v = await K.valores(m, [['consulta', 'Now()'], ['solicitacao_max', 'Max({1} ' + c.data + ')'],
      ['agendamento_max', 'Max({1} ' + c.data_ag + ')']]);
    return {recarga_utc: lay.qLastReloadTime, consulta: v.consulta, solicitacao_max: v.solicitacao_max, agendamento_max: v.agendamento_max};
  };
  K.nomes = async function (m) {
    const c = K.campos();
    const sol = await K.cubo(m, [c.nome_sol, c.cod_sol], ['Count(Distinct {1} ' + c.contador + ')',
      'Count(Distinct ' + K.conj([K.mod_fila()]) + ' ' + c.contador + ')']);
    const ag = await K.cubo(m, [c.nome_ag, c.cod_ag], ['Count(Distinct {1} ' + c.contador_ag + ')']);
    return {sol: sol, ag: ag};
  };
  K.agendadas = async function (m, ctx) {
    const c = K.campos();
    return K.cubo(m, [c.nome_ag, c.cod_ag], ['Count(Distinct ' + K.conj([ctx.janelas.agendadas_12m]) + ' ' + c.contador_ag + ')']);
  };
  K.tem_termo = function (nome, termo) {
    const palavras = K.norm(nome).split(/[^A-Z0-9]+/);
    return K.norm(termo).split(' ').every(w => palavras.some(p => p.startsWith(w)));
  };
  K.parecido = function (nome, pedido) {
    const a = K.norm(nome), b = K.norm(pedido);
    return a === b || (b.length >= 8 && a.includes(b)) || (a.length >= 8 && b.includes(a));
  };
  // o nome pedido -> os nomes exatos do motor: todos os que so diferem na grafia (espaco duplo,
  // espaco nao separavel, acento), o exato primeiro. Na tabela de agendamentos a mesma fila pode
  // vir com as duas grafias (prova de 26/10/2026: a videoendoscopia nasal flexivel)
  K.resolver = function (pedido, nomes) {
    const alvo = K.norm(pedido), achados = [...new Set(nomes.filter(n => K.norm(n) === alvo))].sort();
    return achados.includes(pedido) ? [pedido].concat(achados.filter(n => n !== pedido)) : achados;
  };
  // as agendadas em 12 meses do par nome x codigo: 0 quando o par existe na tabela de agendamentos
  // sem agendamento na janela; nulo quando o par nao existe la (a fila pode ter outro nome)
  K.oferta = function (ctx) {
    const ag = new Map(ctx.agendadas.map(r => [r[0] + '|' + r[1], r[2]])), existe = new Set(ctx.nomes.ag.map(r => r[0] + '|' + r[1]));
    return (nome, cod) => ag.has(nome + '|' + cod) ? ag.get(nome + '|' + cod) : (existe.has(nome + '|' + cod) ? 0 : null);
  };
  K.lacuna = (ctx, onde, e) => { ctx.lacunas.push({onde: onde, motivo: String(e && e.message || e)}); };
  K.tabela = (cols, linhas) => ({cols: cols, linhas: linhas});

  // a varredura: toda fila que o objeto atende, pelo codigo, pelo nome e, na OCI, pelo CID; depois,
  // o estudo de cada fila achada na tabela de solicitacoes
  K.varrer = async function (m, ordem, ctx) {
    const c = K.campos(), achados = new Map();
    const marca = (tab, nome, cod, por, id) => {
      const k = tab + '|' + nome + '|' + cod;
      if (!achados.has(k)) achados.set(k, {tabela: tab, nome: nome, codigo: cod, por: new Set(), objetos: new Set()});
      achados.get(k).por.add(por); achados.get(k).objetos.add(id);
    };
    for (const o of ordem.objetos) {
      const cods = (o.codigos || []).map(K.codigo), filas = (o.filas || []).map(f => f.nome), termos = o.termos || [];
      [['sol', ctx.nomes.sol], ['ag', ctx.nomes.ag]].forEach(([tab, linhas]) => linhas.forEach(r => {
        if (cods.some(p => K.casa_codigo(r[1], p))) marca(tab, r[0], r[1], 'codigo', o.id);
        if (filas.some(p => K.parecido(r[0], p))) marca(tab, r[0], r[1], 'nome', o.id);
        if (termos.some(t => K.tem_termo(r[0], t))) marca(tab, r[0], r[1], 'termo', o.id);
      }));
      if (o.tipo !== 'oci') continue;
      for (const [rot, expr] of [['cid_aceito', o.cid_aceito], ['cid_finalidade', o.cid_finalidade]]) {
        try {
          (await K.cubo(m, [c.nome_sol, c.cod_sol], ['Count(Distinct ' + K.conj([K.mod_fila(), expr]) + ' ' + c.contador + ')']))
            .forEach(r => marca('sol', r[0], r[1], rot, o.id));
          (await K.cubo(m, [c.nome_ag, c.cod_ag], ['Count(Distinct ' + K.conj([ctx.janelas.agendadas_12m, K.cid_ag(expr)]) + ' ' + c.contador_ag + ')']))
            .forEach(r => marca('ag', r[0], r[1], rot, o.id));
        } catch (e) { K.lacuna(ctx, 'varredura ' + o.id + ' ' + rot, e); }
      }
    }
    const sol = [...achados.values()].filter(a => a.tabela === 'sol'), nomes = [...new Set(sol.map(a => a.nome))];
    const ocis = ordem.objetos.filter(o => o.tipo === 'oci');
    const est = new Map(), cids = new Map();
    let cols = [];
    if (nomes.length) {
      const med = K.medidas_fila([K.mod_nomes(nomes)], ctx.janelas.viva);
      ocis.forEach(o => {
        med.push(['fila_cid_aceito ' + o.id, 'Count(Distinct ' + K.conj([K.mod_fila(), K.mod_nomes(nomes), o.cid_aceito]) + ' ' + c.contador + ')']);
        med.push(['fila_cid_finalidade ' + o.id, 'Count(Distinct ' + K.conj([K.mod_fila(), K.mod_nomes(nomes), o.cid_finalidade]) + ' ' + c.contador + ')']);
      });
      cols = med.map(x => x[0]);
      try {
        (await K.cubo(m, [c.nome_sol, c.cod_sol], med.map(x => x[1]))).forEach(r => est.set(r[0] + '|' + r[1], r.slice(2)));
        (await K.cubo(m, [c.nome_sol, '=Left(' + c.cid + ',3)'], ['Count(Distinct ' + K.conj([K.mod_fila(), K.mod_nomes(nomes)]) + ' ' + c.contador + ')']))
          .forEach(r => { if (!cids.has(r[0])) cids.set(r[0], []); cids.get(r[0]).push([r[1], r[2]]); });
      } catch (e) { K.lacuna(ctx, 'estudo das filas achadas', e); }
    }
    const ag = K.oferta(ctx);
    const linhas = [...achados.values()].map(a => [a.tabela, a.nome, a.codigo, [...a.por].sort(), [...a.objetos].sort()]
      .concat(a.tabela === 'sol' ? (est.get(a.nome + '|' + a.codigo) || cols.map(() => null)) : cols.map(() => null))
      .concat([ag(a.nome, a.codigo),
        a.tabela === 'sol' ? (cids.get(a.nome) || []).sort((x, y) => y[1] - x[1]).slice(0, 5) : []]));
    return K.tabela(['tabela', 'nome', 'codigo', 'por', 'objetos'].concat(cols, ['agendadas_12m', 'cid_principais']), linhas);
  };

  // as dimensoes pedidas, sobre um conjunto (S na tabela de solicitacoes, Sag na de agendamentos)
  K.dimensoes = async function (m, dims, S, Sag, ctx, onde) {
    const c = K.campos(), out = {}, cont = mods => 'Count(Distinct ' + K.conj(mods) + ' ' + c.contador + ')',
      pes = mods => 'Count(Distinct ' + K.conj(mods) + ' ' + c.cns + ')';
    for (const d of dims || []) {
      try {
        if (d === 'regiao') {
          const linhas = await K.cubo(m, [c.regiao], [cont(S), pes(S)]);
          const sem = 'Count(Distinct {1<' + S.filter(Boolean).join(', ') + '> - 1<' + c.regiao + '={"*"}>} ';
          const v = await K.valores(m, [['fila', sem + c.contador + ')'], ['pessoas', sem + c.cns + ')']]);
          out.regiao = Object.assign(K.tabela(['regiao', 'fila', 'pessoas'], linhas), {sem_regiao: v});
        } else if (d === 'idade') {
          out.idade = K.tabela(['faixa', 'fila', 'pessoas'], await K.cubo(m, ['=Floor(' + c.idade + '/10)*10'], [cont(S), pes(S)]));
        } else if (d === 'cid') {
          const l = await K.cubo(m, ['=Left(' + c.cid + ',3)'], [cont(S), pes(S)]);
          out.cid = K.tabela(['cid', 'fila', 'pessoas'], l.sort((a, b) => b[1] - a[1]).slice(0, 20));
        } else if (d === 'ano') {
          out.ano = K.tabela(['ano', 'fila', 'fila_viva'], await K.cubo(m, [c.ano], [cont(S), cont(S.concat([ctx.janelas.viva]))]));
        } else if (d === 'entrantes') {
          const sol = S.filter(x => x !== K.mod_fila()).concat([ctx.janelas.entrantes_sol]);
          const ab = await K.cubo(m, ["=Date(MonthStart(" + c.data + "),'YYYY-MM')"], [cont(sol)]);
          const ag = await K.cubo(m, ["=Date(MonthStart(" + c.data_ag + ' - ' + c.espera_ag + "),'YYYY-MM')"],
            ['Count(Distinct ' + K.conj(Sag.concat([ctx.janelas.entrantes_ag])) + ' ' + c.contador_ag + ')']);
          const meses = new Map();
          ab.forEach(r => { if (r[0] >= ctx.janelas.entrantes_desde) meses.set(r[0], [r[0], r[1], 0]); });
          ag.forEach(r => { if (r[0] >= ctx.janelas.entrantes_desde) { const x = meses.get(r[0]) || [r[0], 0, 0]; x[2] = r[1]; meses.set(r[0], x); } });
          out.entrantes = K.tabela(['mes', 'abertas', 'agendadas'], [...meses.values()].sort((a, b) => a[0] < b[0] ? -1 : 1));
        } else if (d === 'oferta' || d === 'situacao') {
          if (!Sag.filter(Boolean).length) throw new Error('sem fila na tabela de agendamentos: o conjunto seria a base inteira');
          if (d === 'oferta') {
            out.oferta = K.tabela(['mes', 'agendamentos', 'realizados', 'faltas'],
              (await K.cubo(m, [K.mes_ag()], K.medidas_oferta(Sag.concat([ctx.janelas.oferta])))).sort((a, b) => a[0] < b[0] ? -1 : 1));
          } else {
            out.situacao = K.tabela(['situacao', 'agendamentos'],
              await K.cubo(m, [c.situacao_ag], ['Count(Distinct ' + K.conj(Sag.concat([ctx.janelas.agendadas_12m])) + ' ' + c.contador_ag + ')']));
          }
        } else {
          throw new Error('dimensao que o kit nao conhece: ' + d);
        }
      } catch (e) { K.lacuna(ctx, onde + ' ' + d, e); }
    }
    return out;
  };

  // a medicao de um objeto: na OCI, teto, finalidade e nucleo, e a finalidade so nos exames e so
  // nas consultas quando a composicao tem os dois; no exame, a uniao das filas. A oferta de cada
  // fila sao as agendadas em 12 meses pelos nomes exatos da tabela de agendamentos; cada fila da
  // composicao sai sem recorte e no recorte de CID (o teto, a finalidade, os da ordem)
  K.medir = async function (m, o, ordem, ctx) {
    const c = K.campos(), out = {tipo: o.tipo, nomes: {}, nomes_ag: {}};
    const sol = ctx.nomes.sol.map(r => r[0]), ag = ctx.nomes.ag.map(r => r[0]);
    const exatos = f => out.nomes[f.nome] || [];
    (o.filas || []).forEach(f => {
      out.nomes[f.nome] = K.resolver(f.nome, sol);
      out.nomes_ag[f.nome] = K.resolver(f.nome, ag);
      if (!out.nomes[f.nome].length) K.lacuna(ctx, o.id + ' fila', 'o nome pedido nao existe na tabela de solicitacoes: ' + f.nome);
    });
    out.agendadas_12m = {};
    (o.filas || []).forEach(f => {
      const ns = out.nomes_ag[f.nome];
      out.agendadas_12m[f.nome] = ns.length ? ctx.agendadas.filter(r => ns.includes(r[0])).reduce((s, r) => s + r[2], 0) : null;
    });
    const nomes = [...new Set((o.filas || []).flatMap(exatos))], nomes_ag = [...new Set(Object.values(out.nomes_ag).flat())];
    if (!nomes.length) { K.lacuna(ctx, o.id, 'nenhuma fila de partida existe no motor'); return out; }
    const base = [K.mod_idade(o.idade), K.mod_sexo(o.sexo)], viva = ctx.janelas.viva;
    const V = (k, mods) => [[k + '.pessoas', 'Count(Distinct ' + K.conj(mods) + ' ' + c.cns + ')'],
      [k + '.pessoas_viva', 'Count(Distinct ' + K.conj(mods.concat([viva])) + ' ' + c.cns + ')']];
    const ficha = (k, mods) => V(k, mods).concat([
      [k + '.fila', 'Count(Distinct ' + K.conj(mods) + ' ' + c.contador + ')'],
      [k + '.fila_viva', 'Count(Distinct ' + K.conj(mods.concat([viva])) + ' ' + c.contador + ')'],
      [k + '.espera_media', 'Avg(' + K.conj(mods) + ' ' + c.espera + ')'],
      [k + '.espera_mediana', 'Median(' + K.conj(mods) + ' ' + c.espera + ')'],
      [k + '.devolvidas', 'Count(Distinct ' + K.conj([K.mod_dev(), K.mod_nomes(nomes)].concat(mods.slice(2))) + ' ' + c.contador + ')']]);
    const pares = [];
    let S, Sag;
    if (o.tipo === 'oci') {
      pares.push(...ficha('teto', [K.mod_fila(), K.mod_nomes(nomes), o.cid_aceito].concat(base)));
      pares.push(...ficha('finalidade', [K.mod_fila(), K.mod_nomes(nomes), o.cid_finalidade].concat(base)));
      pares.push(...V('finalidade_sem_idade_sexo', [K.mod_fila(), K.mod_nomes(nomes), o.cid_finalidade]));
      const papel = p => [...new Set((o.filas || []).filter(f => (f.papel || 'exame') === p).flatMap(exatos))];
      if (papel('exame').length && papel('consulta').length) {
        pares.push(...V('finalidade_exames', [K.mod_fila(), K.mod_nomes(papel('exame')), o.cid_finalidade].concat(base)));
        pares.push(...V('finalidade_consultas', [K.mod_fila(), K.mod_nomes(papel('consulta')), o.cid_finalidade].concat(base)));
      }
      const entrada = [...new Set((o.filas || []).filter(f => f.entrada).flatMap(exatos))];
      if (entrada.length) pares.push(...V('nucleo_entrada', [K.mod_fila(), K.mod_nomes(entrada), o.cid_finalidade].concat(base)));
      const obrig = (o.filas || []).filter(f => f.obrigatorio).map(exatos).filter(g => g.length);
      if (obrig.length >= 2) {
        pares.push(['nucleo_obrigatorios.pessoas', K.todas_ao_mesmo_tempo(obrig, [o.cid_finalidade].concat(base))]);
        pares.push(['nucleo_obrigatorios.pessoas_viva', K.todas_ao_mesmo_tempo(obrig, [o.cid_finalidade, viva].concat(base))]);
      } else if (obrig.length === 1) {
        pares.push(...V('nucleo_obrigatorios', [K.mod_fila(), K.mod_nomes(obrig[0]), o.cid_finalidade].concat(base)));
      }
      out.obrigatorios = (o.filas || []).filter(f => f.obrigatorio).map(f => f.nome);
      out.entrada = (o.filas || []).filter(f => f.entrada).map(f => f.nome);
      S = [K.mod_fila(), K.mod_nomes(nomes), o.cid_finalidade].concat(base);
      Sag = [nomes_ag.length ? K.mod_nomes_ag(nomes_ag) : '', K.cid_ag(o.cid_finalidade)];
    } else {
      pares.push(...ficha('uniao', [K.mod_fila(), K.mod_nomes(nomes)].concat(base)));
      S = [K.mod_fila(), K.mod_nomes(nomes)].concat(base);
      Sag = [nomes_ag.length ? K.mod_nomes_ag(nomes_ag) : ''];
    }
    try { out.valores = await K.valores(m, pares); } catch (e) { K.lacuna(ctx, o.id + ' numeros', e); }
    try {
      const recs = o.tipo === 'oci' ? [['teto', o.cid_aceito], ['finalidade', o.cid_finalidade]] : (o.recortes || []).map(r => [r.rotulo, r.cid]);
      const med = K.medidas_fila([K.mod_nomes(nomes)], viva);
      recs.forEach(([rot, cid]) => {
        med.push(['recorte ' + rot + ' fila', 'Count(Distinct ' + K.conj([K.mod_fila(), K.mod_nomes(nomes), cid]) + ' ' + c.contador + ')']);
        med.push(['recorte ' + rot + ' fila_viva', 'Count(Distinct ' + K.conj([K.mod_fila(), K.mod_nomes(nomes), cid, viva]) + ' ' + c.contador + ')']);
      });
      out.filas = K.tabela(['nome'].concat(med.map(x => x[0])), await K.cubo(m, [c.nome_sol], med.map(x => x[1]), false));
      out.filas.linhas = out.filas.linhas.filter(r => nomes.includes(r[0]));
      out.cid_principais = {};
      for (const [rot, cid] of recs.length ? recs : [['sem recorte', '']]) {
        const l = await K.cubo(m, [c.nome_sol, '=Left(' + c.cid + ',3)'], ['Count(Distinct ' + K.conj([K.mod_fila(), K.mod_nomes(nomes), cid]) + ' ' + c.contador + ')']);
        out.cid_principais[rot] = {};
        nomes.forEach(n => { out.cid_principais[rot][n] = l.filter(r => r[0] === n).map(r => [r[1], r[2]]).sort((a, b) => b[1] - a[1]).slice(0, 10); });
      }
    } catch (e) { K.lacuna(ctx, o.id + ' filas da composicao', e); }
    out.dimensoes = await K.dimensoes(m, o.dimensoes || ordem.dimensoes, S, Sag, ctx, o.id);
    return out;
  };

  // o panorama: toda fila (nome x codigo) do universo pedido, sem objeto, e o total distinto do
  // universo pelo motor (a soma das filas conta duas vezes o pedido que esta em dois pares: prova
  // de 26/10/2026, 100.431 somados e 100.429 distintos na ultrassonografia)
  K.panorama = async function (m, ordem, ctx) {
    const c = K.campos(), med = K.medidas_fila([], ctx.janelas.viva), out = {};
    const linhas = await K.cubo(m, [c.nome_sol, c.cod_sol], med.map(x => x[1]));
    const cid = new Map();
    (await K.cubo(m, [c.nome_sol, c.cod_sol, '=Left(' + c.cid + ',3)'], ['Count(Distinct ' + K.conj([K.mod_fila()]) + ' ' + c.contador + ')']))
      .forEach(r => { const k = r[0] + '|' + r[1]; if (!cid.has(k)) cid.set(k, []); cid.get(k).push([r[2], r[3]]); });
    const ag = K.oferta(ctx), ag_cod = new Map();
    ctx.agendadas.forEach(r => ag_cod.set(r[1], (ag_cod.get(r[1]) || 0) + r[2]));
    const ifila = med.findIndex(x => x[0] === 'fila') + 2;
    for (const u of ordem.universo) {
      const cods = (u.codigos || []).map(K.codigo), termos = u.termos || [];
      const casa = r => (!cods.length && !termos.length) || cods.some(p => K.casa_codigo(r[1], p)) || termos.some(t => K.tem_termo(r[0], t));
      const sel = linhas.filter(r => casa(r) && (r[ifila] || 0) >= (ordem.minimo || 1));
      const k = r => r[0] + '|' + r[1];
      out[u.rotulo] = {filas: K.tabela(['nome', 'codigo'].concat(med.map(x => x[0]), ['agendadas_12m', 'agendadas_12m_no_codigo', 'cid_principais']),
        sel.map(r => r.concat([ag(r[0], r[1]), ag_cod.has(r[1]) ? ag_cod.get(r[1]) : null,
          (cid.get(k(r)) || []).sort((a, b) => b[1] - a[1]).slice(0, 5)])))};
      if (!sel.length) continue;
      const mod = cods.length && !termos.length ? K.busca(c.cod_sol, cods) : K.mod_nomes([...new Set(sel.map(r => r[0]))]);
      const mod_ag = cods.length && !termos.length ? K.busca(c.cod_ag, cods) : K.mod_nomes_ag([...new Set(sel.map(r => r[0]))]);
      const S = [K.mod_fila(), mod];
      try {
        out[u.rotulo].total = await K.valores(m, [['fila', 'Count(Distinct ' + K.conj(S) + ' ' + c.contador + ')'],
          ['fila_viva', 'Count(Distinct ' + K.conj(S.concat([ctx.janelas.viva])) + ' ' + c.contador + ')'],
          ['pessoas', 'Count(Distinct ' + K.conj(S) + ' ' + c.cns + ')']]);
      } catch (e) { K.lacuna(ctx, u.rotulo + ' total', e); }
      if ((ordem.dimensoes || []).length) out[u.rotulo].dimensoes = await K.dimensoes(m, ordem.dimensoes, S, [mod_ag], ctx, u.rotulo);
    }
    return out;
  };

  // no panorama, o rumo de cada codigo das filas do universo: os entrantes pelo mes do pedido, a
  // oferta pelo mes do agendamento, com realizados e faltas, e a situacao dos agendamentos em 12
  // meses. Por codigo e nao por fila: a rede oferta o exame, e um codigo junta muitos nomes de fila
  K.por_codigo = async function (m, ordem, ctx, pan) {
    const c = K.campos(), out = {}, cods = new Set(), desde = ctx.janelas.entrantes_desde;
    Object.values(pan).forEach(p => p.filas.linhas.forEach(r => cods.add(r[1])));
    const lista = [...cods].sort();
    if (!lista.length) return out;
    const sol = K.busca(c.cod_sol, lista), ag = K.busca(c.cod_ag, lista);
    const ordenar = linhas => linhas.sort((a, b) => a[0] < b[0] ? -1 : a[0] > b[0] ? 1 : (a[1] < b[1] ? -1 : a[1] > b[1] ? 1 : 0));
    for (const d of ordem.por_codigo || []) {
      try {
        if (d === 'entrantes') {
          const ab = await K.cubo(m, [c.cod_sol, "=Date(MonthStart(" + c.data + "),'YYYY-MM')"],
            ['Count(Distinct ' + K.conj([sol, ctx.janelas.entrantes_sol]) + ' ' + c.contador + ')']);
          const agd = await K.cubo(m, [c.cod_ag, "=Date(MonthStart(" + c.data_ag + ' - ' + c.espera_ag + "),'YYYY-MM')"],
            ['Count(Distinct ' + K.conj([ag, ctx.janelas.entrantes_ag]) + ' ' + c.contador_ag + ')']);
          const x = new Map();
          ab.forEach(r => { if (r[1] >= desde) x.set(r[0] + '|' + r[1], [r[0], r[1], r[2], 0]); });
          agd.forEach(r => {
            if (r[1] < desde) return;
            const k = r[0] + '|' + r[1], v = x.get(k) || [r[0], r[1], 0, 0];
            v[3] = r[2];
            x.set(k, v);
          });
          out.entrantes = K.tabela(['codigo', 'mes', 'abertas', 'agendadas'], ordenar([...x.values()]));
        } else if (d === 'oferta') {
          out.oferta = K.tabela(['codigo', 'mes', 'agendamentos', 'realizados', 'faltas'],
            ordenar(await K.cubo(m, [c.cod_ag, K.mes_ag()], K.medidas_oferta([ag, ctx.janelas.oferta]))));
        } else if (d === 'situacao') {
          out.situacao = K.tabela(['codigo', 'situacao', 'agendamentos'], ordenar(await K.cubo(m, [c.cod_ag, c.situacao_ag],
            ['Count(Distinct ' + K.conj([ag, ctx.janelas.agendadas_12m]) + ' ' + c.contador_ag + ')'])));
        } else {
          throw new Error('medida por codigo que o kit nao conhece: ' + d);
        }
      } catch (e) { K.lacuna(ctx, 'por codigo ' + d, e); }
    }
    return out;
  };

  // ------------------------------------------------------------------ a execucao
  K.rodar = function (ordem) {
    const job = {fase: 'abrindo', inicio: Date.now(), erro: null, feito: false};
    raiz.__ms_job = job;
    raiz.__out = null;
    raiz.__partes = null;
    (async () => {
      try {
        const m = await K.modelo();
        job.fase = 'campos';
        await K.conferir_campos(m, ordem);
        job.fase = 'datas';
        const d0 = await K.datas(m), ctx = {lacunas: []};
        ctx.janelas = K.janelas(d0.solicitacao_max, ordem.janela_viva_meses || 24);
        job.fase = 'nomes';
        ctx.nomes = await K.nomes(m);
        ctx.agendadas = await K.agendadas(m, ctx);
        const out = {kit: {versao: K.versao(), assinatura: K.assinatura()}, ordem_hash: K.djb2(K.ascii(JSON.stringify(ordem))),
          tipo: ordem.tipo, app: K.app(), titulo_app: (await m.getAppLayout()).qTitle,
          filtro_fila: K.mod_fila(), filtro_devolvidas: K.mod_dev(), janelas: ctx.janelas, datas: {inicio: d0}};
        if (ordem.tipo === 'panorama') {
          job.fase = 'panorama';
          out.panorama = await K.panorama(m, ordem, ctx);
          if ((ordem.por_codigo || []).length) {
            job.fase = 'por codigo';
            out.por_codigo = await K.por_codigo(m, ordem, ctx, out.panorama);
          }
        } else {
          job.fase = 'varrer';
          out.varredura = await K.varrer(m, ordem, ctx);
          out.objetos = {};
          for (const o of ordem.objetos) {
            job.fase = 'medir ' + o.id;
            out.objetos[o.id] = await K.medir(m, o, ordem, ctx);
          }
        }
        job.fase = 'datas do fim';
        out.datas.fim = await K.datas(m);
        if (out.datas.fim.recarga_utc !== d0.recarga_utc) {
          throw new Error('recarga no meio: a base recarregou de ' + d0.recarga_utc + ' para ' + out.datas.fim.recarga_utc + '; refazer');
        }
        out.lacunas = ctx.lacunas;
        out.campos_data = ['solicitacao_max', 'agendamento_max', 'mais_antiga'];
        out.campos_hora = ['consulta'];
        raiz.__out = K.ascii(JSON.stringify(out));
        job.tamanho = raiz.__out.length;
        job.hash = K.djb2(raiz.__out);
        job.feito = true;
        job.fase = 'pronto';
      } catch (e) {
        job.erro = String(e && e.message || e);
        job.fase = 'erro';
      }
      job.segundos = Math.round((Date.now() - job.inicio) / 1000);
    })();
    return 'rodando: acompanhe com __ms.estado()';
  };
  K.estado = function () {
    const j = raiz.__ms_job || {};
    return {fase: j.fase, feito: !!j.feito, erro: j.erro || null, segundos: j.segundos || Math.round((Date.now() - (j.inicio || Date.now())) / 1000),
      tamanho: j.tamanho || null, hash: j.hash || null, partes: raiz.__partes ? raiz.__partes.length : null};
  };
  K.preparar = function (tamanho) {
    if (!raiz.__out) throw new Error('sem saida: rode a ordem e espere o estado "pronto"');
    raiz.__partes = K.dividir(raiz.__out, tamanho || 300000);
    return raiz.__partes.map(p => p.split('\n')[0]);
  };
  K.parte = i => raiz.__partes[i - 1];
  // o botao copia a parte i para a area de transferencia num clique de verdade (o computer do
  // navegador): navigator.clipboard e negado no painel, e o execCommand funciona
  K.botao = function (i) {
    const doc = raiz.document;
    let b = doc.getElementById('__ms_copiar');
    if (!b) {
      b = doc.createElement('button');
      b.id = '__ms_copiar';
      b.style.cssText = 'position:fixed;top:8px;right:8px;z-index:2147483647;padding:12px 18px;font:16px sans-serif;background:#05a;color:#fff;border:0;border-radius:6px';
      doc.body.appendChild(b);
    }
    b.textContent = 'copiar parte ' + i + '/' + raiz.__partes.length;
    b.onclick = () => {
      const t = doc.createElement('textarea');
      t.value = raiz.__partes[i - 1];
      t.setAttribute('readonly', '');
      t.style.cssText = 'position:fixed;top:0;left:0;width:1px;height:1px;opacity:0';
      doc.body.appendChild(t);
      t.select();
      const ok = doc.execCommand('copy');
      t.remove();
      b.textContent = (ok ? 'copiada a parte ' : 'falhou a parte ') + i + '/' + raiz.__partes.length;
    };
    return b.textContent;
  };

  raiz.__ms = K;
  if (typeof module === 'object' && module && module.exports) module.exports = K;
})(typeof window !== 'undefined' ? window : globalThis);

// --------------------------------------------------------------------- node (CLI)
if (typeof module === 'object' && module && typeof require === 'function' && require.main === module) {
  const fs = require('fs'), path = require('path'), K = module.exports, args = process.argv.slice(2);
  if (args[0] === '--assinatura') {
    console.log(K.assinatura());
  } else if (args[0] === '--hash-ordem') {
    console.log(K.djb2(K.ascii(JSON.stringify(JSON.parse(fs.readFileSync(args[1], 'utf8'))))));
  } else if (args[0] === '--partes') {
    const texto = K.ascii(JSON.stringify(JSON.parse(fs.readFileSync(args[1], 'utf8'))));
    K.dividir(texto, Number(args[3] || 300000)).forEach((p, i) => fs.writeFileSync(path.join(args[2], 'motor_parte_' + (i + 1) + '.txt'), p));
  } else {
    console.error('uso: node motor.js --assinatura | --hash-ordem <ordem.json> | --partes <saida.json> <pasta> [tamanho]');
    process.exit(2);
  }
}
