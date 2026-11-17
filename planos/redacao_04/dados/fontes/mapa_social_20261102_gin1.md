# Mapa Social da Saúde — fila de Ultrassonografia transvaginal (02.05.02.018-6), coleta de 02/11/2026

Ordem de coleta: Quantos pedidos da fila de transvaginal têm um dos 37 CID da OCI GIN1 (09.06.01.001-2) que o IEV executa no convênio 030977 — para aplicar a regra um pedido, um plano.

Coleta montada por `ferramentas/montar_coleta.py` a partir da saída do kit do motor: o modelo não escreveu número nenhum, e o resumo não se edita à mão (conferência K). A decisão de cada fila vem do enquadramento do plano.

| campo | conteúdo |
|---|---|
| Fonte | Mapa Social da Saúde – Regulamentação (MPDFT) · Lista de Espera – Exames e Consultas · `https://paineis-ext.mpdft.mp.br/extensions/mapasauderegulamentacao/mapasauderegulamentacao.html` · app Qlik `7edb02fa-f1f5-4ea6-b348-049a4ac2d095` · dados SISREG/DATASUS |
| Última recarga da base | 02/11/2026 12:31:57 (qLastReloadTime 2026-11-02T15:31:57.837Z) |
| Consulta | 02/11/2026 12:50:07 a 12:50:18 (relógio do motor), sem recarga no meio |
| Solicitação mais recente na base | 28/10/2026 (agendamento mais distante: 04/02/2027) |
| Medida | **fila** = os três status: pendente de regulação, corrigida e reenviada para regulação, pendente de regulação por fila de espera. Devolvidas para complementação ficam fora e são contadas à parte |
| Fila viva | só as solicitações a partir de `data_solicitacao={">=28/10/2024"}` (24 meses contados da solicitação mais recente) |
| Agendadas em 12 meses | `data_agendamento={">=28/10/2025<=27/10/2026"}`, todos os status |
| Ordem | medicao; `ordem.json` (hash 3270919603) |
| Via | kit do motor `ferramentas/mapa_social/motor.js` (versão 2026-10-27, assinatura 2089625745); saída pela área de transferência, 1 parte(s) conferidas por hash (`ferramentas/ler_motor.py`) |

Pessoas = CNS distintos no conjunto (quem espera por mais de um exame conta uma vez); só a contagem sai do motor. Espera em dias, calculada no motor sobre os registros do conjunto.

## Alarmes

Limites de `ferramentas/conferir_coleta.py`: 30% (CID dominante), 5% (CID raro), 30% (fila velha), 3 anos (estoque), 20 categorias (CID largo).

- **fila velha**: ECOGRAFIA TRANSVAGINAL: 3.595 de 9.294 pedidos de antes da janela
- **fila velha**: USG TRANSVAGINAL: 1 de 1 pedidos de antes da janela

## Lacunas

nenhuma

## Exames

A união das filas de cada exame, na idade e no sexo da ordem, quando ela os dá.

| exame | filas | fila | fila viva | pessoas | pessoas viva | devolvidas | espera média | espera mediana |
|---|---|---|---|---|---|---|---|---|
| Ultrassonografia transvaginal (02.05.02.018-6) | 2 | 9.277 | 5.689 | **9.276** | 5.688 | 8.923 | 658,8 | 528,1 |

## Filas do objeto

As filas de partida da ordem, pelo nome exato do motor, sem recorte de CID. Anos de estoque = fila ÷ agendadas em 12 meses (**calculado** no montador).

| fila | código | objeto | papel | fila | fila viva | pessoas | devolvidas | espera média | espera mediana | espera máxima | pedido mais antigo | agendadas 12 m | anos de estoque | CID principais |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ECOGRAFIA TRANSVAGINAL | 02.05.02.018-6 | 02.05.02.018-6 | exame | 9.294 | 5.699 | 9.293 | 8.953 | 658,7 | 528,1 | 5.893,5 | 14/09/2010 | 18.028 | 0,5 | — |
| USG TRANSVAGINAL | 02.05.02.018-6 | 02.05.02.018-6 | exame | 1 | 0 | 1 | 0 | 3.969,1 | 3.969,1 | 3.969,1 | 21/12/2015 | — | — | — |

**Por recorte de CID**, em pedidos:

| fila | recorte | fila | fila viva | parte da fila (calculado) | CID principais no recorte |
|---|---|---|---|---|---|
| ECOGRAFIA TRANSVAGINAL | CID da OCI GIN1 09.06.01.001-2 (IEV) | 3.068 | 2.162 | 33% | N95 1.210, D25 387, N93 365, N92 213, N80 165 |
| USG TRANSVAGINAL | CID da OCI GIN1 09.06.01.001-2 (IEV) | 0 | 0 | 0% | — |

