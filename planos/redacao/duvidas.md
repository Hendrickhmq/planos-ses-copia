# duvidas.md — o que falta responder

Todas as dúvidas abertas do plano, num lugar só. Cada uma tem: a pergunta, por
que importa, o que já se sabe, e um campo **Resposta** em branco.

Fluxo: você responde o que souber, marca `→ professor` no que não souber, e o que
for respondido vira decisão em `estado.yaml` e texto no `plano_atual/`.

Estado: `aberta` · `→ professor` · `respondida`

---

## Para o professor — as quatro principais

### DV-001 · Produção excedente à meta

**Pergunta.** Se o executor produzir acima das 35.000 OCI pactuadas, o Ministério
remunera esse excedente por FAEC, ainda que o convênio não pague?

**Por que importa.** Define se errar a meta para baixo tem conserto. Se não tem,
o dimensionamento vira decisão irreversível.

**O que já se sabe.**
- O convênio **não** paga: cláusula veda alteração do objeto, da finalidade das
  despesas e do valor global pactuado (AC-029). Além disso, só com termo aditivo.
- O SIA valida contra a FPO antes de aprovar. Acima do teto programado, a
  produção fica *apresentada* e não *aprovada* (AC-026, AC-028).
- A FPO é programada a partir do que foi pactuado em convênio (AC-028).

**Desdobra em três.**
- (a) A FPO é programada no mesmo quantitativo da meta ou acima? Se igual, o
  excedente nem chega a ser aprovado — morre na FPO, antes do Ministério.
- (b) Se aprovado, o recurso vai ao Fundo de Saúde do DF ou ao executor? Pelo
  fluxo, o FAEC repassa ao Fundo, e quem paga o executor é a SES via convênio,
  travado no valor global. Produção aprovada ≠ executor remunerado.
- (c) Há caminho direto do Ministério ao executor? Só se ele for prestador
  contratado ou credenciado por **outro** instrumento, em paralelo ao convênio.

**Hipótese:** não há pagamento do excedente. A FPO barra a aprovação e o convênio
barra o repasse. É hipótese, não resposta.

**Status:** `→ professor`

**Resposta:**

---

### DV-003 · O que a prestação de contas tem que demonstrar

**Reformulada em 2026-08-17.** A pergunta original era "o repasse tem por base
produção apresentada ou aprovada". **A premissa estava errada:** o repasse do
convênio não tem por base a produção nenhuma — é liberação antecipada contra
cronograma (AC-032). A pergunta certa é outra.

**Pergunta.** Na prestação de contas, o que comprova a execução física: produção
**apresentada** ou **aprovada** no SIA? E o que acontece com a diferença — glosa,
devolução, compensação na parcela seguinte?

**Por que importa.** Como o dinheiro entra antes da despesa, o risco migra do
repasse para a devolução. Produção aquém do repassado vira obrigação de devolver.
Isso é Seção 8 e risco da Seção 11, não Seção 6.

**O que já se sabe.** O SIA classifica a produção em *apresentada*, *orçada* e
*aprovada*. Nenhum dos quatro planos usa esse vocabulário; busca por `glosa`
retorna zero (AC-024).

**Status:** `→ professor`

**Resposta provisória (2026-08-18, usuário).** **Produção aprovada** — há alguém
dentro da SES que aprova ou reprova. Adotado até validação do professor.

Confirma o que a Seção 3 já fazia: IND-01 usa produção aprovada no numerador. O
executor registra também a apresentada, porque a diferença entre as duas separa
problema de faturamento de problema de assistência.

**Pendente de validação**, e o destino da diferença — glosa, devolução ou
compensação — continua sem resposta.

---

### DV-004 · FPO — Ficha de Programação Orçamentária

**Ampliada em 2026-08-17.** O proponente nunca teve contato com a sigla. A dúvida
deixa de ser só operacional e passa a incluir o entendimento do instrumento.

**O que a FPO é, até onde se sabe hoje.** É o cadastro que define, dentro do
SIA/SUS, quais procedimentos cada estabelecimento pode faturar e até que limite —
em quantidade e em valor. O SIA confere a produção registrada contra a FPO
**antes** de aprovar. Procedimento sem FPO programada para aquele CNES, ou acima
do teto programado, fica **apresentado e não aprovado**: o atendimento aconteceu
e o sistema não o reconhece. Quem programa é a gestão, não o executor (AC-026,
AC-028, OB-009 — Manual Operacional da FPO, `a_verificar`).

**Perguntas para o professor, na ordem:**

1. **O que é a FPO, na prática da SES-DF?** Quem preenche, com que periodicidade
   se revisa, e onde o executor consegue ver a sua.
2. **Qual o prazo de programação** entre a assinatura do convênio e a FPO
   disponível para faturar? É isso que define a duração da Etapa 0 — a curva da
   Seção 2 hoje assume **1 mês** como premissa declarada (LC-015).
3. **A OCI entra no limite como FAEC ou como MAC?** Muda o teto contra o qual a
   produção é validada.
