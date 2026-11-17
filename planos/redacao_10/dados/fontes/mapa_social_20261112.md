# Mapa Social da Saúde — panorama: colonoscopia (código), colonoscopia (nome), retossigmoidoscopia, coleta de 12/11/2026

Ordem de coleta: pré-plano de colonoscopia do ISHP, R$ 11 mi: tamanho e espera da fila de colonoscopia

Coleta montada por `ferramentas/montar_coleta.py` a partir da saída do kit do motor: o modelo não escreveu número nenhum, e o resumo não se edita à mão (conferência K). A decisão de cada fila vem do enquadramento do plano.

| campo | conteúdo |
|---|---|
| Fonte | Mapa Social da Saúde – Regulamentação (MPDFT) · Lista de Espera – Exames e Consultas · `https://paineis-ext.mpdft.mp.br/extensions/mapasauderegulamentacao/mapasauderegulamentacao.html` · app Qlik `7edb02fa-f1f5-4ea6-b348-049a4ac2d095` · dados SISREG/DATASUS |
| Última recarga da base | 12/11/2026 16:33:01 (qLastReloadTime 2026-11-12T19:33:01.478Z) |
| Consulta | 12/11/2026 18:04:28 a 18:05:03 (relógio do motor), sem recarga no meio |
| Solicitação mais recente na base | 12/11/2026 (agendamento mais distante: 18/02/2027) |
| Medida | **fila** = os três status: pendente de regulação, corrigida e reenviada para regulação, pendente de regulação por fila de espera. Devolvidas para complementação ficam fora e são contadas à parte |
| Fila viva | só as solicitações a partir de `data_solicitacao={">=12/11/2024"}` (24 meses contados da solicitação mais recente) |
| Agendadas em 12 meses | `data_agendamento={">=12/11/2025<=11/11/2026"}`, todos os status |
| Ordem | panorama; `ordem.json` (hash 220378065) |
| Via | kit do motor `ferramentas/mapa_social/motor.js` (versão 2026-10-27, assinatura 1939648169); saída pela transcrição, 1 parte(s) conferidas por hash (`ferramentas/ler_motor.py`) |

Pessoas = CNS distintos no conjunto (quem espera por mais de um exame conta uma vez); só a contagem sai do motor. Espera em dias, calculada no motor sobre os registros do conjunto.

## Alarmes

Não se aplicam ao panorama: os alarmes são do objeto (CID, composição, fila viva), e o panorama não tem objeto.

## Lacunas

nenhuma

## O universo

O total de cada universo é do motor, com cada pedido e cada pessoa uma vez: a soma das filas pode passar dele, porque o mesmo pedido pode estar em dois pares nome × código.

| recorte | o que entra | filas | fila | fila viva | pessoas |
|---|---|---|---|---|---|
| colonoscopia (código) | codigos: 02.09.01.002-9 | 3 | 22.826 | 20.072 | 22.821 |
| colonoscopia (nome) | termos: COLONOSCOPIA | 3 | 22.826 | 20.072 | 22.821 |
| retossigmoidoscopia | codigos: 02.09.01.005-3 | 1 | 415 | 415 | 415 |

## Varredura das filas (panorama)

Cada fila do universo (nome exato × código), sem decisão: o panorama só mostra. Anos de estoque = fila ÷ agendadas em 12 meses pelo mesmo nome e código (**calculado**).

### colonoscopia (código): por pessoas

| fila | código | fila | fila viva | pessoas | devolvidas | espera média | espera mediana | espera máxima | pedido mais antigo | agendadas 12 m | anos de estoque | CID principais |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| COLONOSCOPIA | 02.09.01.002-9 | 22.439 | 19.742 | 22.439 | 4.017 | 417,3 | 416,3 | 1.904,0 | 26/08/2021 | 6.510 | 3,4 | Z12 6.109, K92 2.821, K59 1.443 |
| COLONOSCOPIA C/ ANESTESIA | 02.09.01.002-9 | 386 | 330 | 386 | 449 | 295,4 | 181,0 | 1.025,3 | 22/01/2024 | 151 | 2,6 | Z12 132, K92 42, K63 26 |
| COLONOSCOPIA (COLOSCOPIA) | 02.09.01.002-9 | 1 | 0 | 1 | 0 | 3.398,0 | 3.398,0 | 3.398,0 | 24/07/2017 | — | — | Z00 1 |

### colonoscopia (código): as 20 de maior espera média

