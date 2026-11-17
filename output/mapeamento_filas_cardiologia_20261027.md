# Mapeamento das filas de cardiologia — os R$ 2 milhões da Emenda 41360018

**Controle interno.** Mapeamento de 27/10/2026 para o redacao_08: Emenda 41360018/2024, do
Senador Izalci Lucas, individual, federal, ação 2E90; executor Instituto Fazer o Bem, Faz Bem.
É o mesmo trabalho que se fez para a imagem (`mapeamento_imagem_20261027.md`). Para cada fila:
- quanto entra;
- quanto a rede agenda e realiza;
- quantos faltam;
- quem mais atende.

Nada daqui foi para documento do plano.

## 1. As coletas

Duas coletas do agente `mapa-social`, recarga do painel de 27/10/2026 12:32, kit novo do ramo
`melhorias/mapa-social`. Estão em `planos/redacao_08/dados/fontes/`, no ramo `plano_oci_cardiologia`:

| coleta | o quê | conferência |
|---|---|---|
| `mapa_social_20261027_panorama.md` | todo exame e consulta de cardiologia com 10 ou mais na fila, com o rumo de cada código: entrantes, oferta pelo mês do agendamento, realizados e faltas | 9/9 |
| `mapa_social_20261027_ocis.md` | as sete OCI pelo CID da finalidade, e a consulta de risco cirúrgico inteira (P-08): entrantes, oferta, faltas, situação e ano | 11/11 |

**As outras fontes:**
- **o IEV:** `mapeamento_iev_20261026.md`;
- **as propostas do Agora Tem Especialistas no DF:** `registros/fontes/pate_propostas_aprovadas_df_20260903.xlsx`,
  posição de 03/09/2026;
- **os planos aprovados:** `estudo/normalizados/pt_ses_01` a `05`.

## 2. Como ler os números

Os termos são os do mapeamento de imagem, seção 3:
- **fila:** total menos devolvidas;
- **viva:** os pedidos dos últimos 24 meses;
- **entram:** pedidos novos por mês;
- **rede agenda:** agendamentos pelo mês em que acontecem, em todas as situações;
- **falta:** faltas ÷ (realizados + faltas).

As médias são dos 12 meses fechados (10/2025 a 09/2026) e dos 3 últimos (07 a 09/2026).

Mais três coisas:
- **realizados** são os agendamentos que o SISREG marca como feitos. Entre agendar e realizar
  ficam a falta, o cancelamento e o que ainda está pendente;
- **anos para zerar** = fila ÷ realizados em 12 meses. É mais duro que o "estoque" do painel,
  que divide pelos agendamentos;
- **nas OCI**, entram e rede agenda contam pedidos em todas as filas da composição com o CID da
  finalidade: a mesma pessoa com consulta e eletrocardiograma conta duas vezes. A fila é em pessoas.

**A fila não segue a conta de entra menos sai.** Parte do que entra é devolvida ao médico (no
eco, 16.446 devolvidas, mais que a fila) ou cancelada, e parte de quem falta volta a pedir.

## 3. As filas das OCI

| fila | pessoas (viva) | entram/mês | rede agenda/mês | realizados/mês | falta | saldo/mês | 3 últimos meses: entram · agenda · realiza |
|---|---|---|---|---|---|---|---|
| **consulta de risco cirúrgico inteira** (P-08: 001-8 e 007-7) | **9.654** (8.170) | 704 | 417 | 215 | **38%** | +287 | **819 · 796 · 399** |
| 006-9 insuficiência cardíaca (I50) | **6.461** (4.570) | 773 | 638 | 415 | 29% | +135 | 798 · 690 · 462 |
| 003-4 coronária, inicial (I20, I25) | **3.644** (3.051) | 588 | 532 | 368 | 25% | +56 | 664 · 589 · 412 |
| 005-0 coronária, cintilografia | **3.313** (2.913) | 342 | 193 | 123 | 28% | +150 | 400 · 250 · 156 |
| 004-2 coronária, eco de estresse | **2.053** (1.648) | 250 | 187 | 118 | 29% | +63 | 295 · 243 · 147 |
| 002-6 avaliação cardiológica (Z13.6, Z84.8) | 417 (299) | 42 | 27 | 17 | 32% | +14 | 46 · 40 · 26 |
| 001-8 risco cirúrgico pelo CID da ficha | 358 (248) | 34 | 22 | 14 | 34% | +12 | 38 · 33 · 21 |
| 007-7 pré-operatório pelo CID da ficha | 136 (130) | 20 | 14 | 9 | 25% | +5 | 23 · 19 · 13 |

