# Estudo comparado — quanto cada OCI dos planos aprovados recebe

**Controle interno.** Estudo de 27/10/2026. Destrincha as 15 linhas de OCI dos cinco convênios
aprovados pela SES-DF em 2026:
- o valor pago na OCI;
- o SIGTAP da época e o de hoje;
- quanto cada OCI custa com o apoio do plano;
- a comparação com a Tabela SUS Candanga e, quando houver pesquisa, com o mercado do DF.

Serve à argumentação do apoio do redacao_08 (`argumentacao_apoio_cardiologia_20261027.md`).

**As fontes:**
- **as planilhas aprovadas:** `estudo/normalizados/pt_ses_01` a `05`, `planilha.csv`, com o
  "Total Geral" de cada uma;
- **o SIGTAP:**
  - o da época é o da análise comparativa da Candanga (agosto de 2026), igual ao das planilhas;
  - o de hoje é o do pacote oficial de 10/2026;
- **a Candanga:** a análise comparativa da SES de 06/08/2026
  (`biblioteca/precos/tabela_sus_candanga/`, no `main`). A medida usada está no quadro abaixo;
- **o mercado:** só onde há pesquisa no acervo:
  - cardiologia: `planos/redacao_08/dados/precos.md`, mínimo da APAC no DF;
  - déficit auditivo: `planos/redacao_05/dados/precos.md`.

**Como se calcula o custo por OCI.** Cada plano tem um fator, global ÷ produção. O custo total de
uma OCI é o valor dela × o fator: o apoio se divide na proporção do valor. Na seção 4 vai também a
outra divisão, com o apoio igual para toda OCI.

> **Qual valor da Candanga este estudo usa: o Valor Máximo, sempre que não disser outro.**
>
> **O que o PDF da SES traz.** Para cada código, várias referências de preço:
> - o SIGTAP;
> - o IVR;
> - o PATE;
> - a CBHPM;
> - a Tabela SUS Paulista;
> - as Deliberações da SES-DF;
> - o SIGTAP corrigido pelo IPCA-DF.
>
> **Dessas referências, saem três resumos:**
> - **Valor Máximo:** a maior referência da linha;
> - **Valor Médio:** a média das referências da linha;
> - **Valor Mediano:** o valor do meio das referências da linha.
>
> **Por que o Máximo:** é o que o PDF destaca em amarelo, e o README da tabela no `main` manda
> usá-lo. O Anexo Único publicado ainda tem de confirmar que ele é o "Valor Tabela SUS Candanga".
>
> **Nas OCI, só há quatro referências:** o SIGTAP, o IVR e a Paulista (as duas a 1,5 vez o
> SIGTAP) e o IPCA (cerca de 1,11 vez). Por isso as três medidas ficam numa proporção fixa do
> SIGTAP:
>
> | medida | quanto vale, nas OCI | apoio que deixa o custo por OCI igual a ela |
> |---|---|---|
> | **Valor Máximo** | **1,5 × SIGTAP** | **33,3%** |
> | Valor Mediano | cerca de 1,31 × SIGTAP | 23,4% |
> | Valor Médio | cerca de 1,28 × SIGTAP | 21,8% |
>
> A GIN1 é a exceção: não tem a Paulista, e o mediano dela é o IPCA (R$ 92,64).
>
> A seção 2.1 mostra as três medidas OCI por OCI, e o que muda em cada plano.

## 1. Os cinco convênios

| plano | convênio | proponente | global | produção (OCI) | apoio | apoio no global | fator | OCI pactuadas | apoio por OCI |
|---|---|---|---|---|---|---|---|---|---|
| pt_ses_01 | 030989/2026 | ISHP | R$ 8.532.671,65 | R$ 5.760.000,00 | R$ 2.772.671,65 | **32,5%** | 1,481 | 36.000 | R$ 77,02 |
| pt_ses_02 | 030975/2026 (DOA) | IEV | R$ 16.671.550,00 | R$ 11.561.200,00 | R$ 5.110.350,00 | **30,7%** | 1,442 | 67.364 | R$ 75,86 |
| pt_ses_03 | 030976/2026 (DOAR) | IEV | R$ 5.998.920,00 | R$ 4.114.800,00 | R$ 1.884.120,00 | **31,4%** | 1,458 | 11.430 | R$ 164,84 |
| pt_ses_04 | 030977/2026 (Fila Zero) | IEV | R$ 8.998.131,20 | R$ 5.707.251,20 | R$ 3.290.880,00 | **36,6%** | 1,577 | 44.101 | R$ 74,62 |
| pt_ses_05 | 031061/2026 | ISHP | R$ 2.000.000,00 | R$ 1.680.000,00 | R$ 320.000,00 | 16,0% | 1,190 | 8.400 | R$ 38,10 |
| **os cinco** | | | **R$ 42.201.272,85** | **R$ 28.823.251,20** | **R$ 13.378.021,65** | **31,7%** | 1,464 | **167.295** | R$ 79,97 |

