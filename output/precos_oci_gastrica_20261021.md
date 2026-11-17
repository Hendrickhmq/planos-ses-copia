# Preços — OCI Avaliação Diagnóstica de Câncer Gástrico (09.01.01.007-3)

**Controle interno: não vai ao documento.**

Plano: planos/redacao_03/ (plano assinado pelo ISHP em 01/10/2026, `dados/ishp_plano_assinado_20261001.pdf`) · Pesquisado em 21/10/2026 · Origem do recurso: federal (emenda individual da Dep. Bia Kicis, R$ 2.500.000,00, e demais recursos consignados pela SES-DF, plano assinado, seção 1.2)
Oferta inicial: a definir · Teto: a definir (decisão do usuário; a conta do teto técnico está em `estudos/precificacao_oci_20261021.md`)

*Primeira pesquisa deste arquivo. O comparativo antigo de `valor_unitario.md` (a hipótese do
incremento de 627%) não tinha preço de mercado; lá fica só o valor e a portaria.*

## 1. Valor que a unidade recebe

| código | nome | valor | fonte |
|---|---|---|---|
| 09.01.01.007-3 | OCI Avaliação Diagnóstica de Câncer Gástrico | R$ 600,11 | SIGTAP 10/2026, arquivo oficial do DATASUS (`dados/fontes/sigtap_ftp_202610.md`); o mesmo valor da ficha de 08/2026, `dados/fontes/sigtap_0901010073_082026.md` (Portaria SAES/MS 4.653/2026) |

A composição: esofagogastroduodenoscopia (02.09.01.003-7, obrigatória, 1), sedação
(04.17.01.006-0, 1), anatomopatológico (02.03.02.003-0, 1), consulta (03.01.01.007-2, até 2) e
teleconsulta (03.01.01.030-7, até 2). Avulsos na tabela: R$ 48,16, R$ 15,15, R$ 40,78, R$ 10,00
e R$ 10,00.

O plano paga a OCI concluída, com todos os componentes aplicáveis e o desfecho registrado (seção
7.2). A gestão, a recepção e a prestação de contas estão fora do unitário, nas Metas 01 e 03
(R$ 596.696,76, seção 19.2): **o R$ 600,11 inteiro é do custo de executar.**

## 2. O que a SES-DF paga

| código | fonte | valor | o que é |
|---|---|---|---|
| 09.01.01.007-3 | este convênio: plano assinado do ISHP, item 2.1.1 da planilha (`dados/ishp_plano_assinado_20261001.pdf`, p. 16) | R$ 600,11 | o valor da tabela, sem complemento, por 13.012 OCIs (LI-002) |
| 09.01.01.007-3, componente esofagogastroduodenoscopia (02.09.01.003-7) | Tabela Regionalizada SUS/DF, Anexo Único da Deliberação CG-SES 24/2024, republicado pela Deliberação CG-SES 16/2025, item IV (SADT), Endoscopia. SINJ: https://www.sinj.df.gov.br/sinj/Norma/482f67237e0a4bd1a7e9dd40dfe9b158/x.html | R$ 335,00 | valor regionalizado da EDA, sem a sedação. É a tabela da contratação complementar de terapia intensiva, não de ambulatório |
| 09.01.01.007-3, componentes esofagogastroduodenoscopia (02.09.01.003-7) e sedação (04.17.01.006-0) | Portaria SAES/MS 4.282/2026, Anexo I; Tabela de 10/2026 (`dados/fontes/sigtap_ftp_202610.md`) | R$ 350,12 e R$ 149,99 | **não é da SES-DF:** é o que o Ministério paga ao estabelecimento habilitado no Agora Tem Especialistas (38.05, créditos financeiros; 38.01, PMAE), avulsos, com incremento de 627% e 890%. Somam R$ 500,11; com R$ 100,00 a mais dão os R$ 600,11 da OCI |

O anatomopatológico 02.03.02.003-0 não está na Tabela Regionalizada (só os de colo uterino e de
mama). A consulta da Tabela de Complementariedade de Cirurgias Eletivas é o valor SIGTAP (R$ 10,00,
`planos/redacao_05/dados/precos.md`, seção 2). Nenhum convênio do acervo (`estudo/normalizados/pt_ses_01`
a `pt_ses_05`, `registros/acervo.csv`) traz OCI de câncer gástrico ou endoscopia.

