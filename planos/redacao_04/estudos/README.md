# estudos/ — estudos internos do plano 4

Uso interno do usuário. Nada daqui vai ao plano nem aos parceiros sem decisão dele.

- `estudo_polos_rede_capacidade_20261020.md` — o quadro decidido, por que juntar a Central e a Centro-Sul (demanda,
  distância, transporte e a rede de clínicas), a rede com CNES, o ultrassom com margem, a tomografia em 6 e em 5 polos
  (a Leste sem) e o que falta confirmar.
- `custo_por_exame_v2_20261020.xlsx` — **a versão para decidir:** quanto custa executar o plano em três cenários (tudo
  nas clínicas; ultrassom feito por nós nos 6 polos; misto, com os polos escolhidos na planilha), com o ultrassom e a
  tomografia polo a polo, a equipe e as premissas numa aba só. Gerada por
  `../calculo_v24/planilha_cenarios_execucao.py`.
- `salas_ultrassom_metricas_20261020.xlsx` — se as 13 salas do documento da equipe de 20/10 (Projeto Zero Fila | USG,
  quantitativo revisado) aguentam: a rede em 11 cenários (tempo por exame, faltas, salas fechadas, 7 meses), cada
  unidade pela fila do plano e pela população do documento, e a tabela de sensibilidade. Gerada por
  `../calculo_v24/planilha_salas_metricas.py`.
- `custo_por_exame_v1_20261020.xlsx` — a primeira versão, guardada como estava: ultrassom pela execução própria, tomografia
  pelas clínicas, a comparação da tomografia com equipe própria e a conta por polo em duas contas. Gerada por
  `../calculo_v24/planilha_custo_por_exame.py`.
- `estudo_filas_imagem_20261102.md` e `.xlsx` — **o estudo das filas de imagem para escolher a carteira do plano 4** pela
  Candanga: o inventário de todas as filas de imagem (coleta de 02/11/2026), o rumo de cada código, quem sustenta a oferta,
  a cobertura dos outros planos (L-008, IEV, redacao_07), a viabilidade e as carteiras comparadas com a v26 e com a
  recomendação de 01/11. Gerado por `estudo_filas_imagem_20261102.py` (o `.json` ao lado é a saída intermediária).
- `estudo_outros_planos_imagem_20261102.md` e `.xlsx` — **o que os planos aprovados já contratam** (os cinco convênios
  do acervo: oftalmologia do ISHP e as OCI do IEV), com quantidades, o exame de imagem de cada OCI e a medida da
  transvaginal com os CID da GIN1. Os nossos planos em elaboração ficam à parte e não contam. Gerado por
  `estudo_outros_planos_imagem_20261102.py`.
- `estudo_filas_imagem_20261102_organizada.xlsx` — **a cópia organizada da planilha do estudo das filas, para ler e
  mostrar.** Revista à tarde de 02/11, com a carteira 1 escolhida: resumo com as respostas; enquadramento (siglas,
  decisões, premissas, tempos, o que confirmar com a SES, metas e proteções); as 20 salas e os 5 tomógrafos por polo;
  pedidos novos; encaminhamento da SES; faltas e pedidos; filas do plano; IEV; origem regional (coleta de Região de
  02/11, `../dados/fontes/mapa_social_20261102_regiao.*`); depois as abas da manhã. Gerada por
  `formatar_estudo_filas_imagem_20261102.py` a partir da planilha completa; não refaz conta.
- `anterior_20261102_manha/` — o estudo das filas como estava antes da revisão da tarde (relatório, scripts, `.json`
  e as duas planilhas), para comparar. O que ficou superado está na seção 0 do relatório.
- `melhorias_planilha_20261102.md` — o mapa das melhorias que o usuário pediu na planilha organizada (cinco abas), o
  que já foi feito, as ofertas sem resposta e as decisões que ficaram com ele.
- `passo_a_passo_painel/` — como ver no Mapa Social quem realizou um exame ou consulta, com capturas (testado em
  02/11/2026 com a mama no HRS).
