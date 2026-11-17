# Mapeamento de cardiologia — os R$ 2 milhões da Emenda 41360018

**Controle interno.** Documento de 27/10/2026 que reúne o que se estudou para o redacao_08, de
22 a 27/10:
- as filas;
- quem mais as atende;
- o que paga cada OCI e cada exame;
- as decisões de enquadramento;
- a conta de quantas pessoas cabem.

Acompanha a planilha `planos/redacao_08/carteira_ampla_cardiologia.xlsx` (seção 9), no ramo
`plano_oci_cardiologia`. Nada daqui foi para documento do plano. A escolha é sua.

## 1. O recurso e o objeto

| | |
|---|---|
| Emenda | 41360018/2024, Senador Izalci Lucas, individual, **federal**, ação 2E90 |
| Valor | **R$ 2.000.000,00**: R$ 200.000,00 de gestão e apoio (10%, provisório, P-05) e **R$ 1.800.000,00 para produção** |
| Executor | Instituto Fazer o Bem, Faz Bem (filial DF 21.324.949/0002-06). **Sem CNES** e primeiro convênio |
| Objeto | "atendimentos relacionados à OCI de Cardiologia" (Ofício 36/2026). Exames avulsos pedem um ofício novo (lição do Ofício 398 da ARINS) |
| Valor por unidade | SIGTAP de 10/2026, sem complemento (LI-002) |
| Instrumento | convênio, com o núcleo executado pelo Instituto (Decreto 48.727/2026, art. 17, I, e art. 33) |

## 2. O que se estudou

Arquivos em `output/` (sua pasta) e coletas em `planos/redacao_08/dados/fontes/` (ramo `plano_oci_cardiologia`):

| quando | o quê | onde está |
|---|---|---|
| 22/10 | dossiê das sete OCI, fichas do SIGTAP, preços no DF | `dossie/`, `dados/precos.md`, `dados/fontes/sigtap_*` |
| 25/10 | recoleta pelo método novo (a fila de 22/10 estava inflada) | `mapa_social_20261025.md`, `comparacao_agentes_cardiologia_20261025.md` |
| 26/10 | o que fazer com os R$ 2 milhões; o IEV | `estudo_cardiologia_2_milhoes_20261026.md`, `mapeamento_iev_20261026.md` |
| 27/10 | exames avulsos | `mapa_exames_cardiologia_20261027.md` |
| 27/10 | por OCI e por exame, com as portarias novas e a Tabela SUS Candanga | `estudo_cardiologia_por_oci_20261027.md`, `estudo_cardiologia_por_exames_20261027.md` |
| 27/10 | **panorama** de exames e consultas, e **medição** das OCI com entrada, oferta e falta | `mapa_social_20261027_panorama.md` (9/9), `mapa_social_20261027_ocis.md` (11/11), `mapeamento_filas_cardiologia_20261027.md` |
| 27/10 | as decisões de enquadramento | `estudo_enquadramento_cardiologia_20261027.md`, `dados/enquadramento_mapa_social.json` |
| 27/10 | **medição pela porta de entrada**, com as decisões | `mapa_social_20261027_porta.md` (10/11, item I; ver seção 12), `estudo_porta_cardiologia_20261027.md` |

## 3. Como ler os números

| termo | o que é |
|---|---|
| **pessoas** | CNS distintos, na idade da ficha. Nas OCI, em pessoas; nos exames avulsos, em pedidos |
| **fila viva** | os pedidos dos últimos 24 meses (de 27/10/2024 em diante), sem as devolvidas |
| **porta de entrada** | a fila por onde a pessoa chega à OCI. Caso 1: só a consulta com o CID. Caso 2: a consulta e os exames obrigatórios com o CID |
| **entram por mês** | pedidos novos (abertos e já agendados, pelo mês do pedido), média de 10/2025 a 09/2026 |
| **rede** | agendamentos pelo mês em que acontecem. "Hoje" = 07 a 09/2026, com o IEV dentro. "Sem o IEV" = 10/2025 a 04/2026 |
| **disponíveis em 12 meses** | fila viva − o que o IEV ainda faz + 12 × (entram − rede) |
| **falta** | faltas ÷ (realizados + faltas) em 12 meses |
| **realizáveis** | disponíveis × (1 − falta). Supõe que quem falta não volta (premissa pessimista) |

