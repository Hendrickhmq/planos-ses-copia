# Mapa Social da Saúde — fila das sete OCI de cardiologia (09.02.01), recarga de 25/10/2026 14:31

Recoleta do agente `mapa-social` para o redacao_08 (Instituto Fazer o Bem, Faz Bem; emenda
41360018/2024), pelo **método de 25/10/2026**: cada OCI sai com três números (teto, finalidade e
núcleo), cada um com a fila inteira e a **fila viva** (24 meses), e com os alarmes antes dos
números. Mesmas filas da composição da coleta de 22/10/2026 (`mapa_social_20261022.md`), que não
se sobrescreve. Planilha em `mapa_social_20261025.xlsx`; JSON do motor, JSON da coleta no formato
do método e script em `mapa_social_20261025_bruto/`.

| campo | conteúdo |
|---|---|
| Fonte | Mapa Social da Saúde – Regulamentação (MPDFT) · Lista de Espera – Exames e Consultas · `https://paineis-ext.mpdft.mp.br/extensions/mapasauderegulamentacao/mapasauderegulamentacao.html` · app Qlik `7edb02fa-f1f5-4ea6-b348-049a4ac2d095` · dados SISREG/DATASUS |
| Última recarga da base | 25/10/2026 14:31:55 (qLastReloadTime 2026-10-25T17:31:55Z) |
| Consulta | 25/10/2026, de 15:19 a 15:33 (relógio do motor), sem recarga no meio |
| Solicitação mais recente na base | 25/10/2026 (agendamento mais distante: 27/01/2027) |
| Medida | **fila** = os três status: pendente de regulação, corrigida e reenviada para regulação, pendente de regulação por fila de espera. Devolvidas para complementação ficam fora e são contadas à parte |
| Fila viva | só as solicitações de 25/10/2024 em diante (24 meses contados da solicitação mais recente), `data_solicitacao={">=25/10/2024"}`; conferida contra a soma por ano no ECG (594 + 5.119 + 9.418 = 15.131). Na finalidade, também as janelas de 12 meses (desde 25/10/2025) e de 36 meses (desde 25/10/2023) |
| Recorte | todos os anos na fila inteira; cada fila fixa pelo nome interno; OCI pelo CID da solicitação (`codigo_cid_solicitado`) |
| Via | Qlik Engine API do próprio painel (evaluateEx e hipercubos de sessão), no navegador embutido |

Pessoas = CNS distintos no conjunto (quem espera por mais de um exame conta uma vez); só a
contagem sai do motor. Espera em dias, calculada no motor sobre os registros do conjunto.

**Os CID de cada OCI.** O aceito é o da ficha do SIGTAP 10/2026 (`sigtap_09020100*_102026.md`,
ainda no formato antigo, com uma expressão só). A finalidade e as variantes são a proposta de
quem chamou a coleta, para o usuário escolher; a principal está marcada.

| OCI | CID aceito (teto) | finalidade principal | variante calculada |
|---|---|---|---|
| 001-8 risco cirúrgico | Z136, Z848 | = o aceito | a consulta de risco cirúrgico sem recorte de CID, "a decidir" (P-08) |
| 002-6 avaliação cardiológica | Z136, Z848 | = o aceito | — |
| 003-4 SCC, inicial | I00–I99 (`I*`) | I20, I25 (angina e isquêmica crônica) | I20–I25 (todas as isquêmicas) |
| 004-2 SCC, progressão I | I20–I25 | = o aceito | I20, I25 |
| 005-0 SCC, progressão II | I20–I25 | = o aceito | I20, I25 |
| 006-9 insuficiência cardíaca | I00–I99 (`I*`) | I50 | IC ampliada: I50, I110, I130, I132, I42, I43 |
| 007-7 pré-operatório | Z018, Z488, Z489 | = o aceito | — |

---

## Alarmes

Os seis alarmes do método dispararam (29 ocorrências, que a conferência refaz pelo JSON).
Limites propostos em 25/10/2026 e ainda a confirmar pelo usuário: 30%, 5%, 24 meses, 3 anos.

- **CID largo** — 003-4 e 006-9: o CID aceito pela ficha é o capítulo I inteiro (`I*`). O teto
  (28.734 e 50.055 pessoas) não vai ao dossiê; a finalidade proposta é I20 e I25 na 003-4
  (3.683 pessoas) e I50 na 006-9 (6.510).
- **CID dominante** — 003-4 e 006-9: no teto, I10 (hipertensão essencial), fora da finalidade
  das duas, é 88% do eletrocardiograma com CID do capítulo I (10.223 de 11.662 solicitações) e
  49% do teste ergométrico (835 de 1.707).
- **CID raro** — 001-8: Z136/Z848 em 447 de 30.686 solicitações das filas da composição (1,5%);
  002-6: em 519 de 44.904 (1,2%); 007-7: Z018/Z488/Z489 em 142 de 30.686 (0,5%). Na consulta de
  risco cirúrgico, o CID pedido é o da cirurgia (I83 varizes 1.328, K80 colelitíase 1.307, K40
  hérnia inguinal 657, N40 próstata 399, E66 obesidade 382, H25 catarata 283). A fila sem
  recorte vai como **a decidir**: 9.630 pessoas (8.150 na viva), para a 001-8 (P-08) e a 007-7.
