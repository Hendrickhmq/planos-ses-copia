# Mapa Social da Saúde — panorama: diagnóstico em cardiologia, ecocardiografia, medicina nuclear, consultas de cardiologia, coleta de 27/10/2026

Ordem de coleta: R$ 2 mi de cardiologia (Emenda 41360018): panorama das filas de exames e consultas de cardiologia, com o rumo de cada código (entrantes, oferta pelo mês do agendamento, faltas), para ver o que outros planos atendem e o que a SES já dá conta

Coleta montada por `ferramentas/montar_coleta.py` a partir da saída do kit do motor: o modelo não escreveu número nenhum, e o resumo não se edita à mão (conferência K). A decisão de cada fila vem do enquadramento do plano.

| campo | conteúdo |
|---|---|
| Fonte | Mapa Social da Saúde – Regulamentação (MPDFT) · Lista de Espera – Exames e Consultas · `https://paineis-ext.mpdft.mp.br/extensions/mapasauderegulamentacao/mapasauderegulamentacao.html` · app Qlik `7edb02fa-f1f5-4ea6-b348-049a4ac2d095` · dados SISREG/DATASUS |
| Última recarga da base | 27/10/2026 12:32:51 (qLastReloadTime 2026-10-27T15:32:51.453Z) |
| Consulta | 27/10/2026 14:21:15 a 14:22:07 (relógio do motor), sem recarga no meio |
| Solicitação mais recente na base | 27/10/2026 (agendamento mais distante: 27/01/2027) |
| Medida | **fila** = os três status: pendente de regulação, corrigida e reenviada para regulação, pendente de regulação por fila de espera. Devolvidas para complementação ficam fora e são contadas à parte |
| Fila viva | só as solicitações a partir de `data_solicitacao={">=27/10/2024"}` (24 meses contados da solicitação mais recente) |
| Agendadas em 12 meses | `data_agendamento={">=27/10/2025<=26/10/2026"}`, todos os status |
| Ordem | panorama; `ordem.json` (hash 899825040) |
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
| diagnóstico em cardiologia | codigos: 02.11.02* | 5 | 72.346 | 34.129 | 64.933 |
| ecocardiografia | codigos: 02.05.01.001-6, 02.05.01.002-4, 02.05.01.003-2 | 4 | 14.629 | 14.623 | 14.605 |
| medicina nuclear | codigos: 02.08.01* | 3 | 3.274 | 3.274 | 1.942 |
| consultas de cardiologia | termos: CARDIOLOGIA | 13 | 25.954 | 21.271 | 25.056 |

## Varredura das filas (panorama)

Cada fila do universo (nome exato × código), sem decisão: o panorama só mostra. Anos de estoque = fila ÷ agendadas em 12 meses pelo mesmo nome e código (**calculado**).

### diagnóstico em cardiologia: por pessoas

| fila | código | fila | fila viva | pessoas | devolvidas | espera média | espera mediana | espera máxima | pedido mais antigo | agendadas 12 m | anos de estoque | CID principais |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| HOLTER 24 HORAS | 02.11.02.004-4 | 36.198 | 11.109 | 36.167 | 3.493 | 1.320,9 | 1.203,1 | 5.173,8 | 27/08/2012 | 2.756 | 13,1 | I10 6.379, I49 5.643, R00 4.365 |
| ELETROCARDIOGRAMA | 02.11.02.003-6 | 20.272 | 15.077 | 20.252 | 5.220 | 766,5 | 349,1 | 5.916,5 | 16/08/2010 | 14.194 | 1,4 | I10 10.213, R07 933, R00 919 |
| MONITORIZACAO AMBULATORIAL DE PRESSAO ARTERIAL | 02.11.02.005-2 | 12.678 | 6.245 | 12.670 | 1.412 | 1.008,2 | 761,0 | 4.243,0 | 16/03/2015 | 2.592 | 4,9 | I10 8.162, R03 553, I50 498 |
| TESTE DE ESFORCO OU TESTE ERGOMETRICO 2 | 02.11.02.006-0 | 3.181 | 1.682 | 3.181 | 2.198 | 827,2 | 648,1 | 1.980,8 | 25/05/2021 | 5.629 | 0,6 | I10 837, R07 640, I20 337 |
| CATETERISMO | 02.11.02.001-0 | 14 | 14 | 14 | 878 | 0,8 | 0,8 | 1,0 | 26/10/2026 | 7.564 | 0,0 | I20 4, I21 4, I50 1 |

