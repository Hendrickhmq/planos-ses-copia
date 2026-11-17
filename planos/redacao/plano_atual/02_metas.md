# Seção 2 — Metas

Status: `rascunho` · Nível: **mínimo viável** (melhorias em `redacao/melhorias.md`)
Depende de: Seção 1 · Lacunas: 4 (nenhuma bloqueante)
Vigência: 10 meses · Ciclo da OCI: 30 dias (teto)
Entradas: 2ª metade do mês 1 até o mês 9 · Conclusões: mês 2 até o mês 10

---

## Redação proposta — quadro de metas

| # | meta | unidade de medida | quantidade | prazo próprio |
|---|---|---|---|---|
| **1** | Realizar Ofertas de Cuidado Integrado — OCI 09.02.01.002-6, Avaliação Cardiológica — **concluídas**, para usuários do SUS/DF referenciados pelo Complexo Regulador | **OCI concluída** | **35.000** | meses 2 a 10 |
| 1.1 | Polo 1 — eixo Sudoeste/Oeste | OCI concluída | 11.667 | idem |
| 1.2 | Polo 2 — eixo Sudoeste/Oeste | OCI concluída | 11.667 | idem |
| 1.3 | Polo 3 — Sobradinho, referência Norte/Leste | OCI concluída | 11.666 | idem |
| **2** | Colocar os 3 polos em condição de operar: equipe contratada, agendas abertas no SISREG, acessos aos sistemas oficiais habilitados e FPO programada | **polo em operação** | **3** | 2 primeiras semanas do mês 1 |

**Divisão entre polos: média aritmética.** 35.000 ÷ 3 = 11.666,67 — arredondado
para 11.667, 11.667 e 11.666, que somam exatamente 35.000. É divisão provisória e
declarada como tal: não pondera capacidade instalada de cada ambiente, população
da região nem volume de fila. A chave por demanda do pt_ses_01 (AC-021) e o
critério por capacidade ficam para revisão quando LC-003 chegar — registrado em
`melhorias.md` como M-15.

**Definição de meta cumprida (Meta 1).** Uma OCI conta para a meta quando duas
coisas acontecem, nesta ordem:

1. **Assistencial** — o usuário completa o fluxo do pacote: consulta
   especializada, exames integrantes e **consulta ou teleconsulta de retorno**.
2. **Documental** — **todos os formulários são carregados nos sistemas oficiais
   de registro**. Sem o registro completo, a OCI está clinicamente concluída e
   administrativamente inexistente: não é aferível, não é conciliável e não é
   paga.

A unidade **não** é "atendimento realizado". E a conclusão tem, portanto, dois
prazos: o do retorno e o do registro. A defasagem entre eles é o que faz a última
competência da vigência física fechar depois do mês 9 — é a vigência financeira
da DV-012, e é onde a Seção 8 tem que amarrar prazo de carga.

**Não existe meia OCI.** O pacote incompleto não gera receita nenhuma: não há
pagamento proporcional por consulta realizada, exame feito ou procedimento
secundário isolado. Quem entra e não conclui produz custo sem contrapartida
financeira. Isso tem três efeitos, todos registrados aqui e cobrados adiante:

1. **Dimensionamento** — a agenda precisa comportar remarcação nos **dois** pontos
   do fluxo, entrada e retorno, porque a perda no retorno custa o pacote inteiro,
   não metade dele.
2. **Operação** — o não comparecimento é tratado com **reagendamento e busca
   ativa do usuário**, a partir dos dados de contato fornecidos pela SES-DF para
   os pacientes regulados. Não é ação opcional: é o que protege a meta.
3. **Risco** — a OCI iniciada e não concluída é risco de execução com impacto
   financeiro direto sobre o executor, e vai nomeada na Seção 11.

**Distribuição entre polos.** É estimativa e referencial, ajustável conforme a
dinâmica das filas no SISREG, **sem alteração do quantitativo global pactuado** e
vedada qualquer mesclagem indevida de filas regionais (método do corpus, AC-021 e
AC-030). A cláusula não é formalidade: é ela que impede a divisão por média
aritmética de virar descumprimento quando a fila real se mostrar desigual entre
as regiões.

---

## Fechamento com a Seção 1

Verificação 1 do `validador.py`, aplicada ao próprio rascunho:

```
1.1 + 1.2 + 1.3  =  35.000  =  quantitativo do objeto (Seção 1)
```

A Meta 2 está em outra unidade — polo em operação — e **não soma** ao
quantitativo do objeto. Existe porque a primeira parcela precisa de lastro físico
verificável, e nenhuma OCI estará concluída quando ela for liberada.

Oferta de agenda **não** aparece como meta. É dimensionamento, e o motivo está
mais abaixo.

---