- **fila velha** — 001-8: 134 de 441 pessoas da finalidade (30,4%) só têm pedido de antes de
  25/10/2024; o pedido mais antigo é de 18/10/2012 (ECG). Viva: 307 pessoas. A 006-9 fica logo
  abaixo do limite (29,0%: 6.510 inteira, 4.620 viva; o pedido mais antigo é de 01/08/2012), e o
  teto dela, acima (41,9%: 50.055 e 29.097).
- **estoque** — HOLTER 24 HORAS (obrigatório na 006-9): 36.178 na fila e 2.739 agendadas em 12
  meses, 13,2 anos de agendamentos (a fila viva, 11.115, dá 4,1 anos). Cintilografia de
  estresse: 1.720 e 365, 4,7 anos; de repouso: 1.484 e 347, 4,3 anos (as duas obrigatórias na
  005-0). A fila não anda, e parte dos pedidos pode não valer mais.
- **fila genérica** — está nas sete: eletrocardiograma (001-8, 002-6, 003-4, 006-9, 007-7), RX
  de tórax (001-8, 007-7), Holter (006-9), eco transtorácico adulto (002-6, 003-4, 006-9) e
  consulta de cardiologia adulto (002-6, 003-4, 004-2, 005-0, 006-9). Contam só pelo CID da
  finalidade, e pô-las na OCI é decisão do usuário. Sem as genéricas, a finalidade fica em:
  001-8 54; 002-6 0; 003-4 745; 004-2 303; 005-0 1.595; 006-9 969; 007-7 87 pessoas (seção 1.4).

**O que o método não resolve:**
- Na 004-2 e na 005-0 a finalidade é o próprio CID aceito, e a fila vem quase toda da consulta
  adulto (genérica): 1.793 das 2.055 pessoas da 004-2. O exame obrigatório da 004-2 (eco de
  estresse) tem 32 pessoas com I20–I25. Se a consulta adulto não entrar, a 004-2 cai para 303.
- Na 001-8 e na 002-6 o núcleo é o ECG com Z136/Z848 (387 pessoas, as mesmas nas duas): a
  consulta de entrada com esse CID é menor (54 e 41).
- O que a ficha aceita na 001-8 (Z136/Z848) não descreve o risco cirúrgico; a fila sem recorte
  (9.630) é de quem pede avaliação pré-operatória para qualquer cirurgia, e serve também à 007-7.

## 1. Os três números por OCI

Em pessoas. A finalidade é a fila da OCI; o teto fica como referência; o núcleo é o piso.

| OCI | CID aceito | CID da finalidade | teto | teto viva | finalidade | finalidade viva | núcleo | núcleo viva | espera média (finalidade) |
|---|---|---|---|---|---|---|---|---|---|
| 09.02.01.001-8 risco cirúrgico | Z136/Z848 | o aceito | 441 | 307 | **441** | **307** | 387 | 261 | 661 |
| 09.02.01.002-6 avaliação cardiológica | Z136/Z848 | o aceito | 502 | 360 | **502** | **360** | 387 | 261 | 590 |
| 09.02.01.003-4 SCC inicial | capítulo I | I20 e I25 | 28.734 | 23.140 | **3.683** | **3.087** | 1.437 | 1.133 | 364 |
| 09.02.01.004-2 SCC progressão I | isquêmicas | o aceito | 2.055 | 1.651 | **2.055** | **1.651** | 2.026 | 1.621 | 376 |
| 09.02.01.005-0 SCC progressão II | isquêmicas | o aceito | 3.310 | 2.911 | **3.310** | **2.911** | 2.026 | 1.621 | 330 |
| 09.02.01.006-9 insuficiência cardíaca | capítulo I | I50 | 50.055 | 29.097 | **6.510** | **4.620** | 2.077 | 1.793 | 763 |
| 09.02.01.007-7 pré-operatório | Z018/Z488/Z489 | o aceito | 136 | 130 | **136** | **130** | 87 | 86 | 235 |
| união das sete (a mesma pessoa em várias) | | | 51.632 | 30.717 | **12.380** | **9.714** | | | |

Na 001-8, 002-6, 004-2, 005-0 e 007-7 a finalidade é igual ao teto: a ficha não separa um CID
mais estreito, ou a lista já é estreita. "Isquêmicas" = I20–I25.

### 1.1 Finalidade principal: as janelas da fila viva e a espera

| OCI | inteira | viva 12 m | **viva 24 m** | viva 36 m | solicitações (inteira / viva 24 m) | espera média | mediana | máxima | média na viva | mediana na viva | devolvidas | 18 anos ou mais | pedido mais antigo |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 001-8 | 441 | 238 | **307** | 367 | 447 / 312 | 661 | 325 | 5.120 | 250 | 198 | 151 | 360 | 18/10/2012 |
| 002-6 | 502 | 300 | **360** | 424 | 519 / 376 | 590 | 257 | 5.120 | 210 | 165 | 344 | 420 | 18/10/2012 |
| 003-4 | 3.683 | 2.659 | **3.087** | 3.366 | 3.931 / 3.323 | 364 | 160 | 5.709 | 173 | 130 | 2.518 | 3.677 | 10/03/2011 |
| 004-2 | 2.055 | 1.233 | **1.651** | 1.988 | 2.097 / 1.691 | 376 | 230 | 2.050 | 231 | 173 | 2.337 | 2.053 | 15/03/2021 |
| 005-0 | 3.310 | 1.909 | **2.911** | 3.243 | 4.314 / 3.908 | 330 | 292 | 2.050 | 263 | 247 | 1.746 | 3.308 | 15/03/2021 |
| 006-9 | 6.510 | 3.764 | **4.620** | 5.204 | 7.259 / 5.132 | 763 | 431 | 5.198 | 223 | 170 | 3.492 | 6.502 | 01/08/2012 |
| 007-7 | 136 | 103 | **130** | 136 | 142 / 136 | 235 | 150 | 934 | 201 | 145 | 33 | 135 | 04/04/2024 |

