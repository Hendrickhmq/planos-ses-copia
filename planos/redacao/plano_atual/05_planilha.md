# Seção 5 — Planilha orçamentária e memória de cálculo

Status: `esqueleto` · Nível: **mínimo viável** (melhorias em `redacao/melhorias.md`)
Depende de: Seção 4 · Lacunas: 3 · Valor global: R$ 10.000.000,00
Estrutura: rubrica → descritivo → valor unitário (orientação do professor)
**A rubrica de produção está fechada. A de apoio depende de dados que ainda não existem.**

---

## A linha que organiza a seção inteira

O valor global se divide em duas rubricas de natureza diferente, e a fronteira
entre elas é a decisão mais importante desta seção:

| natureza | rubricas | valor | % | como se justifica |
|---|---|---|---|---|
| **produção assistencial** | R1 | R$ 7.000.000,00 | 70% | 35.000 × R$ 200,00 |
| **apoio não assistencial** | R2 a R7 | R$ 3.000.000,00 | 30% | item a item, `[[lacuna: LC-006]]` |
| **total** | | **R$ 10.000.000,00** | 100% | |

Contrapartida: **zero** — ver Seção 10.

**A regra que separa as duas.** A OCI é pacote fechado: o valor de R$ 200,00 já
remunera consulta de entrada, ecocardiograma, eletrocardiograma, radiografia de
tórax, exames laboratoriais e consulta ou teleconsulta de retorno. Nada disso
pode reaparecer na rubrica de apoio — seria pagar duas vezes o mesmo item. O
argumento é o do corpus (AC-009): a infraestrutura custeada compreende apenas
recursos não assistenciais, não abrangendo equipamento médico, clínico ou
assistencial, que já está no valor unitário do procedimento.

---

## A planilha, por rubrica

Estrutura conforme a orientação do professor: **rubrica → descritivo → valor
unitário**. A etapa da Seção 4 é coluna, não nível hierárquico.

**Quantidade e frequência já estão calculadas** — saem da Seção 2 e da Seção 9,
não de estimativa. O que falta é o **valor unitário** de cada linha.

### R1 · Produção assistencial — R$ 7.000.000,00

**Linha única, ao valor de tabela.** O convênio remunera o procedimento, não os
insumos que o compõem — é a estrutura do corpus (AC-015) e é o que sustenta a
decisão de seguir a SIGTAP sem incremento.

| item | descritivo | etapa | origem do preço | unid. | qtd | freq | valor unit. | total |
|---|---|---|---|---|---|---|---|---|
| 1.1 | OCI 09.02.01.002-6 — Avaliação Cardiológica, concluída | 2 | Tabela SUS, Portaria SAES/MS 1.822/2024, comp. 04/2026 | OCI | 35.000 | 1 | R$ 200,00 | **R$ 7.000.000,00** |
| | ***sub-total R1*** | | | | | | | **R$ 7.000.000,00** |

**Memória de cálculo:**

```
35.000 OCI concluídas × R$ 200,00  =  R$ 7.000.000,00
              verificação D: 35.000 × 1 × 200,00 = 7.000.000,00 ✓
```

**Por que R1 não é itemizada, e o que isso deixa em aberto.** Itemizar a produção
— equipe assistencial, exames, insumos, equipamento médico — exigiria expor a
composição de custo do procedimento, que é exatamente o que a remuneração por
tabela dispensa. Desmontaria o argumento do "sem incremento" da Seção 1.

A alternativa existe, está desenhada e está guardada em `melhorias.md` (M-17). Ela
só entra se a resposta da **DV-023 reformulada** disser que a produção precisa de
comprovação por documento fiscal vinculado a item da planilha. Enquanto isso, o
lastro de R1 é físico: produção aprovada no SIA/SUS, por competência.

**Volumes que a rubrica compromete** — derivados da Seção 2, para conferência de
capacidade na Seção 9, não para compor preço:

| | total | por mês cheio | por dia útil (3 polos) |
|---|---|---|---|
| consultas (entrada + retorno) | 70.000 | 8.250 | 393 |
| ecocardiogramas | 35.000 | 4.125 | 196 |
| eletrocardiogramas | 35.000 | 4.125 | 196 |
| radiografias de tórax | 35.000 | 4.125 | 196 |
| painéis laboratoriais | 35.000 | 4.125 | 196 |