## 4. Normas e preços

- **Nenhuma portaria nova mudou as OCI de cardiologia nem os valores** de exames e consultas.
  - Fontes: Notas Técnicas do SIGTAP de 06 a 11/2026, DOU de 09 a 27/10 e pacote oficial de 10/2026.
  - As novidades de cardiologia não servem ao Instituto:
    - SAES 5.086/2026 (habilitação 38.14, unidade móvel federal);
    - SAES 4.857/2026 (38.04 no eco, Holter e MAPA);
    - SAES 4.960/2026 (eletrocardiograma na atenção primária, valor zero).
- **O SIGTAP paga** R$ 270,00 na 003-4, R$ 200,00 na 002-6, R$ 130,00 na 007-7 e R$ 350,00 na 006-9.
- **Os exames avulsos pagam pouco:**
  - eletrocardiograma R$ 5,15; Holter e ergométrico R$ 30,00; MAPA R$ 10,07;
  - eco R$ 67,86, ou R$ 160,14 com o incremento da SAES 4.282, que exige a habilitação 38.05 e CNES.
- **A Tabela SUS Candanga** é o preço que a SES reconhece (análise comparativa de 06/08/2026, mediano).
  - **Ela não muda o valor do plano:** o que passa do SIGTAP é recurso do DF.
  - **Nas OCI, ela é o SIGTAP mais 31%:** o SIGTAP cobre 77% dela em todas.
  - **Nos exames, cobre de 34% a 56%.** O eco com incremento fica em 97%.

| linha | cobre o mercado (mínimo do DF) | cobre a Candanga |
|---|---|---|
| 007-7 pré-operatório, com cardiologista | **116%** | 77% |
| 002-6 avaliação cardiológica | **132%** | 77% |
| 003-4 coronária, inicial | 90% | 77% |
| 006-9 insuficiência cardíaca | 67% | 77% |
| eco com incremento | 80% | 97% |
| Holter, ergométrico, eletrocardiograma | 12% a 26% | 34% a 43% |

## 5. As filas

**Pela porta de entrada** (medição de 27/10, 16:32):

| fila | caso | pessoas (viva) | entram/mês | rede hoje · sem o IEV | falta |
|---|---|---|---|---|---|
| 007-7, fila inteira de risco cirúrgico (P-08) | — | **9.654** (8.170) | 704 | 796 · 291 | **38%** |
| 006-9, I50 e I11.0 | 1 | 2.113 (1.819), estimado | 196 | 145 · 109 | 29% |
| 006-9, I50 e I11.0 | 2 | 4.726 (2.662), estimado | 285 | 208 · 174 | 32% |
| 003-4 coronária (I20 a I25) | 1 | **2.023** (1.617) | 213 | 206 · 131 | 24% |
| 003-4 coronária (I20 a I25) | 2 | 2.816 (2.105) | 372 | 365 · 286 | 29% |
| 002-6, pelo eletrocardiograma | — | 345 (227) | 30 | 29 · 14 | 35% |
| 007-7, só o CID da ficha | — | 88 (87) | 20 | 19 · 10 | 25% |

**Os exames** (panorama, por código):

| exame | fila (viva) | entram/mês | rede hoje | realizados/mês | falta |
|---|---|---|---|---|---|
| Holter | 36.198 (11.109) | 560 | 259 | 97 | **49%** |
| eletrocardiograma | 20.272 (15.077) | 1.540 | 1.264 | 660 | 42% |
| eco transtorácico | 14.551 (14.551) | 3.582 | 3.571 | 2.326 | 26% |
| MAPA | 12.678 (6.245) | 388 | 256 | 115 | 40% |
| ergométrico | 3.181 (1.682) | 471 | 476 | 286 | 35% |
| eco de estresse | 70 | 71 | 70 | 30 | 47% |

