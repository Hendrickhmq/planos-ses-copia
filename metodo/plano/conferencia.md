# plano/conferencia.md — a fase 6

Obrigatória antes de entregar. São **quatro conferências**, e nenhuma substitui a
outra:

| conferência | o que garante |
|---|---|
| **bateria do padrão** — `conferir_plano.py` | coerência interna, aritmética, estrutura, regra de método |
| **bateria do plano** — `planos/redacao_NN/conferencia/` | o que só este objeto tem, e a bateria do padrão não sabe conferir |
| **checklist das lições** — `consultar.py checklist` | as lições do acervo que nenhuma verificação cobre inteira |
| **revisão cega** — o Claude cego e, na versão final, o Sol (`../revisao/cega.md`) | o que um parecerista que não conhece a conversa devolveria: contas, contradição interna, estrutura contra os aprovados, lastro, faturamento, risco, régua e voz |

```bash
python3 ferramentas/conferir_plano.py planos/redacao_NN/
python3 ferramentas/testar_conferencia_plano.py planos/redacao_NN/
python3 ferramentas/consultar.py checklist planos/redacao_NN/ --saida planos/redacao_NN/checklist.md
```

## As duas baterias

**A bateria do padrão** roda em todo plano, sempre igual: as verificações A a X do
`conferir_plano.py`. **A bateria do plano** mora na pasta do plano e confere o que só
aquele objeto tem, como o dimensionamento de sala e de aparelho de um exame que dura
25 minutos:

```
planos/redacao_NN/conferencia/
  verificacoes.py     funções verificar_<nome>(d, r); o conferir_plano.py as carrega se existirem
```

O relatório sai em dois blocos, o do padrão e o do plano. **Para entregar, os dois
estão em 100%**, e o `testar_conferencia_plano.py` também: ele injeta um erro
conhecido por vez numa cópia do plano e exige que a verificação certa falhe. Suíte
que passa não prova nada; prova que não acusou.

**Uma verificação do plano que se mostra geral sobe para o `conferir_plano.py`**, com
linha de origem, pela triagem de `procedimento.md`. Nenhuma constante nem exceção de um
plano fica na ferramenta geral: o que muda de plano para plano vem do `estado.yaml`.
*Origem: reorganização de 08/10/2026 — a G tinha a fórmula da endoscopia na ferramenta geral.*

**Quando a conferência acusar, a primeira pergunta é se o defeito é do plano ou do
teste.** No `redacao_03`, defeito da própria ferramenta foi a maioria dos alarmes nas
primeiras rodadas: 3 achados reais contra 9 defeitos da conferência. Defeito de teste
se corrige e se registra no `estado.yaml`.

**Achado novo vira verificação nova.** Assim nasceram a O (identificação repetida), a P
(meta sem dotação) e a R (prosa contra tabela): o usuário apontou, e se codificou para
não acontecer de novo. A W (código contra o catálogo do SIGTAP) e a X (rubrica vedada
ou atacada) vieram de erro alheio, dos aprovados e do que o MPCDF atacou neles. O que
não dá para codificar vira lição com pergunta, no `registros/licoes.csv`.

**A verificação Y confere o plano contra o pré-plano enviado**, quando o projeto tem os
dois e o `estado.yaml` aponta o enviado em `pre_plano_enviado`. Todo código SIGTAP do
plano estava no pré-plano; o valor global do plano é o Valor Total do pré-plano; a
produção assistencial do plano é a aplicação das despesas do pré-plano. A SES já recebeu
aqueles números, e o plano detalhado é lido contra eles. Divergência decidida (a SUCONV
pediu outro valor, um código saiu) se declara em `pre_plano_divergencias`, com motivo.

**A verificação R é comum, regra 14, virada em máquina.** A, B e C conferem tabela
contra tabela, e por isso não veem o defeito mais comum depois de uma mudança de
premissa: a planilha muda e a prosa fica para trás. A R confere que valor em reais
citado no texto existe em alguma tabela, num parâmetro do `estado.yaml` ou numa norma
citada no mesmo parágrafo; que quantidade dita com o rótulo de um item da planilha é
uma quantidade dela; e que consumo derivado ("quatro folhas por OCI") bate com o
quantitativo.
*Origem: redacao_03 — a meta de 13.000 para 13.005 deixou "104 resmas" onde a planilha
dizia 105, e passou por dezessete verificações.*

## O checklist das lições

Cada lição de `registros/licoes.csv` (o que os aprovados erraram, o que o termo veda e
o que o MPCDF atacou depois da aprovação) sai em ordem de gravidade. O que uma
verificação cobre inteiro vem marcado; o resto é pergunta, e a resposta vai para o
`checklist.md` do plano. Item aberto não é falha: é pergunta que só uma pessoa
responde. Verificação que falhou é falha.

## A revisão cega

As baterias garantem que o plano é coerente consigo mesmo. Não garantem que ele é
verdadeiro contra as fontes, nem que um parecerista de fora o aprovaria. Essa parte é a
**revisão cega**: dois revisores que não conhecem a conversa leem o plano num pacote cego
e devolvem o que um parecerista devolveria. Na versão final, o Sol, de outra família, lê
uma vez. O método está em `../revisao/cega.md`, com o pacote, as perguntas, a triagem com
fonte e as três rodadas. Roda pelo comando `/revisao`.

As consultas C1 a C4 da antiga conferência no NotebookLM viraram a G1, a G2 e a G3 de
`../revisao/perguntas.md`. A C2 saiu: comparar seis documentos de uma vez é onde o Gemini
confabula. A estrutura contra os aprovados é a A7, e o inventário se confere aqui,
localmente.

### O inventário dos aprovados, local

**Para estrutura e itens, o `grep`, que não confabula; para valores, a planilha
consolidada, sempre.** Na rodada do `redacao_03` a C2 deu assistente a R$ 4.300 e
recepcionista a R$ 3.000, e a extração local (colunas `Valor Unitário` e `Quantidade`)
mostra **R$ 3.200** para os dois.

```bash
python3 - <<'PY'
import csv, pathlib
for d in ("pt_ses_01","pt_ses_02","pt_ses_03","pt_ses_04","pt_ses_05"):
    f = pathlib.Path(f"estudo/normalizados/{d}/planilha.csv")
    if not f.exists(): continue
    for row in csv.DictReader(f.open(encoding="utf-8")):
        print(d, row["Item"], row["Quantidade"], row["Valor Unitário"], row["DESCRIÇÃO"][:40])
PY
```

O inventário do nosso lado:

```bash
grep -nE "^## [0-9]+\." planos/redacao_NN/plano.md                 # seções
grep -nE "^\|\s*(1\.1\.|1\.2\.|3\.)" planos/redacao_NN/plano.md   # postos e rubricas
grep -nE "^\|\s*R-[0-9]{2}" planos/redacao_NN/plano.md              # riscos
```
