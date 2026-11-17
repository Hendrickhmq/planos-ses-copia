# v23 (08/10/2026) — a 4.16 com a sugestão da equipe sobre as salas, sobre a v22

- `aplicar_v23.py <docx_descompactado> limpo|marcado` — muda só a 4.16 da v22:
  - a alínea (b) passa a pedir, nos polos com tomografia, o projeto de blindagem aprovado e o laudo de
    levantamento radiométrico, junto com a licença sanitária, na formalização;
  - a alínea (h), nova, trata da conformidade com a IN Anvisa 93/2021 e a RDC Anvisa 50/2002, no que couber
    a cada modalidade.

  O modo `marcado` mostra só o que mudou em relação à v22.
- `gerar_v23.sh <python_com_lxml> <pasta>` — roda as duas cópias e o sumário. As páginas não mudaram: são 33.

As normas citadas estão em `biblioteca/normas/` (NM-087 a NM-089 no `registros/acervo.csv`). As decisões e o que
os planos do IEV dizem sobre as salas estão em `../estado.yaml`, no bloco `v23_20261008`.

## Planilhas de apoio (08/10/2026), em `planilhas/`

- `por_codigo_regiao.py <saida.json>` — exames de cada procedimento em cada Região, com a mesma parte de cada
  fila que o rateio usa. Os inteiros fecham com o total do código (planilha do plano) e com o ultrassom e a
  tomografia de cada Região (7.3). É estimativa: o plano não fixa essa divisão. Resultado em `matriz_v23.json`.
- `montar_xlsx.py matriz_v23.json <saida.xlsx>` — gera `../../dados/exames_por_procedimento_e_regiao_v23.xlsx`.
- `montar_cotacao.py matriz_v23.json <saida.xlsx>` — gera `../../dados/pesquisa_precos_clinicas_v23.xlsx`, com
  referência de 50% do valor unitário (com o incremento), cotação de quatro clínicas e volume por Região.
- `montar_cotacao_tabela.py matriz_v23.json <saida.xlsx>` — gera `../../dados/pesquisa_precos_clinicas_v23_tabela.xlsx`,
  a mesma cotação só com a tabela, sem o valor unitário do plano e sem notas.
  Na aba do volume, a última linha traz os polos de cada Região (os dez da v21, `polos_por_regiao` no `estado.yaml`).
- `montar_tomografia.py matriz_v23.json ../../dados/polos_de_imagem_no_df_v20.html <saida.xlsx>` (14/10/2026) — gera
  `../../dados/tomografia_panorama_polos.xlsx`, o panorama da tomografia para a equipe de negociação: a demanda por
  Região e por RA, os cenários de 6 polos (o pedido da SES-DF, um por Região), 5 e 4 polos (um tomógrafo cada) contra
  a faixa de 300 a 500 exames por mês, o contraste, a capacidade do tomógrafo e um teste de atraso da regulação. Vai
  a quem não tem o plano: não cita versão nem seção. A divisão das Regiões entre as RAs segue a população do Censo 2022
  (estimativa); Norte e Leste se separam pela fila de 15/09/2026. O polo de cada RA em cada cenário fica em células
  amarelas da aba Por RA.
- `montar_valores_parceiros.py matriz_v23.json <saida.xlsx>` (16/10/2026) — gera
  `../../dados/valores_procedimentos_parceiros.xlsx`: a planilha para os parceiros: valor cheio por exame (tabela SUS + incremento),
  valor ao parceiro (50%), exames previstos e total ao parceiro. Sem versão, custo administrativo nem diferença.

As planilhas precisam de openpyxl. As fórmulas foram recalculadas com o `recalc.py` da skill xlsx.
