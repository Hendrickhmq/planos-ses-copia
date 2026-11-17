> **ATENDIDO POR INTEIRO em 15/09/2026.** Tomografia e ultrassonografia coletadas.
> L-001, L-002 e a parte crítica da L-003 fecharam. Fica como registro do pedido.

> **BLOCO 1 ATENDIDO em 15/09/2026** pela coleta em
> `fontes/mapa_social_tomografia_20260915.xlsx`. A L-002 fechou: a SES-DF registra a
> angiotomografia de coronárias sob 02.06.02.003-1. **Continua aberto o bloco de
> ultrassonografia**, que é 82% do objeto.

# O que extrair do painel — lista de pedido

Montada em 15/09/2026, com o usuário no painel. Ordem de prioridade: o que bloqueia o
documento vem primeiro.

**Formato:** sempre que o visual tiver o ícone de exportação, **exportar em vez de
capturar tela**. Os números do painel de tomografia hoje registrados vieram de leitura
de imagem e estão marcados como tal.

---

## Bloco 1 — enquanto o filtro está em tomografia

### 1.1 A lista completa de procedimentos · resolve L-002

O visual *Tipo de Procedimento / Descrição Procedimento* rola além dos dez primeiros.
**Todas as linhas**, com o nome exato e o número de solicitações.

Serve para três coisas: saber o tamanho real da fila de tomografia, ver se há
procedimento grande fora do objeto, e ler os nomes completos das três linhas de
angiotomografia — que na captura aparecem truncados.

### 1.2 O código SIGTAP, se o painel tiver · resolve L-002

Os prefixos do painel — 063, 111, 055, 053, 031, 061, 309, 109 — são numeração da
SES-DF. **Se a exportação trouxer coluna de código da Tabela do SUS**, é ela que
fecha a angiotomografia de coronárias. Se não trouxer, o caminho é outro: qual código
a SES-DF fatura hoje para esse exame.

### 1.3 Região de Saúde · confirma o rateio de tomografia

A tabela inteira do visual *Região de Saúde\Unidade Solicitante*, com os números
exatos. Os que estão registrados foram lidos da imagem.

### 1.4 O filtro que está aplicado

O chip diz `nome_grupo_p... 2 de 55`. **Quais são os dois grupos selecionados**, e se
há filtro de status, de data ou de unidade executante além dele.

Sem isso não se sabe qual universo os números descrevem.

---

## Bloco 2 — trocando o filtro para ultrassonografia

**A ultrassonografia é 82% do objeto** — 61.999 dos 75.451 exames. Todo o bloco 1 se
repete para ela, e o item mais importante é o rateio.

| # | o que | para quê |
|---|---|---|
| 2.1 | Região de Saúde\Unidade Solicitante, tabela completa | **fecha o rateio dos três polos — é o que trava a seção 3.5** |
| 2.2 | Tipo de Procedimento, todas as linhas | resolve L-001 — sob que nome entram parede abdominal e partes moles |
| 2.3 | Cabeçalho: Pessoas na Fila, Solicitações, Devolvidas e os tempos de espera | a seção 3.1 abre com o tempo de espera |
| 2.4 | Classificação de Risco | a seção 3.1 publica a participação de Prioridade 1 e 2 |
| 2.5 | Faixa etária | sustenta o parágrafo clínico da 3.2 |

---

## Bloco 3 — a reconciliação · não é extração, é resposta

**A planilha e o painel contam coisas diferentes, e a diferença é de quase o dobro.**

| linha | planilha | painel | razão |
|---|---|---|---|
| TC abdômen superior c/ contraste | 4.453 | 9.814 | 2,20× |
| TC pelve/bacia c/ contraste | 3.808 | 7.599 | 2,00× |
| TC tórax c/ contraste | 3.068 | 4.869 | 1,59× |
| TC tórax s/ contraste | 726 | 2.604 | 3,59× |
| Angiotomografia de coronárias | 1.397 | 1.550 | 1,11× |
| **soma** | **13.452** | **26.436** | **1,97×** |

E o cabeçalho do painel traz quatro números do mesmo universo: Pessoas na Fila 12.543,
Solicitações 22.483, Devolvidas 26.418, e a soma por Região 47.655.

**As três perguntas:**

1. **A coluna da planilha conta pessoa ou solicitação?** Os 13.452 da planilha estão
   perto das 12.543 pessoas na fila e longe das 22.483 solicitações.
2. **Qual filtro gerou a planilha** — grupos, status, data, unidade executante?
3. **A planilha cobre o status "devolvida"?** São 26.418 solicitações devolvidas para
   complementação, com 1.294 dias de espera — mais da metade do universo.

**Por que isto importa mais do que parece:** a seção 3 do plano abre com o número da
fila, e o parecerista tem o painel aberto. Se o plano diz 75.451 e o painel mostra
outro número para o mesmo recorte, a diferença precisa estar explicada pelo próprio
plano — qual universo, qual data, qual filtro. É a pergunta 8 da leitura de entrega:
**o documento não publica dois totais do mesmo universo.**

---

## Bloco 4 — o que o painel não tem · L-006

Não sai do Mapa Social e continua faltando:

- salas de ultrassonografia por polo;
- tomógrafos por polo;
- turno praticado.

A aritmética da seção 6.3 pede dez salas de ultrassonografia e dois tomógrafos em
turno de dez horas. O documento declara **capacidade requerida**, não inventário — mas
se o parque real ficar abaixo disso, o risco 1 da matriz deixa de ser risco e vira
fato.
