# Seção 13 — Identificação e base legal

Status: `rascunho` · Nível: **mínimo viável** (melhorias em `redacao/melhorias.md`)
Depende de: Fase 2 · Lacunas: 5 · **BL-003 aberta**
⚠️ **Dados do proponente são FICTÍCIOS, para exercício.** Ver aviso abaixo.

---

## Aviso sobre os dados de identificação

O proponente descrito nesta seção **não existe**. Nome, CNPJ, endereço,
representante legal e processo são **preenchimentos de exemplo**, marcados
`[[exemplo]]`, e servem apenas para que o documento tenha a forma completa de um
plano de trabalho. Nenhum campo foi copiado de entidade real, e nenhum número
aqui identifica pessoa física ou jurídica existente.

Antes de qualquer uso real, todo campo marcado `[[exemplo]]` tem de ser
substituído pelos dados verdadeiros da entidade proponente.

---

## Identificação do proponente

| campo | conteúdo |
|---|---|
| Razão social | `[[exemplo]]` Instituto Exemplo de Cuidado Cardiovascular — IECC |
| Natureza jurídica | `[[exemplo]]` associação privada sem fins lucrativos |
| Qualificação | `[[exemplo]]` entidade filantrópica, com certificação a informar |
| CNPJ | `[[exemplo — número fictício, não utilizar]]` |
| Endereço | `[[exemplo]]` |
| Representante legal | `[[exemplo]]` — nome, cargo, CPF e contato |
| Responsável técnico assistencial | `[[exemplo]]` — médico com RQE em cardiologia, conforme Seção 9 |

## Identificação do concedente

| campo | conteúdo |
|---|---|
| Órgão | Secretaria de Estado de Saúde do Distrito Federal — SES-DF |
| Unidade responsável | `[[lacuna: LC-026]]` — a área que recebe, analisa e decide |
| Responsável pelo acompanhamento | `[[lacuna: LC-026]]` — **a função, não a pessoa** |

O campo acima é o que o pt_ses_01 preencheu como "A definir pela SES/DF", com
função, CPF, telefone e e-mail em branco, e foi aprovado assim (AC-043). Aqui ele
está declarado como lacuna consciente, e a Seção 7 explica por que sem
destinatário nomeado não há manifestação — e sem manifestação, não há
consequência. DV-021.

---

## Objeto, vigência e valor

| campo | conteúdo | confere com |
|---|---|---|
| Instrumento | **Convênio** | premissa BL-001, abaixo |
| Objeto | 35.000 OCI 09.02.01.002-6 — Avaliação Cardiológica, concluídas | Seção 1 |
| Vigência | **10 meses** — 2 semanas de pré-produção, entradas até o mês 9, conclusões até o mês 10 | Seções 1, 2 e 4 |
| Vigência financeira | posterior à física, prazo a definir | `[[lacuna]]` DV-012 |
| Valor global | **R$ 10.000.000,00** | Seção 5 |
| Contrapartida | **não há** | Seção 10 |
| Fonte do recurso | emenda parlamentar federal → Fundo de Saúde do DF → convênio | Seção 1, BL-002 |
| Identificação orçamentária | `[[lacuna: LC-035]]` — nº da emenda, exercício, programa de trabalho, natureza da despesa | M-01 |
| Processo | `[[exemplo]]` SEI nº a informar | — |

**Declarar a fonte do recurso é desvio deliberado do corpus.** Nenhum dos quatro
planos aprovados diz de onde vem o dinheiro — zero menções a emenda, dotação,
programa de trabalho ou natureza de despesa (AC-011). Dizem quanto custa e não
dizem quem paga. Aqui a cadeia está declarada porque o roteiro pede fonte de
recurso nesta seção; o detalhamento orçamentário completo continua como melhoria
M-01, dependente de LC-035.

---

## Base legal

Organizada por camada, da mais alta para a mais próxima da prática. **A última
linha é a que o corpus esquece** — e é justamente onde a SES efetivamente se
apoia.

