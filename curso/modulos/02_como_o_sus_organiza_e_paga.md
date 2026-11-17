# Módulo 2 — Como o SUS organiza e paga

**Interno.** Este módulo conta discussão e erro nosso. Nada daqui vai a documento.

Antes deste módulo: o módulo 1. Lá está por que a entidade pode atender pelo SUS. Aqui
está como o SUS descreve, mede e paga o que ela faz: a tabela, o código, o pacote, o
registro, a fila e o cadastro.

**No cofre.** As notas deste módulo, com as definições e os links ([[Início]]):

- Conceitos: [[APAC]] · [[BPA]] · [[CBO]] · [[CNES]] · [[Competência]] · [[Código SIGTAP]] · [[FAEC]] · [[Ficha do SIGTAP]] · [[Habilitação 38.01]] · [[Incremento de habilitação]] · [[MAC]] · [[Níveis de atenção]] · [[OCI]] · [[PAP]] · [[Programa Agora Tem Especialistas]] · [[Regulação]] · [[SIA]] · [[SIGTAP]] · [[SISREG]] · [[SUS]] · [[Tabela SUS Candanga]] · [[Valor unitário]]
- Normas: [[Lei 15.233-2025]] · [[Portaria GM-MS 3.492-2024]] · [[Portaria GM-MS 7.266-2025]] · [[Portaria SAES-MS 1.640-2024]] · [[Portaria SAES-MS 4.282-2026]] · [[Portaria SAES-MS 4.795-2026]]
- Órgãos: [[Complexo Regulador]]
- Casos: [[Caso - a emenda não paga por FAEC]] · [[Caso - o código e o valor copiados]] · [[Caso - o e que virou ou]]

---

## Para que serve

Ao fim do módulo, a pessoa consegue:

- ler um código da tabela do SUS e dizer o que cada parte dele significa;
- abrir a ficha de um procedimento e achar o valor, quem pode executar e como se registra;
- explicar o que é uma OCI e por que ela muda a conta e o objeto;
- dizer por que a emenda usa o programa federal como base e não é paga por ele;
- explicar o caminho de um pedido, da unidade básica até o atendimento;
- saber qual tabela dá o valor, e por que conferir de novo antes de enviar.

## A lógica

**1. A rede tem degraus, e o nosso é o do meio.** A porta de entrada é a atenção
primária, a unidade básica. Quando ela não resolve, pede uma consulta com especialista
ou um exame: é a atenção especializada, de média complexidade. Acima está o hospital. Os
nossos objetos são quase sempre consultas e exames especializados feitos em ambulatório.
É onde a fila se forma, porque o pedido sai fácil e a oferta é curta.

**2. O dinheiro federal desce por caminhos com nome.** O da média e alta complexidade
(MAC) é um limite por ente, repassado fundo a fundo. O FAEC paga à parte, por produção,
ações que o Ministério quer estimular. A atenção primária tem o piso dela. A emenda
parlamentar dos nossos convênios entra como **incremento temporário de MAC**: um reforço
de custeio, por tempo certo, que não aumenta para sempre o repasse.

**3. Tudo o que o SUS faz tem um código numa tabela.** É o SIGTAP. Cada procedimento tem
uma ficha com o nome exato, o valor, a idade e o sexo de quem pode receber, a ocupação
de quem pode executar, o que o estabelecimento precisa ter e como se registra. O código
se lê assim:

| parte | no código 09.04.01.003-1 | o que é |
|---|---|---|
| grupo | 09 | o grande tipo: 02 são exames, 03 são procedimentos clínicos, 09 são as OCI |
| subgrupo | 04 | a área: aqui, otorrinolaringologia |
| forma de organização | 01 | a subdivisão do subgrupo |
| procedimento | 003 | o número dele |
| dígito | 1 | o verificador. Errado o dígito, é outro código, ou nenhum |

**4. A tabela muda por portaria, a cada poucos meses.** Valor, composição e exigência
mudam. Por isso a ficha tem competência (o mês de referência), e o valor que vale é o da
competência vigente na data do protocolo. Compilação de terceiros serve para achar o
procedimento, nunca para fixar o valor.

**5. A OCI é um pacote.** A Oferta de Cuidado Integrado junta, num código só, a consulta
com o especialista, os exames e o retorno de uma investigação. Paga-se um valor pelo
conjunto, e só quando o conjunto se completa. Ela nasceu de um programa federal de 2024
(hoje, Agora Tem Especialistas) para atacar a fila de um jeito diferente: em vez de
pagar exame por exame, paga-se o paciente resolvido. O catálogo do projeto, em outubro de
2026, tinha 55 códigos, três deles revogados, em nove áreas: os 49 da competência 09/2026
e seis de nefrologia que a vigia achou no Diário Oficial para 10/2026, ainda não
conferidos no SIGTAP. Os valores iam de R$ 100,00 a R$ 3.000,63. Consequências para o plano:
- o objeto se descreve pelo conjunto, executado inteiro, sem triagem nem execução parcial;
- a quantidade é de pacotes concluídos, não de exames;
- a fila da OCI não existe pronta: está espalhada nas filas dos exames que a compõem
  (módulo 6).

