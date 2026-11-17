# Mapa Social da Saúde — panorama: candidatos do plano 4, coleta de 02/11/2026

Ordem de coleta: Estudo das filas de imagem para decidir o plano 4: quem sustenta a oferta (unidade executante por mês) nos códigos candidatos de rumo inconclusivo ou de maior peso — abdômen total, Doppler, TC de tórax, de abdômen superior e de pelve.

Coleta montada por `ferramentas/montar_coleta.py` a partir da saída do kit do motor: o modelo não escreveu número nenhum, e o resumo não se edita à mão (conferência K). A decisão de cada fila vem do enquadramento do plano.

| campo | conteúdo |
|---|---|
| Fonte | Mapa Social da Saúde – Regulamentação (MPDFT) · Lista de Espera – Exames e Consultas · `https://paineis-ext.mpdft.mp.br/extensions/mapasauderegulamentacao/mapasauderegulamentacao.html` · app Qlik `7edb02fa-f1f5-4ea6-b348-049a4ac2d095` · dados SISREG/DATASUS |
| Última recarga da base | 02/11/2026 10:31:47 (qLastReloadTime 2026-11-02T13:31:47.865Z) |
| Consulta | 02/11/2026 12:30:34 a 12:30:55 (relógio do motor), sem recarga no meio |
| Solicitação mais recente na base | 28/10/2026 (agendamento mais distante: 04/02/2027) |
| Medida | **fila** = os três status: pendente de regulação, corrigida e reenviada para regulação, pendente de regulação por fila de espera. Devolvidas para complementação ficam fora e são contadas à parte |
| Fila viva | só as solicitações a partir de `data_solicitacao={">=28/10/2024"}` (24 meses contados da solicitação mais recente) |
| Agendadas em 12 meses | `data_agendamento={">=28/10/2025<=27/10/2026"}`, todos os status |
| Ordem | panorama; `ordem.json` (hash 2175197108) |
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
| candidatos do plano 4 | codigos: 02.05.02.004-6, 02.05.01.004-0, 02.06.02.003-1, 02.06.03.001-0, 02.06.03.003-7 | 83 | 47.800 | 39.138 | 36.919 |

## Varredura das filas (panorama)

Cada fila do universo (nome exato × código), sem decisão: o panorama só mostra. Anos de estoque = fila ÷ agendadas em 12 meses pelo mesmo nome e código (**calculado**).

### candidatos do plano 4: por pessoas

