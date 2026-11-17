# Conferência procedimento a procedimento — correspondência de nomes

Fechada em 15/09/2026 com as duas coletas do Mapa Social da Saúde. Substitui a versão
de 15/09 que trabalhava só contra o Anexo I da portaria.

**As quantidades são todas da planilha `filas_ultrassom_tomografia_20260915.xlsx`**, a
primeira que o usuário enviou, extraída em 10/09/2026. O painel entra para código,
espera e rateio — nunca para quantidade.

**Revisto em 22/09/2026 (D-007):** a ecografia de partes moles sai do objeto — será
contemplada em outra OCI. A linha continua na tabela abaixo, riscada, porque a
correspondência de nomes é da fila e não do objeto; fica fora de todos os totais.

## As três camadas de nome

Cada exame tem três nomes, e eles não coincidem:

1. **O nome na planilha do objeto** — como o usuário o escreveu.
2. **O nome interno no SISREG** — `descrição_procedimento_solicitacao`, que é o que a
   unidade solicitante escolhe na tela.
3. **O nome na Tabela do SUS** — o que vai à APAC e ao Anexo I da portaria.

## A tabela de correspondência

| nome na planilha | exames | nome interno no SISREG | nome na Tabela do SUS | código | diferença |
|---|---|---|---|---|---|
| Ecografia de mama bilateral | 14.608 | ECOGRAFIA DE MAMAS - BILATERAL | ULTRASSONOGRAFIA MAMÁRIA BILATERAL | 02.05.02.009-7 | grafia |
| Ecografia transvaginal | 10.481 | ECOGRAFIA TRANSVAGINAL | ULTRASSONOGRAFIA TRANSVAGINAL | 02.05.02.018-6 | grafia |
| Ecografia abdômen total adulto | 9.959 | ECOGRAFIA DE ABDOMEN TOTAL ADULTO | ULTRASSONOGRAFIA DE ABDOMEN TOTAL | 02.05.02.004-6 | grafia · "adulto" não existe na tabela |
| **US doppler venoso MMII (bilateral)** | 9.793 | ULTRA-SONOGRAFIA DOPPLER VENOSO - MMII ( BILATERAL) | ULTRASSONOGRAFIA DOPPLER COLORIDO DE VASOS | 02.05.01.004-0 | **nome diferente** — a tabela não nomeia território |
| **Ecodoppler de carótidas** | 4.608 | 10. ECODOPPLER DE CAROTIDAS | ULTRASSONOGRAFIA DOPPLER COLORIDO DE VASOS | 02.05.01.004-0 | **nome diferente** — mesmo código do anterior |
| Ecografia do aparelho urinário | 3.921 | ECOGRAFIA DO APARELHO URINARIO (RINS, BEXIGA) ADULTO | ULTRASSONOGRAFIA DE APARELHO URINÁRIO | 02.05.02.005-4 | grafia · a tabela não lista os órgãos |
| Ecografia de tireoide adulto | 3.195 | ECOGRAFIA DE TIREOIDE ADULTO | ULTRASSONOGRAFIA DE TIREOIDE | 02.05.02.012-7 | grafia · "adulto" |
| Ecografia de próstata (via abdominal) | 3.185 | ECOGRAFIA DE PROSTATA ( VIA ABDOMINAL ) | ULTRASSONOGRAFIA DE PRÓSTATA POR VIA ABDOMINAL | 02.05.02.010-0 | grafia |
| **Ultrassonografia de parede abdominal** | 3.121 | ULTRASONOGRAFIA DE PAREDE ABDOMINAL | ULTRASSONOGRAFIA DE ABDOMEN TOTAL | 02.05.02.004-6 | **nome diferente** — não existe na tabela |
| ~~Ecografia de partes moles~~ | ~~2.974~~ | ECOGRAFIA␣␣DE PARTES MOLES | ULTRASSONOGRAFIA DE ARTICULAÇÃO | 02.05.02.006-2 | **fora do objeto desde 22/09/2026** — outra OCI |
| Ecografia de abdômen superior adulto | 2.249 | ECOGRAFIA DE ABDOMEN SUPERIOR ADULTO | ULTRASSONOGRAFIA DE ABDOMEN SUPERIOR | 02.05.02.003-8 | grafia · "adulto" |
| Abdômen superior adulto c/contraste s/sedação | 4.453 | 063. TC DO ABDOMEN SUPERIOR ADULTO C/CONTRASTE S/SEDACAO | TOMOGRAFIA COMPUTADORIZADA DE ABDOMEN SUPERIOR | 02.06.03.001-0 | a tabela não distingue contraste nem sedação |
| Tomografia de pelve ou bacia c/contraste s/sedação | 3.808 | 111. TC DE PELVE OU BACIA ADULTO C/CONTRASTE S/SEDACAO | TC DE PELVE / BACIA / ABDOMEN INFERIOR | 02.06.03.003-7 | a tabela acrescenta "abdômen inferior" |
| Tomografia do tórax c/contraste s/sedação | 3.068 | 055. TC DO TORAX ADULTO C/CONTRASTE S/SEDACAO | TOMOGRAFIA COMPUTADORIZADA DE TÓRAX | 02.06.02.003-1 | a tabela não distingue contraste |
| **Angiotomografia das artérias coronárias** | 1.397 | ANGIOTOMOGRAFIA␣␣DAS ARTÉRIAS CORONARIAS ADULTO S/SEDACAO | TOMOGRAFIA COMPUTADORIZADA DE TÓRAX | 02.06.02.003-1 | **nome diferente** — não existe na tabela |
| Tomografia do tórax s/contraste s/sedação | 726 | 053. TC DO TORAX␣␣ADULTO S/CONTRASTE S/SEDACAO | TOMOGRAFIA COMPUTADORIZADA DE TÓRAX | 02.06.02.003-1 | mesmo código da linha com contraste |
| | **78.572** | | | | objeto: 15 nomes de fila, 11 códigos |

