# Calibração da revisão externa — redacao_03, 11/10/2026

O primeiro teste da revisão externa (`metodo/revisao/externa.md`). O documento é a versão
do `redacao_03` enviada ao professor em 03/09/2026 (`dados/enviado_20260903.md`). O
gabarito é a devolutiva dele de 05/09, lida item a item em `apontamentos_professor.md`.

## O gabarito

São 40 apontamentos na devolutiva, e **31 entram no gabarito**: os que o professor marcou
e que a nossa leitura confirmou como defeito. Ficam fora nove:
- D12: a frase do CPF estava certa;
- D16: o "branco" que pode ser descuido;
- F6 e F10: os "azuis" não decifrados;
- F9: a troca de cargo, que é preferência;
- D8: a dúvida era do usuário, não marca do professor;
- D3 a D7 contam como **um** (a subseção 5.9 inteira).

**Ressalva:** as doze perguntas da leitura de entrega nasceram desta devolutiva, e as
classes das passadas de diligência (A3, A6, G5, G9) vêm dela. A taxa de acerto aqui é
otimista. O teste de verdade é a próxima devolutiva.

**A conferência de 01/09 não serve de gabarito para o Gemini.** Os seis achados dela foram
corrigidos antes do envio de 03/09, então não estão no texto que ele leu.

## O Astra (GPT-6 Astra, esforço high), passadas A1 a A4

- 18 achados em menos de 3 minutos por passada, que rodaram em paralelo.
- 240 mil tokens no total.
- **Todas as 18 citações conferem** na máquina.

### O que ele acertou do gabarito

| gabarito | o que o professor marcou | o achado | |
|---|---|---|---|
| A3 | "duas regras operacionais": primeira quinzena e laudo em 15 dias (E1, régua) | AST-A3-01 | pegou |
| A5 | 2.5, a origem territorial dos usuários (E7, compromisso) | AST-A3-04: os polos "sem deslocamento a outro quadrante" | pegou, pelo outro lado da mesma promessa |
| B3 | "o que o recurso disponível compra" (E10, registro) | AST-A3-06 | pegou |
| D11 | a memória de tempos da coordenação, com números sem fonte (E3) | AST-A1-02 e A1-03 | pegou |
| D15 | metas de ≥ 95% nos indicadores (E1) | AST-A3-02 | pegou |
| D18 | I-06 com 100% ± 15% (E1) | AST-A3-03 | pegou |
| D13 | a tabela de atividades de terceiros (E12) | AST-A2-02: o laboratório contratado contra "a execução assistencial não é subcontratada" | parcial: outra contradição na mesma tabela |
| E2 | a parcela do mês 10 sem produção (E9) | AST-A2-03 e A2-04: o mês 10 contra a Meta 2 e contra a busca ativa | parcial: a mesma ferida, vista pela meta |
| A4 | a faixa etária afirmada por analogia (E4) | AST-A3-07: "maiores de 18" contra a ficha (mínimo de 18 anos) | parcial |

**Pegou 6 dos 31 e tocou mais 3** (19% firme, 29% com os parciais).

### O que ele achou e o professor não marcou

| achado | verdade? |
|---|---|
| AST-A1-01 e A2-01: "12.967,03"; a conta dá 12.967,29 | **erro real**, sem efeito no inteiro |
| AST-A1-04 e A2-06: "Os três riscos altos", mas a matriz tem quatro (R-02, R-06, R-09, R-11) | **erro real**, conferido na matriz |
| AST-A4-01: a sedação conduzida pelo endoscopista, contra a recomendação do art. 5º da Res. CFM 2.174/2017 | plausível: é recomendação, não proibição. **O Gemini achou o mesmo, sozinho (G1)** |
| AST-A3-05: o R-06 diagnostica a inviabilidade por polo e não fecha | plausível (argumento aberto) |
| AST-A2-05: a parcela "na celebração" contra "precedem qualquer receita" | **leitura errada**: a frase justifica a parcela antecipada |

**A precisão:** dos 16 achados distintos, 15 são verdadeiros ou plausíveis, e um é leitura
errada. **Nenhum é inventado.**

### O que ele não pegou

