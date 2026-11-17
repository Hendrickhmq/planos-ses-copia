# Módulo 7 — O preço

**Interno.** Este módulo fala de margem, de mercado e do que se diz à clínica. Nada daqui
vai a documento, nem a quem executa.

Antes deste módulo: os módulos 2, 3 e 6. O método inteiro está em
`metodo/coleta/precos.md`, e quem pesquisa é o agente `precos`.

**No cofre.** As notas deste módulo, com as definições e os links ([[Início]]):

- Conceitos: [[Absenteísmo]] · [[Apoio (custo acessório)]] · [[Cobertura]] · [[Custo de executar]] · [[Fila viva]] · [[Incremento de habilitação]] · [[Mercado mínimo]] · [[Oferta inicial e teto]] · [[Subcontratação]] · [[Tabela SUS Candanga]] · [[Taxa de administração]] · [[Valor unitário]]
- Normas: [[Deliberação CG-SES 46-2026]] · [[Lei DF 7.897-2026]] · [[Portaria SAES-MS 4.282-2026]]
- Órgãos: [[Colegiado de Gestão da SES-DF]]
- Casos: [[Caso - a tabela que não era a tabela]] · [[Caso - o apoio multiplicado pelo prazo]] · [[Caso - o fixo mensal da clínica]] · [[Caso - o mercado de outro lugar]]

---

## Para que serve

Ao fim do módulo, a pessoa consegue:

- dizer, de um código, o valor unitário que vale no plano, e de qual tabela;
- calcular a cobertura, a oferta inicial, o teto e a margem de um objeto;
- dimensionar o apoio e saber por que ele é um valor, não um percentual;
- negociar com uma clínica sem entregar a conta;
- dizer o que da conta vai ao documento e o que fica dentro de casa.

## A lógica

**1. São dois preços, e não se misturam.**

| | o que é | quem vê |
|---|---|---|
| **o custo de executar** | quanto custa fazer uma OCI ou um exame, comparado com o que a unidade recebe e com o mercado | só nós |
| **o apoio** | os postos, a locação e os serviços de gestão que vão à planilha | o documento, sem a origem linha a linha |

**2. O valor unitário vem de uma tabela, nunca de negociação.** A regra de hoje:

| situação | valor |
|---|---|
| o código está no Anexo da Tabela SUS Candanga | o valor do Anexo, na modalidade do objeto (exame e OCI de ambulatório: SIA), qualquer que seja a origem do recurso |
| o SIGTAP vigente é igual ou maior que o do Anexo | o SIGTAP |
| o código não está no Anexo | o SIGTAP da ficha vigente, mais o incremento da portaria quando o exame tem, e o plano diz que o código não está na Candanga |

O valor da Candanga já contém o SIGTAP: a diferença é o complemento que o DF paga. O
incremento é truncado na segunda casa, não arredondado. É o primeiro caso abaixo: a
regra mudou em 01/11/2026.

**3. A cobertura diz se o objeto se paga.** Cobertura é o valor que a unidade recebe
dividido pelo menor preço encontrado no DF para fazer o mesmo (o mercado mínimo). Abaixo
de 100%, executar custa mais do que se recebe, e só a negociação por volume fecha a
conta. Numa OCI, a conta soma uma unidade de cada componente da ficha.

**4. A oferta inicial e o teto são decisão, e mudam de plano para plano.** São
percentuais do valor que a unidade recebe: a oferta é o que se propõe à clínica; o teto
é o máximo que se aceita pagar. A margem no teto é o valor menos o teto. Tudo isso é
controle interno. À clínica se diz "o limite do que conseguimos", nunca o percentual.

**5. O apoio nasce do fluxo, posto a posto, e o percentual é resultado.** Recepção,
agendamento, coordenação, prestação de contas, cada um com o passo do atendimento que o
justifica (módulo 9). O nome e o preço de cada posto vêm do acervo
(`biblioteca/precos/cargos_no_acervo.md`); a locação e os serviços, de três orçamentos.
O apoio nunca paga o que o valor unitário já paga.

**6. O tamanho do apoio depende de quanto o procedimento paga.** É o critério que a SES
aplica: o que paga bem leva apoio pequeno; o que paga mal leva mais, com cada linha
justificada. Nos planos aprovados, 36,6% de apoio a R$ 129 de valor médio, cerca de 31%
entre R$ 160 e R$ 360; nos nossos, de valor alto, 8% a 8,5%. E o percentual não se
publica.

