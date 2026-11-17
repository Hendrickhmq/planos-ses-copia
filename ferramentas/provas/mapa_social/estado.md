# O gauntlet do agente mapa-social — o placar

O procedimento é `metodo/agentes/gauntlet.md`. As saídas das rodadas ficam fora do
repositório, em `~/.cache/planos-ses/gauntlet/mapa_social/rodada_<N>/<versão>/<caso>/`.

**Campeão:** v2, desde a rodada 2 (em `.claude/agents/mapa-social.md`). **O usuário parou o gauntlet no v2 em 27/10/2026**, para testar o agente antes de juntar ao main.

**Os modelos das rodadas 1 e 2.** Nada fixava o modelo, e todo papel herdou o da conversa, o
Opus 5.5 (`claude-opus-5-5`, pelos registros da sessão): o v1 e os candidatos da rodada 1 em
esforço extra (`xhigh`); o v0 no P5, o construtor do v2, o v2 nos cinco casos e os dois
críticos da rodada 2 em esforço alto (`high`). Desde 27/10/2026 o agente roda em Sonnet,
esforço médio (o cabeçalho de `.claude/agents/mapa-social.md`): **o título do v2 vale para o
Opus** até os cinco casos rodarem no modelo do agente.

## Rodada 1 — v1 (o agente enxuto) contra v0 (o agente de a2e199e)

Recarga da base: 26/10/2026 22:32:42 (qLastReloadTime 2026-10-27T01:32:42.805Z), a mesma em
todas as execuções e em todos os árbitros. Kit da rodada: assinatura 511491576.

| caso | v1: portões | v1: árbitro (coleta = árbitro) | v0 | vence |
|---|---|---|---|---|
| P1 | todos ok | otorrino geral 5.418 pedidos e 5.418 pessoas; ecografia de mamas 13.188; soma por ano 13.188 | não rodou: o portão do kit cai por construção | v1, por portão |
| P2 | todos ok | 006-9 finalidade 6.461, teto 49.653; 004-2 finalidade viva 1.648; soma por ano 7.210 | não rodou: idem | v1, por portão |
| P3 | todos ok | finalidade 5.431, viva 4.152, núcleo 2.054; soma por ano 5.482 | não rodou: idem | v1, por portão |
| P4 | todos ok | bolsa escrotal 966, mamografia 6.746, TC de crânio 413; soma por ano 6.747 | não rodou: idem | v1, por portão |
| P5 | todos ok (parou e listou o CID da finalidade e a ficha) | não se aplica | **mediu com a ordem incompleta** (tirou a composição do pacote da Tabela) e escreveu um script próprio: caem o escopo e o gabarito | v1, por portão |

**O crítico não votou nesta rodada:** todo caso se decidiu nos portões. O v0 não usa a ordem
nem o kit, e o portão do kit (as partes conferidas pelo `ler_motor.py`) e a K caem nele por
construção; por isso ele rodou só onde o resultado não estava decidido antes (P5). O P3 do
v0 ficou de fora também pelo custo: o limite de uso da sessão bateu no meio do P5 do v0.

**Catraca:** o v1 vence os 5 casos sem perder portão. Campeão: v1.

**Correções fora do loop, para a rodada 2** (peças determinísticas, na suíte):
- o árbitro do P1 comparava a soma das filas da ultrassonografia (100.431) com o total
  distinto (100.429): dois pedidos contam em dois pares nome × código. O caso passou a
  comparar números por fila, e o kit passou a medir o total distinto de cada universo
  (assinatura nova 3348663882; montador 2026-10-27.2);
- no panorama, a resposta do montador não imprime mais "achados fora do enquadramento";
- o método ganhou o botão fora da tela com o painel escondido (o `find`), o cabeçalho
  "Atualizado em" do painel, que junta a data UTC com a hora de Brasília, e a aba que fica
  aberta no fim — os três "o que faltou no método" que o v1 devolveu.

**O veredito para o construtor da rodada 2** (o que pesou contra o campeão, nas respostas
dele): a resposta do P2 copiou 40 achados e o "e mais 148", longa para o líder; as
respostas repetem o que o montador imprimiu em vez de apontar para ele; o v1 achou o botão
escondido por conta própria, sem o método dizer.

## Rodada 2 — v2 (a resposta curta) contra v1

O construtor mudou só "O que você devolve" (a impressão do montador num bloco de código, sem
reescrever, com os 10 primeiros achados e "e mais N"; sem hash, assinatura nem tempo; o que
faltou no método só se o método não cobre) e apontou o método para o botão escondido e para as
armadilhas. Kit da rodada: assinatura 3348663882; montador 2026-10-27.2.

Recarga do v2: 27/10/2026 02:32:53 (2026-10-27T05:32:53Z), a mesma nos cinco árbitros. **O v1
não rodou de novo** na recarga nova, embora o método mande: os dois diferem só na forma da
resposta, as medidas saem do kit e dos scripts, e cada execução tem o árbitro na própria
recarga. A economia foi de cinco execuções, depois de o limite de uso da sessão ter batido na
rodada 1.

| caso | v2: portões | v2: árbitro (coleta = árbitro) | crítico |
|---|---|---|---|
| P1 | todos ok | otorrino geral 5.418 e 5.418; ecografia de mamas 13.188; o total distinto da ultrassonografia, 100.430, igual ao do kit | v2 |
| P2 | todos ok | 006-9 finalidade 6.461, teto 49.652; 004-2 finalidade viva 1.648 | v2, por pouco |
| P3 | todos ok | 5.431, 4.152, 2.054 | v2 |
| P4 | todos ok | 966, 6.746, 413 | v2 |
| P5 | todos ok | não se aplica | v2 |

**O crítico.** O primeiro crítico votou com as respostas do v1 do P2, do P3 e do P4
**resumidas pelo líder** ao gravar o `resposta.md` (os achados num parêntese), e puniu o v1 por
isso; ele mesmo apontou que parte da diferença vinha do montador novo. O voto foi descartado,
as três respostas voltaram ao texto que o v1 devolveu, e um crítico novo, avisado de que a
diferença que vem só dos scripts não decide, votou: **v2 em 5 de 5**, todos pelo critério 4
(resposta curta e útil). Nos critérios 1, 2, 3 e 6 os dois empatam em todos os casos: nenhum
número próprio, nenhuma decisão, nenhum arquivo a mais, a parada certa no P5.

**Catraca:** o v2 vence os 5 casos sem perder portão. Campeão: v2.

**Achado do crítico para o montador:** no P4, a TC de crânio de emergência com pedidos (391,
136, 68 e 23) estava no `.md` como "a decidir", mas não aparecia na resposta, porque o
enquadramento já a tinha (sem decisão) e a resposta só listava o que estava fora dele. A
resposta do montador passou a listar também as filas que o enquadramento deixou a decidir.

**Por que o loop parou aqui:** a regra é parar em 5 rodadas ou em 2 vitórias seguidas do
campeão, e o v2 ainda não defendeu o título. A rodada 3 custa outras 6 a 11 execuções no
painel; com o limite de uso já batido uma vez, ela fica para o usuário decidir (o freio do
método). O veredito para o construtor da rodada 3 é o do crítico novo: no P5, a resposta do v1
orientava o líder além de listar o que faltava; nas outras, o bastidor (hash, assinatura,
rótulo da tela) alongava a resposta. O v2 já não faz nenhuma das duas coisas.
