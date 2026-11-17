# Estudo — as OCI escolhidas e as dos planos aprovados, pelas três medidas da Candanga

**Controle interno.** Estudo de 27/10/2026 para o redacao_08: Emenda 41360018/2024, do Senador
Izalci Lucas, R$ 2 milhões; executor Instituto Fazer o Bem, Faz Bem. Compara, pelas três medidas
da Tabela SUS Candanga (Valor Máximo, Médio e Mediano):
- as quatro OCI escolhidas para a carteira;
- as 15 linhas de OCI dos cinco convênios aprovados.

Complementa o `estudo_comparado_ocis_aprovadas_20261027.md` e a
`argumentacao_apoio_cardiologia_20261027.md`.

**As fontes:**
- **a Candanga:** análise comparativa da SES de 06/08/2026, p. 26 e 27
  (`biblioteca/precos/tabela_sus_candanga/`, no `main`);
- **as planilhas aprovadas:** `estudo/normalizados/pt_ses_01` a `05`;
- **a carteira:** `planos/redacao_08/carteira_ampla_cardiologia.xlsx`, prioridade sugerida, P-08,
  rede de hoje, ninguém no lugar do IEV no risco cirúrgico;
- **o mercado:** `planos/redacao_08/dados/precos.md`, mínimo da APAC no DF.

## 1. As três medidas

O PDF da SES traz, para cada código, as referências de preço que achou: SIGTAP, IVR, PATE, CBHPM,
Tabela SUS Paulista, Deliberações da SES-DF e SIGTAP corrigido pelo IPCA-DF. Dessas referências
saem três resumos:

| medida | o que é | como este estudo a trata |
|---|---|---|
| **Valor Máximo** | a maior das referências da linha | a medida padrão: é a que o PDF destaca em amarelo e o README da tabela manda usar. O Anexo Único ainda tem de confirmar |
| **Valor Médio** | a média das referências da linha | ao lado |
| **Valor Mediano** | o valor do meio das referências da linha | ao lado |

**Nas OCI, só há quatro referências:**
- o SIGTAP;
- o IVR, a 1,5 vez o SIGTAP;
- a Paulista, a 1,5 vez o SIGTAP;
- o IPCA, a cerca de 1,11 vez.

Por isso as três medidas são proporções fixas do SIGTAP: 1,500, 1,278 e 1,306. A GIN1 é a única
exceção, porque não tem a Paulista.

**O apoio que deixa o custo total por OCI igual a cada medida** é 1 − SIGTAP ÷ medida:

| medida | × SIGTAP | apoio que iguala |
|---|---|---|
| Valor Máximo | 1,500 | **33,3%** |
| Valor Mediano | 1,306 | **23,4%** |
| Valor Médio | 1,278 | **21,8%** |

---

## PARTE A — AS OCI ESCOLHIDAS

## 2. As quatro OCI da carteira

| OCI | SIGTAP (o que a emenda paga) | Valor Máximo | Valor Médio | Valor Mediano | referências da linha na Candanga | mínimo da APAC no DF |
|---|---|---|---|---|---|---|
| 09.02.01.003-4 coronária, inicial | R$ 270,00 | **R$ 405,00** | R$ 345,07 | R$ 352,64 | SIGTAP 270,00 · IVR 405,00 · Paulista 405,00 · IPCA 300,28 | R$ 301,00 |
| 09.02.01.002-6 avaliação cardiológica | R$ 200,00 | **R$ 300,00** | R$ 255,61 | R$ 261,22 | SIGTAP 200,00 · IVR 300,00 · Paulista 300,00 · IPCA 222,43 | R$ 151,00 |
| 09.02.01.007-7 pré-operatório (pela 001-8, ver nota) | R$ 130,00 | **R$ 195,00** | R$ 166,15 | R$ 169,79 | SIGTAP 130,00 · IVR 195,00 · Paulista 195,00 · IPCA 144,58 | R$ 111,95 (com cardiologista) |
| 09.02.01.006-9 insuficiência cardíaca | R$ 350,00 | **R$ 525,00** | R$ 447,31 | R$ 457,13 | SIGTAP 350,00 · IVR 525,00 · Paulista 525,00 · IPCA 389,26 | R$ 522,22 |

