# Mapa Social da Saúde — fila de Ultrassonografia de articulação (02.05.02.006-2), coleta de 27/10/2026

Ordem de coleta: US de articulação 02.05.02.006-2 completa para o R$ 1,5 mi de imagem (Emenda 71080005): fila, viva, devolvidas, por nome de fila, dentro e fora do CID da OCI 09.03.01.002-0 do IEV, região, idade, CID, ano e entrantes por mês

Coleta montada por `ferramentas/montar_coleta.py` a partir da saída do kit do motor: o modelo não escreveu número nenhum, e o resumo não se edita à mão (conferência K). A decisão de cada fila vem do enquadramento do plano.

| campo | conteúdo |
|---|---|
| Fonte | Mapa Social da Saúde – Regulamentação (MPDFT) · Lista de Espera – Exames e Consultas · `https://paineis-ext.mpdft.mp.br/extensions/mapasauderegulamentacao/mapasauderegulamentacao.html` · app Qlik `7edb02fa-f1f5-4ea6-b348-049a4ac2d095` · dados SISREG/DATASUS |
| Última recarga da base | 27/10/2026 08:33:03 (qLastReloadTime 2026-10-27T11:33:03.576Z) |
| Consulta | 27/10/2026 09:12:05 a 09:12:31 (relógio do motor), sem recarga no meio |
| Solicitação mais recente na base | 27/10/2026 (agendamento mais distante: 27/01/2027) |
| Medida | **fila** = os três status: pendente de regulação, corrigida e reenviada para regulação, pendente de regulação por fila de espera. Devolvidas para complementação ficam fora e são contadas à parte |
| Fila viva | só as solicitações a partir de `data_solicitacao={">=27/10/2024"}` (24 meses contados da solicitação mais recente) |
| Agendadas em 12 meses | `data_agendamento={">=27/10/2025<=26/10/2026"}`, todos os status |
| Ordem | medicao; `ordem.json` (hash 3217843873) |
| Via | kit do motor `ferramentas/mapa_social/motor.js` (versão 2026-10-27, assinatura 3348663882); saída pela transcrição, 4 parte(s) conferidas por hash (`ferramentas/ler_motor.py`) |

Pessoas = CNS distintos no conjunto (quem espera por mais de um exame conta uma vez); só a contagem sai do motor. Espera em dias, calculada no motor sobre os registros do conjunto.

## Alarmes

Limites de `ferramentas/conferir_coleta.py`: 30% (CID dominante), 5% (CID raro), 30% (fila velha), 3 anos (estoque), 20 categorias (CID largo).

- **estoque**: DOPPLER DE AORTA E ILIACA: 6 na fila, sem agendamento em 12 meses
- **fila velha**: DOPPLER DE AORTA E ILIACA: 6 de 6 pedidos de antes da janela
- **estoque**: ECOGRAFIA DE ARTICULACAO COXO-FEMURAL D INFANTIL: 77 na fila, 5,5 anos de agendamentos
- **estoque**: ECOGRAFIA DE ARTICULACAO COXO-FEMURAL E INFANTIL: 82 na fila, 6,8 anos de agendamentos
- **fila velha**: ECOGRAFIA DE ARTICULACAO JOELHO D ADULTO: 192 de 552 pedidos de antes da janela
- **fila velha**: ECOGRAFIA DE ARTICULACAO JOELHO D INFANTIL: 5 de 16 pedidos de antes da janela
- **fila velha**: ECOGRAFIA DE ARTICULACAO JOELHO E ADULTO: 202 de 595 pedidos de antes da janela
- **fila velha**: ECOGRAFIA DE ARTICULACAO NAO LISTADA: 44 de 97 pedidos de antes da janela
- **fila velha**: ECOGRAFIA DE PARTES MOLES: 1.246 de 3.124 pedidos de antes da janela
- **estoque**: ECOGRAFIA DE ARTICULACAO COLUNA LOMBAR: 134 na fila, 33,5 anos de agendamentos
- **fila velha**: ECOGRAFIA DE ARTICULACAO COLUNA LOMBAR: 41 de 134 pedidos de antes da janela
- **estoque**: ECOGRAFIA DE ARTICULACAO COTOVELO D INFANTIL: 1 na fila, sem agendamento em 12 meses
- **estoque**: ECOGRAFIA DE ARTICULACAO COTOVELO E INFANTIL: 1 na fila, sem agendamento em 12 meses
- **fila velha**: ECOGRAFIA DE ARTICULACAO PUNHO D INFANTIL: 2 de 6 pedidos de antes da janela
- **fila velha**: ECOGRAFIA DE ARTICULACAO PUNHO E INFANTIL: 4 de 9 pedidos de antes da janela
- **estoque**: ECOGRAFIA DE QUADRIL DIREITO: 4 na fila, 4,0 anos de agendamentos
- **estoque**: ULTRA-SONOGRAFIA DE REGIAO CERVICAL (PESCOCO): 2 na fila, sem agendamento em 12 meses
- **fila velha**: ULTRA-SONOGRAFIA DE REGIAO CERVICAL (PESCOCO): 2 de 2 pedidos de antes da janela
- **fila velha**: ULTRASSONOGRAFIA DA BACIA: 2 de 4 pedidos de antes da janela
- **estoque**: ULTRASSONOGRAFIA DA REGIAO GLUTEA: 5 na fila, sem agendamento em 12 meses
- **fila velha**: ULTRASSONOGRAFIA DA REGIAO GLUTEA: 2 de 5 pedidos de antes da janela
- **estoque**: ULTRASSONOGRAFIA DA REGIAO LOMBAR: 55 na fila, 18,3 anos de agendamentos
- **estoque**: ULTRASSONOGRAFIA DO CALCANEO: 15 na fila, sem agendamento em 12 meses
- **estoque**: ULTRASSONOGRAFIA DO DEDO: 17 na fila, 8,5 anos de agendamentos
- **fila velha**: ULTRASSONOGRAFIA DO DEDO: 7 de 17 pedidos de antes da janela
- **estoque**: ULTRASSONOGRAFIA DO PESCOCO: 160 na fila, 4,6 anos de agendamentos
- **estoque**: USB AXILA DIREITA: 23 na fila, sem agendamento em 12 meses
- **estoque**: USG AXILA ESQUERDA: 20 na fila, sem agendamento em 12 meses
- **fila velha**: USG AXILA ESQUERDA: 7 de 20 pedidos de antes da janela
- **fila velha**: USG BRACO DIREITO: 21 de 28 pedidos de antes da janela
- **estoque**: USG BRACO ESQUERDO: 50 na fila, 5,0 anos de agendamentos
- **fila velha**: USG BRACO ESQUERDO: 43 de 50 pedidos de antes da janela
- **estoque**: USG COXA DIREITA: 1 na fila, sem agendamento em 12 meses
- **fila velha**: USG COXA DIREITA: 1 de 1 pedidos de antes da janela
- **estoque**: USG OMBRO ESQUERDO: 1 na fila, sem agendamento em 12 meses
- **fila velha**: USG OMBRO ESQUERDO: 1 de 1 pedidos de antes da janela
- **fila velha**: USG PE DIREITO: 40 de 114 pedidos de antes da janela
- **estoque**: USG PERNA DIREITA: 17 na fila, 3,4 anos de agendamentos
- **estoque**: USG PERNA ESQUERDA: 27 na fila, 4,5 anos de agendamentos
- **fila velha**: USG PERNA ESQUERDA: 10 de 27 pedidos de antes da janela
- **fila velha**: USG TENDAO DE AQUILES ESQUERDO: 2 de 6 pedidos de antes da janela

## Lacunas

nenhuma

## Exames

A união das filas de cada exame, na idade e no sexo da ordem, quando ela os dá.

| exame | filas | fila | fila viva | pessoas | pessoas viva | devolvidas | espera média | espera mediana |
|---|---|---|---|---|---|---|---|---|
| Ultrassonografia de articulação (02.05.02.006-2) | 61 | 14.428 | 10.433 | **11.465** | 8.119 | 4.923 | 546,5 | 398,6 |

## Filas do objeto

As filas de partida da ordem, pelo nome exato do motor, sem recorte de CID. Anos de estoque = fila ÷ agendadas em 12 meses (**calculado** no montador).

