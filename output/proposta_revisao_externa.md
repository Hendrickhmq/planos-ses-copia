# Revisão externa: Astra e Gemini — proposta

> **Superada em 11/10/2026.** A proposta foi construída e calibrada. O que vale agora é
> `metodo/revisao/` (externa, astra, gemini), no ramo `revisao-externa` a partir do
> `main`. Três coisas mudaram em relação a este texto:
> - não há agentes: o transporte é por script;
> - os planos aprovados não entram no caderno do Gemini;
> - as diligências de leitura passaram ao Gemini, porque a cota do Astra é curta.
>
> Este arquivo fica só como registro.

11/10/2026. **Proposta, não padrão.** Nada daqui entrou em `metodo/`. Se for aprovada, vai
para o `main` como diz a seção 7.

---

## 1. O problema

Hoje quem escreve o plano comigo também sou eu quem confere. Isso cria três vieses:

| viés | o que acontece | como se corta |
|---|---|---|
| **autopreferência** | o modelo avalia melhor o texto que reconhece como seu. Isso está medido: Panickssery, Bowman e Feng, NeurIPS 2024 | um revisor de **outra família** de modelo, já que dentro da mesma família a preferência se mantém |
| **contexto que justifica** | quem leu a conversa e o `estado.yaml` já conhece as razões e as aceita | um **pacote cego**: só o documento e as fontes oficiais |
| **enquadramento** | a pergunta "o plano está bom?" já puxa a resposta para o sim | o revisor recebe o **papel de parecerista que procura motivo para devolver**, com listas vazias permitidas |

Há um quarto viés, que volta pela porta dos fundos: **a triagem**. Se sou eu quem decide qual
achado vale, posso descartar o que incomoda. Por isso nenhum achado é descartado sem
motivo escrito e sem a fonte. A lista de rejeitados também vai para você.

---

## 2. O que a pesquisa mostrou

### GPT-6 Astra (ChatGPT)

- Lançado em setembro de 2026. No seu Mac, está disponível pelo Codex que vem dentro do app
  do ChatGPT. **Testei hoje: respondeu em modo não interativo, com saída em JSON fixo**,
  sem nenhum dado do projeto.
- **Pontos fortes:**
  - raciocínio e matemática: GPQA Diamond 96,0%, FrontierMath T4 97,6%;
  - trabalho de agente: ele roda código. Pode recalcular a planilha em Python, em vez de
    "achar" que a conta fecha;
  - lidera o GDP.pdf, um teste de trabalho de conhecimento sobre documentos (Artificial
    Analysis);
  - recuperação em contexto longo: 100% no MRCR de 256 a 512 mil tokens, segundo a própria
    OpenAI. No Codex, a janela é de 272 mil;
  - devolve a resposta num esquema fixo (`--output-schema`), o que deixa conferir cada
    achado por máquina.
- **Ponto fraco:** de memória, ele erra muito. Alucinou 51% no AA-Omniscience, o teste de
  conhecimento da Artificial Analysis. O número caiu de 92%, mas é alto. Também fecha a
  tarefa em poucos turnos.
- **Conclusão:** ele é o **parecerista que faz conta e cruza o documento consigo mesmo**.
  É proibido citar norma de memória: só vale o arquivo do pacote, com o trecho literal.
  Uma pergunta por execução.

### Gemini (Gemini Notebook, o antigo NotebookLM)

- Rebatizado em julho de 2026. Já está ligado aqui pelo `nlm` e pelo servidor MCP
  (21 cadernos na sua conta).
- **Pontos fortes:**
  - a resposta é presa às fontes do caderno, com o trecho citado;
  - cada fonte aceita até 500 mil palavras, e o caderno aceita dezenas de fontes. Cabem as
    normas inteiras, os cinco aprovados e as fichas;
  - a família Gemini tende a dizer "não sei" em vez de inventar. O Gemini 4 Argon fez 15%
    no mesmo teste em que o Astra fez 51%. **Mas não se sabe qual modelo roda no caderno
    hoje**, e o Argon ainda não está aberto ao público.
- **Pontos fracos já medidos aqui:**
  - confabulou 11 de 15 pontos quando comparou seis documentos de uma vez (C2, 01/09);
  - dá resposta sem `sources_used`;
  - confere instantâneo velho se o plano não for subido de novo (C4, `redacao_03`).