| fila | código | fila | fila viva | pessoas | devolvidas | espera média | espera mediana | espera máxima | pedido mais antigo | agendadas 12 m | anos de estoque | CID principais |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ULTRA-SONOGRAFIA DOPPLER VENOSO - MMII ( BILATERAL) | 02.05.01.004-0 | 10.045 | 6.060 | 10.043 | 599 | 630,9 | 577,8 | 1.476,9 | 17/10/2022 | 3.496 | 2,9 | I83 5.333, I87 2.042, I82 577 |
| ECOGRAFIA DE ABDOMEN TOTAL ADULTO | 02.05.02.004-6 | 9.895 | 7.386 | 9.890 | 11.564 | 553,9 | 356,6 | 6.124,4 | 26/01/2010 | 8.207 | 1,2 | R10 3.302, K76 1.277, K80 725 |
| 10. ECODOPPLER DE CAROTIDAS | 02.05.01.004-0 | 4.143 | 4.143 | 4.143 | 2.776 | 136,3 | 124,7 | 592,0 | 20/03/2025 | 8.258 | 0,5 | I10 944, I25 419, I50 419 |
| 063. TC DO ABDOMEN SUPERIOR ADULTO C/CONTRASTE S/SEDACAO | 02.06.03.001-0 | 4.116 | 4.101 | 4.112 | 5.271 | 129,2 | 126,0 | 850,0 | 05/07/2024 | 8.164 | 0,5 | C50 762, C18 388, R10 321 |
| 111. TC DE PELVE OU BACIA ADULTO C/CONTRASTE S/SEDACAO | 02.06.03.003-7 | 3.639 | 3.629 | 3.637 | 3.718 | 128,7 | 129,7 | 850,0 | 05/07/2024 | 7.036 | 0,5 | C50 613, C18 361, R10 305 |
| ULTRASONOGRAFIA DE PAREDE ABDOMINAL | 02.05.02.004-6 | 3.304 | 2.199 | 3.304 | 1.278 | 598,3 | 507,8 | 2.452,6 | 14/02/2020 | 1.470 | 2,2 | K42 870, K40 842, K46 486 |
| 055. TC DO TORAX ADULTO C/CONTRASTE S/SEDACAO | 02.06.02.003-1 | 2.350 | 2.341 | 2.348 | 1.864 | 132,1 | 130,7 | 966,0 | 11/03/2024 | 5.981 | 0,4 | C50 557, C18 247, C20 123 |
| ULTRA-SONOGRAFIA DOPPLER ARTERIAL - MMII (BILATERAL) | 02.05.01.004-0 | 1.800 | 1.358 | 1.800 | 331 | 474,7 | 396,0 | 1.442,0 | 21/11/2022 | 519 | 3,5 | I70 398, I83 379, I73 356 |
| ANGIOTOMOGRAFIA DAS ARTÉRIAS CORONARIAS ADULTO S/SEDACAO | 02.06.02.003-1 | 1.532 | 1.531 | 1.532 | 138 | 292,6 | 265,1 | 747,8 | 15/10/2024 | 137 | 11,2 | I20 447, I25 410, R07 128 |
| TC DO TORAX ADULTO S/CONTRASTE S/SEDACAO EMERGENCIA | 02.06.02.003-1 | 895 | 857 | 895 | 79 | 355,6 | 333,0 | 3.617,7 | 06/12/2016 | 1.983 | 0,5 | J18 178, I25 75, J44 43 |
| TC DO ABDOMEN SUPER.ADULTO C/CONTRASTE S/SEDACAO EMERG. | 02.06.03.001-0 | 726 | 696 | 726 | 85 | 363,9 | 363,0 | 766,0 | 27/09/2024 | 1.516 | 0,5 | R10 158, C50 33, C18 33 |
| TC DE PELVE OU BACIA ADULTO C/CONTRASTE S/SEDACAO EMERG. | 02.06.03.003-7 | 674 | 645 | 674 | 68 | 356,0 | 339,8 | 765,8 | 27/09/2024 | 1.328 | 0,5 | R10 133, Z54 33, C18 30 |
| ECOGRAFIA DE ABDOMEN TOTAL INFANTIL | 02.05.02.004-6 | 452 | 286 | 452 | 433 | 586,1 | 349,7 | 2.079,0 | 22/02/2021 | 1.067 | 0,4 | R10 178, E66 75, Q90 16 |
| TC DO ABDOMEN SUPER.ADULTO S/CONTRASTE S/SEDACAO EMERG. | 02.06.03.001-0 | 393 | 380 | 393 | 69 | 370,8 | 361,8 | 3.617,7 | 06/12/2016 | 721 | 0,5 | R10 105, N20 23, Z54 13 |
| TC DE PELVE OU BACIA ADULTO S/CONTRASTE S/SEDACAO EMERG. | 02.06.03.003-7 | 370 | 356 | 370 | 65 | 372,6 | 357,1 | 3.617,7 | 06/12/2016 | 658 | 0,6 | R10 93, N20 15, Z54 13 |
| ANGIOTOMOGRAFIA DA AORTA TORÁCICA E SEUS RAMOS ADULTO S/SEDACAO | 02.06.02.003-1 | 357 | 357 | 357 | 176 | 200,1 | 173,7 | 543,6 | 07/05/2025 | 653 | 0,5 | I71 173, I35 46, I50 16 |
| ANGIOTOMOGRAFIA DO TORAX OU PULMONAR ADULTO S/SEDACAO | 02.06.02.003-1 | 328 | 328 | 328 | 596 | 134,1 | 110,8 | 544,7 | 06/05/2025 | 1.311 | 0,3 | I26 121, I71 36, I27 23 |
| ANGIOTOMOGRAFIA DA AORTA ABDOMINAL E DOS SEUS RAMOS ADULTO S/SEDACAO | 02.06.03.001-0 | 323 | 323 | 323 | 145 | 199,1 | 171,0 | 474,8 | 15/07/2025 | 605 | 0,5 | I71 141, I70 26, I35 24 |
| TC DO TORAX ADULTO C/CONTRASTE S/SEDACAO EMERGENCIA | 02.06.02.003-1 | 305 | 292 | 305 | 30 | 360,6 | 336,0 | 767,4 | 26/09/2024 | 979 | 0,3 | I26 19, C50 18, J18 14 |
| ANGIOTOMOGRAFIA DA PELVE ADULTO S/SEDACAO | 02.06.03.003-7 | 253 | 253 | 253 | 142 | 218,3 | 181,9 | 473,0 | 17/07/2025 | 330 | 0,8 | N18 40, I82 39, I71 37 |
| ANGIOTOMOGRAFIA DO ABDOME SUPERIOR ADULTO S/SEDACAO | 02.06.03.001-0 | 245 | 245 | 245 | 130 | 219,8 | 187,8 | 543,6 | 07/05/2025 | 309 | 0,8 | I71 46, N18 36, K55 20 |
| ANGIOTOMOGRAFIA DAS ARTERIAS CAROTIDAS E VERTEBRAIS ADULTO S/SEDACAO | 02.06.03.001-0 | 243 | 243 | 243 | 130 | 134,6 | 121,7 | 439,8 | 19/08/2025 | 541 | 0,4 | I65 76, I64 33, I63 25 |
| ULTRA-SONOGRAFIA DOPPLER DE CAROTIDAS E VERTEBRAIS | 02.05.01.004-0 | 190 | 19 | 190 | 26 | 971,1 | 942,5 | 1.362,7 | 08/02/2023 | 0 | sem agendamento | I10 71, E11 23, E78 21 |
| 053. TC DO TORAX ADULTO S/CONTRASTE S/SEDACAO | 02.06.02.003-1 | 180 | 177 | 180 | 2.167 | 36,7 | 6,8 | 1.056,9 | 11/12/2023 | 18.474 | 0,0 | C50 25, J44 16, R91 12 |
| ULTRA-SONOGRAFIA DOPPLER COLORIDO DE VASOS | 02.05.01.004-0 | 169 | 169 | 169 | 0 | 30,6 | 34,0 | 60,7 | 02/09/2026 | — | — | I83 56, I87 25, M79 8 |
| ULTRA-SONOGRAFIA DOPPLER VENOSO - MMSS ( BILATERAL) | 02.05.01.004-0 | 144 | 139 | 144 | 207 | 164,8 | 113,3 | 866,0 | 19/06/2024 | 100 | 1,4 | I83 39, I87 23, I82 17 |
| ECOGRAFIA TRANSVAGINAL COM DOPPLER | 02.05.01.004-0 | 133 | 89 | 133 | 151 | 562,7 | 419,1 | 1.397,0 | 05/01/2023 | 140 | 0,9 | Z01 21, N95 17, R10 14 |
| ULTRASSONOGRAFIA COM DOPPLER COLORIDO DE ARTERIAS RENAIS | 02.05.01.004-0 | 92 | 92 | 92 | 5 | 199,0 | 166,9 | 514,9 | 05/06/2025 | 16 | 5,8 | I10 37, I15 22, N18 15 |
| 061. TC DO ABDOMEN SUPERIOR ADULTO S/CONTRASTE S/SEDACAO | 02.06.03.001-0 | 68 | 68 | 68 | 1.489 | 18,8 | 6,7 | 221,8 | 25/03/2026 | 5.496 | 0,0 | N20 22, R10 15, N18 3 |
| 109. TC DE PELVE OU BACIA ADULTO S/CONTRASTE S/SEDACAO | 02.06.03.003-7 | 57 | 57 | 57 | 952 | 21,1 | 6,7 | 278,8 | 27/01/2026 | 5.469 | 0,0 | N20 18, R10 13, N18 3 |
| ULTRA-SONOGRAFIA DOPPLER ARTERIAL - MMSS (BILATERAL) | 02.05.01.004-0 | 54 | 52 | 54 | 85 | 248,7 | 266,9 | 786,8 | 06/09/2024 | 92 | 0,6 | I25 5, I77 5, N18 5 |
| TC DO TORAX INFANTIL S/CONTRASTE S/SEDACAO EMERGENCIA | 02.06.02.003-1 | 44 | 43 | 44 | 0 | 343,4 | 389,4 | 759,8 | 03/10/2024 | 8 | 5,5 | J18 14, P27 4, J15 4 |
| ANGIOTOMOGRAFIA DAS ARTÉRIAS RENAIS ADULTO S/SEDACAO | 02.06.03.001-0 | 36 | 36 | 36 | 11 | 160,1 | 132,4 | 429,8 | 29/08/2025 | 47 | 0,8 | I15 15, I10 4, I77 3 |
| TC DO ABDOMEN SUPER.INFANTIL C/CONTRASTE S/SEDACAO EMERG. | 02.06.03.001-0 | 33 | 33 | 33 | 1 | 349,2 | 313,9 | 725,0 | 07/11/2024 | 16 | 2,1 | R10 9, R16 2, A41 2 |
| TC DE PELVE OU BACIA INFANTIL C/CONTRASTE S/SEDACAO EMERG. | 02.06.03.003-7 | 31 | 30 | 31 | 3 | 347,6 | 314,9 | 754,7 | 08/10/2024 | 18 | 1,7 | R10 6, C34 2, C18 2 |
| TC DO TORAX INFANTIL C/CONTRASTE S/SEDACAO EMERGENCIA | 02.06.02.003-1 | 23 | 23 | 23 | 0 | 344,0 | 335,0 | 725,8 | 06/11/2024 | 11 | 2,1 | J18 8, R10 3, C38 1 |
| TC DE PELVE OU BACIA INFANTIL S/CONTRASTE S/SEDACAO EMERG. | 02.06.03.003-7 | 15 | 15 | 15 | 1 | 463,0 | 522,8 | 674,8 | 27/12/2024 | 9 | 1,7 | R10 3, N20 1, C16 1 |
| TC DO ABDOMEN SUPER.INFANTIL S/CONTRASTE S/SEDACAO EMERG. | 02.06.03.001-0 | 13 | 12 | 13 | 0 | 385,7 | 363,7 | 762,0 | 01/10/2024 | 12 | 1,1 | R50 2, I25 1, N39 1 |
| ANGIOTOMOGRAFIA DO SISTEMA PORTA (VASOS HEPÁTICOS) ADULTO S/SEDACAO | 02.06.03.001-0 | 12 | 12 | 12 | 8 | 228,9 | 197,9 | 425,9 | 02/09/2025 | 10 | 1,2 | I82 4, I81 4, I83 1 |
| ANGIOTOMOGRAFIA DAS ARTÉRIAS CORONARIAS INFANTIL S/SEDACAO | 02.06.02.003-1 | 12 | 12 | 12 | 4 | 266,6 | 225,4 | 640,0 | 31/01/2025 | — | — | Q24 4, Q25 3, I25 1 |
| ULTRA-SONOGRAFIA DOPPLER DE AORTA E VASOS ILIACOS | 02.05.01.004-0 | 11 | 11 | 11 | 1 | 55,2 | 62,8 | 81,0 | 13/08/2026 | 20 | 0,6 | N18 3, I25 1, E88 1 |
| ULTRA-SONOGRAFIA DOPPLER VENOSO - MIE | 02.05.01.004-0 | 10 | 0 | 10 | 439 | 1.608,4 | 1.592,0 | 1.873,7 | 15/09/2021 | 0 | sem agendamento | I83 8, M79 1, G83 1 |
| ANGIOTOMOGRAFIA DA AORTA TORÁCICA E SEUS RAMOS INFANTIL S/SEDACAO | 02.06.02.003-1 | 9 | 9 | 9 | 10 | 162,1 | 95,8 | 459,0 | 31/07/2025 | 14 | 0,6 | Q25 5, I10 1, I71 1 |
| ULTRA-SONOGRAFIA DOPPLER VENOSO - MID | 02.05.01.004-0 | 8 | 0 | 8 | 483 | 1.568,1 | 1.536,7 | 1.703,8 | 04/03/2022 | 0 | sem agendamento | I83 5, I87 2, G63 1 |
| ULTRA-SONOGRAFIA DOPPLER DE ARTERIA AORTA ABDOMINAL | 02.05.01.004-0 | 5 | 5 | 5 | 3 | 35,3 | 32,0 | 52,7 | 10/09/2026 | 16 | 0,3 | I25 2, E66 1, I71 1 |
| ULTRASSONOGRAFIA DAS GLANDULAS PAROTIDAS | 02.05.01.004-0 | 5 | 5 | 5 | 2 | 80,7 | 81,8 | 81,8 | 12/08/2026 | 18 | 0,3 | K11 2, D11 1, Q76 1 |
| ULTRA-SONOGRAFIA DOPPLER DE CAROTIDAS E VERTEBRAIS | 02.05.01.004-0 | 4 | 0 | 4 | 17 | 1.667,9 | 1.668,0 | 1.700,8 | 07/03/2022 | 0 | sem agendamento | E14 1, E78 1, I10 1 |
| ANGIOTOMOGRAFIA | 02.06.02.003-1 | 3 | 3 | 3 | 0 | 10,2 | 8,7 | 13,9 | 19/10/2026 | 268 | 0,0 | I26 2, I25 1 |
| ULTRA-SONOGRAFIA DOPPLER COLORIDO DE UM VASO | 02.05.01.004-0 | 3 | 0 | 3 | 2 | 1.524,9 | 1.525,0 | 1.525,1 | 30/08/2022 | 0 | sem agendamento | N18 2, I73 1 |
| ULTRA-SONOGRAFIA DE ABDOMEN TOTAL | 02.05.02.004-6 | 3 | 0 | 3 | 1 | 1.524,8 | 1.524,9 | 1.524,9 | 30/08/2022 | 0 | sem agendamento | Z10 1, C44 1, R10 1 |
| ULTRA-SONOGRAFIA DOPPLER ARTERIAL-M I D | 02.05.01.004-0 | 3 | 0 | 3 | 0 | 1.536,0 | 1.524,8 | 1.558,4 | 27/07/2022 | 0 | sem agendamento | L98 1, M79 1, I73 1 |
| ULTRA-SONOGRAFIA DOPPLER VENOSO - MID | 02.05.01.004-0 | 3 | 0 | 3 | 0 | 1.536,0 | 1.524,8 | 1.558,4 | 27/07/2022 | 0 | sem agendamento | L98 1, M79 1, I73 1 |
| 051. TC DO TORAX INFANTIL C/CONTRASTE S/SEDACAO | 02.06.02.003-1 | 2 | 2 | 2 | 52 | 328,5 | 328,5 | 646,0 | 25/01/2025 | 58 | 0,0 | D21 1, C18 1 |
| ANGIOTOMOGRAFIA DA AORTA ABDOMINAL E DOS SEUS RAMOS INFANTIL S/SEDACAO | 02.06.03.001-0 | 2 | 2 | 2 | 2 | 309,3 | 309,3 | 319,8 | 17/12/2025 | 3 | 0,7 | N39 1, I70 1 |
| ANGIOTOMOGRAFIA DO TORAX OU PULMONAR INFANTIL S/SEDACAO | 02.06.02.003-1 | 2 | 2 | 2 | 7 | 135,8 | 135,8 | 265,7 | 09/02/2026 | 19 | 0,1 | Q24 1, Q21 1 |
| DOPPLER ARTERIAL DE MI | 02.05.01.004-0 | 2 | 0 | 2 | 0 | 1.524,7 | 1.524,7 | 1.524,8 | 30/08/2022 | 0 | sem agendamento | M79 1, I73 1 |
| DOPPLER VENOSO DE MI | 02.05.01.004-0 | 2 | 0 | 2 | 0 | 1.524,7 | 1.524,7 | 1.524,7 | 30/08/2022 | 0 | sem agendamento | M79 1, I73 1 |
| ULTRA-SONOGRAFIA DOPPLER ARTERIAL- M I D | 02.05.01.004-0 | 2 | 0 | 2 | 288 | 1.537,9 | 1.537,9 | 1.544,9 | 10/08/2022 | 0 | sem agendamento | Z10 1, I83 1 |
| ULTRA-SONOGRAFIA DOPPLER ARTERIAL- M I E | 02.05.01.004-0 | 2 | 0 | 2 | 246 | 1.522,7 | 1.518,6 | 1.530,8 | 24/08/2022 | 0 | sem agendamento | Z10 1, I83 1 |
| ULTRA-SONOGRAFIA DOPPLER DE ARTERIAS VERTEBRAIS | 02.05.01.004-0 | 2 | 0 | 2 | 0 | 1.446,7 | 1.446,7 | 1.479,7 | 14/10/2022 | — | — | I10 1, R42 1 |
| ULTRASSONOGRAFIA DOPPLER ARTERIAL MEMBRO SUPERIOR E | 02.05.01.004-0 | 2 | 0 | 2 | 0 | 1.525,0 | 1.525,0 | 1.525,1 | 30/08/2022 | 0 | sem agendamento | N18 2 |
| 049. TC DO TORAX INFANTIL S/CONTRASTE S/SEDACAO | 02.06.02.003-1 | 1 | 1 | 1 | 56 | 283,7 | 283,7 | 283,7 | 22/01/2026 | 153 | 0,0 | C56 1 |
| 059. TC DO ABDOMEN SUPERIOR INFANTIL C/CONTRASTE S/SEDACAO | 02.06.03.001-0 | 1 | 1 | 1 | 122 | 10,9 | 10,9 | 10,9 | 22/10/2026 | 98 | 0,0 | D21 1 |
| 060. TC DO ABDOMEN SUPERIOR INFANTIL C/CONTRASTE C/SEDACAO | 02.06.03.001-0 | 1 | 1 | 1 | 20 | 290,9 | 290,9 | 290,9 | 15/01/2026 | 21 | 0,0 | R50 1 |
| 064. TC DO ABDOMEN SUPERIOR ADULTO C/CONTRASTE C/SEDACAO | 02.06.03.001-0 | 1 | 1 | 1 | 238 | 223,1 | 223,1 | 223,1 | 24/03/2026 | 26 | 0,0 | N18 1 |
| 107. TC DE PELVE OU BACIA INFANTIL C/CONTRASTE S/SEDACAO | 02.06.03.003-7 | 1 | 1 | 1 | 138 | 10,9 | 10,9 | 10,9 | 22/10/2026 | 88 | 0,0 | D21 1 |
| 108. TC DE PELVE OU BACIA INFANTIL C/CONTRASTE C/SEDACAO | 02.06.03.003-7 | 1 | 1 | 1 | 13 | 290,9 | 290,9 | 290,9 | 15/01/2026 | 9 | 0,1 | R50 1 |
| 110. TC DE PELVE OU BACIA ADULTO S/CONTRASTE C/SEDACAO | 02.06.03.003-7 | 1 | 1 | 1 | 116 | 6,6 | 6,6 | 6,6 | 26/10/2026 | 13 | 0,1 | R10 1 |
| 112. TC DE PELVE OU BACIA ADULTO C/CONTRASTE C/SEDACAO | 02.06.03.003-7 | 1 | 1 | 1 | 219 | 646,0 | 646,0 | 646,0 | 25/01/2025 | 23 | 0,0 | C18 1 |
| ANGIOTOMOGRAFIA DA PELVE INFANTIL S/SEDACAO | 02.06.03.003-7 | 1 | 1 | 1 | 0 | 50,8 | 50,8 | 50,8 | 12/09/2026 | 1 | 1,0 | I80 1 |
| ANGIOTOMOGRAFIA DAS ARTÉRIAS RENAIS INFANTIL S/SEDACAO | 02.06.03.001-0 | 1 | 1 | 1 | 1 | 319,8 | 319,8 | 319,8 | 17/12/2025 | 2 | 0,5 | N39 1 |
| ECOGRAFIA DE ABDOMEN TOTAL ADULTO EMERGENCIA | 02.05.02.004-6 | 1 | 1 | 1 | 0 | 8,4 | 8,4 | 8,4 | 25/10/2026 | 0 | sem agendamento | R10 1 |
| ECOGRAFIA DOPPLER COLORIDO DE ORGAO | 02.05.01.004-0 | 1 | 1 | 1 | 2 | 142,7 | 142,7 | 142,7 | 12/06/2026 | — | — | I65 1 |
| ULTRA-SONOGRAFIA DOPPLER ARTERIAL- M S D | 02.05.01.004-0 | 1 | 0 | 1 | 30 | 1.643,7 | 1.643,7 | 1.643,7 | 03/05/2022 | 0 | sem agendamento | I83 1 |
| ULTRA-SONOGRAFIA DOPPLER COLORIDO DE DOIS VASOS | 02.05.01.004-0 | 1 | 0 | 1 | 12 | 1.700,0 | 1.700,0 | 1.700,0 | 08/03/2022 | — | — | I83 1 |
| ULTRA-SONOGRAFIA DOPPLER COLORIDO DE ORGAO OU ESTRUTURA ISO | 02.05.01.004-0 | 1 | 0 | 1 | 0 | 1.524,7 | 1.524,7 | 1.524,7 | 30/08/2022 | 0 | sem agendamento | I73 1 |
| ULTRA-SONOGRAFIA DOPPLER DE CAROTIDAS | 02.05.01.004-0 | 1 | 0 | 1 | 8 | 1.637,0 | 1.637,0 | 1.637,0 | 10/05/2022 | 0 | sem agendamento | I10 1 |
| ULTRA-SONOGRAFIA DE BOLSA ESCROTAL COM DOPPLER | 02.05.01.004-0 | 1 | 0 | 1 | 0 | 1.524,7 | 1.524,7 | 1.524,7 | 30/08/2022 | 0 | sem agendamento | E29 1 |
| ULTRA-SONOGRAFIA DE PAREDE ABDOMINAL | 02.05.02.004-6 | 1 | 0 | 1 | 0 | 1.524,8 | 1.524,8 | 1.524,8 | 30/08/2022 | 0 | sem agendamento | N18 1 |
| ULTRA-SONOGRAFIA DOPPLER - ARTERIAS RENAIS | 02.05.01.004-0 | 1 | 0 | 1 | 0 | 1.558,5 | 1.558,5 | 1.558,5 | 27/07/2022 | 0 | sem agendamento | I70 1 |
| ULTRA-SONOGRAFIA DOPPLER - CERVICAL | 02.05.01.004-0 | 1 | 0 | 1 | 0 | 1.382,7 | 1.382,7 | 1.382,7 | 19/01/2023 | 0 | sem agendamento | E04 1 |
| ULTRA-SONOGRAFIA DOPPLER ARTERIAL-M I E | 02.05.01.004-0 | 1 | 0 | 1 | 0 | 1.524,7 | 1.524,7 | 1.524,7 | 30/08/2022 | 0 | sem agendamento | I73 1 |
| ULTRA-SONOGRAFIA DOPPLER VENOSO - MIE | 02.05.01.004-0 | 1 | 0 | 1 | 0 | 1.524,7 | 1.524,7 | 1.524,7 | 30/08/2022 | 0 | sem agendamento | I73 1 |

