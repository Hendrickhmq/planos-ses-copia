# Extração do painel Lista de Espera — instrução para colar

Contexto para quem executa: o painel é **Lista de Espera — Exames e Consultas**, da
Secretaria de Estado de Saúde do Distrito Federal, acesso interno. No topo há um filtro
`nome_grupo_p...` que seleciona grupos de procedimento — na última consulta estava em
**2 de 55**.

**Prefira exportar a transcrever.** Cada painel tem um ícone de exportação no canto
superior direito. Se der para exportar em Excel ou CSV, exporte e mande o arquivo — é
melhor do que qualquer tabela digitada. Só transcreva o que não exportar.

**Em toda tabela, transcreva a linha inteira e o número exato, sem arredondar e sem
cortar o nome do procedimento.** Vários nomes aparecem truncados na tela com reticências
— abra, passe o mouse ou exporte para pegar o nome completo.

---

## Tarefa 0 — dizer qual é o filtro

Antes de tudo, abrir o filtro `nome_grupo_p...` e listar:

1. **Quais grupos estão selecionados** na configuração atual.
2. **A lista dos 55 grupos disponíveis**, ou pelo menos todos os que contenham
   "TOMOGRAFIA", "ULTRA", "ULTRASSOM", "ECOGRAFIA", "US " ou "DOPPLER" no nome.

Sem isso não dá para saber que universo cada número mede.

---

## Tarefa 1 — TOMOGRAFIA · conferir o que já temos

Com o filtro nos grupos de **tomografia**, transcrever ou exportar:

**1.1 — os cinco indicadores do topo**

| indicador | valor | tempo de espera |
|---|---|---|
| Pessoas na Fila | | — |
| Solicitações | | dias |
| Solicitações Pendentes — Regulação CRDF | | dias |
| Solicitações Pendentes — Regulação Local | | dias |
| Solicitações Devolvidas | | dias |

**1.2 — Região de Saúde \ Unidade Solicitante** — todas as linhas, inclusive URD,
Contratado/Credenciado, Serviços Centralizados e Público — Não SES.

**1.3 — Tipo de Procedimento / Descrição Procedimento** — **a lista inteira, rolando
até o fim.** Esta é a mais importante da tarefa 1: a captura anterior mostrou só os dez
primeiros e a barra de rolagem indicava mais. Formato:

```
código | nome completo do procedimento | quantidade
```

---

## Tarefa 2 — ULTRASSONOGRAFIA · é o que falta

Trocar o filtro para os grupos de **ultrassonografia / ecografia** e repetir **tudo**
que está na tarefa 1 — os cinco indicadores do topo, a Região de Saúde e a lista
completa de procedimentos.

**Esta é a tarefa mais importante das duas.** A ultrassonografia é 84% do objeto e não
temos nenhum número dela por território.

Além disso, nesta filtragem também:

**2.1 — Classificação de Risco** — Prioridade 1, 2 e 3, com as quantidades.

**2.2 — Solicitações por Faixa Etária** — a quantidade de cada barra do histograma.

---

## Tarefa 3 — procurar o código SIGTAP

Os códigos que aparecem na lista de procedimentos — 063, 111, 055, 053, 031, 061, 309,
109 — são numeração interna da SES-DF, não o código da Tabela do SUS.

Verificar se em algum lugar o painel expõe o código da Tabela do SUS, que tem o formato
`02.06.02.003-1`, com dez dígitos e um hífen. Tentar, nesta ordem:

1. Passar o mouse sobre a barra de um procedimento e ver o que o tooltip mostra.
2. Exportar a tabela de procedimentos e olhar todas as colunas do arquivo, inclusive as
   que não aparecem na tela.
3. Clicar na barra e ver se abre detalhe.

**Se não houver código da Tabela do SUS em lugar nenhum, dizer isso explicitamente** —
é uma resposta útil.

---

## Tarefa 4 — quatro procedimentos específicos

Independentemente das listas acima, procurar e informar a quantidade exata destes,
com o nome como o painel escreve:

| o que procurar | por quê |
|---|---|
| **ANGIOTOMOGRAFIA** — todas as linhas que começam assim | a captura mostrou três linhas diferentes somando 3.862, e a planilha do plano traz 1.397 só de coronárias |
| **PAREDE ABDOMINAL** — qualquer procedimento com esse termo | não existe procedimento com esse nome na Tabela do SUS; preciso ver como o painel o chama |
| **PARTES MOLES** — qualquer procedimento com esse termo | mesma situação |
| **DOPPLER** — todas as linhas, separando carótidas de membros inferiores | as duas caem no mesmo código da Tabela do SUS e preciso confirmar se o painel as separa |

---

## Como mandar

Markdown ou CSV, uma tabela por item, com o número do item. Se exportar arquivos,
mandar os arquivos e dizer a qual item cada um corresponde.

**Não somar, não arredondar, não resumir e não omitir linha pequena.** Linha de duas
solicitações importa para saber que o total fecha.

**Se algum número na tela estiver cortado ou ilegível, dizer que está — não estimar.**
