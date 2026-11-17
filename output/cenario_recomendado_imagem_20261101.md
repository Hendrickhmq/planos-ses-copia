# O cenário recomendado — exames de imagem do plano de R$ 11,5 mi pela Candanga

> **Em revisão (01/11/2026, mais tarde):** este cenário usa filas que já têm dono. A bolsa
> escrotal e as TC de pescoço, crânio e face são do redacao_07, e as TC de coluna, de
> articulações e de segmentos são compatíveis com a OCI de ortopedia do IEV. A regra de que
> um pedido só entra num plano está na L-008 de `planos/redacao_04/pendencias.md`. Sem essas
> filas, o cenário não fecha só com ultrassom. A alternativa é a do plano 4 assinado com
> mais tomografia, ainda a decidir.

**Controle interno, 01/11/2026.** Este é o melhor cenário para o ajuste de preço do plano 4:
**R$ 10.636.535,77 em 83.545 exames**, contra R$ 10.636.542,52 em 79.144 exames na versão
assinada. A diferença é de R$ 6,75, porque o Doppler fecha em exame inteiro. O apoio
(R$ 956.160,00) fica fora desta conta e não muda.

Os números vêm de duas fontes:
- **as filas:** a coleta do Mapa Social de 29/10/2026, com todos os pedidos pendentes, a
  mesma base que o plano 4 usou;
- **os preços:** a Tabela SUS Candanga, modalidade SIA.

O estudo completo está em `estudo_imagem_candanga_20261101.md`.

## 1. O que entra

| posição | exame | código | exames | preço | valor |
|---|---|---|---:|---:|---:|
| núcleo | Abdômen total | 02.05.02.004-6 | 10.342 | R$ 117,51 | R$ 1.215.288,42 |
| núcleo | Doppler de carótidas e vertebrais | 02.05.01.004-0 | 4.334 | R$ 115,61 | R$ 501.053,74 |
| núcleo | Aparelho urinário | 02.05.02.005-4 | 4.031 | R$ 90,53 | R$ 364.926,43 |
| núcleo | Abdômen superior | 02.05.02.003-8 | 2.222 | R$ 101,27 | R$ 225.021,94 |
| condicionada | Parede abdominal | 02.05.02.004-6 | 3.303 | R$ 117,51 | R$ 388.135,53 |
| complemento | Mama bilateral | 02.05.02.009-7 | 12.943 | R$ 70,97 | R$ 918.564,71 |
| complemento | Articulação e segmentos | 02.05.02.006-2 | 9.978 | R$ 70,97 | R$ 708.138,66 |
| complemento | Tireoide | 02.05.02.012-7 | 3.049 | R$ 64,07 | R$ 195.349,43 |
| complemento | Próstata abdominal | 02.05.02.010-0 | 2.969 | R$ 74,19 | R$ 220.270,11 |
| complemento | Bolsa escrotal | 02.05.02.007-0 | 934 | R$ 100,00 | R$ 93.400,00 |
| fechamento | Transvaginal | 02.05.02.018-6 | 9.287 | R$ 83,77 | R$ 777.971,99 |
| fechamento | Doppler de membros (venoso e arterial) | 02.05.01.004-0 | 5.870 | R$ 115,61 | R$ 678.630,70 |
| **ultrassom** | | | **69.262** | | **R$ 6.286.751,66** |
| núcleo | TC com contraste: abdômen, pelve, tórax, pescoço | 02.06.03.001-0, 02.06.03.003-7, 02.06.02.003-1, 02.06.01.005-2 | 10.575 | R$ 309,25 | R$ 3.270.318,75 |
| complemento | Angiotomografias (sem as de coronárias) | código da região | 2.494 | R$ 251,29 a R$ 309,25 | R$ 748.781,02 |
| complemento | TC com contraste: crânio, face, coluna | 02.06.01.007-9, 02.06.01.004-4, 02.06.01.001-0 a 003-6 | 695 | R$ 251,29 a R$ 260,09 | R$ 176.142,55 |
| complemento | TC sem contraste, eletiva | código da região | 519 | R$ 251,29 a R$ 309,25 | R$ 154.541,79 |
| **tomografia** | | | **14.283** | | **R$ 4.349.784,11** |
| **total** | | | **83.545** | | **R$ 10.636.535,77** |

**O que fica de fora:**
- **as partes moles:** são do IEV;
- **as partes moles por região** (inguinal, pescoço, axila): falta confirmar se também são do IEV;
- **a angiotomografia de coronárias:** a R$ 309,25, provavelmente não cobre a clínica;
- **as filas de emergência;**
- **o Doppler de tireoide, a pélvica, as obstétricas e a transfontanela:** pagam pouco por
  hora, têm fila pequena ou pedem equipe própria.

## 2. Por que este cenário

A ordem de entrada segue os quatro critérios do estudo: equipamento compartilhado, receita
por hora, custo de execução e tamanho da fila.