As OCI 001-8 a 006-9 são de 18 a 130 anos; a 007-7, de 0 a 130. A coluna "18 anos ou mais" é
a idade na solicitação.

### 1.2 As variantes de finalidade

| OCI | recorte | CID | pessoas | viva 24 m | solicitações | espera média | mediana |
|---|---|---|---|---|---|---|---|
| 003-4 | **principal** | I20, I25 | **3.683** | **3.087** | 3.931 | 364 | 160 |
| 003-4 | variante | I20–I25 | 4.450 | 3.750 | 4.772 | 355 | 163 |
| 004-2 | **principal** (= aceito) | I20–I25 | **2.055** | **1.651** | 2.097 | 376 | 230 |
| 004-2 | variante | I20, I25 | 1.466 | 1.162 | 1.491 | 387 | 239 |
| 005-0 | **principal** (= aceito) | I20–I25 | **3.310** | **2.911** | 4.314 | 330 | 292 |
| 005-0 | variante | I20, I25 | 2.696 | 2.396 | 3.639 | 328 | 325 |
| 006-9 | **principal** | I50 | **6.510** | **4.620** | 7.259 | 763 | 431 |
| 006-9 | variante "IC ampliada" | I50, I110, I130, I132, I42, I43 | 7.092 | 4.982 | 7.905 | 776 | 447 |
| 001-8 e 007-7 | **a decidir** (P-08) | consulta de risco cirúrgico, sem recorte de CID | 9.630 | 8.150 | 9.704 | 428 | 423 |

Na consulta de risco cirúrgico sem recorte: viva de 12 meses 4.081 e de 36 meses 9.546 pessoas;
espera máxima 1.465 dias; idade mediana 58. Somada aos exames da 001-8 com Z136/Z848 (ECG e RX),
10.011 pessoas (8.408 na viva). A união das sete com as variantes no lugar da principal (IC
ampliada na 006-9, I20–I25 na 003-4) dá 13.131 pessoas.

### 1.3 O núcleo

| OCI | (a) consultas da OCI com o CID da finalidade | viva | só a consulta específica | (b) todos os exames obrigatórios com fila, ao mesmo tempo | viva | núcleo |
|---|---|---|---|---|---|---|
| 001-8 | risco cirúrgico: 54 | 46 | 54 | ECG: 387 | 261 | **387, pelo (b)** |
| 002-6 | adulto: 41 | 25 | 41 | ECG: 387 | 261 | **387, pelo (b)** |
| 003-4 | adulto + coronária: 1.437 | 1.133 | coronária: 204 | ECG e ergométrico: 15 | 15 | **1.437, pelo (a)** |
| 004-2 | coronária + adulto: 2.026 | 1.621 | coronária: 271 | eco de estresse: 32 | 32 | **2.026, pelo (a)** |
| 005-0 | coronária + adulto: 2.026 | 1.621 | coronária: 271 | as duas cintilografias: 917 | 917 | **2.026, pelo (a)** |
| 006-9 | adulto + insuficiência cardíaca: 2.077 | 1.793 | insuficiência cardíaca: 892 | ECG, ergométrico e Holter: 1 | 0 | **2.077, pelo (a)** |
| 007-7 | risco cirúrgico: 87 | 86 | 87 | não tem obrigatório | — | **87, pelo (a)** |

O (b) conta quem tem pedido, com o CID da finalidade, em cada um dos exames obrigatórios que
têm fila no SISREG (o BNP da 006-9 não tem fila); na viva, cada pedido dentro da janela. No
motor, pela interseção `cns_usuario_solicitacao=P(...)*P(...)`, conferida contra o `Aggr`
(ergométrico e Holter com I*: 382 pelos dois). A consulta adulto é genérica: sem ela, o (a) fica
na consulta específica.

### 1.4 A finalidade fila a fila

Pessoas com o CID da finalidade principal em cada fila da composição; a viva entre parênteses.
(G) = fila genérica, regra 4 do enquadramento.

