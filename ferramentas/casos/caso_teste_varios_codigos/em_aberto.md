# O que está em aberto — 17/09/2026

Consolidado depois da v4. Quatro frentes.

---

## 1. Dados que só você tem · 8 lacunas no documento

Nenhuma delas é difícil; todas impedem a entrega.

| onde | o que falta |
|---|---|
| 1.1 | razão social, CNPJ, endereço, CNES, representante legal, telefone e correio eletrônico |
| 1.2 e 7.2 | autor, número e RP da emenda |
| 4 | apresentação narrativa do proponente — natureza jurídica, tempo de atuação, serviços de imagem em operação, habilitações sanitárias, experiência com a rede pública |

---

## 2. Achados da revisão · 21 abertos

**A contagem que dei estava errada.** Falei em dezesseis; conferindo item a item são
**vinte e dois**, dos quais um — a carga por posto — foi resolvido na v4. Restam 21.

### Materiais · 2

| # | achado | tamanho |
|---|---|---|
| **A1** | A **creatinina** é pré-condição que o plano exige e não oferta | 12.726 exames |
| **A2** | O **sistema de imagem** sustenta a 5.6, a 5.7 e a mitigação do R-09, e não está na 9.3 nem tem rubrica | preço no acervo: R$ 5.980 a R$ 7.500 |

### Delimitação incompleta na 9.3 · 3

Meios de atendimento a reação adversa ao contraste · meio corporativo de contato ·
impresso de entrega do laudo. Nenhum é caro; o defeito é a 9.3 dizer "o valor unitário
remunera" com a lista incompleta.

### Régua contra o proponente · 4

| # | trecho |
|---|---|
| **C1** | Meta 2 conta "81.546 solicitações agendadas **e confirmadas**" — confirmar depende do usuário |
| **C2** | 5.11 — "reapresentados **dentro da competência seguinte**" |
| **C3** | 5.9 — "a busca ativa é **diária**" |
| **C4** | R-04 — "o consumo por exame é apurado **mensalmente**" |

### Afirmação sobre sistema da concedente · 3

| # | trecho |
|---|---|
| **D1** | 5.9 — "o reagendamento não devolve o usuário ao fim da fila: ele mantém a posição" |
| **D2** | 5.6 — "remarcado **com prioridade sobre a fila corrente**" |
| **D3** | 5.2 — "o agendamento observa risco e data, **nessa ordem**" |

Os três podem estar certos. **Nenhum foi conferido** contra o modo como a SES-DF opera
a fila — e essa conferência é sua.

### Voz · 5

Quatro negações defensivas — E1 "a busca ativa é diária, **e não mensal**" (a mais
clara: ninguém disse mensal), E2 "exame interrompido não é exame perdido", E3 "achado
que exige conduta imediata não espera o laudo", E4 "o laudo não depende da presença do
radiologista no polo" — e um meta-comentário na 5.8 sobre a prestação de contas.

**A taxa geral está na faixa** — 14% de negação contra 15% do plano 3. São estas cinco
frases, não o volume.

### Registro · 2

"Preparo conferido na recepção é vaga preservada" é construção de slogan, que o acervo
não usa. E a frase do "último momento em que uma falha ainda se corrige sem perda de
vaga" veio inteira do plano 3.

### Lastro · 2

O **CPF obrigatório** é provável — Portaria SAES/MS 2.723/2025 e Anexo III da 4.282/2026
— e não foi conferido procedimento a procedimento. E a **3.1 traz onze nomes de fila**
contra os **nove códigos de ultrassonografia da 2.2**, sem remeter à ponte.

---

## 3. Fase 0 · 3 lacunas

| # | o que | efeito |
|---|---|---|
| **L-003** | fichas SIGTAP dos doze códigos — idade, sexo, atributos complementares, CBO, habilitações | a parte que movia dinheiro fechou; o que resta vira condição de elegibilidade na seção 2 se alguma for restritiva. **Fecha também o G2 acima** |
| **L-004** | o contraste de tomografia ficou fora da planilha, com a dúvida registrada | reabre se a SES-DF orientar o registro do secundário. R$ 679.740,00 |
| **L-006** | o parque instalado não foi confirmado | o plano declara **capacidade requerida**, não inventário. O risco R-01 fica de pé: abaixo de treze salas e três tomógrafos, a meta não roda no ritmo previsto |

---

## 4. Conferência · nenhuma das três foi rodada

O `PADRAO.md` exige as duas locais em 100% e a substantiva no NotebookLM antes de
entregar. **Nenhuma rodou.**

```
python3 conferir_plano.py redacao_04/
erro: estado.yaml sem parametros.valor_unitario.valor
```

**O defeito é do teste, não do plano.** A ferramenta pressupõe um valor unitário único
e tabelas de OCI. Precisam de adaptação:

| verificação | por quê |
|---|---|
| carregar_parametros | exige `valor_unitario.valor`; aqui há cinco unitários e doze códigos |
| **E** | procura coluna "OCI" na tabela de rateio |
| **G** | procura "Salas de procedimento" e "Endoscópios" |
| **H** | confere `quantitativo_oci` |
| **N** | confere o código da OCI na fonte; não há OCI neste objeto |

A `testar_conferencia_plano.py` confere a primeira e cai junto. A substantiva no
NotebookLM depende de o `plano.md` subir como fonte.

---

## 5. Uma decisão pontual

A 6.3 publica a **ocupação do tomógrafo do Gama em 35,9%**. É da mesma família da carga
por posto que saiu na v4 — convida à pergunta "então por que três aparelhos?". O
parágrafo seguinte responde, e o plano 3 tem precedente com 61%. Tirar a linha de
ocupação do tomógrafo e manter só a contagem é uma palavra sua.

---

## A ordem que eu seguiria

1. **A1 e A2** — são os dois que um parecerista usa.
2. **C1** — a Meta 2 é a única régua que vira meta não cumprida.
3. **D1 a D3** — conferir com a regulação, e cortar o que não se confirmar.
4. **As cinco frases de voz e as duas de registro** — meia hora.
5. **Os oito campos cadastrais.**
6. **Adaptar `conferir_plano.py`** e rodar as três conferências.

Os passos 1 a 4 não tocam a aritmética. **R$ 11.688.862,74 e 81.546 exames seguem
travados desde a v2.**