### candidatos do plano 4: as 20 de maior espera média

| fila | código | fila | fila viva | pessoas | devolvidas | espera média | espera mediana | espera máxima | pedido mais antigo | agendadas 12 m | anos de estoque | CID principais |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ULTRA-SONOGRAFIA DOPPLER COLORIDO DE DOIS VASOS | 02.05.01.004-0 | 1 | 0 | 1 | 12 | 1.700,0 | 1.700,0 | 1.700,0 | 08/03/2022 | — | — | I83 1 |
| ULTRA-SONOGRAFIA DOPPLER DE CAROTIDAS E VERTEBRAIS | 02.05.01.004-0 | 4 | 0 | 4 | 17 | 1.667,9 | 1.668,0 | 1.700,8 | 07/03/2022 | 0 | sem agendamento | E14 1, E78 1, I10 1 |
| ULTRA-SONOGRAFIA DOPPLER ARTERIAL- M S D | 02.05.01.004-0 | 1 | 0 | 1 | 30 | 1.643,7 | 1.643,7 | 1.643,7 | 03/05/2022 | 0 | sem agendamento | I83 1 |
| ULTRA-SONOGRAFIA DOPPLER DE CAROTIDAS | 02.05.01.004-0 | 1 | 0 | 1 | 8 | 1.637,0 | 1.637,0 | 1.637,0 | 10/05/2022 | 0 | sem agendamento | I10 1 |
| ULTRA-SONOGRAFIA DOPPLER VENOSO - MIE | 02.05.01.004-0 | 10 | 0 | 10 | 439 | 1.608,4 | 1.592,0 | 1.873,7 | 15/09/2021 | 0 | sem agendamento | I83 8, M79 1, G83 1 |
| ULTRA-SONOGRAFIA DOPPLER VENOSO - MID | 02.05.01.004-0 | 8 | 0 | 8 | 483 | 1.568,1 | 1.536,7 | 1.703,8 | 04/03/2022 | 0 | sem agendamento | I83 5, I87 2, G63 1 |
| ULTRA-SONOGRAFIA DOPPLER - ARTERIAS RENAIS | 02.05.01.004-0 | 1 | 0 | 1 | 0 | 1.558,5 | 1.558,5 | 1.558,5 | 27/07/2022 | 0 | sem agendamento | I70 1 |
| ULTRA-SONOGRAFIA DOPPLER ARTERIAL- M I D | 02.05.01.004-0 | 2 | 0 | 2 | 288 | 1.537,9 | 1.537,9 | 1.544,9 | 10/08/2022 | 0 | sem agendamento | Z10 1, I83 1 |
| ULTRA-SONOGRAFIA DOPPLER ARTERIAL-M I D | 02.05.01.004-0 | 3 | 0 | 3 | 0 | 1.536,0 | 1.524,8 | 1.558,4 | 27/07/2022 | 0 | sem agendamento | L98 1, M79 1, I73 1 |
| ULTRA-SONOGRAFIA DOPPLER VENOSO - MID | 02.05.01.004-0 | 3 | 0 | 3 | 0 | 1.536,0 | 1.524,8 | 1.558,4 | 27/07/2022 | 0 | sem agendamento | L98 1, M79 1, I73 1 |
| ULTRASSONOGRAFIA DOPPLER ARTERIAL MEMBRO SUPERIOR E | 02.05.01.004-0 | 2 | 0 | 2 | 0 | 1.525,0 | 1.525,0 | 1.525,1 | 30/08/2022 | 0 | sem agendamento | N18 2 |
| ULTRA-SONOGRAFIA DOPPLER COLORIDO DE UM VASO | 02.05.01.004-0 | 3 | 0 | 3 | 2 | 1.524,9 | 1.525,0 | 1.525,1 | 30/08/2022 | 0 | sem agendamento | N18 2, I73 1 |
| ULTRA-SONOGRAFIA DE ABDOMEN TOTAL | 02.05.02.004-6 | 3 | 0 | 3 | 1 | 1.524,8 | 1.524,9 | 1.524,9 | 30/08/2022 | 0 | sem agendamento | Z10 1, C44 1, R10 1 |
| ULTRA-SONOGRAFIA DE PAREDE ABDOMINAL | 02.05.02.004-6 | 1 | 0 | 1 | 0 | 1.524,8 | 1.524,8 | 1.524,8 | 30/08/2022 | 0 | sem agendamento | N18 1 |
| DOPPLER ARTERIAL DE MI | 02.05.01.004-0 | 2 | 0 | 2 | 0 | 1.524,7 | 1.524,7 | 1.524,8 | 30/08/2022 | 0 | sem agendamento | M79 1, I73 1 |
| ULTRA-SONOGRAFIA DOPPLER ARTERIAL-M I E | 02.05.01.004-0 | 1 | 0 | 1 | 0 | 1.524,7 | 1.524,7 | 1.524,7 | 30/08/2022 | 0 | sem agendamento | I73 1 |
| DOPPLER VENOSO DE MI | 02.05.01.004-0 | 2 | 0 | 2 | 0 | 1.524,7 | 1.524,7 | 1.524,7 | 30/08/2022 | 0 | sem agendamento | M79 1, I73 1 |
| ULTRA-SONOGRAFIA DOPPLER VENOSO - MIE | 02.05.01.004-0 | 1 | 0 | 1 | 0 | 1.524,7 | 1.524,7 | 1.524,7 | 30/08/2022 | 0 | sem agendamento | I73 1 |
| ULTRA-SONOGRAFIA DOPPLER COLORIDO DE ORGAO OU ESTRUTURA ISO | 02.05.01.004-0 | 1 | 0 | 1 | 0 | 1.524,7 | 1.524,7 | 1.524,7 | 30/08/2022 | 0 | sem agendamento | I73 1 |
| ULTRA-SONOGRAFIA DE BOLSA ESCROTAL COM DOPPLER | 02.05.01.004-0 | 1 | 0 | 1 | 0 | 1.524,7 | 1.524,7 | 1.524,7 | 30/08/2022 | 0 | sem agendamento | E29 1 |

