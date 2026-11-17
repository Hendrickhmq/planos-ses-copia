# estudo/ — o acervo dos planos aprovados e sua extração

**Este é o README do estudo, não do projeto.** O estudo comparou os planos de trabalho
de convênio aprovados pela SES/DF para produzir um modelo próprio, e não uma cópia dos
existentes. Os planos aprovados são a régua do **mínimo viável**, não do bom. O que
saiu dele vale para todo plano e mora em `metodo/`: o `PADRAO.md` e o `modelo.md`. Para
começar um plano, ler o `README.md` da raiz.

Corpus: 5 planos de trabalho, todos do instrumento **convênio**, todos públicos,
publicados no site da secretaria. Os quatro primeiros foram assinados em
29/04/2026; o `pt_ses_05` entrou depois, assinado em 09/07/2026, e é o único
publicado como imagem — ver "PDF sem camada de texto", abaixo.

---

## Estrutura

O estudo ocupa a pasta `estudo/`. Os scripts estão em `ferramentas/` e os registros
em `registros/`, na raiz, porque servem também ao método e à biblioteca. Os caminhos
de todas as pastas estão num lugar só, em `ferramentas/comum.py`.

```
estudo/
├── README.md                  este arquivo
├── schema.md                  definição dos campos de registros/ (ler antes de preencher)
├── planos_aprovados/          pt_ses_01_<processo>.pdf ... pt_ses_05_...
├── controle/                  CT-001... pareceres, acórdãos, checklists
│                              IT-001... termos de convênio, aditivos, apostilamentos
├── extraidos/                 BRUTO — só o extrator escreve aqui
│   └── pt_ses_01/
│       ├── texto.md           texto corrido, sem conteúdo de tabela
│       ├── tabelas/*.csv      uma CSV por tabela
│       └── meta.yaml          metadados e estatísticas
├── extraidos_ocr/             BRUTO — leitura por OCR de célula do PDF digitalizado
│   └── pt_ses_05/             (é a que o tratamento usa para o pt_ses_05)
├── extraidos_controle/        a mesma extração, sobre controle/ (termos e apostilamentos)
├── normalizados/              DERIVADO — apagar e reconstruir dá igual
│   └── pt_ses_01/
│       ├── texto.md           cópia byte a byte do bruto
│       ├── tabelas/*.csv      as mesmas CSVs, tratadas
│       ├── planilha.csv       a planilha orçamentária inteira, consolidada
│       └── tratamento.yaml    o que o tratamento aplicou, e de qual pasta veio
├── destilados/
│   └── roteiro.md             a entrevista de construção do plano — HISTÓRICO, substituído
│                              pelo metodo/ (13 seções contra 9; não usar)
└── historico/                 gerações anteriores do extrator, sem uso

registros/                     na raiz
├── acervo.csv                 o que existe, de que espécie e de onde veio
├── obrigacoes.csv             o que o plano PRECISA conter, e por quê
├── achados.csv                o que foi OBSERVADO nos planos
├── licoes.csv                 o que FAZER no nosso plano, com origem e modo de conferir
├── correcoes.csv              correção de forma, célula a célula, com motivo
├── conferencia.csv            o que foi conferido à mão, com hash do conteúdo
├── exigencias_resposta.csv    exigência → versão que respondeu
└── fontes/                    dados de sistema: catálogo SIGTAP do grupo 09, comparativos
```

O que o estudo produziu e que vale para todo plano saiu daqui: o `modelo.md` e o
`criterios.md` estão em `metodo/`; as normas, a nota do CNES e o fluxo da emenda, em
`biblioteca/`.

O fluxo é de mão única, e é o que torna a pasta delegável:

```
planos_aprovados/*.pdf  →  extrair_planos.py         →  extraidos/      (bruto, imutável)
planos_aprovados/*.pdf  →  extrair_digitalizados.py  →  extraidos_ocr/  (bruto, só digitalizado)
extraidos/ + extraidos_ocr/ + correcoes.csv  →  tratar_planos.py  →  normalizados/  (derivado)
```

Quando o mesmo plano existe nas duas pastas brutas, o tratamento lê o de
`extraidos_ocr/`: é a leitura que reconstrói a tabela, e é a que foi conferida.