### diagnóstico em cardiologia: as 20 de maior espera média

| fila | código | fila | fila viva | pessoas | devolvidas | espera média | espera mediana | espera máxima | pedido mais antigo | agendadas 12 m | anos de estoque | CID principais |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| HOLTER 24 HORAS | 02.11.02.004-4 | 36.198 | 11.109 | 36.167 | 3.493 | 1.320,9 | 1.203,1 | 5.173,8 | 27/08/2012 | 2.756 | 13,1 | I10 6.379, I49 5.643, R00 4.365 |
| MONITORIZACAO AMBULATORIAL DE PRESSAO ARTERIAL | 02.11.02.005-2 | 12.678 | 6.245 | 12.670 | 1.412 | 1.008,2 | 761,0 | 4.243,0 | 16/03/2015 | 2.592 | 4,9 | I10 8.162, R03 553, I50 498 |
| TESTE DE ESFORCO OU TESTE ERGOMETRICO 2 | 02.11.02.006-0 | 3.181 | 1.682 | 3.181 | 2.198 | 827,2 | 648,1 | 1.980,8 | 25/05/2021 | 5.629 | 0,6 | I10 837, R07 640, I20 337 |
| ELETROCARDIOGRAMA | 02.11.02.003-6 | 20.272 | 15.077 | 20.252 | 5.220 | 766,5 | 349,1 | 5.916,5 | 16/08/2010 | 14.194 | 1,4 | I10 10.213, R07 933, R00 919 |
| CATETERISMO | 02.11.02.001-0 | 14 | 14 | 14 | 878 | 0,8 | 0,8 | 1,0 | 26/10/2026 | 7.564 | 0,0 | I20 4, I21 4, I50 1 |

### diagnóstico em cardiologia: as 20 de mais anos de estoque

| fila | código | fila | fila viva | pessoas | devolvidas | espera média | espera mediana | espera máxima | pedido mais antigo | agendadas 12 m | anos de estoque | CID principais |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| HOLTER 24 HORAS | 02.11.02.004-4 | 36.198 | 11.109 | 36.167 | 3.493 | 1.320,9 | 1.203,1 | 5.173,8 | 27/08/2012 | 2.756 | 13,1 | I10 6.379, I49 5.643, R00 4.365 |
| MONITORIZACAO AMBULATORIAL DE PRESSAO ARTERIAL | 02.11.02.005-2 | 12.678 | 6.245 | 12.670 | 1.412 | 1.008,2 | 761,0 | 4.243,0 | 16/03/2015 | 2.592 | 4,9 | I10 8.162, R03 553, I50 498 |
| ELETROCARDIOGRAMA | 02.11.02.003-6 | 20.272 | 15.077 | 20.252 | 5.220 | 766,5 | 349,1 | 5.916,5 | 16/08/2010 | 14.194 | 1,4 | I10 10.213, R07 933, R00 919 |
| TESTE DE ESFORCO OU TESTE ERGOMETRICO 2 | 02.11.02.006-0 | 3.181 | 1.682 | 3.181 | 2.198 | 827,2 | 648,1 | 1.980,8 | 25/05/2021 | 5.629 | 0,6 | I10 837, R07 640, I20 337 |
| CATETERISMO | 02.11.02.001-0 | 14 | 14 | 14 | 878 | 0,8 | 0,8 | 1,0 | 26/10/2026 | 7.564 | 0,0 | I20 4, I21 4, I50 1 |

### ecocardiografia: por pessoas

