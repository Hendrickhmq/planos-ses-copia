# Mapa Social da Saúde — fila de TC de abdômen superior (tc_abdomen); TC de pelve (tc_pelve); Ultrassonografia transfontanela (transfontanela); TC de pescoço (tc_pescoco); Ultrassonografia de abdômen superior (abdomen_superior); Ultrassonografia de bolsa escrotal (bolsa_escrotal); Ultrassonografia de aparelho urinário (urinario); Ultrassonografia de abdômen total (abdomen_total); Ultrassonografia de parede abdominal (parede); Doppler de carótidas, renais e outros (doppler_outros); Ultrassonografia de próstata por via abdominal (prostata); Ultrassonografia de tireoide (tireoide); Ultrassonografia mamária bilateral (mama); Doppler bilateral de membros (doppler_membros); Ultrassonografia pélvica (pelvica); TC de tórax, sem a angio coronária (tc_torax); TC de crânio (tc_cranio); TC de face (tc_face); Ultrassonografia transvaginal (transvaginal), coleta de 02/11/2026

Ordem de coleta: Região de Saúde da unidade solicitante de cada grupo de filas da carteira 1 do plano 4 (só as filas que a carteira usa), para dimensionar as 20 salas de ultrassom e os 5 tomógrafos por polo.

Coleta montada por `ferramentas/montar_coleta.py` a partir da saída do kit do motor: o modelo não escreveu número nenhum, e o resumo não se edita à mão (conferência K). A decisão de cada fila vem do enquadramento do plano.

| campo | conteúdo |
|---|---|
| Fonte | Mapa Social da Saúde – Regulamentação (MPDFT) · Lista de Espera – Exames e Consultas · `https://paineis-ext.mpdft.mp.br/extensions/mapasauderegulamentacao/mapasauderegulamentacao.html` · app Qlik `7edb02fa-f1f5-4ea6-b348-049a4ac2d095` · dados SISREG/DATASUS |
| Última recarga da base | 02/11/2026 18:31:39 (qLastReloadTime 2026-11-02T21:31:39.947Z) |
| Consulta | 02/11/2026 19:43:15 a 19:44:12 (relógio do motor), sem recarga no meio |
| Solicitação mais recente na base | 28/10/2026 (agendamento mais distante: 04/02/2027) |
| Medida | **fila** = os três status: pendente de regulação, corrigida e reenviada para regulação, pendente de regulação por fila de espera. Devolvidas para complementação ficam fora e são contadas à parte |
| Fila viva | só as solicitações a partir de `data_solicitacao={">=28/10/2024"}` (24 meses contados da solicitação mais recente) |
| Agendadas em 12 meses | `data_agendamento={">=28/10/2025<=27/10/2026"}`, todos os status |
| Ordem | medicao; `ordem.json` (hash 3216986928) |
| Via | kit do motor `ferramentas/mapa_social/motor.js` (versão 2026-10-27, assinatura 2089625745); saída pela área de transferência, 1 parte(s) conferidas por hash (`ferramentas/ler_motor.py`) |

Pessoas = CNS distintos no conjunto (quem espera por mais de um exame conta uma vez); só a contagem sai do motor. Espera em dias, calculada no motor sobre os registros do conjunto.

## Alarmes

Limites de `ferramentas/conferir_coleta.py`: 30% (CID dominante), 5% (CID raro), 30% (fila velha), 3 anos (estoque), 20 categorias (CID largo).

- **fila velha**: ECOGRAFIA DE ABDOMEN SUPERIOR ADULTO: 984 de 2.213 pedidos de antes da janela
- **fila velha**: ECOGRAFIA DE ABDOMEN TOTAL INFANTIL: 166 de 452 pedidos de antes da janela
- **fila velha**: ECOGRAFIA DE BOLSA ESCROTAL ADULTO: 272 de 700 pedidos de antes da janela
- **fila velha**: ECOGRAFIA DE MAMAS - BILATERAL: 4.440 de 12.950 pedidos de antes da janela
- **fila velha**: ECOGRAFIA DO APARELHO URINARIO (RINS, BEXIGA) ADULTO: 1.279 de 3.677 pedidos de antes da janela
- **fila velha**: ECOGRAFIA PELVICA (GINECOLOGICA) - ADULTO: 234 de 573 pedidos de antes da janela
- **fila velha**: ECOGRAFIA TRANSVAGINAL: 3.595 de 9.294 pedidos de antes da janela
- **fila velha**: ECOGRAFIA TRANSVAGINAL COM DOPPLER: 44 de 133 pedidos de antes da janela
- **estoque**: ULTRA-SONOGRAFIA DOPPLER DE CAROTIDAS E VERTEBRAIS: 190 na fila, sem agendamento em 12 meses
- **fila velha**: ULTRA-SONOGRAFIA DOPPLER DE CAROTIDAS E VERTEBRAIS: 171 de 190 pedidos de antes da janela
- **estoque**: ULTRA-SONOGRAFIA DOPPLER ARTERIAL - MMII (BILATERAL): 1.800 na fila, 3,5 anos de agendamentos
- **estoque**: ULTRA-SONOGRAFIA DOPPLER DE CAROTIDAS E VERTEBRAIS: 4 na fila, sem agendamento em 12 meses
- **fila velha**: ULTRA-SONOGRAFIA DOPPLER DE CAROTIDAS E VERTEBRAIS: 4 de 4 pedidos de antes da janela
- **fila velha**: ULTRA-SONOGRAFIA DOPPLER VENOSO - MMII ( BILATERAL): 3.985 de 10.045 pedidos de antes da janela
- **fila velha**: ULTRASONOGRAFIA DE PAREDE ABDOMINAL: 1.105 de 3.304 pedidos de antes da janela
- **estoque**: ULTRASSONOGRAFIA COM DOPPLER COLORIDO DE ARTERIAS RENAIS: 92 na fila, 5,8 anos de agendamentos
- **estoque**: ULTRASSONOGRAFIA RENAL: 72 na fila, 4,0 anos de agendamentos
- **fila velha**: ULTRASSONOGRAFIA RENAL: 27 de 72 pedidos de antes da janela

## Lacunas

nenhuma

## Exames

A união das filas de cada exame, na idade e no sexo da ordem, quando ela os dá.

| exame | filas | fila | fila viva | pessoas | pessoas viva | devolvidas | espera média | espera mediana |
|---|---|---|---|---|---|---|---|---|
| TC de abdômen superior (tc_abdomen) | 6 | 5.031 | 5.016 | **4.949** | 4.935 | 7.176 | 137,4 | 130,3 |
| TC de pelve (tc_pelve) | 3 | 3.949 | 3.939 | **3.939** | 3.929 | 4.812 | 133,3 | 130,3 |
| Ultrassonografia transfontanela (transfontanela) | 1 | 270 | 243 | **270** | 243 | 201 | 309,0 | 251,3 |
| TC de pescoço (tc_pescoco) | 2 | 657 | 655 | **655** | 654 | 525 | 120,3 | 115,4 |
| Ultrassonografia de abdômen superior (abdomen_superior) | 1 | 2.213 | 1.229 | **2.211** | 1.228 | 984 | 688,1 | 622,7 |
| Ultrassonografia de bolsa escrotal (bolsa_escrotal) | 2 | 934 | 599 | **934** | 599 | 501 | 576,5 | 469,7 |
| Ultrassonografia de aparelho urinário (urinario) | 3 | 4.025 | 2.654 | **4.011** | 2.644 | 4.104 | 640,6 | 418,0 |
| Ultrassonografia de abdômen total (abdomen_total) | 2 | 10.347 | 7.672 | **10.340** | 7.672 | 11.997 | 555,6 | 356,4 |
| Ultrassonografia de parede abdominal (parede) | 1 | 3.304 | 2.199 | **3.304** | 2.199 | 1.278 | 598,6 | 508,1 |
| Doppler de carótidas, renais e outros (doppler_outros) | 6 | 4.731 | 4.512 | **4.700** | 4.489 | 2.975 | 180,9 | 130,0 |
| Ultrassonografia de próstata por via abdominal (prostata) | 1 | 2.969 | 2.203 | **2.966** | 2.202 | 2.714 | 600,7 | 467,3 |
| Ultrassonografia de tireoide (tireoide) | 3 | 3.854 | 3.098 | **3.821** | 3.080 | 3.327 | 484,6 | 374,4 |
| Ultrassonografia mamária bilateral (mama) | 1 | 12.950 | 8.510 | **12.928** | 8.500 | 7.731 | 628,8 | 518,4 |
| Doppler bilateral de membros (doppler_membros) | 4 | 12.043 | 7.609 | **10.883** | 6.780 | 1.222 | 600,6 | 536,3 |
| Ultrassonografia pélvica (pelvica) | 2 | 1.014 | 699 | **1.005** | 694 | 920 | 614,2 | 395,1 |
| TC de tórax, sem a angio coronária (tc_torax) | 4 | 3.214 | 3.202 | **3.169** | 3.159 | 4.803 | 134,9 | 125,1 |
| TC de crânio (tc_cranio) | 3 | 801 | 794 | **793** | 786 | 2.136 | 99,9 | 83,0 |
| TC de face (tc_face) | 2 | 139 | 137 | **137** | 135 | 147 | 126,6 | 111,7 |
| Ultrassonografia transvaginal (transvaginal) | 1 | 9.294 | 5.699 | **9.293** | 5.698 | 8.953 | 658,9 | 528,3 |

## Filas do objeto

As filas de partida da ordem, pelo nome exato do motor, sem recorte de CID. Anos de estoque = fila ÷ agendadas em 12 meses (**calculado** no montador).