4. **O teto programado é igual à meta pactuada, ou fica acima dela?** Se for
   igual, o excedente nem chega a ser aprovado — e a DV-001 morre aqui, antes de
   chegar ao Ministério.
5. **O que acontece se a FPO atrasar** e houver produção realizada antes dela:
   perde-se, ou se refatura na competência seguinte?
6. **Como a FPO trata o pacote incompleto** — a OCI iniciada e não concluída
   consome limite? (encadeia com DV-013, respondida)

**Por que importa.** Sem FPO programada, a produção existe e não é aprovada. Se
não estiver pronta no mês 1, os 9 meses viram 8 e a curva mensal inteira desloca.
E como o teto sai do que foi pactuado, **a meta do plano vira o teto de
faturamento do executor** — o que amarra esta dúvida à DV-001 e à Seção 6.

**Status:** `→ professor` — pauta de estudo, não só pergunta pontual

**Resposta:**

---

### DV-005 · Emenda e reembolso FAEC

**Pergunta.** Produção custeada por emenda é sinalizada para **não** gerar
reembolso FAEC ao Fundo de Saúde do DF, ou entra normalmente?

**Por que importa.** Se entra normalmente, o Fundo recebe pela mesma produção
duas vezes — pela emenda e pelo FAEC. Não muda o que o executor recebe, mas é a
pergunta que um analista de controle faz.

**Status:** `→ professor`

**Resposta:**

---

## Menores, mas abertas

### DV-006 · Nome do sistema local

**Pergunta.** "APAC SUS" é a APAC dentro do **SIASUS**, ou existe outro sistema
na SES-DF com esse nome?

**O que já se sabe.** O fluxo está confirmado: APAC Magnético (captação) → SIASUS
(a SES importa, processa e valida) → transmissão à base nacional. Só o nome local
está em aberto, e o plano não depende dele.

**Status:** `→ professor`

**Resposta:**

---

### DV-007 · Validade da APAC

**Pergunta.** Qual a validade da APAC? Uma fonte indica 3 meses; não confirmado
em manual da SES-DF.

**Por que importa.** Se a OCI só se conclui no retorno (ver DV-002, respondida), e
a APAC tem validade, o ciclo inteiro precisa caber dentro dela.

**Status:** `aberta` — resolve com o manual operacional da SES-DF

**Resposta:**

---

### DV-008 · Cronograma de fechamento de competência

**Pergunta.** Quais os prazos mensais de entrega de bases e fechamento de
competência na SES-DF?

**Por que importa.** Amarra as parcelas da Seção 6. Parcela que vence antes da
aprovação da produção é adiantamento.

**O que já se sabe.** A SES-DF publica cronograma anual de entrega de bases.

**Status:** `aberta` — resolve com o cronograma publicado

**Resposta:**

---

### DV-009 · Solicitações devolvidas — → PROFESSOR

**Pergunta.** O que "solicitação devolvida" significa no Mapa Social, e as 21.572
estão dentro ou fora das 42.632?

**Por que importa.** Não afeta a meta, que usa CNS. Afeta a Seção 12 se o número
for citado. Hoje não fecha: se saíssem, restariam 21.060 solicitações, menos que
os 36.052 CNS.

**Status:** `aberta`

**Status atualizado (2026-08-18).** Vai para o professor.

---

### DV-010 · Contrapartida — respondida em substância

**Resposta (2026-08-17).** Não há contrapartida do executor. No convênio, o
concedente libera recurso **antes** da despesa, justamente para dar partida ao
contrato. O executor não precisa aportar capital próprio para começar.

Confirmado pelo corpus (AC-032): "assegurando que os valores sejam
disponibilizados **previamente à realização das despesas correspondentes**".

**O que ainda falta.** O plano não pode só omitir a seção: precisa **declarar que
não há contrapartida e citar o dispositivo que dispensa**. Seção ausente e seção
que declara ausência são coisas diferentes para quem analisa. Candidato: Decreto
DF nº 37.843/2016.

**Status:** `aberta` — falta só o dispositivo

**Resposta:**

---

### DV-013 · OCI iniciada e não concluída — RESPONDIDA

**Pergunta.** O usuário que faz a consulta de entrada e os exames, mas não
comparece ao retorno dentro da vigência: o que acontece com os procedimentos
secundários já realizados? São registrados avulsos no SIA/SUS, perdem-se, ou
contam parcialmente para alguma coisa?

**Por que importa.** A meta é de OCI **concluída** (DV-002). Se o pacote
incompleto não tem nenhum registro, o executor absorve custo real sem lastro de
produção — e isso é risco da Seção 11 e memória de cálculo da Seção 5. Se tem
registro avulso, aparece na FPO e precisa estar previsto.

**O que já se sabe.** A OCI é pacote fechado, com procedimento principal e
secundários (AC-023, OB-010). Nenhum dos quatro planos define conclusão de OCI
(AC-031), logo o corpus não responde.

**Status:** `respondida`

