# Argumentação — por que pedir um custo de apoio maior na cardiologia

**Controle interno.** Material de 27/10/2026 para você estudar e conversar com a SES-DF sobre o
teto do apoio do redacao_08: Emenda 41360018/2024, do Senador Izalci Lucas, R$ 2 milhões;
executor Instituto Fazer o Bem, Faz Bem. Trava F-08 e pendência P-05.

Substitui, como argumento, o `estudo_custo_apoio_cardiologia_20261027.md`. Aquele usava o valor
mediano da Candanga; o README da tabela no `main` diz que o valor destacado pela SES é o
**Valor Máximo**, e este material usa ele.

> **A medida da Candanga, sempre:**
> - **Valor Máximo:** a maior das referências da linha. É o padrão deste material.
> - **Valor Médio:** a média das referências.
> - **Valor Mediano:** o valor do meio delas.
>
> As referências de cada linha são SIGTAP, IVR, PATE, CBHPM, Tabela SUS Paulista, Deliberações e
> IPCA-DF. Nas OCI de cardiologia, as três medidas valem 1,5, cerca de 1,28 e cerca de 1,31 vez o
> SIGTAP. Onde a medida não for o Máximo, o texto diz qual é. O estudo comparado
> (`estudo_comparado_ocis_aprovadas_20261027.md`, seção 2.1) traz as três, OCI por OCI.

**Não vai ao plano.** O plano não traz "custo acessório", percentual de apoio nem o motivo interno
(`metodo/comum.md`, regra 12). Lá, cada linha de apoio se justifica sozinha (LI-017).

---

## 1. O pedido

**Teto de 30% do global para o apoio.**

Com 30%, o convênio custa por OCI **95% do que a Tabela SUS Candanga pagaria a um prestador
privado pelas mesmas OCI.**
- Os convênios que a SES já aprovou ficaram entre 96% e 105%.
- A exceção é um que aproveitava a estrutura de outro.

## 2. A Candanga é o preço justo que a própria SES fixou

A **Lei distrital 7.897/2026** e a **Deliberação CG-SES 46/2026** criaram a Tabela SUS Candanga.

**O que a lei diz:**
- **finalidade** (art. 2º): assegurar "a qualidade do atendimento, o equilíbrio
  econômico-financeiro na prestação dos serviços e a preservação do valor real" da remuneração;
- **mercado** (art. 4º, § 4º): a tabela é revista para "manter valores compatíveis com o
  mercado";
- **teto** (art. 6º): é vedado fixar remuneração em contratos ou convênios complementares ao SUS
  em desconformidade com a Candanga, ou reajustar acima dela;
- **quem paga a diferença** (art. 4º, § 1º): o SIGTAP, financiado com recurso federal, mais a
  complementação do DF, com recurso próprio.

**O que a Deliberação 46 diz:**
- **a quem vale** (art. 3º): a tabela é a "referência remuneratória para os contratos, convênios,
  credenciamentos e demais instrumentos" da participação complementar;
- **o que é a diferença** (art. 4º, § 5º): a diferença sobre o SIGTAP é a "complementação
  distrital".

**O que isso quer dizer, em uma frase:** a SES-DF declarou, por lei e por deliberação, que o preço
justo de cada procedimento é o da Candanga, e não o do SIGTAP.

## 3. O que a Candanga paga pelas nossas OCI

Valores da análise comparativa da SES de 06/08/2026, p. 26
(`biblioteca/precos/tabela_sus_candanga/`, no `main`):

| OCI | SIGTAP (o que a emenda paga) | Candanga, Valor Máximo | diferença |
|---|---|---|---|
| 09.02.01.001-8 risco cirúrgico (a 007-7 tem o mesmo valor e ainda não está na tabela) | R$ 130,00 | **R$ 195,00** | +50% |
| 09.02.01.002-6 avaliação cardiológica | R$ 200,00 | **R$ 300,00** | +50% |
| 09.02.01.003-4 coronária, inicial | R$ 270,00 | **R$ 405,00** | +50% |
| 09.02.01.006-9 insuficiência cardíaca | R$ 350,00 | **R$ 525,00** | +50% |

- **Em todas as OCI de cardiologia, a Candanga vale 1,5 vez o SIGTAP.** Não importa a mistura que
  a carteira tiver.
- **O Valor Máximo é o que o PDF da SES destaca em amarelo.** O Anexo Único publicado ainda tem de
  confirmar que ele é o "Valor Tabela SUS Candanga".
- **Pelo Valor Mediano**, a diferença seria de +31%; **pelo Valor Médio**, de +28%.

**A emenda federal não pode pagar esses 50% dentro da OCI** (LI-002; Lei 7.897, art. 4º, § 1º).
Então a única forma de o executor chegar perto do preço que a SES reconhece como justo é a
estrutura do convênio: o apoio.

