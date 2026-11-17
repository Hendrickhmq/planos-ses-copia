# Agentes antes e depois — a OCI de cardiologia do redacao_08

**Controle interno.** Comparação de 25/10/2026 entre o que os agentes entregaram em 22/10/2026
e o que entregam pelo método novo, no ramo `melhorias/agentes` (commits `a45d4d8` e `b7126c0`,
locais, fora do `main`). Nada do redacao_08 foi alterado: a coleta nova é um arquivo a mais
(`dados/fontes/mapa_social_20261025.*`), ao lado da de 22/10.

## Resumo

| agente | antes (22/10) | depois (25/10) |
|---|---|---|
| Mapa Social | 50.317 pessoas na OCI de insuficiência cardíaca e 51.918 na união das sete, com 7/7 na conferência | 6.510 na insuficiência cardíaca (4.620 com pedido dos últimos 24 meses) e 12.380 na união; os seis alarmes no topo; a coleta de 22/10 reprovaria no conferidor novo (H e I) |
| Ficha do SIGTAP | sete fichas reconstituídas pelas Notas Técnicas, sem conferência com a Tabela | as sete batem com o pacote oficial de 10/2026; da próxima vez saem dele |
| Preços | ordem pela cobertura da descrição inteira; a 005-0 era a única que se pagava (105%) | ao lado, o mínimo da APAC, a APAC num só prestador e o preço fraco: a 005-0 depende de um preço de São Paulo, e a 006-9 cai a 51% num só prestador |
| Normas | rodada só no dia 10: a Nota e o pacote de 10/2026, de 15/10, ficavam para 10/11 | rodada também no dia 22 (proposta, a tarefa agendada não mudou) e o pacote confere as fichas |

## A fila: a mesma base, outro método

A base quase não mudou entre 22 e 25/10 (a união das sete foi de 51.918 para 51.632 no
teto). O que mudou foi o recorte. Coleta nova:
`planos/redacao_08/dados/fontes/mapa_social_20261025.md`, conferência nova 9/9.

| OCI | 22/10 | teto | **finalidade** (CID) | finalidade viva 12 / **24** / 36 m | variante | núcleo (como) |
|---|---|---|---|---|---|---|
| 001-8 risco cirúrgico | 442 | 441 | **441** (Z136, Z848) | 238 / **307** / 367 | sem recorte de CID: 9.630 (P-08) | 387 (o ECG) |
| 002-6 avaliação cardiológica | 504 | 502 | **502** (Z136, Z848) | 300 / **360** / 424 | — | 387 (o ECG) |
| 003-4 SCC inicial | 29.111 | 28.734 | **3.683** (I20, I25) | 2.659 / **3.087** / 3.366 | I20 a I25: 4.450 | 1.437 (consultas) |
| 004-2 SCC, eco de estresse | 2.119 | 2.055 | **2.055** (I20 a I25) | 1.233 / **1.651** / 1.988 | I20, I25: 1.466 | 2.026 (consultas) |
| 005-0 SCC, cintilografia | 3.413 | 3.310 | **3.310** (I20 a I25) | 1.909 / **2.911** / 3.243 | I20, I25: 2.696 | 2.026 (consultas) |
| 006-9 insuficiência cardíaca | 50.317 | 50.055 | **6.510** (I50) | 3.764 / **4.620** / 5.204 | IC ampliada: 7.092 | 2.077 (consultas) |
| 007-7 pré-operatório | 132 | 136 | **136** (Z018, Z488, Z489) | 103 / **130** / 136 | sem recorte: 9.630 | 87 (consulta) |
| a união das sete | 51.918 | 51.632 | **12.380** | — / **9.714** / — | 13.131 | — |

**Os alarmes da coleta nova:**
- **CID largo e CID dominante** na 003-4 e na 006-9. No teto, o I10 (hipertensão) é 88% do
  ECG com CID do capítulo I.
- **CID raro** na 001-8 (1,5%), na 002-6 (1,2%) e na 007-7 (0,5%). Na consulta de risco
  cirúrgico, o pedido vem com o CID da cirurgia (varizes, colelitíase, hérnia): é a P-08.
- **Fila velha** na 001-8 (30%). A 006-9 fica logo abaixo do limite, com 29%.
- **Estoque:** o Holter tem 13,2 anos de agendamentos na fila; as cintilografias, 4,7 e 4,3.
- **Fila genérica** nas sete. Sem as genéricas, a finalidade da 006-9 cairia para 969
  pessoas (só a consulta de insuficiência cardíaca e o ergométrico).

