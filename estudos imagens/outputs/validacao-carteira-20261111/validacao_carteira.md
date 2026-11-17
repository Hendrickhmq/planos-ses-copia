# Validação da carteira final v2 — 11/11/2026

**Conclusão: as contas principais e os preços escolhidos são reproduzíveis, mas a carteira não está integralmente validada para execução.** Há mudança relevante nas filas, itens condicionados incluídos no total, classificação clínica a corrigir e projeções cuja metodologia não acompanha exatamente o recorte final.

Arquivo analisado: `planos/redacao_04/estudos/carteira_final_v2_20261111.xlsx`. O original foi preservado. Nenhuma decisão registrada nos documentos foi tratada como nova autorização do usuário.

## 1. O que foi conferido

- Leitura das oito abas e de suas 352 fórmulas por extração do XML do XLSX.
- Recálculo independente de quantidades, receitas, margens, subtotais por modalidade, cenários de Doppler e ponte com a versão enviada.
- Comparação dos 24 preços das linhas escolhidas com a modalidade SIA da tabela oficial preservada no Git, referência `main`, commit `6673d50cdd0c5a0cbbdc8afb5452d771b8c4fb04`.
- Confronto com a coleta bruta do Mapa Social de 02/11, com o estudo de demanda e com os scripts que geraram a carteira e o estudo de margem.
- Consulta ao vivo de filas relevantes no Mapa Social. Atualização apresentada pelo painel: **11/11/2026 00:32:28**. A tabela da seção 3 documenta as consultas aproveitadas.
- Consulta à Deliberação CG-SES 46/2026, a fontes públicas sobre o registro do Doppler e à Nota Técnica SES-DF 21/2023 de ortopedia.

**Limites:** não houve nova coleta completa do universo, de CID, idade, oferta e entradas pelo motor Qlik. As consultas atuais foram pelo nome do procedimento, usando o indicador “Solicitações”; não se deve confundir esse número com pessoas, devolvidas ou com o recorte elegível por CID. Não foram conferidos contratos vigentes e produção atualizada do IEV, nem obtidas autorizações ou cotações das clínicas. Não foi executado Excel/LibreOffice para recalcular o arquivo.

## 2. Contas que conferem

| Medida | Resultado independente |
|---|---:|
| Meta de valor dos exames usada no arquivo | R$ 10.636.602,00 |
| Quantidade da carteira | 78.144 procedimentos/pedidos contabilizados |
| Ultrassons | 67.217 |
| Tomografias | 10.927 |
| Valor dos ultrassons | R$ 6.377.948,53 |
| Valor das tomografias | R$ 3.376.624,51 |
| Valor total da carteira | **R$ 9.754.573,04** |
| Falta para a meta de valor | **R$ 882.028,96** |
| Margem estimada antes dos demais compromissos do projeto | R$ 3.007.903,64, ou 30,84% |
| Doppler de membros incluído, uma unidade por pedido | R$ 1.392.291,23 |
| Falta caso o Doppler de membros seja excluído | **R$ 2.274.320,19** |
| Excesso caso o mesmo estoque de Doppler seja remunerado em dobro | R$ 510.262,27 |
| Projeção denominada “pedidos novos”: 11.824 unidades | R$ 1.361.258,12 |
| Essa projeção, excluindo o Doppler de membros | R$ 1.057.897,48 |
| Falta sem Doppler, mesmo somando a projeção dos demais exames | **R$ 1.216.422,71** |
| Carteira da versão enviada, valorizada pela Candanga | R$ 10.390.824,04 |
| Falta nessa versão enviada | R$ 245.777,96 |
| Não escolhidos classificados no arquivo como “cabe no aparelho” | R$ 2.604.841,90 |

Localizadores principais: `Resumo!B4:B14`, `Escolhidos!D5:L32`, `Da sobra à falta!B5:F29` e `Não escolhidos!D24:G26`.

**Preços:** não encontrei divergência nas 24 linhas escolhidas em relação ao CSV do Anexo oficial, modalidade SIA. A antiga análise comparativa de 06/08 tem valores diferentes e não deve substituí-lo. A conferência foi com a extração oficial preservada no repositório; não foi uma nova homologação de cada preço para o instrumento a celebrar.

## 3. O Mapa Social já mudou

