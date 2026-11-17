# plano/modelo.md — o esqueleto do plano de trabalho

O esqueleto de qualquer plano de convênio de emenda com a SES-DF para produção
assistencial ambulatorial, **seja ele de OCI ou de procedimento avulso** (exame,
consulta), na estrutura `padrao` de `estrutura.md`. Montado em 27/09/2026 a partir do
padrão de então, dos dois planos que o projeto
já redigiu (`redacao_03`, OCI de câncer gástrico; `redacao_04`, exames de
ultrassonografia e tomografia) e das lições de `registros/licoes.csv`.

O que está pronto aqui é a parte **administrativa, financeira e de gestão** — igual em
qualquer objeto. O que depende do procedimento está marcado, e cada marca diz de onde
vem a resposta. A parte assistencial está reunida no **Anexo A**, em perguntas.

**Fronteira anticópia (comum, regra 13):** nenhum parágrafo daqui veio de plano
aprovado. Os aprovados geraram lições; o texto é do projeto.

---

## Como se usa

1. Fechar a **fase 0** de `procedimento.md`: nada se escreve antes.
2. Copiar as seções 1 a 9 para `planos/redacao_NN/plano.md`, e criar o `estado.yaml`
   com as chaves de `procedimento.md`.
3. Escolher a variante de cada trecho `{OCI: … | exame: …}` e apagar a outra.
4. Substituir cada marca pela resposta. Marca que sobra no documento é erro que a
   verificação **L** acusa.
5. Conferir como manda `conferencia.md`.

**As marcas:**

| marca | o que é | quem responde | sai do documento? |
|---|---|---|---|
| `[preencher: …]` | dado cadastral, do termo ou da emenda | proponente / SES-DF | só pode ficar em campo de identificação |
| `[[assistencial: …]]` | parâmetro clínico ou de fluxo | área assistencial — Anexo A | sim, sempre |
| `[[preço: …]]` | preço de mercado | pesquisa de preço, registrada em `dados/` | sim, sempre |
| `{OCI: … \| exame: …}` | trecho que muda com a modalidade | escolha | fica uma das duas |
| `> Lições: …` | o que conferir nesta subseção | `python3 ferramentas/consultar.py LI-NNN` | sim, sempre |

---

# PLANO DE TRABALHO

## 1. Identificação

> Lições: LI-027, LI-029, LI-039

### 1.1 Dados cadastrais do proponente

| | |
|---|---|
| **Razão social** | [preencher] |
| **CNPJ** | [preencher] |
| **Endereço** | [preencher] |
| **CNES do proponente** | [preencher] |
| **Telefone e correio eletrônico institucional** | [preencher] |
| **Representante legal** | [preencher: nome, cargo, CPF] |
| **Responsável pelo acompanhamento do convênio** | [preencher: nome, função, CPF e correio eletrônico] |

### 1.2 Dados do instrumento

| | |
|---|---|
| **Concedente** | Secretaria de Estado de Saúde do Distrito Federal — SES-DF |
| **Processo SEI** | [preencher] |
| **Instrumento** | convênio |
| **Objeto** | {OCI: execução de [N] Ofertas de Cuidado Integrado [código] — [nome da tabela] \| exame: realização de [N] exames de [tipo], com entrega de laudo} |
| **Origem do recurso** | emenda parlamentar federal — incremento temporário do custeio de Média e Alta Complexidade |
| **Emenda parlamentar** | [preencher: número, autor e RP] |
| **Programa de trabalho / natureza da despesa** | [preencher] |
| **Valor global** | [o do termo, ao centavo] |
| **Vigência** | [a do termo] meses, contados da assinatura |
| **Parcelas** | [número] |

## 2. Objeto

### 2.1 Descrição do objeto

> Lições: LI-004

