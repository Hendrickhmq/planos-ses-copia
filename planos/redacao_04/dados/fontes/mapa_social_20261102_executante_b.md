# Mapa Social da Saúde — panorama: segunda leva do plano 4, coleta de 02/11/2026

Ordem de coleta: Estudo das filas de imagem do plano 4, segunda leva de executantes: quem atende hoje o ultrassom de globo ocular (oftalmologia, preço baixo), a ecocardiografia transtorácica (fila grande fora do plano 4) e a bolsa escrotal, mês a mês, para saber se a oferta é de oftalmologia ou de radiologia, se é mutirão e quem sustenta.

Coleta montada por `ferramentas/montar_coleta.py` a partir da saída do kit do motor: o modelo não escreveu número nenhum, e o resumo não se edita à mão (conferência K). A decisão de cada fila vem do enquadramento do plano.

| campo | conteúdo |
|---|---|
| Fonte | Mapa Social da Saúde – Regulamentação (MPDFT) · Lista de Espera – Exames e Consultas · `https://paineis-ext.mpdft.mp.br/extensions/mapasauderegulamentacao/mapasauderegulamentacao.html` · app Qlik `7edb02fa-f1f5-4ea6-b348-049a4ac2d095` · dados SISREG/DATASUS |
| Última recarga da base | 02/11/2026 16:31:31 (qLastReloadTime 2026-11-02T19:31:31.679Z) |
| Consulta | 02/11/2026 17:03:18 a 17:03:47 (relógio do motor), sem recarga no meio |
| Solicitação mais recente na base | 28/10/2026 (agendamento mais distante: 04/02/2027) |
| Medida | **fila** = os três status: pendente de regulação, corrigida e reenviada para regulação, pendente de regulação por fila de espera. Devolvidas para complementação ficam fora e são contadas à parte |
| Fila viva | só as solicitações a partir de `data_solicitacao={">=28/10/2024"}` (24 meses contados da solicitação mais recente) |
| Agendadas em 12 meses | `data_agendamento={">=28/10/2025<=27/10/2026"}`, todos os status |
| Ordem | panorama; `ordem.json` (hash 2241777300) |
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
| segunda leva do plano 4 | codigos: 02.05.02.008-9, 02.05.01.003-2, 02.05.02.007-0 | 12 | 16.879 | 16.536 | 16.799 |

## Varredura das filas (panorama)

Cada fila do universo (nome exato × código), sem decisão: o panorama só mostra. Anos de estoque = fila ÷ agendadas em 12 meses pelo mesmo nome e código (**calculado**).

### segunda leva do plano 4: por pessoas