### R2 a R7 · Apoio não assistencial — R$ 3.000.000,00

**Preenchida em 2026-08-18 com valores de referência do pt_ses_01** — plano
aprovado pela SES-DF —, ajustados ao desenho deste plano: 3 polos em vez de 4,
10 meses em vez de 9, e sem os cargos de apoio direto ao exame, que aqui são
assistenciais e ficam dentro de R1.

⚠️ **Estes valores não são pesquisa de preços.** São referência de plano aprovado,
com a coluna `ref.` apontando o item de origem. LC-023 continua aberta: para uso
real, cada linha precisa de pesquisa de mercado própria, com data.

| rubrica | item | descritivo | ref. pt_ses_01 | unid. | qtd | freq | valor unit. | total |
|---|---|---|---|---|---|---|---|---|
| **R2 · Pessoal não assistencial** | 2.1 | Direção executiva do projeto | 1.1.1 | mês | 1 | 10 | R$ 14.500,00 | R$ 145.000,00 |
|  | 2.2 | Coordenação administrativa e financeira | 1.1.2 | mês | 1 | 10 | R$ 10.500,00 | R$ 105.000,00 |
|  | 2.3 | Coordenação operacional | 1.1.4 | mês | 1 | 10 | R$ 9.500,00 | R$ 95.000,00 |
|  | 2.4 | Supervisão de polo — 1 por polo | 1.1.11 | mês | 3 | 10 | R$ 6.155,00 | R$ 184.650,00 |
|  | 2.5 | Recepção e acolhimento — 2 por polo | 1.1.7 | mês | 6 | 10 | R$ 4.155,00 | R$ 249.300,00 |
|  | 2.6 | Agendamento e gestão de agenda no SISREG — 2 por polo | 1.1.5 | mês | 6 | 10 | R$ 4.549,94 | R$ 272.996,40 |
|  | 2.7 | Busca ativa — 1 por polo | 1.1.5 | mês | 3 | 10 | R$ 4.549,94 | R$ 136.498,20 |
|  | 2.8 | Faturamento e registro de APAC — 1 por polo | 1.1.5 | mês | 3 | 10 | R$ 4.549,94 | R$ 136.498,20 |
| **R3 · Locação de espaço físico** | 3.1 | Locação de espaço físico — Polo 1 | 1.2.1 | mês | 1 | 10 | R$ 26.300,97 | R$ 263.009,70 |
|  | 3.2 | Locação de espaço físico — Polo 2 | 1.2.2 | mês | 1 | 10 | R$ 26.441,41 | R$ 264.414,10 |
|  | 3.3 | Locação de espaço físico — Polo 3 | 1.2.3 | mês | 1 | 10 | R$ 29.991,46 | R$ 299.914,60 |
| **R4 · TI, sistema e material** | 4.1 | Locação de notebooks — 4 por polo | 1.2.5 | mês | 12 | 10 | R$ 450,00 | R$ 54.000,00 |
|  | 4.2 | Locação de impressoras multifuncionais — 2 por polo | 1.2.6 | mês | 6 | 10 | R$ 380,00 | R$ 22.800,00 |
|  | 4.3 | Sistema de gestão operacional | 1.2.11 | mês | 1 | 10 | R$ 7.500,00 | R$ 75.000,00 |
|  | 4.4 | Material de consumo administrativo e de apoio | 1.2.10 (ajustado) | mês | 1 | 10 | R$ 9.234,55 | R$ 92.345,50 |
| **R5 · Conectividade** | 5.1 | Internet — 2 links por polo | 1.2.7 | mês | 6 | 10 | R$ 150,00 | R$ 9.000,00 |
|  | 5.2 | Telefonia — insumo da busca ativa | sem referência | mês | 3 | 10 | R$ 500,00 | R$ 15.000,00 |
| **R6 · Serviços gerais e utilidades** | 6.1 | Limpeza e conservação | 1.1.12 | mês | 1 | 10 | R$ 10.500,00 | R$ 105.000,00 |
|  | 6.2 | Vigilância patrimonial — 1 posto por polo | 1.1.13 | mês | 3 | 10 | R$ 7.500,00 | R$ 225.000,00 |
|  | 6.3 | Energia elétrica | 1.2.8 | mês | 1 | 10 | R$ 3.751,16 | R$ 37.511,60 |
|  | 6.4 | Água | 1.2.9 | mês | 1 | 10 | R$ 3.751,17 | R$ 37.511,70 |
| **R7 · Encerramento e transparência** | 7.1 | Assessoria de prestação de contas | 3.1.1 | mês | 1 | 10 | R$ 5.455,00 | R$ 54.550,00 |
|  | 7.2 | Comunicação institucional e transparência | 3.1.3 | mês | 1 | 10 | R$ 12.000,00 | R$ 120.000,00 |
| | | ***sub-total R2*** | | | | | | **R$ 1.324.942,80** |
| | | ***sub-total R3*** | | | | | | **R$ 827.338,40** |
| | | ***sub-total R4*** | | | | | | **R$ 244.145,50** |
| | | ***sub-total R5*** | | | | | | **R$ 24.000,00** |
| | | ***sub-total R6*** | | | | | | **R$ 405.023,30** |
| | | ***sub-total R7*** | | | | | | **R$ 174.550,00** |
| | | **TOTAL APOIO (R2 a R7)** | | | | | | **R$ 3.000.000,00** |

