# Mapa Social da Saúde — fila de 1. ECOCARDIOGRAFIA BI-DIMENSIONAL COM DOPPLER ADULTO (eco adulto); 2. ECOCARDIOGRAFIA BI-DIMENSIONAL COM DOPPLER INFANTIL (eco infantil); 9. ECOCARDIOGRAFIA FETAL (eco fetal); 5. ECOCARDIOGRAFIA DE ESTRESSE ADULTO (eco de estresse); 7. ECOCARDIOGRAFIA TRANSEOFAGICA ADULTO (eco transesofágico adulto), coleta de 04/11/2026

Ordem de coleta: Eco ambulatorial de 04/11/2026, fila a fila: entrantes, oferta pelo mês do agendamento (realizados e faltas), situação e ano de cada fila de ecocardiografia com fila viva

Coleta montada por `ferramentas/montar_coleta.py` a partir da saída do kit do motor: o modelo não escreveu número nenhum, e o resumo não se edita à mão (conferência K). A decisão de cada fila vem do enquadramento do plano.

| campo | conteúdo |
|---|---|
| Fonte | Mapa Social da Saúde – Regulamentação (MPDFT) · Lista de Espera – Exames e Consultas · `https://paineis-ext.mpdft.mp.br/extensions/mapasauderegulamentacao/mapasauderegulamentacao.html` · app Qlik `7edb02fa-f1f5-4ea6-b348-049a4ac2d095` · dados SISREG/DATASUS |
| Última recarga da base | 04/11/2026 14:33:58 (qLastReloadTime 2026-11-04T17:33:58.854Z) |
| Consulta | 04/11/2026 15:39:10 a 15:39:37 (relógio do motor), sem recarga no meio |
| Solicitação mais recente na base | 03/11/2026 (agendamento mais distante: 04/02/2027) |
| Medida | **fila** = os três status: pendente de regulação, corrigida e reenviada para regulação, pendente de regulação por fila de espera. Devolvidas para complementação ficam fora e são contadas à parte |
| Fila viva | só as solicitações a partir de `data_solicitacao={">=03/11/2024"}` (24 meses contados da solicitação mais recente) |
| Agendadas em 12 meses | `data_agendamento={">=03/11/2025<=02/11/2026"}`, todos os status |
| Ordem | medicao; `ordem.json` (hash 3299284906) |
| Via | kit do motor `ferramentas/mapa_social/motor.js` (versão 2026-10-27, assinatura 1939648169); saída pela área de transferência, 1 parte(s) conferidas por hash (`ferramentas/ler_motor.py`) |

Pessoas = CNS distintos no conjunto (quem espera por mais de um exame conta uma vez); só a contagem sai do motor. Espera em dias, calculada no motor sobre os registros do conjunto.

## Alarmes

nenhum

## Lacunas

nenhuma

## Exames

A união das filas de cada exame, na idade e no sexo da ordem, quando ela os dá.

| exame | filas | fila | fila viva | pessoas | pessoas viva | devolvidas | espera média | espera mediana |
|---|---|---|---|---|---|---|---|---|
| 1. ECOCARDIOGRAFIA BI-DIMENSIONAL COM DOPPLER ADULTO (eco adulto) | 1 | 13.474 | 13.474 | **13.473** | 13.473 | 13.473 | 129,7 | 119,0 |
| 2. ECOCARDIOGRAFIA BI-DIMENSIONAL COM DOPPLER INFANTIL (eco infantil) | 1 | 1.360 | 1.360 | **1.360** | 1.360 | 2.568 | 111,7 | 104,0 |
| 9. ECOCARDIOGRAFIA FETAL (eco fetal) | 1 | 36 | 36 | **36** | 36 | 391 | 36,9 | 19,6 |
| 5. ECOCARDIOGRAFIA DE ESTRESSE ADULTO (eco de estresse) | 1 | 69 | 69 | **69** | 69 | 1.437 | 28,4 | 29,0 |
| 7. ECOCARDIOGRAFIA TRANSEOFAGICA ADULTO (eco transesofágico adulto) | 1 | 8 | 8 | **8** | 8 | 1.049 | 58,0 | 5,0 |

## Filas do objeto

