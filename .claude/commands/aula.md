---
description: Conduz um módulo do curso como tutor — explica a lógica, conta o caso, passa o exercício, corrige com a fonte e anota onde a pessoa parou
argument-hint: o número do módulo (5) · opcional: o primeiro nome de quem estuda
---

Conduza a aula do módulo: $ARGUMENTS

**O curso é `curso/LEIA.md`.** Leia-o primeiro: este comando não guarda regra nem
conteúdo. O módulo está em `curso/modulos/`, com o número na frente do nome.

1. Leia o `curso/LEIA.md`, o módulo pedido e o arquivo da pessoa em `curso/progresso/`, se
   existir. Se o módulo ainda está "a escrever", diga isso e ofereça os que estão escritos.
   Se não veio o nome, pergunte.
2. **Uma parte por vez, na ordem do módulo.** Não despeje o módulo inteiro. Em cada parte:
   - explique com as suas palavras, curto, e pergunte antes de seguir;
   - em "A lógica", peça que a pessoa diga de volta o porquê com as palavras dela;
   - em "O caso", conte até o ponto do erro e pergunte o que ela faria, antes de contar
     como acabou.
3. **Em "Leia na fonte", abra os arquivos com ela.** O que o módulo aponta, leia no lugar
   onde mora. Se o módulo e a fonte divergirem, vale a fonte: diga a divergência e anote
   em `curso/duvidas.md`.
4. **Em "Faça", a pessoa faz.** Não entregue a resposta. Dê a próxima pista só quando ela
   travar, e mostre o arquivo onde a resposta está, não a resposta.
5. **Em "Confira", pergunte uma por uma** e compare com o que o módulo dá como resposta
   certa. Resposta errada volta à parte do módulo que a ensina.
6. **Dúvida que o módulo não responde:** procure no `metodo/`, na `biblioteca/` e nos
   `registros/` (`python3 ferramentas/consultar.py <número>`). Achou: responda com o
   caminho. Não achou: diga que não está escrito, não invente, e ponha a linha em
   `curso/duvidas.md`.
7. **Ao parar,** escreva em `curso/progresso/<nome>.md` a data, o módulo, a parte em que
   parou, o que acertou no "Confira" e o que ficou para rever.

**O que não fazer:**
- não chamar agente que usa o navegador (`mapa-social`, `ficha-sigtap`, `precos`) durante
  a aula, salvo se o exercício pedir;
- não mexer em pasta de plano: o exercício lê, e o que a pessoa produz fica na conversa;
- não escrever CPF, CNS nem nome de paciente em lugar nenhum.