- `estudo_v26_salas_precos_custos_20261105.xlsx` — **sobre a v26 enviada:** as 20 salas e os 6 tomógrafos polo a
  polo, a demanda por Região (coleta de 15/09), o preço cotado (SIGTAP + 4.282) contra a Candanga, exames por hora
  (CBR 2017 e pesquisa), duas adaptações com a diferença (mais ultrassom ou mais tomografia) e o custo de cada
  procedimento item a item, com as premissas em amarelo. Gerada por `gerar_estudo_v26_salas_precos_custos_20261105.py`.
- `tc_dados_basicos_v26_20261105.xlsx` — só a tomografia da v26: nomes e quantidade de exames por procedimento e
  por fila (com e sem contraste). Gerada por `gerar_tc_dados_basicos_v26_20261105.py`.
- `estudo_12_meses_3_tomografos_20261107.md` e `.xlsx` — **o que muda se a execução passar a 12 meses, com 6 polos
  de ultrassom e 3 de tomografia** (pedido da equipe, 07/11): o quadro de gestão em cinco cenários e quantos exames ele
  tira, o custo de executar (salas, recepção, itens por polo), as salas por polo contra os contratos, a capacidade dos 3
  tomógrafos com o tempo do contraste, o arranjo dos 3 polos de TC, o mapa seção a seção do plano e as decisões. Sobre a
  carteira 1. Na segunda parte do mesmo dia: a gestão readequada para caber em 8,5% (P1, P2 recomendada e P3, com o
  mercado e o menor preço aprovado de cada cargo), o fluxo de atendimento de cada grupo de ultrassom e da tomografia
  com contraste em série e em linha (preparo em paralelo) e os meses da tomografia com 3, 4 ou 5 tomógrafos, com a
  conversão para sem contraste. Gerada por `gerar_estudo_12_meses_3_tomografos_20261107.py`.
- `analise_despacho_gediag_20261108.md` — **o parecer da GEDIAG sobre o PT v1** (Despacho SEI 218755566, assinado em
  05/11; o PDF está em `../recebidos/20261105_ses_despacho_gediag/`): o que ele aprova, os oito elementos que
  condicionam a viabilidade (12.4, a a h) ligados ao plano, os trechos do PT v1 a mudar, o que ele confirma e contesta
  nos estudos de 02/11 e 07/11 e o que acrescenta à devolutiva do Anexo Técnico I.
- `estudo_contraste_fluxo_tempo_20261108.md` e `.xlsx` — **o exame com contraste: tempo, fluxo e regras** (pesquisa
  de 08/11): o tempo de tomógrafo medido em 16 fontes (em série, em linha, sem contraste e coronária), o fluxo do
  usuário passo a passo, a capacidade da v26 e da carteira 1 com esses tempos, as poltronas e a enfermagem do
  repouso, as reações esperadas, a conversão realista para sem contraste (com os CIDs da fila) e a 4.8 do PT v1
  contra o ACR 2026, o ESUR 2026 e as normas do CFM. No adendo do mesmo dia, o que muda no fluxo com contraste e
  as medidas que o agilizam (aba 8 e seção 10). Gerada por `gerar_estudo_contraste_fluxo_tempo_20261108.py`.
- `estudo_tempos_tomografia_3_polos_20261109.md` e `.xlsx` — **o fluxo da TC com e sem contraste, quanto cada
  tomógrafo faz por hora, o ultrassom por tipo de exame e a equipe para 10 horas, para revisitar** (09/11): quem
  decide o contraste e quando, a punção na mesa contra a punção antes, o passo a passo com onde o paciente fica e os
  tempos de referência do estudo de 08/11, as cadeiras ou macas do preparo e do repouso, 6 e 5 polos em 8 meses
  contra 3 em 12, o limite de horas por dia contra minutos por exame, os 12 tipos de ultrassom com as horas de sala,
  a equipe de um tomógrafo e de uma sala de ultrassom (cargos da v26, 4.15, e o auxiliar de sala do ultrassom) e as
  pausas. O lugar das respostas recalcula tudo por pessoa. O .md traz a mensagem ao grupo. Gerada por
  `gerar_tempos_tomografia_20261109.py`.