| fila | código | fila | fila viva | pessoas | devolvidas | espera média | espera mediana | espera máxima | pedido mais antigo | agendadas 12 m | anos de estoque | CID principais |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1. ECOCARDIOGRAFIA BI-DIMENSIONAL COM DOPPLER ADULTO | 02.05.01.003-2 | 13.212 | 13.212 | 13.212 | 13.504 | 125,3 | 115,0 | 533,0 | 12/05/2025 | 33.880 | 0,4 | I10 2.410, I50 2.314, I25 1.150 |
| 2. ECOCARDIOGRAFIA BI-DIMENSIONAL COM DOPPLER INFANTIL | 02.05.01.003-2 | 1.309 | 1.309 | 1.308 | 2.554 | 108,2 | 102,9 | 713,8 | 12/11/2024 | 5.856 | 0,2 | R01 304, Q21 301, Q25 86 |
| 5. ECOCARDIOGRAFIA DE ESTRESSE ADULTO | 02.05.01.001-6 | 70 | 70 | 70 | 1.437 | 26,3 | 27,5 | 48,8 | 08/09/2026 | 757 | 0,1 | I20 16, I25 15, R07 10 |
| 9. ECOCARDIOGRAFIA FETAL | 02.05.01.003-2 | 30 | 30 | 30 | 388 | 35,2 | 13,7 | 301,8 | 29/12/2025 | 787 | 0,0 | Z35 12, O24 3, Q89 2 |

### ecocardiografia: as 20 de maior espera média

| fila | código | fila | fila viva | pessoas | devolvidas | espera média | espera mediana | espera máxima | pedido mais antigo | agendadas 12 m | anos de estoque | CID principais |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1. ECOCARDIOGRAFIA BI-DIMENSIONAL COM DOPPLER ADULTO | 02.05.01.003-2 | 13.212 | 13.212 | 13.212 | 13.504 | 125,3 | 115,0 | 533,0 | 12/05/2025 | 33.880 | 0,4 | I10 2.410, I50 2.314, I25 1.150 |
| 2. ECOCARDIOGRAFIA BI-DIMENSIONAL COM DOPPLER INFANTIL | 02.05.01.003-2 | 1.309 | 1.309 | 1.308 | 2.554 | 108,2 | 102,9 | 713,8 | 12/11/2024 | 5.856 | 0,2 | R01 304, Q21 301, Q25 86 |
| 9. ECOCARDIOGRAFIA FETAL | 02.05.01.003-2 | 30 | 30 | 30 | 388 | 35,2 | 13,7 | 301,8 | 29/12/2025 | 787 | 0,0 | Z35 12, O24 3, Q89 2 |
| 5. ECOCARDIOGRAFIA DE ESTRESSE ADULTO | 02.05.01.001-6 | 70 | 70 | 70 | 1.437 | 26,3 | 27,5 | 48,8 | 08/09/2026 | 757 | 0,1 | I20 16, I25 15, R07 10 |

### ecocardiografia: as 20 de mais anos de estoque

| fila | código | fila | fila viva | pessoas | devolvidas | espera média | espera mediana | espera máxima | pedido mais antigo | agendadas 12 m | anos de estoque | CID principais |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1. ECOCARDIOGRAFIA BI-DIMENSIONAL COM DOPPLER ADULTO | 02.05.01.003-2 | 13.212 | 13.212 | 13.212 | 13.504 | 125,3 | 115,0 | 533,0 | 12/05/2025 | 33.880 | 0,4 | I10 2.410, I50 2.314, I25 1.150 |
| 2. ECOCARDIOGRAFIA BI-DIMENSIONAL COM DOPPLER INFANTIL | 02.05.01.003-2 | 1.309 | 1.309 | 1.308 | 2.554 | 108,2 | 102,9 | 713,8 | 12/11/2024 | 5.856 | 0,2 | R01 304, Q21 301, Q25 86 |
| 5. ECOCARDIOGRAFIA DE ESTRESSE ADULTO | 02.05.01.001-6 | 70 | 70 | 70 | 1.437 | 26,3 | 27,5 | 48,8 | 08/09/2026 | 757 | 0,1 | I20 16, I25 15, R07 10 |
| 9. ECOCARDIOGRAFIA FETAL | 02.05.01.003-2 | 30 | 30 | 30 | 388 | 35,2 | 13,7 | 301,8 | 29/12/2025 | 787 | 0,0 | Z35 12, O24 3, Q89 2 |

### medicina nuclear: por pessoas