**Tudo locado, nada adquirido** (decisão de 2026-08-17). Unidade = mês e
frequência = meses de uso em todas as linhas.

**O item 4.4 é o de fechamento.** Material de consumo é a única linha genuinamente
elástica da planilha, e absorve a diferença entre a soma das demais
(R$ 2.907.654,50) e o teto da rubrica. O pt_ses_01 pratica R$ 11.740,00/mês no item
equivalente; aqui ficou em R$ 9.234,55. Quando a pesquisa de preços entrar, a
diferença se redistribui e esta linha volta a ter valor próprio.

**Validação de ordem de grandeza.** O pt_ses_01 gastou **R$ 2.772.671,65** de apoio
para 36.000 OCI, 4 polos e 9 meses. Este plano prevê **R$ 3.000.000,00** para
35.000 OCI, 3 polos e 10 meses — envelope 8% maior para um mês a mais de operação e
um polo a menos. A comparação não valida preço unitário; valida que o teto de 30%
é plausível para a operação descrita.

**Três cargos do pt_ses_01 que este plano NÃO traz no apoio:** auxiliares de apoio
aos exames, assistentes clínicos e assistentes de preparação (pré-atendimento).
Eles reprovam na pergunta 2 do teste abaixo — participam da execução do pacote e,
portanto, já estão remunerados pelo valor de tabela. É diferença deliberada em
relação ao corpus, não omissão.

**TOTAL GERAL: R$ 10.000.000,00**

---

## Resumo por etapa — a ponte com a Seção 4

Derivado da coluna `etapa`. Existe para que subtotal de etapa e cronograma físico
continuem conferíveis com a rubrica no primeiro nível.

Critério de rateio, declarado: o apoio corre por mês ao longo dos 10 meses
(R$ 300.000,00/mês); a Etapa 1 consome meia mensalidade (2 semanas), a Etapa 3
consome a do mês 10, e a Etapa 2 o restante. A produção segue a curva de
conclusões da Seção 2 — 30.875 OCI nas etapas iniciais e 4.125 no mês 10.

| etapa | apoio | produção | total |
|---|---|---|---|
| 1 · Pré-produção (2 semanas) | R$ 150.000,00 | — | **R$ 150.000,00** |
| 2 · Execução assistencial | R$ 2.550.000,00 | R$ 6.175.000,00 | **R$ 8.725.000,00** |
| 3 · Encerramento (mês 10) | R$ 300.000,00 | R$ 825.000,00 | **R$ 1.125.000,00** |
| **total** | **R$ 3.000.000,00** | **R$ 7.000.000,00** | **R$ 10.000.000,00** |

**Item que atravessa etapas tem a frequência repartida, não duplicada.** Cada
locação aparece uma vez na planilha, com a frequência total em meses; é este resumo
que a distribui. Duplicar a linha é como o pt_ses_01 acabou declarando 16 locações
mensais para uma planilha que soma 18 (AC-001).