### candidatos do plano 4: as 20 de mais anos de estoque

| fila | código | fila | fila viva | pessoas | devolvidas | espera média | espera mediana | espera máxima | pedido mais antigo | agendadas 12 m | anos de estoque | CID principais |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| DOPPLER ARTERIAL DE MI | 02.05.01.004-0 | 2 | 0 | 2 | 0 | 1.524,7 | 1.524,7 | 1.524,8 | 30/08/2022 | 0 | sem agendamento | M79 1, I73 1 |
| DOPPLER VENOSO DE MI | 02.05.01.004-0 | 2 | 0 | 2 | 0 | 1.524,7 | 1.524,7 | 1.524,7 | 30/08/2022 | 0 | sem agendamento | M79 1, I73 1 |
| ECOGRAFIA DE ABDOMEN TOTAL ADULTO EMERGENCIA | 02.05.02.004-6 | 1 | 1 | 1 | 0 | 8,4 | 8,4 | 8,4 | 25/10/2026 | 0 | sem agendamento | R10 1 |
| ULTRA-SONOGRAFIA DOPPLER ARTERIAL- M I D | 02.05.01.004-0 | 2 | 0 | 2 | 288 | 1.537,9 | 1.537,9 | 1.544,9 | 10/08/2022 | 0 | sem agendamento | Z10 1, I83 1 |
| ULTRA-SONOGRAFIA DOPPLER ARTERIAL- M I E | 02.05.01.004-0 | 2 | 0 | 2 | 246 | 1.522,7 | 1.518,6 | 1.530,8 | 24/08/2022 | 0 | sem agendamento | Z10 1, I83 1 |
| ULTRA-SONOGRAFIA DOPPLER ARTERIAL- M S D | 02.05.01.004-0 | 1 | 0 | 1 | 30 | 1.643,7 | 1.643,7 | 1.643,7 | 03/05/2022 | 0 | sem agendamento | I83 1 |
| ULTRA-SONOGRAFIA DOPPLER COLORIDO DE ORGAO OU ESTRUTURA ISO | 02.05.01.004-0 | 1 | 0 | 1 | 0 | 1.524,7 | 1.524,7 | 1.524,7 | 30/08/2022 | 0 | sem agendamento | I73 1 |
| ULTRA-SONOGRAFIA DOPPLER COLORIDO DE UM VASO | 02.05.01.004-0 | 3 | 0 | 3 | 2 | 1.524,9 | 1.525,0 | 1.525,1 | 30/08/2022 | 0 | sem agendamento | N18 2, I73 1 |
| ULTRA-SONOGRAFIA DOPPLER DE CAROTIDAS | 02.05.01.004-0 | 1 | 0 | 1 | 8 | 1.637,0 | 1.637,0 | 1.637,0 | 10/05/2022 | 0 | sem agendamento | I10 1 |
| ULTRA-SONOGRAFIA DOPPLER DE CAROTIDAS E VERTEBRAIS | 02.05.01.004-0 | 190 | 19 | 190 | 26 | 971,1 | 942,5 | 1.362,7 | 08/02/2023 | 0 | sem agendamento | I10 71, E11 23, E78 21 |
| ULTRA-SONOGRAFIA DOPPLER VENOSO - MID | 02.05.01.004-0 | 8 | 0 | 8 | 483 | 1.568,1 | 1.536,7 | 1.703,8 | 04/03/2022 | 0 | sem agendamento | I83 5, I87 2, G63 1 |
| ULTRA-SONOGRAFIA DOPPLER VENOSO - MIE | 02.05.01.004-0 | 10 | 0 | 10 | 439 | 1.608,4 | 1.592,0 | 1.873,7 | 15/09/2021 | 0 | sem agendamento | I83 8, M79 1, G83 1 |
| ULTRA-SONOGRAFIA DE ABDOMEN TOTAL | 02.05.02.004-6 | 3 | 0 | 3 | 1 | 1.524,8 | 1.524,9 | 1.524,9 | 30/08/2022 | 0 | sem agendamento | Z10 1, C44 1, R10 1 |
| ULTRA-SONOGRAFIA DE BOLSA ESCROTAL COM DOPPLER | 02.05.01.004-0 | 1 | 0 | 1 | 0 | 1.524,7 | 1.524,7 | 1.524,7 | 30/08/2022 | 0 | sem agendamento | E29 1 |
| ULTRA-SONOGRAFIA DE PAREDE ABDOMINAL | 02.05.02.004-6 | 1 | 0 | 1 | 0 | 1.524,8 | 1.524,8 | 1.524,8 | 30/08/2022 | 0 | sem agendamento | N18 1 |
| ULTRA-SONOGRAFIA DOPPLER - ARTERIAS RENAIS | 02.05.01.004-0 | 1 | 0 | 1 | 0 | 1.558,5 | 1.558,5 | 1.558,5 | 27/07/2022 | 0 | sem agendamento | I70 1 |
| ULTRA-SONOGRAFIA DOPPLER - CERVICAL | 02.05.01.004-0 | 1 | 0 | 1 | 0 | 1.382,7 | 1.382,7 | 1.382,7 | 19/01/2023 | 0 | sem agendamento | E04 1 |
| ULTRA-SONOGRAFIA DOPPLER ARTERIAL-M I D | 02.05.01.004-0 | 3 | 0 | 3 | 0 | 1.536,0 | 1.524,8 | 1.558,4 | 27/07/2022 | 0 | sem agendamento | L98 1, M79 1, I73 1 |
| ULTRA-SONOGRAFIA DOPPLER ARTERIAL-M I E | 02.05.01.004-0 | 1 | 0 | 1 | 0 | 1.524,7 | 1.524,7 | 1.524,7 | 30/08/2022 | 0 | sem agendamento | I73 1 |
| ULTRA-SONOGRAFIA DOPPLER DE CAROTIDAS E VERTEBRAIS | 02.05.01.004-0 | 4 | 0 | 4 | 17 | 1.667,9 | 1.668,0 | 1.700,8 | 07/03/2022 | 0 | sem agendamento | E14 1, E78 1, I10 1 |