| fila | código | objeto | papel | fila | fila viva | pessoas | devolvidas | espera média | espera mediana | espera máxima | pedido mais antigo | agendadas 12 m | anos de estoque | CID principais |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| USG MAO ESQUERDA | 02.05.02.006-2 | 02.05.02.006-2 | exame | 142 | 108 | 142 | 27 | 475,5 | 365,7 | 1.356,7 | 08/02/2023 | 112 | 1,3 | — |
| USG QUADRIL | 02.05.02.006-2 | 02.05.02.006-2 | exame | 121 | 108 | 121 | 18 | 332,7 | 270,6 | 1.357,5 | 07/02/2023 | 93 | 1,3 | — |
| USG PE DIREITO | 02.05.02.006-2 | 02.05.02.006-2 | exame | 114 | 74 | 114 | 20 | 542,0 | 400,8 | 1.357,6 | 07/02/2023 | 63 | 1,8 | — |
| USG PE ESQUERDO | 02.05.02.006-2 | 02.05.02.006-2 | exame | 99 | 71 | 98 | 29 | 494,0 | 391,6 | 1.356,6 | 08/02/2023 | 62 | 1,6 | — |
| USG MAO DIREITA | 02.05.02.006-2 | 02.05.02.006-2 | exame | 197 | 164 | 197 | 31 | 414,8 | 278,6 | 1.356,7 | 08/02/2023 | 133 | 1,5 | — |
| ECOGRAFIA DE ARTICULACAO COXA DIREITA | 02.05.02.006-2 | 02.05.02.006-2 | exame | 1 | 1 | 1 | 3 | 29,0 | 29,0 | 29,0 | 28/09/2026 | 4 | 0,2 | — |
| ECOGRAFIA DE ARTICULACAO COXA ESQUERDA | 02.05.02.006-2 | 02.05.02.006-2 | exame | 2 | 2 | 2 | 2 | 100,7 | 100,7 | 200,6 | 09/04/2026 | 8 | 0,2 | — |
| ULTRASSONOGRAFIA DO CALCANEO | 02.05.02.006-2 | 02.05.02.006-2 | exame | 15 | 11 | 15 | 2 | 418,1 | 370,1 | 1.160,9 | 23/08/2023 | 0 | sem agendamento | — |
| ULTRASSONOGRAFIA DO DEDO | 02.05.02.006-2 | 02.05.02.006-2 | exame | 17 | 10 | 17 | 1 | 592,7 | 424,7 | 1.230,0 | 15/06/2023 | 2 | 8,5 | — |
| USG TENDAO DE AQUILES ESQUERDO | 02.05.02.006-2 | 02.05.02.006-2 | exame | 6 | 4 | 6 | 2 | 663,9 | 692,9 | 1.082,9 | 09/11/2023 | 5 | 1,2 | — |
| ECOGRAFIA DE ARTICULACAO OMBRO E ADULTO | 02.05.02.006-2 | 02.05.02.006-2 | exame | 1.530 | 1.171 | 1.529 | 585 | 535,7 | 384,6 | 2.118,8 | 07/01/2021 | 849 | 1,8 | — |
| ECOGRAFIA DE ARTICULACAO PUNHO E ADULTO | 02.05.02.006-2 | 02.05.02.006-2 | exame | 1.461 | 1.153 | 1.460 | 346 | 494,2 | 369,6 | 2.117,9 | 08/01/2021 | 611 | 2,4 | — |
| ECOGRAFIA DE ARTICULACAO TORNOZELO E ADULTO | 02.05.02.006-2 | 02.05.02.006-2 | exame | 376 | 306 | 375 | 118 | 466,4 | 364,3 | 2.106,7 | 19/01/2021 | 224 | 1,7 | — |
| ECOGRAFIA DE ARTICULACAO COTOVELO E ADULTO | 02.05.02.006-2 | 02.05.02.006-2 | exame | 143 | 111 | 143 | 59 | 463,1 | 317,7 | 2.105,7 | 20/01/2021 | 221 | 0,6 | — |
| ECOGRAFIA DE ARTICULACAO COXO-FEMURAL E ADULTO | 02.05.02.006-2 | 02.05.02.006-2 | exame | 37 | 27 | 37 | 27 | 522,3 | 214,0 | 2.076,4 | 18/02/2021 | 14 | 2,6 | — |
| ECOGRAFIA DE ARTICULACAO JOELHO D ADULTO | 02.05.02.006-2 | 02.05.02.006-2 | exame | 552 | 360 | 552 | 63 | 593,1 | 542,4 | 2.097,9 | 28/01/2021 | 332 | 1,7 | — |
| ECOGRAFIA DE ARTICULACAO COXO-FEMURAL D INFANTIL | 02.05.02.006-2 | 02.05.02.006-2 | exame | 77 | 68 | 77 | 12 | 360,2 | 319,7 | 914,7 | 25/04/2024 | 14 | 5,5 | — |
| ECOGRAFIA DE ARTICULACAO COXO-FEMURAL E INFANTIL | 02.05.02.006-2 | 02.05.02.006-2 | exame | 82 | 67 | 82 | 12 | 415,0 | 391,2 | 1.176,6 | 07/08/2023 | 12 | 6,8 | — |
| ECOGRAFIA DE ARTICULACAO JOELHO E INFANTIL | 02.05.02.006-2 | 02.05.02.006-2 | exame | 15 | 11 | 15 | 2 | 512,7 | 108,7 | 2.054,9 | 12/03/2021 | 10 | 1,5 | — |
| ECOGRAFIA DE ARTICULACAO JOELHO D INFANTIL | 02.05.02.006-2 | 02.05.02.006-2 | exame | 16 | 11 | 16 | 2 | 641,9 | 461,3 | 2.055,6 | 11/03/2021 | 14 | 1,1 | — |
| ECOGRAFIA DE ARTICULACAO COTOVELO D INFANTIL | 02.05.02.006-2 | 02.05.02.006-2 | exame | 1 | 1 | 1 | 5 | 21,9 | 21,9 | 21,9 | 05/10/2026 | 0 | sem agendamento | — |
| ECOGRAFIA DE ARTICULACAO PUNHO D INFANTIL | 02.05.02.006-2 | 02.05.02.006-2 | exame | 6 | 4 | 6 | 3 | 510,1 | 476,2 | 788,7 | 29/08/2024 | 4 | 1,5 | — |
| ECOGRAFIA DE ARTICULACAO PUNHO E INFANTIL | 02.05.02.006-2 | 02.05.02.006-2 | exame | 9 | 5 | 9 | 3 | 769,6 | 687,0 | 1.414,7 | 12/12/2022 | 5 | 1,8 | — |
| USG OMBRO ESQUERDO | 02.05.02.006-2 | 02.05.02.006-2 | exame | 1 | 0 | 1 | 62 | 3.387,6 | 3.387,6 | 3.387,6 | 18/07/2017 | 0 | sem agendamento | — |
| ECOGRAFIA DE ARTICULACAO NAO LISTADA | 02.05.02.006-2 | 02.05.02.006-2 | exame | 97 | 53 | 97 | 262 | 915,3 | 623,9 | 2.111,7 | 14/01/2021 | 51 | 1,9 | — |
| ECOGRAFIA DE ARTICULACAO COTOVELO E INFANTIL | 02.05.02.006-2 | 02.05.02.006-2 | exame | 1 | 1 | 1 | 1 | 19,8 | 19,8 | 19,8 | 07/10/2026 | 0 | sem agendamento | — |
| ECOGRAFIA DE ARTICULACAO COXO-FEMURAL D ADULTO | 02.05.02.006-2 | 02.05.02.006-2 | exame | 46 | 36 | 46 | 26 | 558,1 | 371,2 | 2.092,7 | 02/02/2021 | 26 | 1,8 | — |
| ECOGRAFIA DE ARTICULACAO OMBRO D ADULTO | 02.05.02.006-2 | 02.05.02.006-2 | exame | 1.962 | 1.459 | 1.960 | 743 | 558,9 | 392,0 | 2.113,9 | 12/01/2021 | 1.187 | 1,7 | — |
| ECOGRAFIA DE ARTICULACAO PUNHO D ADULTO | 02.05.02.006-2 | 02.05.02.006-2 | exame | 1.696 | 1.298 | 1.695 | 380 | 511,6 | 369,9 | 5.877,3 | 24/09/2010 | 713 | 2,4 | — |
| ECOGRAFIA DE ARTICULACAO TORNOZELO D ADULTO | 02.05.02.006-2 | 02.05.02.006-2 | exame | 334 | 274 | 334 | 138 | 441,4 | 331,3 | 2.055,9 | 11/03/2021 | 238 | 1,4 | — |
| ECOGRAFIA DE ARTICULACAO JOELHO E ADULTO | 02.05.02.006-2 | 02.05.02.006-2 | exame | 595 | 393 | 595 | 69 | 577,3 | 501,9 | 2.097,9 | 28/01/2021 | 315 | 1,9 | — |
| ECOGRAFIA DE ARTICULACAO COTOVELO D ADULTO | 02.05.02.006-2 | 02.05.02.006-2 | exame | 216 | 157 | 216 | 72 | 522,7 | 293,8 | 2.069,9 | 25/02/2021 | 262 | 0,8 | — |
| ECOGRAFIA DE QUADRIL DIREITO | 02.05.02.006-2 | 02.05.02.006-2 | exame | 4 | 4 | 4 | 0 | 50,4 | 50,4 | 75,8 | 12/08/2026 | 1 | 4,0 | — |
| ECOGRAFIA DE QUADRIL ESQUERDO | 02.05.02.006-2 | 02.05.02.006-2 | exame | 2 | 2 | 2 | 0 | 24,9 | 24,9 | 24,9 | 02/10/2026 | 1 | 2,0 | — |
| USG TENDAO DE AQUILES DIREITO | 02.05.02.006-2 | 02.05.02.006-2 | exame | 1 | 1 | 1 | 0 | 124,6 | 124,6 | 124,6 | 24/06/2026 | 6 | 0,2 | — |
| ECOGRAFIA DE ARTICULACAO TORNOZELO E INFANTIL | 02.05.02.006-2 | 02.05.02.006-2 | exame | 3 | 3 | 3 | 0 | 161,2 | 34,9 | 419,6 | 02/09/2025 | 2 | 1,5 | — |
| ECOGRAFIA DE ARTICULACAO TORNOZELO D INFANTIL | 02.05.02.006-2 | 02.05.02.006-2 | exame | 2 | 2 | 2 | 0 | 159,3 | 159,3 | 219,8 | 21/03/2026 | 5 | 0,4 | — |
| ECOGRAFIA DE PARTES MOLES | 02.05.02.006-2 | 02.05.02.006-2 | exame | 3.124 | 1.878 | 3.122 | 1.456 | 650,8 | 497,8 | 5.843,3 | 28/10/2010 | 1.427 | 2,2 | — |
| ECOGRAFIA DE REGIÃO INGUINAL ESQUERDO | 02.05.02.006-2 | 02.05.02.006-2 | exame | 201 | 179 | 201 | 12 | 349,0 | 273,6 | 1.432,9 | 24/11/2022 | 216 | 0,9 | — |
| ECOGRAFIA DE REGIAO INGUINAL DIREITO | 02.05.02.006-2 | 02.05.02.006-2 | exame | 241 | 213 | 241 | 16 | 373,8 | 321,9 | 1.327,8 | 09/03/2023 | 259 | 0,9 | — |
| ULTRASSONOGRAFIA DA REGIAO INGUINAL | 02.05.02.006-2 | 02.05.02.006-2 | exame | 166 | 132 | 166 | 26 | 436,0 | 434,8 | 1.307,9 | 29/03/2023 | 260 | 0,6 | — |
| ULTRASSONOGRAFIA DO PESCOCO | 02.05.02.006-2 | 02.05.02.006-2 | exame | 160 | 119 | 160 | 8 | 508,6 | 478,8 | 1.358,8 | 06/02/2023 | 35 | 4,6 | — |
| ULTRASSONOGRAFIA COM DOPPLER COLORIDO DE REGIAO CERVICAL | 02.05.02.006-2 | 02.05.02.006-2 | exame | 17 | 14 | 17 | 33 | 420,8 | 483,7 | 858,9 | 20/06/2024 | 13 | 1,3 | — |
| ULTRASSONOGRAFIA CERVICAL | 02.05.02.006-2 | 02.05.02.006-2 | exame | 100 | 86 | 100 | 38 | 333,4 | 171,7 | 1.348,7 | 16/02/2023 | 151 | 0,7 | — |
| ULTRA-SONOGRAFIA DE REGIAO CERVICAL (PESCOCO) | 02.05.02.006-2 | 02.05.02.006-2 | exame | 2 | 0 | 2 | 0 | 3.772,0 | 3.772,0 | 6.025,3 | 29/04/2010 | 0 | sem agendamento | — |
| USG PERNA ESQUERDA | 02.05.02.006-2 | 02.05.02.006-2 | exame | 27 | 17 | 27 | 62 | 523,9 | 287,9 | 1.293,6 | 12/04/2023 | 6 | 4,5 | — |
| USG PERNA DIREITA | 02.05.02.006-2 | 02.05.02.006-2 | exame | 17 | 12 | 17 | 57 | 537,9 | 461,6 | 1.293,6 | 12/04/2023 | 5 | 3,4 | — |
| USG ESTRUTURA SUPERFICIE | 02.05.02.006-2 | 02.05.02.006-2 | exame | 2 | 2 | 2 | 24 | 14,9 | 14,9 | 18,9 | 08/10/2026 | 4 | 0,5 | — |
| USG BRACO DIREITO | 02.05.02.006-2 | 02.05.02.006-2 | exame | 28 | 7 | 28 | 15 | 1.001,0 | 1.356,7 | 1.356,7 | 08/02/2023 | 18 | 1,6 | — |
| ECOGRAFIA PELVICA | 02.05.02.006-2 | 02.05.02.006-2 | exame | 46 | 46 | 46 | 15 | 88,6 | 82,7 | 166,7 | 13/05/2026 | 21 | 2,2 | — |
| USB AXILA DIREITA | 02.05.02.006-2 | 02.05.02.006-2 | exame | 23 | 17 | 23 | 1 | 620,3 | 613,6 | 965,0 | 06/03/2024 | 0 | sem agendamento | — |
| USG BRACO ESQUERDO | 02.05.02.006-2 | 02.05.02.006-2 | exame | 50 | 7 | 50 | 10 | 1.178,4 | 1.356,7 | 1.356,7 | 08/02/2023 | 10 | 5,0 | — |
| USG ANTEBRACO ESQUERDO | 02.05.02.006-2 | 02.05.02.006-2 | exame | 8 | 6 | 8 | 9 | 642,0 | 609,1 | 1.064,7 | 27/11/2023 | 8 | 1,0 | — |
| ULTRASSONOGRAFIA DA REGIAO LOMBAR | 02.05.02.006-2 | 02.05.02.006-2 | exame | 55 | 45 | 55 | 7 | 459,5 | 408,8 | 1.113,0 | 10/10/2023 | 3 | 18,3 | — |
| ULTRASSONOGRAFIA DAS GLANDULAS SUBMANDIBULARES | 02.05.02.006-2 | 02.05.02.006-2 | exame | 12 | 11 | 12 | 2 | 201,6 | 75,8 | 873,9 | 05/06/2024 | 11 | 1,1 | — |
| ULTRASSONOGRAFIA DA BACIA | 02.05.02.006-2 | 02.05.02.006-2 | exame | 4 | 2 | 4 | 3 | 606,9 | 575,3 | 1.173,8 | 10/08/2023 | — | — | — |
| ECOGRAFIA DE ARTICULACAO COLUNA LOMBAR | 02.05.02.006-2 | 02.05.02.006-2 | exame | 134 | 93 | 134 | 1 | 519,9 | 517,9 | 915,7 | 24/04/2024 | 4 | 33,5 | — |
| USG COXA DIREITA | 02.05.02.006-2 | 02.05.02.006-2 | exame | 1 | 0 | 1 | 1 | 1.419,7 | 1.419,7 | 1.419,7 | 07/12/2022 | 0 | sem agendamento | — |
| USG AXILA ESQUERDA | 02.05.02.006-2 | 02.05.02.006-2 | exame | 20 | 13 | 20 | 2 | 660,1 | 617,3 | 965,0 | 06/03/2024 | 0 | sem agendamento | — |
| ULTRASSONOGRAFIA DA REGIAO GLUTEA | 02.05.02.006-2 | 02.05.02.006-2 | exame | 5 | 3 | 5 | 0 | 665,9 | 629,9 | 1.162,9 | 21/08/2023 | 0 | sem agendamento | — |
| DOPPLER DE AORTA E ILIACA | 02.05.02.006-2 | 02.05.02.006-2 | exame | 6 | 0 | 6 | 0 | 1.523,2 | 1.519,0 | 1.543,9 | 05/08/2022 | 0 | sem agendamento | — |