## 2. Todas as OCI pactuadas

| plano · item | OCI (código certo) | quantidade | valor na planilha | SIGTAP da época | SIGTAP de hoje (10/2026) | custo total por OCI, com o apoio do plano | Candanga, Valor Máximo | custo ÷ Candanga Máximo | mercado mínimo no DF (quanto o valor cobre) |
|---|---|---|---|---|---|---|---|---|---|
| **Oftalmologia** | | | | | | | | | |
| pt_ses_01 · 2.1.1 | 09.05.01.003-5 avaliação inicial, a partir de 9 anos | 36.000 | R$ 160,00 | R$ 160,00 | R$ 160,00 | **R$ 237,02** | R$ 240,00 | 99% | não pesquisado |
| pt_ses_05 · 2.1.1 | 09.05.01.001-9 avaliação inicial, 0 a 8 anos | 8.400 | R$ 200,00 | R$ 200,00 | R$ 200,00 | **R$ 238,10** | R$ 300,00 | 79% | não pesquisado |
| **Ortopedia** | | | | | | | | | |
| pt_ses_02 · 2.1.1 | 09.03.01.001-1 com radiologia | 38.594 | R$ 100,00 | R$ 100,00 | R$ 100,00 | **R$ 144,20** | R$ 150,00 | 96% | não pesquisado |
| pt_ses_04 · 2.2.1 | 09.03.01.001-1 com radiologia | 14.192 | R$ 100,00 | R$ 100,00 | R$ 100,00 | **R$ 157,66** | R$ 150,00 | 105% | não pesquisado |
| pt_ses_02 · 2.1.2 | 09.03.01.002-0 com radiologia e ultrassom | 12.070 | R$ 140,00 | R$ 140,00 | **R$ 216,83** | **R$ 201,88** | R$ 210,00 | 96% | não pesquisado |
| pt_ses_04 · 2.2.2 | 09.03.01.002-0 com radiologia e ultrassom | 7.000 | R$ 140,00 | R$ 140,00 | **R$ 216,83** | **R$ 220,73** | R$ 210,00 | 105% | não pesquisado |
| pt_ses_04 · 2.2.3 | 09.03.01.003-8 com radiologia e tomografia | 539 | R$ 230,00 | R$ 230,00 | **R$ 417,15** | **R$ 362,62** | R$ 345,00 | 105% | não pesquisado |
| pt_ses_02 · 2.1.3 | 09.03.01.004-6 com radiologia e ressonância (a planilha escreve 004-0) | 16.700 | R$ 360,00 | R$ 360,00 | **R$ 616,76** | **R$ 519,13** | R$ 540,00 | 96% | não pesquisado |
| pt_ses_03 · 2.1.1 | 09.03.01.004-6 com radiologia e ressonância (a planilha escreve 004-0) | 11.430 | R$ 360,00 | R$ 360,00 | **R$ 616,76** | **R$ 524,84** | R$ 540,00 | 97% | não pesquisado |
| **Cardiologia** | | | | | | | | | |
| pt_ses_04 · 2.3.1 | 09.02.01.001-8 risco cirúrgico (a planilha escreve 09.02.01.001) | 4.647 | R$ 130,00 | R$ 130,00 | R$ 130,00 | **R$ 204,96** | R$ 195,00 | 105% | R$ 151,00 (86%) |
| pt_ses_04 · 2.3.2 | 09.02.01.006-9 insuficiência cardíaca | 1.000 | **R$ 250,00** (trocado) | R$ 350,00 | R$ 350,00 | **R$ 394,15** | R$ 525,00 | 75% | R$ 522,22 (48% pela planilha; 67% pelo SIGTAP) |
| pt_ses_04 · 2.3.3 | 09.02.01.004-2 coronária, eco de estresse | 900 | **R$ 350,00** (trocado) | R$ 250,00 | R$ 250,00 | **R$ 551,81** | R$ 375,00 | 147% | R$ 693,00 (51% pela planilha; 36% pelo SIGTAP) |
| **Saúde da mulher** | | | | | | | | | |
| pt_ses_04 · 2.1.1 | 09.06.01.001-2 GIN1, avaliação inicial | 3.218 | R$ 88,40 | R$ 88,40 | **R$ 199,95** | **R$ 139,37** | R$ 132,60 | 105% | não pesquisado |
| **Otorrino** | | | | | | | | | |
| pt_ses_04 · 2.4.1 | 09.04.01.001-5 déficit auditivo, avaliação inicial | 6.250 | R$ 100,00 | R$ 100,00 | R$ 100,00 | **R$ 157,66** | R$ 150,00 | 105% | R$ 261,00 (38%) |
| pt_ses_04 · 2.4.2 | 09.04.01.002-3 déficit auditivo, progressão | 5.340 | R$ 150,00 | R$ 150,00 | **R$ 471,57** | **R$ 236,49** | R$ 225,00 | 105% | R$ 534,00 (28% pela planilha; 88% pelo SIGTAP de hoje) |
| **Oncologia** | | | | | | | | | |
| pt_ses_04 · 2.5.1 | 09.01.01.004-9 câncer de próstata, progressão | 1.015 | R$ 300,00 | R$ 300,00 | **R$ 443,54** | **R$ 472,98** | R$ 450,00 | 105% | não pesquisado |

