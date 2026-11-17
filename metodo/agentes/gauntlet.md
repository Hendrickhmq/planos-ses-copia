# agentes/gauntlet.md — melhorar um agente por rodadas contra uma referência real

O prompt de um agente melhora por **gauntlet loop**: um construtor faz o candidato, os
dois rodam os mesmos casos, portões automáticos derrubam o que erra, um crítico novo e cego
escolhe entre as saídas que sobraram, e uma catraca guarda o melhor. O humano é o freio.
Vale hoje para o agente `mapa-social`; outro agente que entrar segue este arquivo.

*Origem: o gauntlet loop de Matt Shumer, adaptado e com teto, por decisão do usuário em
26/10/2026, quando o `mapa-social` passou a só buscar (`../coleta/mapa_social.md`, "Quem
faz o quê").*

---

## O que entra no loop

**Só o prompt do agente** (`.claude/agents/<nome>.md`). O kit, os scripts e a conferência
são determinísticos: passam pela suíte (`ferramentas/testar_tudo.py`), que faz o papel dos
portões terminais, e não mudam dentro de uma rodada.

| | onde |
|---|---|
| os casos, as âncoras, os gabaritos e o árbitro | `ferramentas/provas/mapa_social/casos.json` e `casos/<caso>/` (a ordem e a pasta mínima do plano) |
| cada versão do prompt | `ferramentas/provas/mapa_social/versoes/v<N>.md` (v0 é o agente de antes da mudança, no commit a2e199e) |
| o placar | `ferramentas/provas/mapa_social/estado.md` |
| as saídas das rodadas | fora do repositório: `~/.cache/planos-ses/gauntlet/mapa_social/rodada_<N>/<versão>/<caso>/` |

## Os modelos

Cada papel roda num modelo e num esforço fixos, e a conversa os passa na chamada do
subagente (os parâmetros `model` e `effort`). Sem isso, o subagente herda o da conversa.

| papel | modelo e esforço |
|---|---|
| candidato e campeão | os do cabeçalho do agente (`model` e `effort` em `.claude/agents/<nome>.md`). O gauntlet mede o que a produção roda. Eles rodam como `general-purpose`, que não tem cabeçalho, e por isso a chamada leva os dois |
| crítico | `opus`, esforço `high` |
| construtor | `opus`, esforço `high` |

O modelo e o esforço do agente não entram no loop: mudá-los é decisão do usuário, e o
campeão medido em outro modelo tem de ser conferido de novo. O placar diz o modelo de cada
execução. *Origem: pedido do usuário, 27/10/2026. O v1 rodou em Opus com esforço extra, e o
v2 em Opus com esforço alto, porque nada fixava o modelo, enquanto o agente passou a rodar
em Sonnet.*
| a ferramenta | `ferramentas/provas/mapa_social/gauntlet.py` (preparar, árbitro, portões) |

## Os casos

Cinco, em três tamanhos, com âncoras reais. A base recarrega até duas vezes por dia: o
número da âncora vale como ordem de grandeza, e o que se confere exato é o árbitro.

| caso | tamanho | ordem | âncora | gabarito |
|---|---|---|---|---|
| P1 | amplo | panorama das consultas especializadas e da ultrassonografia | — | responde à ordem inteira; nomes exatos; nada de ranking nem recomendação |
| P2 | dada a fila | cardiologia: a OCI de insuficiência cardíaca (capítulo I aceito, I50 de finalidade) e uma estreita | redacao_08, 25/10/2026 | teto ≠ finalidade; CID largo, dominante e genérica disparam; ECG e Holter a decidir |
| P3 | estreito, OCI | otorrino 09.04.01.003-1, J30–J39 | redacao_05, 08/10/2026 (3.459 pessoas nos exames) | finalidade = teto, dito; as filas de consulta achadas |
| P4 | estreito, exame | bolsa escrotal, mamografia e TC de crânio, com o enquadramento do redacao_07 | redacao_07, 26/10/2026 | o nome exato achado pelo motor; a TC de emergência separada como fila achada; nenhuma decisão |
| P5 | incompleto | a OCI sem o CID da finalidade e sem a ficha | — | para e lista o que falta; nenhum número |

## A referência real

1. **O árbitro, na mesma recarga.** Logo depois de cada execução, o líder mede três
   números por caso com as expressões escritas à mão em `casos.json` (não pelo kit), mais a
   soma por ano, e grava `arbitro.json` na pasta do caso
   (`gauntlet.py arbitro <rodada> <versão> <caso>` imprime as expressões). Se a recarga
   mudou entre a execução e o árbitro, a rodada é **inválida** e o campeão fica.
2. **As âncoras.** A varredura tem de achar toda fila da âncora que ainda existe (o árbitro
   diz quais existem), com o nome exato.
3. **O escopo.** A conferência K passa, e não há arquivo do agente fora do contrato.

## A rodada

1. **Construtor** (um subagente): recebe o prompt do campeão, o método e o veredito da
   última derrota. Devolve o candidato, com uma linha por mudança.
2. **Execução:** `gauntlet.py preparar <rodada> <versão>`; o candidato roda os cinco casos,
   e o campeão roda de novo se a recarga mudou desde a última execução dele. Cada um roda
   como `general-purpose`, com o prompt colado (assim os dois convivem sem recarregar a
   definição do agente) e o modelo e o esforço do agente ("Os modelos"), **um de cada vez**, cada um na sua aba: o navegador é um só, e
   agentes em paralelo derrubam a sessão um do outro (`../coleta/ficha_sigtap.md`). A
   mensagem final de cada execução vai para `resposta.md` na pasta do caso **como veio**: o
   líder não resume nem corta, porque o crítico julga exatamente esse texto. *Origem: rodada
   2, 27/10/2026: as respostas do v1 resumidas pelo líder fizeram o primeiro crítico punir o
   v1 pelo corte, e o voto foi descartado.*
3. **Portões automáticos:** `gauntlet.py portoes <rodada> <versão>` confere o kit (o
   `ler_motor.py`), a conferência em 100%, o árbitro, a privacidade, a âncora, o escopo e o
   gabarito. Um portão que cai é derrota imediata no caso, com o nome do portão.
4. **Crítico** (um subagente novo a cada rodada, no modelo de "Os modelos", que não vê o
   raciocínio do construtor):
   recebe, por caso, a ordem, a âncora e as duas saídas como A e B, em ordem sorteada.
   Escolhe uma pela rubrica:
   - responde à ordem inteira;
   - só número do motor, ou lacuna dita;
   - nada além de buscar;
   - resposta curta e útil ao líder;
   - achados com tamanho;
   - parou quando devia.
   Cada voto cita arquivo e linha; o voto vago anula o caso. O crítico julga o comportamento
   do agente: a diferença que vem só dos scripts (o montador mudou entre as execuções) não
   decide o voto.
5. **Catraca:** o candidato vira campeão se vencer a maioria dos casos sem perder portão
   em nenhum.
6. **Placar:** o `estado.md` registra a rodada, a recarga, o modelo e o esforço de cada
   papel, os portões, os votos e o campeão.

**Parada:** 5 rodadas, ou o campeão vencer 2 seguidas, ou o usuário mandar parar. No fim, o
campeão vai para `.claude/agents/<nome>.md`, e o placar é mostrado ao usuário antes do
commit.

**O custo** de cada rodada são de 5 a 10 execuções no painel ao vivo. Quando o resultado
de um lado está decidido antes de rodar (o v0 não usa o kit, e os portões do kit e da K
caem por construção), ele roda só onde a comparação diz algo, e o placar diz por quê.