---|---|---|
| 1 · Pré-produção | parcelas iniciais de R2 a R6 — as 2 primeiras semanas | `[[lacuna]]` |
| 2 · Execução assistencial | R1 integral + operação corrente de R2 a R6 | `[[lacuna]]` |
| 3 · Encerramento | R7, mais a fração de R2 que se estende ao mês 10 | `[[lacuna]]` |
| | **total** | **R$ 10.000.000,00** |

**Item que atravessa etapas tem a frequência repartida, não duplicada.** Uma
locação usada nas etapas 1 e 2 aparece uma vez na planilha, com a frequência total
em meses; o resumo por etapa a distribui. Duplicar a linha é como o pt_ses_01
acabou declarando 16 locações mensais para uma planilha que soma 18 (AC-001).

---

## Origem do preço — os quatro caminhos admissíveis

Até 2026-08-17 a coluna "origem do preço" era critério próprio deste rascunho.
Deixou de ser: o Decreto DF nº 37.843/2016, art. 28, §3º, nomeia as formas pelas
quais a compatibilidade dos custos com o mercado é examinada (OB-014).

| via | o que serve como origem | o que precisa constar |
|---|---|---|
| I | preço público de contratação similar em sistema público de compras | identificação do sistema e da contratação |
| II | ajuste, parceria ou contratação de outro ente público | finalizada até **180 dias** antes da pesquisa, ou em execução |
| III | pesquisa em mídia ou sítio especializado | **domínio consultado, data e hora de acesso** |
| IV | proposta escrita de fornecedor | razão social, CNPJ e assinatura de preposto ou representante legal |

Cada linha da planilha usa **uma** dessas quatro e a identifica. A via III é a
mais fácil e a mais fácil de reprovar: sem domínio, data e hora, não serve.

⚠️ **Condicionado a BL-003.** Este dispositivo vem de decreto de parceria (MROSC).
Se o instrumento for convênio fora desse regime, o método continua sendo boa
prática, mas perde a força de exigência — e a norma aplicável precisa ser
localizada.

---

## Duas linhas que faltam na planilha

O mesmo art. 28 exige do plano de trabalho dois itens que este rascunho **não
tem**:

| inciso | exigência | onde entra | id |
|---|---|---|---|
| V | valores dos tributos e encargos sociais e trabalhistas incidentes, **ou** informação sobre imunidade ou isenção | rubricas R2 a R7 e nota própria | OB-012 |
| VI | percentuais e valores provisionados para **verbas rescisórias**, quando houver repasse para despesas de pessoal | R2, que remunera pessoal não assistencial | OB-013 |

`[[lacuna: LC-024 — encargos e tributos sobre a folha de R2, ou a declaração de
imunidade/isenção da entidade; e o percentual de provisão rescisória]]`

Entidade filantrópica costuma ter imunidade ou isenção, e o inciso V admite isso
expressamente — mas exige que seja **declarado**, não omitido. Omissão aqui é o
tipo de coisa que volta como diligência.

---

## DV-023 reformulada — a pergunta estava errada

A pergunta original — "R1 presta contas por produção aprovada ou por despesa
realizada?" — tratava como alternativas duas coisas que são respostas a perguntas
diferentes:

| pergunta | resposta |
|---|---|
| Como se **calcula** o repasse de R1? | 35.000 × R$ 200,00, valor de tabela, sem incremento |
| Como se **comprova** o uso de R1? | **é isto que segue em aberto** |

Se a comprovação exigir documento fiscal vinculado a item da planilha, R1 precisa
ser itemizada (M-17) e o "sem incremento" cai. Se bastar a produção aprovada no
SIA/SUS como lastro físico, a linha única basta e o desenho atual se mantém.

**Adotado até resposta: linha única, lastro físico.** É o que o corpus faz e o que
o nível mínimo viável pede. `[[lacuna: LC-032 — forma de comprovação de R1]]`,
DV-023.

---

## Comparativo de remuneração do pacote — DD-002