{OCI: Execução de **[N] ([por extenso]) Ofertas de Cuidado Integrado do código
[código] — [nome exato da tabela]**, destinadas a usuários do Sistema Único de Saúde
encaminhados pelo Complexo Regulador da SES-DF, em [n] polos distribuídos no território
do Distrito Federal.

| exame: Realização de **[N] exames de [tipo]** em usuários do Sistema Único de Saúde
com solicitação pendente na fila de regulação da SES-DF, com entrega do laudo ao
usuário ou à unidade de saúde solicitante, em [n] polos distribuídos no território do
Distrito Federal.}

### 2.2 Composição

> Lições: LI-001, LI-002, LI-003, LI-004 · OB-047

{OCI: A Oferta de Cuidado Integrado é unidade de remuneração por conjunto, e não por
procedimento isolado. A Tabela de Procedimentos do SUS descreve o código [código], na
competência [MM/AAAA], assim:

> [transcrição literal da descrição da ficha]

| procedimento | código | condição no conjunto |
|---|---|---|
| [cada procedimento da composição] | [código] | [obrigatório \| opcional, com a fonte da condição] |

O conjunto é executado inteiro, sem supressão, substituição ou simplificação de
procedimento obrigatório.

| exame: O objeto é a realização de **[N] exames** e a entrega do respectivo laudo,
distribuídos nos procedimentos da Tabela de Procedimentos do SUS:

| código | procedimento | exames |
|---|---|---|
| [código com dígito] | [nome da tabela] | [quantidade] |
| | **total** | **[N]** |}

### 2.3 Unidade de aferição

> Lições: LI-005

{OCI: **A unidade de aferição é a OCI concluída**, e não o procedimento realizado. A
OCI se conclui com a execução dos procedimentos obrigatórios do conjunto, [[assistencial:
o que marca o fim do percurso — retorno, laudo, entrega]]. A APAC abre no primeiro
procedimento e encerra no último, dentro do prazo que o atributo da ficha fixa
[[a validade da APAC, em competências, está na ficha]].

| exame: **A unidade de aferição é o exame laudado e entregue.** O exame se considera
executado quando o laudo é entregue ao usuário ou encaminhado à unidade que o
solicitou. A aferição é por exame, e não por usuário: cada solicitação da fila é uma
unidade.}

### 2.4 Público-alvo

> Lições: LI-006, LI-010

Usuários do Sistema Único de Saúde no Distrito Federal, [sexo da ficha], [faixa etária
da ficha], com solicitação de [procedimento] pendente na fila de regulação da SES-DF.

O acesso é integralmente regulado: os usuários são convocados na ordem da fila do
sistema de regulação, sem captação, seleção ou triagem pelo executor.

### 2.5 Local de execução

> Lições: LI-024, LI-025, LI-039, LI-040 · OB-053, OB-054

A execução ocorre em **[n] polos**, situados de modo que as sete Regiões de Saúde tenham
polo de referência:

| polo | Regiões de Saúde atendidas | CNES | serviço/classificação |
|---|---|---|---|
| [polo] | [regiões] | [número] | [o que a ficha pede] |

Os polos são serviços licenciados e em funcionamento, cadastrados no CNES com o serviço
que os procedimentos do objeto exigem. [Se o estabelecimento executor não for o próprio
proponente: o vínculo formal entre os dois, e o que cada um executa.]

O usuário é encaminhado ao polo de referência do seu domicílio.

## 3. Justificativa e dimensionamento

### 3.1 A fila

> Lições: LI-009 · comum, regra 11: a fila medida é a justificativa, e a seção para aí

A fila de regulação da SES-DF registra, em [data da extração], **[número]
solicitações** de [procedimento], com espera média de [dias], segundo [fonte e data da
consulta]. [Tabela por procedimento, se mais de um.]

**O convênio resolve [a totalidade | x%] dessas solicitações.**

### 3.2 A etapa no percurso assistencial

[[assistencial: um parágrafo — que doença ou condição, que percurso, e por que esta
etapa é a que trava a decisão clínica. Sem literatura, sem série epidemiológica.]]

### 3.3 Modalidade

> Lições: LI-002, LI-026, LI-040

A execução se dá por convênio, e o pagamento observa os valores unitários pactuados
neste plano, contra produção executada e comprovada.