## 4. A conta de equivalência

O custo total de cada OCI no convênio é o SIGTAP ÷ (1 − apoio). Comparado com a Candanga:

| apoio no global | custo total por OCI ÷ Valor Máximo | ÷ Valor Mediano | ÷ Valor Médio |
|---|---|---|---|
| 10% | 74% | 85% | 87% |
| 20% | 83% | 96% | 98% |
| 21,8% | 85% | 98% | 100% |
| 23,4% | 87% | 100% | 102% |
| **30%** | **95%** | 109% | 112% |
| 33,3% | 100% | 115% | 117% |

**Com 33,3%, o convênio custa exatamente o Valor Máximo.** Com 30%, fica 5% abaixo dele: abaixo do
que a lei põe como teto (art. 6º).

## 5. Os planos que a SES já aprovou

Os cinco convênios de OCI do acervo, com o global e a produção da planilha aprovada (`estudo/normalizados/pt_ses_0X/planilha.csv`):

| plano · convênio · proponente | objeto | valor médio por OCI | apoio no global | custo total por OCI | Valor Máximo da mesma carteira | global ÷ Valor Máximo |
|---|---|---|---|---|---|---|
| pt_ses_01 · 030989/2026 · ISHP | OCI oftalmologia, a partir de 9 anos (36.000) | R$ 160,00 | **32,5%** | R$ 237,02 | R$ 240,00 | **98,8%** |
| pt_ses_02 · 030975/2026 (DOA) · IEV | três OCI de ortopedia (67.364) | R$ 171,62 | **30,7%** | R$ 247,48 | R$ 257,43 | **96,1%** |
| pt_ses_03 · 030976/2026 (DOAR) · IEV | OCI ortopedia com ressonância (11.430) | R$ 360,00 | **31,4%** | R$ 524,84 | R$ 540,00 | **97,2%** |
| pt_ses_04 · 030977/2026 (Fila Zero) · IEV | dez OCI, três delas de cardiologia (44.101) | R$ 129,41 | **36,6%** | R$ 204,03 | R$ 194,46 | **104,9%** |
| pt_ses_05 · 031061/2026 · ISHP | OCI oftalmologia, 0 a 8 anos (8.400) | R$ 200,00 | 16,0% | R$ 238,10 | R$ 300,00 | 79,4% |
| **nosso, com teto de 30%** | **OCI de cardiologia** | **R$ 151 a R$ 184** | **30%** | **SIGTAP × 1,43** | **SIGTAP × 1,5** | **95,2%** |

"Global ÷ Valor Máximo" é o global aprovado dividido pelo que a Candanga, no Valor Máximo, pagaria
pelas mesmas OCI nas mesmas quantidades.

**Pelas outras duas medidas** (global ÷ Valor Médio · ÷ Valor Mediano):

| plano | ÷ Valor Médio | ÷ Valor Mediano |
|---|---|---|
| pt_ses_01 | 115,9% | 113,4% |
| DOA | 112,8% | 110,4% |
| DOAR | 114,1% | 111,6% |
| Fila Zero | 123,6% | 121,7% |
| pt_ses_05 | 93,1% | 91,1% |
| **nosso, com 30%** | **111,8%** | **109,4%** |

Pelo Médio e pelo Mediano, os aprovados de estrutura própria ficam acima da Candanga, e o nosso
também. Em qualquer medida, porém, o nosso custa menos por OCI que os quatro.

**O que a tabela mostra:**
- **Quatro dos cinco aprovados custam entre 96% e 105% do Valor Máximo da Candanga.** A SES
  aprovou em abril de 2026, antes de a tabela existir, o mesmo nível de preço que ela fixou como
  justo em setembro.
- **O apoio aprovado ficou entre 30,7% e 36,6%** nos quatro. A conta da seção 4 dá 33,3% para
  chegar ao Máximo: é o mesmo número.
- **O único com 16% é o pt_ses_05,** que, segundo o próprio plano, aproveita a estrutura que o
  ISHP já tinha montado para o pt_ses_01. O Instituto Fazer o Bem não tem estrutura para
  aproveitar (seção 7).
- **Pedir 30% é pedir menos que qualquer um dos quatro.**

## 6. O mesmo atendimento: as OCI de cardiologia do Fila Zero

O convênio 030977/2026 do IEV (pt_ses_04, itens 2.3.1 a 2.3.3) executa três OCI de cardiologia,
com o fator de apoio do plano (global ÷ produção = 1,577):