- `tempos_e_equipe_tomografia_ultrassom_20261109.xlsx` — **o formulário para quem ajuda o projeto na parte
  assistencial** (09/11; não é para as clínicas), só sobre tempo e equipe: na aba Tomografia, os minutos de cada
  etapa, com as duas punções em linhas separadas, onde o paciente fica e o repouso, a equipe para 10 horas e as
  pausas; na aba Ultrassom, as cinco partes de cada um dos 12 tipos de exame e a equipe de uma sala. Sem nada
  interno. Pede só o nome de quem preenche. Gerada pelo mesmo script.
- `tempos_e_equipe_tomografia_ultrassom_nossa_referencia_20261109.xlsx` — **o mesmo formulário preenchido com a nossa
  referência** (09/11), com a fonte de cada número na Observação, para mandar junto com o em branco. Gerada pelo
  mesmo script.
- `estudo_readequacao_candanga_margem_20261109.md` e `.xlsx` — **a readequação à Candanga pela margem de cada exame**
  (09/11): a margem por exame, por hora e em % do preço, com a complexidade e a fila de hoje e de 12 meses; o cenário 1
  (a v26 como está e a sobra de R$ 245 mil); o cenário 2 (as filas escolhidas de novo); e a comparação com a carteira 1.
  Gerada por `gerar_readequacao_candanga_margem_20261109.py`.
- `quantitativo_tc_polo_oeste_20261109.xlsx` — **para o parceiro do polo Oeste** (09/11): os exames de tomografia por
  mês, nos 12 meses, num arranjo de 4 polos (Oeste, Central, Norte e Leste), sem valores. Parte da TC do cenário 2 da
  readequação (14.565), repartida pela origem da fila por Região (02/11), com a Sudoeste no Oeste e o Sul e o
  Centro-Sul no Central, e dois meses de rampa. Gerada por `gerar_quantitativo_tc_polo_oeste_20261109.py`, que
  imprime os 4 polos.
- `quantitativo_tc_total_por_regiao_20261109.xlsx` — **a demanda total de tomografia por Região de Saúde** (09/11),
  mês a mês nas 7 Regiões, sem polos nem valores. Mesma conta e mesmo gerador do quantitativo do polo Oeste.
- `roteiro_reuniao_20261110.md` — **o roteiro da reunião de 10/11:** tempo de cada exame e a média do ultrassom e da
  tomografia; salas de ultrassom nos 6 polos de 8 a 12 meses; uso dos tomógrafos por % de contraste, com a punção na
  mesa e antes; custos e percentuais de hoje, com o que cada custo inclui; e a documentação das parcerias. Junta os
  estudos de 20/10 a 09/11; as contas de salas por mês e de contraste são novas, feitas à mão, sem gerador.
- `analise_oficio_parceiro_20261110.md` — **a análise do rascunho de ofício do parceiro** (12 meses, USG unilateral e TC
  com contraste, PDF de 09/11): a conta dele ao lado da nossa, a garantia de R$ 1.500 por plantão, as 11 salas contra
  as 15, a tomografia em 4 unidades, as perguntas sobre salas a mais e sobre o preço do contraste, e o que conflita
  com o plano e com o despacho da GEDIAG.
- `planilha_custos_sebastião.xlsx` — **o ofício do parceiro destrinchado, só com os números dele**
  (11/11), sem o plano de trabalho e sem comparação com a carteira: aba Ultrassom (cada custo por mês, em 12 meses e
  por exame; a garantia do médico explicada, em plantão de 10 h com 1 h de almoço, com o quadro de quanto ele recebe
  conforme a agenda e os dois extremos, agenda cheia e 11 salas abertas todo dia) e aba Tomografia (R$ 175 + R$ 43,
  unidade a unidade). Gerada por `gerar_planilha_custos_sebastiao.py`.
