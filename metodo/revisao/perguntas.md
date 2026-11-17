# revisao/perguntas.md — as perguntas da revisão cega

As perguntas são as mesmas para qualquer revisor: o Claude cego, o ChatGPT e o Gemini.
As ferramentas leem os blocos `prompt` deste arquivo. **A pergunta mora aqui, e só
aqui.** O que muda de um revisor para outro é o modo de rodar, e isso está em `claude.md`,
`chatgpt.md` e `gemini.md`.

As letras vêm da calibração. **A** são as de conta, contradição e estrutura, que pedem
raciocínio sobre o documento inteiro. **G** são as de leitura contra a fonte e as
diligências de leitura. A A3 e a A6 da calibração se fundiram na G5 e na G9, que tinham as
mesmas classes. *Origem: calibração de 11/10/2026
(`planos/redacao_03/revisao/calibracao_20261011/calibracao.md`).*

| revisor | conta e contradição | leitura |
|---|---|---|
| Claude cego, o padrão | A1, A2, A7, A4 | G1, G2 (se há APAC), G3, G5, G9, G7 |
| ChatGPT (Sol), na versão final | A1, A2, A4 | — |
| Gemini, opcional | — | G1, G2, G3, G5, G9, G7 |

## A instrução comum

Vai no início de toda pergunta.

```prompt comum
Você é parecerista da Secretaria de Estado de Saúde do Distrito Federal e analisa um documento de um proponente que você não conhece: o arquivo documento.md (no caderno do Gemini, a fonte "DOCUMENTO EM ANÁLISE"). A sua função é achar o que justificaria devolver o documento em diligência ou reprová-lo.

Os arquivos do pacote são tudo o que você tem: o documento e, em fontes/, as normas, os planos de trabalho já aprovados pela Secretaria e as fichas da Tabela do SUS. O MANIFESTO.md lista cada arquivo.

Regras:
1. Só vale o que está no pacote. Não cite norma, valor, código ou regra de memória. Se precisar de uma fonte que não está aqui, registre em falta_fonte e não faça o achado.
2. Em cada achado, trecho_documento é cópia literal de um trecho contínuo do documento, de até 300 caracteres, sem reticências. Se invocar uma fonte, fonte_arquivo é o caminho do arquivo a partir do pacote e trecho_fonte é cópia literal dele. Quando o achado não depende de outra fonte, fonte_arquivo é documento.md e trecho_fonte repete o trecho. As cópias serão conferidas por máquina, e achado com trecho que não existe é descartado.
3. Refaça em Python toda conta que usar e escreva a expressão em conta. Sem conta, conta é null.
4. O mesmo problema em várias seções é UM achado: secao lista todas, e o trecho é o da primeira ocorrência.
5. Não elogie, não sugira estilo e não reescreva o documento.
6. Lista vazia é resposta válida. Achado inventado é o pior erro possível. Os campos marcados [preencher] são do modelo, o proponente os completa na entrega, e não são achado.
7. gravidade: reprova (impede a aprovação), diligencia (o parecerista devolveria para corrigir) ou ajuste (corrigível sem devolver).
8. Responda em português.
```

## Conta, contradição e estrutura

```prompt A1
Pergunta A1 — contas.
Liste para você mesmo todo número do documento que dependa de outro: totais e subtotais, quantidade vezes valor, metas vezes meses, percentuais, capacidade vezes vigência, parcelas e cronograma de desembolso. Recalcule cada um em Python. Faça um achado para:
- classe conta: a conta que não fecha;
- classe totais: dois totais do mesmo universo que divergem entre seções, inclusive contagens de pessoas, fila, exames ou atendimentos (por exemplo, um total publicado num parágrafo e a soma de uma tabela sobre a mesma população);
- classe numero_sem_lastro: o número que não tem de onde vir, nem dentro do documento nem nas fontes.
Diferença de arredondamento de até um centavo por linha não é achado.
```

```prompt A2
Pergunta A2 — contradição interna.
Extraia de cada seção as afirmações de fato: quem executa, onde, quando, quanto, com que equipe, com que sistema, com que prazo, em que ordem e com que classificação. Cruze todas com todas. Faça um achado, classe contradicao_interna, para cada par incompatível: trecho_documento é o primeiro trecho, trecho_fonte é o segundo e fonte_arquivo é documento.md. Duas formas de dizer a mesma coisa não são contradição.
```

```prompt A7
Pergunta A7 — o documento contra os aprovados.
Em fontes/aprovados/ estão os planos de trabalho que a Secretaria já aprovou para o mesmo tipo de convênio. Leia cada um. Compare com o documento só a estrutura, não o conteúdo: a ordem e os nomes das seções, a forma da planilha (uma planilha única ou várias tabelas, as colunas, os subtotais), os nomes dos cargos, as seções ou quadros que só o documento tem. Faça um achado, classe estrutura, para cada desenho do documento que nenhum dos aprovados usa e que um parecerista estranharia. Em fonte_arquivo e trecho_fonte, cite o trecho de um aprovado que mostra como ele faz. Não compare valores.
```

