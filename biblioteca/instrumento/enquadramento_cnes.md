# enquadramento_cnes.md — o que o estabelecimento executor precisa ter no CNES

Nota de consulta, de 27/09/2026. O plano descreve o procedimento; o CNES diz se o
estabelecimento pode executá-lo e faturá-lo pelo SUS. Os cinco aprovados não tratam
disso (AC-077), e foi por aí que o MPCDF atacou os convênios do IEV (CT-002).

Fontes: ficha de cada procedimento no SIGTAP (DD-006,
`registros/fontes/sigtap_enquadramento_092026.csv`), CNES dos executores dos aprovados
(DD-005, `registros/fontes/cnes_executores_20260927.csv`), Portaria SAES/MS 1.640/2024,
arts. 6º e 7º (NM-017; OB-053, OB-054), e Portaria SAES/MS 3.200/2025, arts. 3º a 5º
(NM-026).

---

## 1. O que a ficha do procedimento exige

Cada procedimento do SIGTAP traz, além de valor, idade e sexo, os campos que o
estabelecimento precisa satisfazer. Os da ficha que importam para o enquadramento:

| campo da ficha | o que é | exemplo — ultrassonografia mamária, 02.05.02.009-7 | exemplo — OCI oftalmologia, 09.05.01.003-5 |
|---|---|---|---|
| Instrumento de registro | por onde a produção vai ao SIA | BPA individualizado, APAC principal ou secundária, AIH especial | só APAC principal, com os secundários na mesma APAC |
| Serviço / classificação | o serviço especializado que o CNES do estabelecimento precisa ter | 121/002 ultrassonografia (ou 121/008, por telemedicina) | não exige |
| CBO | a ocupação do profissional que executa, vinculado ao CNES | radiologista, ginecologista-obstetra, mastologista | médico oftalmologista |
| Habilitações | a marcação do estabelecimento num programa | 38.01, 38.05, 38.06 | 38.01 a 38.06 |
| Incremento | o acréscimo sobre o valor de tabela que a habilitação dá | +313% com 38.01, 38.05 ou 38.06; +190% com 38.04 | não há |

**No exame, o incremento é da habilitação, não da tabela.** O ultrassom de tabela
R$ 24,20 vale R$ 99,94 com o incremento de 313%; a tomografia de R$ 138,63 vale
R$ 299,44 com 116%. O valor unitário do plano de ultrassom e tomografia (redacao_04) é
esse valor com incremento, e ele supõe a habilitação.

**Na OCI não há incremento.** O valor da tabela já é o do pacote (R$ 160,00 na OCI de
oftalmologia), e a ficha pede o CBO do médico da especialidade.

## 2. As habilitações do programa

| código | nome | como se obtém |
|---|---|---|
| 38.01 | Programa Mais Acesso a Especialistas | **inserção descentralizada**: o gestor local (a SES-DF) marca no CNES depois de publicar ato normativo, para o estabelecimento do Plano de Ação Regional. Quem tem 38.01 precisa ter também o serviço **170/002 — Núcleo de Gestão do Cuidado**, de preferência com enfermeiro e técnico de enfermagem (Portaria 1.640/2024, arts. 6º e 7º) |
| 38.02 | Agora Tem Especialistas — Modalidade 1 | componente de cirurgias (Portaria 3.200/2025) |
| 38.03 | Agora Tem Especialistas — Modalidade 2, Equipes Volantes | exige a equipe 81 EqAE registrada no CNES |
| 38.04 | Agora Tem Especialistas — Modalidade 3, Unidades Móveis | estabelecimento classificado como ambulatório de estrutura móvel, com gestão federal no CNES |
| 38.05 | Agora Tem Especialistas — Componente Créditos Financeiros | componente dos hospitais privados (ver NM-015) |
| 38.06 | Agora Tem Especialistas — Componente Ressarcimento ao SUS | idem |

A pergunta que fica para a SES-DF, e que decide o valor do exame no plano: **no
convênio de emenda, o incremento depende de o executor ter a 38.01 marcada, ou é só
referência de preço?** Enquanto não houver resposta escrita, o plano que usa o valor
com incremento diz de onde ele vem (LI-040).

## 3. O que o CNES dos executores dos aprovados mostra

Consulta pública do CNES em 27/09/2026:

| estabelecimento | tipo | atende SUS | serviços | habilitação | profissionais |
|---|---|---|---|---|---|
| ISHP — CNES 8078858 | Policlínica | sim | 131 oftalmologia (SUS), 142 endoscopia (não SUS), 170 | nenhuma | 43, dos quais 5 oftalmologistas e 16 assistentes administrativos |
| IEV — CNES 5830427 | **Consultório isolado** | **não** | nenhum | nenhuma | 2 — um diretor e um médico clínico |
| Centro Clínico e Ecográfico, Sobradinho — 3031543 | Policlínica | sim | 121 imagem (SUS) | nenhuma | 17, com 2 radiologistas |
| CIG Centro de Imagens, Gama — 9180168 | Clínica/Centro de Especialidade | sim | 121 imagem (SUS) | nenhuma | 39, com 4 radiologistas e 11 técnicos e tecnólogos |

O IEV não tem, no próprio CNES, nada do que os três convênios executam: a execução
está nas clínicas, cada uma com CNES e CNPJ próprios. É o que a COASIS registrou em
março de 2026 e o MPCDF chamou de quarteirização.

## 4. O que conferir antes de escrever o plano

Para **cada** estabelecimento onde o procedimento será executado, na consulta pública
do CNES (`cnes.datasus.gov.br`, busca pelo número ou pelo CNPJ):

1. **Tipo de estabelecimento** compatível com o objeto — e, se a entidade proponente
   não for o estabelecimento executor, o vínculo formal entre os dois (LI-024, LI-025).
2. **Serviço e classificação** que a ficha pede, com a marca de atendimento **SUS**.
3. **Profissionais** com o CBO da ficha, vinculados àquele CNES, em número compatível
   com a capacidade da subseção 6.3 do plano.
4. **Equipamentos** que o procedimento usa (ultrassom, tomógrafo, endoscópio).
5. **Habilitação** 38.01 — se o valor do plano usar o incremento, ou se a SES-DF a
   exigir para a execução (OB-053) —, e o **Núcleo de Gestão do Cuidado** 170/002 que
   vem com ela (OB-054).

O que o CNES não tiver na data do plano entra como etapa de implantação, no mês 1,
com responsável — e não como afirmação de algo que ainda não existe.
