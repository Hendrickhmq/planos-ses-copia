# Fila das OCIs de otorrinolaringologia — enquadramento e números

Coleta de 07/10/2026 no Mapa Social da Saúde (MPDFT), pela Qlik Engine API do painel.
Base recarregada em 07/10/2026 19:32; solicitações até 01/10/2026. Medida **fila**: os
três status de fila do SISREG (pendente de regulação, corrigida e reenviada, pendente por
fila de espera); devolvidas fora. Todos os anos.

OCIs: **09.04.01.001-5** Avaliação inicial diagnóstica de déficit auditivo e
**09.04.01.003-1** Avaliação diagnóstica de nasofaringe e de orofaringe.

---

## 1. O que a ficha do SIGTAP diz (competência 09/2026)

| | 09.04.01.001-5 — déficit auditivo | 09.04.01.003-1 — nasofaringe e orofaringe |
|---|---|---|
| Composição | consulta médica especializada, audiometria tonal e vocal, imitanciometria | consulta médica especializada, videolaringoscopia **ou** laringoscopia |
| Atributo | — | "Exige procedimento de Videolaringoscopia ou Laringoscopia" |
| Idade | 0 meses a 130 anos | 0 meses a 130 anos |
| CID principal | **H60 a H95** (todo o capítulo de doenças do ouvido) | **J30 a J39** (vias aéreas superiores) |
| Serviço Ambulatorial | R$ 100,00 | R$ 393,55 |
| Financiamento | FAEC, Agora Tem Especialistas — Componente Ambulatorial | idem |

Composição confirmada também nas NT 1/2025 e 3/2025 (`extraidos_normas/`).

## 2. Não existe fila com o código da OCI

Nenhum nome de fila do SISREG carrega código 09.04. A demanda está em filas de
consulta e de exame, e o **critério de enquadramento é o CID da solicitação** contra a
lista de CID da ficha.

## 3. O enquadramento, fila a fila

### Déficit auditivo (CID H60–H95)

| fila no SISREG | código no SISREG | fila total | **com CID H60–H95** | | |
|---|---|---|---|---|---|
| AUDIOMETRIA E IMITANCIOMETRIA – ATÉ 7 ANOS | 02.11.07.003-3 | 3.524 | **749** | 21% | o resto é F80/F84 (fala, autismo) |
| AUDIOMETRIA E IMITANCIOMETRIA – 8 A 64 ANOS | 02.11.07.003-3 | 2.781 | **2.233** | 80% | resto: R42 tontura, F81/F90 |
| AUDIOMETRIA E IMITANCIOMETRIA – ACIMA DE 65 ANOS | 02.11.07.003-3 | 1.325 | **1.252** | 94% | |
| CONSULTA EM ATENÇÃO À SAÚDE AUDITIVA – MÉDIA E ALTA COMPLEXIDADE | 03.01.01.007-2 | 5.573 | **5.552** | 99,6% | porta da saúde auditiva (AASI) |
| CONSULTA EM OTORRINOLARINGOLOGIA – GERAL | 03.01.01.007-2 | 5.213 | **1.960** | 38% | a mesma fila tem 1.981 J30–J39 |
| *CONSULTA EM OTONEUROLOGIA* | 03.01.01.007-2 | 225 | *85* | | vertigem; fora da soma |

**As filas de audiometria são registradas como 02.11.07.003-3, audiometria em campo
livre**, e não como 02.11.07.004-1, audiometria tonal limiar, que é o exame da OCI. O
nome da fila ("audiometria e imitanciometria") descreve o conjunto da OCI; o código é
outro.

As filas de 8 a 64 anos e acima de 65 só têm solicitações de 2026, com espera de 85 a
91 dias — parecem filas recriadas este ano.

### Nasofaringe e orofaringe (CID J30–J39)

