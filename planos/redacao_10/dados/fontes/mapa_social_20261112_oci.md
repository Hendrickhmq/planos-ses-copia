# Mapa Social da Saúde — fila de OCI 09.01.01.008-1 (OCI AVALIAÇÃO DIAGNÓSTICA DE CÂNCER COLORRETAL), coleta de 12/11/2026

Ordem de coleta: pré-plano da OCI de câncer colorretal (09.01.01.008-1) do ISHP: quanto da fila de colonoscopia tem CID compatível com a OCI

Coleta montada por `ferramentas/montar_coleta.py` a partir da saída do kit do motor: o modelo não escreveu número nenhum, e o resumo não se edita à mão (conferência K). A decisão de cada fila vem do enquadramento do plano.

| campo | conteúdo |
|---|---|
| Fonte | Mapa Social da Saúde – Regulamentação (MPDFT) · Lista de Espera – Exames e Consultas · `https://paineis-ext.mpdft.mp.br/extensions/mapasauderegulamentacao/mapasauderegulamentacao.html` · app Qlik `7edb02fa-f1f5-4ea6-b348-049a4ac2d095` · dados SISREG/DATASUS |
| Última recarga da base | 12/11/2026 16:33:01 (qLastReloadTime 2026-11-12T19:33:01.478Z) |
| Consulta | 12/11/2026 18:23:41 a 18:24:13 (relógio do motor), sem recarga no meio |
| Solicitação mais recente na base | 12/11/2026 (agendamento mais distante: 18/02/2027) |
| Medida | **fila** = os três status: pendente de regulação, corrigida e reenviada para regulação, pendente de regulação por fila de espera. Devolvidas para complementação ficam fora e são contadas à parte |
| Fila viva | só as solicitações a partir de `data_solicitacao={">=12/11/2024"}` (24 meses contados da solicitação mais recente) |
| Agendadas em 12 meses | `data_agendamento={">=12/11/2025<=11/11/2026"}`, todos os status |
| Ordem | medicao; `ordem.json` (hash 2106312731) |
| Via | kit do motor `ferramentas/mapa_social/motor.js` (versão 2026-10-27, assinatura 1939648169); saída pela transcrição, 4 parte(s) conferidas por hash (`ferramentas/ler_motor.py`) |

Pessoas = CNS distintos no conjunto (quem espera por mais de um exame conta uma vez); só a contagem sai do motor. Espera em dias, calculada no motor sobre os registros do conjunto.

## Alarmes

Limites de `ferramentas/conferir_coleta.py`: 30% (CID dominante), 5% (CID raro), 30% (fila velha), 3 anos (estoque), 20 categorias (CID largo).

- **estoque**: COLONOSCOPIA: 22.439 na fila, 3,4 anos de agendamentos

## Lacunas

nenhuma

## Os três números

Em pessoas, na idade e no sexo da ficha. A finalidade é a fila da OCI; o teto fica como referência e nunca vai ao dossiê nem à justificativa.

| OCI | CID aceito | CID da finalidade | teto | teto viva | finalidade | finalidade viva | núcleo | núcleo viva | espera média (finalidade) |
|---|---|---|---|---|---|---|---|---|---|
| 09.01.01.008-1 | `codigo_cid_solicitado={"C17*","C18*","C19*","C20*","C21*","D01*","D12*","K62*","K63*"}` | `codigo_cid_solicitado={"C18*","C19*","C20*"}` | 4.025 | 3.600 | **1.477** | 1.328 | 1.477 | 1.328 | 437,3 |

- **09.01.01.008-1** (OCI AVALIAÇÃO DIAGNÓSTICA DE CÂNCER COLORRETAL): ficha `dados/fontes/sigtap_0901010081_112026.md`; idade 10 a 130 anos, sexo ambos. Na idade e no sexo da ficha ficam 1.477 das 1.477 pessoas da finalidade. Núcleo: o unico exame obrigatorio com fila (COLONOSCOPIA). Fila (pedidos) na finalidade: 1.477 (1.328 na viva), devolvidas 355, espera mediana 456,9 dias.

## Filas do objeto

As filas de partida da ordem, pelo nome exato do motor, sem recorte de CID. Anos de estoque = fila ÷ agendadas em 12 meses (**calculado** no montador).