- **A memória e a voz:** A1, A2 e D8 (memorial), D9, F1, F2, F5 e F8 (ausência e defesa
  antecipada), D3 a D7 (lugar) e F3 e F4 (registro). A A3 devolveu vazias as classes
  `memorial`, `ausencia` e `lugar`: oito classes numa passada só é demais para ele.
- **A estrutura contra os aprovados:** C1 (as condições de partida, que nenhum aprovado
  tem), F11 (a planilha única) e G1 (a ordem das seções).
- **Os totais da fila:** B1 (24.868 contra 29.528), embora a A1 pedisse "dois totais do
  mesmo universo".
- **O resto:** B2 (fechar a justificativa), D2 (contrarreferência "ao ponto de origem"),
  D14 (a meta qualitativa de 95%), D17 (I-05) e F7 (SISCAN).

### O que mudou nele por causa disto

- **A A1 nomeia as contagens** de pessoas e de fila, para pegar o B1.
- **As diligências se dividiram em duas passadas:** conteúdo (A3) e voz e lugar (A6), com
  "liste todos os casos".
- **Nasceu a A7,** a estrutura contra os aprovados, para C1, F11 e G1. Ele lê um arquivo
  por vez, que é o que o Gemini não faz.
- **A segunda rodada (A1 a A7) não chegou a rodar:** o plano do ChatGPT bateu no limite de
  uso, da conta inteira e não só do Astra, com volta às 19h09. Com a cota curta, as
  diligências de leitura passaram ao Gemini (G5 e G9), e o Astra fica com A1, A2 e A7. A
  A3, a A6 e a A4 continuam no método como opcionais, para quando sobrar cota.

## O Gemini (Gemini Notebook)

Um caderno novo, com o documento, 31 normas e a ficha. Rodaram a G1, a G2, a G3, a G5, a
G9 e a G7, cada uma em 1,5 a 3 minutos.

- 51 achados: **37 com citação literal, 13 aproximadas** (tabela achatada) e **1
  derrubado** pela máquina.
- A G4 (obrigações) não chegou a rodar: a cota do plano do Gemini acabou antes. Nessa hora
  todos os cadernos pararam de responder, inclusive o de teste, com uma fonte só.

### Os defeitos do transporte que a calibração achou, todos corrigidos

| o que aconteceu | a correção |
|---|---|
| Com os cinco aprovados no caderno, a G1 tomou um aprovado de oftalmologia pelo documento em análise. Os seis achados eram sobre outro plano, sem nenhuma citação. A conferência por máquina derrubou todos | os aprovados não sobem; toda consulta leva `--source-ids` |
| O Google troca o título "nome.md" por "[suspicious link removed]" | títulos sem extensão; a fonte sai da marca de citação ou do conteúdo |
| No formato rígido de resposta, o caderno não devolve a marca de citação | a fonte se acha pelo conteúdo: o trecho literal em todo o pacote |
| Ao copiar uma tabela, o Gemini troca as barras por dois-pontos e vírgulas | a conferência "aproximada", com 85% das palavras na ordem |
| O título do bloco em negrito (`**### ACHADO**`) se perdia | o leitor aceita as três formas |

### O que ele acertou do gabarito

| gabarito | o achado | |
|---|---|---|
| A1 memorial da NT 3/2025 | GEM-G9-01 | pegou |
| A3 laudo em 15 dias | GEM-G5-05 | pegou |
| A4 faixa etária: o "legalmente incapaz" contra o mínimo de 18 anos da ficha | GEM-G5-08 e G7-03 | pegou, pelo trecho da 5.3 que a devolutiva mandava corrigir junto |
| B3 "o recurso compra" | GEM-G9-13 (e G9-14, "envelope") | pegou |
| C1 as condições que precedem a assinatura | GEM-G5-01 | pegou: **a régua mais cara, que o Astra não viu** |
| D10 e D11 a memória de tempos | GEM-G9-19 e G9-20 | pegou |
| D14 a meta qualitativa de 95% | GEM-G5-02 | pegou |
| D18 I-06 com 100% ± 15% | GEM-G5-04 | pegou |
| E2 a parcela do mês 10 sem produção | GEM-G5-11 (e G7-08) | pegou |
| F2 a Portaria 4.282 citada para os 627% | GEM-G5-09: "a portaria não estabelece esse percentual ou valor" | pegou |
| F3 "perguntando de cada um qual custo" | GEM-G9-15 | pegou |
| F5 "Não há rubrica de sistema" | GEM-G9-08 | pegou |
| F8 "A planilha é integralmente de pessoal" | GEM-G9-09 | pegou |
| A2, A5, B2, D13, F1 | G9-02, G5-07, G5-12, G7-06, G9-10 | parciais |

