# Mapa Social da Saúde — panorama: mama e transvaginal, coleta de 01/11/2026

Ordem de coleta: Mama e transvaginal: quem fez a oferta extra de jul. a out. de 2026 (mutirão nas unidades de sempre ou oferta nova)? A oferta por unidade executante e mês, com os entrantes e a oferta do código.

Coleta montada por `ferramentas/montar_coleta.py` a partir da saída do kit do motor: o modelo não escreveu número nenhum, e o resumo não se edita à mão (conferência K). A decisão de cada fila vem do enquadramento do plano.

| campo | conteúdo |
|---|---|
| Fonte | Mapa Social da Saúde – Regulamentação (MPDFT) · Lista de Espera – Exames e Consultas · `https://paineis-ext.mpdft.mp.br/extensions/mapasauderegulamentacao/mapasauderegulamentacao.html` · app Qlik `7edb02fa-f1f5-4ea6-b348-049a4ac2d095` · dados SISREG/DATASUS |
| Última recarga da base | 01/11/2026 14:31:49 (qLastReloadTime 2026-11-01T17:31:49.085Z) |
| Consulta | 01/11/2026 15:03:54 a 15:04:24 (relógio do motor), sem recarga no meio |
| Solicitação mais recente na base | 28/10/2026 (agendamento mais distante: 04/02/2027) |
| Medida | **fila** = os três status: pendente de regulação, corrigida e reenviada para regulação, pendente de regulação por fila de espera. Devolvidas para complementação ficam fora e são contadas à parte |
| Fila viva | só as solicitações a partir de `data_solicitacao={">=28/10/2024"}` (24 meses contados da solicitação mais recente) |
| Agendadas em 12 meses | `data_agendamento={">=28/10/2025<=27/10/2026"}`, todos os status |
| Ordem | panorama; `ordem.json` (hash 1509844900) |
| Via | kit do motor `ferramentas/mapa_social/motor.js` (versão 2026-10-27, assinatura 2089625745); saída pela área de transferência, 1 parte(s) conferidas por hash (`ferramentas/ler_motor.py`) |

Pessoas = CNS distintos no conjunto (quem espera por mais de um exame conta uma vez); só a contagem sai do motor. Espera em dias, calculada no motor sobre os registros do conjunto.

## Alarmes

Não se aplicam ao panorama: os alarmes são do objeto (CID, composição, fila viva), e o panorama não tem objeto.

## Lacunas

nenhuma

## O universo

O total de cada universo é do motor, com cada pedido e cada pessoa uma vez: a soma das filas pode passar dele, porque o mesmo pedido pode estar em dois pares nome × código.

| recorte | o que entra | filas | fila | fila viva | pessoas |
|---|---|---|---|---|---|
| mama e transvaginal | codigos: 02.05.02.009-7, 02.05.02.018-6 | 5 | 22.247 | 14.209 | 20.115 |

## Varredura das filas (panorama)

Cada fila do universo (nome exato × código), sem decisão: o panorama só mostra. Anos de estoque = fila ÷ agendadas em 12 meses pelo mesmo nome e código (**calculado**).

### mama e transvaginal: por pessoas

| fila | código | fila | fila viva | pessoas | devolvidas | espera média | espera mediana | espera máxima | pedido mais antigo | agendadas 12 m | anos de estoque | CID principais |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ECOGRAFIA DE MAMAS - BILATERAL | 02.05.02.009-7 | 12.950 | 8.510 | 12.928 | 7.731 | 627,6 | 517,2 | 6.128,6 | 21/01/2010 | 10.474 | 1,2 | N63 3.381, Z12 2.707, N64 2.092 |
| ECOGRAFIA TRANSVAGINAL | 02.05.02.018-6 | 9.294 | 5.699 | 9.293 | 8.953 | 657,7 | 527,1 | 5.892,6 | 14/09/2010 | 18.028 | 0,5 | Z01 2.704, N95 1.210, R10 711 |
| ULTRA-SONOGRAFIA DE MAMAS (BILATERAL) | 02.05.02.009-7 | 1 | 0 | 1 | 0 | 1.524,0 | 1.524,0 | 1.524,0 | 30/08/2022 | 0 | sem agendamento | N60 1 |
| ULTRA-SONOGRAFIA DOPPLER DE MAMAS | 02.05.02.009-7 | 1 | 0 | 1 | 0 | 1.523,9 | 1.523,9 | 1.523,9 | 30/08/2022 | 0 | sem agendamento | Z12 1 |
| USG TRANSVAGINAL | 02.05.02.018-6 | 1 | 0 | 1 | 0 | 3.968,2 | 3.968,2 | 3.968,2 | 21/12/2015 | — | — | Z00 1 |

