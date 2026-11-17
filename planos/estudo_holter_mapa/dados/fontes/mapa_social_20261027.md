# Mapa Social da Saúde — fila de Holter 24 horas (02.11.02.004-4); Monitorização ambulatorial de pressão arterial (MAPA) (02.11.02.005-2), coleta de 27/10/2026

Ordem de coleta: Estudo das filas de Holter 24 h e MAPA como exames avulsos, sem plano: região, idade, CID, ano, entrantes, oferta e situação, com a varredura das filas dos dois códigos

Coleta montada por `ferramentas/montar_coleta.py` a partir da saída do kit do motor: o modelo não escreveu número nenhum, e o resumo não se edita à mão (conferência K). A decisão de cada fila vem do enquadramento do plano.

| campo | conteúdo |
|---|---|
| Fonte | Mapa Social da Saúde – Regulamentação (MPDFT) · Lista de Espera – Exames e Consultas · `https://paineis-ext.mpdft.mp.br/extensions/mapasauderegulamentacao/mapasauderegulamentacao.html` · app Qlik `7edb02fa-f1f5-4ea6-b348-049a4ac2d095` · dados SISREG/DATASUS |
| Última recarga da base | 27/10/2026 18:32:22 (qLastReloadTime 2026-10-27T21:32:22.176Z) |
| Consulta | 27/10/2026 20:00:51 a 20:01:28 (relógio do motor), sem recarga no meio |
| Solicitação mais recente na base | 27/10/2026 (agendamento mais distante: 27/01/2027) |
| Medida | **fila** = os três status: pendente de regulação, corrigida e reenviada para regulação, pendente de regulação por fila de espera. Devolvidas para complementação ficam fora e são contadas à parte |
| Fila viva | só as solicitações a partir de `data_solicitacao={">=27/10/2024"}` (24 meses contados da solicitação mais recente) |
| Agendadas em 12 meses | `data_agendamento={">=27/10/2025<=26/10/2026"}`, todos os status |
| Ordem | medicao; `ordem.json` (hash 2571610543) |
| Via | kit do motor `ferramentas/mapa_social/motor.js` (versão 2026-10-27, assinatura 1939648169); saída pela área de transferência, 1 parte(s) conferidas por hash (`ferramentas/ler_motor.py`) |

Pessoas = CNS distintos no conjunto (quem espera por mais de um exame conta uma vez); só a contagem sai do motor. Espera em dias, calculada no motor sobre os registros do conjunto.

## Alarmes

Limites de `ferramentas/conferir_coleta.py`: 30% (CID dominante), 5% (CID raro), 30% (fila velha), 3 anos (estoque), 20 categorias (CID largo).

- **estoque**: HOLTER 24 HORAS: 36.198 na fila, 13,1 anos de agendamentos
- **fila velha**: HOLTER 24 HORAS: 25.089 de 36.198 pedidos de antes da janela
- **estoque**: MONITORIZACAO AMBULATORIAL DE PRESSAO ARTERIAL: 12.678 na fila, 4,9 anos de agendamentos
- **fila velha**: MONITORIZACAO AMBULATORIAL DE PRESSAO ARTERIAL: 6.433 de 12.678 pedidos de antes da janela

## Lacunas

nenhuma

## Exames

A união das filas de cada exame, na idade e no sexo da ordem, quando ela os dá.

| exame | filas | fila | fila viva | pessoas | pessoas viva | devolvidas | espera média | espera mediana |
|---|---|---|---|---|---|---|---|---|
| Holter 24 horas (02.11.02.004-4) | 1 | 36.198 | 11.109 | **36.167** | 11.108 | 3.493 | 1.321,2 | 1.203,3 |
| Monitorização ambulatorial de pressão arterial (MAPA) (02.11.02.005-2) | 1 | 12.678 | 6.245 | **12.670** | 6.243 | 1.412 | 1.008,5 | 761,3 |

## Filas do objeto

As filas de partida da ordem, pelo nome exato do motor, sem recorte de CID. Anos de estoque = fila ÷ agendadas em 12 meses (**calculado** no montador).

