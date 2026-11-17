# Mapa Social da Saúde — fila das sete OCI de cardiologia (09.02.01), recarga de 22/10/2026 08:32

Coleta do agente `mapa-social` para o dossiê do objeto do redacao_08 (Instituto Fazer o Bem,
Faz Bem; emenda 41360018/2024, R$ 2.000.000,00): as OCI 09.02.01.001-8 a 09.02.01.007-7,
com o recorte de CID das fichas do SIGTAP 10/2026 (`sigtap_09020100*_102026.md`). Primeira
coleta desta pasta. Planilha em `mapa_social_20261022.xlsx`; JSON do motor, enquadramento e
script em `mapa_social_20261022_bruto/`.

| campo | conteúdo |
|---|---|
| Fonte | Mapa Social da Saúde – Regulamentação (MPDFT) · Lista de Espera – Exames e Consultas · `https://paineis-ext.mpdft.mp.br/extensions/mapasauderegulamentacao/mapasauderegulamentacao.html` · app Qlik `7edb02fa-f1f5-4ea6-b348-049a4ac2d095` · dados SISREG/DATASUS |
| Última recarga da base | 22/10/2026 08:32:12 (qLastReloadTime 2026-10-22T11:32:12Z) |
| Consulta | 22/10/2026, de 09:06 a 09:20 (relógio do motor) |
| Solicitação mais recente na base | 22/10/2026 (agendamento mais distante: 25/01/2027) |
| Medida | **fila** = os três status: pendente de regulação, corrigida e reenviada para regulação, pendente de regulação por fila de espera. Devolvidas para complementação ficam fora e são contadas à parte |
| Recorte | todos os anos; cada fila fixa na expressão de conjunto pelo nome interno; OCI pelo CID da solicitação (`codigo_cid_solicitado`): Z136 e Z848 (001-8, 002-6); I00–I99 (003-4, 006-9); I20–I25 (004-2, 005-0); Z018, Z488 e Z489 (007-7) |
| Via | Qlik Engine API do próprio painel (evaluateEx e hipercubos de sessão), no navegador embutido |

Pessoas = CNS distintos no conjunto (quem espera por mais de um exame conta uma vez). Espera
em dias, calculada no motor sobre os registros do conjunto. "18+" = pessoas com 18 anos ou
mais na solicitação (seis das sete OCI são de 18 a 130 anos; a 007-7, de 0 a 130).

---

## 1. Fila por OCI

**Enquadramento desta coleta** (proposta para a conversa principal decidir; seção 3): cada
OCI recebe as filas de exame da sua composição que existem no SISREG e as filas de consulta
de cardiologia que servem à sua finalidade, sempre com o CID da ficha.

### 1.1 Exames da composição

| OCI | CID | filas de exame | fila | **pessoas** | 18+ | devolvidas | espera média | mediana | máxima | solicitadas em 2026 |
|---|---|---|---|---|---|---|---|---|---|---|
| **001-8** risco cirúrgico | Z136, Z848 | ECG (obrig.) + RX tórax | 392 | **391** | 310 | 120 | 692 | 309 | 5.117 | 190 |
| **002-6** avaliação cardiológica | Z136, Z848 | ECG (obrig.) + eco transtorácico | 480 | **464** | 382 | 255 | 589 | 233 | 5.117 | 274 |
| **003-4** SCC inicial | I00–I99 | ECG + ergométrico (obrig.) + eco | 22.630 | **21.406** | 21.275 | 12.491 | 538 | 182 | 5.911 | 14.571 |
| · só os obrigatórios | | ECG + ergométrico | 13.307 | 13.139 | 13.041 | 4.370 | 826 | 407 | 5.911 | 5.629 |
| **004-2** SCC progressão I | I20–I25 | eco de estresse (obrig.) | 30 | **30** | 30 | 713 | 21 | 23 | 44 | 30 |
| **005-0** SCC progressão II | I20–I25 | cintilografia estresse + repouso (obrig.) | 2.346 | **1.374** | 1.374 | 74 | 280 | 352 | 450 | 1.043 |
| **006-9** insuficiência cardíaca | I00–I99 | ECG + ergométrico + Holter (obrig.) + eco | 47.889 | **43.224** | 42.948 | 14.948 | 1.076 | 838 | 5.911 | 18.015 |
| · só os obrigatórios | | ECG + ergométrico + Holter | 38.566 | 37.332 | 37.082 | 6.827 | 1.215 | 1.039 | 5.911 | 9.073 |
| **007-7** pré-operatório | Z018, Z488, Z489 | ECG + RX tórax (compatíveis) | 52 | **52** | 51 | 5 | 224 | 130 | 931 | 41 |