**6. O programa é a base; quem paga é a emenda.** O programa das OCI é pago pelo FAEC.
Quando o recurso é de emenda, não há pagamento por FAEC. Do programa aproveitam-se o
código, a composição, a regra de conclusão e o valor. A habilitação, o teto e o
financiamento do programa descrevem o programa: não viram exigência para o proponente.
É o primeiro caso abaixo, e é o erro em que mais se recai.

**7. A produção se registra, e é o registro que comprova.** O atendimento vai ao sistema
de informação ambulatorial (SIA) por um de dois instrumentos: a APAC, uma autorização
individual que acompanha o paciente, ou o BPA, um boletim de produção. A ficha diz qual.
A OCI vai por APAC, com o código do pacote como principal e os procedimentos dele como
secundários, de valor zerado. No convênio de emenda, a APAC não dispara pagamento
federal: ela é a prova de que o pacote foi feito. E há um cuidado que é da SES, não do
executor: a mesma produção não pode ser apresentada duas vezes, ao convênio e ao FAEC.

**8. Ninguém entra direto: tudo passa pela regulação.** O médico da unidade faz o
pedido, que entra no SISREG. A regulação confere, classifica a prioridade e marca a
vaga, na rede própria ou num prestador. Pedido incompleto é devolvido à unidade. O que
espera é a fila. Para o convênio, isso quer dizer que a entidade oferece agenda, e quem
preenche a agenda é o Complexo Regulador. A entidade não chama paciente por conta
própria.

**9. O estabelecimento tem cadastro, e a ficha confere com ele.** Todo lugar que atende
tem um número no CNES, com o tipo, os serviços, os profissionais e os equipamentos. A
ficha do procedimento diz o que esse cadastro precisa mostrar. Alguns exames têm um
acréscimo sobre o valor da tabela, o **incremento**, que não é do exame: é da
habilitação do estabelecimento num programa. Um ultrassom de R$ 24,20 vale R$ 99,94 com
o incremento de 313%.

**10. No DF há uma terceira tabela.** A Tabela SUS Candanga, criada por lei distrital em
2026, fixa valores maiores para parte dos códigos. A regra de hoje: se o código está no
anexo dela, vale o valor do anexo, qualquer que seja a origem do recurso; se o SIGTAP
vigente for igual ou maior, vale o SIGTAP; fora do anexo, o SIGTAP, com o incremento
quando houver. O módulo 7 trata disso por inteiro.

## Pode e não pode

| pode | não pode | por quê | onde está escrito |
|---|---|---|---|
| usar do programa federal o código, a composição e o valor | exigir do proponente a habilitação, o teto ou o financiamento do programa | a emenda não paga por FAEC | `biblioteca/instrumento/convenio_ses_df.md`, "O financiamento" |
| tratar a APAC como comprovação do atendimento | tratá-la como o que dispara o pagamento | quem paga é o convênio, pelo procedimento realizado | idem; LI-032 |
| escrever o código com o dígito e o nome exato da ficha | abreviar o nome, ou copiar o código de outro plano | três dos cinco planos aprovados erraram, e o controle usou o erro | LI-001 |
| tirar o valor da ficha da competência vigente, e reconferir perto do envio | usar o valor da portaria que criou o procedimento | a tabela muda por portaria | LI-003; `metodo/comum.md`, regra 2 |
| descrever a OCI como conjunto executado inteiro | descrever como triagem, avaliação simplificada ou execução parcial | é cláusula do termo, igual em todos os convênios | LI-004 |
| declarar a idade e o sexo que a ficha diz | herdar a faixa etária de outro plano | um plano aprovado copiou a faixa do molde, e o controle atacou | LI-006 |
| dizer como a produção vai ao SIA e como se evita pagar duas vezes | calar sobre o registro | nenhum plano aprovado trata disso, e é por onde se glosa | LI-032 |
| usar o valor com incremento, dizendo de onde ele vem | supor que o executor tem a habilitação | o incremento é da habilitação, e nenhum executor estudado a tinha | LI-040 |
| oferecer agenda à regulação | chamar paciente por fora do SISREG | o serviço complementar se submete às regras do SUS | LI-010 |

## O caso

### Caso 1 — a emenda não paga por FAEC

