# O que difere neste plano

O `PADRAO.md` vale inteiro. Este arquivo registra só o que o plano 4 faz de
diferente dos três anteriores, e por quê.

## 1. O objeto é o exame, não a OCI

Os planos 1 a 3 compraram Ofertas de Cuidados Integrados: um percurso com consulta,
procedimento, laudo e retorno, remunerado por um código único de grupo 09.

Aqui o objeto é **a realização do exame e a entrega do resultado ao usuário e à
unidade solicitante**. Não há consulta de entrada, não há retorno, não há gestão do
cuidado dentro do objeto. A obrigação nasce no exame agendado e termina no laudo
entregue.

Três consequências que atravessam o documento inteiro:

- **A unidade de aferição é o exame laudado e entregue**, não o usuário atendido nem
  o percurso concluído.
- **A meta qualitativa mede a entrega do laudo**, porque é ali que a obrigação
  termina — não na conclusão de um percurso que o plano não contrata.
- **Não há janela de duas competências a administrar.** O que o cronograma físico
  precisa dizer é a capacidade mensal e a curva, e nada mais.

## 2. Não há um valor unitário — há cinco

Um plano de OCI tem um número: R$ 600,11. Este tem cinco bases de tabela e cinco
unitários, e onze códigos SIGTAP repartidos entre eles.

**A planilha de execução se organiza por código**, não por nome de fila, porque é o
código que vai ao SIA. Dois pares de linhas da fila colapsam no mesmo código — os
dois dopplers e os dois tórax.

O `dados/valor_unitario.md` traz a tabela por código; o
`dados/conferencia_procedimentos.md` traz a correspondência entre o nome da fila e o
nome da tabela, linha a linha, com o verdito de cada uma.

## 3. O unitário tem incremento, e o incremento é da portaria

O valor não é o da tabela pura: é **tabela × (1 + incremento do Anexo I da Portaria
SAES/MS nº 4.282/2026)**. O incremento é desenho da portaria e não composição do
plano, o que mantém a regra 1 do padrão — o número tem fonte com data, não
plausibilidade.

**O centavo se trunca.** R$ 99,946 declara-se R$ 99,94.

## 4. A direção do dimensionamento se inverte — se D-001 confirmar

Nos planos anteriores o recurso era dado e o quantitativo era o piso de
`(recurso − apoio) ÷ unitário`. Aqui a planilha do usuário pede o contrário: as filas
são dadas e o recurso é a soma.

A regra 2 do padrão não some com a inversão, muda de lugar: **o total continua sem
fechar por ajuste**, e continua havendo um piso indivisível — o exame. Se D-001
trouxer teto de emenda, a direção volta a ser a dos planos 1 a 3 e o quantitativo
volta a ser calculado.

## 5. O que a fase 0 ainda não tem

O `pendencias.md` tem quatro lacunas e quatro decisões. Três linhas da fila — 7.492
exames, R$ 1,1 milhão — não têm código fechado, e as fichas SIGTAP dos onze códigos
não foram consultadas. **Nenhuma seção se escreve antes disso.**
