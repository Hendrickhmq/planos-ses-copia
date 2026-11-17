# 00_metodo.md — terceiro plano de trabalho

O acordo de trabalho **não muda**. Vale integralmente o `redacao_02/00_metodo.md`:
as rodadas, a regra do enxuto, o teste do leitor, o teste da norma citada, a
estrutura padrão de 9 seções, a forma dos títulos e as três regras. Este arquivo
registra só **o que é próprio deste plano**.

Leitura obrigatória antes de escrever qualquer seção:
`redacao_02/00_metodo.md` · `redacao_02/analise_aprovados.md` ·
`redacao_02/CONTINUAR.md`.

---

## Parâmetros travados em 31/08/2026

| parâmetro | decisão | quem decidiu |
|---|---|---|
| **Origem do recurso** | emenda parlamentar **federal**, R$ 8.500.000,00 | usuário |
| **Objeto** | **OCI 09.01.01.007-3 — Avaliação Diagnóstica de Câncer Gástrico** (consulta/teleconsulta + esofagogastroduodenoscopia + anatomopatológico) | usuário |
| **Unitário** | **R$ 600,11** — valor de tabela vigente da OCI (Portaria SAES/MS nº 4.653/2026) | norma |
| **Custo acessório** | **8%** era a entrada inicial; em 02/09/2026 o usuário abriu o teto para **até 8,5%**. A montagem de baixo para cima fechou em **R$ 718.200,00 = 8,45%** | usuário / derivado |
| **Vigência** | **10 meses** | usuário |
| **Quantitativo** | **12.967 OCI** — piso de (8.500.000 − 718.200) ÷ 600,11 —, resto de R$ 173,63 · 9 meses de produção · 75,29 por dia útil no regime pleno | derivado |
| **Eixo de desenho** | **ganhar na gestão**: concentrar o acessório em direção e coordenação, minimizar operacional e infraestrutura | usuário |
| **Diretório** | `redacao_03/`. Os anteriores não se tocam | — |

## O que é diferente neste plano

**1. O acessório é um quarto do menor do acervo.** 8,45% contra uma banda de 30,65% a
36,57% para quem levanta estrutura, e contra 16% no único caso que apenas
complementa estrutura existente. Isso é ativo de economicidade e **precisa aparecer
como argumento**, não como número solto — mas sem escrever "custo acessório" nem
publicar percentual, que é o que nenhum dos cinco aprovados faz.

**2. O eixo é a gestão, e a gestão é entrega.** Os cinco aprovados classificam
direção e coordenação em **Meta 01 — Planejamento e Estruturação da Execução**,
Etapa 1.1. Não são overhead: são a primeira entrega do convênio. A seção 5
(Metodologia) e a seção 8 (Planilha) têm de sustentar cada posto pelo passo do fluxo
que o exige — o método de baixo para cima continua valendo, e a gestão não é
exceção a ele.

**3. Não há preço a defender.** A Portaria SAES/MS nº 4.653, de 07/08/2026 (DOU nº
149, de 10/08/2026, s.1, p.61) fixou o Serviço Ambulatorial da OCI em **R$ 600,11**,
com efeitos desde a competência de agosto de 2026. A produção é remunerada pelo valor
federal vigente, e o convênio custa **R$ 655,50 por OCI** — 9,23% acima da tabela,
que é o custo inteiro da estrutura. A seção 3 transcreve a referência com data e
página de DOU; não constrói memória de cálculo do unitário.

**3.1. A mesma portaria mudou a composição da OCI, e isso é estrutural.** A descrição
vigente é *"consulta médica especializada, esofagogastroduodenoscopia (com ou sem
sedação), anatomopatológico, consulta ou teleconsulta de retorno"*, e o Anexo II
tornou a **sedação** (04.17.01.006-0) APAC secundária compatível. Duas consequências
que atravessam o plano inteiro: **são dois encontros por OCI**, e a conclusão depende
do retorno — governa as metas (rodada 2), o fluxo (rodada 4) e a curva do cronograma
físico, que precisa de janela de retorno no último mês. E a **sedação é custo
assistencial dentro do unitário**, o que exige do executor sedação habilitada e sala
de recuperação: condição de partida na seção 4, risco na seção 9, nenhuma linha na
planilha de apoio.

**4. Três polos, e a equipe de apoio dividida entre eles e a coordenação.** Decisão do
usuário em 01/09/2026: Ceilândia, Sobradinho e Gama, serviços de endoscopia já
licenciados do proponente. Em 02/09 o desenho da equipe foi corrigido — o que acontece
com o usuário presente (acolhimento, ficha, termo, lançamento de APAC) é feito no
polo e não numa central; o que independe dele (fila da regulação, cobrança de laudo,
prestação de contas) é único para os três.

## O que não muda, e vale repetir porque é onde se erra

- **O instrumento é convênio.** Espinha: art. 199, §1º da CF e art. 24, parágrafo
  único da Lei nº 8.080/1990. Camada distrital: **Decreto DF nº 48.727/2026**. A
  **IN CGDF nº 01/2005 incide**.
- **A fonte não é o FAEC.** Incremento MAC, art. 24 da Portaria GM/MS nº
  10.297/2026. O Agora Tem Especialistas é base paramétrica. A APAC é comprovação,
  não gatilho de pagamento. Isso vale também para o incremento da Portaria SAES/MS
  nº 4.282/2026 — ele é **referência de preço**, não fonte.
- **A planilha se monta de baixo para cima**, pelo fluxo, em três setores. O técnico
  (endoscopista, sedação, enfermagem de endoscopia, sala, torre, insumo, patologia)
  **está dentro dos R$ 600,11 e não se repete na planilha**. Recolocá-lo no apoio é
  duplicidade e vira achado.
- **Fronteira anticópia.** Os cinco aprovados geram achado, nunca parágrafo.

## Onde mora o estado

```
redacao_03/
  00_metodo.md              este arquivo
  estado.yaml               parâmetros e aprovações por rodada
  dados/envelope.md         a aritmética travada
  dados/valor_unitario.md   a OCI, a tabela e a origem do R$ 600,11
  dados/gestao_no_acervo.md direção e coordenação nos cinco aprovados
  secoes/NN_*.md            uma por rodada
  plano.md                  só no fim, na remontagem
```

O NotebookLM do objeto:
https://notebooklm.google.com/notebook/4b564246-d0c2-437f-a150-afadbec9c676
