# Mapa Social da Saúde — fila das três OCIs de otorrinolaringologia, recarga de 08/10/2026 21:32

Coleta piloto do agente `mapa-social` para o pré-plano geral (`plano_v1_geral.md`): OCIs
09.04.01.001-5, 09.04.01.002-3 e 09.04.01.003-1. Mesmas filas e mesmo enquadramento de
`../fila.md` (base de 08/10/2026 07:32) e de
`registros/fontes/mapa_social_oci_otorrino_20261007.md` (base de 07/10/2026 19:32).
Planilha em `mapa_social_20261008.xlsx`; JSON do motor e script em
`mapa_social_20261008_bruto/`.

| campo | conteúdo |
|---|---|
| Fonte | Mapa Social da Saúde – Regulamentação (MPDFT) · Lista de Espera – Exames e Consultas · `https://paineis-ext.mpdft.mp.br/extensions/mapasauderegulamentacao/mapasauderegulamentacao.html` · app Qlik `7edb02fa-f1f5-4ea6-b348-049a4ac2d095` · dados SISREG/DATASUS |
| Última recarga da base | 08/10/2026 21:32:58 (qLastReloadTime 2026-10-09T00:32:58Z) |
| Consulta | 08/10/2026 23:10 (relógio do motor) |
| Solicitação mais recente na base | 02/10/2026 (na base de 08/10 07:32 era 01/10/2026) |
| Medida | **fila** = os três status: pendente de regulação, corrigida e reenviada para regulação, pendente de regulação por fila de espera. Devolvidas para complementação ficam fora e são contadas à parte |
| Recorte | todos os anos; cada fila fixa na expressão de conjunto; OCI pelo CID da solicitação (`codigo_cid_solicitado`) contra a ficha do SIGTAP: H60–H95 para 001-5 e 002-3, J30–J39 para 003-1 |
| Via | Qlik Engine API do próprio painel (evaluateEx e hipercubos de sessão), no navegador embutido |

---

## 1. Fila por OCI

Pessoas = CNS distintos no conjunto (quem espera por mais de um exame conta uma vez).
Espera em dias, calculada no motor sobre os registros do conjunto.

| conjunto | CID | fila | **pessoas** | devolvidas | espera média | mediana | idade mediana | solicitada em 2026 |
|---|---|---|---|---|---|---|---|---|
| **001-5** — audiometria (3 filas) | H60–H95 | 4.276 | **4.276** | 2.047 | 120 | 92 | 53 | 3.979 |
| **002-3** — BERA (2 filas) | H60–H95 | 1.812 | **1.812** | 1.467 | 457 | 444 | 10 | 574 |
| auditivas — exames (001-5 + 002-3) | H60–H95 | 6.088 | 5.951 | 3.514 | 220 | 119 | 47 | 4.553 |
| auditivas — consultas (saúde auditiva + otorrino geral) | H60–H95 | 7.521 | 7.481 | 1.957 | 352 | 225 | 60 | 3.383 |
| auditivas — exames + consultas | H60–H95 | 13.609 | 12.849 | 5.471 | 301 | 150 | 57 | 7.936 |
| **003-1** — videoendoscopias e videolaringoscopia (3 filas) | J30–J39 | 3.478 | **3.459** | 150 | 520 | 532 | 9 | 1.033 |
| 003-1 — consulta otorrino geral | J30–J39 | 1.988 | 1.988 | 530 | 149 | 80 | 18 | 1.664 |
| 003-1 — exames + consulta | J30–J39 | 5.466 | 5.402 | 680 | 322 | 168 | 11 | 2.697 |
| **as três OCIs — exames** | | **9.566** | **9.143** | | 329 | 159 | | |
| as três OCIs — exames + consultas | | 19.075 | 17.955 | | | | | |

Sobreposição: 137 pessoas esperam audiometria e BERA ao mesmo tempo; 296 estão nas duas
famílias (auditiva e nasofaringe, exames + consultas).

## 2. Fila a fila

