# pre_plano/conferencia.md — a bateria do pré-plano

Obrigatória antes de enviar. As duas em 100%:

```bash
python3 ferramentas/conferir_pre_plano.py planos/redacao_NN/plano_v1_geral.md
python3 ferramentas/testar_conferencia_pre_plano.py planos/redacao_NN/plano_v1_geral.md
```

A primeira confere o documento. A segunda injeta um erro conhecido por vez numa cópia e
exige que a verificação certa falhe: bateria que só passa não prova nada. O erro que morde
uma construção que o documento não tem (o percentual da fila, num pré-plano que não o
publica) sai como "não se aplica a este pré-plano" e não conta; o que não acha onde morder
numa construção que deveria existir é falha da própria bateria.

## O que ela confere

**As verificações do padrão que valem para as duas trilhas** são as mesmas do plano, e o
código é um só (`conferir_plano.py`):

| | o que confere | regra |
|---|---|---|
| **J** | os nove campos do formulário da SES, na ordem | `formulario.md` |
| **K** | os títulos | `../plano/estrutura.md` |
| **L** | nada do método no documento | comum, regra 12 |
| **M** | toda norma citada tem arquivo em `biblioteca/normas/` | comum, regra 7 |
| **Q** | a voz do documento | comum, regra 9 |
| **S** | nenhuma régua contra o proponente; indicadores em 100% | comum, regra 6 |
| **T** | todo percentual e toda medida de tempo têm o mesmo número em `estado.yaml` ou `dados/` | comum, regra 1 |
| **U** | nenhum parágrafo para dizer o que o documento não tem | comum, regra 9 |
| **W** | código e valor de cada OCI contra o catálogo do SIGTAP | comum, regra 3 |
| **X** | nenhuma rubrica vedada ou atacada pelo controle | — |

**As próprias do pré-plano:**

| | o que confere | regra |
|---|---|---|
| **PA** | a aplicação das despesas só tem custo assistencial: nenhuma linha de gestão, apoio ou pessoal com valor, nenhum percentual | `procedimento.md`, regras 3 e 4 |
| **PB** | nada do plano detalhado: quadro de equipe ou de salários, curva mensal, capacidade ou polo com número, parcela de desembolso | `formulario.md`, "O que não entra" |
| **PE** | o Valor Total não passa do recurso do `estado.yaml`; a aplicação das despesas não passa do Valor Total; a meta em valor é igual à aplicação | `procedimento.md`, regra 2 |

## A revisão cega

Depois das duas baterias em 100%, e antes do envio, o pré-plano passa pela revisão cega:
dois revisores que não conhecem a conversa leem o documento num pacote cego, que leva
também o formulário da SES. Na versão que vai ao envio, o Sol lê uma vez. O método é
`../revisao/cega.md`, e o comando é `/revisao`. No pré-plano, a pergunta de contas encolhe,
porque o documento tem poucos números.

## O que ela ainda não confere

- **O texto literal da SUCONV** no campo do MROSC: não há fonte local para comparar.
  Confere-se à mão, no diff contra a versão devolvida.
- **O plano contra o pré-plano**: está na bateria do plano, `../plano/conferencia.md`.

**O número arredondado no documento se registra na fonte.** A T casa o número exato,
colado à unidade, porque janela folgada já deixou passar número falso. Se o documento
diz 84% e a conta dá 83,8%, a linha de `dados/` diz as duas coisas.

*Origem: reorganização de 08/10/2026 — o pré-plano não tinha conferência. Ao montar o
teste desta bateria, a S se mostrou cega para a coluna "parâmetro", que o `modelo.md`
do plano também usa; foi corrigida para as duas trilhas.*
