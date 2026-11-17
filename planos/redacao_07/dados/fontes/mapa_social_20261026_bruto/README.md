# Mapa Social, 26/10/2026 (recarga 16:32) — dados brutos da coleta

Recoleta do agente `mapa-social` para o redacao_07 (Emenda de Bancada 71080005, ISHP, exames de
imagem avulsos), pelo método de 25/10/2026: varredura das filas de imagem (subgrupos SIGTAP 02.04 a
02.08 e 02.10, e nomes de imagem com outro código), tabela de destaque, mamografia por nome e CID,
e diferença para 15/10/2026. Saída da Qlik Engine API do painel. Só contagens agregadas: nenhum
CNS, CPF, nome ou data de nascimento.

| arquivo | o que é |
|---|---|
| `motor_filas_20261026.txt` | o texto do motor: uma linha por fila (nome × código) com gente esperando, 684 linhas |
| `motor_codigos_20261026.txt` | o texto do motor: uma linha por código do universo, com fila ou agendamento |
| `motor_agregados_20261026.txt` | o texto do motor: recortes por nome (G), Região de Saúde por recorte (GR) e por código (CR), idade (ID), CID da mamografia (MC), união da carteira (CA), filas fora dos subgrupos (FO), fila por ano (ANO), totais (TOT), nomes só na tabela de agendamentos (AO) |
| `ler_motor_20261026.py` | confere o hash de cada texto, troca `{U+XXXX}` pelo caractere e grava `motor_20261026.json` |
| `motor_20261026.json` | o JSON do motor: os mesmos dados, com os nomes exatos e as datas em DD/MM/AAAA |
| `motor_complementar_20261026.json` | medida complementar das 17:12:50 a 17:13:08, mesma recarga: cateterismo e as filas "ORGAOS INTERNOS DO TORAX" (sem termo de imagem no nome), digitada da saída do motor |
| `anterior_20261015_resumo.json` | subconjunto da coleta de 15/10/2026 (ramo `pre-plano-07-imagem-bancada`, commit c4ad0c7), para a diferença |
| `montar_20261026.py` | grava `coleta_20261026.json` (o formato do método: `filas`, `ocis` vazio, a janela viva, `nomes_internos`, `alarmes`) e `../mapa_social_20261026.xlsx`; a decisão de cada fila é a função `decidir()`, regra escrita a partir das decisões do usuário de 15 a 20/10/2026, não dado do motor |
| `coleta_20261026.json` | o JSON da coleta, que a conferência (`ferramentas/conferir_coleta.py`) lê |

Rodar: `python3 ler_motor_20261026.py && python3 montar_20261026.py` (de qualquer pasta; precisa de
openpyxl).

**A base recarregou durante a coleta.** O painel foi aberto às 16:24:21 com a base de 26/10/2026
14:36:46 (qLastReloadTime 2026-10-26T17:36:46Z); a recarga das 16:32:44 (19:32:44Z) entrou no meio da
transcrição. Tudo o que está aqui saiu depois dela, numa ida só, de 16:46:44 a 16:48:33, com a recarga
conferida no início e no fim; o que foi lido antes foi descartado.

**Transcrição.** O motor devolveu as tabelas em texto (campos separados por `|`; o espaço não
separável e os caracteres fora do Latin-1 como `{U+XXXX}`). Para encurtar, os nomes de fila que já
estavam na leitura descartada vieram como índice dela e foram trocados pelo nome conferido; o texto
resultante bate com o hash do texto inteiro calculado no navegador. Hashes djb2 de 32 bits:
filas 109.303 caracteres, 1068364975; códigos 20.382, 2206795101; agregados 28.324, 3777938657.

**Medidas.** Fila = os três status (pendente de regulação, corrigida e reenviada, pendente por fila
de espera), devolvidas à parte; viva = pedidos de 26/10/2024 em diante; agendadas 12 meses =
`data_agendamento` de 26/10/2025 a 25/10/2026, todos os status. Anos de estoque = fila ÷ agendadas em
12 meses (calculado no script).