| camada | norma | o que sustenta | id | situação |
|---|---|---|---|---|
| constitucional | CF/1988, art. 199, §1º | participação complementar de instituição privada no SUS por contrato de direito público ou convênio, com preferência para entidades filantrópicas e sem fins lucrativos | OB-001 | `a_verificar` |
| legal | Lei nº 8.080/1990, art. 24 | recurso a serviços privados quando as disponibilidades do SUS forem insuficientes | OB-002 | `a_verificar` |
| legal | Lei nº 8.080/1990, art. 26 | remuneração segundo critérios e valores fixados pela direção nacional do SUS — âncora do "sem incremento" | OB-003 | `a_verificar` |
| legal | Lei nº 8.080/1990, art. 26, §2º | submissão às normas técnicas e administrativas e às diretrizes do SUS | OB-004 | `a_verificar` |
| **distrital** | **Decreto DF nº 37.843/2016**, arts. 28, 33 a 36 | plano de trabalho, repasse conforme cronograma com liberação anterior à despesa, conta específica, retenção de parcelas | OB-006, OB-011 a OB-019 | ⚠️ **BL-003** — é decreto de parceria (MROSC); aplicabilidade em disputa |
| infralegal federal | Portaria SAES/MS nº 1.822/2024 | institui a OCI 09.02.01.002-6 e define composição, atributos e regras | OB-007 | `a_verificar`, **Anexo não lido** |
| infralegal federal | Portaria SAS/MS nº 768/2006 | laudo prévio à realização do procedimento — o "A" de APAC | OB-008 | `a_verificar` |
| operacional | Manual Operacional da FPO | programação restrita ao pactuado, com o quantitativo correspondente | OB-009 | `a_verificar` |

### ⚠️ BL-003 — a camada distrital está em contradição

**Aberto em 2026-08-17, ao ler o texto do Decreto DF nº 37.843/2016.**

O decreto que este plano usa como camada distrital é decreto de **parceria**, do
regime da Lei nº 13.019/2014. O vocabulário é inequívoco: "organização da
sociedade civil", "termo de colaboração ou de fomento", "edital", "chamamento".
O art. 28 disciplina o plano de trabalho **da parceria**; o art. 35 fala em
inadimplemento **da OSC**; o art. 36 diz que os recursos não são pagamento por
prestação de serviços.

Ou seja, o plano faz duas coisas incompatíveis ao mesmo tempo: **nega que o MROSC
reja o instrumento e se apoia no decreto que regulamenta o MROSC.** A pista foi
herdada do pt_ses_01, que cita o art. 33 (AC-010) — e ela pode indicar que o
próprio corpus mistura os regimes.

**As duas saídas, e o que cada uma custa:**

| se… | então | e cai |
|---|---|---|
| o regime for **parceria** | a Lei 13.019/2014 volta a ser espinha, o instrumento é termo de colaboração ou fomento, com chamamento público | a premissa de BL-001, e a rubrica R1 escrita como remuneração (art. 36) |
| o regime for **convênio** | art. 199 §1º da CF e Lei 8.080/90 seguem como espinha | este decreto inteiro: OB-006, OB-014 a OB-019 — e a camada distrital fica **vazia** |

A segunda saída é a mais provável pela premissa de BL-001, e é também a mais
incômoda: deixa exatamente o buraco que o roteiro nomeia como armadilha desta
seção — citar a norma federal e esquecer a distrital, que é onde a SES se apoia.

**O que resolve:** confirmar a ementa e o âmbito do decreto no SINJ-DF, e
localizar a norma distrital que rege **convênios fora do MROSC** — provavelmente
nas normas de execução orçamentária e financeira do DF, ainda não identificadas.
`[[lacuna: LC-044 — a norma distrital do convênio]]`, DV-025.

Até que isso se resolva, **as obrigações OB-014 a OB-019 estão registradas como
condicionais** e as seções que as citam trazem a marca ⚠️.