| fila | 001-8 | 002-6 | 003-4 | 004-2 | 005-0 | 006-9 | 007-7 |
|---|---|---|---|---|---|---|---|
| ELETROCARDIOGRAMA (G) | 387 (261) | 387 (261) | 253 (192) | — | — | 141 (118) | 46 (41) |
| TESTE DE ESFORCO OU TESTE ERGOMETRICO 2 | — | — | 542 (300) | — | — | 77 (65) | — |
| 1. ECOCARDIOGRAFIA … ADULTO (G) | — | 90 (90) | 1.676 (1.676) | — | — | 2.364 (2.364) | — |
| 5. ECOCARDIOGRAFIA DE ESTRESSE ADULTO | — | — | — | 32 (32) | — | — | — |
| HOLTER 24 HORAS (G) | — | — | — | — | — | 2.530 (727) | — |
| CINTILOGRAFIA … ESTRESSE | — | — | — | — | 1.211 (1.211) | — | — |
| CINTILOGRAFIA … REPOUSO | — | — | — | — | 1.038 (1.038) | — | — |
| TORAX : PA E PERFIL (G) | 4 (4) | — | — | — | — | — | 9 (9) |
| CONSULTA EM CARDIOLOGIA - ADULTO (G) | — | 41 (25) | 1.255 (951) | 1.793 (1.388) | 1.793 (1.388) | 1.252 (965) | — |
| CONSULTA EM CARDIOLOGIA - RISCO CIRURGICO | 54 (46) | — | — | — | — | — | 87 (86) |
| CONSULTA EM CARDIOLOGIA - INSUFICIENCIA CARDIACA | — | — | — | — | — | 892 (892) | — |
| CONSULTA EM CARDIOLOGIA - CORONARIA | — | — | 204 (204) | 271 (271) | 271 (271) | — | — |
| **finalidade, união no motor** | **441 (307)** | **502 (360)** | **3.683 (3.087)** | **2.055 (1.651)** | **3.310 (2.911)** | **6.510 (4.620)** | **136 (130)** |
| sem as genéricas, união no motor | 54 (46) | 0 (0) | 745 (503) | 303 (303) | 1.595 (1.595) | 969 (957) | 87 (86) |

As linhas não somam a união: a mesma pessoa pode estar em duas filas.

## 2. O que pesa na leitura

- **A finalidade separa a 003-4 da 006-9.** Com `I*` as duas disputavam a mesma fila (28.929
  pessoas nas duas em 22/10); pela finalidade, 117 estão nas duas (seção 6). A finalidade é 13%
  do teto em cada uma (3.683 de 28.734; 6.510 de 50.055).
- **Na 006-9, o Holter guarda o passado.** Das 2.530 pessoas com I50 no Holter, 727 têm pedido na
  janela viva. A espera média da finalidade é 763 dias na fila inteira e 223 na viva. O eco
  adulto (2.364 com I50) é fila nova, toda da janela viva.
- **Na 005-0, pessoas ≠ fila:** 917 pessoas esperam as duas cintilografias com I20–I25, que a OCI
  junta numa só (4.314 solicitações para 3.310 pessoas). O contratado é a maior origem da
  finalidade (588 de 3.310 pessoas; seção 5).
- **Eco de estresse quase não tem fila:** 69 pendentes (a mais antiga de 08/09/2026), 1.437
  devolvidas, 750 agendadas em 12 meses.
- **Z136/Z848 quase não aparecem no SISREG.** As 387 pessoas do ECG com esses CID são as mesmas
  na 001-8 e na 002-6. No ECG, Z13 (a categoria) é pedida 623 vezes, das quais 387 com Z136.

## 3. Varredura das filas

Refeita no motor sobre todas as filas: 1.570 nomes na tabela de solicitações e 2.247 na de
agendamentos, com os oito recortes de CID na medida (sem recorte, I*, I20–I25, I20 e I25, I50,
IC ampliada, Z136/Z848, Z018/Z488/Z489) e o código SIGTAP. Partiu da de 22/10. **Nenhuma fila
nova com CID das sete OCI**: as que não estavam na lista de 22/10 não têm CID do capítulo I nem
os Z da ficha (ecocardiografia sem doppler, 1 a 2 pendentes; 16. ecocardiografia transtorácica
infantil, 1), ou só têm agendamento (ECOCARDIOGRAMA, 1 agendamento em 12 meses, desde
26/06/2026). Abas 9 e 10 da planilha.

**Entra** (filas específicas da composição, pelo CID da finalidade):

| fila | papel | OCI | fila | pessoas | devolvidas | espera média / mediana | mais antiga | agendadas 12 m |
|---|---|---|---|---|---|---|---|---|
| TESTE DE ESFORCO OU TESTE ERGOMETRICO 2 (02.11.02.006-0) | exame | 003-4, 006-9 (obrigatório) | 3.159 | 3.159 | 2.198 | 831 / 654 | 25/05/2021 | 5.619 |
| 5. ECOCARDIOGRAFIA DE ESTRESSE ADULTO (02.05.01.001-6) | exame | 004-2 (obrigatório) | 69 | 69 | 1.437 | 25 / 27 | 08/09/2026 | 750 |
| CINTILOGRAFIA … ESTRESSE (02.08.01.002-5) | exame | 005-0 (obrigatório) | 1.720 | 1.720 | 152 | 290 / 351 | 29/07/2025 | 365 |
| CINTILOGRAFIA … REPOUSO (02.08.01.003-3) | exame | 005-0 (obrigatório) | 1.484 | 1.484 | 34 | 286 / 364 | 29/07/2025 | 347 |
| CONSULTA EM CARDIOLOGIA - RISCO CIRURGICO | consulta | 001-8, 007-7 | 9.704 | 9.630 | 4.247 | 428 / 423 | 21/10/2022 | 5.816 |
| CONSULTA EM CARDIOLOGIA - INSUFICIENCIA CARDIACA | consulta | 006-9 | 1.105 | 1.105 | 882 | 207 / 186 | 15/01/2025 | 599 |
| CONSULTA EM CARDIOLOGIA - CORONARIA | consulta | 003-4, 004-2, 005-0 | 320 | 320 | 539 | 111 / 110 | 26/12/2025 | 604 |

**A decidir — filas genéricas** (regra 4: no teto aparecem; na finalidade, só com o CID dela; pô-las
na OCI é decisão do usuário):

