# A fila da colonoscopia

Fonte: `fontes/mapa_social_20261112.md` (agente mapa-social, panorama, base recarregada em
12/11/2026 16:33, consulta às 18:04; conferência 9/9). Medida: os três status de espera;
devolvidas para complementação à parte.

| fila (nome exato) | código | fila | pessoas | fila viva (24 m) | devolvidas | espera média | espera mediana | agendadas 12 m |
|---|---|---|---|---|---|---|---|---|
| COLONOSCOPIA | 02.09.01.002-9 | 22.439 | 22.439 | 19.742 | 4.017 | 417,3 dias | 416,3 dias | 6.510 |
| COLONOSCOPIA C/ ANESTESIA | 02.09.01.002-9 | 386 | 386 | 330 | 449 | 295,4 dias | 181,0 dias | 151 |
| COLONOSCOPIA (COLOSCOPIA) | 02.09.01.002-9 | 1 | 1 | 0 | 0 | 3.398,0 dias | — | — |
| **código 02.09.01.002-9** | | **22.826** | **22.821** | **20.072** | **4.466** | | | |

No documento, a espera se escreve em dias inteiros: 417 dias (417,3) e 295 dias (295,4).

**Os "24 mil" do pedido.** A fila medida é de 22.821 pessoas. Com as 4.466 devolvidas para
complementação, os pedidos passam de 27 mil; a fila viva (pedidos dos últimos 24 meses) é de
20.072. O documento usa a medida do método: 22.821 pessoas.

**O que o recurso alcança (controle interno, não vai ao documento).** 20.327 colonoscopias =
90,6% das 22.439 solicitações da fila "COLONOSCOPIA" (90,59%), a única do documento. O
documento diz "a maior parte dessa fila", sem percentual.

**O rumo (seção "Rumo por código" da coleta).** Nos 12 meses fechados (11/2025 a 10/2026)
entraram 12.141 pedidos e a rede ofertou 6.688 agendamentos, com 40% de faltas: a fila cresce
cerca de 454 pedidos por mês. Em 12 meses de execução, com a oferta atual mantida, entram
cerca de 12 mil e a rede atende cerca de 6,7 mil; as 20.327 do projeto mais a oferta da rede
cobrem a fila de hoje e a maior parte da que entra. O absenteísmo não vai ao plano
(decisão do usuário, LI-016 fora).

**Região de Saúde** (fila): Sudoeste 4.611, URD 3.171, Norte 2.793, Sul 2.703, Oeste 2.529,
Contratado/Credenciado 1.937, Central 1.756, Centro-Sul 1.589, Leste 1.505, sem região 231,
Serviços Centralizados 1. A maior concentração é a Região Sudoeste.

**Enquadramento** (`enquadramento_mapa_social.json`): o documento mostra só a fila
"COLONOSCOPIA" (22.439 solicitações, 22.439 pessoas, 417 dias), por decisão do usuário de
12/11/2026 ("na parte fila deixe apenas colonoscopia"). Ficam fora a "COLONOSCOPIA C/
ANESTESIA" (386) e o pedido de 2017 em "COLONOSCOPIA (COLOSCOPIA)", do mesmo código, e a
retossigmoidoscopia flexível (02.09.01.005-3), outro procedimento.

## A fila da OCI 09.01.01.008-1 (medição de 12/11/2026, 18:23)

Fonte: `fontes/mapa_social_20261112_oci.md` (agente mapa-social, medição, conferência 11/11).
A OCI só se fatura com CID compatível (ficha 11/2026: C17 a C21, D01, D12, K62, K63) e idade
de 10 anos ou mais. Na fila "COLONOSCOPIA" (22.439):

| recorte | pedidos | viva | parte da fila | CID principais |
|---|---|---|---|---|
| teto (CID aceito) | 4.025 | 3.600 | 18% | C18 1.231, K63 1.027, K62 985, D12 469, C20 231 |
| finalidade (C18 a C20) | 1.477 | 1.328 | 7% | C18 1.231, C20 231, C19 15 |

Espera média na finalidade: 437,3 dias (mediana 456,9). Os CIDs mais pedidos da fila inteira
(Z12 rastreamento 6.109, K92 sangramento 2.821, K59 1.443, no panorama) **não** são aceitos pela
OCI.

**O problema (controle interno).** O recurso compra 14.444 OCI, 3,6 vezes o teto (4.025) e
9,8 vezes a finalidade (1.477). Com a OCI sozinha, a maior parte das 22.439 pessoas da fila
não pode ser atendida pela OCI sem CID compatível. Alternativa (B, carteira mista): OCI para
as 4.025 do CID aceito (R$ 2.820.035,75) e colonoscopia avulsa 02.09.01.002-9 a R$ 497,84 para
o resto, 14.663 exames (R$ 7.299.827,92); juntas, R$ 10.119.863,67 e 18.688 pessoas, 83,3% da
fila; sobra R$ 136,33. Decisão do usuário (`../pendencias.md`, P-10).