- **Conclusão:** ele é o **leitor das fontes**. Faz lastro, faturamento, risco e omissão
  normativa, sempre uma afirmação contra uma fonte. Ele transcreve, e a comparação é nossa.
  Nunca compara vários documentos de uma vez e nunca dá valores.

### Os números de modelo são do fabricante ou de um teste só

Por isso a seção 5 mede os dois **nos nossos documentos**, antes de confiar em qualquer um.

---

## 3. A arquitetura

```
                 ┌──────────────── pacote cego ────────────────┐
                 │ documento.md  + normas + aprovados + fichas │
                 │ (CPF e CNS mascarados; sem estado, lições,  │
                 │  pendências, conversa, nem metodo/)         │
                 └───────────┬───────────────────┬─────────────┘
                             │                   │
             revisor-astra   ▼                   ▼  revisor-gemini
        (Codex, somente leitura,         (caderno novo e neutro,
         sem memória, sem rede)           conversas separadas)
                             │                   │
                  astra.json │                   │ gemini.json
                             └─────────┬─────────┘
                                       ▼
                     conferir_revisao.py: o trecho citado existe
                     literalmente no documento e na fonte?
                                       ▼
                     triagem na conversa (Claude): fonte primária,
                     comum regra 4 → confirmado · decisão travada ·
                     rejeitado (com fonte) · hipótese aberta
                                       ▼
                     revisao/AAAAMMDD/triagem.md + estado.yaml
```

- **Os dois não se veem.** Rodam em paralelo, e nenhum recebe a resposta do outro.
  Quando os dois apontam o mesmo ponto, ele sobe na prioridade.
- **Eu não julgo o mérito do plano nessa etapa.** Monto o pacote, transporto, confiro a
  citação e faço a triagem na fonte primária.
- **O pacote não leva `metodo/`.** O revisor julga contra a fonte oficial e pelo olhar de
  quem lê, não pelo nosso padrão: as regras são nossas e também podem estar erradas. O
  formulário da SES entra, porque é o do leitor.
- **Privacidade:** quatro dos cinco aprovados normalizados (`pt_ses_01` a `04`) têm CPF. O
  pacote mascara CPF e CNS com o mesmo padrão do `conferir_coleta.py`. Se sobrar algum, a
  montagem para.

---

## 4. Os dois comportamentos

### 4.1 `revisor-astra` — o parecerista que faz conta

**Como roda:** um subagente do Claude monta a pasta temporária com o pacote e chama:

```
codex exec -m gpt-6-astra -c model_reasoning_effort="xhigh" \
  --ephemeral --ignore-user-config --skip-git-repo-check -s read-only \
  -C <pacote> --output-schema esquema_astra.json -o <saída>/A<n>.json "<passada>"
```

- `--ignore-user-config` e `--ephemeral`: sem a memória do Codex e sem as suas regras;
- `-s read-only`: lê e roda Python, mas não escreve nem sai para a rede;
- uma execução por passada.

**Instrução comum, no início de cada passada:**

> Você é parecerista da Secretaria de Estado de Saúde do DF e vai analisar
> `documento.md`, de um proponente que você não conhece. Sua função é achar o que
> justifica devolver o documento em diligência ou reprová-lo.
> 1. Só vale o que está nos arquivos desta pasta. Não cite norma, valor ou regra de
>    memória. Se precisar de uma fonte que não está aqui, registre em `falta_fonte`.
> 2. Cada achado traz o trecho do documento **copiado literalmente** e, se invocar
>    fonte, o arquivo e o trecho literal dela.
> 3. Refaça em Python toda conta que usar, e mostre a expressão.
> 4. Não elogie, não sugira estilo, não reescreva o documento.
> 5. Lista vazia é resposta válida. **Achado inventado é o pior erro possível.**

**As passadas:**

