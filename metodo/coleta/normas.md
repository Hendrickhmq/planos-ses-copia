# coleta/normas.md — vigiar, validar e registrar as normas

O padrão confere coerência; este método confere **atualidade**. A Tabela do SUS muda por
portaria a cada competência, e as regras da emenda e do convênio também mudam
(`../comum.md`, regra 2). Sem vigia, o dado fica velho em silêncio: o catálogo do grupo
09 passou um mês com os valores de antes da SAES 4.795/2026 sem ninguém notar.

Quem executa é o agente `normas` (`.claude/agents/normas.md`), agendado para os dias
10 e 22 ("Agendado", abaixo), ou o assistente na conversa. O método é este arquivo; o agente não guarda regra.

*Origem: regra do usuário, 09/10/2026 — "procurar e validar portarias que mudaram os
valores, metodologia, tudo"; o agente foi pedido no mesmo dia, agendado para o dia 10.
Mais tarde, no mesmo dia, o usuário pediu que a vigia acompanhe as portarias do Ministério da Saúde,
"lá que saem as coisas novas". Em 10/10/2026 entrou o controle externo, que o usuário chama de "o
mais perigoso".*

---

## O que se vigia

| frente | fonte | o que interessa |
|---|---|---|
| **Tabela do SUS** | a **Nota Técnica CGSI** de cada competência, no FTP do DATASUS: `ftp://ftp2.datasus.gov.br/pub/sistemas/tup/downloads/notastecnicas/nota_tecnica_cgsi_sigtap_<AAAA>_<MM>.pdf`. Ela lista, procedimento por procedimento, toda portaria que alterou a Tabela naquela competência | valor, descrição, composição, atributo, compatibilidade, CID, habilitação, inclusão e exclusão de procedimento |
| **Ministério da Saúde** | **todo** ato do Ministério no DOU, dia a dia, na Seção 1, na edição extra e no suplemento: `python3 ferramentas/ler_dou.py --de <AAAA-MM-DD> --ate <AAAA-MM-DD>`. É lá que sai o que é novo | o que altera ou cita na ementa norma do acervo, trata de emenda ou do Distrito Federal (**projeto**); ato normativo sobre OCI, Agora Tem Especialistas, Tabela do SUS, remuneração, Portaria de Consolidação, incremento, financiamento, MAC, atenção especializada, regulação (**novidade**) |
| **Controle externo** | as decisões do TCDF, nas atas das sessões publicadas no DODF; as representações e notícias do MPCDF e as notícias do TCDF, pelos feeds dos sites: `python3 ferramentas/ler_controle.py --de <AAAA-MM-DD> --ate <AAAA-MM-DD>` | a decisão ou a representação sobre convênio, termo de fomento, emenda, parceria, OCI ou credenciamento da SES-DF, e sobre as entidades e os instrumentos do acervo (**projeto**); o resto da saúde do DF (**saúde**) |
| **Camada distrital** | SINJ-DF (`https://www.sinj.df.gov.br`) e DODF (`https://dodf.df.gov.br`) | alteração do Decreto DF 48.727/2026, da IN CGDF 01/2005, da Portaria SES-DF 98/2025; norma nova da SES-DF sobre convênio, emenda, plano de trabalho ou remuneração, inclusive as Deliberações do Colegiado de Gestão da SES-DF. Foi por uma delas que saiu a Tabela SUS Candanga (NM-093), cujo Anexo Único, com os valores, ainda não tinha saído em 09/10/2026 |

**Os códigos que importam** são os que o projeto usa:
- os do catálogo do grupo 09, `registros/fontes/sigtap_grupo09_<MMAAAA>.csv`;
- os das fichas em `planos/*/dados/fontes/sigtap_*.md`;
- os do `estado.yaml` de cada plano, **inclusive de plano em ramo próprio**: `git branch -a`
  e `git show <ramo>:planos/<plano>/estado.yaml`;
- os de plano que ainda não está em ramo nenhum, só na pasta de trabalho do usuário: ler o
  `estado.yaml` de lá, sem mexer em nada.

**As normas que importam** são as do acervo (`registros/acervo.csv`, tipo norma) e as
que alteram ou revogam alguma delas.

## Como fazer

