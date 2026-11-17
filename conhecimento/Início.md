---
tipo: mapa
aliases:
  - "Inicio"
  - "Home"
tags: [mapa]
---
# Início

O cofre de conhecimento do projeto: os conceitos, as normas, os órgãos, os casos e os planos,
ligados entre si e aos treze módulos do curso. **Ele não guarda regra.** A regra mora em
[[metodo/LEIA|metodo/]], e a nota aponta para lá.

## Por onde começar

1. [[curso/mapa|O mapa do curso]]: o percurso inteiro numa página.
2. [[curso/LEIA|A ordem dos módulos]], e o primeiro: [[01_as_leis_do_sus_e_a_complementaridade|Módulo 1]].
3. As cinco perguntas de todo projeto, abaixo.

## As cinco perguntas

| pergunta | comece por |
|---|---|
| Por que uma entidade privada pode atender pelo SUS? | [[Complementaridade]] · [[SUS]] · [[Constituição arts. 196 a 200]] · [[Lei 8.080-1990]] |
| De onde vem o dinheiro? | [[Emenda parlamentar]] · [[Os dois trilhos da emenda]] · [[MAC]] · [[FAEC]] |
| Por qual instrumento, e por onde ele anda? | [[Convênio]] · [[MROSC]] · [[Fluxo dentro da SES]] |
| Para fazer o quê, para quem? | [[Fila regulada]] · [[OCI]] · [[SIGTAP]] · [[CNES]] · [[Dossiê do objeto]] |
| Quanto custa, e fecha? | [[Valor unitário]] · [[Tabela SUS Candanga]] · [[Cobertura]] · [[Apoio (custo acessório)]] |

## Os três documentos

[[Pré-projeto]] → [[Pré-plano]] → [[Plano de trabalho]] → [[Termo de convênio]] →
[[Prestação de contas]]

## As famílias de notas

| pasta | o que tem | comece por |
|---|---|---|
| `conhecimento/conceitos/` | o vocabulário do ofício, uma ideia por nota | [[Complementaridade]] |
| `conhecimento/normas/` | as leis, decretos e portarias que mais pesam, com o número no acervo | [[Normas por camada]] |
| `conhecimento/orgaos/` | quem é quem | [[SES-DF]] |
| `conhecimento/casos/` | o que aconteceu de verdade, e o que ensinou | [[Caso - os 50.317 da cardiologia]] |
| `conhecimento/planos/` | os cinco convênios estudados e os nossos projetos | [[redacao_04 - ultrassom e tomografia]] |
| `curso/` | os módulos, o mapa, o glossário e as dúvidas | [[curso/glossario|Glossário]] |

## Os temas que mais confundem

- [[FAEC]] e o [[Programa Agora Tem Especialistas]] (a PATE): base de preço, não fonte do dinheiro.
- [[Emenda individual]] e [[Emenda de bancada]]: cada uma com a sua portaria.
- [[Tabela SUS Candanga]] e [[SIGTAP]]: qual vale, e quando.
- O teto da fila ([[Teto, finalidade e núcleo]]) e o teto do preço ([[Oferta inicial e teto]]).
- Necessidade e insuficiência: ver [[Complementaridade]] e [[Caso - necessidade não é complementaridade]].

## Como o cofre se mantém

- Conceito novo vira nota em `conhecimento/conceitos/`, com os links e o módulo em que aparece.
- Regra nova vai para `metodo/`, nunca para a nota.
- `python3 ferramentas/testar_curso.py` confere que todo link resolve.