Em negrito, o SIGTAP que mudou depois da aprovação.

## 2.1 As três medidas da Candanga, OCI por OCI

| OCI | Valor Máximo | Valor Médio | Valor Mediano | custo total por OCI (plano) | ÷ Máximo | ÷ Médio | ÷ Mediano |
|---|---|---|---|---|---|---|---|
| 09.05.01.003-5 oftalmologia, 9 anos ou mais | R$ 240,00 | R$ 204,49 | R$ 208,97 | R$ 237,02 (pt_ses_01) | 99% | 116% | 113% |
| 09.05.01.001-9 oftalmologia, 0 a 8 anos | R$ 300,00 | R$ 255,61 | R$ 261,22 | R$ 238,10 (pt_ses_05) | 79% | 93% | 91% |
| 09.03.01.001-1 ortopedia com radiologia | R$ 150,00 | R$ 127,80 | R$ 130,61 | R$ 144,20 (DOA) · R$ 157,66 (Fila Zero) | 96% · 105% | 113% · 123% | 110% · 121% |
| 09.03.01.002-0 com ultrassom | R$ 210,00 | R$ 178,93 | R$ 182,85 | R$ 201,88 (DOA) · R$ 220,73 (Fila Zero) | 96% · 105% | 113% · 123% | 110% · 121% |
| 09.03.01.003-8 com tomografia | R$ 345,00 | R$ 293,95 | R$ 300,40 | R$ 362,62 (Fila Zero) | 105% | 123% | 121% |
| 09.03.01.004-6 com ressonância | R$ 540,00 | R$ 460,09 | R$ 470,19 | R$ 519,13 (DOA) · R$ 524,84 (DOAR) | 96% · 97% | 113% · 114% | 110% · 112% |
| 09.02.01.001-8 risco cirúrgico | R$ 195,00 | R$ 166,15 | R$ 169,79 | R$ 204,96 (Fila Zero) | 105% | 123% | 121% |
| 09.02.01.006-9 insuficiência cardíaca | R$ 525,00 | R$ 447,31 | R$ 457,13 | R$ 394,15 (Fila Zero, valor trocado) | 75% | 88% | 86% |
| 09.02.01.004-2 coronária, eco de estresse | R$ 375,00 | R$ 319,51 | R$ 326,52 | R$ 551,81 (Fila Zero, valor trocado) | 147% | 173% | 169% |
| 09.06.01.001-2 GIN1 | R$ 132,60 | R$ 104,55 | R$ 92,64 | R$ 139,37 (Fila Zero) | 105% | 133% | 150% |
| 09.04.01.001-5 déficit auditivo, inicial | R$ 150,00 | R$ 127,80 | R$ 130,61 | R$ 157,66 (Fila Zero) | 105% | 123% | 121% |
| 09.04.01.002-3 déficit auditivo, progressão | R$ 225,00 | R$ 191,71 | R$ 195,91 | R$ 236,49 (Fila Zero) | 105% | 123% | 121% |
| 09.01.01.004-9 próstata, progressão | R$ 450,00 | R$ 383,41 | R$ 391,82 | R$ 472,98 (Fila Zero) | 105% | 123% | 121% |

