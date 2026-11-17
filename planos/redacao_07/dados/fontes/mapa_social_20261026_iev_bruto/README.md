# Mapa Social, 26/10/2026 (recarga 16:32) — sobreposição com o IEV, dados brutos

Coleta do agente `mapa-social` para os estudos do redacao_07 (imagem) e do redacao_08 (cardiologia):
o que as unidades do IEV (Instituto Esporte e Vida) agendam no SISREG desde o termo de 29/04/2026, e
a fila que as quatro OCI de ortopedia contratadas pelo IEV (09.03.01.001-1 a 004-6) podem atender pelo
CID aceito da ficha (Tabela 10/2026). Método de 25/10/2026. Só contagens agregadas: nenhum CNS, CPF,
nome ou data de nascimento.

| arquivo | o que é |
|---|---|
| `motor_iev_20261026.txt` | o texto que o motor devolveu (Qlik Engine API do painel), numa ida, de 17:33 a 17:46, com a recarga conferida no início e no fim. Para a transcrição, aspas viraram `~` e a barra invertida virou `^`. 117.748 caracteres, djb2 de 32 bits 2141536843 (calculado no navegador e conferido em cinco partes) |
| `montar_iev_20261026.py` | confere o hash, decodifica o texto e grava os três arquivos abaixo; a identificação das unidades do IEV (`IEV`, `CERTEZA`) e o contratado (`OCIS`, `CONTRATADO_OUTROS`, dos planos aprovados informados pela conversa principal) estão escritos no script, não vêm do motor |
| `motor_iev_20261026.json` | o JSON do motor, decodificado; a chave `formato` diz o que é cada coluna |
| `coleta_iev_20261026.json` | o JSON da coleta no formato do método: `filtro_fila`, `nomes_internos`, `filas` (um objeto por nome exato de fila, com `recortes` por OCI), `ocis` (teto, finalidade, núcleo), `alarmes`, `unidades_iev` |
| `../mapa_social_20261026_iev.xlsx` | a planilha, 26 abas e Leia-me; cabeçalho amarelo = calculado |

Rodar: `python3 montar_iev_20261026.py` (de qualquer pasta; precisa de openpyxl).

**Medidas.** Fila = os três status (pendente de regulação, corrigida e reenviada, pendente por fila de
espera), devolvidas à parte; viva = pedidos de 26/10/2024 em diante; agendadas 12 meses =
`data_agendamento` de 26/10/2025 a 25/10/2026; agendamentos do IEV = `data_agendamento` de 29/04/2026
em diante, `codigo_unidade_executante` em 0366986, 3031543 e 9180168. CID da OCI = `codigo_cid_solicitado`
igual a um código da lista da ficha (lista exata). Campos novos usados nesta coleta, além dos do método:
`codigo_unidade_executante`, `nome_unidade_executante`, `nome_unidade_executante_sisreg`,
`regiao_saude_executante` (o tipo da unidade: região da SES, URD, Contratado/Credenciado, Privado,
Não Relacionado - Base SES) e `status_solicitacao_agendamento_alias`.
