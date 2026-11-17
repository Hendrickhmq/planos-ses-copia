> **HISTÓRICO — não usar.** Substituído em 08/10/2026 por `metodo/plano/` (o
> `procedimento.md`, a `estrutura.md` e o `modelo.md`). Este roteiro é da fase de estudo:
> tem 13 seções contra as 9 do padrão, prevê seções que não voltam (contrapartida,
> prestação de contas, base legal) e chama um `validador.py` que nunca existiu.

# roteiro.md — a entrevista

Roteiro de construção assistida de um plano de trabalho. É o `modelo.md` virado
do avesso: cada seção do modelo vira uma pergunta, e cada critério de aceite vira
o teste da resposta.

Existe **antes** do `modelo.md` de propósito. No modo em que a redação puxa o
estudo, escrever é o que revela a lacuna; a lacuna é que dirige a leitura. Os
campos `fundamento` nascem vazios e são preenchidos conforme as fases fecham.

---

## Como se usa

Uma seção por vez, na ordem abaixo. Para cada uma:

1. Eu faço a pergunta.
2. Você responde com o que tiver — inclusive "não sei".
3. Eu escrevo a seção em `redacao/plano_atual/<NN>_<secao>.md`.
4. O que não tiver resposta vira `[[lacuna: descrição]]` **dentro do texto**, no
   lugar exato onde falta, e não numa lista à parte.
5. `redacao/estado.yaml` registra onde paramos.

A lacuna não é um defeito do rascunho, é o produto dele. É a fila de estudo,
gerada pela escrita em vez de adivinhada antes dela.

### Regras da conversa

- **Não invento número.** Valor, quantitativo, código SIGTAP e data saem de você
  ou viram lacuna. Nunca de plausibilidade.
- **Não copio dos planos aprovados.** A fronteira do README vale aqui: entram
  `modelo.md`, `obrigacoes.csv` e `criterios.md`. Nunca as fichas nem os
  `texto.md`. Se eu precisar de algo que só existe nas fichas, isso é sinal de
  que faltou uma linha em `obrigacoes.csv` — e é lá que vai.
- **Fundamento pendente é lacuna, não silêncio.** Se a exigência de uma seção
  ainda depende da Fase 2, a seção sai escrita e marcada, não adiada.

---

## Ordem de redação

Não é a ordem de leitura do documento final. Justificativa vem por último porque
justificativa boa é escrita sabendo o que se vai justificar; capa e base legal
também, porque dependem da Fase 2. O documento é remontado na ordem canônica só
na hora de fechar.

| # | seção | depende de |
|---|---|---|
| 1 | Objeto | — |
| 2 | Metas | 1 |
| 3 | Indicadores e meios de verificação | 2 |
| 4 | Etapas e cronograma físico | 2 |
| 5 | Planilha orçamentária e memória de cálculo | 4 |
| 6 | Cronograma de desembolso | 5 |
| 7 | Monitoramento e avaliação | 3 |
| 8 | Prestação de contas | 6, 7 |
| 9 | Equipe e estrutura física | 4 |
| 10 | Contrapartida | 5 |
| 11 | Riscos | 4, 5 |
| 12 | Justificativa | 1–11 |
| 13 | Identificação e base legal | Fase 2 |

---

## A distinção que organiza tudo

Do `schema.md`, e vale repetir aqui porque é onde o roteiro mais insiste:

| conceito | pergunta que responde | exemplo de forma |
|---|---|---|
| **meta** | quanto se compromete a entregar | 4.800 consultas em 12 meses |
| **indicador** | como se mede o desempenho | consultas realizadas / consultas pactuadas |
| **parâmetro de aferição** | qual valor conta como cumprido | ≥ 95% da meta mensal |
| **meio de verificação** | onde se comprova | produção aprovada no SIA/SUS, comp. mensal |

Plano ruim confunde os quatro — em geral escrevendo a meta na coluna do
indicador e deixando o meio de verificação em branco. As perguntas das seções 2 e
3 são desenhadas para forçar os quatro a saírem separados.

---

## Seção 1 — Objeto

**Pergunta.** O que exatamente vai ser executado, para quem, onde, em quanto
tempo, e em que quantidade? Uma frase, com número dentro.

**Critério de aceite.**
- Tem quantitativo explícito, não adjetivo ("ampliar a oferta" reprova).
- Tem a população e o território definidos.
- Tem prazo, e o prazo bate com a vigência declarada na seção 13.
- É verificável por um terceiro que não participou da negociação.

