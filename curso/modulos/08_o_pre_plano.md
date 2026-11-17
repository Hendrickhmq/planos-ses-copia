# Módulo 8 — O pré-plano

**Interno.** Este módulo conta discussão e erro nosso. Nada daqui vai a documento.

Antes deste módulo: os módulos 5, 6 e 7. O método está em `metodo/pre_plano/`, e o modelo
pronto é `planos/redacao_05/plano_v1_geral.md`, na versão que a SUCONV ajustou.

**No cofre.** As notas deste módulo, com as definições e os links ([[Início]]):

- Conceitos: [[Enquadramento jurídico]] · [[Pré-plano]] · [[TrakCare]]
- Órgãos: [[SUCONV]]
- Casos: [[Caso - da versão da equipe à versão da SUCONV]] · [[Caso - zerar a fila]]
- Planos: [[redacao_05 - OCI de otorrino]] · [[redacao_07 - pré-plano de imagem da bancada]] · [[redacao_10 - colonoscopia]]

---

## Para que serve

Ao fim do módulo, a pessoa consegue:

- reconhecer um pedido de pré-plano e dizer por que ele não é um plano curto;
- preencher os nove campos do formulário da SES, e só eles;
- decidir entre uma versão geral e uma de item único;
- montar uma carteira com reserva;
- tratar o retorno da SUCONV sem estragar o que ela escreveu;
- rodar a conferência do pré-plano e saber o que ela não pega.

## A lógica

**1. O pré-plano serve para a SES decidir se e como fazer.** A ARINS o pede por ofício,
para "análise inicial". Depois dele, a SUCONV define o instrumento e pede o plano de
trabalho detalhado. O "com quem" e o "quanto custa cada coisa" ficam para o plano. Quem
define a trilha é a finalidade do documento, não o nome do formulário.

**2. Todo número escrito vira compromisso.** O plano detalhado vai ser conferido contra
o pré-plano enviado: o objeto, os códigos, o valor total e as metas não podem
contradizê-lo. Por isso o mínimo de números fechados e o máximo de espaço para pactuar
depois. É a regra 6 do `metodo/comum.md` no grau mais forte.

**3. O formulário manda.** Entram os nove campos do modelo da SES, na ordem dele, e só o
que eles pedem. Nada de seção a mais.

Um aviso sobre o valor: o `formulario.md` e o modelo do otorrino são de outubro de 2026,
de antes de a Tabela SUS Candanga virar o preço (01/11/2026, módulo 7). Onde eles dizem
"valor SIGTAP vigente", vale hoje o valor da regra do módulo 7. No modelo, a OCI
09.04.01.001-5 aparece a R$ 100,00 (SIGTAP); hoje ela valeria R$ 127,80 (Candanga).

**4. Só o custo assistencial.** A aplicação das despesas mostra o que os procedimentos
custam. A gestão e o apoio entram numa frase: completam o Valor Total e serão
detalhados no plano de trabalho. Foi a SUCONV quem cortou a linha do apoio, na primeira
versão que ela ajustou.

**5. O raciocínio interno não vai para o papel.** Nem o percentual do apoio, nem quanto
se paga ao prestador, nem o motivo financeiro de escolher uma fila. A justificativa é a
fila medida, com a espera.