As filas de partida da ordem, pelo nome exato do motor, sem recorte de CID. Anos de estoque = fila ÷ agendadas em 12 meses (**calculado** no montador).

| fila | código | objeto | papel | fila | fila viva | pessoas | devolvidas | espera média | espera mediana | espera máxima | pedido mais antigo | agendadas 12 m | anos de estoque | CID principais |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1. ECOCARDIOGRAFIA BI-DIMENSIONAL COM DOPPLER ADULTO | 02.05.01.003-2 | eco adulto | exame (genérica) | 13.474 | 13.474 | 13.473 | 13.473 | 129,7 | 119,0 | 541,1 | 12/05/2025 | 33.842 | 0,4 | I10 2.444, I50 2.343, I25 1.174, R07 499, I20 489 |
| 2. ECOCARDIOGRAFIA BI-DIMENSIONAL COM DOPPLER INFANTIL | 02.05.01.003-2 | eco infantil | exame (genérica) | 1.360 | 1.360 | 1.360 | 2.568 | 111,7 | 104,0 | 721,9 | 12/11/2024 | 5.847 | 0,2 | R01 317, Q21 306, Q25 92, Q20 41, Q24 38 |
| 9. ECOCARDIOGRAFIA FETAL | 02.05.01.003-2 | eco fetal | exame (genérica) | 36 | 36 | 36 | 391 | 36,9 | 19,6 | 309,9 | 29/12/2025 | 786 | 0,0 | Z35 16, Z36 3, E11 2, O24 2, Q89 2 |
| 5. ECOCARDIOGRAFIA DE ESTRESSE ADULTO | 02.05.01.001-6 | eco de estresse | exame | 69 | 69 | 69 | 1.437 | 28,4 | 29,0 | 50,9 | 14/09/2026 | 763 | 0,1 | I20 19, I25 15, I10 8, I50 8, R07 7 |
| 7. ECOCARDIOGRAFIA TRANSEOFAGICA ADULTO | 02.05.01.002-4 | eco transesofágico adulto | exame (genérica) | 8 | 8 | 8 | 1.049 | 58,0 | 5,0 | 406,9 | 23/09/2025 | 1.134 | 0,0 | I33 3, C50 1, R94 1, I35 1, R78 1 |

## Varredura das filas

Toda fila que a varredura achou, pelo código, pelo nome e, na OCI, pelo CID aceito e pelo da finalidade, nas tabelas de solicitações e de agendamentos. A decisão é a do enquadramento do plano; fila sem decisão sai **a decidir** e não entra na soma.

