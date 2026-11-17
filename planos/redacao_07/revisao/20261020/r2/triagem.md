# Triagem — rodada 2 (20/10/2026)

Tréplica do Claude cego (contas e leitura) sobre o documento corrigido. Isolamento conferido
no registro dos dois: nada lido fora da pasta cega. `conferir_revisao.py --veredito`: ok.

| status da rodada 1 | veredito | achados |
|---|---|---|
| aceito | resolvido | 9 |
| aceito em parte | resolvido | 1 |
| contestado | contestação procede | 1 (CLL-G9-04: a frase sobre bens permanentes e obras fica) |
| aceito em parte (controle interno) | não resolvido | 10 |
| decisão do usuário | não resolvido | 34 |

**Achado novo, dos dois revisores (aceito):** a retirada de "truncado na segunda casa decimal"
(CLL-G9-10, rodada 1) deixou quatro valores de referência sem regra que os produza: a conta
exata dá R$ 99,946, R$ 100,188, R$ 300,155 e R$ 300,1152. **A frase voltou**, e as contas
batem com a tabela do objeto. É o único caso em que a correção criou o problema: a aceitação
do CLL-G9-10 foi um erro da triagem, e a lição é conferir se o "detalhe" que se tira sustenta
um número do documento.

**Rodada 3:** não rodou. O que voltou como não resolvido é, todo ele, decisão do usuário ou
controle interno, e a resposta não muda numa terceira leitura. Os dois lados estão em
`../divergencias.md`.
