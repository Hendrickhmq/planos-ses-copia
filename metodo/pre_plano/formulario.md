# pre_plano/formulario.md — o formulário da SES, campo a campo

O formulário é o "Plano de Trabalho Simplificado – Modelo Parceria" da SES (SEI
216131719), pedido pelo Ofício 387/2026 da ARINS. Os títulos de primeiro nível são os
nove campos dele, nesta ordem; a tabela que a verificação J lê está em
`../plano/estrutura.md`, estrutura `formulario_ses_parceria`, porque o plano de
trabalho também pode usar o formulário.

## O que cada campo tem

| campo do formulário | o que entra |
|---|---|
| Informações iniciais | o quadro de cadastro. No campo "OSC nos termos do MROSC?", o texto da SUCONV, **literal** |
| Objeto | um parágrafo amplo, com o nome da proposta ou da emenda, e a lista de OCIs ou procedimentos com código, composição, valor SIGTAP vigente e a portaria que fixou o valor |
| Justificativa | a fila da fonte pública (Mapa Social) com a data da consulta: pessoas e espera por item, e a proporção da fila que o recurso alcança, sem número fechado de atendimentos |
| Metodologia | público-alvo, local ("unidade identificada na formalização, com endereço e CNES"), nível de atenção, percurso do usuário em etapas |
| Objetivos | geral e específicos, curtos |
| Metas e indicadores | meta quantitativa (art. 7º, parágrafo único, da Portaria GM/MS 10.297/2026, quando o ofício a cita) dada em **valor**, com a quantidade de cada item pactuada com a SES; indicadores em 100% |
| Cronograma | três fases: implantação, execução, encerramento. Sem curva mensal |
| Aplicação das despesas | **só o custo assistencial**. Gestão e apoio entram numa frase: "completam o Valor Total e serão detalhados no plano de trabalho" |
| Interface com os sistemas | SISREG para ofertar as vagas e TrakCare para a contrarreferência, quando o paciente vem da regulação |

## O que não entra, e para onde vai

| item | para onde vai | quem tirou |
|---|---|---|
| Linha, valor e percentual do custo acessório | planilha do plano detalhado | SUCONV |
| Frase da sobra ("diferença de R$ X para o recurso") — depende da linha de apoio para fechar | plano detalhado | consequência da linha acima |
| Argumento jurídico de convênio ou MROSC, com artigos | é ato da SUCONV | SUCONV e usuário |
| Quadro de equipe, postos, salários | plano detalhado | usuário |
| Capacidade, salas, produção por mês, polos | plano detalhado | usuário |
| Desembolso mensal | instrumento | usuário |
| "Zerar a fila" e quantidade fechada por item, na versão geral | só na versão de item único, se houver | usuário |
| Responsabilidades e condições de formalização, lista de documentos | a SUCONV indica (item 5 do ofício) | o formulário não pede |
| Quadro com processo, ação orçamentária, GND, autoria | o quadro do formulário substitui | o formulário não pede |
| Campos "[a preencher]" e "não há dados para quantificar a fila" | dado com fonte, ou "na formalização" | usuário |

*Origem: redacao_05, 08/10/2026 — o que a SUCONV tirou, o que o usuário cortou e o que o
formulário não pede.*