**Cada plano inteiro** (o global ÷ o que a Candanga pagaria pelas mesmas OCI nas mesmas quantidades):

| plano | apoio | ÷ Máximo | ÷ Médio | ÷ Mediano |
|---|---|---|---|---|
| pt_ses_01 (ISHP) | 32,5% | **98,8%** | 115,9% | 113,4% |
| DOA (IEV) | 30,7% | **96,1%** | 112,8% | 110,4% |
| DOAR (IEV) | 31,4% | **97,2%** | 114,1% | 111,6% |
| Fila Zero (IEV) | 36,6% | **104,9%** | 123,6% | 121,7% |
| pt_ses_05 (ISHP) | 16,0% | **79,4%** | 93,1% | 91,1% |
| **nosso, com 30%** | 30% | **95,2%** | 111,8% | 109,4% |

**O que muda conforme a medida:**
- **Pelo Valor Máximo,** os quatro aprovados de estrutura própria ficam entre 96% e 105%: no
  preço da Candanga. O nosso, com 30%, fica em 95%, abaixo de todos.
- **Pelo Médio ou pelo Mediano,** os mesmos quatro ficam de 10% a 24% acima da Candanga. O nosso,
  com 30%, fica 9% a 12% acima: ainda abaixo de todos eles.
- **Qualquer que seja a medida, 30% custa por OCI menos que os quatro aprovados.** O que muda é
  se o argumento é "dentro da Candanga" (Máximo) ou "mais barato que o que a SES já aprovou"
  (Médio e Mediano).

## 3. O que a tabela mostra

**1. Nenhum plano pagou acima do SIGTAP na OCI.**
- Todas as linhas trazem o valor da tabela da época.
- A exceção é o Fila Zero, que troca os valores da 006-9 e da 004-2 (AC-058): paga R$ 565 mil
  onde a tabela dá R$ 575 mil.
- **Tudo o que passa do SIGTAP está no apoio.**

**2. Com o apoio, o custo por OCI ficou no Valor Máximo da Candanga.** Pelo Médio e pelo
Mediano, ficou acima (seção 2.1).
- O fator é o mesmo para toda OCI de um plano. Por isso, cada plano tem uma relação só com o
  Valor Máximo:
  - pt_ses_01: 99%;
  - DOA: 96%;
  - DOAR: 97%;
  - Fila Zero: 105%;
  - pt_ses_05: 79%.
- **A SES aprovou, em abril, o preço que fixou como justo em setembro.**

**3. A mesma OCI custa diferente em planos diferentes, conforme o apoio:**

| OCI | DOA (30,7%) | DOAR (31,4%) | Fila Zero (36,6%) | Candanga Máximo |
|---|---|---|---|---|
| 09.03.01.001-1 ortopedia com radiologia | R$ 144,20 | — | R$ 157,66 | R$ 150,00 |
| 09.03.01.002-0 com ultrassom | R$ 201,88 | — | R$ 220,73 | R$ 210,00 |
| 09.03.01.004-6 com ressonância | R$ 519,13 | R$ 524,84 | — | R$ 540,00 |

**4. Os dois do ISHP custam o mesmo por OCI, com apoios diferentes.**
- O pt_ses_01 (32,5% de apoio) sai a R$ 237,02 por OCI; o pt_ses_05 (16%), a R$ 238,10.
- O valor da OCI de 0 a 8 anos é maior (R$ 200,00 contra R$ 160,00), e o apoio menor compensa.
- O pt_ses_05 aproveita a estrutura do pt_ses_01.
- **O que a SES olhou foi o custo total por atendimento, não o percentual.**

**5. O SIGTAP subiu depois da aprovação em seis OCI:**