`extraidos/` é o que o PDF diz, com os defeitos do PDF. `normalizados/` é o que
dá para usar. Nunca editar `extraidos/` à mão: se o número está errado no
documento, ele continua errado nos dois lados e vira linha em `achados.csv`.

---

## Consulta — erros e acertos

A base tem quatro camadas, e cada uma responde a uma pergunta:

| registro | pergunta |
|---|---|
| `achados.csv` | o que os planos aprovados fizeram, de bom e de ruim? |
| `obrigacoes.csv` | o que a norma e o termo exigem? |
| peças `CT` do `acervo.csv` | o que o controle externo atacou depois da aprovação? |
| `licoes.csv` | o que fazer no nosso plano — e como conferir? |

A lição é a camada que se usa na redação: uma regra no imperativo, com a
gravidade (`reprova`, `questiona`, `melhora`), a origem (os achados, cláusulas e
representações de onde saiu) e o modo de conferir (verificação do
`conferir_plano.py` ou pergunta). O `consultar.py` liga as quatro:

```bash
python3 ferramentas/consultar.py                          # panorama
python3 ferramentas/consultar.py LI-013                   # a lição, a evidência e quem a cita
python3 ferramentas/consultar.py AC-014                   # o achado — e o aviso de que o AC-058 o desmente
python3 ferramentas/consultar.py pt_ses_01                # erros, acertos, termo e controle de um aprovado
python3 ferramentas/consultar.py buscar locacao           # busca sem acento nem caixa em todos os registros
python3 ferramentas/consultar.py tema dimensionamento     # as lições de um tema
python3 ferramentas/consultar.py checklist planos/redacao_05/ --saida planos/redacao_05/checklist.md
python3 ferramentas/consultar.py criterios                # regenera metodo/criterios.md
```

O **checklist** roda o `conferir_plano.py` no plano e devolve as lições em ordem
de gravidade: marcada só a que a verificação automática cobre e passou; a
parcial e a manual ficam abertas com a pergunta. É o último passo antes do
protocolo.

Para um plano novo, o ponto de partida é o **`destilados/modelo.md`**: as 9 seções
com o texto administrativo, financeiro e de gestão pronto, variantes para OCI e para
procedimento avulso, e marcas no lugar do que depende do objeto — a parte
assistencial reunida em perguntas no Anexo A, o que é da SES-DF no Anexo B. O
**`destilados/enquadramento_cnes.md`** diz o que conferir no CNES de cada polo antes de
escrever, e o **`destilados/fluxo_emenda.md`** dá o percurso inteiro em dois trilhos —
o do dinheiro, da União ao Fundo de Saúde do DF, e o da indicação e do convênio, todo
dentro da SES-DF —, com quem faz, prazo e norma de cada etapa.

Achado novo que ensina algo vira lição nova — ou reforça a origem de uma que já
existe. `destilados/criterios.md` é derivado: corrige-se a lição e gera-se de
novo, e o `testar_tudo.py` falha se os dois se desencontrarem.

---

## Hierarquia de precedência

Em caso de conflito entre registros, vale nesta ordem:

```
obrigacoes.csv   (norma)              ← vence tudo
criterios.md     (professor/revisor)
exigencias_resposta.csv (diligências)
achados.csv      (prática observada)  ← nunca vence nada acima
```

E **dentro** do `obrigacoes.csv`, quando duas linhas se contradizem, decide a
coluna `hierarquia` da norma que fundamenta cada uma, registrada em
`acervo.csv`. Linha de `natureza: contratual` fica fora dessa escada: ela vem do
termo de convênio, que não é norma e obriga só quem assinou. Contra norma
vigente, perde; acrescentando, vale.

```
1 constituição · 2 lei · 3 decreto · 4 portaria/resolução
5 instrução normativa · 6 nota técnica
```

Número menor vence. Isso importa aqui porque a SES se apoia ao mesmo tempo em
portaria do Ministério da Saúde e em decreto distrital, e os dois não têm o
mesmo peso.

Duas regras que decorrem disso:

1. **Achado nunca vence norma.** Se três planos fazem de um jeito e a norma diz
   outro, a norma manda. Repetição não cria obrigação.
2. **Prática observada nunca vira exigência.** Uma linha de `achados.csv` só sobe
   para `obrigacoes.csv` quando se encontra o dispositivo que a fundamenta — e
   aí a linha nova cita o dispositivo, não o plano onde foi vista.

Essa ordem existe porque o projeto foi desenhado para ser delegado. Quem receber
a pasta precisa saber decidir sem perguntar.

---

## Instalação

**Mac**
```bash
python3 -m venv ~/.venvs/planos && source ~/.venvs/planos/bin/activate
pip install -r requirements.txt
brew install tesseract tesseract-lang poppler node
npm ci
```

**Windows (PowerShell)**
```powershell
py -m venv $HOME\.venvs\planos; & $HOME\.venvs\planos\Scripts\Activate.ps1
pip install -r requirements.txt
npm ci
```

O `requirements.txt` fixa a versão exata do `pdfplumber` e do `pdfminer.six`: é a
combinação que reproduz byte a byte as CSVs de `extraidos/`. Versão nova do leitor
de PDF muda quebra de linha e detecção de tabela.

Programas de fora do Python:

- **Tesseract com o idioma `por`** — para o OCR. Sem ele, página digitalizada sai
  vazia e as verificações A, E e G do `conferir.py` não rodam. No Windows, o
  instalador do UB Mannheim põe em `C:\Program Files\Tesseract-OCR`, e os
  scripts o acham lá mesmo fora do PATH. O `meta.yaml` registra a versão: o
  mesmo PDF sai com OCR diferente em versões diferentes.
- **pdftotext** (poppler) — para a verificação N do `conferir_plano.py`, que lê o
  valor unitário na portaria. O Git para Windows já traz um, e os scripts o
  acham. Sem ele, a N sai como NÃO SE APLICA e o relatório termina com aviso.
- **Node** — só para gerar o `.docx` (`npm ci` instala o pacote `docx`).

Não instalar `rapidocr`: reconhece sem acentuação, e texto sem acento contamina
a comparação de cobertura.

**O repositório não converte fim de linha** (`.gitattributes`). Cada arquivo tem
os mesmos bytes no Mac e no Windows, que é o que mantém válida uma conferência
feita no outro computador e o "reconstruir dá igual" do tratamento. Os scripts
gravam em LF em qualquer sistema.

Três regras se a pasta ficar no Google Drive:

1. Marcar como **disponível offline** nos dois computadores. Com streaming
   ligado o arquivo é um ponteiro e o Python falha ao abrir.
2. **Nunca** criar o venv dentro do Drive. Milhares de arquivinhos sincronizando,
   e binários de Mac e Windows se sobrescrevendo.
3. **Nunca** colocar repositório Git dentro do Drive. A sincronização corrompe
   o `.git`.

---

## Extração

Nomeie os PDFs no padrão `pt_ses_<NN>_<processo>.pdf` — por exemplo
`pt_ses_01_030989-2026.pdf` — em `planos_aprovados/`. Sem espaço no nome.
Depois:

```bash
python3 ferramentas/extrair_planos.py estudo/planos_aprovados/ estudo/extraidos/
```

O script faz texto e tabela na **mesma varredura**, página a página. O texto das
tabelas é removido do texto corrido — senão viria embaralhado — e substituído
por um marcador `[[tabela: pNNN_tNN]]` **na posição vertical em que a tabela
estava**. O conteúdo vai para `tabelas/pNNN_tNN.csv`.

O script avisa quando encontra páginas sem texto extraível, o que indica
digitalização e necessidade de OCR.

### Ajuste por página

Tabela sem borda, moldura de página lida como coluna, sombreado de linha lido
como separador: não se resolve com um ajuste global, porque o que conserta uma
página estraga outra. Cada caso vira uma entrada no dicionário `AJUSTES` do
script, com o motivo escrito ao lado:

```python
ajustar("pt_ses_04", range(21, 33),
        settings={"intersection_x_tolerance": 1.0},
        nota="sombreado de linha lido como separador de linha")
```

