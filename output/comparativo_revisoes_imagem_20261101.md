# Comparativo — as duas revisões da escolha de exames de imagem

**Controle interno, 01/11/2026.** Este arquivo compara as duas revisões feitas sobre o mesmo
estudo, `estudo_imagem_candanga_20261101`:
- **a minha (Claude):** a aba "7 Quatro critérios" e a seção 7 do texto;
- **a outra ferramenta:** a aba "7 Escolha por aparelho", a seção 6 do texto e os ajustes das
  abas 0, 1, 2, 5 e 6.

A aba da outra revisão saiu da planilha quando eu a regerei. Ela foi reconstituída a partir
dos arquivos que essa revisão deixou em `tmp/revisao_carteira_20261101/`:
- o preparo, em `preparar.py`;
- os dados por grupo, em `dados.json`;
- o script, em `revisar.mjs`;
- as imagens das abas.

Os números citados dela foram conferidos: 15.709 pedidos, R$ 1.746.396,13 e 4.912,25 horas.

## 1. O método

| | outra ferramenta | Claude |
|---|---|---|
| critério de ordem | receita bruta por hora; quando os custos forem preenchidos, resultado estimado por hora (escolha numa lista) | soma de notas de 1 a 3 em quatro critérios: compartilhamento, receita por hora, custo e fila |
| custo | **deixado em branco de propósito** ("nenhum custo inventado"); o resultado só aparece quando alguém preenche | **premissas do plano 4** (`custo_por_exame_v2`): médico a R$ 100/h, sala e aparelho a R$ 5.500/mês em 168 h, insumos a R$ 3; tomografia na clínica a R$ 170 |
| tamanho da fila | aparece na tabela, mas não entra na ordem | é um dos quatro critérios |
| compartilhamento | descreve o transdutor ou recurso de cada exame; parte de **uma plataforma de US geral com Doppler, convexo e linear** | nota de 1 a 3, por julgamento: sala comum, recurso próprio ou equipe à parte |
| tomografia | não ordena: "cotar por protocolo", separando contraste, emergência, sedação e pediatria | ordena cinco blocos pelo preço da clínica |
| ordem automática | sim: reordena quando mudam os tempos, os custos ou o critério | as notas e os pontos se recalculam, mas a ordem das linhas é fixa (dá para ordenar pelo filtro) |

**A diferença de fundo:** a outra revisão não quis usar custo sem cotação, e por isso só
ordena pela receita. A minha usa o custo do plano 4, que ainda não foi negociado, para poder
ordenar agora. As duas escolhas são defensáveis, e a minha depende de premissas que podem mudar.

## 2. Os resultados, exame a exame

| exame | 24 meses | outra ferramenta | Claude (pontos) | concordam? |
|---|---:|---|---|---|
| Abdômen total | 7.664 | núcleo | núcleo (12) | sim |
| Abdômen superior | 1.234 | núcleo | núcleo (11) | sim |
| Aparelho urinário | 2.655 | núcleo | núcleo (11) | sim |
| **Doppler de carótidas** | 4.156 | **núcleo** | **segunda camada (10)** | **não** |
| **Parede abdominal** | 2.197 | **condicionada** (tempo por analogia, enquadramento) | **núcleo (11)** | **não** |
| Transvaginal | 5.691 | ampliação (custo do endocavitário) | segunda camada (10) | quase |
| Bolsa escrotal | 599 | complemento | segunda camada (10) | quase |
| Articulação | 7.468 | complemento | volume com margem menor (9) | sim |
| Próstata, tireoide | 2.201 / 2.408 | complemento | volume com margem menor (9) | sim |
| Mama | 8.501 | complemento; "não excluir só pela tarifa" | cauda (7); "caso a decidir" | no lugar, sim; na ênfase, não |
| Doppler de membros | 7.607 | reavaliar depois de tempo e custo reais | cauda (6 e 5) | sim |
| Obstétricas e transfontanela | pequenas | perfil próprio, à parte | cauda | sim |
| **Partes moles** | 1.891 | **condicionada: conferir sobreposição com o IEV por pedido e CID** | **do IEV, em vermelho, fora da conta** | **não** |
| TC com contraste de abdômen, pelve e tórax | 10.066 | começar a cotação por aqui | 1º da TC (12) | sim |
| Angiotomografia de coronárias | 1.542 | avaliação técnica e econômica própria | último da TC (5); cotar | sim |

**Onde as duas concordam:**
- o núcleo convexo: abdômen total, superior e urinário;
- separar o Doppler de carótidas do de membros, e rebaixar o de membros;
- 1 unidade por Doppler bilateral (ficha SIGTAP);
- a mama, a articulação e a tireoide como complemento;
- a TC de abdômen, pelve e tórax em primeiro;
- a angiotomografia de coronárias à parte.

## 3. As quatro divergências

**a) O Doppler de carótidas (núcleo × segunda camada).** A diferença está só na nota de
compartilhamento. Eu dei 2 por pedir Doppler. A outra revisão parte de uma plataforma geral
que já traz Doppler e linear, e nessa premissa o Doppler cabe na sala comum. Se a cotação for
dessa plataforma, a nota sobe para 3 e as carótidas vão a 11 pontos, no núcleo. **A outra
revisão está mais próxima do que se vai cotar.** Fica uma ressalva: o laudo de Doppler pede um
médico que o faça.