### 1.2 Consultas e exames + consultas

| OCI | consultas que entram | consultas: fila | pessoas | devolvidas | espera média | mediana | exames + consultas: fila | **pessoas** | 18+ | devolvidas | espera média | mediana | máxima |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 001-8 | risco cirúrgico | 56 | 55 | 31 | 453 | 490 | 448 | **442** | 361 | 151 | 660 | 330 | 5.117 |
| 002-6 | adulto | 41 | 41 | 88 | 573 | 609 | 521 | **504** | 422 | 343 | 587 | 254 | 5.117 |
| 003-4 | adulto + coronária | 8.691 | 8.634 | 6.527 | 448 | 373 | 31.321 | **29.111** | 28.967 | 19.018 | 513 | 210 | 5.911 |
| 004-2 | coronária + adulto | 2.132 | 2.091 | 1.625 | 394 | 241 | 2.162 | **2.119** | 2.117 | 2.338 | 388 | 238 | 2.047 |
| 005-0 | coronária + adulto | 2.132 | 2.091 | 1.625 | 394 | 241 | 4.478 | **3.413** | 3.411 | 1.699 | 334 | 311 | 2.047 |
| 006-9 | adulto + insuficiência cardíaca | 9.437 | 9.316 | 6.844 | 432 | 349 | 57.326 | **50.317** | 50.028 | 21.792 | 1.002 | 735 | 5.911 |
| 007-7 | risco cirúrgico | 85 | 85 | 28 | 266 | 219 | 137 | **132** | 131 | 33 | 250 | 166 | 931 |
| **as sete, união no motor** | | | | | | | **60.716** | **51.918** | | | | | |
| as sete, só exames (união) | | | | | | | 50.801 | 44.575 | | | | | |

A união não é a soma das linhas: a mesma pessoa está em várias OCI (seção 5).

**O que pesa na leitura:**
- **Z136 e Z848 quase não aparecem no SISREG.** A 001-8 tem 442 pessoas e a 002-6, 504; 387
  estão nas duas, porque a fila de ECG com esses CID é a mesma. A consulta de risco cirúrgico tem 10.123
  solicitações na fila, mas só 56 com Z136/Z848 e 85 com Z018/Z488/Z489: o CID que o
  solicitante põe é o da cirurgia (I839 varizes, 1.048; K80 colelitíase, 1.030; K40 hérnia
  inguinal, 508; N40 próstata, 399; H25 catarata, 361). A demanda de risco cirúrgico existe;
  o recorte pelo CID da ficha é que não a enxerga (seção 3, "a decidir").
- **I00–I99 é o capítulo inteiro, e a hipertensão domina.** Nos exames da 003-4, 13.020 das
  21.406 pessoas têm I10 ou I15 numa solicitação; nos da 006-9, 18.873 de 43.224. No ECG,
  10.157 das 11.584 solicitações com I* são I10.
- **Holter e ECG têm fila antiga.** Holter: 36.152 na fila, a mais antiga de 27/08/2012,
  cerca de 5 mil solicitações por ano desde 2021 ainda pendentes e 2.735 agendadas em 12
  meses. ECG: a mais antiga de 16/08/2010. A espera média da 006-9 (1.076 dias) vem disso.