| OCI | fila no SISREG (nome interno) | SIGTAP da fila | fila sem recorte | **com o CID** | pessoas | devolvidas (CID) | espera média | mediana | idade | mais antiga |
|---|---|---|---|---|---|---|---|---|---|---|
| 001-5 | AUDIOMETRIA E IMITANCIOMETRIA – ATÉ 7 ANOS | 02.11.07.003-3 | 3.533 | **755** | 755 | 821 | 270 | 177 | 0–8 (med. 5) | 02/05/2024 |
| 001-5 | AUDIOMETRIA E IMITANCIOMETRIA – 8 A 64 ANOS | 02.11.07.003-3 | 2.806 | **2.255** | 2.255 | 661 | 85 | 84 | 8–65 (med. 48) | 25/02/2026 |
| 001-5 | AUDIOMETRIA E IMITANCIOMETRIA – ACIMA DE 65 ANOS | 02.11.07.003-3 | 1.339 | **1.266** | 1.266 | 565 | 91 | 92 | 65–90 (med. 73) | 08/04/2026 |
| 002-3 | POTENCIAL EVOCADO AUDITIVO BERA – ATÉ 4 ANOS | 02.11.05.011-3 | 2.289 | **687** | 687 | 1.073 | 433 | 415 | 0–4 (med. 2) | 09/02/2024 |
| 002-3 | POTENCIAL EVOCADO AUDITIVO BERA – ACIMA DE 5 ANOS | 02.11.05.011-3 | 2.272 | **1.125** | 1.125 | 394 | 472 | 470 | 5–90 (med. 47) | 05/02/2024 |
| consulta H | CONSULTA EM ATENCAO A SAUDE AUDITIVA - MEDIA E ALTA COMPLEXIDADE | 03.01.01.007-2 | 5.584 | **5.563** | 5.559 | 708 | 512 | 493 | 0–90 (med. 65) | 31/10/2023 |
| consulta H | CONSULTA EM OTORRINOLARINGOLOGIA - GERAL | 03.01.01.007-2 | 5.226 | **1.958** | 1.956 | 1.249 | 125 | 66 | 0–90 (med. 53) | 10/06/2021 |
| 003-1 | VIDEOENDOSCOPIA␣␣NASAL␣␣FLEXIVEL | 02.09.04.004-1 | 3.511 | **2.931** | 2.925 | 0 | 580 | 616 | 0–14 (med. 8) | 20/11/2023 |
| 003-1 | VIDEOENDOSCOPIA NASAL RIGIDA | 02.09.04.004-1 | 658 | **487** | 487 | 80 | 209 | 49 | 12–88 (med. 20) | 29/01/2024 |
| 003-1 | VIDEOLARINGOSCOPIA | 02.09.04.004-1 | 296 | **60** | 60 | 70 | 103 | 43 | 1–85 (med. 28) | 29/07/2025 |
| consulta J | CONSULTA EM OTORRINOLARINGOLOGIA - GERAL | 03.01.01.007-2 | 5.226 | **1.988** | 1.988 | 530 | 149 | 80 | 0–88 (med. 18) | 27/06/2023 |

␣␣ = dois espaços comuns no nome interno (sem acento em "FLEXIVEL"). Códigos SIGTAP como
o SISREG registra a fila: 02.11.07.003-3 é audiometria em campo livre, 02.11.05.011-3 é
potencial evocado auditivo, 02.09.04.004-1 é videolaringoscopia.

O que fica fora do CID (aba 8): na audiometria até 7 anos, F80 (1.167) e F84 (713); no
BERA até 4 anos, F80 (469), F84 (287) e P07 (257); na videolaringoscopia, R49 (89), K21
e R13; na videoendoscopia flexível, R06 e R04.

## 3. Por Região de Saúde — medida fila, pessoas

Região de Saúde da unidade solicitante. A linha sem região fica à parte, sem rateio. As
linhas não somam o total de pessoas: quem tem solicitação vinda de duas regiões conta nas
duas.

| Região | 001-5 exames | 002-3 exames | auditivas consultas | 003-1 exames | 003-1 consulta | 003-1 exames + consulta |
|---|---|---|---|---|---|---|
| Central | 326 | 139 | 530 | 177 | 237 | 412 |
| Centro-Sul | 390 | 88 | 761 | 530 | 190 | 717 |
| Leste | 233 | 75 | 399 | 155 | 288 | 436 |
| Norte | 466 | 111 | 400 | 506 | 130 | 632 |
| Oeste | 590 | 248 | 1.047 | 152 | 296 | 448 |
| Sudoeste | 1.061 | 360 | 1.742 | 955 | 504 | 1.447 |
| Sul | 306 | 113 | 934 | 111 | 297 | 406 |
| URD | 781 | 293 | 1.173 | 754 | 0 | 754 |
| Contratado/Credenciado | 45 | 376 | 456 | 119 | 0 | 119 |
| Público – Não SES | 0 | 0 | 1 | 0 | 0 | 0 |
| **sem região informada** | **78** | **9** | **47** | **3** | **46** | **48** |

URD e Contratado/Credenciado não são Região de Saúde: são unidades de referência e
prestadores que solicitam direto. No BERA, o contratado é a maior origem (376 de 1.812).
A fila em solicitações está na aba 3 da planilha.

## 4. Idade — CALCULADO (faixas somadas das idades do motor, medida fila)

| faixa | 001-5 exames | 002-3 exames | auditivas consultas | 003-1 exames | 003-1 consulta |
|---|---|---|---|---|---|
| 0–4 | 329 | 687 | 180 | 431 | 231 |
| 5–9 | 544 | 207 | 94 | 1.600 | 369 |
| 10–14 | 190 | 146 | 143 | 1.113 | 256 |
| 15–19 | 90 | 36 | 114 | 54 | 173 |
| 20–39 | 361 | 101 | 668 | 130 | 503 |
| 40–59 | 1.095 | 275 | 2.156 | 103 | 341 |
| 60–64 | 399 | 93 | 832 | 14 | 50 |
| 65 ou mais | 1.268 | 267 | 3.334 | 33 | 65 |