## 3. Mercado privado

Os preços do DF são a base da conta; os de fora do DF ampliam a base. Todos foram lidos em
21/10/2026, no Doctoralia (`curl` das listagens, até a página 4) e no site do dr.consulta.

**Como se contou.** Um preço por endereço e componente, o menor; consulta e primeira consulta
contam como a mesma consulta. A fonte é o endereço do anúncio, sem o nome do profissional. Saiu o
preço de R$ 1,00 (erro de cadastro, Belo Horizonte).

**O que o mercado não publica.** No DF, só 2 dos 58 anúncios de endoscopia digestiva alta trazem
preço; nenhum separa a sedação ou o anestesiologista. O Medprev não oferece endoscopia no DF. Nenhum
laboratório do DF publica o anatomopatológico de biópsia gástrica. A teleconsulta e o retorno de
gastroenterologia não aparecem com preço. O aluguel de equipamento de videoendoscopia e a pinça de
biópsia não têm preço publicado no Brasil (busca de 21/10/2026).

No DF: 35 preços de consulta e 2 de endoscopia. Fora do DF: 8 de endoscopia (São Paulo/SP: 4; Belo
Horizonte/MG: 3; Goiânia/GO: 1) e 1 de anatomopatológico (São Paulo/SP).

| código | componente | fonte | endereço | data | local | preço | tipo | inclui |
|---|---|---|---|---|---|---|---|---|
| 09.01.01.007-3 | anatomopatológico de biópsia | dr.consulta, rede (unidade não informada) | https://drconsulta.com/servicos/exames/anatomo-patologico-proveniente-de-biopsias-e-exereses-segunda-amostra | 21/10/2026 | fora do DF: São Paulo/SP | R$ 91,00 | fixo | por amostra (a segunda amostra); R$ 130,00 sem o cartão da rede; a primeira amostra não tem preço publicado |
| 09.01.01.007-3 | consulta gastroenterologia | Doctoralia, SGAS 914 914 | https://www.doctoralia.com.br/servicos-de-tratamento/consulta-gastroenterologia/brasilia?page=2 | 21/10/2026 | Brasília | R$ 100,00 | fixo |  |
| 09.01.01.007-3 | consulta gastroenterologia | Doctoralia, SGAS Quadra 610 610 | https://www.doctoralia.com.br/servicos-de-tratamento/consulta-gastroenterologia/brasilia | 21/10/2026 | Brasília | R$ 125,00 | fixo |  |
| 09.01.01.007-3 | consulta gastroenterologia | Doctoralia, Avenida Brasília Qs 11 Conjunto G 11 | https://www.doctoralia.com.br/servicos-de-tratamento/consulta-gastroenterologia/brasilia | 21/10/2026 | Brasília | R$ 199,00 | fixo |  |
| 09.01.01.007-3 | consulta gastroenterologia | Doctoralia, Setor Comercial Sul, Quadra 8 - Bloco 60 - Piso P2 - Salas 24/25/26 | https://www.doctoralia.com.br/servicos-de-tratamento/consulta-gastroenterologia/brasilia?page=2 | 21/10/2026 | Brasília | R$ 300,00 | fixo |  |
| 09.01.01.007-3 | consulta gastroenterologia | Doctoralia, Rua 5 Norte Lt 03 LJ 02/03/04/05 Piso 1 Ed. Albany Medical Center | https://www.doctoralia.com.br/servicos-de-tratamento/consulta-gastroenterologia/brasilia?page=2 | 21/10/2026 | Águas Claras | R$ 300,00 | a partir de |  |
| 09.01.01.007-3 | consulta gastroenterologia | Doctoralia, QI 31 Bloco A sala 208 - Guará II | https://www.doctoralia.com.br/servicos-de-tratamento/consulta-gastroenterologia/brasilia?page=3 | 21/10/2026 | Guará | R$ 300,00 | fixo |  |
| 09.01.01.007-3 | consulta gastroenterologia | Doctoralia, Área Especial Setor C Norte, torre B, sala 112/113, Ed. Prime excelência médica | https://www.doctoralia.com.br/servicos-de-tratamento/primeira-consulta-gastroenterologia/brasilia?page=3 | 21/10/2026 | DF (a listagem não traz o bairro) | R$ 300,00 | fixo | primeira consulta |
| 09.01.01.007-3 | consulta gastroenterologia | Doctoralia, SHLS Quadra 716 Conjunto B Bloco F Centro Clínico Oswaldo Cruz,sala 202 | https://www.doctoralia.com.br/servicos-de-tratamento/primeira-consulta-gastroenterologia/brasilia?page=3 | 21/10/2026 | Brasília | R$ 300,00 | a partir de | primeira consulta |
| 09.01.01.007-3 | consulta gastroenterologia | Doctoralia, QS 11 | https://www.doctoralia.com.br/servicos-de-tratamento/consulta-gastroenterologia/brasilia | 21/10/2026 | Brasília | R$ 350,00 | fixo |  |
| 09.01.01.007-3 | consulta gastroenterologia | Doctoralia, QNC A.E 8/9 Hospital Anchieta 1o. Andar sala 113-B | https://www.doctoralia.com.br/servicos-de-tratamento/consulta-gastroenterologia/brasilia | 21/10/2026 | Brasília | R$ 350,00 | fixo |  |
| 09.01.01.007-3 | consulta gastroenterologia | Doctoralia, Shis Qi 7 Conjunto F | https://www.doctoralia.com.br/servicos-de-tratamento/consulta-gastroenterologia/brasilia | 21/10/2026 | Lago Sul | R$ 350,00 | fixo |  |
| 09.01.01.007-3 | consulta gastroenterologia | Doctoralia, SGAN 607 | https://www.doctoralia.com.br/servicos-de-tratamento/consulta-gastroenterologia/brasilia | 21/10/2026 | Brasília | R$ 350,00 | fixo |  |
| 09.01.01.007-3 | consulta gastroenterologia | Doctoralia, CENTRO MEDICO LUCIO COSTA , 610/611 SUL, BLOCO II SALA T 33 | https://www.doctoralia.com.br/servicos-de-tratamento/consulta-gastroenterologia/brasilia?page=2 | 21/10/2026 | Brasília | R$ 350,00 | a partir de |  |
| 09.01.01.007-3 | consulta gastroenterologia | Doctoralia, Área Especial Setor C Norte | https://www.doctoralia.com.br/servicos-de-tratamento/primeira-consulta-gastroenterologia/brasilia | 21/10/2026 | Brasília | R$ 350,00 | fixo | primeira consulta |
| 09.01.01.007-3 | consulta gastroenterologia | Doctoralia, SMHN Quadra 02 Bloco B - Edifício Cléo Octávio - Salas 704/714 | https://www.doctoralia.com.br/servicos-de-tratamento/consulta-gastroenterologia/brasilia?page=2 | 21/10/2026 | Brasília | R$ 400,00 | fixo |  |
| 09.01.01.007-3 | consulta gastroenterologia | Doctoralia, 709/909 Sul Edifício Biocenter - Asa Sul | https://www.doctoralia.com.br/servicos-de-tratamento/primeira-consulta-gastroenterologia/brasilia | 21/10/2026 | Brasília | R$ 400,00 | fixo | primeira consulta |
| 09.01.01.007-3 | consulta gastroenterologia | Doctoralia, SEPS 715/915, Conjunto A, Bloco D, Edifício Pacini, Sala 304, Asa Sul | https://www.doctoralia.com.br/servicos-de-tratamento/primeira-consulta-gastroenterologia/brasilia | 21/10/2026 | Brasília | R$ 400,00 | fixo | primeira consulta |
| 09.01.01.007-3 | consulta gastroenterologia | Doctoralia, Centro de excelência do Hospital Anchieta, 8° andar torre B salas 802 a 809,814,815 | https://www.doctoralia.com.br/servicos-de-tratamento/primeira-consulta-gastroenterologia/brasilia | 21/10/2026 | Taguatinga | R$ 400,00 | fixo | primeira consulta |
| 09.01.01.007-3 | consulta gastroenterologia | Doctoralia, RUA 05 NORTE LOTE 03 EDIFICIO ALBANY MEDICAL CENTER SALA 309 | https://www.doctoralia.com.br/servicos-de-tratamento/primeira-consulta-gastroenterologia/brasilia?page=4 | 21/10/2026 | Águas Claras | R$ 400,00 | a partir de | primeira consulta |
| 09.01.01.007-3 | consulta gastroenterologia | Doctoralia, Hospital Anchieta, Área Especial Nº 8/10 Setor C Norte Taguatinga - Torre A 8º Andar (salas 802/811) - Centro de Excelência | https://www.doctoralia.com.br/servicos-de-tratamento/consulta-gastroenterologia/brasilia | 21/10/2026 | Taguatinga | R$ 450,00 | fixo |  |
| 09.01.01.007-3 | consulta gastroenterologia | Doctoralia, Bloco C Centro Clínico Linea Vita Loja 01 SGAS 616 SHCS | https://www.doctoralia.com.br/servicos-de-tratamento/consulta-gastroenterologia/brasilia?page=2 | 21/10/2026 | Brasília | R$ 450,00 | a partir de |  |
| 09.01.01.007-3 | consulta gastroenterologia | Doctoralia, SGAN 915 Golden Office Corporate, Sala 204, Bloco A | https://www.doctoralia.com.br/servicos-de-tratamento/consulta-gastroenterologia/brasilia | 21/10/2026 | DF (a listagem não traz o bairro) | R$ 500,00 | fixo |  |
| 09.01.01.007-3 | consulta gastroenterologia | Doctoralia, Shis Qi 15 15 | https://www.doctoralia.com.br/servicos-de-tratamento/consulta-gastroenterologia/brasilia | 21/10/2026 | Brasília | R$ 500,00 | a partir de |  |
| 09.01.01.007-3 | consulta gastroenterologia | Doctoralia, 710 sul Edificio Via Brasil Torres A Salas 413/415 | https://www.doctoralia.com.br/servicos-de-tratamento/consulta-gastroenterologia/brasilia | 21/10/2026 | Brasília | R$ 500,00 | a partir de |  |
| 09.01.01.007-3 | consulta gastroenterologia | Doctoralia, Shls 716 | https://www.doctoralia.com.br/servicos-de-tratamento/primeira-consulta-gastroenterologia/brasilia | 21/10/2026 | Brasília | R$ 500,00 | fixo | primeira consulta |
| 09.01.01.007-3 | consulta gastroenterologia | Doctoralia, Sala 10 | https://www.doctoralia.com.br/servicos-de-tratamento/primeira-consulta-gastroenterologia/brasilia | 21/10/2026 | Brasília | R$ 500,00 | fixo | primeira consulta |
| 09.01.01.007-3 | consulta gastroenterologia | Doctoralia, sgas 614 conjunto C sala 64 | https://www.doctoralia.com.br/servicos-de-tratamento/primeira-consulta-gastroenterologia/brasilia | 21/10/2026 | DF (a listagem não traz o bairro) | R$ 550,00 | fixo | primeira consulta |
| 09.01.01.007-3 | consulta gastroenterologia | Doctoralia, Setor C Norte Qnc 8 8 | https://www.doctoralia.com.br/servicos-de-tratamento/primeira-consulta-gastroenterologia/brasilia?page=3 | 21/10/2026 | Brasília | R$ 580,00 | fixo | primeira consulta |
| 09.01.01.007-3 | consulta gastroenterologia | Doctoralia, SGAS 915 915 | https://www.doctoralia.com.br/servicos-de-tratamento/primeira-consulta-gastroenterologia/brasilia | 21/10/2026 | Brasília | R$ 650,00 | fixo | primeira consulta |
| 09.01.01.007-3 | consulta gastroenterologia | Doctoralia, DF-004 | https://www.doctoralia.com.br/servicos-de-tratamento/primeira-consulta-gastroenterologia/brasilia?page=2 | 21/10/2026 | Brasília | R$ 650,00 | fixo | primeira consulta |
| 09.01.01.007-3 | consulta gastroenterologia | Doctoralia, St. de Clubes Esportivos Sul Trecho 2 Centro de Lazer Beira Lago, Conjunto 02 Lojas 01/02 | https://www.doctoralia.com.br/servicos-de-tratamento/consulta-gastroenterologia/brasilia | 21/10/2026 | Brasília | R$ 800,00 | fixo |  |
| 09.01.01.007-3 | consulta gastroenterologia | Doctoralia, SCN Quadra 2 - Shopping Liberty Mall - Torre B - Salas 1133/1134 - 11 andar Asa Norte | https://www.doctoralia.com.br/servicos-de-tratamento/consulta-gastroenterologia/brasilia | 21/10/2026 | Brasília | R$ 800,00 | fixo |  |
| 09.01.01.007-3 | consulta gastroenterologia | Doctoralia, Setor Sudoeste 105 | https://www.doctoralia.com.br/servicos-de-tratamento/consulta-gastroenterologia/brasilia?page=2 | 21/10/2026 | Brasília | R$ 800,00 | fixo |  |
| 09.01.01.007-3 | consulta gastroenterologia | Doctoralia, Quadra 02 Conjunto 02 02 | https://www.doctoralia.com.br/servicos-de-tratamento/primeira-consulta-gastroenterologia/brasilia | 21/10/2026 | Brasília | R$ 1.000,00 | fixo | primeira consulta |
| 09.01.01.007-3 | consulta gastroenterologia | Doctoralia, SRTVS 701 Ed. Assis Chateaubriant Sala 517 Bloco 1 | https://www.doctoralia.com.br/servicos-de-tratamento/primeira-consulta-gastroenterologia/brasilia?page=2 | 21/10/2026 | Brasília | R$ 1.000,00 | fixo | primeira consulta |
| 09.01.01.007-3 | esofagogastroduodenoscopia | Doctoralia, Bloco C Centro Clínico Linea Vita Loja 01 SGAS 616 SHCS | https://www.doctoralia.com.br/servicos-de-tratamento/endoscopia-digestiva-alta/brasilia | 21/10/2026 | Brasília | R$ 500,00 | a partir de |  |
| 09.01.01.007-3 | esofagogastroduodenoscopia | Doctoralia, Centro Clinico Sul Torre II 4º Andar Sala 424 | https://www.doctoralia.com.br/servicos-de-tratamento/endoscopia-digestiva-alta/brasilia | 21/10/2026 | Brasília | R$ 1.100,00 | a partir de |  |
| 09.01.01.007-3 | esofagogastroduodenoscopia | Doctoralia, Av.Nove de Julho, 4440 | https://www.doctoralia.com.br/servicos-de-tratamento/endoscopia-digestiva-alta/sao-paulo | 21/10/2026 | fora do DF: São Paulo/SP | R$ 240,00 | fixo |  |
| 09.01.01.007-3 | esofagogastroduodenoscopia | Doctoralia, Avenida T-9, 2392 | https://www.doctoralia.com.br/servicos-de-tratamento/endoscopia-digestiva-alta/goiania | 21/10/2026 | fora do DF: Goiânia/GO | R$ 360,00 | fixo |  |
| 09.01.01.007-3 | esofagogastroduodenoscopia | Doctoralia, Rua Doutor Alípio Goulart 25 | https://www.doctoralia.com.br/servicos-de-tratamento/endoscopia-digestiva-alta/belo-horizonte | 21/10/2026 | fora do DF: Belo Horizonte/MG | R$ 400,00 | fixo |  |
| 09.01.01.007-3 | esofagogastroduodenoscopia | Doctoralia, Rua Mato Grosso, 306 - Higienópolis | https://www.doctoralia.com.br/servicos-de-tratamento/endoscopia-digestiva-alta/sao-paulo | 21/10/2026 | fora do DF: São Paulo/SP | R$ 500,00 | a partir de |  |
| 09.01.01.007-3 | esofagogastroduodenoscopia | Doctoralia, Rua Coelho Lisboa, 442 (cj. 43) | https://www.doctoralia.com.br/servicos-de-tratamento/endoscopia-digestiva-alta/sao-paulo | 21/10/2026 | fora do DF: São Paulo/SP | R$ 540,00 | fixo |  |
| 09.01.01.007-3 | esofagogastroduodenoscopia | Doctoralia, Avenida Francisco Sales 1614 | https://www.doctoralia.com.br/servicos-de-tratamento/endoscopia-digestiva-alta/belo-horizonte | 21/10/2026 | fora do DF: Belo Horizonte/MG | R$ 750,00 | fixo |  |
| 09.01.01.007-3 | esofagogastroduodenoscopia | Doctoralia, Avenida Luiz Paulo Franco 500 | https://www.doctoralia.com.br/servicos-de-tratamento/endoscopia-digestiva-alta/belo-horizonte | 21/10/2026 | fora do DF: Belo Horizonte/MG | R$ 750,00 | fixo |  |
| 09.01.01.007-3 | esofagogastroduodenoscopia | Doctoralia, Rua Cincinato Braga, 37 - cj 12 | https://www.doctoralia.com.br/servicos-de-tratamento/endoscopia-digestiva-alta/sao-paulo | 21/10/2026 | fora do DF: São Paulo/SP | R$ 980,00 | a partir de |  |

