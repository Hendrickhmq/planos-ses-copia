# Módulo 10 — Conferir e revisar

**Interno.** Este módulo conta erro nosso que passou pela conferência. Nada daqui vai a
documento.

Antes deste módulo: os módulos 8 e 9. O método está em `metodo/plano/conferencia.md`,
`metodo/plano/leitura_de_entrega.md`, `metodo/pre_plano/conferencia.md` e
`metodo/revisao/cega.md`.

**No cofre.** As notas deste módulo, com as definições e os links ([[Início]]):

- Conceitos: [[Bateria de conferência]] · [[Glosa]] · [[Leitura de entrega]] · [[Leitura hostil]] · [[Revisão cega]] · [[Teste de mutação]]
- Órgãos: [[MPCDF]]
- Casos: [[Caso - 13 de 13 e 55 achados]] · [[Caso - a bateria que deixava passar]] · [[Caso - a leitura hostil]] · [[Caso - o quociente que ninguém viu]]
- Planos: [[redacao_03 - OCI de câncer gástrico]] · [[redacao_07 - pré-plano de imagem da bancada]]

---

## Para que serve

Ao fim do módulo, a pessoa consegue:

- rodar as baterias e ler o relatório;
- dizer o que cada tipo de conferência pega e o que nenhuma pega;
- montar o pacote de uma revisão cega e triar os achados;
- fazer a leitura de entrega com as doze perguntas;
- ler o documento como quem quer reprová-lo.

## A lógica

**1. São quatro conferências, e nenhuma substitui a outra.**

| conferência | o que garante | o que não vê |
|---|---|---|
| **a bateria do padrão** (`conferir_plano.py`) | aritmética, estrutura, voz, régua, número sem fonte, código contra o catálogo | o que exige leitura: julgamento, contradição de sentido, número escrito em prosa que ninguém previu |
| **a bateria do plano** (`planos/redacao_NN/conferencia/`) | o que só aquele objeto tem, como o dimensionamento de uma sala | o resto |
| **o checklist das lições** (`consultar.py checklist`) | as lições que nenhuma verificação cobre inteira | o que não virou lição |
| **a revisão cega** | o que um parecerista que não conhece a conversa devolveria | as decisões tomadas de propósito, que ele aponta como falta |

E depois delas, a **leitura de entrega**: as doze perguntas, uma por vez, o documento
inteiro em cada passada.

**2. Verde não quer dizer aprovável.** A bateria só confere o que alguém previu. Um
plano que passava em 18 de 18 voltou do professor com 130 marcas. Outro, que passava em
22 de 22, teve doze problemas achados na leitura de entrega.

**3. Uma bateria que só passa não prova nada.** Por isso o teste de mutação: ele injeta
um erro conhecido por vez numa cópia do plano e exige que a verificação certa falhe. Se
o erro passa, o defeito é da bateria. Quando a bateria acusa, a primeira pergunta é se
o defeito é do plano ou do teste: no começo, a maioria dos alarmes era defeito da
própria ferramenta.

**4. Achado novo vira verificação nova.** O que um leitor aponta e dá para codificar vira
verificação, para não acontecer de novo. O que não dá vira lição com pergunta.

**5. O revisor precisa ser cego.** Quem revisa o que ajudou a escrever tende a achar
certo o que achou certo. Se o revisor recebe a conversa, o estado do plano ou as
lições, recebe as respostas junto e concorda com elas. Por isso o pacote cego leva só o
documento e as fontes primárias: as normas, as fichas do procedimento, os planos
aprovados (com CPF mascarado) e, no pré-plano, o formulário da SES. O papel do revisor é o de
quem vai devolver o plano em diligência, e "nada a apontar" é uma resposta aceita.