| fila | papel | OCI | fila | pessoas | devolvidas | espera média / mediana | mais antiga | agendadas 12 m | estudo |
|---|---|---|---|---|---|---|---|---|---|
| ELETROCARDIOGRAMA (02.11.02.003-6) | exame | 001-8, 002-6, 003-4, 006-9 (obrigatório); 007-7 (compatível) | 20.313 | 20.293 | 5.221 | 763 / 346 | 16/08/2010 | 14.129 | viva 15.131; I10 é 88% do I*; idade mediana 58 |
| TORAX : PA E PERFIL (02.04.03.015-3) | exame | 001-8, 007-7 (compatível) | 669 | 669 | 188 | 103 / 103 | 23/03/2026 | 13.009 | fila só de 2026; 75 com I*, 4 com Z136/Z848, 9 com Z018/Z488/Z489 |
| HOLTER 24 HORAS (02.11.02.004-4) | exame | 006-9 (obrigatório) | 36.178 | 36.147 | 3.493 | 1.320 / 1.202 | 27/08/2012 | 2.739 | viva 11.115; estoque de 13,2 anos; I10 6.374, I49 5.640, R00 4.360, I50 2.532 |
| 1. ECOCARDIOGRAFIA BI-DIMENSIONAL COM DOPPLER ADULTO (02.05.01.003-2) | exame | 002-6, 003-4, 006-9 (compatível) | 13.477 | 13.477 | 13.454 | 127 / 117 | 12/05/2025 | 33.740 | fila nova, toda na viva; I10 2.452, I50 2.364, I25 1.178 |
| CONSULTA EM CARDIOLOGIA - ADULTO (03.01.01.007-2) | consulta | 002-6, 003-4, 004-2, 005-0, 006-9 | 11.114 | 11.099 | 8.740 | 480 / 402 | 10/11/2020 | 5.936 | viva 8.250; I10 1.903, I50 1.253, I25 866 |

**A decidir — outros:**

| fila ou recorte | tamanho | estudo |
|---|---|---|
| **CONSULTA EM CARDIOLOGIA - RISCO CIRURGICO, sem recorte de CID**, para a 001-8 (P-08) e a 007-7 | 9.704 na fila, 9.630 pessoas (viva 8.150), 4.247 devolvidas, espera 428 / 423, máxima 1.465; idade mediana 58; 3.414 de 2026; 5.816 agendadas em 12 meses | o CID é o da cirurgia (I83, K80, K40, N40, E66, H25, K42, H02, D25, Z48). A Região de Saúde dela não foi refeita nesta coleta (em 22/10: aba 12 da planilha de lá) |
| fila sem recorte para a 002-6 (CID raro) | seria a consulta adulto inteira, 11.099 pessoas | é a mesma consulta das outras quatro OCI e a maior parte tem CID do capítulo I; não se propõe como fila da 002-6 |
| CID só com a categoria (3 caracteres): Z13, Z84, Z01, Z48 | ECG 338; risco cirúrgico 271 (269 pessoas); Holter 82; eco adulto 71; ergométrico 58; consulta adulto 25; RX 13; cintilografias 6 e 5 | o SISREG aceita a categoria sem o subitem; não se sabe se o Z13 é Z136 nem se o Z48 é Z488/Z489 |
| consultas de subespecialidade com o CID das finalidades | arritmia 439 na fila (I50 25, I20–I25 11); valvulopatia 322 (I50 11); fibrilação atrial 241 (I50 9); marcapasso 507 (I50 9); MACC cardiologia e endocrinologia 239 (I20–I25 17); MACC cardiologia 66 (I20–I25 15); cirurgia cardíaca 48 (I20–I25 16); pós-operatório 29 (I20–I25 19); check list 3; geral 2 | compatíveis pela consulta 03.01.01.007-2, mas não são a finalidade de nenhuma das sete |
| CONSULTA  EM CARDIOLOGIA - PEDIATRIA na 007-7 | 3 com Z018/Z488/Z489 | a 007-7 é de 0 a 130 anos; nas outras seis fica fora pela idade |

**Fica fora:**