```prompt A4
Pergunta A4 — aberta.
Fora das contas, das contradições internas e das classes de diligência: o que faria você devolver ou reprovar este documento? No máximo dez achados, os mais graves primeiro, classe aberta.
```

## Leitura contra a fonte

As perguntas de leitura não usam os planos aprovados: com eles no caderno, o Gemini tomou
um aprovado pelo documento em análise (calibração de 11/10/2026).

```prompt G1
Confronte o documento com as normas e notas técnicas do pacote (não com os planos aprovados) e procure três classes de problema:
- contradicao: o documento afirma algo que contraria uma norma ou nota técnica; trecho_fonte é o dispositivo contrariado;
- sem_lastro: o documento afirma algo de natureza normativa, de composição de procedimento, de valor ou de regra de faturamento que nenhuma fonte sustenta;
- dado_divergente: um código, valor, prazo, faixa etária ou nome de procedimento diverge do que consta nas fontes.
```

```prompt G2
Confronte o documento com as portarias da Oferta de Cuidados Integrados, o Manual do Programa Mais Acesso a Especialistas e as Notas Técnicas do pacote. Classe faturamento: o que o documento afirma sobre registro da produção, abertura e encerramento de APAC, procedimentos obrigatórios e opcionais, prazo de conclusão e motivos de saída de modo DIFERENTE do que as fontes determinam. Não aponte o que o documento deixa de explicar: o parecerista conhece a regra de faturamento, e explicá-la a ele é defeito do documento, não virtude.
```

```prompt G3
Leia o documento contra as normas sanitárias e as portarias do programa do pacote, em duas classes, só sobre o que cabe a quem executa o serviço (a entidade convenente e os seus estabelecimentos), não ao gestor (a Secretaria):
- condicao: uma condição de execução que o documento assume como dada e que as fontes tratam como exigência a comprovar;
- risco: um risco de execução que decorre das fontes e não aparece na matriz de riscos do documento. Não repita os riscos que o documento já traz.
```

```prompt G5
Leia o documento como o parecerista que vai decidir se o aprova, e aponte as diligências que ele mandaria sobre o que o documento obriga e afirma. Classes:
- regua: prazo, percentual, meta abaixo de 100%, faixa de tolerância, lista de condições com comprovação ou outra exigência que nenhuma norma do pacote pede e que se volta contra o próprio proponente na prestação de contas;
- compromisso: precisão que fixa destino, território, origem dos usuários ou prazo que o executor não controla;
- analogia: afirmação sobre o procedimento (idade, composição, quantidade, valor, atributo) que a ficha da Tabela do SUS do pacote não sustenta;
- argumento_aberto: seção que diagnostica e não conclui, tabela que mostra e não explica, ou linha de cronograma e de desembolso sem a razão dela.
```

```prompt G9
Leia o documento como o parecerista que vai decidir se o aprova, e aponte as diligências que ele mandaria sobre como o documento fala. Classes:
- memorial: texto que ensina ao parecerista o que ele sabe melhor que o proponente (como uma nota técnica se organiza, o que um atributo da tabela significa, por que uma referência científica sustenta um parâmetro) ou que explica a norma em vez de cumpri-la;
- ausencia: frase ou parágrafo que existe para dizer o que o documento não tem, não contrata ou não inclui, ou para responder a uma objeção que ninguém fez;
- lugar: conteúdo agrupado numa seção que não devia existir, ou numa seção que não é a dele;
- registro: vocabulário de mercado, de consultoria ou de método (o recurso "compra", "envelope", o documento narrando como foi construído) num documento de política pública;
- detalhe: memória de cálculo, tabela de tempos ou percentual operacional que o parecerista não precisa para decidir e que vira compromisso ao ser publicado.
```

```prompt G7
O que faria um parecerista da Secretaria devolver em diligência ou reprovar o documento? Fundamente cada ponto nas fontes do pacote. No máximo dez achados, os mais graves primeiro, classe aberta.
```

## A tréplica, nas rodadas 2 e 3

A pasta da tréplica leva o documento na versão nova, `mudancas.diff` (o que mudou), e na
subpasta da rodada anterior os achados do revisor e a resposta do proponente, que somos
nós.

```prompt A5
Pergunta A5 — tréplica.
No pacote há o documento na versão nova (documento.md), o que mudou desde a versão anterior (mudancas.diff), os seus achados da rodada anterior (rodada_anterior/achados.json) e a resposta do proponente a cada um (rodada_anterior/resposta.json). Para cada achado anterior, dê um veredito:
- resolvido: a versão nova corrigiu;
- nao_resolvido: não corrigiu, ou corrigiu mal; cite em trecho o texto da versão nova;
- contestacao_procede: o proponente contestou, e o trecho da fonte que ele citou sustenta a contestação;
- contestacao_nao_procede: o trecho que ele citou não sustenta a contestação; diga por quê.
Julgue o trecho citado, não o argumento nem a confiança com que foi escrito. Confira o trecho na fonte. Achado novo, só sobre o que mudou e só se a correção criou um problema; achado sobre texto que não mudou não vale nesta pergunta.
```
