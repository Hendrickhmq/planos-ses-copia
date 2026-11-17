# Mapa — exames de cardiologia com os R$ 2 milhões

**Controle interno.** Mapa de 27/10/2026 para o redacao_08: Emenda 41360018/2024, do Senador
Izalci Lucas, individual, federal, ação 2E90; executor Instituto Fazer o Bem, Faz Bem. Parte do
que você disse hoje: os R$ 2 milhões podem ir a exames de cardiologia, e não só a OCI. A escolha
é sua.

Complementa o `estudo_cardiologia_2_milhoes_20261026.md`, que fica como está. Lá os exames eram
os caminhos D a F; aqui eles são o centro.

**As fontes** (as mesmas do estudo de 26/10, no ramo `plano_oci_cardiologia`):
- **a fila:** a coleta do Mapa Social de 25/10/2026, `planos/redacao_08/dados/fontes/mapa_social_20261025.md`;
- **o valor:** o SIGTAP de 10/2026; o eco com o incremento do Anexo I da SAES 4.282/2026;
- **a SES-DF e o mercado:** `planos/redacao_08/dados/precos.md` (22/10/2026), o menor preço de
  lista do DF.

**A conta parte de R$ 1.800.000,00 para produção:** o recurso menos 10% de apoio.

## 1. O que vale para qualquer exame

- **O valor é o do SIGTAP, sem complemento** (LI-002). A SES-DF paga mais pelos mesmos exames
  porque complementa com recurso próprio; a emenda federal não pode.
- **Só o eco tem incremento:** R$ 67,86 vira R$ 160,14 (Anexo I da 4.282). O incremento é da
  habilitação do estabelecimento (38.05; a 38.01 da SAES 4.694 vale só até 31/12/2026), e o
  Instituto não tem CNES (LI-040). Sem CNES, nenhum exame anda, com ou sem incremento (P-03).
- **O núcleo fica com o Instituto** (Decreto 48.727/2026, art. 17, I, e art. 33). A cintilografia,
  que só um serviço de medicina nuclear faz, fica fora.
- **O objeto do ofício.** O Ofício 36 diz "OCI de Cardiologia". Se os exames entram, o plano
  precisa de um ofício que diga exames, pela lição do Ofício 398 da ARINS na emenda de imagem.

## 2. Os exames, um a um

"Zerar a viva" é pagar todos os pedidos dos últimos 24 meses. "O buraco" é o que falta entre o
que a emenda paga e o menor preço de lista do DF, nessa mesma quantidade.

| exame | a emenda paga | a SES-DF paga | mínimo do DF | cobre | fila (viva 24 m) | agendados em 12 m | zerar a viva custa | o buraco |
|---|---|---|---|---|---|---|---|---|
| eco transtorácico adulto, com incremento | R$ 160,14 | R$ 214,50 | R$ 200,00 | **80%** | 13.477 (13.477) | 33.740 | R$ 2.158.206,78 | R$ 537.193,22 |
| eco transtorácico adulto, sem incremento | R$ 67,86 | R$ 214,50 | R$ 200,00 | 34% | 13.477 (13.477) | 33.740 | R$ 914.549,22 | R$ 1.780.850,78 |
| eco de estresse | R$ 165,00 | R$ 264,41 | R$ 585,00, um preço só | 28% | 69 | 750 | R$ 11.385,00 | R$ 28.980,00 |
| Holter 24 h | R$ 30,00 | R$ 82,64 | R$ 117,00 | 26% | 36.178 (11.115) | 2.739 | R$ 333.450,00 | R$ 967.005,00 |
| teste ergométrico | R$ 30,00 | R$ 80,00 | R$ 150,00 | 20% | 3.159 (1.662) | 5.619 | R$ 49.860,00 | R$ 199.440,00 |
| eletrocardiograma | R$ 5,15 | R$ 31,37 | R$ 43,00 | 12% | 20.313 (15.131) | 14.129 | R$ 77.924,65 | R$ 572.708,35 |
| MAPA 24 h | R$ 10,07 | R$ 85,89 | sem preço no DF | 12% do que a SES paga | 12.715 (viva não medida) | — | R$ 128.040,05, a fila inteira | R$ 964.051,30, pelo preço da SES |

- **Holter e eletrocardiograma são as filas mais velhas:** o Holter tem pedidos desde 2012 e um
  estoque de 13 anos de agendamentos; o eletrocardiograma, desde 2010.
- **O eco é fila nova** (desde 05/2025), que a rede atende com 33.740 por ano, e caiu de 16.298
  para 14.721 entre 15 e 26/10 (coleta de imagem de 26/10).
- **Os quatro exames gráficos baratos** (eletrocardiograma, Holter, ergométrico e MAPA) somam
  R$ 589.274,70 para zerar as vivas e um buraco de R$ 2,7 milhões.

## 3. Os cenários

Todos com R$ 1.800.000,00 de produção. "Cobre" é a produção ÷ o custo pelo mínimo de lista.