| fila | código | objeto | papel | fila | fila viva | pessoas | devolvidas | espera média | espera mediana | espera máxima | pedido mais antigo | agendadas 12 m | anos de estoque | CID principais |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 061. TC DO ABDOMEN SUPERIOR ADULTO S/CONTRASTE S/SEDACAO | 02.06.03.001-0 | tc_abdomen | exame | 68 | 68 | 68 | 1.489 | 19,1 | 7,1 | 222,1 | 25/03/2026 | 5.496 | 0,0 | N20 22, R10 15, N18 3, C50 2, K45 2 |
| 063. TC DO ABDOMEN SUPERIOR ADULTO C/CONTRASTE S/SEDACAO | 02.06.03.001-0 | tc_abdomen | exame | 4.116 | 4.101 | 4.112 | 5.271 | 129,5 | 126,3 | 850,4 | 05/07/2024 | 8.164 | 0,5 | C50 762, C18 388, R10 321, C20 149, C16 147 |
| ANGIOTOMOGRAFIA DA AORTA ABDOMINAL E DOS SEUS RAMOS ADULTO S/SEDACAO | 02.06.03.001-0 | tc_abdomen | exame | 323 | 323 | 323 | 145 | 199,5 | 171,4 | 475,1 | 15/07/2025 | 605 | 0,5 | I71 141, I70 26, I35 24, N18 23, I73 9 |
| ANGIOTOMOGRAFIA DO ABDOME SUPERIOR ADULTO S/SEDACAO | 02.06.03.001-0 | tc_abdomen | exame | 245 | 245 | 245 | 130 | 220,2 | 188,1 | 543,9 | 07/05/2025 | 309 | 0,8 | I71 46, N18 36, K55 20, I82 19, I70 11 |
| ANGIOTOMOGRAFIA DAS ARTERIAS CAROTIDAS E VERTEBRAIS ADULTO S/SEDACAO | 02.06.03.001-0 | tc_abdomen | exame | 243 | 243 | 243 | 130 | 135,0 | 122,0 | 440,1 | 19/08/2025 | 541 | 0,4 | I65 76, I64 33, I63 25, I25 19, I70 13 |
| ANGIOTOMOGRAFIA DAS ARTÉRIAS RENAIS ADULTO S/SEDACAO | 02.06.03.001-0 | tc_abdomen | exame | 36 | 36 | 36 | 11 | 160,4 | 132,7 | 430,1 | 29/08/2025 | 47 | 0,8 | I15 15, I10 4, I77 3, I72 2, Z95 1 |
| 109. TC DE PELVE OU BACIA ADULTO S/CONTRASTE S/SEDACAO | 02.06.03.003-7 | tc_pelve | exame | 57 | 57 | 57 | 952 | 21,5 | 7,1 | 279,1 | 27/01/2026 | 5.469 | 0,0 | N20 18, R10 13, N18 3, M79 2, K86 2 |
| 111. TC DE PELVE OU BACIA ADULTO C/CONTRASTE S/SEDACAO | 02.06.03.003-7 | tc_pelve | exame | 3.639 | 3.629 | 3.637 | 3.718 | 129,1 | 130,1 | 850,4 | 05/07/2024 | 7.036 | 0,5 | C50 613, C18 361, R10 305, C16 139, C20 120 |
| ANGIOTOMOGRAFIA DA PELVE ADULTO S/SEDACAO | 02.06.03.003-7 | tc_pelve | exame | 253 | 253 | 253 | 142 | 218,7 | 182,3 | 473,3 | 17/07/2025 | 330 | 0,8 | N18 40, I82 39, I71 37, K55 15, I70 14 |
| ULTRA-SONOGRAFIA TRANSFONTANELA | 02.05.02.017-8 | transfontanela | exame | 270 | 243 | 270 | 201 | 309,0 | 251,3 | 1.594,3 | 22/06/2022 | 818 | 0,3 | Q75 61, P21 44, P07 21, P05 16, Q02 13 |
| 119. TC DE PESCOCO ADULTO C/CONTRASTE S/SEDACAO | 02.06.01.005-2 | tc_pescoco | exame | 479 | 477 | 478 | 337 | 126,8 | 123,2 | 847,3 | 08/07/2024 | 1.361 | 0,4 | C32 41, C73 28, C83 25, C10 23, C44 20 |
| ANGIOTOMOGRAFIA DO PESCOCO ADULTO S/SEDACAO | 02.06.01.005-2 | tc_pescoco | exame | 178 | 178 | 178 | 188 | 102,9 | 97,6 | 252,3 | 23/02/2026 | 414 | 0,4 | I65 37, I64 32, I63 22, I70 12, I67 9 |
| ECOGRAFIA DE ABDOMEN SUPERIOR ADULTO | 02.05.02.003-8 | abdomen_superior | exame | 2.213 | 1.229 | 2.211 | 984 | 688,1 | 622,7 | 5.885,7 | 22/09/2010 | 2.449 | 0,9 | K76 663, R10 382, K80 236, E66 115, K30 92 |
| ECOGRAFIA DE BOLSA ESCROTAL ADULTO | 02.05.02.007-0 | bolsa_escrotal | exame | 700 | 428 | 700 | 430 | 605,0 | 523,2 | 2.105,3 | 27/01/2021 | 627 | 1,1 | N51 164, N43 91, K40 80, I86 60, N50 58 |
| ECOGRAFIA DE BOLSA ESCROTAL INFANTIL | 02.05.02.007-0 | bolsa_escrotal | exame | 234 | 171 | 234 | 71 | 490,8 | 237,3 | 2.090,1 | 11/02/2021 | 316 | 0,7 | Q53 97, N43 49, K40 21, N51 18, Q55 10 |
| ECOGRAFIA DO APARELHO URINARIO (RINS, BEXIGA) ADULTO | 02.05.02.005-4 | urinario | exame | 3.677 | 2.398 | 3.675 | 3.434 | 653,2 | 431,1 | 5.794,7 | 22/12/2010 | 4.119 | 0,9 | N20 832, N18 468, N39 332, N40 258, R31 223 |
| ECOGRAFIA DO APARELHO URINARIO (RINS, BEXIGA) INFANTIL | 02.05.02.005-4 | urinario | exame | 276 | 211 | 276 | 655 | 474,6 | 208,7 | 2.111,0 | 21/01/2021 | 789 | 0,3 | N39 50, Q17 15, Q62 14, N20 12, P70 11 |
| ULTRASSONOGRAFIA RENAL | 02.05.02.005-4 | urinario | exame | 72 | 45 | 72 | 15 | 629,3 | 534,0 | 1.348,2 | 23/02/2023 | 18 | 4,0 | N20 16, N18 9, R31 6, I10 5, Q61 4 |
| ECOGRAFIA DE ABDOMEN TOTAL ADULTO | 02.05.02.004-6 | abdomen_total | exame | 9.895 | 7.386 | 9.890 | 11.564 | 554,2 | 357,0 | 6.124,7 | 26/01/2010 | 8.207 | 1,2 | R10 3.302, K76 1.277, K80 725, E66 434, K30 293 |
| ECOGRAFIA DE ABDOMEN TOTAL INFANTIL | 02.05.02.004-6 | abdomen_total | exame | 452 | 286 | 452 | 433 | 586,5 | 350,1 | 2.079,3 | 22/02/2021 | 1.067 | 0,4 | R10 178, E66 75, Q90 16, K42 15, K59 12 |
| ULTRASONOGRAFIA DE PAREDE ABDOMINAL | 02.05.02.004-6 | parede | exame | 3.304 | 2.199 | 3.304 | 1.278 | 598,6 | 508,1 | 2.453,0 | 14/02/2020 | 1.470 | 2,2 | K42 870, K40 842, K46 486, R10 307, K43 192 |
| 10. ECODOPPLER DE CAROTIDAS | 02.05.01.004-0 | doppler_outros | exame | 4.143 | 4.143 | 4.143 | 2.776 | 136,6 | 125,0 | 592,4 | 20/03/2025 | 8.258 | 0,5 | I10 944, I50 419, I25 419, E78 287, I20 240 |
| ULTRA-SONOGRAFIA DOPPLER DE CAROTIDAS E VERTEBRAIS | 02.05.01.004-0 | doppler_outros | exame | 190 | 19 | 190 | 26 | 971,4 | 942,8 | 1.363,0 | 08/02/2023 | 0 | sem agendamento | I10 71, E11 23, E78 21, I70 21, I65 10 |
| ULTRA-SONOGRAFIA DOPPLER DE CAROTIDAS E VERTEBRAIS | 02.05.01.004-0 | doppler_outros | exame | 4 | 0 | 4 | 17 | 1.668,2 | 1.668,3 | 1.701,1 | 07/03/2022 | 0 | sem agendamento | E11 1, E14 1, I10 1, E78 1 |
| ULTRA-SONOGRAFIA DOPPLER COLORIDO DE VASOS | 02.05.01.004-0 | doppler_outros | exame | 169 | 169 | 169 | 0 | 31,0 | 34,3 | 61,1 | 02/09/2026 | — | — | I83 56, I87 25, M79 8, R60 8, N18 7 |
| ECOGRAFIA TRANSVAGINAL COM DOPPLER | 02.05.01.004-0 | doppler_outros | exame | 133 | 89 | 133 | 151 | 563,0 | 419,4 | 1.397,4 | 05/01/2023 | 140 | 0,9 | Z01 21, N95 17, R10 14, Z12 10, D25 7 |
| ULTRASSONOGRAFIA COM DOPPLER COLORIDO DE ARTERIAS RENAIS | 02.05.01.004-0 | doppler_outros | exame | 92 | 92 | 92 | 5 | 199,3 | 167,2 | 515,3 | 05/06/2025 | 16 | 5,8 | I10 37, I15 22, N18 15, I70 4, R10 3 |
| ECOGRAFIA DE PROSTATA ( VIA ABDOMINAL ) | 02.05.02.010-0 | prostata | exame | 2.969 | 2.203 | 2.966 | 2.714 | 600,7 | 467,3 | 6.004,7 | 26/05/2010 | 4.158 | 0,7 | N40 1.749, Z12 246, N42 136, Z00 114, N41 100 |
| ECOGRAFIA DE TIREOIDE ADULTO | 02.05.02.012-7 | tireoide | exame | 2.988 | 2.360 | 2.988 | 2.749 | 496,4 | 376,3 | 2.125,1 | 07/01/2021 | 3.443 | 0,9 | E07 710, E04 590, E03 428, D34 139, Z01 111 |
| ULTRA-SONOGRAFIA DOPPLER DE TIREOIDE | 02.05.02.012-7 | tireoide | exame | 806 | 687 | 806 | 542 | 441,8 | 355,3 | 1.979,0 | 02/06/2021 | 433 | 1,9 | E07 241, E04 183, E03 114, E05 41, D44 41 |
| ECOGRAFIA DE TIREOIDE INFANTIL | 02.05.02.012-7 | tireoide | exame | 60 | 51 | 60 | 36 | 476,4 | 499,7 | 966,3 | 11/03/2024 | 97 | 0,6 | E03 26, E04 8, E07 6, E06 3, E66 3 |
| ECOGRAFIA DE MAMAS - BILATERAL | 02.05.02.009-7 | mama | exame | 12.950 | 8.510 | 12.928 | 7.731 | 628,8 | 518,4 | 6.129,7 | 21/01/2010 | 10.474 | 1,2 | N63 3.381, Z12 2.707, N64 2.092, Z01 1.449, N95 559 |
| ULTRA-SONOGRAFIA DOPPLER VENOSO - MMII ( BILATERAL) | 02.05.01.004-0 | doppler_membros | exame | 10.045 | 6.060 | 10.043 | 599 | 631,2 | 578,1 | 1.477,3 | 17/10/2022 | 3.496 | 2,9 | I83 5.333, I87 2.042, I82 577, M79 352, R60 281 |
| ULTRA-SONOGRAFIA DOPPLER ARTERIAL - MMII (BILATERAL) | 02.05.01.004-0 | doppler_membros | exame | 1.800 | 1.358 | 1.800 | 331 | 475,1 | 396,4 | 1.442,3 | 21/11/2022 | 519 | 3,5 | I70 398, I83 379, I73 356, I87 136, M79 93 |
| ULTRA-SONOGRAFIA DOPPLER VENOSO - MMSS ( BILATERAL) | 02.05.01.004-0 | doppler_membros | exame | 144 | 139 | 144 | 207 | 165,1 | 113,6 | 866,3 | 19/06/2024 | 100 | 1,4 | I83 39, I87 23, I82 17, N18 12, I80 9 |
| ULTRA-SONOGRAFIA DOPPLER ARTERIAL - MMSS (BILATERAL) | 02.05.01.004-0 | doppler_membros | exame | 54 | 52 | 54 | 85 | 249,0 | 267,2 | 787,2 | 06/09/2024 | 92 | 0,6 | I77 5, N18 5, I25 5, I73 4, I10 3 |
| ECOGRAFIA PELVICA (GINECOLOGICA) - ADULTO | 02.05.02.016-0 | pelvica | exame | 573 | 339 | 573 | 837 | 722,2 | 445,3 | 2.126,1 | 06/01/2021 | 950 | 0,6 | R10 117, N94 81, N92 55, E28 42, Z01 39 |
| ECOGRAFIA PELVICA (GINECOLOGICA) - INFANTIL | 02.05.02.016-0 | pelvica | exame | 441 | 360 | 441 | 83 | 473,7 | 348,3 | 2.113,0 | 19/01/2021 | 417 | 1,1 | E30 181, E22 56, R10 39, Z00 30, N92 20 |
| 053. TC DO TORAX ADULTO S/CONTRASTE S/SEDACAO | 02.06.02.003-1 | tc_torax | exame | 180 | 177 | 180 | 2.167 | 37,0 | 7,1 | 1.057,2 | 11/12/2023 | 18.474 | 0,0 | C50 25, J44 16, R91 12, R06 8, C18 7 |
| 055. TC DO TORAX ADULTO C/CONTRASTE S/SEDACAO | 02.06.02.003-1 | tc_torax | exame | 2.349 | 2.340 | 2.347 | 1.864 | 132,5 | 131,1 | 966,3 | 11/03/2024 | 5.981 | 0,4 | C50 557, C18 246, C20 123, C16 93, C34 76 |
| ANGIOTOMOGRAFIA DA AORTA TORÁCICA E SEUS RAMOS ADULTO S/SEDACAO | 02.06.02.003-1 | tc_torax | exame | 357 | 357 | 357 | 176 | 200,5 | 174,1 | 543,9 | 07/05/2025 | 653 | 0,5 | I71 173, I35 46, I50 16, Q25 13, I70 13 |
| ANGIOTOMOGRAFIA DO TORAX OU PULMONAR ADULTO S/SEDACAO | 02.06.02.003-1 | tc_torax | exame | 328 | 328 | 328 | 596 | 134,4 | 111,1 | 545,0 | 06/05/2025 | 1.311 | 0,3 | I26 121, I71 36, I27 23, R06 23, I73 11 |
| 029. TC DE CRANIO ADULTO S/CONTRASTE S/SEDACAO | 02.06.01.007-9 | tc_cranio | exame | 44 | 44 | 44 | 764 | 33,1 | 7,0 | 325,4 | 12/12/2025 | 8.489 | 0,0 | R51 12, G44 4, R42 4, G40 2, H81 2 |
| ANGIOTOMOGRAFIA DO CRANIO ADULTO S/SEDACAO | 02.06.01.007-9 | tc_cranio | exame | 385 | 385 | 385 | 255 | 79,5 | 74,4 | 724,2 | 08/11/2024 | 1.634 | 0,2 | I67 119, I64 50, R51 36, I63 33, I65 22 |
| 031. TC DE CRANIO ADULTO C/CONTRASTE S/SEDACAO | 02.06.01.007-9 | tc_cranio | exame | 372 | 365 | 372 | 1.117 | 128,7 | 116,2 | 850,3 | 05/07/2024 | 1.909 | 0,2 | R51 77, C50 42, G43 15, C34 11, C43 10 |
| 071. TC DE FACE ADULTO C/CONTRASTE S/SEDACAO | 02.06.01.004-4 | tc_face | exame | 88 | 87 | 88 | 60 | 132,1 | 129,0 | 850,3 | 05/07/2024 | 211 | 0,4 | C44 9, C04 6, J34 5, C10 5, C30 5 |
| 079. TC DE SEIOS DE FACE ADULTO C/CONTRASTE S/SEDACAO | 02.06.01.004-4 | tc_face | exame | 51 | 50 | 51 | 87 | 117,0 | 98,2 | 845,1 | 10/07/2024 | 152 | 0,3 | J34 5, J01 4, C11 4, J32 4, C31 3 |
| ECOGRAFIA TRANSVAGINAL | 02.05.02.018-6 | transvaginal | exame | 9.294 | 5.699 | 9.293 | 8.953 | 658,9 | 528,3 | 5.893,7 | 14/09/2010 | 18.028 | 0,5 | Z01 2.704, N95 1.210, R10 711, Z12 690, Z00 592 |

## Varredura das filas

Toda fila que a varredura achou, pelo código, pelo nome e, na OCI, pelo CID aceito e pelo da finalidade, nas tabelas de solicitações e de agendamentos. A decisão é a do enquadramento do plano; fila sem decisão sai **a decidir** e não entra na soma.