**O que mostram:**
- todas as filas de OCI crescem;
- o risco cirúrgico parou de crescer com o IEV, mas não diminui;
- o Holter é a fila parada: pelo que se realiza hoje, a viva leva 9,5 anos para zerar;
- o eco só fica estável porque a regulação devolve muitos pedidos ao médico: 16.446.

## 6. Quem mais atende

| quem | o quê | na fila |
|---|---|---|
| **IEV**, convênio 030977 (Fila Zero, até 05/2027) | 4.647 OCI 001-8 (2.822 agendadas, faltam 1.825); 1.000 OCI 006-9 e 900 OCI 004-2 (1.138 consultas adulto agendadas, faltam cerca de 760) | risco cirúrgico; consulta adulto |
| **HAPVIDA** (CNES 797146), Agora Tem Especialistas | 792 OCI de risco cirúrgico por mês, aprovada, aguardando a comissão do programa (03/09) | risco cirúrgico |
| **Hospital de Ceilândia** (CNES 3025020), créditos financeiros | 115 OCI de risco cirúrgico por mês, em análise final (03/09) | risco cirúrgico |
| planos aprovados, plano 4, redacao_07 | nada de cardiologia (o eco saiu do redacao_07) | — |
| unidade móvel de cardiologia (38.14) | federal; pode chegar ao DF sem passar pela SES | — |

O IEV não agenda exame no SISREG: os exames da OCI dele vão dentro do pacote e não tiram ninguém
das filas de exame.

## 7. O enquadramento: o que você decidiu

Gravado em `dados/enquadramento_mapa_social.json` (27/10/2026):

| decisão | o que ficou | por quê |
|---|---|---|
| porta de entrada | **medir os dois casos** | a OCI anda pela consulta (precedente do IEV). O caso 2 depende de a SES aceitar converter pedido de exame |
| caso 2 na coronária | só **eletrocardiograma e ergométrico** | são os obrigatórios da 003-4; o eco de estresse e a cintilografia são da progressão |
| consulta adulto | **entra pelo CID** | é onde a maior parte espera; o IEV já usa essa fila |
| 003-4 | **I20 a I25** | inclui quem infartou e está em seguimento (587 pessoas a mais pela consulta) |
| linha coronária | **cada pessoa uma vez, na 003-4** | a 004-2 e a 005-0 são o passo seguinte de parte de quem fez a 003-4 |
| 006-9 | **medir as versões** e decidir (seção 8) | — |
| P-08 | **entra, a confirmar na SES;** 007-7 com cardiologista | maior fila; a regulação já manda essa fila ao IEV com o CID da cirurgia |
| fila viva ou inteira | **viva na conta e na meta;** inteira só na justificativa | pedido de mais de 2 anos muitas vezes não vale mais |
| 002-6 | **porta pelo eletrocardiograma** com Z13.6 ou Z84.8 | é o público da OCI; pela consulta seriam 41 pessoas |

## 8. A 006-9 sem I13.0, I13.2, I42 e I43

O cenário que você pediu é a **006-9 com I50 e I11.0**.

| versão | caso 1: pessoas (viva) | caso 1: disponíveis em 12 meses | caso 2: disponíveis em 12 meses |
|---|---|---|---|
| I50 | 2.079 (1.794) | 1.627 | 2.783 |
| **I50 e I11.0** | **cerca de 2.113 (1.819)** | **1.664** | **2.827** |
| I50, I11.0, I13.0 e I13.2 | 2.120 (1.824) | 1.671 | 2.835 |
| ampliada, com I42 e I43 | 2.280 (1.957) | 1.833 | 3.083 |

Os disponíveis estão na rede de hoje, já sem os cerca de 760 do IEV.

**A linha "I50 e I11.0" é estimada.** A medição separa o I50 e o I50 com I11.0, I13.0 e I13.2.
- Os pedidos a mais desta versão são 36 de I11 e 7 de I13 nas consultas, e 55 e 9 com os exames.
- Apliquei essa proporção às pessoas e ao fluxo.
- A diferença é de poucas pessoas: a próxima coleta mede a versão direto.

**Por que o I11.0 fica:**
- **É o mesmo doente.** I11.0 é a "doença cardíaca hipertensiva com insuficiência cardíaca": a
  insuficiência cardíaca causada pela pressão alta.
