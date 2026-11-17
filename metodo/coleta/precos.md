# coleta/precos.md — os preços do objeto

Vale para as duas trilhas. No plano, é a trava F-10 da fase 0 (`../plano/procedimento.md`).
No pré-plano e no dossiê, é a conta que diz se o objeto se paga.

São dois preços diferentes, e não se misturam:

| | o que é | quem vê |
|---|---|---|
| **o custo de executar** | o que se paga para executar uma unidade (OCI ou exame), comparado com o valor que a unidade recebe e com o mercado | **controle interno**: não vai ao documento, nem a origem dos preços linha a linha (`../plano/procedimento.md`, regra 3) |
| **o apoio** | postos, locação e serviços que vão à planilha | o documento, sem a origem linha a linha |

Quem executa é o agente `precos` (`.claude/agents/precos.md`), ou o assistente na
conversa. O método é este arquivo; o agente não guarda regra.

*Origem: as cotações de clínicas do plano 4 (07–08/10/2026), o orçamento a 50% da OCI e a
faixa do Doctoralia do redacao_05 (07–08/10/2026), cada um feito à mão. O alinhamento com
o usuário em 09/10/2026 deu as fontes, a regra do valor pela origem do recurso e a oferta
inicial e o teto por plano. O piloto do otorrino (09/10/2026) deu os endereços e as regras
de registro. O piloto das OCI de déficit auditivo (09/10/2026) deu o
componente comum, o pacote, o "a partir de" e o que a ficha não inclui.*

---

## O que entra

1. **O valor que a unidade recebe** (lição LI-002, trava F-04): a Tabela SUS Candanga, do
   Anexo Único da Deliberação CG-SES 46/2026, qualquer que seja a origem do recurso. Está em
   `biblioteca/precos/tabela_sus_candanga/`; o README dessa pasta diz a modalidade, como
   citar e o que conferir na ficha (`ficha_sigtap.md`). Se o SIGTAP vigente da ficha for
   igual ou maior que o valor do Anexo, vale o SIGTAP. Código fora do Anexo: o SIGTAP da
   ficha (e o incremento da portaria, no exame), dizendo que o código não está na Candanga.
   Vale para a pesquisa de 01/11/2026 em diante; a anterior seguiu a regra de então
   (federal, o SIGTAP; distrital, a Candanga), e a conferência a lê assim.
2. **O que a SES-DF paga pelo mesmo procedimento:**
   - nos convênios aprovados antes da Candanga, a tabela do SIGTAP;
   - nas tabelas diferenciadas do Colegiado de Gestão: o valor SIGTAP, a complementação e o
     valor pago. São exemplos a Tabela Regionalizada SUS-DF (Deliberação 21/2023, detalhada
     pela 26/2025) e as Deliberações 17 e 52/2024 (NM-099). Procurar no SINJ por "tabela
     diferenciada" e pelo código (`normas.md`, passo 3, explica a pesquisa);
   - a Tabela SUS Candanga, que é também o valor recebido (item 1): uma linha com o valor
     do Anexo. As referências da análise comparativa de 06/08/2026 (CBHPM, Tabela SUS
     Paulista, Deliberações), quando ajudam, estão em
     `biblioteca/precos/tabela_sus_candanga/analise_comparativa_20260806/`.

   Vale o mesmo procedimento e, como referência, os componentes dele e as OCI da mesma
   linha de cuidado. A coluna "o que é" diz qual é qual. Se nada se achar, a seção diz isso,
   com onde se procurou.
3. **O mercado privado**, componente por componente: o do DF, que é a base da conta, e o
   de fora do DF, que é a base maior de custo e de preço privado. Numa OCI, os componentes
   são a composição da ficha. Quando a ficha tem alternativa (a videolaringoscopia **ou** a
   laringoscopia), pesquisam-se as duas, e só a que o plano vai executar entra na conta.
   Num exame avulso, o componente é o próprio exame.
4. **A conta:** quanto do mercado a unidade cobre, a oferta inicial e o teto em reais, e a
   margem no teto.
5. **O apoio**, só no plano. O pré-plano leva só o custo assistencial.

## As fontes do mercado

