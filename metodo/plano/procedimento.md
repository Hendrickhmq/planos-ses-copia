# plano/procedimento.md — como se produz um plano de trabalho

**O que o plano é.** O plano de trabalho instrui o instrumento já decidido: diz **com
quem** se executa e **quanto custa cada coisa**. Quem lê é o parecerista, que
verifica se a proposta é executável e se o preço é aceitável. Tudo nele é calculado, e
tudo o que se afirma vira obrigação aferível na prestação de contas. Se o documento
serve para a SES decidir *se* e *como* fazer o projeto, ele não é plano, é pré-plano:
ver `../pre_plano/procedimento.md`.

**Valem também as regras de `../comum.md`.** Este arquivo não as repete.

---

## As oito fases

Nenhuma se pula. A ordem existe porque cada fase só é possível depois da anterior.

| # | fase | entra | sai | pronto quando | quem confere |
|---|---|---|---|---|---|
| **0** | Travas | o termo, a emenda, a ficha SIGTAP, a fila | `dados/envelope.md`, `dados/valor_unitario.md`, `dados/fontes/` | as onze travas abaixo têm resposta com fonte | H, N, V, W |
| **1** | Ancoragem | as decisões do usuário e os parâmetros que ele não sabe | `dados/parametros_tecnicos.md` | cada parâmetro tem fonte com data, ou é lacuna com dono | comum, regra 4 |
| **2** | Fluxo | os parâmetros da fase 1 | o percurso do usuário, passo a passo, na seção 5 | cada passo diz o que acontece, quem faz, quanto tempo, onde e o que se registra | leitura |
| **3** | Planilha de baixo para cima | o fluxo | a planilha da seção 9 | toda linha aponta um passo do fluxo; o quantitativo é o piso | A, B, C, X |
| **4** | Redação | fases 0–3 | `plano.md`, por rodadas | as 9 seções existem, na voz de comum, regra 9 | J, K, L, O, P, Q, U |
| **5** | Poda normativa | `plano.md` | o mesmo, com as citações que sobreviveram | cada citação passou pelas duas perguntas de comum, regra 7 | M |
| **6** | Conferência | `plano.md` e `estado.yaml` | relatório das baterias, checklist, revisão cega (`../revisao/cega.md`) | as duas baterias em 100% | `conferencia.md` |
| **7** | Leitura de entrega | o documento conferido | nenhuma classe de erro em aberto | as doze perguntas respondidas | `leitura_de_entrega.md` |

Depois da fase 7, a **triagem das lições** do plano (ver "Ao fechar", no fim).

---

## Fase 0 — Travas

Nada se escreve antes disto. Se o objeto ainda não está escolhido, o dossiê vem antes
(`../coleta/dossie.md`).

| # | dado | fonte | onde fica | lições |
|---|---|---|---|---|
| F-01 | emenda: número, autor, RP, valor e funcional programática | usuário / termo | `estado.yaml`, seção 1.2 | LI-027 |
| F-02 | valor global, vigência e data de início **do termo** | termo de convênio | `estado.yaml` | LI-029 |
| F-03 | código de cada procedimento e a **ficha do SIGTAP da competência vigente** (comum, regra 3) | SIGTAP, pelo método de `../coleta/ficha_sigtap.md` (agente `ficha-sigtap`) | `dados/fontes/sigtap_<código>_<competência>.md` | LI-001, LI-003, LI-006 |
| F-04 | valor unitário: a **Tabela SUS Candanga**, na emenda federal e na distrital, na modalidade do objeto (SIA ou SIH); se o SIGTAP vigente for igual ou maior, o SIGTAP. Código fora do Anexo: da OCI, o total ambulatorial do SIGTAP; do exame, o SIGTAP mais o incremento da portaria | o Anexo Único da Deliberação CG-SES 46/2026, em `biblioteca/precos/tabela_sus_candanga/`; a ficha e a portaria | `dados/valor_unitario.md` | LI-002, LI-040 |
| F-05 | fila regulada: total, data da extração, espera, distribuição por Região de Saúde | Mapa Social da Saúde, pelo método de `../coleta/mapa_social.md` (agente `mapa-social`) | `dados/fontes/mapa_social_<data>.md` | LI-009, LI-010 |
| F-06 | CNES de **cada** polo conferido contra a ficha: tipo, serviço/classificação SUS, CBO, equipamento, habilitação | consulta pública do CNES | `dados/fontes/` | LI-039, LI-024 — ver `biblioteca/instrumento/enquadramento_cnes.md` |
| F-07 | direção do dimensionamento: o recurso define a fila, ou a fila define o recurso | usuário | `estado.yaml`, `origem_recurso.direcao` | regra 1, abaixo |
| F-08 | teto do apoio, pela folga entre o que o procedimento paga e o que custa | usuário, com a SES-DF | `estado.yaml`, `custo_acessorio.teto` | LI-038 |
| F-09 | parâmetros assistenciais (Anexo A do `modelo.md`) | área assistencial | `dados/parametros_tecnicos.md` | LI-014, LI-015 |
| F-10 | preços: o custo de executar comparado com o mercado (interno) e os de pessoal, locação e serviços | `biblioteca/precos/cargos_no_acervo.md` e pesquisa de mercado, pelo método de `../coleta/precos.md` (agente `precos`) | `dados/precos.md` | LI-020, LI-021 |
| F-11 | outro convênio do mesmo proponente: objeto, códigos, unidades e equipe | proponente | `pendencias.md` | LI-023 |

