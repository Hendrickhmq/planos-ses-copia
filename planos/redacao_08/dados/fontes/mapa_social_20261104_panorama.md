# Mapa Social da Saúde — panorama: ecocardiografia, coleta de 04/11/2026

Ordem de coleta: Recoleta de 04/11/2026: só a fila de ecocardiografia (o que o plano vai executar), com o rumo de cada código (entrantes, oferta pelo mês do agendamento, faltas, situação)

Coleta montada por `ferramentas/montar_coleta.py` a partir da saída do kit do motor: o modelo não escreveu número nenhum, e o resumo não se edita à mão (conferência K). A decisão de cada fila vem do enquadramento do plano.

| campo | conteúdo |
|---|---|
| Fonte | Mapa Social da Saúde – Regulamentação (MPDFT) · Lista de Espera – Exames e Consultas · `https://paineis-ext.mpdft.mp.br/extensions/mapasauderegulamentacao/mapasauderegulamentacao.html` · app Qlik `7edb02fa-f1f5-4ea6-b348-049a4ac2d095` · dados SISREG/DATASUS |
| Última recarga da base | 04/11/2026 14:33:58 (qLastReloadTime 2026-11-04T17:33:58.854Z) |
| Consulta | 04/11/2026 15:36:32 a 15:36:53 (relógio do motor), sem recarga no meio |
| Solicitação mais recente na base | 03/11/2026 (agendamento mais distante: 04/02/2027) |
| Medida | **fila** = os três status: pendente de regulação, corrigida e reenviada para regulação, pendente de regulação por fila de espera. Devolvidas para complementação ficam fora e são contadas à parte |
| Fila viva | só as solicitações a partir de `data_solicitacao={">=03/11/2024"}` (24 meses contados da solicitação mais recente) |
| Agendadas em 12 meses | `data_agendamento={">=03/11/2025<=02/11/2026"}`, todos os status |
| Ordem | panorama; `ordem.json` (hash 1047463901) |
| Via | kit do motor `ferramentas/mapa_social/motor.js` (versão 2026-10-27, assinatura 1939648169); saída pela área de transferência, 1 parte(s) conferidas por hash (`ferramentas/ler_motor.py`) |

Pessoas = CNS distintos no conjunto (quem espera por mais de um exame conta uma vez); só a contagem sai do motor. Espera em dias, calculada no motor sobre os registros do conjunto.

## Alarmes

Não se aplicam ao panorama: os alarmes são do objeto (CID, composição, fila viva), e o panorama não tem objeto.

## Lacunas

nenhuma

## O universo

O total de cada universo é do motor, com cada pedido e cada pessoa uma vez: a soma das filas pode passar dele, porque o mesmo pedido pode estar em dois pares nome × código.

| recorte | o que entra | filas | fila | fila viva | pessoas |
|---|---|---|---|---|---|
| ecocardiografia | codigos: 02.05.01.001-6, 02.05.01.002-4, 02.05.01.003-2 | 10 | 14.953 | 14.947 | 14.928 |

## Varredura das filas (panorama)

Cada fila do universo (nome exato × código), sem decisão: o panorama só mostra. Anos de estoque = fila ÷ agendadas em 12 meses pelo mesmo nome e código (**calculado**).

### ecocardiografia: por pessoas