**Armadilha.** Objeto que descreve a *atividade* do proponente em vez do
*resultado* contratado. "Manutenção da unidade" é meio; "realização de N
procedimentos" é objeto.

**Fundamento.** `[[lacuna: dispositivo que define conteúdo do objeto — Fase 2]]`

---

## Seção 2 — Metas

**Pergunta.** Desdobre o objeto em metas. Para cada uma: o que entrega, quanto,
até quando. Se houver etapas, a que etapa pertence.

**Critério de aceite.**
- A soma das metas reconstrói o quantitativo do objeto. Se não fecha, um dos dois
  está errado — e é a verificação 1 do `validador.py`.
- Cada meta tem unidade de medida declarada.
- Cada meta tem prazo próprio, não só o prazo global.
- Nenhuma meta é enunciada como indicador ("melhorar o índice de X" não é meta).

**Armadilha.** Meta que só é aferível no último mês. Se a apuração é anual, não
há como notificar no meio do caminho, e a prestação de contas mensal fica sem
lastro.

**Fundamento.** `[[lacuna: — Fase 2]]`

---

## Seção 3 — Indicadores e meios de verificação

**Pergunta.** Para cada meta da seção 2, os quatro campos da tabela acima:
indicador (fórmula), parâmetro de aferição (o valor que conta como cumprido),
meio de verificação (o sistema ou documento) e periodicidade da apuração.

**Critério de aceite.**
- Fórmula com numerador e denominador explícitos.
- Meio de verificação é uma fonte que **existe e é acessível ao concedente** —
  sistema oficial, relatório com formato definido, prontuário auditável. "Relatório
  do proponente" sozinho não é meio de verificação, é autodeclaração.
- Periodicidade da apuração compatível com a periodicidade do desembolso (seção
  6). É a verificação 4 do `validador.py`.

**Armadilha.** Indicador sem denominador, que na prática é uma contagem — e
contagem já era a meta. Duplicar a meta na linha do indicador é o defeito mais
comum.

**Fundamento.** `[[lacuna: — Fase 2 e Fase 3 (SIA/SUS, APAC)]]`

---

## Seção 4 — Etapas e cronograma físico

**Pergunta.** Em que etapas o objeto se divide, em que ordem, com que duração, e
qual meta cada etapa entrega?

**Critério de aceite.**
- Numeração hierárquica sem buraco e sem repetição — é o mesmo teste da
  verificação I do `conferir.py`, e vale igual no rascunho próprio.
- Toda meta da seção 2 aparece em pelo menos uma etapa.
- Início e fim de cada etapa em mês, dentro da vigência.

**Armadilha.** Etapa cuja duração soma mais que a vigência, ou etapa de
"mobilização" sem entrega associada, que depois recebe desembolso.

**Fundamento.** `[[lacuna: — Fase 2]]`

---

## Seção 5 — Planilha orçamentária e memória de cálculo

**Pergunta.** Item a item: descrição, unidade, quantidade, frequência, valor
unitário, valor total, e a **origem do preço**.

### Como se monta: de baixo para cima, pelo fluxo do atendimento

A planilha **não se monta por rubrica**. Rubrica é como ela termina, não como
ela nasce. Montar por rubrica é abrir "Pessoal", "TI", "Serviços gerais" e ir
enchendo — e o que se enche é o que se lembra, não o que o objeto exige. O
resultado passa na conferência aritmética e não passa no teste da pergunta
"por que este posto existe?".

**Percorre-se o fluxo do atendimento, do chão para cima, e cada passo revela o
seu custo.** O usuário chega — logo há recepção. Alguém marca e remarca — logo
há agendamento. Alguém lança no sistema — logo há registro. O sistema cai —
logo há TI. Quem não compareceu precisa ser buscado — logo há busca ativa. Cada
linha da planilha tem de poder apontar o passo do fluxo que a torna necessária,
e um posto que não aponta passo nenhum é um posto que sai.

O ganho é duplo. O dimensionamento deixa de ser arbitrado — quantidade e
frequência saem do volume do passo, não da intuição —, e a defesa do item fica
pronta antes de ser pedida: quem analisa pergunta pela necessidade, e a
necessidade já está escrita ao lado.

### Os três setores