**6. Geral ou item único.** A versão geral fala de uma carteira ("OCIs em
Otorrinolaringologia"), com a meta em valor e a quantidade de cada item pactuada com a
SES. A de item único fala de um procedimento só e pode dizer a quantidade e até "atende
a totalidade da fila", se a conta mostrar. A geral compromete menos.

**7. A carteira pode ter reserva.** Como o plano detalhado não pode usar código que não
estava no pré-plano, um código que talvez seja preciso entra na carteira, com valor, e só
recebe recurso depois dos outros. Se uma fila esvaziar, há para onde ir sem pedir
alteração à SES.

**8. O que é da SUCONV é da SUCONV.** O enquadramento do instrumento e as normas
aplicáveis são ato dela. O texto que ela escreve entra literal, sem acertar nem a
pontuação. Erro factual se corrige e se avisa.

## Pode e não pode

| pode | não pode | por quê | onde está escrito |
|---|---|---|---|
| preencher os nove campos, na ordem | acrescentar seção, ou deixar "[a preencher]" | o formulário manda | `metodo/pre_plano/formulario.md` |
| dar a meta em valor, com a quantidade pactuada com a SES | fixar quantidade por item na versão geral | todo número vira compromisso | idem |
| dizer que o recurso "corresponde a mais da metade da fila" | dizer "zerar a fila" na versão geral, se a conta não fecha | a promessa seria conferida depois | `metodo/pre_plano/procedimento.md`, regra 2 |
| pôr só o custo assistencial na aplicação das despesas | pôr a linha, o valor ou o percentual do apoio | ajuste da SUCONV; o apoio é do plano detalhado | idem, regra 3; verificação PA |
| deixar o local como "identificado na formalização, com endereço e CNES" | pôr quadro de equipe, capacidade, salas, produção por mês, desembolso mensal | é do plano detalhado | `metodo/pre_plano/formulario.md`, "O que não entra"; verificação PB |
| manter literal o texto da SUCONV no campo do MROSC | reescrevê-lo, ou citar artigos do MROSC | é ato dela | `metodo/pre_plano/procedimento.md`, regra 5 |
| deixar um código de reserva na carteira | tirar da carteira o que talvez seja preciso depois | o plano detalhado não pode usar código novo | conversa de 19/10/2026 |
| medir a fila pelo agente, com varredura | medir a fila à mão | a varredura acha filas que a mão não acha | `metodo/coleta/mapa_social.md` |

## O caso

### Caso 1 — da versão da equipe à versão da SUCONV

**O que havia.** Em 08/10/2026, a equipe tinha um pré-plano de otorrino com doze itens,
só da OCI de nasofaringe: identificação com processo, ação orçamentária e autoria; quadro
de equipe com postos e salários; capacidade, salas e "350 OCIs por mês"; desembolso
mensal de R$ 137.742,50; responsabilidades e condições de formalização. Versões
anteriores ainda tinham "[a preencher]" e "não há dados para quantificar a fila" (é a
última linha da tabela "O que não entra" do `formulario.md`). A versão guardada em
`versoes/` já é a de doze itens, sem esses campos.

**O que se fez.** Refeito no formulário da ARINS, com os nove campos. Quem conduz o
projeto cortou o resto: "Não precisa detalhar o quadro agora"; "O ideal para o pré-plano
é fazer de uma maneira mais geral, sem se comprometer tanto." Os "[a preencher]" viraram
dado com fonte ou "na formalização".

**O que a SUCONV fez.** A versão devolvida veio com ajustes feitos por alguém da SUCONV:
tirou a linha do apoio da aplicação das despesas ("deixa só o custo assistencial") e
escreveu ela mesma o campo do enquadramento.

**Os dois erros na hora de tratar o retorno.** O assistente achou que os ajustes eram de
quem conduz o projeto e (a) reescreveu o campo do enquadramento num tom mais formal,
com artigos do decreto e da lei do MROSC; (b) manteve "reenviadas" onde a SUCONV tinha
escrito outra coisa. A correção: "Quem faz o enquadramento do instrumento jurídico são
eles, não a gente." O texto dela voltou literal.

**E uma consequência.** Sem a linha do apoio, a frase que dizia a sobra do recurso não
fechava mais: a diferença visível seria outra. Saiu também. Quando um ajuste tira uma
linha, sai o que dependia dela.

**O que o caso ensina.** O pré-plano é curto de propósito, e o que a SES escreve não se
melhora. O retorno se trata fazendo o diff contra a versão enviada.

*Fontes: `planos/redacao_05/versoes/` (a versão da equipe e a devolvida, lado a lado);
`metodo/pre_plano/formulario.md`, "O que não entra"; `metodo/pre_plano/procedimento.md`,
"O retorno com ajuste da SUCONV". Conversa de 08/10/2026.*

### Caso 2 — zerar a fila

**O que se queria.** O apoio foi fixado em 8,2% (R$ 123.600) "para ter como justificativa
que vamos zerar a fila": assim o recurso comprava 3.504 OCI de nasofaringe para 3.477
pessoas.

**A pergunta certa.** Quem conduz o projeto perguntou: "de forma geral não podemos falar
em zerar fila, correto?" Correto. Na versão geral, as três filas somavam cerca de 9.500
pessoas, e o recurso cobria pouco mais da metade delas, pelo valor. "Zerar" só valia se
tudo fosse para a nasofaringe.

**O que passou a valer.** Duas versões: a geral, com a meta em valor e a frase "o
recurso da proposta corresponde a mais da metade da fila"; e a de item único, só a
nasofaringe, com a meta de 3.504 OCI. A estratégia de zerar uma fila e passar à próxima
ficou como decisão interna.

*Fontes: `planos/redacao_05/plano_v1_geral.md`, seções 3 e 6;
`planos/redacao_05/plano_v2_nasofaringe.md`. Conversa de 08/10/2026.*

### Caso 3 — a reserva

No pré-plano de exames de imagem, de outubro de 2026, a carteira tinha doze exames.
Zerar as doze filas custaria R$ 2,38 milhões; havia R$ 1,35 milhão para exames. A
mamografia e a densitometria tinham espera curta, e a rede da SES dava conta delas no
momento. Ficaram como reserva: com código e valor no pré-plano, recebendo recurso só
depois das outras dez. Quem conduz o projeto: "pode deixar as duas de reserva, mas deixe
isso tudo anotado nas justificativas". No documento, entrou só a frase de que a
programação prioriza as filas de maior espera; o raciocínio ficou no estado do plano.

*Fonte: conversa de 19/10/2026.*

### Caso 4 — a linha que voltou

Num pré-plano de colonoscopia, em novembro de 2026, quem conduz o projeto decidiu pôr na
aplicação das despesas a linha do apoio, com valor. A bateria do pré-plano caiu de 13/13
para 11/13, e o assistente lembrou que foi exatamente essa linha que a SUCONV tirou no
otorrino. A decisão foi mantida, registrada nas pendências, com o recuo previsto se a
SUCONV pedir de novo.

**O que o caso ensina.** A conferência avisa, e a decisão é de quem conduz. Quando a
decisão contraria o padrão, ela se registra, com o motivo e o que fazer se der errado.

*Fonte: conversa de 12/11/2026.*

## Leia na fonte

Na ordem:

1. `metodo/LEIA.md`, a tabela das duas trilhas.
2. `metodo/pre_plano/procedimento.md`, inteiro.
3. `metodo/pre_plano/formulario.md`, inteiro.
4. `metodo/pre_plano/conferencia.md`, inteiro.
5. O modelo: `planos/redacao_05/plano_v1_geral.md`, e depois a versão de item único,
   `planos/redacao_05/plano_v2_nasofaringe.md`.
6. A versão da equipe que foi cortada: `planos/redacao_05/versoes/pre_plano_estrutura_equipe_20261008.md`.
7. As pendências do projeto: `planos/redacao_05/pendencias.md`.

## Faça

Leia e responda; não altere arquivo nenhum.

1. **Que documento é.** Pelo `metodo/pre_plano/procedimento.md`: o que o Ofício 387/2026
   pede, e para quê? O que vem depois dele?
2. **Os nove campos.** Liste os nove campos do formulário, na ordem, e o que entra em
   cada um, numa linha.
3. **O que saiu.** Compare a versão da equipe (em `versoes/`) com o `plano_v1_geral.md`.
   Atenção: a da equipe era só da nasofaringe, e a v1 é a geral, das três OCI; parte da
   diferença é de objeto. Ache três coisas que estavam na da equipe e saíram, e diga para
   onde foi cada uma, pela tabela "O que não entra".
4. **O texto literal.** No `plano_v1_geral.md`, copie a resposta do campo "O Instituto
   enquadra-se como OSC, nos termos do MROSC?". Por que ela não se corrige, mesmo
   parecendo informal?
5. **A meta em valor.** Na seção 6 do `plano_v1_geral.md`: qual é a Meta 2? Por que em
   valor e não em quantidade? Ache a frase que diz como a quantidade se decide.
6. **A aplicação das despesas.** Na seção 8: quanto aparece, e o que diz a frase sobre a
   gestão? Pelo "Ponto de atenção" do procedimento: o que ainda dá para descobrir pela
   subtração, e o que se faz se a SES pedir para não deixar visível?
7. **Geral ou item único.** Compare a seção 6 das duas versões. O que a de item único
   promete que a geral não promete?
8. **A conferência.** Pela `metodo/pre_plano/conferencia.md`: o que as verificações PA,
   PB e PE conferem? O que a bateria não confere de jeito nenhum?
9. **Escreva.** Para um pré-plano de colonoscopia com R$ 10 milhões, escreva o campo
   "Metas e indicadores" em três linhas, no estilo do modelo, sem quantidade fechada.

## Confira

| # | pergunta | o que conta como resposta certa |
|---|---|---|
| 1 | Que documento é | O "Plano de Trabalho Simplificado", para análise inicial: a SES decidir se e como fazer. Depois, a SUCONV define o instrumento e pede o plano de trabalho detalhado e o que faltar |
| 2 | Os nove campos | Informações iniciais; objeto; justificativa; metodologia; objetivos; metas e indicadores; cronograma; aplicação das despesas; interface com os sistemas. O conteúdo de cada um está na tabela do `formulario.md` |
| 3 | O que saiu | Por exemplo: o quadro de equipe e salários (plano detalhado); capacidade, salas e produção por mês (plano detalhado); o desembolso mensal (instrumento); as responsabilidades de formalização (a SUCONV indica); o quadro com processo, ação orçamentária e autoria (o quadro do formulário substitui) |
| 4 | O texto literal | "Sim. O ISHP se enquadra como OSC mas não será utilizado esse normativo por se tratar de um convênio. Decreto N.º 48.727, de 09 de junho de 2026". Não se corrige porque é ato da SUCONV: o enquadramento é dela, e mexer no texto é escrever no lugar dela |
| 5 | A meta em valor | Execução das OCI da carteira, concluídas e registradas: R$ 1.378.999,20 em OCI, com as quantidades pactuadas com a SES. Em valor para não fixar quantidade por item, que viraria compromisso. A frase: "A quantidade de cada OCI é pactuada com a SES/DF conforme a demanda regulada, com prioridade às filas de maior espera, preservado o valor da Meta 2." |
| 6 | A aplicação | R$ 1.378.999,20, só a execução das OCI. A frase diz que a gestão e o apoio completam o Valor Total e serão detalhados no plano de trabalho. A subtração do Valor Total revela o apoio; se a SES pedir, o Valor Total passa a ser o recurso inteiro |
| 7 | Geral ou item único | A de item único fixa a quantidade (3.504 OCI) e pode dizer que alcança a fila inteira daquela OCI. A geral só dá o valor e diz "mais da metade da fila" |
| 8 | A conferência | PA: só custo assistencial na aplicação, sem linha de apoio nem percentual. PB: nada do plano detalhado (equipe, curva mensal, capacidade, desembolso). PE: o Valor Total não passa do recurso, a aplicação não passa do Valor Total, e a meta em valor é igual à aplicação. Não confere o texto literal da SUCONV: isso se faz à mão, pelo diff |
| 9 | Escreva | Algo como: Meta 1, implantação no mês 1; Meta 2, execução das OCI concluídas e registradas, em valor, com a quantidade pactuada com a SES pela demanda regulada; Meta 3, relatórios mensais e prestação de contas. Indicadores em 100% |

E três perguntas para responder de cabeça:

- Por que o pré-plano tem tão poucos números, se a conta já foi feita inteira?
- O que acontece no plano detalhado com um código que não estava no pré-plano?
- A SUCONV devolveu o pré-plano com um texto seu num campo. O que você faz com ele?