### mama e transvaginal: as 20 de maior espera média

| fila | código | fila | fila viva | pessoas | devolvidas | espera média | espera mediana | espera máxima | pedido mais antigo | agendadas 12 m | anos de estoque | CID principais |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| USG TRANSVAGINAL | 02.05.02.018-6 | 1 | 0 | 1 | 0 | 3.968,2 | 3.968,2 | 3.968,2 | 21/12/2015 | — | — | Z00 1 |
| ULTRA-SONOGRAFIA DE MAMAS (BILATERAL) | 02.05.02.009-7 | 1 | 0 | 1 | 0 | 1.524,0 | 1.524,0 | 1.524,0 | 30/08/2022 | 0 | sem agendamento | N60 1 |
| ULTRA-SONOGRAFIA DOPPLER DE MAMAS | 02.05.02.009-7 | 1 | 0 | 1 | 0 | 1.523,9 | 1.523,9 | 1.523,9 | 30/08/2022 | 0 | sem agendamento | Z12 1 |
| ECOGRAFIA TRANSVAGINAL | 02.05.02.018-6 | 9.294 | 5.699 | 9.293 | 8.953 | 657,7 | 527,1 | 5.892,6 | 14/09/2010 | 18.028 | 0,5 | Z01 2.704, N95 1.210, R10 711 |
| ECOGRAFIA DE MAMAS - BILATERAL | 02.05.02.009-7 | 12.950 | 8.510 | 12.928 | 7.731 | 627,6 | 517,2 | 6.128,6 | 21/01/2010 | 10.474 | 1,2 | N63 3.381, Z12 2.707, N64 2.092 |

### mama e transvaginal: as 20 de mais anos de estoque

| fila | código | fila | fila viva | pessoas | devolvidas | espera média | espera mediana | espera máxima | pedido mais antigo | agendadas 12 m | anos de estoque | CID principais |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ULTRA-SONOGRAFIA DE MAMAS (BILATERAL) | 02.05.02.009-7 | 1 | 0 | 1 | 0 | 1.524,0 | 1.524,0 | 1.524,0 | 30/08/2022 | 0 | sem agendamento | N60 1 |
| ULTRA-SONOGRAFIA DOPPLER DE MAMAS | 02.05.02.009-7 | 1 | 0 | 1 | 0 | 1.523,9 | 1.523,9 | 1.523,9 | 30/08/2022 | 0 | sem agendamento | Z12 1 |
| ECOGRAFIA DE MAMAS - BILATERAL | 02.05.02.009-7 | 12.950 | 8.510 | 12.928 | 7.731 | 627,6 | 517,2 | 6.128,6 | 21/01/2010 | 10.474 | 1,2 | N63 3.381, Z12 2.707, N64 2.092 |
| ECOGRAFIA TRANSVAGINAL | 02.05.02.018-6 | 9.294 | 5.699 | 9.293 | 8.953 | 657,7 | 527,1 | 5.892,6 | 14/09/2010 | 18.028 | 0,5 | Z01 2.704, N95 1.210, R10 711 |

## Rumo por código