| fila | tamanho | motivo |
|---|---|---|
| MONITORIZACAO AMBULATORIAL DE PRESSAO ARTERIAL (MAPA) | 12.715; I50 497; I20 e I25 631 | não compõe nenhuma das sete |
| ANGIOTOMOGRAFIA DAS ARTÉRIAS CORONARIAS ADULTO (nome com espaço não separável) | 1.528; I20 e I25 854; I50 128 | não compõe nenhuma das sete |
| 10. ECODOPPLER DE CAROTIDAS | 4.209; I50 427; I20–I25 715; Z136/Z848 56 | não compõe |
| RM DO CORACAO OU AORTA ADULTO (com e sem contraste) | 166 e 79; I50 51 e 26 | não compõe |
| CINTILOGRAFIA DE MIOCARDIO P/ LOCALIZACAO DE NECROSE | 50; I20–I25 19 | não compõe a 005-0 (só perfusão em estresse e repouso) |
| 7. ECOCARDIOGRAFIA TRANSEOFAGICA ADULTO | 2; 1.052 devolvidas | não compõe |
| 2. ECOCARDIOGRAFIA … INFANTIL; CONSULTA EM CARDIOLOGIA - PEDIATRIA | 1.313 (I50 16) e 1.808 (I* 430) | idade, nas seis OCI de 18 anos ou mais; a 007-7 não tem eco |
| estudo eletrofisiológico (391; I20–I25 59), angioplastia (55; 51), cateterismo (17; 14), tilt test (452), TC de tórax de emergência (895; I20–I25 82, I50 14), polissonografia (8.498; I50 42), geriatria (2.259; I50 42), nefrologia (3.459; I50 13), angiotomografias de aorta, carótidas e tórax | abaixo de 900 com CID das finalidades | não compõem nenhuma das sete |
| consultas de cardiologia sem fila pendente: HIPERTENSO/DIABETICO, > 14 ANOS, CIRURGIA DA AORTA, CIRURGIA CARDIACA - INTERNADOS, PEDIATRIA - POS OPERATORIO | 0 na fila (só devolvidas: 60, 136, 12, 65, 2) | sem fila |
| só na tabela de agendamentos: EGRESSO ICDF (4.641 em 12 meses), PRE - TRANSPLANTE - CARDÍACO (2.033; I50 157), CATETERISMO (7.566), ANGIOPLASTIA (2.324) | 0 na fila | agenda direta, sem solicitação pendente |
| ecocardiografia sem doppler (adulto 2, infantil 1, emergência 1); 16. ecocardiografia transtorácica infantil (1); ECOCARDIOGRAMA (1 agendamento) | 1 a 2 | sem CID das OCI; nomes novos em relação a 22/10, sem tamanho |
| laboratório (hemograma, creatinina, ureia, TGO, TGP, hemoglobina glicosilada, lipidograma) e BNP | 1 a 2 solicitações por exame; BNP sem fila | o laboratório não passa pela regulação do SISREG neste painel |

## 4. Fila a fila

Sem recorte de CID. "Agendadas 12 m" = data do agendamento de 25/10/2025 a 24/10/2026, todos os
CID e status do agendamento. "Anos" = fila ÷ agendadas em 12 meses (**calculado**).

| fila no SISREG (nome interno) | SIGTAP | genérica | fila | fila viva | pessoas | devolvidas | espera média | mediana | máxima | mais antiga | agendadas 12 m | anos (calculado) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ELETROCARDIOGRAMA | 02.11.02.003-6 | sim | 20.313 | 15.131 | 20.293 | 5.221 | 763 | 346 | 5.915 | 16/08/2010 | 14.129 | 1,4 |
| TESTE DE ESFORCO OU TESTE ERGOMETRICO 2 | 02.11.02.006-0 | | 3.159 | 1.662 | 3.159 | 2.198 | 831 | 654 | 1.979 | 25/05/2021 | 5.619 | 0,6 |
| 1. ECOCARDIOGRAFIA BI-DIMENSIONAL COM DOPPLER ADULTO | 02.05.01.003-2 | sim | 13.477 | 13.477 | 13.477 | 13.454 | 127 | 117 | 531 | 12/05/2025 | 33.740 | 0,4 |
| 5. ECOCARDIOGRAFIA DE ESTRESSE ADULTO | 02.05.01.001-6 | | 69 | 69 | 69 | 1.437 | 25 | 27 | 47 | 08/09/2026 | 750 | 0,1 |
| HOLTER 24 HORAS | 02.11.02.004-4 | sim | 36.178 | 11.115 | 36.147 | 3.493 | 1.320 | 1.202 | 5.172 | 27/08/2012 | 2.739 | **13,2** |
| CINTILOGRAFIA DE MIOCARDIO P/ AVALIACAO DA PERFUSAO EM SITUACAO DE ESTRESSE (MINIMO 3 PROJECOES) | 02.08.01.002-5 | | 1.720 | 1.720 | 1.720 | 152 | 290 | 351 | 453 | 29/07/2025 | 365 | **4,7** |
| CINTILOGRAFIA DE MIOCARDIO P/ AVALIACAO DA PERFUSAO EM SITUACAO DE REPOUSO (MINIMO 3 PROJECOES) | 02.08.01.003-3 | | 1.484 | 1.484 | 1.484 | 34 | 286 | 364 | 453 | 29/07/2025 | 347 | **4,3** |
| TORAX : PA E PERFIL | 02.04.03.015-3 | sim | 669 | 669 | 669 | 188 | 103 | 103 | 216 | 23/03/2026 | 13.009 | 0,1 |
| CONSULTA EM CARDIOLOGIA - ADULTO | 03.01.01.007-2 | sim | 11.114 | 8.250 | 11.099 | 8.740 | 480 | 402 | 2.175 | 10/11/2020 | 5.936 | 1,9 |
| CONSULTA EM CARDIOLOGIA - RISCO CIRURGICO | 03.01.01.007-2 | | 9.704 | 8.217 | 9.630 | 4.247 | 428 | 423 | 1.465 | 21/10/2022 | 5.816 | 1,7 |
| CONSULTA EM CARDIOLOGIA - INSUFICIENCIA CARDIACA | 03.01.01.007-2 | | 1.105 | 1.105 | 1.105 | 882 | 207 | 186 | 648 | 15/01/2025 | 599 | 1,8 |
| CONSULTA EM CARDIOLOGIA - CORONARIA | 03.01.01.007-2 | | 320 | 320 | 320 | 539 | 111 | 110 | 303 | 26/12/2025 | 604 | 0,5 |

**Nos recortes** (solicitações na fila; a viva entre parênteses quando difere da inteira):