| | pergunta | vem de |
|---|---|---|
| **A1 — contas** | Liste todo número que dependa de outro: totais, quantidade × valor, metas × meses, percentuais, capacidade × vigência. Recalcule cada um. Aponte o que não fecha, os dois totais do mesmo universo que divergem e o número que não tem de onde vir. | leitura de entrega, perguntas 2 e 8 |
| **A2 — contradição interna** | Extraia de cada seção as afirmações de fato: quem executa, onde, quando, quanto, com que equipe e com que sistema. Cruze todas com todas. Aponte os pares incompatíveis, com os dois trechos. | pergunta 12, a mais cara |
| **A3 — diligências** | Escreva as diligências que você mandaria ao proponente. Use como roteiro: régua que nenhuma norma exige, detalhe que vira compromisso fora do controle do executor, seção que diagnostica e não fecha, vocabulário de mercado, conteúdo no lugar errado, memorial do que é ato do parecerista. | perguntas 1, 5, 7, 9, 10 e 11 |
| **A4 — aberta** | Fora do que já foi perguntado: o que faria você devolver este documento? No máximo dez pontos, os mais graves primeiro. | espaço fora do meu enquadramento |

**Saída:** um JSON por passada. Cada achado traz `id`, `passada`, `classe`,
`trecho_documento`, `secao`, `fonte_arquivo`, `trecho_fonte`, `conta`, `gravidade`
(`reprova` · `diligência` · `ajuste`) e `por_que`. A resposta traz ainda
`listas_vazias` e `falta_fonte`.

**No pré-plano:** a A1 encolhe, porque ele tem poucos números. A A3 usa os campos do
formulário da SES como roteiro.

### 4.2 `revisor-gemini` — o leitor das fontes

**Como roda:** um subagente do Claude, pelo servidor `gemini-notebook-mcp`, cria um **caderno
novo a cada rodada**, com nome neutro: "Análise — <objeto> — <data>". As fontes são o
documento, com o título **"DOCUMENTO EM ANÁLISE"**, as normas do tema, os cinco aprovados e
as fichas do SIGTAP. O caderno antigo do plano não serve, porque leva fonte velha. Com o
`chat_configure`, o caderno recebe a instrução:

> Você analisa a fonte "DOCUMENTO EM ANÁLISE" contra as demais fontes. Responda só com o
> que as fontes dizem, citando-as. Se as fontes não tratam do ponto, escreva "as fontes
> não tratam". Não elogie e não sugira estilo.

**As consultas, cada uma em conversa nova (`new_conversation`):**

| | o que faz | onde mora |
|---|---|---|
| **G1 — contradição e lastro** | a C1 de hoje | `metodo/plano/conferencia.md`, sem copiar |
| **G2 — faturamento** | a C3, quando o objeto tem APAC ou OCI | idem |
| **G3 — execução e risco** | a C4 | idem |
| **G4 — obrigações (nova)** | Com `source_ids` restrito às normas: "Liste, norma a norma, as obrigações que estas normas impõem a quem executa este tipo de serviço. Para cada uma, o dispositivo e a transcrição. Não compare com nada." **A comparação com o documento é nossa, por `grep`**. É a lição da C2 aplicada à omissão. | nova |
| **G5 — inventário dos aprovados** | a C2 de hoje, só para estrutura | `metodo/plano/conferencia.md` |
| **G6 — prova (nova)** | Para cada contradição da G1 e da G3, numa conversa nova: "Transcreva literalmente o trecho da fonte X que sustenta: '…'. Se não houver, diga que não há." Achado que não sobrevive à própria prova cai antes de chegar à triagem. | nova |
| **G7 — aberta** | a mesma pergunta da A4, com as mesmas palavras | sobreposição proposital com o Astra |

**Saída:** o subagente transcreve cada resposta com `sources_used` e monta o `gemini.json`
no mesmo esquema do Astra. Resposta sem `sources_used` entra marcada como `indicativa`.

### 4.3 Onde os dois se cruzam

| | Astra | Gemini |
|---|---|---|
| contas e totais | **sim** | não, porque ele erra valores |
| contradição interna | **sim** | só se aparecer |
| contra a norma: lastro, faturamento, risco | só com o trecho do pacote | **sim** |
| omissão normativa | não | **sim** (G4 + grep) |
| diligência do parecerista | **sim** | não |
| pergunta aberta | **sim** | **sim**: é aqui que se mede a concordância |

### 4.4 O ciclo: parecer, resposta, tréplica

O ciclo imita o processo real da SES: a diligência, a resposta à diligência e o novo
parecer. **No máximo três rodadas** (decisão sua, 11/10/2026). A terceira trata só dos
pontos ainda em divergência. O que sobrar depois dela vai para você, e a decisão é sua.