| fila | código | fila | fila viva | pessoas | devolvidas | espera média | espera mediana | espera máxima | pedido mais antigo | agendadas 12 m | anos de estoque | CID principais |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| COLONOSCOPIA (COLOSCOPIA) | 02.09.01.002-9 | 1 | 0 | 1 | 0 | 3.398,0 | 3.398,0 | 3.398,0 | 24/07/2017 | — | — | Z00 1 |
| COLONOSCOPIA | 02.09.01.002-9 | 22.439 | 19.742 | 22.439 | 4.017 | 417,3 | 416,3 | 1.904,0 | 26/08/2021 | 6.510 | 3,4 | Z12 6.109, K92 2.821, K59 1.443 |
| COLONOSCOPIA C/ ANESTESIA | 02.09.01.002-9 | 386 | 330 | 386 | 449 | 295,4 | 181,0 | 1.025,3 | 22/01/2024 | 151 | 2,6 | Z12 132, K92 42, K63 26 |

### colonoscopia (código): as 20 de mais anos de estoque

| fila | código | fila | fila viva | pessoas | devolvidas | espera média | espera mediana | espera máxima | pedido mais antigo | agendadas 12 m | anos de estoque | CID principais |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| COLONOSCOPIA | 02.09.01.002-9 | 22.439 | 19.742 | 22.439 | 4.017 | 417,3 | 416,3 | 1.904,0 | 26/08/2021 | 6.510 | 3,4 | Z12 6.109, K92 2.821, K59 1.443 |
| COLONOSCOPIA C/ ANESTESIA | 02.09.01.002-9 | 386 | 330 | 386 | 449 | 295,4 | 181,0 | 1.025,3 | 22/01/2024 | 151 | 2,6 | Z12 132, K92 42, K63 26 |

### colonoscopia (nome): por pessoas

| fila | código | fila | fila viva | pessoas | devolvidas | espera média | espera mediana | espera máxima | pedido mais antigo | agendadas 12 m | anos de estoque | CID principais |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| COLONOSCOPIA | 02.09.01.002-9 | 22.439 | 19.742 | 22.439 | 4.017 | 417,3 | 416,3 | 1.904,0 | 26/08/2021 | 6.510 | 3,4 | Z12 6.109, K92 2.821, K59 1.443 |
| COLONOSCOPIA C/ ANESTESIA | 02.09.01.002-9 | 386 | 330 | 386 | 449 | 295,4 | 181,0 | 1.025,3 | 22/01/2024 | 151 | 2,6 | Z12 132, K92 42, K63 26 |
| COLONOSCOPIA (COLOSCOPIA) | 02.09.01.002-9 | 1 | 0 | 1 | 0 | 3.398,0 | 3.398,0 | 3.398,0 | 24/07/2017 | — | — | Z00 1 |

### colonoscopia (nome): as 20 de maior espera média

| fila | código | fila | fila viva | pessoas | devolvidas | espera média | espera mediana | espera máxima | pedido mais antigo | agendadas 12 m | anos de estoque | CID principais |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| COLONOSCOPIA (COLOSCOPIA) | 02.09.01.002-9 | 1 | 0 | 1 | 0 | 3.398,0 | 3.398,0 | 3.398,0 | 24/07/2017 | — | — | Z00 1 |
| COLONOSCOPIA | 02.09.01.002-9 | 22.439 | 19.742 | 22.439 | 4.017 | 417,3 | 416,3 | 1.904,0 | 26/08/2021 | 6.510 | 3,4 | Z12 6.109, K92 2.821, K59 1.443 |
| COLONOSCOPIA C/ ANESTESIA | 02.09.01.002-9 | 386 | 330 | 386 | 449 | 295,4 | 181,0 | 1.025,3 | 22/01/2024 | 151 | 2,6 | Z12 132, K92 42, K63 26 |

### colonoscopia (nome): as 20 de mais anos de estoque

| fila | código | fila | fila viva | pessoas | devolvidas | espera média | espera mediana | espera máxima | pedido mais antigo | agendadas 12 m | anos de estoque | CID principais |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| COLONOSCOPIA | 02.09.01.002-9 | 22.439 | 19.742 | 22.439 | 4.017 | 417,3 | 416,3 | 1.904,0 | 26/08/2021 | 6.510 | 3,4 | Z12 6.109, K92 2.821, K59 1.443 |
| COLONOSCOPIA C/ ANESTESIA | 02.09.01.002-9 | 386 | 330 | 386 | 449 | 295,4 | 181,0 | 1.025,3 | 22/01/2024 | 151 | 2,6 | Z12 132, K92 42, K63 26 |

### retossigmoidoscopia: por pessoas

| fila | código | fila | fila viva | pessoas | devolvidas | espera média | espera mediana | espera máxima | pedido mais antigo | agendadas 12 m | anos de estoque | CID principais |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| RETOSSIGMOIDOSCOPIA FLEXÍVEL | 02.09.01.005-3 | 415 | 415 | 415 | 259 | 70,3 | 57,0 | 168,3 | 28/05/2026 | 1.776 | 0,2 | I84 115, K62 57, K92 50 |