| fila | código | fila | fila viva | pessoas | devolvidas | espera média | espera mediana | espera máxima | pedido mais antigo | agendadas 12 m | anos de estoque | CID principais |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CINTILOGRAFIA DE MIOCARDIO P/ AVALIACAO DA PERFUSAO EM SITUACAO DE ESTRESSE (MINIMO 3 PROJECOES) | 02.08.01.002-5 | 1.732 | 1.732 | 1.732 | 149 | 289,7 | 350,1 | 454,7 | 29/07/2025 | 365 | 4,7 | I25 644, I20 539, I50 113 |
| CINTILOGRAFIA DE MIOCARDIO P/ AVALIACAO DA PERFUSAO EM SITUACAO DE REPOUSO (MINIMO 3 PROJECOES) | 02.08.01.003-3 | 1.492 | 1.492 | 1.492 | 34 | 286,7 | 363,8 | 454,7 | 29/07/2025 | 347 | 4,3 | I25 560, I20 448, I50 93 |
| CINTILOGRAFIA DE MIOCARDIO P/ LOCALIZACAO DE NECROSE | 02.08.01.004-1 | 50 | 50 | 50 | 2 | 176,0 | 159,6 | 398,1 | 24/09/2025 | 8 | 6,2 | E85 21, I25 11, I20 5 |

### medicina nuclear: as 20 de maior espera média

| fila | código | fila | fila viva | pessoas | devolvidas | espera média | espera mediana | espera máxima | pedido mais antigo | agendadas 12 m | anos de estoque | CID principais |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CINTILOGRAFIA DE MIOCARDIO P/ AVALIACAO DA PERFUSAO EM SITUACAO DE ESTRESSE (MINIMO 3 PROJECOES) | 02.08.01.002-5 | 1.732 | 1.732 | 1.732 | 149 | 289,7 | 350,1 | 454,7 | 29/07/2025 | 365 | 4,7 | I25 644, I20 539, I50 113 |
| CINTILOGRAFIA DE MIOCARDIO P/ AVALIACAO DA PERFUSAO EM SITUACAO DE REPOUSO (MINIMO 3 PROJECOES) | 02.08.01.003-3 | 1.492 | 1.492 | 1.492 | 34 | 286,7 | 363,8 | 454,7 | 29/07/2025 | 347 | 4,3 | I25 560, I20 448, I50 93 |
| CINTILOGRAFIA DE MIOCARDIO P/ LOCALIZACAO DE NECROSE | 02.08.01.004-1 | 50 | 50 | 50 | 2 | 176,0 | 159,6 | 398,1 | 24/09/2025 | 8 | 6,2 | E85 21, I25 11, I20 5 |

### medicina nuclear: as 20 de mais anos de estoque

| fila | código | fila | fila viva | pessoas | devolvidas | espera média | espera mediana | espera máxima | pedido mais antigo | agendadas 12 m | anos de estoque | CID principais |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CINTILOGRAFIA DE MIOCARDIO P/ LOCALIZACAO DE NECROSE | 02.08.01.004-1 | 50 | 50 | 50 | 2 | 176,0 | 159,6 | 398,1 | 24/09/2025 | 8 | 6,2 | E85 21, I25 11, I20 5 |
| CINTILOGRAFIA DE MIOCARDIO P/ AVALIACAO DA PERFUSAO EM SITUACAO DE ESTRESSE (MINIMO 3 PROJECOES) | 02.08.01.002-5 | 1.732 | 1.732 | 1.732 | 149 | 289,7 | 350,1 | 454,7 | 29/07/2025 | 365 | 4,7 | I25 644, I20 539, I50 113 |
| CINTILOGRAFIA DE MIOCARDIO P/ AVALIACAO DA PERFUSAO EM SITUACAO DE REPOUSO (MINIMO 3 PROJECOES) | 02.08.01.003-3 | 1.492 | 1.492 | 1.492 | 34 | 286,7 | 363,8 | 454,7 | 29/07/2025 | 347 | 4,3 | I25 560, I20 448, I50 93 |

### consultas de cardiologia: por pessoas