Fonte: comparativo fornecido pelo proponente em 2026-08-18, arquivado em
`registros/fontes/comparativo_precos_oci_df.csv`, cadastrado como DD-002.

| item do pacote | OCI SUS | convênios (base CBHPM/DF) | particular |
|---|---|---|---|
| consulta inicial | incluso | R$ 120,00 a R$ 150,00 | R$ 300,00 a R$ 500,00 |
| consulta de retorno | incluso | não remunerada à parte | geralmente isenta em 15 a 30 dias |
| ecocardiograma transtorácico | incluso | R$ 160,00 a R$ 220,00 | R$ 280,00 a R$ 450,00 |
| eletrocardiograma | incluso | R$ 35,00 a R$ 50,00 | R$ 70,00 a R$ 120,00 |
| radiografia de tórax | incluso | R$ 45,00 a R$ 60,00 | R$ 80,00 a R$ 150,00 |
| laboratório básico | incluso | R$ 50,00 a R$ 80,00 | R$ 80,00 a R$ 150,00 |
| **total do pacote** | **R$ 200,00** | **R$ 410,00 a R$ 560,00** | **R$ 810,00 a R$ 1.370,00** |

**O que este quadro demonstra:** a OCI remunera entre **36% e 49%** do que os
convênios pagam pelo mesmo conjunto de procedimentos no DF, e entre 15% e 25% do
particular.

**O que ele NÃO demonstra, e a diferença importa:** isto é **remuneração
comparada, não custo**. Saber que o mercado paga R$ 410,00 não diz quanto custa
produzir. **LC-025 continua aberta** — o que fecha R-05 é o custo unitário do
executor, não o preço de terceiros.

Ainda assim o quadro tem duas utilidades imediatas: é evidência de economicidade
para a Seção 12 — o mesmo pacote pela metade do preço de mercado — e é o primeiro
indício quantificado de que a margem, se existir, é estreita.

---

## O teste de não-assistencialidade

Todo item candidato à rubrica de apoio responde três perguntas. Reprovar em
qualquer uma o elimina:

1. **É equipamento ou insumo médico, clínico ou assistencial?** Se sim, sai — já
   está no valor unitário do procedimento (AC-009).
2. **Está na composição da OCI?** Consulta, ecocardiograma, eletrocardiograma,
   radiografia de tórax, exames laboratoriais e retorno já são remunerados. Se o
   item é um deles, ou parte dele, sai.
3. **Tem origem de preço citável?** Pesquisa de mercado, tabela oficial ou
   contrato anterior, com referência verificável. Sem origem, o item não entra —
   vira lacuna, não estimativa.

**Consequência prática para a equipe:** cardiologista, ecocardiografista, técnico
que opera o exame e demais profissionais que executam o pacote **não entram na
rubrica de apoio** — são custeados pelos R$ 7.000.000,00 da produção. Entram no
apoio apenas recepção, agendamento, busca ativa, administrativo e coordenação
não assistencial. A Seção 9 tem que espelhar essa divisão, cargo a cargo.

---

## As regras aritméticas, declaradas antes de haver número

Escritas aqui porque são o que o `conferir.py` cobra dos planos alheios, e valem
igual para este:

1. **`total = quantidade × frequência × valor unitário`**, linha a linha
   (verificação D).
2. **Subtotal de etapa = soma dos itens da etapa; total geral = soma dos
   subtotais** (verificação C). No pt_ses_04 uma linha de subtotal sem rótulo fez
   o total geral estourar em R$ 1.169.110,00 — e o plano foi aprovado assim
   (AC-005).
3. **Frequência declarada em texto = soma das frequências da planilha.** O
   pt_ses_01 declara 16 locações mensais e a planilha soma 18 (AC-001).
4. **Convenção decimal única** — `1.216,00`, nunca `1,216.00`. O pt_ses_01 mistura
   as duas na mesma planilha.
5. **Frequência máxima = 10**, a vigência. Item com frequência maior que a
   vigência é erro aritmético, não escolha (AC-003: o pt_ses_01 tem internet com
   frequência 10 numa vigência de 9).
6. **Quantidade da descrição = quantidade da coluna.** O pt_ses_01 contrata 12
   notebooks no texto e escreve 16 na coluna (AC-002).