Cada entrada aceita `settings` (repassado a `find_tables`) e `recorte` (a região
onde a tabela vive). Página sem entrada segue o comportamento padrão — por isso
acrescentar um ajuste não mexe no que já estava certo. Depois, reprocesse **só**
o documento afetado:

```bash
python3 ferramentas/extrair_planos.py estudo/planos_aprovados/ estudo/extraidos/ --doc pt_ses_04
```

As páginas ajustadas ficam registradas em `paginas_ajustadas` no `meta.yaml`.

### PDF sem camada de texto

O `pt_ses_05` é digitalização integral: 58 páginas, nenhuma com objeto de texto.
Isso muda duas coisas — e o que resolve as duas é o `extrair_digitalizados.py`,
descrito no fim desta seção.

A primeira é que **o OCR passa a ser a extração, não a recuperação**. As 58
páginas saem com o comentário `<!-- ocr pagina N - REVISAR -->`, e nenhum número
do documento foi lido nativamente.

A segunda é que **não há tabela**. O `pdfplumber` lê tabela a partir de objetos
de texto e linhas de régua; numa imagem ele encontra a régua e não encontra o
texto, e devolve uma grade de células todas vazias. Isso é uma **moldura**, não
uma tabela, e o extrator a descarta — o campo `molduras_descartadas_por_pagina`
do `meta.yaml` registra onde. O descarte importa por um motivo que não é óbvio:
o gatilho do OCR exige página sem texto **e** sem tabela, então a moldura, antes
de ser descartada, bloqueava o OCR e deixava a página em branco sem avisar. Foram
23 das 58 páginas, a planilha orçamentária inteira entre elas.

A consequência prática fica registrada em `AC-052`: sem tabela não há
`planilha.csv`, e sem `planilha.csv` as verificações **B**, **C**, **D** e **I**
do `conferir.py` não têm o que conferir. Elas imprimem `OK` sobre zero linha, e
**`OK` sobre zero linha não é plano conferido**. Ler o relatório desse documento
sem olhar a contagem de CSVs é o erro a evitar.

A saída é ler a grade desenhada em pixel e fazer OCR célula a célula:

```bash
python3 ferramentas/extrair_digitalizados.py estudo/planos_aprovados/ estudo/extraidos_ocr/ --doc pt_ses_05
python3 ferramentas/extrair_digitalizados.py estudo/planos_aprovados/ estudo/extraidos_ocr/ --doc pt_ses_05 --paginas 41,50
```

O segundo comando é amostra, para ajustar parâmetro: grava em
`extraidos_ocr/_amostras/`, sem tocar na extração inteira. O `meta.yaml` traz a
confiança do OCR por página e os códigos de item que o OCR leu sem os pontos
("2141" onde o PDF diz 2.1.1) — esses se conferem na imagem e viram correção de
forma em `correcoes.csv`. A planilha do `pt_ses_05` sai costurada
(`planilha_p041-p053.csv`), chega a `normalizados/` pelo tratamento e fecha nas
verificações C, D e I.

### Conferência obrigatória

Planilha orçamentária e cronograma físico-financeiro são o núcleo de um plano de
trabalho, e são exatamente o que extração automática corrompe — sobretudo quando
a tabela não tem bordas. **Confira cada CSV contra o PDF** e só então registre:

```bash
python3 ferramentas/conferencia.py estudo/extraidos/ --marcar pt_ses_01 --por HB
```

Sem essa marcação você não sabe, seis meses depois, em qual número pode confiar.

O registro é `registros/conferencia.csv` — dado, como o `correcoes.csv` — e cada
linha guarda o **sha256 do conteúdo no momento da conferência** e a **pasta**
conferida (`extraidos`, `extraidos_ocr` ou `normalizados`: cada uma é uma leitura
diferente do mesmo plano). `python3 ferramentas/conferencia.py estudo/extraidos/` recalcula o hash de
agora e diz `vale` ou `CADUCOU`.

