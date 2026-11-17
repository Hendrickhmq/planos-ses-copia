# Mapa Social, 09/10/2026 (recarga 11:32) — dados brutos da coleta

Coleta do agente `mapa-social` para o pré-plano de exames de imagem (redacao_06): os onze
procedimentos de ultrassonografia e tomografia, em dezesseis nomes de fila, e partes moles
à parte. É uma coleta independente, para comparar com a da conversa principal do mesmo dia.
Saída da Qlik Engine API do painel e o script que monta `../mapa_social_20261009.xlsx`. Só
contagens agregadas: nenhum CNS, CPF, nome ou data de nascimento.

| arquivo | o que é | aba da planilha |
|---|---|---|
| `coleta_20261009.json` | o enquadramento (`procedimentos[].nome_sisreg`, exato, com o U+00A0 real), as medidas (`filtro_fila`, `filtro_devolvidas`), fila, pessoas, devolvidas e espera por nome, por código e nos conjuntos; Região de Saúde na medida da fila; a varredura (`varredura`: subtotais por código, as 82 filas do mesmo código, o estudo das 119 filas em `varredura.estudo`, a união com o objeto e as filas de nome parecido em outras modalidades); o contexto dos subgrupos; os grupos 4 e 5 de tomografia | 1 a 7 e 9 |
| `montar_20261009.py` | monta a planilha; calcula só a aba 8 (diferença para 06/10, lida de `planos/redacao_04/dados/fontes/mapa_social_20261006_bruto/coleta_20261006.json`), o % da aba 5 e as agendadas por mês da aba 6; a decisão de cada fila da varredura é a função `decidir()`, regra escrita, não dado do motor | |

Rodar: `python3 montar_20261009.py` (de qualquer pasta; a raiz do repositório vem de
`$PLANOS_SES`, padrão `/Users/hendrick/Projetos/planos-ses`).

O JSON foi transcrito do navegador para o disco em partes, cada uma conferida por hash
contra o texto que o motor devolveu: a coleta (31.460 caracteres, hash 3774485668), o estudo
da varredura (23.948, hash 692024286) e a lista de outras modalidades (3.109, hash
1218940085), com o U+00A0 escrito como ` ` no texto conferido.
