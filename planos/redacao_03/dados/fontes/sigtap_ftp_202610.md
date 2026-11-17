# Tabela do SUS 10/2026 — a OCI de câncer gástrico e os componentes

Lido em 21/10/2026 no arquivo oficial da Tabela Unificada, competência 10/2026:
`ftp://ftp2.datasus.gov.br/pub/sistemas/tup/downloads/TabelaUnificada_202610_v2610151110.zip`
(publicado em 15/10/2026). É a fonte que `metodo/coleta/normas.md` indica para a competência.

**Por que o arquivo, e não a ficha na tela.** Em 21/10/2026 o SIGTAP na web não abriu a sessão
(o endereço da ficha voltava ao `inicio.jsp` em branco, e o seletor de competência parava em
05/2026). O arquivo traz os mesmos campos: `tb_procedimento.txt` (valor, idade, quantidade,
financiamento), `rl_procedimento_compativel.txt` (composição da OCI) e
`rl_procedimento_incremento.txt` (incrementos por habilitação). A ficha completa de 08/2026
continua em `sigtap_0901010073_082026.md`; a de 10/2026, pela tela, fica para o agente
`ficha-sigtap` quando o site voltar.

## Valores

| código | nome | Serviço Ambulatorial | idade | qtd. máx. | financiamento |
|---|---|---|---|---|---|
| 09.01.01.007-3 | OCI Avaliação Diagnóstica de Câncer Gástrico | R$ 600,11 | 18 a 130 anos | 1 | FAEC |
| 02.09.01.003-7 | Esofagogastroduodenoscopia | R$ 48,16 | — | 1 | MAC |
| 04.17.01.006-0 | Sedação | R$ 15,15 | — | 1 | MAC |
| 02.03.02.003-0 | Exame anatomopatológico para congelamento/parafina por peça cirúrgica ou por biópsia (exceto colo uterino e mama) | R$ 40,78 | — | 8 | MAC |
| 03.01.01.007-2 | Consulta médica em atenção especializada | R$ 10,00 | — | — | MAC |
| 03.01.01.030-7 | Teleconsulta médica na atenção especializada | R$ 10,00 | — | 1 | MAC |

A OCI segue com o valor da Portaria SAES/MS 4.653/2026 (`valor_unitario.md`): nada mudou de
08/2026 a 10/2026.

## Composição da OCI (APAC principal × APAC secundária)

| secundário | tipo no arquivo | qtd |
|---|---|---|
| 02.09.01.003-7 Esofagogastroduodenoscopia | 5 (na ficha de 08/2026, "Obrigatória") | 1 |
| 04.17.01.006-0 Sedação | 1 ("Compatível") | 1 |
| 02.03.02.003-0 Anatomopatológico | 1 ("Compatível") | 1 |
| 03.01.01.007-2 Consulta em atenção especializada | 1 ("Compatível") | 2 |
| 03.01.01.030-7 Teleconsulta em atenção especializada | 1 ("Compatível") | 2 |

**O anatomopatológico entra uma vez por OCI.** O procedimento admite até 8 avulso, mas na OCI a
quantidade é 1: dois frascos (antro e corpo, no protocolo de Sydney) continuam sendo um
anatomopatológico para o SUS.

## Incrementos

| procedimento | habilitação | incremento | valor com incremento |
|---|---|---|---|
| 02.09.01.003-7 Esofagogastroduodenoscopia | 38.01 PMAE; 38.05 Agora Tem Especialistas, créditos financeiros; 38.06 ressarcimento ao SUS | 627% | R$ 350,12 |
| 04.17.01.006-0 Sedação | 38.01; 38.05; 38.06 | 890% | R$ 149,99 |
| 02.09.01.003-7 Esofagogastroduodenoscopia | 02.03 alta complexidade em obesidade | 107,64% | — |

Os dois de 627% e 890% vêm da Portaria SAES/MS 4.282/2026, Anexo I (créditos financeiros,
`SAES 4282-2026 incremento creditos financeiros.pdf`, nesta pasta). Valem para o
estabelecimento habilitado, avulsos, não dentro da OCI deste convênio.
