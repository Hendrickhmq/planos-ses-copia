# Parâmetros técnicos — origem de cada número

Decididos por mim em 31/08/2026, porque o usuário respondeu "não sei" às perguntas
1, 2, 3, 4 e 8 da rodada 4 e pediu que a redação seguisse. **Cada um está aqui com a
fonte que o sustenta e a alternativa que foi descartada** — é a lista para ele
ajustar no fim.

| # | parâmetro | adotado | fonte / razão | alternativa descartada |
|---|---|---|---|---|
| 1 | classificação do serviço | **tipo II — confirmado pelo usuário em 01/09/2026** — sedação consciente reversível por antagonista | RDC ANVISA 6/2013, art. 4º, II, e art. 3º, XII (paciente responde ao comando verbal). Não aciona o art. 16 (dois profissionais por sala), que só incide sobre sedação profunda ou anestesia não tópica. É o **tipo mínimo** que autoriza registrar o secundário 04.17.01.006-0 — o tipo I não o pratica. Confirmado em segunda opinião no NotebookLM, 01/09/2026 | tipo III (propofol/anestesia): melhor tolerância e recuperação mais curta, mas exige o art. 21 — aparelho de anestesia, capnografia, via aérea difícil — e anestesista por sala |
| 2 | jornada efetiva de sala | **6 horas por dia útil** | jejum de 8h concentra o exame na manhã; 6h efetivas cobrem manhã plena e início da tarde sem exigir agenda vespertina com jejum desde a madrugada | 8h: reduziria as salas de 2 para 1 por polo, mas a 100% de ocupação, sem folga para intercorrência |
| 3 | intervalo de sala por paciente | **25 minutos** | SPED, parecer de 09/10/2020: EDA de 15 a 20 minutos; a *British Society of Gastroenterology* recomenda intervalo mínimo de 20 minutos. Somam-se entrada, sedação, saída e higienização | 20 min: no limite da recomendação, sem margem |
| 4 | permanência em recuperação | **45 minutos** | tese USP de Marcos Eduardo Lera dos Santos (2012): recuperação média de 28,82 min com propofol e mais longa com midazolam. Adotada a faixa alta porque o parâmetro 1 é tipo II | 30 min: só se aplicaria a propofol |
| 5 | dias úteis por mês | **21 dias úteis** | mesmo parâmetro do plano anterior | — |
| 6 | prazo do laudo de anatomia patológica | **até 15 dias corridos**, pactuado — e só para os casos com biópsia, porque o exame é **opcional** na OCI (NT 3/2025) | é o que cabe na janela do parâmetro 7 no pior caso: exame no último dia da competência exige conclusão até o fim da seguinte, ou seja, ~30 dias | 20 ou 30 dias: estoura a janela e a OCI não conclui |
| 7 | janela de conclusão da OCI | **2 competências** | **atributo complementar 054 — "APAC com validade fixa de 2 competências"**. Portaria SAES/MS 1.640/2024, art. 15, §§1º e 2º; Manual PMAE, item 4.3. Manual: início em 23/01 ⇒ fim no máximo em 28/02 | não é escolha — é regra |
| 8 | número de polos | **3 — Ceilândia, Sobradinho e Gama** | decisão do usuário, 01/09/2026. As sete Regiões de Saúde agrupadas em três territórios | 4 polos: cobertura mais fina, mas o mesmo apoio central |
| 9 | forma do retorno | **teleconsulta** (03.01.01.030-7) | decisão do usuário. Manual PMAE: é obrigatório registrar em toda APAC de OCI a consulta **ou** a teleconsulta; NT 1/2025, item 2.1.10: é a única exceção em que o sistema admite marcação individualizada; a descrição vigente da OCI diz "consulta **ou** teleconsulta de retorno" | consulta presencial: dobraria recepção e sala de espera |
| 11 | antecedência da confirmação ativa | **48 horas** antes do exame | é o último momento em que a ausência de acompanhante ainda se corrige sem perder a vaga: dá um dia útil para o usuário providenciar quem o acompanhe, e à agenda tempo de reofertar se ele desistir | 24 h: não sobra dia útil para corrigir |
| 12 | giro do endoscópio | **70 minutos** por uso — 25 na sala (parâmetro 3) e 45 no processamento | soma dos dois tempos já adotados; é o que define o parque de aparelhos por polo | — |
| 13 | escalonamento do laudo em atraso | alerta no **10º dia**, escalonamento à coordenação no **13º** | dentro do prazo de 15 dias do parâmetro 6, com dois pontos de reação antes do vencimento | alerta só no vencimento: não sobra tempo de reagir |
| 10 | encerramento da produção | **mês 9** | decisão do usuário, e o parâmetro 7 a confirma: a produção do mês 9 conclui dentro do mês 10, último da vigência | produção até o mês 10: os retornos cairiam fora da vigência |

## Dimensionamento derivado — regime pleno, 3 polos

Regime pleno = 1.592 OCI/mês = **75,81 por dia útil**, rateadas pela participação de
cada território na fila do Mapa Social (01/09/2026).

| | Ceilândia | Sobradinho | Gama |
|---|---|---|---|
| Regiões de Saúde | Oeste e Sudoeste | Norte, Leste e Central | Sul e Centro-Sul |
| solicitações na fila | 11.456 | 11.482 | 6.590 |
| participação | 38,80% | 38,89% | 22,32% |
| **OCI no convênio** | **5.031** | **5.042** | **2.894** |
| entradas por dia útil | 29,19 | 29,29 | 16,81 |
| salas (6h × 25 min = 14,4/sala/dia) | **3** (68%) | **3** (68%) | **2** (58%) |
| chegadas por hora | 4,87 | 4,88 | 2,80 |
| postos de recuperação (45 min) | **4** | **4** | **3** |
| lugares na espera (2,5 h, com acompanhante) | **30** | **30** | **20** |
| endoscópios (70 min indisponível por uso: 25 de sala + 45 de processamento) | **6** | **6** | **4** |

Totais: **8 salas, 11 postos de recuperação, 80 lugares de espera, 16 endoscópios.**

A ocupação de 59% a 68% das salas não é folga desperdiçada: é a margem que absorve
falta, intercorrência, exame que se estende e o ciclo de processamento.

**A planilha não muda com o número de polos.** Todo o apoio custeado pelo convênio é
central — gestão, agendamento, registro de APAC, rastreamento de laudo, financeiro e
os meios tecnológicos. O que varia com o número de polos é a capacidade instalada
exigida do executor, que está dentro do valor unitário.

## O que a janela de 2 competências obriga

É o parâmetro mais duro do plano, e ele não vem de nós.

1. **A APAC abre na data do primeiro procedimento** e fecha na data do último
   (art. 15, §§1º e 2º da Portaria 1.640/2024). O último é o retorno.
2. **Se a OCI não concluir no prazo, a APAC é rejeitada** e os atos só podem ser
   apresentados avulsos, em BPA-I, fora da OCI (Manual PMAE).
3. Logo: **o agendamento tem de privilegiar a primeira quinzena da competência**, e
   o laudo de anatomia patológica tem de estar contratado com prazo que caiba na
   janela. São as duas regras operacionais que nascem daqui, e ambas vão ao fluxo.
4. Motivos de saída admitidos na APAC (art. 15, §3º): 1.1 Alta Curado, 1.2 Alta
   Melhorado, 1.4 Alta a pedido, 1.5 Alta com previsão de retorno, 4.1 a 4.3 Óbito.