**Nota sobre a 007-7.** Ela não está na Candanga: foi criada em 06/2026 (SAES 4.104), depois da
base da análise. Este estudo usa a 001-8, que tem o mesmo valor (R$ 130,00), atende a mesma fila
de risco cirúrgico e é a OCI do IEV no Fila Zero. Isso vai à pergunta à SES sobre o Anexo Único.

**A Candanga contra o mercado:**
- **na 003-4 e na 006-9,** o Valor Máximo passa do mínimo da APAC no DF, e o SIGTAP não chega a
  ele;
- **na 002-6 e na 007-7,** até o SIGTAP passa do mínimo da APAC;
- **com a descrição inteira da OCI** (eco, laboratório e retorno), as quatro custam mais que o
  Valor Máximo (`dados/precos.md`).

## 3. O custo por OCI conforme o apoio

O custo total de cada OCI é o SIGTAP ÷ (1 − apoio):

| OCI | 10% | 20% | **30%** | 33,3% |
|---|---|---|---|---|
| 003-4 coronária | R$ 300,00 | R$ 337,50 | **R$ 385,71** | R$ 405,00 |
| 002-6 avaliação cardiológica | R$ 222,22 | R$ 250,00 | **R$ 285,71** | R$ 300,00 |
| 007-7 pré-operatório | R$ 144,44 | R$ 162,50 | **R$ 185,71** | R$ 195,00 |
| 006-9 insuficiência cardíaca | R$ 388,89 | R$ 437,50 | **R$ 500,00** | R$ 525,00 |

**O mesmo custo, dividido por cada medida** (igual nas quatro OCI, porque a proporção é fixa):

| apoio | ÷ Valor Máximo | ÷ Valor Médio | ÷ Valor Mediano |
|---|---|---|---|
| 10% | 74% | 87% | 85% |
| 20% | 83% | 98% | 96% |
| 21,8% | 85% | **100%** | 98% |
| 23,4% | 87% | 102% | **100%** |
| **30%** | **95%** | **112%** | **109%** |
| 33,3% | **100%** | 117% | 115% |

## 4. A carteira inteira, com 30%

Com a prioridade sugerida da planilha:

| base da conta | atendidos (003-4 · 002-6 · 007-7 · 006-9) | produção | apoio | total | Candanga, Valor Máximo | Valor Médio | Valor Mediano |
|---|---|---|---|---|---|---|---|
| realizáveis | 8.781 (1.290 · 152 · 7.034 · 305) | R$ 1.399.870,00 | R$ 600.000,00 | R$ 1.999.870,00 | R$ 2.099.805,00 | R$ 1.789.121,67 | R$ 1.828.338,55 |
| total ÷ a medida | | | | | **95,2%** | **111,8%** | **109,4%** |
| disponíveis | 8.820 (1.693 · 234 · 6.893 · 0) | R$ 1.400.000,00 | R$ 600.000,00 | R$ 2.000.000,00 | R$ 2.100.000,00 | R$ 1.789.288,20 | R$ 1.828.507,47 |
| total ÷ a medida | | | | | **95,2%** | **111,8%** | **109,4%** |

**Com 10%, para comparar:**
- **realizáveis:** 9.657 atendidos e R$ 1.906.470,00 usados, porque sobram R$ 93.530,00. Dá 74,5%
  do Máximo, 87,4% do Médio e 85,5% do Mediano;
- **disponíveis:** 11.896 atendidos. Dá 74,1%, 86,9% e 85,1%.

**Em reais:** com 30%, o convênio inteiro custa R$ 100 mil a menos que a Candanga no Valor Máximo
pelas mesmas OCI. Custa R$ 171 a 211 mil a mais que ela no Médio e no Mediano.

---

## PARTE B — AS OCI DOS PLANOS APROVADOS

## 5. Cada OCI pactuada, pelas três medidas

Custo total por OCI = valor na planilha × o fator do plano (global ÷ produção).