**6. A revisão tem rodadas e triagem.** Até três rodadas: a primeira cega; na segunda,
os mesmos revisores julgam as respostas e o documento corrigido; a terceira, só o que
ficou em divergência. Cada achado recebe uma resposta: aceito (corrige, com a fonte);
aceito em parte; contestado (não muda, e mostra o trecho da norma: sem fonte não se
contesta); decisão de quem conduz o projeto (vai a ele com os dois lados); ou citação
inválida (o trecho citado não existe). Quando o achado é uma condição a comprovar, ele é
aceito no controle interno: vai para as pendências, nunca para o documento, porque
viraria régua. Na versão final, um modelo de outra família lê uma vez.

**7. Ler como quem quer reprovar.** A leitura hostil procura o que daria a alguém um
caminho legal para declarar a entidade inapta, sem precisar inventar exigência. E a
hostilidade não acaba na aprovação: na prestação de contas, cada promessa a mais vira
glosa na mão de quem quer glosar.

**8. Corrigir também cria erro.** Toda correção muda o documento, e o que dependia do
trecho corrigido pode quebrar. Por isso a segunda rodada existe, e por isso as baterias
voltam a rodar depois de cada correção.

## Pode e não pode

| pode | não pode | por quê | onde está escrito |
|---|---|---|---|
| entregar com as duas baterias em 100% e a mutação passando | entregar com verificação falhando sem decisão registrada | a decisão de deixar falhar é de quem conduz, e fica escrita | `metodo/plano/conferencia.md` |
| perguntar primeiro se o defeito é do plano ou do teste | "consertar" o plano para a bateria passar sem entender o alarme | a ferramenta também erra | idem |
| mandar ao revisor cego o documento e as fontes primárias | mandar a conversa, o `estado.yaml`, as lições ou o método | o revisor concordaria com as respostas que recebeu | `metodo/revisao/cega.md`, seção 2 |
| varrer CPF e CNS antes de o pacote sair | mandar pacote com dado pessoal a serviço de fora | se a varredura acusa, nada sai | idem |
| contestar um achado com o trecho da norma | descartar um achado sem fonte | aceitar e contestar exigem fonte | idem, seção 4 |
| mandar condição a comprovar para as pendências | transformar explicação de regra em texto do documento | viraria régua contra o proponente | idem |
| perguntar ao revisor "o que você devolveria em diligência?" | perguntar "o que falta neste plano?" | a segunda pergunta empurra o plano para o memorial | `metodo/revisao/perguntas.md` |
| rodar as baterias de novo depois de cada correção | considerar a correção pronta sem conferir | correção também cria erro | caso 2 |

## O caso

### Caso 1 — o quociente que ninguém viu

**O que se fez.** Em 11/10/2026, para escolher o revisor, testou-se a revisão em um
documento com gabarito: a versão do plano de câncer gástrico de 03/09, contra os 31
apontamentos firmes da devolutiva do professor.

| revisor | apontamentos pegos |
|---|---|
| um modelo de outra empresa, só com contas e contradição | 8 |
| outro modelo de outra empresa, com as normas | 14 |
| dois revisores Claude cegos | 23 (74%) |

Nenhum apontamento achado pelos revisores de fora escapou aos cegos. O custo: os dois
cegos deram 235 achados; só o das perguntas mais longas deu 174, 111 deles pequenos e
repetidos.

**O que ninguém tinha visto.** Os revisores acharam erros que estavam no plano desde
setembro e continuavam na versão atual: o quociente da meta escrito 12.967,03 quando a
conta dá 12.967,29; o título "os três riscos altos" sobre uma matriz que tinha quatro; um
risco classificado médio com a mesma probabilidade e o mesmo impacto que davam alto a
outro.

**E a pergunta que estraga.** A conferência antiga, feita em agosto num caderno de outro
serviço, perguntava o que "faltava" e quais eram as "condições". Gerou uma seção inteira
de condições, que o professor cortou. Pergunta de falta empurra o plano para o memorial e
para a régua.

**O que passou a valer.** O Claude cego é o revisor padrão; o modelo de outra família lê
uma vez a versão final. E a ressalva fica escrita: o teste foi um documento só, e as
perguntas nasceram da mesma devolutiva que serviu de gabarito.