**Resposta (2026-08-17, usuário).** Não há recebimento parcial. Só se recebe pela
OCI **concluída** — não existe meia OCI, nem pagamento por consulta avulsa ou por
procedimento secundário isolado. Por isso a OCI iniciada e não finalizada deve ser
evitada ao máximo: é custo sem contrapartida.

**Consequências, incorporadas na Seção 2:**
1. A oferta da Meta 2 cobre os dois pontos do fluxo — perder o retorno custa o
   pacote inteiro.
2. O faltoso é tratado com reagendamento e **busca ativa**, com os dados de
   contato que a SES-DF fornece para os pacientes regulados.
3. Vira risco nomeado na Seção 11, e entra na memória de cálculo da Seção 5 como
   perda esperada.

**Ainda em aberto:** se o pacote incompleto tem algum registro no SIA/SUS — se os
procedimentos secundários já realizados são lançados avulsos ou simplesmente não
aparecem. Não muda a receita; muda o que a FPO precisa comportar e o que a
Seção 8 concilia. Pergunta técnica, cabe ao professor.

---

### DV-014 · Absenteísmo do retorno — RESPONDIDA (premissa)

**Pergunta.** Os 20% de absenteísmo (AC-022) valem também para a consulta de
retorno, ou o retorno tem taxa própria?

**Por que importa.** A Meta 2 oferta 87.500 vagas — 43.750 de entrada e 43.750 de
retorno — replicando no retorno o parâmetro medido na entrada. Se o retorno falta
mais, a oferta está subdimensionada e a meta de OCI concluída não fecha; se falta
menos, sobra capacidade paga. A teleconsulta de retorno muda o número, e é
exatamente a alavanca apontada em DV-002.

**Respondido em substância (2026-08-17, usuário):** o mecanismo está definido —
paciente regulado pela SES que tem horário marcado e não comparece é procurado
pelo executor, com os dados de contato fornecidos pela própria Secretaria.
Reagendamento e busca ativa, nos dois pontos do fluxo.

**O que ainda falta é o número.** "Taxa própria do retorno" significa: a taxa de
falta na consulta de retorno é a mesma 20% medida na entrada, ou outra? O plano
hoje usa 20% nos dois pontos, por falta de parâmetro próprio. Se existir série do
executor ou da SES sobre falta em retorno — e sobre falta em teleconsulta —, ela
substitui a estimativa e redimensiona a Meta 2.

**Status:** `aberta` — falta só o parâmetro numérico

**Resposta (2026-08-18, usuário).** Não é possível mapear a taxa própria do
retorno. **Adotados os mesmos 20% da entrada, como base declarada.**

Fica registrado como premissa, não como medição: o IND-05 apura entrada e retorno
separadamente justamente para que o parâmetro real apareça durante a execução. Se
divergir, a oferta de agenda se redimensiona. LC-014 passa de lacuna a premissa
declarada.

---

### DV-015 · Entrada de novos usuários na fila — → PROFESSOR

**Pergunta, em duas partes.**
1. Quantas **novas solicitações de ecocardiografia** entram por mês na fila do
   SUS/DF? Precisão dada pelo usuário em 2026-08-17: é gente nova pedindo o
   exame, não atendimento realizado.
2. **Em que ordem a regulação encaminha** — por tempo de espera, o mais antigo
   primeiro, ou por outro critério?

**Por que importa.** A Meta 1 promete 35.000 OCI concluídas. Contra o estoque de
36.052, isso é **97,1% da fila inteira** — cada pessoa comparecendo na entrada e
no retorno, com busca ativa até a terceira tentativa. Premissa agressiva demais
para ficar implícita. Se há fluxo mensal de entrada, o denominador real é maior e
a meta deixa de exigir conversão quase total do estoque.

**O que já se sabe.** O painel informa 42.632 solicitações e 36.052 CNS únicos em
um recorte, com espera média de 777,28 dias. Não se sabe a data de extração
(LC-004, fechada com ressalva) nem se o painel expõe série temporal.

**A segunda parte muda o efeito da primeira.** O executor não capta paciente:
toda entrada vem da regulação. Se o critério for tempo de espera, quem entra na
fila durante a vigência só é encaminhado depois de esgotado o estoque com 777
dias de espera — então o fluxo novo não alivia a meta no começo, alivia no fim, e
só se o estoque drenar antes.

**Como resolver.** Mesmo painel do Mapa Social, se ele der série mensal; ou o
Complexo Regulador — que é também quem responde a ordem de encaminhamento.
Encadeia com DV-009, sobre o mesmo painel.

**Status:** `aberta` — abre na Seção 2, decide a exposição da Seção 11

**Status atualizado (2026-08-18).** Vai para o professor — o usuário não dispõe do
dado de novas solicitações nem da ordem de encaminhamento da regulação.

---

### DV-016 · Vaga ofertada e não regulada

**Pergunta.** Se o executor oferta os horários e a regulação da SES-DF não
encaminha usuários em volume suficiente para preenchê-los, o que acontece com a
meta? Ela é reajustada, o período é prorrogado, ou o executor responde pelo
não cumprimento?