Um código por linha, com as filas do universo somadas (cada par nome × código uma vez). Tudo **calculado** no montador sobre a série mensal do motor (abas "Por código" da planilha). Os 12 meses fechados vão de 2025-10 a 2026-09, e os 12 de antes, de 2024-10 a 2025-09. Entrantes = pedidos abertos mais os já agendados, pelo mês do pedido. Oferta = agendamentos pelo mês em que acontecem, em todas as situações. Falta = faltas ÷ (realizados + faltas). Saldo por mês = (entrantes − oferta) ÷ 12: positivo, a fila cresce. Maior mês de oferta e média dos 3 últimos meses fechados, para ver o esforço que parou.

| código | fila mais pedida do código | fila | fila viva | devolvidas | entrantes 12 m | entrantes 12 m antes | oferta 12 m | oferta 12 m antes | saldo por mês | falta 12 m | maior mês de oferta | oferta média 3 últimos meses |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 02.05.02.009-7 | ECOGRAFIA DE MAMAS - BILATERAL | 12.952 | 8.510 | 7.731 | 10.961 | 9.871 | 9.776 | 4.884 | 98,8 | 38% | 2026-09 (2.821) | 1.777,3 |
| 02.05.02.018-6 | ECOGRAFIA TRANSVAGINAL | 9.295 | 5.699 | 8.953 | 15.123 | 14.063 | 17.599 | 10.016 | -206,3 | 43% | 2026-09 (2.210) | 2.063,7 |

## Oferta por unidade executante

Agendamentos pelo mês em que acontecem, por unidade que executa, em todas as situações. A média mensal é a dos seis meses fechados de 2025-10 a 2026-03; depois, mês a mês, com o mês corrente e o já agendado para depois. 
A última linha é a oferta do código no mesmo mês: o que passa da soma das unidades é agendamento sem unidade. As 25 unidades de maior oferta na janela; as outras, somadas. Planilha: aba "Por código executante".

### 02.05.02.009-7

| unidade executante | CNES | tipo | média mensal antes | 2026-04 | 2026-05 | 2026-06 | 2026-07 | 2026-08 | 2026-09 | 2026-10 | 2026-11 | 2026-12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| HRS | 0010502 | Região Norte | 0,0 | 0 | 0 | 0 | 0 | 1.012 | 1.186 | 17 | 0 | 0 |
| HRL | 2645157 | Região Leste | 45,5 | 24 | 64 | 33 | 14 | 65 | 65 | 313 | 578 | 2 |
| FHB | 0011339 | Serviços Centralizados | 0,0 | 0 | 0 | 0 | 0 | 0 | 718 | 276 | 0 | 0 |
| HMIB | 0010537 | URD | 118,5 | 132 | 90 | 86 | 144 | 160 | 48 | 56 | 32 | 0 |
| Cent Radiologia Tagua | 0011193 | Região Sudoeste | 45,0 | 52 | 97 | 32 | 50 | 31 | 67 | 212 | 22 | 0 |
| HRAN | 0010464 | Região Central | 27,3 | 20 | 48 | 12 | 50 | 136 | 200 | 0 | 0 | 0 |
| HRT | 0010499 | Região Sudoeste | 33,0 | 48 | 44 | 36 | 24 | 84 | 97 | 99 | 28 | 0 |
| HRPl | 0010529 | Região Norte | 27,7 | 24 | 26 | 20 | 24 | 23 | 231 | 81 | 2 | 0 |
| Policlínica Ceilândia II | 9578501 | Região Oeste | 0,0 | 0 | 0 | 0 | 240 | 0 | 0 | 127 | 50 | 0 |
| Hospital Dia | 0010596 | Região Central | 38,0 | 28 | 48 | 48 | 49 | 44 | 52 | 40 | 22 | 0 |
| HRG | 0010472 | Região Sul | 76,7 | 16 | 99 | 3 | 104 | 59 | 0 | 0 | 0 | 0 |
| Policlínica 514 Sul | 9580816 | Região Central | 34,8 | 48 | 17 | 28 | 13 | 52 | 51 | 31 | 1 | 0 |
| HRSam | 2672197 | Região Sudoeste | 25,3 | 24 | 26 | 38 | 34 | 22 | 29 | 16 | 0 | 0 |
| Policlínica Gama | 5598575 | Região Sul | 19,5 | 38 | 29 | 2 | 2 | 9 | 42 | 10 | 0 | 0 |
| HRC | 0010480 | Região Oeste | 19,3 | 0 | 0 | 0 | 5 | 25 | 25 | 20 | 10 | 0 |
| HRGu | 2814897 | Região Centro-Sul | 0,0 | 0 | 0 | 0 | 25 | 11 | 10 | 10 | 11 | 0 |
| **soma das unidades** |  |  | 510,7 | 454 | 588 | 338 | 778 | 1.733 | 2.821 | 1.308 | 756 | 2 |
| **oferta do código** |  |  | 510,7 | 454 | 588 | 338 | 778 | 1.733 | 2.821 | 1.308 | 756 | 2 |