- **Pela regra de codificação,** quando a hipertensão causou a insuficiência cardíaca, o código é
  o I11.0, e não o I50. Tirá-lo deixaria de fora quem foi codificado do jeito certo.
- **A investigação e a conduta são as da 006-9.**

**Por que o I13.0 e o I13.2 saem:**
- **São cardiopatia e nefropatia hipertensivas com insuficiência cardíaca.** No I13.2, também com
  insuficiência renal. É o doente cardiorrenal.
- **O NT-proBNP, exame obrigatório da 006-9, perde valor:** a doença renal o eleva por si, sem
  dizer se é o coração.
- **O ergométrico, também obrigatório,** costuma ser limitado nesse doente.
- **O cuidado pede nefrologia,** que a OCI não tem.
- **São poucos:** cerca de 7 pessoas.

**Por que o I42 e o I43 saem:**
- **I42 são as cardiomiopatias** (dilatada, hipertrófica, restritiva, alcoólica). O diagnóstico e
  a estratificação pedem ressonância cardíaca, teste genético e avaliação da família, que a OCI
  não tem. É doente de ambulatório especializado.
- **I43 é a cardiomiopatia de outra doença** (amiloidose, tireoide). A doença de base manda, e os
  exames próprios dela também ficam fora da OCI.
- **São cerca de 160 pessoas,** quase todas I42, das quais 142 pedidos na consulta adulto.

**O que não muda:** a ficha da 006-9 aceita todo o capítulo I. A escolha é de foco e de defesa
da fila, não de faturamento. A cardiopatia chagásica (B57.2) não entra em nenhuma versão: o
código dela está fora do capítulo I.

## 9. A planilha da carteira

`planos/redacao_08/carteira_ampla_cardiologia.xlsx`, no molde da carteira de imagem:

| aba | o que tem |
|---|---|
| **Resumo** | os parâmetros (amarelos), o resultado e a conta por grupo |
| **Carteira ampla** | uma linha por alternativa, com a prioridade na coluna A |
| **Fontes e notas** | de onde vem cada número e cada premissa |

**Como usar:**
1. **A prioridade** vai na coluna A da Carteira (1 = primeiro, sem repetir). O recurso vai na
   ordem: cada linha recebe o que sobra das anteriores, até a base da conta.
2. **Só uma linha de cada grupo** pode ter prioridade. As linhas de um grupo são alternativas e
   contam as mesmas pessoas:
   - coronária: caso 1 ou 2;
   - insuficiência cardíaca: caso e versão do CID;
   - risco cirúrgico: com ou sem a P-08;
   - eco: com ou sem incremento.

   O Resumo avisa se um grupo tem duas.
3. **Os quatro parâmetros do Resumo:**
   - **base da conta:** 1 = realizáveis, 2 = disponíveis em 12 meses, 3 = fila viva;
   - **ritmo da rede:** 1 = hoje, com o IEV; 2 = sem o IEV;
   - **cenário do risco cirúrgico:** 1 = ninguém entra no lugar do IEV; 2 = Ceilândia;
     3 = HAPVIDA; 4 = os dois;
   - **gestão e apoio:** em %.

**A prioridade sugerida:**
1. coronária (003-4, caso 1);
2. avaliação cardiológica (002-6);
3. risco cirúrgico (007-7 com a P-08);
4. insuficiência cardíaca (006-9, caso 1, I50 e I11.0).

As OCI mais baratas para o executor vêm antes: a 007-7 e a 002-6 se pagam; a 003-4 chega a 90%.
A 006-9 fica por último, porque paga 67% do mercado. Os exames avulsos estão na lista, sem
prioridade, para não fechar a porta.

**As cores:**
- azul = número das fontes;
- preto = calculado;
- verde = vem de outra aba ou parâmetro;
- amarelo = o que você muda;
- cinza = fora da conta.

## 10. Os cenários

Com a prioridade sugerida e R$ 1,8 milhão para produção. Atendidos de cada linha na ordem
003-4 · 002-6 · 007-7 · 006-9.

