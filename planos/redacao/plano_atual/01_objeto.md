# Seção 1 — Objeto

Status: `rascunho` · Nível: **mínimo viável** (melhorias em `redacao/melhorias.md`)
Vigência: 10 meses — 2 semanas de pré-produção, entradas até o mês 9,
conclusões até o mês 10 · Polos: 3
Lacunas: 4 · nenhuma bloqueante — BL-002 encerrada

---

## Redação proposta

> Realização de **35.000 (trinta e cinco mil) Ofertas de
> Cuidado Integrado — OCI 09.02.01.002-6, Avaliação Cardiológica**, no âmbito do
> Programa Mais Acesso a Especialistas, instituída pela Portaria SAES/MS nº
> 1.822, de 11 de junho de 2024, ao valor unitário de R$ 200,00 conforme Tabela
> de Procedimentos do SUS, para usuários do SUS/DF em espera regulada por
> avaliação cardiológica com solicitação de ecocardiografia, referenciados pelo
> Complexo Regulador da SES/DF a partir das Regiões de Saúde **Norte, Sul, Oeste
> e Sudoeste**, executadas em **3 (três) polos assistenciais**
> [[lacuna: LC-003 — localização]], pelo prazo de **10 (dez) meses**, com valor
> global de **R$ 10.000.000,00**, sendo **R$ 7.000.000,00 (70%)** destinados à
> produção assistencial e **R$ 3.000.000,00 (30%)** às despesas de apoio
> discriminadas na Seção 5.

**Composição da OCI:** consulta médica especializada, ecocardiograma,
eletrocardiograma, radiografia de tórax, exames laboratoriais específicos e
consulta ou teleconsulta de retorno. Pacote fechado — nenhum desses itens pode
reaparecer como rubrica na Seção 5.

---

## De onde vem a meta

A ordem está certa desta vez: **a fila define a meta, o valor se ajusta.**

| | |
|---|---|
| fila (Mapa Social/MPDFT, filtro ecocardiografia, extração de **16/08/2026**) | 42.632 solicitações · **36.052 CNS únicos** · espera média **777,28 dias** |
| absenteísmo estimado | **20%** — parâmetro do pt_ses_01 (AC-022) |
| meta | **35.000** = rendimento realista da fila |
| produção | 35.000 × R$ 200,00 = **R$ 7.000.000,00** (70,0%) |
| apoio | **R$ 3.000.000,00** (30,0%) |
| agendamentos a ofertar | **~87.500** — 43.750 na entrada e 43.750 no retorno (fator 1,25 em cada ponta) |
| ritmo | 4.125 entradas/mês nos meses cheios · ~65/polo/dia útil (Seção 2) |

O quantitativo é **pessoa**, não solicitação: 42.632 ÷ 36.052 = 1,18 solicitações
por CNS. Contar solicitação inflaria a meta em 18% sobre gente já contada.

**Por que 35.000 e não 36.052.** Com 20% de absenteísmo, a fila de 36.052 CNS não
rende 36.052 atendimentos. Rende, com reagendamento de faltosos:

| rodada | agenda | comparecem | acumulado |
|---|---|---|---|
| 1ª | 36.052 | 28.842 | 28.842 |
| 2ª | 7.210 | 5.768 | 34.610 |
| 3ª | 1.442 | 1.154 | 35.764 |

**35.000 é o que a fila entrega**, com duas rodadas de reagendamento e alguma
margem. Não é arredondamento para caber no 70/30 — é o rendimento operacional, e
o 70/30 exato é consequência dele.

Daí a oferta de **43.750 horários na entrada** — meta ÷ 0,80 — e outros 43.750 no
retorno, já que a OCI só conclui na segunda visita (DV-002). São **~87.500
agendamentos**, e o pt_ses_01 faz o mesmo movimento: oferta de vagas em
quantitativo superior à meta, para compensar as perdas por não comparecimento
(AC-022).

