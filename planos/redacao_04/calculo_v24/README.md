# calculo_v24 — a v24: seis polos, o quadro do cenário 3 e dois planos de tomografia

Aberto em 20/10/2026. A v24 sai da v9 final da equipe, que é a nossa v23, byte a byte (`versoes/plano_v23_20261008.docx`
= `v9_final.docx`), em duas variantes:

- **v24a** (`versoes/plano_v24a_20261020.docx`, que também é o `plano.docx`): tomografia nos seis polos, um tomógrafo
  por polo; a carga da Sudoeste que passa de um equipamento é absorvida no polo da Oeste;
- **v24b** (`versoes/plano_v24b_20261020.docx`): tomografia em rede, sem número de tomógrafos nem distribuição por polo,
  só a carga (3,33) e as horas no total. Internamente, cinco polos com tomografia e a Leste sem.

Cópias marcadas sobre a v23: `dados/v24a_marcado_20261020.docx` e `dados/v24b_marcado_20261020.docx`.

## O que está decidido (usuário, 20/10/2026)

**Cenário 3 com o preço proposto.** Direção Executiva, três coordenações (Administrativa e Financeira, Operacional,
Assistencial), três supervisores de polo (um para dois polos), oito operadores de registro, seis assistentes e a
assessoria de prestação de contas, por 8 meses: R$ 954.560,00, 8,23% do valor global, 79.152 exames. O registro
da decisão está no bloco `v24_em_preparo_20261020` do `../estado.yaml`.

## Os arquivos

- `calculo_v24.py` — o cálculo da v24: o `calculo_v22.py` com o quadro do cenário 3 e o rateio nas 7 Regiões, somado
  nos 6 polos; salas, médicos, tomógrafos, curva e parcelas. Grava `v24.json`.
- `aplicar_v24.py <docx_descompactado> limpo|marcado A|B` — escreve a v24 sobre a v23, na variante A ou B.
- `gerar_v24.sh <python_com_lxml> <pasta>` — roda o cálculo, as quatro cópias (A e B, limpa e marcada) e o sumário.
  O `plano.md` sai do `plano.docx` por `ferramentas/docx_para_md.py`; o da variante B está em
  `versoes/plano_v24b_20261020.md`.

- `cenarios_quadro.py` — roda o `../calculo_v22/calculo_v22.py` com o quadro de cada cenário no lugar do da v22
  (o resto igual) e grava `cenarios_quadro.json`. São seis rodadas: os cenários 1, 2 e 3 com o preço de hoje e
  com o preço proposto. Sem o quadro trocado, o cálculo reproduz a v9 (79.373 exames, R$ 10.673.026,22).
- `planilha_cenarios_quadro.py cenarios_quadro.json <saida.xlsx>` — gera
  `../dados/quadro_gestao_cenarios_e_precificacao_20261020.xlsx`, com cinco abas: a precificação proposta (regra,
  função, mercado, faixa dos aprovados, preço), os três cenários do quadro, o que cada um faz com o plano (exames
  por código, produção, parcelas, carga por operador e por assistente), o mercado do DF e as premissas com os
  aprovados citados. As fórmulas foram recalculadas com o `recalc.py` da skill xlsx.

- `polos_capacidade.py` — roda o cálculo com o quadro do cenário 3 e o rateio nas 7 Regiões de Saúde (o método do
  plano), divide cada Região entre as RAs pela população do Censo 2022 (`../dados/polos_de_imagem_no_df_v20.html`,
  que traz também a posição de cada RA em km) e grava `polos_capacidade.json`. Inclui:
  - as 21 duplas de Regiões;
  - os 6 polos (a Central com a Centro-Sul);
  - a tomografia em 6 e em 5 polos (a Leste sem), RA a RA.

  Importa `quadro` de `cenarios_quadro.py`.
- `planilha_equipe_polos.py polos_capacidade.json <saida.xlsx>` — gera `../dados/rede_imagem_6_polos_20261020.xlsx`, a
  planilha da equipe que negocia com as clínicas. Mostra os 6 polos, o ultrassom e a tomografia que cada clínica
  precisa, com células amarelas para o que a clínica informar, os cenários de 6 e 5 polos, a RA a RA e as perguntas.
  Não cita versão, seção nem custo de gestão.
- O estudo do usuário, com tudo, está em `../estudos/estudo_polos_rede_capacidade_20261020.md`.
- `planilha_custo_por_exame.py v24.json polos_capacidade.json <saida.xlsx>` — gera
  `../estudos/custo_por_exame_v1_20261020.xlsx`, quanto custa um exame para o ISHP. É controle interno.
- `planilha_cenarios_execucao.py v24.json polos_capacidade.json <saida.xlsx>` — gera
  `../estudos/custo_por_exame_v2_20261020.xlsx`, os três cenários de execução. É controle interno.

## A precificação

Regra única: o custo para a empresa, em Brasília, da ocupação que faz o mesmo trabalho (salario.com.br, CAGED dos
últimos 12 meses, acesso em 20/10/2026), limitado à faixa dos aprovados para o nível do cargo
(`biblioteca/precos/cargos_no_acervo.md`), com a hierarquia conferida. Só as duas coordenações administrativas
mudam: a Administrativa e Financeira de R$ 10.500 e a Operacional de R$ 9.500 vão a R$ 8.400. O preço fica fora do
documento linha a linha; ele vai à planilha com o nome do posto (`metodo/coleta/precos.md`).