| fila | código | objeto | papel | fila | fila viva | pessoas | devolvidas | espera média | espera mediana | espera máxima | pedido mais antigo | agendadas 12 m | anos de estoque | CID principais |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| COLONOSCOPIA | 02.09.01.002-9 | 09.01.01.008-1 | exame, obrigatório | 22.439 | 19.742 | 22.439 | 4.017 | 417,3 | 416,3 | 1.904,0 | 26/08/2021 | 6.510 | 3,4 | C18 1.231, K63 1.027, K62 985, D12 469, C20 231 |

**Por recorte de CID**, em pedidos:

| fila | recorte | fila | fila viva | parte da fila (calculado) | CID principais no recorte |
|---|---|---|---|---|---|
| COLONOSCOPIA | teto 09.01.01.008-1 | 4.025 | 3.600 | 18% | C18 1.231, K63 1.027, K62 985, D12 469, C20 231 |
| COLONOSCOPIA | finalidade 09.01.01.008-1 | 1.477 | 1.328 | 7% | C18 1.231, C20 231, C19 15 |

## Varredura das filas

Toda fila que a varredura achou, pelo código, pelo nome e, na OCI, pelo CID aceito e pelo da finalidade, nas tabelas de solicitações e de agendamentos. A decisão é a do enquadramento do plano; fila sem decisão sai **a decidir** e não entra na soma.