## Prazo próprio: a curva mensal

A vigência física é de 9 meses, mas a Meta 1 é de OCI **concluída**. Entre a
entrada e o retorno há um ciclo, e é ele que fecha a porta de entrada antes do
fim do convênio:

```
janela de entrada    = 9 meses − implantação (d) − ciclo da OCI (c)
janela de conclusão  = do mês (d + c + 1) ao mês 9
```

**Ciclo de 30 dias — e 30 é teto, não média.** Prazo entre a consulta de entrada
e a consulta ou teleconsulta de retorno com os exames prontos (DV-011,
respondida). Três qualificações que fazem parte do parâmetro e precisam estar
escritas no plano:

1. **É prazo máximo.** O tempo médio e o mínimo são menores e variam com a
   liberação dos resultados: retorno se marca quando o exame fica pronto, não no
   trigésimo dia. O plano dimensiona pelo teto porque cronograma se monta pelo
   pior caso; a operação real roda mais rápido, e essa diferença é folga, não
   ociosidade.
2. **O retorno se agenda na própria consulta de entrada, sempre que possível.**
   O usuário sai da primeira visita com a segunda marcada. Não é conveniência de
   atendimento: é o que garante o recebimento, porque OCI sem retorno não é
   receita nenhuma.
3. **OCI em andamento tem prioridade sobre OCI nova.** Diante de disputa por
   agenda, quem já entrou no pacote passa na frente de quem ainda não entrou.
   Abrir entrada nova sem fechar as que estão em curso troca receita certa por
   receita incompleta.

Os itens 2 e 3 são regras operacionais com efeito financeiro direto, e reaparecem
na Seção 7 como objeto de monitoramento e na Seção 11 como mitigação.

**Pré-produção de 2 semanas, vigência de 10 meses.** Decisão do proponente, e
alinhada ao corpus: os planos 02, 03 e 04 abrem com Etapa de Pré-Produção de
**2 semanas** — estrutura, contratação, acesso ao SISREG e ao TrackCare,
alinhamento de fluxos e planejamento das agendas —, com produção a partir da 3ª
semana (AC-034); e três dos quatro declaram **vigência um mês maior que o período
assistencial** (AC-035). O corpus compra o tempo de partida esticando a vigência,
e é o que este plano passa a fazer.

**Isto altera a decisão anterior de 9 meses.** A Seção 1 foi atualizada. O que se
perde é a comparação direta de intensidade operacional com o pt_ses_01, que
também roda 9; o que se ganha está na tabela:

| desenho | janela de entrada | entradas/mês | consultas/polo/dia útil |
|---|---|---|---|
| 9 meses, mês 1 inteiro de partida (anterior) | 7,0 meses | 5.000 | ~159 |
| **10 meses, 2 semanas de partida (adotado)** | **8,5 meses** | **4.125** | **~131** |

Um mês de vigência e duas semanas de partida em vez de quatro derrubam a carga
diária de cada polo em **18%**, sem mexer em meta, valor ou objeto.

```
janela de entrada    = 2ª metade do mês 1 até o fim do mês 9   (8,5 meses)
janela de conclusão  = 2ª metade do mês 2 até o fim do mês 10  (8,5 meses)
```

O mês 1 opera meia janela. Convenção declarada para fechar a divisão: 2.000
entradas no mês 1 e 4.125 nos meses cheios.

| mês | Meta 2 | entradas | retornos | **OCI concluídas (Meta 1)** | agendamentos |
|---|---|---|---|---|---|
| 1 | pré-produção (2 semanas) | 2.000 | — | — | 2.500 |
| 2 | | 4.125 | 2.000 | **2.000** | 7.656 |
| 3 | | 4.125 | 4.125 | **4.125** | 10.312 |
| 4 | | 4.125 | 4.125 | **4.125** | 10.312 |
| 5 | | 4.125 | 4.125 | **4.125** | 10.312 |
| 6 | | 4.125 | 4.125 | **4.125** | 10.312 |
| 7 | | 4.125 | 4.125 | **4.125** | 10.312 |
| 8 | | 4.125 | 4.125 | **4.125** | 10.312 |
| 9 | | 4.125 | 4.125 | **4.125** | 10.312 |
| 10 | | — | 4.125 | **4.125** | 5.156 |
| **total** | **3 polos** | **35.000** | **35.000** | **35.000** | ~87.500 |

Fechamentos, verificados:

```
entradas    2.000 + (8 × 4.125)  =  35.000
conclusões  2.000 + (8 × 4.125)  =  35.000   = Meta 1
```

### Agendamento não é meta — é dimensionamento

Os números da última coluna são **agendamentos**, não pessoas e não vagas
distintas:

- **O teto de pessoas é a fila: 36.052 CNS.** Não existe atender mais gente do
  que existe gente na fila.