### A camada distrital continua vazia — e é a armadilha do roteiro

Com a PRC nº 1/2017 no lugar do Decreto DF 37.843/2016, a contradição de BL-003 se
dissolve: o convênio deixa de se apoiar em decreto de parceria. Mas o efeito
colateral é que **a camada distrital fica sem norma**, e o roteiro nomeia
exatamente isso como armadilha — citar a federal e esquecer aquela em que a SES se
apoia na prática.

Duas saídas, e a escolha é do professor: localizar a norma distrital que rege
convênios fora do MROSC — provavelmente nas normas de execução orçamentária e
financeira do DF —, ou declarar que não há e citar apenas a camada federal, dizendo
por quê. `[[lacuna: LC-044]]`, DV-025.

### Por que a Lei nº 13.019/2014 não é a espinha

O MROSC não rege este instrumento. A premissa, registrada em BL-001: a SES-DF não
executa por MROSC, salvo exceções na atenção primária; quando executa, o objeto é
de PAP, nunca de MAC, e em geral em outras pastas. O instrumento é **convênio**,
em participação complementar ao SUS.

`[[lacuna: LC-036 — localizar o dispositivo de exclusão da Lei 13.019/2014
aplicável a convênio com entidade filantrópica em participação complementar ao
SUS. OB-005 registra a exigência; o inciso ainda não foi identificado.]]`

---

## O critério que esta seção ainda não cumpre

O roteiro é explícito: base legal **confirmada, não assumida**. Hoje ela está
assumida.

**Nenhuma das oito normas acima foi lida no original nesta sessão.** Todas entraram
no acervo por citação no corpus ou por fonte secundária, e todas estão como
`status_vigencia: a_verificar`. Duas pendências são nominais:

- **Decreto DF nº 37.843/2016 sem URL** — conhecido apenas pela citação do
  pt_ses_01 (AC-010). Buscar no SINJ-DF.
- **Anexo da Portaria SAES/MS nº 1.822/2024 não lido** — é o que define o que
  conta como OCI entregue, e por isso a lacuna mais cara do plano inteiro:
  sustenta a Seção 1, a definição de meta cumprida da Seção 2 e o teste de
  não-assistencialidade da Seção 5.

Enquanto isso não for feito, esta seção fica `com_lacuna` **por decisão**, e não
por descuido: citar norma não lida é o oposto do método adotado.

---

## Conferências de consistência

| verificação | resultado |
|---|---|
| Vigência da capa = prazo do objeto (Seção 1) | ✓ 10 meses nas duas |
| Vigência = janela do cronograma físico (Seção 4) | ✓ etapas 1 a 3 dentro dos 10 meses |
| Valor global = total da planilha (Seção 5) | ✓ R$ 10.000.000,00 |
| Valor global = soma das parcelas (Seção 6) | **pendente** — Seção 6 travada em DV-022 |
| Contrapartida declarada (Seção 10) | ✓ ausência declarada, dispositivo pendente |

---

## Lacunas

| id | descrição | como se resolve |
|---|---|---|
| LC-026 | Unidade e função da SES-DF responsáveis pelo acompanhamento. | DV-021 |
| LC-035 | Identificação orçamentária: nº da emenda, exercício, programa de trabalho, natureza da despesa. | proponente / SES |
| LC-036 | Dispositivo de exclusão da Lei 13.019/2014. | OB-005, leitura no original |
| LC-037 | Conferência das oito normas no original, com data de acesso. | leitura direta — SINJ-DF e Planalto |
| LC-044 | A norma distrital que rege convênios fora do MROSC. **BL-003.** | SINJ-DF, DV-025 |

LC-037 é a que impede fechar. As demais são preenchimento.

---

## Fundamento

Esta seção é o fundamento das outras. Os ids da tabela de base legal são os
mesmos citados como `fundamento` nas Seções 2, 3, 4, 5, 7, 9, 10 e 11 — e todos
carregam a mesma ressalva: **nenhuma norma lida no original**.
