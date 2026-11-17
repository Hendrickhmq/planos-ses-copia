# PLANEJADO.md — o que foi pedido e ficou para depois

Cada item diz quando foi pedido, o que já existe e o que falta decidir. Quando um item
começa, ele sai daqui e vira método (`metodo/`), agente (`.claude/agents/`) ou ferramenta
(`ferramentas/`), no lugar dele.

---

## 1. Alerta de normas em tempo real, pelo WhatsApp

**Pedido em 09/10/2026:** um agente que avise, em tempo real, as notícias sobre portarias
e outros atos, pelo WhatsApp. Fica para mais adiante.

**A diferença para a vigia do dia 10.** A vigia (`metodo/coleta/normas.md`) é mensal:
valida cada mudança no texto da norma, registra no acervo e corrige o catálogo. O alerta
é aviso: chega no dia em que o ato sai e diz o que ele é e por que pode importar. Ele não
valida nem grava nada; a validação continua com a vigia.

**O que já existe e serve de base**
- `ferramentas/ler_dou.py` lê todo ato do Ministério da Saúde no DOU, com a edição extra,
  e separa o que toca o projeto do que é novidade. É o motor do alerta. Falta rodar
  várias vezes por dia e lembrar o que já foi avisado.
- `ferramentas/testar_ler_dou.py` testa essa classificação.

**O que falta montar**
1. **Fontes além do DOU:**
   - o DODF e o SINJ-DF, para a camada distrital;
   - as notícias do Ministério da Saúde e da SES-DF;
   - a Nota Técnica CGSI, no dia em que aparecer no FTP do DATASUS.
2. **Frequência.** O DOU sai de madrugada e a edição extra sai ao longo do dia. Ler, por
   exemplo, às 7h, às 13h e às 19h.
3. **Memória do que já foi avisado.** Cada ato do DOU tem um endereço único (o `urlTitle`).
   Guardar os já enviados evita repetir o aviso.
4. **A mensagem.** Título, órgão, a ementa em uma linha, por que importa (o motivo da
   classificação) e o link. Um resumo em linguagem simples exige um modelo de linguagem
   (API da Anthropic), com custo por chamada.
5. **Onde roda.** A tarefa agendada do aplicativo só roda com o aplicativo aberto, e por
   isso não serve para tempo real. O alerta precisa rodar fora dele, em um destes:
   - o GitHub Actions, com agendamento. O repositório é privado, e a chave do WhatsApp vai
     num segredo do GitHub;
   - o agendador do próprio Mac (launchd), que só roda com o Mac ligado.

   Antes de escolher, conferir se o in.gov.br responde aos servidores do GitHub. Daqui,
   ele recusa o urllib e só aceita o curl.
6. **O envio pelo WhatsApp.** As opções:
   - **a API oficial do WhatsApp Business (Cloud API, da Meta):** exige conta business,
     um número próprio e um modelo de mensagem aprovado para mensagens que não são
     resposta. Tem custo por mensagem enviada;
   - **a Twilio, que funciona por cima da API oficial:** é mais simples de montar, tem as
     mesmas exigências e soma o custo dela ao da Meta;
   - **serviços gratuitos de envio para o próprio número, como o CallMeBot:** são simples,
     mas não têm garantia nem suporte;
   - **bibliotecas não oficiais que imitam o WhatsApp Web:** estão descartadas, porque o
     número pode ser bloqueado.
7. **Bateria de testes, como todo agente:**
   - a classificação, que já existe;
   - a memória dos avisos, para não repetir;
   - o formato da mensagem: tamanho e link;
   - um modo de ensaio, que monta a mensagem sem enviar.

**O que decidir quando começar**
- quem recebe: só o usuário, a equipe ou um grupo;
- o que dispara aviso: só o que toca o projeto ou também as novidades. Habilitações de
  estabelecimentos de outros entes ficam de fora;
- o canal de envio e quem paga por ele;
- o horário de silêncio, e se o aviso do fim de semana espera a segunda-feira.

**Regra que já vale:** a mensagem leva só ato público. Não leva nada do Mapa Social, nem
CPF, CNS ou nome (`metodo/coleta/mapa_social.md`).

---

## 2. Precificação e dossiê do objeto — feitos em 09/10/2026

Os dois viraram método, com as decisões do alinhamento e a origem de cada uma:
- `metodo/coleta/precos.md`, com o agente `precos` e o `ferramentas/conferir_precos.py`;
- `metodo/coleta/dossie.md`, com o comando `/dossie` e o `ferramentas/conferir_dossie.py`.

O valor unitário pela origem do recurso está na lição LI-002 e na trava F-04.