| fila | código | tabela | achada por | objeto | fila | fila viva | pessoas | devolvidas | espera média | pedido mais antigo | agendadas 12 m | CID principais | no CID do objeto | parte no CID aceito (calculado) | decisão | motivo |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| COLONOSCOPIA | 02.09.01.002-9 | solicitações | CID aceito, CID da finalidade, código, nome | 09.01.01.008-1 | 22.439 | 19.742 | 22.439 | 4.017 | 417,3 | 26/08/2021 | 6.510 | Z12 6.109, K92 2.821, K59 1.443, R19 1.413, C18 1.231 | 09.01.01.008-1 cid aceito 4.025; 09.01.01.008-1 cid finalidade 1.477 | 18% | entra | na fila, só a colonoscopia, 22.439 (usuário, 12/11/2026) |
| CONSULTA EM PROCTOLOGIA - GERAL (genérica) | 03.01.01.007-2 | solicitações | CID aceito, CID da finalidade | 09.01.01.008-1 | 8.390 | 5.155 | 8.375 | 3.936 | 637,8 | 14/12/2018 | 4.040 | I84 3.418, K60 663, K62 601, L05 477, K59 408 | 09.01.01.008-1 cid aceito 1.080; 09.01.01.008-1 cid finalidade 86 | 13% | a decidir | achada pela varredura, sem decisao no enquadramento |
| 063. TC DO ABDOMEN SUPERIOR ADULTO C/CONTRASTE S/SEDACAO | 02.06.03.001-0 | solicitações | CID aceito, CID da finalidade | 09.01.01.008-1 | 3.345 | 3.331 | 3.345 | 5.262 | 105,1 | 05/07/2024 | 8.253 | C50 606, C18 301, R10 277, C20 117, C16 115 | 09.01.01.008-1 cid aceito 470; 09.01.01.008-1 cid finalidade 428 | 14% | a decidir | achada pela varredura, sem decisao no enquadramento |
| 111. TC DE PELVE OU BACIA ADULTO C/CONTRASTE S/SEDACAO | 02.06.03.003-7 | solicitações | CID aceito, CID da finalidade | 09.01.01.008-1 | 2.946 | 2.936 | 2.946 | 3.712 | 106,2 | 05/07/2024 | 7.077 | C50 499, C18 283, R10 263, C16 110, C20 94 | 09.01.01.008-1 cid aceito 425; 09.01.01.008-1 cid finalidade 388 | 14% | a decidir | achada pela varredura, sem decisao no enquadramento |
| 055. TC DO TORAX ADULTO C/CONTRASTE S/SEDACAO | 02.06.02.003-1 | solicitações | CID aceito, CID da finalidade | 09.01.01.008-1 | 1.883 | 1.875 | 1.881 | 1.864 | 104,2 | 29/04/2024 | 6.205 | C50 431, C18 182, C20 93, C16 73, C34 70 | 09.01.01.008-1 cid aceito 315; 09.01.01.008-1 cid finalidade 284 | 17% | a decidir | achada pela varredura, sem decisao no enquadramento |
| CONSULTA EM ONCOLOGIA CLINICA | 03.01.01.007-2 | solicitações | CID aceito, CID da finalidade | 09.01.01.008-1 | 786 | 786 | 784 | 2.355 | 37,2 | 04/05/2026 | 3.827 | C50 207, C61 112, C18 72, C53 34, C20 34 | 09.01.01.008-1 cid aceito 120; 09.01.01.008-1 cid finalidade 109 | 15% | a decidir | achada pela varredura, sem decisao no enquadramento |
| CONSULTA EM ONCOGENETICA | 03.01.01.007-2 | solicitações | CID aceito, CID da finalidade | 09.01.01.008-1 | 781 | 767 | 781 | 15 | 299,5 | 04/04/2023 | 455 | C50 387, C18 86, Z80 42, C56 24, C20 20 | 09.01.01.008-1 cid aceito 113; 09.01.01.008-1 cid finalidade 108 | 14% | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC DO ABDOMEN SUPER.ADULTO C/CONTRASTE S/SEDACAO EMERG. | 02.06.03.001-0 | solicitações | CID aceito, CID da finalidade | 09.01.01.008-1 | 749 | 708 | 749 | 85 | 362,8 | 27/09/2024 | 1.518 | R10 166, C18 34, C50 33, Z54 32, K85 24 | 09.01.01.008-1 cid aceito 59; 09.01.01.008-1 cid finalidade 48 | 8% | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC DE PELVE OU BACIA ADULTO C/CONTRASTE S/SEDACAO EMERG. | 02.06.03.003-7 | solicitações | CID aceito, CID da finalidade | 09.01.01.008-1 | 693 | 657 | 693 | 68 | 356,4 | 27/09/2024 | 1.336 | R10 140, Z54 33, C18 31, C50 28, K85 19 | 09.01.01.008-1 cid aceito 52; 09.01.01.008-1 cid finalidade 44 | 8% | a decidir | achada pela varredura, sem decisao no enquadramento |
| RETOSSIGMOIDOSCOPIA FLEXÍVEL | 02.09.01.005-3 | solicitações | CID aceito, CID da finalidade | 09.01.01.008-1 | 415 | 415 | 415 | 259 | 70,3 | 28/05/2026 | 1.776 | I84 115, K62 57, K92 50, K60 42, Z12 33 | 09.01.01.008-1 cid aceito 82; 09.01.01.008-1 cid finalidade 20 | 20% | fica fora | outro procedimento (02.09.01.005-3) |
| COLONOSCOPIA C/ ANESTESIA | 02.09.01.002-9 | solicitações | CID aceito, CID da finalidade, código, nome | 09.01.01.008-1 | 386 | 330 | 386 | 449 | 295,4 | 22/01/2024 | 151 | Z12 132, K92 42, K63 26, K59 20, C18 19 | 09.01.01.008-1 cid aceito 78; 09.01.01.008-1 cid finalidade 25 | 20% | fica fora | na fila, só a colonoscopia (usuário, 12/11/2026) |
| TC DO TORAX ADULTO C/CONTRASTE S/SEDACAO EMERGENCIA | 02.06.02.003-1 | solicitações | CID aceito, CID da finalidade | 09.01.01.008-1 | 319 | 299 | 319 | 30 | 354,8 | 26/09/2024 | 982 | I26 19, C50 18, C53 15, J18 14, C34 13 | 09.01.01.008-1 cid aceito 17; 09.01.01.008-1 cid finalidade 15 | 5% | a decidir | achada pela varredura, sem decisao no enquadramento |
| TOMOGRAFIA POR EMISSÃO DE PÓSITRONS (PET-CT) | 02.06.01.009-5 | solicitações | CID aceito, CID da finalidade | 09.01.01.008-1 | 248 | 248 | 248 | 860 | 129,5 | 10/11/2025 | 824 | C85 30, C50 24, C81 21, C83 20, C18 19 | 09.01.01.008-1 cid aceito 22; 09.01.01.008-1 cid finalidade 22 | 9% | a decidir | achada pela varredura, sem decisao no enquadramento |
| CONSULTA EM RADIOTERAPIA | 03.01.01.007-2 | solicitações | CID aceito, CID da finalidade | 09.01.01.008-1 | 236 | 236 | 234 | 459 | 33,5 | 13/06/2025 | 3.458 | C50 78, C79 36, C61 25, L91 14, C20 11 | 09.01.01.008-1 cid aceito 16; 09.01.01.008-1 cid finalidade 13 | 7% | a decidir | achada pela varredura, sem decisao no enquadramento |
| 023. TC COLUNA LOMBO-SACRA ADULTO C/CONTRASTE S/SEDACAO | 02.06.01.002-8 | solicitações | CID aceito, CID da finalidade | 09.01.01.008-1 | 40 | 40 | 40 | 125 | 100,9 | 28/04/2026 | 215 | M54 12, C90 5, C61 3, C81 2, C80 1 | 09.01.01.008-1 cid aceito 2; 09.01.01.008-1 cid finalidade 2 | 5% | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC DO ABDOMEN SUPER.INFANTIL C/CONTRASTE S/SEDACAO EMERG. | 02.06.03.001-0 | solicitações | CID aceito, CID da finalidade | 09.01.01.008-1 | 34 | 33 | 34 | 1 | 349,2 | 07/11/2024 | 17 | R10 9, I88 2, A09 2, C25 2, A41 2 | 09.01.01.008-1 cid aceito 2; 09.01.01.008-1 cid finalidade 1 | 6% | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC DE PELVE OU BACIA INFANTIL C/CONTRASTE S/SEDACAO EMERG. | 02.06.03.003-7 | solicitações | CID aceito, CID da finalidade | 09.01.01.008-1 | 31 | 29 | 31 | 3 | 357,9 | 08/10/2024 | 18 | R10 6, C18 2, C34 2, R50 2, S37 1 | 09.01.01.008-1 cid aceito 3; 09.01.01.008-1 cid finalidade 2 | 10% | a decidir | achada pela varredura, sem decisao no enquadramento |
| 047. TC DE ORBITAS ADULTO C/CONTRASTE S/SEDACAO | 02.06.01.006-0 | solicitações | CID aceito, CID da finalidade | 09.01.01.008-1 | 17 | 17 | 17 | 62 | 66,5 | 21/05/2026 | 89 | H05 3, H04 3, C50 1, H53 1, C90 1 | 09.01.01.008-1 cid aceito 1; 09.01.01.008-1 cid finalidade 1 | 6% | a decidir | achada pela varredura, sem decisao no enquadramento |
| TC DE PELVE OU BACIA INFANTIL S/CONTRASTE S/SEDACAO EMERG. | 02.06.03.003-7 | solicitações | CID aceito, CID da finalidade | 09.01.01.008-1 | 15 | 15 | 15 | 1 | 473,3 | 27/12/2024 | 9 | R10 3, N20 1, Z54 1, C16 1, K56 1 | 09.01.01.008-1 cid aceito 1; 09.01.01.008-1 cid finalidade 1 | 7% | a decidir | achada pela varredura, sem decisao no enquadramento |
| IMUNOHISTOQUIMICA DE NEOPLASIAS MALIGNAS | 02.03.02.004-9 | solicitações | CID aceito, CID da finalidade | 09.01.01.008-1 | 12 | 12 | 12 | 134 | 1,5 | 10/11/2026 | 1.617 | D77 2, C44 1, D22 1, C90 1, C18 1 | 09.01.01.008-1 cid aceito 2; 09.01.01.008-1 cid finalidade 2 | 17% | a decidir | achada pela varredura, sem decisao no enquadramento |
| CONSULTA EM ONCOLOGIA CLINICA - CUIDADOS PALIATIVOS | 03.01.01.007-2 | solicitações | CID aceito, CID da finalidade | 09.01.01.008-1 | 12 | 12 | 12 | 54 | 3,4 | 04/11/2026 | 759 | C50 3, G40 1, C71 1, C78 1, C18 1 | 09.01.01.008-1 cid aceito 1; 09.01.01.008-1 cid finalidade 1 | 8% | a decidir | achada pela varredura, sem decisao no enquadramento |
| COLETA DE SANGUE PARA TRIAGEM NEONATAL | 02.01.02.005-0 | solicitações | CID aceito, CID da finalidade | 09.01.01.008-1 | 10 | 0 | 10 | 1 | 1.538,1 | 04/05/2022 | 0 | K92 2, C18 2, Z12 2, Z93 1, Z10 1 | 09.01.01.008-1 cid aceito 3; 09.01.01.008-1 cid finalidade 3 | 30% | a decidir | achada pela varredura, sem decisao no enquadramento |
| TORAX : APICO - LORDORTICA (genérica) | 02.04.03.012-9 | solicitações | CID aceito, CID da finalidade | 09.01.01.008-1 | 5 | 5 | 5 | 0 | 26,8 | 17/09/2026 | 10 | Z01 1, R07 1, C18 1, K40 1, C20 1 | 09.01.01.008-1 cid aceito 2; 09.01.01.008-1 cid finalidade 2 | 40% | a decidir | achada pela varredura, sem decisao no enquadramento |
| ACOLHIMENTO ESPECIALIZADO EM SAUDE DA MULHER | 03.01.01.004-8 | solicitações | CID aceito, CID da finalidade | 09.01.01.008-1 | 1 | 1 | 1 | 212 | 0,9 | 11/11/2026 | 331 | C18 1 | 09.01.01.008-1 cid aceito 1; 09.01.01.008-1 cid finalidade 1 | 100% | a decidir | achada pela varredura, sem decisao no enquadramento |
| 051. TC DO TORAX INFANTIL C/CONTRASTE S/SEDACAO | 02.06.02.003-1 | solicitações | CID aceito, CID da finalidade | 09.01.01.008-1 | 1 | 1 | 1 | 52 | 656,2 | 25/01/2025 | 57 | C18 1 | 09.01.01.008-1 cid aceito 1; 09.01.01.008-1 cid finalidade 1 | 100% | a decidir | achada pela varredura, sem decisao no enquadramento |
| 112. TC DE PELVE OU BACIA ADULTO C/CONTRASTE C/SEDACAO | 02.06.03.003-7 | solicitações | CID aceito, CID da finalidade | 09.01.01.008-1 | 1 | 1 | 1 | 220 | 656,2 | 25/01/2025 | 23 | C18 1 | 09.01.01.008-1 cid aceito 1; 09.01.01.008-1 cid finalidade 1 | 100% | a decidir | achada pela varredura, sem decisao no enquadramento |
| COLONOSCOPIA (COLOSCOPIA) | 02.09.01.002-9 | solicitações | código, nome | 09.01.01.008-1 | 1 | 0 | 1 | 0 | 3.398,0 | 24/07/2017 | — | Z00 1 | 09.01.01.008-1 cid aceito 0; 09.01.01.008-1 cid finalidade 0 | 0% | fica fora | na fila, só a colonoscopia (usuário, 12/11/2026) |
| COLONOSCOPIA C/ANESTESIA | 02.09.01.002-9 | solicitações | código, nome | 09.01.01.008-1 | 0 | 0 | 0 | 1 | — | — | — | — | 09.01.01.008-1 cid aceito 0; 09.01.01.008-1 cid finalidade 0 | — | a decidir | achada pela varredura, sem decisao no enquadramento |