1. **A competência.** Ver no FTP quais Notas Técnicas existem (a listagem da pasta
   responde) e qual é a mais nova. Publicação não tem dia fixo: em 2026 saíram entre o
   dia 9 e o dia 21. **Se a do mês ainda não saiu, registrar isso e conferir as outras
   frentes.** Se uma Nota Técnica já lida mudou de tamanho ou de data na listagem, foi
   republicada: ler de novo.
   - **Se a competência nova já abriu** se vê no mesmo FTP, sem o navegador: a pasta
     `ftp://ftp2.datasus.gov.br/pub/sistemas/tup/downloads/` traz um
     `TabelaUnificada_<AAAAMM>_v<data>.zip` por competência publicada. É o primeiro passo para
     conferir na tela do SIGTAP a OCI que entrou no catálogo com `vigente desde` (passo 6).
     *Origem: vigia de 10/10/2026.*
   - **Com o pacote novo no FTP, baixá-lo e conferir contra ele** (`python3
     ferramentas/ler_tabela_unificada.py --baixar <MMAAAA>`): cada ficha dos planos na
     competência (`conferir_ficha.py`, H), inclusive a reconstituída, que passa a dizer "no
     pacote"; e cada linha do catálogo do grupo 09 (valor e idade). O pacote é a Tabela
     inteira: a divergência dele com a ficha vai para "Planos afetados". O FTP também
     republica pacote de competência antiga (06 a 08/2026 saíram de novo em 23/10/2026):
     listar as datas e reler o que mudou.
     *Origem: o redacao_08, 22/10/2026: fichas de 10/2026 reconstituídas pelas Notas
     Técnicas com o pacote no FTP desde 15/10.*
2. **Ler a Nota Técnica** de cada competência ainda não vigiada e listar as portarias e
   os procedimentos alterados. Filtrar pelos códigos que importam.
   - Separar por portaria, inclusive a "PORTARIA CONJUNTA nº ... - SAES/SECTICS", cujos
     procedimentos não se somam aos da portaria de cima.
   - Conferir cada procedimento do projeto contra o catálogo (valor, idade, sexo) e contra
     o enquadramento (`biblioteca/instrumento/enquadramento_cnes.md`: habilitação,
     incremento, instrumento de registro).