Também na fase 0: identificar o **proponente** e ver se existe
`biblioteca/proponentes/<nome>/`, e ver se a SES mandou **formulário** (comum,
regra 15). O que decidir vai para a chave `estrutura` do `estado.yaml` (ver
`estrutura.md`).

## Fase 1 — Ancoragem

Cada parâmetro que o usuário não souber recebe fonte com data, ou vira lacuna com
dono. Cada decisão do usuário vai a segunda opinião antes de virar texto (comum,
regra 4). Cada parâmetro vai para `dados/parametros_tecnicos.md` com a fonte e com a
alternativa descartada.

## Fase 2 — Fluxo

O percurso do usuário, da chegada à conclusão, um passo por subseção da seção 5. Cada
passo diz **o que acontece, quem faz (com o CBO da ficha), quanto tempo leva, onde e o
que se registra**. O fluxo é de onde a planilha é puxada: sem ele escrito antes, a
planilha volta a nascer com postos redondos.

## Fase 3 — Planilha de baixo para cima

**A planilha não se monta por rubrica.** Percorre-se o fluxo do atendimento, do chão
para cima, e cada passo revela o seu custo. O usuário chega, logo há recepção. Alguém
marca e remarca, logo há agendamento. Alguém lança no sistema, logo há registro. O
sistema cai, logo há TI. Quem faltou precisa ser buscado, logo há busca ativa. Posto
que não aponta passo nenhum sai.

**Os três setores:**

| setor | o que abrange | onde costuma estar |
|---|---|---|
| **técnico** | a execução assistencial propriamente dita | **quase sempre já dentro do valor do procedimento**, e por isso não se repete na planilha |
| **administrativo** | recepção, agendamento, registro, busca ativa, supervisão, TI, infraestrutura | planilha de apoio |
| **financeiro** | execução financeira, conciliação, prestação de contas | planilha de apoio |

O erro do setor técnico é sempre o mesmo: **cobrar duas vezes**. A pergunta que separa
é única: *este custo já está dentro do valor que se cobra pela unidade produzida?* Se
está, não entra. Se não está, entra com a demonstração de que não está.

**A rubrica é o último passo.** Levantados os postos pelo fluxo, eles se agrupam na
natureza de despesa que a norma admite. A rubrica justifica a *natureza* da despesa;
só o fluxo justifica a *existência* dela.

**Pronto quando:**
- cada linha aponta o passo do fluxo que a torna necessária;
- nenhuma linha recompõe custo já remunerado no valor unitário;
- quantidade e frequência derivam do volume do passo, não de arredondamento;
- `total = quantidade × frequência × valor unitário`, linha a linha;
- os subtotais fecham com os itens e o global com os subtotais;
- nome e preço de cada posto foram procurados em `biblioteca/precos/cargos_no_acervo.md`
  antes de serem inventados.

*Origem: redacao_02, 24/08/2026; o "Assistente de polo" que o acervo chamava de
Recepcionista, 02/09/2026.*

## Fase 4 — Redação, por rodadas

A ordem de escrita não é a ordem de leitura. Cada seção só nasce quando a anterior já
lhe deu o que ela precisa:

| rodada | o que se escreve | por que aqui |
|---|---|---|
| 1 | Objeto (seção 2) | tudo depende dele |
| 2 | Metas e indicadores (seção 5) | a soma das metas reconstrói o quantitativo do objeto |
| 3 | Fluxo e equipe (seção 5) | vêm da fase 2 |
| 4 | Cronograma físico (seção 6) | as etapas saem do fluxo, não de calendário genérico |
| 5 | Planilha e memória de cálculo (seção 9) | vem da fase 3 — **ponto de reabertura** |
| 6 | Cronograma de desembolso (seção 7) | as parcelas seguem a curva física |
| 7 | Riscos (seção 8) | **ponto de reabertura** |
| 8 | Justificativa e dimensionamento (seção 3) | escrita sabendo o que se vai justificar |
| 9 | Proponente (seção 4) e identificação (seção 1) | dependem do proponente e do termo |

O documento se remonta na ordem das 9 seções (`estrutura.md`) só no fim.

**Os pontos de reabertura.** O que foi aprovado não se reabre, salvo em dois momentos
declarados de antemão:
- **depois da planilha:** se o custo levantado pelo fluxo não couber no envelope, quem
  cede é o objeto ou a meta, não a planilha;
- **depois dos riscos:** risco alto sem mitigação viável é desenho errado, não risco.

**Como funciona uma rodada:**
1. **O assistente abre** com um briefing curto: o que a seção tem de provar, o critério
   de aceite, a armadilha conhecida, e perguntas numeradas, só do que depende do
   usuário.
2. **O usuário responde** o que tiver. "Não sei" é resposta válida: vira lacuna com
   dono, marcada no lugar exato do texto.
3. **O assistente escreve** a seção inteira em `secoes/`.
4. **O assistente fecha** com um quadro: em que cada afirmação se apoia, que lacunas
   nasceram e o que esta seção obriga as seguintes a respeitar.
5. **O usuário aprova, corrige ou manda refazer.** A aprovação vai para o
   `estado.yaml`, não fica na conversa.

*Origem: redacao_02, acordo de trabalho de 24/08/2026.*

## Fase 5 — Poda normativa

Cada citação passa pelas duas perguntas de comum, regra 7. A poda se faz com o
documento escrito, porque só então se vê qual seção decide.

## Fases 6 e 7 — Conferência e leitura de entrega

Em `conferencia.md` e `leitura_de_entrega.md`.

---

## As regras próprias do plano

**1. A meta é calculada, não escolhida.** O quantitativo é o **piso** da divisão
`(recurso − custo de apoio) ÷ valor unitário`. Arredonda-se para baixo porque a unidade
produzida é indivisível e o valor global não pode exceder o recurso, e por nenhuma
outra razão. Meta redonda por estética é proibida: descartar 5 OCI para fechar em
13.000 joga fora produção que o recurso comprava. A sobra é o resto da divisão e é
sempre menor que um valor unitário. Com vários códigos, a sobra fica abaixo do menor
unitário. O total nunca fecha por ajuste de uma linha elástica: a soma dá o que dá.
*Origem: redacao_03, 13.000 contra 13.005 OCI; virou a verificação C.*

**2. Não há fração de usuário, e o arredondamento depende de quem paga o erro.**
- **Capacidade** (entradas por dia, salas, postos, lugares de espera, equipamentos):
  **teto**. Arredondar para baixo promete atender quem não cabe.
- **Capacidade de um recurso** (exames por sala por dia): **piso**. Exame não se faz
  pela metade.
- **Quantitativo contratado:** **piso**, sempre (regra 1).

*Origem: regra do usuário de 05/09/2026; virou parte da D e da G.*

**3. Dependência de fonte única é controle interno.** Ela é rastreada linha a linha
(`biblioteca/precos/cargos_no_acervo.md` mostra quantos aprovados sustentam cada
preço) e define a prioridade da pesquisa de preços, mas não vai ao documento, nem a
origem dos preços linha a linha.
*Origem: redacao_02, decisão do usuário de 31/08/2026.*

**4. A margem decide onde a infraestrutura aparece.** Com margem de apoio larga, a
infraestrutura vira rubrica. Com margem estreita, ela é declarada como remunerada
dentro do valor unitário, e o risco de não caber ali entra na matriz. O motivo nunca
vai ao documento: fica em `dados/envelope.md`.
*Origem: redacao_03, decisão do usuário de 05/09/2026.*

**5. Enxuto corta volume, não raciocínio, não exigência e não campo de formulário.**
- Corta-se a norma citada por erudição, o artigo repetido, a mesma ideia dita duas
  vezes, a seção que existe para provar que o assunto foi considerado.
- Onde a seção *decide* (objeto, dimensionamento, planilha, riscos, justificativa),
  ela argumenta em prosa, e a tabela fica como apoio.
- O que a norma manda constar, consta.
- O quadro cadastral é formulário da concedente, não redação: não se corta.