| fila | código | tabela | achada por | objeto | fila | fila viva | pessoas | devolvidas | espera média | pedido mais antigo | agendadas 12 m | CID principais | no CID do objeto | parte no CID aceito (calculado) | decisão | motivo |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1. ECOCARDIOGRAFIA BI-DIMENSIONAL COM DOPPLER ADULTO (genérica) | 02.05.01.003-2 | solicitações | código, nome | eco adulto, eco fetal, eco infantil | 13.474 | 13.474 | 13.473 | 13.473 | 129,7 | 12/05/2025 | 33.842 | I10 2.444, I50 2.343, I25 1.174, R07 499, I20 489 | — | — | fica fora | compatível, não obrigatório: a porta é a consulta, ou a consulta com os obrigatórios (usuário, 27/10/2026) |
| 2. ECOCARDIOGRAFIA BI-DIMENSIONAL COM DOPPLER INFANTIL (genérica) | 02.05.01.003-2 | solicitações | código, nome | eco adulto, eco fetal, eco infantil | 1.360 | 1.360 | 1.360 | 2.568 | 111,7 | 12/11/2024 | 5.847 | R01 317, Q21 306, Q25 92, Q20 41, Q24 38 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| 5. ECOCARDIOGRAFIA DE ESTRESSE ADULTO | 02.05.01.001-6 | solicitações | código, nome | eco de estresse | 69 | 69 | 69 | 1.437 | 28,4 | 14/09/2026 | 763 | I20 19, I25 15, I10 8, I50 8, R07 7 | — | — | fica fora | obrigatório na 004-2: não conta em nenhum dos dois casos; no caso 2, a linha coronária conta só os obrigatórios da 003-4 (eletrocardiograma e ergométrico) (usuário, 27/10/2026) |
| 9. ECOCARDIOGRAFIA FETAL (genérica) | 02.05.01.003-2 | solicitações | código, nome | eco adulto, eco fetal, eco infantil | 36 | 36 | 36 | 391 | 36,9 | 29/12/2025 | 786 | Z35 16, Z36 3, E11 2, O24 2, Q89 2 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| 7. ECOCARDIOGRAFIA TRANSEOFAGICA ADULTO (genérica) | 02.05.01.002-4 | solicitações | código, nome | eco transesofágico adulto | 8 | 8 | 8 | 1.049 | 58,0 | 23/09/2025 | 1.134 | I33 3, C50 1, R94 1, I35 1, R78 1 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ECOCARDIOGRAFIA BI-DIMENSIONAL SEM DOPPLER ADULTO (genérica) | 02.05.01.003-2 | solicitações | código | eco adulto, eco fetal, eco infantil | 2 | 0 | 2 | 0 | 6.969,6 | 03/10/2007 | — | R68 2 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 16.ECOCARDIOGRAFIA TRANSTORACICA - INFANTIL (genérica) | 02.05.01.003-2 | solicitações | código | eco adulto, eco fetal, eco infantil | 1 | 0 | 1 | 0 | 4.950,9 | 15/04/2013 | 0 | L81 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 8. ECOCARDIOGRAFIA TRANSEOFAGICA INFANTIL (genérica) | 02.05.01.002-4 | solicitações | código | eco transesofágico adulto | 1 | 0 | 1 | 46 | 1.825,1 | 05/11/2021 | 0 | Q20 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOCARDIOGRAFIA BI-DIMENSIONAL SEM DOPPLER ADULTO EMERGENCIA (genérica) | 02.05.01.003-2 | solicitações | código | eco adulto, eco fetal, eco infantil | 1 | 0 | 1 | 0 | 6.986,6 | 19/09/2007 | — | R68 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOCARDIOGRAFIA BI-DIMENSIONAL SEM DOPPLER INFANTIL (genérica) | 02.05.01.003-2 | solicitações | código | eco adulto, eco fetal, eco infantil | 1 | 0 | 1 | 0 | 6.980,6 | 25/09/2007 | — | R68 1 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOCARDIOGRAMA (genérica) | 02.05.01.002-4 | só agendamentos | código | eco transesofágico adulto | — | — | — | — | — | — | 1 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| 6. ECOCARDIOGRAFIA DE ESTRESSE INFANTIL | 02.05.01.001-6 | só agendamentos | código | eco de estresse | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |

## Região de Saúde

Região de Saúde: não pedida na ordem.

## Por ano da solicitação

**eco adulto**:

| ano | fila | fila viva |
|---|---|---|
| 2025 | 572 | 572 |
| 2026 | 12.902 | 12.902 |

**eco infantil**:

| ano | fila | fila viva |
|---|---|---|
| 2024 | 2 | 2 |
| 2025 | 1 | 1 |
| 2026 | 1.357 | 1.357 |

**eco fetal**:

| ano | fila | fila viva |
|---|---|---|
| 2025 | 1 | 1 |
| 2026 | 35 | 35 |

**eco de estresse**:

| ano | fila | fila viva |
|---|---|---|
| 2026 | 69 | 69 |

**eco transesofágico adulto**:

| ano | fila | fila viva |
|---|---|---|
| 2025 | 1 | 1 |
| 2026 | 7 | 7 |

## Entrantes por mês

Abertas = solicitações de todos os status pelo mês do pedido; agendadas = agendamentos pelo mês da solicitação (data do agendamento menos a espera). O último mês está incompleto.

**eco adulto**:

| mês | abertas | agendadas | entrantes (calculado) |
|---|---|---|---|
| 2024-11 | 98 | 2.427 | 2.525 |
| 2024-12 | 119 | 2.292 | 2.411 |
| 2025-01 | 131 | 2.948 | 3.079 |
| 2025-02 | 164 | 2.761 | 2.925 |
| 2025-03 | 217 | 2.656 | 2.873 |
| 2025-04 | 182 | 2.784 | 2.966 |
| 2025-05 | 232 | 2.697 | 2.929 |
| 2025-06 | 208 | 2.821 | 3.029 |
| 2025-07 | 230 | 3.048 | 3.278 |
| 2025-08 | 262 | 2.813 | 3.075 |
| 2025-09 | 258 | 2.709 | 2.967 |
| 2025-10 | 207 | 2.619 | 2.826 |
| 2025-11 | 194 | 2.351 | 2.545 |
| 2025-12 | 308 | 2.189 | 2.497 |
| 2026-01 | 290 | 2.570 | 2.860 |
| 2026-02 | 265 | 2.465 | 2.730 |
| 2026-03 | 799 | 2.416 | 3.215 |
| 2026-04 | 1.652 | 1.275 | 2.927 |
| 2026-05 | 1.783 | 1.432 | 3.215 |
| 2026-06 | 1.659 | 1.375 | 3.034 |
| 2026-07 | 1.803 | 1.524 | 3.327 |
| 2026-08 | 2.041 | 1.308 | 3.349 |
| 2026-09 | 1.762 | 1.310 | 3.072 |
| 2026-10 | 1.785 | 1.248 | 3.033 |
| 2026-11 | 51 | 22 | 73 |

**eco infantil**:

| mês | abertas | agendadas | entrantes (calculado) |
|---|---|---|---|
| 2024-11 | 52 | 473 | 525 |
| 2024-12 | 31 | 519 | 550 |
| 2025-01 | 35 | 525 | 560 |
| 2025-02 | 34 | 512 | 546 |
| 2025-03 | 26 | 490 | 516 |
| 2025-04 | 32 | 471 | 503 |
| 2025-05 | 26 | 473 | 499 |
| 2025-06 | 18 | 504 | 522 |
| 2025-07 | 23 | 545 | 568 |
| 2025-08 | 40 | 503 | 543 |
| 2025-09 | 23 | 529 | 552 |
| 2025-10 | 40 | 528 | 568 |
| 2025-11 | 29 | 444 | 473 |
| 2025-12 | 65 | 384 | 449 |
| 2026-01 | 28 | 489 | 517 |
| 2026-02 | 24 | 413 | 437 |
| 2026-03 | 113 | 424 | 537 |
| 2026-04 | 247 | 305 | 552 |
| 2026-05 | 286 | 316 | 602 |
| 2026-06 | 269 | 306 | 575 |
| 2026-07 | 240 | 308 | 548 |
| 2026-08 | 305 | 353 | 658 |
| 2026-09 | 275 | 307 | 582 |
| 2026-10 | 287 | 220 | 507 |
| 2026-11 | 19 | 0 | 19 |

**eco fetal**:

| mês | abertas | agendadas | entrantes (calculado) |
|---|---|---|---|
| 2024-11 | 6 | 31 | 37 |
| 2024-12 | 4 | 31 | 35 |
| 2025-01 | 0 | 39 | 39 |
| 2025-02 | 7 | 49 | 56 |
| 2025-03 | 3 | 46 | 49 |
| 2025-04 | 9 | 80 | 89 |
| 2025-05 | 0 | 75 | 75 |
| 2025-06 | 3 | 62 | 65 |
| 2025-07 | 6 | 82 | 88 |
| 2025-08 | 9 | 89 | 98 |
| 2025-09 | 6 | 72 | 78 |
| 2025-10 | 4 | 74 | 78 |
| 2025-11 | 4 | 70 | 74 |
| 2025-12 | 8 | 50 | 58 |
| 2026-01 | 0 | 70 | 70 |
| 2026-02 | 4 | 84 | 88 |
| 2026-03 | 3 | 73 | 76 |
| 2026-04 | 3 | 54 | 57 |
| 2026-05 | 15 | 47 | 62 |
| 2026-06 | 9 | 61 | 70 |
| 2026-07 | 4 | 70 | 74 |
| 2026-08 | 14 | 66 | 80 |
| 2026-09 | 36 | 56 | 92 |
| 2026-10 | 57 | 47 | 104 |
| 2026-11 | 2 | 0 | 2 |

**eco de estresse**:

| mês | abertas | agendadas | entrantes (calculado) |
|---|---|---|---|
| 2024-11 | 7 | 58 | 65 |
| 2024-12 | 5 | 56 | 61 |
| 2025-01 | 7 | 46 | 53 |
| 2025-02 | 4 | 58 | 62 |
| 2025-03 | 8 | 48 | 56 |
| 2025-04 | 14 | 63 | 77 |
| 2025-05 | 18 | 52 | 70 |
| 2025-06 | 15 | 49 | 64 |
| 2025-07 | 10 | 63 | 73 |
| 2025-08 | 10 | 51 | 61 |
| 2025-09 | 11 | 65 | 76 |
| 2025-10 | 4 | 57 | 61 |
| 2025-11 | 4 | 48 | 52 |
| 2025-12 | 6 | 41 | 47 |
| 2026-01 | 12 | 53 | 65 |
| 2026-02 | 5 | 49 | 54 |
| 2026-03 | 11 | 89 | 100 |
| 2026-04 | 10 | 81 | 91 |
| 2026-05 | 9 | 68 | 77 |
| 2026-06 | 5 | 52 | 57 |
| 2026-07 | 7 | 84 | 91 |
| 2026-08 | 8 | 80 | 88 |
| 2026-09 | 43 | 30 | 73 |
| 2026-10 | 49 | 8 | 57 |
| 2026-11 | 2 | 0 | 2 |

**eco transesofágico adulto**:

| mês | abertas | agendadas | entrantes (calculado) |
|---|---|---|---|
| 2024-11 | 3 | 98 | 101 |
| 2024-12 | 6 | 84 | 90 |
| 2025-01 | 5 | 111 | 116 |
| 2025-02 | 8 | 94 | 102 |
| 2025-03 | 4 | 76 | 80 |
| 2025-04 | 2 | 87 | 89 |
| 2025-05 | 4 | 102 | 106 |
| 2025-06 | 6 | 76 | 82 |
| 2025-07 | 3 | 77 | 80 |
| 2025-08 | 8 | 69 | 77 |
| 2025-09 | 9 | 94 | 103 |
| 2025-10 | 4 | 86 | 90 |
| 2025-11 | 1 | 83 | 84 |
| 2025-12 | 3 | 76 | 79 |
| 2026-01 | 7 | 77 | 84 |
| 2026-02 | 3 | 93 | 96 |
| 2026-03 | 8 | 84 | 92 |
| 2026-04 | 28 | 78 | 106 |
| 2026-05 | 22 | 83 | 105 |
| 2026-06 | 17 | 84 | 101 |
| 2026-07 | 9 | 105 | 114 |
| 2026-08 | 23 | 132 | 155 |
| 2026-09 | 22 | 122 | 144 |
| 2026-10 | 28 | 114 | 142 |
| 2026-11 | 3 | 4 | 7 |

## Oferta por mês do agendamento

Agendamentos pelo mês em que acontecem, em todas as situações; realizados e faltas pela situação do agendamento. Os meses depois da solicitação mais recente são o que já está marcado, e o mês dela está incompleto. Falta = faltas ÷ (realizados + faltas).

**eco adulto**:

| mês | agendamentos | realizados | faltas | falta (calculado) |
|---|---|---|---|---|
| 2024-11 | 2.597 | 1.826 | 594 | 25% |
| 2024-12 | 2.462 | 1.655 | 640 | 28% |
| 2025-01 | 3.067 | 2.071 | 784 | 27% |
| 2025-02 | 3.091 | 2.091 | 743 | 26% |
| 2025-03 | 2.599 | 1.828 | 673 | 27% |
| 2025-04 | 2.532 | 1.774 | 633 | 26% |
| 2025-05 | 2.789 | 1.947 | 722 | 27% |
| 2025-06 | 2.697 | 1.862 | 712 | 28% |
| 2025-07 | 2.978 | 1.979 | 875 | 31% |
| 2025-08 | 2.648 | 1.718 | 732 | 30% |
| 2025-09 | 2.792 | 1.860 | 829 | 31% |
| 2025-10 | 2.727 | 1.754 | 859 | 33% |
| 2025-11 | 2.725 | 1.919 | 717 | 27% |
| 2025-12 | 2.648 | 1.701 | 805 | 32% |
| 2026-01 | 2.739 | 1.706 | 885 | 34% |
| 2026-02 | 2.673 | 1.881 | 644 | 26% |
| 2026-03 | 2.935 | 1.907 | 871 | 31% |
| 2026-04 | 2.591 | 1.775 | 607 | 25% |
| 2026-05 | 2.927 | 2.117 | 634 | 23% |
| 2026-06 | 2.881 | 2.227 | 552 | 20% |
| 2026-07 | 3.022 | 2.194 | 711 | 24% |
| 2026-08 | 2.868 | 2.058 | 685 | 25% |
| 2026-09 | 3.026 | 2.163 | 675 | 24% |
| 2026-10 | 2.807 | 1.747 | 588 | 25% |
| 2026-11 | 1.987 | 25 | 1 | 4% |