*Fontes: `metodo/revisao/cega.md`, seção 8;
`planos/redacao_03/revisao/calibracao_20261011/calibracao.md`. Conversa de 11/10/2026.*

### Caso 2 — 13/13 e 55 achados

**O que havia.** O pré-plano de exames de imagem, em 19/10/2026, passava nas duas
baterias, 13 de 13 e 12 de 12.

**O que a revisão cega achou.** 55 achados. Oito viraram correção, entre eles:
- o plano dizia que a produção se registrava em APAC, mas a APAC desses exames é do
  programa federal: exame avulso se registra em BPA-I;
- a fila da mamografia somava 187 pedidos da fila diagnóstica, mas o código com
  incremento é só o de rastreamento;
- a base legal da meta citava só a portaria das emendas individuais, e a emenda era de
  bancada.

Sete condições sanitárias que os revisores pediram (responsável técnico, proteção
radiológica, licença, entre outras) foram para as pendências: no pré-plano, viraram
régua contra o proponente. E 34 achados bateram em decisões já tomadas por quem conduz o
projeto, como esperado de um revisor cego.

**A correção que criou erro.** Ao corrigir, o assistente tirou a frase "truncado na
segunda casa decimal". Na segunda rodada, os revisores viram que os valores unitários
deixaram de decorrer da regra escrita: 99,946 vira 99,94 só se a regra estiver lá. A
frase voltou.

**O que o caso ensina.** Nenhuma verificação lê a norma do programa federal; a revisão
lê. E a segunda rodada existe porque toda correção mexe no documento.

*Fontes: `metodo/revisao/cega.md`; `metodo/pre_plano/conferencia.md`, "A revisão cega".
Conversa de 19/10/2026.*

### Caso 3 — a leitura hostil

Em 07/10/2026 o plano de ultrassom e tomografia, na versão 20, foi lido como quem quer
reprová-lo, usando como régua os documentos da própria SES em outro processo. Achou
quatro pontos que abririam caminho para reprovar, e que nenhuma verificação via:

- os polos sem CNES, endereço ou licença, com uma seção dizendo que o CNES estava
  cumprido e outra dizendo que não constava;
- "capacidade instalada do proponente", numa estrutura que era alugada;
- o valor unitário 2,75 vezes a tabela, sem tratar da habilitação que dá o incremento;
- a troca de beneficiário da emenda, sem explicação.

E mais quinze, em três grupos: o que atrasa, o que morde na prestação de contas e o que
arranha a credibilidade. A decisão do que mexer foi de quem conduz o projeto, e os
pontos não mexidos ficaram registrados como decisão.

*Fonte: `planos/redacao_04/leitura_hostil_v20.md`, no ramo `plano-04-ultrassom-tomografia`.*

### Caso 4 — a bateria que deixava passar

Quatro defeitos das próprias baterias, achados por mutação ou por leitura:
- a verificação de indicadores não via a coluna "parâmetro": um indicador a 95% passava;
- a de número sem fonte, ao tentar aceitar percentual arredondado, deixou passar um 43%
  falso; desfeito, e o arredondamento passou a ser registrado na fonte;
- a conferência de preços aceitava erro de um centavo no teto; apertada para meio;
- a conferência da coleta procurava "recarg" e a palavra no arquivo era "recarregada".

*Fonte: `metodo/plano/conferencia.md`, "As duas baterias".*

## Leia na fonte

Na ordem:

1. `metodo/plano/conferencia.md`, inteiro.
2. `metodo/plano/leitura_de_entrega.md`, inteiro.
3. `metodo/pre_plano/conferencia.md`, inteiro.
4. `metodo/revisao/cega.md`, inteiro, e `metodo/revisao/perguntas.md`.
5. `planos/redacao_03/revisao/calibracao_20261011/calibracao.md`.

## Faça

Rode os comandos; não altere arquivo nenhum.

1. **A bateria.** Rode `python3 ferramentas/conferir_plano.py planos/redacao_03/`. Quantas
   verificações há, quantas passam e quais "não se aplicam"? Por que a Y não se aplica?