### retossigmoidoscopia: as 20 de maior espera média

| fila | código | fila | fila viva | pessoas | devolvidas | espera média | espera mediana | espera máxima | pedido mais antigo | agendadas 12 m | anos de estoque | CID principais |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| RETOSSIGMOIDOSCOPIA FLEXÍVEL | 02.09.01.005-3 | 415 | 415 | 415 | 259 | 70,3 | 57,0 | 168,3 | 28/05/2026 | 1.776 | 0,2 | I84 115, K62 57, K92 50 |

### retossigmoidoscopia: as 20 de mais anos de estoque

| fila | código | fila | fila viva | pessoas | devolvidas | espera média | espera mediana | espera máxima | pedido mais antigo | agendadas 12 m | anos de estoque | CID principais |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| RETOSSIGMOIDOSCOPIA FLEXÍVEL | 02.09.01.005-3 | 415 | 415 | 415 | 259 | 70,3 | 57,0 | 168,3 | 28/05/2026 | 1.776 | 0,2 | I84 115, K62 57, K92 50 |

## Rumo por código

Um código por linha, com as filas do universo somadas (cada par nome × código uma vez). Tudo **calculado** no montador sobre a série mensal do motor (abas "Por código" da planilha). Os 12 meses fechados vão de 2025-11 a 2026-10, e os 12 de antes, de 2024-11 a 2025-10. Entrantes = pedidos abertos mais os já agendados, pelo mês do pedido. Oferta = agendamentos pelo mês em que acontecem, em todas as situações. Falta = faltas ÷ (realizados + faltas). Saldo por mês = (entrantes − oferta) ÷ 12: positivo, a fila cresce. Maior mês de oferta e média dos 3 últimos meses fechados, para ver o esforço que parou.

| código | fila mais pedida do código | fila | fila viva | devolvidas | entrantes 12 m | entrantes 12 m antes | oferta 12 m | oferta 12 m antes | saldo por mês | falta 12 m | maior mês de oferta | oferta média 3 últimos meses |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 02.09.01.002-9 | COLONOSCOPIA | 22.826 | 20.072 | 4.466 | 12.141 | 12.561 | 6.688 | 6.897 | 454,4 | 40% | 2025-02 (927) | 609,0 |
| 02.09.01.005-3 | RETOSSIGMOIDOSCOPIA FLEXÍVEL | 415 | 415 | 259 | 1.642 | 2.110 | 1.775 | 1.705 | -11,1 | 27% | 2026-10 (192) | 150,3 |

## Região de Saúde

**colonoscopia (código)**, na medida da fila (o conjunto do objeto):

| Região de Saúde | fila | pessoas |
|---|---|---|
| Região Sudoeste | 4.611 | 4.611 |
| URD | 3.171 | 3.171 |
| Região Norte | 2.793 | 2.791 |
| Região Sul | 2.703 | 2.702 |
| Região Oeste | 2.529 | 2.529 |
| Contratado/Credenciado | 1.937 | 1.937 |
| Região Central | 1.756 | 1.756 |
| Região Centro-Sul | 1.589 | 1.589 |
| Região Leste | 1.505 | 1.505 |
| Serviços Centralizados | 1 | 1 |
| sem Região de Saúde | 231 | 231 |

**colonoscopia (nome)**, na medida da fila (o conjunto do objeto):

| Região de Saúde | fila | pessoas |
|---|---|---|
| Região Sudoeste | 4.611 | 4.611 |
| URD | 3.171 | 3.171 |
| Região Norte | 2.793 | 2.791 |
| Região Sul | 2.703 | 2.702 |
| Região Oeste | 2.529 | 2.529 |
| Contratado/Credenciado | 1.937 | 1.937 |
| Região Central | 1.756 | 1.756 |
| Região Centro-Sul | 1.589 | 1.589 |
| Região Leste | 1.505 | 1.505 |
| Serviços Centralizados | 1 | 1 |
| sem Região de Saúde | 231 | 231 |

**retossigmoidoscopia**, na medida da fila (o conjunto do objeto):

| Região de Saúde | fila | pessoas |
|---|---|---|
| Região Sudoeste | 158 | 158 |
| Região Norte | 62 | 62 |
| Região Sul | 51 | 51 |
| Região Central | 37 | 37 |
| Região Oeste | 32 | 32 |
| Região Leste | 24 | 24 |
| Região Centro-Sul | 22 | 22 |
| URD | 14 | 14 |
| Contratado/Credenciado | 11 | 11 |
| sem Região de Saúde | 4 | 4 |

## Diferença para a coleta anterior

Sem coleta anterior na pasta.
