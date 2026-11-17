# revisao/cega.md — a revisão cega: quem não conhece a conversa lê o que fizemos

Vale para as duas trilhas. No plano, é a quarta conferência da fase 6
(`../plano/conferencia.md`). No pré-plano, roda antes do envio
(`../pre_plano/conferencia.md`). Quem roda é o comando `/revisao`
(`.claude/commands/revisao.md`). O método é este arquivo.

| arquivo | o que guarda |
|---|---|
| `cega.md` | este: por que, o pacote, a rodada, a triagem, a tréplica, a versão final, o registro |
| `perguntas.md` | as perguntas, as mesmas para qualquer revisor |
| `claude.md` | o revisor padrão: o Claude cego, em dois subagentes |
| `chatgpt.md` | o revisor de outra família, uma vez, na versão final: o Sol |
| `gemini.md` | o revisor do Google, opcional, fora do padrão |
| `esquemas/` | os formatos do achado, da resposta e do veredito |

*Origem: pedido do usuário, 11/10/2026: "analisar meus planos para fazer sem viés". A
calibração do mesmo dia comparou o ChatGPT, o Gemini e o Claude cego contra a devolutiva
do professor, e o usuário decidiu: o Claude cego é o padrão, e a versão final passa pelo
Sol.*

---

## 1. Por que revisão cega

Quem escreve o plano com o usuário é o assistente, e a conferência dele tem três vieses.
Cada um tem uma trava:

| viés | o que acontece | a trava |
|---|---|---|
| **autopreferência** | o modelo avalia melhor o texto que reconhece como seu (Panickssery, Bowman e Feng, NeurIPS 2024) | o revisor padrão não conhece o texto nem a conversa, e **a versão final passa por outra família** (o Sol, `chatgpt.md`). Na calibração, o Claude cego foi mais duro com o texto do que os de fora |
| **contexto que justifica** | quem leu a conversa e o `estado.yaml` já conhece as razões e as aceita | o **pacote cego** (seção 2) |
| **enquadramento** | "o plano está bom?" puxa para o sim | o revisor é **o parecerista que procura motivo para devolver**, e a lista vazia é resposta válida |

**O quarto viés é a triagem**, onde o assistente decide o que vale. A trava está na seção 4:
nada é aceito nem contestado sem fonte, e o usuário vê também o que foi recusado.

**Cada revisor recebe só o que faz bem.** O que ele muito provavelmente devolveria errado
não vai para ele (`perguntas.md`, a tabela de quem responde o quê; `chatgpt.md` e
`gemini.md`, o que não dar a cada um). *Origem: o usuário,
11/10/2026: "pondere a usabilidade dos modelos, e não passe para eles coisas que muito
provavelmente eles vão retornar de forma errônea".*

## 2. O pacote cego

```bash
python3 ferramentas/pacote_revisao.py --documento planos/redacao_NN/plano.md \
    --saida planos/redacao_NN/revisao/AAAAMMDD/r1/pacote --titulo "<objeto>" \
    --norma "<pasta em biblioteca/extraidos_normas/ ou arquivo em biblioteca/normas/>" ... \
    --aprovados --fichas-de planos/redacao_NN
```

**O que entra:**
- o documento;
- as normas do objeto e as do instrumento. São as que o documento cita, mais as do
  programa e a sanitária do serviço. A versão vigente é a da data do documento;
- os cinco planos aprovados;
- as fichas do SIGTAP;
- no pré-plano, o formulário da SES, porque é o do leitor.

**O que não entra:** o `estado.yaml`, as lições, as pendências, a conversa, a devolutiva,
e **nem o `metodo/`**. O revisor julga contra a fonte oficial e pelo olhar de quem lê, não
pelo nosso padrão, porque as regras são nossas e também podem estar erradas.

**Dado pessoal:** a ferramenta mascara CPF e CNS em todos os arquivos e varre o pacote de
novo. Se sobrar um, ela para, e o pacote não sai. Quatro dos cinco aprovados normalizados
têm CPF.

**O envio está autorizado** à OpenAI e ao Google, sem perguntar a cada rodada, desde que
o pacote passe nessa varredura. *Origem: decisão do usuário, 11/10/2026.* O Claude cego
não manda nada para fora: a pasta cega fica no computador.

## 3. A rodada

O revisor padrão é o Claude cego, em dois subagentes paralelos, contas e leitura
(`claude.md`).

```bash
python3 ferramentas/revisar_claude.py preparar <r1>/pacote --pasta <pasta cega> [--faturamento]
#   o /revisao abre os dois subagentes com o texto impresso
python3 ferramentas/revisar_claude.py juntar <pasta cega> --saida <r1>/claude
python3 ferramentas/conferir_revisao.py <r1>/pacote <r1>/claude/achados.json
```

- **Os dois revisores não se veem,** e nenhum conhece a conversa. Quem prepara a pasta e
  junta a resposta é o script; a pergunta sai do método e a resposta vai direto para o
  arquivo.
- **A conferência é por máquina:** o trecho citado existe no documento e na fonte, literal
  ou "aproximado" (a tabela achatada)? Achado com citação que não confere não chega à
  triagem como achado. Vai como `citacao_invalida`, para o usuário ver quantos foram.
- **Quando os dois apontam o mesmo ponto**, ele sobe na prioridade da triagem.

## 4. A triagem e a resposta

O assistente lê cada achado contra a fonte primária (comum, regra 4) e escreve
`<rodada>/resposta.json` (esquema `esquemas/resposta.json`) e `<rodada>/triagem.md`:

| status | o que se faz | o que tem de vir junto |
|---|---|---|
| `aceito` | corrige o documento | a seção alterada e a fonte que sustenta a correção |
| `aceito_em_parte` | corrige o que procede | o que muda, o que não muda e por quê, com a fonte |
| `contestado` | não muda | o trecho literal da fonte primária que contradiz o achado. **Sem fonte não se contesta** |
| `decisao_do_usuario` | não muda e não descarta | o achado bate numa decisão travada (`estado.yaml`, com a data). Vai ao usuário com os dois lados |
| `citacao_invalida` | não muda | o trecho citado não existe, conforme a conferência por máquina |

```bash
python3 ferramentas/conferir_revisao.py <r1>/pacote <r1>/claude/achados.json --resposta <r1>/resposta.json
```

**As duas travas do assistente:**
- **Contra o viés defensivo:** contestar exige o trecho da fonte, e a tréplica julga esse
  trecho.
- **Contra o viés bajulador:** aceitar também exige a fonte, como qualquer mudança no
  documento. O revisor erra, e o de fora alucina de memória: aceitar tudo para fechar
  rápido põe no plano o erro dele. A correção roda as baterias da trilha; correção que quebra a bateria não
  entra.

**Aceitar um achado não é sempre acrescentar texto.** O que o revisor diz que "falta" passa
pelas perguntas da leitura de entrega antes de entrar (`../plano/leitura_de_entrega.md`):
a explicação de regra é memorial, e a condição a comprovar é régua contra o proponente.
Esse achado se aceita no controle interno (`pendencias.md`, o checklist de
pré-assinatura), e o documento fica como está. *Origem: calibração de 11/10/2026. A C4 de
01/09 pôs o teto de MAC como condição de partida na 4.2, e a devolutiva de 05/09 cortou a
4.2 inteira. A G2 de 11/10 pediu quatro explicações de regra de faturamento.*

**A triagem também mede o revisor.** O `<rodada>/triagem.md` conta, por revisor e por passada,
quantos achados foram aceitos, contestados e inválidos. Com o tempo, isso diz qual
pergunta paga o custo.

## 5. A tréplica: no máximo três rodadas

A rodada 2 roda sobre o documento corrigido, num pacote novo. A rodada 3, só sobre o que
ainda estiver em discussão.

```bash
python3 ferramentas/revisar_claude.py preparar <r2>/pacote --pasta <pasta cega> --treplica <r1>
python3 ferramentas/revisar_claude.py juntar <pasta cega> --saida <r2>/claude --treplica
python3 ferramentas/conferir_revisao.py <r2>/pacote <r1>/claude/achados.json --veredito <r2>/claude/veredito.json
```

- O revisor recebe só o documento novo, o que mudou, os achados dele e a resposta curta,
  com a fonte. **Não recebe o raciocínio do assistente,** e é instruído a julgar o trecho
  citado, não o argumento.
- O veredito de cada achado é `resolvido`, `nao_resolvido`, `contestacao_procede` ou
  `contestacao_nao_procede`.
- Ponto novo só sobre o que mudou, e só se a correção criou o problema. Sem isso o ciclo
  não termina.
- **Depois da terceira rodada, o que sobrar vai ao usuário** em `revisao/AAAAMMDD/divergencias.md`, com os
  dois lados e as fontes. A decisão dele entra no `estado.yaml` com a data.

*Origem: decisão do usuário, 11/10/2026: três rodadas.*

## 6. A versão final: o Sol

Quando as rodadas do Claude cego fecham e o documento está pronto para a entrega, ele passa
**uma vez** pelo ChatGPT, no modelo Sol (`chatgpt.md`), com as perguntas A1, A2 e A4. É a
leitura de outra família. A resposta passa pela mesma triagem da seção 4, e o que sobrar
vai ao usuário junto com as divergências.

```bash
python3 ferramentas/revisar_chatgpt.py <rf>/pacote --saida <rf>/chatgpt
```

## 7. O registro

```
planos/redacao_NN/revisao/AAAAMMDD/
  r1/ pacote/  claude/  resposta.json  triagem.md
  r2/ pacote/  claude/  resposta.json
  r3/ ...
  final/ pacote/  chatgpt/  resposta.json
  divergencias.md
```

- **O que vai para o git:** o documento e o `manifesto.json` de cada `<rodada>/pacote/`.
  As fontes do pacote se refazem pelo manifesto e ficam fora (`.gitignore`).
- O `estado.yaml` leva, sob `revisao_cega`, a data, o número de rodadas e os achados por
  status e por revisor.
- **Achado confirmado que se repete de um plano para outro vira verificação** na bateria
  da trilha, ou lição. É o ciclo que o método já usa.

## 8. A calibração

O primeiro teste usou o gabarito que o projeto tem: o `redacao_03`, versão enviada em
03/09/2026 (`dados/enviado_20260903.md`), contra a devolutiva do professor de 05/09
(`apontamentos_professor.md`: 31 apontamentos firmes).

| | Astra | Gemini | Claude cego (2) |
|---|---|---|---|
| gabarito pego | 8 | 14 | **23 (74%)** |

**Ressalva:** as perguntas de diligência nasceram dessa mesma devolutiva, e a taxa é
otimista. O teste de verdade é a próxima devolutiva. O resultado completo está em
`planos/redacao_03/revisao/calibracao_20261011/calibracao.md`.