| fila | I* | I20–I25 | I20 e I25 | I50 | IC ampliada | Z136/Z848 | Z018/Z488/Z489 |
|---|---|---|---|---|---|---|---|
| ELETROCARDIOGRAMA | 11.662 (8.421) | 279 (214) | 253 (192) | 141 (118) | 155 (128) | 388 (261) | 46 (41) |
| TESTE ERGOMETRICO 2 | 1.707 (908) | 559 (309) | 542 (300) | 77 (65) | 87 (73) | 56 (37) | 2 (1) |
| 1. ECO ADULTO | 9.152 | 1.869 | 1.676 | 2.364 | 2.499 | 90 | 13 |
| 5. ECO DE ESTRESSE | 51 | 32 | 31 | 9 | 9 | 1 | 0 |
| HOLTER 24 HORAS | 25.271 (7.519) | 2.854 (1.036) | 2.592 (943) | 2.532 (728) | 2.813 (806) | 99 (42) | 2 (1) |
| CINTILOGRAFIA ESTRESSE | 1.452 | 1.211 | 1.176 | 113 | 117 | 4 | 0 |
| CINTILOGRAFIA REPOUSO | 1.253 | 1.038 | 1.003 | 93 | 98 | 4 | 0 |
| TORAX : PA E PERFIL | 75 | 4 | 3 | 4 | 4 | 4 | 9 |
| CONSULTA ADULTO | 8.097 (6.244) | 1.794 (1.388) | 1.256 (951) | 1.253 (965) | 1.430 (1.102) | 41 (25) | 5 |
| CONSULTA RISCO CIRURGICO | 1.765 (1.446) | 33 (30) | 26 (24) | 29 (28) | 34 (33) | 55 (47) | 87 (86) |
| CONSULTA INSUFICIENCIA CARDIACA | 1.056 | 51 | 37 | 892 | 921 | 0 | 0 |
| CONSULTA CORONARIA | 293 | 271 | 204 | 7 | 8 | 0 | 0 |

Os dez CID mais pedidos por categoria, por fila e por recorte (teto e finalidade), estão no JSON
(`filas.<nome>.recortes.<recorte>.cid_principais`) e na aba 5 da planilha. Pessoas e espera por
recorte: aba 3.

## 5. Por Região de Saúde — finalidade principal, medida fila

Região de Saúde da unidade solicitante. Pessoas, e a fila em solicitações entre parênteses. URD e
Contratado/Credenciado não são Região de Saúde: são unidades de referência e prestadores que
solicitam direto. A linha sem região fica à parte, sem rateio. As linhas de pessoas não somam o
total: quem tem pedido vindo de duas regiões conta nas duas; a fila soma. A viva por região está
na aba 6 da planilha.

| Região | 001-8 | 002-6 | 003-4 | 004-2 | 005-0 | 006-9 | 007-7 |
|---|---|---|---|---|---|---|---|
| Central | 143 (145) | 159 (163) | 219 (237) | 42 (43) | 116 (144) | 243 (268) | 4 (5) |
| Centro-Sul | 66 (66) | 68 (72) | 447 (468) | 270 (272) | 387 (503) | 842 (965) | 20 (21) |
| Leste | 41 (41) | 49 (50) | 233 (250) | 207 (212) | 231 (241) | 450 (492) | 8 (8) |
| Norte | 14 (15) | 12 (13) | 360 (382) | 315 (319) | 381 (418) | 598 (646) | 22 (24) |
| Oeste | 37 (37) | 45 (45) | 330 (357) | 56 (57) | 123 (141) | 569 (627) | 26 (27) |
| Sudoeste | 51 (52) | 45 (49) | 781 (846) | 415 (424) | 528 (585) | 980 (1.075) | 44 (45) |
| Sul | 70 (72) | 98 (101) | 623 (655) | 648 (655) | 690 (712) | 1.013 (1.094) | 9 (9) |
| URD | 0 | 3 (3) | 516 (533) | 103 (103) | 292 (417) | 1.106 (1.186) | 0 |
| Contratado/Credenciado | 0 | 3 (3) | 191 (192) | 2 (2) | 588 (1.139) | 782 (859) | 0 |
| **sem região informada** | **19 (19)** | **20 (20)** | **10 (11)** | **10 (10)** | **13 (14)** | **46 (47)** | **3 (3)** |
| total da finalidade | 441 (447) | 502 (519) | 3.683 (3.931) | 2.055 (2.097) | 3.310 (4.314) | 6.510 (7.259) | 136 (142) |

## 6. Pessoas em mais de uma OCI — finalidade principal

Do motor, sem expor CNS: pares por `cns_usuario_solicitacao=P(A)*P(B)` e a distribuição por
`Aggr(RangeSum(If(Count(A_k)>0,1,0)), cns_usuario_solicitacao)`.

| pessoas em | finalidade principal |
|---|---|
| uma OCI | 9.655 |
| duas | 1.246 |
| três | 1.426 |
| quatro | 53 |
| cinco ou mais | 0 |
| **duas ou mais** (soma das três linhas acima, calculada) | **2.725** |
| **união das sete** | **12.380** (viva 9.714) |

| par | pessoas nas duas |
|---|---|
| 004-2 × 005-0 | 2.026 |
| 003-4 × 005-0 | 1.603 |
| 003-4 × 004-2 | 1.458 |
| 001-8 × 002-6 | 387 |
| 005-0 × 006-9 | 157 |
| 003-4 × 006-9 | 117 |
| 004-2 × 006-9 | 64 |
| 001-8 × 006-9 | 7 |
| 002-6 × 006-9 | 5 |
| 006-9 × 007-7 | 4 |
| os demais onze pares | 0 a 3 cada |