**Duas coisas que a coleta nova revelou:**
- **A idade da ficha.** A 001-8 e a 002-6 são de 18 anos em diante: na idade, são 360 e 420
  pessoas, e não 441 e 502. Corrigido no método (`d3f9d80`); os números da tabela ainda não
  aplicam a idade.
- **O IEV e o risco cirúrgico.** O IEV executa 4.647 OCI 001-8, dez vezes a fila com o CID
  da ficha. Ele só pode estar atendendo a consulta de risco cirúrgico sem recorte (9.630).
  Isso reforça a P-08.

## O que cada medida faz no dossiê

Recurso de R$ 2.000.000,00, apoio provisório de R$ 200.000,00 (o mesmo comparativo de 22/10).
"Recurso + IEV" soma as OCI que o recurso compra às que o IEV já executa no convênio
030977/2026, contra a fila.

| OCI | medida | pessoas | atendidas pelo recurso | parte da fila | sobra do recurso | IEV na fila | recurso + IEV |
|---|---|---|---|---|---|---|---|
| **006-9** | A antiga (teto) | 50.317 | 5.142 | 10% | R$ 300,00 | 2% | 12% |
| | B finalidade inteira | 6.510 | 5.142 | 79% | R$ 300,00 | 15% | 94% |
| | C finalidade viva | 4.620 | 4.620 | 100% | R$ 183.000,00 | 22% | 122% |
| | D núcleo | 2.077 | 2.077 | 100% | R$ 1.073.050,00 | 48% | 148% |
| **003-4** | A antiga | 29.111 | 6.666 | 23% | R$ 180,00 | — | — |
| | B finalidade inteira | 3.683 | 3.683 | 100% | R$ 805.590,00 | — | — |
| | C finalidade viva | 3.087 | 3.087 | 100% | R$ 966.510,00 | — | — |
| | D núcleo | 1.437 | 1.437 | 100% | R$ 1.412.010,00 | — | — |
| **005-0** | A antiga | 3.413 | 957 | 28% | R$ 1.031,40 | — | — |
| | B finalidade inteira | 3.310 | 957 | 29% | R$ 1.031,40 | — | — |
| | C finalidade viva | 2.911 | 957 | 33% | R$ 1.031,40 | — | — |
| | D núcleo | 2.026 | 957 | 47% | R$ 1.031,40 | — | — |
| **004-2** | A antiga | 2.119 | 2.119 | 100% | R$ 1.270.250,00 | 42% | 142% |
| | B finalidade inteira | 2.055 | 2.055 | 100% | R$ 1.286.250,00 | 44% | 144% |
| | C finalidade viva | 1.651 | 1.651 | 100% | R$ 1.387.250,00 | 55% | 155% |

As OCI de CID Z (001-8, 002-6, 007-7) têm de 87 a 502 pessoas em qualquer medida: o recurso
zera a fila e sobra quase tudo, como antes.

**O que muda na conclusão do dossiê de 22/10:**
- **"O IEV executa 2% da fila da 006-9; fazer a mesma OCI é trabalhar em conjunto, não
  sobrepor."** Na finalidade, o IEV é 15% da fila, e o recurso mais o IEV chegam a 94%. Na
  fila viva, passam dela (122%): a sobreposição com o IEV vira risco real.
- **"As filas grandes são as do capítulo I."** A 003-4 deixa de ser grande: o recurso zera a
  finalidade e sobram R$ 805.590,00. A única fila que o recurso não zera em nenhuma medida é
  a da 005-0 (cintilografia), justamente a de preço fraco.
- **"A 003-4 e a 006-9 dividem 28.929 pessoas, quase todas com hipertensão."** Pela
  finalidade, dividem 117.

## A justificativa em cada medida

- **A (antiga):** "As filas de regulação do DF de cardiologia com CID das doenças do aparelho
  circulatório reúnem mais de 50 mil pessoas" — o conferidor novo do dossiê reprova.
- **B:** "6.510 pessoas aguardam exame ou consulta de cardiologia com CID de insuficiência
  cardíaca (I50) nas filas de regulação do DF, com espera média de 763 dias (Mapa Social da
  Saúde, base de 25/10/2026)."
- **C:** "4.620 pessoas com pedido feito nos últimos dois anos aguardam exame ou consulta de
  cardiologia com CID de insuficiência cardíaca, com espera média de 223 dias (Mapa Social da
  Saúde, base de 25/10/2026)."
- **D:** "2.077 pessoas aguardam consulta de cardiologia com CID de insuficiência cardíaca
  (Mapa Social da Saúde, base de 25/10/2026)."

## A recomendação

