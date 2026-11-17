# Seção 7 — Monitoramento e avaliação

Status: `rascunho` · Nível: **mínimo viável** (melhorias em `redacao/melhorias.md`)
Depende de: Seção 3 · Lacunas: 3 (nenhuma bloqueante)
Periodicidade: mensal, por competência · Indicadores: os da Seção 3, sem métrica nova

---

## Quem monitora

| lado | quem | o que faz |
|---|---|---|
| **proponente** | Coordenação do Projeto — cargo, não pessoa | apura os indicadores, produz o relatório mensal, executa o plano de recuperação quando acionado |
| **proponente** | Responsável Técnico Assistencial, com RQE | responde pela conformidade clínica do pacote e pelo desfecho registrado |
| **concedente** | `[[lacuna: LC-026 — a função da SES-DF que recebe, analisa e decide]]` | recebe o relatório, analisa, manifesta-se no prazo e decide a consequência |

**Por que a lacuna do concedente não é detalhe.** O pt_ses_01 foi aprovado com
esse campo preenchido como "A definir pela SES/DF", e função, CPF, telefone e
e-mail em branco (AC-043). Monitoramento sem destinatário nomeado é relatório
enviado a ninguém: não há quem se manifeste, e sem manifestação não há
consequência. Este plano nomeia a **função**, não a pessoa — assim o instrumento
não vence quando o servidor muda. `[[DV-021]]`

---

## O que se olha, e quem apura

Os indicadores são os da Seção 3. Nenhuma métrica nova nasce aqui — se algo
precisa ser medido e não está lá, o lugar de corrigir é a Seção 3.

| indicador | apura | fonte | periodicidade | gera consequência? |
|---|---|---|---|---|
| IND-01 execução física mensal | proponente, conferido pelo concedente | SIA/SUS, produção aprovada | mensal | **sim** |
| IND-02 cobertura acumulada | proponente, conferido pelo concedente | consolidação das competências | mensal | **sim** |
| IND-03 implantação dos polos | concedente | documentos da Etapa 1 | única | **sim** — libera a 1ª parcela |
| IND-04 preenchimento das vagas reguladas | proponente | SISREG | mensal | não — **defende** o executor |
| IND-05 comparecimento, entrada e retorno | proponente | SISREG + TrakCare | mensal | não |
| IND-06 recuperação do faltoso | proponente, conciliado no SISREG | registro de contato + SISREG | mensal | não |
| IND-07 ciclo em até 30 dias | proponente | TrakCare | mensal | não |
| IND-08 completude do registro | proponente | sistemas oficiais | mensal | não |
| IND-09 a IND-11 qualitativos | proponente | TrakCare + SISREG | mensal | não |

---

## O ciclo mensal — quem recebe, em quanto tempo, e o que decide

A armadilha desta seção é descrever o envio do relatório e parar aí. O que
importa é o que acontece depois que ele chega.

```
fecha a competência
      │
      ├─ (1) executor apura os 8 indicadores e envia o relatório mensal
      │        prazo: até [[lacuna: LC-027]] dias do fechamento
      │
      ├─ (2) concedente analisa e SE MANIFESTA
      │        prazo: até [[lacuna: LC-027]] dias do recebimento
      │        silêncio no prazo NÃO equivale a aprovação
      │
      └─ (3) a manifestação decide uma de três coisas:
               • conforme          → segue o cronograma, libera a parcela seguinte
               • conforme com ressalva → segue, com ponto a corrigir na competência seguinte
               • não conforme      → aciona a escada de consequências abaixo
```

O relatório mensal contém, no mínimo: os onze indicadores com numerador e
denominador explícitos, a produção apresentada **e** a aprovada por competência,
a relação de vagas ofertadas contra reguladas por polo, e o registro da busca
ativa conciliado com os reagendamentos do SISREG. Relatório do executor nunca
vale sozinho — cada número tem âncora em sistema oficial (AC-038).

---

## A escada de consequências

**O corpus tem metade disto, e a metade que falta é a que faz funcionar.** A
contagem de vocabulário nos quatro planos dá notificação 0, glosa 0, retenção 0,
advertência 0, sanção 0, plano de recuperação 0 (AC-041) — mas o pt_ses_01 traz,
na seção de riscos e com outras palavras, uma ordem escalonada de medidas
compensatórias: remanejamento de quantitativos, ações compensatórias, aplicação do
instrumento de medição de resultados e, por último, devolução do valor não
executado (AC-042).

Ou seja: a ideia de escada existe no corpus. **O que não existe é gatilho, limiar
e prazo** — a partir de que desvio cada medida se aplica, quanto conta como
descumprimento e em quanto tempo. Sem isso a ordem está escrita e não é
acionável. É essa parte que a tabela abaixo acrescenta.

Aqui existe, e por uma razão estrutural: **o desembolso é antecipado**. O dinheiro
entra antes da despesa, então o que se discute quando a meta não fecha não é
quanto pagar — é quanto devolver. Sem escada escrita, a única saída seria a
rescisão, que é desproporcional para um mês ruim.