| fila | código | fila | fila viva | pessoas | devolvidas | espera média | espera mediana | espera máxima | pedido mais antigo | agendadas 12 m | anos de estoque | CID principais |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1. ECOCARDIOGRAFIA BI-DIMENSIONAL COM DOPPLER ADULTO | 02.05.01.003-2 | 13.474 | 13.474 | 13.473 | 13.473 | 129,7 | 119,0 | 541,1 | 12/05/2025 | 33.842 | 0,4 | I10 2.444, I50 2.343, I25 1.174 |
| 2. ECOCARDIOGRAFIA BI-DIMENSIONAL COM DOPPLER INFANTIL | 02.05.01.003-2 | 1.360 | 1.360 | 1.360 | 2.568 | 111,7 | 104,0 | 721,9 | 12/11/2024 | 5.847 | 0,2 | R01 317, Q21 306, Q25 92 |
| 5. ECOCARDIOGRAFIA DE ESTRESSE ADULTO | 02.05.01.001-6 | 69 | 69 | 69 | 1.437 | 28,4 | 29,0 | 50,9 | 14/09/2026 | 763 | 0,1 | I20 19, I25 15, I10 8 |
| 9. ECOCARDIOGRAFIA FETAL | 02.05.01.003-2 | 36 | 36 | 36 | 391 | 36,9 | 19,6 | 309,9 | 29/12/2025 | 786 | 0,0 | Z35 16, Z36 3, E11 2 |
| 7. ECOCARDIOGRAFIA TRANSEOFAGICA ADULTO | 02.05.01.002-4 | 8 | 8 | 8 | 1.049 | 58,0 | 5,0 | 406,9 | 23/09/2025 | 1.134 | 0,0 | I33 3, C50 1, R94 1 |
| ECOCARDIOGRAFIA BI-DIMENSIONAL SEM DOPPLER ADULTO | 02.05.01.003-2 | 2 | 0 | 2 | 0 | 6.969,6 | 6.969,6 | 6.972,6 | 03/10/2007 | — | — | R68 2 |
| 16.ECOCARDIOGRAFIA TRANSTORACICA - INFANTIL | 02.05.01.003-2 | 1 | 0 | 1 | 0 | 4.950,9 | 4.950,9 | 4.950,9 | 15/04/2013 | 0 | sem agendamento | L81 1 |
| 8. ECOCARDIOGRAFIA TRANSEOFAGICA INFANTIL | 02.05.01.002-4 | 1 | 0 | 1 | 46 | 1.825,1 | 1.825,1 | 1.825,1 | 05/11/2021 | 0 | sem agendamento | Q20 1 |
| ECOCARDIOGRAFIA BI-DIMENSIONAL SEM DOPPLER ADULTO EMERGENCIA | 02.05.01.003-2 | 1 | 0 | 1 | 0 | 6.986,6 | 6.986,6 | 6.986,6 | 19/09/2007 | — | — | R68 1 |
| ECOCARDIOGRAFIA BI-DIMENSIONAL SEM DOPPLER INFANTIL | 02.05.01.003-2 | 1 | 0 | 1 | 0 | 6.980,6 | 6.980,6 | 6.980,6 | 25/09/2007 | — | — | R68 1 |

### ecocardiografia: as 20 de maior espera média

| fila | código | fila | fila viva | pessoas | devolvidas | espera média | espera mediana | espera máxima | pedido mais antigo | agendadas 12 m | anos de estoque | CID principais |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ECOCARDIOGRAFIA BI-DIMENSIONAL SEM DOPPLER ADULTO EMERGENCIA | 02.05.01.003-2 | 1 | 0 | 1 | 0 | 6.986,6 | 6.986,6 | 6.986,6 | 19/09/2007 | — | — | R68 1 |
| ECOCARDIOGRAFIA BI-DIMENSIONAL SEM DOPPLER INFANTIL | 02.05.01.003-2 | 1 | 0 | 1 | 0 | 6.980,6 | 6.980,6 | 6.980,6 | 25/09/2007 | — | — | R68 1 |
| ECOCARDIOGRAFIA BI-DIMENSIONAL SEM DOPPLER ADULTO | 02.05.01.003-2 | 2 | 0 | 2 | 0 | 6.969,6 | 6.969,6 | 6.972,6 | 03/10/2007 | — | — | R68 2 |
| 16.ECOCARDIOGRAFIA TRANSTORACICA - INFANTIL | 02.05.01.003-2 | 1 | 0 | 1 | 0 | 4.950,9 | 4.950,9 | 4.950,9 | 15/04/2013 | 0 | sem agendamento | L81 1 |
| 8. ECOCARDIOGRAFIA TRANSEOFAGICA INFANTIL | 02.05.01.002-4 | 1 | 0 | 1 | 46 | 1.825,1 | 1.825,1 | 1.825,1 | 05/11/2021 | 0 | sem agendamento | Q20 1 |
| 1. ECOCARDIOGRAFIA BI-DIMENSIONAL COM DOPPLER ADULTO | 02.05.01.003-2 | 13.474 | 13.474 | 13.473 | 13.473 | 129,7 | 119,0 | 541,1 | 12/05/2025 | 33.842 | 0,4 | I10 2.444, I50 2.343, I25 1.174 |
| 2. ECOCARDIOGRAFIA BI-DIMENSIONAL COM DOPPLER INFANTIL | 02.05.01.003-2 | 1.360 | 1.360 | 1.360 | 2.568 | 111,7 | 104,0 | 721,9 | 12/11/2024 | 5.847 | 0,2 | R01 317, Q21 306, Q25 92 |
| 7. ECOCARDIOGRAFIA TRANSEOFAGICA ADULTO | 02.05.01.002-4 | 8 | 8 | 8 | 1.049 | 58,0 | 5,0 | 406,9 | 23/09/2025 | 1.134 | 0,0 | I33 3, C50 1, R94 1 |
| 9. ECOCARDIOGRAFIA FETAL | 02.05.01.003-2 | 36 | 36 | 36 | 391 | 36,9 | 19,6 | 309,9 | 29/12/2025 | 786 | 0,0 | Z35 16, Z36 3, E11 2 |
| 5. ECOCARDIOGRAFIA DE ESTRESSE ADULTO | 02.05.01.001-6 | 69 | 69 | 69 | 1.437 | 28,4 | 29,0 | 50,9 | 14/09/2026 | 763 | 0,1 | I20 19, I25 15, I10 8 |