**Por que importa.** O fluxo tem uma etapa que não é do executor: ele libera a
agenda, mas quem seleciona da fila e agenda é o Complexo Regulador. Vaga ofertada
e não regulada é capacidade instalada ociosa — custo incorrido sem OCI possível.
Como o desembolso é antecipado, produção aquém do repassado vira obrigação de
devolver (DV-003), e a causa da falha muda quem deve.

**O que já se sabe.** A execução observa a organização das filas e a distribuição
regional da demanda regulada pela SES-DF, vedada mesclagem indevida de filas
regionais (AC-030). Nenhum dos quatro planos trata da hipótese de sub-regulação.

**Como resolver.** Professor, e cláusula de ajuste no instrumento. A prova do lado
do executor é o registro mensal de vagas ofertadas contra vagas reguladas — que
por isso vira indicador na Seção 3.

**Status:** `aberta` — abre na Seção 2, decide cláusula na Seção 7 e risco na 11

**Resposta:**

---

### DV-017 · Acesso do executor à crítica do SIA

**Pergunta.** O executor consegue ver, por conta própria, o resultado do
processamento da sua produção no SIA/SUS — o que foi apresentado, o que foi
aprovado e o motivo da rejeição —, ou depende de a SES-DF informar?

**Por que importa.** O IND-01 usa produção **aprovada** no numerador. Se o
executor só descobre a crítica quando a SES comunica, ele não consegue corrigir
dentro da competência: erra, fica sabendo tarde e o prazo de reapresentação pode
já ter passado. Com desembolso antecipado, produção não aprovada vira devolução —
então o acesso ao dado deixa de ser conveniência e vira controle de risco.

**O que já se sabe.** A produção é registrada por APAC no SIA/SUS (AC-023) e
validada contra a FPO antes da aprovação (AC-028). Nenhum dos quatro planos
menciona quem enxerga o quê no processamento (AC-024, AC-026).

**Status:** `→ professor` — abre na Seção 3, decide LC-020

**Resposta:**

---

### DV-018 · Parâmetro de aferição — qual limiar conta como meta cumprida

**Pergunta.** Qual o percentual de execução da meta mensal que a SES-DF considera
cumprimento em convênio deste tipo, e qual a consequência de ficar abaixo dele —
notificação, glosa, retenção da parcela seguinte, devolução? Existe janela de
compensação, isto é, o mês abaixo do limiar deixa de gerar consequência se o
acumulado se recuperar nas competências seguintes?

**Por que importa.** É o único campo do quadro de indicadores que ainda está
vazio, e o desembolso antecipado o torna crítico: como o recurso entra antes da
despesa, o limiar não decide quanto pagar, decide **quanto devolver**. Sem ele
não há critério para separar oscilação normal de inadimplemento — e a Seção 7 não
tem o que escrever como consequência.

**O que já se sabe.** Nenhum dos quatro planos aprovados declara limiar numérico:
o 02, o 03 e o 04 têm seção de "Parâmetros de Aferição" sem parâmetro algum
(AC-036) e o pt_ses_01 declara seus indicadores como "exclusivamente gerenciais",
sem obrigação (AC-037). Busca por `no mínimo N%` nos quatro: zero ocorrências.
Logo o corpus não oferece piso — o número tem que vir da SES ou da norma.

**Três desenhos possíveis**, com a recomendação registrada na Seção 3:
- (a) limiar único mensal;
- (b) **limiar mensal com compensação no acumulado** — recomendado, coerente com
  IND-01 e IND-02 já estarem separados;
- (c) limiar só no acumulado final — reprovado: impede notificar no meio do
  caminho.

**Faltam três valores:** o limiar mensal, a janela de compensação e a consequência
de cada faixa.

**Status:** `→ professor` — o proponente não dispõe do número; sai da negociação
com a SES ou da norma distrital

**Resposta:**

---

### DV-019 · Habilitação dos acessos aos sistemas

**Pergunta.** Quem solicita e quem concede o acesso do executor ao SISREG e ao
TrakCare, e em quanto tempo? O acesso é por unidade (CNES do polo), por
profissional, ou os dois?

**Por que importa.** É a subetapa 1.3 da Etapa 1. Sem acesso ao SISREG o executor
não oferta vaga nem enxerga a regulação; sem TrakCare não registra o atendimento.
A curva da Seção 2 assume que 2 semanas bastam para isso e para a FPO. Cada
quinzena perdida na partida custa cerca de 240 entradas a mais por mês nos meses
seguintes.

**O que já se sabe.** Os planos 02, 03 e 04 listam "acesso operacional aos
sistemas oficiais da SES/DF, especialmente SISREG e TrackCare, incluindo
habilitação de acessos e validação de fluxos" como ação da etapa de pré-produção
(AC-034) — mas nenhum declara prazo nem responsável pela concessão.

**Status:** `aberta` — abre na Seção 4, resolve LC-021

**Resposta:**

---

### DV-020 · Unidade gestora, prazo de manifestação e o "instrumento de medição de resultados"

**Pergunta, em três partes.**
1. Qual unidade da SES-DF é a gestora do convênio — quem recebe e analisa o
   relatório mensal, e quem assina a manifestação?
