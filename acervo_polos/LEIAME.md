# Acervo de polos e clínicas parceiras

Registro do que cada polo tem, não tem, pode e não pode fazer, com as fotos que
comprovam. Serve ao plano em curso (ultrassom e tomografia) e fica para as próximas
parcerias.

## Como usar

Dois cliques em **`abrir_acervo.bat`** (ou `python app.py`). O navegador abre em
`http://127.0.0.1:8765`, só neste computador.

1. **Escolha o polo** na lista da esquerda, ou crie um em "Novo polo".
2. **Busque no CNES** pelo nome da clínica, CNPJ ou número. O que o cadastro oficial
   tiver — razão social, endereço, contato, licença sanitária, equipamentos, serviço de
   imagem com ou sem marca SUS — aparece como **sugestão para confirmar**. Nada entra na
   ficha sem um "Aceitar".
3. **Escreva as anotações da visita** do seu jeito e clique em "Interpretar com IA". Ela
   distribui o que você escreveu nos campos e mostra, em cada sugestão, o trecho em que
   se apoiou.
4. **Complete à mão** o que faltar: cada item é um clique (ok, ajustar, não tem, n/a)
   e uma observação.
5. **Fotos:** arraste para o ambiente certo na aba Fotos.

Salva sozinho a cada alteração.

### Onde fica salvo e como enviar

Tudo fica em arquivos desta pasta, neste computador — nada vai para a internet. Cada
alteração é gravada em menos de um segundo no `dados.json` do polo, e o aviso "salvo às
hh:mm" aparece no alto. Fechar o navegador não perde nada; para cópia de segurança,
copie a pasta `polos_us_tc` inteira.

Para mandar a alguém:

- **Gerar relatório** (no alto do polo) cria `relatorio.html` na pasta do polo: uma
  página só, com a ficha e as fotos dentro. É um arquivo único, abre em qualquer
  navegador ou celular, e vira PDF com Ctrl+P → "Salvar como PDF".
- **Relatório de todos os polos** (abaixo da lista) cria `relatorio_geral.html` na raiz:
  a tabela de polos com parecer e pendências.

O relatório é uma fotografia do momento: mudou a ficha, gere de novo.

### Essencial e complementar

A tela mostra só o **essencial**: o que viabiliza ou impede o atendimento e o que entra
na gestão de risco — regularidade, acessibilidade, o aparelho, a equipe, a resposta a
intercorrência, a capacidade. O percentual de cada polo conta só esses itens.

O resto (vaga de PcD, internet, climatização, piso tátil…) é **complementar**: aparece
ao marcar "Mostrar itens complementares" e só sai no `.md` se for preenchido. O que é
essencial se decide em `esquema.py`: item complementar leva um `X` no fim da linha.

### Responsável técnico e horário

- O CNES não marca quem é o responsável técnico. O aplicativo lista os médicos e
  diretores vinculados ao polo e você clica em quem for.
- O CNES só sabe o turno (manhã, tarde). "Buscar na web com IA" procura o horário no
  perfil da clínica no Google e no site dela, e devolve como sugestão com a fonte;
  "Abrir no Google Maps" leva direto à clínica para conferir à mão.

### A IA

Usa o Claude Code instalado neste computador, com o login que ele tiver — não precisa
de chave. Se aparecer "sem login", abra um terminal, rode `claude`, digite `/login` e
tente de novo. Para escolher o modelo, defina a variável `POLOS_IA_MODELO` antes de abrir.
Sem a IA, todo o resto funciona igual.

## Como está organizado

```
polos_us_tc/
├── abrir_acervo.bat     abre o aplicativo
├── app.py, app/         o aplicativo (servidor local e tela)
├── esquema.py           o que cada ficha pergunta — fonte da tela e dos .md
├── validar.py           conferência de CNPJ e CNES contra bases públicas
├── datasus.py           leitura dos arquivos mensais do CNES
├── cadastro.csv         a lista de polos (o aplicativo mantém)
├── INDICE.md            todos os polos numa tabela (o aplicativo gera)
├── _modelos/            as fichas em branco, geradas do esquema
├── _cache_cnes/         arquivos baixados do DATASUS — pode apagar, baixa de novo
└── setor_<região>/<polo>/
    ├── dados.json           o que foi preenchido — a fonte
    ├── polo.md              ficha do prédio, gerada de dados.json
    ├── vistoria_US.md       ficha do exame, só se o polo fará ultrassom
    ├── vistoria_TC.md       idem, tomografia
    ├── capacidade.md        capacidade e meta de cada exame, analisadas à parte
    ├── validacao.md         o que confere e o que diverge nas bases públicas
    ├── _consulta/           resposta bruta da Receita e do CNES
    └── fotos/<ambiente>/    01_fachada_acesso … 10_documentos
```

Os `.md` são para ler e anexar; **edita-se pelo aplicativo**. O que for escrito à mão
num `.md` gerado se perde no salvamento seguinte.

## Por que duas fichas

O **prédio** muda pouco e interessa a qualquer parceria: banheiros, acessibilidade,
recepção, fila, bebedouro, inventário de salas. É a aba "Prédio", preenchida uma vez.

O **exame** muda a cada plano: aparelho, sala específica, equipe, capacidade, CNES.
São as abas "Ultrassom" e "Tomografia".

O que não foi visto na visita fica em branco. Em branco quer dizer "não sei"; não
marcar "ok" por suposição.

## De onde vêm os dados oficiais

| o quê | fonte | atraso |
|---|---|---|
| CNPJ, razão social, situação, atividades (CNAE) | Receita Federal, por brasilapi.com.br ou minhareceita.org | dias |
| Nome, endereço, contato, turno do estabelecimento | API de dados abertos do Ministério da Saúde | dias |
| Equipamentos, serviço 121, marca SUS, licença sanitária, instalações | arquivos mensais do DATASUS (EQ, SR, ST do DF) | um a dois meses |
| Profissionais vinculados, por ocupação | arquivo mensal PF do DATASUS | um a dois meses |

O arquivo de profissionais é grande: na primeira busca de cada mês o aplicativo leva
alguns minutos para abri-lo; depois é imediato.

O que nenhuma delas responde: quem é o responsável técnico, a validade da licença
sanitária, o alvará de funcionamento e a vistoria dos Bombeiros. Esses se pedem em
cópia ao polo e vão para `fotos/10_documentos/`.

A validação também roda sem o aplicativo: `python validar.py` (todos) ou
`python validar.py CIG` (um).

## Modalidade nova

Para ressonância, endoscopia ou consulta: acrescentar a ficha em `esquema.py`, no
molde de `US` e `TC`, e a regra de equipamento e serviço em `IMAGEM`, no `validar.py`.
A tela e os `.md` saem do esquema sozinhos.

## Ligação com o plano de trabalho

- A aba **Capacidade e metas** fica fora da vistoria: preenche-se e analisa-se à parte,
  com o que o polo declarou e o que o plano pede, e não conta no percentual da ficha.
  Alimenta a subseção 6.3 do plano (salas e tomógrafos por polo). Sai em `capacidade.md`
  e numa tabela própria do relatório geral.
- A seção **CNES** é a conferência pedida em `planos-ses/destilados/enquadramento_cnes.md`,
  item 4: serviço com marca SUS, profissionais com o CBO, equipamento.
- A linha **vínculo formal com a entidade proponente**, na Documentação, é o ponto que
  o controle externo atacou nos convênios aprovados. Não deixar em branco.