- **Agendamento é evento, não pessoa.** Quem falta e é remarcado consome um
  segundo horário, e um terceiro se faltar de novo. Para 35.000 comparecimentos
  com 20% de falta são precisos 43.750 horários — fator 1,25, cinco horários para
  cada quatro comparecimentos. Como há dois pontos, entrada e retorno, dá ~87.500
  horários para 36.052 pessoas, sem contradição.

Isso **não vira meta**. Meta é o que se entrega ao concedente; oferta de agenda é
como o executor se organiza para entregar — e, como se vê no fluxo abaixo, é a
única ponta da cadeia que ele controla sozinho. Vai para a Seção 9, que dimensiona
capacidade, e para a Seção 7, que monitora.

### Quem faz o quê — e o que isso faz com a meta

O fluxo de uma OCI, ponta a ponta:

```
1. executor  →  libera os horários na agenda
2. SES-DF    →  REGULA: seleciona da fila e agenda o usuário (Complexo Regulador / SISREG)
3. executor  →  atende a consulta de entrada
4. executor  →  realiza os exames do pacote
5. executor  →  realiza a consulta ou teleconsulta de retorno
6. executor  →  carrega os formulários nos sistemas oficiais  →  OCI concluída
```

**A etapa 2 não é do executor.** Ele oferta a vaga; quem a preenche é a regulação
da SES-DF. E o fluxo acima vale para **quem já está na fila**: o executor não
capta, não seleciona e não recruta usuário — toda entrada vem da regulação, o que
é a própria vedação de mesclagem indevida de filas do AC-030 vista pelo lado
operacional. Isso parte a responsabilidade pela meta em duas, e o plano precisa
dizer isso com todas as letras:

- **Do executor:** ofertar horário suficiente, atender, examinar, fazer o
  retorno acontecer e registrar.
- **Da SES-DF:** encaminhar usuários da fila em volume compatível com as vagas
  ofertadas.

Vaga ofertada e não regulada é capacidade instalada ociosa — custo incorrido sem
OCI possível. É por isso que a taxa de preenchimento das vagas ofertadas vira
indicador na Seção 3 e risco na Seção 11, e é a razão pela qual o executor
precisa registrar a oferta mês a mês: é a prova de que a ponta dele foi cumprida.
Falta definir o que acontece com a meta se a regulação não preencher —
`[[lacuna: LC-017]]`, DV-016.

### Busca ativa: obrigação, não esforço

O usuário que não retorna é procurado até retornar — contato reiterado, por todos
os meios disponíveis, com os dados que a SES-DF fornece para os pacientes
regulados. Não é cortesia nem best effort: sem retorno não há OCI, e sem OCI não
há receita. A insistência é o que sustenta a premissa de recuperação do faltoso
que a meta assume.

### O aperto que a conta revela

Com 36.052 pessoas na fila e meta de 35.000 OCI **concluídas**, o plano converte
**97,1% de toda a fila** — cada pessoa comparecendo na entrada e no retorno.
Fecha na aritmética, mas só com a busca ativa acima funcionando até a terceira
tentativa nos dois pontos, e supondo que todo mundo da fila é elegível e
localizável.

Duas coisas aliviam, e nenhuma está medida:

1. **A fila não é estoque parado.** Gente nova pede o exame durante os 10 meses,
   entra na espera e passa a ser regulável como qualquer outro — o executor não
   os capta, eles chegam pela mesma porta. O denominador real é maior que 36.052,
   mas o fluxo mensal de novas solicitações não foi levantado
   — `[[lacuna: LC-016]]`, DV-015.

   **Ressalva que o alívio tem.** Se a regulação encaminha por tempo de espera —
   o mais antigo primeiro —, o usuário que entrou na fila durante a vigência só
   chega ao polo depois de esgotado o estoque de 777 dias de espera. Ou seja: o
   fluxo novo não alivia a meta no começo, alivia no fim, e só se o estoque
   drenar. Faz parte da DV-015 saber a ordem que a regulação usa.
2. **A teleconsulta de retorno** reduz a falta no ponto mais caro (DV-002).

Se a fila for estoque fechado e a recuperação render menos, quem cede é a meta —
que é teto da FPO e rubrica de produção ao mesmo tempo. Vai nomeado na Seção 11.

**Três consequências que as próximas seções herdam:**

1. **Não há OCI concluída no mês 1.** A primeira competência com produção é a do
   mês 2, e ainda assim parcial (2.000). A Seção 6 tem que refletir isso: a
   primeira parcela não tem produção concluída para conciliar.