**7. O apoio é um valor global, não uma mensalidade.** Se o prazo muda, o apoio não se
multiplica pelos meses: os salários se readequam para caber no mesmo valor. É o caso 2.

**8. Paga-se o que foi feito.** À clínica ou ao médico, paga-se por exame realizado,
laudado e registrado. Um "mínimo mensal garantido" é despesa sem contraprestação, e vira
glosa. Reservar turnos de sala, como locação de horário, tem contraprestação e cabe.
Crédito acumulado de um mês para o outro, não.

**9. A margem não é lucro.** O que sobra entre o que a unidade recebe e o que custa
executá-la cobre o que não tem preço na planilha: responsável técnico, faltas, férias,
retaguarda. O que não for gasto no objeto volta à SES em 30 dias. Taxa de administração
é proibida.

**10. Tempo de sala também é preço.** Um exame que paga R$ 70 e leva metade do tempo de
um que paga R$ 100 rende mais por hora. Valor por hora = preço × 60 ÷ minutos. Isso
entra na escolha da carteira e no jeito de pagar o médico.

## Pode e não pode

| pode | não pode | por quê | onde está escrito |
|---|---|---|---|
| usar o valor da Candanga, ou o SIGTAP quando for maior, citando a fonte | usar valor negociado, ou coluna de estudo que não é a tabela oficial | o valor é o da tabela, sem ajuste | LI-002; `biblioteca/precos/tabela_sus_candanga/README.md` |
| registrar cada preço com fonte, endereço, data e tipo | usar preço sem endereço, de outro estado como se fosse do DF, ou com mais de 180 dias | a base da conta é o DF, e o preço envelhece | `metodo/coleta/precos.md`, "As regras" |
| dizer à clínica "o limite do que conseguimos" | dizer o teto, o percentual, ou quanto a entidade recebe | a negociação acaba no número que se entrega | `metodo/coleta/precos.md` |
| mandar à clínica uma cotação com valor e quantidade | mandar a conta da margem | idem | idem |
| pagar por exame realizado e laudado, com teto de volume | pagar mínimo mensal como "exames garantidos", ou crédito acumulado | despesa sem contraprestação vira glosa | conversa de 11/11/2026 |
| pôr o apoio posto a posto, com preço do acervo e três orçamentos | pôr taxa de administração, ou percentual de gestão | vedação do decreto e do termo | LI-019; LI-021 |
| manter o apoio no mesmo valor global quando o prazo muda | multiplicar o apoio pelo número de meses | o apoio é um valor do convênio, não uma mensalidade | conversa de 07/11/2026 |
| pôr no documento o valor unitário e a planilha de apoio | pôr custo de executar, mercado, margem, oferta, teto ou cobertura | é controle interno | `metodo/coleta/dossie.md`, "A justificativa pública" |
| alugar horário de sala e equipamento, com a equipe da entidade | pagar a clínica para fazer o objeto inteiro com a equipe dela | é subcontratar a execução, vedado | OB-020; OB-021 |

## O caso

### Caso 1 — a tabela que não era a tabela

**O que havia.** Até outubro de 2026 a regra era: emenda federal paga o SIGTAP; emenda
distrital paga a Tabela SUS Candanga. Uma deliberação do DF de 2024 vedava usar recurso
federal acima do SIGTAP.

**O primeiro erro.** De 27 a 31/10/2026, sem o anexo oficial em mãos, os estudos usaram a
coluna "Valor Máximo" de uma análise comparativa que a SES tinha distribuído em agosto,
antes da tabela sair. Parecia a Candanga, e não era. O ultrassom de abdômen total valia
R$ 334,88 nessa coluna e vale R$ 117,51 no anexo oficial.

**Como se descobriu.** Em 01/11/2026 chegou o Anexo Único oficial, com o número do SEI.
Conferido código a código, a coluna da análise não batia.

**A mudança de regra.** No mesmo dia, a Candanga passou a ser o preço também na emenda
federal: a lei distrital manda financiar a tabela com recurso de emenda, distrital ou
federal, e veda remunerar convênio em desconformidade com ela. O plano de ultrassom e
tomografia foi readequado: os mesmos 79.144 exames passaram a valer R$ 245,7 mil a menos
(−2,31%), porque cada exame ganhou o seu preço, alguns acima e outros abaixo do que se
usava.

**O que o caso ensina.** Preço só vale com a norma que o nomeia. Coluna de estudo,
compilação ou planilha de terceiro serve para comparar, nunca para fixar o valor. E a
regra do valor pode mudar no meio de um plano: é decisão que muda premissa e pede
varrer o documento inteiro.