| fonte | o que dá | como |
|---|---|---|
| Doctoralia | a maior parte dos preços: consulta por especialidade e exame por serviço, com o endereço e o bairro | `https://www.doctoralia.com.br/servicos-de-tratamento/<serviço>/<cidade>` e `https://www.doctoralia.com.br/<especialidade>/<cidade>`, com `?page=N`. A especialidade vai com o nome que o Doctoralia usa (`otorrino`; `otorrinolaringologista` dá 404). O HTML vem pronto e o `curl` lê. A listagem traz cidades vizinhas. **"Preço não disponível"** pode vir ao lado do preço da teleconsulta: leia o preço do serviço pedido |
| Medprev | consulta e exames (audiometria, imitanciometria, BERA, pacotes) | `https://medprev.online/busca/<serviço>/?cidade=<cidade-uf>`, só no navegador embutido. O endereço de cada serviço sai da janela que abre em "Agendar pelo site". Costuma sair mais barato que o mesmo endereço no Doctoralia |
| dr.consulta e AmorSaúde | consulta e alguns exames; a AmorSaúde tem uma tabela nacional de consulta | dr.consulta pelo WebFetch; AmorSaúde pelo `curl`. As unidades da AmorSaúde no DF não dizem a especialidade |
| sites de clínicas do DF | tabela de preços, quando publicam | busca por exame, especialidade e "Brasília" ou a Região Administrativa. No piloto de 09/10/2026 nenhum publicou |
| cotação direta | proposta por escrito, dizendo o que está incluído | **é do usuário ou da equipe**: o agente não telefona, não manda mensagem, não preenche formulário |

**Os nomes dos serviços no Doctoralia** variam, e o mesmo exame aparece com vários. Os do
otorrino e da audiologia, em 09/10/2026: `consulta-otorrinolaringologia`,
`primeira-consulta-otorrinolaringologia`, `videolaringoscopia`, `videofaringolaringoscopia`,
`nasofibrolaringoscopia`, `laringoscopia`, `audiometria`, `audiometria-tonal`,
`audiometria-tonal-e-vocal`, `impedanciometria`, `imitanciometria`,
`audiometria-e-imitanciometria`, `audiometria-tonal-vocal-srt-impedanciometria`, `peate-bera`,
`exame-bera`, `exame-bera-adulto` e `bera-sem-sedacao`.

**O acesso ao SINJ** (a pesquisa, o texto e o que fazer quando o firewall bloqueia) está em
`normas.md`, passo 3.

**Não deram preço no piloto de 09/10/2026:**
- a Rede D'Or, que manda telefonar;
- o TuaSaúde, que lista sem preço;
- os laboratórios, que não fazem exame endoscópico;
- a Clínica Popular da Família e a Doutor Certo, sem preço de otorrino;
- média nacional publicada não se achou.

**O canal muda o preço.** O mesmo endereço cobrou R$ 125 pela Medprev e R$ 300 pelo
Doctoralia. O preço de lista não é o piso da negociação, e a cotação direta continua
necessária: a seção "O que falta" diz quais pedir.

## As regras

- **Todo preço tem fonte, endereço e data.** Preço sem endereço só entra como cotação, e a
  cotação cita o documento.
- **O tipo do preço se registra como veio:** `fixo`, `a partir de`, `faixa mín`,
  `faixa máx` ou `cotação`. "A partir de" é o mínimo daquela fonte, não o preço.
- **O preço do DF é a base da conta.** A linha diz a Região Administrativa ou o bairro.
- **O preço de fora do DF entra também, para ampliar a base** de custo e de preço privado:
  outras capitais (São Paulo, Goiânia, Belo Horizonte, Rio de Janeiro) e médias nacionais
  publicadas. A linha diz `fora do DF: <cidade>/<UF>`. Ele tem resumo à parte, e só entra na
  conta do componente que não tem preço no DF; a linha da conta diz a base usada.
  *Origem: usuário, 09/10/2026 — "às vezes é bom para ter uma base maior de custo e preço
  privado".*
- **O que o preço inclui** se escreve: consulta com o exame, laudo, retorno. Preço que
  junta dois componentes vale para os dois, e a linha diz isso.
- **Preço com mais de 180 dias** na data da pesquisa se pesquisa de novo.
- **A fonte é o estabelecimento ou a plataforma, e o nome do profissional não entra.**
  Escreve-se `<plataforma>: <estabelecimento>, <endereço comercial>`. Quando o
  estabelecimento tem o nome do profissional, escreve-se `estabelecimento com o nome do
  profissional (omitido)`. Endereços de listagem, não de perfil.
- **Um preço por estabelecimento, componente e base: o menor.** Os outros do mesmo lugar
  vão para a coluna "inclui". O mesmo estabelecimento com dois nomes, ou dois profissionais
  no mesmo endereço, contam uma vez. A faixa dá duas linhas, o mínimo e o máximo.