| setor | o que abrange | onde costuma estar |
|---|---|---|
| **Técnico** | a execução assistencial propriamente dita | **quase sempre já dentro do valor do procedimento**, e por isso **não se repete na planilha** |
| **Administrativo** | recepção, agendamento, registro e lançamento em sistema, busca ativa, supervisão, TI, infraestrutura | planilha de apoio |
| **Financeiro** | execução financeira, conciliação, prestação de contas | planilha de apoio |

O setor técnico é o que mais gera erro, e o erro é sempre o mesmo: **cobrar duas
vezes**. Quando o objeto é remunerado por procedimento ou por pacote, o custo
assistencial já está no valor unitário — consulta, exame, insumo, profissional
que executa. Recolocá-lo no apoio é duplicidade, e é achado de análise. A
pergunta que separa é única: *este custo já está dentro do valor que se cobra
pela unidade produzida?* Se está, não entra. Se não está — e há casos —, entra
com a demonstração de que não está.

**A conversão para rubrica é o último passo, não o primeiro.** Levantados os
postos pelo fluxo, aí sim eles se agrupam na natureza de despesa que a norma
aplicável admite, com o dispositivo ao lado de cada linha. A ordem importa: do
fluxo se chega à rubrica, e nunca ao contrário, porque a rubrica justifica a
*natureza* da despesa e só o fluxo justifica a sua *existência*.

**Critério de aceite.**
- Cada linha de apoio aponta o passo do fluxo que a torna necessária. Linha sem
  passo é linha que sai.
- Nenhuma linha de apoio recompõe custo já remunerado no valor unitário da
  produção — a verificação é explícita, item a item.
- Quantidade e frequência derivam do volume do passo (atendimentos, faltas,
  competências), não de arredondamento.
- `total = quantidade × frequência × valor unitário`, linha a linha. É a
  verificação D do `conferir.py`, aplicada ao próprio rascunho.
- Subtotal por etapa fecha com a soma dos itens; total geral fecha com a soma dos
  subtotais (verificação C).
- Toda frequência declarada em texto bate com a soma das frequências da planilha
  — o achado AC-001 do pt_ses_01 é exatamente essa divergência (16 declarados
  contra 18 somados).
- Cada preço tem origem citada: pesquisa, tabela oficial, contrato anterior.
- Convenção decimal única no documento inteiro. O pt_ses_01 mistura `1.216,00` e
  `1,216.00` na mesma planilha.

**Armadilha.** Duas. A primeira: memória de cálculo que repete o total em vez de
mostrar como se chegou nele — memória de cálculo é o caminho, não o destino. A
segunda: planilha montada por rubrica e justificada depois. Reconhece-se pelo
sintoma — os postos são redondos (2 por polo, 1 por polo, sempre), o
dimensionamento não cita volume nenhum, e a defesa de cada item é a natureza da
despesa em vez da necessidade dela.

**Fundamento.** `[[lacuna: pesquisa de preços — Fase 4]]`

---

## Seção 6 — Cronograma de desembolso

**Pergunta.** Quantas parcelas, em que meses, de que valor, e vinculadas a qual
entrega?

**Critério de aceite.**
- Soma das parcelas = valor global da seção 5.
- Percentuais, se declarados, batem com os valores (verificação 2 do
  `validador.py`).
- Número de parcelas compatível com a vigência (verificação 3).
- Data da parcela posterior à data de apuração da entrega que ela paga
  (verificação 4). Parcela que vence antes do que ela remunera é adiantamento.

**Armadilha.** Parcelas iguais em plano cujas etapas têm custo desigual. Divisão
em doze avos é sinal de que o desembolso não conversa com o cronograma físico.

**Fundamento.** `[[lacuna: — Fase 2 e Fase 3 (repasse fundo a fundo)]]`

---

## Seção 7 — Monitoramento e avaliação

**Pergunta.** Quem monitora, com que frequência, olhando o quê, e o que acontece
quando o indicador não bate o parâmetro?

**Critério de aceite.**
- Nomeia o responsável pelo lado do concedente e pelo lado do proponente.
- Define a consequência do descumprimento — glosa, retenção, notificação, prazo
  de recuperação. Sem consequência escrita, monitoramento é relatório.
- Usa os indicadores da seção 3, sem inventar métrica nova aqui.

**Armadilha.** Monitoramento que descreve o envio do relatório e não a análise
dele. Quem recebe, em quanto tempo se manifesta, e o que a manifestação decide.

**Fundamento.** `[[lacuna: — Fase 4]]`

---