{OCI: O valor unitário é o valor de tabela federal vigente do código [código] na
competência [MM/AAAA], na forma da subseção 9.1.
| exame: Os valores unitários têm como referência o valor de tabela e o incremento que a
[portaria] fixa para cada procedimento, na forma da subseção 9.1.}

### 3.4 Distribuição entre os polos

> Lições: LI-010

A participação de cada polo corresponde à participação das Regiões de Saúde que ele
atende no conjunto das solicitações.

| polo | Regiões de Saúde | participação | quantitativo |
|---|---|---|---|
| [polo] | [regiões] | [x,xx%] | [n] |
| **total** | | **100%** | **[N]** |

As solicitações originadas em unidades sem vínculo territorial seguem para o polo de
referência do domicílio do usuário.

### 3.5 Economicidade

> Lições: LI-002, LI-017, LI-038

O valor unitário é a referência federal da subseção 3.3, aplicada sem acréscimo. O
parâmetro é público e verificável, e é o mesmo que a União adota para o mesmo
procedimento.

Os demais valores da planilha resultam de pesquisa de mercado registrada na memória de
cálculo, na forma da subseção 9.2.

## 4. Proponente

> Lições: LI-024, LI-035, LI-036

[preencher: apresentação narrativa — natureza jurídica, tempo de atuação, serviços em
operação com os respectivos CNES, habilitações sanitárias e do programa, e experiência
na especialidade do objeto, com números próprios e verificáveis. Sem texto de outro
projeto e sem lista de pré-condições.]

## 5. Metodologia e detalhamento das ações

### 5.1 Origem da demanda

A solicitação chega pela fila de regulação da SES-DF, com a classificação de risco
atribuída pela unidade solicitante. O convênio não capta demanda própria e não recebe
solicitação que não tenha passado pela regulação.

### 5.2 a 5.9 O percurso do usuário

> Lições: LI-005, LI-014, LI-015, LI-016 · procedimento, fase 2: o fluxo é de onde a planilha é puxada

Uma subseção por passo, com título nominal ("Agendamento e orientação de preparo",
"Recepção e identificação", "Realização do exame", "Laudo", "Retorno"…). Cada passo diz:
**o que acontece, quem faz (com o CBO da ficha), quanto tempo leva, onde, e o que se
registra**. Os passos administrativos têm texto-base; os clínicos são do Anexo A.

**Agendamento e orientação de preparo.** O usuário é contatado a partir da fila, recebe
data, horário, polo e a orientação de preparo por escrito. [[assistencial: o preparo
exigido, e com quanta antecedência]]

**Confirmação.** A presença é confirmada nominalmente na véspera, com repetição da
orientação de preparo. A vaga não confirmada é oferecida ao usuário seguinte da mesma
fila.

**Recepção e identificação.** O usuário é identificado pelo CPF na recepção, antes do
procedimento, com conferência do preparo.

[[assistencial: os passos clínicos da composição, um por subseção — o que se faz, quem
faz, tempo por usuário, sala e equipamento]]

**Busca ativa e reagendamento.** O usuário que falta é contatado e reagendado; a
segunda falta devolve a solicitação à regulação, com registro do motivo.
[[assistencial: absenteísmo esperado, que entra no dimensionamento da subseção 6.3]]

### 5.10 Equipe de gestão e apoio

> Lições: LI-017, LI-018, LI-019, LI-023, LI-038 · OB-051, OB-054

| postos | cargo | atuação | passos que executa |
|---|---|---|---|
| [n] | [cargo — nome e preço procurados em `biblioteca/precos/cargos_no_acervo.md`] | [meses] | [subseções] |

A equipe assistencial — [[assistencial: profissionais da execução, com o CBO da ficha]]
— integra a capacidade instalada do proponente e é remunerada pelo valor unitário.

{se o estabelecimento for habilitado em 38.01: O Núcleo de Gestão do Cuidado,
[composição], acompanha o tempo e a qualidade da execução e a transição do usuário para
a atenção primária.}

### 5.11 Registro da produção

> Lições: LI-032 · OB-010