| OCI | valor na planilha | custo total com o apoio do plano | Candanga Máximo | custo ÷ Candanga |
|---|---|---|---|---|
| 09.02.01.001-8 risco cirúrgico (4.647) | R$ 130,00 | R$ 204,96 | R$ 195,00 | 105% |
| 09.02.01.006-9 insuficiência cardíaca (1.000) | R$ 250,00 na planilha (o SIGTAP é R$ 350,00) | R$ 394,15 | R$ 525,00 | 75% |
| 09.02.01.004-2 coronária, eco de estresse (900) | R$ 350,00 na planilha (o SIGTAP é R$ 250,00) | R$ 551,81 | R$ 375,00 | 147% |

- **A planilha do Fila Zero troca os valores da 006-9 e da 004-2** (AC-058). Pelo SIGTAP certo,
  as duas ficariam em 105% da Candanga, como a 001-8.
- **A 001-8 do IEV tem o mesmo valor da nossa 007-7 (R$ 130,00) e usa a mesma fila de risco
  cirúrgico.** A SES aprovou para ela um custo total de R$ 204,96 por OCI.
- **Com 30%, a nossa 007-7 custaria R$ 185,71:** 9% a menos que a do IEV, e abaixo da Candanga.

## 7. Por que o nosso convênio precisa de apoio

1. **O executor começa do zero:**
   - sem CNES (nem a matriz no RJ, nem a filial no DF, de 25/08/2026);
   - sem unidade no DF;
   - sem equipamento;
   - primeiro convênio.

   O SIGTAP paga o atendimento num estabelecimento que já funciona. Não paga montar local,
   cadastro, responsável técnico, eletrocardiógrafo, ergômetro e Holter, regulação, agendamento e
   prestação de contas mensal. A ação 2E90 é de custeio: o equipamento vai por locação.
2. **Duas das OCI pagam menos que o atendimento mínimo no DF** (obrigatórios e uma consulta, pelo
   menor preço de lista; `dados/precos.md`):
   - a 003-4 cobre 90%;
   - a 006-9 cobre 67%.

   Com a descrição inteira da OCI, todas ficam entre 37% e 46%.
3. **O critério da SES é esse** (AC-075, contato de 27/09/2026): o apoio aceito sobe quando o
   procedimento paga mal. A carteira vale de R$ 151 a R$ 184 por OCI, a faixa do pt_ses_01 e do
   DOA (30,7% a 32,5%).

## 8. A resposta à crítica do MPCDF

Na representação contra os convênios do IEV (Representação 31/2026, TCDF 00600-00005805/2026-19;
CT-002), o MPCDF disse:
- que no credenciamento a SES pagaria a OCI pelo SIGTAP, "já com todos os custos";
- que os convênios custavam R$ 10,3 milhões a mais.

Com a Candanga, a conta é outra:

| convênio | global | credenciamento pelo SIGTAP (a conta do MPCDF) | credenciamento pela Candanga, Máximo | convênio contra a Candanga |
|---|---|---|---|---|
| DOA (030975) | R$ 16.671.550,00 | R$ 11.561.200,00 | R$ 17.341.800,00 | **R$ 670.250,00 mais barato** |
| DOAR (030976) | R$ 5.998.920,00 | R$ 4.114.800,00 | R$ 6.172.200,00 | **R$ 173.280,00 mais barato** |
| Fila Zero (030977) | R$ 8.998.131,20 | R$ 5.707.251,20 | R$ 8.575.876,80 | R$ 422.254,40 mais caro |

- **Pela tabela que a própria SES fixou, dois dos três convênios do IEV custam menos do que um
  credenciado custaria.**
- **A "economia" do credenciamento só existe se o credenciado aceitar o SIGTAP puro**, e a Lei
  7.897 diz que ele recebe a Candanga.
- **O nosso pedido fica abaixo dos três:** 95,2% da Candanga.

## 9. O preço de um apoio maior

Mais apoio é menos produção. Com a carteira sugerida e a P-08 (`carteira_ampla_cardiologia.xlsx`):

| apoio | produção | atendidos (realizáveis, rede de hoje) | atendidos (disponíveis, rede de hoje) |
|---|---|---|---|
| 10% | R$ 1.800.000 | 9.657 | 11.896 |
| 20% | R$ 1.600.000 | 9.352 | 10.358 |
| **30%** | **R$ 1.400.000** | **8.781** | **8.820** |
| 33,3% | R$ 1.334.000 | 8.592 | 8.312 |

- **De 10% para 30%, a meta cai de 880 a 3.080 pessoas,** conforme a base da conta.
- **Sem a P-08, ou se a HAPVIDA e o Hospital de Ceilândia começarem a atender o risco cirúrgico,
  a fila acaba antes do dinheiro,** e o apoio maior não tira ninguém.
- **É a pergunta que a SES vai fazer.** A resposta é a seção 7: com 10%, o executor não monta a
  estrutura, e a meta fica no papel.