## Seção 8 — Prestação de contas

**Pergunta.** Que documentos, em que prazo, comprovando o quê, e conciliados
como com a seção 6?

**Critério de aceite.**
- Prazo de apresentação e prazo de análise, ambos.
- Vincula despesa a item da planilha, não só ao total.
- Diz o que comprova execução **física** além da financeira.

**Armadilha.** Prestação de contas só financeira. Nota fiscal prova gasto, não
prova entrega.

**Fundamento.** `[[lacuna: — Fase 4]]`

---

## Seção 9 — Equipe e estrutura física

**Pergunta.** Quem executa — cargo, quantidade, carga horária, vínculo — e em que
estrutura.

**Critério de aceite.**
- Carga horária da equipe compatível com o quantitativo do objeto. Se o objeto
  são N atendimentos e a equipe não comporta N, um dos dois está errado.
- Todo cargo remunerado pelo convênio aparece na planilha da seção 5, e vice-versa.

**Armadilha.** Equipe listada sem carga horária, o que impede exatamente a
conferência acima.

**Fundamento.** `[[lacuna: — Fase 2]]`

---

## Seção 10 — Contrapartida

**Pergunta.** Há contrapartida? De que natureza — financeira, bens, serviços — em
que valor, e como se comprova?

**Critério de aceite.**
- Se não há, o plano **diz que não há e cita o dispositivo que dispensa**. Seção
  ausente e seção que declara ausência são coisas diferentes para quem analisa.
- Se há, tem valor, forma de aferição e prazo.

**Fundamento.** `[[lacuna: exigibilidade e percentual — Fase 2]]`

---

## Seção 11 — Riscos

**Pergunta.** O que pode dar errado em cada etapa, com que probabilidade, com que
impacto, e qual a ação prevista.

**Critério de aceite.**
- Matriz P×I, com o critério de classificação escrito.
- Todo risco alto tem ação de mitigação **e** responsável.
- Cobre risco de execução, risco de financiamento e risco regulatório — não só o
  primeiro.

**Armadilha.** Matriz genérica, que serviria para qualquer convênio. Risco que
não menciona o objeto não é risco deste plano.

**Fundamento.** `[[lacuna: — Fase 4]]`

---

## Seção 12 — Justificativa

**Pergunta.** Por que este objeto, neste tamanho, para esta população, agora?

**Critério de aceite.**
- Dado epidemiológico ou assistencial com fonte e data, não adjetivo.
- **Justifica o dimensionamento**, não só a necessidade. Explicar por que existe
  demanda não explica por que a meta é 4.800 e não 3.000.
- Ancorada em instrumento de planejamento vigente (PDS, PAS).
- Escrita depois das seções 1–11, e coerente com elas.

**Armadilha.** Justificativa que é a única seção bem escrita do plano. Costuma
indicar que o resto foi preenchido para caber num valor já decidido.

**Fundamento.** `[[lacuna: PDS 2024–2027, PAS — Fase 3]]`

---

## Seção 13 — Identificação e base legal

**Pergunta.** Proponente, concedente, instrumento, base legal, processo,
vigência, valor global, fonte de recurso.

**Critério de aceite.**
- Base legal **confirmada, não assumida**. É a Fase 2 do README: se o convênio é
  com entidade filantrópica em participação complementar ao SUS, a Lei 13.019/2014
  pode não reger, e a espinha passa a ser o art. 199 §1º da CF, a Lei 8.080/90 e a
  norma distrital.
- Vigência bate com o prazo do objeto (seção 1) e com o cronograma (seções 4 e 6).
- Valor global bate com o total da seção 5.

**Armadilha.** Citar a norma federal e esquecer a camada distrital, que é onde a
SES efetivamente se apoia.

**Fundamento.** `[[lacuna: BLOQUEANTE — Fase 2, resolver antes de fechar]]`

---

## Fechamento

O rascunho não está pronto quando as treze seções existem. Está pronto quando:

1. Nenhuma `[[lacuna:]]` restante é bloqueante.
2. `validador.py` passa nas seis verificações sobre `redacao/plano_atual/`.
3. Toda seção tem `fundamento` preenchido com id de `obrigacoes.csv`.
4. Um item do eixo 2 do `criterios.md` que nenhum dos quatro planos aprovados
   cumpre está cumprido aqui. Se não houver nenhum, o rascunho empatou com o
   mínimo viável — que é o que o projeto existe para superar.