## Rumo por código

Um código por linha, com as filas do universo somadas (cada par nome × código uma vez). Tudo **calculado** no montador sobre a série mensal do motor (abas "Por código" da planilha). Os 12 meses fechados vão de 2025-10 a 2026-09, e os 12 de antes, de 2024-10 a 2025-09. Entrantes = pedidos abertos mais os já agendados, pelo mês do pedido. Oferta = agendamentos pelo mês em que acontecem, em todas as situações. Falta = faltas ÷ (realizados + faltas). Saldo por mês = (entrantes − oferta) ÷ 12: positivo, a fila cresce. Maior mês de oferta e média dos 3 últimos meses fechados, para ver o esforço que parou.

| código | fila mais pedida do código | fila | fila viva | devolvidas | entrantes 12 m | entrantes 12 m antes | oferta 12 m | oferta 12 m antes | saldo por mês | falta 12 m | maior mês de oferta | oferta média 3 últimos meses |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 02.05.01.004-0 | ULTRA-SONOGRAFIA DOPPLER VENOSO - MMII ( BILATERAL) | 16.844 | 12.143 | 5.713 | 16.307 | 14.999 | 12.637 | 11.188 | 305,8 | 25% | 2026-04 (1.272) | 1.099,7 |
| 02.05.02.004-6 | ECOGRAFIA DE ABDOMEN TOTAL ADULTO | 13.656 | 9.872 | 13.276 | 13.861 | 12.763 | 10.667 | 8.974 | 266,2 | 37% | 2026-07 (1.685) | 1.169,0 |
| 02.06.03.001-0 | 063. TC DO ABDOMEN SUPERIOR ADULTO C/CONTRASTE S/SEDACAO | 6.214 | 6.155 | 7.722 | 18.188 | 19.417 | 17.711 | 15.805 | 39,8 | 36% | 2026-03 (1.829) | 1.504,0 |
| 02.06.02.003-1 | 055. TC DO TORAX ADULTO C/CONTRASTE S/SEDACAO | 6.043 | 5.978 | 5.179 | 29.855 | 28.772 | 29.553 | 24.461 | 25,2 | 33% | 2026-09 (3.572) | 2.949,7 |
| 02.06.03.003-7 | 111. TC DE PELVE OU BACIA ADULTO C/CONTRASTE S/SEDACAO | 5.044 | 4.990 | 5.435 | 15.261 | 16.868 | 14.962 | 13.999 | 24,9 | 34% | 2026-03 (1.536) | 1.309,0 |