| fila | código | objeto | papel | fila | fila viva | pessoas | devolvidas | espera média | espera mediana | espera máxima | pedido mais antigo | agendadas 12 m | anos de estoque | CID principais |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| HOLTER 24 HORAS | 02.11.02.004-4 | 02.11.02.004-4 | exame (genérica) | 36.198 | 11.109 | 36.167 | 3.493 | 1.321,2 | 1.203,3 | 5.174,1 | 27/08/2012 | 2.756 | 13,1 | — |
| MONITORIZACAO AMBULATORIAL DE PRESSAO ARTERIAL | 02.11.02.005-2 | 02.11.02.005-2 | exame | 12.678 | 6.245 | 12.670 | 1.412 | 1.008,5 | 761,3 | 4.243,3 | 16/03/2015 | 2.592 | 4,9 | — |

**Por recorte de CID**, em pedidos:

| fila | recorte | fila | fila viva | parte da fila (calculado) | CID principais no recorte |
|---|---|---|---|---|---|
| HOLTER 24 HORAS | arritmia e palpitação | 12.549 | 3.640 | 35% | I49 5.643, R00 4.365, I48 1.490, I47 1.051 |
| HOLTER 24 HORAS | hipertensão | 6.379 | 1.814 | 18% | I10 6.379 |
| MONITORIZACAO AMBULATORIAL DE PRESSAO ARTERIAL | hipertensão | 9.000 | 4.076 | 71% | I10 8.162, R03 553, I15 285 |

## Varredura das filas

Toda fila que a varredura achou, pelo código, pelo nome e, na OCI, pelo CID aceito e pelo da finalidade, nas tabelas de solicitações e de agendamentos. A decisão é a do enquadramento do plano; fila sem decisão sai **a decidir** e não entra na soma.

| fila | código | tabela | achada por | objeto | fila | fila viva | pessoas | devolvidas | espera média | pedido mais antigo | agendadas 12 m | CID principais | no CID do objeto | parte no CID aceito (calculado) | decisão | motivo |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| HOLTER 24 HORAS (genérica) | 02.11.02.004-4 | solicitações | código, nome, termo | 02.11.02.004-4 | 36.198 | 11.109 | 36.167 | 3.493 | 1.321,2 | 27/08/2012 | 2.756 | I10 6.379, I49 5.643, R00 4.365, I50 2.533, I64 1.896 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| MONITORIZACAO AMBULATORIAL DE PRESSAO ARTERIAL | 02.11.02.005-2 | solicitações | código, nome | 02.11.02.005-2 | 12.678 | 6.245 | 12.670 | 1.412 | 1.008,5 | 16/03/2015 | 2.592 | I10 8.162, R03 553, I50 498, I25 356, I15 285 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |

## Região de Saúde

**02.11.02.004-4**, na medida da fila (o conjunto do objeto):

| Região de Saúde | fila | pessoas |
|---|---|---|
| Região Sudoeste | 6.976 | 6.974 |
| Região Sul | 5.486 | 5.477 |
| Região Norte | 4.303 | 4.303 |
| Região Leste | 4.127 | 4.111 |
| URD | 4.020 | 4.018 |
| Contratado/Credenciado | 3.466 | 3.465 |
| Região Oeste | 2.847 | 2.847 |
| Região Centro-Sul | 2.757 | 2.757 |
| Região Central | 1.960 | 1.960 |
| Serviços Centralizados | 1 | 1 |
| sem Região de Saúde | 255 | 255 |

**02.11.02.005-2**, na medida da fila (o conjunto do objeto):

| Região de Saúde | fila | pessoas |
|---|---|---|
| Região Sudoeste | 3.860 | 3.856 |
| Região Sul | 2.623 | 2.622 |
| Região Norte | 1.327 | 1.327 |
| Região Centro-Sul | 1.325 | 1.324 |
| Região Leste | 1.226 | 1.224 |
| Contratado/Credenciado | 652 | 652 |
| Região Oeste | 644 | 644 |
| Região Central | 504 | 504 |
| URD | 449 | 449 |
| Serviços Centralizados | 1 | 1 |
| sem Região de Saúde | 67 | 67 |

## Idade na solicitação

**02.11.02.004-4**:

| faixa | fila | pessoas |
|---|---|---|
| 0 a 9 | 49 | 49 |
| 10 a 19 | 568 | 568 |
| 20 a 29 | 1.376 | 1.375 |
| 30 a 39 | 1.859 | 1.855 |
| 40 a 49 | 3.961 | 3.959 |
| 50 a 59 | 6.925 | 6.918 |
| 60 a 69 | 8.947 | 8.941 |
| 70 a 79 | 7.864 | 7.860 |
| 80 a 89 | 3.767 | 3.763 |
| 90 a 99 | 882 | 879 |

**02.11.02.005-2**:

| faixa | fila | pessoas |
|---|---|---|
| 10 a 19 | 6 | 6 |
| 20 a 29 | 365 | 365 |
| 30 a 39 | 832 | 832 |
| 40 a 49 | 1.890 | 1.890 |
| 50 a 59 | 3.008 | 3.006 |
| 60 a 69 | 3.243 | 3.241 |
| 70 a 79 | 2.372 | 2.369 |
| 80 a 89 | 817 | 817 |
| 90 a 99 | 145 | 144 |

## CID principais

**02.11.02.004-4**:

| CID | fila | pessoas |
|---|---|---|
| I10 | 6.379 | 6.375 |
| I49 | 5.643 | 5.640 |
| R00 | 4.365 | 4.361 |
| I50 | 2.533 | 2.531 |
| I64 | 1.896 | 1.895 |
| I48 | 1.490 | 1.489 |
| I25 | 1.340 | 1.340 |
| R55 | 1.310 | 1.310 |
| I20 | 1.251 | 1.251 |
| R07 | 1.069 | 1.068 |
| I47 | 1.051 | 1.051 |
| B57 | 746 | 746 |
| I63 | 596 | 596 |
| I45 | 382 | 381 |
| I44 | 342 | 342 |
| I05 | 314 | 314 |
| I42 | 258 | 258 |
| R06 | 256 | 256 |
| I21 | 235 | 235 |
| I15 | 229 | 229 |

**02.11.02.005-2**:

| CID | fila | pessoas |
|---|---|---|
| I10 | 8.162 | 8.156 |
| R03 | 553 | 553 |
| I50 | 498 | 498 |
| I25 | 356 | 355 |
| I15 | 285 | 284 |
| I20 | 264 | 264 |
| R07 | 172 | 172 |
| I49 | 156 | 156 |
| I11 | 151 | 151 |
| I64 | 144 | 144 |
| Z00 | 127 | 127 |
| R00 | 117 | 117 |
| Z13 | 109 | 109 |
| R55 | 90 | 90 |
| Z01 | 59 | 59 |
| I95 | 56 | 56 |
| I48 | 51 | 51 |
| Z95 | 49 | 49 |
| I47 | 45 | 45 |
| I21 | 43 | 43 |

## Por ano da solicitação

**02.11.02.004-4**:

| ano | fila | fila viva |
|---|---|---|
| 2012 | 66 | 0 |
| 2013 | 227 | 0 |
| 2014 | 265 | 0 |
| 2015 | 317 | 0 |
| 2016 | 488 | 0 |
| 2017 | 531 | 0 |
| 2018 | 240 | 0 |
| 2019 | 1.402 | 0 |
| 2020 | 1.978 | 0 |
| 2021 | 4.382 | 0 |
| 2022 | 5.386 | 0 |
| 2023 | 5.456 | 0 |
| 2024 | 5.220 | 869 |
| 2025 | 5.045 | 5.045 |
| 2026 | 5.195 | 5.195 |

**02.11.02.005-2**:

| ano | fila | fila viva |
|---|---|---|
| 2015 | 96 | 0 |
| 2016 | 56 | 0 |
| 2017 | 29 | 0 |
| 2018 | 95 | 0 |
| 2019 | 458 | 0 |
| 2020 | 596 | 0 |
| 2021 | 1.050 | 0 |
| 2022 | 1.885 | 0 |
| 2023 | 1.352 | 0 |
| 2024 | 1.014 | 198 |
| 2025 | 2.729 | 2.729 |
| 2026 | 3.318 | 3.318 |

## Entrantes por mês

Abertas = solicitações de todos os status pelo mês do pedido; agendadas = agendamentos pelo mês da solicitação (data do agendamento menos a espera). O último mês está incompleto.

**02.11.02.004-4**:

| mês | abertas | agendadas | entrantes (calculado) |
|---|---|---|---|
| 2024-10 | 520 | 159 | 679 |
| 2024-11 | 469 | 123 | 592 |
| 2024-12 | 333 | 131 | 464 |
| 2025-01 | 354 | 260 | 614 |
| 2025-02 | 476 | 98 | 574 |
| 2025-03 | 399 | 146 | 545 |
| 2025-04 | 430 | 105 | 535 |
| 2025-05 | 487 | 129 | 616 |
| 2025-06 | 456 | 102 | 558 |
| 2025-07 | 546 | 143 | 689 |
| 2025-08 | 473 | 111 | 584 |
| 2025-09 | 456 | 142 | 598 |
| 2025-10 | 420 | 134 | 554 |
| 2025-11 | 310 | 165 | 475 |
| 2025-12 | 299 | 131 | 430 |
| 2026-01 | 389 | 162 | 551 |
| 2026-02 | 376 | 160 | 536 |
| 2026-03 | 564 | 82 | 646 |
| 2026-04 | 525 | 27 | 552 |
| 2026-05 | 599 | 17 | 616 |
| 2026-06 | 508 | 26 | 534 |
| 2026-07 | 618 | 24 | 642 |
| 2026-08 | 582 | 20 | 602 |
| 2026-09 | 582 | 3 | 585 |
| 2026-10 | 475 | 1 | 476 |

**02.11.02.005-2**:

| mês | abertas | agendadas | entrantes (calculado) |
|---|---|---|---|
| 2024-10 | 101 | 304 | 405 |
| 2024-11 | 100 | 208 | 308 |
| 2024-12 | 96 | 196 | 292 |
| 2025-01 | 115 | 271 | 386 |
| 2025-02 | 110 | 293 | 403 |
| 2025-03 | 129 | 234 | 363 |
| 2025-04 | 120 | 237 | 357 |
| 2025-05 | 192 | 235 | 427 |
| 2025-06 | 296 | 75 | 371 |
| 2025-07 | 338 | 62 | 400 |
| 2025-08 | 321 | 85 | 406 |
| 2025-09 | 327 | 60 | 387 |
| 2025-10 | 321 | 65 | 386 |
| 2025-11 | 266 | 71 | 337 |
| 2025-12 | 229 | 48 | 277 |
| 2026-01 | 286 | 81 | 367 |
| 2026-02 | 303 | 65 | 368 |
| 2026-03 | 369 | 80 | 449 |
| 2026-04 | 323 | 79 | 402 |
| 2026-05 | 357 | 69 | 426 |
| 2026-06 | 340 | 70 | 410 |
| 2026-07 | 355 | 84 | 439 |
| 2026-08 | 379 | 58 | 437 |
| 2026-09 | 325 | 38 | 363 |
| 2026-10 | 302 | 13 | 315 |

## Oferta por mês do agendamento

Agendamentos pelo mês em que acontecem, em todas as situações; realizados e faltas pela situação do agendamento. Os meses depois da solicitação mais recente são o que já está marcado, e o mês dela está incompleto. Falta = faltas ÷ (realizados + faltas).

**02.11.02.004-4**:

| mês | agendamentos | realizados | faltas | falta (calculado) |
|---|---|---|---|---|
| 2024-10 | 106 | 49 | 34 | 41% |
| 2024-11 | 67 | 35 | 17 | 33% |
| 2024-12 | 81 | 37 | 24 | 39% |
| 2025-01 | 96 | 46 | 33 | 42% |
| 2025-02 | 90 | 38 | 33 | 46% |
| 2025-03 | 74 | 29 | 29 | 50% |
| 2025-04 | 46 | 24 | 18 | 43% |
| 2025-05 | 55 | 18 | 27 | 60% |
| 2025-06 | 43 | 23 | 17 | 42% |
| 2025-07 | 61 | 19 | 31 | 62% |
| 2025-08 | 52 | 23 | 20 | 47% |
| 2025-09 | 59 | 28 | 23 | 45% |
| 2025-10 | 101 | 42 | 47 | 53% |
| 2025-11 | 141 | 51 | 61 | 54% |
| 2025-12 | 160 | 75 | 75 | 50% |
| 2026-01 | 185 | 77 | 100 | 56% |
| 2026-02 | 209 | 97 | 89 | 48% |
| 2026-03 | 280 | 108 | 146 | 57% |
| 2026-04 | 214 | 108 | 98 | 48% |
| 2026-05 | 278 | 118 | 121 | 51% |
| 2026-06 | 273 | 111 | 118 | 52% |
| 2026-07 | 257 | 127 | 76 | 37% |
| 2026-08 | 276 | 128 | 99 | 44% |
| 2026-09 | 245 | 125 | 87 | 41% |
| 2026-10 | 255 | 73 | 49 | 40% |
| 2026-11 | 13 | 0 | 0 | — |