**Fica para depois:**
- **No primeiro plano pela Candanga (regra de 01/11/2026):** as verificações V e W do
  `ferramentas/conferir_plano.py` conferem o valor contra o SIGTAP e precisam aceitar o
  valor da Tabela SUS Candanga.
- **O comparativo em planilha,** se for para fora.
- **A oferta inicial e o teto por OCI.** Hoje valem para o plano inteiro. O dossiê do
  otorrino mostrou coberturas muito diferentes (100%, 88% e 38%). O usuário deixou a
  discussão para depois em 10/10/2026.
- **O que faltou nos casos reais:** o usuário não lembra de cabeça; apura-se no próximo
  caso.

---

## 3. Vigia de normas: o que ainda se faz à mão

O piloto de 09/10/2026 fez estes passos sem ferramenta (`registros/vigia/vigia_2026-10-09.md`,
"O que faltou no método"). O método já diz como fazê-los. Falta automatizar:

1. **A lista dos códigos do projeto.** Ela junta o catálogo, as fichas e o `estado.yaml`
   de cada ramo e da pasta do usuário. O piloto achou 74 códigos.
2. **A Nota Técnica separada por portaria e conferida contra o catálogo e o
   enquadramento.** O primeiro leitor não reconhecia a "Portaria Conjunta".
3. **Os códigos procurados no texto integral** de cada ato de projeto e de novidade. O
   `texto_integral()` do `ferramentas/ler_dou.py` já baixa o texto.
4. **O `testar_atualidade.py` lê só o `estado.yaml` do `main`.** As portarias de um plano
   em ramo não são conferidas.

Pendências do acervo que a vigia apontou:
- a PRC GM/MS 6/2017, alterada pela GM 12.116, não está no acervo;
- o Decreto DF 37.843/2016 (NM-004) aparece como "Alterado" no SINJ e não foi revisto.

---

## 4. Agente da lista de executores por Região de Saúde

**Pedido em 09/10/2026:** um agente que, dentro de uma macrorregião de saúde, pesquise
quem tem CNES e monte a lista para a cotação.

**O que ele faria**, dado o objeto e a Região:
- listaria no CNES os estabelecimentos com o serviço e a classificação, o equipamento e
  os profissionais (CBO) que a ficha do SIGTAP exige;
- marcaria quem já atende SUS e quem tem habilitação;
- juntaria os contatos públicos;
- entregaria a base para as três cotações por Região (IN CGDF 01/2005, art. 25).

**Base que já existe:** `biblioteca/instrumento/enquadramento_cnes.md` e a trava F-06 de
`metodo/plano/procedimento.md`.

**A decidir quando começar:** o que é a "macrorregião" no DF (as sete Regiões de Saúde ou
um agrupamento delas) e se a lista sai por Região ou por polo do plano.

---

## 5. Agente que entra em contato com as clínicas

**Pedido em 09/10/2026:** depois do agente que mapeia as clínicas (item 4), um agente que
entre em contato com elas para pedir a proposta.

**Depende de:**
- **a lista do item 4**, com os contatos públicos de cada estabelecimento;
- **o canal de envio**, que o alerta pelo WhatsApp do item 1 também precisa (e-mail ou
  WhatsApp Business);
- **o orçamento a mandar.** Já existe o modelo do otorrino (`planos/redacao_05/gerar_orcamento_xlsx.py`):
  o valor por unidade e a quantidade de cada cenário, sem o percentual.

**O que ele faria:**
- montaria a mensagem de cada clínica a partir de um modelo;
- **mandaria só depois que o usuário aprovasse cada envio**, porque a mensagem fala em nome
  dele;
- leria as respostas e registraria cada proposta como `cotação` em `dados/precos.md`, com o
  documento;
- marcaria quem não respondeu, para lembrar.

**Regras que já valem:**
- nunca dizer o teto nem o percentual (`metodo/coleta/precos.md`);
- três cotações por Região (IN CGDF 01/2005, art. 25);
- a proposta precisa vir por escrito, dizendo o que inclui.

---

## 6. Guia do processo para a equipe técnica

**Combinado em 07/10/2026; o usuário deixou a implantação para depois em 10/10/2026.** Os
colegas da área técnica vão fazer planos junto com o usuário. Eles trabalham no Word, não no
GitHub nem no terminal.

**O que seria:** um guia, uma espécie de aula, que deixe todos na mesma página: as duas
trilhas, as fases, o que cada agente faz, o que vai ao documento e o que é controle interno.

**Regras que já valem:**
- **Sai de `metodo/`**, onde cada regra tem a origem. Não se escreve uma versão paralela.
- **O formato é um que eles abrem sem instalar nada:** um documento com link único ou o
  NotebookLM.