| fila | código | fila | fila viva | pessoas | devolvidas | espera média | espera mediana | espera máxima | pedido mais antigo | agendadas 12 m | anos de estoque | CID principais |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1. ECOCARDIOGRAFIA BI-DIMENSIONAL COM DOPPLER ADULTO | 02.05.01.003-2 | 13.236 | 13.236 | 13.236 | 13.508 | 130,0 | 118,6 | 539,2 | 12/05/2025 | 33.920 | 0,4 | I10 2.420, I50 2.312, I25 1.155 |
| 2. ECOCARDIOGRAFIA BI-DIMENSIONAL COM DOPPLER INFANTIL | 02.05.01.003-2 | 1.332 | 1.332 | 1.331 | 2.564 | 112,5 | 105,2 | 720,0 | 12/11/2024 | 5.871 | 0,2 | R01 313, Q21 302, Q25 90 |
| ULTRA-SONOGRAFIA DO GLOBO OCULAR OU DE ORBITA | 02.05.02.008-9 | 1.316 | 1.316 | 1.316 | 198 | 272,7 | 277,8 | 509,1 | 11/06/2025 | 598 | 2,2 | H25 482, H35 129, H26 98 |
| ECOGRAFIA DE BOLSA ESCROTAL ADULTO | 02.05.02.007-0 | 700 | 428 | 700 | 430 | 604,9 | 523,1 | 2.105,2 | 27/01/2021 | 627 | 1,1 | N51 164, N43 91, K40 80 |
| ECOGRAFIA DE BOLSA ESCROTAL INFANTIL | 02.05.02.007-0 | 234 | 171 | 234 | 71 | 490,7 | 237,2 | 2.090,0 | 11/02/2021 | 316 | 0,7 | Q53 97, N43 49, K40 21 |
| 9. ECOCARDIOGRAFIA FETAL | 02.05.01.003-2 | 29 | 29 | 29 | 390 | 41,7 | 19,9 | 308,0 | 29/12/2025 | 788 | 0,0 | Z35 13, O24 2, Z34 2 |
| ULTRASSONOGRAFIA COM DOPPLER COLORIDO DA BOLSA ESCROTAL | 02.05.02.007-0 | 18 | 15 | 18 | 2 | 412,1 | 358,7 | 860,3 | 25/06/2024 | 0 | sem agendamento | N51 5, Q53 4, I86 2 |
| ULTRASSONOGRAFIA COM DOPPLER COLORIDO DOS TESTICULOS | 02.05.02.007-0 | 9 | 9 | 9 | 2 | 405,2 | 385,1 | 651,2 | 20/01/2025 | 1 | 9,0 | N51 6, E29 1, N49 1 |
| ECOCARDIOGRAFIA BI-DIMENSIONAL SEM DOPPLER ADULTO | 02.05.01.003-2 | 2 | 0 | 2 | 0 | 6.967,7 | 6.967,7 | 6.970,7 | 03/10/2007 | — | — | R68 2 |
| 16.ECOCARDIOGRAFIA TRANSTORACICA - INFANTIL | 02.05.01.003-2 | 1 | 0 | 1 | 0 | 4.948,9 | 4.948,9 | 4.948,9 | 15/04/2013 | 0 | sem agendamento | L81 1 |
| ECOCARDIOGRAFIA BI-DIMENSIONAL SEM DOPPLER ADULTO EMERGENCIA | 02.05.01.003-2 | 1 | 0 | 1 | 0 | 6.984,7 | 6.984,7 | 6.984,7 | 19/09/2007 | — | — | R68 1 |
| ECOCARDIOGRAFIA BI-DIMENSIONAL SEM DOPPLER INFANTIL | 02.05.01.003-2 | 1 | 0 | 1 | 0 | 6.978,7 | 6.978,7 | 6.978,7 | 25/09/2007 | — | — | R68 1 |

### segunda leva do plano 4: as 20 de maior espera média