3. **Ler o Ministério da Saúde no DOU**, todos os dias desde a última vigia:
   `python3 ferramentas/ler_dou.py --de <o dia da última vigia> --ate <hoje>
   --saida registros/vigia/dou_<AAAA-MM-DD>.md --bruto <pasta temporária, fora do
   repositório>`.
   - **Começa no dia da última vigia, e não no seguinte:** a edição extra daquele dia pode
     ter saído depois que a vigia rodou, e a ferramenta não guarda o dia de hoje. Os atos
     repetidos daquele dia já estão no relatório anterior. *Origem: vigia de 10/10/2026.*
   - **O que a ferramenta faz:**
     - lê a página "leitura do jornal" do in.gov.br de cada dia, pelo `curl`, porque o
       in.gov.br recusa o navegador embutido e o Python;
     - separa os atos do Ministério e os classifica, pelo título e pela ementa, em
       **projeto**, **novidade** e **local** (estabelecimento ou repasse de outro ente, só
       listado);
     - guarda em `--bruto` o que baixou. Reclassificar o período, ou procurar falso
       negativo, não baixa tudo de novo.
   - **Se ela parar com "sem o bloco de dados"**, a rede de entrega do in.gov.br devolveu
     página de erro. Rodar de novo com o mesmo `--bruto`: os dias já lidos não se baixam
     outra vez.
   - **A lista é o ponto de partida.** O resumo de cada ato tem uns 300 caracteres e
     esconde o anexo. Por isso:
     - a frase genérica "Estados, Distrito Federal e Municípios" só conta se o texto
       integral tiver o DF, e a ferramenta abre esse texto sozinha;
     - **cada ato de projeto e de novidade se abre e se lê**, e no texto integral se
       procuram os códigos que importam. A SAES 4.940/2026 só se mostrou do projeto pelo
       anexo;
     - na lista dos outros entes, passar o olho: é onde cairia um ato do DF que o resumo
       não deixou ver.
   - A busca por palavra do in.gov.br (`https://www.in.gov.br/consulta/-/buscar/dou?q=<termos>`)
     serve para achar um ato que se conhece pelo número, não para vigiar: ela perde ato
     de edição extra, e a SAES 4.795/2026 saiu em edição extra.
   - **No SINJ e no DODF**, buscar desde a última vigia o que altera o Decreto DF
     48.727/2026, a IN CGDF 01/2005 e a Portaria SES-DF 98/2025, e norma nova da SES-DF
     sobre convênio, emenda, plano de trabalho ou remuneração. Como:
     - **a pesquisa do SINJ** só funciona no navegador embutido, porque o firewall bloqueia
       o `curl`:
       - o endereço é `https://www.sinj.df.gov.br/sinj/ResultadoDePesquisa?tipo_pesquisa=norma&nr_norma=<n>&ano_assinatura=<aaaa>`;
       - os dados vêm de um POST que a própria página faz e que se chama com `fetch` de
         dentro dela: `/sinj/ashx/Datatable/ResultadoDePesquisaNormaDatatable.ashx?<a
         mesma query string>`, com o corpo `bbusca=sinj_norma&iDisplayStart=0&iDisplayLength=100`;
       - **a varredura se faz sem termo:** só com `tipo_pesquisa=norma&ano_assinatura=<aaaa>`,
         a resposta vem da norma mais nova para a mais antiga. O que saiu desde a última
         vigia cabe em uma ou duas páginas de 100, filtradas por órgão e ementa. *Origem:
         vigia de 10/10/2026: nenhuma inversão de data nas 600 primeiras.*
       - não há filtro de período, e a ordenação pedida (`iSortCol_0`) numa pesquisa com
         termo não funciona. A pesquisa por número ou por termo serve para achar uma norma
         conhecida;
       - o tipo de norma se filtra por `ch_tipo_norma`, não por `nm_tipo_norma`;
     - **as alterações** vêm vazias na pesquisa (`vides`). Só a página de detalhe as mostra,
       em "Vides - Normas que afetam": `/sinj/DetalhesDeNorma.aspx?id_norma=<ch_norma>`. Mudam
       a norma "Alterado(a)", "Acrescido(a)" e "Renumerado(a)"; "Legislação Correlata" não
       muda;
     - **o texto compilado** baixa pelo `curl`: `https://www.sinj.df.gov.br/sinj/Norma/<ch_norma>/x.html`.
       Quando o firewall bloqueia também esse endereço, como aconteceu em 09/10/2026, ele abre
       no navegador embutido;
     - **o DODF inteiro** baixa pelo `curl`, com os parâmetros codificados (`-G
       --data-urlencode`): `https://dodf.df.gov.br/dodf/jornal/visualizar-pdf?pasta=<AAAA>|<MM>_<Mês>|DODF <nº> <DD-MM-AAAA>|&arquivo=DODF <nº> <DD-MM-AAAA> INTEGRA.pdf`;
     - **a edição extra do DODF:** a listagem por pasta dá a íntegra e as edições extras de
       qualquer dia: `https://dodf.df.gov.br/dodf/jornal/pastas?pasta=<AAAA>/<MM>_<Mês>/<DD MM AAAA>`
       (com `-G --data-urlencode`; o mês vai com o nome em português, como `03_Março`). A
       página `https://dodf.df.gov.br/dodf/jornal/diario` mostra só o dia mais recente.
       *Origem: vigia de 10/10/2026, que achou só a página do dia; a listagem por pasta foi
       achada no mesmo dia, ao montar o controle externo.*
     - **script que passa de 45 s** cai por tempo no navegador embutido. Partir a varredura
       e ler o resultado de `window` na chamada seguinte.

   - **O controle externo**, todos os dias desde a última vigia:
     `python3 ferramentas/ler_controle.py --de <o dia da última vigia> --ate <hoje> --saida
     registros/vigia/controle_<AAAA-MM-DD>.md --bruto <pasta temporária, fora do repositório>`.
     - **O que a ferramenta faz:**
       - para o TCDF, lista os arquivos de cada dia do DODF (a íntegra e as edições extras),
         tira o texto com o `pdftotext` e separa cada processo da ata com a sua decisão
         ("PROCESSO Nº ... DECISÃO Nº N/AAAA - O Tribunal...");
       - para o MPCDF e para as notícias do TCDF, lê o feed dos sites página a página, até a
         data da última vigia. O MPCDF publica no site o resumo de cada representação. A
         busca interna do site é fechada;
       - classifica em **projeto** e **saúde**. O ato de pessoal (aposentadoria, pensão,
         admissão) fica sempre fora, porque não interessa e traz o nome de terceiros;
       - guarda em `--bruto` o texto de cada DODF, uns 8 MB de PDF por dia.
     - **A lista é o ponto de partida.** Cada peça do projeto se lê inteira: a decisão do TCDF
       no DODF; a representação do MPCDF, que aparece primeiro só como resumo no site.
     - **Não serviram:** a API de distribuição de processos do TCDF, que só traz códigos sem
       o órgão nem o assunto; o detalhe do processo e o ADA, que pedem login; os boletins de
       jurisprudência, que são uma seleção, e cujo último era de abril.

   *Origem: piloto da vigia, 09/10/2026. A classificação pelo resumo inteiro pôs cerca
   de 35 falsos positivos em projeto e 160 CEBAS em novidade. A página de erro do
   in.gov.br, com HTTP 200, passava por dia sem edição. O controle externo entrou em
   10/10/2026: no teste, a Decisão TCDF 715/2026, sobre termos de fomento da SES-DF
   custeados por emenda, saiu como projeto.*
