# revisao/gemini.md — o revisor do Google (Gemini Notebook), opcional

O método comum, com o pacote, a triagem e as rodadas, está em `cega.md`, e as perguntas em
`perguntas.md`. Este arquivo diz como o Gemini roda e guarda só os blocos próprios dele.
Quem roda é o `ferramentas/revisar_gemini.py`. As consultas C1 a C4 da antiga conferência
no NotebookLM viraram a G1, a G2 e a G3; a C2 saiu (abaixo, "não dá a ele").

**Fora do padrão.** Na calibração de 11/10/2026, o Gemini não achou nenhum apontamento que o
Claude cego não tenha achado. Ele também deu mais trabalho que os outros revisores:
- tomou um aprovado pelo documento em análise;
- perdeu as citações no formato rígido;
- não deixa escolher o modelo;
- a cota acabou em umas 15 consultas.

Fica para quando o usuário pedir uma leitura do Google. A tabela abaixo é o que se aprendeu
dele, e vale se ele voltar. *Origem: `planos/redacao_03/revisao/calibracao_20261011/calibracao.md`.*

## O papel: o leitor das fontes

| dá a ele | não dá a ele |
|---|---|
| **lastro e contradição contra a norma**, uma afirmação contra as fontes do caderno | **comparar vários documentos de uma vez**: no `redacao_03` (01/09/2026) ele confabulou 11 de 15 pontos ao comparar o plano com os cinco aprovados; e com os aprovados no caderno, toma um deles pelo documento em análise (11/10/2026) |
| **faturamento:** APAC, obrigatórios e opcionais, prazo, saída. **Só o que o documento diz diferente da norma:** perguntado pelo que "falta", ele pediu quatro explicações de regra, e explicar a regra ao parecerista é o memorial que a devolutiva corta (calibração de 11/10/2026) | **valores:** deu R$ 4.300 e R$ 3.000 onde a planilha dos aprovados diz R$ 3.200. Preço se lê da planilha consolidada, sempre |
| **execução e risco:** condição a comprovar, risco que a norma cria. **O achado de condição vai para o controle interno (`pendencias.md`), nunca para o documento:** em 01/09/2026 a C4 achou o teto de MAC, que entrou como "condição de partida" na 4.2, e a 4.2 inteira foi a régua mais cara que a devolutiva de 05/09 cortou (C1) | **o inventário dos aprovados (a antiga C2):** a estrutura e os itens saem por `grep` em `estudo/normalizados/`, que não confabula |
| **obrigações de uma norma só**, com o dispositivo e a transcrição (a comparação com o documento é nossa) | **contas e contradição interna:** são do Claude cego e do ChatGPT |
| **as diligências de leitura (G5 e G9):** régua, compromisso, analogia, argumento aberto, memorial, ausência, lugar, registro e detalhe. É a leitura de um documento só, com a norma ao lado | **as nossas decisões:** ele não as conhece, e é de propósito |
| **a pergunta aberta (G7)** | |

*Origem: proposta de 11/10/2026. Os pontos fortes são a resposta presa às fontes, com o
trecho citado (o `nlm` devolve o texto exato de cada citação), e caderno grande. Os pontos
fracos foram medidos aqui: a C2 de 01/09/2026, os valores da mesma rodada, a resposta sem
`sources_used` e a C4 lida sobre o instantâneo velho do `redacao_03`.*

## Como roda

```bash
python3 ferramentas/revisar_gemini.py <pacote> --saida <rodada>/gemini [--faturamento] [--obrigacoes <arquivo>...]
python3 ferramentas/revisar_gemini.py <pacote> --saida <rodada>/gemini --treplica <rodada anterior>
```

- **Um caderno novo a cada rodada,** com o nome "Análise — <objeto> — <data>". O caderno
  antigo do plano não serve: leva versões velhas do plano e páginas da web.
- O documento sobe com o título **"DOCUMENTO EM ANÁLISE"**, e as demais fontes com o nome
  do arquivo do pacote. O caderno recebe a instrução abaixo pelo `nlm chat configure`.
- **Os planos aprovados não sobem.** Com eles no caderno, numa pergunta longa, o Gemini
  tomou um aprovado de oftalmologia pelo documento em análise e respondeu sem citar nada:
  os seis achados da G1 eram sobre outro plano. A estrutura contra os aprovados é a A7, do Claude
  cego. *Origem: calibração de 11/10/2026.*