| fila | código | fila | fila viva | pessoas | devolvidas | espera média | espera mediana | espera máxima | pedido mais antigo | agendadas 12 m | anos de estoque | CID principais |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ECOCARDIOGRAFIA BI-DIMENSIONAL SEM DOPPLER ADULTO EMERGENCIA | 02.05.01.003-2 | 1 | 0 | 1 | 0 | 6.984,7 | 6.984,7 | 6.984,7 | 19/09/2007 | — | — | R68 1 |
| ECOCARDIOGRAFIA BI-DIMENSIONAL SEM DOPPLER INFANTIL | 02.05.01.003-2 | 1 | 0 | 1 | 0 | 6.978,7 | 6.978,7 | 6.978,7 | 25/09/2007 | — | — | R68 1 |
| ECOCARDIOGRAFIA BI-DIMENSIONAL SEM DOPPLER ADULTO | 02.05.01.003-2 | 2 | 0 | 2 | 0 | 6.967,7 | 6.967,7 | 6.970,7 | 03/10/2007 | — | — | R68 2 |
| 16.ECOCARDIOGRAFIA TRANSTORACICA - INFANTIL | 02.05.01.003-2 | 1 | 0 | 1 | 0 | 4.948,9 | 4.948,9 | 4.948,9 | 15/04/2013 | 0 | sem agendamento | L81 1 |
| ECOGRAFIA DE BOLSA ESCROTAL ADULTO | 02.05.02.007-0 | 700 | 428 | 700 | 430 | 604,9 | 523,1 | 2.105,2 | 27/01/2021 | 627 | 1,1 | N51 164, N43 91, K40 80 |
| ECOGRAFIA DE BOLSA ESCROTAL INFANTIL | 02.05.02.007-0 | 234 | 171 | 234 | 71 | 490,7 | 237,2 | 2.090,0 | 11/02/2021 | 316 | 0,7 | Q53 97, N43 49, K40 21 |
| ULTRASSONOGRAFIA COM DOPPLER COLORIDO DA BOLSA ESCROTAL | 02.05.02.007-0 | 18 | 15 | 18 | 2 | 412,1 | 358,7 | 860,3 | 25/06/2024 | 0 | sem agendamento | N51 5, Q53 4, I86 2 |
| ULTRASSONOGRAFIA COM DOPPLER COLORIDO DOS TESTICULOS | 02.05.02.007-0 | 9 | 9 | 9 | 2 | 405,2 | 385,1 | 651,2 | 20/01/2025 | 1 | 9,0 | N51 6, E29 1, N49 1 |
| ULTRA-SONOGRAFIA DO GLOBO OCULAR OU DE ORBITA | 02.05.02.008-9 | 1.316 | 1.316 | 1.316 | 198 | 272,7 | 277,8 | 509,1 | 11/06/2025 | 598 | 2,2 | H25 482, H35 129, H26 98 |
| 1. ECOCARDIOGRAFIA BI-DIMENSIONAL COM DOPPLER ADULTO | 02.05.01.003-2 | 13.236 | 13.236 | 13.236 | 13.508 | 130,0 | 118,6 | 539,2 | 12/05/2025 | 33.920 | 0,4 | I10 2.420, I50 2.312, I25 1.155 |
| 2. ECOCARDIOGRAFIA BI-DIMENSIONAL COM DOPPLER INFANTIL | 02.05.01.003-2 | 1.332 | 1.332 | 1.331 | 2.564 | 112,5 | 105,2 | 720,0 | 12/11/2024 | 5.871 | 0,2 | R01 313, Q21 302, Q25 90 |
| 9. ECOCARDIOGRAFIA FETAL | 02.05.01.003-2 | 29 | 29 | 29 | 390 | 41,7 | 19,9 | 308,0 | 29/12/2025 | 788 | 0,0 | Z35 13, O24 2, Z34 2 |

### segunda leva do plano 4: as 20 de mais anos de estoque

| fila | código | fila | fila viva | pessoas | devolvidas | espera média | espera mediana | espera máxima | pedido mais antigo | agendadas 12 m | anos de estoque | CID principais |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 16.ECOCARDIOGRAFIA TRANSTORACICA - INFANTIL | 02.05.01.003-2 | 1 | 0 | 1 | 0 | 4.948,9 | 4.948,9 | 4.948,9 | 15/04/2013 | 0 | sem agendamento | L81 1 |
| ULTRASSONOGRAFIA COM DOPPLER COLORIDO DA BOLSA ESCROTAL | 02.05.02.007-0 | 18 | 15 | 18 | 2 | 412,1 | 358,7 | 860,3 | 25/06/2024 | 0 | sem agendamento | N51 5, Q53 4, I86 2 |
| ULTRASSONOGRAFIA COM DOPPLER COLORIDO DOS TESTICULOS | 02.05.02.007-0 | 9 | 9 | 9 | 2 | 405,2 | 385,1 | 651,2 | 20/01/2025 | 1 | 9,0 | N51 6, E29 1, N49 1 |
| ULTRA-SONOGRAFIA DO GLOBO OCULAR OU DE ORBITA | 02.05.02.008-9 | 1.316 | 1.316 | 1.316 | 198 | 272,7 | 277,8 | 509,1 | 11/06/2025 | 598 | 2,2 | H25 482, H35 129, H26 98 |
| ECOGRAFIA DE BOLSA ESCROTAL ADULTO | 02.05.02.007-0 | 700 | 428 | 700 | 430 | 604,9 | 523,1 | 2.105,2 | 27/01/2021 | 627 | 1,1 | N51 164, N43 91, K40 80 |
| ECOGRAFIA DE BOLSA ESCROTAL INFANTIL | 02.05.02.007-0 | 234 | 171 | 234 | 71 | 490,7 | 237,2 | 2.090,0 | 11/02/2021 | 316 | 0,7 | Q53 97, N43 49, K40 21 |
| 1. ECOCARDIOGRAFIA BI-DIMENSIONAL COM DOPPLER ADULTO | 02.05.01.003-2 | 13.236 | 13.236 | 13.236 | 13.508 | 130,0 | 118,6 | 539,2 | 12/05/2025 | 33.920 | 0,4 | I10 2.420, I50 2.312, I25 1.155 |
| 2. ECOCARDIOGRAFIA BI-DIMENSIONAL COM DOPPLER INFANTIL | 02.05.01.003-2 | 1.332 | 1.332 | 1.331 | 2.564 | 112,5 | 105,2 | 720,0 | 12/11/2024 | 5.871 | 0,2 | R01 313, Q21 302, Q25 90 |
| 9. ECOCARDIOGRAFIA FETAL | 02.05.01.003-2 | 29 | 29 | 29 | 390 | 41,7 | 19,9 | 308,0 | 29/12/2025 | 788 | 0,0 | Z35 13, O24 2, Z34 2 |