| fila no SISREG | código no SISREG | fila total | **com CID J30–J39** | | |
|---|---|---|---|---|---|
| VIDEOENDOSCOPIA NASAL FLEXÍVEL | 02.09.04.004-1 | 3.514 | **2.933** | 83% | 0 a 14 anos — adenoide |
| VIDEOENDOSCOPIA NASAL RÍGIDA | 02.09.04.004-1 | 697 | **520** | 75% | a partir de 12 anos |
| VIDEOLARINGOSCOPIA | 02.09.04.004-1 | 292 | **60** | 21% | resto: R49 voz, K21 refluxo, R13 disfagia |
| CONSULTA EM OTORRINOLARINGOLOGIA – GERAL | 03.01.01.007-2 | 5.213 | **1.981** | 38% | |
| *VIDEOENDOSCOPIA DA DEGLUTIÇÃO (VED)* | 02.09.04.004-1 | 208 | *11* | | disfagia (R13); fora |

Não há fila de laringoscopia (02.09.04.002-5).

### Fora das duas OCIs

BERA até 4 anos (2.300) e acima de 5 anos (2.271) são da OCI de **progressão**
(09.04.01.002-3). Testes de processamento auditivo (464) não fazem parte de nenhuma.

## 4. Os números de cada OCI

Pessoas = CNS distintos; quem está em mais de uma fila conta uma vez.

| | solicitações | **pessoas** | espera média | mediana | idade mediana | solicitadas em 2026 |
|---|---|---|---|---|---|---|
| **Déficit auditivo — exames** | 4.234 | 4.234 | 120 | 92 | 53 | 3.937 |
| déficit auditivo — consultas | 7.512 | 7.472 | 352 | 224 | 60 | 3.375 |
| **Déficit auditivo — exames + consultas** | 11.746 | **11.329** | 280 | 135 | 58 | 7.312 |
| **Nasofaringe — exames** | 3.513 | 3.493 | 517 | 527 | 9 | 1.052 |
| nasofaringe — consulta | 1.981 | 1.981 | 148 | 79 | 18 | 1.657 |
| **Nasofaringe — exames + consulta** | 5.494 | **5.430** | 322 | 168 | 11 | 2.709 |
| **as duas OCIs** | | **16.506** | | | | |

Sobreposição: 377 pessoas estão ao mesmo tempo numa fila de exame e numa de consulta
do déficit auditivo; 44 na nasofaringe; 253 aparecem nas duas OCIs.

A nasofaringe é **pediátrica**: idade mediana de 9 anos nos exames, e a fila de
videoendoscopia flexível espera 580 dias em média.

## 5. Por Região de Saúde

| Região | déficit auditivo — pessoas (exames + consultas) | nasofaringe — pessoas (exames + consulta) |
|---|---|---|
| Central | 813 | 412 |
| Centro-Sul | 1.129 | 716 |
| Leste | 603 | 435 |
| Norte | 828 | 631 |
| Oeste | 1.609 | 449 |
| Sudoeste | 2.695 | 1.451 |
| Sul | 1.202 | 411 |
| URD | 1.881 | 772 |
| Contratado/Credenciado | 494 | 121 |
| sem região | 123 | 48 |

As linhas não somam o total de pessoas: quem tem solicitação vinda de duas regiões
conta nas duas.

## 6. Decisões em aberto

1. **Qual cenário vira demanda:** só as filas de exame (4.234 e 3.493 pessoas) ou exame +
   consulta (11.329 e 5.430). A consulta geral de otorrino só entra pela parte com CID
   compatível.
2. **A consulta de saúde auditiva** (5.552) é a porta do aparelho auditivo. Entra na OCI
   de diagnóstico ou fica com o serviço de saúde auditiva?
3. **Audiometria até 7 anos fora do CID** (2.775 solicitações, a maioria F80/F84): a ficha
   não aceita, mesmo sendo pedido clássico de avaliação auditiva na criança com atraso de
   fala.
4. **Audiometria em campo livre × tonal limiar:** o código que a SES-DF registra não é o
   da composição da OCI.

---

## 7. Valor das duas OCIs e as portarias que mexeram nelas

Histórico de alterações do SIGTAP, lido em 07/10/2026, com a ficha conferida antes e
depois de cada portaria.