---

## Locação, não aquisição

O corpus custeia o apoio por **locação**, não por compra: locação de espaço,
locação de equipamento de TI, com frequência mensal amarrada aos meses de
ativação de cada polo. Contagem nos quatro planos: locação aparece 7 vezes contra
3 de aquisição no pt_ses_01, e 4×0, 4×0 e 3×0 nos demais — nenhum estrutura o
apoio como compra de bem permanente (AC-039).

**Decisão do proponente (2026-08-17): alugado.** Todo o apoio material — espaço,
equipamento de TI, mobiliário — entra como locação. Fecha com a prática do corpus
e com o desenho do convênio: a vigência de 10 meses não amortiza bem permanente,
e não se cria a questão da destinação do bem ao término.

Consequência para a planilha: os itens de apoio material têm **unidade = mês** e
**frequência = número de meses de uso**, nunca quantidade única com valor cheio.
E a frequência de cada item precisa bater com os meses em que o polo
correspondente opera — é onde o pt_ses_01 errou, declarando 16 locações mensais
para uma planilha que soma 18 (AC-001).

---

## A tensão do art. 36 — repasse não é pagamento por serviço

O art. 36 do Decreto DF nº 37.843/2016 diz que os recursos ficam **vinculados ao
plano de trabalho** e **não caracterizam receita própria nem pagamento por
prestação de serviços** (OB-018).

Isso conversa mal com a redação atual da rubrica R1, escrita como remuneração:
`35.000 OCI × R$ 200,00`. Se o regime desse decreto se aplicar, R1 precisa mudar
de figura — deixa de ser preço por unidade entregue e passa a ser **estimativa de
custo da execução do objeto**, dimensionada pelo valor de referência da Tabela
SUS. O número não muda; o que muda é o que ele significa juridicamente, e com
isso muda a prestação de contas: não se comprova "produção vendida", comprova-se
"recurso aplicado no objeto".

Está condicionado a **BL-003**, e é a razão pela qual aquele bloqueante não é
formalidade: ele decide se a Seção 5 fala de remuneração ou de custeio.

---

## O alerta que esta seção produz

**A rubrica de apoio não pode cobrir déficit assistencial.** Se o custo real de
executar uma OCI — dois atendimentos médicos, ecocardiograma, eletrocardiograma,
radiografia, laboratório — for maior que R$ 200,00, o plano tem um problema de
viabilidade que a rubrica de apoio **legalmente não resolve**: usá-la para
complementar assistência é exatamente o que o teste acima proíbe, e é o que
transformaria o "sem incremento" em incremento disfarçado.

Isso precisa ser verificado antes de a planilha ser preenchida, não depois. É
risco de execução e vai nomeado na Seção 11.

---

## O que falta, e de quem depende

| id | o que | de quem |
|---|---|---|
| LC-006 | Itemização dos R$ 3.000.000,00 de apoio: o que se contrata, em que quantidade, por quantos meses | proponente |
| LC-023 | Origem de cada preço, por uma das quatro vias do art. 28, §3º (OB-014) | proponente |
| LC-024 | Tributos e encargos sobre a folha de R2, ou declaração de imunidade/isenção; e provisão de verbas rescisórias | proponente, OB-012 e OB-013 |
| LC-025 | Custo real por OCI, para verificar se R$ 200,00 cobre a assistência | proponente |

Nenhuma bloqueia a redação das outras seções. Todas bloqueiam **fechar esta**: sem
itemização não há subtotal, sem subtotal não há cronograma de desembolso (Seção 6)
e sem valor por etapa a Seção 11 não tem o que classificar como risco financeiro.

---

## Fundamento

- **OB-003** — Lei 8.080/90, art. 26: remuneração dos serviços contratados
  segundo critérios e valores fixados pela direção nacional do SUS. É a âncora
  legal do "sem incremento" e, portanto, da linha 2.1. `a_verificar`.
- **OB-007** — Portaria SAES/MS nº 1.822/2024, Anexo: a composição da OCI, que é
  o que define quais itens **não** podem aparecer no apoio. `a_verificar`,
  **Anexo não lido** — é a lacuna mais cara desta seção.

Nenhuma lida no original.