## Rumo por código

Um código por linha, com as filas do universo somadas (cada par nome × código uma vez). Tudo **calculado** no montador sobre a série mensal do motor (abas "Por código" da planilha). Os 12 meses fechados vão de 2025-10 a 2026-09, e os 12 de antes, de 2024-10 a 2025-09. Entrantes = pedidos abertos mais os já agendados, pelo mês do pedido. Oferta = agendamentos pelo mês em que acontecem, em todas as situações. Falta = faltas ÷ (realizados + faltas). Saldo por mês = (entrantes − oferta) ÷ 12: positivo, a fila cresce. Maior mês de oferta e média dos 3 últimos meses fechados, para ver o esforço que parou.

| código | fila mais pedida do código | fila | fila viva | devolvidas | entrantes 12 m | entrantes 12 m antes | oferta 12 m | oferta 12 m antes | saldo por mês | falta 12 m | maior mês de oferta | oferta média 3 últimos meses |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 02.05.01.003-2 | 1. ECOCARDIOGRAFIA BI-DIMENSIONAL COM DOPPLER ADULTO | 14.602 | 14.597 | 16.462 | 42.979 | 42.338 | 40.371 | 40.157 | 217,3 | 26% | 2024-10 (3.783) | 3.571,0 |
| 02.05.02.008-9 | ULTRA-SONOGRAFIA DO GLOBO OCULAR OU DE ORBITA | 1.316 | 1.316 | 198 | 917 | 1.115 | 588 | 252 | 27,4 | 48% | 2026-06 (140) | 63,3 |
| 02.05.02.007-0 | ECOGRAFIA DE BOLSA ESCROTAL ADULTO | 961 | 623 | 505 | 1.136 | 1.184 | 834 | 968 | 25,2 | 35% | 2026-05 (132) | 60,7 |

## Oferta por unidade executante

Agendamentos pelo mês em que acontecem, por unidade que executa, em todas as situações. A média mensal é a dos seis meses fechados de 2025-10 a 2026-03; depois, mês a mês, com o mês corrente e o já agendado para depois. 
A última linha é a oferta do código no mesmo mês: o que passa da soma das unidades é agendamento sem unidade. As 25 unidades de maior oferta na janela; as outras, somadas. Planilha: aba "Por código executante".

### 02.05.01.003-2