- A 004-2 e a 005-0 têm o mesmo CID (I20–I25) e as mesmas consultas: as 2.026 pessoas do par são
  as do núcleo (a) das duas. Nos exames, quase ninguém espera eco de estresse e cintilografia ao
  mesmo tempo.
- A 003-4 entra nas duas pelas pessoas com I20 ou I25 na consulta adulto e na coronária.
- A 001-8 e a 002-6 dividem o CID e a fila de ECG: 387 pessoas nas duas.

## 7. Diferença para a coleta de 22/10/2026

A de 22/10 (recarga 08:32, método anterior) mediu, em cada OCI, as pessoas "exames + consultas"
com o CID aceito: é o mesmo conjunto do teto de agora (as mesmas filas, o mesmo CID). A
finalidade não existia lá.

| OCI | 22/10: exames + consultas | 25/10: teto | diferença (calculada) | 25/10: finalidade | 25/10: finalidade viva | finalidade ÷ teto (calculado) |
|---|---|---|---|---|---|---|
| 001-8 | 442 | 441 | −1 | 441 | 307 | 100% |
| 002-6 | 504 | 502 | −2 | 502 | 360 | 100% |
| 003-4 | 29.111 | 28.734 | −377 | 3.683 | 3.087 | 13% |
| 004-2 | 2.119 | 2.055 | −64 | 2.055 | 1.651 | 100% |
| 005-0 | 3.413 | 3.310 | −103 | 3.310 | 2.911 | 100% |
| 006-9 | 50.317 | 50.055 | −262 | 6.510 | 4.620 | 13% |
| 007-7 | 132 | 136 | +4 | 136 | 130 | 100% |
| **união das sete** | **51.918** | **51.632** | **−286** | **12.380** | **9.714** | 24% |

Fila a fila, de 22/10 para 25/10 (solicitações na fila, sem recorte): consulta de risco cirúrgico
10.123 → 9.704 (−419); consulta adulto 11.425 → 11.114 (−311); eco adulto 13.676 → 13.477 (−199);
cintilografia de estresse 1.824 → 1.720 (−104); de repouso 1.510 → 1.484 (−26); ergométrico
3.183 → 3.159 (−24); coronária 322 → 320; ECG 20.194 → 20.313 (+119); Holter 36.152 → 36.178
(+26); RX de tórax 653 → 669 (+16); insuficiência cardíaca 1.090 → 1.105 (+15); eco de estresse
67 → 69. Três dias e uma recarga: o teto quase não mudou (−286 na união). A queda da consulta de
risco cirúrgico é a maior; a de 22/10 viu 406 agendamentos dela já marcados a partir daquele dia
em unidades "Privado", e esta coleta não refez essa parte (seção 8).

**O que mudou de verdade foi o método, não a fila:** a união das sete cai de 51.918 (CID aceito)
para 12.380 pela finalidade (9.714 na viva). A 006-9 sai de 50.317 para 6.510 (4.620 na viva) e a
003-4 de 29.111 para 3.683 (3.087). As outras cinco não mudam de tamanho, porque a finalidade é o
próprio CID aceito.

## 8. Lacunas e o que fica a decidir

**A decidir (do usuário):**
- a finalidade de cada OCI (principal ou variante, seção 1.2) e a janela da fila viva (12, 24 ou
  36 meses, seção 1.1);
- se cada fila genérica entra na OCI (ECG, RX de tórax, Holter, eco adulto, consulta adulto), e
  com ela os números sem as genéricas da seção 1.4;
- a consulta de risco cirúrgico sem recorte de CID para a 001-8 (P-08) e a 007-7 (9.630 pessoas);
- os CID só com a categoria (Z13, Z84, Z01, Z48);
- os limites dos alarmes (30%, 5%, 24 meses, 3 anos), propostos em 25/10/2026.

**Lacunas:**
- **Não refeito nesta coleta:** a sobreposição com o convênio 030977/2026 do IEV e as duas
  unidades "Privado" (seção 6 de 22/10), a Região de Saúde da consulta de risco cirúrgico sem
  recorte e a tabela de cirurgias eletivas. Valem os números de 22/10 para isso, com a data de lá.
- **Fichas no formato antigo:** trazem só o CID aceito; a finalidade e as variantes vieram de
  quem chamou a coleta, não da ficha.
- **Validade das solicitações antigas:** Holter desde 2012 e ECG desde 2010 seguem pendentes; o
  painel não diz se a pessoa ainda precisa do exame. A fila viva é a resposta do método, não do
  painel.
- **Exame feito dentro da OCI fora do SISREG:** quando a unidade executa o pacote, os exames
  internos não viram agendamento regulado.
- **BNP e laboratório** sem fila no SISREG: a parte laboratorial da 006-9 (BNP obrigatório) não
  se mede aqui, e o núcleo (b) da 006-9 conta só ECG, ergométrico e Holter.
- **Entrantes por mês:** não coletados (o objeto não pediu); a oferta recente está nas agendadas
  em 12 meses.
- **Data da marcação:** o painel só tem a data do atendimento agendado; "12 meses" é pela data do
  atendimento.
- **Motivo das devolvidas** (eco adulto 13.454, eco de estresse 1.437): o painel não traz.
- **Idade:** é a idade na solicitação (`idade_solicitacao`), não a de hoje.