- **Cada consulta numa conversa nova** (`--new-conversation`) e **sempre com
  `--source-ids`**: a restrição de fontes é mecânica, nunca um pedido no texto da
  pergunta.
- O script guarda a resposta bruta e a converte para o esquema `esquemas/achados.json`.
  Quando o caderno devolve a marca de citação, a fonte sai dela. As fontes sobem sem a
  extensão no título, porque o Google troca "nome.md" por "[suspicious link removed]".
- **A prova é o trecho literal, não a marca de citação.** No formato rígido de resposta, o
  caderno quase nunca devolve a marca (`sources_used` vazio). Por isso o
  `conferir_revisao.py` procura o trecho da fonte, literal, em todo o pacote, e o arquivo
  em que ele aparece é a fonte. Trecho que não aparece em nenhum arquivo derruba o achado.
  *Origem: calibração de 11/10/2026: a G2 veio com quatro achados reais e nenhuma marca.*
- **A G6 roda sozinha** sobre todo achado cujo trecho da fonte não confere. Achado que não
  sobrevive à própria prova sai antes da triagem.

## A instrução do caderno

```prompt instrucao
Você analisa a fonte "DOCUMENTO EM ANÁLISE", um plano de trabalho apresentado à Secretaria de Estado de Saúde do Distrito Federal, contra as demais fontes deste caderno. Responda só com o que as fontes dizem, sempre citando-as. Se as fontes não tratam de um ponto, escreva "as fontes não tratam". Os campos marcados "[preencher]" são do modelo, o proponente os completa na entrega, e não são achado. Não elogie, não resuma o documento e não sugira estilo. Responda em português.
```

## O formato da resposta

O script cola este bloco no fim da G1, da G2, da G3 e da G7.

```prompt formato
Responda só com blocos neste formato, um por achado, sem texto antes nem depois:

### ACHADO
classe: <a classe pedida>
trecho_documento: "<cópia literal, contínua, de até 300 caracteres, do DOCUMENTO EM ANÁLISE>"
fonte: <o título exato da fonte que sustenta o achado>
trecho_fonte: "<cópia literal do trecho dessa fonte>"
gravidade: <reprova, diligencia ou ajuste>
por_que: <uma ou duas frases>

Quando o problema é uma ausência, trecho_documento é o trecho do documento mais próximo de onde o ponto deveria estar. Se não houver achado numa classe, escreva uma linha: VAZIO: <classe>. Lista vazia é resposta válida; achado sem fonte não vale.
```

## Os blocos próprios do Gemini

As perguntas G1, G2, G3, G5, G9 e G7 estão em `perguntas.md`. Aqui ficam a G4 (as obrigações de uma norma só) e a G6 (a prova), que só ele faz.

```prompt G4
Considerando apenas esta fonte, liste as obrigações que ela impõe a quem executa o serviço: o prestador, o estabelecimento ou a entidade convenente. Não compare com nada e não resuma. Responda só com blocos neste formato, um por obrigação:

### OBRIGACAO
dispositivo: <artigo, parágrafo, inciso ou item>
transcricao: "<cópia literal do dispositivo>"
```

```prompt G6
Considerando apenas esta fonte: transcreva literalmente, sem resumir nem parafrasear, o trecho que sustenta a afirmação abaixo. Se esta fonte não tiver trecho que a sustente, responda só NAO_HA.

Afirmação: {afirmacao}
```

## A tréplica, nas rodadas 2 e 3

O script troca a fonte do documento pela versão nova, com o mesmo título. A pergunta leva
os achados em discussão e as respostas.

```prompt G8
A fonte "DOCUMENTO EM ANÁLISE" é a versão nova de um documento que você analisou antes. Abaixo estão os seus achados da rodada anterior e a resposta do proponente a cada um. Para cada achado, dê um veredito: resolvido (a versão nova corrigiu), nao_resolvido (não corrigiu ou corrigiu mal; cite o trecho novo), contestacao_procede (o trecho de fonte que o proponente citou sustenta a contestação) ou contestacao_nao_procede (não sustenta; diga por quê com a fonte). Julgue o trecho citado, não o argumento. Responda só com blocos neste formato:

### VEREDITO
id: <o id do achado>
veredito: <resolvido, nao_resolvido, contestacao_procede ou contestacao_nao_procede>
trecho: "<o trecho do documento novo ou da fonte, literal>"
por_que: <uma ou duas frases>

{achados_e_respostas}
```