## 4. Resumo do mercado

| código | componente | base | na conta | preços | mínimo | mediana | máximo |
|---|---|---|---|---|---|---|---|
| 09.01.01.007-3 | anatomopatológico de biópsia | fora do DF | sim | 1 | R$ 91,00 | R$ 91,00 | R$ 91,00 |
| 09.01.01.007-3 | consulta gastroenterologia | DF | sim | 35 | R$ 100,00 | R$ 400,00 | R$ 1.000,00 |
| 09.01.01.007-3 | esofagogastroduodenoscopia | DF | sim | 2 | R$ 500,00 | R$ 800,00 | R$ 1.100,00 |
| 09.01.01.007-3 | esofagogastroduodenoscopia | fora do DF | sim | 8 | R$ 240,00 | R$ 520,00 | R$ 980,00 |

A consulta entra uma vez, como manda o método; a OCI tem duas (a inicial e o retorno), e o retorno
pode ser teleconsulta. A sedação não tem linha própria: os poucos preços de endoscopia não dizem se
a incluem.

## 5. A conta

| código | base | valor recebido | mercado mínimo | mercado mediana | cobertura | oferta inicial | teto | margem no teto |
|---|---|---|---|---|---|---|---|---|
| 09.01.01.007-3 | DF e fora do DF | R$ 600,11 | R$ 691,00 | R$ 1.291,00 | 87% | a definir | a definir | a definir |