2. **A carga real do polo é o dobro da meta.** Nos meses 3 a 9 cada polo atende
   ~1.375 entradas **e** ~1.375 retornos — cerca de **131 consultas por dia útil
   por polo**, contra as 65 que só a entrada sugeriria. É esse o número que
   dimensiona equipe e estrutura na Seção 9, e a teleconsulta de retorno é a
   alavanca que o torna viável.
3. **O mês 10 é só conclusão.** Não entra ninguém novo; o mês existe para fechar
   os pacotes abertos no mês 9 e carregar o que falta de registro.

**Apuração mensal, por competência.** A Meta 1 é apurada a cada competência do
SIA/SUS, não só ao fim. É o que permite notificar no meio do caminho e o que dá
lastro à conciliação da Seção 8. Meta apurável só no último mês deixaria a
prestação de contas mensal sem objeto.

**A Meta 2 é o lastro da 1ª parcela.** O recebimento antecipado que dá partida ao
convênio está confirmado pelo proponente e pelo corpus (AC-032). Como nenhuma OCI
estará concluída antes do mês 2, a primeira parcela não pode se vincular à
Meta 1. Vincula-se à Meta 2, cujas entregas são verificáveis por documento:
contrato de equipe, agenda publicada no SISREG e FPO programada. Sem entregas
verificáveis, a pré-produção seria mobilização sem entrega recebendo desembolso — o
defeito que a Seção 4 tem que evitar.

---

## O que a meta não promete

1. **Não promete produção acima de 35.000.** O valor global é travado e a
   alteração do objeto, da finalidade das despesas e do valor global é vedada sem
   termo aditivo (AC-029). A meta pactuada ainda vira o teto de faturamento na
   FPO do executor (AC-028, OB-009). O que acontece com o excedente é **DV-001**,
   aberta.
2. **Não promete distribuição fixa por polo.** A média aritmética é ponto de
   partida, não compromisso por unidade — ver a ressalva do SISREG acima.
3. **Não promete atendimento, promete OCI concluída.** Consulta realizada sem
   retorno não é meta cumprida — é vaga consumida.

---

## Lacunas

| id | descrição | como se resolve |
|---|---|---|
| LC-014 | Taxa de não comparecimento **no retorno**. O mecanismo está definido — reagendamento e busca ativa com dados da SES —, falta o número: hoje se replica no retorno os 20% medidos na entrada (AC-022). | DV-014, parcial |
| LC-016 | Fluxo mensal de **novas solicitações de ecocardiografia** entrando na fila, e a **ordem que a regulação usa** para encaminhar. Define se o denominador é o estoque de 36.052 ou algo maior, e quando o alívio chega. | DV-015 |
| LC-015 | Prazo de programação da FPO. A curva assume que 2 semanas bastam; se a FPO demorar mais, a janela de entrada encolhe. | DV-004 |
| LC-017 | O que acontece com a meta se a regulação da SES-DF não preencher as vagas ofertadas. | DV-016 |

**Fechadas:** LC-013 (curva mensal, com o ciclo de 30 dias) e LC-003 no que
depende desta seção — os volumes por polo saíram por média aritmética. O
refinamento por capacidade e população continua desejável, mas é melhoria
(M-15), não lacuna.

Nenhuma das três é bloqueante: a Meta 1 global, o desdobramento por polo e a
curva mensal estão fixados e reconstroem o objeto. O que resta afeta o parâmetro
de falta no retorno, o tamanho real do denominador e o início da contagem.

---

## Dúvidas abertas nesta seção

- **DV-013** — **respondida.** Não há pagamento parcial: OCI iniciada e não
  concluída não gera receita. Incorporada acima, em "Não existe meia OCI".
- **DV-014** — **respondida em substância, falta o número.** O tratamento do
  faltoso é reagendamento e busca ativa com os dados que a SES-DF fornece. A taxa
  própria do retorno continua sem medição (LC-014).
- **DV-015** — **aberta.** Quantos usuários entram por mês na fila de
  ecocardiografia? Define se a meta consome 97% de um estoque fechado ou uma
  fração menor de um fluxo (LC-016).

Registradas em `redacao/duvidas.md`.

---

## Fundamento

- **OB-007** — Portaria SAES/MS nº 1.822/2024, Anexo: composição, atributos e
  regras condicionadas da OCI 09.02.01.002-6. É o que define o que conta como OCI
  entregue. `status_vigencia: a_verificar` — **Anexo não lido no original**.
- **OB-009** — Manual Operacional da FPO: programação restrita ao pactuado, com o
  quantitativo correspondente. É por isso que a meta é também teto.
  `a_verificar`.
- **OB-010** — registro da produção por APAC no SIA/SUS, com procedimento
  principal e secundários. É o meio pelo qual a meta se comprova. `a_verificar`,
  e ainda **sem dispositivo identificado**.

Nenhuma das três foi lida no original. Citar no plano final só depois de conferir.