| unidade executante | CNES | tipo | média mensal antes | 2026-04 | 2026-05 | 2026-06 | 2026-07 | 2026-08 | 2026-09 | 2026-10 | 2026-11 | 2026-12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ICDF | 3276678 | Contratado/Credenciado | 1.944,2 | 1.698 | 2.051 | 1.904 | 2.023 | 1.944 | 1.905 | 1.930 | 1.505 | 3 |
| CRDF | 3044432 | URD | 460,3 | 518 | 546 | 575 | 580 | 605 | 727 | 459 | 372 | 0 |
| HBDF | 0010456 | URD | 426,8 | 494 | 462 | 510 | 481 | 511 | 451 | 381 | 97 | 0 |
| HUB | 0010510 | Contratado/Credenciado | 256,7 | 263 | 244 | 299 | 269 | 252 | 388 | 301 | 255 | 0 |
| HMIB | 0010537 | URD | 106,5 | 129 | 146 | 96 | 93 | 113 | 160 | 98 | 35 | 0 |
| HCB | 6876617 | URD | 59,0 | 76 | 72 | 54 | 52 | 60 | 99 | 53 | 72 | 6 |
| **soma das unidades** |  |  | 3.253,5 | 3.178 | 3.521 | 3.438 | 3.498 | 3.485 | 3.730 | 3.222 | 2.336 | 9 |
| **oferta do código** |  |  | 3.253,5 | 3.178 | 3.521 | 3.438 | 3.498 | 3.485 | 3.730 | 3.222 | 2.336 | 9 |

### 02.05.02.007-0

| unidade executante | CNES | tipo | média mensal antes | 2026-04 | 2026-05 | 2026-06 | 2026-07 | 2026-08 | 2026-09 | 2026-10 | 2026-11 | 2026-12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| HRL | 2645157 | Região Leste | 7,5 | 10 | 3 | 6 | 0 | 3 | 0 | 177 | 44 | 0 |
| HRG | 0010472 | Região Sul | 4,7 | 9 | 61 | 31 | 2 | 6 | 0 | 0 | 0 | 0 |
| HRS | 0010502 | Região Norte | 4,8 | 10 | 2 | 7 | 22 | 15 | 9 | 12 | 0 | 0 |
| Cent Radiologia Tagua | 0011193 | Região Sudoeste | 3,3 | 9 | 6 | 3 | 12 | 12 | 8 | 2 | 0 | 0 |
| HRAN | 0010464 | Região Central | 5,8 | 10 | 8 | 8 | 4 | 6 | 8 | 6 | 0 | 0 |
| HRBz | 0010545 | Região Oeste | 6,5 | 0 | 39 | 7 | 0 | 0 | 0 | 0 | 0 | 0 |
| HRC | 0010480 | Região Oeste | 3,5 | 0 | 1 | 16 | 12 | 3 | 14 | 0 | 0 | 0 |
| HRPl | 0010529 | Região Norte | 9,3 | 10 | 6 | 7 | 6 | 2 | 7 | 2 | 4 | 0 |
| HRSam | 2672197 | Região Sudoeste | 4,5 | 0 | 4 | 3 | 12 | 3 | 8 | 2 | 0 | 0 |
| HRGu | 2814897 | Região Centro-Sul | 1,3 | 2 | 2 | 2 | 0 | 1 | 6 | 4 | 6 | 0 |
| HRSM | 5717515 | Região Sul | 8,8 | 9 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| FHB | 0011339 | Serviços Centralizados | 0,0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| Policlínica 514 Sul | 9580816 | Região Central | 0,0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **soma das unidades** |  |  | 60,2 | 69 | 132 | 90 | 70 | 51 | 61 | 205 | 54 | 0 |
| **oferta do código** |  |  | 60,2 | 69 | 132 | 90 | 70 | 51 | 61 | 205 | 54 | — |

### 02.05.02.008-9

| unidade executante | CNES | tipo | média mensal antes | 2026-04 | 2026-05 | 2026-06 | 2026-07 | 2026-08 | 2026-09 | 2026-10 | 2026-11 | 2026-12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CRDF | 3044432 | URD | 20,0 | 28 | 110 | 140 | 30 | 102 | 58 | 50 | 0 | 0 |
| **soma das unidades** |  |  | 20,0 | 28 | 110 | 140 | 30 | 102 | 58 | 50 | 0 | 0 |
| **oferta do código** |  |  | 20,0 | 28 | 110 | 140 | 30 | 102 | 58 | 50 | — | — |

## Região de Saúde

Região de Saúde: não pedida na ordem.

## Diferença para a coleta anterior

Contra `dados/fontes/mapa_social_20261102_imagem_bruto/coleta_20261102.json` (recarga 02/11/2026 10:31:47). Diferença **calculada** no montador.

A coleta anterior não tem as mesmas filas nem os mesmos objetos.