**Por recorte de CID**, em pedidos:

| fila | recorte | fila | fila viva | parte da fila (calculado) | CID principais no recorte |
|---|---|---|---|---|---|
| USG MAO ESQUERDA | CID da OCI 09.03.01.002-0 | 9 | 7 | 6% | M65 9 |
| USG MAO ESQUERDA | fora do CID da OCI 09.03.01.002-0 | 133 | 101 | 94% | M25 28, M65 18, G56 18, M71 13, M79 8 |
| USG QUADRIL | CID da OCI 09.03.01.002-0 | 6 | 4 | 5% | M65 6 |
| USG QUADRIL | fora do CID da OCI 09.03.01.002-0 | 115 | 104 | 95% | Q65 44, M25 13, M70 8, M76 7, Q90 5 |
| USG PE DIREITO | CID da OCI 09.03.01.002-0 | 7 | 4 | 6% | M65 7 |
| USG PE DIREITO | fora do CID da OCI 09.03.01.002-0 | 107 | 70 | 94% | M72 38, M71 15, M25 14, M77 13, M79 6 |
| USG PE ESQUERDO | CID da OCI 09.03.01.002-0 | 5 | 4 | 5% | M65 5 |
| USG PE ESQUERDO | fora do CID da OCI 09.03.01.002-0 | 94 | 67 | 95% | M72 34, M25 14, M77 12, M71 6, M79 6 |
| USG MAO DIREITA | CID da OCI 09.03.01.002-0 | 31 | 25 | 16% | M65 31 |
| USG MAO DIREITA | fora do CID da OCI 09.03.01.002-0 | 166 | 139 | 84% | M25 31, M65 26, G56 21, M71 13, M79 9 |
| ECOGRAFIA DE ARTICULACAO COXA DIREITA | CID da OCI 09.03.01.002-0 | 0 | 0 | 0% | — |
| ECOGRAFIA DE ARTICULACAO COXA DIREITA | fora do CID da OCI 09.03.01.002-0 | 1 | 1 | 100% | Z54 1 |
| ECOGRAFIA DE ARTICULACAO COXA ESQUERDA | CID da OCI 09.03.01.002-0 | 0 | 0 | 0% | — |
| ECOGRAFIA DE ARTICULACAO COXA ESQUERDA | fora do CID da OCI 09.03.01.002-0 | 2 | 2 | 100% | Z00 1, D17 1 |
| ULTRASSONOGRAFIA DO CALCANEO | CID da OCI 09.03.01.002-0 | 1 | 1 | 7% | M65 1 |
| ULTRASSONOGRAFIA DO CALCANEO | fora do CID da OCI 09.03.01.002-0 | 14 | 10 | 93% | M76 4, M77 4, M25 2, M72 2, M79 1 |
| ULTRASSONOGRAFIA DO DEDO | CID da OCI 09.03.01.002-0 | 1 | 0 | 6% | M65 1 |
| ULTRASSONOGRAFIA DO DEDO | fora do CID da OCI 09.03.01.002-0 | 16 | 10 | 94% | M71 4, M79 3, M25 3, M65 2, M21 1 |
| USG TENDAO DE AQUILES ESQUERDO | CID da OCI 09.03.01.002-0 | 3 | 2 | 50% | M65 2, M66 1 |
| USG TENDAO DE AQUILES ESQUERDO | fora do CID da OCI 09.03.01.002-0 | 3 | 2 | 50% | M76 3 |
| ECOGRAFIA DE ARTICULACAO OMBRO E ADULTO | CID da OCI 09.03.01.002-0 | 98 | 60 | 6% | M65 96, M66 2 |
| ECOGRAFIA DE ARTICULACAO OMBRO E ADULTO | fora do CID da OCI 09.03.01.002-0 | 1.432 | 1.111 | 94% | M75 905, M25 253, M79 48, R52 42, Z00 18 |
| ECOGRAFIA DE ARTICULACAO PUNHO E ADULTO | CID da OCI 09.03.01.002-0 | 156 | 112 | 11% | M65 155, M87 1 |
| ECOGRAFIA DE ARTICULACAO PUNHO E ADULTO | fora do CID da OCI 09.03.01.002-0 | 1.305 | 1.041 | 89% | G56 563, M25 208, M71 141, M13 56, M79 53 |
| ECOGRAFIA DE ARTICULACAO TORNOZELO E ADULTO | CID da OCI 09.03.01.002-0 | 51 | 42 | 14% | M65 50, M66 1 |
| ECOGRAFIA DE ARTICULACAO TORNOZELO E ADULTO | fora do CID da OCI 09.03.01.002-0 | 325 | 264 | 86% | M25 91, M72 33, S93 29, M79 25, R52 23 |
| ECOGRAFIA DE ARTICULACAO COTOVELO E ADULTO | CID da OCI 09.03.01.002-0 | 10 | 9 | 7% | M65 10 |
| ECOGRAFIA DE ARTICULACAO COTOVELO E ADULTO | fora do CID da OCI 09.03.01.002-0 | 133 | 102 | 93% | M77 38, M25 24, G56 20, M70 12, M79 7 |
| ECOGRAFIA DE ARTICULACAO COXO-FEMURAL E ADULTO | CID da OCI 09.03.01.002-0 | 2 | 1 | 5% | M65 1, M87 1 |
| ECOGRAFIA DE ARTICULACAO COXO-FEMURAL E ADULTO | fora do CID da OCI 09.03.01.002-0 | 35 | 26 | 95% | M25 10, M70 8, M76 4, M79 3, K40 2 |
| ECOGRAFIA DE ARTICULACAO JOELHO D ADULTO | CID da OCI 09.03.01.002-0 | 7 | 5 | 1% | M65 7 |
| ECOGRAFIA DE ARTICULACAO JOELHO D ADULTO | fora do CID da OCI 09.03.01.002-0 | 545 | 355 | 99% | M23 191, M25 151, M17 57, S83 21, M79 18 |
| ECOGRAFIA DE ARTICULACAO COXO-FEMURAL D INFANTIL | CID da OCI 09.03.01.002-0 | 1 | 1 | 1% | M67 1 |
| ECOGRAFIA DE ARTICULACAO COXO-FEMURAL D INFANTIL | fora do CID da OCI 09.03.01.002-0 | 75 | 66 | 97% | Q65 47, Q90 4, P07 3, P03 3, Z13 3 |
| ECOGRAFIA DE ARTICULACAO COXO-FEMURAL E INFANTIL | CID da OCI 09.03.01.002-0 | 1 | 1 | 1% | M67 1 |
| ECOGRAFIA DE ARTICULACAO COXO-FEMURAL E INFANTIL | fora do CID da OCI 09.03.01.002-0 | 80 | 65 | 98% | Q65 49, Q90 4, P07 3, P03 3, S73 3 |
| ECOGRAFIA DE ARTICULACAO JOELHO E INFANTIL | CID da OCI 09.03.01.002-0 | 0 | 0 | 0% | — |
| ECOGRAFIA DE ARTICULACAO JOELHO E INFANTIL | fora do CID da OCI 09.03.01.002-0 | 15 | 11 | 100% | M25 5, M71 2, M23 2, L72 1, M21 1 |
| ECOGRAFIA DE ARTICULACAO JOELHO D INFANTIL | CID da OCI 09.03.01.002-0 | 0 | 0 | 0% | — |
| ECOGRAFIA DE ARTICULACAO JOELHO D INFANTIL | fora do CID da OCI 09.03.01.002-0 | 16 | 11 | 100% | M23 5, M25 3, M75 3, M71 1, R22 1 |
| ECOGRAFIA DE ARTICULACAO COTOVELO D INFANTIL | CID da OCI 09.03.01.002-0 | 0 | 0 | 0% | — |
| ECOGRAFIA DE ARTICULACAO COTOVELO D INFANTIL | fora do CID da OCI 09.03.01.002-0 | 1 | 1 | 100% | M77 1 |
| ECOGRAFIA DE ARTICULACAO PUNHO D INFANTIL | CID da OCI 09.03.01.002-0 | 2 | 2 | 33% | M65 2 |
| ECOGRAFIA DE ARTICULACAO PUNHO D INFANTIL | fora do CID da OCI 09.03.01.002-0 | 4 | 2 | 67% | M71 3, M79 1 |
| ECOGRAFIA DE ARTICULACAO PUNHO E INFANTIL | CID da OCI 09.03.01.002-0 | 1 | 1 | 11% | M65 1 |
| ECOGRAFIA DE ARTICULACAO PUNHO E INFANTIL | fora do CID da OCI 09.03.01.002-0 | 8 | 4 | 89% | M71 6, M85 1, R22 1 |
| USG OMBRO ESQUERDO | CID da OCI 09.03.01.002-0 | 0 | 0 | 0% | — |
| USG OMBRO ESQUERDO | fora do CID da OCI 09.03.01.002-0 | 1 | 0 | 100% | Z00 1 |
| ECOGRAFIA DE ARTICULACAO NAO LISTADA | CID da OCI 09.03.01.002-0 | 12 | 9 | 12% | M65 12 |
| ECOGRAFIA DE ARTICULACAO NAO LISTADA | fora do CID da OCI 09.03.01.002-0 | 85 | 44 | 88% | M25 10, R22 10, M72 7, M65 6, M71 5 |
| ECOGRAFIA DE ARTICULACAO COTOVELO E INFANTIL | CID da OCI 09.03.01.002-0 | 0 | 0 | 0% | — |
| ECOGRAFIA DE ARTICULACAO COTOVELO E INFANTIL | fora do CID da OCI 09.03.01.002-0 | 1 | 1 | 100% | Z13 1 |
| ECOGRAFIA DE ARTICULACAO COXO-FEMURAL D ADULTO | CID da OCI 09.03.01.002-0 | 2 | 2 | 4% | M65 2 |
| ECOGRAFIA DE ARTICULACAO COXO-FEMURAL D ADULTO | fora do CID da OCI 09.03.01.002-0 | 43 | 33 | 93% | M25 13, M70 7, M16 4, M76 4, M79 2 |
| ECOGRAFIA DE ARTICULACAO OMBRO D ADULTO | CID da OCI 09.03.01.002-0 | 130 | 79 | 7% | M65 130 |
| ECOGRAFIA DE ARTICULACAO OMBRO D ADULTO | fora do CID da OCI 09.03.01.002-0 | 1.832 | 1.380 | 93% | M75 1.189, M25 327, M79 64, R52 42, S46 19 |
| ECOGRAFIA DE ARTICULACAO PUNHO D ADULTO | CID da OCI 09.03.01.002-0 | 165 | 123 | 10% | M65 165 |
| ECOGRAFIA DE ARTICULACAO PUNHO D ADULTO | fora do CID da OCI 09.03.01.002-0 | 1.531 | 1.175 | 90% | G56 686, M25 244, M71 139, M79 67, M13 61 |
| ECOGRAFIA DE ARTICULACAO TORNOZELO D ADULTO | CID da OCI 09.03.01.002-0 | 48 | 37 | 14% | M65 44, M66 2, S93 2 |
| ECOGRAFIA DE ARTICULACAO TORNOZELO D ADULTO | fora do CID da OCI 09.03.01.002-0 | 286 | 237 | 86% | M25 72, M72 29, M79 25, R52 23, S93 22 |
| ECOGRAFIA DE ARTICULACAO JOELHO E ADULTO | CID da OCI 09.03.01.002-0 | 10 | 4 | 2% | M65 10 |
| ECOGRAFIA DE ARTICULACAO JOELHO E ADULTO | fora do CID da OCI 09.03.01.002-0 | 585 | 389 | 98% | M23 185, M25 152, M17 58, M71 34, S83 22 |
| ECOGRAFIA DE ARTICULACAO COTOVELO D ADULTO | CID da OCI 09.03.01.002-0 | 21 | 18 | 10% | M65 20, M70 1 |
| ECOGRAFIA DE ARTICULACAO COTOVELO D ADULTO | fora do CID da OCI 09.03.01.002-0 | 195 | 139 | 90% | M77 69, M25 41, G56 20, M70 13, M79 11 |
| ECOGRAFIA DE QUADRIL DIREITO | CID da OCI 09.03.01.002-0 | 0 | 0 | 0% | — |
| ECOGRAFIA DE QUADRIL DIREITO | fora do CID da OCI 09.03.01.002-0 | 4 | 4 | 100% | Q65 4 |
| ECOGRAFIA DE QUADRIL ESQUERDO | CID da OCI 09.03.01.002-0 | 0 | 0 | 0% | — |
| ECOGRAFIA DE QUADRIL ESQUERDO | fora do CID da OCI 09.03.01.002-0 | 2 | 2 | 100% | Q65 2 |
| USG TENDAO DE AQUILES DIREITO | CID da OCI 09.03.01.002-0 | 1 | 1 | 100% | M65 1 |
| USG TENDAO DE AQUILES DIREITO | fora do CID da OCI 09.03.01.002-0 | 0 | 0 | 0% | — |
| ECOGRAFIA DE ARTICULACAO TORNOZELO E INFANTIL | CID da OCI 09.03.01.002-0 | 0 | 0 | 0% | — |
| ECOGRAFIA DE ARTICULACAO TORNOZELO E INFANTIL | fora do CID da OCI 09.03.01.002-0 | 3 | 3 | 100% | R60 1, M71 1, D17 1 |
| ECOGRAFIA DE ARTICULACAO TORNOZELO D INFANTIL | CID da OCI 09.03.01.002-0 | 0 | 0 | 0% | — |
| ECOGRAFIA DE ARTICULACAO TORNOZELO D INFANTIL | fora do CID da OCI 09.03.01.002-0 | 2 | 2 | 100% | M25 2 |
| ECOGRAFIA DE PARTES MOLES | CID da OCI 09.03.01.002-0 | 70 | 40 | 2% | M65 69, M70 1 |
| ECOGRAFIA DE PARTES MOLES | fora do CID da OCI 09.03.01.002-0 | 3.053 | 1.837 | 98% | R22 767, D17 665, L72 206, K40 190, R59 135 |
| ECOGRAFIA DE REGIÃO INGUINAL ESQUERDO | CID da OCI 09.03.01.002-0 | 0 | 0 | 0% | — |
| ECOGRAFIA DE REGIÃO INGUINAL ESQUERDO | fora do CID da OCI 09.03.01.002-0 | 201 | 179 | 100% | K40 161, R10 14, Q53 4, N40 2, K42 2 |
| ECOGRAFIA DE REGIAO INGUINAL DIREITO | CID da OCI 09.03.01.002-0 | 0 | 0 | 0% | — |
| ECOGRAFIA DE REGIAO INGUINAL DIREITO | fora do CID da OCI 09.03.01.002-0 | 241 | 213 | 100% | K40 192, R10 14, R22 6, Q53 5, K42 2 |
| ULTRASSONOGRAFIA DA REGIAO INGUINAL | CID da OCI 09.03.01.002-0 | 0 | 0 | 0% | — |
| ULTRASSONOGRAFIA DA REGIAO INGUINAL | fora do CID da OCI 09.03.01.002-0 | 166 | 132 | 100% | K40 122, R10 9, Q53 7, K42 3, N51 3 |
| ULTRASSONOGRAFIA DO PESCOCO | CID da OCI 09.03.01.002-0 | 0 | 0 | 0% | — |
| ULTRASSONOGRAFIA DO PESCOCO | fora do CID da OCI 09.03.01.002-0 | 160 | 119 | 100% | R22 44, R59 23, M54 7, E04 6, R13 6 |
| ULTRASSONOGRAFIA COM DOPPLER COLORIDO DE REGIAO CERVICAL | CID da OCI 09.03.01.002-0 | 0 | 0 | 0% | — |
| ULTRASSONOGRAFIA COM DOPPLER COLORIDO DE REGIAO CERVICAL | fora do CID da OCI 09.03.01.002-0 | 17 | 14 | 100% | E04 2, C73 2, R55 2, I51 1, I65 1 |
| ULTRASSONOGRAFIA CERVICAL | CID da OCI 09.03.01.002-0 | 0 | 0 | 0% | — |
| ULTRASSONOGRAFIA CERVICAL | fora do CID da OCI 09.03.01.002-0 | 100 | 86 | 100% | R22 32, R59 20, D17 5, R13 5, M54 4 |
| ULTRA-SONOGRAFIA DE REGIAO CERVICAL (PESCOCO) | CID da OCI 09.03.01.002-0 | 0 | 0 | 0% | — |
| ULTRA-SONOGRAFIA DE REGIAO CERVICAL (PESCOCO) | fora do CID da OCI 09.03.01.002-0 | 2 | 0 | 100% | Z00 1, Q89 1 |
| USG PERNA ESQUERDA | CID da OCI 09.03.01.002-0 | 2 | 1 | 7% | M65 2 |
| USG PERNA ESQUERDA | fora do CID da OCI 09.03.01.002-0 | 25 | 16 | 93% | M79 8, I83 3, R60 2, M62 1, R25 1 |
| USG PERNA DIREITA | CID da OCI 09.03.01.002-0 | 1 | 0 | 6% | M65 1 |
| USG PERNA DIREITA | fora do CID da OCI 09.03.01.002-0 | 16 | 12 | 94% | I83 3, I87 2, M62 1, C44 1, M71 1 |
| USG ESTRUTURA SUPERFICIE | CID da OCI 09.03.01.002-0 | 0 | 0 | 0% | — |
| USG ESTRUTURA SUPERFICIE | fora do CID da OCI 09.03.01.002-0 | 2 | 2 | 100% | D17 1, R10 1 |
| USG BRACO DIREITO | CID da OCI 09.03.01.002-0 | 6 | 1 | 21% | M65 6 |
| USG BRACO DIREITO | fora do CID da OCI 09.03.01.002-0 | 22 | 6 | 79% | M75 9, D17 5, M79 3, R07 1, M25 1 |
| ECOGRAFIA PELVICA | CID da OCI 09.03.01.002-0 | 3 | 3 | 7% | M65 3 |
| ECOGRAFIA PELVICA | fora do CID da OCI 09.03.01.002-0 | 43 | 43 | 93% | R10 10, K40 6, Z01 4, E30 3, N92 3 |
| USB AXILA DIREITA | CID da OCI 09.03.01.002-0 | 0 | 0 | 0% | — |
| USB AXILA DIREITA | fora do CID da OCI 09.03.01.002-0 | 23 | 17 | 100% | N63 6, C50 5, R22 5, Q83 2, L72 1 |
| USG BRACO ESQUERDO | CID da OCI 09.03.01.002-0 | 15 | 1 | 30% | M65 15 |
| USG BRACO ESQUERDO | fora do CID da OCI 09.03.01.002-0 | 35 | 6 | 70% | M75 22, M79 5, M25 3, S46 2, R07 1 |
| USG ANTEBRACO ESQUERDO | CID da OCI 09.03.01.002-0 | 1 | 1 | 12% | M65 1 |
| USG ANTEBRACO ESQUERDO | fora do CID da OCI 09.03.01.002-0 | 7 | 5 | 88% | D17 2, L72 1, R60 1, M61 1, R20 1 |
| ULTRASSONOGRAFIA DA REGIAO LOMBAR | CID da OCI 09.03.01.002-0 | 0 | 0 | 0% | — |
| ULTRASSONOGRAFIA DA REGIAO LOMBAR | fora do CID da OCI 09.03.01.002-0 | 55 | 45 | 100% | Q76 17, Q07 9, M54 4, Q05 4, D17 4 |
| ULTRASSONOGRAFIA DAS GLANDULAS SUBMANDIBULARES | CID da OCI 09.03.01.002-0 | 0 | 0 | 0% | — |
| ULTRASSONOGRAFIA DAS GLANDULAS SUBMANDIBULARES | fora do CID da OCI 09.03.01.002-0 | 12 | 11 | 100% | R22 6, M35 2, K11 2, R59 1, R13 1 |
| ULTRASSONOGRAFIA DA BACIA | CID da OCI 09.03.01.002-0 | 0 | 0 | 0% | — |
| ULTRASSONOGRAFIA DA BACIA | fora do CID da OCI 09.03.01.002-0 | 4 | 2 | 100% | M16 2, Z12 1, Q65 1 |
| ECOGRAFIA DE ARTICULACAO COLUNA LOMBAR | CID da OCI 09.03.01.002-0 | 0 | 0 | 0% | — |
| ECOGRAFIA DE ARTICULACAO COLUNA LOMBAR | fora do CID da OCI 09.03.01.002-0 | 134 | 93 | 100% | Q76 108, Q05 16, M54 2, Z00 2, R15 1 |
| USG COXA DIREITA | CID da OCI 09.03.01.002-0 | 0 | 0 | 0% | — |
| USG COXA DIREITA | fora do CID da OCI 09.03.01.002-0 | 1 | 0 | 100% | M25 1 |
| USG AXILA ESQUERDA | CID da OCI 09.03.01.002-0 | 0 | 0 | 0% | — |
| USG AXILA ESQUERDA | fora do CID da OCI 09.03.01.002-0 | 20 | 13 | 100% | C50 5, R59 4, N63 4, D17 2, M79 1 |
| ULTRASSONOGRAFIA DA REGIAO GLUTEA | CID da OCI 09.03.01.002-0 | 0 | 0 | 0% | — |
| ULTRASSONOGRAFIA DA REGIAO GLUTEA | fora do CID da OCI 09.03.01.002-0 | 5 | 3 | 100% | L05 3, M76 1, T85 1 |
| DOPPLER DE AORTA E ILIACA | CID da OCI 09.03.01.002-0 | 0 | 0 | 0% | — |
| DOPPLER DE AORTA E ILIACA | fora do CID da OCI 09.03.01.002-0 | 6 | 0 | 100% | N18 4, I71 1, R10 1 |

