# Mapa Social, 15/10/2026 (recarga 19:32) — dados brutos da coleta

Coleta do agente `mapa-social` para o redacao_07: varredura das filas de exames de imagem
(subgrupos SIGTAP 02.04, 02.05, 02.06, 02.07, 02.08 e 02.10, e filas de nome de imagem com outro
código) para escolher a fila de uma emenda nova, fora do plano 4. Não há objeto. Saída da Qlik
Engine API do painel e o script que monta `../mapa_social_20261015.xlsx`. Só contagens
agregadas: nenhum CNS, CPF, nome ou data de nascimento.

| arquivo | o que é | aba da planilha |
|---|---|---|
| `coleta_20261015.json` | as medidas (`filtro_fila`, `filtro_devolvidas`, `nota_medidas`, `conjuntos_set`); o universo e as categorias; os dezesseis nomes do plano 4 (`plano4_nomes_sisreg`, do JSON de 09/10 do redacao_06) e os nomes-resíduo (`residuo_nomes_sisreg`), exatos, com o U+00A0 real; `filas`: as 756 filas achadas, com `nome_sisreg` exato e o estudo; `por_codigo`, `por_modalidade` e `totais` de cada conjunto no motor; agendadas de jan–set/2026 por código e modalidade; Região de Saúde (quinze códigos candidatos, conjuntos e modalidades); descrição SIGTAP de cada código; falsos positivos da busca por nome; uma medida complementar (`extra_motor`) | 1 a 8 |
| `montar_20261015.py` | monta a planilha; a decisão de cada fila é a função `decidir()`, regra escrita, não dado do motor; calcula só as agendadas por mês (jan–set ÷ 9), os % de URD e contratado e a aba 9 (diferença para 09/10, lida de `planos/redacao_06/dados/fontes/mapa_social_20261009_bruto/coleta_20261009.json`) | 9 |

Rodar: `python3 montar_20261015.py` (de qualquer pasta; a raiz do repositório vem de
`$PLANOS_SES`, padrão `/Users/hendrick/Projetos/planos-ses`).

A base recarregou às 19:32:31 durante a coleta (o painel foi aberto às 19:25:48 com a base das
17:33:23). Tudo o que está no JSON saiu entre 19:35:33 e 19:36:21, numa ida só, com a recarga
conferida no início e no fim; o que foi lido antes foi descartado. A medida complementar das
cintilografias de miocárdio é das 19:53:40, na mesma recarga.

O motor devolveu as tabelas em texto (campos separados por `|`, caracteres fora do Latin-1
escritos como `{U+XXXX}`). O texto foi transcrito para o disco em partes, cada uma conferida
por hash djb2 de 32 bits contra o texto do motor, e o JSON foi montado dele: filas (96.160
caracteres, hash 3325946482, cinco partes) e agregados (30.091 caracteres, hash 2080346389,
duas partes). Os hashes de cada parte estão em `transcricao` no JSON.