As pessoas mudaram pouco desde 25/10: a 006-9 foi de 6.510 a 6.461, a 003-4 de 3.683 a 3.644 e o
risco cirúrgico de 9.630 a 9.654.

**O que a tabela mostra:**
- **Todas as filas crescem.** Em nenhuma a rede agenda o que entra.
- **O risco cirúrgico mudou de ritmo com o IEV.**
  - Até 06/2026, a rede agendava uns 300 por mês nessa fila.
  - Em 07/2026, foram 1.039, e em 10/2026, 1.299, com mais 575 já marcados para novembro.
  - Nos 3 últimos meses, a rede agenda quase o que entra (796 contra 819).
  - **A fila parou de crescer, mas não diminui,** e a falta é a mais alta das OCI: 38%.
    Realizam-se 399 por mês.
- **A 006-9 é a maior fila de OCI e a que tem os pedidos mais velhos:** 1.603 pedidos são de
  antes de 2024, o mais antigo de 2012.
- **A 005-0 é a que mais cresce em proporção:** entram 342 pedidos por mês, e a rede agenda 193.
  O motivo é a cintilografia (seção 4).
- **Na coronária inicial (003-4), a rede quase acompanha:** saldo de +56 por mês. Entram 664
  pedidos por mês nos últimos 3 meses.

## 4. Os exames

| exame (código) | fila (viva) | devolvidas | entram/mês | rede agenda/mês | realizados/mês | falta | saldo/mês | anos para zerar pelo que se realiza |
|---|---|---|---|---|---|---|---|---|
| Holter 24 h (02.11.02.004-4) | **36.198** (11.109) | 3.493 | 560 | 218 | **97** | **49%** | +342 | **31** (a viva, 9,5) |
| eletrocardiograma (02.11.02.003-6) | 20.272 (15.077) | 5.220 | 1.540 | 1.202 | 660 | 42% | +339 | 2,6 |
| eco transtorácico, adulto, infantil e fetal (02.05.01.003-2) | 14.551 (14.551) | 16.446 | 3.582 | 3.364 | 2.326 | 26% | +218 | 0,5 |
| MAPA (02.11.02.005-2) | 12.678 (6.245) | 1.412 | 388 | 210 | 115 | 40% | +179 | 9,2 (a viva, 4,5) |
| teste ergométrico (02.11.02.006-0) | 3.181 (1.682) | 2.198 | 471 | 482 | 286 | 35% | −12 | 0,9 |
| cintilografia de miocárdio, estresse (02.08.01.002-5) | 1.732 (1.732) | 149 | 106 | 31 | 16 | 44% | +75 | 9,3 |
| cintilografia de miocárdio, repouso (02.08.01.003-3) | 1.492 (1.492) | 34 | 84 | 30 | 17 | 42% | +54 | 7,4 |
| eco de estresse (02.05.01.001-6) | 70 (70) | 1.437 | 71 | 63 | 30 | 47% | +9 | 0,2 |
| cateterismo (02.11.02.001-0) | 14 | 878 | 623 | 629 | 463 | 12% | −6 | 0 |

**Fora do universo, mas achados pela varredura com CID cardiológico:**
- **angiotomografia de coronárias** (02.06.02.003-1): 1.531 na fila, espera média de 287 dias.
  É o código da TC de tórax, do plano 4;
- **ecodoppler de carótidas** e **doppler venoso e arterial de membros inferiores**
  (02.05.01.004-0): 4.138, 10.026 e 1.795. São de cirurgia vascular, não de cardiologia.

**O que a tabela mostra:**
- **O Holter é a fila parada:**
  - entram 560 pedidos por mês, e se realizam 97;
  - metade dos agendados falta;
  - pelo que se realiza hoje, a fila viva levaria 9,5 anos para zerar.
- **O eletrocardiograma também cresce:** 42% de falta, 660 realizados por mês contra 1.540
  pedidos. Mas 88% dos pedidos com CID do capítulo I são de hipertensão (I10).
- **O eco não anda sozinho como parecia.** A rede agenda quase o que entra, mas só realiza 2.326
  por mês. A fila fica estável porque a regulação devolve muitos pedidos ao médico (16.446).
  A queda de 15 a 26/10 pode ter sido devolução, e não atendimento.
- **O ergométrico é o único exame em que a rede dá conta:** saldo negativo.
- **A cintilografia** tem três vezes mais entrada que oferta, mas exige medicina nuclear (CNEN).

