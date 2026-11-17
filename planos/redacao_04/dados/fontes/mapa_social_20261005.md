# Mapa Social da Saúde — recoleta de 05/10/2026

Coleta feita pelo Claude no navegador embutido, arquivada em
`mapa_social_20261005.xlsx`. Mesma origem e mesma via das coletas de 15/09/2026
(`mapa_social_tomografia.md` e `validacao_ultrassom.md`): Mapa Social da Saúde
(MPDFT), dados do SISREG/DATASUS, camada de dados do painel pela Qlik Engine API.

| campo | conteúdo |
|---|---|
| Última recarga da base | 05/10/2026 13:32:34 |
| Consulta | 05/10/2026 14:48 |
| Recorte | todos os anos; cada procedimento fixo na expressão de conjunto, sem depender da tela |
| Medida | **fila** = `Solicitações` do cabeçalho, os três status de fila — **também na Região de Saúde** |

**As abas 1 a 4 não têm número calculado.** A aba 5, o rateio, é calculada e diz isso
no título.

**As quantidades do objeto continuam sendo as da planilha de 10/09/2026.** O painel
entra para código, espera e rateio, como antes.

---

## 1. Os códigos não mudaram

Os dezesseis nomes internos — quinze do objeto e partes moles — carregam o mesmo
`codigo_sigtap_solicitacao` de 15/09. Nenhuma correspondência da
`conferencia_procedimentos.md` se altera.

**Armadilha de grafia nova:** o "espaço duplo" da angiotomografia de coronárias é um
espaço não separável (U+00A0) seguido de espaço comum. Busca com dois espaços comuns
volta zero.

## 2. A fila e a espera, procedimento a procedimento

| procedimento | fila 15/09 | fila 05/10 | espera 15/09 | espera 05/10 |
|---|---|---|---|---|
| Ecografia de abdômen superior adulto | 2.276 | 2.274 | 684 | **690** |
| Ecografia do aparelho urinário | 3.914 | 3.884 | 631 | **638** |
| Ecografia transvaginal | 10.383 | 9.950 | 593 | **626** |
| Ecografia de mama bilateral | 14.396 | 13.732 | 624 | **621** |
| Doppler venoso de membros inferiores | 9.824 | 9.899 | 610 | **621** |
| Ultrassonografia de parede abdominal | 3.143 | 3.189 | 585 | **593** |
| Ecografia de próstata por via abdominal | 3.243 | 3.325 | 578 | **581** |
| Ecografia de abdômen total adulto | 9.912 | 10.130 | 532 | **532** |
| Ecografia de tireoide adulto | 3.216 | 3.152 | 487 | **479** |
| Ecodoppler de carótidas | 4.537 | 4.533 | 140 | **142** |
| **conjunto da ultrassonografia** | 64.844 | **64.068** | 561 | **567** |
| TC abdômen superior c/contraste | 4.467 | 4.088 | 129,5 | 125,9 |
| TC pelve ou bacia c/contraste | 3.836 | 3.631 | 129,9 | 126,3 |
| TC tórax c/contraste | 2.987 | 2.447 | 126,4 | 127,0 |
| Angiotomografia de coronárias | 1.409 | 1.459 | 272,9 | 277,8 |
| TC tórax s/contraste | 426 | **20** | 19,1 | 254,2 |
| **conjunto da tomografia** | 13.125 | **11.645** | 141 | **146** |
| *partes moles — fora do objeto* | *2.992* | *3.099* | *663* | *660* |

O 561 e o 141 de 15/09 eram reconstituídos por ponderação; **o 567 e o 146 saem
direto do motor**, com a média recalculada sobre os registros.

**A ordem da tabela da 3.1 muda:** a transvaginal sobe do quinto para o terceiro lugar.

**A TC de tórax sem contraste esvaziou na fila** — de 426 para 20 solicitações, com
2.171 devolvidas. A espera de 254 dias é a média de vinte registros e não diz nada
sobre o procedimento.

**Na tomografia, 11.645 solicitações são de 6.229 pessoas.** Na ultrassonografia a
proporção é quase uma por pessoa (64.068 para 55.546). A tomografia de abdômen
superior e a de pelve chegam juntas para o mesmo usuário.

## 3. Região de Saúde, agora na medida da fila

A coleta de 15/09 rateou a tomografia pela medida dos gráficos, que inclui as
devolvidas. Esta trouxe a Região de Saúde dos cinco procedimentos **nas duas medidas**,
e a diferença é grande:

| procedimento de TC | Ceilândia | Sobradinho | Gama |
|---|---|---|---|
| abdômen superior — fila | 55,0% | 29,0% | 16,0% |
| abdômen superior — com devolvidas | 42,3% | 36,6% | 21,2% |
| tórax c/contraste — fila | 64,8% | 26,0% | 9,2% |
| tórax c/contraste — com devolvidas | 52,4% | 34,0% | 13,6% |
| **as cinco, ponderadas — fila** | **56,4%** | **28,8%** | **14,9%** |
| as cinco, ponderadas — com devolvidas | 43,8% | 35,9% | 20,3% |

**As devolvidas se concentram fora de Ceilândia.** Tirá-las do rateio desloca cerca de
1.700 exames de tomografia para Ceilândia.

Na fila, **URD e Contratado/Credenciado respondem por 52% da tomografia do objeto**
(6.038 de 11.645). Na ultrassonografia, 1,6% (1.056 de 64.068).

## 4. O rateio do objeto — calculado

| polo | Regiões | tudo na fila, 05/10 | exames | plano v18 | exames |
|---|---|---|---|---|---|
| Ceilândia | Oeste e Sudoeste | **43,05%** | **33.828** | 39,69% | 31.183 |
| Sobradinho | Norte, Leste e Central | **27,92%** | **21.941** | 29,94% | 23.527 |
| Gama | Sul e Centro-Sul | **29,02%** | **22.803** | 30,37% | 23.862 |
| **total** | | 100% | **78.572** | 100% | 78.572 |

O método é o da seção 3.4, e reproduz exatamente os 39,69% / 29,94% / 30,37% quando
alimentado com os dados de 15/09. Com os dados de hoje e a medida antiga na
tomografia, daria 40,91% / 29,15% / 29,94% — **a maior parte do deslocamento vem da
medida, não da data.**

A TC de tórax sem contraste entra no rateio com a distribuição de dezoito solicitações
com região nomeada, aplicada às 726 da planilha.

## 5. Perfil etário e risco

| recorte | ultrassonografia | tomografia |
|---|---|---|
| 40 a 69 anos | 42.966 — **67,1%** | 7.690 — 66,0% |
| pico decenal | 50 a 59 — 25,3% | 60 a 69 — 26,8% |
| Prioridade 1 | 2,1% | 59,4% |
| Prioridade 2 | 44,0% | 39,4% |
| Prioridade 3 | 36,0% | 1,0% |
| Prioridade 4 | 17,9% | 0,2% |

"Cerca de dois terços" continua valendo. A classificação de risco segue fora do
documento, pelo motivo registrado em `validacao_ultrassom.md`.

---

## 6. Fila e pessoas, em número absoluto

Consulta de 05/10/2026 14:58, mesma recarga da base. Medida da fila nas três colunas
do painel; a planilha é a extração da SES-DF de 10/09.

| fila | planilha 10/09 | fila 15/09 | fila 05/10 | pessoas 15/09 | pessoas 05/10 |
|---|---|---|---|---|---|
| Mama bilateral | 14.608 | 14.396 | 13.732 | 14.370 | 13.709 |
| Transvaginal | 10.481 | 10.383 | 9.950 | 10.382 | 9.949 |
| Abdômen total | 9.959 | 9.912 | 10.130 | 9.908 | 10.125 |
| Doppler MMII | 9.793 | 9.824 | 9.899 | 9.822 | 9.897 |
| Carótidas | 4.608 | 4.537 | 4.533 | 4.537 | 4.533 |
| Aparelho urinário | 3.921 | 3.914 | 3.884 | 3.914 | 3.883 |
| Tireoide | 3.195 | 3.216 | 3.152 | 3.216 | 3.152 |
| Próstata | 3.185 | 3.243 | 3.325 | 3.237 | 3.319 |
| Parede abdominal | 3.121 | 3.143 | 3.189 | 3.143 | 3.189 |
| Abdômen superior | 2.249 | 2.276 | 2.274 | 2.274 | 2.272 |
| TC abdômen sup. c/contraste | 4.453 | 4.467 | 4.088 | 4.465 | 4.085 |
| TC pelve c/contraste | 3.808 | 3.836 | 3.631 | 3.835 | 3.629 |
| TC tórax c/contraste | 3.068 | 2.987 | 2.447 | 2.984 | 2.444 |
| Angiotomografia de coronárias | 1.397 | 1.409 | 1.459 | 1.409 | 1.459 |
| TC tórax s/contraste | 726 | 426 | 20 | 426 | 20 |
| **objeto** | **78.572** | **77.969** | **75.713** | | **61.012** |