- **O nome do mercado não é o da tabela.** O componente se escreve com o nome da ficha, e o
  nome do anúncio vai para "inclui": por exemplo, nasofibrolaringoscopia vai para a
  laringoscopia. A seção 7 diz cada correspondência, para conferir no SIGTAP.
- **Sai o preço que não é do componente:** a teleconsulta, quando a ficha pede consulta
  presencial; outra especialidade; o erro evidente, como R$ 2,00. A seção 7 diz quantos
  preços saíram e por quê.
- **A conta soma uma unidade de cada componente.** O retorno que a ficha admite não se soma
  de novo.
- **O componente comum a várias OCI se registra uma vez**, com os códigos na mesma célula
  (`09.04.01.001-5, 09.04.01.002-3`). O resumo e a conta continuam um por código.
- **O preço de pacote** (dois componentes juntos) tem linha própria, com `na conta: não`. A
  conta soma os avulsos. O pacote fica para a negociação.
- **O "a partir de" entra no resumo como o preço daquela fonte**, porque é o menor que ela
  cobra. Se o mínimo do componente for um "a partir de", a seção 5 diz qual seria o mínimo
  só com os preços fixos.
- **O mínimo da APAC vai ao lado da descrição inteira.** A OCI fecha com os obrigatórios e
  uma consulta ou teleconsulta (SAES 2.331/2024, art. 7º: ao menos dois secundários, um
  deles a consulta). Sem obrigatório, entram a consulta e o componente mais barato. No
  resumo, a coluna `na conta` diz `sim, obrigatório` e `sim, consulta` nesses componentes,
  e a conta traz `mínimo da APAC` e `cobertura APAC` ao lado da descrição inteira. O custo
  real fica entre os dois, conforme a parte dos pacientes que precisar dos compatíveis.
- **A APAC num só prestador.** O mínimo de cada componente vem de um lugar diferente, e
  nenhum lugar faz tudo por aquela soma. Abaixo da conta, a seção 5 diz, para cada código,
  o prestador do DF que faz a APAC mínima inteira e por quanto (`APAC num só prestador:
  <estabelecimento>, R$ ...`), ou que nenhum faz. É a primeira cotação a pedir.
- **Preço fraco se marca.** Na APAC mínima, o componente com um só preço no DF, sem preço
  no DF ou cujo mínimo é um "a partir de" vai para a seção 5 como `preço fraco`, com o
  motivo. A cobertura que depende dele não decide sozinha.
  *Origem: o redacao_08, 22/10/2026. O agente fez a conta do mínimo da APAC por conta
  própria, e a cobertura de 105% da cintilografia vinha de um pacote de São Paulo e de um
  "a partir de" nacional, sem marca no comparativo.*
- **Executa quem a ficha admite** (CBO): no exame audiológico, o fonoaudiólogo conta.
- **Fica fora o que a ficha não inclui:** a sedação, a variante de outro procedimento (no
  potencial evocado, entra só o de curta latência, o BERA) e o exame ocupacional.
- **Norma que manda pagar pelo SIGTAP sem trazer tabela** entra na seção 2 com o avulso do
  SIGTAP, e a coluna "o que é" diz isso. **Código impresso que não bate com o nome no SIGTAP**
  entra como está impresso, e a seção 7 aponta a diferença.
- **A tabela nacional de uma rede** se marca `fora do DF: Brasil (tabela nacional)`.
- **Fora do DF, uma ou duas páginas de listagem por componente e por capital bastam.**
- **A oferta inicial e o teto mudam de plano para plano.** São decisão do usuário e se
  registram aqui, com a data, como percentual do valor que a unidade recebe. Sem decisão,
  a conta diz "a definir".
- **No apoio,** o nome e o preço de cada posto vêm de `biblioteca/precos/cargos_no_acervo.md`.
  A locação e o serviço levam três orçamentos (portal imobiliário, preço por consultório ou
  por m²), e o unitário sai da pesquisa, nunca de um total fixado antes (LI-020, LI-021).

## O que sai

`planos/redacao_NN/dados/precos.md`, um arquivo por plano, refeito a cada pesquisa (o
histórico fica no git). O comparativo de mercado que algum `dados/valor_unitario.md`
antigo traga passa para cá: lá fica só o valor e a fonte.