**Agendamento é evento, não pessoa, e não é meta.** São 36.052 pessoas ocupando
~87.500 horários, porque quem falta e é remarcado consome um segundo. O teto de
pessoas continua sendo a fila. Isso dimensiona as Seções 4 e 9; a meta é só a
Seção 2.

Sobre as **21.572 solicitações devolvidas**: não dá para dizer se saem do estoque
ativo ou se é contador histórico — se saíssem, restariam 21.060 solicitações, o
que é menos que os 36.052 CNS, e isso não fecha. `[[lacuna: LC-011 — o que
"devolvida" significa no painel e se está dentro ou fora das 42.632]]` Não afeta
a meta, que usa CNS. Afeta a Seção 12, se o número for citado lá.

**777 dias — 2,1 anos — de espera média.** É o dado mais forte que este plano
tem, e vai para a justificativa.

---

## Decisões

### 3 polos, distribuídos por alcance

Definido: 3. O método vem do pt_ses_01, que distribui a meta entre polos
"observando-se o volume histórico de demanda por Região de Saúde e a necessidade
de garantir isonomia no acesso" (AC-021) — e cobre as **7** Regiões com 4 polos.

Chave do pt_ses_01, aplicável enquanto a fila de cardiologia por região não chega:

| agrupamento | pt_ses_01 | % | sobre 35.000 | /mês | /dia útil |
|---|---|---|---|---|---|
| Sudoeste + Oeste | 17.634 | 49,0% | 17.144 | 1.905 | ~91 |
| Norte + Leste | 8.879 | 24,7% | 8.632 | 959 | ~46 |
| Sul + Central + Centro-Sul | 9.487 | 26,4% | 9.223 | 1.025 | ~49 |

**O problema:** Sudoeste + Oeste concentra metade da demanda. Um polo só ali
opera ~91/dia útil, o dobro dos outros dois.

**Dois desenhos:**

- **A — cobertura geográfica.** Um polo por agrupamento, como na tabela. Cobre
  tudo, mas desequilibra.
- **B — ponderado por demanda** (o desenho que você descreveu): **dois** polos no
  eixo Sudoeste/Oeste — Taguatinga e Samambaia ou Ceilândia — e **um** em
  Sobradinho cobrindo Norte e Leste. Sul, Central e Centro-Sul são referenciados
  ao polo mais próximo. Divide os 49% entre duas unidades e equilibra a carga.

**Recomendado: B.** É o desenho que aparece na prática, e resolve a concentração.
O que falta para fixar os volumes é a fila de cardiologia aberta por Região de
Saúde — mesmo painel, filtro adicional. `[[lacuna: LC-003]]`

Registrar, como o pt_ses_01 faz, que a distribuição é **estimativa e
referencial**, ajustável conforme a dinâmica das filas no SISREG, **sem alteração
do quantitativo global pactuado**. Essa cláusula é o que evita virar
descumprimento quando a fila se move.

### Polo de execução ≠ região de referência

O DF tem 7 Regiões de Saúde. Samambaia é Sudoeste e Ceilândia é Oeste, então
"3 regiões" seriam 4. O objeto separa **onde se executa** (3 polos) de **de onde
vem o usuário** (4 regiões, por decisão do Complexo Regulador). O pt_ses_01
organiza assim.

### Fonte federal — SIGTAP sem incremento

Decidido: o recurso é federal, logo a produção é remunerada estritamente pelo
valor da tabela, R$ 200,00. Sem acréscimo sobre o procedimento.

**Isso cria uma tensão que a Seção 5 tem que resolver** — ver abaixo.

---

## A tensão do "sem incremento"

Se o convênio repassa R$ 10.000.000,00 por 35.000 OCI, o custo efetivo é
**R$ 285,71 por OCI** — 42,9% acima da tabela. Lido assim, há incremento.

Esse número não é preço unitário e não aparece em lugar nenhum do plano. Está
aqui porque é a conta que um analista faz em dez segundos, e a seção existe para
respondê-la antes que ela seja feita.

Duas leituras, e elas produzem planos diferentes:

**Leitura estrita.** Todo o recurso é produção. R$ 10.000.000 ÷ R$ 200,00 =
50.000 OCI, e nenhuma rubrica de apoio.
→ **Não fecha**: 50.000 é 139% da fila. Sobra dinheiro sem demanda, e some a
estrutura que viabiliza a execução.

**Leitura do corpus.** O procedimento continua remunerado a R$ 200,00. A rubrica
de apoio custeia o que a SIGTAP **não** remunera — e por isso não é incremento
sobre o procedimento. É exatamente o argumento do pt_ses_01 (AC-009):

> a infraestrutura "compreende apenas recursos não assistenciais [...] não
> abrangendo, em nenhuma hipótese, equipamentos médicos, clínicos ou
> assistenciais, os quais se encontram integralmente contemplados no valor
> unitário do procedimento previsto na tabela SUS"

**Adotada: a leitura do corpus**, por ser o mínimo viável pedido e por já ter
sido aprovada. O preço é que a Seção 5 fica com ônus de prova: **todo item dos
30% precisa passar no teste de não-assistencialidade**, item a item. Item que a
OCI já remunera não entra. O teste está escrito na Seção 5, em três perguntas.

---

## Lacunas

| id | descrição | como se resolve |
|---|---|---|
| LC-003 | Localização dos 3 polos. Critério: volume de fila por Região de Saúde. | painel, filtro por região + proponente |
| LC-006 | O que os 30% de apoio custeiam, item a item, com o teste de não-assistencialidade. | Seção 5 |
| LC-011 | O que "solicitação devolvida" significa no painel. | painel / Complexo Regulador |
| LC-012 | Se produção custeada por emenda gera reembolso FAEC ao Fundo. Contabilidade do Fundo, não do convênio. | DV-005, → professor |

**Fechadas:** LC-001 (meta = 35.000, rendimento da fila), LC-002 (R$ 200,00,
Portaria 1.822/2024), LC-004 (fila obtida), LC-005 (regiões), LC-007 (base legal
— ver abaixo), LC-008 (vigência, hoje 10 meses), LC-009 (**era bloqueante**: FAEC
ou teto MAC — dissolvida com BL-002, o executor é remunerado uma vez, pelo
convênio), LC-010 (rota multi-OCI descartada — código único).

---

## Base legal — BL-001 encerrada

Situação real da SES-DF: **não se executa por MROSC**, salvo exceções na atenção
primária. O instrumento é **convênio**. MROSC é difícil de rodar dentro da
secretaria e, quando ocorre, cai em objeto de PAP — nunca de MAC.

Consequência: a Lei 13.019/2014 não é a espinha. A base é o art. 199, §1º da CF,
a Lei 8.080/90 e a camada distrital — pista confirmada no corpus: **Decreto DF
nº 37.843/2016, art. 33**, que o pt_ses_01 cita para o cronograma de desembolso
(AC-010).

Registrado como premissa do exercício. Cadastrar as normas em `acervo.csv` e
desdobrar em `obrigacoes.csv` continua pendente.

---

## BL-002 — encerrada

**O fluxo real:** Ministério da Saúde → **Fundo de Saúde do DF** → a SES paga o
executor **por meio do convênio**.

É cadeia, não duplicidade. O executor é remunerado **uma vez**, pelo convênio. O
recurso federal não vai direto a ele.

```
MS  ──repasse──▶  Fundo de Saúde do DF  ──convênio──▶  executor
                                                        │
                                        produção ──APAC/SIA-SUS──▶ registro
```

Consequências para o plano:

1. **A Seção 5 fica desimpedida.** O repasse remunera produção ao valor de tabela,
   sem sobreposição no nível do executor.
2. **O registro por APAC continua obrigatório** — é o lastro físico da produção, e
   é o que a Seção 8 concilia contra a despesa.
3. **A Seção 1 declara a cadeia.** Nenhum dos quatro planos declara (AC-011,
   AC-012); custa um parágrafo e elimina a dúvida antes que o analista a levante.