| degrau | quando | o que acontece | quem aciona |
|---|---|---|---|
| **1 · notificação** | IND-01 abaixo do limiar em uma competência | executor apresenta justificativa em prazo definido | concedente |
| **2 · plano de recuperação** | duas competências consecutivas abaixo, ou IND-02 abaixo do limiar acumulado | executor apresenta plano com prazo e meta de recuperação; a recuperação é aferida pelo IND-02, não pelo IND-01 | concedente, sob análise |
| **3 · retenção da parcela seguinte** | plano de recuperação descumprido | a liberação da parcela fica suspensa até a recomposição do acumulado | concedente |
| **4 · devolução proporcional** | encerramento com produção aprovada abaixo do repassado | devolução da diferença, apurada na Seção 8 | concedente |

Antes do degrau 4, cabem as medidas que o pt_ses_01 nomeia e que este plano
adota na mesma ordem: **remanejamento de quantitativos entre polos** — que a
cláusula de ajuste pelo SISREG já autoriza (Seção 2) — e **ações compensatórias**
dentro da vigência. Devolução é a última medida, não a primeira.

`[[lacuna: LC-018 — o limiar que aciona o degrau 1, a janela de compensação do
degrau 2 e os prazos de cada degrau. É DV-018, ao professor.]]`

### A âncora normativa do degrau 3 — e o que faltava nela

O Decreto DF nº 37.843/2016, art. 35, prevê a **retenção de parcelas** em três
hipóteses: evidência de irregularidade na aplicação de parcela anterior; desvio de
finalidade ou inadimplemento; e falta de adoção das medidas saneadoras apontadas
pela administração ou pelos órgãos de controle (OB-017).

E acrescenta o que a escada não tinha: **devido processo.** A decisão de reter
comporta **recurso administrativo em 10 dias**, dirigido à autoridade que decidiu,
que reconsidera em 5 dias ou encaminha à superior — com possibilidade de efeito
suspensivo quando houver justo receio de prejuízo de difícil reparação.

O degrau 3 passa a ser redigido com isso: retenção não é ato imediato e definitivo,
é decisão recorrível. Para o executor, é a diferença entre ficar sem a parcela e
poder discutir antes de ficar.

⚠️ **Condicionado a BL-003** — dispositivo de decreto de parceria. Se o instrumento
for convênio fora do MROSC, a escada continua de pé pelo desenho do plano, mas
perde esta âncora e o rito do recurso precisa vir de outra norma.

A escada é proporcional de propósito: um mês abaixo é oscilação de agenda, dois
meses é tendência, plano descumprido é inadimplemento. Rescisão não entra na
escada — é do instrumento, não do plano de trabalho.

---

## Antes da consequência, a causa

Regra que precede todos os degraus: **a análise identifica de que lado do fluxo
veio a falha antes de decidir a consequência.** O executor controla a oferta de
vaga, o atendimento, o retorno e o registro. Não controla a regulação, que é da
SES-DF (Seção 2).

| IND-04 | IND-01 | leitura | consequência |
|---|---|---|---|
| alto | alto | tudo correndo | nenhuma |
| **alto** | **baixo** | vagas foram preenchidas e a produção não saiu | é do executor — aciona a escada |
| **baixo** | **baixo** | vagas ofertadas e não reguladas: capacidade ociosa | **não é descumprimento do executor** |
| baixo | alto | ofertou pouco e entregou muito | revisar dimensionamento, não punir |

A terceira linha é a razão de o IND-04 existir. Sem ele, sub-regulação e
sub-execução são indistinguíveis no relatório, e a segunda paga pela primeira. O
que o plano ainda não sabe é o que acontece com a **meta** nessa hipótese — se é
reajustada, se o prazo se estende, ou se o valor se readequa (DV-016).

---

## Avaliação final

Ao término da vigência física, avaliação consolidada com: execução acumulada por
polo contra a meta pactuada (IND-02), série mensal dos oito indicadores,
demonstrativo de produção apresentada contra aprovada, e o resultado da busca
ativa. É o insumo da prestação de contas (Seção 8) e o que sustenta — ou não — a
inexistência de valor a devolver.

---

## Lacunas

| id | descrição | como se resolve |
|---|---|---|
| LC-018 | Limiar de aferição, janela de compensação e prazos de cada degrau da escada. | DV-018, → professor |
| LC-026 | Qual função da SES-DF recebe, analisa e decide. | DV-021 |
| LC-027 | Prazo de envio do relatório e prazo de manifestação do concedente. | DV-021, e o instrumento |

Nenhuma bloqueante. A estrutura do monitoramento — quem, o quê, com que fonte, em
que ordem, com que consequência — está escrita. O que falta são prazos e limiares,
que são pactuação, não pesquisa.

---

## Fundamento

- **OB-004** — Lei 8.080/90, art. 26, §2º: os serviços contratados submetem-se às
  normas técnicas e administrativas e aos princípios e diretrizes do SUS. É a
  âncora da supervisão pelo concedente. `a_verificar`, numeração do parágrafo a
  confirmar.
- **OB-009** — Manual Operacional da FPO: a validação da produção contra a FPO é
  o que dá objetividade ao IND-01. `a_verificar`.

Nenhuma lida no original.