| porta | P-08 | base | rede | risco cirúrgico | atendidos | valor pago | sobra |
|---|---|---|---|---|---|---|---|
| **caso 1** | **sim** | **realizáveis** | **hoje** | **ninguém entra** | **9.657** (1.290 · 152 · 7.034 · 1.181) | R$ 1.706.470 | R$ 93.530 |
| caso 1 | sim | disponíveis | hoje | ninguém entra | 11.896 (1.693 · 234 · 9.969 · 0) | R$ 1.799.880 | R$ 120 |
| caso 1 | sim | realizáveis | hoje | HAPVIDA e Ceilândia | 2.887 (1.290 · 152 · 264 · 1.181) | R$ 826.370 | R$ 973.630 |
| caso 1 | sim | disponíveis | sem o IEV | HAPVIDA e Ceilândia | 5.529 | R$ 1.572.620 | R$ 227.380 |
| caso 1 | não | realizáveis | hoje | — | 2.692 | R$ 801.020 | R$ 998.980 |
| caso 1 | não | disponíveis | sem o IEV | — | 5.305 | R$ 1.543.500 | R$ 256.500 |
| caso 2 | sim | realizáveis | hoje | ninguém entra | 9.982 (1.547 · 152 · 7.034 · 1.249) | R$ 1.799.660 | R$ 340 |
| caso 2 | sim | disponíveis | hoje | HAPVIDA e Ceilândia | 5.669 | R$ 1.680.910 | R$ 119.090 |
| caso 2 | não | disponíveis | hoje | — | 5.337 | R$ 1.637.750 | R$ 162.250 |
| caso 2 | não | disponíveis | sem o IEV | — | 6.160 | R$ 1.799.790 | R$ 210 |

**O que os cenários dizem:**
- **Com a P-08 e ninguém no lugar do IEV, o recurso é o limite.** São 9 a 12 mil pessoas, e a
  006-9, por último, recebe pouco ou nada.
- **Se a HAPVIDA e o Hospital de Ceilândia começarem, ou sem a P-08, a fila é o limite.** No
  caso 1 sobram de R$ 230 mil a R$ 1 milhão.
- **O caso 2 usa melhor o recurso sem a P-08,** mas só vale se a SES aceitar converter pedido de
  exame em OCI.
- **O risco cirúrgico é a peça que mais move a conta.** Depende de duas respostas da SES: a P-08
  e a situação das duas propostas.

## 11. O que ficou de fora, e por quê

| o quê | por quê |
|---|---|
| OCI 005-0 e as cintilografias | medicina nuclear (CNEN) é serviço de terceiro; o núcleo fica com o Instituto |
| OCI 004-2 | passo seguinte da linha coronária; não se soma à fila |
| OCI 001-8 | é a do IEV, na mesma fila da 007-7 |
| angiotomografia de coronárias | código da TC de tórax, do plano 4 |
| exames avulsos (na planilha, sem prioridade) | o Ofício 36 fala em OCI; pagam de 12% a 28% do mercado, menos o eco com incremento, que exige CNES e 38.05 |
| consulta avulsa | paga R$ 10,00 (9% do mercado); só se paga dentro da OCI |

## 12. O que falta

1. **A SES,** com quatro perguntas:
   - a P-08;
   - converter pedido de exame em OCI (caso 2 e porta da 002-6);
   - quando começam a HAPVIDA e o Hospital de Ceilândia;
   - o que o IEV ainda faz na 006-9 e na 004-2.
2. **O CNES do Instituto** (P-03): sem ele, nenhum caminho anda.
3. **Medir a versão I50 e I11.0** direto, na próxima coleta.
4. **O risco cirúrgico por estabelecimento:** pede uma dimensão nova no kit do Mapa Social.
5. **O conferidor:** o item I procura a linha da OCI pelos últimos cinco caracteres do id. Na
   coleta da porta, isso trocou duas linhas da 006-9. Os números estão certos no `.md`, conferidos
   à mão. Falta corrigir a ferramenta.
6. **O apoio (P-05):** com 30%, a produção cai para R$ 1,4 milhão, e o recurso fica ainda mais
   curto com a P-08.