## Oferta por unidade executante

Agendamentos pelo mês em que acontecem, por unidade que executa, em todas as situações. A média mensal é a dos seis meses fechados de 2025-10 a 2026-03; depois, mês a mês, com o mês corrente e o já agendado para depois. 
A última linha é a oferta do código no mesmo mês: o que passa da soma das unidades é agendamento sem unidade. As 25 unidades de maior oferta na janela; as outras, somadas. Planilha: aba "Por código executante".

### 02.05.01.004-0

| unidade executante | CNES | tipo | média mensal antes | 2026-04 | 2026-05 | 2026-06 | 2026-07 | 2026-08 | 2026-09 | 2026-10 | 2026-11 | 2026-12 | 2027-01 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ICDF | 3276678 | Contratado/Credenciado | 453,2 | 526 | 231 | 441 | 467 | 429 | 411 | 418 | 411 | 0 | 0 |
| HRAN | 0010464 | Região Central | 129,0 | 127 | 244 | 225 | 162 | 216 | 205 | 190 | 49 | 0 | 0 |
| CRDF | 3044432 | URD | 148,2 | 260 | 154 | 132 | 204 | 186 | 184 | 150 | 113 | 0 | 0 |
| Cent Radiologia Tagua | 0011193 | Região Sudoeste | 43,5 | 154 | 84 | 92 | 59 | 100 | 96 | 106 | 51 | 0 | 0 |
| HUB | 0010510 | Contratado/Credenciado | 41,7 | 80 | 29 | 51 | 39 | 44 | 49 | 46 | 61 | 0 | 0 |
| HRS | 0010502 | Região Norte | 50,0 | 56 | 71 | 62 | 32 | 56 | 45 | 56 | 0 | 0 | 0 |
| HRG | 0010472 | Região Sul | 81,8 | 54 | 61 | 72 | 37 | 42 | 56 | 38 | 6 | 0 | 0 |
| HBDF | 0010456 | URD | 48,8 | 2 | 48 | 50 | 46 | 62 | 48 | 42 | 18 | 0 | 0 |
| HRL | 2645157 | Região Leste | 4,8 | 12 | 9 | 2 | 2 | 3 | 2 | 1 | 14 | 0 | 0 |
| HRC | 0010480 | Região Oeste | 0,0 | 0 | 0 | 0 | 0 | 16 | 0 | 0 | 0 | 0 | 0 |
| HRGu | 2814897 | Região Centro-Sul | 0,0 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 3 | 0 | 0 |
| HRPl | 0010529 | Região Norte | 0,3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **soma das unidades** |  |  | 1.001,3 | 1.272 | 931 | 1.127 | 1.048 | 1.155 | 1.096 | 1.047 | 726 | 0 | 0 |
| **oferta do código** |  |  | 1.001,3 | 1.272 | 931 | 1.127 | 1.048 | 1.155 | 1.096 | 1.047 | 726 | — | — |