## Varredura das filas

Toda fila que a varredura achou, pelo código, pelo nome e, na OCI, pelo CID aceito e pelo da finalidade, nas tabelas de solicitações e de agendamentos. A decisão é a do enquadramento do plano; fila sem decisão sai **a decidir** e não entra na soma.

| fila | código | tabela | achada por | objeto | fila | fila viva | pessoas | devolvidas | espera média | pedido mais antigo | agendadas 12 m | CID principais | no CID do objeto | parte no CID aceito (calculado) | decisão | motivo |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ECOGRAFIA DE PARTES MOLES | 02.05.02.006-2 | solicitações | código, nome | 02.05.02.006-2 | 3.124 | 1.878 | 3.122 | 1.456 | 650,8 | 28/10/2010 | 1.427 | R22 767, D17 665, L72 206, K40 190, R59 135 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ECOGRAFIA DE ARTICULACAO OMBRO D ADULTO | 02.05.02.006-2 | solicitações | código, nome | 02.05.02.006-2 | 1.962 | 1.459 | 1.960 | 743 | 558,9 | 12/01/2021 | 1.187 | M75 1.189, M25 327, M65 131, M79 64, R52 42 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ECOGRAFIA DE ARTICULACAO PUNHO D ADULTO | 02.05.02.006-2 | solicitações | código, nome | 02.05.02.006-2 | 1.696 | 1.298 | 1.695 | 380 | 511,6 | 24/09/2010 | 713 | G56 686, M25 244, M65 187, M71 139, M79 67 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ECOGRAFIA DE ARTICULACAO OMBRO E ADULTO | 02.05.02.006-2 | solicitações | código, nome | 02.05.02.006-2 | 1.530 | 1.171 | 1.529 | 585 | 535,7 | 07/01/2021 | 849 | M75 905, M25 253, M65 99, M79 48, R52 42 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ECOGRAFIA DE ARTICULACAO PUNHO E ADULTO | 02.05.02.006-2 | solicitações | código, nome | 02.05.02.006-2 | 1.461 | 1.153 | 1.460 | 346 | 494,2 | 08/01/2021 | 611 | G56 563, M25 208, M65 171, M71 141, M13 56 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ECOGRAFIA DE ARTICULACAO JOELHO E ADULTO | 02.05.02.006-2 | solicitações | código, nome | 02.05.02.006-2 | 595 | 393 | 595 | 69 | 577,3 | 28/01/2021 | 315 | M23 185, M25 152, M17 58, M71 34, S83 22 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ECOGRAFIA PELVICA (GINECOLOGICA) - ADULTO | 02.05.02.016-0 | solicitações | nome | 02.05.02.006-2 | 585 | 351 | 585 | 836 | 701,7 | 06/01/2021 | 957 | R10 123, N94 83, N92 56, E28 42, Z01 39 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA DE ARTICULACAO JOELHO D ADULTO | 02.05.02.006-2 | solicitações | código, nome | 02.05.02.006-2 | 552 | 360 | 552 | 63 | 593,1 | 28/01/2021 | 332 | M23 191, M25 151, M17 57, S83 21, M79 18 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ECOGRAFIA PELVICA (GINECOLOGICA) - INFANTIL | 02.05.02.016-0 | solicitações | nome | 02.05.02.006-2 | 441 | 360 | 441 | 83 | 467,4 | 19/01/2021 | 418 | E30 180, E22 56, R10 39, Z00 30, N92 20 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA DE ARTICULACAO TORNOZELO E ADULTO | 02.05.02.006-2 | solicitações | código, nome | 02.05.02.006-2 | 376 | 306 | 375 | 118 | 466,4 | 19/01/2021 | 224 | M25 91, M65 50, M72 33, S93 29, M79 25 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ECOGRAFIA DE ARTICULACAO TORNOZELO D ADULTO | 02.05.02.006-2 | solicitações | código, nome | 02.05.02.006-2 | 334 | 274 | 334 | 138 | 441,4 | 11/03/2021 | 238 | M25 72, M65 44, M72 29, M79 25, S93 24 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ECOGRAFIA DE REGIAO INGUINAL DIREITO | 02.05.02.006-2 | solicitações | código, nome | 02.05.02.006-2 | 241 | 213 | 241 | 16 | 373,8 | 09/03/2023 | 259 | K40 192, R10 14, R22 6, Q53 5, K42 2 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ECOGRAFIA DE ARTICULACAO COTOVELO D ADULTO | 02.05.02.006-2 | solicitações | código, nome | 02.05.02.006-2 | 216 | 157 | 216 | 72 | 522,7 | 25/02/2021 | 262 | M77 69, M25 41, M65 21, G56 20, M70 14 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ECOGRAFIA DE REGIÃO INGUINAL ESQUERDO | 02.05.02.006-2 | solicitações | código, nome | 02.05.02.006-2 | 201 | 179 | 201 | 12 | 349,0 | 24/11/2022 | 216 | K40 161, R10 14, Q53 4, N40 2, K42 2 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| USG MAO DIREITA | 02.05.02.006-2 | solicitações | código, nome | 02.05.02.006-2 | 197 | 164 | 197 | 31 | 414,8 | 08/02/2023 | 133 | M65 57, M25 31, G56 21, M71 13, M79 9 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ULTRASSONOGRAFIA DA REGIAO INGUINAL | 02.05.02.006-2 | solicitações | código, nome | 02.05.02.006-2 | 166 | 132 | 166 | 26 | 436,0 | 29/03/2023 | 260 | K40 122, R10 9, Q53 7, K42 3, N51 3 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ULTRASSONOGRAFIA DO PESCOCO | 02.05.02.006-2 | solicitações | código, nome | 02.05.02.006-2 | 160 | 119 | 160 | 8 | 508,6 | 06/02/2023 | 35 | R22 44, R59 23, M54 7, E04 6, R13 6 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ECOGRAFIA DE ARTICULACAO COTOVELO E ADULTO | 02.05.02.006-2 | solicitações | código, nome | 02.05.02.006-2 | 143 | 111 | 143 | 59 | 463,1 | 20/01/2021 | 221 | M77 38, M25 24, G56 20, M70 12, M65 10 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| USG MAO ESQUERDA | 02.05.02.006-2 | solicitações | código, nome | 02.05.02.006-2 | 142 | 108 | 142 | 27 | 475,5 | 08/02/2023 | 112 | M25 28, M65 27, G56 18, M71 13, M79 8 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ECOGRAFIA DE ARTICULACAO COLUNA LOMBAR | 02.05.02.006-2 | solicitações | código, nome | 02.05.02.006-2 | 134 | 93 | 134 | 1 | 519,9 | 24/04/2024 | 4 | Q76 108, Q05 16, M54 2, Z00 2, R15 1 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| USG QUADRIL | 02.05.02.006-2 | solicitações | código, nome | 02.05.02.006-2 | 121 | 108 | 121 | 18 | 332,7 | 07/02/2023 | 93 | Q65 44, M25 13, M70 8, M76 7, M65 6 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| USG PE DIREITO | 02.05.02.006-2 | solicitações | código, nome | 02.05.02.006-2 | 114 | 74 | 114 | 20 | 542,0 | 07/02/2023 | 63 | M72 38, M71 15, M25 14, M77 13, M65 7 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ULTRASSONOGRAFIA CERVICAL | 02.05.02.006-2 | solicitações | código, nome | 02.05.02.006-2 | 100 | 86 | 100 | 38 | 333,4 | 16/02/2023 | 151 | R22 32, R59 20, D17 5, R13 5, M54 4 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| USG PE ESQUERDO | 02.05.02.006-2 | solicitações | código, nome | 02.05.02.006-2 | 99 | 71 | 98 | 29 | 494,0 | 08/02/2023 | 62 | M72 34, M25 14, M77 12, M71 6, M79 6 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ECOGRAFIA DE ARTICULACAO NAO LISTADA | 02.05.02.006-2 | solicitações | código, nome | 02.05.02.006-2 | 97 | 53 | 97 | 262 | 915,3 | 14/01/2021 | 51 | M65 18, M25 10, R22 10, M72 7, M71 5 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ECOGRAFIA DE ARTICULACAO COXO-FEMURAL E INFANTIL | 02.05.02.006-2 | solicitações | código, nome | 02.05.02.006-2 | 82 | 67 | 82 | 12 | 415,0 | 07/08/2023 | 12 | Q65 49, Q90 4, P07 3, P03 3, S73 3 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ECOGRAFIA DE ARTICULACAO COXO-FEMURAL D INFANTIL | 02.05.02.006-2 | solicitações | código, nome | 02.05.02.006-2 | 77 | 68 | 77 | 12 | 360,2 | 25/04/2024 | 14 | Q65 47, Q90 4, P07 3, P03 3, Z13 3 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ULTRASSONOGRAFIA DA REGIAO LOMBAR | 02.05.02.006-2 | solicitações | código, nome | 02.05.02.006-2 | 55 | 45 | 55 | 7 | 459,5 | 10/10/2023 | 3 | Q76 17, Q07 9, M54 4, Q05 4, D17 4 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| USG BRACO ESQUERDO | 02.05.02.006-2 | solicitações | código, nome | 02.05.02.006-2 | 50 | 7 | 50 | 10 | 1.178,4 | 08/02/2023 | 10 | M75 22, M65 15, M79 5, M25 3, S46 2 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ECOGRAFIA DE ARTICULACAO COXO-FEMURAL D ADULTO | 02.05.02.006-2 | solicitações | código, nome | 02.05.02.006-2 | 46 | 36 | 46 | 26 | 558,1 | 02/02/2021 | 26 | M25 13, M70 7, M16 4, M76 4, M79 2 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ECOGRAFIA PELVICA | 02.05.02.006-2 | solicitações | código, nome | 02.05.02.006-2 | 46 | 46 | 46 | 15 | 88,6 | 13/05/2026 | 21 | R10 10, K40 6, Z01 4, M65 3, E30 3 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ECOGRAFIA DE ARTICULACAO COXO-FEMURAL E ADULTO | 02.05.02.006-2 | solicitações | código, nome | 02.05.02.006-2 | 37 | 27 | 37 | 27 | 522,3 | 18/02/2021 | 14 | M25 10, M70 8, M76 4, M79 3, K40 2 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| USG BRACO DIREITO | 02.05.02.006-2 | solicitações | código, nome | 02.05.02.006-2 | 28 | 7 | 28 | 15 | 1.001,0 | 08/02/2023 | 18 | M75 9, M65 6, D17 5, M79 3, R07 1 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| USG PERNA ESQUERDA | 02.05.02.006-2 | solicitações | código, nome | 02.05.02.006-2 | 27 | 17 | 27 | 62 | 523,9 | 12/04/2023 | 6 | M79 8, I83 3, R60 2, M65 2, M62 1 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| USB AXILA DIREITA | 02.05.02.006-2 | solicitações | código, nome | 02.05.02.006-2 | 23 | 17 | 23 | 1 | 620,3 | 06/03/2024 | 0 | N63 6, C50 5, R22 5, Q83 2, L72 1 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| USG AXILA ESQUERDA | 02.05.02.006-2 | solicitações | código, nome | 02.05.02.006-2 | 20 | 13 | 20 | 2 | 660,1 | 06/03/2024 | 0 | C50 5, R59 4, N63 4, D17 2, M79 1 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ULTRASSONOGRAFIA COM DOPPLER COLORIDO DE REGIAO CERVICAL | 02.05.02.006-2 | solicitações | código, nome | 02.05.02.006-2 | 17 | 14 | 17 | 33 | 420,8 | 20/06/2024 | 13 | E04 2, C73 2, R55 2, I51 1, I65 1 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| USG PERNA DIREITA | 02.05.02.006-2 | solicitações | código, nome | 02.05.02.006-2 | 17 | 12 | 17 | 57 | 537,9 | 12/04/2023 | 5 | I83 3, I87 2, M62 1, C44 1, M71 1 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ULTRASSONOGRAFIA DO DEDO | 02.05.02.006-2 | solicitações | código, nome | 02.05.02.006-2 | 17 | 10 | 17 | 1 | 592,7 | 15/06/2023 | 2 | M71 4, M79 3, M25 3, M65 3, M21 1 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ECOGRAFIA DE ARTICULACAO JOELHO D INFANTIL | 02.05.02.006-2 | solicitações | código, nome | 02.05.02.006-2 | 16 | 11 | 16 | 2 | 641,9 | 11/03/2021 | 14 | M23 5, M25 3, M75 3, M71 1, R22 1 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ECOGRAFIA DE ARTICULACAO JOELHO E INFANTIL | 02.05.02.006-2 | solicitações | código, nome | 02.05.02.006-2 | 15 | 11 | 15 | 2 | 512,7 | 12/03/2021 | 10 | M25 5, M71 2, M23 2, L72 1, M21 1 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ULTRASSONOGRAFIA DO CALCANEO | 02.05.02.006-2 | solicitações | código, nome | 02.05.02.006-2 | 15 | 11 | 15 | 2 | 418,1 | 23/08/2023 | 0 | M76 4, M77 4, M25 2, M72 2, M79 1 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ULTRASSONOGRAFIA DAS GLANDULAS SUBMANDIBULARES | 02.05.02.006-2 | solicitações | código, nome | 02.05.02.006-2 | 12 | 11 | 12 | 2 | 201,6 | 05/06/2024 | 11 | R22 6, M35 2, K11 2, R59 1, R13 1 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ECOGRAFIA DE ARTICULACAO PUNHO E INFANTIL | 02.05.02.006-2 | solicitações | código, nome | 02.05.02.006-2 | 9 | 5 | 9 | 3 | 769,6 | 12/12/2022 | 5 | M71 6, M65 1, M85 1, R22 1 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| USG ANTEBRACO ESQUERDO | 02.05.02.006-2 | solicitações | código, nome | 02.05.02.006-2 | 8 | 6 | 8 | 9 | 642,0 | 27/11/2023 | 8 | D17 2, L72 1, R60 1, M65 1, M61 1 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| PERNA DIREITA | 02.04.06.016-8 | solicitações | nome | 02.05.02.006-2 | 7 | 7 | 7 | 2 | 131,3 | 17/03/2026 | 48 | M54 2, M21 2, M86 1, Z00 1, Q66 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| USG TENDAO DE AQUILES ESQUERDO | 02.05.02.006-2 | solicitações | código, nome | 02.05.02.006-2 | 6 | 4 | 6 | 2 | 663,9 | 09/11/2023 | 5 | M76 3, M65 2, M66 1 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ECOGRAFIA DE ARTICULACAO PUNHO D INFANTIL | 02.05.02.006-2 | solicitações | código, nome | 02.05.02.006-2 | 6 | 4 | 6 | 3 | 510,1 | 29/08/2024 | 4 | M71 3, M65 2, M79 1 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| DOPPLER DE AORTA E ILIACA | 02.05.02.006-2 | solicitações | código, nome | 02.05.02.006-2 | 6 | 0 | 6 | 0 | 1.523,2 | 05/08/2022 | 0 | N18 4, I71 1, R10 1 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| CALCANEO | 02.04.06.010-9 | solicitações | nome | 02.05.02.006-2 | 5 | 5 | 5 | 1 | 165,3 | 02/04/2026 | 406 | M77 4, Z00 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| PERNA ESQUERDA | 02.04.06.016-8 | solicitações | nome | 02.05.02.006-2 | 5 | 5 | 5 | 1 | 120,9 | 17/03/2026 | 42 | M54 1, M21 1, M79 1, W01 1, Q66 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRASSONOGRAFIA DA REGIAO GLUTEA | 02.05.02.006-2 | solicitações | código, nome | 02.05.02.006-2 | 5 | 3 | 5 | 0 | 665,9 | 21/08/2023 | 0 | L05 3, M76 1, T85 1 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ECOGRAFIA DE QUADRIL DIREITO | 02.05.02.006-2 | solicitações | código, nome | 02.05.02.006-2 | 4 | 4 | 4 | 0 | 50,4 | 12/08/2026 | 1 | Q65 4 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ULTRASSONOGRAFIA DA BACIA | 02.05.02.006-2 | solicitações | código, nome | 02.05.02.006-2 | 4 | 2 | 4 | 3 | 606,9 | 10/08/2023 | — | M16 2, Z12 1, Q65 1 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ECOGRAFIA DE ARTICULACAO TORNOZELO E INFANTIL | 02.05.02.006-2 | solicitações | código, nome | 02.05.02.006-2 | 3 | 3 | 3 | 0 | 161,2 | 02/09/2025 | 2 | R60 1, M71 1, D17 1 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| COXA ESQUERDA | 02.04.06.011-7 | solicitações | nome | 02.05.02.006-2 | 2 | 2 | 2 | 1 | 80,3 | 09/06/2026 | 8 | M54 1, M86 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA DE ARTICULACAO COXA ESQUERDA | 02.05.02.006-2 | solicitações | código, nome | 02.05.02.006-2 | 2 | 2 | 2 | 2 | 100,7 | 09/04/2026 | 8 | Z00 1, D17 1 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ECOGRAFIA DE ARTICULACAO TORNOZELO D INFANTIL | 02.05.02.006-2 | solicitações | código, nome | 02.05.02.006-2 | 2 | 2 | 2 | 0 | 159,3 | 21/03/2026 | 5 | M25 2 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| USG ESTRUTURA SUPERFICIE | 02.05.02.006-2 | solicitações | código, nome | 02.05.02.006-2 | 2 | 2 | 2 | 24 | 14,9 | 08/10/2026 | 4 | D17 1, R10 1 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ECOGRAFIA DE QUADRIL ESQUERDO | 02.05.02.006-2 | solicitações | código, nome | 02.05.02.006-2 | 2 | 2 | 2 | 0 | 24,9 | 02/10/2026 | 1 | Q65 2 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DE REGIAO CERVICAL (PESCOCO) | 02.05.02.006-2 | solicitações | código, nome | 02.05.02.006-2 | 2 | 0 | 2 | 0 | 3.772,0 | 29/04/2010 | 0 | Z00 1, Q89 1 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| COXA DIREITA | 02.04.06.011-7 | solicitações | nome | 02.05.02.006-2 | 1 | 1 | 1 | 2 | 20,7 | 06/10/2026 | 14 | M54 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| USG TENDAO DE AQUILES DIREITO | 02.05.02.006-2 | solicitações | código, nome | 02.05.02.006-2 | 1 | 1 | 1 | 0 | 124,6 | 24/06/2026 | 6 | M65 1 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ECOGRAFIA DE ARTICULACAO COXA DIREITA | 02.05.02.006-2 | solicitações | código, nome | 02.05.02.006-2 | 1 | 1 | 1 | 3 | 29,0 | 28/09/2026 | 4 | Z54 1 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ANTEBRACO ESQUERDO | 02.04.04.001-9 | solicitações | nome | 02.05.02.006-2 | 1 | 1 | 1 | 1 | 20,7 | 06/10/2026 | 2 | M25 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| BRACO DIREITO | 02.04.04.005-1 | solicitações | nome | 02.05.02.006-2 | 1 | 1 | 1 | 0 | 20,7 | 06/10/2026 | 1 | M25 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| BRACO ESQUERDO | 02.04.04.005-1 | solicitações | nome | 02.05.02.006-2 | 1 | 1 | 1 | 0 | 20,7 | 06/10/2026 | 0 | M25 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA DE ARTICULACAO COTOVELO D INFANTIL | 02.05.02.006-2 | solicitações | código, nome | 02.05.02.006-2 | 1 | 1 | 1 | 5 | 21,9 | 05/10/2026 | 0 | M77 1 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ECOGRAFIA DE ARTICULACAO COTOVELO E INFANTIL | 02.05.02.006-2 | solicitações | código, nome | 02.05.02.006-2 | 1 | 1 | 1 | 1 | 19,8 | 07/10/2026 | 0 | Z13 1 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| USG COXA DIREITA | 02.05.02.006-2 | solicitações | código, nome | 02.05.02.006-2 | 1 | 0 | 1 | 1 | 1.419,7 | 07/12/2022 | 0 | M25 1 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| USG OMBRO ESQUERDO | 02.05.02.006-2 | solicitações | código, nome | 02.05.02.006-2 | 1 | 0 | 1 | 62 | 3.387,6 | 18/07/2017 | 0 | Z00 1 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| COTOVELO | 02.04.04.007-8 | solicitações | nome | 02.05.02.006-2 | 0 | 0 | 0 | 2 | — | — | 172 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| USG ANTEBRACO DIREITO | 02.05.02.006-2 | solicitações | código | 02.05.02.006-2 | 0 | 0 | 0 | 4 | — | — | 11 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DE COLUNA LOMBOSSACRA - PEDIATRICA | 02.05.02.006-2 | solicitações | código | 02.05.02.006-2 | 0 | 0 | 0 | 2 | — | — | 10 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA DE ARTICULACAO OMBRO E INFANTIL | 02.05.02.006-2 | solicitações | código | 02.05.02.006-2 | 0 | 0 | 0 | 2 | — | — | 4 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA DE ARTICULACAO OMBRO D INFANTIL | 02.05.02.006-2 | solicitações | código | 02.05.02.006-2 | 0 | 0 | 0 | 3 | — | — | 2 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA DE ARTICULACAO PANTURRILHA DIREITA | 02.05.02.006-2 | solicitações | código | 02.05.02.006-2 | 0 | 0 | 0 | 1 | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DE PARTES MOLES | 02.05.02.006-2 | solicitações | código | 02.05.02.006-2 | 0 | 0 | 0 | 4 | — | — | — | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRASSONOGRAFIA ARTICULAÇÃO COM DOPPLER COLORIDO | 02.05.02.006-2 | solicitações | código | 02.05.02.006-2 | 0 | 0 | 0 | 1 | — | — | — | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| USG AXILA DIREITA | 02.05.02.006-2 | solicitações | código | 02.05.02.006-2 | 0 | 0 | 0 | 1 | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| USG COTOVELO DIREITO | 02.05.02.006-2 | solicitações | código | 02.05.02.006-2 | 0 | 0 | 0 | 14 | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| USG COTOVELO ESQUERDO | 02.05.02.006-2 | solicitações | código | 02.05.02.006-2 | 0 | 0 | 0 | 15 | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| USG COXA ESQUERDA | 02.05.02.006-2 | solicitações | código | 02.05.02.006-2 | 0 | 0 | 0 | 2 | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| USG JOELHO DIREITO | 02.05.02.006-2 | solicitações | código | 02.05.02.006-2 | 0 | 0 | 0 | 5 | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| USG JOELHO ESQUERDO | 02.05.02.006-2 | solicitações | código | 02.05.02.006-2 | 0 | 0 | 0 | 12 | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| USG MUSCULO | 02.05.02.006-2 | solicitações | código | 02.05.02.006-2 | 0 | 0 | 0 | 1 | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| USG OMBRO DIREITO | 02.05.02.006-2 | solicitações | código | 02.05.02.006-2 | 0 | 0 | 0 | 68 | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| USG PANTURRILHA ESQUERDA | 02.05.02.006-2 | solicitações | código | 02.05.02.006-2 | 0 | 0 | 0 | 1 | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| USG PARTES MOLES | 02.05.02.006-2 | solicitações | código | 02.05.02.006-2 | 0 | 0 | 0 | 25 | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| USG PUNHO DIREITO | 02.05.02.006-2 | solicitações | código | 02.05.02.006-2 | 0 | 0 | 0 | 38 | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| USG PUNHO ESQUERDO | 02.05.02.006-2 | solicitações | código | 02.05.02.006-2 | 0 | 0 | 0 | 34 | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| USG TORNOZELO DIREITO | 02.05.02.006-2 | solicitações | código | 02.05.02.006-2 | 0 | 0 | 0 | 17 | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| USG TORNOZELO ESQUERDO | 02.05.02.006-2 | solicitações | código | 02.05.02.006-2 | 0 | 0 | 0 | 18 | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ANTEBRACO | 02.04.04.001-9 | só agendamentos | nome | 02.05.02.006-2 | — | — | — | — | — | — | 69 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA DE ARTICULACAO COXO-FEMURAL D ADULTO EMERGENCIA | 02.05.02.006-2 | só agendamentos | código, nome | 02.05.02.006-2 | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA DE ARTICULACAO COXO-FEMURAL D INFANTIL EMERGENCIA | 02.05.02.006-2 | só agendamentos | código, nome | 02.05.02.006-2 | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA DE ARTICULACAO COXO-FEMURAL E INFANTIL EMERGENCIA | 02.05.02.006-2 | só agendamentos | código, nome | 02.05.02.006-2 | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA DE ARTICULACAO JOELHO D INFANTIL EMERGENCIA | 02.05.02.006-2 | só agendamentos | código, nome | 02.05.02.006-2 | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA DE ARTICULACAO JOELHO E INFANTIL EMERGENCIA | 02.05.02.006-2 | só agendamentos | código, nome | 02.05.02.006-2 | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA DE ARTICULACAO NAO LISTADA EMERGENCIA | 02.05.02.006-2 | só agendamentos | código, nome | 02.05.02.006-2 | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA DE ARTICULACAO TORNOZELO D INFANTIL EMERGENCIA | 02.05.02.006-2 | só agendamentos | código, nome | 02.05.02.006-2 | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA DE PARTES MOLES EMERGENCIA | 02.05.02.006-2 | só agendamentos | código, nome | 02.05.02.006-2 | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA DE ARTICULACAO COTOVELO D ADULTO EMERGENCIA | 02.05.02.006-2 | só agendamentos | código, nome | 02.05.02.006-2 | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA DE ARTICULACAO COTOVELO D INFANTIL EMERGENCIA | 02.05.02.006-2 | só agendamentos | código, nome | 02.05.02.006-2 | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA DE ARTICULACAO COTOVELO E ADULTO EMERGENCIA | 02.05.02.006-2 | só agendamentos | código, nome | 02.05.02.006-2 | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA DE ARTICULACAO COTOVELO E INFANTIL EMERGENCIA | 02.05.02.006-2 | só agendamentos | código, nome | 02.05.02.006-2 | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA DE ARTICULACAO OMBRO D ADULTO EMERGENCIA | 02.05.02.006-2 | só agendamentos | código, nome | 02.05.02.006-2 | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA DE ARTICULACAO OMBRO D INFANTIL EMERGENCIA | 02.05.02.006-2 | só agendamentos | código | 02.05.02.006-2 | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA DE ARTICULACAO OMBRO E ADULTO EMERGENCIA | 02.05.02.006-2 | só agendamentos | código, nome | 02.05.02.006-2 | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA DE ARTICULACAO OMBRO E INFANTIL EMERGENCIA | 02.05.02.006-2 | só agendamentos | código | 02.05.02.006-2 | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA DE ARTICULACAO PANTURILHA ESQUERDA | 02.05.02.006-2 | só agendamentos | código | 02.05.02.006-2 | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA DE ARTICULACAO PUNHO D ADULTO EMERGENCIA | 02.05.02.006-2 | só agendamentos | código, nome | 02.05.02.006-2 | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA DE ARTICULACAO PUNHO D INFANTIL EMERGENCIA | 02.05.02.006-2 | só agendamentos | código, nome | 02.05.02.006-2 | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA DE ARTICULACAO PUNHO E ADULTO EMERGENCIA | 02.05.02.006-2 | só agendamentos | código, nome | 02.05.02.006-2 | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA DE ARTICULACAO PUNHO E INFANTIL EMERGENCIA | 02.05.02.006-2 | só agendamentos | código, nome | 02.05.02.006-2 | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA DE PARTES MOLES | 02.05.02.006-2 | só agendamentos | código, nome | 02.05.02.006-2 | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA PELVICA (GINECOLOGICA) - ADULTO - EMERGENCIA | 02.05.02.016-0 | só agendamentos | nome | 02.05.02.006-2 | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA PELVICA (GINECOLOGICA) - INFANTIL - EMERGENCIA | 02.05.02.016-0 | só agendamentos | nome | 02.05.02.006-2 | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DE ANTEBRACO ESQUERDO | 02.05.02.006-2 | só agendamentos | código | 02.05.02.006-2 | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DE ARTICULACAO COTOVELO DIREITO | 02.05.02.006-2 | só agendamentos | código | 02.05.02.006-2 | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DE ARTICULACAO COTOVELO ESQUERDO | 02.05.02.006-2 | só agendamentos | código | 02.05.02.006-2 | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DE ARTICULACAO DEDOS | 02.05.02.006-2 | só agendamentos | código | 02.05.02.006-2 | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DE ARTICULACAO DEDOS DO PE | 02.05.02.006-2 | só agendamentos | código | 02.05.02.006-2 | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DE ARTICULACAO JOELHO DIREITO | 02.05.02.006-2 | só agendamentos | código | 02.05.02.006-2 | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DE ARTICULACAO JOELHO ESQUERDO | 02.05.02.006-2 | só agendamentos | código | 02.05.02.006-2 | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DE ARTICULACAO MAO DIREITA | 02.05.02.006-2 | só agendamentos | código | 02.05.02.006-2 | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DE ARTICULACAO MAO ESQUERDA | 02.05.02.006-2 | só agendamentos | código | 02.05.02.006-2 | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DE ARTICULACAO OMBRO DIREITO | 02.05.02.006-2 | só agendamentos | código | 02.05.02.006-2 | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DE ARTICULACAO OMBRO ESQUERDO | 02.05.02.006-2 | só agendamentos | código | 02.05.02.006-2 | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DE ARTICULACAO PE DIREITO | 02.05.02.006-2 | só agendamentos | código | 02.05.02.006-2 | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DE ARTICULACAO PE ESQUERDO | 02.05.02.006-2 | só agendamentos | código | 02.05.02.006-2 | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DE ARTICULACAO PUNHO DIREITO | 02.05.02.006-2 | só agendamentos | código | 02.05.02.006-2 | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DE ARTICULACAO PUNHO ESQUERDO | 02.05.02.006-2 | só agendamentos | código | 02.05.02.006-2 | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DE ARTICULACAO TENDAO DE AQUILES | 02.05.02.006-2 | só agendamentos | código | 02.05.02.006-2 | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DE ARTICULACAO TORNOZELO DIREITO | 02.05.02.006-2 | só agendamentos | código | 02.05.02.006-2 | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DE ARTICULACAO TORNOZELO ESQUERDO | 02.05.02.006-2 | só agendamentos | código | 02.05.02.006-2 | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DE PERNA DIREITA | 02.05.02.006-2 | só agendamentos | código | 02.05.02.006-2 | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DE PERNA ESQUERDA | 02.05.02.006-2 | só agendamentos | código | 02.05.02.006-2 | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DE ARTICULACAO COLUNA LOMBAR | 02.05.02.006-2 | só agendamentos | código | 02.05.02.006-2 | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DE BRACO DIREITO | 02.05.02.006-2 | só agendamentos | código | 02.05.02.006-2 | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DE BRACO ESQUERDO | 02.05.02.006-2 | só agendamentos | código | 02.05.02.006-2 | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DE COXA ESQUERDA | 02.05.02.006-2 | só agendamentos | código | 02.05.02.006-2 | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DE GLANDULAS SALIVARES | 02.05.02.006-2 | só agendamentos | código | 02.05.02.006-2 | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DE REGIAO INGUINAL | 02.05.02.006-2 | só agendamentos | código | 02.05.02.006-2 | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DE REGIAO INGUINAL DIREITO | 02.05.02.006-2 | só agendamentos | código | 02.05.02.006-2 | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA DE REGIAO INGUINAL ESQUERDO | 02.05.02.006-2 | só agendamentos | código | 02.05.02.006-2 | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRASSONOGRAFIA DE ARTICULACAO QUADRIL DIREITO | 02.05.02.006-2 | só agendamentos | código | 02.05.02.006-2 | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRASSONOGRAFIA DE ARTICULACAO QUADRIL ESQUERDO | 02.05.02.006-2 | só agendamentos | código | 02.05.02.006-2 | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRASSONOGRAFIA DE QUADRIL DIREITO | 02.05.02.006-2 | só agendamentos | código | 02.05.02.006-2 | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| USG PANTURRILHA DIREITA | 02.05.02.006-2 | só agendamentos | código | 02.05.02.006-2 | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |

## Região de Saúde

**02.05.02.006-2**, na medida da fila (o conjunto do objeto):

| Região de Saúde | fila | pessoas |
|---|---|---|
| Região Sudoeste | 4.272 | 3.747 |
| Região Centro-Sul | 2.825 | 2.213 |
| Região Leste | 2.709 | 2.167 |
| Região Sul | 2.295 | 1.443 |
| Região Oeste | 1.568 | 1.308 |
| Região Norte | 526 | 428 |
| Região Central | 66 | 54 |
| Contratado/Credenciado | 6 | 6 |
| URD | 1 | 1 |
| sem Região de Saúde | 160 | 129 |

## Idade na solicitação

**02.05.02.006-2**:

| faixa | fila | pessoas |
|---|---|---|
| 0 a 9 | 804 | 713 |
| 10 a 19 | 399 | 362 |
| 20 a 29 | 681 | 593 |
| 30 a 39 | 1.178 | 964 |
| 40 a 49 | 2.517 | 1.977 |
| 50 a 59 | 4.004 | 2.991 |
| 60 a 69 | 3.078 | 2.428 |
| 70 a 79 | 1.338 | 1.105 |
| 80 a 89 | 387 | 299 |
| 90 a 99 | 42 | 33 |

## CID principais

**02.05.02.006-2**:

| CID | fila | pessoas |
|---|---|---|
| M75 | 2.195 | 1.857 |
| M25 | 1.757 | 1.299 |
| G56 | 1.355 | 929 |
| R22 | 975 | 969 |
| M65 | 963 | 714 |
| D17 | 716 | 711 |
| K40 | 675 | 623 |
| M71 | 539 | 495 |
| M79 | 462 | 363 |
| M23 | 397 | 321 |
| R52 | 244 | 106 |
| L72 | 221 | 220 |
| M77 | 206 | 153 |
| M72 | 200 | 158 |
| R59 | 191 | 188 |
| M13 | 156 | 83 |
| Q65 | 151 | 110 |
| Q76 | 138 | 138 |
| M17 | 125 | 102 |
| Z00 | 112 | 93 |

## Por ano da solicitação

**02.05.02.006-2**:

| ano | fila | fila viva |
|---|---|---|
| 2010 | 4 | 0 |
| 2017 | 1 | 0 |
| 2021 | 249 | 0 |
| 2022 | 668 | 0 |
| 2023 | 1.772 | 0 |
| 2024 | 1.657 | 356 |
| 2025 | 4.313 | 4.313 |
| 2026 | 5.764 | 5.764 |

## Entrantes por mês

Abertas = solicitações de todos os status pelo mês do pedido; agendadas = agendamentos pelo mês da solicitação (data do agendamento menos a espera). O último mês está incompleto.

