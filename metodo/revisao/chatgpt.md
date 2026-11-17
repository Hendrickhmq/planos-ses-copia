# revisao/chatgpt.md — o revisor do ChatGPT, na versão final

O método comum, com o pacote, a triagem e as rodadas, está em `cega.md`, e as perguntas em
`perguntas.md`. Este arquivo diz quando e como o ChatGPT roda.

## Quando

**Uma vez, na versão final do documento,** depois que as rodadas do Claude cego fecharam e
antes da entrega. É a leitura de outra família de modelo, a última trava contra o viés de o
Claude conferir o que o Claude ajudou a escrever. *Origem: decisão do usuário, 11/10/2026:
"acho válido a versão final do plano passar pelo Sol".*

## O modelo

**O padrão é o GPT-6.1 Sol, nas perguntas A1, A2 e A4,** no esforço `high`.

| modelo | quando | por quê |
|---|---|---|
| **Sol** (`gpt-6.1-sol`) | o padrão | rende de 15 a 160 mensagens a cada 5 horas no plano Plus, contra 5 a 45 do Astra. Basta para contas, contradição e a pergunta aberta |
| **Astra** (`gpt-6-astra`) | só se o usuário pedir | na calibração, uma rodada de quatro perguntas gastou 240 mil tokens e esgotou a cota da conta inteira por cerca de 4 horas |
| **Luna** | nunca para revisar | é o modelo de tarefa fácil |

*Origem: os limites são estimativas de terceiros, porque a OpenAI não publica números
exatos. O consumo do Astra foi medido na calibração de 11/10/2026.*

**O que não dar a ele:** norma de memória. O Astra alucinou 51% no AA-Omniscience (setembro
de 2026), e só vale o arquivo do pacote, com o trecho literal. Também não as nossas
decisões: ele não as conhece, e é de propósito.

**Se a cota acabar no meio,** a entrega espera a cota voltar ou segue sem ele, e quem decide
é o usuário. Não se troca de modelo sem perguntar.

## Como roda

```bash
python3 ferramentas/revisar_chatgpt.py <rodada>/pacote --saida <rodada>/chatgpt
python3 ferramentas/revisar_chatgpt.py <rodada>/pacote --saida <rodada>/chatgpt --modelo gpt-6-astra --passadas A1,A2,A7,A4
python3 ferramentas/revisar_chatgpt.py <rodada>/pacote --saida <rodada>/chatgpt --treplica <rodada anterior>
```

- Usa o Codex que vem no app do ChatGPT, em modo não interativo.
- O sandbox é somente leitura: ele lê e roda Python, mas não escreve nem sai para a rede.
- A sessão é efêmera e não leva a configuração do usuário. Memória, plugins, apps e skills
  ficam desligados.
- A resposta segue o esquema `esquemas/achados.json`, ou `esquemas/veredito.json` na
  tréplica.
- **Uma pergunta por execução,** porque ele fecha a tarefa em poucos turnos. As perguntas
  rodam em paralelo, cada uma em 2 a 3 minutos.
