# Estudo — filas de imagem pela Tabela SUS Candanga

**Controle interno, 01/11/2026.** Serve para escolher os exames de ultrassom e tomografia do
plano de R$ 11,5 mi (plano 4), agora com o preço da Candanga e não mais o da Portaria SAES/MS
4.282/2026. O plano 4 não foi alterado.

A planilha é `estudo_imagem_candanga_20261101.xlsx`, e o script que a gera é
`estudo_imagem_candanga_20261101.py`, os dois nesta pasta. **As filas de US de partes moles
estão em vermelho: são do IEV.**

**As fontes:**
- **Filas:** a coleta do agente `mapa-social` de 29/10/2026, em `registros/mapa_social/imagem/`.
  - A recarga foi em 29/10, às 18:32, e o pedido mais recente é de 27/10.
  - "Pendentes" já desconta os devolvidos.
  - "24 meses" conta os pedidos desde 27/10/2024 (a fila viva).
- **Preço:** o Anexo Único da Deliberação CG-SES 46/2026 (SEI 212117347), modalidade SIA.

## 1. O panorama de todas as filas de imagem

| modalidade | filas | pendentes | últimos 24 meses | valor Candanga dos 24 meses |
|---|---:|---:|---:|---:|
| Ultrassonografia e Doppler | 139 | 82.983 (82.981 distintos) | 57.887 | R$ 5,31 mi |
| Endoscopia | 10 | 54.227 | 42.341 | R$ 17,06 mi |
| Tomografia | 191 | 20.627 | 20.397 | R$ 6,20 mi |
| Oftalmologia | 10 | 16.551 | 15.513 | R$ 0,55 mi |
| Ecocardiografia | 10 | 14.656 | 14.650 | R$ 3,15 mi |
| Ressonância | 127 | 10.127 | 10.117 | R$ 4,77 mi |
| Mamografia | 2 | 6.569 | 6.518 | R$ 0,65 mi |
| Medicina nuclear e PET-CT | 25 | 6.041 | 6.041 | R$ 5,35 mi |
| Radiologia (raio-X) | 167 | 3.455 | 3.439 | R$ 0,10 mi |
| Densitometria | 1 | 2.172 | 2.171 | R$ 0,48 mi |
| Odontológica, colposcopia, cateterismo, intervencionista | 11 | 2.751 | 2.722 | R$ 0,12 mi |

- **O preço de cada código está na aba 1:** são todas as filas de imagem, código a código, com o valor da Candanga.
- **Quase tudo está no Anexo.** Ficam fora:
  - a OCT (02.11.06.028-3, 3.902 pendentes);
  - a radiografia periapical (02.04.01.018-7);
  - dois códigos de raio-X com cadastro quebrado;
  - a angiografia cerebral.
  
  Nesses, vale o SIGTAP da ficha, pela regra do projeto (README da tabela Candanga, item 3).
- **O "valor da fila" é só quantidade × preço.** Serve para comparar o tamanho das filas e não é meta.

## 2. Ultrassom e tomografia: o preço de cada exame

**A mudança que decide a escolha:** na Portaria, todo ultrassom valia cerca de R$ 100 e toda
tomografia cerca de R$ 300. Na Candanga, cada exame tem o seu preço.