- `carteira_final_20261111.xlsx` — **a carteira final, para decidir** (11/11): os exames escolhidos com a fila de
  02/11, a fila da SES de 09/11 (Despacho SEI 219528407) e o valor pela Candanga; o que ficou fora, com o valor e o
  motivo; o rumo de cada código e cada fila pelo nome; as saídas para fechar o valor pedido, com uma coluna para
  marcar e somar; e como se saiu da sobra de R$ 245 mil da v26 para a falta de hoje. As decisões estão em
  `../pendencias.md`, D-011 e D-012. Gerada por `gerar_carteira_final_20261111.py`.
- `carteira_final_v2_20261111.xlsx` — **a mesma carteira, versão 2** (11/11, a pedido do usuário): uma coluna de
  fila só (coleta de 02/11), a articulação fora da ortopedia numa linha, com o detalhe na aba Articulação; em Não
  escolhidos, o valor de cada grupo pela Candanga e o total que trariam ao plano; sem a aba Estudos, e a v26 tratada
  como versão enviada (PT v1). Revista no mesmo dia: margem em R$ e subtotais por modalidade, as filas
  infantis de ortopedia fora da articulação, o rumo nas duas janelas (12 meses e 3 últimos), o Doppler separado dos
  pedidos novos nas saídas, a ponte ligada a Escolhidos e a aba Conferência, que fecha a fila de cada código. Aba Agenda
  da SES: quem entra na fila por mês e quanto do que a SES realiza a rede do plano assume nos exames fáceis para
  fechar a falta, com o uso das salas. Gerada
  por `gerar_carteira_final_v2_20261111.py`; a v1 fica como estava.
- `carteira_final_v3_20261111.xlsx` — **a versão simples da carteira** (11/11, a pedido do usuário): Resumo; Escolhidos
  (exame, modalidade, código, fila de hoje, exames novos em 12 meses, preço e valor, com a condição do Doppler de
  membros); Filas escolhidas (cada fila do SISREG que compõe cada exame); Saídas (as escolhidas, as de reserva se o
  Doppler sair e as descartadas); Não escolhidos e Estudos das filas, iguais à v2. Fecha o valor com os exames novos
  de 7 exames fáceis de ultrassom. Gerada por `gerar_carteira_final_v3_20261111.py`, que roda o gerador da v2 antes.
- `simulador_margem_20261111.xlsx` — **o simulador de margem** (11/11), controle interno: troca-se a quantidade de
  cada exame de ultrassom e de tomografia e a planilha mostra o valor que traz pela Candanga, o custo pelas contas do
  parceiro (as de `planilha_custos_sebastião.xlsx`) e a margem, no melhor e no pior cenário do ultrassom; no rodapé, a
  diferença para o valor a fechar (global menos o custo acessório de R$ 956.160), a margem do conjunto, o médico do
  ultrassom e se as quantidades cabem nas salas, pelos minutos do nosso estudo e pelos do ofício do parceiro. No alto,
  a parte da fila de tomografia com contraste que é feita de fato com contraste, com um quadro de 100% a 50%. Parte
  das quantidades da carteira v3. Aba Salas por polo: a fila de cada exame repartida pelos 6 polos (coleta de Região
  de 02/11), as salas que cada polo precisa e quantas faltam contra a rede do ofício, no cenário ideal (cada polo
  atende a própria Região) e no real (uma matriz diz para qual polo vai a fila de cada Região). Aba Premissas com os custos do
  parceiro e o tempo do estudo dele (70 ultrassons em 9 horas). Gerada por `gerar_simulador_margem_20261111.py`.
- A conta do Sebastião ao lado da nossa, com o valor final e a margem por exame (11/11), saiu daqui e está em
  `../custos_e_margens/` (veja o README de lá).