## Varredura das filas

Toda fila que a varredura achou, pelo código, pelo nome e, na OCI, pelo CID aceito e pelo da finalidade, nas tabelas de solicitações e de agendamentos. A decisão é a do enquadramento do plano; fila sem decisão sai **a decidir** e não entra na soma.

| fila | código | tabela | achada por | objeto | fila | fila viva | pessoas | devolvidas | espera média | pedido mais antigo | agendadas 12 m | CID principais | no CID do objeto | parte no CID aceito (calculado) | decisão | motivo |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ECOGRAFIA TRANSVAGINAL | 02.05.02.018-6 | solicitações | código, nome | 02.05.02.018-6 | 9.294 | 5.699 | 9.293 | 8.953 | 658,7 | 14/09/2010 | 18.028 | Z01 2.704, N95 1.210, R10 711, Z12 690, Z00 592 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ECOGRAFIA TRANSVAGINAL COM DOPPLER | 02.05.01.004-0 | solicitações | nome | 02.05.02.018-6 | 133 | 89 | 133 | 151 | 562,8 | 05/01/2023 | 140 | Z01 21, N95 17, R10 14, Z12 10, D25 7 | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| USG TRANSVAGINAL | 02.05.02.018-6 | solicitações | código, nome | 02.05.02.018-6 | 1 | 0 | 1 | 0 | 3.969,1 | 21/12/2015 | — | Z00 1 | — | — | a decidir | fila de partida da ordem, sem decisao no enquadramento |
| ULTRA-SONOGRAFIA TRANSVAGINAL | 02.05.02.018-6 | solicitações | código | 02.05.02.018-6 | 0 | 0 | 0 | 2 | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRASSONOGRAFIA TRANSVAGINAL | 02.05.02.018-6 | solicitações | código | 02.05.02.018-6 | 0 | 0 | 0 | 1 | — | — | — | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA TRANSVAGINAL COM DOPPLER | 02.05.02.015-1 | só agendamentos | nome | 02.05.02.018-6 | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA TRANSVAGINAL COM DOPPLER EMERGENCIA | 02.05.01.004-0 | só agendamentos | nome | 02.05.02.018-6 | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ECOGRAFIA TRANSVAGINAL EMERGENCIA | 02.05.02.018-6 | só agendamentos | código, nome | 02.05.02.018-6 | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |
| ULTRASONOGRAFIA TRANSVAGINAL COM PREPARO INTESTINAL | 02.05.02.018-6 | só agendamentos | código | 02.05.02.018-6 | — | — | — | — | — | — | 0 | — | — | — | a decidir | achada pela varredura, sem decisao no enquadramento |

## Região de Saúde

Região de Saúde: não pedida na ordem.

## CID principais

**02.05.02.018-6**:

| CID | fila | pessoas |
|---|---|---|
| Z01 | 2.699 | 2.699 |
| N95 | 1.209 | 1.209 |
| R10 | 710 | 710 |
| Z12 | 690 | 690 |
| Z00 | 592 | 592 |
| D25 | 384 | 384 |
| N93 | 364 | 364 |
| Z30 | 300 | 300 |
| N92 | 212 | 212 |
| Z10 | 202 | 202 |
| Z97 | 185 | 185 |
| N80 | 165 | 165 |
| E28 | 148 | 148 |
| N83 | 142 | 142 |
| N94 | 139 | 139 |
| N91 | 100 | 100 |
| N84 | 100 | 100 |
| N81 | 88 | 88 |
| R32 | 84 | 84 |
| Z13 | 80 | 80 |

## Por ano da solicitação

**02.05.02.018-6**:

| ano | fila | fila viva |
|---|---|---|
| 2010 | 2 | 0 |
| 2015 | 1 | 0 |
| 2019 | 2 | 0 |
| 2021 | 677 | 0 |
| 2022 | 428 | 0 |
| 2023 | 1.184 | 0 |
| 2024 | 1.549 | 255 |
| 2025 | 1.744 | 1.744 |
| 2026 | 3.690 | 3.690 |

## Nomes internos

O nome pedido na ordem e o nome exato do motor, com o invisível à mostra ({NBSP} é o espaço não separável). O JSON guarda o exato.

| pedido | exato |
|---|---|
| ECOGRAFIA TRANSVAGINAL | ECOGRAFIA TRANSVAGINAL |
| USG TRANSVAGINAL | USG TRANSVAGINAL |

## Diferença para a coleta anterior

Contra `dados/fontes/mapa_social_20261102_imagem_bruto/coleta_20261102.json` (recarga 02/11/2026 10:31:47). Diferença **calculada** no montador.

A coleta anterior não tem as mesmas filas nem os mesmos objetos.