Fica uma pergunta menor, **não bloqueante**: se a produção registrada por APAC
também gera reembolso de FAEC ao Fundo de Saúde do DF, o Fundo recebe pela mesma
produção duas vezes — pela emenda e pelo FAEC. Isso é contabilidade do Fundo, não
do convênio, e não muda o que o executor recebe. `[[lacuna: LC-012 — confirmar se
produção custeada por emenda é sinalizada para não gerar reembolso FAEC. Fase 3,
pergunta para o professor.]]`

---

## Anexo — o problema que BL-002 resolvia

**A pergunta:** quem paga a produção, e quantas vezes ela é paga?

A OCI é registrada por APAC no SIA/SUS e custeada por FAEC — é o que os quatro
planos declaram (AC-007, AC-008). FAEC é recurso federal, extra-teto: o Ministério
paga por produção registrada.

Só que o convênio **também** paga o executor pela mesma produção. Concretamente,
para uma única OCI:

```
executor realiza 1 OCI  →  registra APAC no SIA/SUS  →  FAEC paga R$ 200,00
                        →  e o convênio repassa R$ 200,00 pela mesma OCI
                                                 ────────────────────────
                                        mesma produção, R$ 400,00 pagos
```

Nenhum dos quatro planos diz como isso não acontece (AC-012). Por isso é
bloqueante: sem responder, a Seção 5 não tem como ser escrita e a Seção 8 não tem
o que conciliar.

**Três saídas possíveis:**

| saída | mecanismo | o que o plano precisaria escrever |
|---|---|---|
| **S-1 · sem faturamento** | a produção **não** é faturada no SIA/SUS; o convênio paga sozinho | o controle que garante o não-faturamento |
| **S-2 · pagamento da diferença** | a produção é faturada; o convênio paga só a diferença | a memória de custo real — mas com "sem incremento" a diferença é zero |
| **S-3 · dedução do FAEC** | a produção é faturada e o valor do FAEC é **deduzido** do repasse | a rotina de conciliação, competência a competência |

*(Rotuladas S-1 a S-3 para não se confundirem com o desenho de financiamento,
que também usava letras. Nenhuma das três foi adotada — ver abaixo.)*

Com a decisão de fonte federal e SIGTAP sem incremento, a **S-2 fica vazia**: se
não há incremento, não há diferença a pagar. Sobrariam S-1 e S-3.

**O que decide:** para onde o FAEC paga. Se o repasse vai ao Fundo de Saúde do DF
e o convênio é o meio pelo qual o DF remunera o executor, não há duplicidade — há
uma cadeia. Se o executor fatura e recebe direto, há. Isso é Fase 3, e é a
próxima pergunta a levar ao professor.

---

## Financiamento — desenho adotado

**Produção + apoio**, com os valores da Seção 5:

| rubrica | valor | % | o que remunera |
|---|---|---|---|
| produção | R$ 7.000.000,00 | 70% | 35.000 OCI × R$ 200,00, valor de tabela, sem incremento |
| apoio | R$ 3.000.000,00 | 30% | o que a SIGTAP não remunera, item a item pelo teste da Seção 5 |
| **total** | **R$ 10.000.000,00** | 100% | |

**Nenhuma das saídas S-1, S-2 ou S-3 foi adotada** — e é importante que isso fique
escrito, porque as três pressupunham o problema que BL-002 dissolveu. Elas
respondiam "como evitar que a mesma OCI seja paga duas vezes ao executor". A
resposta é que ela nunca foi: o FAEC credita o **Fundo de Saúde do DF**, e quem
paga o executor é a SES, pelo convênio. Uma cadeia, um pagamento.

A APAC continua obrigatória, com papel de **lastro**, não de fatura: prova que a
produção existiu e é contra ela que a Seção 8 concilia a despesa.

Não é mais presunção — BL-002 está encerrada. O que resta é LC-012, um andar
acima e fora do convênio: se a mesma produção também gera reembolso FAEC ao
Fundo, quem recebe duas vezes é o Fundo, não o executor.