```
 rodada 1   revisor ── parecer (achados) ──▶ conferir_revisao.py ──▶ eu
                                                                     │
 resposta   eu: cada achado recebe um status, com a fonte ◀──────────┘
            corrijo o documento → rodo as baterias (conferir_plano etc.)
                                                                     │
 rodada 2   revisor, sessão NOVA, recebe: documento novo + o que mudou
            + os achados dele + a minha resposta  ──▶ veredito por achado
                                                                     │
 rodada 3   só os achados ainda em divergência: nova resposta minha, novo veredito
                                                                     │
 fim        resolvido → fecha · divergência → vai para você com os dois lados
```

**Na resposta, cada achado recebe um destes status:**

| status | o que eu faço | o que tem de vir junto |
|---|---|---|
| `aceito` | corrijo | a seção alterada e a fonte que sustenta a correção |
| `aceito em parte` | corrijo o que procede | o que muda, o que não muda e por quê, com a fonte |
| `contestado` | não mudo | o trecho literal da fonte primária que contradiz o achado. **Sem fonte, não posso contestar** |
| `sua decisão` | não mudo e não descarto | o achado bate numa decisão travada (`estado.yaml`, com a data). Vai para você com o argumento dos dois lados |
| `citação inválida` | não mudo | o trecho que ele citou não existe no documento ou na fonte |

**Os dois vieses da minha parte, e a trava de cada um:**
- **Defensivo:** rejeitar o que incomoda. A trava é que contestar exige o trecho da fonte, e a
  rodada 2 julga essa fonte.
- **Bajulador:** aceitar tudo para fechar rápido. Isso põe no plano o erro dele, porque o
  Astra alucina de memória. A trava é que aceitar também exige a fonte (comum, regra 4),
  como qualquer outra mudança no documento. Correção que quebra a bateria não entra.

**Nas rodadas 2 e 3, a sessão é nova:**
- O revisor não traz a conversa da rodada 1 e não vê o meu raciocínio, só a resposta
  curta, com a fonte. A instrução manda **julgar o trecho citado, não o argumento**, para
  ele não ser convencido pela minha confiança.
- O veredito de cada achado é um destes: `resolvido`, `não resolvido`,
  `contestação procede` ou `contestação não procede`. Os dois últimos vêm com o trecho.
- Ponto novo só sobre o que mudou, ou seja, a correção que criou problema. Sem essa trava,
  o ciclo não termina.

**As perguntas das rodadas 2 e 3:** **A5 — tréplica**, no Astra; **G8 — tréplica**, no Gemini,
sobre as fontes, nos moldes da G6.

**O que fica registrado** em `revisao/AAAAMMDD/`:
- `resposta.md`, com o status de cada achado;
- `veredito_2.json` e `veredito_3.json`, as rodadas 2 e 3;
- `divergencias.md`, o que vai para você.

A sua decisão entra no `estado.yaml` com a data e vira decisão travada. Achado confirmado
que se repete de um plano para outro vira verificação na bateria, que é o ciclo que o
método já usa.

---

## 5. Calibrar antes de confiar

Já existe um gabarito: o **`redacao_03`**.

- `dados/enviado_20260903.md` é a versão que foi ao professor. Não tem CPF.
- A devolutiva de 05/09 trouxe 35 comentários e 130 marcas, mapeados item a item em
  `apontamentos_professor.md`, seções A a G.
- Ela não serve para conferir o Gemini, porque o professor marcou estrutura e julgamento,
  não lastro contra a norma. Para o Gemini há um segundo gabarito: os seis achados
  confirmados da conferência de 01/09, registrados em `estado.yaml`.

**O ensaio:**

1. Rodar o Astra e o Gemini sobre o enviado de 03/09, sem a devolutiva no pacote.
2. Medir, para cada um, quantos apontamentos do professor pegou e quantos achados que não
   se confirmaram trouxe.
3. Separar o resultado por classe de erro: as doze da leitura de entrega.
4. Ajustar os papéis pelo que se medir, não pelo benchmark do fabricante.

Se um revisor não pegar nada que a devolutiva pegou, ele não entra no método. Assim o custo
vira medida.

---

## 6. Custo e limites