Mais 83 filas de solicitação achadas só pelo CID, com menos de 5% dos pedidos no CID aceito do objeto (538 pedidos no CID, somados), e 104 nomes só da tabela de agendamentos achados só pelo CID: estão no JSON da coleta e na aba Varredura da planilha.

## Região de Saúde

Região de Saúde: não pedida na ordem.

## Idade na solicitação

**09.01.01.008-1**:

| faixa | fila | pessoas |
|---|---|---|
| 20 a 29 | 12 | 12 |
| 30 a 39 | 39 | 39 |
| 40 a 49 | 194 | 194 |
| 50 a 59 | 402 | 402 |
| 60 a 69 | 484 | 484 |
| 70 a 79 | 302 | 302 |
| 80 a 89 | 43 | 43 |
| 90 a 99 | 1 | 1 |

## CID principais

**09.01.01.008-1**:

| CID | fila | pessoas |
|---|---|---|
| C18 | 1.231 | 1.231 |
| C20 | 231 | 231 |
| C19 | 15 | 15 |

## Nomes internos

O nome pedido na ordem e o nome exato do motor, com o invisível à mostra ({NBSP} é o espaço não separável). O JSON guarda o exato.

| pedido | exato |
|---|---|
| COLONOSCOPIA | COLONOSCOPIA |

## Diferença para a coleta anterior

Contra `dados/fontes/mapa_social_20261112_bruto/coleta_20261112.json` (recarga 12/11/2026 16:33:01). Diferença **calculada** no montador.

A coleta anterior não tem as mesmas filas nem os mesmos objetos.
