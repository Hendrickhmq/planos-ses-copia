# Estudo — a fila de US de articulação (02.05.02.006-2)

**Controle interno.** Estudo de 27/10/2026 para o redacao_07: Emenda de Bancada do DF 71080005,
R$ 1.502.687,00. É o primeiro passo do mapeamento pedido hoje: coletar a US de articulação por
inteiro e depois, no panorama, descartar o que outros planos atendem e o que a SES já dá conta.

**A fonte:** coleta do agente `mapa-social` de 27/10/2026, recarga das 08:33, pelo kit novo
(ramo `melhorias/mapa-social`), conferência 10/10
(`planos/redacao_07/dados/fontes/mapa_social_20261027_articulacao.md`, na sua pasta). As somas
por grupo de filas e por recorte são **calculadas** sobre o JSON da coleta. Os grupos são os da
coleta de 26/10.

## 1. O tamanho

| grupo de filas | fila válida | devolvidos | fila viva | no CID da OCI do IEV | **fora do CID do IEV** | **fora, viva** | agendadas em 12 m | espera média (dias) |
|---|---|---|---|---|---|---|---|---|
| articulações (37 filas) | 9.979 | 3.125 | 7.531 | 781 | **9.195** | **6.974** | 5.599 | 524 |
| partes moles | 3.124 | 1.456 | 1.878 | 70 | **3.053** | **1.837** | 1.427 | 651 |
| região inguinal | 608 | 54 | 524 | 0 | **608** | **524** | 735 | 383 |
| pescoço e região cervical | 279 | 79 | 219 | 0 | **279** | **219** | 199 | 464 |
| outras regiões (16 filas) | 438 | 209 | 281 | 28 | **410** | **274** | 90 | 595 |
| **total, 61 filas** | **14.428** | **4.923** | **10.433** | **879** | **13.545** | **9.828** | **8.050** | **546** |

- **A fila válida já desconta os 4.923 devolvidos.** Há 4 pedidos sem CID, que não entram em
  nenhum recorte.
- **Pessoas:** 11.465 na fila válida e 8.119 na viva. Quem espera por mais de uma articulação
  conta uma vez.
- **A fila viva fora do CID do IEV é de 9.828.** O estudo de ontem estimou 9.761.
- **A fila velha está concentrada em partes moles:** 1.246 de 3.124 pedidos são de antes de
  27/10/2024. Nas articulações, joelho D e E adulto têm 35% de fila velha.

## 2. O rumo

Entrantes são os pedidos novos de cada mês: os abertos, em qualquer situação, mais os que já
foram agendados, pelo mês do pedido (**calculado** pelo montador).

| período | entrantes | por mês |
|---|---|---|
| 10/2024 a 09/2025 | 11.130 | 928 |
| 10/2025 a 09/2026 | 11.450 | 954 |

- **A procura está estável e sobe pouco:** 3% de um ano para o outro, entre 750 e 1.190 por
  mês. O pico foi em 09/2025 (1.191). Nos últimos doze meses, o mês mais alto foi 08/2026 (1.088).
- **A rede agendou 8.050 em 12 meses.** A procura é de uns 11.450 por ano. **Faltam uns
  3.400 por ano, cerca de 280 por mês: a fila cresce.**
- **Nada indica mutirão.** A fila por ano do pedido sobe sempre: 1.657 de 2024, 4.313 de 2025
  e 5.764 de 2026. Mas o kit ainda não mede os agendamentos pelo mês em que aconteceram, e é
  essa série que mostra se houve esforço para baixar a fila e ela voltou a subir. A coluna
  "agendadas" dos entrantes é pelo mês do pedido: cai nos meses recentes porque esses pedidos
  ainda esperam (mediana de 399 dias), não porque a oferta caiu.
- **"Abertas" inclui os devolvidos.** A procura real pode ser um pouco menor.

## 3. Quem espera

- **Região:** Sudoeste 4.272, Centro-Sul 2.825, Leste 2.709, Sul 2.295, Oeste 1.568, Norte
  526, Central 66, sem região 160. Quase nada vem de URD ou contratado: a fila é da atenção
  primária e dos ambulatórios das regiões.
- **Idade:** 76% dos pedidos são de 40 a 79 anos, e a faixa de 50 a 59 é a maior (4.004).
  Há 804 pedidos de crianças de 0 a 9 anos, sobretudo de quadril e coluna.
- **CID:** ombro M75 (2.195), dor articular M25 (1.757), túnel do carpo G56 (1.355), nódulo R22
  (975), tenossinovite M65 (963, a maior parte dentro da OCI), lipoma D17 (716), hérnia inguinal
  K40 (675), M71 (539), M79 (462) e joelho M23 (397).

## 4. Para a conta

| | exames | valor (R$ 99,94) |
|---|---|---|
| toda a fila viva fora do CID do IEV | 9.828 | R$ 982.210,32 |
| toda a fila válida fora do CID do IEV | 13.545 | R$ 1.353.687,30 |

**Atualização do cenário 1 do estudo por aparelho** (só ultrassom, pela fila viva):
- sai a **US de próstata transretal**: a OCI 09.01.01.004-9 (próstata) a tem, e o IEV a executa no
  Fila Zero, com 1.015 OCI;
- ficam oito ultrassons pela fila viva (3.578 exames, R$ 357.626,03) e a articulação fora do CID
  do IEV pela fila viva (9.828, R$ 982.210,32);
- **13.406 exames, R$ 1.339.836,35, e sobram R$ 12.581,95.**

A procura nova da articulação (uns 950 por mês) põe na fila, em 12 meses, mais gente do que a
sobra paga: o fundo de fila contra a falta não acaba.

## 5. A varredura

Pelo nome, o kit achou 67 filas fora das 61 de partida (seção "Varredura das filas" do `.md`).
- Duas são a US pélvica com outro nome: "ECOGRAFIA PELVICA (GINECOLOGICA)", adulto (585) e
  infantil (441). Já estão na carteira, pelo código 02.05.02.016-0.
- O resto é radiografia do mesmo segmento (perna, calcâneo, coxa, braço), com 1 a 7 pedidos
  cada. Não é ultrassom.
- No próprio código da articulação há uma fila "ECOGRAFIA PELVICA" (46 pedidos, todos de 2026).
  É pélvica registrada com o código errado: entra na conta pelo código, mas vale saber.