Essa âncora não é preciosismo. A marcação morava no `meta.yaml` como
`tabelas_conferidas`, e era um bug: o extrator monta o `meta.yaml` do zero e
escreve por cima, com o campo em `false` fixo. Reprocessar um documento — que é
o que a seção anterior manda fazer depois de acrescentar um ajuste de página —
apagava a marcação sem dizer nada. E só preservar o campo seria pior: o `true`
sobreviveria a uma reextração que mudou o conteúdo, e passaria a afirmar
"conferido" sobre números que ninguém viu. Marcação de conferência tem que
caducar sozinha quando o conteúdo muda.

Dá para marcar arquivo por arquivo, quando a leitura foi parcial, e para
distinguir leitura limpa de leitura que achou defeito:

```bash
python3 ferramentas/conferencia.py estudo/extraidos/ --marcar pt_ses_01 --por HB \
    --alvo tabelas/p034_t01.csv --resultado com_achado \
    --observacao "soma não fecha; ver achados.csv"
```

`com_achado` continua sendo conferido: diz que a leitura foi feita e o que
sobrou de errado está em `achados.csv`. Conferido e correto são coisas
diferentes.

O `conferir.py` faz a parte mecânica dessa conferência — não substitui a
leitura, mas diz onde olhar:

```bash
python3 ferramentas/conferir.py estudo/extraidos/ estudo/planos_aprovados/
```

Oito verificações: quatro numéricas, três de texto e uma da consolidação. **A**
relê cada página com OCR e compara os valores monetários com a extração nativa.
**B** olha estrutura da CSV. **C** confere subtotal contra soma dos itens,
encadeando páginas — e trata linha só com valor, sem rótulo e sem descrição,
como total de rótulo perdido, não como item: lê-la como item faz o subtotal
seguinte contar o valor duas vezes e acusar diferença que não existe. **D**
confere, linha a linha, se o total é o produto dos
fatores — é o teste mais forte, porque só fecha se cada número estiver na coluna
certa. **E** mede cobertura de palavras, **F** procura artefato de quebra de
linha e **G** compara a ordem de leitura. **I** roda sobre a `planilha.csv` e
por isso só tem o que conferir em `normalizados/` — ver abaixo. O script não
altera nada; imprime o relatório e sai com código 1 quando uma verificação
numérica (A, C, D ou I) acusa. As de texto são aviso.

As letras daqui (A a I) são as da extração. As do `conferir_plano.py` (A a X,
PADRAO.md) são outra lista, sobre o plano redigido: a mesma letra não quer dizer
a mesma coisa nos dois.

Falha que sobra depois do ajuste costuma ser defeito do documento, não da
leitura. Nesse caso não se conserta: registra-se em `achados.csv`, com o
`arquivo:linha` da evidência.

---

## Tratamento

```bash
python3 ferramentas/tratar_planos.py estudo/extraidos/ estudo/normalizados/
```

Lê `extraidos/`, `extraidos_ocr/` e `registros/correcoes.csv` e escreve
`normalizados/`, sob três regras:

1. `extraidos/` é bruto e só o extrator escreve lá.
2. `normalizados/` é derivado e descartável: apagar a pasta e rodar de novo
   produz os mesmos bytes. Por isso não entra data nem hora em nada que sai lá.
3. `correcoes.csv` é **dado**, não código — uma linha por célula corrigida, com
   `plano, arquivo, linha, campo, valor_novo, classe, motivo`. `linha` e `campo`
   são 1-based e apontam para a CSV da pasta bruta. `linha` 0 é o cabeçalho que a
   extração não capturou — o do `pt_ses_05` está na página 40, fora da grade
   lida. Só entra classe `forma` (quebra de palavra pela largura da célula,
   ponto de código perdido no OCR, e coisas dessa natureza). Defeito do
   documento é recusado ali e vai para `achados.csv`.

O tratamento junta cabeçalho quebrado, tira cabeçalho repetido no meio da
planilha e linha vazia, e uniformiza a convenção decimal — o pt_ses_01 mistura
`1.216,00` e `1,216.00` dentro do mesmo documento, e o separador decimal é o
último que aparece.

O ganho maior é o `normalizados/<plano>/planilha.csv`: a planilha orçamentária
atravessa dezenas de páginas e sai como uma CSV por página; consolidada, com
`pagina_origem` e `csv_origem` em cada linha, dá para somar e ainda voltar ao
PDF. Item cuja descrição vira a página é emendado, e as duas origens ficam
registradas.