### 02.05.02.004-6

| unidade executante | CNES | tipo | média mensal antes | 2026-04 | 2026-05 | 2026-06 | 2026-07 | 2026-08 | 2026-09 | 2026-10 | 2026-11 | 2026-12 | 2027-01 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| HRS | 0010502 | Região Norte | 46,8 | 131 | 156 | 118 | 145 | 141 | 369 | 98 | 0 | 0 | 0 |
| Policlínica Ceilândia II | 9578501 | Região Oeste | 0,0 | 0 | 0 | 51 | 1.060 | 0 | 0 | 0 | 0 | 0 | 0 |
| HRL | 2645157 | Região Leste | 133,3 | 64 | 49 | 60 | 2 | 77 | 47 | 252 | 446 | 1 | 1 |
| HRAN | 0010464 | Região Central | 100,3 | 158 | 132 | 188 | 95 | 154 | 139 | 72 | 0 | 0 | 0 |
| Cent Radiologia Tagua | 0011193 | Região Sudoeste | 53,2 | 218 | 101 | 36 | 50 | 84 | 80 | 110 | 84 | 0 | 0 |
| HRC | 0010480 | Região Oeste | 42,3 | 141 | 166 | 135 | 14 | 48 | 30 | 48 | 0 | 0 | 0 |
| HRSam | 2672197 | Região Sudoeste | 64,8 | 67 | 63 | 76 | 115 | 38 | 90 | 36 | 5 | 0 | 0 |
| HRPl | 0010529 | Região Norte | 70,0 | 61 | 81 | 44 | 43 | 57 | 45 | 69 | 11 | 0 | 0 |
| HRBz | 0010545 | Região Oeste | 43,3 | 93 | 64 | 85 | 1 | 27 | 26 | 55 | 16 | 0 | 0 |
| HRG | 0010472 | Região Sul | 41,2 | 34 | 38 | 52 | 73 | 72 | 24 | 37 | 13 | 0 | 0 |
| Hospital Dia | 0010596 | Região Central | 31,0 | 52 | 75 | 33 | 25 | 30 | 16 | 12 | 4 | 0 | 0 |
| Policlínica Gama | 5598575 | Região Sul | 11,3 | 19 | 26 | 21 | 18 | 36 | 15 | 3 | 0 | 0 | 0 |
| HRGu | 2814897 | Região Centro-Sul | 16,8 | 10 | 16 | 12 | 15 | 30 | 10 | 21 | 11 | 0 | 0 |
| FHB | 0011339 | Serviços Centralizados | 0,0 | 0 | 0 | 0 | 0 | 0 | 102 | 0 | 0 | 0 | 0 |
| HRT | 0010499 | Região Sudoeste | 6,0 | 2 | 0 | 4 | 29 | 35 | 0 | 0 | 0 | 0 | 0 |
| HRSM | 5717515 | Região Sul | 36,0 | 49 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Policlínica 514 Sul | 9580816 | Região Central | 0,0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **soma das unidades** |  |  | 696,5 | 1.099 | 967 | 915 | 1.685 | 829 | 993 | 813 | 590 | 1 | 1 |
| **oferta do código** |  |  | 696,5 | 1.099 | 967 | 915 | 1.685 | 829 | 993 | 813 | 590 | 1 | 1 |

### 02.06.02.003-1

| unidade executante | CNES | tipo | média mensal antes | 2026-04 | 2026-05 | 2026-06 | 2026-07 | 2026-08 | 2026-09 | 2026-10 | 2026-11 | 2026-12 | 2027-01 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CRDF | 3044432 | URD | 685,2 | 1.373 | 1.176 | 1.060 | 1.031 | 1.172 | 1.655 | 1.212 | 164 | 0 | 0 |
| HUB | 0010510 | Contratado/Credenciado | 467,2 | 696 | 504 | 609 | 517 | 468 | 454 | 462 | 0 | 0 | 0 |
| ICDF | 3276678 | Contratado/Credenciado | 390,0 | 439 | 461 | 423 | 517 | 566 | 425 | 375 | 43 | 1 | 0 |
| HRAN | 0010464 | Região Central | 124,7 | 147 | 138 | 124 | 140 | 128 | 131 | 118 | 1 | 0 | 0 |
| FHB | 0011339 | Serviços Centralizados | 0,0 | 0 | 0 | 0 | 0 | 254 | 582 | 71 | 0 | 0 | 0 |
| HBDF | 0010456 | URD | 188,5 | 83 | 0 | 0 | 47 | 81 | 166 | 392 | 8 | 0 | 0 |
| HMIB | 0010537 | URD | 78,3 | 60 | 245 | 10 | 0 | 0 | 63 | 40 | 26 | 0 | 0 |
| HRG | 0010472 | Região Sul | 44,5 | 38 | 72 | 54 | 81 | 41 | 16 | 27 | 0 | 0 | 0 |
| HRL | 2645157 | Região Leste | 23,5 | 22 | 34 | 19 | 36 | 36 | 32 | 23 | 0 | 0 | 0 |
| HRSam | 2672197 | Região Sudoeste | 32,7 | 33 | 46 | 35 | 33 | 4 | 0 | 10 | 0 | 0 | 0 |
| HCB | 6876617 | URD | 17,8 | 16 | 22 | 21 | 24 | 19 | 12 | 16 | 7 | 3 | 0 |
| HRC | 0010480 | Região Oeste | 26,2 | 11 | 0 | 0 | 30 | 42 | 30 | 27 | 0 | 0 | 0 |
| HRS | 0010502 | Região Norte | 28,0 | 24 | 23 | 0 | 0 | 0 | 0 | 8 | 0 | 0 | 0 |
| HRPl | 0010529 | Região Norte | 0,0 | 0 | 0 | 0 | 0 | 7 | 6 | 3 | 0 | 0 | 0 |
| HRT | 0010499 | Região Sudoeste | 0,0 | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 |
| Hosp S Mateus | 6730914 | Contratado/Credenciado | 7,8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **soma das unidades** |  |  | 2.114,3 | 2.942 | 2.721 | 2.355 | 2.456 | 2.821 | 3.572 | 2.784 | 249 | 4 | 0 |
| **oferta do código** |  |  | 2.114,3 | 2.942 | 2.721 | 2.355 | 2.456 | 2.821 | 3.572 | 2.784 | 249 | 4 | — |