- **Eco transtorácico adulto é fila nova:** 13.104 das 13.676 são de 2026 (a mais antiga de
  12/05/2025), espera média de 128 dias, 33.864 agendadas em 12 meses e 13.430 devolvidas.
- **Eco de estresse quase não tem fila:** 67 pendentes (a mais antiga de 08/09/2026), 1.436
  devolvidas e 754 agendadas em 12 meses.
- **Na 005-0, pessoas ≠ fila:** 972 pessoas esperam as duas cintilografias (estresse e
  repouso), que a OCI junta numa só. 1.374 pessoas, 2.346 solicitações.

## 2. Fila a fila

Sem recorte, com a contagem em cada recorte de CID ao lado. "Agendadas 12 m" = agendamentos
com data de 22/10/2025 a 21/10/2026, todos os CID, todos os status do agendamento.

| fila no SISREG (nome interno) | SIGTAP da fila | fila | pessoas | devolvidas | espera média | mediana | máxima | mais antiga | I* | I20–I25 | Z136/Z848 | Z018/Z488/Z489 | agendadas 12 m |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ELETROCARDIOGRAMA | 02.11.02.003-6 | 20.194 | 20.174 | 5.221 | 765 | 346 | 5.911 | 16/08/2010 | 11.584 | 277 | 388 | 44 | 14.223 |
| TESTE DE ESFORCO OU TESTE ERGOMETRICO 2 | 02.11.02.006-0 | 3.183 | 3.183 | 2.200 | 823 | 640 | 1.976 | 25/05/2021 | 1.723 | 564 | 56 | 2 | 5.668 |
| 1. ECOCARDIOGRAFIA BI-DIMENSIONAL COM DOPPLER ADULTO | 02.05.01.003-2 | 13.676 | 13.676 | 13.430 | 128 | 120 | 528 | 12/05/2025 | 9.323 | 1.898 | 92 | 13 | 33.864 |
| 5. ECOCARDIOGRAFIA DE ESTRESSE ADULTO | 02.05.01.001-6 | 67 | 67 | 1.436 | 23 | 27 | 44 | 08/09/2026 | 49 | 30 | 1 | 0 | 754 |
| HOLTER 24 HORAS | 02.11.02.004-4 | 36.152 | 36.121 | 3.493 | 1.318 | 1.200 | 5.169 | 27/08/2012 | 25.259 | 2.851 | 99 | 2 | 2.735 |
| CINTILOGRAFIA DE MIOCARDIO … ESTRESSE (MINIMO 3 PROJECOES) | 02.08.01.002-5 | 1.824 | 1.824 | 72 | 281 | 344 | 450 | 29/07/2025 | 1.545 | 1.283 | 4 | 0 | 364 |
| CINTILOGRAFIA DE MIOCARDIO … REPOUSO (MINIMO 3 PROJECOES) | 02.08.01.003-3 | 1.510 | 1.510 | 33 | 286 | 368 | 450 | 29/07/2025 | 1.277 | 1.063 | 4 | 0 | 360 |
| TORAX : PA E PERFIL | 02.04.03.015-3 | 653 | 653 | 188 | 102 | 101 | 213 | 23/03/2026 | 73 | 4 | 4 | 8 | 13.057 |
| CONSULTA EM CARDIOLOGIA - ADULTO | 03.01.01.007-2 | 11.425 | 11.409 | 8.746 | 490 | 419 | 2.172 | 10/11/2020 | 8.395 | 1.860 | 41 | 5 | 5.945 |
| CONSULTA EM CARDIOLOGIA - RISCO CIRURGICO | 03.01.01.007-2 | 10.123 | 10.041 | 4.246 | 435 | 429 | 1.462 | 21/10/2022 | 1.765 | 34 | 56 | 85 | 5.683 |
| CONSULTA EM CARDIOLOGIA - INSUFICIENCIA CARDIACA | 03.01.01.007-2 | 1.090 | 1.090 | 882 | 206 | 189 | 645 | 15/01/2025 | 1.042 | 50 | 0 | 0 | 609 |
| CONSULTA EM CARDIOLOGIA - CORONARIA | 03.01.01.007-2 | 322 | 322 | 538 | 110 | 109 | 300 | 26/12/2025 | 296 | 272 | 0 | 0 | 609 |