2. Em que prazo ela precisa se manifestar sobre o relatório recebido?
3. O pt_ses_01 cita, na escada de medidas compensatórias, a "aplicação do
   instrumento de medição de resultados" (AC-040), sem definir o que é. Existe
   um IMR padronizado na SES-DF para convênios assistenciais?

**Por que importa.** Monitoramento sem prazo de análise é entrega de papel: o
executor manda, ninguém responde, e o problema só aparece na prestação de contas,
quando o recurso já foi gasto. Com desembolso antecipado, cada mês sem
manifestação é um mês a mais de exposição à devolução. E se o IMR existir, ele
provavelmente já traz o limiar que falta na DV-018.

**O que já se sabe.** Nenhum dos quatro planos aprovados fixa prazo para o gestor
se manifestar, e três deles não têm vocabulário de consequência nenhum — zero
ocorrências de notificação, retenção, rescisão, devolução ou ressarcimento
(AC-040). O pt_ses_01 é a exceção, e ainda assim coloca a escada na seção de
riscos, não na de monitoramento.

**Status:** `→ professor` — abre na Seção 7, resolve LC-026 e pode resolver LC-018

**Resposta:**

---

### DV-021 · Interlocutor e prazos do monitoramento

**Pergunta.** Qual função da SES-DF recebe o relatório mensal do executor, analisa
e decide — gestor do convênio, área técnica, comissão de acompanhamento? E quais
os prazos: quantos dias o executor tem para enviar depois de fechada a
competência, e quantos dias a SES tem para se manifestar?

**Por que importa.** Monitoramento sem destinatário nomeado é relatório enviado a
ninguém — não há quem se manifeste, e sem manifestação não há consequência. O
pt_ses_01 foi aprovado com esse campo preenchido como "A definir pela SES/DF", e
função, CPF, telefone e e-mail em branco (AC-040). O plano deve nomear a
**função**, não a pessoa, para não vencer quando o servidor mudar.

**O que já se sabe.** Nenhum dos quatro planos nomeia responsável do lado do
concedente nem fixa prazo de análise. Do lado do proponente, o corpus nomeia
coordenação e responsável técnico.

**Status:** `aberta` — abre na Seção 7, resolve LC-026 e LC-027

**Resposta:**

---

### DV-022 · A primeira parcela — quantos meses ela cobre

**Pergunta.** O primeiro recebimento do convênio cobre quantos meses de execução?
E qual é a base de cálculo dele — o custo da etapa de pré-produção, um trimestre
inteiro adiantado, ou um percentual do valor global?

**Por que importa.** É a peça que falta para desenhar a Seção 6. A estrutura de
desembolso já está definida — **um recebimento inicial, depois recebimentos
trimestrais, e um final** —, mas sem saber o alcance do primeiro não se sabe onde
começa o segundo, nem quantas parcelas trimestrais cabem nos 10 meses.

Importa também para o risco: o desembolso é antecipado, então o valor da primeira
parcela é exposição pura. Se ela cobrir um trimestre, o executor recebe três meses
de custo antes de concluir a primeira OCI — e produção aquém do repassado vira
obrigação de devolver (DV-003).

**O que já se sabe.** A 1ª parcela não pode se vincular à Meta 1: nenhuma OCI
estará concluída no mês 1 (Seção 2). Ela se vincula à Meta 2 — os 3 polos aptos —,
aferida pelo IND-03, que não admite tolerância. Isso define o **lastro** da
parcela, não o seu valor.

**Premissa de trabalho adotada em 2026-08-17**, a pedido do usuário e sem
confirmação: **a 1ª parcela cobre os meses 1 a 3**. A Seção 6 foi escrita sobre
ela e declara isso no topo. O quadro de parcelas não muda de estrutura conforme a
resposta — mudam as datas e o número de linhas; a própria seção lista os três
cenários.

**Status:** `→ professor` — premissa assumida, resposta pendente

**Status atualizado (2026-08-18).** Segue com o professor: o usuário vai verificar
se há regra interna na SES. A premissa de trabalho — 1ª parcela cobrindo os meses
1 a 3 — continua declarada no topo da Seção 6.

---

### DV-023 · Como se COMPROVA o uso da rubrica de produção — REFORMULADA

**Reformulada em 2026-08-18.** A pergunta original — "R1 presta contas por produção
aprovada ou por despesa realizada?" — estava mal posta: tratava como alternativas
duas coisas que respondem a perguntas diferentes. O usuário respondeu "despesa
realizada", e a consequência disso (itemizar R1) desmontava o argumento do "sem
incremento", o que revelou o defeito da formulação.

**Separando as duas perguntas:**

| | resposta |
|---|---|
| Como se **calcula** o repasse de R1? | 35.000 × R$ 200,00, valor de tabela, sem incremento — **fechado** |
| Como se **comprova** o uso de R1? | **em aberto — é esta a dúvida** |

**Pergunta.** A prestação de contas da rubrica de produção se satisfaz com a
**produção aprovada no SIA/SUS** como lastro físico, ou exige **documento fiscal
vinculado a item da planilha**, item a item?