| competência | portaria | déficit auditivo (09.04.01.001-5) | nasofaringe e orofaringe (09.04.01.003-1) |
|---|---|---|---|
| 07/2024 | SAES 1.825, de 11/06/2024 — inclui as OCIs | R$ 100,00 | R$ 200,00 — consulta + videolaringoscopia **e** laringoscopia |
| 04/2025 | SAES 2.723, de 31/03/2025 | CPF obrigatório | CPF obrigatório |
| 09/2025 | SAES 3.199 e 3.200, de 02/09/2025 | atributos de Modalidade 2 e 3 (equipes volantes, unidades móveis) | idem |
| 04/2026 | SAES 3.958, de 20/03/2026 | sai a "APAC com validade fixa de 2 competências" | idem |
| **09/2026** | **SAES 4.795, de 26/08/2026** | — não alterada | **R$ 393,55 (+96,8%)**; videolaringoscopia **ou** laringoscopia; atributo "Exige procedimento de Videolaringoscopia ou Laringoscopia" |

**A OCI de déficit auditivo está em R$ 100,00 desde a criação.** Nenhuma portaria lhe deu
incremento.

**Os atributos de Modalidade 2 e 3 não são incremento.** A SAES 3.200/2025 só os usa para
permitir o registro por equipes volantes e unidades móveis; a complementação federal ao
valor da tabela (art. 23) vale para procedimentos cirúrgicos.

### A Portaria SAES/MS nº 4.795, de 26/08/2026

Publicada em **edição extra** do DOU — 31/08/2026, Edição 164-C, Seção 1 – Extra C, p. 4 —,
por isso não consta da legislação diária do Conasems. Íntegra em
`portaria_saes_4795_2026/portaria_saes_4795_2026_dou.html` (página do gov.br) e conferida
na Nota Técnica CGSI nº 09/2026, de 25/08/2026, que lista as alterações da competência
09/2026 (`notas_tecnicas_cgsi/nota_tecnica_cgsi_sigtap_2026_09.pdf`). Assina Mozart
Julio Tabosa Sales.

- Art. 1º cria o atributo **072 — Exige procedimento de Videolaringoscopia ou
  Laringoscopia**: a APAC tem de registrar um dos dois.
- Art. 2º e Anexo I **revalorizam onze OCIs**. Art. 3º e Anexo II trocam a compatibilidade da
  videolaringoscopia e da laringoscopia de "obrigatória" para "compatível" na OCI de
  nasofaringe.

| OCI | 08/2026 | 09/2026 | |
|---|---|---|---|
| 09.04.01.002-3 Progressão da avaliação de déficit auditivo | R$ 150,00 | **R$ 471,57** | +214% |
| 09.06.01.001-2 e 002-0 GIN1 saúde da mulher I e II | R$ 88,40 | R$ 199,95 | +126% |
| 09.02.01.005-0 Síndrome coronariana crônica II | R$ 840,00 | R$ 1.879,80 | +124% |
| 09.04.01.003-1 Nasofaringe e orofaringe | R$ 200,00 | **R$ 393,55** | +97% |
| 09.03.01.003-8 Ortopedia com radiologia e TC | R$ 230,00 | R$ 417,15 | +81% |
| 09.01.01.001-4 Câncer de mama, inicial | R$ 125,00 | R$ 222,45 | +78% |
| 09.03.01.004-6 Ortopedia com radiologia e RM | R$ 360,00 | R$ 616,76 | +71% |
| 09.06.01.005-5 GIN3 endometriose profunda | R$ 372,49 | R$ 599,88 | +61% |
| 09.03.01.002-0 Ortopedia com radiologia e US | R$ 140,00 | R$ 216,83 | +55% |
| 09.01.01.004-9 Câncer de próstata, progressão | R$ 300,00 | R$ 443,54 | +48% |

**A 09.04.01.001-5, avaliação inicial de déficit auditivo, não está no Anexo I.** Segue em
R$ 100,00. A OCI de progressão, que é a continuação dela (BERA), triplicou.

O incremento não é percentual sobre a tabela, como o da Portaria SAES 4.282/2026 para a
imagem: é novo valor do Serviço Ambulatorial da OCI, válido para todo o SUS.