**eco infantil**:

| mês | agendamentos | realizados | faltas | falta (calculado) |
|---|---|---|---|---|
| 2024-11 | 554 | 339 | 74 | 18% |
| 2024-12 | 449 | 268 | 52 | 16% |
| 2025-01 | 514 | 393 | 37 | 9% |
| 2025-02 | 502 | 344 | 58 | 14% |
| 2025-03 | 489 | 356 | 67 | 16% |
| 2025-04 | 507 | 351 | 49 | 12% |
| 2025-05 | 517 | 374 | 69 | 16% |
| 2025-06 | 497 | 366 | 65 | 15% |
| 2025-07 | 514 | 352 | 91 | 21% |
| 2025-08 | 487 | 371 | 56 | 13% |
| 2025-09 | 465 | 333 | 78 | 19% |
| 2025-10 | 457 | 338 | 61 | 15% |
| 2025-11 | 422 | 314 | 45 | 13% |
| 2025-12 | 391 | 255 | 56 | 18% |
| 2026-01 | 469 | 311 | 98 | 24% |
| 2026-02 | 377 | 273 | 80 | 23% |
| 2026-03 | 555 | 370 | 134 | 27% |
| 2026-04 | 500 | 359 | 69 | 16% |
| 2026-05 | 518 | 368 | 79 | 18% |
| 2026-06 | 530 | 407 | 62 | 13% |
| 2026-07 | 412 | 280 | 50 | 15% |
| 2026-08 | 556 | 336 | 97 | 22% |
| 2026-09 | 625 | 471 | 64 | 12% |
| 2026-10 | 492 | 289 | 56 | 16% |
| 2026-11 | 416 | 8 | 0 | 0% |
| 2026-12 | 11 | 0 | 0 | — |

**eco fetal**:

| mês | agendamentos | realizados | faltas | falta (calculado) |
|---|---|---|---|---|
| 2024-11 | 37 | 26 | 9 | 26% |
| 2024-12 | 42 | 25 | 6 | 19% |
| 2025-01 | 45 | 32 | 9 | 22% |
| 2025-02 | 37 | 27 | 6 | 18% |
| 2025-03 | 36 | 31 | 2 | 6% |
| 2025-04 | 76 | 40 | 15 | 27% |
| 2025-05 | 76 | 57 | 11 | 16% |
| 2025-06 | 73 | 43 | 10 | 19% |
| 2025-07 | 53 | 34 | 11 | 24% |
| 2025-08 | 77 | 54 | 12 | 18% |
| 2025-09 | 75 | 53 | 14 | 21% |
| 2025-10 | 75 | 44 | 25 | 36% |
| 2025-11 | 68 | 27 | 12 | 31% |
| 2025-12 | 62 | 28 | 5 | 15% |
| 2026-01 | 76 | 46 | 18 | 28% |
| 2026-02 | 42 | 24 | 16 | 40% |
| 2026-03 | 80 | 47 | 21 | 31% |
| 2026-04 | 87 | 42 | 24 | 36% |
| 2026-05 | 76 | 47 | 14 | 23% |
| 2026-06 | 27 | 17 | 7 | 29% |
| 2026-07 | 64 | 43 | 9 | 17% |
| 2026-08 | 61 | 42 | 9 | 18% |
| 2026-09 | 79 | 40 | 17 | 30% |
| 2026-10 | 64 | 42 | 12 | 22% |
| 2026-11 | 61 | 1 | 0 | 0% |
| 2026-12 | 3 | 0 | 0 | — |

