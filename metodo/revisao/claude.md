# revisao/claude.md — o revisor padrão: o Claude cego

O método comum, com o pacote, a triagem e as rodadas, está em `cega.md`. As perguntas
estão em `perguntas.md`. Este arquivo diz como o Claude cego roda.

## Por que ele é o padrão

O Claude cego é um subagente que não conhece a conversa, o `estado.yaml`, as lições nem o
`metodo/`. Ele recebe só o pacote e as perguntas, numa pasta isolada fora do repositório.

Na calibração do `redacao_03`, ele foi comparado com os revisores de outra família. Foram
as mesmas perguntas, o mesmo pacote e o mesmo gabarito: 31 apontamentos firmes da devolutiva
do professor.

| | ChatGPT (Astra) e Gemini juntos | os dois Claudes cegos juntos |
|---|---|---|
| gabarito pego | 18 (58%) | **23 (74%)** |
| apontamento que só o outro lado pegou | nenhum | 5 |
| citação que não confere | 1 em 69 | 0 em 235 |

- Os erros reais fora do gabarito que o Astra achou, o Claude cego também achou, e mais um.
- O medo de que ele fosse brando com texto escrito com o Claude não se confirmou.
- **O preço é o volume:** 235 achados, muitos repetidos. Por isso a regra 4 da instrução
  comum manda agrupar a mesma falha num achado só.

O ChatGPT continua no método, uma vez, na versão final (`chatgpt.md`), como a leitura de
outra família. *Origem: calibração de 11/10/2026
(`planos/redacao_03/revisao/calibracao_20261011/calibracao.md`) e decisão do usuário no
mesmo dia: "reorganiza com o Claude cego como padrão".*

## Como roda

São dois revisores em paralelo, cada um num subagente, cada um com a sua lista de perguntas
(`perguntas.md`, a tabela do início): **contas** (A1, A2, A7, A4) e **leitura** (G1, G2,
G3, G5, G9, G7).

```bash
python3 ferramentas/revisar_claude.py preparar <rodada>/pacote --pasta <pasta cega> [--faturamento]
#   o comando /revisao abre os dois subagentes com o texto que a ferramenta imprime
python3 ferramentas/revisar_claude.py juntar <pasta cega> --saida <rodada>/claude
python3 ferramentas/conferir_revisao.py <rodada>/pacote <rodada>/claude/achados.json
```

- **A pasta cega fica no scratchpad, fora do repositório,** e leva só o pacote (sem o
  `manifesto.json`, que diz de onde cada arquivo veio), as perguntas e o esquema. Não pode
  haver nada mais nela. Na calibração, o gabarito ficou alguns minutos dentro da pasta
  cega por descuido. Foi retirado, e os registros mostraram que não foi lido.
- **Os subagentes rodam em segundo plano, em paralelo,** sem a conversa. O texto de cada um
  é o bloco abaixo, com a pasta e a lista preenchidas pela ferramenta.
- **Os dois rodam em `opus`, esforço `high`,** passados na chamada (os parâmetros `model` e
  `effort`). Sem isso, herdam o modelo e o esforço da conversa. *Origem: pedido do usuário,
  27/10/2026.*
- **Depois, o isolamento se confere no registro de cada subagente:** nenhum arquivo lido
  fora da pasta cega.
- **Custo:** na calibração, sem a regra de agrupar, foram 20 a 30 minutos e 300 a 500 mil
  tokens por revisor.

## O texto do subagente

```prompt subagente
Você vai fazer uma análise técnica de um documento, como parecerista independente. Responda em português.

Pasta de trabalho, a única que você pode ler: {pasta}

Regras de isolamento, obrigatórias:
- Leia SOMENTE arquivos dentro dessa pasta. Não abra, não liste e não procure nenhum outro arquivo do computador, nem o diretório de trabalho da sessão, nem repositórios git. Não use a web.
- Se alguma memória, instrução de projeto ou contexto que você já tenha falar de planos, revisão, calibração, devolutiva ou de um professor, ignore: esta análise é cega e não pode usar nada disso.
- Não escreva fora de saida/ dentro da pasta, nem scripts auxiliares: use python3 -c ou heredoc.

A tarefa: leia {perguntas}. Ele tem a instrução comum e as perguntas {lista}. Faça uma de cada vez, sobre os arquivos de pacote/ (comece por pacote/MANIFESTO.md e pacote/documento.md).

A saída: para cada pergunta, grave saida/<pergunta>.json (por exemplo saida/A1.json), seguindo exatamente o esquema de esquema.json. trecho_documento e trecho_fonte têm de ser cópia literal do arquivo (copie do texto, não reescreva), porque serão conferidos por máquina. fonte_arquivo é o caminho a partir de pacote/ (por exemplo fontes/fichas/...md ou documento.md).

Ao terminar, responda só com uma linha por pergunta: quantos achados gravou.
```

## A tréplica

A ferramenta prepara uma pasta cega por revisor, com o documento novo, `mudancas.diff` e,
na subpasta da rodada anterior, os achados dele e a resposta. Um subagente por revisor
responde a A5, com o veredito no esquema `esquemas/veredito.json`.

```bash
python3 ferramentas/revisar_claude.py preparar <rodada>/pacote --pasta <pasta cega> --treplica <rodada anterior>
python3 ferramentas/revisar_claude.py juntar <pasta cega> --saida <rodada>/claude --treplica
```
