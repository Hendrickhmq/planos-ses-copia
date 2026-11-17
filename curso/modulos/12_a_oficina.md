# Módulo 12 — A oficina

**Interno.** Este módulo é sobre o repositório e as ferramentas. Nada daqui vai a
documento.

Antes deste módulo: todos os outros. Este é o último porque junta tudo: como o trabalho
se organiza, quem faz o quê, o que nunca entra no repositório, e um projeto de treino
de ponta a ponta.

**No cofre.** As notas deste módulo, com as definições e os links ([[Início]]):

- Conceitos: [[Bateria de conferência]] · [[Dossiê do objeto]] · [[Mapa Social da Saúde]] · [[Revisão cega]] · [[SEI]] · [[Teste de mutação]]

---

## Para que serve

Ao fim do módulo, a pessoa consegue:

- abrir o repositório numa máquina nova e saber onde está cada coisa;
- começar um plano novo no lugar certo, com a pasta e o ramo certos;
- chamar um agente com o que ele precisa, e ler o que ele devolve;
- mudar uma regra do método do jeito certo;
- dizer o que nunca entra no repositório;
- conduzir, com o Claude, um projeto de treino do recurso à conferência.

## A lógica

**1. Um repositório, uma verdade.** O padrão, as ferramentas, a base e os planos ficam
juntos porque se leem o tempo todo. Cada regra e cada fato moram num lugar só, e os
outros apontam para ele:

| pasta | o que é |
|---|---|
| `metodo/` | o padrão: como se faz qualquer plano ou pré-plano |
| `biblioteca/` | consulta: normas, instrumento, preços, proponentes |
| `registros/` | a base: acervo, obrigações, achados, lições |
| `planos/redacao_NN/` | um projeto por pasta |
| `ferramentas/` | os scripts e os testes |
| `estudo/` | os planos aprovados e a extração deles |
| `curso/` | este curso |

**2. O `main` é o tronco; cada plano em andamento tem o seu ramo.** O padrão e as
ferramentas moram só no `main`. O plano em andamento fica num ramo próprio, que guarda
só a pasta dele, e de preferência numa pasta de trabalho própria. Quando o `main`
melhora, o plano recebe a melhoria por merge. Se o plano precisa mudar uma regra ou uma
ferramenta, a mudança vai primeiro para o `main`. Quando o plano encerra, a pasta dele
entra no `main`.

**3. A pasta do plano tem lugar para cada coisa.**

| lugar | o que guarda |
|---|---|
| `estado.yaml` | as decisões e os números do projeto |
| `pendencias.md` | o que falta e o que se decidiu |
| `dados/` | as travas da fase 0: valor unitário, fila, preços, envelope |
| `dados/fontes/` | a ficha do SIGTAP e as coletas da fila, com a pasta bruta |
| `dossie/` | a escolha do objeto |
| `plano.md`, `plano_v<N>_<versão>.md` | o documento |
| `versoes/` | o enviado e o devolvido, lado a lado, e os PDFs |
| `recebidos/` | o que a SES mandou |
| `estudos/` | os estudos do projeto |
| `conferencia/` | a bateria própria do plano |

**4. Tarefa que se repete vira agente; o agente não decide.**

| agente ou comando | faz | não faz |
|---|---|---|
| `mapa-social` | busca a fila no painel, a partir de uma ordem de coleta | decidir que fila entra, interpretar, escrever resumo |
| `ficha-sigtap` | lê a ficha de cada código, com o histórico, e grava na pasta do plano | decidir o valor do plano |
| `precos` | pesquisa o valor, o que a SES paga e o mercado, e faz a conta | dizer o teto à clínica, decidir a oferta |
| `normas` | vigia as normas e o controle externo, nos dias 10 e 22 | mudar o método sem revisão |
| `/dossie` | junta os agentes para escolher o objeto | escolher: a escolha é de quem conduz |
| `/revisao` | a revisão cega | aceitar achado sem fonte |
| `/aula` | este curso | responder o que não está escrito |

O número sai do sistema para o disco por script, conferido por hash; o agente só busca.
Dois agentes de navegador nunca rodam ao mesmo tempo.

**5. O padrão muda por triagem.** Cada entendimento novo passa por uma pergunta: isto
muda como se faz qualquer documento desta trilha? Se sim, entra no `metodo/`, no arquivo
certo, com a linha de origem, e se registra em `metodo/MUDANCAS.md`. Se dá para
codificar, vira verificação. Se vale só para um tipo de objeto, vai para a `biblioteca/`.
Se não, fica nas lições do plano.

**6. O padrão se testa.** `ferramentas/testar_tudo.py` roda todas as conferências: que
todo caminho citado existe, que as regras citadas existem, que o dado não envelheceu, e
cada bateria. Roda também no GitHub, a cada envio.