O registro é feito no polo, no mesmo dia da execução, pelo posto responsável. Cada
{OCI: OCI é registrada em Autorização de Procedimento Ambulatorial, com o procedimento
principal e os secundários efetivamente realizados | exame: exame é registrado pelo
instrumento que a ficha do procedimento admite}, com o usuário identificado pelo CPF.

Os registros rejeitados são criticados, têm a causa apurada e são reapresentados.
Registro rejeitado é produção executada e não comprovada, e a apuração da causa evita
que o erro se repita no lote seguinte.

### 5.12 Execução direta do objeto

> Lições: LI-024, LI-025 · OB-050

**A execução assistencial não é subcontratada**: ocorre nos polos do próprio
proponente, por equipe própria. As funções de gestão, coordenação e direção são
exercidas diretamente pelo proponente. [Atividade acessória contratada — como a
assessoria de prestação de contas — é relacionada aqui, pelo nome.]

A responsabilidade pela execução permanece integralmente do proponente, inclusive
quanto ao registro da produção e à prestação de contas.

### 5.13 Metas

> Lições: LI-007, LI-008, LI-012 · estrutura.md: toda meta tem dotação, e meta e indicador se pactuam em 100%

| meta | descrição | quantitativo | prazo |
|---|---|---|---|
| **Meta 1** | **Estruturação e coordenação da execução.** No mês 1: designação da equipe e do responsável técnico de cada polo, acessos aos sistemas oficiais da SES-DF, pactuação do fluxo com o Complexo Regulador, conferência da capacidade instalada contra a subseção 6.3 e publicação das agendas | [n] polos em operação a partir do mês 1 | meses 1 a [v] |
| **Meta 2** | **Execução assistencial.** {OCI: OCI concluídas na forma da subseção 2.3 \| exame: exames realizados e com laudo entregue} — uma meta por grupo de procedimentos, se houver mais de um | **[N]** | meses [p] a [v] |
| **Meta 3** | **Monitoramento, conclusão e prestação de contas.** Apuração mensal dos indicadores, relatórios mensais de execução, consolidação da produção e relatório final | [v] relatórios mensais e 1 relatório final | meses 1 a [v] |

A meta de execução se decompõe por polo, na proporção da subseção 3.4, e por período,
na curva da subseção 6.2 — e as parcelas somam o quantitativo exatamente, com o
arredondamento acomodado na última.

**Meta qualitativa:** {OCI: concluir, dentro do prazo da APAC, 100% das OCI iniciadas
| exame: entregar o laudo em 100% dos exames realizados}.

### 5.14 Indicadores e meios de verificação

> Lições: LI-011, LI-013

| id | indicador | fórmula | parâmetro | meio de verificação | meta |
|---|---|---|---|---|---|
| I-01 | Execução física | unidades concluídas ÷ unidades pactuadas no período | 100% | registros apresentados nos sistemas oficiais | 2 |
| I-02 | Conclusão | {OCI: OCI concluídas no prazo da APAC ÷ OCI iniciadas \| exame: laudos entregues ÷ exames realizados} | 100% | registro oficial da produção e de entrega | 2 |
| I-03 | Registro da produção | unidades registradas na competência ÷ unidades executadas | 100% | autorizações apresentadas | 1 e 3 |
| I-04 | Relatórios de execução | relatórios entregues ÷ relatórios devidos | 100% | protocolo na concedente | 3 |

A fonte primária dos indicadores de execução é o registro oficial da produção, não
instrumento criado para o convênio.

### 5.15 Proteção dos dados dos usuários

O tratamento de dados pessoais e de saúde se restringe ao agendamento, à execução, à
entrega do resultado, ao registro da produção e à prestação de contas. Contato com o
usuário e encaminhamento de resultado se fazem por meio corporativo, com registro de
acesso e sem aplicativo pessoal. Os perfis de acesso aos sistemas são atribuídos por
posto de trabalho.

## 6. Cronograma físico

> Lições: LI-031

### 6.1 Etapas