4. **Validar no texto** cada alteração que importa: o artigo ou o anexo, a mudança exata
   e a **competência de vigência** ("efeitos a partir da competência seguinte à
   publicação"). A página do SIGTAP e o resumo da Nota Técnica não bastam.
5. **Registrar** a norma nova ou alterada:
   - baixar para `biblioteca/normas/` com o nome no padrão do acervo (`SAES 4795-2026
     <assunto>.html`). O in.gov.br recusa o navegador embutido; o `curl` baixa;
   - extrair: `python3 ferramentas/extrair_html.py biblioteca/normas/
     biblioteca/extraidos_normas/ --doc "<nome>"` para HTML,
     `python3 ferramentas/extrair_planos.py biblioteca/normas/ biblioteca/extraidos_normas/
     --doc "<nome>"` para PDF;
   - uma linha no `registros/acervo.csv`, com o próximo NM livre, a url e a data de
     acesso. As linhas do acervo terminam em CRLF (`.gitattributes`). Acrescentar a linha
     com CRLF, sem regravar o arquivo inteiro. A espécie sai da lista do
     `ferramentas/verificar_registros.py`;
   - a Nota Técnica em `registros/fontes/notas_tecnicas_cgsi/`;
   - **a peça de controle externo que importa:** uma linha no acervo com o próximo CT livre,
     tipo `controle`, espécie `representacao` ou `decisao`, o órgão, a data, o processo e o
     endereço. O acesso é `integral` quando se leu o texto da decisão ou da representação, e
     `so_indice` quando só se leu o resumo. Se ela ataca alguma coisa que um plano faz, vai
     para "A decidir", com a lição que pode virar.
6. **Atualizar o que a norma mudou e o projeto usa**, sempre pelo texto validado:
   - a linha do catálogo do grupo 09 (valor, composição, atributo), e a linha DD-003 do
     acervo diz a correção;
   - a norma revogada ganha `situacao: revogada` no acervo;
   - **a OCI ou o procedimento que a portaria cria e o SIGTAP ainda não mostra** entra no
     catálogo vigente com a situação `vigente desde MM/AAAA (<portaria>)`, com o valor e a
     composição tirados do anexo da portaria. Quando o catálogo da competência dele for
     aberto, o valor se confere na tela do SIGTAP. *Origem: SAES 4.940/2026, vigia de
     09/10/2026.*

   O que mexe em plano (ficha, `estado.yaml`, documento) **não se muda aqui**: vai para o
   relatório, com o plano afetado.
7. **Conferir:** `python3 ferramentas/testar_tudo.py`, em especial o
   `testar_atualidade.py` e o `verificar_registros.py`.
8. **Escrever o relatório** em `registros/vigia/vigia_<AAAA-MM-DD>.md`.

## O relatório

`registros/vigia/vigia_<AAAA-MM-DD>.md`, sempre, mesmo quando nada mudou:

| seção | o que tem |
|---|---|
| Competências | quais Notas Técnicas foram lidas, quais ainda não saíram, quais foram republicadas |
| Buscas | o período lido no DOU (com o `dou_<AAAA-MM-DD>.md` ao lado) e os termos do SINJ |
| O que mudou | cada norma que importa ao projeto: número, data, o que muda, onde no texto, desde quando |
| **Novidades do Ministério** | cada ato normativo novo que pode virar objeto ou mudar regra (OCI nova, incremento, programa, regra de emenda, regulação): o que é, desde quando, e por que pode interessar — mesmo que não toque nenhum plano hoje |
| **Controle externo** | cada decisão do TCDF e cada representação do MPCDF que toca o projeto: o número, o processo, o instrumento e a entidade, o que se decidiu ou se pediu, o prazo, e se pega algum plano — mesmo que não peguem nenhum, e com o `controle_<AAAA-MM-DD>.md` ao lado |
| O que foi registrado | normas baixadas, linhas novas do acervo, linhas corrigidas do catálogo |
| Planos afetados | cada plano em que a mudança pesa, e o que precisa ser revisto nele |
| A decidir | o que pede decisão do usuário |

A última linha do relatório diz a **competência vigiada** (`competência vigiada: MM/AAAA`)
e a data. O `testar_atualidade.py` lê essa linha.

## Agendado

**Duas rodadas por mês: no dia 10 e no dia 22.** A Nota Técnica e o pacote saem entre o
dia 9 e o dia 21, e a rodada do dia 10 costuma chegar antes deles: a de 10/10/2026 achou a
Nota de 10/2026 por sair, e ela saiu por volta de 15/10, com a próxima rodada só em 10/11.
A rodada do dia 22 lê a Nota e o pacote do mês; a do dia 10, o DOU, o SINJ e o controle
externo do mês que passou. Se a do dia 22 achar a Nota ainda por sair, diz isso, e a do dia
10 a lê.
*Proposta de 25/10/2026; a tarefa agendada muda só com o sim do usuário.*

Quando roda sozinho (todo dia 10 e 22), o agente trabalha numa cópia separada do `main`
(`git worktree`), num ramo `vigia/<AAAA-MM-DD>`, e **não envia nem junta ao `main`**. O
usuário revê o ramo e decide. Nada do plano em andamento é tocado.
