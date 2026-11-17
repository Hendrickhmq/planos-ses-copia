# Mapa Social da Saúde — coleta da fila de tomografia

Planilha recebida do usuário em **15/09/2026**, arquivada em
`mapa_social_tomografia_20260915.xlsx`. Substitui a leitura de captura de tela
que este projeto tinha feito no mesmo dia.

| campo | conteúdo |
|---|---|
| Painel | Mapa Social da Saúde — Regulamentação · "Lista de Espera - Exames e Consultas" |
| Endereço | `https://paineis-ext.mpdft.mp.br/extensions/mapasauderegulamentacao/mapasauderegulamentacao.html` |
| Fonte declarada | SISREG/DATASUS |
| Carimbo de atualização | 15/09/2026 13:32:28 |
| Origem dos números | camada de dados do painel (Qlik Engine API), expressões originais dos objetos |
| Recorte | grupos 4 e 5 de tomografia, todos os anos e todos os status |

**Nenhum número foi calculado, arredondado ou completado pela coleta.** É fonte de
primeira ordem, e é o que dá lastro ao que segue.

---

## 1. A medida muda o número, e o painel tem duas

| medida | expressão | o que conta |
|---|---|---|
| **Solicitações** | três status de fila — pendente de regulação, corrigida e reenviada, pendente por fila de espera | **a fila** |
| **Total de Solicitações** | `Count(Distinct contador_solicitacao)`, sem filtro de status | tudo, **inclusive as devolvidas** |

Os cinco cartões do cabeçalho usam a primeira. **Todos os gráficos usam a segunda.**
Daí os dois patamares de número para o mesmo procedimento: a TC de abdômen superior
com contraste aparece como 4.467 no cartão e 9.814 no gráfico, e a diferença é
inteiramente o status DEVOLVIDA — 5.347 solicitações.

**A planilha do objeto está na faixa da fila**, não na dos gráficos: 4.453 contra
4.465 de Pessoas na Fila e 4.467 de Solicitações, medidos em 15/09. A extração do
objeto é de 10/09, e a base se atualiza diariamente.

---

## 2. O código SIGTAP de cada nome interno — resolve a L-002

O painel guarda o campo `codigo_sigtap_solicitacao`. Os cinco procedimentos do objeto:

| nome na fila da SES-DF | SIGTAP |
|---|---|
| 063. TC DO ABDOMEN SUPERIOR ADULTO C/CONTRASTE S/SEDACAO | 02.06.03.001-0 |
| 111. TC DE PELVE OU BACIA ADULTO C/CONTRASTE S/SEDACAO | 02.06.03.003-7 |
| 055. TC DO TORAX ADULTO C/CONTRASTE S/SEDACAO | 02.06.02.003-1 |
| 053. TC DO TORAX ADULTO S/CONTRASTE S/SEDACAO | 02.06.02.003-1 |
| **ANGIOTOMOGRAFIA DAS ARTÉRIAS CORONARIAS ADULTO S/SEDACAO** | **02.06.02.003-1** |

**A SES-DF fatura a angiotomografia de coronárias como tomografia computadorizada de
tórax.** Não é analogia deste plano: é o código que o próprio sistema de regulação
carrega. As 1.397 angiotomografias do objeto passam a integrar a linha do
02.06.02.003-1.

## 3. A fila de tomografia agregada por código SIGTAP

343 nomes internos colapsam em treze códigos da Tabela do SUS.

| SIGTAP | solicitações | participação | nomes internos | |
|---|---|---|---|---|
| 02.06.03.001-0 — abdômen superior | 14.628 | 29,91% | 36 | **no objeto** |
| 02.06.02.003-1 — tórax | 13.720 | 28,06% | 25 | **no objeto** |
| 02.06.03.003-7 — pelve, bacia e abdômen inferior | 10.851 | 22,19% | 22 | **no objeto** |
| 02.06.01.007-9 — crânio | 4.377 | 8,95% | 16 | |
| 02.06.01.005-2 — pescoço | 1.515 | 3,10% | 14 | |
| 02.06.01.004-4 — face e seios da face | 1.061 | 2,17% | 50 | |
| 02.06.01.002-8 — coluna lombo-sacra | 598 | 1,22% | 12 | |
| 02.06.01.001-0 — coluna cervical | 541 | 1,11% | 12 | |
| 02.06.03.002-9 — articulações de membro inferior | 514 | 1,05% | 44 | |
| 02.06.02.002-3 — segmentos apendiculares | 434 | 0,89% | 61 | |
| 02.06.01.003-6 — coluna torácica | 242 | 0,49% | 9 | |
| 02.06.01.006-0 — sela túrcica | 226 | 0,46% | 19 | |
| 02.06.02.001-5 — articulações de membro superior | 194 | 0,40% | 23 | |
| **total** | **48.901** | | **343** | |

**Os três códigos do objeto cobrem 80,2% da fila de tomografia** — 39.199 de 48.901
solicitações.

## 4. Tempo de espera — e a armadilha do cabeçalho

O tempo de espera do cabeçalho **não filtra status**, e por isso a média publicada
inclui as devolvidas, que esperam muito mais.

| recorte | espera da fila | espera de todos os status | espera das devolvidas |
|---|---|---|---|
| Grupos 4 e 5 de tomografia | **181,7 dias** | 791,3 dias | 1.294,4 dias |
| 063. TC abdômen superior c/contraste | 129,5 | 744,9 | 1.242,8 |
| 111. TC pelve c/contraste | 129,9 | 697,9 | 1.260,2 |
| 055. TC tórax c/contraste | 126,4 | 648,4 | 1.453,3 |
| Angiotomografia de coronárias | 272,9 | 298,0 | 541,9 |
| 053. TC tórax s/contraste | 19,1 | 1.413,9 | 1.680,6 |

**O número que o plano usa é o da fila.** A espera máxima da fila chega a 1.009 dias.

## 5. Classificação de risco — os cinco procedimentos do objeto

| classificação | solicitações | participação |
|---|---|---|
| Prioridade 1 | 11.944 | 45,18% |
| Prioridade 2 | 13.440 | 50,84% |
| Prioridade 3 | 597 | 2,26% |
| Prioridade 4 | 455 | 1,72% |
| **total** | **26.436** | |

**Prioridade 4 existe na base e a rosca do painel não a mostra.**

## 6. Região de Saúde — os cinco procedimentos do objeto

| polo | Regiões de Saúde | solicitações | participação |
|---|---|---|---|
| Ceilândia | Oeste e Sudoeste | 6.285 | **42,58%** |
| Sobradinho | Norte, Leste e Central | 5.350 | **36,24%** |
| Gama | Sul e Centro-Sul | 3.127 | **21,18%** |
| **base territorial** | | **14.762** | |

Fora do território, **11.674 solicitações — 44,2% do universo**: URD 7.701,
Contratado/Credenciado 3.443, sem região informada 528, Serviços Centralizados 1 e
Público — Não SES 1.

**Este rateio vale para a tomografia**, que é 16% do objeto em exames. O mesmo recorte
para ultrassonografia não foi coletado.

## 7. Os três totais do painel se reconciliam

A coleta desfez a divergência que a leitura de captura tinha apontado. Não são
universos diferentes: **são categorias ocultas na exibição.**

| bloco | total publicado | o que falta | universo |
|---|---|---|---|
| Classificação de risco | 47.555 | Prioridade 4, com 1.346 | 48.901 |
| Região de Saúde | 47.655 | sem região informada, com 1.246 | 48.901 |
| Status | 48.901 | — | 48.901 |

**O universo da fila de tomografia é 48.901 solicitações**, em todos os status e anos.