**O que se fez.** No primeiro plano, em agosto de 2026, o raciocínio foi direto: o
objeto é uma OCI; a OCI é do programa federal; o programa é pago pelo FAEC; logo a
produção seria paga pelo FAEC, com ressarcimento. O plano inteiro foi escrito assim.

**A correção.** Em 20/08/2026, quem conduz o projeto disse: "Quando o recurso vem de
emenda, não tem o pagamento por FAEC, apesar de utilizar o programa agora tem
especialista, que é um programa do FAEC. Ele só é utilizado como base."

**O que mudou.** Nove seções foram reescritas. A habilitação e o plano de ação regional
deixaram de ser condição para "faturar" e passaram a ser assunto de registro. O teto do
programa deixou de limitar o objeto.

**E voltou.** A premissa de que a execução era pelo programa voltou ao raciocínio três
vezes até setembro. Volta porque a ficha do SIGTAP diz "Financiamento: FAEC", e quem lê
a ficha conclui de novo. Por isso as fichas guardadas no projeto trazem, ao lado, "só
referência: a emenda não paga por FAEC".

**O que o caso ensina.** O que a ficha descreve é o procedimento dentro do programa
federal. A origem do dinheiro vem antes, e muda o que da ficha é regra e o que é só
referência. Sempre que aparecer "habilitação", "teto" ou "FAEC" num raciocínio, pergunte
de onde vem o dinheiro deste plano.

*Fontes: `biblioteca/instrumento/convenio_ses_df.md`, "O financiamento";
`metodo/coleta/ficha_sigtap.md`, "O que a ficha não decide". Conversa de 20/08/2026.*

### Caso 2 — o código e o valor copiados

**O que os planos aprovados mostram.** Três dos cinco planos estudados erram código ou
nome de procedimento: um dígito verificador trocado, uma OCI chamada por um nome que
não é o dela, um código sem dígito. Um deles citou R$ 435,00, tirados da portaria que
criou a OCI, para um pacote que valia R$ 840,00 havia mais de um ano.

**O que aconteceu depois.** O Ministério Público de Contas, ao representar contra os
convênios, repetiu o código errado, e o usou como prova de que dois convênios pagavam a
mesma coisa.

**Do nosso lado.** Uma OCI de câncer gástrico passou de R$ 250,00 a R$ 600,11 numa
portaria de agosto de 2026. A diferença foi tratada primeiro como "prêmio", por
dedução, antes de alguém procurar a portaria posterior.

**O que o caso ensina.** Código e valor não se copiam, nem de plano aprovado. Tiram-se
da ficha, na competência vigente. E número que não bate com a tabela que se tem pede,
antes de qualquer explicação, a portaria mais nova.

*Fontes: LI-001; LI-003; `metodo/comum.md`, regra 2.*

### Caso 3 — o "e" que virou "ou"

A OCI de nasofaringe exigia "videolaringoscopia **e** laringoscopia". Em setembro de
2026 passou a "videolaringoscopia **ou** laringoscopia", e o valor foi de R$ 200,00 a
R$ 393,55. Uma palavra mudou o que se executa e o que se compra de equipamento.

E a página de histórico do SIGTAP não conta tudo: ela lista a portaria, sem dizer o que
mudou, e não mostra mudança de composição. A portaria que tornou obrigatórios os exames
das OCI, em janeiro de 2025, não aparece nela. O que mudou só se vê comparando a ficha
de uma competência com a da outra.

**O que o caso ensina.** A ficha se lê inteira e na data: descrição, composição,
atributos e histórico. A leitura é do agente `ficha-sigtap`, que grava a ficha na pasta
do plano com tudo isso.

*Fontes: `planos/redacao_05/dados/fontes/sigtap_0904010031_092026.md`;
`metodo/coleta/ficha_sigtap.md`, "O que se lê".*

## Leia na fonte

Na ordem:

1. `biblioteca/instrumento/convenio_ses_df.md`, "O financiamento".
2. `metodo/coleta/ficha_sigtap.md`: "O que se lê" e "O que a ficha não decide". O
   começo do arquivo é como o agente acessa o sistema, e fica para o módulo 12.
3. Uma ficha de verdade: `planos/redacao_05/dados/fontes/sigtap_0904010031_092026.md`.
4. O catálogo das OCI: `registros/fontes/sigtap_grupo09_092026.csv`.
5. `biblioteca/instrumento/enquadramento_cnes.md`, seções 1 e 2.
6. As normas do programa, só o título e a ementa, com o `consultar.py`: NM-014 (cria o
   programa), NM-047 e NM-072 (Agora Tem Especialistas), NM-017 (como o programa opera).
7. As lições LI-001, LI-003, LI-004, LI-006, LI-032 e LI-040.

## Faça

Leia e responda; não altere arquivo nenhum.

