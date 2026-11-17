---
description: Gauntlet loop do prompt de um agente — o construtor faz o candidato, candidato e campeão rodam os casos de prova no painel, os portões automáticos derrubam o que erra, um crítico cego escolhe, a catraca guarda o melhor; até 5 rodadas ou 2 vitórias seguidas do campeão
argument-hint: o agente (hoje só mapa-social) · a rodada · "continuar" para seguir do estado.md
---

Rode o gauntlet de: $ARGUMENTS

**O método é `metodo/agentes/gauntlet.md`.** Leia-o primeiro, e o placar em
`ferramentas/provas/mapa_social/estado.md`: este comando não guarda regra.

1. **O construtor.** Na primeira rodada, o candidato é o que está em `versoes/`. Nas
   seguintes, chame um subagente, com `model` e `effort` na chamada, os do construtor no
   método, e com o prompt do campeão, o método e o veredito da última
   derrota; grave o candidato em `versoes/v<N>.md`, com uma linha por mudança.
2. **Preparar.** `python3 ferramentas/provas/mapa_social/gauntlet.py preparar <rodada> <versão>`.
   Escolha o caminho da saída de cada ordem: a área de transferência só quando o usuário
   não estiver usando a máquina (o botão sobrescreve o que ele copiou, e o app o avisa a cada cópia).
3. **Executar**, um caso de cada vez, nunca em paralelo: um `general-purpose` com o prompt
   da versão colado e a pasta bruta do caso, e com `model` e `effort` na chamada, os do
   cabeçalho do agente (o método, "Os modelos"). Grave a mensagem final dele em `resposta.md`,
   na pasta do caso. Depois de cada execução, o árbitro: `gauntlet.py arbitro ...` dá as
   expressões; meça-as no painel pelo motor (não pelo kit), na mesma recarga, e grave
   `arbitro.json`. Recarga diferente da coleta: a rodada não vale.
4. **Os portões.** `gauntlet.py portoes <rodada> <versão>`, para o candidato e para o campeão.
5. **O crítico.** Um subagente novo, que não viu o construtor, com `model` e `effort` na
   chamada, os do crítico no método: por caso, a ordem, a âncora e
   as duas saídas como A e B, sorteadas. A rubrica e o voto com arquivo e linha estão no
   método. Voto vago anula o caso.
6. **A catraca e o placar.** Atualize o `estado.md`: rodada, recarga, modelos, portões, votos e
   campeão. Pare em 5 rodadas, em 2 vitórias seguidas do campeão ou quando o usuário mandar.
7. Mostre o placar ao usuário. O campeão vai para `.claude/agents/<nome>.md` só depois.
