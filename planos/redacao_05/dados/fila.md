# A fila — Mapa Social da Saúde, base recarregada em 08/10/2026 07:32

Solicitações até 01/10/2026. Medida **fila**: os três status (pendente de regulação,
corrigida e reenviada, pendente por fila de espera); devolvidas fora. Enquadramento
pelo CID da solicitação contra a lista da ficha (J30–J39). Coleta pela Qlik Engine
API do painel. Filas que ficaram de fora e a coleta de 07/10 em
`registros/fontes/mapa_social_oci_otorrino_20261007.md`.

**É esta a base do plano.md** — todos os números do documento saem daqui.

## Filas que entram

| fila no SISREG | código no SISREG | com CID J30–J39 | pessoas | espera média | mediana | idade | de 2026 |
|---|---|---|---|---|---|---|---|
| VIDEOENDOSCOPIA NASAL FLEXÍVEL | 02.09.04.004-1 | 2.930 | 2.924 | 580 dias | 616 | 0–14 (mediana 8) | 635 |
| VIDEOENDOSCOPIA NASAL RÍGIDA | 02.09.04.004-1 | 507 | 506 | 212 dias | 51 | 12–88 (mediana 20) | 357 |
| VIDEOLARINGOSCOPIA | 02.09.04.004-1 | 60 | 60 | 102 dias | 43 | 1–85 (mediana 28) | 52 |
| **filas de exame** | | **3.497** | **3.477** | **518 dias** | 531 | mediana 9 | 1.044 |
| CONSULTA EM OTORRINOLARINGOLOGIA – GERAL | 03.01.01.007-2 | 1.983 | 1.983 | 149 dias | 80 | mediana 18 | 1.659 |
| **exames + consulta** | | 5.480 | 5.416 | 322 dias | 168 | mediana 11 | 2.703 |

A fibroscopia flexível é 83,8% das solicitações de exame (2.930 de 3.497); o pré-plano arredonda para 84%.

**Meta de 3.504 OCIs ≥ 3.477 pessoas nas filas de exame** — zera a fila da data da
consulta, com 27 OCIs a mais.

## Filas mapeadas, fora do objeto

Achadas pela varredura da coleta de 08/10/2026 (base das 21:32,
`fontes/mapa_social_20261008.md`): filas de consulta com o CID da ficha da 003-1
(J30–J39) que as coletas anteriores não listavam. **Ficam mapeadas e fora do objeto**,
por decisão do usuário em 09/10/2026: não entram na soma, na meta nem no documento.

| fila no SISREG | código no SISREG | com CID J30–J39 | pessoas | devolvidas | espera média | mediana | idade | de 2026 | pedido mais antigo |
|---|---|---|---|---|---|---|---|---|---|
| CONSULTA PARA RESPIRADOR BUCAL | 03.01.01.007-2 | 722 | 722 | 474 | 206 dias | 180 | 1–61 (mediana 7) | 552 | 27/06/2024 |
| CONSULTA EM RINOLOGIA | 03.01.01.007-2 | 131 | 131 | 252 | 32 dias | 30 | 8–75 (mediana 35) | 131 | 10/02/2026 |

- Sem o recorte de CID, a fila de respirador bucal tem 794 pedidos e a de rinologia, 141:
  a maior parte dos pedidos das duas tem o CID da 003-1.
- A de respirador bucal é infantil, como a videoendoscopia flexível, e espera há mais de
  dois anos. A de rinologia só tem pedidos de 2026: parece fila criada este ano.
- O nome interno da de rinologia tem espaço duplo: "CONSULTA EM␣␣RINOLOGIA". A
  expressão de conjunto usa o texto exato, que está no JSON da coleta.
- Somadas, seriam mais 853 pedidos de consulta na 003-1. Se um dia entrarem, mudam o
  total de "exames + consulta", não o das filas de exame, que é a base da meta.

## Por Região de Saúde — pessoas

| Região | exames + consulta | só exames |
|---|---|---|
| Sudoeste | 1.447 | 958 |
| Centro-Sul | 717 | 530 |
| Norte | 631 | 506 |
| Oeste | 446 | 152 |
| Leste | 437 | 157 |
| Central | 413 | 178 |
| Sul | 410 | 113 |
| URD | 764 | 764 |
| Contratado/Credenciado | 119 | 119 |
| sem região | 48 | 3 |

## As OCIs auditivas — mesma base (08/10/2026 07:32), CID H60–H95

Usadas na versão geral (v1), que traz as três OCIs de otorrino.

| OCI | filas no SISREG | pessoas | espera média | idade mediana |
|---|---|---|---|---|
| 09.04.01.001-5 inicial do déficit auditivo | AUDIOMETRIA E IMITANCIOMETRIA – até 7, 8 a 64 e acima de 65 anos | 4.255 | 120 dias | 53 |
| 09.04.01.002-3 progressão do déficit auditivo | POTENCIAL EVOCADO AUDITIVO BERA – até 4 e acima de 5 anos | 1.810 | 457 dias | 10 |
| (consultas com CID do ouvido) | CONSULTA EM ATENÇÃO À SAÚDE AUDITIVA; CONSULTA EM OTORRINOLARINGOLOGIA – GERAL | 7.468 | 353 dias | 60 |