**02.05.02.006-2**:

| mês | abertas | agendadas | entrantes (calculado) |
|---|---|---|---|
| 2024-10 | 279 | 645 | 924 |
| 2024-11 | 227 | 613 | 840 |
| 2024-12 | 203 | 553 | 756 |
| 2025-01 | 301 | 692 | 993 |
| 2025-02 | 267 | 645 | 912 |
| 2025-03 | 331 | 549 | 880 |
| 2025-04 | 311 | 578 | 889 |
| 2025-05 | 402 | 535 | 937 |
| 2025-06 | 348 | 505 | 853 |
| 2025-07 | 338 | 591 | 929 |
| 2025-08 | 487 | 539 | 1.026 |
| 2025-09 | 575 | 616 | 1.191 |
| 2025-10 | 512 | 544 | 1.056 |
| 2025-11 | 475 | 445 | 920 |
| 2025-12 | 395 | 362 | 757 |
| 2026-01 | 479 | 420 | 899 |
| 2026-02 | 458 | 457 | 915 |
| 2026-03 | 584 | 464 | 1.048 |
| 2026-04 | 510 | 375 | 885 |
| 2026-05 | 534 | 389 | 923 |
| 2026-06 | 651 | 309 | 960 |
| 2026-07 | 683 | 381 | 1.064 |
| 2026-08 | 760 | 328 | 1.088 |
| 2026-09 | 727 | 208 | 935 |
| 2026-10 | 667 | 81 | 748 |