## 5. As consultas

| consulta | fila (viva) | devolvidas | espera média (dias) | agendadas em 12 m | anos de estoque | CID principais |
|---|---|---|---|---|---|---|
| cardiologia adulto | **11.097** (8.220) | 8.739 | 483 | 5.958 | 1,9 | I10, I50, I25 |
| risco cirúrgico | **9.727** (8.236) | 4.247 | 429 | 5.928 | 1,6 | I83, K80, K40 (CID da cirurgia) |
| pediatria | 1.812 (1.499) | 513 | 486 | 2.722 | 0,7 | Q21, Q25, R01 |
| insuficiência cardíaca | 1.108 (1.108) | 882 | 208 | 599 | 1,8 | I50 |
| marcapasso | 508 (507) | 83 | 56 | 1.986 | 0,3 | Z45 |
| arritmia | 437 (437) | 1.099 | 57 | 1.961 | 0,2 | I49, I48 |
| coronária | 322 (322) | 539 | 112 | 604 | 0,5 | I25, I21, I20 |
| valvulopatia | 321 (320) | 354 | 148 | 293 | 1,1 | I35, I34 |
| fibrilação atrial | 241 (241) | 164 | 173 | 224 | 1,1 | I48 |
| MACC, cardiologia e endocrinologia | 239 (239) | 323 | 118 | 142 | 1,7 | E10, E11 |
| outras três (MACC, cirurgia cardíaca, pós-operatório) | 142 | 555 | 15 a 48 | 1.652 | 0,1 a 0,2 | — |

**A falta nas consultas** não sai por fila: o código é o mesmo para toda consulta
especializada do DF. No conjunto das consultas especializadas, a falta é de **26%**. Nas filas
das OCI, que juntam consulta e exame, vai de 25% a 38% (seção 3).

**O que a tabela mostra:**
- **Duas consultas concentram a espera:** adulto e risco cirúrgico têm 21 mil pedidos e mais
  de um ano de espera média.
- **As subespecialidades andam:** marcapasso, arritmia e coronária esperam menos de 4 meses.

## 6. Quem mais atende essas filas

### 6.1 O IEV (convênio 030977, Fila Zero, até 28/05/2027)

| OCI | contratou | agendou até 26/10 | falta fazer | fila em que entra |
|---|---|---|---|---|
| 001-8 risco cirúrgico | 4.647 | 2.822 (990 atendidas, 499 faltas, 720 por vir) | 1.825 | consulta de risco cirúrgico |
| 006-9 insuficiência cardíaca e 004-2 eco de estresse | 1.000 e 900 | 1.138 consultas adulto (300 atendidas, 314 faltas) | cerca de 760 | consulta de cardiologia adulto |

- **O IEV é a maior parte do salto do risco cirúrgico:** em outubro, ficou com 87% dos
  agendamentos dessa fila.
- **No ritmo de outubro (1.127 agendados), ele termina as 1.825 que faltam até o fim de 2026,**
  antes do fim do convênio.
- **Ele não agenda exame no SISREG.** Holter, eco e eletrocardiograma da OCI dele são feitos
  dentro do pacote. Não tira ninguém das filas da seção 4.

### 6.2 O Agora Tem Especialistas: duas propostas aprovadas com risco cirúrgico

Pela planilha de propostas aprovadas no DF (posição de 03/09/2026):

| proponente | CNES | modalidade | OCI de risco cirúrgico | situação na SES em 03/09 |
|---|---|---|---|---|
| **HAPVIDA** | 797146 | não informada na planilha | **792 por mês** | aguardando a nomeação da comissão do programa (CAC) |
| **Hospital das Clínicas e Pronto Socorro de Fraturas de Ceilândia** | 3025020 | créditos financeiros | **115 por mês** | análise final do plano de trabalho |

- **As duas juntas dão 907 por mês na fila de risco cirúrgico.** É mais do que entra (819).
- **Se começarem, com o IEV a fila esvazia em cerca de um ano.** A 007-7 do caminho A encontraria
  pouca fila em 2027.
- **Se não começarem, a fila volta a crescer quando o IEV acabar.** Sem o IEV, a rede agendava
  de 170 a 460 por mês (10/2025 a 06/2026), e entram 800.
- **Nenhuma das duas propostas tem outra OCI de cardiologia.** A do Hospital de Ceilândia tem
  cirurgias e outras OCI; a da HAPVIDA, cirurgias (varizes, colecistectomia, histerectomia) e
  ortopedia.