Rodar o `conferir.py` **nos dois lados** é o fecho: o que melhorar é forma, o
que sobrar igual nos dois é defeito do documento.

```bash
python3 ferramentas/conferir.py estudo/normalizados/ estudo/planos_aprovados/
```

### Verificação I — a consolidação

De A a G, todas leem uma CSV por página. Cada CSV isolada pode estar perfeita
enquanto a **junção** entre elas está errada, e é justamente aí que mora o risco
da `planilha.csv`. A **I** roda sobre ela e confere três coisas:

1. **Numeração dos itens.** A planilha numera item dentro de etapa — 1.1.1,
   1.1.2, e recomeça em 1.2.1. Buraco significa linha perdida; repetição, linha
   contada duas vezes. É o teste que a aritmética não faz: se a cadeia parar no
   meio, o bloco perdido leva junto o subtotal dele, e a soma dos itens que
   sobraram continua fechando com os subtotais que sobraram. O **C** não acusa
   nada. A numeração acusa.
2. **Hierarquia ponta a ponta**, com itens de páginas diferentes no mesmo
   subtotal — o que prova que as emendas de virada de página caíram no lugar
   certo.
3. **Truncamento.** Consolidada que não termina em total geral é cadeia que
   parou cedo.

Sem `planilha.csv` a verificação não se aplica e diz isso, então rodar em
`extraidos/` não gera ruído.

O **C** e a **I** sobem a mesma hierarquia pela mesma função (`escada`). O que
muda entre as duas é só como as linhas foram reunidas — o C encadeia páginas de
`extraidos/`, a I lê a consolidada. Se as duas divergirem, o relatório passa a
afirmar coisas diferentes sobre o mesmo documento, e quem lê não tem como saber
qual está certa.

### Testes

```bash
python3 ferramentas/testar_tudo.py              # suítes, planos redigidos, extração tratada, registros
python3 ferramentas/testar_tudo.py --mutacoes   # mais o arnês de mutação dos planos (~30 s)
```

Só biblioteca padrão — nenhuma suíte abre PDF. A integração contínua do GitHub
roda o segundo comando a cada envio (`.github/workflows/testes.yml`).

| suíte | o que fixa |
|---|---|
| `testar_conferir.py` | classificação de linha, a escada nos três níveis, a numeração dos itens, a equivalência entre C e I, e os cinco planos de `normalizados/` fechando |
| `testar_conferencia.py` | a marcação caduca quando o conteúdo muda, sobrevive a reextração idêntica, enxerga arquivo entrando e saindo, pertence à pasta em que foi feita e não caduca por fim de linha |
| `testar_tratar.py` | `normalizados/` se reconstrói byte a byte; decimal, código de item, limpeza da rodada anterior, cabeçalho de linha 0 e planilha costurada |
| `testar_registros.py` | os registros reais sem erro de schema, e cada classe de erro sendo apanhada |
| `testar_conferir_plano.py` | a leitura do `estado.yaml`, os números, a C no modo em que a fila define o recurso |
| `testar_devolutiva.py` | o texto de link e de inserção controlada na devolutiva |
| `testar_conferencia_plano.py` | injeta um erro conhecido por vez num plano real e exige que a verificação certa o apanhe |

---

## Procedimento

### Fase 0 — Fundação
Estrutura criada, script rodando nos dois computadores, PDFs extraídos, tabelas
conferidas. Preencher uma linha de plano em `acervo.csv` por documento, com `url`
e `data_acesso` — página de secretaria reorganiza e derruba link, e sem isso não
há proveniência nem como reencontrar o original. A listagem de origem é
`https://www.saude.df.gov.br/convenios-suconv`, e é lá que estão também os termos
de convênio e os apostilamentos, que o acervo ainda não cobre.

### Fase 1 — Fichamento

**Um plano por conversa. Nunca vários juntos.**

Dois motivos:

- **Custo.** Os cinco somam ~100k tokens, e cada turno seguinte reprocessa o
  contexto inteiro. Conversas separadas saem em torno de 1/3 do custo.