**7. O que nunca entra.** Dado de paciente: CPF, CNS, nome, registro de atendimento,
APAC, laudo. Do painel, só contagens. O repositório é privado e guarda CPFs que vêm
nos documentos publicados pela SES (quatro dos cinco planos aprovados têm): por isso não se torna público nem se dá acesso
sem limpar antes. E nada pessoal, que não seja do projeto.

**8. Plano em andamento também precisa estar a salvo.** Trabalho que só existe na
máquina se perde. O que está pronto vai por commit e envio; o que ainda não está pronto
pode ir como ramo de cópia de segurança, sem decidir onde mora.

## Pode e não pode

| pode | não pode | por quê | onde está escrito |
|---|---|---|---|
| mudar regra no `main`, com origem e linha no `MUDANCAS.md` | mudar regra dentro do ramo de um plano | o padrão mora só no `main` | `metodo/LEIA.md`, "Como o padrão muda" |
| escrever a regra uma vez e apontar para ela | copiar a regra para outro arquivo, ou para a memória | duas cópias divergem | `README.md`, "A regra da organização" |
| pedir a fila ao agente, com a ordem de coleta | coletar à mão, ou deixar o agente decidir a fila | o número precisa sair conferido, e a decisão é de quem conduz | `metodo/coleta/mapa_social.md`, "Quem faz o quê" |
| olhar o maior número de registro em todos os ramos antes de criar um | criar um número novo olhando só o ramo aberto | dois ramos já usaram o mesmo número | caso 1 |
| guardar as contagens da fila | guardar CPF, CNS, nome ou telefone | dado de paciente nunca entra | `metodo/coleta/mapa_social.md`, "O que nunca sai do painel" |
| rodar `testar_tudo.py` antes de juntar ao `main` | juntar com teste falhando sem saber por quê | o teste é o que garante a uma verdade | `README.md`, "Comandos" |
| assinar o PDF por último, no programa de assinatura | passar o PDF assinado por ferramenta online | ela apaga a assinatura digital | caso 3 |

## O caso

### Caso 1 — o mesmo número em dois ramos

Em outubro de 2026, o `main` deu o número 100 da série de normas do acervo a uma
deliberação nova. Mas o ramo do pré-plano de imagem já usava os números 100 a 103, em
PDFs, documentos e 14 fichas, e o ramo de saúde mental usava o 104. Ao juntar os ramos,
os números colidiram. A do `main`, citada em três lugares, passou a NM-105, e entrou a
regra: antes de criar um número, olhar o maior em todos os ramos.

No mesmo merge, um script regravou o `registros/acervo.csv` trocando o fim de linha de
todas as linhas, e o git mostrou o arquivo inteiro como mudado. Foi refeito preservando o
formato. O `.gitattributes` explica por quê: a conferência depende dos mesmos bytes em
qualquer máquina.

*Fontes: `metodo/MUDANCAS.md`, linha de 28/10/2026; `.gitattributes`.*

### Caso 2 — o agente que media e julgava

Numa coleta de outubro de 2026, o mesmo agente mediu a fila e julgou o resultado, e o
teto de 50.317 pessoas (o caso 1 do módulo 6) passou na conferência. Noutra, um agente
escreveu na hora um script de 37 mil caracteres, com uma função que copiava decisões de
quem conduz o projeto. Daí a regra de 26/10/2026: o agente só busca; o número sai por
script, conferido por hash; o julgamento é do script e da conversa. Uma coleta feita à
mão, sem a ordem, passou a ser barrada pela conferência.

*Fontes: `metodo/coleta/mapa_social.md`, "Quem faz o quê" e "A ordem"; `metodo/MUDANCAS.md`,
linha de 26/10/2026.*

### Caso 3 — a assinatura que sumiu

Em 23/10/2026 o PDF do plano de ultrassom e tomografia foi assinado e, depois, passado
por uma ferramenta online. O texto era idêntico ao da versão aprovada, mas a assinatura
digital se perdeu: ficou só o carimbo visual, e ele cobria a linha da data. Quem conduz
o projeto notou que a assinatura não levava ao original.

**O que o caso ensina.** A assinatura é o último passo, e o arquivo assinado não passa
por mais nada. Confere-se no validador oficial antes de enviar.

*Fonte: conversa de 23/10/2026.*

### Caso 4 — o que só existia na máquina

Em 16/11/2026, antes de clonar o projeto em outra máquina, levantou-se o que só existia
na máquina: sete ramos que nunca tinham sido enviados, 732 arquivos sem commit na pasta
do plano 4, dois rascunhos empilhados e a memória do assistente. Tudo subiu, e o que
estava sem commit foi como ramos de cópia (`backup/pc-20261116/`), sem decidir por
quem conduz onde cada coisa mora. Antes do envio, procurou-se CPF e CNS em todos os
arquivos, inclusive dentro das planilhas. E as fotos pessoais que estavam numa pasta do
projeto saíram dele.