| etapa | conteúdo | entrega verificável | meses |
|---|---|---|---|
| **Etapa 1 — Implantação** | equipe, acessos aos sistemas, fluxo com o Complexo Regulador, conferência da capacidade, agendas publicadas | ato de designação, acessos, agendas | 1 |
| **Etapa 2 — Produção** | agendamento, execução, resultado, registro | registros apresentados e relatório mensal | [p] a [v] |
| **Etapa 3 — Conclusão e encerramento** | conclusão das unidades iniciadas, apuração final, relatório final e prestação de contas | relatório final | [v] e o prazo do instrumento |

### 6.2 Curva de produção

A produção começa no mês [p] e se reparte pelos períodos da vigência. Cada procedimento
tem a mesma parcela por período, e o resto da divisão se acomoda nos últimos.

| período | meses | quantitativo |
|---|---|---|
| [1º] | [meses] | [n] |
| **total** | | **[N]** |

### 6.3 Capacidade requerida no regime pleno

> Lições: LI-014, LI-015, LI-016 · verificação G

A produção do período de maior carga corresponde a **[n] unidades por dia útil**,
distribuídas entre os polos na proporção da subseção 3.4. Os quantitativos diários e
os equipamentos de cada polo são números inteiros, arredondados para cima.

| recurso | total | [polo 1] | [polo 2] | [polo 3] |
|---|---|---|---|---|
| Unidades por dia útil | | | | |
| Horário de funcionamento | | [[assistencial: horas de operação por dia]] | | |
| Salas / equipamentos | | [[assistencial: tempo de sala ou de equipamento por usuário]] | | |
| Profissionais por turno | | [[assistencial: equipe mínima por sala, com CBO]] | | |

[[assistencial: a folga que o arredondamento produz, e o que ela absorve — falta,
procedimento que se estende, manutenção]]

## 7. Cronograma de desembolso

> Lições: LI-012, LI-029, LI-030, LI-041 · OB-015, OB-042, OB-043

### 7.1 Regime

O desembolso é feito em **[n] parcelas**, correspondentes aos períodos de produção. A
primeira é liberada logo após a assinatura, porque a equipe de planejamento, gestão e
prestação de contas é contratada antes do início da produção; as demais, no início do
período a que se referem, em consonância com as metas e a prestação de contas parcial.

### 7.2 Parcelas

| parcela | meses | unidades do período | produção assistencial | planejamento, gestão e prestação de contas | **valor da parcela** |
|---|---|---|---|---|---|
| 1 | [meses] | [n] | [valor] | [valor] | **[valor]** |
| | | **[N]** | **[total]** | **[total]** | **[o global do termo, ao centavo]** |

### 7.3 Ajuste por execução

A produção executada em cada período é apurada pelos registros apresentados nos sistemas
oficiais, aos valores unitários da seção 9, e a diferença em relação à prevista é
ajustada na parcela subsequente. O saldo não executado ao final da vigência é devolvido.

## 8. Riscos

> Lições: LI-034, LI-041

### 8.1 Critério

Cada risco é classificado pela combinação de probabilidade e impacto sobre a execução, e
recebe medida de mitigação com responsável. Materializado o risco, a resposta segue esta
ordem: redistribuição da agenda entre os polos; ampliação do turno no polo afetado,
dentro da capacidade instalada; ações compensatórias no período seguinte; ajuste da
parcela subsequente; devolução do saldo ao final da vigência.

### 8.2 Matriz

Os riscos que valem para qualquer objeto — cada um com probabilidade, impacto e medida:

| id | risco | medida |
|---|---|---|
| R-01 | capacidade instalada insuficiente para o ritmo da subseção 6.3 | conferência no mês 1, antes das agendas; turno ampliado e redistribuição |
| R-02 | absenteísmo na data agendada | confirmação nominal, busca ativa, reaproveitamento da vaga com a mesma fila |
| R-03 | interrupção do envio da demanda regulada | ritmo de encaminhamento pactuado com o Complexo Regulador no mês 1; monitoramento pelo I-01 |
| R-04 | rejeição de registro nos sistemas oficiais | registro no mesmo dia, CPF conferido na recepção, crítica e reapresentação na competência seguinte |
| R-05 | alteração da tabela ou do incremento durante a vigência | produção apurada pelos valores vigentes na competência; recomposição do quantitativo por termo aditivo |
| R-06 | pactuação interfederativa pendente | produção suspensa até a liberação e curva recomposta no período remanescente |
| R-07 | atraso da parcela seguinte | prestação parcial pronta no 3º mês; cronograma físico que não depende de a parcela chegar no dia |
| R-08 | leitura da rubrica de gestão como taxa de administração | rubrica composta posto a posto, sem percentual sobre o global |
| R-09 | acesso indevido a dado pessoal e de saúde | meio corporativo, perfis por posto |
| R-10 | indisponibilidade de profissional ou de equipamento em um polo | [[assistencial: retaguarda — profissional substituto, laudo à distância, redistribuição]] |

[[assistencial: os riscos clínicos do procedimento — intercorrência, contraindicação,
preparo não cumprido, resultado não entregue — com medida]]

### 8.3 Os riscos altos

Um parágrafo por risco classificado alto: por que é alto neste objeto e o que a medida
controla. O risco que define o objeto vem primeiro.

## 9. Planilha e memória de cálculo

> Lições: LI-017, LI-018, LI-019, LI-020, LI-021, LI-022, LI-038 · OB-049, OB-051 · verificações A, B, C, W, X

### 9.1 Composição do valor unitário

{OCI: A produção assistencial é remunerada pelo valor de tabela federal vigente: o
código [código] vale R$ [valor] na competência [MM/AAAA], praticado sem acréscimo, sem
índice e sem recomposição.
| exame: O valor unitário de cada exame é o valor do Serviço Ambulatorial da tabela
acrescido do incremento que a [portaria] fixa para o procedimento:

| código | valor de tabela | incremento | valor unitário |
|---|---|---|---|
| [código] | R$ [valor] | [x%] | R$ [valor, com o centavo truncado] |}

### 9.2 Metodologia de composição de custos

Cada linha da planilha corresponde a um passo do percurso da seção 5, indicado na coluna
**referência**. Os valores de recursos humanos são o custo total mensal do posto, com
remuneração, benefícios e encargos incluídos. Os preços de locação, serviços e materiais
resultam de pesquisa de mercado registrada na memória de cálculo. [[preço: a referência
de cada linha]]

### 9.3 Delimitação das rubricas

O valor unitário remunera:

- a equipe assistencial em todas as suas funções;
- [[assistencial: salas, equipamentos, insumos, exames complementares e impressos que o
  procedimento consome]];
- o imóvel, a energia, a água, a limpeza e a vigilância dos polos.

A planilha remunera, fora do valor unitário, o planejamento, a gestão, o agendamento, o
registro da produção e a prestação de contas — o que nenhum procedimento da tabela
paga.

### 9.4 Memória de cálculo

**Postos.** Quantos por polo e quantos únicos, e por quê, na forma da subseção 5.10.
**Períodos.** Quantos meses cada posto atua, e por quê — a produção, a conclusão e a
prestação de contas têm prazos diferentes.

### 9.5 Planilha

| # | item | referência | un. | qtd | frequência | v. unitário | v. total |
|---|---|---|---|---|---|---|---|
| | **Meta 1 — Planejamento, estruturação e gestão da execução** | | | | | | |
| | *Etapa 1.1 — Recursos humanos* | | | | | | |
| 1.1.1 | [posto] | [5.x] | posto | [n] | [m] meses | [[preço]] | [total] |
| | **subtotal da Etapa 1.1** | | | | | | **[valor]** |
| | **TOTAL DA META 1** | | | | | | **[valor]** |
| | **Meta 2 — Execução assistencial** | | | | | | |
| 2.1.1 | {OCI: OCI [código] — [nome da tabela] \| exame: [código] — [nome da tabela]} | 2.2 | [un.] | [N] | 1 | [valor unitário] | [total] |
| | **TOTAL DA META 2** | | | | | | **[valor]** |
| | **Meta 3 — Monitoramento, conclusão e prestação de contas** | | | | | | |
| | **VALOR GLOBAL** | | | | | | **[o do termo, ao centavo]** |