| fila | código | fila | fila viva | pessoas | devolvidas | espera média | espera mediana | espera máxima | pedido mais antigo | agendadas 12 m | anos de estoque | CID principais |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CONSULTA EM CARDIOLOGIA - ADULTO | 03.01.01.007-2 | 11.097 | 8.220 | 11.082 | 8.739 | 482,7 | 404,7 | 2.176,7 | 10/11/2020 | 5.958 | 1,9 | I10 1.899, I50 1.251, I25 868 |
| CONSULTA EM CARDIOLOGIA - RISCO CIRURGICO | 03.01.01.007-2 | 9.727 | 8.236 | 9.654 | 4.247 | 428,6 | 421,1 | 1.467,1 | 21/10/2022 | 5.928 | 1,6 | I83 1.335, K80 1.307, K40 659 |
| CONSULTA EM CARDIOLOGIA - PEDIATRIA | 03.01.01.007-2 | 1.812 | 1.499 | 1.812 | 513 | 486,0 | 427,8 | 1.974,0 | 01/06/2021 | 2.722 | 0,7 | Q21 416, Q25 140, R01 134 |
| CONSULTA EM CARDIOLOGIA - INSUFICIENCIA CARDIACA | 03.01.01.007-2 | 1.108 | 1.108 | 1.108 | 882 | 208,1 | 187,5 | 650,0 | 15/01/2025 | 599 | 1,8 | I50 895, I25 31, I42 20 |
| CONSULTA EM CARDIOLOGIA - MARCAPASSO | 03.01.01.007-2 | 508 | 507 | 508 | 83 | 55,9 | 54,1 | 1.614,1 | 27/05/2022 | 1.986 | 0,3 | Z45 433, Z95 19, I44 15 |
| CONSULTA EM CARDIOLOGIA - ARRITMIA | 03.01.01.007-2 | 437 | 437 | 437 | 1.099 | 56,6 | 48,8 | 132,0 | 17/06/2026 | 1.961 | 0,2 | I49 133, I48 75, I47 59 |
| CONSULTA EM CARDIOLOGIA - CORONARIA | 03.01.01.007-2 | 322 | 322 | 322 | 539 | 112,2 | 110,5 | 305,0 | 26/12/2025 | 604 | 0,5 | I25 154, I21 64, I20 52 |
| CONSULTA EM CARDIOLOGIA - VALVULOPATIA | 03.01.01.007-2 | 321 | 320 | 321 | 354 | 148,3 | 137,1 | 3.514,1 | 14/03/2017 | 293 | 1,1 | I35 80, I34 62, I05 56 |
| CONSULTA EM CARDIOLOGIA - FIBRILACAO ATRIAL | 03.01.01.007-2 | 241 | 241 | 241 | 164 | 173,0 | 167,0 | 357,8 | 03/11/2025 | 224 | 1,1 | I48 188, I49 18, I50 9 |
| ATENDIMENTO MULTIDICIPLINAR EM CARDIOLOGIA E ENDOCRINOLOGIA - MACC | 03.01.01.007-2 | 239 | 239 | 239 | 323 | 117,6 | 95,8 | 425,9 | 27/08/2025 | 142 | 1,7 | E10 69, E11 55, I10 35 |
| ATENDIMENTO MULTIDISCIPLINAR EM CARDIOLOGIA - MACC | 03.01.01.007-2 | 65 | 65 | 65 | 148 | 47,9 | 37,4 | 194,0 | 16/04/2026 | 349 | 0,2 | I10 21, I25 7, I50 6 |
| CONSULTA EM CARDIOLOGIA - CIRURGIA CARDIACA | 03.01.01.007-2 | 50 | 50 | 50 | 292 | 15,3 | 13,0 | 31,8 | 25/09/2026 | 956 | 0,1 | I25 7, I35 6, I71 5 |
| CONSULTA EM CARDIOLOGIA - POS-OPERATORIO | 03.01.01.007-2 | 27 | 27 | 27 | 115 | 27,1 | 19,8 | 146,0 | 03/06/2026 | 347 | 0,1 | I21 8, I25 6, Z95 3 |

### consultas de cardiologia: as 20 de maior espera média