- **Ancoragem.** Com todos em contexto, a ficha do plano 3 sai descrita nos
  termos do plano 1 e as diferenças reais achatam.

Ficha é **observação independente**. Comparação é a `sintese.md`, feita depois, a
partir das fichas — não dos `texto.md`.

Procedimento por plano: abrir conversa nova, anexar o `texto.md` (e as CSVs de
tabela que a ficha exigir), pedir a ficha conforme `schema.md`, salvar em
`destilados/fichas/pt_ses_XX.md`, fechar a conversa.

Depois do **segundo** plano, parar e revisar o `schema.md`. Se faltou campo,
ajustar e refazer a Ficha 01. É barato agora e caro depois.

Enquanto ficha, toda citação normativa que aparecer vira linha em
`obrigacoes.csv` com `status_vigencia: a_verificar`. Toda observação vira linha
em `achados.csv`.

Mapear o índice dos outros três processos SEI aqui, não antes — o schema só fica
estável depois do segundo plano.

### Fase 2 — O instrumento

Descobrir qual norma rege convênio de saúde para participação complementar ao
SUS, e qual é o conteúdo obrigatório do plano de trabalho segundo essa norma.

**Resolver antes de escrever qualquer linha do `obrigacoes.csv`:** a Lei
13.019/2014 (MROSC) tem exclusão expressa para convênios com entidades
filantrópicas e sem fins lucrativos que participam de forma complementar do SUS.
Se for esse o caso, a espinha dorsal é outra — art. 199, §1º da CF, Lei 8.080/90
e a norma distrital correspondente. **Confirmar, não assumir**, e confirmar
também a camada distrital, que é onde a SES efetivamente se apoia.

#### O que o termo de convênio respondeu — 31/08/2026

*Registro do estudo. O que se sabe hoje sobre o instrumento, com as correções
posteriores (a IN 01/2005 incide pelo veículo orçamentário, não pela origem do recurso),
está em `biblioteca/instrumento/convenio_ses_df.md`.*

O Termo de Convênio 031061/2026 (`IT-001`) resolve metade da pergunta, porque
diz textualmente sob que normas a SES celebra:

> Lei nº 14.133, de 1º de abril de 2021, Decreto Distrital nº 44.330, de 16
> março de 2023, Instrução Normativa nº 01/2005 da Corregedoria-Geral do
> Distrito Federal, Lei de Diretrizes Orçamentárias vigente

**Não há MROSC** — a suposição acima se confirma. Mas **também não há art. 199,
§1º da CF nem Lei 8.080/90**: a SES rege o convênio pela lei de licitações e
contratos. As duas coisas não se contradizem — a Constituição não precisa ser
citada para valer, e o `OB-001` continua de pé — mas quem escreve o plano deve
saber que **a concedente raciocina pela 14.133**, não pela lógica sanitária.

A camada distrital pedida no parágrafo anterior é o Decreto 44.330/2023
(`NM-009`) e a IN 01/2005 (`NM-011`), as duas já no acervo. A IN 01/2005 se
aplica porque o recurso é **distrital** — cláusula 5.1, dotação
`10.302.6202.4205.0001`, fonte `1600.739030844`, natureza `335043`.

Falta a segunda metade da pergunta: o conteúdo obrigatório do plano segundo
essas normas. As cláusulas do termo já entregaram seis linhas (`OB-041` a
`OB-046`); as outras catorze cláusulas ainda não foram varridas.

### Fase 3 — Financiamento e assistência
SIGTAP e a lógica da OCI; APAC e registro no SIA/SUS; FAEC vs. teto MAC; repasse
fundo a fundo; PMAE/PATE. Depois PDS 2024–2027, PAS e RAG.

### Fase 4 — Custo, risco e contas
Memória de cálculo e pesquisa de preços; matriz de risco P×I; prestação de
contas e monitoramento.

### Fase 5 — Controle e validação

Pareceres da PGDF e decisões do TCDF sobre planos de trabalho e parcerias na
saúde. É aqui que aparece **o que derruba um plano** — informação que nenhum
plano aprovado contém.