**02.11.02.005-2**:

| mês | agendamentos | realizados | faltas | falta (calculado) |
|---|---|---|---|---|
| 2024-10 | 241 | 133 | 75 | 36% |
| 2024-11 | 161 | 81 | 62 | 43% |
| 2024-12 | 175 | 95 | 62 | 39% |
| 2025-01 | 203 | 105 | 84 | 44% |
| 2025-02 | 167 | 92 | 53 | 37% |
| 2025-03 | 131 | 69 | 48 | 41% |
| 2025-04 | 136 | 73 | 48 | 40% |
| 2025-05 | 153 | 70 | 66 | 49% |
| 2025-06 | 148 | 83 | 48 | 37% |
| 2025-07 | 177 | 87 | 74 | 46% |
| 2025-08 | 193 | 94 | 73 | 44% |
| 2025-09 | 215 | 126 | 67 | 35% |
| 2025-10 | 216 | 107 | 92 | 46% |
| 2025-11 | 173 | 95 | 69 | 42% |
| 2025-12 | 183 | 97 | 71 | 42% |
| 2026-01 | 179 | 99 | 65 | 40% |
| 2026-02 | 176 | 101 | 61 | 38% |
| 2026-03 | 240 | 123 | 96 | 44% |
| 2026-04 | 182 | 92 | 77 | 46% |
| 2026-05 | 203 | 121 | 67 | 36% |
| 2026-06 | 200 | 113 | 65 | 37% |
| 2026-07 | 227 | 138 | 68 | 33% |
| 2026-08 | 270 | 148 | 91 | 38% |
| 2026-09 | 270 | 142 | 113 | 44% |
| 2026-10 | 285 | 95 | 38 | 29% |
| 2026-11 | 73 | 0 | 0 | — |

## Situação dos agendamentos em 12 meses

**02.11.02.004-4**:

| situação | agendamentos | parte (calculado) |
|---|---|---|
| PROCEDIMENTO REALIZADO | 1.211 | 44% |
| PROCEDIMENTO NÃO REALIZADO POR FALTA DO PACIENTE | 1.129 | 41% |
| PROCEDIMENTO CANCELADO PELA REGULAÇÃO | 225 | 8% |
| PROCEDIMENTO AGENDADO PENDENTE DE CONFIRMAÇÃO | 122 | 4% |
| PROCEDIMENTO CANCELADO PELO SOLICITANTE | 37 | 1% |
| AGENDAMENTO CANCELADO PELO COORD. DA REGULAÇÃO LOCAL | 32 | 1% |
| total | 2.756 | 100% |

**02.11.02.005-2**:

| situação | agendamentos | parte (calculado) |
|---|---|---|
| PROCEDIMENTO REALIZADO | 1.383 | 53% |
| PROCEDIMENTO NÃO REALIZADO POR FALTA DO PACIENTE | 905 | 35% |
| PROCEDIMENTO CANCELADO PELA REGULAÇÃO | 137 | 5% |
| PROCEDIMENTO AGENDADO PENDENTE DE CONFIRMAÇÃO | 135 | 5% |
| PROCEDIMENTO CANCELADO PELO SOLICITANTE | 24 | 1% |
| AGENDAMENTO CANCELADO PELO COORD. DA REGULAÇÃO LOCAL | 8 | 0% |
| total | 2.592 | 100% |

## Nomes internos

O nome pedido na ordem e o nome exato do motor, com o invisível à mostra ({NBSP} é o espaço não separável). O JSON guarda o exato.

| pedido | exato |
|---|---|
| HOLTER 24 HORAS | HOLTER 24 HORAS |
| MONITORIZACAO AMBULATORIAL DE PRESSAO ARTERIAL | MONITORIZACAO AMBULATORIAL DE PRESSAO ARTERIAL |

## Diferença para a coleta anterior

Sem coleta anterior na pasta.