| código | exame | Candanga | Portaria (plano 4) | diferença | 24 meses |
|---|---|---:|---:|---:|---:|
| 02.05.02.017-8 | US transfontanela | R$ 268,73 | — | | 242 |
| 02.05.02.015-1 | US obstétrica com Doppler | R$ 134,44 | — | | 138 |
| 02.05.02.004-6 | US abdômen total | **R$ 117,51** | R$ 100,18 | **+17,3%** | 9.861 |
| 02.05.01.004-0 | Doppler colorido de vasos | **R$ 115,61** | R$ 100,18 | **+15,4%** | 12.132 |
| 02.05.02.003-8 | US abdômen superior | R$ 101,27 | R$ 99,94 | +1,3% | 1.234 |
| 02.05.02.007-0 | US bolsa escrotal | R$ 100,00 | — | | 623 |
| 02.05.02.005-4 | US aparelho urinário | R$ 90,53 | R$ 99,94 | −9,4% | 2.655 |
| 02.05.02.018-6 | US transvaginal | R$ 83,77 | R$ 99,94 | −16,2% | 5.691 |
| 02.05.02.010-0 | US próstata abdominal | R$ 74,19 | R$ 99,94 | −25,8% | 2.201 |
| 02.05.02.006-2 | US articulação (inclui partes moles) | R$ 70,97 | — | | 10.365 |
| 02.05.02.009-7 | US mamária bilateral | R$ 70,97 | R$ 99,94 | **−29,0%** | 8.501 |
| 02.05.02.012-7 | US tireoide | R$ 64,07 | R$ 99,94 | **−35,9%** | 3.093 |
| 02.05.02.016-0 | US pélvica | R$ 43,41 | — | | 698 |
| 02.06.01.006-0 | TC sela túrcica (e órbitas) | R$ 371,02 | — | | 43 |
| 02.06.03.001-0 | TC abdômen superior | R$ 309,25 | R$ 299,44 | +3,3% | 6.146 |
| 02.06.02.003-1 | TC tórax (e angio de coronárias) | R$ 309,25 | R$ 300,10 | +3,0% | 5.955 |
| 02.06.03.003-7 | TC pelve/bacia | R$ 309,25 | R$ 299,44 | +3,3% | 4.983 |
| 02.06.01.005-2 | TC pescoço | R$ 309,25 | — | | 750 |
| 02.06.01.007-9 | TC crânio | R$ 251,29 | — | | 1.392 |
| 02.06.01.004-4 | TC face/seios/ATM | R$ 260,09 | — | | 261 |
| demais TC (coluna, articulações, segmentos) | | R$ 251,29 a R$ 309,25 | — | | 867 |

A lista completa, com cada nome de fila, está nas abas 2 e 3.

**Os mesmos 79.144 exames do plano 4, pela Candanga:** R$ 10.390.824,04, contra
R$ 10.636.542,52 pela Portaria. São **R$ 245.718,48 a menos (−2,31%)**. A conta está na aba 4.
- **Ganham:** abdômen total (+R$ 228 mil) e Doppler (+R$ 224 mil), além da tomografia (+R$ 130 mil).
- **Perdem:** mama (−R$ 426 mil), tireoide (−R$ 115 mil), transvaginal (−R$ 170 mil) e próstata (−R$ 83 mil).

Para chegar perto do mesmo valor de produção, há dois caminhos: fazer mais exames ou trocar
parte da mama e da tireoide por exames que pagam mais.

## 3. O que pesa na escolha

- **Os que pagam mais e têm fila grande** são abdômen total (9.861) e Doppler (12.132), a
  ~R$ 116, e a tomografia de abdômen, tórax e pelve (17.084), a R$ 309,25.
  - Os três já estão no plano 4.
  - Na Candanga, eles ganham peso na carteira.
- **Os que pagam pouco e têm fila grande** são mama (8.501) e articulação (10.365), os dois a R$ 70,97, e tireoide (3.093), a R$ 64,07.
  - Entram pela necessidade da fila, não pelo preço.
  - Na articulação, sem as partes moles do IEV (1.891), sobram 8.474.
- **Os que pagam mais e têm fila pequena** podem completar a carteira, mas não servem de base:
  - bolsa escrotal (623, R$ 100);
  - obstétrica com Doppler (138);
  - transfontanela (242, infantil);
  - TC de pescoço (750);
  - TC de sela/órbitas (43).
- **A TC de crânio (1.392) mistura filas:** emergência, angiotomografia e só ~400 eletivas.
- **O contraste não é pago à parte.** O 02.06.03.004-5 não está no Anexo, então a TC com
  contraste recebe só os R$ 309,25 e o contraste é custo dentro do exame. A maior parte da
  fila de TC eletiva é com contraste.
- **As quantidades mudaram desde a v26.** Por exemplo, a mama tinha 14.689 exames no plano e
  hoje tem 12.941 pendentes, dos quais 8.501 dos últimos 24 meses. A quantidade de cada exame
  escolhido se mede de novo na coleta do plano.

## 4. Enquadramento: está direto na Candanga?

Todos os códigos de US e TC das filas estão no Anexo (SIA). A questão é outra: **se o nome da
fila é o procedimento do código**. A aba 5 resume, e a aba 2 traz a classificação de cada fila.

| categoria | pendentes | 24 meses | o que fazer |
|---|---:|---:|---|
| **Direto** | 89.971 | 67.611 | nada: o preço é o da Candanga |
| **Agrupado pela SES no código** | 13.561 | 10.604 | o plano diz o enquadramento (fila → código) e aceita o preço do código |
| **Código a conferir** | 78 | 69 | conferir com a regulação e na ficha antes de entrar |

**Os agrupamentos que importam para a escolha:**