### ecocardiografia: as 20 de mais anos de estoque

| fila | código | fila | fila viva | pessoas | devolvidas | espera média | espera mediana | espera máxima | pedido mais antigo | agendadas 12 m | anos de estoque | CID principais |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 16.ECOCARDIOGRAFIA TRANSTORACICA - INFANTIL | 02.05.01.003-2 | 1 | 0 | 1 | 0 | 4.950,9 | 4.950,9 | 4.950,9 | 15/04/2013 | 0 | sem agendamento | L81 1 |
| 8. ECOCARDIOGRAFIA TRANSEOFAGICA INFANTIL | 02.05.01.002-4 | 1 | 0 | 1 | 46 | 1.825,1 | 1.825,1 | 1.825,1 | 05/11/2021 | 0 | sem agendamento | Q20 1 |
| 1. ECOCARDIOGRAFIA BI-DIMENSIONAL COM DOPPLER ADULTO | 02.05.01.003-2 | 13.474 | 13.474 | 13.473 | 13.473 | 129,7 | 119,0 | 541,1 | 12/05/2025 | 33.842 | 0,4 | I10 2.444, I50 2.343, I25 1.174 |
| 2. ECOCARDIOGRAFIA BI-DIMENSIONAL COM DOPPLER INFANTIL | 02.05.01.003-2 | 1.360 | 1.360 | 1.360 | 2.568 | 111,7 | 104,0 | 721,9 | 12/11/2024 | 5.847 | 0,2 | R01 317, Q21 306, Q25 92 |
| 5. ECOCARDIOGRAFIA DE ESTRESSE ADULTO | 02.05.01.001-6 | 69 | 69 | 69 | 1.437 | 28,4 | 29,0 | 50,9 | 14/09/2026 | 763 | 0,1 | I20 19, I25 15, I10 8 |
| 9. ECOCARDIOGRAFIA FETAL | 02.05.01.003-2 | 36 | 36 | 36 | 391 | 36,9 | 19,6 | 309,9 | 29/12/2025 | 786 | 0,0 | Z35 16, Z36 3, E11 2 |
| 7. ECOCARDIOGRAFIA TRANSEOFAGICA ADULTO | 02.05.01.002-4 | 8 | 8 | 8 | 1.049 | 58,0 | 5,0 | 406,9 | 23/09/2025 | 1.134 | 0,0 | I33 3, C50 1, R94 1 |

## Rumo por código

Um código por linha, com as filas do universo somadas (cada par nome × código uma vez). Tudo **calculado** no montador sobre a série mensal do motor (abas "Por código" da planilha). Os 12 meses fechados vão de 2025-11 a 2026-10, e os 12 de antes, de 2024-11 a 2025-10. Entrantes = pedidos abertos mais os já agendados, pelo mês do pedido. Oferta = agendamentos pelo mês em que acontecem, em todas as situações. Falta = faltas ÷ (realizados + faltas). Saldo por mês = (entrantes − oferta) ÷ 12: positivo, a fila cresce. Maior mês de oferta e média dos 3 últimos meses fechados, para ver o esforço que parou.

| código | fila mais pedida do código | fila | fila viva | devolvidas | entrantes 12 m | entrantes 12 m antes | oferta 12 m | oferta 12 m antes | saldo por mês | falta 12 m | maior mês de oferta | oferta média 3 últimos meses |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 02.05.01.003-2 | 1. ECOCARDIOGRAFIA BI-DIMENSIONAL COM DOPPLER ADULTO | 14.875 | 14.870 | 16.432 | 43.146 | 42.122 | 40.475 | 39.633 | 222,6 | 25% | 2026-09 (3.730) | 3.526,0 |
| 02.05.01.001-6 | 5. ECOCARDIOGRAFIA DE ESTRESSE ADULTO | 69 | 69 | 1.437 | 852 | 779 | 763 | 722 | 7,4 | 48% | 2026-07 (75) | 67,7 |
| 02.05.01.002-4 | 7. ECOCARDIOGRAFIA TRANSEOFAGICA ADULTO | 9 | 8 | 1.095 | 1.303 | 1.118 | 1.135 | 1.098 | 14,0 | 50% | 2026-08 (123) | 119,3 |

## Região de Saúde

Região de Saúde: não pedida na ordem.

## Diferença para a coleta anterior

Contra `dados/fontes/mapa_social_20261027_porta_bruto/coleta_20261027.json` (recarga 27/10/2026 16:32:47). Diferença **calculada** no montador.

A coleta anterior não tem as mesmas filas nem os mesmos objetos.