*Fonte: conversa de 16/11/2026; `claude/README.md`, para restaurar a memória.*

## Leia na fonte

Na ordem:

1. `README.md`, inteiro.
2. `metodo/LEIA.md`, "Como o padrão muda".
3. `metodo/MUDANCAS.md`: as cinco linhas mais novas.
4. `.claude/agents/mapa-social.md` e `.claude/commands/dossie.md`.
5. `metodo/coleta/mapa_social.md`: "Quem faz o quê", "A ordem" e "O que nunca sai do
   painel".
6. `claude/README.md`: como restaurar a memória numa máquina nova.

## Faça

Rode os comandos; não altere arquivo nenhum, até o exercício 6.

1. **A suíte.** Rode `python3 ferramentas/testar_tudo.py`. Quantas conferências passam?
   Ache, na saída, a do curso.
2. **Os ramos.** Rode `git branch -a`. Quais ramos são de plano, quais são cópia de
   segurança e qual é o tronco? Rode `git worktree list`: quais planos têm pasta
   própria?
3. **Onde vai.** Diga onde guardar cada coisa: (a) o ofício que a ARINS mandou para o
   plano 10; (b) uma regra nova sobre arredondamento de meta; (c) a ficha do SIGTAP de
   um código do plano 10; (d) uma norma nova que vale para todos; (e) o PDF enviado à
   SES; (f) uma dúvida que este curso não respondeu.
4. **Um registro.** Rode `python3 ferramentas/consultar.py LI-009`. O que é cada campo?
   Que outros registros ela cita?
5. **O agente.** Leia `.claude/agents/mapa-social.md`. O que quem chama precisa informar?
   O que o agente devolve, e o que ele nunca faz?
6. **O projeto de treino.** Com o Claude, numa pasta de treino fora dos planos de
   verdade (combine o lugar com quem conduz o projeto), faça de ponta a ponta:
   - recurso: R$ 1.000.000,00 de emenda de bancada, apoio de 8%;
   - objeto: escolha, com os dados já coletados no `planos/redacao_05/` (dossiê, fila e
     preços), entre as três OCI de otorrino;
   - escreva o pré-plano nos nove campos, com a meta em valor;
   - calcule a meta do plano pelo piso (módulo 9), com o valor da tabela que vale hoje
     (módulo 7), e o apoio como 8% do recurso;
   - monte a planilha de apoio pelo fluxo do atendimento (fase 2 do
     `metodo/plano/procedimento.md`), posto a posto, com preço do acervo;
   - rode as conferências e faça a leitura de entrega com as doze perguntas.
   Leve o resultado a quem conduz o projeto, para a correção.

## Confira

| # | pergunta | o que conta como resposta certa |
|---|---|---|
| 1 | A suíte | Todas passam (33 de 33 em 16/11/2026, sem as mutações). A do curso é a `testar_curso.py` |
| 2 | Os ramos | Tronco: `main`. De plano: `plano-03-cancer-gastrico`, `plano-04-ultrassom-tomografia`, `plano-09-saude-mental-infantojuvenil`, `plano-10-colonoscopia`, `plano_oci_cardiologia`, `pre-plano-07-imagem-bancada`. Cópias de segurança: os `backup/` (os `backup/pc-20261116/` são de 16/11; os outros, de outubro). Os demais são frentes de trabalho sobre o próprio projeto: `curso`, `plataforma`, `aprimoramento`, `revisao-externa`, `ajustes/ficha-g-e-metodo`. O `worktree list` mostra as pastas próprias; a pasta principal pode estar num ramo de plano, e então o `main` não está aberto em pasta nenhuma |
| 3 | Onde vai | (a) `recebidos/`, na pasta do plano 10, no ramo dele. (b) `metodo/`, no arquivo da regra, com origem e linha no `MUDANCAS.md`, no `main`. (c) `dados/fontes/`, na pasta do plano 10. (d) `biblioteca/normas/`, com linha no `registros/acervo.csv`, no `main`. (e) `versoes/`, na pasta do plano 10. (f) `curso/duvidas.md` |
| 4 | Um registro | A regra, o porquê, a origem (os registros de onde veio), como se verifica e a pergunta do checklist. Cita, entre outros, CT-001 e CT-012 |
| 5 | O agente | Quem chama informa a pasta bruta com a ordem de coleta. O agente devolve o que os scripts imprimem, as lacunas e o que faltou no método. Nunca decide nem interpreta, e nunca escreve resumo, planilha ou script |
| 6 | O treino | Corrigido por quem conduz o projeto. As conferências em 100% são o mínimo, não a nota |

E três perguntas para responder de cabeça:

- Você achou uma regra melhor enquanto fazia um plano. Onde ela vai, e como?
- Por que o agente não decide qual fila entra?
- O que você confere antes de enviar qualquer coisa a um serviço de fora?