*Origem: redacao_02, a v1 reprovada por "básica" em 18/08/2026; redacao_03, a
identificação de 01/09/2026.*

---

## Onde mora o estado de cada plano

```
planos/redacao_NN/
  00_metodo.md              o que difere do padrão neste plano
  estado.yaml               parâmetros, derivados, rodadas, achados, conferência
  pendencias.md             decisões a confirmar, o que falta, controle de fonte única
  licoes.md                 o que este plano ensinou, e a triagem de cada lição
  dados/envelope.md         a aritmética travada
  dados/valor_unitario.md   o unitário e sua fonte oficial
  dados/parametros_tecnicos.md   cada parâmetro com fonte e alternativa descartada
  dados/fontes/             cópias das fontes externas usadas
  secoes/                   briefings e fechamentos de rodada — não vão ao documento
  conferencia/              a bateria própria do plano, se houver (ver conferencia.md)
  plano.md                  o documento
  plano.docx                gerado por ferramentas/md2docx.js
```

O `.docx` se gera da raiz, e o título do cabeçalho sai do `estado.yaml` do plano:

```bash
npm ci                                            # uma vez por computador
npm run docx -- planos/redacao_NN/plano.md planos/redacao_NN/plano.docx
```

### As chaves do `estado.yaml` que a conferência lê

Sem elas, verificações param ou passam caladas. **Esta lista é o contrato e sai
direto do código:** `ferramentas/conferir_plano.py`, funções `carregar_parametros`,
`parametro`, `verificar_C`, `verificar_H`, `verificar_J`, `verificar_N`, `verificar_V` e
`verificar_Y`,
mais o `md2docx.js`. A bateria de um plano pode ler chaves próprias, e as declara no
`verificacoes.py` dela.

| chave | quem usa | se faltar |
|---|---|---|
| `titulo_documento` (na raiz do arquivo, com acento) | **md2docx.js** | o `.docx` não é gerado |
| `estrutura` | **J** | assume `padrao` — as 9 seções de `estrutura.md` |
| `parametros.valor_unitario.valor` | tudo | a conferência para e diz qual falta |
| `parametros.valor_unitario.por_codigo` + `metas_execucao` | plano de vários códigos: B, F, H, N | substitui o `valor` acima |
| `parametros.origem_recurso.valor` | C, H | a conferência para |
| `parametros.origem_recurso.direcao` | C | assume `recurso_define_fila` |
| `parametros.custo_acessorio.teto` | C, com `fila_define_recurso` ou `recurso_define_meta` | o teto do apoio não é conferido |
| `parametros.objeto.oci` | **N**, V | N não confere o código do objeto na fonte |
| `parametros.ficha_sigtap.situacao: dispensada` | V | V exige a ficha em `dados/fontes/` |
| `indicadores_fora_de_100` | S | exceção declarada, com motivo de mais de dez caracteres |
| `pre_plano_enviado` (caminho a partir da raiz) | **Y** | Y vira NÃO SE APLICA — o projeto não tem pré-plano |
| `pre_plano_divergencias` (`codigos`, `valor_total`, `producao`, cada um com motivo) | Y | toda divergência do pré-plano é falha |
| `vigencia_meses` (ou `vigencia_meses.valor`) | D, **F** | F acusa: os meses das parcelas não têm contra o que fechar |
| `derivados.valor_global` | **H** | H acusa a ausência |
| `derivados.quantitativo_oci` (ou `quantitativo_exames`) | **H** | idem |
| `derivados.apoio_total` | **H** | idem |
| `parametros.polos.nomes` | E, G | as duas viram NÃO SE APLICA — plano de sítio único é isso mesmo |
| `dias_uteis` | D, G | assume 21 |

O que **não** é lido, e por isso não precisa estar lá: `meses_producao`. Fica no
`estado.yaml` porque é memória da decisão.

---

## Ao fechar: a triagem das lições

Cada entendimento novo que o plano trouxe vai para o `licoes.md` dele, no momento em
que aparece, com uma pergunta: **isto muda como se faz qualquer plano?**

- **Sim:** a regra entra no padrão, no arquivo certo (`../comum.md` se vale para as
  duas trilhas, este arquivo se só para o plano), com a linha de origem, e a mudança
  se registra em `../MUDANCAS.md`. Se dá para codificar, vira verificação.
- **Só para este tipo de objeto:** vai para a biblioteca, no tema, ou para a bateria
  do plano.
- **Não:** fica no `licoes.md` do plano.

A triagem não espera o plano acabar: o entendimento geral entra no padrão quando
aparece.