## Nomes internos

O nome pedido na ordem e o nome exato do motor, com o invisível à mostra ({NBSP} é o espaço não separável). O JSON guarda o exato.

| pedido | exato |
|---|---|
| USG MAO ESQUERDA | USG MAO ESQUERDA |
| USG QUADRIL | USG QUADRIL |
| USG PE DIREITO | USG PE DIREITO |
| USG PE ESQUERDO | USG PE ESQUERDO |
| USG MAO DIREITA | USG MAO DIREITA |
| ECOGRAFIA DE ARTICULACAO COXA DIREITA | ECOGRAFIA DE ARTICULACAO COXA DIREITA |
| ECOGRAFIA DE ARTICULACAO COXA ESQUERDA | ECOGRAFIA DE ARTICULACAO COXA ESQUERDA |
| ULTRASSONOGRAFIA DO CALCANEO | ULTRASSONOGRAFIA DO CALCANEO |
| ULTRASSONOGRAFIA DO DEDO | ULTRASSONOGRAFIA DO DEDO |
| USG TENDAO DE AQUILES ESQUERDO | USG TENDAO DE AQUILES ESQUERDO |
| ECOGRAFIA DE ARTICULACAO OMBRO E ADULTO | ECOGRAFIA DE ARTICULACAO OMBRO E ADULTO |
| ECOGRAFIA DE ARTICULACAO PUNHO E ADULTO | ECOGRAFIA DE ARTICULACAO PUNHO E ADULTO |
| ECOGRAFIA  DE ARTICULACAO TORNOZELO E ADULTO | ECOGRAFIA  DE ARTICULACAO TORNOZELO E ADULTO |
| ECOGRAFIA DE ARTICULACAO COTOVELO E ADULTO | ECOGRAFIA DE ARTICULACAO COTOVELO E ADULTO |
| ECOGRAFIA  DE ARTICULACAO COXO-FEMURAL E ADULTO | ECOGRAFIA  DE ARTICULACAO COXO-FEMURAL E ADULTO |
| ECOGRAFIA  DE ARTICULACAO JOELHO D ADULTO | ECOGRAFIA  DE ARTICULACAO JOELHO D ADULTO |
| ECOGRAFIA  DE ARTICULACAO COXO-FEMURAL D INFANTIL | ECOGRAFIA  DE ARTICULACAO COXO-FEMURAL D INFANTIL |
| ECOGRAFIA  DE ARTICULACAO COXO-FEMURAL E INFANTIL | ECOGRAFIA  DE ARTICULACAO COXO-FEMURAL E INFANTIL |
| ECOGRAFIA  DE ARTICULACAO JOELHO E INFANTIL | ECOGRAFIA  DE ARTICULACAO JOELHO E INFANTIL |
| ECOGRAFIA  DE ARTICULACAO JOELHO D INFANTIL | ECOGRAFIA  DE ARTICULACAO JOELHO D INFANTIL |
| ECOGRAFIA DE ARTICULACAO COTOVELO D INFANTIL | ECOGRAFIA DE ARTICULACAO COTOVELO D INFANTIL |
| ECOGRAFIA DE ARTICULACAO PUNHO D INFANTIL | ECOGRAFIA DE ARTICULACAO PUNHO D INFANTIL |
| ECOGRAFIA DE ARTICULACAO PUNHO E INFANTIL | ECOGRAFIA DE ARTICULACAO PUNHO E INFANTIL |
| USG OMBRO ESQUERDO | USG OMBRO ESQUERDO |
| ECOGRAFIA  DE ARTICULACAO NAO LISTADA | ECOGRAFIA  DE ARTICULACAO NAO LISTADA |
| ECOGRAFIA DE ARTICULACAO COTOVELO E INFANTIL | ECOGRAFIA DE ARTICULACAO COTOVELO E INFANTIL |
| ECOGRAFIA  DE ARTICULACAO COXO-FEMURAL D ADULTO | ECOGRAFIA  DE ARTICULACAO COXO-FEMURAL D ADULTO |
| ECOGRAFIA DE ARTICULACAO OMBRO D ADULTO | ECOGRAFIA DE ARTICULACAO OMBRO D ADULTO |
| ECOGRAFIA DE ARTICULACAO PUNHO D ADULTO | ECOGRAFIA DE ARTICULACAO PUNHO D ADULTO |
| ECOGRAFIA  DE ARTICULACAO TORNOZELO D ADULTO | ECOGRAFIA  DE ARTICULACAO TORNOZELO D ADULTO |
| ECOGRAFIA  DE ARTICULACAO JOELHO E ADULTO | ECOGRAFIA  DE ARTICULACAO JOELHO E ADULTO |
| ECOGRAFIA DE ARTICULACAO COTOVELO D ADULTO | ECOGRAFIA DE ARTICULACAO COTOVELO D ADULTO |
| ECOGRAFIA DE QUADRIL DIREITO | ECOGRAFIA DE QUADRIL DIREITO |
| ECOGRAFIA DE QUADRIL ESQUERDO | ECOGRAFIA DE QUADRIL ESQUERDO |
| USG TENDAO DE AQUILES DIREITO | USG TENDAO DE AQUILES DIREITO |
| ECOGRAFIA  DE ARTICULACAO TORNOZELO E INFANTIL | ECOGRAFIA  DE ARTICULACAO TORNOZELO E INFANTIL |
| ECOGRAFIA  DE ARTICULACAO TORNOZELO D INFANTIL | ECOGRAFIA  DE ARTICULACAO TORNOZELO D INFANTIL |
| ECOGRAFIA  DE PARTES MOLES | ECOGRAFIA  DE PARTES MOLES |
| ECOGRAFIA DE REGIÃO INGUINAL ESQUERDO | ECOGRAFIA DE REGIÃO INGUINAL ESQUERDO |
| ECOGRAFIA DE REGIAO INGUINAL DIREITO | ECOGRAFIA DE REGIAO INGUINAL DIREITO |
| ULTRASSONOGRAFIA DA REGIAO INGUINAL | ULTRASSONOGRAFIA DA REGIAO INGUINAL |
| ULTRASSONOGRAFIA DO PESCOCO | ULTRASSONOGRAFIA DO PESCOCO |
| ULTRASSONOGRAFIA COM DOPPLER COLORIDO DE REGIAO CERVICAL | ULTRASSONOGRAFIA COM DOPPLER COLORIDO DE REGIAO CERVICAL |
| ULTRASSONOGRAFIA CERVICAL | ULTRASSONOGRAFIA CERVICAL |
| ULTRA-SONOGRAFIA DE REGIAO CERVICAL (PESCOCO) | ULTRA-SONOGRAFIA DE REGIAO CERVICAL (PESCOCO) |
| USG PERNA ESQUERDA | USG PERNA ESQUERDA |
| USG PERNA DIREITA | USG PERNA DIREITA |
| USG ESTRUTURA SUPERFICIE | USG ESTRUTURA SUPERFICIE |
| USG BRACO DIREITO | USG BRACO DIREITO |
| ECOGRAFIA PELVICA | ECOGRAFIA PELVICA |
| USB AXILA DIREITA | USB AXILA DIREITA |
| USG BRACO ESQUERDO | USG BRACO ESQUERDO |
| USG ANTEBRACO ESQUERDO | USG ANTEBRACO ESQUERDO |
| ULTRASSONOGRAFIA DA REGIAO LOMBAR | ULTRASSONOGRAFIA DA REGIAO LOMBAR |
| ULTRASSONOGRAFIA DAS GLANDULAS SUBMANDIBULARES | ULTRASSONOGRAFIA DAS GLANDULAS SUBMANDIBULARES |
| ULTRASSONOGRAFIA DA BACIA | ULTRASSONOGRAFIA DA BACIA |
| ECOGRAFIA DE ARTICULACAO COLUNA LOMBAR | ECOGRAFIA DE ARTICULACAO COLUNA LOMBAR |
| USG COXA DIREITA | USG COXA DIREITA |
| USG AXILA ESQUERDA | USG AXILA ESQUERDA |
| ULTRASSONOGRAFIA DA REGIAO GLUTEA | ULTRASSONOGRAFIA DA REGIAO GLUTEA |
| DOPPLER DE AORTA E ILIACA | DOPPLER DE AORTA E ILIACA |

## Diferença para a coleta anterior

Sem coleta anterior na pasta.