| fila | código | fila | fila viva | pessoas | devolvidas | espera média | espera mediana | espera máxima | pedido mais antigo | agendadas 12 m | anos de estoque | CID principais |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CONSULTA EM CARDIOLOGIA - PEDIATRIA | 03.01.01.007-2 | 1.812 | 1.499 | 1.812 | 513 | 486,0 | 427,8 | 1.974,0 | 01/06/2021 | 2.722 | 0,7 | Q21 416, Q25 140, R01 134 |
| CONSULTA EM CARDIOLOGIA - ADULTO | 03.01.01.007-2 | 11.097 | 8.220 | 11.082 | 8.739 | 482,7 | 404,7 | 2.176,7 | 10/11/2020 | 5.958 | 1,9 | I10 1.899, I50 1.251, I25 868 |
| CONSULTA EM CARDIOLOGIA - RISCO CIRURGICO | 03.01.01.007-2 | 9.727 | 8.236 | 9.654 | 4.247 | 428,6 | 421,1 | 1.467,1 | 21/10/2022 | 5.928 | 1,6 | I83 1.335, K80 1.307, K40 659 |
| CONSULTA EM CARDIOLOGIA - INSUFICIENCIA CARDIACA | 03.01.01.007-2 | 1.108 | 1.108 | 1.108 | 882 | 208,1 | 187,5 | 650,0 | 15/01/2025 | 599 | 1,8 | I50 895, I25 31, I42 20 |
| CONSULTA EM CARDIOLOGIA - FIBRILACAO ATRIAL | 03.01.01.007-2 | 241 | 241 | 241 | 164 | 173,0 | 167,0 | 357,8 | 03/11/2025 | 224 | 1,1 | I48 188, I49 18, I50 9 |
| CONSULTA EM CARDIOLOGIA - VALVULOPATIA | 03.01.01.007-2 | 321 | 320 | 321 | 354 | 148,3 | 137,1 | 3.514,1 | 14/03/2017 | 293 | 1,1 | I35 80, I34 62, I05 56 |
| ATENDIMENTO MULTIDICIPLINAR EM CARDIOLOGIA E ENDOCRINOLOGIA - MACC | 03.01.01.007-2 | 239 | 239 | 239 | 323 | 117,6 | 95,8 | 425,9 | 27/08/2025 | 142 | 1,7 | E10 69, E11 55, I10 35 |
| CONSULTA EM CARDIOLOGIA - CORONARIA | 03.01.01.007-2 | 322 | 322 | 322 | 539 | 112,2 | 110,5 | 305,0 | 26/12/2025 | 604 | 0,5 | I25 154, I21 64, I20 52 |
| CONSULTA EM CARDIOLOGIA - ARRITMIA | 03.01.01.007-2 | 437 | 437 | 437 | 1.099 | 56,6 | 48,8 | 132,0 | 17/06/2026 | 1.961 | 0,2 | I49 133, I48 75, I47 59 |
| CONSULTA EM CARDIOLOGIA - MARCAPASSO | 03.01.01.007-2 | 508 | 507 | 508 | 83 | 55,9 | 54,1 | 1.614,1 | 27/05/2022 | 1.986 | 0,3 | Z45 433, Z95 19, I44 15 |
| ATENDIMENTO MULTIDISCIPLINAR EM CARDIOLOGIA - MACC | 03.01.01.007-2 | 65 | 65 | 65 | 148 | 47,9 | 37,4 | 194,0 | 16/04/2026 | 349 | 0,2 | I10 21, I25 7, I50 6 |
| CONSULTA EM CARDIOLOGIA - POS-OPERATORIO | 03.01.01.007-2 | 27 | 27 | 27 | 115 | 27,1 | 19,8 | 146,0 | 03/06/2026 | 347 | 0,1 | I21 8, I25 6, Z95 3 |
| CONSULTA EM CARDIOLOGIA - CIRURGIA CARDIACA | 03.01.01.007-2 | 50 | 50 | 50 | 292 | 15,3 | 13,0 | 31,8 | 25/09/2026 | 956 | 0,1 | I25 7, I35 6, I71 5 |

### consultas de cardiologia: as 20 de mais anos de estoque