1. **O código.** Decomponha 09.04.01.002-3 nas cinco partes. De que área é?
2. **O catálogo.** Abra `registros/fontes/sigtap_grupo09_092026.csv`. Quantos códigos
   há, quantos estão revogados, quantas áreas (subgrupos)? Qual a OCI mais cara e
   quanto ela vale? Quantas valem R$ 100,00?
3. **A ficha.** Na ficha da 09.04.01.003-1, ache: o instrumento de registro, a
   quantidade máxima, o que a linha de financiamento diz, e o que significa a regra
   condicionada 0009.
4. **A composição.** Na mesma ficha: o que compõe o pacote, e quanto valeria cada
   componente se fosse cobrado avulso? Some a consulta (duas) e o exame mais caro.
   Compare com o valor do pacote. O que isso diz sobre a intenção do programa?
5. **O incremento.** Em `enquadramento_cnes.md`: quanto vale o ultrassom de tabela, e
   quanto com o incremento? Refaça a conta. O resultado bate centavo a centavo? O que
   se fez com a terceira casa?
6. **De quem é o incremento.** Ainda ali: o incremento é do exame ou de quê? Que
   pergunta ficou em aberto para a SES?
7. **O registro.** Abra a LI-032. O que o plano precisa dizer sobre o registro, e por
   que isso importa mesmo sem pagamento por FAEC?
8. **Qual tabela.** Pela LI-002: um exame está no anexo da Tabela SUS Candanga e a
   emenda é federal. Que valor se usa? E se o código não está no anexo? Onde o anexo
   está guardado?
9. **De onde vem o dinheiro.** Alguém escreve no plano: "a entidade deverá estar
   habilitada no programa para faturar as OCI". Corrija a frase e diga por quê.

## Confira

| # | pergunta | o que conta como resposta certa |
|---|---|---|
| 1 | As cinco partes | Grupo 09 (OCI), subgrupo 04 (otorrinolaringologia), forma de organização 01, procedimento 002, dígito 3 |
| 2 | O catálogo | 55 códigos, 3 revogados, 9 áreas. A mais cara é a 09.09.01.006-4, de nefrologia, a R$ 3.000,63: uma das seis que a coluna `situacao` diz "vigente desde 10/2026", vindas do Diário Oficial e ainda não conferidas na ficha. Antes delas, o catálogo de 09/2026 tinha 49 códigos e 8 áreas (DD-003). Três valem R$ 100,00 |
| 3 | A ficha | APAC, como procedimento principal. Quantidade máxima 1. A linha diz FAEC, "só referência: a emenda não paga por FAEC". A regra 0009 zera o valor dos secundários: eles se registram, e quem carrega o valor é o pacote |
| 4 | A composição | Consulta especializada (até duas, R$ 10,00 cada) e videolaringoscopia (R$ 45,50) ou laringoscopia (R$ 47,14). Avulso, daria R$ 67,14 no máximo; o pacote paga R$ 393,55. O programa paga muito acima do avulso para que o percurso se complete |
| 5 | O incremento | R$ 24,20 de tabela, R$ 99,94 com 313%. A conta dá 99,946, e o arquivo dá 99,94: o centavo é truncado, não arredondado. É a regra que o modelo do plano pede (`metodo/plano/modelo.md`, "o centavo truncado") e que o plano de imagem escreve |
| 6 | De quem é | Da habilitação do estabelecimento (38.01, 38.05 ou 38.06), não do exame. Ficou em aberto se, no convênio de emenda, o incremento depende de o executor ter a habilitação marcada ou se é só referência de preço |
| 7 | O registro | Como a produção vai ao SIA pelo instrumento da ficha, que só a produção aprovada conta, e como se evita pagamento em duplicidade entre FAEC e convênio. Importa porque a SES registra a produção, e a mesma produção não pode ser apresentada duas vezes |
| 8 | Qual tabela | O valor do anexo da Candanga, mesmo com emenda federal; se o SIGTAP vigente for igual ou maior, o SIGTAP. Fora do anexo: o SIGTAP vigente, com o incremento quando houver, e o plano diz que o código não está na Candanga. O anexo está em `biblioteca/precos/tabela_sus_candanga/` |
| 9 | A frase | Sai a exigência. O recurso é de emenda, que não paga por FAEC: a habilitação descreve o programa federal e não é condição do proponente. O plano diz como a produção se registra, não o que é preciso para "faturar" |

E quatro perguntas para responder de cabeça:

- O que é uma OCI, e por que a fila dela não aparece pronta em lugar nenhum?
- A ficha diz "Financiamento: FAEC". O que isso quer dizer para um plano pago por emenda?
- Quem escolhe o paciente que ocupa cada vaga, e o que a entidade oferece?
- Por que se confere a ficha de novo perto do envio, se ela já foi lida no começo?