Fonte ao vivo: [Mapa Social da Saúde — MPDFT](https://paineis-ext.mpdft.mp.br/extensions/mapasauderegulamentacao/mapasauderegulamentacao.html), Lista de Espera, Exames e Consultas. Coluna histórica: coleta bruta de 02/11. As comparações abaixo usam o mesmo nome de fila, com espaços normalizados na interface.

| Fila | Coleta 02/11 | Painel 11/11 | Diferença |
|---|---:|---:|---:|
| TC abdômen superior, adulto, com contraste, sem sedação | 4.116 | 3.522 | −594 |
| TC pelve/bacia, adulto, com contraste, sem sedação | 3.639 | 3.104 | −535 |
| TC tórax, adulto, com contraste, sem sedação | 2.350 | 1.978 | −372 |
| TC pescoço, adulto, com contraste, sem sedação | 479 | 403 | −76 |
| TC abdômen superior, adulto, sem contraste, sem sedação | 68 | 23 | −45 |
| TC pelve/bacia, adulto, sem contraste, sem sedação | 57 | 20 | −37 |
| TC tórax, adulto, sem contraste, sem sedação | 180 | 89 | −91 |
| TC crânio, adulto, sem contraste, sem sedação | 44 | 36 | −8 |
| Mamas bilateral | 12.950 | 12.874 | −76 |
| Transvaginal, antes da reserva do IEV | 9.294 | 9.251 | −43 |
| Abdômen total adulto | 9.895 | 10.042 | +147 |
| Abdômen total infantil | 452 | 439 | −13 |
| Parede abdominal | 3.304 | 3.318 | +14 |
| Abdômen superior adulto | 2.213 | 2.238 | +25 |
| Bolsa escrotal adulto | 700 | 713 | +13 |
| Bolsa escrotal infantil | 234 | 229 | −5 |
| Aparelho urinário adulto | 3.677 | 3.694 | +17 |
| Ultrassonografia renal | 72 | 72 | 0 |
| Aparelho urinário infantil | 276 | 278 | +2 |
| Próstata via abdominal | 2.969 | 2.981 | +12 |
| Tireoide adulto | 2.988 | 2.906 | −82 |
| Doppler de tireoide | 806 | 813 | +7 |
| Tireoide infantil | 60 | 61 | +1 |
| Doppler venoso MMII bilateral | 10.045 | 9.989 | −56 |
| Doppler arterial MMII bilateral | 1.800 | 1.799 | −1 |
| Partes moles | 3.140 | 3.081 | −59 |

**Implicação:** a carteira é uma simulação com estoque histórico, não uma medição atualizada em 11/11. Nas oito filas de TC acima, o estoque bruto passa de 10.933 para 9.175 pedidos: −1.758, aproximadamente **R$ 543.197,82** aos preços da carteira. Isso é uma comparação de estoque bruto por nome, não uma nova carteira elegível: a carteira antiga já retirava seis pedidos da pelve por recorte. Não descontei novamente a reserva de CID nem substituí o orçamento por esse número.

O Doppler de membros escolhido soma várias filas. Os 9.989 do venoso MMII não devem ser comparados sozinhos aos 12.043 da linha agregada. O mesmo cuidado vale para urinário adulto, que incorpora 72 pedidos de ultrassonografia renal, e tireoide adulto, que incorpora o Doppler de tireoide.

A coleta de 02/11 informa que a solicitação mais recente na base era de **28/10/2026**. A data de consulta e a atualidade do conteúdo são campos distintos.

## 4. Achados que impedem validar a carteira como definitiva

### 4.1. Doppler condicionado está no total principal

Em `Escolhidos!H27:I27`, 12.043 pedidos entram por R$ 1.392.291,23. A observação da própria linha exige aceitação da remuneração em dobro. A pendência local D-011 registra que, sem atendimento dessa condição, o exame fica fora.

A planilha mostra os cenários alternativos, portanto a aritmética não está escondida. O problema é chamar de escolhida/final uma base que já contém o item condicionado. A base sem autorização é o cenário de **R$ 8.362.281,81**; o cenário com remuneração em dobro precisa de fundamento assistencial e de faturamento, além da formalização da SES.

A Deliberação 46/2026 mantém as regras nacionais de registro e quantidade do SIGTAP. O teto de cinco registros por paciente/competência não demonstra, por si, que um bilateral autorize duas unidades. A documentação pública de auditoria reproduz a regra de independência em relação à quantidade de vasos. Não encontrei uma autorização específica para os dois registros deste objeto.

Fontes: [Deliberação 46/2026, arts. 2º e 4º](https://www.sinj.df.gov.br/sinj/Norma/08cdc67f1b9a46158271100a13d7d382/ses_cg_dlb_46_2026.html); [SES-MS, material de auditoria SIA/SUS](https://www.saude.ms.gov.br/wp-content/uploads/2020/12/SIA-SUS.pdf). A ficha local de outubro é a referência de competência consultada no acervo; não houve nova extração do pacote de novembro.

### 4.2. “Displasia do quadril não é ortopedia” está errado

O detalhe da articulação fecha corretamente em **4.557 pedidos**, dos quais 3.065 na janela de menos de 24 meses. Contudo, chamar todo esse conjunto de “não ortopedia” não se sustenta.

As três filas de quadril somam **283 pedidos, R$ 20.084,51**: USG QUADRIL, coxo-femoral esquerdo infantil e direito infantil. A própria planilha apresenta Q65 como CID importante. A [Nota Técnica SES-DF 21/2023, pp. 3–4](https://saude.df.gov.br/documents/37101/0/Nota%2BTecnica%2BN%C2%BA%2B21-2023%2B-%2BSES-SAIS-CATES-DUAEC-GESCIR%2B-%2BCriterios%2Bpara%2Bencaminhamento%2Bde%2Bpacientes%2Bpara%2Bos%2BServicos%2Bde%2BOrtopedia%2Be%2BTraumatologia%2Bda%2BAtencao.pdf/b44c9c51-0b86-4080-0b87-10e057e57a6f?t=1717676096814) inclui displasia do desenvolvimento do quadril em ortopedia infantil e trata Q65 e Q76.0 nos critérios de encaminhamento.

Isso **não prova** que esses pedidos sejam elegíveis ou estejam contratados na OCI específica do IEV. A correção necessária é trocar a justificativa clínica e conferir CID completo, composição, idade, finalidade e escopo do instrumento vigente. Filtrar por palavras do nome ou por idade mediana não resolve essa conferência. Também não se pode assumir que todas as partes moles sejam alheias à ortopedia.

### 4.3. Parede abdominal: preço confere, enquadramento continua pendente

A carteira inclui 3.304 pedidos no código do abdômen total, R$ 117,51, total de **R$ 388.253,04**. A presença da fila sob esse código no SISREG prova o cadastro observado, mas não homologa o faturamento do objeto contratado.

Se o código aceito passar a ser o de articulação/estruturas superficiais, a R$ 70,97, o impacto nesse estoque será **−R$ 153.768,16**. Se o item não for autorizado, todo o valor da linha fica sem sustentação. São alternativas diferentes, não perdas cumulativas. A pendência L-007 continua aberta no acervo.

### 4.4. “Pedidos novos” é crescimento líquido estimado, com recorte herdado

`Escolhidos!K5:L28` não contém contagem observada de novas solicitações futuras. O gerador aplica o saldo mensal estimado de entradas menos agendamentos, multiplicado por 12, quando positivo. O saldo elegível vem de um rateio por participação no estoque do código.

Há um problema adicional: a demanda usada foi calculada para uma carteira anterior. Exemplos:

- Abdômen superior: o recorte que origina o saldo tinha 5.031 pedidos elegíveis, incluindo angiografias; o estoque agora escolhido é 4.184.
- Pelve: o recorte anterior tinha 3.942 pedidos; a carteira atual usa 3.690.
- Tórax: o recorte anterior tinha 3.215; a carteira atual usa 2.530.
- Abdômen total: o crescimento do código é alocado ao adulto, enquanto o estoque desse código inclui parede e crianças.

Portanto, **R$ 1.361.258,12 não é demanda futura confirmada especificamente para os exames finais**. Refazer a projeção para o recorte atual, registrar o método de alocação e comparar cenários de oferta é necessário antes de usar a “Saída 2” para fechar o orçamento. O histórico recente também diverge da média anual: por exemplo, o estudo registra queda observada de mama apesar de saldo anual positivo.

### 4.5. “Não escolhidos” não é um inventário completo

O total dessa aba soma corretamente as linhas existentes, mas a lista não cobre tudo o que ficou fora. Na coleta bruta há, por exemplo:

- **379 pedidos de PET-CT**, código 02.06.01.009-5, dentro do universo tomografia; não estão no grupo medicina nuclear baseado em 02.08 nem em outro grupo da aba.
- **23 pedidos de órbitas/sela túrcica**, código 02.06.01.006-0.
- No código de face/seios, há 394 pedidos não emergenciais, mas a aba inclui apenas 139 com contraste. Sobram **255**, dos quais 195 constam como cone beam.

Não significa que esses exames devam entrar no plano ou que usem o mesmo equipamento. Significa que “Total de tudo o que ficou fora” é um título abrangente demais. É necessário classificar explicitamente os omitidos e manter grupos exclusivos e exaustivos. O valor de R$ 2,60 milhões é o das alternativas listadas como compatíveis, não uma garantia de contratação ou de capacidade técnica.

### 4.6. A conferência deixa 154 pedidos sem classificação explícita

Recalculando `Conferência!K5:K21`, os resíduos são: 2, 74, 4, 1, 5, 3, 2, 16, 27, 0, 0, 1, 7, 3, 5, 4 e 0. Soma: **154**. Não encontrei resíduo negativo no estado atual.

Parte dos resíduos é explicável pelo estudo anterior — 74 filas pequenas de Doppler, por exemplo. No código de pelve, seis pedidos já foram retirados por recorte na carteira, mas a coluna “Fora: IEV” está zerada. O resíduo de sete mistura essa exclusão com o restante. Assim, não é correto apresentar toda a coluna como algo sem explicação. Ela precisa de uma reconciliação por motivo e nome exato, e não apenas de uma igualdade entre totais.

### 4.7. O simulador de saídas não incorpora todas as dependências

Em `Saídas!C15`, a soma é apenas `SUMIFS` das linhas marcadas “sim”. Ela não verifica se a autorização do Doppler existe, se a reserva do IEV terminou ou se duas escolhas são compatíveis.

Exemplo concreto: a linha 2b informa que os pedidos novos do Doppler dobram se a saída 1 for usada, mas `C7=Escolhidos!L27` permanece em **R$ 303.360,64**. Somar 1 e 2b não calcula os **R$ 606.721,28** correspondentes à remuneração dobrada desses pedidos novos. A observação textual não altera a fórmula.

Antes de usar o simulador para escolher uma combinação, definir cenários completos com unidades, autorização, período e multiplicador consistentes. “Falta negativa” significa ultrapassar o orçamento, não fechamento exato.

### 4.8. Margem e capacidade são estimativas condicionais

Os percentuais reproduzem os custos adotados: médico US R$ 100/h, sala/aparelho R$ 5.500/mês, dois auxiliares de R$ 2.959, 168 horas produtivas/mês e R$ 3 de insumo por exame. TC: R$ 175 sem contraste e R$ 225 com contraste. Não validei esses preços com fornecedores.

Pelos próprios minutos da carteira, o estoque usa **24.432,83 horas de US** e **3.590,13 horas de TC**. Com 252 dias, 10h/dia e 80% de produtividade, isso equivale a 12,12 salas anuais de US, portanto ao menos 13 na conta agregada, e 59,36% da capacidade agregada de três tomógrafos. Isso não comprova a distribuição por polo, implantação, disponibilidade de especialistas ou reposição de faltas. Somar novos pedidos exige recalcular a capacidade. A margem total não é lucro nem validação de todos os custos do projeto.

### 4.9. Alguns fundamentos documentais permanecem sem validação

Não foi possível confirmar nesta revisão a vigência e o consumo atual da reserva de 4.000 transvaginais, a produção e o escopo contratual atual do IEV, o teor integral do Despacho SEI 219528407 citado no Resumo ou a afirmação de aproximadamente 1.357 TC a menos em 09/11. Essas afirmações não devem ser promovidas a fatos atuais apenas porque aparecem em uma observação. A nova consulta ao painel é uma verificação independente, em outra data e por nome.

## 5. Aspectos técnicos do arquivo

O XLSX contém 352 fórmulas, sem valores calculados armazenados no XML. Isso é compatível com um arquivo gerado para recálculo ao abrir, mas leitores que apenas extraem valores podem apresentar vazios. As contas deste parecer foram calculadas independentemente dos valores em cache. Não se está atestando o comportamento nativo de recálculo em Excel.

O Resumo usa “Tudo é fórmula sobre as outras abas”, embora a meta `B4` seja um valor fixo. Preços, margens, minutos e várias quantidades também são entradas fixas. Não é erro por si só; é necessário identificar fonte, competência e quais entradas devem ser atualizadas juntas. Mudanças de preço não propagam automaticamente por todos os valores fixos em “Não escolhidos” e “Da sobra à falta”.

A soma de procedimentos não equivale a pacientes únicos. A coleta original também alerta que a soma de pares nome × código pode exceder o total distinto do universo. Não houve auditoria individual de duplicidade por solicitação; nenhum dado pessoal de pacientes foi coletado nesta revisão.

## 6. Ajustes necessários antes de fechar a versão

1. Preservar a coluna de 02/11 como histórico e construir uma nova base elegível com mesma data, status, código, nome e recorte clínico para todo o objeto.
2. Usar como base o cenário sem itens cuja condição de inclusão não foi atendida. Manter Doppler simples, Doppler duplo autorizado e exclusão em cenários distintos.
3. Corrigir a justificativa sobre quadril infantil e demonstrar a separação entre a carteira e a OCI/contrato do IEV.
4. Confirmar o código de parede abdominal e o valor aplicável no instrumento.
5. Recalcular crescimento líquido e oferta para a composição final, sem herdar automaticamente os rateios anteriores.
6. Completar o inventário dos não escolhidos, fechar a reconciliação de 154 pedidos e corrigir dependências do simulador.
7. Confirmar custos e capacidade por polo, incluindo o cenário de demanda futura que vier a ser usado.
8. Abrir em Excel, recalcular e verificar os cenários antes de circulação formal.

**Resultado da revisão:** preços escolhidos e aritmética principal conferem com as fontes preservadas. Atualidade integral, elegibilidade, faturamento bilateral, não sobreposição e execução financeira/assistencial ainda não estão demonstrados. A planilha serve como estudo de alternativas, com as ressalvas e correções acima.