**eco de estresse**:

| mês | agendamentos | realizados | faltas | falta (calculado) |
|---|---|---|---|---|
| 2024-11 | 52 | 30 | 19 | 39% |
| 2024-12 | 53 | 24 | 25 | 51% |
| 2025-01 | 54 | 24 | 26 | 52% |
| 2025-02 | 56 | 35 | 17 | 33% |
| 2025-03 | 58 | 29 | 21 | 42% |
| 2025-04 | 60 | 30 | 25 | 45% |
| 2025-05 | 61 | 34 | 22 | 39% |
| 2025-06 | 64 | 37 | 21 | 36% |
| 2025-07 | 71 | 39 | 25 | 39% |
| 2025-08 | 64 | 32 | 25 | 44% |
| 2025-09 | 71 | 31 | 30 | 49% |
| 2025-10 | 58 | 34 | 21 | 38% |
| 2025-11 | 61 | 30 | 24 | 44% |
| 2025-12 | 63 | 25 | 33 | 57% |
| 2026-01 | 55 | 27 | 28 | 51% |
| 2026-02 | 55 | 19 | 34 | 64% |
| 2026-03 | 60 | 20 | 33 | 62% |
| 2026-04 | 61 | 34 | 22 | 39% |
| 2026-05 | 63 | 37 | 21 | 36% |
| 2026-06 | 67 | 32 | 28 | 47% |
| 2026-07 | 75 | 40 | 26 | 39% |
| 2026-08 | 70 | 31 | 29 | 48% |
| 2026-09 | 64 | 35 | 23 | 40% |
| 2026-10 | 69 | 26 | 30 | 54% |
| 2026-11 | 54 | 0 | 0 | — |
| 2026-12 | 54 | 0 | 0 | — |

**eco transesofágico adulto**:

| mês | agendamentos | realizados | faltas | falta (calculado) |
|---|---|---|---|---|
| 2024-11 | 90 | 43 | 38 | 47% |
| 2024-12 | 94 | 33 | 50 | 60% |
| 2025-01 | 105 | 48 | 50 | 51% |
| 2025-02 | 102 | 42 | 45 | 52% |
| 2025-03 | 90 | 47 | 41 | 47% |
| 2025-04 | 96 | 39 | 51 | 57% |
| 2025-05 | 86 | 39 | 41 | 51% |
| 2025-06 | 86 | 40 | 33 | 45% |
| 2025-07 | 91 | 39 | 46 | 54% |
| 2025-08 | 82 | 37 | 41 | 53% |
| 2025-09 | 89 | 45 | 34 | 43% |
| 2025-10 | 87 | 41 | 40 | 49% |
| 2025-11 | 70 | 19 | 46 | 71% |
| 2025-12 | 68 | 25 | 39 | 61% |
| 2026-01 | 72 | 30 | 38 | 56% |
| 2026-02 | 81 | 40 | 34 | 46% |
| 2026-03 | 93 | 22 | 58 | 72% |
| 2026-04 | 85 | 36 | 42 | 54% |
| 2026-05 | 94 | 44 | 46 | 51% |
| 2026-06 | 103 | 55 | 40 | 42% |
| 2026-07 | 110 | 61 | 48 | 44% |
| 2026-08 | 123 | 73 | 44 | 38% |
| 2026-09 | 116 | 69 | 40 | 37% |
| 2026-10 | 119 | 41 | 46 | 53% |
| 2026-11 | 43 | 0 | 0 | — |

## Situação dos agendamentos em 12 meses

**eco adulto**:

| situação | agendamentos | parte (calculado) |
|---|---|---|
| PROCEDIMENTO REALIZADO | 23.395 | 69% |
| PROCEDIMENTO NÃO REALIZADO POR FALTA DO PACIENTE | 8.374 | 25% |
| PROCEDIMENTO AGENDADO PENDENTE DE CONFIRMAÇÃO | 913 | 3% |
| PROCEDIMENTO CANCELADO PELA REGULAÇÃO | 715 | 2% |
| PROCEDIMENTO CANCELADO PELO SOLICITANTE | 351 | 1% |
| PROCEDIMENTO AGENDADO PELA UND. SOLICITANTE | 86 | 0% |
| AGENDAMENTO CANCELADO PELO COORD. DA REGULAÇÃO LOCAL | 8 | 0% |
| total | 33.842 | 100% |