*Fontes: `biblioteca/precos/tabela_sus_candanga/README.md`, "Qual valor usar" e "A
análise comparativa"; LI-002. Conversas de 27/10 e 01/11/2026.*

### Caso 2 — o apoio multiplicado pelo prazo

**O que se fez.** Em 07/11/2026 estudou-se executar o plano em 12 meses em vez de 8, com
o mesmo valor de convênio. A primeira resposta manteve o quadro de apoio e o multiplicou
pelos meses: o apoio iria de R$ 956.160 a R$ 1.434.240 (12,4% do global), R$ 478 mil a
mais, tirados dos exames.

**A correção.** Quem conduz o projeto: "O custo de gestão e apoio deve manter o mesmo
valor global, ou variar pouquíssimo até 8,5%. Os salários vão precisar de readequação."

**O que mudou.** Refeito em cinco cenários. Cortar 31% de todos os salários deixava seis
de oito cargos abaixo do menor preço já aprovado. O cenário escolhido, com menos postos e
preços de planos aprovados, fechou em R$ 978.120 (8,44%).

**O que o caso ensina.** O apoio é um valor do convênio, decidido uma vez. Prazo maior
não traz dinheiro novo: o que muda é como ele se distribui.

*Fontes: LI-038. Conversa de 07/11/2026.*

### Caso 3 — o fixo mensal da clínica

**O que chegou.** Em 08/10/2026, uma clínica propôs R$ 75 mil por mês por 400 tomografias,
com créditos acumuláveis. Para a Região em questão (1.061 tomografias em 8 meses, pelas
quais o convênio receberia R$ 318 mil), isso seria R$ 600 mil: 189% do que entraria.
Cada exame sairia a R$ 565,50, contra R$ 299,69 recebidos.

**O segundo tropeço.** A regra passada à mesa era "no máximo 70%", e foi lida como 70% da
quantidade. Era 70% do valor que o convênio paga por exame.

**O que passou a valer.** Paga-se o exame realizado e laudado, com teto de volume e sem
crédito acumulado. Se for preciso reservar agenda, paga-se o turno reservado, como
locação de horário, que tem contraprestação. E o percentual nunca se diz à clínica.

*Fonte: conversa de 08/10/2026.*

### Caso 4 — o mercado de outro lugar

A primeira pesquisa de mercado guardava, sob "mercado privado no DF", preços de outros
estados. Noutro plano, a cobertura de 105% de um exame vinha de um pacote de São Paulo e
de um "a partir de" nacional, sem nenhuma marca. Daí as regras: todo preço com fonte,
endereço e data; o do DF é a base, o de fora entra à parte; "a partir de" é o mínimo
daquela fonte; componente com um preço só é "preço fraco" e não decide sozinho.

*Fonte: `metodo/coleta/precos.md`, "As regras".*

## Leia na fonte

Na ordem:

1. `metodo/coleta/precos.md`: "O que entra", "As regras" e "O que os preços não
   decidem".
2. `biblioteca/precos/tabela_sus_candanga/README.md`, inteiro.
3. Uma pesquisa de verdade: `planos/redacao_05/dados/precos.md`.
4. `biblioteca/precos/cargos_no_acervo.md`: o começo e uma tabela de cargos.
5. `metodo/plano/procedimento.md`, as travas F-04, F-08 e F-10.
6. As lições LI-002, LI-019, LI-020, LI-021 e LI-038.

## Faça

Leia e responda; não altere arquivo nenhum.

1. **Qual valor.** Ache na Tabela Candanga (`biblioteca/precos/tabela_sus_candanga/tabela_sus_candanga.csv`)
   o valor de: a ultrassonografia de abdômen total (02.05.02.004-6), a tomografia de
   tórax (02.06.02.003-1) e a OCI de nasofaringe (09.04.01.003-1). Para a OCI, que valor
   se usa no plano, e por quê?
2. **A citação.** Escreva a citação do valor da ultrassonografia de abdômen total, no
   formato do README da Candanga.
3. **O incremento.** Suponha um exame fora do Anexo que vale R$ 97,44 no SIGTAP e tem
   incremento de 208%. Quanto ele vale? E se a conta der mais de duas casas decimais, o
   que se faz?