Nos recortes, pessoas e fila quase coincidem (no ECG com I*, 11.584 e 11.573). Fila a fila
em cada recorte, com idade, fila de 2026 e solicitação mais antiga: aba 1 da planilha. Fila
por ano da solicitação: aba 5.

## 3. Varredura das filas

Feita na tabela de solicitações (1.572 nomes de fila) e na de agendamentos (2.247 nomes),
com os cinco recortes de CID na medida, e pelo código SIGTAP de cada componente das sete
fichas. Abas 10 e 11 da planilha trazem a varredura inteira.

**Entra** (filas da composição, com o CID da ficha):

| fila | papel | OCI em que entra | por quê |
|---|---|---|---|
| ELETROCARDIOGRAMA | exame | 001-8, 002-6, 003-4, 006-9 (obrigatório); 007-7 (compatível) | ECG 02.11.02.003-6 |
| TESTE DE ESFORCO OU TESTE ERGOMETRICO 2 | exame | 003-4, 006-9 (obrigatório) | 02.11.02.006-0. Fica fora da 001-8 e da 002-6, que não o têm (56 com Z136/Z848) |
| 1. ECOCARDIOGRAFIA … ADULTO | exame | 002-6, 003-4, 006-9 (compatível) | 02.05.01.003-2 |
| 5. ECOCARDIOGRAFIA DE ESTRESSE ADULTO | exame | 004-2 (obrigatório) | 02.05.01.001-6 |
| HOLTER 24 HORAS | exame | 006-9 (obrigatório) | 02.11.02.004-4. Fica fora da 001-8 e da 002-6 (99 com Z136/Z848) |
| CINTILOGRAFIA … ESTRESSE e … REPOUSO | exame | 005-0 (obrigatórias) | 02.08.01.002-5 e 003-3 |
| TORAX : PA E PERFIL | exame | 001-8, 007-7 (compatível) | 02.04.03.015-3 |
| CONSULTA EM CARDIOLOGIA - ADULTO | consulta | 002-6, 003-4, 004-2, 005-0, 006-9 | consulta 03.01.01.007-2, compatível em todas |
| CONSULTA EM CARDIOLOGIA - RISCO CIRURGICO | consulta | 001-8, 007-7 | finalidade da OCI |
| CONSULTA EM CARDIOLOGIA - INSUFICIENCIA CARDIACA | consulta | 006-9 | finalidade da OCI |
| CONSULTA EM CARDIOLOGIA - CORONARIA | consulta | 003-4, 004-2, 005-0 | finalidade da OCI |

**A decidir** (fora da soma até a conversa principal decidir):