2. **A mutação.** Rode `python3 ferramentas/testar_conferencia_plano.py planos/redacao_03/`.
   O que o relatório diz? O que significaria uma mutação que passa?
3. **O que a bateria não vê.** Pela tabela da `leitura_de_entrega.md`: das doze
   perguntas, quais têm verificação automática, e quais só a leitura pega?
4. **A leitura.** Pegue a seção 3 do `planos/redacao_03/plano.md` e faça nela as
   perguntas 2 (número sem lastro), 8 (totais que não se reconciliam) e 12 (contradição
   interna). O que você acha?
5. **O pacote.** Pelo `metodo/revisao/cega.md`, seção 2: liste o que entra no pacote cego
   e o que nunca entra. Por que o `estado.yaml` não entra?
6. **A triagem.** Numa revisão do plano 3, para cada achado, diga a resposta (aceito,
   contestado, decisão de quem conduz, ou aceito no controle interno): (a) "a soma da
   coluna de valores não fecha com o total", e você conferiu que não fecha; (b) "o plano não diz quem é o responsável técnico pela radioproteção em cada
   polo"; (c) "o plano deveria trazer 12 meses de vigência, e não 8"; (d) "o plano cita
   a portaria de emenda individual numa emenda de bancada".
7. **A calibração.** No `calibracao.md`: por que o próprio estudo diz que o resultado é
   otimista?
8. **O checklist.** Rode `python3 ferramentas/consultar.py checklist planos/redacao_03/`
   (sem `--saida`, só para ler). Escolha três perguntas e responda sobre o plano 3.

## Confira

| # | pergunta | o que conta como resposta certa |
|---|---|---|
| 1 | A bateria | 26 verificações, 24 passam (padrão 23 de 25, plano 1 de 1). A G (capacidade por polo) e a Y (contra o pré-plano) não se aplicam. A Y não se aplica porque o plano 3 não tem pré-plano enviado apontado no `estado.yaml` |
| 2 | A mutação | Cada erro injetado precisa ser acusado pela verificação certa. Uma mutação que passa quer dizer que a bateria tem um ponto cego: o defeito é dela |
| 3 | O que não vê | Têm verificação: régua (S), número sem lastro (T), ausência anunciada (U), em parte a analogia (V) e a estrutura (J). Só a leitura pega: memorial, detalhe que vira compromisso, totais que não se reconciliam, argumento aberto, registro de linguagem, matéria no lugar errado, contradição interna |
| 4 | A leitura | O quociente 12.967,03, que a conta dá 12.967,29. Se a seção trouxer dois totais da mesma fila sem reconciliar, é a pergunta 8. Vale qualquer achado com o trecho e a conta |
| 5 | O pacote | Entram o documento, as normas citadas, as do programa e a sanitária, as fichas do SIGTAP, os cinco planos aprovados com CPF mascarado e, no pré-plano, o formulário. Nunca entram a conversa, o `estado.yaml`, as lições, o método, nem CPF ou CNS. O `estado.yaml` traz as decisões e as respostas: o revisor concordaria com elas |
| 6 | A triagem | (a) aceito, corrige. (b) aceito no controle interno: vai para as pendências, não para o documento. (c) decisão de quem conduz: o `estado.yaml` do plano 3 registra a vigência como decisão do usuário; vai a ele com os dois lados (e, quando houver termo, vale o termo). (d) aceito: cita-se a portaria do tipo da emenda |
| 7 | Otimista | Porque as perguntas de diligência nasceram da mesma devolutiva que serviu de gabarito, e porque foi um documento só |
| 8 | O checklist | Vale qualquer resposta que cite o trecho do plano e a lição |

E quatro perguntas para responder de cabeça:

- A bateria está verde. O plano pode ir? O que falta?
- Por que o revisor não pode ver a conversa?
- O revisor diz que falta um requisito sanitário no pré-plano. Onde isso vai?
- Por que a segunda rodada da revisão existe?