### 6.3 O resto

- **Planos aprovados:** só o pt_ses_04 (IEV) tem cardiologia. Os outros quatro são de
  oftalmologia (pt_ses_01 e 05, ISHP) e ortopedia (pt_ses_02 e 03, IEV).
- **Plano 4 (ultrassom e tomografia):** não tem exame de cardiologia. A angiotomografia de
  coronárias usa o código da TC de tórax, que é dele.
- **redacao_07 (imagem, Bancada):** o eco saiu da carteira (seção 6.2 do mapeamento de imagem).
  A cintilografia de miocárdio ficou como "pode entrar", sem prioridade, pela exigência da CNEN.
- **Unidade móvel de cardiologia (SAES 5.086/2026, habilitação 38.14):** é federal, contratada
  pela União. Pode chegar ao DF sem passar pela SES, e o SISREG mostraria a oferta nova.
- **A rede própria e os credenciados da SES:** o painel não separa por estabelecimento nesta
  coleta. A SES paga a rede complementar pela tabela cardiovascular (Deliberação CG-SES 17/2022).

## 7. A falta

| fila | falta |
|---|---|
| Holter | 49% |
| eco de estresse | 47% |
| cintilografia | 42% a 44% |
| eletrocardiograma | 42% |
| MAPA | 40% |
| risco cirúrgico | **38%** |
| ergométrico | 35% |
| OCI 001-8 e 002-6 (CID da ficha) | 32% a 34% |
| OCI 004-2, 005-0 e 006-9 | 28% a 29% |
| eco transtorácico | 26% |
| consultas especializadas do DF | 26% |
| OCI 003-4 e 007-7 | 25% |
| cateterismo | 12% |

- **Na cardiologia, um em cada três agendados falta.** Nos exames gráficos baratos, quase metade.
- **No IEV, a falta é maior que na rede:** 34% no risco cirúrgico (499 de 1.489) e 51% na
  cardiologia adulto (314 de 614).
- **Para o plano, é controle interno.** Pela sua decisão de 21/10, o plano não traz taxa de falta
  nem oferta acima da meta. Na execução, ela decide o tamanho da agenda: 5.550 OCI realizadas
  com 38% de falta pedem uns 9 mil agendamentos.

## 8. O que muda nos caminhos

**Caminho A (007-7, 003-4 e 002-6):**
- **a 003-4** continua firme: a fila cresce devagar (+56 por mês), ninguém mais atende, e as
  3.644 pessoas de hoje se repõem;
- **a 002-6** é pequena (417) e também cresce;
- **a 007-7 depende de duas coisas,** e não só da P-08:
  - se a HAPVIDA e o Hospital de Ceilândia vão executar;
  - quando. Com os dois, a fila do risco cirúrgico pode sumir antes do nosso convênio. Sem eles,
    ela volta a crescer depois de 05/2027, quando o IEV sai, e a 007-7 chega na hora certa.

**E1 (só eco):** a fila não anda sozinha como o estudo de 26/10 dizia.
- A rede realiza 2.326 por mês e entram 3.582. A fila fica parada pela devolução ao médico.
- Os 11.240 ecos são uns 5 meses do que a rede realiza.
- Continua dependendo da habilitação e do ofício.

**A 006-9 volta a ser candidata:**
- é a maior fila de OCI (6.461) e cresce 135 por mês;
- tem os pedidos mais velhos;
- o IEV só atende 1.000 delas.

Contra ela, continua o custo: o SIGTAP paga 67% do mínimo da APAC no mercado.

**O Holter é a fila mais necessitada e a mais difícil.** Entram 560 por mês, a rede realiza 97 e
metade falta. A emenda paga R$ 30,00 por exame. Dentro da 006-9, ele vem no pacote.

## 9. O que falta

1. **Perguntar à SES:**
   - se a HAPVIDA e o Hospital de Ceilândia já começaram a OCI de risco cirúrgico, ou quando
     começam;
   - se a fila do risco cirúrgico pode ir à 007-7 (P-08).
2. **Ver no painel quem agenda o risco cirúrgico por estabelecimento,** para saber se os dois já
   aparecem. Esta coleta não separou por unidade.
3. **A falta por consulta:** o kit mede a falta por código, e a consulta tem um código só para
   todas as especialidades. Nas OCI ela sai junto com os exames. Medir a consulta sozinha pede
   uma mudança no kit.
4. **Pessoas que entram por mês:** o painel conta pedidos, não pessoas novas.
