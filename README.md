# Planos SES-DF — guia de chegada

Seja bem-vinda. Este é o guia para quem nunca usou nada disso: o que é o projeto, o que
instalar, por onde começar a estudar e como trabalhar sem medo de estragar nada.

> **Esta é uma cópia só sua.** Ela foi tirada do projeto original em 17/11/2026, e tudo o
> que você mudar aqui fica aqui. Não há como uma alteração sua chegar ao projeto original,
> então pode mexer, testar e errar à vontade.

**Sumário**

1. [O que é este projeto](#1-o-que-é-este-projeto)
2. [O que você vai precisar](#2-o-que-você-vai-precisar)
3. [Primeiro acesso, passo a passo](#3-primeiro-acesso-passo-a-passo)
4. [Por onde começar: a trilha de estudo](#4-por-onde-começar-a-trilha-de-estudo)
5. [O que tem em cada pasta](#5-o-que-tem-em-cada-pasta)
6. [Os planos que estão aqui](#6-os-planos-que-estão-aqui)
7. [Trabalhar com o Claude](#7-trabalhar-com-o-claude)
8. [Salvar o seu trabalho](#8-salvar-o-seu-trabalho)
9. [Regras que não se quebram](#9-regras-que-não-se-quebram)
10. [O que ficou de fora desta cópia](#10-o-que-ficou-de-fora-desta-cópia)
11. [Palavras que vão aparecer](#11-palavras-que-vão-aparecer)
12. [Dúvidas comuns](#12-dúvidas-comuns)
13. [Referência técnica](#referência-técnica) (para depois)

---

## 1. O que é este projeto

Uma **entidade sem fins lucrativos** (um instituto, uma associação) recebe dinheiro de uma
**emenda parlamentar** para atender, pelo SUS, gente que está na fila da Secretaria de
Saúde do DF (SES-DF): exames, consultas, cirurgias. Para esse dinheiro sair, a entidade
assina um **convênio** com a SES-DF. Antes do convênio, ela precisa apresentar documentos
que dizem o que vai fazer, para quem, quanto custa e como se confere. São eles:

- o **pré-plano** (o "plano de trabalho simplificado"): a primeira proposta, curta, num
  formulário da SES;
- o **plano de trabalho**: o documento completo, que a SES analisa, devolve com pedidos de
  ajuste e, no fim, aprova.

**Este projeto escreve esses documentos.** E escreve sempre do mesmo jeito: há um
**método** (um passo a passo com regras) que foi sendo melhorado a cada plano, a cada
erro e a cada devolução da SES. Junto com o método, há:

- uma **biblioteca** de consulta: leis, portarias, tabelas de preço do SUS, os modelos da
  SES, os dados de cada entidade;
- uma **base de registros**: cada norma, cada lição aprendida e cada obrigação tem um
  número (como `NM-010` ou `LI-026`) e uma origem;
- **ferramentas** (pequenos programas) que conferem o plano, montam o arquivo do Word e
  buscam dados (a fila no Mapa Social da Saúde, a ficha do procedimento no SIGTAP);
- um **curso** feito para quem está chegando, com casos reais;
- **os planos**, cada um na sua pasta, com tudo o que foi feito para ele.

O trabalho do dia a dia é feito em conversa com o **Claude**, um assistente de
inteligência artificial que lê este projeto inteiro, segue o método e usa as ferramentas.
Você não precisa saber programar: precisa entender o assunto (o SUS, a emenda, o convênio,
a fila) para saber pedir e para saber conferir o que ele entrega. É isso que o curso
ensina.

## 2. O que você vai precisar

| o quê | para quê | onde | custa? |
|---|---|---|---|
| **Conta no GitHub** | é o site onde esta cópia mora. Sem conta, você não recebe o convite | [github.com/signup](https://github.com/signup) | grátis |
| **GitHub Desktop** | traz a cópia para o seu computador e salva o que você mudar, com botões, sem digitar comando | [desktop.github.com](https://desktop.github.com) | grátis |
| **Claude** (app para computador) | o assistente com quem se faz o trabalho e se estuda o curso (aba **Code**) | [claude.ai/download](https://claude.ai/download) | precisa de plano pago (Pro ou Max) |
| **Obsidian** (opcional, recomendado) | lê as notas do curso como um caderno com links clicáveis entre os assuntos | [obsidian.md](https://obsidian.md) | grátis |
| **Word** | abrir os planos prontos (`.docx`) | o que você já usa | — |

Programas como Python, Node e Tesseract só são necessários quando você for **rodar as
ferramentas** (conferir um plano, gerar um `.docx`). Isso fica para depois do curso, e o
próprio Claude pode instalar para você: veja a [Referência técnica](#instalação).

## 3. Primeiro acesso, passo a passo

**Passo 1. Crie a conta no GitHub** e mande o seu nome de usuário (o "@" que aparece no
seu perfil) para quem te passou este projeto. Ele vai te convidar.

**Passo 2. Aceite o convite.** Chega um e-mail do GitHub com o título parecido com
"invited you to collaborate". Clique em **View invitation** e depois em **Accept
invitation**. A partir daí você vê este repositório no site.

**Passo 3. Instale o GitHub Desktop** e entre com a mesma conta (`File → Options →
Accounts` no Windows, `GitHub Desktop → Settings → Accounts` no Mac).

**Passo 4. Traga a cópia para o computador.** No GitHub Desktop: `File → Clone
repository`, aba **GitHub.com**, escolha este repositório, escolha a pasta onde ele vai
ficar (por exemplo `Documentos/planos-ses-copia`) e clique em **Clone**. São uns 500 MB;
pode demorar alguns minutos.

**Passo 5. Abra no Claude.** No app do Claude, vá na aba **Code**, escolha a pasta que
você acabou de clonar. Antes da primeira aula, leia o mapa do curso
([`curso/mapa.md`](curso/mapa.md)); depois escreva, com o seu primeiro nome:

```
/aula 1 Seunome
```

O Claude conduz o módulo 1: explica uma parte por vez, pergunta, passa o exercício,
corrige mostrando a fonte e anota onde você parou, para continuar outro dia.

**Passo 6 (opcional). Abra no Obsidian.** No Obsidian: `Open folder as vault` e escolha a
mesma pasta. Comece pela nota **Início**. Cada assunto (convênio, emenda, OCI, SUCONV...)
é uma nota, e as palavras sublinhadas levam de uma nota para outra.

> Você também pode só **ler pelo site**: no GitHub, clique nas pastas e nos arquivos `.md`,
> que aparecem formatados. Para estudar sem instalar nada, comece por
> [`curso/mapa.md`](curso/mapa.md).

## 4. Por onde começar: a trilha de estudo

A ideia é **entender tudo antes de mexer nos planos**. A ordem que funciona:

| etapa | o que ler | por quê |
|---|---|---|
| **1. A vista de cima** | [`curso/mapa.md`](curso/mapa.md) e, aberto ao lado, [`curso/glossario.md`](curso/glossario.md) | o percurso inteiro numa página: de onde vem o dinheiro, quem faz o quê na SES, as siglas |
| **2. A base (módulos 1 a 5)** | [`curso/modulos/`](curso/modulos/), do 01 ao 05 | a lei do SUS e por que uma entidade privada pode atender pelo SUS; como o SUS paga; o dinheiro da emenda; o convênio; o caminho do processo dentro da SES. **Sem isso, o resto vira receita** |
| **3. O trabalho (módulos 6 a 10)** | módulos 06 ao 10 | escolher o que o plano vai oferecer (a fila, o procedimento), o preço, o pré-plano, o plano, a conferência |
| **4. Depois e a oficina (11 e 12)** | módulos 11 e 12 | o que acontece depois da assinatura; e como o projeto funciona por dentro (agentes, comandos, pastas) |
| **5. Os planos de verdade** | [`planos/`](planos/), começando pelo [`redacao_04`](planos/redacao_04/) | ver o método aplicado: as versões, as devoluções da SES, os estudos |
| **6. O método por inteiro** | [`metodo/LEIA.md`](metodo/LEIA.md) | a regra completa que todo plano segue. Os módulos do curso apontam para cá |

Cada módulo tem sempre as mesmas sete partes: **para que serve**, **a lógica**, **pode e
não pode**, **o caso** (o que aconteceu de verdade, inclusive os erros), **leia na
fonte**, **faça** (um exercício com dado real) e **confira** (as perguntas que você
precisa saber responder).

**Dúvida que o curso não responde?** Anote em [`curso/duvidas.md`](curso/duvidas.md) com
a data e o módulo, e leve para a próxima conversa com quem te passou o projeto. O seu
avanço fica anotado em [`curso/progresso/`](curso/progresso/).

## 5. O que tem em cada pasta

| pasta | em palavras simples |
|---|---|
| [`curso/`](curso/) | **comece aqui.** O curso: o mapa, o glossário, os 13 módulos, as dúvidas e o seu progresso |
| [`conhecimento/`](conhecimento/) | as notas do Obsidian: cada conceito, norma, órgão, caso e plano numa nota curta, ligada às outras |
| [`metodo/`](metodo/) | **a regra.** O passo a passo que todo pré-plano e todo plano seguem. Se o curso e o método divergirem, vale o método |
| [`biblioteca/`](biblioteca/) | material de consulta: as normas (leis, portarias, PDFs), os dados de cada entidade proponente, os preços (a Tabela SUS Candanga), o modelo da SES, o fluxo da emenda |
| [`registros/`](registros/) | a base de dados com número: normas (`NM-`), lições (`LI-`), achados (`AC-`), obrigações (`OB-`), controle externo (`CT-`); e as coletas da fila do Mapa Social |
| [`estudo/`](estudo/) | os planos já aprovados pela SES em 2026, transformados em texto, de onde o método foi tirado |
| [`planos/`](planos/) | **os projetos**, um por pasta (`redacao_NN`). Ver a seção 6 |
| [`ferramentas/`](ferramentas/) | os programas que conferem, consultam, extraem e geram o `.docx`. Você não precisa abrir; o Claude usa |
| [`acervo_polos/`](acervo_polos/) | o levantamento das clínicas e dos polos de ultrassom e tomografia (com um aplicativo de vistoria) |
| [`output/`](output/), [`outputs/`](outputs/), [`estudos imagens/`](estudos%20imagens/) | estudos avulsos, feitos para decidir alguma coisa (preço, cenário, carteira de exames). Cada arquivo tem a data no nome |
| `.claude/` | as instruções dos agentes e dos comandos do Claude (`/aula`, `/dossie`, `/revisao`, `/gauntlet`) |
| `PLANEJADO.md` | o que foi pedido e ficou para depois |

## 6. Os planos que estão aqui

Cada pasta tem um `estado.yaml` (onde o trabalho parou, com as decisões e as fontes) e,
quase sempre, um `pendencias.md` (o que falta). **Ao abrir um plano, leia esses dois
primeiro.** As versões enviadas e assinaladas ficam em `versoes/`.

| pasta | o que é | entidade | recurso | onde parou |
|---|---|---|---|---|
| [`redacao`](planos/redacao/) | o primeiro plano, de exercício: OCI de Avaliação Cardiológica | — | emenda federal de R$ 10 mi | congelado em 18/08/2026; é história |
| [`redacao_02`](planos/redacao_02/) | o mesmo objeto, refeito do zero com o método novo | — | exercício | concluído em 24/08/2026 |
| [`redacao_03`](planos/redacao_03/) | plano 3: OCI de Avaliação Diagnóstica de Câncer Gástrico | — | emenda federal de R$ 8,5 mi | estudo de preço para negociar com as clínicas (21/10/2026) |
| [`redacao_04`](planos/redacao_04/) | **plano 4: exames de ultrassonografia e tomografia.** O maior e mais completo | ISHP | emenda de bancada 71080005, R$ 11.592.762,00 | PT v1 enviado à SES; depois, o ajuste à Tabela SUS Candanga, o estudo de 12 meses e a análise do parecer técnico. Ver `estudos/` e `pendencias.md` |
| [`redacao_05`](planos/redacao_05/) | pré-plano de OCI em otorrinolaringologia | ISHP | emenda de bancada 71080005, R$ 1.502.687,00 | substituído pelo `redacao_07`, porque a SES pediu imagem |
| [`redacao_06`](planos/redacao_06/) | o pré-plano (PT simplificado) do plano 4 | ISHP | o mesmo do plano 4 | enviado; serve de modelo para os pré-planos seguintes |
| [`redacao_07`](planos/redacao_07/) | pré-plano de exames de imagem, no lugar do otorrino | ISHP | a mesma emenda do `redacao_05`, R$ 1,5 mi | carteira de 12 exames em cenários (planilhas na pasta) |
| [`redacao_08`](planos/redacao_08/) | OCI de Cardiologia | Instituto Fazer o Bem | emenda 41360018/2024, R$ 2 mi | fase 0: escolha do objeto (dossiê e estudos) |
| [`redacao_09`](planos/redacao_09/) | projeto de saúde mental infantojuvenil (COMPP e Adolescentro), por termo de fomento (MROSC) | a informar | federal, valor a informar | estruturação e entendimento; ainda não é plano |
| [`redacao_10`](planos/redacao_10/) | pré-plano da OCI de Avaliação Diagnóstica de Câncer Colorretal | ISHP | R$ 11 mi | v1 do pré-plano; emenda e ofício a confirmar |
| [`estudo_holter_mapa`](planos/estudo_holter_mapa/) | estudo avulso de Holter e MAPA | — | — | só dados |

> **Atenção:** no projeto original, cada plano em andamento vive num "ramo" separado. Nesta
> cópia, juntamos todos numa pasta só para facilitar a leitura. Por isso, quando um
> documento antigo falar em "ramo do plano" ou "pasta de trabalho", saiba que aqui tudo
> está junto em `planos/`.

## 7. Trabalhar com o Claude

Com a pasta aberta na aba **Code** do app do Claude, você conversa em português, como
com um colega. Ele lê o método antes de fazer, cita a fonte de cada número e confere com
as ferramentas.

**Comandos prontos** (escreva no começo da mensagem):

| comando | o que faz |
|---|---|
| `/aula 3` | dá o módulo 3 do curso: explica, pergunta, passa exercício e corrige |
| `/dossie` | monta o dossiê do objeto de um plano: qual fila atender e qual procedimento oferecer, chamando os agentes abaixo |
| `/revisao` | revisão cega: outros "leitores" que não conhecem a conversa leem o plano procurando erro |

**Agentes** (o Claude chama sozinho quando precisa): `mapa-social` busca a fila de espera
no Mapa Social da Saúde; `ficha-sigtap` lê a ficha do procedimento na tabela do SUS;
`precos` pesquisa os preços; `normas` vigia leis e portarias novas.

**Como pedir bem:**

- diga **qual pasta**: "no `planos/redacao_04`, ...";
- peça **com a fonte**: "de onde saiu esse número?" é sempre uma boa pergunta;
- peça para **explicar antes de fazer** quando estiver aprendendo: "me explica o que você
  vai fazer e por quê, antes";
- se algo parecer estranho, **diga**. O método foi construído assim, com cada erro virando
  regra.

## 8. Salvar o seu trabalho

O Git guarda a história do projeto em "fotos" (os **commits**). Quando você muda alguma
coisa (ou o Claude muda), a mudança fica só no seu computador até você salvar e enviar:

1. abra o GitHub Desktop: à esquerda aparecem os arquivos mudados;
2. embaixo, em **Summary**, escreva uma frase do que mudou ("Módulo 3 estudado",
   "Plano 10: meta revista");
3. clique em **Commit to main**;
4. clique em **Push origin**, no alto. Pronto: está salvo no GitHub, nesta cópia.

Para trazer o que outra pessoa salvou nesta cópia, clique em **Fetch origin** e depois em
**Pull**.

**Por que isso não mexe no projeto original?** Porque esta cópia é outro repositório, sem
ligação nenhuma com o original. O botão **Push** envia para cá, e só para cá. Se o
original tiver novidades que você deva receber, quem te passou o projeto atualiza esta
cópia.

**Errou?** No GitHub Desktop, clique com o botão direito no arquivo e em **Discard
changes** para voltar ao que estava (antes do commit). Depois do commit, a aba **History**
mostra tudo, e nada se perde.

## 9. Regras que não se quebram

1. **Dado de paciente nunca entra aqui.** Nem CPF, nem cartão SUS (CNS), nem nome, nem
   laudo. Do paciente, só números totais: tamanho da fila, produção do mês, meta.
2. **Nada sai para a SES ou para a entidade sem passar por quem te passou o projeto.** O
   curso e os estudos são internos: falam de preço, de margem e dos nossos erros.
3. **Número sem fonte não vale.** Todo valor no plano diz de onde veio (a tabela, a
   portaria, a coleta da fila com a data).
4. **A regra mora num lugar só, o `metodo/`.** Se você achar duas versões da mesma regra,
   avise: uma delas está errada.
5. **Este repositório é privado.** Não mude a visibilidade para pública nem convide outras
   pessoas sem combinar antes.

## 10. O que ficou de fora desta cópia

Para proteger dados pessoais, a cópia saiu diferente do original em alguns pontos:

- **CPFs tarjados.** Os 12 CPFs de pessoas reais que apareciam em documentos (planos
  assinados, convênios, propostas) foram trocados por `XXX.XXX.XXX-XX` nos textos, nos
  arquivos do Word e do Excel, e tarjados de preto nos PDFs. Se alguma ferramenta reclamar
  de CPF inválido num plano, é por isso.
- **Assinaturas digitais retiradas** dos PDFs assinados (o carimbo trazia o CPF). Esses
  PDFs servem para leitura; o original assinado está no SEI.
- **PDFs digitalizados de convênios e planos aprovados** (`estudo/planos_aprovados/`,
  `estudo/controle/` e um plano inicial em `registros/fontes/pre_planos_20261007/`) não
  vieram, porque são imagens com CPF que não dá para tarjar com segurança. O texto deles,
  já sem CPF, está em `estudo/extraidos/`, `estudo/extraidos_controle/` e
  `estudo/normalizados/`. A lista completa está em [`FORA_DA_COPIA.md`](FORA_DA_COPIA.md).
- **O histórico** do projeto original (as versões antigas de cada arquivo) não veio: a
  cópia começa com tudo como estava em 17/11/2026.
- **As anotações pessoais** do assistente e a verificação automática do GitHub (CI) não
  vieram.

## 11. Palavras que vão aparecer

**Do Git e do GitHub**

| palavra | quer dizer |
|---|---|
| repositório (repo) | a pasta do projeto, com toda a sua história |
| clonar | baixar o repositório para o seu computador |
| commit | uma "foto" salva das mudanças, com uma frase explicando |
| push | enviar os seus commits para o GitHub |
| pull / fetch | trazer do GitHub o que outra pessoa enviou |
| ramo (branch) | uma linha paralela de trabalho. Aqui só existe a `main` |
| `.md` | arquivo de texto com formatação simples (Markdown). Abre no GitHub, no Obsidian ou em qualquer editor |
| `.yaml` | arquivo de texto organizado em "campo: valor". Os `estado.yaml` dos planos são assim |

**Do assunto** (o glossário completo, com quase noventa termos, está em
[`curso/glossario.md`](curso/glossario.md))

| sigla | quer dizer |
|---|---|
| SES-DF | Secretaria de Estado de Saúde do Distrito Federal |
| PT | plano de trabalho |
| OCI | Oferta de Cuidados Integrados: um "pacote" do SUS (consulta + exames + retorno) pago por um preço só |
| SIGTAP | a tabela oficial dos procedimentos do SUS, com código, valor e regras |
| Tabela SUS Candanga | a tabela de valores do SUS no DF, maior que a federal em muitos códigos; é dela que sai o preço dos nossos planos |
| CNES | o cadastro nacional dos estabelecimentos de saúde |
| ARINS / SUCONV | na SES-DF: a porta de entrada das emendas / a área que instrui os convênios |
| MROSC | o marco das parcerias com organizações da sociedade civil (termo de fomento), diferente do convênio |
| ISHP | Instituto de Saúde Humanidade e Pesquisa, proponente de vários planos daqui |
| Mapa Social da Saúde | painel do MPDFT de onde se mede a fila de espera |

## 12. Dúvidas comuns

**Preciso saber programar?** Não. As ferramentas são usadas pelo Claude. Você precisa
entender o assunto para pedir e conferir.

**Posso apagar ou mudar um arquivo sem querer e estragar tudo?** Não de forma
definitiva. Antes do commit, "Discard changes" desfaz. Depois do commit, a história
guarda a versão anterior. E o projeto original nunca é afetado.

**O curso fala em "o usuário". Quem é?** É quem montou o projeto e tomou as decisões: a
pessoa que te passou esta cópia.

**Um arquivo cita um caminho que não existe aqui.** Pode ser um dos PDFs que ficaram de
fora (seção 10) ou uma referência ao projeto original (pasta de trabalho, ramo). Pergunte
ao Claude: "esse arquivo existe nesta cópia?".

**Os módulos falam de comandos como `python3 ferramentas/...`.** São para rodar as
ferramentas. Na primeira vez, peça ao Claude: "instale o que a Referência técnica do
README pede e rode o teste". Ele faz e explica.

**Quanto tempo leva o curso?** Os módulos 1 a 5 são os mais densos; reserve uma ou duas
sessões para cada um. Melhor fazer com o `/aula`, que pergunta e corrige, do que só ler.

---

# Referência técnica

*O que vem abaixo é o README original do projeto, com dois ajustes para esta cópia.
Serve para consulta quando você já tiver feito o curso, em especial o módulo 12.*

## Onde está cada coisa

| pasta | o que é |
|---|---|
| `metodo/` | **o padrão.** O procedimento que todo plano segue e as regras que valem para todos. Começar por aqui |
| `biblioteca/` | material de consulta comum aos planos: normas, proponentes, preços de postos, a Tabela SUS Candanga, o instrumento (fluxo da emenda, CNES). Não é regra; entra quando o objeto pede |
| `planos/` | um projeto por pasta (`planos/redacao_NN/`): o pré-projeto, o pré-plano e o plano de trabalho dele, com tudo o que é só dele. Nesta cópia, todos os planos estão aqui, juntos |
| `registros/` | a base de dados: acervo, lições, achados, obrigações. Liga o estudo, a biblioteca e o método |
| `estudo/` | o acervo dos planos aprovados e sua extração, de onde o método saiu. Tem o próprio `README.md` |
| `ferramentas/` | os scripts: conferência, consulta, extração, gerador de `.docx` e os testes. Os caminhos das pastas estão num lugar só, em `ferramentas/comum.py` |
| `curso/` | o curso para formar quem faz a parte técnica: treze módulos por casos, com o comando `/aula` |
| `conhecimento/` | o cofre do Obsidian: conceitos, normas, órgãos, casos e planos em notas ligadas. Abrir a raiz do repositório como cofre e começar por `conhecimento/Início.md` |

O que foi pedido e ficou para depois está em `PLANEJADO.md`.

## A regra da organização

**Uma verdade só.** Cada regra e cada fato moram num lugar; os outros lugares apontam
para ele. Antes de escrever uma regra, procurar onde ela já mora. Regra que vale para
qualquer plano vai para `metodo/`. O que é de um plano só fica na pasta dele.

**O padrão e as ferramentas moram só no `main`.** O ramo de um plano guarda só a pasta
do plano. Se o plano precisa mudar a ferramenta, a mudança vai primeiro para o `main`.

**Um repositório só.** O padrão, as ferramentas, a base e os planos ficam juntos porque se
leem o tempo todo:
- a conferência do plano lê o acervo, o catálogo do grupo 09 e a ficha do plano;
- a vigia corrige o catálogo que os planos usam;
- o teste do padrão confere cada caminho que o método cita.

A divisão em módulos é por pasta e por ramo. A fronteira que importa é a do dado:
- **dado de paciente não entra no repositório:** CPF, CNS, nome, registro de atendimento,
  APAC, laudo. Daqui fica só o total: fila, produção do mês, meta;
- **outro repositório, só em dois casos:**
  - quando outras pessoas forem receber acesso. Aí o método e as ferramentas saem sem CPF,
    e os dados dos planos ficam privados;
  - para isolar um serviço com chave própria, como o alerta pelo WhatsApp;
- **arquivo grande demais** vai para fora do histórico (Git LFS), sem dividir o repositório.

*Decisão do usuário, 10/10/2026.*

## Comandos

```bash
python3 ferramentas/conferir_plano.py planos/redacao_NN/            # confere um plano
python3 ferramentas/testar_conferencia_plano.py planos/redacao_NN/  # confere a conferência
python3 ferramentas/consultar.py checklist planos/redacao_NN/       # checklist das lições
python3 ferramentas/testar_tudo.py --mutacoes                       # tudo, antes de juntar ao main
npm run docx -- planos/redacao_NN/plano.md planos/redacao_NN/plano.docx

python3 ferramentas/conferir_pre_plano.py planos/redacao_NN/plano_v1.md            # confere um pré-plano
python3 ferramentas/testar_conferencia_pre_plano.py planos/redacao_NN/plano_v1.md  # confere a conferência
python3 ferramentas/gerar_pre_plano.py planos/redacao_NN/                          # .docx e .pdf do pré-plano
python3 ferramentas/montar_coleta.py --ordem planos/redacao_NN/dados/fontes/mapa_social_AAAAMMDD_bruto/  # confere a ordem de coleta
python3 ferramentas/ler_motor.py planos/redacao_NN/dados/fontes/mapa_social_AAAAMMDD_bruto/        # lê e confere a saída do kit do motor
python3 ferramentas/montar_coleta.py planos/redacao_NN/dados/fontes/mapa_social_AAAAMMDD_bruto/    # monta a coleta: JSON, .md, planilha
python3 ferramentas/conferir_coleta.py planos/redacao_NN/dados/fontes/mapa_social_AAAAMMDD.md   # confere uma coleta
node ferramentas/mapa_social/motor.js --assinatura                                           # a assinatura do kit do motor
python3 ferramentas/conferir_ficha.py planos/redacao_NN/dados/fontes/sigtap_CODIGO_MMAAAA.md      # confere uma ficha
python3 ferramentas/ler_tabela_unificada.py --baixar MMAAAA                                  # o pacote oficial da Tabela, para o cache
python3 ferramentas/ler_tabela_unificada.py MMAAAA CODIGO                                   # a ficha de um código no pacote
python3 ferramentas/ler_dou.py --de AAAA-MM-DD --ate AAAA-MM-DD                             # o Ministério da Saúde no DOU
python3 ferramentas/ler_controle.py --de AAAA-MM-DD --ate AAAA-MM-DD                        # o TCDF e o MPCDF
python3 ferramentas/conferir_precos.py planos/redacao_NN/dados/precos.md                     # confere os preços do objeto
python3 ferramentas/conferir_dossie.py planos/redacao_NN/dossie/                            # confere o dossiê do objeto
python3 ferramentas/extrair_candanga.py "<pdf>" biblioteca/precos/tabela_sus_candanga/       # a Tabela SUS Candanga do PDF da SES
python3 ferramentas/pacote_revisao.py --documento planos/redacao_NN/plano.md --saida <r1>/pacote ...  # o pacote cego da revisão
python3 ferramentas/revisar_claude.py preparar <r1>/pacote --pasta <pasta cega>           # o Claude cego: prepara (o /revisao abre os subagentes)
python3 ferramentas/revisar_claude.py juntar <pasta cega> --saida <r1>/claude             # o Claude cego: junta
python3 ferramentas/revisar_chatgpt.py <rf>/pacote --saida <rf>/chatgpt                   # a versão final pelo Sol (ChatGPT)
python3 ferramentas/conferir_revisao.py <r1>/pacote <r1>/claude/achados.json              # confere as citações dos revisores
```

## Agentes

Tarefas que se repetem igual de plano para plano têm um agente, em `.claude/agents/`. O
agente não guarda regra: segue o método em `metodo/` e devolve o resultado pronto.

| agente | o que faz | método |
|---|---|---|
| `mapa-social` | busca a fila no Mapa Social da Saúde a partir de uma ordem de coleta (panorama ou medição); o kit do motor mede e os scripts montam a coleta em `dados/fontes/`; não decide nem interpreta | `metodo/coleta/mapa_social.md` |
| `ficha-sigtap` | lê a ficha de cada código no SIGTAP, com o histórico e o CID para a coleta | `metodo/coleta/ficha_sigtap.md` |
| `normas` | vigia a Tabela do SUS, o DOU, a camada distrital e o controle externo (TCDF e MPCDF); valida, registra e corrige o catálogo; **agendado todo dia 10**, num ramo `vigia/<data>` que o usuário revê | `metodo/coleta/normas.md` |
| `precos` | pesquisa o valor pela origem do recurso, o que a SES-DF paga e o mercado do DF, e faz a conta do objeto em `dados/precos.md` (controle interno) | `metodo/coleta/precos.md` |

**O dossiê do objeto** junta os agentes para escolher a fila e a OCI. Como um agente não abre
outro, ele é um comando da conversa principal: `/dossie` (`.claude/commands/dossie.md`), que
segue `metodo/coleta/dossie.md`.

**O gauntlet** melhora o prompt de um agente por rodadas: candidato e campeão rodam os casos
de prova, portões automáticos derrubam o que erra, um crítico cego escolhe e a catraca guarda o
melhor. O comando é `/gauntlet` (`.claude/commands/gauntlet.md`), o método é
`metodo/agentes/gauntlet.md`, e os casos e o placar do `mapa-social` estão em
`ferramentas/provas/mapa_social/`.

**A revisão cega** põe quem não conhece a conversa para ler o que fizemos. Dois subagentes
Claude leem o documento num pacote cego, sem a conversa nem o padrão, e o assistente
responde a cada achado com fonte, em até três rodadas. Na versão final, o ChatGPT (o
modelo Sol) lê uma vez, como outra família. O comando é `/revisao`
(`.claude/commands/revisao.md`), e o método é `metodo/revisao/cega.md`.

## Instalação

```bash
python3 -m venv ~/.venvs/planos && source ~/.venvs/planos/bin/activate
pip install -r requirements.txt
npm ci
```

O OCR precisa do binário **Tesseract com o idioma `por`**, instalado à parte. Os
detalhes, inclusive para Windows, estão em `estudo/README.md`.

Esta cópia é **privada**. Os CPFs foram tarjados ao montá-la (ver `FORA_DA_COPIA.md`);
mesmo assim, não torná-la pública nem compartilhar sem combinar antes.