### 02.06.03.001-0

| unidade executante | CNES | tipo | média mensal antes | 2026-04 | 2026-05 | 2026-06 | 2026-07 | 2026-08 | 2026-09 | 2026-10 | 2026-11 | 2026-12 | 2027-01 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CRDF | 3044432 | URD | 535,5 | 467 | 738 | 476 | 703 | 490 | 627 | 544 | 72 | 0 | 0 |
| HUB | 0010510 | Contratado/Credenciado | 369,8 | 181 | 382 | 389 | 362 | 358 | 351 | 314 | 0 | 0 | 0 |
| ICDF | 3276678 | Contratado/Credenciado | 194,5 | 149 | 185 | 175 | 187 | 158 | 191 | 200 | 53 | 0 | 0 |
| HBDF | 0010456 | URD | 131,7 | 81 | 0 | 0 | 44 | 73 | 149 | 354 | 10 | 0 | 0 |
| HRAN | 0010464 | Região Central | 90,0 | 98 | 106 | 85 | 87 | 88 | 81 | 100 | 1 | 0 | 0 |
| FHB | 0011339 | Serviços Centralizados | 0,0 | 0 | 0 | 0 | 0 | 123 | 133 | 19 | 0 | 0 | 0 |
| HMIB | 0010537 | URD | 92,0 | 41 | 33 | 4 | 0 | 0 | 20 | 39 | 37 | 0 | 0 |
| HRL | 2645157 | Região Leste | 24,5 | 15 | 24 | 29 | 21 | 23 | 20 | 19 | 0 | 0 | 0 |
| HRG | 0010472 | Região Sul | 25,3 | 13 | 27 | 19 | 26 | 26 | 9 | 12 | 0 | 0 | 0 |
| HCB | 6876617 | URD | 14,3 | 15 | 12 | 16 | 16 | 21 | 18 | 14 | 4 | 0 | 0 |
| HRC | 0010480 | Região Oeste | 17,2 | 10 | 0 | 0 | 33 | 17 | 28 | 28 | 0 | 0 | 0 |
| HRSam | 2672197 | Região Sudoeste | 26,7 | 29 | 30 | 30 | 14 | 0 | 0 | 9 | 0 | 0 | 0 |
| HRS | 0010502 | Região Norte | 20,8 | 26 | 19 | 0 | 0 | 0 | 0 | 6 | 0 | 0 | 0 |
| HRPl | 0010529 | Região Norte | 0,0 | 0 | 0 | 0 | 0 | 6 | 7 | 4 | 0 | 0 | 0 |
| HRT | 0010499 | Região Sudoeste | 0,0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 |
| Hosp S Mateus | 6730914 | Contratado/Credenciado | 6,8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **soma das unidades** |  |  | 1.549,2 | 1.125 | 1.556 | 1.223 | 1.493 | 1.385 | 1.634 | 1.662 | 177 | 0 | 0 |
| **oferta do código** |  |  | 1.549,2 | 1.125 | 1.556 | 1.223 | 1.493 | 1.385 | 1.634 | 1.662 | 177 | — | — |

### 02.06.03.003-7

| unidade executante | CNES | tipo | média mensal antes | 2026-04 | 2026-05 | 2026-06 | 2026-07 | 2026-08 | 2026-09 | 2026-10 | 2026-11 | 2026-12 | 2027-01 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CRDF | 3044432 | URD | 448,2 | 381 | 645 | 395 | 653 | 435 | 513 | 344 | 30 | 0 | 0 |
| HUB | 0010510 | Contratado/Credenciado | 276,0 | 108 | 325 | 355 | 299 | 325 | 303 | 283 | 0 | 0 | 0 |
| ICDF | 3276678 | Contratado/Credenciado | 170,7 | 109 | 163 | 138 | 176 | 127 | 150 | 162 | 47 | 0 | 0 |
| HBDF | 0010456 | URD | 119,7 | 52 | 0 | 0 | 38 | 62 | 113 | 283 | 9 | 0 | 0 |
| HRAN | 0010464 | Região Central | 85,2 | 78 | 78 | 74 | 76 | 66 | 75 | 93 | 1 | 0 | 0 |
| FHB | 0011339 | Serviços Centralizados | 0,0 | 0 | 0 | 0 | 0 | 115 | 130 | 23 | 0 | 0 | 0 |
| HRL | 2645157 | Região Leste | 26,7 | 17 | 22 | 32 | 23 | 24 | 24 | 18 | 0 | 0 | 0 |
| HMIB | 0010537 | URD | 77,5 | 36 | 31 | 7 | 0 | 0 | 11 | 39 | 28 | 0 | 0 |
| HRG | 0010472 | Região Sul | 25,0 | 12 | 27 | 21 | 26 | 27 | 9 | 13 | 0 | 0 | 0 |
| HRC | 0010480 | Região Oeste | 10,8 | 9 | 0 | 0 | 32 | 17 | 18 | 21 | 0 | 0 | 0 |
| HCB | 6876617 | URD | 13,0 | 16 | 8 | 9 | 9 | 12 | 14 | 14 | 2 | 1 | 0 |
| HRSam | 2672197 | Região Sudoeste | 14,2 | 23 | 14 | 23 | 10 | 1 | 0 | 7 | 0 | 0 | 0 |
| HRS | 0010502 | Região Norte | 22,3 | 29 | 21 | 0 | 0 | 0 | 0 | 5 | 0 | 0 | 0 |
| HRPl | 0010529 | Região Norte | 0,0 | 0 | 0 | 0 | 0 | 6 | 7 | 5 | 0 | 0 | 0 |
| HRT | 0010499 | Região Sudoeste | 0,0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| Hosp S Mateus | 6730914 | Contratado/Credenciado | 7,0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **soma das unidades** |  |  | 1.296,2 | 870 | 1.334 | 1.054 | 1.342 | 1.218 | 1.367 | 1.310 | 117 | 1 | 0 |
| **oferta do código** |  |  | 1.296,2 | 870 | 1.334 | 1.054 | 1.342 | 1.218 | 1.367 | 1.310 | 117 | 1 | — |

## Região de Saúde

Região de Saúde: não pedida na ordem.

## Diferença para a coleta anterior

Contra `dados/fontes/mapa_social_20261102_imagem_bruto/coleta_20261102.json` (recarga 02/11/2026 10:31:47). Diferença **calculada** no montador.

A coleta anterior não tem as mesmas filas nem os mesmos objetos.