| OCI | o que mudou |
|---|---|
| ortopedia com ultrassom | R$ 140,00 → R$ 216,83 (+55%) |
| ortopedia com tomografia | R$ 230,00 → R$ 417,15 (+81%) |
| ortopedia com ressonância | R$ 360,00 → R$ 616,76 (+71%) |
| GIN1 | R$ 88,40 → R$ 199,95 (+126%) |
| déficit auditivo, progressão | R$ 150,00 → R$ 471,57 (+214%) |
| câncer de próstata, progressão | R$ 300,00 → R$ 443,54 (+48%) |

- **Nessas seis, o SIGTAP de hoje sozinho já passa do Valor Máximo da Candanga.** A Candanga usou
  o SIGTAP de agosto e não acompanhou (Deliberação 46, art. 5º, § 1º).
- **O próprio Ministério reconheceu que aqueles valores não pagavam o atendimento.**
- **Pelo SIGTAP de hoje, as quantidades do DOA custariam R$ 16,78 milhões só em OCI,** mais que o
  global do convênio (R$ 16,67 milhões). As do DOAR, R$ 7,05 milhões, contra R$ 6,00 milhões de
  global.
- **Na cardiologia, só a 005-0 (cintilografia) subiu**, pela SAES 4.795/2026. As outras seis
  (R$ 130, R$ 200, R$ 250, R$ 270 e R$ 350) continuam no valor com que foram criadas: 2024 e,
  na 007-7, 06/2026.

**6. Onde há preço de mercado, o valor da OCI não paga o atendimento:**
- a 001-8 cobre 86% do mínimo da APAC no DF;
- a déficit auditivo inicial, 38%;
- a eco de estresse, 36%;
- a insuficiência cardíaca, 67%.

O apoio é o que fecha a conta.

## 4. O apoio por OCI, em reais

Se o apoio se dividir por igual entre as OCI de cada plano:

| plano | apoio por OCI |
|---|---|
| pt_ses_01 (oftalmologia) | R$ 77,02 |
| DOA (ortopedia) | R$ 75,86 |
| Fila Zero (dez OCI) | R$ 74,62 |
| DOAR (ressonância) | R$ 164,84 |
| pt_ses_05 (oftalmologia, com a estrutura do pt_ses_01) | R$ 38,10 |

- **Três planos de objeto e tamanho diferentes chegaram a cerca de R$ 75 de apoio por OCI.**
- **O DOAR tem mais porque a ressonância é cara,** e o critério da SES é dar apoio maior a quem
  recebe pouco perto do custo (AC-075).

**O nosso, com teto de 30%:**
- R$ 600 mil de apoio para 8.781 a 8.820 OCI, conforme a base da conta;
- **cerca de R$ 68 por OCI,** abaixo dos R$ 75 dos três.

## 5. Os erros que as planilhas aprovadas carregam

| erro | onde | achado |
|---|---|---|
| código com dígito verificador errado: 09.03.01.004-0, por 004-6 | pt_ses_02 e pt_ses_03 | AC-059 |
| código incompleto: 09.02.01.001, sem o dígito | pt_ses_04 | — |
| valores da 006-9 e da 004-2 trocados | pt_ses_04 | AC-058 |

Nenhum impediu a aprovação. Servem de alerta para conferir código e valor na planilha (LI-003).

## 6. O que isso diz para a cardiologia

| | Fila Zero, mesma OCI (001-8, R$ 130) | nossa 007-7 (R$ 130), com 30% |
|---|---|---|
| custo total por OCI | R$ 204,96 | **R$ 185,71** |
| ÷ Candanga Máximo (R$ 195,00) | 105% | **95%** |
| apoio por OCI | R$ 74,62 | **cerca de R$ 68** |

- **O pedido de 30% fica abaixo de todos os aprovados de estrutura própria,** em percentual, em
  custo por OCI e em reais por OCI.
- **O único abaixo dele é o pt_ses_05,** que não montou estrutura.
- **E as OCI da nossa carteira não tiveram o reajuste que a ortopedia, o otorrino, a ginecologia e
  a próstata tiveram em 09/2026.** O valor delas continua o de quando foram criadas.

**A conferir:**
1. **o Anexo Único da Candanga:** se o Valor Máximo é o valor da tabela;
2. **as portarias que subiram o SIGTAP das seis OCI em 09/2026,** e se o termo de cada convênio
   paga pelo valor vigente ou pelo da planilha. Isso fica para a vigia de normas, que não leu o
   DOU de setembro.
