> **ATENDIDO em 15/09/2026** por `fontes/validacao_ultrassom_20260915.xlsx`, lido em
> `fontes/validacao_ultrassom.md`. As quatro coisas pedidas vieram e nada do que a
> lista mandava cortar apareceu.

# Coleta de ultrassonografia — o que pedir, e o que não pedir

Escrito em 15/09/2026, depois de medir o que da coleta de tomografia entrou de fato no
plano: **nove abas e cerca de 580 linhas, das quais umas 60 foram usadas.**

## A regra que economiza mais do que cortar linha

**Rotular a medida.** A coleta de tomografia custou uma rodada de forense porque o
mesmo procedimento aparecia como 4.467 num lugar e 9.814 noutro — cartão contra
gráfico, fila contra fila mais devolvidas.

Uma linha no topo resolve:

> Todos os números usam a medida **Solicitações** (os três status de fila), todos os
> anos, grupos de ultrassonografia.

Com o rótulo, as abas de conferência e de reconciliação deixam de ser necessárias.

## O que precisa vir — quatro coisas

### 1. Lista completa dos procedimentos, com o código SIGTAP · fecha a L-001

Nome interno, solicitações e o campo `codigo_sigtap_solicitacao`. **É a aba mais
valiosa.** Na tomografia foi ela que revelou que 343 nomes internos colapsam em treze
códigos da Tabela do SUS, e que a angiotomografia de coronárias é faturada como
tomografia de tórax.

Aqui ela decide onde entram **parede abdominal** e **partes moles** — 6.095 exames sem
código fechado.

### 2. Região de Saúde por procedimento do objeto · preenche a seção 3.5

Todas as categorias, **inclusive "sem região informada"** e as de origem de serviço —
URD, Contratado/Credenciado. Sem elas o rateio não se sabe sobre que base foi feito.

### 3. Espera média da fila

Só os três status de fila. A espera de "todos os status" mistura as devolvidas e não
entra no documento.

### 4. Classificação de risco, com todas as prioridades

Inclusive a **Prioridade 4**, que a rosca do painel esconde.

## O que não precisa vir

| item | por quê |
|---|---|
| **Pendentes — Regulação CRDF** | zerada em todos os recortes da tomografia, e o LEIA-ME registra que usa campo de status diferente das outras medidas |
| **Recorte `Ano = 2026`** | o plano trabalha com todos os anos |
| **Coluna "todos os procedimentos da base"** | é o SISREG inteiro; plano de objeto delimitado não usa |
| **Faixa etária ano a ano** | virou uma oração no plano. Bastam a faixa de concentração e o pico |
| **Status por procedimento** | o plano não reporta status |
| **Espera de "todos os status" e das devolvidas** | serviram uma vez, para mostrar a armadilha da medida. A regra já está registrada |
| **Abas de conferência e de reconciliação de totais** | existiam para desfazer dúvidas que nasceram de leitura de captura de tela |

## Os onze nomes que a coleta precisa alcançar

Oito já têm código fechado e servem de conferência cruzada — se o painel trouxer outro
código para algum deles, é o painel que manda.

| nome na planilha do objeto | código que o plano usa hoje |
|---|---|
| Ecografia de mama bilateral | 02.05.02.009-7 |
| Ecografia transvaginal | 02.05.02.018-6 |
| Ecografia abdômen total adulto | 02.05.02.004-6 |
| Ultrassonografia doppler venoso MMII (bilateral) | 02.05.01.004-0 |
| Ecodoppler de carótidas | 02.05.01.004-0 |
| Ecografia do aparelho urinário | 02.05.02.005-4 |
| Ecografia de tireoide adulto | 02.05.02.012-7 |
| Ecografia de próstata (via abdominal) | 02.05.02.010-0 |
| Ecografia de abdômen superior adulto | 02.05.02.003-8 |
| **Ultrassonografia de parede abdominal** | **sem código — L-001** |
| **Ecografia de partes moles** | **sem código — L-001** |

O doppler tem uma pergunta a mais, que a lista não responde e a ficha do SIGTAP sim:
**a quantidade máxima do 02.05.01.004-0**. Se um doppler venoso bilateral de membros
inferiores exigir dois registros, a linha de 14.401 exames dobra — é a maior
sensibilidade aberta na planilha.
