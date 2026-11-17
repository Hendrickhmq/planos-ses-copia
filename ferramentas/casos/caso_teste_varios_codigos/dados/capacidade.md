# Capacidade requerida — memória interna

Aberto em 15/09/2026, depois de travada a vigência de 12 meses.

**Os intervalos de agendamento saíram do plano em 17/09/2026**, pela mesma regra da
carga por posto: são premissa sem fonte, e a verificação T os apanhou publicados no
documento. O plano declara as horas de sala e os equipamentos que elas exigem; a
conversão de exame em minuto fica aqui.

**Este arquivo calcula a capacidade que a meta exige, não o parque que o proponente
tem.** O usuário declarou em 15/09/2026 que o proponente já possui ultrassom e
tomógrafo e não conseguiu confirmar quantas salas nem em que turno — L-006. Inventário
não confirmado não se publica; capacidade requerida se calcula e se declara.

**Os tempos de sala abaixo são premissa sem fonte** e continuam precisando de
confirmação.

## As premissas de tempo

| exame | tempo de sala | fonte |
|---|---|---|
| ultrassom de região isolada | 20 min | **premissa, sem fonte** |
| ultrassom com doppler colorido | 30 min | **premissa, sem fonte** |
| tomografia com contraste | 20 min | **premissa, sem fonte** |
| tomografia sem contraste | 15 min | **premissa, sem fonte** |

O doppler pesa mais porque são 14.401 exames a 30 minutos: sozinho, consome 432.030
minutos de sala, 31% de toda a carga de ultrassom.

## A carga

**Revisto em 22/09/2026 (D-007):** sai a ecografia de partes moles, 2.974 exames a
20 minutos. A carga de tomografia não muda.

A execução do objeto requer **28.530 horas** de sala no período: **24.106 horas** de
ultrassonografia e **4.424 horas** de tomografia computadorizada.

| | exames | horas de sala |
|---|---|---|
| Ultrassom | 65.120 | 24.106 h |
| Tomografia | 13.452 | 4.424 h |
| **Total** | **78.572** | **28.530 h** |

## As salas que a vigência exige

Com 12 meses de produção — 252 dias úteis, 6.171 por mês, 294 por dia útil:

| turno | salas de ultrassom | tomógrafos |
|---|---|---|
| turno de 8 horas | 12 | 2 |
| turno de 10 horas | **10** | **2** |
| turno de 12 horas | 8 | 2 |

## O que isto diz sobre os três polos

Os polos são Ceilândia, Sobradinho e Gama, com a cobertura do plano 3.

**A ordem de grandeza é de dez salas de ultrassom e dois tomógrafos em turno de 10 horas.** E os dois números se comportam de modo oposto entre três endereços:

- **Ultrassom distribui.** Dez salas repartidas entre três polos é um arranjo natural,
  e o ultrassom é o exame que o usuário faz perto de casa.
- **Tomografia concentra.** Dois tomógrafos não se espalham por três endereços sem
  ociosidade — 4.424 horas de sala em doze meses são 15,7 horas por dia útil, que um
  aparelho absorve em dois turnos.

**A repartição entre os polos ainda não se calcula**, porque a fila de imagem não veio
aberta por Região de Saúde — L-005. É ela que governa quantas salas cada polo recebe.

## O risco que este arquivo abre

Se o parque real ficar abaixo de dez salas de ultrassom em turno de 10 horas, **a
meta não é executável no ritmo previsto**. É o maior risco de execução do plano e vai
à seção 8 com este número.

## O que falta

| falta | efeito |
|---|---|
| distribuição da fila por Região de Saúde | **L-005** · reparte as salas entre os polos |
| tempos de sala do proponente | substituem as quatro premissas acima |
| turno praticado | escolhe a linha das tabelas acima |
| parque instalado por polo | **L-006** · não se publica; entra como risco |

## Por polo — o que a 6.3 publica (v8, 22/09/2026)

Horas de cada polo = exames rateados procedimento a procedimento × tempo de sala,
arredondadas ao inteiro; o total da tabela é a soma dos polos. Salas =
teto(horas ÷ (252 dias × 10 h × 0,80)) — ocupação máxima de 80% sobre turno de 10 h,
regra que reproduz exatamente os 5 / 4 / 4 da v7.

| | Ceilândia | Sobradinho | Gama | total |
|---|---|---|---|---|
| exames | 31.183 | 23.527 | 23.862 | 78.572 |
| exames por dia útil (teto de ÷ 252) | 124 | 94 | 95 | 313 |
| horas de ultrassom | 9.176 | 7.066 | 7.864 | 24.106 |
| salas de ultrassom | 5 | 4 | 4 | 13 |
| horas de tomografia | 1.928 | 1.592 | 904 | 4.424 |
| tomógrafos | 1 | 1 | 1 | 3 |

O total de horas de US é a soma dos polos, 24.106; o agregado sem arredondar por polo
seria 24.106,83. A diferença é de arredondamento e não muda sala nenhuma.

## A 6.3 detalhada — v10, 24/09/2026

A devolutiva de 20/09 marcou a tabela da 6.3 em azul: **"precisa de mais
detalhamento"**. O usuário definiu o alcance em 24/09: *"só um plano geral de quantas
salas, quantos exames etc"*. Os parâmetros não mudaram, e salas e tomógrafos continuam
13 e 3.

**Exames por modalidade e polo.** A tomografia de cada polo é o rateio procedimento a
procedimento, arredondado pelos maiores restos até fechar 13.452; a ultrassonografia é
o total do polo menos a tomografia.

| | Ceilândia | Sobradinho | Gama | total |
|---|---|---|---|---|
| ultrassonografia | 25.327 | 18.685 | 21.108 | 65.120 |
| tomografia | 5.856 | 4.842 | 2.754 | 13.452 |
| US por dia útil (teto de ÷ 252) | 101 | 75 | 84 | 260 |
| TC por dia útil (teto de ÷ 252) | 24 | 20 | 11 | 55 |
| exames por sala de US por dia útil (teto) | 21 | 19 | 21 | |

O horário de 10 horas por dia útil é o turno em que a regra das salas foi montada
(ocupação até 80%).

**O que ficou fora, de propósito.** O tempo por exame (20 e 30 minutos) segue sem ir ao
documento. Em 24/09 conferimos a Seção D dos Parâmetros SUS (Portaria GM/MS nº
1.631/2015, NESCON/UFMG 2013), que propõe **40 minutos e 12 exames por equipamento por
dia** no ultrassom: nesse parâmetro seriam **23 salas** (9 / 7 / 7), e não 13. No
tomógrafo, 7.000 exames por equipamento por ano confirmam um por polo. O Quadro 1 do
mesmo documento (UKAS 2008) dá de 15 a 30 minutos por tipo de exame, o que está mais
perto da nossa premissa. O usuário escolheu não entrar em parâmetro. **Se o analista
confrontar com os Parâmetros SUS, é aqui que a conta aparece** — o R-01 continua de pé.

Cópia do documento: `~/.claude/projects/.../tool-results/webfetch-1790272462018-69a8nk.pdf`
(gov.br, "se-o-d-equipamentos.pdf", 93 páginas). Não está em `normas/`.