1. **O núcleo rende mais por hora numa sala só.**
   - Abdômen total, abdômen superior, aparelho urinário e Doppler de carótidas rendem de
     R$ 347 a R$ 405 por hora.
   - Todos cabem na mesma plataforma de ultrassom (Doppler, convexo e linear) e no mesmo
     radiologista.
   - Na tomografia, o núcleo é a fila grande de abdômen, pelve e tórax com contraste: 10.575
     exames, a R$ 309,25.
2. **A parede abdominal é o exame que mais rende** (R$ 470 por hora), mas depende de a SES
   confirmar o enquadramento (seção 3).
3. **Os complementos usam a mesma sala e esgotam filas grandes.** A mama e a articulação têm
   as maiores filas de ultrassom. Rendem menos por hora, entre R$ 213 e R$ 297, e entram pela
   necessidade da fila. A mama entra inteira (12.943), e não pelos 14.689 do plano anterior,
   porque a fila diminuiu.
4. **O fechamento usa os dois melhores entre os exames à parte.**
   - O **transvaginal** rende R$ 335 por hora, quase o mesmo que o núcleo. Fica à parte só
     porque pede transdutor endocavitário e maca ginecológica.
   - O **Doppler de membros** entra só no quanto falta, 5.870 de 12.041. É o exame que menos
     rende por hora (R$ 173, em 40 minutos), mas a fila é grande e ajusta o valor exato.
5. **Sem os dois do fechamento, não fecha.**
   - Núcleo, parede e complementos somam R$ 9,18 mi.
   - Sem o transvaginal, faltaria mais Doppler de membros do que a fila tem.

**Comparado ao plano 4 assinado:**

| | plano 4 (Portaria) | este cenário (Candanga) |
|---|---:|---:|
| valor dos exames | R$ 10.636.542,52 | R$ 10.636.535,77 |
| exames | 79.144 | 83.545 (+4.401) |
| horas de sala de ultrassom, nos intervalos do plano 4 (20 min; Doppler 30) | 24.260 | 24.788 (+2%) |
| horas de tomógrafo | 4.478 | 4.718 (+5%) |

São mais exames pelo mesmo valor, porque a Candanga paga menos que a Portaria nos exames
de região isolada. A capacidade exigida sobe pouco.

## 3. Os riscos

| # | risco | tamanho | o que fazer |
|---|---|---|---|
| 1 | **A SES não confirmar a parede abdominal como abdômen total**, ou a auditoria glosar depois | até R$ 388 mil | confirmar por escrito antes de assinar (L-007 em `planos/redacao_04/pendencias.md`); sem confirmação, a parede sai e o Doppler de membros sobe para 9.227 |
| 2 | **Pedidos antigos não acharem paciente.** A base é a fila inteira, com pedidos de 2021 a 2024; pela fila dos últimos 24 meses, nem tudo somado chega a R$ 10,64 mi (R$ 9,93 mi) | difícil de medir; maior na mama, articulação, transvaginal e Doppler de membros, onde a fila velha pesa | busca ativa e confirmação já previstas no plano; medir os entrantes dos 8 meses na nova coleta, porque pedidos novos repõem os que não se acham |
| 3 | **O Doppler de membros não achar médico pelo preço.** Ele ocupa a sala 40 minutos por R$ 115,61, e um médico pago por exame tende a recusar | 5.870 exames, R$ 679 mil | cotar com quem faz Doppler vascular; se não houver, trocar por mais tomografia (angiotomografia de coronárias, depois de cotada) |
| 4 | **Os tempos são de referência, não medidos.** O CBR é de 2017 e dá o intervalo mínimo; os 40 minutos do Doppler bilateral são 2 × 20, extrapolação | muda a capacidade, não o valor | pedir às clínicas o tempo praticado; a planilha refaz a conta |
| 5 | **Os custos são premissas do plano 4**, não cotação: sala, aparelho, médico e tomografia na clínica a R$ 165–175 com contraste | a margem pode ser menor | cotar a plataforma com o transdutor endocavitário, o médico por exame e a TC com contraste incluído (o contraste não é pago à parte na Candanga) |
| 6 | **Sobreposição com outros planos: não pode acontecer** (decisão do usuário) | qualquer pedido contado duas vezes | regra da L-008: ficam fora as filas do redacao_07 e as TC de ortopedia do IEV; a TC de pelve entra sem os CID da OCI 09.03.01.003-8; as partes moles ficam fora inteiras |
| 7 | **A coleta é de 29/10.** As filas mudam | os números exatos | medir de novo os exames escolhidos na fase 0, pela ordem de coleta |
| 8 | **A troca no mix pode ser questionada.** O plano assinado tinha mais mama (14.689) e menos abdômen e transvaginal | de redação | explicar que a mama entra inteira, toda a fila que existe, e que a troca segue o preço da Candanga |

**Os dois riscos que mais pesam são o 1 e o 2.** O 1 se resolve com um documento antes de
assinar. O 2 é o mesmo risco que o plano 4 já corria, e se mede na nova coleta.