**Por que importa.** Decide a estrutura da Seção 5:
- Se basta a produção aprovada: R1 é linha única, como no corpus (AC-015), e o
  "sem incremento" se sustenta.
- Se exige documento fiscal por item: R1 tem de ser itemizada por natureza de
  despesa (M-17), o que expõe a composição de custo do procedimento — exatamente o
  que a remuneração por tabela dispensa.

E decide também o que acontece com saldo: na segunda hipótese, entregar as 35.000
OCI não basta para reter o valor — o que não for comprovado como gasto volta.

**O que já se sabe.** Nenhum dos quatro planos aprovados itemiza a produção
(AC-015). Nenhum descreve a conciliação da rubrica de produção contra despesa.

**Adotado até a resposta:** linha única, lastro físico por produção aprovada.

**Status:** `→ professor` — decide LC-032 e a estrutura da Seção 5

**Resposta:**

---

### DV-024 · Ancoragem no PDS e na PAS

**Pergunta.** Em que diretriz, objetivo e meta do Plano Distrital de Saúde
2024–2027 e da Programação Anual de Saúde vigente este objeto se ancora? Há meta
de redução de fila em cardiologia ou de ampliação de oferta especializada a que o
convênio se vincule?

**Por que importa.** O roteiro exige que a justificativa se ancore em instrumento
de planejamento vigente, e não apenas em dado de fila. Sem isso, a Seção 12
demonstra necessidade e não demonstra alinhamento — que é o que liga o gasto à
política de saúde do DF, e o que um analista de controle procura primeiro.

**O que já se sabe.** Nada: nenhum dos dois instrumentos foi consultado nesta
fase, e o corpus não os cita.

**Status:** `aberta` — abre na Seção 12, resolve LC-042

**Resposta:**

---

### DV-025 · Norma do convênio — RESPONDIDA EM PARTE — BL-003

**Pergunta.** O Decreto DF nº 37.843/2016 regulamenta a Lei nº 13.019/2014 e trata
de parcerias com organizações da sociedade civil. Se o instrumento aqui é
**convênio** em participação complementar ao SUS, e não parceria do MROSC:

1. Esse decreto se aplica mesmo assim, por analogia ou por remissão?
2. Se não se aplica, **qual é a norma distrital** que rege convênios da
   administração do DF — liberação de parcelas, conta específica, retenção,
   prestação de contas?
3. A prática da SES-DF de citar o art. 33 desse decreto em plano de convênio
   (AC-010) é consolidada, ou é imprecisão que passou?
4. Os rendimentos da aplicação financeira dos recursos não empregados incorporam
   o objeto ou são devolvidos ao final?

**Por que importa.** É a BL-003. Hoje o plano nega que o MROSC reja o instrumento
e, ao mesmo tempo, se apoia no decreto que regulamenta o MROSC. Da resposta
dependem: a âncora do desembolso antecipado (OB-015), o degrau de retenção da
Seção 7 (OB-017), a conta específica da Seção 8 (OB-016), o método de pesquisa de
preços da Seção 5 (OB-014) e a natureza da rubrica R1 — remuneração ou custeio
(OB-018, art. 36).

**O que já se sabe.** O texto do decreto foi lido em parte, fornecido pelo
usuário. O vocabulário é inteiramente de parceria. Nenhuma norma distrital de
convênio foi localizada até aqui.

**Status:** `→ professor` — **bloqueante da Seção 13**

**Resposta (2026-08-18, usuário).** A norma para convênios é a **Portaria de
Consolidação GM/MS nº 1, de 28 de setembro de 2017**. Cadastrada como NM-008.

**O que isso resolve.** Desloca o Decreto DF 37.843/2016 — de parceria/MROSC — da
posição de norma do instrumento. A contradição central de BL-003 deixa de existir:
o convênio passa a se apoiar na consolidação federal, e não num decreto de
parceria.

**O que continua aberto.** (1) O **anexo e o artigo** específicos da PRC nº 1/2017
ainda não foram localizados — a norma não foi lida no original. (2) A **camada
distrital** segue vazia, que é a armadilha nomeada no roteiro; ou existe norma do
DF para convênios fora do MROSC, ou o plano cita só a federal e diz por quê.

---

## Respondidas

### DV-002 · Quando uma OCI está concluída — RESPONDIDA

**Resposta (2026-08-17).** A OCI está concluída quando o usuário completa o fluxo
inteiro, **até a consulta de retorno**. Sem consulta de retorno, não há pagamento.

**Consequências, todas já incorporadas:**

1. **A unidade da meta é OCI concluída**, não atendimento realizado.
2. **Há dois pontos de absenteísmo**, entrada e retorno — não um. A oferta de
   vagas de consulta dobra: **87.500**, não 43.750.
3. **A janela de entrada é menor que a vigência.** A última OCI precisa começar
   com um ciclo de folga para concluir dentro dos 9 meses.
4. **A primeira parcela não pode ser vinculada a OCI concluída no mês 1** —
   nenhuma estará.