**Pegou 14 dos 31 e tocou mais 5** (45% firme, 61% com os parciais).

### O que ele trouxe e não serve

- **Os campos "[preencher]"** (G5-10, G7-01, G7-04): o modelo é preenchido pelo proponente
  e não é defeito. A instrução do caderno e a do Astra passaram a dizer isso.
- **As quatro omissões de faturamento da G2:** são verdadeiras, mas explicar a regra ao
  parecerista é o memorial que a devolutiva corta. A G2 passou a pedir só contradição.
- **As condições da G3** (a climatização da sala de processamento, a capacitação da
  equipe): empurram o documento para a régua da 4.2. Vão para o controle interno.
- **A G3-06** atribuiu ao executor a obrigação do gestor (a lista de espera por CPF é do
  gestor, art. 16 da Portaria SAES/MS 1.640/2024). A G3 passou a pedir só o que cabe a quem
  executa.
- **A G9-18** pôs como "detalhe" a 5.10, que o professor deixou inteira sem marca.

**A precisão:** dos 51, cerca de 35 são verdadeiros e úteis, perto de 10 são fracos ou
errados, e 6 são verdadeiros mas empurrariam o documento para o erro (memorial ou régua). A
triagem existe para esses.

## Os dois juntos

| | Astra | Gemini | os dois |
|---|---|---|---|
| gabarito pego, firme | 6 | 14 | **16 de 31 (52%)** |
| com os parciais | 9 | 19 | **20 de 31 (65%)** |
| achados | 18 | 51 | |
| citação que não confere | 0 | 1 | |
| verdadeiro e útil | 15 de 16 distintos | ~35 de 51 | |
| erro real fora do gabarito | 2 (o quociente; os "três" riscos altos que são quatro) | 0 | |

**Os dois se completam, e por isso ficam os dois.**
- O Astra é preciso e bom de conta e de contradição interna. Achou dois erros reais que nem
  o professor nem a bateria pegaram, e **os dois continuam na versão atual do plano**.
- O Gemini cobre a leitura: régua, memorial, ausência, registro. Pegou mais que o dobro do
  gabarito.
- **A concordância independente** aconteceu uma vez: a sedação conduzida pelo endoscopista
  contra a Res. CFM 2.174/2017, achada pelos dois sem que um visse o outro (AST-A4-01 e
  GEM-G1-01).

**O que nenhum dos dois pegou** (11):
- B1, os totais da fila;
- D2, a contrarreferência "ao ponto de origem";
- D3 a D7, a subseção 5.9 no lugar errado;
- D9, a defesa antecipada da equipe;
- D17, o I-05;
- E1, o "e rampa";
- F4, o parágrafo de quinze itens;
- F7, o SISCAN;
- F11, a planilha única;
- G1, a ordem das seções.

F11, G1 e C1 são da A7, a estrutura contra os aprovados, que não rodou por falta de cota.

## O que ficou pendente antes da decisão

- **A A7 e a A6 do Astra,** quando a cota do ChatGPT voltar (19h09 de 11/10/2026).
- **A G4 do Gemini e a tréplica dos dois** (A5 e G8), quando as cotas voltarem. A resposta
  aos achados do Astra já está escrita (`resposta_astra.json`) e passou na conferência, e a
  rodada 2 vai usar a versão atual do `plano.md` do `redacao_03` como documento corrigido.
- **O teste de verdade,** que é a próxima devolutiva de um plano revisado assim.

## O Claude cego, o teste de controle (11/10/2026, à tarde)