**b) A parede abdominal (condicionada × núcleo).** Os dois números são os mesmos: R$ 470 por
hora, em 15 minutos. A outra revisão marca que o CBR não cita a parede abdominal e que os 15
minutos são analogia. Ela também diz que o pagamento como abdômen total é enquadramento da SES.
Eu tinha marcado esse enquadramento na seção 4, mas pus a parede no núcleo mesmo assim. **A
outra revisão está mais cuidadosa:** a parede é o melhor exame da lista se o enquadramento
ficar, e não deve ser a base do plano antes disso.

**c) As partes moles (sobreposição × do IEV).** A outra revisão trocou o meu texto, "são do IEV",
por "conferir possível sobreposição". **Aqui vale a sua instrução:** você disse que as filas
de partes moles são do IEV. O que a outra revisão aponta tem fundamento num estudo anterior
(`estudo_us_articulacao_20261027.md`): naquela data, só 70 dos 3.124 pedidos de partes moles
tinham CID aceito pela OCI do IEV. Se a cobertura do IEV for por plano, e não por CID, a
instrução fica como está. Se for pela OCI, a sobreposição real é pequena.

**d) O código fora do Anexo ("vale o SIGTAP" × "não atribuir automaticamente").** O padrão do
projeto diz "código fora do Anexo: vale o SIGTAP da ficha". Isso está no README da tabela
Candanga, item 3, e na LI-002. **A minha redação segue o padrão.** A da outra revisão é mais
restritiva e só pesa em 5 códigos, nenhum de US ou TC (OCT, radiografia periapical, dois de
raio-X e a angiografia).

## 4. Outras diferenças menores

- **82.981 × 82.983 pedidos de US.** A outra revisão está certa: 82.981 conta cada pedido uma
  vez só (a união medida no motor), e 82.983 é a soma das filas. Ela guardou os dois na aba 0.
- **O transdutor do Doppler de membros:** ela pôs "linear + Doppler", e eu pus "linear +
  convexo + Doppler". Na ilíaca e em paciente obeso usa-se o convexo, mas isso não muda nada
  na plataforma geral.
- **Os 40 minutos do bilateral:** ela os chama de extrapolação a confirmar, e eu os usei como
  dado. Ela é mais precisa: o CBR só traz o unilateral (20 minutos).
- **Sedação e pediatria:** ela conta, em cada grupo de TC, os pedidos com sedação e os
  infantis. Eu só os marquei fila a fila, na aba 2.

## 5. A minha ordem resiste ao modo de pagar o médico?

A outra revisão observa que, se o médico for pago por exame, o custo dele entra no variável.
Refiz a minha conta com o modelo do ISHP, de R$ 33,33 por exame qualquer que seja o tempo:

| exame | margem/h (médico por hora) | margem/h (médico por exame) |
|---|---:|---:|
| Parede abdominal | 325 | 292 |
| Abdômen superior | 260 | 227 |
| Bolsa escrotal | 255 | 222 |
| Abdômen total | 211 | 211 |
| Doppler de carótidas | 205 | 205 |
| Aparelho urinário | 217 | **184** (nota cai de 3 para 2) |
| Transvaginal | 190 | 157 |
| Próstata | 152 | 119 |
| Articulação | 139 | 106 |
| **Doppler de membros** | **36** | **86** |
| Tireoide | 112 | **78** (nota cai de 2 para 1) |
| Mama | 71 | 71 |

**A ordem quase não muda.** O aparelho urinário perde um ponto, e a tireoide também. O
Doppler de membros melhora, porque o médico deixa de custar pelo tempo, mas continua entre os
piores. Ainda assim, um médico pago por exame dificilmente aceita o mesmo valor por 40
minutos e por 15.

## 6. Juntando o melhor das duas

Uma carteira que as duas sustentam:

1. **Núcleo para cotar:** abdômen total, abdômen superior, aparelho urinário e Doppler de
   carótidas, na plataforma geral com Doppler, convexo e linear. São 15.709 pedidos dos últimos
   24 meses, a R$ 355 por hora em média.
2. **Condicionada:** a parede abdominal, que entra no núcleo se a SES confirmar o pagamento
   como abdômen total.
3. **Complementos na mesma plataforma:** articulação, bolsa escrotal, próstata, tireoide e
   mama. A mama entra por decisão de necessidade, não pelo preço.
4. **A avaliar à parte:**
   - transvaginal, que depende do custo do transdutor endocavitário;
   - Doppler de membros, que depende do tempo real e do pagamento do médico;
   - obstétricas e transfontanela.
5. **Tomografia:** cotar abdômen superior, tórax e pelve com contraste, por protocolo. A
   angiotomografia de coronárias vai em cotação própria.
6. **Partes moles:** fora, como do IEV (sua instrução). Fica o registro da ressalva da outra
   revisão sobre o CID.

**O que falta nas duas:** a cotação real, que traz o aluguel com os transdutores, o médico por
exame ou por hora, o preço da clínica de TC e a angiotomografia de coronárias. Também falta o
tempo praticado pelas clínicas. Com isso, a aba da outra revisão e a minha passam a dar
resultado em vez de hipótese.