| fila | registrada como | efeito |
|---|---|---|
| parede abdominal (2.197) | abdômen total, R$ 117,51 | paga mais que um US de região isolada |
| angiotomografia de coronárias (1.530) | TC de tórax, R$ 309,25 | paga muito abaixo do custo de mercado da angio coronária |
| outras angiotomografias (2.494) | TC da região | contraste e técnica a mais, sem valor a mais |
| Doppler de tireoide (685) | US de tireoide, R$ 64,07 | é Doppler e paga como US simples |
| **partes moles (1.891, IEV)** e regiões sem código (inguinal, pescoço, axila, glútea) | US de articulação, R$ 70,97 | não há código próprio de partes moles no SIGTAP |
| segmentos (mão, pé, braço, perna, dedo, tendão) | US de articulação | idem |
| morfológica (132) | obstétrica, R$ 62,22 | exame mais longo, pago como simples |
| TC de órbitas, mastoides e ouvidos | sela túrcica / face | mesmo valor do código |

**As filas com código a conferir:**
- US pélvica (47) e Doppler cervical, de aorta e ilíaca, no código de articulação;
- parótidas, no de Doppler;
- TC sacro-ilíaca, no de articulações de membro superior.

**Doppler bilateral:** o Doppler venoso de MMII bilateral e o de carótidas e vertebrais são
uma unidade do 02.05.01.004-0. A descrição da ficha SIGTAP de 10/2026 diz que a quantidade
independe dos vasos estudados. O plano 4 já contava uma por pedido.

## 5. O tempo de cada exame: quanto paga por hora de sala

Um exame que paga R$ 70 em 15 minutos rende mais que um que paga R$ 115 em 40. O que se
compara é **R$ por hora = preço × 60 ÷ minutos**. A aba 6 faz a conta.

No ultrassom, o custo da hora (médico e sala) é quase o mesmo para qualquer exame. Por isso o
exame que paga mais por hora é também o que exige menos horas de sala para executar o mesmo
valor e o que deixa mais folga.

**Os tempos:**
- **Ultrassom:** o intervalo mínimo de agendamento da Recomendação do CBR (Colégio Brasileiro
  de Radiologia), de 14/11/2017, item a item.
- **Tomografia:** os intervalos do plano 4, de 20 minutos com contraste e 15 sem. A
  angiotomografia de coronárias tem 30 minutos por hipótese.

As células dos minutos estão em amarelo e podem ser editadas: com os tempos que as clínicas
praticarem, a conta se refaz.

**Ultrassom, do que paga mais por hora para o que paga menos** (filas dos últimos 24 meses):

| exame | Candanga | min | R$/hora | Portaria R$/hora | 24 meses |
|---|---:|---:|---:|---:|---:|
| Transfontanela (infantil) | R$ 268,73 | 25 | 645 | — | 242 |
| Parede abdominal (paga como abdômen total) | R$ 117,51 | 15 | **470** | 401 | 2.197 |
| Abdômen superior | R$ 101,27 | 15 | 405 | 400 | 1.234 |
| Bolsa escrotal | R$ 100,00 | 15 | 400 | — | 599 |
| Aparelho urinário | R$ 90,53 | 15 | 362 | 400 | 2.655 |
| Abdômen total | R$ 117,51 | 20 | **353** | 301 | 7.664 |
| Doppler de carótidas e vertebrais | R$ 115,61 | 20 | **347** | 301 | 4.156 |
| Transvaginal | R$ 83,77 | 15 | **335** | 400 | 5.691 |
| Obstétrica com Doppler | R$ 134,44 | 25 | 323 | — | 138 |
| Próstata abdominal | R$ 74,19 | 15 | 297 | 400 | 2.201 |
| Articulação e segmentos | R$ 70,97 | 15 | 284 | — | 7.468 |
| Partes moles por região (inguinal, pescoço, axila) | R$ 70,97 | 15 | 284 | — | 959 |
| **Partes moles (IEV)** | R$ 70,97 | 15 | 284 | — | 1.891 |
| Tireoide | R$ 64,07 | 15 | 256 | 400 | 2.408 |
| Mamas | R$ 70,97 | 20 | **213** | 300 | 8.501 |
| Doppler de tireoide | R$ 64,07 | 20 | 192 | 300 | 685 |
| Pélvica | R$ 43,41 | 15 | 174 | — | 698 |
| **Doppler de membros, bilateral** (venoso e arterial) | R$ 115,61 | 40 | **173** | 150 | 7.607 |
| Obstétrica morfológica | R$ 62,22 | 45 | 83 | — | 59 |