**Dentro de cada fila, solicitação e pessoa quase coincidem.** A diferença está entre
as filas: as 75.713 solicitações do objeto são de **61.012 pessoas**.

| conjunto | solicitações | pessoas | com 1 exame | com 2 | com 3 | 4 ou mais |
|---|---|---|---|---|---|---|
| ultrassonografia | 64.068 | 55.546 | 48.236 | 6.259 | 903 | 148 |
| tomografia | 11.645 | **6.229** | 2.372 | 2.308 | 1.539 | 10 |
| objeto inteiro | 75.713 | 61.012 | 49.611 | 8.468 | 2.609 | 324 |

**Na tomografia, 3.481 pessoas esperam ao mesmo tempo a TC de abdômen superior e a
de pelve** — 85% de quem está na fila de abdômen superior. É o abdome total pedido em
duas linhas.

## 7. Entrantes — 2026 mês a mês e 2025 inteiro

### O recorte pedido não mede entrada

O `Total de Solicitações` com `Ano_Solicitacao = 2026` conta só o que **ainda está na
tabela de solicitações** — pendentes e devolvidas. A solicitação agendada sai dessa
tabela e passa para a de agendamentos. Por isso o número **cai** entre 15/09 e 05/10,
com três semanas de entrada a mais no meio:

| TC | Total Ano=2026, 15/09 | Total Ano=2026, 05/10 |
|---|---|---|
| abdômen superior c/contraste | 4.447 | 4.321 |
| pelve c/contraste | 3.723 | 3.739 |
| tórax c/contraste | 2.873 | 2.477 |
| angiotomografia de coronárias | 723 | 783 |
| tórax s/contraste | 522 | 110 |

É estoque, não fluxo.

### Entrantes = abertas + agendadas, pela data da solicitação

A tabela de agendamentos guarda a data do agendamento e o tempo de espera; a diferença
é a data da solicitação, e confere com a `Calendar.Data_Solicitacao` do próprio modelo.
As duas tabelas não se sobrepõem (60.881 chaves contra 60.882 linhas, na mama). **A
base traz solicitações até 30/09/2026**, com o último dia aparentemente incompleto.

| fila | entrantes 2026 (jan–set) | por mês | entrantes 2025 | por mês |
|---|---|---|---|---|
| Mama bilateral | 8.737 | 971 | 9.819 | 818 |
| Transvaginal | 11.999 | 1.333 | 13.828 | 1.152 |
| Abdômen total | 8.187 | 910 | 9.740 | 812 |
| Doppler MMII | 4.005 | 445 | 5.389 | 449 |
| Carótidas | 7.047 | 783 | 8.387 | 699 |
| Aparelho urinário | 3.773 | 419 | 4.783 | 399 |
| Tireoide | 3.175 | 353 | 3.978 | 332 |
| Próstata | 3.380 | 376 | 4.480 | 373 |
| Parede abdominal | 1.754 | 195 | 2.265 | 189 |
| Abdômen superior | 2.042 | 227 | 2.552 | 213 |
| **ultrassonografia** | **54.099** | **6.011** | **65.221** | **5.435** |
| TC abdômen sup. c/contraste | 6.287 | 699 | 8.720 | 727 |
| TC pelve c/contraste | 5.314 | 590 | 7.609 | 634 |
| TC tórax c/contraste | 4.421 | 491 | 5.788 | 482 |
| Angiotomografia de coronárias | 820 | 91 | 852 | 71 |
| TC tórax s/contraste | 12.925 | 1.436 | 16.388 | 1.366 |
| **tomografia** | **29.767** | **3.307** | **39.357** | **3.280** |
| **objeto** | **83.866** | **9.318** | **104.578** | **8.715** |

Mês a mês, o objeto oscila entre 8.414 e 10.530 entrantes em 2026, sem tendência; em
2025, entre 7.250 (dezembro) e 9.419.

**A TC de tórax sem contraste é o caso extremo:** cerca de 1.400 entrantes por mês e
vinte na fila. A rede já absorve esse fluxo — 7.961 das solicitações de 2026 já foram
realizadas.

**É piso.** Solicitação cancelada antes de ser agendada não aparece em nenhuma das
duas tabelas.