5. **A teleconsulta de retorno vira alavanca operacional**, não detalhe: a OCI
   admite "consulta **ou** teleconsulta de retorno", e teleconsulta tem menos
   falta e nenhum deslocamento. Protege a meta diretamente.

**Pendente daqui:** a duração do ciclo (entrada → exames → retorno), que define a
janela. Ver DV-011.

---

### DV-012 · Vigência financeira

**Pergunta.** A execução física — até a consulta de retorno — tem que caber nos
9 meses, mas o pagamento é posterior. Quanto tempo depois? A vigência do convênio
cobre esse período, ou há prazo separado para pagamento e prestação de contas?

**Por que importa.** Define onde termina o cronograma da Seção 6. A última parcela
não pode estar dentro da janela de execução física, porque paga produção que ainda
não fechou. Nenhum dos quatro planos separa as duas vigências (AC-033).

**O que já se sabe.** Confirmado que a execução física cabe nos 9 meses e o
pagamento vem depois.

**Status:** `aberta`

**Resposta:**

---

### DV-011 · Duração do ciclo da OCI — RESPONDIDA

**Pergunta.** Quantos dias, na prática, entre a consulta de entrada e o retorno
com resultados? 30, 45, 60?

**Por que importa.** Define a janela de entrada e, com ela, o ritmo diário de
cada polo:

| ciclo | janela de entrada | entradas/mês | por polo/mês | ~/dia útil |
|---|---|---|---|---|
| 30 dias | 8,0 meses | 4.375 | 1.458 | 69 |
| 45 dias | 7,5 meses | 4.667 | 1.556 | 74 |
| 60 dias | 7,0 meses | 5.000 | 1.667 | 79 |
| *(ignorando o ciclo)* | *9,0 meses* | *3.889* | *1.296* | *62* |

A diferença entre a última linha e as outras é o erro que o cronograma cometeria
se tratasse a vigência inteira como janela de produção.

*(Tabela do momento da pergunta: calculada sem descontar a implantação. A curva
final da Seção 2 desconta o mês 1 e chega a 5.000 entradas/mês, não 4.375.)*

**Status:** `respondida`

**Resposta (2026-08-17, usuário).** **30 dias como TETO, factível na operação.**
O tempo médio e o mínimo são menores e acompanham a liberação dos resultados dos
exames — o retorno se marca quando o exame fica pronto, não no trigésimo dia.
Duas regras vêm junto: o retorno é agendado **já na consulta de entrada** sempre
que possível, para garantir o recebimento; e **OCI em andamento é prioridade**
sobre entrada nova.

Vira parâmetro pactuado, não observação: o executor se compromete a devolver o
usuário com os exames prontos em até 30 dias. Curva mensal fechada na Seção 2 —
implantação no mês 1, entradas nos meses 2 a 8, conclusões nos meses 3 a 9,
5.000 por mês em cada ponta. LC-013 fechada.

---

# Bloco novo — 2026-08-19 · lacunas da v2 que dependem da SES-DF

Triagem feita pelo usuário em 19/08/2026: **tudo que depende da SES-DF vira
pergunta para o professor.** As DV abaixo não bloqueiam a redação — bloqueiam
declarar o plano definitivo.

---

### DV-026 · Capacidade da rede própria da SES-DF — → PROFESSOR · **A MAIS IMPORTANTE**

**Pergunta.** Quanto a rede própria da SES-DF produz, por mês, em consulta
cardiológica especializada e em ecocardiografia transtorácica, por unidade, nos
últimos 12 meses — e qual o déficit resultante contra a demanda regulada?

**Por que importa.** É o requisito do **art. 24 da Lei nº 8.080/1990**: o recurso a
serviço privado só se admite quando as disponibilidades do SUS forem insuficientes.
Sem esse número, a insuficiência é afirmada e não demonstrada. **É o único vazio que
atinge a base legal do instrumento**, e não apenas a qualidade do argumento.

**O que já se sabe.** A fila é de 36.125 pessoas com espera média de 776,55 dias
(Mapa Social, 19/08/2026). Fila comprova demanda; a razão entre estoque e vazão da
rede própria é o que comprova insuficiência.

**Status:** `→ professor` — lacuna LC-041, bloqueante.

---

### DV-027 · PAR do DF e habilitação 38.01 — → PROFESSOR

**Pergunta, em quatro partes.** O PAR do Distrito Federal já foi publicado? Contempla
a OCI 09.02.01.002-6? Admite inclusão de novo executor depois de publicado? Qual o
prazo e o rito da Resolução do Colegiado de Gestão do DF?

**Por que importa.** Sem PAR e sem habilitação 38.01 no CNES, o atendimento não vira
APAC. E, pela observação do usuário, o problema real é anterior: uma instituição sem
CNES não obtém aprovação da SES para operar — logo isto é **condição precedente à
contratação**, não risco de execução.

**Status:** `→ professor` — lacuna LC-056, bloqueante.

---

### DV-028 · InvestSUS, limite orçamentário e prazos da concedente — → PROFESSOR