## 10. Perguntas que podem vir, e o que responder

**"Por que não 10%, como nos planos de vocês de ultrassom e tomografia?"**
Lá o procedimento pagava bem: ultrassom e tomografia com o incremento da 4.282, e a OCI gástrica a
R$ 600,11. O apoio ficou em 8% a 8,5%, pelo mesmo critério da SES (AC-075). Aqui a OCI vale de
R$ 130 a R$ 350, e o executor não tem estrutura.

**"Isso não é complementar o SIGTAP com recurso federal, que é vedado?"**
Não. O valor da OCI fica no SIGTAP, sem complemento. O apoio paga estrutura com preço,
quantidade e orçamento:
- local;
- locação de equipamento;
- responsável técnico;
- regulação;
- gestão;
- prestação de contas.

A Candanga entra só como referência de que o custo total fica dentro do que a SES considera justo.

**"O MPCDF já atacou convênio com 31% a 37% de apoio."**
Pela Candanga, aqueles convênios custam de 96% a 105% do que a SES pagaria a um credenciado. O
nosso, com 30%, custa 95%. E cada linha de apoio terá três orçamentos e memória de cálculo
(LI-021).

**"O pt_ses_05 fez com 16%."**
Porque usou a estrutura do pt_ses_01, montada com 32,5%. Somados, os dois convênios do ISHP
ficaram em 29,4% de apoio no global: R$ 3.092.671,65 de R$ 10.532.671,65.

**"A Candanga é para recurso do DF, não para emenda federal."**
A Deliberação 46 diz que ela é a referência para convênios (art. 3º), e a Lei 7.897 veda
remunerar convênio fora dela (art. 6º). A emenda federal não paga o que passa do SIGTAP na OCI.
Mas o preço justo que a lei fixou continua sendo o parâmetro do que é razoável gastar no total.

**"Qual dos valores da Candanga vale?"**
O PDF da SES destaca o Valor Máximo, e é ele que este material usa. Se o Anexo Único usar outra
medida, o argumento muda de forma, mas não de sentido:

| medida | apoio que deixa o custo por OCI igual a ela | o nosso, com 30% | os quatro aprovados de estrutura própria |
|---|---|---|---|
| Valor Máximo | 33,3% | 95% | 96% a 105% |
| Valor Mediano | 23,4% | 109% | 110% a 122% |
| Valor Médio | 21,8% | 112% | 113% a 124% |

Pelo Máximo, o argumento é "dentro da tabela da SES". Pelo Médio e pelo Mediano, é "mais barato
que tudo o que a SES já aprovou".

**"Vai atender menos gente."**
De 880 a 3.080 pessoas a menos que com 10%. Mas, sem estrutura, os 10% não executam: o executor
não tem onde nem com quê atender.

## 11. O que não dizer, e onde cada coisa vai

| tema | onde vai |
|---|---|
| o percentual, a Candanga e a comparação com os aprovados | só na conversa com a SES |
| "diferença de tabela", "complemento do SIGTAP" | nunca. O apoio é estrutura |
| a falta (24% a 38% na cardiologia) | controle interno. O plano não traz taxa nem vagas a mais (decisão de 21/10) |
| cada linha de apoio | no plano detalhado, com preço do acervo ou três orçamentos e memória de cálculo |
| taxa de administração | vedada (LI-019): a gestão vai posto a posto |

## 12. As fontes

- **Lei distrital 7.897/2026** e **Deliberação CG-SES 46/2026**: `biblioteca/extraidos_normas/`.
- **Tabela SUS Candanga (SIA):**
  - análise comparativa da SES de 06/08/2026, Valor Máximo, p. 26 a 27;
  - `biblioteca/precos/tabela_sus_candanga/`, no `main` (commit db38264).
- **Planos aprovados:**
  - `estudo/normalizados/pt_ses_01` a `05`, planilha e "Total Geral";
  - convênios 030989 (ISHP), 030975, 030976 e 030977 (IEV) e 031061 (ISHP).
- **Achados e controle externo:**
  - AC-015 (rateio do pt_ses_01);
  - AC-058 (valores trocados no Fila Zero);
  - AC-071 e CT-002 (representação do MPCDF);
  - AC-075 (critério da SES para o apoio).
- **A carteira e o mapeamento:**
  - `planos/redacao_08/carteira_ampla_cardiologia.xlsx`;
  - `output/mapeamento_cardiologia_20261027.md`.
- **Preço de mercado:** `planos/redacao_08/dados/precos.md`.

**A conferir antes de levar:**
1. **o Anexo Único da Candanga:** o Valor Máximo é o valor da tabela?
2. **a norma das emendas individuais de 2024** (GM/MS 3.283/2024, fora do acervo): o que a ação
   2E90 aceita de custeio de estrutura.
