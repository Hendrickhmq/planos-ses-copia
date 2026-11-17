# Seção 8 — Prestação de contas

Status: `rascunho` · Nível: **mínimo viável** (melhorias em `redacao/melhorias.md`)
Depende de: Seções 6 e 7 · Lacunas: 4 (nenhuma bloqueante)
**O calendário depende da Seção 6. O resto não.**

---

## As duas comprovações

A armadilha desta seção é prestar contas só do dinheiro. **Nota fiscal prova
gasto, não prova entrega.** Por isso a prestação tem duas metades, e nenhuma
substitui a outra.

| | comprova | com o quê |
|---|---|---|
| **física** | que as 35.000 OCI aconteceram | produção **aprovada** no SIA/SUS por competência, registro de APAC, relatório mensal com os 11 indicadores da Seção 3 |
| **financeira** | que o dinheiro foi aplicado no que o plano disse | documento fiscal vinculado a **item da planilha**, extrato da conta do convênio, conciliação com as parcelas da Seção 6 |

**O corpus só menciona a existência da prestação de contas.** Nos quatro planos:
"nota fiscal" aparece 0 vez, "conta específica" 0, "aplicação financeira" 0,
"rendimento" 0. Prestação de contas é citada 5, 3, 2 e 3 vezes — sempre como
finalidade, nunca como procedimento com documento e prazo.

---

## O que se apresenta

### Comprovação física

1. **Demonstrativo de produção por competência**, com as três colunas que o SIA
   distingue: apresentada, rejeitada e **aprovada**. O IND-01 usa a aprovada; a
   diferença entre as duas primeiras é o que se explica.
2. **Relatório mensal consolidado**, com os 11 indicadores em numerador e
   denominador, e a série acumulada (IND-02).
3. **Conciliação de oferta e regulação** — vagas ofertadas contra vagas reguladas
   por polo (IND-04). É o que separa sub-execução de sub-regulação, e é a prova da
   ponta do executor.
4. **Registro da busca ativa** conciliado com os reagendamentos no SISREG
   (IND-06).
5. **Relação analítica dos usuários atendidos**, com data de entrada, data de
   retorno e desfecho registrado, para auditabilidade por amostragem.

### Comprovação financeira

1. **Documento fiscal vinculado a item da planilha** — rubrica e item, não só o
   total. Uma nota de locação de espaço aponta para R3.1, não para "despesas
   diversas". É o que permite a verificação C: soma dos itens = subtotal da
   rubrica = total geral.
2. **Extrato da conta do convênio**, com as entradas de cada parcela e as saídas
   conciliadas.
3. **Demonstrativo de saldo por rubrica**, ao fim de cada período e no
   encerramento.

---

## A pergunta que a rubrica de produção levanta

R1 é linha única — 35.000 × R$ 200,00 — porque o convênio remunera o
procedimento, não os insumos (Seção 5). Isso cria uma pergunta que o plano precisa
responder antes de ser assinado, e que nenhum dos quatro aprovados enfrenta:

**R1 presta contas por produção aprovada, ou por despesa realizada?**

| | se for por produção | se for por despesa |
|---|---|---|
| o que se apresenta | produção aprovada no SIA/SUS × R$ 200,00 | folha, insumos e serviços assistenciais, item a item |
| consequência | a linha única se sustenta | a itemização assistencial volta, e a estrutura da Seção 5 muda |
| o que sobra ou falta | diferença entre repassado e produzido → devolução | saldo não aplicado → devolução |

`[[lacuna: LC-032 — como se presta contas da rubrica de produção]]`, DV-023.

**Não é detalhe de formulário.** Se a resposta for "por despesa realizada", o
executor precisa demonstrar o custo assistencial real — que é exatamente a LC-025,
a lacuna que decide a viabilidade. As duas perguntas são a mesma vista de ângulos
diferentes.

---

## Como se calcula o que se devolve

Com desembolso antecipado, devolução não é exceção: é o mecanismo normal de
acerto. E ela tem **duas lógicas diferentes**, que não podem ser somadas antes de
serem calculadas em separado:

```
R1 · produção   →  devolve (valor repassado em R1) − (OCI aprovadas × R$ 200,00)
R2 a R7 · apoio →  devolve o saldo não aplicado, rubrica a rubrica
```