- **Astra:** sai da cota do seu plano do ChatGPT pelo Codex, não de cobrança por API. Um
  "ok" gastou 14 mil tokens, só com a instrução do sistema. Uma rodada de quatro passadas
  em `xhigh` deve ficar entre centenas de milhares e um milhão de tokens; isso a calibração
  mede.
- **Gemini Notebook:** a cota se renova a cada 5 horas, com um teto semanal, desde
  02/09/2026. São sete consultas mais as provas da G6.
- **Os dois mandam o documento para fora: OpenAI e Google.** Você deu autorização
  permanente em 11/10/2026, com uma condição: o pacote tem de passar na checagem de CPF e
  CNS. Se a checagem acusar dado pessoal, o pacote não sai.

---

## 7. Onde mora, se aprovado (no `main`)

| arquivo | o que guarda |
|---|---|
| `metodo/revisao/externa.md` | o método comum: os vieses, o pacote cego, a independência, a triagem, o registro e a calibração |
| `metodo/revisao/astra.md` | o comportamento do Astra: comando, instrução, passadas A1 a A4 e esquema |
| `metodo/revisao/gemini.md` | o comportamento do Gemini: caderno, instrução, G1 a G7 (G1 a G3 e G5 apontam para `plano/conferencia.md`) |
| `.claude/agents/revisor-astra.md` e `revisor-gemini.md` | os agentes, sem regra própria; entram na tabela do README |
| `.claude/commands/revisao.md` | o `/revisao`: chama os dois em paralelo e faz a triagem (um agente não abre outro) |
| `ferramentas/pacote_revisao.py` | monta o pacote, mascara CPF e CNS, grava o manifesto e para se sobrar dado pessoal |
| `ferramentas/conferir_revisao.py` | confere o JSON: o trecho citado existe literalmente no documento e na fonte; na resposta, todo `aceito` e todo `contestado` têm fonte; no veredito, todo achado da rodada 1 tem um |
| `metodo/revisao/esquemas/` | os três formatos: o achado, a resposta e o veredito |
| `metodo/plano/conferencia.md` | a quarta conferência passa a ser "revisão externa", e aponta para `revisao/` |
| `metodo/pre_plano/conferencia.md` | ganha a revisão externa antes do envio |
| `LEIA.md`, `MUDANCAS.md`, `README.md` | a lista, a linha de origem e a tabela dos agentes |

**O resultado de cada rodada** fica em `planos/redacao_NN/revisao/AAAAMMDD/`:
`manifesto.md`, `astra.json`, `gemini.json` e `triagem.md`. O `estado.yaml` leva o
resumo, com quantos achados de cada revisor foram confirmados. Com o tempo, isso diz qual
deles acerta o quê.

**A ordem:**

1. as duas ferramentas, com os testes;
2. o método, os agentes e o comando;
3. a calibração com o `redacao_03`;
4. o ajuste dos papéis;
5. o primeiro uso de verdade, no `redacao_06`;
6. a versão manual para a equipe: os mesmos prompts, para colar no ChatGPT e no Gemini
   pela web, com o `.docx` e os PDFs anexados, sem GitHub.

---

## Fontes

- [GPT-6 Astra: Features, Benchmarks, and Pricing — DataCamp](https://www.datacamp.com/blog/gpt-6-astra)
- [Benchmarking GPT-6 Astra — Artificial Analysis](https://artificialanalysis.ai/articles/benchmarking-gpt-6-astra)
- [Gemini 4 Argon matches GPT-6 Astra and hallucinates far less — The Next Web](https://thenextweb.com/news/gemini-4-argon-artificial-analysis-gpt-6-astra-hallucination)
- [Gemini 3.5: frontier intelligence with action — Google](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-5/)
- [Gemini API release notes — Google](https://ai.google.dev/gemini-api/docs/changelog)
- [NotebookLM Is Now Gemini Notebook: 2026 Guide — Glasp](https://glasp.co/articles/notebooklm-2026)
- [NotebookLM & Gemini Notebook Limits (2026)](https://geminiomniprompts.org/blog/notebooklm-limits/)
- [LLM Evaluators Recognize and Favor Their Own Generations — Panickssery et al., NeurIPS 2024](https://arxiv.org/abs/2404.13076)
- [MLLM-as-a-Judge Exhibits Model Preference Bias](https://www.themoonlight.io/review/mllm-as-a-judge-exhibits-model-preference-bias)