---

## Anexo A — perguntas para a área assistencial

Cada resposta vem com fonte — norma, protocolo, diretriz de sociedade ou medição do
serviço — e vai para `dados/parametros_tecnicos.md` antes de entrar no texto. Resposta
sem fonte vira lacuna com dono, não número (comum, regras 1 e 2).

| # | pergunta | onde entra | lições |
|---|---|---|---|
| AS-01 | Qual é o percurso do usuário, passo a passo, da chegada à conclusão? | 5.2 a 5.9 | LI-004, LI-005 |
| AS-02 | O que conclui a unidade: o retorno, o laudo, a entrega? | 2.3, 5.13 | LI-005 |
| AS-03 | Quanto tempo cada passo ocupa de sala, de equipamento e de profissional, com a composição inteira? | 5.x, 6.3 | LI-014 |
| AS-04 | Quantos usuários por hora e por turno cada sala ou equipamento comporta? | 6.3 | LI-015 |
| AS-05 | Que equipe mínima cada sala exige, com que CBO? | 5.10, 6.3, 9.3 | LI-039 |
| AS-06 | Que preparo o procedimento exige, e com que antecedência se orienta? | 5.2 | — |
| AS-07 | Que proporção dos usuários segue para a etapa seguinte (biópsia, repetição, retorno presencial)? | 5.x, 6.3, 9.3 | LI-014 |
| AS-08 | Qual o absenteísmo esperado para este procedimento, nesta fila? | 5.9, 6.3 | LI-016 |
| AS-09 | Que salas, equipamentos, insumos e exames complementares o valor unitário tem de cobrir? | 9.3 | LI-017, LI-018 |
| AS-10 | Quais os riscos clínicos e a medida de cada um? | 8.2 | LI-034 |
| AS-11 | Que parágrafo situa o objeto: que condição, que percurso, por que esta etapa trava? | 3.2 | — |

## Anexo B — perguntas para a SES-DF

| # | pergunta | por quê | lições |
|---|---|---|---|
| SES-01 | No convênio de emenda, o valor com incremento depende de o executor ter a habilitação 38.01 marcada no CNES, ou é só referência de preço? | o incremento é da habilitação, e nenhum executor dos aprovados a tem | LI-040 · OB-053 |
| SES-02 | Qual o teto de apoio aceito para este procedimento, dada a remuneração? | o peso do apoio varia com o quanto o procedimento paga | LI-038 |
| SES-03 | Há registro do Conselho de Saúde e da coerência com o PDS e a PAS para esta emenda? | o MPCDF apontou a falta nos convênios do IEV | LI-033 |
| SES-04 | A nota técnica de regulação da especialidade está vigente? | a NT 11/2025 de oftalmologia foi retirada do portal | NM-038 |
| SES-05 | Que documento instrui a prestação parcial do 3º mês? | as segundas parcelas do IEV não saíram | LI-012, LI-041 |

## Anexo C — os erros e acertos que este modelo já absorve

`metodo/criterios.md` traz todas as lições com a evidência de cada uma. As que o
modelo já resolve no texto-base — e que por isso só se perdem se o texto for mexido:

- valor global, vigência e início copiados do termo, o mesmo valor em todo o documento
  (LI-029); primeira parcela logo após a assinatura (LI-030);
- a OCI executada inteira, sem triagem (LI-004); o acesso só pela regulação (LI-010);
- a gestão posto a posto, sem taxa de administração (LI-019); nenhuma comunicação fora
  da educativa (LI-020);
- metas com dotação e em 100%, indicadores com fórmula e fonte oficial (LI-011, LI-013);
- o registro da produção no mesmo dia e a reapresentação do rejeitado (LI-032);
- a execução direta, com a atividade acessória nomeada (LI-025);
- o atraso de parcela como risco com medida (LI-041).