| fila ou recorte | tamanho | estudo |
|---|---|---|
| **CONSULTA EM CARDIOLOGIA - RISCO CIRURGICO, sem recorte de CID**, para a 001-8 (e a 007-7) | 10.123 na fila, 10.041 pessoas, 4.246 devolvidas, espera média 435 e mediana 429, máxima 1.462; idade mediana 59; 3.430 de 2026; 5.683 agendadas em 12 meses | o CID é o da cirurgia, não Z136/Z848 nem Z018/Z488/Z489. Região: Central 3.579, Sudoeste 2.726, Norte 1.426, Sul 1.349, Oeste 495, Leste 261, Centro-Sul 229, URD 24, sem região 33 (aba 12). É a fila em que as unidades privadas agendam desde 07/2026 (seção 6) |
| CONSULTA EM CARDIOLOGIA - ADULTO na 001-8 / na 007-7 | 41 com Z136/Z848; 5 com Z018/Z488/Z489 | posta só na 002-6 (avaliação cardiológica); a de risco cirúrgico serve à 001-8 e à 007-7 |
| CONSULTA EM CARDIOLOGIA - RISCO CIRURGICO na 002-6 | 56 com Z136/Z848 | posta só na 001-8 |
| CID só com a categoria (3 caracteres): Z13, Z84, Z01, Z48 | ECG 338 (Z13 228, Z01 59, Z48 51); risco cirúrgico 276 (Z48 213, Z01 53, Z13 10); Holter 82; MAPA 82; eco adulto 70; ergométrico 58; consulta adulto 25; RX 13 | o SISREG aceita a categoria sem o subitem; não se sabe se o Z13 é Z136 nem se o Z48 é Z488/Z489 |
| consultas de subespecialidade com I* | arritmia 348; valvulopatia 266; fibrilação atrial 227; MACC cardiologia e endocrinologia 73; MACC cardiologia 49; marcapasso 43; cirurgia cardíaca 36; pós-operatório 22; geral 2; check list 1 | compatíveis pela consulta 03.01.01.007-2 e pelo CID, mas não são a finalidade de nenhuma das sete (arritmia, válvula, marcapasso, seguimento cirúrgico). Em I20–I25: pós-operatório 18, MACC 17 + 13, cirurgia cardíaca 15, arritmia 11 |
| CONSULTA  EM CARDIOLOGIA - PEDIATRIA na 007-7 | 3 com Z018/Z488/Z489 | a 007-7 é de 0 a 130 anos; nas outras seis fica fora pela idade (mediana 6) |

**Fica fora:**

| fila | tamanho | motivo |
|---|---|---|
| MONITORIZACAO AMBULATORIAL DE PRESSAO ARTERIAL (MAPA) | 12.722; 10.615 com I* | não compõe nenhuma das sete |
| ANGIOTOMOGRAFIA  DAS ARTÉRIAS CORONARIAS ADULTO S/SEDACAO | 1.525; 884 com I20–I25 | não compõe nenhuma das sete |
| CINTILOGRAFIA DE MIOCARDIO P/ LOCALIZACAO DE NECROSE | 50; 19 com I20–I25 | não compõe a 005-0 (só perfusão em estresse e repouso) |
| 7. ECOCARDIOGRAFIA TRANSEOFAGICA ADULTO | 6; 1.043 devolvidas | não compõe nenhuma das sete |
| 2. ECOCARDIOGRAFIA … INFANTIL | 1.340; 177 com I* | idade (0 a 17); a 007-7, que aceita criança, não tem eco |
| CONSULTA  EM CARDIOLOGIA - PEDIATRIA | 1.803; 430 com I* | idade, nas seis OCI de 18 anos ou mais |
| TILT TEST; angiotomografias de aorta, carótidas e tórax; RM e TC cardíaca; estudo eletrofisiológico; angioplastia e cateterismo | 451 no tilt; os demais abaixo de 400 | não compõem nenhuma das sete |
| consultas de cardiologia sem fila pendente: HIPERTENSO/DIABETICO, > 14 ANOS (HIPERTENSAO/DIABETES), CIRURGIA DA AORTA, CIRURGIA CARDIACA - INTERNADOS, PEDIATRIA - POS OPERATORIO | 0 na fila (só devolvidas: 60, 136, 12, 65, 2) | sem fila |
| CONSULTA EM CARDIOLOGIA - EGRESSO ICDF (só na tabela de agendamentos) | 0 na fila; 4.659 agendadas em 12 meses | agenda direta de egressos do ICDF, sem solicitação pendente |
| CONSULTA PRE - TRANSPLANTE - CARDÍACO - GERAL (só agendamentos) | 0 na fila; 2.059 agendadas em 12 meses | transplante; sem fila |
| filas de outras especialidades com CID I* | doppler venoso MMII 8.792 (I83); proctologia 3.611 (I84); ecodoppler de carótidas 3.067; cirurgia vascular 1.704; neurologia 1.266; e outras | não são filas da composição; o I* ali é variz, hemorroida, carótida, AVC |
| filas de outras especialidades com Z136/Z848 ou Z018/Z488/Z489 | ecodoppler de carótidas 56; ecografia de abdome 1 + 8; endoscopia 6; demais abaixo de 7 | não são filas da composição |
| laboratório (hemograma, glicose, creatinina, ureia, TGO, TGP, HbA1c) e BNP | 1 a 5 solicitações por exame; BNP sem fila | o laboratório não passa pela regulação do SISREG neste painel |
| cirurgias eletivas (tabela CE do painel) | 33.686 na fila, 31.830 pessoas; 0 com Z018/Z488/Z489 e 0 com Z136/Z848 | o CID é o da cirurgia; não há como ligar ao pré-operatório pelo CID |