A primeira mede **entrega**; a segunda mede **aplicação**. Um convênio pode ter
apoio integralmente gasto e produção abaixo da meta — e nesse caso devolve pela
primeira linha, não pela segunda.

Antes de chegar à devolução, valem as medidas compensatórias na ordem da Seção 7:
remanejamento de quantitativos entre polos, ações compensatórias dentro da
vigência, e só então devolução — a mesma ordem que o pt_ses_01 estabelece
(AC-042).

---

## Prazos

O roteiro exige os dois, e os dois estão em aberto:

| | prazo | depende de |
|---|---|---|
| apresentação pelo executor | `[[lacuna: LC-027]]` | fechamento da competência (DV-008) e o instrumento |
| análise pelo concedente | `[[lacuna: LC-027]]` | DV-021 |

**Estrutura proposta, a confirmar quando a Seção 6 fechar:** uma prestação
**parcial** a cada parcela — a parcela seguinte não se libera sem a análise da
anterior — e uma prestação **final** consolidando a vigência inteira, apresentada
depois do fechamento da última competência.

`[[lacuna: LC-033 — o calendário exato, que depende do alcance da primeira parcela
(DV-022) e do número de parcelas trimestrais]]`

**Silêncio do concedente no prazo não equivale a aprovação** — a mesma regra da
Seção 7.

---

## A defasagem que o encerramento tem

A execução física termina no mês 10, mas a produção do mês 10 só é apresentada,
processada e aprovada depois dele. Logo **a prestação final não cabe dentro da
vigência física** — ela pertence à vigência financeira, que ainda não tem prazo
definido (DV-012). Nenhum dos quatro planos faz essa separação (AC-033).

Consequência prática: o convênio não pode ser encerrado na data em que a última
consulta acontece. Precisa de janela posterior para fechar competência, conciliar
e apurar devolução.

---

## Conta específica, aplicação financeira e rendimentos

Acrescentado em 2026-08-17, a partir do texto do Decreto DF nº 37.843/2016
(OB-016). O rascunho não tratava disto, e é matéria de prestação de contas:

- **Conta corrente específica**, isenta de tarifas de qualquer natureza, em
  instituição financeira pública oficial do Distrito Federal. Recurso do convênio
  não se mistura com o caixa da entidade, e o extrato dessa conta é peça da
  prestação de contas.
- **Aplicação financeira obrigatória** enquanto os recursos não forem empregados
  na finalidade — poupança, fundo de curto prazo ou operação lastreada em títulos
  públicos.

A segunda regra é consequência direta do desembolso antecipado: se o dinheiro
entra antes da despesa, ele fica parado por algum tempo, e a norma não admite que
fique parado sem render.

**Fica em aberto o destino dos rendimentos.** O texto disponível manda aplicar e
não diz, no trecho conhecido, se o rendimento incorpora o objeto ou se é devolvido
ao final. A diferença é material num convênio de R$ 10.000.000,00 com liberação
trimestral antecipada. `[[lacuna: LC-043 — destino dos rendimentos da aplicação
financeira]]`, DV-025.

⚠️ **Condicionado a BL-003.**

---

## Lacunas

| id | descrição | como se resolve |
|---|---|---|
| LC-027 | Prazo de apresentação e prazo de análise. | DV-021, DV-008 |
| LC-032 | Se R1 presta contas por produção aprovada ou por despesa realizada. | DV-023, → professor |
| LC-033 | Calendário das prestações parciais, atrelado às parcelas. | DV-022 e Seção 6 |
| LC-019 | Se o que se cobra é produção apresentada ou aprovada. | DV-003, → professor |
| LC-043 | Destino dos rendimentos da aplicação financeira dos recursos não empregados. | DV-025, OB-016 |

Nenhuma bloqueia a redação. LC-032 é a mais pesada: dependendo da resposta, a
Seção 5 muda de estrutura.

---

## Fundamento

- **OB-006** — Decreto DF nº 37.843/2016, art. 33: liberação conforme cronograma
  de desembolso. É a norma que sustenta o desembolso antecipado e, com ele, a
  lógica de devolução. `a_verificar`, conhecida por citação no corpus, não pelo
  texto do decreto.
- **OB-010** — registro por APAC no SIA/SUS: é o lastro da comprovação física.
  `a_verificar`, sem dispositivo identificado.

Nenhuma lida no original.