**Pergunta.** Qual o prazo de envio da relação de executores ao InvestSUS e qual
limite orçamentário seria indicado para este executor (LC-057)? E existe prática ou
norma que fixe **prazo para os atos da concedente** — PAR, acessos, FPO, InvestSUS,
regulação das vagas?

**Por que importa.** Hoje o desenho tem consequência contratual só de um lado: o
executor tem prazo, a concedente não. Cada quinzena perdida na partida se acumula
sobre todos os meses seguintes, e a última competência não tem para onde empurrar.

**Status:** `→ professor` — lacunas LC-057 e LC-017.

---

### DV-029 · Volume de fila por Região de Saúde — → PROFESSOR

**Pergunta.** Qual o volume da fila de avaliação cardiológica por Região de Saúde do
DF?

**Por que importa.** Hoje a meta se divide entre os 3 polos por média aritmética
(11.667 cada), declarada como provisória. Com o volume por região, a divisão passa a
ser proporcional à demanda — que é o método do plano aprovado pt_ses_01 (AC-021).

**Status:** `→ professor` — lacuna LC-059.

---

### DV-030 · Regras locais de CID, CBO, autorização prévia e bloqueio — → PROFESSOR

**Pergunta.** Quais as regras locais da SES-DF para CID, CBO, autorização prévia e
bloqueio no SISREG-DF aplicáveis a esta OCI?

**Por que importa.** Regra local não atendida é APAC rejeitada na crítica.

**Nota do usuário (19/08/2026).** Parte disso deve estar publicada — protocolos de
regulação e manuais do SISREG-DF. Buscar antes de perguntar.

**Status:** `→ professor`, com busca própria antes — lacuna LC-058.

---

### DV-031 · Demanda de cardiologia sem filtro de exame — → PROFESSOR

**Pergunta.** Qual a fila de **avaliação cardiológica** no DF, sem filtro de
ecocardiografia — em solicitações, pessoas distintas e espera média?

**Por que importa.** A extração do Mapa Social é por ecocardiografia: mede a ponta da
demanda, não a demanda. Todo o dimensionamento do plano usou esse número como se
fosse a fila inteira.

**O que tentar antes de perguntar.** A mesma consulta ao Mapa Social da Saúde
(MPDFT), trocando o filtro de procedimento por especialidade ou por consulta em
cardiologia. Se o painel não permitir, a pergunta fica.

**Não bloqueia.** O plano segue apresentando 36.125 como **piso declarado** da
demanda — o que é mais defensável do que apresentá-lo como a fila.

**Status:** `→ professor` — lacuna LC-068 (novo id).

---

### DV-032 · Contrarreferência à APS e ouvidoria — → PROFESSOR

**Pergunta.** Qual o mecanismo de contrarreferência à Atenção Primária que a SES-DF
adota (LC-060), e como se dá a integração com a Ouvidoria da SES-DF (LC-067)?

**Por que importa.** LC-060 sustenta o IND-14 e a seção 6.7. LC-067 é secundária — a
recomendação em `ajustes_v3.md` (C3) é encolher a seção 17, e nesse caso a pergunta
some junto.

**Status:** `→ professor` — lacunas LC-060 e LC-067.

---

### DV-033 · Teto PMAE 2026 e estimativa física por OCI — → PROFESSOR

**Pergunta.** Existe distribuição do PMAE por UF para 2026, e qual a estimativa
física de OCI cardiológica prevista para o DF?

**Por que importa.** A produção deste plano equivale a 19,0% do envelope anual do DF
de 2025 (R$ 34.813.717,40), concentrada numa OCI e num executor. Se o ressarcimento
federal não vier, o custo fica integralmente no Fundo distrital.

**O que tentar antes.** O Anexo I da NT 2/2025-DAET traz a produção física estimada
por OCI e por UF, mas é **tabela em imagem** e nunca foi extraída. O PDF está em
`normas/NT 2-2025 teto orcamentario.pdf`.

**Status:** `→ professor`, com extração própria antes — lacuna LC-053.

---

## Atualizações de dúvidas existentes — 2026-08-19

**DV-009 (solicitações devolvidas).** Números atualizados pela extração de
19/08/2026: **21.613 devolvidas** contra **42.724 solicitações** e **36.125 CNS**. A
aritmética que não fecha continua sem fechar, e com a mesma força: se as devolvidas
estivessem dentro das 42.724, restariam **21.111 solicitações para 36.125 pessoas** —
menos pedidos que pessoas. Segue `→ professor`. Corresponde a LC-011, que a v2
perdeu e precisa restabelecer.

**DV-015 (entrada de novos usuários na fila).** **Parte 1 encerrada por decisão do
usuário em 19/08/2026:** o volume mensal de entrada não é necessário e não bloqueia —
mais gente entrando na fila só ajuda a cumprir a meta, e o plano não promete zerar a
fila. **Parte 2 segue aberta:** a ordem em que a regulação encaminha continua
importando, porque define quem chega ao polo. Lacuna LC-016 rebaixada de
estruturante para operacional.
