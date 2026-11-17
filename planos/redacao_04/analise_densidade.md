# O que faltava, medido contra o plano 3

Feito em 15/09/2026, depois de salva a v1. O usuário apontou metodologia, metas,
indicadores e riscos como rasos. **Estava certo, e a medida mostra onde.**

## O tamanho, seção a seção

| seção | v1 | v2 | plano 3 |
|---|---|---|---|
| 1. Identificação | 24 | 24 | 35 |
| 2. Objeto | 62 | 74 | 78 |
| 3. Justificativa e dimensionamento | 75 | 75 | 92 |
| 4. Proponente | 6 | 6 | 14 |
| **5. Metodologia** | **86** | **171** | **263** |
| 6. Cronograma físico | 40 | 70 | 49 |
| 7. Cronograma de desembolso | 36 | 36 | 36 |
| **8. Riscos** | **18** | **66** | **53** |
| 9. Planilha e memória de cálculo | 90 | 97 | 92 |
| **total** | **437** | **619** | **712** |

---

## Seção 5 — o que entrou

A v1 tinha treze subseções, das quais dez eram uma frase cada. O plano 3 tem quinze,
e a diferença não é de comprimento: é que **cada passo dele diz o que se faz, com que
parâmetro e por quem**.

### As subseções novas

| # | subseção | por que existia no plano 3 e faltava aqui |
|---|---|---|
| **5.10** | **Equipe de gestão e apoio** | existia, mas sem dizer que passo cada posto executa nem onde está a equipe assistencial |
| **5.11** | **Registro da produção** | era uma frase. Agora diz onde, quando, por quem, com que identificador e o que se faz com o rejeitado |
| **5.12** | **Execução direta do objeto** | não existia. É o que afasta a leitura de subcontratação |
| **5.15** | **Proteção dos dados dos usuários** | não existia. Confirmação, busca ativa e envio de laudo transmitem dado de saúde |

### O que os passos ganharam

**O preparo virou tabela por procedimento.** A v1 dizia "jejum, bexiga, acesso venoso
e triagem de contraste" numa linha. Os doze procedimentos têm preparos diferentes, e
é o preparo que decide se o exame acontece na data marcada — por isso virou quadro na
5.2, repetido na confirmação em 5.3 e conferido na recepção pelo R-03.

**A triagem de contraste ganhou subseção própria.** São 12.726 dos 13.452 exames de
tomografia. A v1 mencionava; agora a 5.5 diz o que se avalia, o que se faz com quem
tem contraindicação, e que o polo mantém os meios de atendimento a reação adversa.

**A capacidade saiu do agregado.** A v1 dizia "dez salas e dois tomógrafos". A
derivação por polo mostra **treze salas e três tomógrafos** — porque não há fração de
sala, e o arredondamento para cima em três polos custa três salas e um tomógrafo a
mais que a conta agregada.

A derivação ficou na **subseção 6.3**, e não numa subseção própria da metodologia: por
decisão do usuário em 15/09/2026, a 5.10 que a continha foi retirada. Capacidade é
matéria do cronograma físico, e ter a mesma tabela em duas seções publicava dois
lugares para o mesmo número.

### As metas — de três a seis

A v1 tinha três metas, na estrutura do `PADRAO.md`: planejamento, execução,
encerramento. A v2 tem **seis**, e cada uma tem dotação própria na planilha.

| meta | quantitativo | dotação |
|---|---|---|
| 1 — Estruturação e coordenação | 3 polos em operação | R$ 126.000,00 |
| 2 — Gestão da fila | 81.546 solicitações agendadas e confirmadas | R$ 230.400,00 |
| 3 — Registro da produção | 81.546 exames registrados | R$ 309.600,00 |
| 4 — Execução em ultrassonografia | 68.094 exames | R$ 6.811.909,80 |
| 5 — Execução em tomografia | 13.452 exames | R$ 4.031.492,94 |
| 6 — Monitoramento e prestação de contas | 12 relatórios mensais e 1 final | R$ 179.460,00 |

**A lógica veio do acervo.** O `analise_aprovados.md` registra que nos cinco planos
aprovados o custo de apoio não aparece como apoio: aparece como meta, "com etapa,
cronograma e aferição próprios". Separar agendamento e registro em metas distintas é
aplicar isso até o fim — cada função de apoio vira entrega contratada e aferível, em
vez de overhead.

As Metas 4 e 5 se decompõem **por polo** (33.073 · 24.196 · 24.277), **por
procedimento** e **por mês**.

A **meta qualitativa** continua sendo a entrega do laudo, que é onde a obrigação
termina.