- **O mínimo** (R$ 691,00) é a consulta mais barata do DF (R$ 100,00, SGAS 914), a endoscopia mais
  barata do DF (R$ 500,00 "a partir de", SGAS 616) e o anatomopatológico por amostra de fora do DF
  (R$ 91,00). A OCI cobre 87% disso, sem contar o retorno e o anestesiologista.
- **O varejo não é a régua desta negociação.** A régua é o que o SUS já paga por cada peça (seção 2):
  R$ 335,00 a R$ 350,12 pelo exame e R$ 149,99 pela sedação. Uma clínica habilitada no programa
  federal receberia R$ 600,11 por esta mesma OCI, direto do Ministério.
- **O teto técnico** (o máximo sem tirar dinheiro da gestão, que o plano paga à parte) e a conta de
  quanto sobra para o exame estão no estudo e na planilha `estudos/teto_oci_20261021.xlsx`. A
  oferta inicial e o teto, em %, são decisão do usuário e entram aqui quando decididos.

## 6. Apoio

Não se aplica: o apoio está fechado no plano assinado (seção 19.1 e Metas 01 e 03). Este arquivo
trata só do custo de executar a OCI.

## 7. O que falta

- **Cotação direta das clínicas** dos dois polos (Taguatinga e CONIC), dizendo o que está incluído:
  a sedação e o anestesiologista, o anatomopatológico (por paciente ou por frasco), a pinça, o
  retorno, a teleconsulta. É da equipe: o agente não telefona.
- **O anatomopatológico no DF:** um preço de laboratório com serviço 120-001 no CNES, por paciente.
- **A ficha de 10/2026 pela tela do SIGTAP** (agente `ficha-sigtap`): o site não abriu a sessão
  em 21/10/2026; os valores vieram do arquivo oficial.
- **Os componentes de custo da execução própria** (equipamento, pinça, insumos), se o ISHP for montar
  a estrutura: hoje são hipóteses na aba C da planilha.