A 003-1 é pediátrica: 3.144 das 3.478 solicitações de exame (90%) são de 0 a 14 anos.

## 5. Entrantes — CALCULADO (abertas + agendadas, por mês da solicitação)

| | 001-5 exames | 002-3 exames | auditivas consultas | 003-1 exames | 003-1 consulta |
|---|---|---|---|---|---|
| 2025, doze meses | 11.430 | 1.049 | 10.332 | 3.412 | 4.964 |
| 2025, por mês | 953 | 87 | 861 | 284 | 414 |
| 2026, jan–set | 8.160 | 634 | 7.754 | 2.437 | 3.688 |
| 2026, por mês | 907 | 70 | 862 | 271 | 410 |

Piso: solicitação cancelada antes de agendar não consta. Mês a mês nas abas 6 e 7.

**Sinal a conferir antes de usar:** as agendadas com solicitação a partir de abril/2026
caem a zero no BERA (0 por mês desde abril) e despencam na audiometria (de ~900 por mês
para 295 em maio e 120–150 de junho a setembro), enquanto as abertas da audiometria sobem para 600–800 por mês. As filas de
audiometria de 8 a 64 e acima de 65 só têm solicitações de 2026 (a mais antiga é de
25/02 e 08/04/2026). Parece fila recriada e oferta parada, não queda de demanda.

## 6. Filas com CID compatível que ficam fora da soma

| fila | CID | fila | motivo |
|---|---|---|---|
| CONSULTA EM OTONEUROLOGIA | H60–H95 | 85 | vertigem; fora no enquadramento de 07/10 |
| TESTES DE PROCESSAMENTO AUDITIVO | H60–H95 | 178 | não faz parte de nenhuma das OCIs (07/10) |
| VIDEOENDOSCOPIA DA DEGLUTICAO  ( VED) | J30–J39 | 11 | disfagia; fora no enquadramento de 07/10 |
| CONSULTA PARA RESPIRADOR BUCAL | J30–J39 | 722 | **não estava no enquadramento de 07/10**; idade mediana 7, espera 206 dias |
| CONSULTA EM  RINOLOGIA | J30–J39 | 131 | **não estava no enquadramento de 07/10**; fila só de 2026 |

As duas últimas são filas de consulta com o CID da ficha da 003-1 que as coletas anteriores
não listaram. Ficam fora até a conversa principal decidir; somadas, seriam mais 853
solicitações de consulta na 003-1.

## 7. Diferença para as coletas anteriores — CALCULADO

| | 07/10 19:32 | 08/10 07:32 | **08/10 21:32** | Δ no dia |
|---|---|---|---|---|
| 003-1 exames — pessoas | 3.493 | 3.477 | **3.459** | −18 |
| · videoendoscopia flexível — fila | 2.933 | 2.930 | 2.931 | +1 |
| · videoendoscopia rígida — fila | 520 | 507 | **487** | **−20** |
| · videolaringoscopia — fila | 60 | 60 | 60 | 0 |
| 003-1 consulta — pessoas | 1.981 | 1.983 | 1.988 | +5 |
| 003-1 exames + consulta — pessoas | 5.430 | 5.416 | 5.402 | −14 |
| 001-5 exames — pessoas | 4.234 | 4.255 | 4.276 | +21 |
| 002-3 exames — pessoas | — | 1.810 | 1.812 | +2 |
| auditivas consultas — pessoas | 7.472 | 7.468 | 7.481 | +13 |
| espera média 003-1 exames | 517 | 518 | 520 | +2 |

A base andou um dia de solicitações (de 01/10 para 02/10). A única mudança fora do ruído é
a videoendoscopia rígida, 20 solicitações a menos em 14 horas (de 507 para 487); o painel
não diz se foram agendadas ou devolvidas. Por região, a 003-1 mexe no máximo 10 pessoas
(URD). **A meta de 3.504 OCIs continua acima das pessoas nas filas de exame da 003-1
(3.459)**, agora com 45 de folga (eram 27).

## 8. Lacunas

- **Motivo da queda da videoendoscopia rígida:** o painel não guarda o histórico de status
  da solicitação; só a comparação entre coletas mostra a saída.
- **Laringoscopia (02.09.04.002-5):** não há fila com esse nome nem esse código no SISREG.
- **Devolvidas na videoendoscopia flexível:** zero, com e sem recorte de CID. É o que o
  motor responde; não há como saber se a fila não devolve ou se não registra devolução.
- **Idade:** é a idade na solicitação (`idade_solicitacao`), não a de hoje.