| fila | código | tabela | achada por | objeto | fila | fila viva | pessoas | devolvidas | espera média | pedido mais antigo | agendadas 12 m | CID principais | no CID do objeto | parte no CID aceito (calculado) | decisão | motivo |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ECOGRAFIA DE MAMAS - BILATERAL | 02.05.02.009-7 | solicitações | código, nome | mama | 12.950 | 8.510 | 12.928 | 7.731 | 628,8 | 21/01/2010 | 10.474 | N63 3.381, Z12 2.707, N64 2.092, Z01 1.449, N95 559 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DOPPLER VENOSO - MMII ( BILATERAL) | 02.05.01.004-0 | solicitações | código, nome | doppler_membros, doppler_outros | 10.045 | 6.060 | 10.043 | 599 | 631,2 | 17/10/2022 | 3.496 | I83 5.333, I87 2.042, I82 577, M79 352, R60 281 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ECOGRAFIA DE ABDOMEN TOTAL ADULTO | 02.05.02.004-6 | solicitações | código, nome | abdomen_total, parede | 9.895 | 7.386 | 9.890 | 11.564 | 554,2 | 26/01/2010 | 8.207 | R10 3.302, K76 1.277, K80 725, E66 434, K30 293 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ECOGRAFIA TRANSVAGINAL | 02.05.02.018-6 | solicitações | código, nome | doppler_outros, transvaginal | 9.294 | 5.699 | 9.293 | 8.953 | 658,9 | 14/09/2010 | 18.028 | Z01 2.704, N95 1.210, R10 711, Z12 690, Z00 592 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| 10. ECODOPPLER DE CAROTIDAS | 02.05.01.004-0 | solicitações | código, nome | doppler_membros, doppler_outros | 4.143 | 4.143 | 4.143 | 2.776 | 136,6 | 20/03/2025 | 8.258 | I10 944, I50 419, I25 419, E78 287, I20 240 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| 063. TC DO ABDOMEN SUPERIOR ADULTO C/CONTRASTE S/SEDACAO | 02.06.03.001-0 | solicitações | código, nome | tc_abdomen | 4.116 | 4.101 | 4.112 | 5.271 | 129,5 | 05/07/2024 | 8.164 | C50 762, C18 388, R10 321, C20 149, C16 147 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ECOGRAFIA DO APARELHO URINARIO (RINS, BEXIGA) ADULTO | 02.05.02.005-4 | solicitações | código, nome | urinario | 3.677 | 2.398 | 3.675 | 3.434 | 653,2 | 22/12/2010 | 4.119 | N20 832, N18 468, N39 332, N40 258, R31 223 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| 111. TC DE PELVE OU BACIA ADULTO C/CONTRASTE S/SEDACAO | 02.06.03.003-7 | solicitações | código, nome | tc_pelve | 3.639 | 3.629 | 3.637 | 3.718 | 129,1 | 05/07/2024 | 7.036 | C50 613, C18 361, R10 305, C16 139, C20 120 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ULTRASONOGRAFIA DE PAREDE ABDOMINAL | 02.05.02.004-6 | solicitações | código, nome | abdomen_total, parede | 3.304 | 2.199 | 3.304 | 1.278 | 598,6 | 14/02/2020 | 1.470 | K42 870, K40 842, K46 486, R10 307, K43 192 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ECOGRAFIA DE TIREOIDE ADULTO | 02.05.02.012-7 | solicitações | código, nome | tireoide | 2.988 | 2.360 | 2.988 | 2.749 | 496,4 | 07/01/2021 | 3.443 | E07 710, E04 590, E03 428, D34 139, Z01 111 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ECOGRAFIA DE PROSTATA ( VIA ABDOMINAL ) | 02.05.02.010-0 | solicitações | código, nome | prostata | 2.969 | 2.203 | 2.966 | 2.714 | 600,7 | 26/05/2010 | 4.158 | N40 1.749, Z12 246, N42 136, Z00 114, N41 100 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| 055. TC DO TORAX ADULTO C/CONTRASTE S/SEDACAO | 02.06.02.003-1 | solicitações | código, nome | tc_torax | 2.349 | 2.340 | 2.347 | 1.864 | 132,5 | 11/03/2024 | 5.981 | C50 557, C18 246, C20 123, C16 93, C34 76 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ECOGRAFIA DE ABDOMEN SUPERIOR ADULTO | 02.05.02.003-8 | solicitações | código, nome | abdomen_superior | 2.213 | 1.229 | 2.211 | 984 | 688,1 | 22/09/2010 | 2.449 | K76 663, R10 382, K80 236, E66 115, K30 92 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DOPPLER ARTERIAL - MMII (BILATERAL) | 02.05.01.004-0 | solicitações | código, nome | doppler_membros, doppler_outros | 1.800 | 1.358 | 1.800 | 331 | 475,1 | 21/11/2022 | 519 | I70 398, I83 379, I73 356, I87 136, M79 93 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ANGIOTOMOGRAFIA DAS ARTÉRIAS CORONARIAS ADULTO S/SEDACAO | 02.06.02.003-1 | solicitações | código | tc_torax | 1.532 | 1.531 | 1.532 | 138 | 292,9 | 15/10/2024 | 137 | I20 447, I25 410, I50 128, R07 128, I10 55 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC DO TORAX ADULTO S/CONTRASTE S/SEDACAO EMERGENCIA | 02.06.02.003-1 | solicitações | código | tc_torax | 895 | 857 | 895 | 79 | 355,9 | 06/12/2016 | 1.983 | J18 178, I25 75, J44 43, C50 38, J15 31 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DOPPLER DE TIREOIDE | 02.05.02.012-7 | solicitações | código, nome | tireoide | 806 | 687 | 806 | 542 | 441,8 | 02/06/2021 | 433 | E07 241, E04 183, E03 114, E05 41, D44 41 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| TC DO ABDOMEN SUPER.ADULTO C/CONTRASTE S/SEDACAO EMERG. | 02.06.03.001-0 | solicitações | código | tc_abdomen | 726 | 696 | 726 | 85 | 364,2 | 27/09/2024 | 1.516 | R10 158, C18 33, C50 33, Z54 32, K85 23 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA DE BOLSA ESCROTAL ADULTO | 02.05.02.007-0 | solicitações | código, nome | bolsa_escrotal | 700 | 428 | 700 | 430 | 605,0 | 27/01/2021 | 627 | N51 164, N43 91, K40 80, I86 60, N50 58 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| TC DE PELVE OU BACIA ADULTO C/CONTRASTE S/SEDACAO EMERG. | 02.06.03.003-7 | solicitações | código | tc_pelve | 674 | 645 | 674 | 68 | 356,3 | 27/09/2024 | 1.328 | R10 133, Z54 33, C18 30, C50 28, K85 18 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA PELVICA (GINECOLOGICA) - ADULTO | 02.05.02.016-0 | solicitações | código, nome | pelvica | 573 | 339 | 573 | 837 | 722,2 | 06/01/2021 | 950 | R10 117, N94 81, N92 55, E28 42, Z01 39 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| 119. TC DE PESCOCO ADULTO C/CONTRASTE S/SEDACAO | 02.06.01.005-2 | solicitações | código, nome | tc_pescoco | 479 | 477 | 478 | 337 | 126,8 | 08/07/2024 | 1.361 | C32 41, C73 28, C83 25, C10 23, C44 20 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ECOGRAFIA DE ABDOMEN TOTAL INFANTIL | 02.05.02.004-6 | solicitações | código, nome | abdomen_total, parede | 452 | 286 | 452 | 433 | 586,5 | 22/02/2021 | 1.067 | R10 178, E66 75, Q90 16, K42 15, K59 12 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ECOGRAFIA PELVICA (GINECOLOGICA) - INFANTIL | 02.05.02.016-0 | solicitações | código, nome | pelvica | 441 | 360 | 441 | 83 | 473,7 | 19/01/2021 | 417 | E30 181, E22 56, R10 39, Z00 30, N92 20 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| TC DO ABDOMEN SUPER.ADULTO S/CONTRASTE S/SEDACAO EMERG. | 02.06.03.001-0 | solicitações | código | tc_abdomen | 393 | 380 | 393 | 69 | 371,2 | 06/12/2016 | 721 | R10 105, N20 23, Z54 13, K56 10, N18 8 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC DE CRANIO ADULTO S/CONTRASTE S/SEDACAO EMERGENCIA | 02.06.01.007-9 | solicitações | código | tc_cranio | 386 | 373 | 386 | 80 | 380,1 | 23/09/2024 | 1.087 | I64 57, R51 33, S06 23, R41 22, I63 18 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ANGIOTOMOGRAFIA DO CRANIO ADULTO S/SEDACAO | 02.06.01.007-9 | solicitações | código, nome | tc_cranio | 385 | 385 | 385 | 255 | 79,5 | 08/11/2024 | 1.634 | I67 119, I64 50, R51 36, I63 33, I65 22 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| 031. TC DE CRANIO ADULTO C/CONTRASTE S/SEDACAO | 02.06.01.007-9 | solicitações | código, nome | tc_cranio | 372 | 365 | 372 | 1.117 | 128,7 | 05/07/2024 | 1.909 | R51 77, C50 42, G43 15, C34 11, C43 10 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| TC DE PELVE OU BACIA ADULTO S/CONTRASTE S/SEDACAO EMERG. | 02.06.03.003-7 | solicitações | código | tc_pelve | 370 | 356 | 370 | 65 | 372,9 | 06/12/2016 | 658 | R10 93, N20 15, Z54 13, S72 9, T81 9 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ANGIOTOMOGRAFIA DA AORTA TORÁCICA E SEUS RAMOS ADULTO S/SEDACAO | 02.06.02.003-1 | solicitações | código, nome | tc_torax | 357 | 357 | 357 | 176 | 200,5 | 07/05/2025 | 653 | I71 173, I35 46, I50 16, Q25 13, I70 13 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ANGIOTOMOGRAFIA DO TORAX OU PULMONAR ADULTO S/SEDACAO | 02.06.02.003-1 | solicitações | código, nome | tc_torax | 328 | 328 | 328 | 596 | 134,4 | 06/05/2025 | 1.311 | I26 121, I71 36, I27 23, R06 23, I73 11 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ANGIOTOMOGRAFIA DA AORTA ABDOMINAL E DOS SEUS RAMOS ADULTO S/SEDACAO | 02.06.03.001-0 | solicitações | código, nome | tc_abdomen | 323 | 323 | 323 | 145 | 199,5 | 15/07/2025 | 605 | I71 141, I70 26, I35 24, N18 23, I73 9 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| TC DO TORAX ADULTO C/CONTRASTE S/SEDACAO EMERGENCIA | 02.06.02.003-1 | solicitações | código | tc_torax | 305 | 292 | 305 | 30 | 361,0 | 26/09/2024 | 979 | I26 19, C50 18, J18 14, C53 14, C34 13 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA DO APARELHO URINARIO (RINS, BEXIGA) INFANTIL | 02.05.02.005-4 | solicitações | código, nome | urinario | 276 | 211 | 276 | 655 | 474,6 | 21/01/2021 | 789 | N39 50, Q17 15, Q62 14, N20 12, P70 11 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA TRANSFONTANELA | 02.05.02.017-8 | solicitações | código, nome | transfontanela | 270 | 243 | 270 | 201 | 309,0 | 22/06/2022 | 818 | Q75 61, P21 44, P07 21, P05 16, Q02 13 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ANGIOTOMOGRAFIA DA PELVE ADULTO S/SEDACAO | 02.06.03.003-7 | solicitações | código, nome | tc_pelve | 253 | 253 | 253 | 142 | 218,7 | 17/07/2025 | 330 | N18 40, I82 39, I71 37, K55 15, I70 14 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ANGIOTOMOGRAFIA DO ABDOME SUPERIOR ADULTO S/SEDACAO | 02.06.03.001-0 | solicitações | código, nome | tc_abdomen | 245 | 245 | 245 | 130 | 220,2 | 07/05/2025 | 309 | I71 46, N18 36, K55 20, I82 19, I70 11 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ANGIOTOMOGRAFIA DAS ARTERIAS CAROTIDAS E VERTEBRAIS ADULTO S/SEDACAO | 02.06.03.001-0 | solicitações | código, nome | tc_abdomen | 243 | 243 | 243 | 130 | 135,0 | 19/08/2025 | 541 | I65 76, I64 33, I63 25, I25 19, I70 13 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ECOGRAFIA DE BOLSA ESCROTAL INFANTIL | 02.05.02.007-0 | solicitações | código, nome | bolsa_escrotal | 234 | 171 | 234 | 71 | 490,8 | 11/02/2021 | 316 | Q53 97, N43 49, K40 21, N51 18, Q55 10 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| TOMOGRAFIA CONE BEAN | 02.06.01.004-4 | solicitações | código | tc_face | 195 | 195 | 195 | 203 | 94,6 | 23/01/2026 | 343 | K01 116, K04 27, S02 15, K08 12, K10 6 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DOPPLER DE CAROTIDAS E VERTEBRAIS | 02.05.01.004-0 | solicitações | código, nome | doppler_membros, doppler_outros | 190 | 19 | 190 | 26 | 971,4 | 08/02/2023 | 0 | I10 71, E11 23, E78 21, I70 21, I65 10 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| 053. TC DO TORAX ADULTO S/CONTRASTE S/SEDACAO | 02.06.02.003-1 | solicitações | código, nome | tc_torax | 180 | 177 | 180 | 2.167 | 37,0 | 11/12/2023 | 18.474 | C50 25, J44 16, R91 12, R06 8, C18 7 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ANGIOTOMOGRAFIA DO PESCOCO ADULTO S/SEDACAO | 02.06.01.005-2 | solicitações | código, nome | tc_pescoco | 178 | 178 | 178 | 188 | 102,9 | 23/02/2026 | 414 | I65 37, I64 32, I63 22, I70 12, I67 9 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DOPPLER COLORIDO DE VASOS | 02.05.01.004-0 | solicitações | código, nome | doppler_membros, doppler_outros | 169 | 169 | 169 | 0 | 31,0 | 02/09/2026 | — | I83 56, I87 25, M79 8, R60 8, N18 7 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DOPPLER VENOSO - MMSS ( BILATERAL) | 02.05.01.004-0 | solicitações | código, nome | doppler_membros, doppler_outros | 144 | 139 | 144 | 207 | 165,1 | 19/06/2024 | 100 | I83 39, I87 23, I82 17, N18 12, I80 9 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| TC DE CRANIO ADULTO C/CONTRASTE S/SEDACAO EMERGENCIA | 02.06.01.007-9 | solicitações | código | tc_cranio | 134 | 127 | 134 | 10 | 372,6 | 24/09/2024 | 461 | C50 18, I64 10, C79 7, C34 6, R41 5 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA TRANSVAGINAL COM DOPPLER | 02.05.01.004-0 | solicitações | código, nome | doppler_membros, doppler_outros, transvaginal | 133 | 89 | 133 | 151 | 563,0 | 05/01/2023 | 140 | Z01 21, N95 17, R10 14, Z12 10, D25 7 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ULTRASSONOGRAFIA COM DOPPLER COLORIDO DE ARTERIAS RENAIS | 02.05.01.004-0 | solicitações | código, nome | doppler_membros, doppler_outros | 92 | 92 | 92 | 5 | 199,3 | 05/06/2025 | 16 | I10 37, I15 22, N18 15, I70 4, R10 3 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| 071. TC DE FACE ADULTO C/CONTRASTE S/SEDACAO | 02.06.01.004-4 | solicitações | código, nome | tc_face | 88 | 87 | 88 | 60 | 132,1 | 05/07/2024 | 211 | C44 9, C04 6, J34 5, C10 5, C30 5 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ULTRASSONOGRAFIA RENAL | 02.05.02.005-4 | solicitações | código, nome | urinario | 72 | 45 | 72 | 15 | 629,3 | 23/02/2023 | 18 | N20 16, N18 9, R31 6, I10 5, Q61 4 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| 061. TC DO ABDOMEN SUPERIOR ADULTO S/CONTRASTE S/SEDACAO | 02.06.03.001-0 | solicitações | código, nome | tc_abdomen | 68 | 68 | 68 | 1.489 | 19,1 | 25/03/2026 | 5.496 | N20 22, R10 15, N18 3, C50 2, K45 2 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| TC DE CRANIO INFANTIL S/CONTRASTE S/SEDACAO EMERGENCIA | 02.06.01.007-9 | solicitações | código | tc_cranio | 68 | 67 | 68 | 4 | 344,6 | 16/10/2024 | 40 | R56 15, G40 9, P35 7, P37 4, G91 2 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC DE PESCOCO ADULTO C/CONTRASTE / S/SEDACAO EMERGENCIA | 02.06.01.005-2 | solicitações | código | tc_pescoco | 60 | 56 | 60 | 3 | 359,7 | 24/09/2024 | 123 | L02 4, C15 3, C76 3, R13 3, I64 3 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA DE TIREOIDE INFANTIL | 02.05.02.012-7 | solicitações | código, nome | tireoide | 60 | 51 | 60 | 36 | 476,4 | 11/03/2024 | 97 | E03 26, E04 8, E07 6, E06 3, E66 3 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| 109. TC DE PELVE OU BACIA ADULTO S/CONTRASTE S/SEDACAO | 02.06.03.003-7 | solicitações | código, nome | tc_pelve | 57 | 57 | 57 | 952 | 21,5 | 27/01/2026 | 5.469 | N20 18, R10 13, N18 3, M79 2, K86 2 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DOPPLER ARTERIAL - MMSS (BILATERAL) | 02.05.01.004-0 | solicitações | código, nome | doppler_membros, doppler_outros | 54 | 52 | 54 | 85 | 249,0 | 06/09/2024 | 92 | I77 5, N18 5, I25 5, I73 4, I10 3 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| 079. TC DE SEIOS DE FACE ADULTO C/CONTRASTE S/SEDACAO | 02.06.01.004-4 | solicitações | código, nome | tc_face | 51 | 50 | 51 | 87 | 117,0 | 10/07/2024 | 152 | J34 5, J01 4, C11 4, J32 4, C31 3 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ECOGRAFIA PELVICA | 02.05.02.006-2 | solicitações | nome | pelvica | 47 | 47 | 47 | 15 | 93,1 | 13/05/2026 | 21 | R10 10, K40 7, Z01 4, M65 3, N92 3 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 029. TC DE CRANIO ADULTO S/CONTRASTE S/SEDACAO | 02.06.01.007-9 | solicitações | código, nome | tc_cranio | 44 | 44 | 44 | 764 | 33,1 | 12/12/2025 | 8.489 | R51 12, G44 4, R42 4, G40 2, H81 2 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| TC DO TORAX INFANTIL S/CONTRASTE S/SEDACAO EMERGENCIA | 02.06.02.003-1 | solicitações | código | tc_torax | 44 | 43 | 44 | 0 | 343,7 | 03/10/2024 | 8 | J18 14, J15 4, P27 4, J98 3, J91 3 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ANGIOTOMOGRAFIA DAS ARTÉRIAS RENAIS ADULTO S/SEDACAO | 02.06.03.001-0 | solicitações | código, nome | tc_abdomen | 36 | 36 | 36 | 11 | 160,4 | 29/08/2025 | 47 | I15 15, I10 4, I77 3, I72 2, Z95 1 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| TC DO ABDOMEN SUPER.INFANTIL C/CONTRASTE S/SEDACAO EMERG. | 02.06.03.001-0 | solicitações | código | tc_abdomen | 33 | 33 | 33 | 1 | 349,5 | 07/11/2024 | 16 | R10 9, A41 2, C25 2, R16 2, A09 2 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC DE PELVE OU BACIA INFANTIL C/CONTRASTE S/SEDACAO EMERG. | 02.06.03.003-7 | solicitações | código | tc_pelve | 31 | 30 | 31 | 3 | 347,9 | 08/10/2024 | 18 | R10 6, C18 2, C34 2, R50 2, K57 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC DE PESCOCO ADULTO S/CONTRASTE / S/SEDACAO EMERGENCIA | 02.06.01.005-2 | solicitações | código | tc_pescoco | 29 | 29 | 29 | 1 | 293,5 | 16/11/2024 | 25 | J95 4, R63 1, E05 1, D48 1, C78 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 095. TC DE MASTOIDES ADULTO C/CONTRASTE S/SEDACAO | 02.06.01.004-4 | solicitações | código | tc_face | 28 | 28 | 28 | 68 | 99,8 | 04/03/2026 | 127 | H66 5, H90 4, H93 3, C44 3, H70 3 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC DO TORAX INFANTIL C/CONTRASTE S/SEDACAO EMERGENCIA | 02.06.02.003-1 | solicitações | código | tc_torax | 23 | 23 | 23 | 0 | 344,4 | 06/11/2024 | 11 | J18 8, R10 3, J15 1, R06 1, R84 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC DE CRANIO INFANTIL C/CONTRASTE S/SEDACAO EMERGENCIA | 02.06.01.007-9 | solicitações | código | tc_cranio | 23 | 23 | 23 | 1 | 347,0 | 25/03/2025 | 10 | R56 5, G40 2, G11 2, R22 1, C25 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC DE FACE ADULTO S/CONTRASTE S/SEDACAO EMERGENCIA | 02.06.01.004-4 | solicitações | código | tc_face | 18 | 18 | 18 | 4 | 354,6 | 08/11/2024 | 25 | J01 3, I64 2, R51 2, S06 1, E05 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRASSONOGRAFIA COM DOPPLER COLORIDO DA BOLSA ESCROTAL | 02.05.02.007-0 | solicitações | código | bolsa_escrotal | 18 | 15 | 18 | 2 | 412,2 | 25/06/2024 | 0 | N51 5, Q53 4, I86 2, N43 2, N45 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA DE ABDOMEN SUPERIOR INFANTIL | 02.05.02.003-8 | solicitações | código | abdomen_superior | 15 | 11 | 15 | 17 | 525,6 | 25/03/2021 | 124 | K76 3, R10 3, Q53 1, K80 1, K83 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC DE PELVE OU BACIA INFANTIL S/CONTRASTE S/SEDACAO EMERG. | 02.06.03.003-7 | solicitações | código | tc_pelve | 15 | 15 | 15 | 1 | 463,4 | 27/12/2024 | 9 | R10 3, A41 1, K56 1, C16 1, C61 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC DE SEIOS DE FACE ADULTO S/CONTRASTE S/SEDACAO EMERG. | 02.06.01.004-4 | solicitações | código | tc_face | 13 | 13 | 13 | 3 | 341,1 | 06/02/2025 | 35 | J01 2, R51 2, S02 1, M30 1, C61 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC DO ABDOMEN SUPER.INFANTIL S/CONTRASTE S/SEDACAO EMERG. | 02.06.03.001-0 | solicitações | código | tc_abdomen | 13 | 12 | 13 | 0 | 386,0 | 01/10/2024 | 12 | R50 2, R19 1, J15 1, K81 1, R10 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ANGIOTOMOGRAFIA DO SISTEMA PORTA (VASOS HEPÁTICOS) ADULTO S/SEDACAO | 02.06.03.001-0 | solicitações | código | tc_abdomen | 12 | 12 | 12 | 8 | 229,3 | 02/09/2025 | 10 | I82 4, I81 4, C50 1, K83 1, I80 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ANGIOTOMOGRAFIA DAS ARTÉRIAS CORONARIAS INFANTIL S/SEDACAO | 02.06.02.003-1 | solicitações | código | tc_torax | 12 | 12 | 12 | 4 | 267,0 | 31/01/2025 | — | Q24 4, Q25 3, I77 1, R07 1, Q21 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DOPPLER DE AORTA E VASOS ILIACOS | 02.05.01.004-0 | solicitações | código | doppler_membros, doppler_outros | 11 | 11 | 11 | 1 | 55,5 | 13/08/2026 | 20 | N18 3, E88 1, I10 1, I87 1, E78 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC DE MASTOIDES INFANTIL S/CONTRASTE S/SEDACAO EMERGENCIA | 02.06.01.004-4 | solicitações | código | tc_face | 11 | 11 | 11 | 1 | 409,7 | 18/11/2024 | 0 | H70 5, H66 3, H65 2, L03 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DOPPLER VENOSO - MIE | 02.05.01.004-0 | solicitações | código | doppler_membros, doppler_outros | 10 | 0 | 10 | 439 | 1.608,8 | 15/09/2021 | 0 | I83 8, G83 1, M79 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 077. TC DE SEIOS DE FACE ADULTO S/CONTRASTE S/SEDACAO | 02.06.01.004-4 | solicitações | código | tc_face | 9 | 9 | 9 | 121 | 6,8 | 26/10/2026 | 1.987 | J32 3, J34 2, C44 1, J33 1, J01 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 093. TC DE MASTOIDES ADULTO S/CONTRASTE S/SEDACAO | 02.06.01.004-4 | solicitações | código | tc_face | 9 | 9 | 9 | 55 | 6,5 | 26/10/2026 | 1.167 | H72 2, H93 1, H90 1, H65 1, H83 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ANGIOTOMOGRAFIA DA AORTA TORÁCICA E SEUS RAMOS INFANTIL S/SEDACAO | 02.06.02.003-1 | solicitações | código | tc_torax | 9 | 9 | 9 | 10 | 162,4 | 31/07/2025 | 14 | Q25 5, I10 1, Q21 1, I71 1, I70 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRASSONOGRAFIA COM DOPPLER COLORIDO DOS TESTICULOS | 02.05.02.007-0 | solicitações | código | bolsa_escrotal | 9 | 9 | 9 | 2 | 405,3 | 20/01/2025 | 1 | N51 6, Q53 1, E29 1, N49 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DOPPLER VENOSO - MID | 02.05.01.004-0 | solicitações | código | doppler_membros, doppler_outros | 8 | 0 | 8 | 483 | 1.568,4 | 04/03/2022 | 0 | I83 5, I87 2, G63 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC DE MASTOIDES INFANTIL C/CONTRASTE S/SEDACAO EMERGENCIA | 02.06.01.004-4 | solicitações | código | tc_face | 7 | 7 | 7 | 0 | 415,8 | 14/03/2025 | 1 | H70 4, H66 2, H65 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC DE PESCOCO INFANTIL C/CONTRASTE / S/SEDACAO EMERGENCIA | 02.06.01.005-2 | solicitações | código | tc_pescoco | 6 | 6 | 6 | 0 | 398,4 | 04/06/2025 | 4 | L04 2, J39 2, J96 1, R45 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 117. TC DE PESCOCO ADULTO S/CONTRASTE S/SEDACAO | 02.06.01.005-2 | solicitações | código | tc_pescoco | 5 | 5 | 5 | 58 | 6,3 | 26/10/2026 | 479 | M35 1, R49 1, E07 1, C73 1, D44 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 103. TC DE OUVIDOS ADULTO C/CONTRASTE S/SEDACAO | 02.06.01.004-4 | solicitações | código | tc_face | 5 | 5 | 5 | 23 | 102,2 | 16/04/2026 | 40 | H90 2, H92 1, H93 1, Q17 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC DE FACE ADULTO C/CONTRASTE S/SEDACAO EMERGENCIA | 02.06.01.004-4 | solicitações | código | tc_face | 5 | 5 | 5 | 3 | 403,4 | 05/02/2025 | 29 | L30 1, G45 1, C79 1, L02 1, C69 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRASSONOGRAFIA DAS GLANDULAS PAROTIDAS | 02.05.01.004-0 | solicitações | código | doppler_membros, doppler_outros | 5 | 5 | 5 | 2 | 81,0 | 12/08/2026 | 18 | K11 2, Q76 1, M35 1, D11 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DOPPLER DE ARTERIA AORTA ABDOMINAL | 02.05.01.004-0 | solicitações | código | doppler_membros, doppler_outros | 5 | 5 | 5 | 3 | 35,6 | 10/09/2026 | 16 | I25 2, E66 1, I50 1, I71 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DO APARELHO URINARIO (RINS, BEXIGA) | 02.05.02.005-4 | solicitações | código | urinario | 5 | 0 | 5 | 0 | 1.533,3 | 27/07/2022 | 0 | N18 1, N28 1, N20 1, N40 1, I70 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 025. TC DE CRANIO INFANTIL S/CONTRASTE S/SEDACAO | 02.06.01.007-9 | solicitações | código | tc_cranio | 4 | 4 | 4 | 96 | 24,2 | 04/10/2026 | 829 | H53 1, S06 1, R56 1, S09 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 027. TC DE CRANIO INFANTIL C/CONTRASTE S/SEDACAO | 02.06.01.007-9 | solicitações | código | tc_cranio | 4 | 4 | 4 | 48 | 24,5 | 04/10/2026 | 149 | G06 2, H53 1, R51 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC DE FACE INFANTIL S/CONTRASTE S/SEDACAO EMERGENCIA | 02.06.01.004-4 | solicitações | código | tc_face | 4 | 4 | 4 | 1 | 514,8 | 31/03/2025 | 4 | J35 1, L02 1, J01 1, G51 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC DE PESCOCO INFANTIL S/CONTRASTE / S/SEDACAO EMERGENCIA | 02.06.01.005-2 | solicitações | código | tc_pescoco | 4 | 4 | 4 | 0 | 292,6 | 04/06/2025 | 0 | L03 1, L04 1, R05 1, R50 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DOPPLER DE CAROTIDAS E VERTEBRAIS | 02.05.01.004-0 | solicitações | código, nome | doppler_membros, doppler_outros | 4 | 0 | 4 | 17 | 1.668,2 | 07/03/2022 | 0 | E11 1, E14 1, I10 1, E78 1 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| 069. TC DE FACE ADULTO S/CONTRASTE S/SEDACAO | 02.06.01.004-4 | solicitações | código | tc_face | 3 | 3 | 3 | 95 | 7,3 | 26/10/2026 | 613 | J34 1, Q38 1, J33 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ANGIOTOMOGRAFIA | 02.06.02.003-1 | solicitações | código, nome | tc_abdomen, tc_cranio, tc_pelve, tc_pescoco, tc_torax | 3 | 3 | 3 | 0 | 10,5 | 19/10/2026 | 268 | I26 2, I25 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 087. TC ARTIC. TEMP. MAND. (ATM) ADULTO C/CONTRASTE S/SEDACAO | 02.06.01.004-4 | solicitações | código | tc_face | 3 | 3 | 3 | 2 | 123,8 | 10/04/2026 | 7 | C91 1, R22 1, C03 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ANGIOTOMOGRAFIA DO CRANIO INFANTIL S/SEDACAO | 02.06.01.007-9 | solicitações | código | tc_cranio | 3 | 3 | 3 | 5 | 252,9 | 18/11/2025 | 7 | Q75 1, D18 1, I61 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC DE MASTOIDES ADULTO C/CONTRASTE S/SEDACAO EMERGENCIA | 02.06.01.004-4 | solicitações | código | tc_face | 3 | 3 | 3 | 0 | 325,5 | 12/02/2025 | 4 | G96 1, A49 1, H70 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DOPPLER COLORIDO DE UM VASO | 02.05.01.004-0 | solicitações | código | doppler_membros, doppler_outros | 3 | 0 | 3 | 2 | 1.525,3 | 30/08/2022 | 0 | N18 2, I73 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DE ABDOMEN TOTAL | 02.05.02.004-6 | solicitações | código | abdomen_total, parede | 3 | 0 | 3 | 1 | 1.525,2 | 30/08/2022 | 0 | Z10 1, C44 1, R10 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DE TIREOIDE | 02.05.02.012-7 | solicitações | código | tireoide | 3 | 0 | 3 | 0 | 1.525,1 | 30/08/2022 | 0 | N18 1, D44 1, E35 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DOPPLER ARTERIAL-M I D | 02.05.01.004-0 | solicitações | código | doppler_membros, doppler_outros | 3 | 0 | 3 | 0 | 1.536,3 | 27/07/2022 | 0 | L98 1, M79 1, I73 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DOPPLER VENOSO - MID | 02.05.01.004-0 | solicitações | código | doppler_membros, doppler_outros | 3 | 0 | 3 | 0 | 1.536,3 | 27/07/2022 | 0 | L98 1, M79 1, I73 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 026. TC DE CRANIO INFANTIL S/CONTRASTE C/SEDACAO | 02.06.01.007-9 | solicitações | código | tc_cranio | 2 | 2 | 2 | 38 | 46,4 | 26/08/2026 | 271 | S06 1, Q67 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 051. TC DO TORAX INFANTIL C/CONTRASTE S/SEDACAO | 02.06.02.003-1 | solicitações | código | tc_torax | 2 | 2 | 2 | 52 | 328,8 | 25/01/2025 | 58 | C18 1, D21 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ANGIOTOMOGRAFIA DO TORAX OU PULMONAR INFANTIL S/SEDACAO | 02.06.02.003-1 | solicitações | código | tc_torax | 2 | 2 | 2 | 7 | 136,1 | 09/02/2026 | 19 | Q24 1, Q21 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC DE SEIOS DE FACE ADULTO C/CONTRASTE S/SEDACAO EMERG. | 02.06.01.004-4 | solicitações | código | tc_face | 2 | 2 | 2 | 0 | 263,3 | 06/06/2025 | 12 | M86 1, A49 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ANGIOTOMOGRAFIA DA AORTA ABDOMINAL E DOS SEUS RAMOS INFANTIL S/SEDACAO | 02.06.03.001-0 | solicitações | código | tc_abdomen | 2 | 2 | 2 | 2 | 309,7 | 17/12/2025 | 3 | N39 1, I70 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC DE FACE INFANTIL C/CONTRASTE S/SEDACAO EMERGENCIA | 02.06.01.004-4 | solicitações | código | tc_face | 2 | 2 | 2 | 1 | 404,9 | 02/09/2025 | 1 | L03 1, L02 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| DOPPLER ARTERIAL DE MI | 02.05.01.004-0 | solicitações | código | doppler_membros, doppler_outros | 2 | 0 | 2 | 0 | 1.525,1 | 30/08/2022 | 0 | M79 1, I73 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| DOPPLER VENOSO DE MI | 02.05.01.004-0 | solicitações | código | doppler_membros, doppler_outros | 2 | 0 | 2 | 0 | 1.525,1 | 30/08/2022 | 0 | M79 1, I73 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA DO APARELHO URINARIO (RINS, BEXIGA) INFANTIL EMERG | 02.05.02.005-4 | solicitações | código, nome | urinario | 2 | 2 | 2 | 0 | 6,8 | 26/10/2026 | 0 | N20 1, N39 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC DE OUVIDOS ADULTO C/CONTRASTE S/SEDACAO EMERGENCIA | 02.06.01.004-4 | solicitações | código | tc_face | 2 | 2 | 2 | 0 | 432,2 | 23/05/2025 | 0 | G96 1, H70 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DOPPLER ARTERIAL- M I D | 02.05.01.004-0 | solicitações | código | doppler_membros, doppler_outros | 2 | 0 | 2 | 288 | 1.538,2 | 10/08/2022 | 0 | Z10 1, I83 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DOPPLER ARTERIAL- M I E | 02.05.01.004-0 | solicitações | código | doppler_membros, doppler_outros | 2 | 0 | 2 | 246 | 1.523,0 | 24/08/2022 | 0 | Z10 1, I83 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DE PROSTATA (VIA ABDOMINAL) | 02.05.02.010-0 | solicitações | código | prostata | 2 | 0 | 2 | 0 | 1.528,8 | 23/08/2022 | 0 | C44 1, N40 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DOPPLER DE ARTERIAS VERTEBRAIS | 02.05.01.004-0 | solicitações | código | doppler_membros, doppler_outros | 2 | 0 | 2 | 0 | 1.447,0 | 14/10/2022 | — | I10 1, R42 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA TRANSFONTANELAR | 02.05.02.017-8 | solicitações | código, nome | transfontanela | 2 | 0 | 2 | 0 | 1.525,3 | 30/08/2022 | 0 | P07 1, R56 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRASSONOGRAFIA DOPPLER ARTERIAL MEMBRO SUPERIOR E | 02.05.01.004-0 | solicitações | código | doppler_membros, doppler_outros | 2 | 0 | 2 | 0 | 1.525,4 | 30/08/2022 | 0 | N18 2 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 049. TC DO TORAX INFANTIL S/CONTRASTE S/SEDACAO | 02.06.02.003-1 | solicitações | código | tc_torax | 1 | 1 | 1 | 56 | 284,0 | 22/01/2026 | 153 | C56 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 073. TC DE SEIOS DE FACE INFANTIL S/CONTRASTE S/SEDACAO | 02.06.01.004-4 | solicitações | código | tc_face | 1 | 1 | 1 | 10 | 21,3 | 12/10/2026 | 132 | J01 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 059. TC DO ABDOMEN SUPERIOR INFANTIL C/CONTRASTE S/SEDACAO | 02.06.03.001-0 | solicitações | código | tc_abdomen | 1 | 1 | 1 | 122 | 11,3 | 22/10/2026 | 98 | D21 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 107. TC DE PELVE OU BACIA INFANTIL C/CONTRASTE S/SEDACAO | 02.06.03.003-7 | solicitações | código | tc_pelve | 1 | 1 | 1 | 138 | 11,3 | 22/10/2026 | 88 | D21 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 085. TC ARTIC. TEMP. MAND. (ATM) ADULTO S/CONTRASTE S/SEDACAO | 02.06.01.004-4 | solicitações | código | tc_face | 1 | 1 | 1 | 10 | 6,3 | 27/10/2026 | 77 | H92 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 030. TC DE CRANIO ADULTO S/CONTRASTE C/SEDACAO | 02.06.01.007-9 | solicitações | código | tc_cranio | 1 | 1 | 1 | 223 | 94,1 | 31/07/2026 | 72 | G80 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 028. TC DE CRANIO INFANTIL C/CONTRASTE C/SEDACAO | 02.06.01.007-9 | solicitações | código | tc_cranio | 1 | 1 | 1 | 36 | 20,3 | 13/10/2026 | 52 | G06 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 064. TC DO ABDOMEN SUPERIOR ADULTO C/CONTRASTE C/SEDACAO | 02.06.03.001-0 | solicitações | código | tc_abdomen | 1 | 1 | 1 | 238 | 223,4 | 24/03/2026 | 26 | N18 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 112. TC DE PELVE OU BACIA ADULTO C/CONTRASTE C/SEDACAO | 02.06.03.003-7 | solicitações | código | tc_pelve | 1 | 1 | 1 | 219 | 646,3 | 25/01/2025 | 23 | C18 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 060. TC DO ABDOMEN SUPERIOR INFANTIL C/CONTRASTE C/SEDACAO | 02.06.03.001-0 | solicitações | código | tc_abdomen | 1 | 1 | 1 | 20 | 291,3 | 15/01/2026 | 21 | R50 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 032. TC DE CRANIO ADULTO C/CONTRASTE C/SEDACAO | 02.06.01.007-9 | solicitações | código | tc_cranio | 1 | 1 | 1 | 67 | 103,4 | 22/07/2026 | 20 | F10 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 110. TC DE PELVE OU BACIA ADULTO S/CONTRASTE C/SEDACAO | 02.06.03.003-7 | solicitações | código | tc_pelve | 1 | 1 | 1 | 116 | 6,9 | 26/10/2026 | 13 | R10 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 091. TC DE MASTOIDES INFANTIL C/CONTRASTE S/SEDACAO | 02.06.01.004-4 | solicitações | código | tc_face | 1 | 1 | 1 | 1 | 5,4 | 28/10/2026 | 10 | H65 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 108. TC DE PELVE OU BACIA INFANTIL C/CONTRASTE C/SEDACAO | 02.06.03.003-7 | solicitações | código | tc_pelve | 1 | 1 | 1 | 13 | 291,3 | 15/01/2026 | 9 | R50 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC DE MASTOIDES ADULTO S/CONTRASTE S/SEDACAO EMERGENCIA | 02.06.01.004-4 | solicitações | código | tc_face | 1 | 1 | 1 | 0 | 634,1 | 06/02/2025 | 6 | H71 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ANGIOTOMOGRAFIA DAS ARTÉRIAS RENAIS INFANTIL S/SEDACAO | 02.06.03.001-0 | solicitações | código | tc_abdomen | 1 | 1 | 1 | 1 | 320,1 | 17/12/2025 | 2 | N39 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ANGIOTOMOGRAFIA DO PESCOCO INFANTIL S/SEDACAO | 02.06.01.005-2 | solicitações | código | tc_pescoco | 1 | 1 | 1 | 0 | 51,1 | 12/09/2026 | 2 | I82 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ANGIOTOMOGRAFIA DA PELVE INFANTIL S/SEDACAO | 02.06.03.003-7 | solicitações | código | tc_pelve | 1 | 1 | 1 | 0 | 51,1 | 12/09/2026 | 1 | I80 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC DE OUVIDOS ADULTO S/CONTRASTE S/SEDACAO EMERGENCIA | 02.06.01.004-4 | solicitações | código | tc_face | 1 | 1 | 1 | 0 | 76,4 | 18/08/2026 | 1 | H80 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC DE SEIOS DE FACE INFANTIL C/CONTRASTE S/SEDACAO EMERG. | 02.06.01.004-4 | solicitações | código | tc_face | 1 | 1 | 1 | 0 | 389,3 | 09/10/2025 | 1 | H65 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC DE SEIOS DE FACE INFANTIL S/CONTRASTE S/SEDACAO EMERG. | 02.06.01.004-4 | solicitações | código | tc_face | 1 | 1 | 1 | 0 | 515,4 | 05/06/2025 | 1 | J00 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA DE ABDOMEN TOTAL ADULTO EMERGENCIA | 02.05.02.004-6 | solicitações | código, nome | abdomen_total, parede | 1 | 1 | 1 | 0 | 8,7 | 25/10/2026 | 0 | R10 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA DE TIREOIDE ADULTO EMERGENCIA | 02.05.02.012-7 | solicitações | código, nome | tireoide | 1 | 0 | 1 | 0 | 7.007,7 | 27/08/2007 | 0 | R68 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA DOPPLER COLORIDO DE ORGAO | 02.05.01.004-0 | solicitações | código | doppler_membros, doppler_outros | 1 | 1 | 1 | 2 | 143,0 | 12/06/2026 | — | I65 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC ARTIC.TEMP.MAND.(ATM)ADULT.S/CONTRASTE S/SEDACAO EMERG. | 02.06.01.004-4 | solicitações | código | tc_face | 1 | 1 | 1 | 0 | 502,0 | 18/06/2025 | 0 | S02 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DOPPLER ARTERIAL- M S D | 02.05.01.004-0 | solicitações | código | doppler_membros, doppler_outros | 1 | 0 | 1 | 30 | 1.644,1 | 03/05/2022 | 0 | I83 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DOPPLER COLORIDO DE DOIS VASOS | 02.05.01.004-0 | solicitações | código | doppler_membros, doppler_outros | 1 | 0 | 1 | 12 | 1.700,3 | 08/03/2022 | — | I83 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DOPPLER COLORIDO DE ORGAO OU ESTRUTURA ISO | 02.05.01.004-0 | solicitações | código | doppler_membros, doppler_outros | 1 | 0 | 1 | 0 | 1.525,1 | 30/08/2022 | 0 | I73 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DOPPLER DE CAROTIDAS | 02.05.01.004-0 | solicitações | código, nome | doppler_membros, doppler_outros | 1 | 0 | 1 | 8 | 1.637,3 | 10/05/2022 | 0 | I10 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DE ABDOMEN SUPERIOR | 02.05.02.003-8 | solicitações | código | abdomen_superior | 1 | 0 | 1 | 0 | 1.525,1 | 30/08/2022 | 0 | K80 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DE BOLSA ESCROTAL COM DOPPLER | 02.05.01.004-0 | solicitações | código | doppler_membros, doppler_outros | 1 | 0 | 1 | 0 | 1.525,1 | 30/08/2022 | 0 | E29 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DE MAMAS (BILATERAL) | 02.05.02.009-7 | solicitações | código | mama | 1 | 0 | 1 | 0 | 1.525,1 | 30/08/2022 | 0 | N60 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DE PAREDE ABDOMINAL | 02.05.02.004-6 | solicitações | código | abdomen_total, parede | 1 | 0 | 1 | 0 | 1.525,1 | 30/08/2022 | 0 | N18 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DOPPLER - ARTERIAS RENAIS | 02.05.01.004-0 | solicitações | código | doppler_membros, doppler_outros | 1 | 0 | 1 | 0 | 1.558,8 | 27/07/2022 | 0 | I70 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DOPPLER - CERVICAL | 02.05.01.004-0 | solicitações | código | doppler_membros, doppler_outros | 1 | 0 | 1 | 0 | 1.383,1 | 19/01/2023 | 0 | E04 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DOPPLER ARTERIAL-M I E | 02.05.01.004-0 | solicitações | código | doppler_membros, doppler_outros | 1 | 0 | 1 | 0 | 1.525,1 | 30/08/2022 | 0 | I73 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DOPPLER DE MAMAS | 02.05.02.009-7 | solicitações | código | mama | 1 | 0 | 1 | 0 | 1.525,1 | 30/08/2022 | 0 | Z12 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DOPPLER VENOSO - MIE | 02.05.01.004-0 | solicitações | código | doppler_membros, doppler_outros | 1 | 0 | 1 | 0 | 1.525,1 | 30/08/2022 | 0 | I73 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA PELVICA | 02.05.02.016-0 | solicitações | código | pelvica | 1 | 0 | 1 | 0 | 1.525,2 | 30/08/2022 | 0 | E30 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| USG PELVICA | 02.05.02.016-0 | solicitações | código | pelvica | 1 | 0 | 1 | 0 | 3.588,4 | 05/01/2017 | — | Z00 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| USG TRANSVAGINAL | 02.05.02.018-6 | solicitações | código | transvaginal | 1 | 0 | 1 | 0 | 3.969,4 | 21/12/2015 | — | Z00 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 247. TC CARDIACA ADULTO C/ CONTRASTE S/ SEDACAO | 02.06.03.001-0 | solicitações | código | tc_abdomen | 0 | 0 | 0 | 43 | — | — | 143 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 101. TC DE OUVIDOS ADULTO S/CONTRASTE S/SEDACAO | 02.06.01.004-4 | solicitações | código | tc_face | 0 | 0 | 0 | 13 | — | — | 140 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 065. TC DE FACE INFANTIL S/CONTRASTE S/SEDACAO | 02.06.01.004-4 | solicitações | código | tc_face | 0 | 0 | 0 | 2 | — | — | 123 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 089. TC DE MASTOIDES INFANTIL S/CONTRASTE S/SEDACAO | 02.06.01.004-4 | solicitações | código | tc_face | 0 | 0 | 0 | 12 | — | — | 88 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 245. TC CARDIACA ADULTO S/ CONTRASTE S/ SEDACAO | 02.06.03.001-0 | solicitações | código | tc_abdomen | 0 | 0 | 0 | 17 | — | — | 72 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 057. TC DO ABDOMEN SUPERIOR INFANTIL S/CONTRASTE S/SEDACAO | 02.06.03.001-0 | solicitações | código | tc_abdomen | 0 | 0 | 0 | 35 | — | — | 71 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 105. TC DE PELVE OU BACIA INFANTIL S/CONTRASTE S/SEDACAO | 02.06.03.003-7 | solicitações | código | tc_pelve | 0 | 0 | 0 | 47 | — | — | 69 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 050. TC DO TORAX INFANTIL S/CONTRASTE C/SEDACAO | 02.06.02.003-1 | solicitações | código | tc_torax | 0 | 0 | 0 | 11 | — | — | 32 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 052. TC DO TORAX INFANTIL C/CONTRASTE C/SEDACAO | 02.06.02.003-1 | solicitações | código | tc_torax | 0 | 0 | 0 | 10 | — | — | 26 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 054. TC DO TORAX ADULTO S/CONTRASTE C/SEDACAO | 02.06.02.003-1 | solicitações | código | tc_torax | 0 | 0 | 0 | 218 | — | — | 21 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 056. TC DO TORAX ADULTO C/CONTRASTE C/SEDACAO | 02.06.02.003-1 | solicitações | código | tc_torax | 0 | 0 | 0 | 142 | — | — | 21 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 062. TC DO ABDOMEN SUPERIOR ADULTO S/CONTRASTE C/SEDACAO | 02.06.03.001-0 | solicitações | código | tc_abdomen | 0 | 0 | 0 | 111 | — | — | 17 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 090. TC DE MASTOIDES INFANTIL S/CONTRASTE C/SEDACAO | 02.06.01.004-4 | solicitações | código | tc_face | 0 | 0 | 0 | 10 | — | — | 16 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 097. TC DE OUVIDOS INFANTIL S/CONTRASTE S/SEDACAO | 02.06.01.004-4 | solicitações | código | tc_face | 0 | 0 | 0 | 4 | — | — | 16 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 115. TC DE PESCOCO INFANTIL C/CONTRASTE S/SEDACAO | 02.06.01.005-2 | solicitações | código | tc_pescoco | 0 | 0 | 0 | 16 | — | — | 16 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 067. TC DE FACE INFANTIL C/CONTRASTE S/SEDACAO | 02.06.01.004-4 | solicitações | código | tc_face | 0 | 0 | 0 | 5 | — | — | 13 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 066. TC DE FACE INFANTIL S/CONTRASTE C/SEDACAO | 02.06.01.004-4 | solicitações | código | tc_face | 0 | 0 | 0 | 1 | — | — | 11 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 113. TC DE PESCOCO INFANTIL S/CONTRASTE S/SEDACAO | 02.06.01.005-2 | solicitações | código | tc_pescoco | 0 | 0 | 0 | 2 | — | — | 10 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 075. TC DE SEIOS DE FACE INFANTIL C/CONTRASTE S/SEDACAO | 02.06.01.004-4 | solicitações | código | tc_face | 0 | 0 | 0 | 5 | — | — | 9 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 058. TC DO ABDOMEN SUPERIOR INFANTIL S/CONTRASTE C/SEDACAO | 02.06.03.001-0 | solicitações | código | tc_abdomen | 0 | 0 | 0 | 6 | — | — | 6 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 106. TC DE PELVE OU BACIA INFANTIL S/CONTRASTE C/SEDACAO | 02.06.03.003-7 | solicitações | código | tc_pelve | 0 | 0 | 0 | 4 | — | — | 5 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 116. TC DE PESCOCO INFANTIL C/CONTRASTE C/SEDACAO | 02.06.01.005-2 | solicitações | código | tc_pescoco | 0 | 0 | 0 | 3 | — | — | 5 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 068. TC DE FACE INFANTIL C/CONTRASTE C/SEDACAO | 02.06.01.004-4 | solicitações | código | tc_face | 0 | 0 | 0 | 2 | — | — | 4 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 070. TC DE FACE ADULTO S/CONTRASTE C/SEDACAO | 02.06.01.004-4 | solicitações | código | tc_face | 0 | 0 | 0 | 8 | — | — | 4 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 074. TC DE SEIOS DE FACE INFANTIL S/CONTRASTE C/SEDACAO | 02.06.01.004-4 | solicitações | código | tc_face | 0 | 0 | 0 | 3 | — | — | 4 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 098. TC DE OUVIDOS INFANTIL S/CONTRASTE C/SEDACAO | 02.06.01.004-4 | solicitações | código | tc_face | 0 | 0 | 0 | 1 | — | — | 4 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 078. TC DE SEIOS DE FACE ADULTO S/CONTRASTE C/SEDACAO | 02.06.01.004-4 | solicitações | código | tc_face | 0 | 0 | 0 | 32 | — | — | 3 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 094. TC DE MASTOIDES ADULTO S/CONTRASTE C/SEDACAO | 02.06.01.004-4 | solicitações | código | tc_face | 0 | 0 | 0 | 15 | — | — | 3 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 120. TC DE PESCOCO ADULTO C/CONTRASTE C/SEDACAO | 02.06.01.005-2 | solicitações | código | tc_pescoco | 0 | 0 | 0 | 38 | — | — | 3 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 072. TC DE FACE ADULTO C/CONTRASTE C/SEDACAO | 02.06.01.004-4 | solicitações | código | tc_face | 0 | 0 | 0 | 4 | — | — | 2 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 092. TC DE MASTOIDES INFANTIL C/CONTRASTE C/SEDACAO | 02.06.01.004-4 | solicitações | código | tc_face | 0 | 0 | 0 | 3 | — | — | 2 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 096. TC DE MASTOIDES ADULTO C/CONTRASTE C/SEDACAO | 02.06.01.004-4 | solicitações | código | tc_face | 0 | 0 | 0 | 3 | — | — | 2 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 100. TC DE OUVIDOS INFANTIL C/CONTRASTE C/SEDACAO | 02.06.01.004-4 | solicitações | código | tc_face | 0 | 0 | 0 | 1 | — | — | 2 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ANGIOTOMOGRAFIA DA PELVE ADULTO C/SEDACAO | 02.06.03.003-7 | solicitações | código | tc_pelve | 0 | 0 | 0 | 6 | — | — | 2 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ANGIOTOMOGRAFIA DO CRANIO ADULTO C/SEDACAO | 02.06.01.007-9 | solicitações | código | tc_cranio | 0 | 0 | 0 | 12 | — | — | 2 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ANGIOTOMOGRAFIA DO TORAX OU PULMONAR ADULTO C/SEDACAO | 02.06.02.003-1 | solicitações | código | tc_torax | 0 | 0 | 0 | 11 | — | — | 2 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 076. TC DE SEIOS DE FACE INFANTIL C/CONTRASTE C/SEDACAO | 02.06.01.004-4 | solicitações | código | tc_face | 0 | 0 | 0 | 2 | — | — | 1 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 083. TC ARTIC. TEMP. MAND. (ATM) INFANTIL C/CONTRASTE S/SEDACAO | 02.06.01.004-4 | solicitações | código | tc_face | 0 | 0 | 0 | 1 | — | — | 1 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 099. TC DE OUVIDOS INFANTIL C/CONTRASTE S/SEDACAO | 02.06.01.004-4 | solicitações | código | tc_face | 0 | 0 | 0 | 1 | — | — | 1 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 243. TC CARDIACA INFANTIL C/ CONTRASTE S/ SEDACAO | 02.06.03.001-0 | solicitações | código | tc_abdomen | 0 | 0 | 0 | 1 | — | — | 1 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ANGIOTOMOGRAFIA DA AORTA TORÁCICA E SEUS RAMOS INFANTIL C/SEDACAO | 02.06.02.003-1 | solicitações | código | tc_torax | 0 | 0 | 0 | 4 | — | — | 1 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ANGIOTOMOGRAFIA DAS ARTERIAS CAROTIDAS E VERTEBRAIS ADULTO C/SEDACAO | 02.06.03.001-0 | solicitações | código | tc_abdomen | 0 | 0 | 0 | 4 | — | — | 1 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ANGIOTOMOGRAFIA DAS ARTERIAS CAROTIDAS E VERTEBRAIS INFANTIL S/SEDACAO | 02.06.03.001-0 | solicitações | código | tc_abdomen | 0 | 0 | 0 | 3 | — | — | 1 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ANGIOTOMOGRAFIA DO ABDOME SUPERIOR ADULTO C/SEDACAO | 02.06.03.001-0 | solicitações | código | tc_abdomen | 0 | 0 | 0 | 9 | — | — | 1 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 080. TC DE SEIOS DE FACE ADULTO C/CONTRASTE C/SEDACAO | 02.06.01.004-4 | solicitações | código | tc_face | 0 | 0 | 0 | 1 | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 081. TC ARTIC. TEMP. MAND. (ATM) INFANTIL S/CONTRASTE S/SEDACAO | 02.06.01.004-4 | solicitações | código | tc_face | 0 | 0 | 0 | 1 | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 102. TC DE OUVIDOS ADULTO S/CONTRASTE C/SEDACAO | 02.06.01.004-4 | solicitações | código | tc_face | 0 | 0 | 0 | 2 | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 118. TC DE PESCOCO ADULTO S/CONTRASTE C/SEDACAO | 02.06.01.005-2 | solicitações | código | tc_pescoco | 0 | 0 | 0 | 12 | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 242. TC CARDIACA INFANTIL S/ CONTRASTE C/ SEDACAO | 02.06.03.001-0 | solicitações | código | tc_abdomen | 0 | 0 | 0 | 1 | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 244. TC CARDIACA INFANTIL C/ CONTRASTE C/ SEDACAO | 02.06.03.001-0 | solicitações | código | tc_abdomen | 0 | 0 | 0 | 2 | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 246. TC CARDIACA ADULTO S/ CONTRASTE C/ SEDACAO | 02.06.03.001-0 | solicitações | código | tc_abdomen | 0 | 0 | 0 | 3 | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 248. TC CARDIACA ADULTO C/ CONTRASTE C/ SEDACAO | 02.06.03.001-0 | solicitações | código | tc_abdomen | 0 | 0 | 0 | 3 | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 249. TC DE CORACAO COM CONTRASTE SEM SEDACAO | 02.06.02.003-1 | solicitações | código | tc_torax | 0 | 0 | 0 | 2 | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 250. TC DE CORACAO COM CONTRASTE COM SEDACAO | 02.06.02.003-1 | solicitações | código | tc_torax | 0 | 0 | 0 | 5 | — | — | — | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 287. TC DE FIGADO ADULTO S/ CONTRASTE S/ SEDACAO | 02.06.03.001-0 | solicitações | código | tc_abdomen | 0 | 0 | 0 | 2 | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 288. TC DE FIGADO ADULTO S/ CONTRASTE C/ SEDACAO | 02.06.03.001-0 | solicitações | código | tc_abdomen | 0 | 0 | 0 | 2 | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 289. TC DE FIGADO ADULTO C/ CONTRASTE S/ SEDACAO | 02.06.03.001-0 | solicitações | código | tc_abdomen | 0 | 0 | 0 | 4 | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 291. TC DO ABDOMEN INFERIOR ADULTO S/CONTRASTE S/SEDACAO | 02.06.03.003-7 | solicitações | código | tc_pelve | 0 | 0 | 0 | 1 | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 294. TC DO ABDOMEN INFERIOR INFANTIL C/CONTRASTE C/SEDACAO | 02.06.03.003-7 | solicitações | código | tc_pelve | 0 | 0 | 0 | 1 | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 298. TC DO ABDOMEM INFERIOR ADULTO S/CONTRASTE S/SEDACAO | 02.06.03.003-7 | solicitações | código | tc_pelve | 0 | 0 | 0 | 3 | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 300. TC DO ABDOMEN INFERIOR ADULTO C/CONTRASTE S/SEDACAO | 02.06.03.003-7 | solicitações | código | tc_pelve | 0 | 0 | 0 | 16 | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 304. TC DO ABDOMEN INFERIOR INFANTIL C/CONTRASTE S/SEDACAO | 02.06.03.003-7 | solicitações | código | tc_pelve | 0 | 0 | 0 | 1 | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 309. ANGIOTOMOGRAFIA | 02.06.02.003-1 | solicitações | código | tc_torax | 0 | 0 | 0 | 1.285 | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 314. TC DE DE APARELHO URINARIO - COM LAUDO | 02.06.03.003-7 | solicitações | código | tc_pelve | 0 | 0 | 0 | 1 | — | — | — | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 315.TC DO ABDOMEN TOTAL | 02.06.03.001-0 | solicitações | código | tc_abdomen | 0 | 0 | 0 | 2 | — | — | — | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ANGIOTOMOGRAFIA DA AORTA ABDOMINAL E DOS SEUS RAMOS ADULTO C/SEDACAO | 02.06.03.001-0 | solicitações | código | tc_abdomen | 0 | 0 | 0 | 5 | — | — | — | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ANGIOTOMOGRAFIA DA AORTA TORÁCICA E SEUS RAMOS ADULTO C/SEDACAO | 02.06.02.003-1 | solicitações | código | tc_torax | 0 | 0 | 0 | 8 | — | — | — | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ANGIOTOMOGRAFIA DAS ARTÉRIAS RENAIS INFANTIL C/SEDACAO | 02.06.03.001-0 | solicitações | código | tc_abdomen | 0 | 0 | 0 | 1 | — | — | — | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ANGIOTOMOGRAFIA DE TORAX | 02.06.03.003-7 | solicitações | código | tc_pelve | 0 | 0 | 0 | 41 | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ANGIOTOMOGRAFIA DO ABDOME SUPERIOR INFANTIL C/SEDACAO | 02.06.03.001-0 | solicitações | código | tc_abdomen | 0 | 0 | 0 | 1 | — | — | — | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ANGIOTOMOGRAFIA DO CRANIO INFANTIL CS/SEDACAO | 02.06.01.007-9 | solicitações | código | tc_cranio | 0 | 0 | 0 | 1 | — | — | — | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ANGIOTOMOGRAFIA DO PESCOCO ADULTO C/SEDACAO | 02.06.01.005-2 | solicitações | código | tc_pescoco | 0 | 0 | 0 | 4 | — | — | — | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ANGIOTOMOGRAFIA DO TORAX OU PULMONAR INFANTIL C/SEDACAO | 02.06.02.003-1 | solicitações | código | tc_torax | 0 | 0 | 0 | 1 | — | — | — | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| DOPPLER DE BOLSA ESCROTAL | 02.05.01.004-0 | solicitações | código | doppler_membros, doppler_outros | 0 | 0 | 0 | 1 | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA CRANIANA | 02.05.02.017-8 | solicitações | código | transfontanela | 0 | 0 | 0 | 1 | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA PENIANA ADULTO | 02.05.02.007-0 | solicitações | código | bolsa_escrotal | 0 | 0 | 0 | 2 | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| TOMOGRAFIA COMPUTADORIZADA DO ABDOMEN TOTAL COM CONTRASTE | 02.06.03.001-0 | solicitações | código | tc_abdomen | 0 | 0 | 0 | 5 | — | — | — | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DOPPLER ARTERIAL- M S E | 02.05.01.004-0 | solicitações | código | doppler_membros, doppler_outros | 0 | 0 | 0 | 21 | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DOPPLER COLORIDO DE TRES VASOS | 02.05.01.004-0 | solicitações | código | doppler_membros, doppler_outros | 0 | 0 | 0 | 6 | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DOPPLER VENOSO - MSD | 02.05.01.004-0 | solicitações | código | doppler_membros, doppler_outros | 0 | 0 | 0 | 56 | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DOPPLER VENOSO - MSE | 02.05.01.004-0 | solicitações | código | doppler_membros, doppler_outros | 0 | 0 | 0 | 37 | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DOPPLER DE ARTERIA AORTA ABDOMINAL | 02.05.01.004-0 | solicitações | código | doppler_membros, doppler_outros | 0 | 0 | 0 | 3 | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DOPPLER DE ARTERIAS RENAIS | 02.05.01.004-0 | solicitações | código | doppler_membros, doppler_outros | 0 | 0 | 0 | 15 | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DOPPLER DE SUBCLAVIAS E JUGULARESS | 02.05.01.004-0 | solicitações | código | doppler_membros, doppler_outros | 0 | 0 | 0 | 1 | — | — | — | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DOPPLER PELVICA - GINECOLOGICA | 02.05.02.016-0 | solicitações | código | pelvica | 0 | 0 | 0 | 4 | — | — | — | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA PELVICA ( GINECOLOGICA ) | 02.05.02.016-0 | solicitações | código | pelvica | 0 | 0 | 0 | 1 | — | — | — | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA TRANSVAGINAL | 02.05.02.018-6 | solicitações | código | transvaginal | 0 | 0 | 0 | 2 | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRASSONOGRAFIA DOPPLER COLORIDO DE VASOS | 02.05.01.004-0 | solicitações | código | doppler_membros, doppler_outros | 0 | 0 | 0 | 69 | — | — | — | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRASSONOGRAFIA DOPPLER COLORIDO DE VASOS INTRA-OPERATÓRIO | 02.05.01.004-0 | solicitações | código | doppler_membros, doppler_outros | 0 | 0 | 0 | 1 | — | — | — | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRASSONOGRAFIA TRANSVAGINAL | 02.05.02.018-6 | solicitações | código | transvaginal | 0 | 0 | 0 | 1 | — | — | — | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 114. TC DE PESCOCO INFANTIL S/CONTRASTE C/SEDACAO | 02.06.01.005-2 | só agendamentos | código | tc_pescoco | — | — | — | — | — | — | 4 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC DE OUVIDOS INFANTIL S/CONTRASTE S/SEDACAO EMERGENCIA | 02.06.01.004-4 | só agendamentos | código | tc_face | — | — | — | — | — | — | 3 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 241. TC CARDIACA INFANTIL S/ CONTRASTE S/ SEDACAO | 02.06.03.001-0 | só agendamentos | código | tc_abdomen | — | — | — | — | — | — | 2 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 082. TC ARTIC. TEMP. MAND. (ATM) INFANTIL S/CONTRASTE C/SEDACAO | 02.06.01.004-4 | só agendamentos | código | tc_face | — | — | — | — | — | — | 1 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ANGIOTOMOGRAFIA DO SISTEMA PORTA (VASOS HEPÁTICOS) INFANTIL S/SEDACAO | 02.06.03.001-0 | só agendamentos | código | tc_abdomen | — | — | — | — | — | — | 1 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC ART.TEMP.MAND.(ATM) INFANTIL S/CONTRASTE S/SEDACAO EMERG | 02.06.01.004-4 | só agendamentos | código | tc_face | — | — | — | — | — | — | 1 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC ARTIC.TEMP.MAND.(ATM)ADULT.C/CONTRASTE S/SEDACAO EMERG | 02.06.01.004-4 | só agendamentos | código | tc_face | — | — | — | — | — | — | 1 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| (020501004-0) ULTRA-SONOGRAFIA DOPPLER VENOSO PROFUNDO - MID | 02.05.01.004-0 | só agendamentos | código | doppler_membros, doppler_outros | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 084. TC ARTIC. TEMP. MAND. (ATM) INFANTIL C/CONTRASTE C/SEDACAO | 02.06.01.004-4 | só agendamentos | código | tc_face | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 086. TC ARTIC. TEMP. MAND. (ATM) ADULTO S/CONTRASTE C/SEDACAO | 02.06.01.004-4 | só agendamentos | código | tc_face | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 104. TC DE OUVIDOS ADULTO C/CONTRASTE C/SEDACAO | 02.06.01.004-4 | só agendamentos | código | tc_face | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 11. ECOCARDIOGRAFIA DE ARTERIAS VERTEBRAIS (genérica) | 02.05.01.004-0 | só agendamentos | código | doppler_membros, doppler_outros | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 283. TC DE FIGADO INFANTIL S/ CONTRASTE S/ SEDACAO | 02.06.03.001-0 | só agendamentos | código | tc_abdomen | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 293. TC DO ABDOMEN INFERIOR INFANTIL S/CONTRASTE S/SEDACAO | 02.06.03.003-7 | só agendamentos | código | tc_pelve | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ANGIOTOMOGRAFIA DO ABDOME SUPERIOR INFANTIL S/SEDACAO | 02.06.03.001-0 | só agendamentos | código | tc_abdomen | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| DOPPLER DE CAROTIDAS | 02.05.01.004-0 | só agendamentos | código, nome | doppler_membros, doppler_outros | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA CRANIANA EMERGENICA | 02.05.02.017-8 | só agendamentos | código | transfontanela | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA DE ABDOMEN SUPERIOR | 02.05.02.003-8 | só agendamentos | código, nome | abdomen_superior | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA DE ABDOMEN SUPERIOR ADULTO EMERGENCIA | 02.05.02.003-8 | só agendamentos | código, nome | abdomen_superior | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA DE ABDOMEN SUPERIOR INFANTIL EMERGENCIA | 02.05.02.003-8 | só agendamentos | código | abdomen_superior | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA DE ABDOMEN TOTAL (ABDOMEN SUP. RETROPERITONIO, RI | 02.05.02.004-6 | só agendamentos | código | abdomen_total, parede | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA DE ABDOMEN TOTAL INFANTIL EMERGENCIA | 02.05.02.004-6 | só agendamentos | código, nome | abdomen_total, parede | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA DE BOLSA ESCROTAL | 02.05.02.007-0 | só agendamentos | código, nome | bolsa_escrotal | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA DE BOLSA ESCROTAL ADULTO EMERGENCIA | 02.05.02.007-0 | só agendamentos | código, nome | bolsa_escrotal | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA DE BOLSA ESCROTAL INFANTIL EMERGENCIA | 02.05.02.007-0 | só agendamentos | código, nome | bolsa_escrotal | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA DE MAMAS - BILATERAL EMERGENCIA | 02.05.02.009-7 | só agendamentos | código, nome | mama | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA DE PROSTATA ( VIA ABDOMINAL ) EMERGENCIA | 02.05.02.010-0 | só agendamentos | código, nome | prostata | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA DE TIREOIDE | 02.05.02.012-7 | só agendamentos | código, nome | tireoide | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA DE TIREOIDE INFANTIL EMERGENCIA | 02.05.02.012-7 | só agendamentos | código, nome | tireoide | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA DE ULTRASONOGRAFIA PAREDE ABDOMINAL | 02.05.02.004-6 | só agendamentos | código | abdomen_total, parede | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA DO APARELHO URINARIO (RINS, BEXIGA) ADULTO EMERG | 02.05.02.005-4 | só agendamentos | código, nome | urinario | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA DOPPLER COLORIDO DE DOIS VASOS | 02.05.01.004-0 | só agendamentos | código | doppler_membros, doppler_outros | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA DOPPLER COLORIDO DE DOIS VASOS EMERGENCIA | 02.05.01.004-0 | só agendamentos | código | doppler_membros, doppler_outros | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA DOPPLER COLORIDO DE ESTRUTURA ISOLADA | 02.05.01.004-0 | só agendamentos | código | doppler_membros, doppler_outros | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA DOPPLER COLORIDO DE ORGAO EMERGENCIA | 02.05.01.004-0 | só agendamentos | código | doppler_membros, doppler_outros | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA DOPPLER COLORIDO DE TRES VASOS | 02.05.01.004-0 | só agendamentos | código | doppler_membros, doppler_outros | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA ESTUDO DE 1 VASO COM DOPPLER PULSADO CONT | 02.05.01.004-0 | só agendamentos | código | doppler_membros, doppler_outros | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA ESTUDO DE 2 VASOS COM DOPPLER PULSADO CONT | 02.05.01.004-0 | só agendamentos | código | doppler_membros, doppler_outros | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA ESTUDO DE 3 OU MAIS VASOS COM DOPPLER PULSADO CONT | 02.05.01.004-0 | só agendamentos | código | doppler_membros, doppler_outros | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA PELVICA (GINECOLOGICA) - ADULTO - EMERGENCIA | 02.05.02.016-0 | só agendamentos | código, nome | pelvica | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA PELVICA (GINECOLOGICA) - INFANTIL - EMERGENCIA | 02.05.02.016-0 | só agendamentos | código, nome | pelvica | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA PENIANA ADULTO EMERGENCIA | 02.05.02.007-0 | só agendamentos | código | bolsa_escrotal | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA PENIANA INFANTIL | 02.05.02.007-0 | só agendamentos | código | bolsa_escrotal | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA TRANSVAGINAL COM DOPPLER | 02.05.02.015-1 | só agendamentos | nome | doppler_outros, transvaginal | — | — | — | — | — | — | 0 | — | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ECOGRAFIA TRANSVAGINAL COM DOPPLER EMERGENCIA | 02.05.01.004-0 | só agendamentos | código, nome | doppler_membros, doppler_outros, transvaginal | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA TRANSVAGINAL EMERGENCIA | 02.05.02.018-6 | só agendamentos | código, nome | transvaginal | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC DE PESCOCO ADULTO C/CONTRASTE / C/SEDACAO EMERGENCIA | 02.06.01.005-2 | só agendamentos | código | tc_pescoco | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC DE PESCOCO ADULTO S/CONTRASTE / C/SEDACAO EMERGENCIA | 02.06.01.005-2 | só agendamentos | código | tc_pescoco | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC DE PESCOCO INFANTIL C/CONTRASTE / C/SEDACAO EMERGENCIA | 02.06.01.005-2 | só agendamentos | código | tc_pescoco | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC DE PESCOCO INFANTIL S/CONTRASTE / C/SEDACAO EMERGENCIA | 02.06.01.005-2 | só agendamentos | código | tc_pescoco | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC ART.TEMP.MAND.(ATM) INFANTIL C/CONTRASTE S/SEDACAO EMERG | 02.06.01.004-4 | só agendamentos | código | tc_face | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC DE CORACAO COM CONTRASTE SEM SEDACAO | 02.06.02.003-1 | só agendamentos | código | tc_torax | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC DE CRANIO ADULTO C/CONTRASTE C/SEDACAO EMERGENCIA | 02.06.01.007-9 | só agendamentos | código | tc_cranio | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC DE CRANIO ADULTO S/CONTRASTE C/SEDACAO EMERGENCIA | 02.06.01.007-9 | só agendamentos | código | tc_cranio | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC DE CRANIO INFANTIL C/CONTRASTE C/SEDACAO EMERGENCIA | 02.06.01.007-9 | só agendamentos | código | tc_cranio | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC DE CRANIO INFANTIL S/CONTRASTE C/SEDACAO EMERGENCIA | 02.06.01.007-9 | só agendamentos | código | tc_cranio | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC DE FACE ADULTO C/CONTRASTE C/SEDACAO EMERGENCIA | 02.06.01.004-4 | só agendamentos | código | tc_face | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC DE FACE ADULTO S/CONTRASTE C/SEDACAO EMERGENCIA | 02.06.01.004-4 | só agendamentos | código | tc_face | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC DE FACE INFANTIL C/CONTRASTE C/SEDACAO EMERGENCIA | 02.06.01.004-4 | só agendamentos | código | tc_face | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC DE FACE INFANTIL S/CONTRASTE C/SEDACAO EMERGENCIA | 02.06.01.004-4 | só agendamentos | código | tc_face | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC DE FIGADO C/ CONTRASTE C/ SEDACAO | 02.06.03.001-0 | só agendamentos | código | tc_abdomen | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC DE FIGADO C/ CONTRASTE S/ SEDACAO | 02.06.03.001-0 | só agendamentos | código | tc_abdomen | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC DE FIGADO S/ CONTRASTE S/ SEDACAO | 02.06.03.001-0 | só agendamentos | código | tc_abdomen | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC DE MASTOIDES ADULTO C/CONTRASTE C/SEDACAO EMERGENCIA | 02.06.01.004-4 | só agendamentos | código | tc_face | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC DE MASTOIDES ADULTO S/CONTRASTE C/SEDACAO EMERGENCIA | 02.06.01.004-4 | só agendamentos | código | tc_face | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC DE MASTOIDES INFANTIL C/CONTRASTE C/SEDACAO EMERGENCIA | 02.06.01.004-4 | só agendamentos | código | tc_face | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC DE MASTOIDES INFANTIL S/CONTRASTE C/SEDACAO EMERGENCIA | 02.06.01.004-4 | só agendamentos | código | tc_face | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC DE OUVIDOS INFANTIL C/CONTRASTE C/SEDACAO EMERGENCIA | 02.06.01.004-4 | só agendamentos | código | tc_face | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC DE OUVIDOS INFANTIL C/CONTRASTE S/SEDACAO EMERGENCIA | 02.06.01.004-4 | só agendamentos | código | tc_face | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC DE OUVIDOS INFANTIL S/CONTRASTE C/SEDACAO EMERGENCIA | 02.06.01.004-4 | só agendamentos | código | tc_face | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC DE PELVE OU BACIA ADULTO C/CONTRASTE C/SEDACAO EMERG. | 02.06.03.003-7 | só agendamentos | código | tc_pelve | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC DE PELVE OU BACIA ADULTO S/CONTRASTE C/SEDACAO EMERG. | 02.06.03.003-7 | só agendamentos | código | tc_pelve | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC DE PELVE OU BACIA INFANTIL C/CONTRASTE C/SEDACAO EMERG. | 02.06.03.003-7 | só agendamentos | código | tc_pelve | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC DE PELVE OU BACIA INFANTIL S/CONTRASTE C/SEDACAO EMERG. | 02.06.03.003-7 | só agendamentos | código | tc_pelve | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC DE SEIOS DE FACE ADULTO S/CONTRASTE C/SEDACAO EMERG. | 02.06.01.004-4 | só agendamentos | código | tc_face | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC DE SEIOS DE FACE INFANTIL C/CONTRASTE C/SEDACAO EMERG. | 02.06.01.004-4 | só agendamentos | código | tc_face | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC DE SEIOS DE FACE INFANTIL S/CONTRASTE C/SEDACAO EMERG. | 02.06.01.004-4 | só agendamentos | código | tc_face | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC DO ABDOMEN SUPER.ADULTO C/CONTRASTE C/SEDACAO EMERG. | 02.06.03.001-0 | só agendamentos | código | tc_abdomen | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC DO ABDOMEN SUPER.ADULTO S/CONTRASTE C/SEDACAO EMERG. | 02.06.03.001-0 | só agendamentos | código | tc_abdomen | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC DO ABDOMEN SUPER.INFANTIL C/CONTRASTE C/SEDACAO EMERG. | 02.06.03.001-0 | só agendamentos | código | tc_abdomen | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC DO ABDOMEN SUPER.INFANTIL S/CONTRASTE C/SEDACAO EMERG. | 02.06.03.001-0 | só agendamentos | código | tc_abdomen | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC DO TORAX ADULTO C/CONTRASTE C/SEDACAO EMERGENCIA | 02.06.02.003-1 | só agendamentos | código | tc_torax | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC DO TORAX ADULTO S/CONTRASTE C/SEDACAO EMERGENCIA | 02.06.02.003-1 | só agendamentos | código | tc_torax | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC DO TORAX INFANTIL C/CONTRASTE C/SEDACAO EMERGENCIA | 02.06.02.003-1 | só agendamentos | código | tc_torax | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC DO TORAX INFANTIL S/CONTRASTE C/SEDACAO EMERGENCIA | 02.06.02.003-1 | só agendamentos | código | tc_torax | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DE TIREOIDE COM DOPPLER COLORIDO | 02.05.02.012-7 | só agendamentos | código | tireoide | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA ESTUDO DE 1 VASO COM DOPPLER PULSADO CONTI | 02.05.01.004-0 | só agendamentos | código | doppler_membros, doppler_outros | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA HIPOCONDRIO DIREITO (FIGADO, VESICULA, VIAS BILIARES) | 02.05.02.003-8 | só agendamentos | código | abdomen_superior | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA AXILA | 02.05.02.009-7 | só agendamentos | código | mama | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DE ABDOMEN SUPERIOR (FIGADO, VESICULA, VIAS BILIARES) | 02.05.02.003-8 | só agendamentos | código | abdomen_superior | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DE ARTERIAS CAROTIDAS E VERTEBRAIS COM DOPPLER | 02.05.01.004-0 | só agendamentos | código | doppler_membros, doppler_outros | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DE BOLSA ESCROTAL | 02.05.02.007-0 | só agendamentos | código | bolsa_escrotal | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DE TIREOIDE COM DOPPLER | 02.05.01.004-0 | só agendamentos | código | doppler_membros, doppler_outros | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DOPPLER ARTERIAL E VENOSO – MIE | 02.05.01.004-0 | só agendamentos | código | doppler_membros, doppler_outros | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DOPPLER ARTERIAL E VENOSO – MSD | 02.05.01.004-0 | só agendamentos | código | doppler_membros, doppler_outros | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DOPPLER ARTERIAL E VENOSO – MSE | 02.05.01.004-0 | só agendamentos | código | doppler_membros, doppler_outros | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DOPPLER ARTERIAL-M S D | 02.05.01.004-0 | só agendamentos | código | doppler_membros, doppler_outros | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DOPPLER ARTERIAL-M S E | 02.05.01.004-0 | só agendamentos | código | doppler_membros, doppler_outros | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DOPPLER DE ABDOMEN | 02.05.02.004-6 | só agendamentos | código | abdomen_total, parede | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DOPPLER DE BOLSA ESCROTAL | 02.05.02.007-0 | só agendamentos | código | bolsa_escrotal | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DOPPLER VENOSO - MSD | 02.05.01.004-0 | só agendamentos | código | doppler_membros, doppler_outros | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DOPPLER VENOSO - MSE | 02.05.01.004-0 | só agendamentos | código | doppler_membros, doppler_outros | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DOPPLER VENOSO PROFUNDO - MIE | 02.05.01.004-0 | só agendamentos | código | doppler_membros, doppler_outros | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DOPPLER VENOSO SUPERFICIAL - MID | 02.05.01.004-0 | só agendamentos | código | doppler_membros, doppler_outros | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DOPPLER VENOSO SUPERFICIAL - MIE | 02.05.01.004-0 | só agendamentos | código | doppler_membros, doppler_outros | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRASONOGRAFIA TRANSVAGINAL COM PREPARO INTESTINAL | 02.05.02.018-6 | só agendamentos | código | transvaginal | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRASSONOGRAFIA AXILA DIREITA | 02.05.02.009-7 | só agendamentos | código | mama | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRASSONOGRAFIA AXILA ESQUERDA | 02.05.02.009-7 | só agendamentos | código | mama | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRASSONOGRAFIA DE ABDOMEN INFERIOR | 02.05.02.004-6 | só agendamentos | código | abdomen_total, parede | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRASSONOGRAFIA DE ORGAOS E ESTRUTURAS SUPERFICIAIS | 02.05.02.012-7 | só agendamentos | código | tireoide | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRASSONOGRAFIA DOPPLER ARTERIAL MEMBRO SUPERIOR D | 02.05.01.004-0 | só agendamentos | código | doppler_membros, doppler_outros | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRASSONOGRAFIA DOPPLER VENOSO MEMBRO SUPERIOR D | 02.05.01.004-0 | só agendamentos | código | doppler_membros, doppler_outros | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRASSONOGRAFIA DOPPLER VENOSO MEMBRO SUPERIOR E | 02.05.01.004-0 | só agendamentos | código | doppler_membros, doppler_outros | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |

## Região de Saúde

**tc_abdomen**, na medida da fila (o conjunto do objeto):

| Região de Saúde | fila | pessoas |
|---|---|---|
| URD | 1.839 | 1.809 |
| Região Sudoeste | 931 | 927 |
| Contratado/Credenciado | 806 | 793 |
| Região Norte | 328 | 325 |
| Região Sul | 324 | 321 |
| Região Oeste | 321 | 315 |
| Região Central | 202 | 198 |
| Região Leste | 157 | 156 |
| Região Centro-Sul | 96 | 94 |
| sem Região de Saúde | 27 | 26 |

**tc_pelve**, na medida da fila (o conjunto do objeto):

| Região de Saúde | fila | pessoas |
|---|---|---|
| URD | 1.526 | 1.524 |
| Região Sudoeste | 742 | 741 |
| Contratado/Credenciado | 634 | 631 |
| Região Norte | 275 | 275 |
| Região Sul | 274 | 273 |
| Região Oeste | 171 | 171 |
| Região Central | 153 | 153 |
| Região Leste | 96 | 96 |
| Região Centro-Sul | 60 | 60 |
| sem Região de Saúde | 18 | 18 |

**transfontanela**, na medida da fila (o conjunto do objeto):

| Região de Saúde | fila | pessoas |
|---|---|---|
| Região Sul | 156 | 156 |
| Região Centro-Sul | 105 | 105 |
| Região Sudoeste | 5 | 5 |
| Região Leste | 1 | 1 |
| Região Norte | 1 | 1 |
| sem Região de Saúde | 2 | 2 |

**tc_pescoco**, na medida da fila (o conjunto do objeto):

| Região de Saúde | fila | pessoas |
|---|---|---|
| URD | 330 | 329 |
| Contratado/Credenciado | 139 | 138 |
| Região Sudoeste | 73 | 73 |
| Região Oeste | 44 | 44 |
| Região Sul | 17 | 17 |
| Região Norte | 16 | 16 |
| Região Central | 14 | 14 |
| Região Leste | 13 | 13 |
| Região Centro-Sul | 9 | 9 |
| Público - Não SES | 1 | 1 |
| sem Região de Saúde | 1 | 1 |

**abdomen_superior**, na medida da fila (o conjunto do objeto):

| Região de Saúde | fila | pessoas |
|---|---|---|
| Região Sudoeste | 1.538 | 1.536 |
| Região Centro-Sul | 391 | 391 |
| Região Leste | 130 | 130 |
| Região Oeste | 62 | 62 |
| Região Norte | 44 | 44 |
| Região Sul | 23 | 23 |
| Região Central | 20 | 20 |
| URD | 3 | 3 |
| sem Região de Saúde | 2 | 2 |

**bolsa_escrotal**, na medida da fila (o conjunto do objeto):

| Região de Saúde | fila | pessoas |
|---|---|---|
| Região Sudoeste | 514 | 514 |
| Região Centro-Sul | 156 | 156 |
| Região Leste | 130 | 130 |
| Região Sul | 72 | 72 |
| Região Oeste | 38 | 38 |
| Região Norte | 10 | 10 |
| Região Central | 6 | 6 |
| sem Região de Saúde | 8 | 8 |

**urinario**, na medida da fila (o conjunto do objeto):

| Região de Saúde | fila | pessoas |
|---|---|---|
| Região Sudoeste | 1.423 | 1.423 |
| Região Centro-Sul | 959 | 952 |
| Região Sul | 904 | 899 |
| Região Leste | 535 | 533 |
| Região Oeste | 90 | 90 |
| Região Norte | 35 | 35 |
| Região Central | 30 | 30 |
| URD | 1 | 1 |
| sem Região de Saúde | 48 | 48 |

**abdomen_total**, na medida da fila (o conjunto do objeto):

| Região de Saúde | fila | pessoas |
|---|---|---|
| Região Sul | 3.120 | 3.119 |
| Região Sudoeste | 2.536 | 2.535 |
| Região Centro-Sul | 1.940 | 1.937 |
| Região Leste | 1.451 | 1.449 |
| Região Central | 726 | 726 |
| Região Oeste | 359 | 359 |
| Região Norte | 80 | 80 |
| URD | 7 | 7 |
| Serviços Centralizados | 1 | 1 |
| sem Região de Saúde | 127 | 127 |

**parede**, na medida da fila (o conjunto do objeto):

| Região de Saúde | fila | pessoas |
|---|---|---|
| Região Sudoeste | 1.546 | 1.546 |
| Região Sul | 831 | 831 |
| Região Leste | 378 | 378 |
| Região Centro-Sul | 346 | 346 |
| Região Oeste | 114 | 114 |
| Região Norte | 37 | 37 |
| Região Central | 12 | 12 |
| URD | 1 | 1 |
| sem Região de Saúde | 39 | 39 |

**doppler_outros**, na medida da fila (o conjunto do objeto):

| Região de Saúde | fila | pessoas |
|---|---|---|
| Região Sudoeste | 802 | 790 |
| Região Centro-Sul | 698 | 692 |
| Região Oeste | 551 | 549 |
| Região Norte | 528 | 526 |
| URD | 506 | 503 |
| Região Central | 487 | 486 |
| Contratado/Credenciado | 441 | 441 |
| Região Leste | 337 | 336 |
| Região Sul | 330 | 330 |
| sem Região de Saúde | 51 | 50 |

**prostata**, na medida da fila (o conjunto do objeto):

| Região de Saúde | fila | pessoas |
|---|---|---|
| Região Sul | 1.180 | 1.179 |
| Região Centro-Sul | 609 | 608 |
| Região Leste | 535 | 535 |
| Região Sudoeste | 502 | 501 |
| Região Norte | 57 | 57 |
| Região Oeste | 48 | 48 |
| Região Central | 21 | 21 |
| URD | 1 | 1 |
| sem Região de Saúde | 16 | 16 |

**tireoide**, na medida da fila (o conjunto do objeto):

| Região de Saúde | fila | pessoas |
|---|---|---|
| Região Sudoeste | 1.099 | 1.088 |
| Região Sul | 982 | 982 |
| Região Leste | 760 | 748 |
| Região Centro-Sul | 722 | 713 |
| Região Norte | 146 | 146 |
| Região Oeste | 99 | 99 |
| Região Central | 20 | 20 |
| Contratado/Credenciado | 1 | 1 |
| URD | 1 | 1 |
| sem Região de Saúde | 24 | 24 |

**mama**, na medida da fila (o conjunto do objeto):

| Região de Saúde | fila | pessoas |
|---|---|---|
| Região Sudoeste | 5.215 | 5.208 |
| Região Sul | 2.228 | 2.217 |
| Região Leste | 1.723 | 1.722 |
| Região Oeste | 1.621 | 1.618 |
| Região Central | 1.370 | 1.370 |
| Região Centro-Sul | 519 | 519 |
| Região Norte | 109 | 109 |
| URD | 10 | 10 |
| Contratado/Credenciado | 1 | 1 |
| sem Região de Saúde | 154 | 154 |

**doppler_membros**, na medida da fila (o conjunto do objeto):

| Região de Saúde | fila | pessoas |
|---|---|---|
| Região Sul | 4.335 | 4.029 |
| Região Norte | 3.827 | 3.220 |
| Região Sudoeste | 3.169 | 2.962 |
| Região Central | 517 | 517 |
| Região Centro-Sul | 7 | 6 |
| Região Leste | 3 | 2 |
| sem Região de Saúde | 185 | 157 |

**pelvica**, na medida da fila (o conjunto do objeto):

| Região de Saúde | fila | pessoas |
|---|---|---|
| Região Leste | 410 | 404 |
| Região Centro-Sul | 314 | 312 |
| Região Sul | 128 | 128 |
| Região Oeste | 88 | 88 |
| Região Sudoeste | 58 | 57 |
| Região Central | 3 | 3 |
| Região Norte | 3 | 3 |
| URD | 1 | 1 |
| sem Região de Saúde | 9 | 9 |

**tc_torax**, na medida da fila (o conjunto do objeto):

| Região de Saúde | fila | pessoas |
|---|---|---|
| URD | 1.287 | 1.274 |
| Contratado/Credenciado | 607 | 597 |
| Região Sudoeste | 537 | 533 |
| Região Oeste | 197 | 197 |
| Região Norte | 156 | 155 |
| Região Sul | 131 | 130 |
| Região Leste | 128 | 127 |
| Região Central | 108 | 108 |
| Região Centro-Sul | 48 | 48 |
| sem Região de Saúde | 15 | 15 |

**tc_cranio**, na medida da fila (o conjunto do objeto):

| Região de Saúde | fila | pessoas |
|---|---|---|
| URD | 251 | 248 |
| Região Sudoeste | 145 | 145 |
| Contratado/Credenciado | 103 | 99 |
| Região Oeste | 73 | 72 |
| Região Leste | 60 | 60 |
| Região Sul | 55 | 55 |
| Região Norte | 52 | 52 |
| Região Centro-Sul | 30 | 30 |
| Região Central | 23 | 23 |
| sem Região de Saúde | 9 | 9 |

**tc_face**, na medida da fila (o conjunto do objeto):

| Região de Saúde | fila | pessoas |
|---|---|---|
| URD | 64 | 63 |
| Região Sudoeste | 26 | 26 |
| Contratado/Credenciado | 19 | 19 |
| Região Oeste | 11 | 11 |
| Região Leste | 8 | 8 |
| Região Central | 4 | 4 |
| Região Norte | 4 | 4 |
| Região Centro-Sul | 2 | 2 |
| Região Sul | 1 | 1 |
| sem Região de Saúde | 0 | 0 |

**transvaginal**, na medida da fila (o conjunto do objeto):

| Região de Saúde | fila | pessoas |
|---|---|---|
| Região Sudoeste | 4.352 | 4.351 |
| Região Leste | 2.722 | 2.722 |
| Região Sul | 1.444 | 1.444 |
| Região Centro-Sul | 423 | 423 |
| Região Norte | 129 | 129 |
| Região Central | 101 | 101 |
| Região Oeste | 34 | 34 |
| Contratado/Credenciado | 1 | 1 |
| URD | 1 | 1 |
| sem Região de Saúde | 87 | 87 |

## Nomes internos

O nome pedido na ordem e o nome exato do motor, com o invisível à mostra ({NBSP} é o espaço não separável). O JSON guarda o exato.

| pedido | exato |
|---|---|
| 061. TC DO ABDOMEN SUPERIOR ADULTO S/CONTRASTE S/SEDACAO | 061. TC DO ABDOMEN SUPERIOR ADULTO S/CONTRASTE S/SEDACAO |
| 063. TC DO ABDOMEN SUPERIOR ADULTO C/CONTRASTE S/SEDACAO | 063. TC DO ABDOMEN SUPERIOR ADULTO C/CONTRASTE S/SEDACAO |
| ANGIOTOMOGRAFIA DA AORTA ABDOMINAL E DOS SEUS RAMOS ADULTO S/SEDACAO{NBSP} | ANGIOTOMOGRAFIA DA AORTA ABDOMINAL E DOS SEUS RAMOS ADULTO S/SEDACAO{NBSP} |
| ANGIOTOMOGRAFIA DO ABDOME SUPERIOR ADULTO S/SEDACAO{NBSP} | ANGIOTOMOGRAFIA DO ABDOME SUPERIOR ADULTO S/SEDACAO{NBSP} |
| ANGIOTOMOGRAFIA DAS ARTERIAS CAROTIDAS E VERTEBRAIS ADULTO S/SEDACAO | ANGIOTOMOGRAFIA DAS ARTERIAS CAROTIDAS E VERTEBRAIS ADULTO S/SEDACAO |
| ANGIOTOMOGRAFIA DAS ARTÉRIAS RENAIS ADULTO S/SEDACAO | ANGIOTOMOGRAFIA DAS ARTÉRIAS RENAIS ADULTO S/SEDACAO |
| 109. TC DE PELVE OU BACIA ADULTO S/CONTRASTE  S/SEDACAO | 109. TC DE PELVE OU BACIA ADULTO S/CONTRASTE  S/SEDACAO |
| 111. TC DE PELVE OU BACIA ADULTO C/CONTRASTE S/SEDACAO | 111. TC DE PELVE OU BACIA ADULTO C/CONTRASTE S/SEDACAO |
| ANGIOTOMOGRAFIA DA PELVE ADULTO S/SEDACAO | ANGIOTOMOGRAFIA DA PELVE ADULTO S/SEDACAO |
| ULTRA-SONOGRAFIA TRANSFONTANELA | ULTRA-SONOGRAFIA TRANSFONTANELA |
| 119. TC DE PESCOCO ADULTO C/CONTRASTE S/SEDACAO | 119. TC DE PESCOCO ADULTO C/CONTRASTE S/SEDACAO |
| ANGIOTOMOGRAFIA DO PESCOCO ADULTO S/SEDACAO | ANGIOTOMOGRAFIA DO PESCOCO ADULTO S/SEDACAO |
| ECOGRAFIA DE ABDOMEN SUPERIOR ADULTO | ECOGRAFIA DE ABDOMEN SUPERIOR ADULTO |
| ECOGRAFIA DE BOLSA ESCROTAL ADULTO | ECOGRAFIA DE BOLSA ESCROTAL ADULTO |
| ECOGRAFIA DE BOLSA ESCROTAL INFANTIL | ECOGRAFIA DE BOLSA ESCROTAL INFANTIL |
| ECOGRAFIA DO APARELHO URINARIO (RINS, BEXIGA) ADULTO | ECOGRAFIA DO APARELHO URINARIO (RINS, BEXIGA) ADULTO |
| ECOGRAFIA DO APARELHO URINARIO (RINS, BEXIGA) INFANTIL | ECOGRAFIA DO APARELHO URINARIO (RINS, BEXIGA) INFANTIL |
| ULTRASSONOGRAFIA RENAL | ULTRASSONOGRAFIA RENAL |
| ECOGRAFIA DE ABDOMEN TOTAL ADULTO | ECOGRAFIA DE ABDOMEN TOTAL ADULTO |
| ECOGRAFIA DE ABDOMEN TOTAL INFANTIL | ECOGRAFIA DE ABDOMEN TOTAL INFANTIL |
| ULTRASONOGRAFIA DE PAREDE ABDOMINAL | ULTRASONOGRAFIA DE PAREDE ABDOMINAL |
| 10. ECODOPPLER DE CAROTIDAS | 10. ECODOPPLER DE CAROTIDAS |
| ULTRA-SONOGRAFIA  DOPPLER DE CAROTIDAS E VERTEBRAIS | ULTRA-SONOGRAFIA  DOPPLER DE CAROTIDAS E VERTEBRAIS; ULTRA-SONOGRAFIA DOPPLER DE CAROTIDAS E VERTEBRAIS |
| ULTRA-SONOGRAFIA DOPPLER COLORIDO DE VASOS | ULTRA-SONOGRAFIA DOPPLER COLORIDO DE VASOS |
| ECOGRAFIA TRANSVAGINAL COM DOPPLER | ECOGRAFIA TRANSVAGINAL COM DOPPLER |
| ULTRASSONOGRAFIA COM DOPPLER COLORIDO DE ARTERIAS RENAIS | ULTRASSONOGRAFIA COM DOPPLER COLORIDO DE ARTERIAS RENAIS |
| ECOGRAFIA DE PROSTATA ( VIA ABDOMINAL ) | ECOGRAFIA DE PROSTATA ( VIA ABDOMINAL ) |
| ECOGRAFIA DE TIREOIDE ADULTO | ECOGRAFIA DE TIREOIDE ADULTO |
| ULTRA-SONOGRAFIA DOPPLER DE TIREOIDE | ULTRA-SONOGRAFIA DOPPLER DE TIREOIDE |
| ECOGRAFIA DE TIREOIDE INFANTIL | ECOGRAFIA DE TIREOIDE INFANTIL |
| ECOGRAFIA DE MAMAS - BILATERAL | ECOGRAFIA DE MAMAS - BILATERAL |
| ULTRA-SONOGRAFIA DOPPLER VENOSO - MMII ( BILATERAL) | ULTRA-SONOGRAFIA DOPPLER VENOSO - MMII ( BILATERAL) |
| ULTRA-SONOGRAFIA DOPPLER ARTERIAL - MMII (BILATERAL) | ULTRA-SONOGRAFIA DOPPLER ARTERIAL - MMII (BILATERAL) |
| ULTRA-SONOGRAFIA DOPPLER VENOSO - MMSS ( BILATERAL) | ULTRA-SONOGRAFIA DOPPLER VENOSO - MMSS ( BILATERAL) |
| ULTRA-SONOGRAFIA DOPPLER ARTERIAL - MMSS (BILATERAL) | ULTRA-SONOGRAFIA DOPPLER ARTERIAL - MMSS (BILATERAL) |
| ECOGRAFIA PELVICA (GINECOLOGICA) - ADULTO | ECOGRAFIA PELVICA (GINECOLOGICA) - ADULTO |
| ECOGRAFIA PELVICA (GINECOLOGICA) - INFANTIL | ECOGRAFIA PELVICA (GINECOLOGICA) - INFANTIL |
| 053. TC DO TORAX  ADULTO S/CONTRASTE S/SEDACAO | 053. TC DO TORAX  ADULTO S/CONTRASTE S/SEDACAO |
| 055. TC DO TORAX ADULTO C/CONTRASTE S/SEDACAO | 055. TC DO TORAX ADULTO C/CONTRASTE S/SEDACAO |
| ANGIOTOMOGRAFIA DA AORTA TORÁCICA E SEUS RAMOS{NBSP} ADULTO S/SEDACAO{NBSP} | ANGIOTOMOGRAFIA DA AORTA TORÁCICA E SEUS RAMOS{NBSP} ADULTO S/SEDACAO{NBSP} |
| ANGIOTOMOGRAFIA DO TORAX OU PULMONAR ADULTO S/SEDACAO | ANGIOTOMOGRAFIA DO TORAX OU PULMONAR ADULTO S/SEDACAO |
| 029. TC DE CRANIO ADULTO S/CONTRASTE S/SEDACAO | 029. TC DE CRANIO ADULTO S/CONTRASTE S/SEDACAO |
| ANGIOTOMOGRAFIA DO CRANIO ADULTO S/SEDACAO | ANGIOTOMOGRAFIA DO CRANIO ADULTO S/SEDACAO |
| 031. TC DE CRANIO ADULTO C/CONTRASTE S/SEDACAO | 031. TC DE CRANIO ADULTO C/CONTRASTE S/SEDACAO |
| 071. TC DE FACE ADULTO C/CONTRASTE S/SEDACAO | 071. TC DE FACE ADULTO C/CONTRASTE S/SEDACAO |
| 079. TC DE SEIOS DE FACE ADULTO C/CONTRASTE S/SEDACAO | 079. TC DE SEIOS DE FACE ADULTO C/CONTRASTE S/SEDACAO |
| ECOGRAFIA TRANSVAGINAL | ECOGRAFIA TRANSVAGINAL |

## Diferença para a coleta anterior

Contra `dados/fontes/mapa_social_20261102_imagem_bruto/coleta_20261102.json` (recarga 02/11/2026 10:31:47). Diferença **calculada** no montador.

A coleta anterior não tem as mesmas filas nem os mesmos objetos.
