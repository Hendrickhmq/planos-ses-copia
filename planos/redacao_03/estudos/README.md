# estudos/ — estudos internos da OCI de câncer gástrico

Uso interno do ISHP. Nada daqui vai ao plano nem às clínicas sem decisão do usuário.

A base é o plano assinado pelo ISHP em 01/10/2026 (`../dados/ishp_plano_assinado_20261001.pdf`):
13.012 OCIs 09.01.01.007-3 a R$ 600,11, dois polos (Taguatinga e CONIC), dez/2026 a jul/2027.
Ele sucede o rascunho deste diretório (`../plano.md`, 3 polos e 12.967 OCIs).

- `precificacao_oci_20261021.md` — o que é preciso para precificar a OCI e até quanto pagar às
  clínicas: o que o plano obriga, a OCI por dentro, o dinheiro, as três formas de contratar (pacote,
  por componente, equipe própria), a biópsia, o retorno, as perguntas para cada clínica.
- `teto_oci_20261021.xlsx` — a planilha das contas, com as premissas e a cotação em amarelo. Gerada
  por `calculo/planilha_teto_oci.py <saida.xlsx>` e recalculada com o `recalc.py` da skill xlsx.

Os preços de mercado, linha a linha, estão em `../dados/precos.md`; a Tabela de 10/2026, em
`../dados/fontes/sigtap_ftp_202610.md`.