## 4. Por Região de Saúde — medida fila, pessoas

Região de Saúde da unidade solicitante. URD e Contratado/Credenciado não são Região de
Saúde: são unidades de referência e prestadores que solicitam direto. A linha sem região
fica à parte, sem rateio. As linhas não somam o total de pessoas: quem tem solicitação vinda
de duas regiões conta nas duas. A fila em solicitações está na aba 3 da planilha.

**Exames + consultas:**

| Região | 001-8 | 002-6 | 003-4 | 004-2 | 005-0 | 006-9 | 007-7 |
|---|---|---|---|---|---|---|---|
| Central | 143 | 159 | 2.147 | 42 | 116 | 3.152 | 4 |
| Centro-Sul | 66 | 68 | 3.668 | 273 | 392 | 5.231 | 20 |
| Leste | 40 | 48 | 3.274 | 219 | 244 | 5.719 | 7 |
| Norte | 15 | 12 | 2.293 | 315 | 382 | 4.882 | 20 |
| Oeste | 37 | 45 | 3.957 | 54 | 126 | 5.761 | 27 |
| Sudoeste | 51 | 45 | 5.676 | 441 | 556 | 9.922 | 43 |
| Sul | 71 | 100 | 5.063 | 672 | 715 | 8.301 | 9 |
| URD | 0 | 3 | 1.648 | 101 | 294 | 4.570 | 0 |
| Contratado/Credenciado | 0 | 4 | 1.439 | 2 | 611 | 3.443 | 0 |
| Público – Não SES | 0 | 0 | 1 | 0 | 0 | 1 | 0 |
| **sem região informada** | **19** | **20** | **236** | **13** | **17** | **420** | **2** |

**Só exames:**

| Região | 001-8 | 002-6 | 003-4 | 004-2 | 005-0 | 006-9 | 007-7 |
|---|---|---|---|---|---|---|---|
| Central | 136 | 156 | 1.950 | 3 | 77 | 2.945 | 2 |
| Centro-Sul | 61 | 66 | 2.716 | 2 | 126 | 4.335 | 12 |
| Leste | 38 | 42 | 2.242 | 3 | 29 | 4.763 | 2 |
| Norte | 8 | 7 | 1.256 | 6 | 80 | 3.930 | 9 |
| Oeste | 37 | 45 | 3.813 | 10 | 84 | 5.562 | 15 |
| Sudoeste | 29 | 37 | 3.799 | 4 | 125 | 8.165 | 8 |
| Sul | 63 | 84 | 2.584 | 2 | 49 | 6.102 | 4 |
| URD | 0 | 3 | 1.541 | 0 | 196 | 4.261 | 0 |
| Contratado/Credenciado | 0 | 4 | 1.437 | 0 | 609 | 3.416 | 0 |
| **sem região informada** | **19** | **20** | **138** | **0** | **4** | **312** | **0** |

Na 005-0, o contratado é a maior origem (609 de 1.374 pessoas nos exames): a cintilografia é
pedida de dentro do próprio prestador.

## 5. Pessoas em mais de uma OCI

Do motor, sem expor CNS: `Sum(Aggr(If(...), cns_usuario_solicitacao))` sobre o conjunto
"exames + consultas" de cada OCI.