**A pergunta do usuário:** valeu a pena consultar outros modelos, ou basta um Claude que
não conheça a conversa? O teste respondeu com:
- **o mesmo pacote,** copiado para uma pasta isolada, sem o manifesto de origem;
- **as mesmas perguntas,** na versão exata que o Astra e o Gemini responderam;
- **dois subagentes Claude sem a conversa:** um com as perguntas do Astra (A1 a A4) e
  outro com as do Gemini (G1, G2, G3, G5, G9, G7);
- **o mesmo gabarito e a mesma regra de pontuação para os quatro revisores:** o trecho cai
  na faixa de linhas do apontamento **e** a classe do problema é compatível
  (`gabarito.json`).

**O isolamento foi conferido nos registros:** nenhum dos dois leu o gabarito, a devolutiva
ou o relatório. Durante o teste o gabarito ficou alguns minutos dentro da pasta cega, e foi
retirado; os registros mostram que não foi aberto.

| | Astra | Gemini | Claude cego (A) | Claude cego (G) | **os dois de fora** | **os dois Claude** |
|---|---|---|---|---|---|---|
| gabarito pego, firme (de 31) | 8 | 14 | 15 | 23 | **18 (58%)** | **23 (74%)** |
| achados | 18 | 51 | 61 | 174 | 69 | 235 |
| citação que não confere | 0 | 1 | 0 | 0 | | |
| tempo de relógio | 3 min (em paralelo) | ~25 min (com a subida) | 21 min | 30 min | | |
| custo | a cota do ChatGPT de 5 h, inteira | a cota do Gemini | 300 mil tokens | 500 mil tokens | | |

*Nesta tabela a contagem do Astra subiu de 6 para 8 e a do Gemini ficou em 14, porque a
regra de pontuação passou a ser uma só para os quatro, por faixa de linha e classe.*

**O que o teste mostrou:**
- **Os de fora não acrescentaram nenhum apontamento do gabarito que o Claude cego não
  tenha achado.** O Claude cego achou mais cinco que nenhum de fora achou: B1 (os totais da
  fila), D1 (a quinzena na 5.2), D17 (o I-05), F1 (a "aula de economicidade") e a
  contradição da plataforma de teleconsulta com a 8.3 (D13, pelo lado que o professor viu).
- **Os erros reais fora do gabarito também foram achados pelo Claude cego:** o quociente
  12.967,29, os "três" riscos altos que são quatro e, a mais, o R-05 classificado "médio"
  com a mesma probabilidade e o mesmo impacto que levam o R-02 a "alto". A sedação contra a
  Res. CFM 2.174/2017 também.
- **A precisão é parecida:** numa amostra de 15 dos 174, uns 12 são verdadeiros ou
  plausíveis. **O preço é o volume:** 111 dos 174 são "ajuste", com muita repetição da mesma
  falha em seções diferentes. Sem um limite de achados, a triagem fica cara.
- **Não apareceu a leniência que se temia:** o Claude cego foi mais duro com o texto, que
  sessões anteriores do Claude ajudaram a escrever, do que os de fora.

**Um achado fora do gabarito, resolvido pelo usuário:** o art. 93 da Portaria GM/MS
10.297/2026 veda usar emenda individual "para custear despesas relacionadas ao pagamento de
pessoal da saúde", e a planilha de apoio do plano é toda de pessoal (CLG-G1-06 e G7-02).
**Segundo o usuário (11/10/2026), a vedação é para o pessoal da SES, não para emenda que
contempla convênio.** A leitura bate com a prática: os cinco aprovados pagam postos de
pessoal com emenda. É o tipo de achado que a triagem fecha como `contestado`, com a fonte,
ou como `decisao_do_usuario`.

## A decisão (11/10/2026)

O usuário decidiu:
- **o Claude cego é o padrão** (`metodo/revisao/claude.md`);
- **a versão final passa uma vez pelo Sol**, do ChatGPT (`metodo/revisao/chatgpt.md`);
- **o Gemini fica opcional;**
- **nada de testes novos por enquanto.**

Ficaram sem rodar: a A7 (a estrutura contra os aprovados), a G4, a tréplica e o Sol. Rodam
no primeiro uso de verdade.

**As ressalvas:**
- É um documento só, e um gabarito só.
- As perguntas vêm da mesma devolutiva.
- O Claude cego rodou no modelo mais forte da casa, e o modelo do Gemini Notebook não é
  conhecido.