| fila | código | fila | fila viva | pessoas | devolvidas | espera média | espera mediana | espera máxima | pedido mais antigo | agendadas 12 m | anos de estoque | CID principais |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CONSULTA EM CARDIOLOGIA - ADULTO | 03.01.01.007-2 | 11.097 | 8.220 | 11.082 | 8.739 | 482,7 | 404,7 | 2.176,7 | 10/11/2020 | 5.958 | 1,9 | I10 1.899, I50 1.251, I25 868 |
| CONSULTA EM CARDIOLOGIA - INSUFICIENCIA CARDIACA | 03.01.01.007-2 | 1.108 | 1.108 | 1.108 | 882 | 208,1 | 187,5 | 650,0 | 15/01/2025 | 599 | 1,8 | I50 895, I25 31, I42 20 |
| ATENDIMENTO MULTIDICIPLINAR EM CARDIOLOGIA E ENDOCRINOLOGIA - MACC | 03.01.01.007-2 | 239 | 239 | 239 | 323 | 117,6 | 95,8 | 425,9 | 27/08/2025 | 142 | 1,7 | E10 69, E11 55, I10 35 |
| CONSULTA EM CARDIOLOGIA - RISCO CIRURGICO | 03.01.01.007-2 | 9.727 | 8.236 | 9.654 | 4.247 | 428,6 | 421,1 | 1.467,1 | 21/10/2022 | 5.928 | 1,6 | I83 1.335, K80 1.307, K40 659 |
| CONSULTA EM CARDIOLOGIA - VALVULOPATIA | 03.01.01.007-2 | 321 | 320 | 321 | 354 | 148,3 | 137,1 | 3.514,1 | 14/03/2017 | 293 | 1,1 | I35 80, I34 62, I05 56 |
| CONSULTA EM CARDIOLOGIA - FIBRILACAO ATRIAL | 03.01.01.007-2 | 241 | 241 | 241 | 164 | 173,0 | 167,0 | 357,8 | 03/11/2025 | 224 | 1,1 | I48 188, I49 18, I50 9 |
| CONSULTA EM CARDIOLOGIA - PEDIATRIA | 03.01.01.007-2 | 1.812 | 1.499 | 1.812 | 513 | 486,0 | 427,8 | 1.974,0 | 01/06/2021 | 2.722 | 0,7 | Q21 416, Q25 140, R01 134 |
| CONSULTA EM CARDIOLOGIA - CORONARIA | 03.01.01.007-2 | 322 | 322 | 322 | 539 | 112,2 | 110,5 | 305,0 | 26/12/2025 | 604 | 0,5 | I25 154, I21 64, I20 52 |
| CONSULTA EM CARDIOLOGIA - MARCAPASSO | 03.01.01.007-2 | 508 | 507 | 508 | 83 | 55,9 | 54,1 | 1.614,1 | 27/05/2022 | 1.986 | 0,3 | Z45 433, Z95 19, I44 15 |
| CONSULTA EM CARDIOLOGIA - ARRITMIA | 03.01.01.007-2 | 437 | 437 | 437 | 1.099 | 56,6 | 48,8 | 132,0 | 17/06/2026 | 1.961 | 0,2 | I49 133, I48 75, I47 59 |
| ATENDIMENTO MULTIDISCIPLINAR EM CARDIOLOGIA - MACC | 03.01.01.007-2 | 65 | 65 | 65 | 148 | 47,9 | 37,4 | 194,0 | 16/04/2026 | 349 | 0,2 | I10 21, I25 7, I50 6 |
| CONSULTA EM CARDIOLOGIA - POS-OPERATORIO | 03.01.01.007-2 | 27 | 27 | 27 | 115 | 27,1 | 19,8 | 146,0 | 03/06/2026 | 347 | 0,1 | I21 8, I25 6, Z95 3 |
| CONSULTA EM CARDIOLOGIA - CIRURGIA CARDIACA | 03.01.01.007-2 | 50 | 50 | 50 | 292 | 15,3 | 13,0 | 31,8 | 25/09/2026 | 956 | 0,1 | I25 7, I35 6, I71 5 |

## Rumo por código