**O que muda com o tempo:**
- **O Doppler de membros é o caso mais forte do seu exemplo.**
  - Ele paga R$ 115,61, mas o CBR conta 20 minutos por membro (só traz o unilateral), e o
    pedido é bilateral: 40 minutos, por extrapolação a confirmar com quem faz o exame.
  - Rende R$ 173 por hora, menos que a articulação (R$ 70,97 em 15 minutos, R$ 284 por hora).
  - É a maior fila de Doppler (7.607) e era a segunda maior parte do plano 4 (9.834).
  - **E não se fatura em dobro.** A ficha SIGTAP (competência 10/2026) diz que as quantidades
    "independem da quantidade de vasos estudados": o pedido bilateral é uma unidade. A ficha
    está em `planos/redacao_04/dados/fontes/sigtap_0205010040_102026.md`.
- **O Doppler de carótidas e vertebrais é o contrário.** É bilateral num item só (20 minutos) e
  rende R$ 347 por hora, o dobro do de membros.
- **A mama cai para o pé da lista.** Paga R$ 70,97 e leva 20 minutos: R$ 213 por hora.
- **Transvaginal, aparelho urinário e abdômen superior sobem.** Pagam menos que o abdômen
  total, mas levam 15 minutos e rendem parecido ou mais por hora.
- **A parede abdominal é a melhor da lista grande.** Paga o abdômen total e leva o tempo de
  uma estrutura superficial. Mas os 15 minutos são por analogia (o CBR não cita parede) e o
  pagamento como abdômen total é enquadramento da SES (seção 4): por isso ela fica condicionada.
- **A articulação, de R$ 70,97, rende mais por hora que a mama, a tireoide e o Doppler de
  membros.**

**Tomografia:**
- **Sem contraste:** R$ 1.237 por hora. Quase toda essa fila é de emergência.
- **Com contraste:** R$ 928 por hora, e o contraste ainda é custo dentro do exame.
- **Angiotomografia de coronárias:** cerca de R$ 618 por hora.

Não compare a hora do tomógrafo com a do ultrassom: o custo da hora de cada aparelho é outro.

**Duas metas que puxam para lados opostos.** Com o valor do plano fixo, o exame que paga mais
por hora executa o recurso com menos salas e médicos. Já o exame mais barato atende mais
gente com o mesmo dinheiro. O R$ por hora diz quanta capacidade a carteira exige. Num
convênio, a folga não vira lucro: volta como saldo ou vira mais exames.

## 6. A escolha: quatro critérios e a carteira conjunta

A aba 7 cruza quatro critérios, exame a exame:
- **compartilhamento do equipamento:** o exame cabe na plataforma de ultrassom geral, com
  Doppler, convexo e linear, e no radiologista geral, ou pede transdutor, sala ou equipe
  própria;
- **receita por hora:** a da seção 5;
- **custo de execução:** no ultrassom feito por nós, a margem por hora; na tomografia feita
  na clínica, a margem por exame;
- **tamanho da fila:** os pedidos dos últimos 24 meses.

Cada critério dá uma nota de 1 a 3, e os pontos são a soma, com máximo de 12. Os pesos, os
custos e a nota de compartilhamento estão em amarelo e podem ser editados.

A coluna **Posição na carteira** traz a carteira que as duas revisões sustentam: a minha e a
do Codex. O cotejo está em `comparativo_revisoes_imagem_20261101.md`.

**De onde vem o custo.** São premissas do plano 4, ainda não negociadas:
- **Ultrassom:** a planilha `custo_por_exame_v2`. Sala e aparelho custam R$ 5.500 por mês,
  em 168 horas. O médico custa R$ 100 por hora, o equivalente a R$ 33,33 por exame de 20
  minutos. Os insumos custam R$ 3. O custo por exame fica em R$ 36 com 15 minutos, R$ 47
  com 20 e R$ 91 com 40.
- **Tomografia:** R$ 170 na clínica, com contraste. A angiotomografia de coronárias falta
  cotar.

Pagando o médico por exame, e não por hora, a ordem quase não muda. O aparelho urinário e a
tireoide perdem um ponto cada, e o Doppler de membros melhora, mas continua entre os piores.

### Carótidas e membros: a mesma tarifa, outro exame

| | Doppler de carótidas e vertebrais | Doppler de membros, bilateral |
|---|---:|---:|
| tarifa | R$ 115,61 | R$ 115,61 |
| tempo de sala | 20 min | 40 min (2 × 20 do CBR unilateral; extrapolação a confirmar) |
| receita por hora | R$ 347 | R$ 173 |
| custo por exame | R$ 47 | R$ 91 |
| margem por hora | **R$ 205** | **R$ 36** |
| equipamento e médico | a plataforma geral com Doppler; exame curto | Doppler vascular; ocupa a sala o dobro do tempo |
| fila (24 meses) | 4.156 | 6.197 venoso e 1.410 arterial |
| **pontos** | **11** | **6 e 5** |