4. **A cobertura.** Em `planos/redacao_05/dados/precos.md`, seção 5 ("A conta"), ache o
   mercado mínimo do DF das três OCI de otorrino e calcule a cobertura de cada uma com o
   valor que o arquivo usa. Qual cobre menos? Depois: o arquivo é de 09/10/2026, antes
   da regra de 01/11. Refaça a cobertura da 09.04.01.001-5 com o valor que vale hoje.
5. **A oferta e o teto.** No cabeçalho do mesmo arquivo: que oferta inicial e que teto
   foram decididos, por quem e quando? Quanto é o teto em reais para a OCI de
   nasofaringe?
6. **O apoio pelo valor.** Pela LI-038: uma OCI de R$ 100 e outra de R$ 700. Qual leva
   apoio proporcionalmente maior, e por quê?
7. **O prazo.** O apoio de um plano de 8 meses é de R$ 960.000. O prazo passa a 12 meses
   e o valor do convênio não muda. Qual o apoio certo, e qual o erro?
8. **A clínica.** Uma clínica pergunta: "quanto vocês recebem por exame, e quanto podem
   pagar?" Escreva a resposta.
9. **O que vai ao documento.** De uma lista: valor unitário da Candanga; cobertura de
   88%; posto de recepcionista a R$ 3.200; teto de 70%; mercado mínimo de R$ 534;
   locação de sala com três orçamentos. Diga o que vai ao plano e o que fica dentro.

## Confira

| # | pergunta | o que conta como resposta certa |
|---|---|---|
| 1 | Qual valor | Abdômen total R$ 117,51; tomografia de tórax R$ 309,25; a OCI de nasofaringe R$ 255,61 no Anexo. Para a OCI vale o SIGTAP vigente, R$ 393,55, porque é maior que o valor do Anexo (a coluna `alerta` marca isso) |
| 2 | A citação | "02.05.02.004-6 Ultrassonografia de abdômen total: R$ 117,51 — Tabela SUS Candanga, Anexo Único da Deliberação CG-SES 46/2026 (SEI 212117347), SIA, p. 5" |
| 3 | O incremento | 97,44 × 3,08 = 300,1152, e vale R$ 300,11: trunca-se na segunda casa, não se arredonda. A portaria fixa o percentual, e ele vale para o estabelecimento com a habilitação; o plano diz de onde ele vem (módulo 2) |
| 4 | A cobertura | Nasofaringe: 393,55 ÷ 395,50 = 99,5%, que o arquivo arredonda para 100%: cobre o par mínimo e nada mais. Progressão do déficit auditivo: 471,57 ÷ 534,00 = 88%. Avaliação inicial: 100 ÷ 261 = 38%, a que cobre menos, longe de se pagar. Hoje, a 001-5 vale R$ 127,80 na Candanga (maior que o SIGTAP de R$ 100,00): 127,80 ÷ 261 = 49%, e continua não se pagando. A 002-3 fica no SIGTAP (R$ 471,57), maior que o Anexo (R$ 191,71) |
| 5 | Oferta e teto | 50% e 50%, decididos por quem conduz o projeto em 08/10/2026 ("o valor que podemos pagar é 50% do valor da sigtap"). 50% de 393,55 = 196,775: o arquivo dá a oferta e o teto em R$ 196,78 e a margem no teto em R$ 196,77 |
| 6 | O apoio pelo valor | A de R$ 100 leva apoio proporcionalmente maior: paga mal, e a folga entre o que paga e o que custa é pequena. A de R$ 700 paga bem e leva apoio pequeno. Nas duas, cada linha se justifica, e o percentual não se publica |
| 7 | O prazo | O apoio continua perto de R$ 960.000, com os salários readequados. O erro é levá-lo a R$ 1.440.000, multiplicando por 12/8, e tirar a diferença dos exames |
| 8 | A clínica | Algo como: "Para este volume, o limite do que conseguimos é R$ X por exame realizado e laudado." Nunca o valor recebido, o percentual nem o teto |
| 9 | O que vai | Vão ao plano o valor unitário da Candanga, o posto de recepcionista e a linha da locação com o valor. Os três orçamentos que sustentam a locação ficam guardados na pasta do plano, como memória. Ficam dentro a cobertura, o teto e o mercado mínimo |

E quatro perguntas para responder de cabeça:

- De onde vem o valor unitário, e quando ele não é o da Candanga?
- Por que a cobertura, e não a margem, decide se um objeto se paga?
- Por que o apoio não se multiplica pelo prazo?
- Por que a sobra entre o que se recebe e o que se paga não é lucro da entidade?