```
# Preços — <objeto>

**Controle interno: não vai ao documento.**

Plano: planos/redacao_NN/ · Pesquisado em DD/MM/AAAA · Origem do recurso: federal
Oferta inicial: 50% · Teto: 70% · decisão do usuário em DD/MM/AAAA

## 1. Valor que a unidade recebe

| código | nome | valor | fonte |
|---|---|---|---|
| 09.04.01.003-1 | OCI ... | R$ 393,55 | SIGTAP 09/2026, `dados/fontes/sigtap_0904010031_092026.md` |

## 2. O que a SES-DF paga

| código | fonte | valor | o que é |
|---|---|---|---|

## 3. Mercado privado

| código | componente | fonte | endereço | data | local | preço | tipo | inclui |
|---|---|---|---|---|---|---|---|---|

## 4. Resumo do mercado

| código | componente | base | na conta | preços | mínimo | mediana | máximo |
|---|---|---|---|---|---|---|---|
| 09.04.01.003-1 | videolaringoscopia | DF | sim | ... |
| 09.04.01.003-1 | laringoscopia | DF | não (alternativa à videolaringoscopia) | ... |

## 5. A conta

| código | base | valor recebido | mercado mínimo | mercado mediana | cobertura | mínimo da APAC | cobertura APAC | oferta inicial | teto | margem no teto |
|---|---|---|---|---|---|---|---|---|---|---|

- 09.04.01.003-1: APAC num só prestador: <estabelecimento>, R$ ... (ou: nenhum prestador do DF faz a APAC mínima inteira)
- preço fraco: <componente>, um só preço no DF

## 6. Apoio

| posto ou serviço | preço | fonte | data |
|---|---|---|---|

## 7. O que falta
```

**As contas, que a conferência refaz:**
- o resumo de cada componente se faz por base, `DF` e `fora do DF`: quantos preços, o
  mínimo, a mediana e o máximo;
- a coluna `na conta` diz `sim` ou `não`, igual nas duas bases do mesmo componente;
- o mercado de um código é a soma dos componentes `na conta: sim`: soma dos mínimos e
  soma das medianas. Cada componente usa o resumo do DF; o de fora do DF, só se o
  componente não tem preço no DF. A coluna `base` da conta diz `DF`, `DF e fora do DF` ou
  `fora do DF`;
- a cobertura é o valor recebido dividido pelo mercado mínimo, em percentual inteiro;
- o mínimo da APAC é a soma dos mínimos dos componentes `sim, obrigatório` e `sim,
  consulta` (com menos de dois, mais o componente `sim` mais barato), e a cobertura APAC é
  o valor recebido dividido por ele;
- a oferta inicial e o teto são os percentuais aplicados ao valor recebido;
- a margem no teto é o valor recebido menos o teto.

Sem oferta e teto decididos, as três últimas colunas dizem `a definir`. No pré-plano, a
seção 6 diz `Não se aplica: o pré-plano leva só o custo assistencial.`

## O que os preços não decidem

- **O valor unitário do documento** é o da tabela pela origem do recurso, nunca o mercado.
  O mercado diz se a unidade se paga e se a oferta é crível.
- **O percentual do teto** não aparece na conversa com a clínica nem no documento.
- **A escolha do objeto** é do usuário. Os preços entram no dossiê como uma das partes.

## Conferência

```bash
python3 ferramentas/conferir_precos.py planos/redacao_NN/dados/precos.md
```

| | confere |
|---|---|
| A | o cabeçalho: título, a marca de controle interno, a data da pesquisa e a origem do recurso |
| B | o valor recebido pela origem: emenda federal cita o SIGTAP e bate com a ficha citada; emenda distrital cita a Tabela SUS Candanga |
| C | a seção do que a SES-DF paga: linhas com código, valor e fonte, ou a frase de que nada se achou; cada código da seção 1 aparece nela |
| D | cada preço do mercado: código, componente, fonte, endereço ou cotação, data, preço em reais e tipo; ao menos um preço por código; sem nome de profissional no estabelecimento; a mesma fonte uma vez por componente e base |
| E | o local de cada preço: no DF, ou marcado fora do DF |
| F | o resumo refeito a partir das linhas, por base, e a coluna `na conta`; a alternativa aponta para um componente que entra na conta |
| G | a conta refeita a partir do resumo, da oferta e do teto, com a base usada |
| H | nenhum preço com mais de 180 dias, nem com data depois da pesquisa |
| I | o apoio: preço, fonte e data em cada linha; três orçamentos na locação e no serviço, ou `pendente`; `Não se aplica` no pré-plano |
| J | nas pesquisas a partir de 25/10/2026: o mínimo da APAC e a cobertura APAC refeitos, a APAC num só prestador de cada código e cada preço fraco da APAC mínima marcado |