### A carteira de ultrassom

| posição | exames (pontos) | por quê |
|---|---|---|
| **1. Núcleo** | abdômen total (12), abdômen superior (11), aparelho urinário (11), Doppler de carótidas (11) | mesma plataforma; R$ 347 a R$ 405 por hora; 15.709 pedidos, a cerca de R$ 355 por hora |
| **2. Condicionada** | parede abdominal (11); partes moles por região (8) | a parede rende R$ 470 por hora, mas os 15 minutos são por analogia (o CBR não cita parede) e o pagamento como abdômen total depende da SES; nas regiões, falta confirmar se também são do IEV |
| **3. Complemento** | bolsa escrotal (10), articulação (9), próstata (9), tireoide (9), mama (7) | mesma plataforma, com menos por hora; a mama entra pela necessidade da fila, não pelo preço |
| **4. À parte** | transvaginal (10), transfontanela (8), Doppler de membros (6 e 5), Doppler de tireoide (6), pélvica (6), obstétricas (6 e 5) | transdutor endocavitário e maca ginecológica, pediatria, Doppler vascular longo ou fila pequena |
| **Fora** | **partes moles (IEV)** (9) | são do IEV, em vermelho |

**A mama é a decisão que falta.** Era o maior item do plano 4, com 14.689 exames, e tem a
maior fila de ultrassom, 8.501. Rende R$ 71 de margem por hora, a mais baixa entre as filas
grandes. Se entrar, entra pela necessidade, e o plano precisa de mais salas para o mesmo
valor.

### A carteira de tomografia

| posição | exame (pontos) | leitura |
|---|---|---|
| **1. Núcleo** | TC com contraste eletiva de abdômen, pelve, tórax e pescoço (12) | fila de 10.539 e R$ 139 de margem por exame na clínica; cotar por protocolo, separando o que tem e o que não tem contraste, a emergência, a sedação e o infantil |
| **3. Complemento** | angiotomografias sem as de coronárias (10), TC sem contraste eletiva (9), TC de crânio, face e coluna (8) | mesmo tomógrafo; a fila eletiva sem contraste é pequena (515); crânio, face e coluna têm tarifa menor |
| **4. À parte** | angiotomografia de coronárias (5) | 30 min, tomógrafo de 64 canais com ECG e betabloqueador; a R$ 309,25 provavelmente não cobre a clínica: cotação própria |

### O cenário recomendado

O cenário que fecha os R$ 10,64 mi do plano 4, exame a exame, com os porquês e os riscos,
está em `cenario_recomendado_imagem_20261101.md`. A dúvida da parede abdominal está
registrada como L-007 em `planos/redacao_04/pendencias.md`.

## Limites

- **Os tempos do CBR são o intervalo mínimo de agendamento, de 2017.** Na prática, cada
  clínica tem o seu ritmo: o plano 4 citou 12 minutos por exame no ISHP. O que importa é a
  proporção entre os exames, e por isso a aba 6 deixa os minutos editáveis.
- **A coleta é de 29/10.** Na fase 0 do plano, a medição dos exames escolhidos se faz de novo,
  pela ordem de coleta.
- **A classificação do enquadramento é por palavra-chave do nome** (regras no script) e serve
  de triagem. A decisão de cada fila é do usuário e vai para o enquadramento do plano.
- **As partes moles são do IEV, por instrução sua.** O Codex lembrou um ponto: em 27/10,
  só 70 dos 3.124 pedidos de partes moles tinham CID aceito pela OCI do IEV
  (`estudo_us_articulacao_20261027.md`). Se a cobertura do IEV for pela OCI, e não pela fila,
  a sobreposição real é pequena.
- **Só a fila com o nome "PARTES MOLES" está marcada como do IEV.** As regiões de partes moles
  com nome próprio estão em preto, e é preciso confirmar se também são do IEV:
  - inguinal (D 214, E 180, sem lado 134);
  - pescoço/cervical (205);
  - axila (30);
  - glútea (3);
  - estrutura superficial (2).


Os achados e cálculos do Codex estão separados na aba **8 Achados Codex**, que tem um ranking
próprio por receita ou resultado por hora e custos em branco até a cotação. O script deste
estudo regera só as abas Leia e 0 a 7 e não mexe na aba 8.
