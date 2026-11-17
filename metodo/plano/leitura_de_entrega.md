# plano/leitura_de_entrega.md — a fase 7: as doze perguntas

Nasceu da devolutiva de 05/09/2026, que trouxe 130 marcas e 40 apontamentos sobre um
plano que passava em 18 de 18 verificações. **Verde não quer dizer aprovável:** a
máquina mede aritmética, estrutura e voz, e o professor lê julgamento.

Das doze classes de erro que a devolutiva revelou, **quatro viraram verificação** —
S, T, U e V. As outras oito não são detectáveis por código, e é para elas que esta
leitura existe. Faz-se com o documento pronto, uma pergunta por vez, o documento
inteiro em cada passada.

| # | classe | a pergunta | quem pega |
|---|---|---|---|
| 1 | **régua contra o proponente** | este prazo, percentual ou quadro de condições é exigido por alguma norma? | **S** — meta abaixo de 100%, faixa de tolerância, coluna de comprovação, condicionante de liberação e gatilho por prazo |
| 2 | **número sem lastro** | de onde vem este número, e onde ele está registrado? | **T** — em dígito e por extenso |
| 3 | **negação de ausência** | este parágrafo existe para dizer o que o plano não tem? | **U** |
| 4 | **afirmado por analogia** | isto foi conferido na ficha do procedimento, ou deduzido de caso parecido? | **V**, em parte |
| 5 | **memorial** | o parecerista sabe disto melhor que eu, ou é ato dele e não meu? | leitura |
| 6 | **estrutura fora do acervo** | os cinco aprovados fazem assim? | J, em parte |
| 7 | **detalhe que vira compromisso** | esta precisão fixa destino, território ou prazo que o executor não controla? | leitura |
| 8 | **totais que não se reconciliam** | o documento publica dois totais do mesmo universo? | leitura |
| 9 | **argumento aberto** | esta seção diagnostica e não fecha? esta tabela mostra e não explica? | leitura |
| 10 | **registro de linguagem** | isto é vocabulário de mercado ou de método num documento de política pública? | leitura |
| 11 | **matéria no lugar errado** | este conteúdo está agrupado numa seção que não devia existir? | leitura |
| 12 | **contradição interna** | há duas seções afirmando coisas incompatíveis? | leitura |

**A primeira rodada desta leitura, em 05/09/2026, achou doze coisas num plano que
passava em 22 de 22** — e duas delas eram pontos cegos das próprias verificações
novas: o T só enxergava dígito, e o S só olhava meta de indicador. Os dois foram
tapados no mesmo dia. É o ciclo que o método já usava: achado novo vira verificação
nova.

**A pergunta 12 é a mais cara e a que mais escapa.** No `redacao_03` a 5.13 previa
contratar plataforma de teleconsulta enquanto a 8.3 declarava que não havia rubrica
de sistema — as duas passaram por dezoito verificações.

**Duas perguntas de fechamento, depois das doze:**

- **O que mudou de premissa nesta rodada, e o que dependia dela?** É comum, regra 14, e ela
  falha exatamente quando a alteração é pequena: em 05/09/2026 o professor apagou
  duas palavras da curva — "e rampa" — e dois parágrafos continuaram dizendo o
  contrário.
- **A devolutiva anterior está inteira tratada?** Não se responde de memória:
  `python3 ferramentas/extrair_devolutiva.py <devolutiva.docx> --plano <plano.md>` procura cada
  trecho marcado no plano atual. E o que o revisor **digitou** não tem marca — para
  achar, `--enviado <o .docx que mandamos>`, o que obriga a arquivar o enviado ao
  lado do devolvido.