Um código por linha, com as filas do universo somadas (cada par nome × código uma vez). Tudo **calculado** no montador sobre a série mensal do motor (abas "Por código" da planilha). Os 12 meses fechados vão de 2025-10 a 2026-09, e os 12 de antes, de 2024-10 a 2025-09. Entrantes = pedidos abertos mais os já agendados, pelo mês do pedido. Oferta = agendamentos pelo mês em que acontecem, em todas as situações. Falta = faltas ÷ (realizados + faltas). Saldo por mês = (entrantes − oferta) ÷ 12: positivo, a fila cresce. Maior mês de oferta e média dos 3 últimos meses fechados, para ver o esforço que parou.

| código | fila mais pedida do código | fila | fila viva | devolvidas | entrantes 12 m | entrantes 12 m antes | oferta 12 m | oferta 12 m antes | saldo por mês | falta 12 m | maior mês de oferta | oferta média 3 últimos meses |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 02.11.02.004-4 | HOLTER 24 HORAS | 36.198 | 11.109 | 3.493 | 6.723 | 7.048 | 2.619 | 830 | 342,0 | 49% | 2026-03 (280) | 259,3 |
| 03.01.01.007-2 | CONSULTA EM CARDIOLOGIA - ADULTO | 25.954 | 21.271 | 17.498 | 396.887 | 366.581 | 321.021 | 278.828 | 6.322,2 | 26% | 2026-07 (38.419) | 35.092,7 |
| 02.11.02.003-6 | ELETROCARDIOGRAMA | 20.272 | 15.077 | 5.220 | 18.485 | 18.870 | 14.422 | 16.413 | 338,6 | 42% | 2025-01 (1.765) | 1.264,3 |
| 02.05.01.003-2 | 1. ECOCARDIOGRAFIA BI-DIMENSIONAL COM DOPPLER ADULTO | 14.551 | 14.551 | 16.446 | 42.983 | 42.338 | 40.371 | 40.157 | 217,7 | 26% | 2024-10 (3.783) | 3.571,0 |
| 02.11.02.005-2 | MONITORIZACAO AMBULATORIAL DE PRESSAO ARTERIAL | 12.678 | 6.245 | 1.412 | 4.661 | 4.505 | 2.519 | 2.100 | 178,5 | 40% | 2026-08 (270) | 255,7 |
| 02.11.02.006-0 | TESTE DE ESFORCO OU TESTE ERGOMETRICO 2 | 3.181 | 1.682 | 2.198 | 5.650 | 5.909 | 5.789 | 4.948 | -11,6 | 35% | 2026-06 (713) | 476,3 |
| 02.08.01.002-5 | CINTILOGRAFIA DE MIOCARDIO P/ AVALIACAO DA PERFUSAO EM SITUACAO DE ESTRESSE (MINIMO 3 PROJECOES) | 1.732 | 1.732 | 149 | 1.274 | 1.054 | 374 | 84 | 75,0 | 44% | 2025-09 (53) | 40,0 |
| 02.08.01.003-3 | CINTILOGRAFIA DE MIOCARDIO P/ AVALIACAO DA PERFUSAO EM SITUACAO DE REPOUSO (MINIMO 3 PROJECOES) | 1.492 | 1.492 | 34 | 1.003 | 943 | 357 | 52 | 53,8 | 42% | 2025-10 (62) | 39,0 |
| 02.05.01.001-6 | 5. ECOCARDIOGRAFIA DE ESTRESSE ADULTO | 70 | 70 | 1.437 | 856 | 790 | 752 | 729 | 8,7 | 47% | 2026-07 (75) | 69,7 |
| 02.08.01.004-1 | CINTILOGRAFIA DE MIOCARDIO P/ LOCALIZACAO DE NECROSE | 50 | 50 | 2 | 56 | 13 | 13 | 4 | 3,6 | 73% | 2025-10 (5) | 0,0 |
| 02.11.02.001-0 | CATETERISMO | 14 | 14 | 878 | 7.481 | 7.381 | 7.547 | 7.113 | -5,5 | 12% | 2026-03 (705) | 692,3 |

## Região de Saúde

Região de Saúde: não pedida na ordem.

## Diferença para a coleta anterior

Contra `dados/fontes/mapa_social_20261025_bruto/coleta_20261025.json` (recarga 25/10/2026 14:31:55). Diferença **calculada** no montador.

A coleta anterior não tem as mesmas filas nem os mesmos objetos.