**B, a finalidade na fila inteira, com a viva ao lado na página.**
- É o número que a SES reproduz no próprio painel, sem corte de data, e o padrão do método.
- A fila velha da 006-9 (29%) não passou do limite.
- A fila viva fica na página (linha "fila viva") e serve de piso na meta: com a viva, o
  recurso já zera a 006-9, e isso pesa na combinação com o IEV.
- C é a alternativa se você preferir não contar pedido de 2012. Ela muda a conta, mas não a
  ordem do dossiê. Exige explicar o corte de 24 meses, e a regra 11 do `comum.md` pede a
  fila sem argumento adicional.
- D é piso, não fila: serve para a meta prudente, não para a justificativa.

Em todas as medidas, a finalidade principal é a escolhida (I50 na 006-9; I20 e I25 na 003-4).
As variantes acrescentam pouco (IC ampliada: +582).

## Preços: o que a regra nova mostra com os mesmos preços de 22/10

Sem pesquisa nova: refeito das 1.245 linhas de preço do `dados/precos.md` de 22/10/2026. Antes, o
comparativo ordenava pela cobertura da descrição inteira, que soma todos os compatíveis. A
regra nova põe ao lado o mínimo da APAC (os obrigatórios e uma consulta), a APAC feita num
só prestador do DF e o preço fraco.

| OCI | valor | cobertura antiga (descrição inteira) | mínimo da APAC | cobertura APAC | APAC num só prestador do DF | cobertura num só prestador | preço fraco |
|---|---|---|---|---|---|---|---|
| 005-0 cintilografia | R$ 1.879,80 | 105% | R$ 1.798,00 | 105% | nenhum | — | cintilografia sem preço no DF (pacote de São Paulo) |
| 003-4 SCC inicial | R$ 270,00 | 46% | R$ 301,00 | 90% | MedicCei, R$ 378,00 | 71% | — |
| 002-6 avaliação cardiológica | R$ 200,00 | 46% | R$ 151,00 | 132% | Bip Coração, R$ 187,00 | 107% | — |
| 001-8 risco cirúrgico | R$ 130,00 | 44% | R$ 151,00 | 86% | Bip Coração, R$ 187,00 | 70% | — |
| 006-9 insuficiência cardíaca | R$ 350,00 | 43% | R$ 522,22 | 67% | MedicCei, R$ 686,74 (o único com os cinco) | 51% | — |
| 007-7 pré-operatório | R$ 130,00 | 37% | R$ 84,45 | 154% | Clínica Femmina, R$ 108,26 | 120% | — |
| 004-2 eco de estresse | R$ 250,00 | 36% | R$ 693,00 | 36% | Poli Sante, R$ 765,00 | 33% | eco de estresse: um só preço no DF |

**O que muda na leitura:**
- A única OCI que "se pagava" (005-0, 105%) depende de um preço que não é do DF, e nenhum
  prestador do DF a faz inteira. Pela regra nova ela sai marcada.
- Num só prestador, a 006-9 cobre 51%, não 67%, e só a MedicCei faz os cinco itens.
- A 002-6 e a 007-7 se pagam mesmo num só prestador; a 003-4 e a 001-8 ficam perto de 70%.

## Fichas: reconstituídas × pacote oficial

As sete fichas de 10/2026 foram reconstituídas em 22/10 pelas Notas Técnicas, porque a tela
do SIGTAP estava parada em 05/2026. O pacote oficial de 10/2026 estava no FTP desde 15/10. Com
o leitor novo (`ler_tabela_unificada.py`) e a verificação H do `conferir_ficha.py`:

| OCI | valor | idade | CID | obrigatórios e compatíveis |
|---|---|---|---|---|
| 001-8 a 007-7 | as sete batem | as sete batem | as sete batem | as sete batem |

A 005-0, por exemplo, sai do pacote com R$ 1.879,80, como a ficha reconstituiu pela SAES
4.795/2026. **As fichas estavam certas; o erro do redacao_08 foi só na fila.** O que o pacote
muda é o caminho: da próxima vez a ficha sai dele, sem reconstituir. Falta o catálogo do grupo
09 de 10/2026 (`registros/fontes/sigtap_grupo09_102026.csv`), e a F do `conferir_ficha.py`
acusa isso nas sete; o pacote permite gerá-lo.

## Normas: o calendário

A vigia rodou em 10/10/2026 e registrou que a Nota Técnica de 10/2026 ainda não tinha saído.
A Nota e o pacote saíram por volta de 15/10, e a próxima rodada é em 10/11. Com a segunda
rodada no dia 22, eles teriam sido lidos em 22/10, no mesmo dia do dossiê. Os pacotes de 06 a
08/2026 foram republicados no FTP em 23/10/2026 e ainda não foram lidos por ninguém.
