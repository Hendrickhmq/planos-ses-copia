# registros/vigia/ — os relatórios da vigia de normas

Um relatório por vigia, escrito pelo agente `normas` (todo dia 10, ou quando chamado):

- `vigia_<AAAA-MM-DD>.md`: o que mudou e importa, as novidades do Ministério da Saúde, o
  que foi registrado e corrigido, os planos afetados e o que fica a decidir. A última linha
  diz a competência vigiada; o `ferramentas/testar_atualidade.py` lê essa linha.
- `dou_<AAAA-MM-DD>.md`: a lista dos atos do Ministério da Saúde no DOU no período, gerada
  pelo `ferramentas/ler_dou.py`. É o ponto de partida da leitura, não a validação.
- `controle_<AAAA-MM-DD>.md`: as decisões do TCDF e as notícias do MPCDF e do TCDF no
  período, gerada pelo `ferramentas/ler_controle.py`. Também é ponto de partida.

O método é `metodo/coleta/normas.md`.
