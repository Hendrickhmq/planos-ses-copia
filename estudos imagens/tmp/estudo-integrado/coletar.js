// Complemento do líder para ano por nome exato x código, sem modificar o kit.
// Executar no mesmo painel: __imagemAnual(<ordem.json>).
// Usa exclusivamente as funções públicas do motor.js para consultar o Qlik.
(function (raiz) {
  raiz.__imagemAnual = function (ordem) {
    const K = raiz.__ms;
    const job = {fase: 'iniciando complemento anual', inicio: Date.now(), feito: false, erro: null};
    raiz.__ms_job = job;
    raiz.__out = null;
    raiz.__partes = null;
    (async function () {
      try {
        if (ordem.contrato !== 'imagem-anual-v1') throw new Error('ordem complementar incompatível');
        const m = await K.modelo(), c = K.campos();
        const d0 = await K.datas(m);
        const ctx = {lacunas: [], janelas: K.janelas(d0.solicitacao_max, ordem.janela_viva_meses)};
        const nomes = [...new Set(ordem.grupos.flatMap(g => g.nomes))];
        const mods = [K.mod_nomes(nomes)];
        const med = K.medidas_fila(mods, ctx.janelas.viva);
        const out = {tipo: 'imagem_anual_complementar', contrato: ordem.contrato,
          kit: {versao: K.versao(), assinatura: K.assinatura()}, app: K.app(),
          ordem_hash: K.djb2(K.ascii(JSON.stringify(ordem))),
          filtro_fila: K.mod_fila(), filtro_devolvidas: K.mod_dev(),
          datas: {inicio: d0}, janelas: ctx.janelas, grupos: [],
          campos_data: ['solicitacao_max', 'agendamento_max', 'mais_antiga'], campos_hora: ['consulta']};
        job.fase = 'nomes e códigos sem fusão de grafias';
        out.filas = K.tabela(['nome', 'codigo'].concat(med.map(x => x[0])),
          await K.cubo(m, [c.nome_sol, c.cod_sol], med.map(x => x[1])));
        // Também traz os zeros atuais que possuem solicitações em outros status.
        job.fase = 'todos os anos por nome e código';
        out.anos = K.tabela(['nome', 'codigo', 'ano'].concat(med.map(x => x[0])),
          await K.cubo(m, [c.nome_sol, c.cod_sol, c.ano], med.map(x => x[1])));
        const unioes = ordem.grupos.concat([
          {escopo: 'exame', modalidade: 'TOTAL EXAMES', nomes: [...new Set(ordem.grupos.filter(g => g.escopo === 'exame').flatMap(g => g.nomes))]},
          {escopo: 'complementar', modalidade: 'TOTAL COMPLEMENTAR', nomes: [...new Set(ordem.grupos.filter(g => g.escopo === 'complementar').flatMap(g => g.nomes))]}
        ]);
        for (const g of unioes) {
          job.fase = 'união distinta e anos: ' + g.modalidade;
          const pares = K.medidas_fila([K.mod_nomes(g.nomes)], ctx.janelas.viva);
          out.grupos.push({escopo: g.escopo, modalidade: g.modalidade,
            total: await K.valores(m, pares),
            anos: K.tabela(['ano'].concat(pares.map(x => x[0])), await K.cubo(m, [c.ano], pares.map(x => x[1])))});
        }
        // Mantém a janela complementar do método, explicitamente separada da fila de todos os anos.
        job.fase = 'entrantes oferta e situação por código (janela do método)';
        const p = {imagem: {filas: {linhas: out.filas.linhas}}};
        out.por_codigo = await K.por_codigo(m, {por_codigo: ordem.por_codigo}, ctx, p);
        out.lacunas = ctx.lacunas;
        out.datas.fim = await K.datas(m);
        if (out.datas.fim.recarga_utc !== d0.recarga_utc) throw new Error('recarga no meio: refazer o complemento');
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
    return 'rodando complemento: __ms.estado()';
  };
})(window);