**eco infantil**:

| situação | agendamentos | parte (calculado) |
|---|---|---|
| PROCEDIMENTO REALIZADO | 4.033 | 69% |
| PROCEDIMENTO NÃO REALIZADO POR FALTA DO PACIENTE | 890 | 15% |
| PROCEDIMENTO AGENDADO PENDENTE DE CONFIRMAÇÃO | 796 | 14% |
| PROCEDIMENTO CANCELADO PELA REGULAÇÃO | 85 | 1% |
| PROCEDIMENTO CANCELADO PELO SOLICITANTE | 40 | 1% |
| AGENDAMENTO CANCELADO PELO COORD. DA REGULAÇÃO LOCAL | 3 | 0% |
| total | 5.847 | 100% |

**eco fetal**:

| situação | agendamentos | parte (calculado) |
|---|---|---|
| PROCEDIMENTO REALIZADO | 445 | 57% |
| PROCEDIMENTO NÃO REALIZADO POR FALTA DO PACIENTE | 164 | 21% |
| PROCEDIMENTO AGENDADO PENDENTE DE CONFIRMAÇÃO | 124 | 16% |
| PROCEDIMENTO CANCELADO PELA REGULAÇÃO | 46 | 6% |
| PROCEDIMENTO CANCELADO PELO SOLICITANTE | 7 | 1% |
| total | 786 | 100% |

**eco de estresse**:

| situação | agendamentos | parte (calculado) |
|---|---|---|
| PROCEDIMENTO REALIZADO | 356 | 47% |
| PROCEDIMENTO NÃO REALIZADO POR FALTA DO PACIENTE | 331 | 43% |
| PROCEDIMENTO CANCELADO PELA REGULAÇÃO | 67 | 9% |
| PROCEDIMENTO CANCELADO PELO SOLICITANTE | 9 | 1% |
| total | 763 | 100% |

**eco transesofágico adulto**:

| situação | agendamentos | parte (calculado) |
|---|---|---|
| PROCEDIMENTO NÃO REALIZADO POR FALTA DO PACIENTE | 521 | 46% |
| PROCEDIMENTO REALIZADO | 515 | 45% |
| PROCEDIMENTO CANCELADO PELA REGULAÇÃO | 42 | 4% |
| PROCEDIMENTO AGENDADO PENDENTE DE CONFIRMAÇÃO | 29 | 3% |
| PROCEDIMENTO CANCELADO PELO SOLICITANTE | 25 | 2% |
| PROCEDIMENTO AGENDADO PELA UND. SOLICITANTE | 2 | 0% |
| total | 1.134 | 100% |

## Nomes internos

O nome pedido na ordem e o nome exato do motor, com o invisível à mostra ({NBSP} é o espaço não separável). O JSON guarda o exato.

| pedido | exato |
|---|---|
| 1. ECOCARDIOGRAFIA BI-DIMENSIONAL COM DOPPLER ADULTO | 1. ECOCARDIOGRAFIA BI-DIMENSIONAL COM DOPPLER ADULTO |
| 2. ECOCARDIOGRAFIA BI-DIMENSIONAL COM DOPPLER INFANTIL | 2. ECOCARDIOGRAFIA BI-DIMENSIONAL COM DOPPLER INFANTIL |
| 9. ECOCARDIOGRAFIA FETAL | 9. ECOCARDIOGRAFIA FETAL |
| 5. ECOCARDIOGRAFIA DE ESTRESSE ADULTO | 5. ECOCARDIOGRAFIA DE ESTRESSE ADULTO |
| 7. ECOCARDIOGRAFIA TRANSEOFAGICA ADULTO | 7. ECOCARDIOGRAFIA TRANSEOFAGICA ADULTO |

## Diferença para a coleta anterior

Contra `dados/fontes/mapa_social_20261104_panorama_bruto/coleta_20261104.json` (recarga 04/11/2026 14:33:58). Diferença **calculada** no montador.

A coleta anterior não tem as mesmas filas nem os mesmos objetos.