- **Ninguém da equipe recebe acesso ao repositório,** que é privado e tem CPF. Nenhum CPF,
  CNS ou nome de paciente vai ao guia.

---

## 7. Trilha de execução e prestação de contas

**Proposto em 10/10/2026 e aceito pelo usuário.** Hoje o processo termina no plano. Depois
da assinatura começam obrigações que o acervo já registra, mas que só servem para escrever o
plano:
- metas aferíveis a partir do terceiro mês de execução, sob pena de suspensão (OB-043);
- estrutura física, equipe e equipamentos prontos antes do início, como condição suspensiva
  (OB-048);
- relatórios mensais com metas, indicadores e intercorrências (OB-052);
- conta específica do convênio (OB-046);
- saldo devolvido em 30 dias e prestação de contas final em 60 (OB-023, OB-044);
- documentos guardados por 10 anos (OB-045).

**O que seria:** uma terceira trilha no `metodo/`, ao lado do pré-plano e do plano, com:
- o calendário das obrigações e dos prazos de cada convênio, a partir do termo assinado;
- a produção do mês contra a meta, com aviso quando o ritmo cair;
- a fila medida de novo no Mapa Social, como prova de resultado no relatório;
- a prestação de contas montada durante a execução, e não no fim.

**Regra que já vale:** dado de paciente (atendimento, APAC, laudo) não entra no repositório.
Ele guarda só os totais (`README.md`, "A regra da organização").

**Piloto:** o primeiro convênio assinado.

---

## 8. Controle externo na vigia de normas — feito em 10/10/2026

Virou frente da vigia: `metodo/coleta/normas.md` e `ferramentas/ler_controle.py`. Cada peça
que importa vira registro CT no acervo. Fica para depois entrar no alerta pelo WhatsApp
(item 1).

---

## 9. Documentos do proponente, com validade

**Proposto em 10/10/2026 e aceito pelo usuário.** A pasta `biblioteca/proponentes/` tem só
o ISHP, com uma análise. A ficha que o `biblioteca/proponentes/README.md` prevê para cada
proponente nunca foi criada.

**O que seria:**
- na ficha de cada proponente, os documentos de habilitação, cada um com a data de emissão
  e a de vencimento: certidões, CNES, estatuto, ata de eleição dos dirigentes, CEBAS se
  houver;
- uma conferência antes de cada envio, que acusa o que vence até a data provável da
  celebração.

**A decidir quando começar:** a lista de documentos que a SES-DF exige. A fonte é o Decreto
DF 48.727/2026 e a IN CGDF 01/2005, conferidos no texto.

---

## 10. Projetos de promoção à saúde pelo MROSC

**Avisado pelo usuário em 10/10/2026:** vão existir projetos de promoção à saúde feitos
pelo MROSC (termo de fomento ou de colaboração). O padrão hoje cobre só o convênio de
serviço assistencial.

**O que já se sabe:**
- **O objeto define o instrumento** (lição LI-026). Serviço assistencial complementar ao SUS
  é convênio, e o TCDF confirmou isso (Decisão 2426/2026, CT-008). Promoção da saúde, sem
  prestação direta de serviço assistencial, pode ir pelo MROSC.
- **A base desses projetos é outra:** a Lei 13.019/2014 (NM-003), o Decreto DF 37.843/2016
  (NM-004, que o SINJ dá como alterado e ainda não foi revisto) e a Portaria SES-DF
  187/2026 (NM-012), que disciplina o MROSC na SES-DF.
- **O controle também ataca o MROSC.** As decisões do TCDF já dizem o que a trilha vai ter
  de cobrar:
  - a transparência e a participação social dos arts. 78 e 79 do Decreto 37.843 (Decisão
    2791/2026, CT-010);
  - a experiência prévia da entidade nas atividades centrais do projeto e a capacidade técnica
    dos profissionais, com visita da SES-DF à sede e ao local (Lei 13.019, art. 33, V, b e c;
    Decisões 1636 e 2509/2026, CT-011);
  - metas ligadas ao objeto e aferíveis, uma versão só do plano e o destino dos bens
    permanentes, num termo que acabou em tomada de contas especial por sobrepreço (Decisão
    2325/2026, CT-009);
  - o encerramento de um termo, com a devolução dos recursos (Decisão 2681/2026, CT-006).

  As lições LI-011, LI-021, LI-024, LI-044 e LI-045 já valem para o convênio e vão valer
  para essa trilha também.

**O que fazer quando o primeiro chegar:**
- uma trilha própria, ou uma variante da trilha do plano, com o plano de trabalho do MROSC;
- a conferência de hoje lê o vocabulário do convênio. Ela vai precisar saber qual é o
  instrumento de cada plano.