## Quatro nomes do objeto não existem na Tabela do SUS

São **18.919 exames, 24,1% do objeto** — eram cinco e 21.893 antes de partes moles sair:

| nome da fila | exames | vira |
|---|---|---|
| Doppler venoso de MMII bilateral | 9.793 | ultrassonografia doppler colorido de vasos |
| Ecodoppler de carótidas | 4.608 | ultrassonografia doppler colorido de vasos |
| Parede abdominal | 3.121 | ultrassonografia de abdômen total |
| Angiotomografia de coronárias | 1.397 | tomografia computadorizada de tórax |

**Nenhum deles é encaixe deste plano.** Todos os quatro carregam esse código no campo
`codigo_sigtap_solicitacao` do próprio painel de regulação: é assim que a SES-DF já
fatura hoje.

## Três códigos reúnem mais de um nome

| código | nomes reunidos | exames |
|---|---|---|
| 02.05.01.004-0 | doppler venoso de MMII + ecodoppler de carótidas | 14.401 |
| 02.05.02.004-6 | abdômen total + parede abdominal | 13.080 |
| 02.06.02.003-1 | tórax com contraste + tórax sem contraste + angiotomografia de coronárias | 5.191 |

**A planilha do plano se organiza por código**, porque é o código que vai ao SIA — e
quinze linhas de fila viram onze linhas de planilha.

## Duas armadilhas de grafia

A coleta registrou duas que quebram busca por texto:

- **`ECOGRAFIA␣␣DE PARTES MOLES`** tem espaço duplo no nome interno.
- **Parede abdominal aparece com dois nomes** — `ULTRASONOGRAFIA DE PAREDE ABDOMINAL`
  (3.142 solicitações no painel) e `ULTRA-SONOGRAFIA DE PAREDE ABDOMINAL` (1). Os dois
  carregam o mesmo código.

## O que "adulto", "com contraste" e "sem sedação" fazem no nome da fila

São qualificadores da tela do SISREG, não da Tabela do SUS. A tabela tem um código de
tomografia de tórax, e a fila tem três nomes para ele. Isso não é defeito de nenhum
dos dois: o nome interno orienta quem solicita, o código orienta quem fatura.