| pessoas em | exames + consultas | só exames |
|---|---|---|
| uma OCI | 22.171 | |
| duas | 27.314 | |
| três | 497 | |
| quatro | 1.932 | |
| cinco | 4 | |
| **duas ou mais** | **29.747** | **22.065** |
| união das sete | 51.918 | 44.575 |

| par | exames + consultas | só exames |
|---|---|---|
| 003-4 × 006-9 | 28.929 | 21.406 |
| 005-0 × 006-9 | 2.476 | 542 |
| 003-4 × 005-0 | 2.392 | 277 |
| 003-4 × 004-2 | 2.095 | 4 |
| 004-2 × 005-0 | 2.091 | 1 |
| 004-2 × 006-9 | 1.935 | 9 |
| 001-8 × 002-6 | 387 | 387 |
| Z136/Z848 × capítulo I (001-8 ou 002-6 com 003-4 a 006-9) | 0 a 31 por par | 0 a 15 |
| 007-7 × as outras | 1 a 20 por par | 0 a 5 |

- As filas de exame da 003-4 (ECG, ergométrico, eco) estão todas na 006-9, com o mesmo CID:
  as 21.406 pessoas dos exames da 003-4 estão todas na 006-9. O que separa as duas é o
  Holter (e o BNP, sem fila no SISREG).
- A 001-8 e a 002-6 dividem o CID e a fila de ECG: as 387 pessoas do ECG com Z136/Z848 estão
  nas duas.
- A 004-2 e a 005-0 dividem o CID e as consultas; nos exames, só 1 pessoa espera eco de
  estresse e cintilografia ao mesmo tempo.
- 386 pessoas esperam ergométrico e Holter (I*) ao mesmo tempo.

## 6. Sobreposição com o convênio 030977/2026 do IEV

O painel traz a unidade executante de cada agendamento (`nome_unidade_executante`, o código
da unidade e o tipo, `regiao_saude_executante`: região da SES, URD, Contratado/Credenciado,
Privado). **Não traz o convênio.** Não há unidade com o nome do IEV.

**Agendamentos em 12 meses (22/10/2025 a 21/10/2026) nas filas do enquadramento, por tipo
de executante, todos os CID:**

| fila | região SES | URD | Contratado/Credenciado | Privado | já marcadas a partir de 22/10/2026 em Privado |
|---|---|---|---|---|---|
| ELETROCARDIOGRAMA | 14.223 | 0 | 0 | 0 | 0 |
| TORAX : PA E PERFIL | 13.057 | 0 | 0 | 0 | 0 |
| TESTE ERGOMETRICO | 0 | 1.694 (HBDF, CRDF) | 3.974 (ICDF 2.422, HUB 1.552) | 0 | 0 |
| ECO ADULTO | 0 | 10.648 (CRDF, HBDF) | 23.216 (ICDF 20.383, HUB 2.833) | 0 | 0 |
| HOLTER | 193 | 124 (HCB) | 2.418 (ICDF 1.528, HUB 890) | 0 | 0 |
| ECO DE ESTRESSE | 0 | 0 | 754 (ICDF) | 0 | 0 |
| CINTILOGRAFIAS | 0 | 0 | 364 + 360 (HUB) | 0 | 0 |
| CONSULTA ADULTO | 5.043 | 80 | 0 | **822** | 73 |
| CONSULTA RISCO CIRURGICO | 3.058 | 688 | 0 | **1.937** | 406 |
| CONSULTA IC | 0 | 609 | 0 | 0 | 0 |
| CONSULTA CORONARIA | 0 | 609 | 0 | 0 | 0 |

ICDF e HUB agendam desde 2009: são a rede contratada antiga, não o convênio de 2026.

**As duas unidades "Privado" com cardiologia** (abas 6 e 7):