Em 27/09/2026: quatro dos cinco aprovados estão sob representação do MPCDF no
TCDF (CT-001 a CT-004). O que foi atacado virou lição em `registros/licoes.csv`,
e dela saiu o `destilados/criterios.md`. O papel do `validador.py` ficou com o
`conferir_plano.py` (verificações W e X, do controle) e com o
`consultar.py checklist` — ver "Consulta — erros e acertos", acima.

Fecha `criterios.md` e `modelo.md`, e entrega o `validador.py`.

**`validador.py`** — script local que confere o rascunho próprio. Custo zero de
tokens, roda quantas vezes quiser. Verificações:

1. soma das metas × quantitativo declarado no objeto
2. percentuais × valores das parcelas
3. vigência declarada × frequência da planilha
4. data da parcela × data de apuração
5. consistência do código SIGTAP entre seções
6. cobertura das seções exigidas contra o `obrigacoes.csv`

Especificação de teste: **os sete erros encontrados no pt_ses_01 (IEV/DOAR)**. O
validador só está pronto quando pega os sete rodando sobre aquele plano.

### Fase 6 — Redação
Projeto separado, em `redacao/`. Só entram `modelo.md`, `obrigacoes.csv` e
`criterios.md`. **Nunca** as fichas nem os `texto.md`.

Essa fronteira é o que impede o produto final de virar cópia dos planos
existentes — que é exatamente o risco quando o objetivo é superá-los.

---

## criterios.md — dois eixos

O arquivo tem duas seções, e elas respondem a perguntas diferentes. Não misturar.

**Eixo 1 — Administração: o que aprova e o que reprova.**
Critério da SES, da PGDF e do TCDF. Define o mínimo viável. Fontes: checklist
interno, pareceres, diligências, decisões de controle.

**Eixo 2 — Qualidade: o que é boa prática.**
O que o professor e revisores indicam como bom, **inclusive quando nenhum dos
quatro planos faz**. Este eixo não se extrai do corpus — o corpus é justamente o
conjunto do que passou, não do que é bom.

É o eixo 2 que separa o plano excelente do mínimo viável, e o objetivo declarado
do projeto é o excelente. Um item pode existir só no eixo 2, e isso não é defeito
do item: é o ponto.

---

## Processos SEI — enriquecimento opcional

**Está decidido não fazer pedido por LAI.** Portanto: o `modelo.md` tem que ser
fechável apenas com os planos publicados, as normas e os critérios do professor.
O inteiro teor do processo é opcional por definição — se aparecer depois,
enriquece; se não aparecer, nada trava. Nenhuma fase depende dele.

### O que já sobreviveu do índice e entra em `criterios.md` agora

O processo mapeado está com acesso restrito na consulta pública, mas o índice
(protocolos, datas, unidades) já entrega três coisas que valem sozinhas:

1. **As quatro versões do plano, com datas.** 1ª em 02/02/2026, 2ª em 26/02/2026,
   3ª — aprovada — em 06/04/2026, e a do 1º Termo Aditivo em 11/08/2026. Nove
   semanas e três versões até aprovar; aditivo quatro meses depois de aprovado.
   Ordem de grandeza do rito, e sinal de que aprovação não é o fim do risco.
2. **A cadeia de análise:** GPICP → GESCIR / SAIS → SEGEA / SEAS / SECCIC.
   Relatório preliminar, depois parecer técnico em dois níveis, depois aprovação
   em três instâncias.
3. **A leitura que decorre das duas:** o plano é lido por instâncias com
   critérios distintos, ao mesmo tempo. É escrito para todas de uma vez.

### Se o inteiro teor aparecer, ordem de valor

1. Lista de Verificação, versão de celebração — critério de aprovação em forma
   de formulário.
2. Versões 1, 2 e a do aditivo — três diffs em cadeia mais um pós-execução.
3. Relatórios Preliminares (GPICP) — listam exigências item a item; os ofícios
   são só o veículo.
4. Parecer jurídico referencial — fixa a base legal do tipo de convênio.
5. Ciclo de execução (notificação, termo aditivo) — mostra o que quebra depois
   da aprovação.

Só nesse caso o `exigencias_resposta.csv` deixa de ser um arquivo vazio.