### Os indicadores

Ganharam **id**, **meio de verificação** e a **meta que cada um afere**. Os seis se
pactuam em 100%.

**Passaram de três a seis na terceira rodada**, por pedido do usuário. Eu havia
argumentado que três bastavam — realizar, entregar, registrar — e estava olhando só a
execução assistencial. Com seis metas, cada uma precisa de aferição própria.

**O I-02 é o achado da rodada.** Execução por procedimento, e não só no agregado: os
doze procedimentos valem entre R$ 99,94 e R$ 300,10, e a contagem global de exames
sozinha não distingue um conjunto do outro. Sem ele, a meta física se cumpre com a
composição errada.

Os que não entraram, e por quê: **aproveitamento de vaga** e **distribuição entre
polos** medem gestão interna, e o `PADRAO.md` os exclui; **percentual da fila
agendado** seria régua contra o proponente, porque o ritmo de envio é da regulação.

---

## Seção 8 — de 6 riscos a 15

A v1 tinha seis riscos numa tabela sem classificação. Agora são quinze, com
probabilidade, impacto, classificação e mitigação — e a seção passou o plano 3 em
tamanho.

### O que a v1 não via

| id | risco que faltava | por que importa |
|---|---|---|
| R-03 | **Preparo não cumprido** | probabilidade alta e efeito imediato: jejum, repleção vesical ou creatinina ausente impedem o exame no dia |
| R-05 | Reação adversa ao meio de contraste | 12.726 exames com contraste iodado |
| R-06 | Contraindicação identificada na triagem | o exame não se perde: faz-se sem contraste ou devolve-se à regulação |
| R-09 | Indisponibilidade de médico radiologista | e a mitigação é própria da imagem: o laudo não exige presença no polo |
| **R-10** | **Laudo realizado e não entregue** | **é o risco próprio deste objeto e de nenhum outro** |
| R-12 | Indisponibilidade do sistema de registro | produção executada e não comprovada |
| R-13 | Concentração da produção em um polo | desequilíbrio contra o rateio da 3.5 |
| R-15 | Vazamento de dado pessoal e de saúde | confirmação, busca ativa e envio de laudo transmitem dado clínico |

### O critério, que não existia

A v1 tinha duas frases. Agora há **ordem de resposta** quando o risco se materializa —
redistribuição entre polos, ampliação de turno, compensação no período seguinte,
ajuste da parcela, devolução do saldo. É a mesma escada do plano 3, com o degrau de
turno acrescentado, porque aqui a capacidade é de sala e não de agenda clínica.

### A 8.3, que não existia

O plano 3 dedica prosa aos riscos altos. A v1 não tinha nada. Agora cinco riscos altos
ganham parágrafo: R-01 capacidade, R-02 absenteísmo, R-04 contraste, R-10 entrega do
laudo e R-14 alteração da tabela.

**R-10 é o achado da rodada.** Exame realizado cujo laudo não chega à unidade
solicitante não cumpre a obrigação do convênio, ainda que a produção esteja registrada
e o pagamento seja devido. Nenhum plano do acervo tem esse risco, porque nenhum deles
tem esse objeto.

---

## O que continua mais magro que o plano 3, e por quê

| seção | diferença | é defeito? |
|---|---|---|
| 1. Identificação | 24 contra 35 | **não** — a diferença são os campos cadastrais em `[preencher]` |
| 3. Justificativa | 75 contra 92 | **não** — o plano 3 descreve o percurso clínico do câncer gástrico; aqui a fila é a justificativa, e a seção 6 do `PADRAO.md` manda parar aí |
| 4. Proponente | 6 contra 14 | **não** — está em `[preencher]` |
| 5. Metodologia | 171 contra 263 | **em parte** — o plano 3 gasta setenta linhas em sedação, recuperação pós-sedação e anatomia patológica, que este objeto não tem. O que resta de diferença é a densidade clínica de cada passo, e ela depende do protocolo do proponente |

---

## O que ainda falta, e depende de você

1. **Os campos cadastrais** — oito lacunas na seção 1, mais a narrativa da seção 4.
2. **O protocolo de preparo do proponente** — a tabela da 5.2 traz o preparo usual de
   cada procedimento. Se o serviço pratica outro, é o dele que vale.
3. **Prazo de entrega do laudo.** O documento não fixa nenhum, de propósito: prazo que
   norma nenhuma exige vira obrigação aferível na prestação de contas. Se a SES-DF
   pactuar um, ele entra; se não, o rastreamento diário do R-10 é o controle.