| unidade (código no painel) | primeiro agendamento | cardiologia desde | risco cirúrgico | consulta adulto | outras filas que agenda |
|---|---|---|---|---|---|
| CLINICA DE IMAGEM SAMAMBAIA (0366986) | 03/06/2026 | 03/07/2026 | 1.151 até 21/10 + 241 marcadas | 440 + 73 | consultas de ortopedia (joelho, ombro, coluna, pé, quadril) |
| Centro Clinico Ecografico Sobrainho (3031543) | 18/09/2025 | 27/07/2026 | 786 + 165 | 382 + 0 | ortopedia e ressonância magnética |

Por mês do agendamento, nas duas unidades: risco cirúrgico jul/2026 615, ago 240, set 362,
out 1.126; consulta adulto jul 61, ago 150, set 233, out 451 (outubro inclui o que já está
marcado até 31/10). Status do risco cirúrgico, todas as datas: 850 realizadas, 500 faltas,
572 agendadas pendentes de confirmação, 400 autorizadas, 21 canceladas; da consulta adulto:
296 realizadas, 317 faltas, 164 pendentes, 70 autorizadas, 48 canceladas.

**Com o CID das OCI do IEV**, o que essas unidades agendaram em 12 meses é pouco: 001-8
(Z136/Z848) 1 consulta; 004-2 (I20–I25) 174 consultas adulto e nenhum eco de estresse;
006-9 (I*) 821 consultas adulto e nenhum ECG, ergométrico, Holter ou eco. Nenhum exame de
cardiologia foi agendado em unidade "Privado" em 12 meses. Os CID mais comuns no risco
cirúrgico dessas unidades são H25 catarata (541 + 187 H250), Z13 (482), Z10 (210), hérnias
(K42, K43, K40) e Z48 (44).

**O que dá para dizer:** desde 07/2026, duas unidades privadas que também fazem consultas
de ortopedia agendam consulta de cardiologia, a maior parte de risco cirúrgico (1.937 de
risco cirúrgico e 822 de consulta adulto em 12 meses, todos desde julho, e mais 406 e 73 já
marcados). O desenho
(ortopedia mais risco cirúrgico, a partir de meados de 2026) é compatível com o "Fila Zero",
mas **o painel não liga a unidade ao convênio**. Se forem do IEV, o que ele tira da fila
aparece na **consulta de risco cirúrgico sem recorte** (10.123 na fila) e na consulta adulto,
não nos exames nem no recorte de CID das fichas. Os exames da OCI, se feitos dentro da
própria unidade, não passam pelo SISREG e não aparecem.

## 7. Diferença para a coleta anterior

Primeira coleta desta pasta: não há coleta anterior do mesmo objeto. As de agosto de 2026
(`planos/redacao/`, `planos/redacao_02/`) não estão nesta forma.

## 8. Lacunas

- **Convênio da unidade executante:** o painel dá nome curto, código e tipo da unidade, não o
  convênio. Confirmar pelo CNES (0366986 e 3031543) ou com a SES se as duas unidades
  privadas são do IEV.
- **Exame feito dentro da OCI fora do SISREG:** quando a unidade executa o pacote, os exames
  internos não viram agendamento regulado; o painel não mede o que o IEV entrega em exame.
- **CID de 3 caracteres** (Z13, Z84, Z01, Z48): não se sabe se correspondem aos subitens da
  ficha (seção 3).
- **BNP e laboratoriais:** sem fila no SISREG; a parte laboratorial da 006-9 e das outras
  não se mede aqui.
- **Validade das solicitações antigas:** Holter desde 2012 e ECG desde 2010 seguem como
  pendentes; o painel não diz se o paciente ainda precisa do exame.
- **Data da marcação:** o painel só tem a data do atendimento agendado, não o dia em que o
  agendamento foi feito; "12 meses" é pela data do atendimento.
- **Motivo das devolvidas** (eco de estresse 1.436, eco adulto 13.430): o painel não traz.
- **Entrantes por mês:** não coletados nesta rodada (o dossiê escolhe a fila; coletar quando
  o plano dimensionar a produção). A oferta recente está nas agendadas em 12 meses (seção 2
  e aba 8).
- **Idade:** é a idade na solicitação (`idade_solicitacao`), não a de hoje.