| cenário | o que compra | unidades | cobre | o buraco | depende de |
|---|---|---|---|---|---|
| **E1. Só eco, com incremento** | 11.240 ecos (83% da fila) | 11.240 | **80%** | R$ 448.026,40 | CNES e 38.05 antes de começar; ofício |
| E2. Todos os exames, nas vivas | eletrocardiograma, ergométrico, eco de estresse, Holter e MAPA zerados; 7.489 ecos com incremento | 48.181 | 37% | R$ 3.030.696,19 | o mesmo do E1, e alguém pagar o buraco |
| E2'. O mesmo, sem incremento | os cinco zerados e o eco inteiro (13.477); sobram R$ 284.791,08 | 54.169 | 25% | R$ 4.513.035,43 | ofício; alguém pagar o buraco |
| E3. Exames e OCI coronária | eletrocardiograma, ergométrico, eco de estresse e Holter zerados nas vivas (sem quem entra na OCI), 3.683 OCI 003-4, 420 OCI 002-6 e 1.625 ecos com incremento | 32.952 | 49% | R$ 1.873.352,80 | o mesmo do E2 |
| E3'. O mesmo, com a 007-7 no lugar do eco | 2.002 OCI 007-7 no lugar dos ecos | 33.329 | 51% | R$ 1.717.389,20 | a P-08; ofício |
| *A de 26/10, só OCI (referência)* | 5.550 OCI 007-7, 3.683 OCI 003-4 e 420 OCI 002-6 | 9.653 | 110% | sobra R$ 159.209,50 | a P-08 |

**Como sai cada número:**
- **E1:** R$ 1.800.000,00 ÷ R$ 160,14 = 11.240 ecos, R$ 1.799.973,60.
- **E2:** as cinco filas custam R$ 600.659,70; o resto, R$ 1.199.340,30, compra 7.489 ecos.
- **E3:** do eletrocardiograma saem 453 pessoas da viva que esperam com o CID da 003-4 (192) ou
  da 002-6 (261); do ergométrico, 300 da 003-4. Elas fazem o exame dentro da OCI.
- **O buraco** usa o mínimo de lista de cada componente (`precos.md`, seção 5): na 003-4, a APAC
  mínima de R$ 301,00; na 002-6, R$ 151,00; na 007-7, R$ 84,45 (consulta de clínico e um exame).

## 4. O que a conta mostra

- **Exame avulso só chega perto de se pagar no eco com incremento.** Os outros pagam de 12% a
  28% do mínimo de lista.
- **Nos exames baratos, o dinheiro sobra e o custo falta.** A emenda paga R$ 5,15 por um
  eletrocardiograma que custa R$ 43,00. Com R$ 1,8 milhão, a tabela compraria 349 mil
  eletrocardiogramas, mas a fila viva tem 15 mil.
- **Quanto mais exame barato entra, maior o buraco.** O E2 zera cinco filas e cobre 37% do custo.
- **Os mesmos exames se pagam dentro da OCI.** A 003-4 paga R$ 270,00 por consulta,
  eletrocardiograma e ergométrico, que custam R$ 301,00 (90%). Avulsos, os dois exames pagariam
  R$ 35,15.
- **O buraco é medido pelo preço de lista.** Com equipe e aparelhos próprios, o custo de um
  eletrocardiograma ou de um Holter pode ficar bem abaixo da lista. Só a planilha de baixo para
  cima do Instituto diz quanto, e o dinheiro para isso é o apoio: R$ 200 mil com 10%, R$ 600 mil
  com 30% (o teto do pt_ses_01: convênio 030989/2026, ISHP, 32,5% do global).
- **Com 30% de apoio, o E1 compra 8.742 ecos** (R$ 1.400.000,00 ÷ R$ 160,14), com um buraco de
  R$ 348.456,12, que cabe nos R$ 600 mil.

## 5. A recomendação

**Se for exame, é o E1: só eco, com incremento.**
- É o único exame que cobre 80% do custo.
- Uma linha só na planilha; uma equipe (cardiologista ecocardiografista e aparelho).
- Não se sobrepõe ao IEV, que não agenda exame no SISREG (`mapeamento_iev_20261026.md`), nem à
  emenda de imagem, de onde o eco saiu.

**Contra o E1, três coisas:**
1. **a habilitação:** sem CNES e sem 38.05 antes do início, o eco cai para R$ 67,86 e cobre 34%;
2. **a fila anda sozinha:** perdeu 1.577 pessoas em onze dias;
3. **o ofício:** precisa dizer exames, ou eco.

**Sem a habilitação, o caminho A de 26/10 continua melhor.** Ele já é um pacote de exames de
cardiologia (eletrocardiograma, ergométrico, eco e laboratório dentro da OCI), cabe no Ofício 36
como está e se paga.

**Holter, eletrocardiograma e MAPA avulsos não se pagam com a emenda sozinha.** O Holter é a
fila mais pedida (36 mil, viva 11 mil), mas zerá-la pela tabela abre um buraco de R$ 967 mil. Só
anda com a SES pondo recurso próprio no complemento (caminho F de 26/10), e o plano não pode
prometer isso.

**Falta, para fechar:**
1. **o CNES do Instituto** e a resposta da SES sobre a 38.05 (P-03, LI-040);
2. **a cotação do eco por volume**, ou o custo dele com equipe própria;
3. **o ofício novo**, se a escolha for exame.