### 02.05.02.018-6

| unidade executante | CNES | tipo | média mensal antes | 2026-04 | 2026-05 | 2026-06 | 2026-07 | 2026-08 | 2026-09 | 2026-10 | 2026-11 | 2026-12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| HRG | 0010472 | Região Sul | 19,2 | 40 | 145 | 715 | 1.095 | 480 | 9 | 10 | 0 | 0 |
| Cent Radiologia Tagua | 0011193 | Região Sudoeste | 239,3 | 283 | 353 | 185 | 132 | 267 | 252 | 441 | 38 | 0 |
| HRAN | 0010464 | Região Central | 133,0 | 84 | 90 | 50 | 90 | 725 | 640 | 96 | 0 | 0 |
| Policlínica Ceilândia II | 9578501 | Região Oeste | 0,0 | 0 | 0 | 243 | 400 | 0 | 58 | 404 | 106 | 0 |
| HRS | 0010502 | Região Norte | 59,8 | 100 | 84 | 85 | 129 | 131 | 444 | 160 | 15 | 0 |
| HRL | 2645157 | Região Leste | 35,8 | 213 | 82 | 38 | 53 | 36 | 59 | 139 | 439 | 0 |
| HRPl | 0010529 | Região Norte | 148,3 | 155 | 124 | 44 | 2 | 27 | 290 | 51 | 9 | 0 |
| HRC | 0010480 | Região Oeste | 243,5 | 85 | 84 | 168 | 105 | 57 | 25 | 75 | 39 | 0 |
| Hospital Dia | 0010596 | Região Central | 56,8 | 42 | 72 | 72 | 84 | 66 | 78 | 61 | 26 | 0 |
| FHB | 0011339 | Serviços Centralizados | 0,0 | 0 | 0 | 0 | 0 | 0 | 276 | 53 | 0 | 0 |
| Policlínica 514 Sul | 9580816 | Região Central | 30,8 | 44 | 16 | 25 | 12 | 48 | 48 | 32 | 0 | 0 |
| HRSam | 2672197 | Região Sudoeste | 15,5 | 18 | 18 | 24 | 18 | 24 | 30 | 0 | 6 | 0 |
| HRT | 0010499 | Região Sudoeste | 181,7 | 0 | 3 | 6 | 0 | 0 | 1 | 17 | 0 | 0 |
| HRGu | 2814897 | Região Centro-Sul | 44,0 | 18 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HRSM | 5717515 | Região Sul | 58,8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **soma das unidades** |  |  | 1.266,7 | 1.082 | 1.071 | 1.655 | 2.120 | 1.861 | 2.210 | 1.539 | 678 | 0 |
| **oferta do código** |  |  | 1.266,7 | 1.082 | 1.071 | 1.655 | 2.120 | 1.861 | 2.210 | 1.539 | 678 | — |

## Região de Saúde

Região de Saúde: não pedida na ordem.

## Diferença para a coleta anterior

Sem coleta anterior na pasta.