| plano · item | OCI | valor na planilha | custo total por OCI | Valor Máximo | Valor Médio | Valor Mediano | ÷ Máximo | ÷ Médio | ÷ Mediano |
|---|---|---|---|---|---|---|---|---|---|
| pt_ses_01 · 2.1.1 | 09.05.01.003-5 oftalmologia, 9 anos ou mais | R$ 160,00 | R$ 237,02 | R$ 240,00 | R$ 204,49 | R$ 208,97 | 99% | 116% | 113% |
| pt_ses_05 · 2.1.1 | 09.05.01.001-9 oftalmologia, 0 a 8 anos | R$ 200,00 | R$ 238,10 | R$ 300,00 | R$ 255,61 | R$ 261,22 | 79% | 93% | 91% |
| pt_ses_02 · 2.1.1 | 09.03.01.001-1 ortopedia com radiologia | R$ 100,00 | R$ 144,20 | R$ 150,00 | R$ 127,80 | R$ 130,61 | 96% | 113% | 110% |
| pt_ses_04 · 2.2.1 | 09.03.01.001-1 ortopedia com radiologia | R$ 100,00 | R$ 157,66 | R$ 150,00 | R$ 127,80 | R$ 130,61 | 105% | 123% | 121% |
| pt_ses_02 · 2.1.2 | 09.03.01.002-0 com ultrassom | R$ 140,00 | R$ 201,88 | R$ 210,00 | R$ 178,93 | R$ 182,85 | 96% | 113% | 110% |
| pt_ses_04 · 2.2.2 | 09.03.01.002-0 com ultrassom | R$ 140,00 | R$ 220,73 | R$ 210,00 | R$ 178,93 | R$ 182,85 | 105% | 123% | 121% |
| pt_ses_04 · 2.2.3 | 09.03.01.003-8 com tomografia | R$ 230,00 | R$ 362,62 | R$ 345,00 | R$ 293,95 | R$ 300,40 | 105% | 123% | 121% |
| pt_ses_02 · 2.1.3 | 09.03.01.004-6 com ressonância | R$ 360,00 | R$ 519,13 | R$ 540,00 | R$ 460,09 | R$ 470,19 | 96% | 113% | 110% |
| pt_ses_03 · 2.1.1 | 09.03.01.004-6 com ressonância | R$ 360,00 | R$ 524,84 | R$ 540,00 | R$ 460,09 | R$ 470,19 | 97% | 114% | 112% |
| pt_ses_04 · 2.3.1 | 09.02.01.001-8 risco cirúrgico | R$ 130,00 | R$ 204,96 | R$ 195,00 | R$ 166,15 | R$ 169,79 | 105% | 123% | 121% |
| pt_ses_04 · 2.3.2 | 09.02.01.006-9 insuficiência cardíaca (valor trocado) | R$ 250,00 | R$ 394,15 | R$ 525,00 | R$ 447,31 | R$ 457,13 | 75% | 88% | 86% |
| pt_ses_04 · 2.3.3 | 09.02.01.004-2 coronária, eco de estresse (valor trocado) | R$ 350,00 | R$ 551,81 | R$ 375,00 | R$ 319,51 | R$ 326,52 | 147% | 173% | 169% |
| pt_ses_04 · 2.1.1 | 09.06.01.001-2 GIN1 (sem a Paulista) | R$ 88,40 | R$ 139,37 | R$ 132,60 | R$ 104,55 | R$ 92,64 | 105% | 133% | 150% |
| pt_ses_04 · 2.4.1 | 09.04.01.001-5 déficit auditivo, inicial | R$ 100,00 | R$ 157,66 | R$ 150,00 | R$ 127,80 | R$ 130,61 | 105% | 123% | 121% |
| pt_ses_04 · 2.4.2 | 09.04.01.002-3 déficit auditivo, progressão | R$ 150,00 | R$ 236,49 | R$ 225,00 | R$ 191,71 | R$ 195,91 | 105% | 123% | 121% |
| pt_ses_04 · 2.5.1 | 09.01.01.004-9 próstata, progressão | R$ 300,00 | R$ 472,98 | R$ 450,00 | R$ 383,41 | R$ 391,82 | 105% | 123% | 121% |

As OCI de cardiologia do Fila Zero (2.3.2 e 2.3.3) têm os valores trocados na planilha (AC-058).
Pelo SIGTAP certo, as duas ficariam em 105% do Máximo, como as outras do plano.

## 6. Cada plano inteiro, pelas três medidas

Global aprovado ÷ o que a Candanga pagaria pelas mesmas OCI nas mesmas quantidades:

| plano | apoio | global | Candanga Valor Máximo | ÷ Máximo | ÷ Médio | ÷ Mediano |
|---|---|---|---|---|---|---|
| pt_ses_01 (ISHP) | 32,5% | R$ 8.532.671,65 | R$ 8.640.000,00 | 98,8% | 115,9% | 113,4% |
| DOA (IEV) | 30,7% | R$ 16.671.550,00 | R$ 17.341.800,00 | 96,1% | 112,8% | 110,4% |
| DOAR (IEV) | 31,4% | R$ 5.998.920,00 | R$ 6.172.200,00 | 97,2% | 114,1% | 111,6% |
| Fila Zero (IEV) | 36,6% | R$ 8.998.131,20 | R$ 8.575.876,80 | 104,9% | 123,6% | 121,7% |
| pt_ses_05 (ISHP), com a estrutura do pt_ses_01 | 16,0% | R$ 2.000.000,00 | R$ 2.520.000,00 | 79,4% | 93,1% | 91,1% |

---

## PARTE C — LADO A LADO

## 7. O nosso contra os aprovados

| | apoio | custo por OCI ÷ Valor Máximo | ÷ Valor Médio | ÷ Valor Mediano |
|---|---|---|---|---|
| Fila Zero (IEV) | 36,6% | 104,9% | 123,6% | 121,7% |
| pt_ses_01 (ISHP) | 32,5% | 98,8% | 115,9% | 113,4% |
| DOAR (IEV) | 31,4% | 97,2% | 114,1% | 111,6% |
| DOA (IEV) | 30,7% | 96,1% | 112,8% | 110,4% |
| **nosso, com 30%** | **30%** | **95,2%** | **111,8%** | **109,4%** |
| nosso, com 23,4% | 23,4% | 87,0% | 102,1% | 100,0% |
| nosso, com 21,8% | 21,8% | 85,3% | 100,0% | 97,9% |
| pt_ses_05 (ISHP) | 16,0% | 79,4% | 93,1% | 91,1% |
| nosso, com 10% | 10% | 74,1% | 86,9% | 85,1% |

**A mesma OCI de risco cirúrgico, na mesma fila:**

| | valor | custo por OCI | ÷ Máximo (R$ 195,00) | ÷ Médio (R$ 166,15) | ÷ Mediano (R$ 169,79) |
|---|---|---|---|---|---|
| 001-8 do IEV, Fila Zero (36,6%) | R$ 130,00 | R$ 204,96 | 105% | 123% | 121% |
| **nossa 007-7, com 30%** | R$ 130,00 | **R$ 185,71** | **95%** | **112%** | **109%** |

## 8. O que o estudo diz, medida por medida

**Pelo Valor Máximo, a medida que a SES destaca:**
- os quatro aprovados de estrutura própria ficam entre 96% e 105%: no preço da Candanga;
- **o nosso, com 30%, fica em 95%, abaixo de todos e abaixo da tabela;**
- o apoio que iguala é 33,3%, dentro da faixa aprovada (30,7% a 36,6%).

**Pelo Valor Médio:**
- os quatro ficam de 13% a 24% acima da Candanga;
- **o nosso, com 30%, fica 12% acima: menos que todos eles;**
- para ficar exatamente no Médio, o apoio seria de 21,8%.

**Pelo Valor Mediano:**
- os quatro ficam de 10% a 22% acima;
- **o nosso, com 30%, fica 9% acima: menos que todos eles;**
- para ficar exatamente no Mediano, o apoio seria de 23,4%.

**Em qualquer das três medidas, 30% é o menor custo por OCI entre os convênios de estrutura
própria.** O único mais barato é o pt_ses_05, que aproveitou a estrutura de outro.

**Como usar na conversa:**
- **se a SES aceitar o Valor Máximo,** o argumento é "dentro da tabela da SES";
- **se ela usar o Médio ou o Mediano,** o argumento é "mais barato que tudo o que a SES já
  aprovou". Nesse caso, o piso que ela pode propor é de 22% a 23%.

**A conferir:**
1. **o Anexo Único da Candanga:** qual das três medidas é o "Valor Tabela SUS Candanga";
2. **a 007-7:** entra no Anexo, e com qual valor?
