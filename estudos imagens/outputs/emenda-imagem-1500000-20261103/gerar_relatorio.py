from pathlib import Path
import json
P=Path(__file__).resolve().parent
d=json.loads((P/'dados_estudo.json').read_text());rs=d['records'];ix={r['code']:r for r in rs}
def br(n,digits=0): return f'{n:,.{digits}f}'.replace(',','@').replace('.',',').replace('@','.')
def cash(n): return 'R$ '+br(n,2)
def table(head,rows): return '| '+' | '.join(head)+' |\n|'+'|'.join(['---']*len(head))+'|\n'+'\n'.join('| '+' | '.join(str(x) for x in row)+' |' for row in rows)+'\n'
price_table=table(['Exame','SIGTAP base','Incremento 38.01 em 10/2026','Base + incremento¹','Candanga oficial'],[[r['name'],cash(r['base']),br(r['increment']*100,0)+'%' if r['increment'] is not None else 'não localizado',cash(r['with_increment']) if r['increment'] is not None else '—',cash(r['candanga'])] for r in rs[:14]])
demand_table=table(['Exame','Pedidos pendentes','Entradas 12m²','Agendamentos 12m','Realizados 12m','Entradas − realizados/mês³'],[[r['name'],br(r['stock']),br(r['entries']),br(r['scheduled']),br(r['performed']),br((r['entries']-r['performed'])/12,1)] for r in rs[:14]])
econ=table(['Exame','Preço público de referência','Cobertura pela base','Cobertura com incremento','Leitura'],[
 ['Densitometria',cash(77.99)+' a partir de; Taguatinga',br(55.1/77.99*100,1)+'%',br(220.4/77.99*100,1)+'%','É a comparação local mais favorável com incremento; validar composição'],
 ['Ecocardiograma',cash(180)+'; Minha Clínica/DF',br(67.86/180*100,1)+'%',br(160.15/180*100,1)+'%','Precisa negociar abaixo do varejo ou demonstrar custo próprio menor'],
 ['Mamografia bilateral',cash(188.48)+' a partir de; Taguatinga',br(45/188.48*100,1)+'%',br(99.9/188.48*100,1)+'%','Mesmo com incremento, preço publicado supera a remuneração'],
 ['RM de crânio',cash(400)+' a partir de; rede Brasília',br(268.75/400*100,1)+'%',br(499.88/400*100,1)+'%','Comparação fraca: unidade/protocolo não definidos; sem margem contratada'],
 ['Cintilografia óssea',cash(464)+'; referência exploratória sem cidade confirmada',br(190.99/464*100,1)+'%',br(763.96/464*100,1)+'%','Sinal para cotar no DF; não é comprovação de custo local'],
 ['Miocárdica, estresse + repouso',cash(1440)+'; pacote exploratório sem cidade confirmada',br((408.52+383.07)/1440*100,1)+'%',br((898.74+881.06)/1440*100,1)+'%','Só comparar pacote completo; pode exigir duas autorizações/procedimentos'],
])
def portfolio(rows):
 out=[]
 for code,q in rows:
  r=ix[code];out.append([r['name'],br(q),cash(r['with_increment']),cash(q*r['with_increment'])])
 total=sum(ix[c]['with_increment']*q for c,q in rows)
 return table(['Exame','Meta proposta','Unitário condicionado','Valor assistencial'],out)+f'\nAssistência: **{cash(total)}**. Apoio hipotético: **R$ 150.000,00**. Total: **{cash(total+150000)}**. Saldo não alocado: **{cash(1500000-total-150000)}**.\n'
text=f'''# Estudo de escolha da carteira — emenda federal de bancada de R$ 1,5 milhão

**Controle interno para decisão. Data: 03/11/2026.** Origem federal de bancada confirmada pelo usuário nesta conversa. Objeto considerado: contratação de exames de imagem. O número da emenda, o exercício orçamentário, o início da execução e os executores ainda não foram informados. Este estudo não altera os planos anteriores e não constitui plano de trabalho aprovado nem cotação aceita.

## 1. Minha recomendação

**Eco e eletro ficam reservados à emenda de R$ 2 milhões de cardiologia, conforme orientação do usuário em 03/11/2026.** Eletro foi entendido como eletrocardiograma (ECG); já não compunha a carteira de imagem. Nenhuma meta ou orçamento dessa emenda de cardiologia foi fechado aqui.

**Para os R$ 1,5 milhão, eu levaria duas carteiras para cotação: (A) cintilografia óssea + densitometria; (B) cintilografia óssea + RM de crânio.** A primeira combina o gargalo registrado da medicina nuclear com a comparação econômica local mais favorável da densitometria sob incremento. A segunda substitui parte dessa demanda por ressonância não ortopédica. A escolha depende das propostas integrais, da remuneração reconhecida e do encaminhamento da SES. Eco permanece nas tabelas apenas como referência para a emenda de cardiologia, com meta zero neste orçamento.

**Nenhuma das duas está demonstrada como viável ao SIGTAP básico.** O atrativo depende de reconhecer formalmente os incrementos pertinentes no instrumento, no executor e na competência de execução, ou de conseguir custo integral inferior à tarifa básica. Não recomendo fechar a carteira usando a Candanga como receita desta emenda federal. Também não recomendo assumir que a habilitação 38.01, por si só, converte todo convênio em pagamento incrementado.

A ordem prática é: confirmar remuneração aplicável e período; obter propostas integrais; confirmar encaminhamento regulado; então fechar quantidades. Há números concretos para negociar neste estudo, mas não há proposta de prestador que permita afirmar lucro, sobra financeira ou execução assegurada. A ausência de proposta não significa que seja impossível negociar abaixo do varejo.

## 2. O que já escolhemos e o que o IEV alcança

**Plano 4 / carteira 1 em estudo:** {br(d['plan4_total'])} exames, com 17 códigos. A revisão de 02/11 mantém US de mamas, Doppler vascular, abdômen total/superior e parede, urinário, tireoide, próstata abdominal, bolsa escrotal, pélvica, transfontanela, transvaginal com reserva ao IEV, e protocolos de TC de tórax, abdômen, pelve, pescoço, crânio e face. São escolhas de planejamento: não as apresento como exames já realizados ou contratação definitivamente aprovada.

**A antiga ideia da emenda de R$ 1,5 milhão não pode ser reaproveitada inteira.** Bolsa escrotal, pélvica, transfontanela e TC de cabeça/pescoço/face já se cruzam com a carteira 1. Um protocolo ausente daquela carteira só poderá entrar depois de conferência nominal; compartilhar código não torna todos os protocolos iguais. A nova emenda deve acrescentar capacidade e públicos definidos, sem disputar os mesmos pedidos.

{table(['Cobertura no acervo aprovado do IEV','Quantidade contratada','Consequência para esta escolha'],[
 ['OCI ortopedia com US', '19.070 OCI', 'Manter US de articulação fora da nova carteira inicial'],
 ['OCI ortopedia com RM', '28.130 OCI', 'Evitar RM de coluna e membros inicialmente; não confundir OCI com RM concluída'],
 ['OCI ortopedia com TC', '539 OCI', 'Não repetir TC ortopédica sem separação de pedidos'],
 ['GIN1, com transvaginal obrigatória', '3.218 OCI; reserva de 4.000 transvaginais no estudo anterior', 'Preservar a reserva; execução baixa não libera automaticamente os pedidos'],
 ['OCI insuficiência cardíaca', '1.000 OCI; eco compatível', 'Planejar reserva conservadora de até 1.000 pedidos, a pactuar'],
 ['OCI coronariana', '900 OCI; eco de estresse obrigatório', 'Eco de estresse fica fora da carteira inicial'],
 ['OCI próstata', '1.015 OCI; US transretal obrigatório', 'Não priorizar US transretal nesta emenda'],
 ])}

As OCI aprovadas do IEV somam 122.895 nos três convênios do acervo. Esse total não é número de exames nem prova de produção concluída. As consultas registradas até outubro tampouco provam OCI encerrada/APAC aprovada. Mamografia, densitometria e cintilografia óssea não foram identificadas como componentes cobertos nos instrumentos aprovados mapeados; isso não certifica ausência de qualquer contrato mais recente da SES.

**A separação é pelo pedido e pelo fluxo pactuado, não apenas pelo CID.** Não usar o CID para declarar que toda a parcela restante está automaticamente livre. No eco, a reserva de 1.000 é premissa conservadora de planejamento, não medição de pacientes já vinculados. Das 14.602 pendências do código, 13.236 são da principal fila adulta e 1.332 da infantil; esse recorte é referência para a futura emenda de cardiologia, não para os R$ 1,5 milhão. Reservar 1.000 na fila adulta deixa 12.236 pedidos como aproximação inicial, sujeita à validação individual. A lista infantil pede equipe e orçamento próprios.

## 3. O que a rede já atende — e onde aparece o gargalo

Fotografia: recarga de 02/11/2026, 10h31; solicitações mais recentes até 28/10/2026. Histórico comparável: **outubro/2025 a setembro/2026**, os 12 meses fechados anteriores ao mês da última solicitação. Não usei outubro parcial como mês cheio.

{demand_table}

² Entradas são a medida agregada reconstruída pela coleta como abertas + agendadas. Sem chave longitudinal, não comprova pedidos novos únicos e não permite reconstruir todos os destinos. ³ Diferença aritmética para comparação operacional; não é crescimento real observado do estoque, pois faltam reconciliação longitudinal, baixas e cancelamentos. As projeções abaixo são condicionais.

**Esses realizados são da rede regulada registrada no painel, incluindo eventuais prestadores complementares; não são uma medição isolada da produção própria da SES.** Para estes novos candidatos não encontrei uma separação completa e atual por executor que autorize afirmar quanto é de cada hospital/clínica. Não atribuo a produção inteira à rede própria e não a desconto novamente como se fosse de outro convênio.

O eco combina estoque alto com diferença relevante entre entradas e realizações. A cintilografia óssea tem 1.587 pendências e 745 realizações registradas no ano, frente a 2.487 entradas; é um bom candidato a oferta adicional. A perfusão miocárdica também tem grande descompasso. Mamografia e densitometria já têm atendimento relevante: a justificativa deve mostrar oferta adicional e acesso territorial, não simplesmente dizer que a SES não faz. RM de crânio e pelve têm mais agendamentos que entradas, mas menos realizações que entradas: **agenda disponível não equivale a exame entregue**. Em PET-CT, apenas 113 dos 578 agendamentos aparecem realizados; há situações ainda não encerradas e possível problema de atualização. Isso pede validação, não autoriza concluir que todos os demais pacientes ficaram sem exame.

## 4. Remuneração: três referências diferentes

{price_table}

¹ Base + incremento é cálculo paramétrico do SIGTAP 10/2026 para habilitação 38.01, arredondado por unidade a dois decimais. A unidade final deve bater com o processamento e com o instrumento. Não some SA, SH e SP de modalidades diferentes. Os percentuais foram lidos na relação oficial `rl_procedimento_incremento`, não inferidos da Candanga. A renal dinâmica não teve incremento 38.01 localizado no pacote; não recebeu incremento por analogia.

**SIGTAP básico:** referência prudente enquanto o reconhecimento específico não for confirmado. A existência de incremento para determinada habilitação não demonstra que o executor o tem nem que ele é aplicável ao convênio de bancada.

**Incremento federal:** as Portarias SAES 4.282/2026 e 4.694/2026 e o pacote de outubro mostram parâmetros próprios de componentes do Agora Tem Especialistas. A 4.694 condiciona a execução às habilitações, prevê registro específico e efeitos até **31/12/2026**. A modalidade de créditos financeiros é uma forma específica de compensação tributária; não deve ser tratada como dinheiro adicional recebido automaticamente pelo convênio. Para usar os parâmetros em convênio de emenda, a SES precisa reconhecer a via, o valor, a habilitação do estabelecimento e a segregação da produção, sem faturar a mesma realização também em FAEC/crédito financeiro. Para execução em 2027, **não foi comprovada neste estudo a continuidade normativa do incremento**. A planilha abre com o valor básico e o reconhecimento desativado.

**Candanga:** usei o Valor Tabela SUS Candanga do Anexo oficial. O README antigo da biblioteca ainda fala do Valor Máximo da análise comparativa de agosto; esse valor preliminar não é a fonte desta conta. A Candanga já contém a composição prevista: não somar novamente o básico nem o incremento. A Lei DF 7.897/2026, art. 4º §1º, e a Deliberação 46/2026, art. 5º, atribuem a complementação a recursos próprios distritais. A GM/MS 12.116/2026 permite nacionalmente remuneração diferenciada inclusive com recursos federais, mas não prova uma adoção diferente pela SES-DF neste caso. Assim, a comparação Candanga serve para negociação e eventual cofinanciamento distrital formal, sem lançar esse complemento como disponível nos R$ 1,5 milhão.

O exercício da emenda também precisa ser identificado. Não aplicar automaticamente regra de emenda de 2027 a uma de exercício anterior; o estudo não inventa número de portaria de transferência, ação orçamentária nem prazo de vigência do instrumento.

## 5. Economia: o que parece pagar bem e o que ainda não está provado

{econ}

Cobertura = tarifa ÷ preço público de referência. Não é margem, custo do prestador nem desconto contratual garantido. Valores “a partir de” podem subir com protocolo, contraste ou unidade. A densitometria exige confirmar coluna/fêmur e laudo; não remunerar segmentos como unidades extras sem regra. O eco precisa confirmar que o serviço publicado corresponde ao transtorácico proposto. Na mamografia, a indicação diagnóstica não pode ser faturada como rastreamento apenas para usar determinada tarifa: há 182 pedidos com nome diagnóstico sob o código de rastreamento no inventário, que precisam ser saneados.

Para referências exploratórias do Exame Social, a listagem apresenta estabelecimentos, mas a cidade e o endereço não ficaram confirmados. Elas ficam fora de qualquer conclusão de custo local. Não usei preço de PET-CT com PSMA para estimar FDG, nem preço de consulta para estimar exame. Não há neste estudo preço mínimo/mediana do mercado DF representativo para medicina nuclear: ainda falta cotação comparável. As referências públicas foram consultadas em 03/11/2026; não substituem proposta escrita com validade.

**Limite econômico para cotar, sem impor percentual de negociação:** para um contrato por exame entregue, o preço integral do prestador mais apoio, tributos eventualmente incidentes e perdas não recuperáveis precisa caber na remuneração reconhecida. A planilha permite informar esses custos. Com uma retenção meramente ilustrativa de 10% da tarifa para custos não assistenciais, os limites integrais do prestador seriam R$ 687,56 na cintilografia óssea, R$ 144,14 no eco, R$ 198,36 na densitometria e R$ 449,89 na RM de crânio com incremento. Na base, seriam R$ 171,89, R$ 61,07, R$ 49,59 e R$ 241,88. Esses valores não são preços obtidos, teto aprovado ou promessa de margem. Não somar a retenção ilustrativa ao apoio orçamentário como se fossem duas despesas obrigatórias.

Se a execução for própria, incluir equipamento/locação, médico e laudo, técnico, enfermagem quando indicada, manutenção, licença, processamento de imagens, insumos, atendimento e encargos. Em medicina nuclear, incluir radiofármaco, perdas de dose por falta, preparo, aquisição de imagens, laudo e autorizações sanitárias/radioproteção aplicáveis. Se a cotação integral já inclui esses componentes, não duplicá-los no apoio. O recurso é de custeio: não o tratei como aquisição de equipamento.

## 6. Carteiras concretas para comparar

As metas abaixo são **hipóteses de negociação com incremento reconhecido**, sem sedação e com indicação/protocolo definidos. O apoio de R$ 150 mil é uma reserva hipotética de 10% do envelope, escolhida para comparação; o orçamento final deve sair de postos, quantidades, preços e escopo reais. Não é rubrica aprovada nem direito de reter 10%. Saldo fica não alocado; não foi criada despesa para completar R$ 1,5 milhão.

### A — Cintilografia óssea + densitometria

{portfolio([('0208050035',1200),('0204060028',1900)])}

Minha primeira carteira para testar com prestadores, se houver executor de medicina nuclear viável. As 1.200 cintilografias equivalem a 75,6% do estoque desse exame. As 1.900 densitometrias equivalem a 87,2% do estoque; é uma parcela elevada e exige confirmação do fluxo, pois a rede já realiza o exame. O volume não é demanda acessível garantida. As metas podem ser reduzidas ou redistribuídas por protocolo após pactuação, sem ocupar os pedidos da cardiologia.

Ao básico, as mesmas quantidades somariam apenas **R$ 333.878,00 em assistência**. Portanto, não se pode manter o custo de execução calculado pelo incremento e presumir que a base paga a mesma coisa. Se o prestador aceitar custo integral compatível com o básico, a carteira pode ser reavaliada por esse valor, mas isso ainda não está comprovado.

### B — Cintilografia óssea + RM de crânio

{portfolio([('0208050035',1000),('0207010064',1150)])}

Alternativa se a oferta de densitometria encaminhável for menor ou se a proposta de RM for mais favorável. As 1.000 cintilografias equivalem a 63,0% do estoque; as 1.150 RM, a 81,4% do estoque agregado de crânio. Esse estoque inclui protocolos distintos: a regulação precisa confirmar a parte sem sedação que será realmente ofertada, o uso de contraste, o custo integral e as respectivas regras. Não tratar todas as 1.412 pendências como elegíveis ao mesmo protocolo. As duas carteiras continuam dependentes de executor nuclear; sem proposta viável, será preciso recompor a carteira de imagem, preservando eco e ECG para a cardiologia.

### C — Ressonância não ortopédica como alternativa

Cotaria crânio, abdômen e colangiorressonância por protocolo, separando contraste e sedação. Evitaria iniciar com coluna/membros, já alcançados pelo IEV. A RM de pelve precisa de separação entre investigação não ortopédica e demanda ortopédica. A remuneração paramétrica de R$ 499,88 é atraente frente a um anúncio a partir de R$ 400, mas a diferença de R$ 99,88 ainda precisa pagar apoio e riscos, e o anúncio não identifica a unidade/protocolo. Não considero isso margem comprovada. A fila de crânio tem 1.412 pedidos no conjunto; uma meta de 2.000 exigiria entradas/encaminhamento ao longo da execução, além de separar os protocolos realmente ofertados.

### D — Somente SIGTAP básico, sem incremento e sem complemento distrital

Não há carteira demonstrada como economicamente positiva pelos preços pesquisados. Densitometria, mamografia, eco e RM têm tarifas básicas inferiores às referências locais publicadas. Cintilografia e PET-CT demandam propostas próprias. **Minha recomendação neste cenário é não assumir uma obrigação de 1,5 milhão com margem imaginada.** A alternativa é obter proposta compatível com o básico, demonstrar custo próprio ou negociar formalmente uma fonte remuneratória admitida; o orçamento fechado vem depois dessa definição.

## 7. Capacidade, faltas e prazo

Horizonte de comparação: 8 meses, hipótese herdada apenas para comparar, ainda não pactuada. Com 20% de faltas e reposições/reagendamentos permitidos, tentativas = realizações ÷ 0,8. Faltas aumentam tentativas e ocupação, sem significar automaticamente novos pedidos ou pessoas.

Na carteira A, são 150 cintilografias e 237,5 densitometrias realizadas por mês, em média. A 20% de faltas, exigem pelo menos 188 e 297 tentativas mensais, arredondando cada modalidade. Com 30%: 215 e 340. Uma cintilografia com dose preparada tem perda econômica própria; a proposta deve disciplinar confirmação e responsabilidade pelas doses.

Na carteira B, são 125 cintilografias e 143,75 RM realizadas por mês: ao menos 157 e 180 tentativas a 20% de faltas; 179 e 206 a 30%. Na carteira A, 21 dias úteis equivalem a aproximadamente 7,1 cintilografias e 11,3 densitometrias entregues por dia. Na B, a aproximadamente 6,0 cintilografias e 6,8 RM. São cargas para cotar; duração de protocolo, radiofármaco, disponibilidade do equipamento, equipe e perdas precisam ser demonstrados pelo executor. Uma sala física sem equipe/equipamento disponível não é capacidade assistencial.

As faltas históricas calculadas como faltas/(realizados+faltas) são cerca de 25,8% no eco, 27,1% na densitometria e 45,5% na cintilografia óssea. Não confundir com faltas/agendamentos. Usar 20% exige operação melhor que o histórico; a planilha deixa esse fator editável. Não prometi recuperar vagas nem zerar filas.

## 8. Como distinguir oferta adicional de transferência da rede

Na planilha, a aproximação de disponibilidade no prazo é estoque − reserva + (entradas − realizações registradas) × meses/12. Não é demanda garantida, pessoas únicas nem previsão real da fila. Serve para evitar metas evidentemente maiores que o recorte; precisa de atualização na data de início. Não supõe transferência de toda a agenda da SES para o convênio. Se a rede reduzir sua oferta para encaminhar os mesmos pacientes ao novo prestador, parte da meta será transferência, e não aumento líquido de produção.

Antes de fechar, pactuar com a regulação quantitativo mensal adulto, região, protocolo e identificação dos pedidos; manter reserva dos pacientes efetivamente vinculados ao IEV; definir como a oferta própria e outros contratos serão preservados. Não adicionar o teto das OCI do IEV ao realizado histórico da rede como se fossem dois fluxos independentes. A execução baixa histórica do IEV não extingue seu objeto. Toda redistribuição deve ser expressa.

O início em 2027 traz duas mudanças: a fila poderá ser outra e a autorização normativa do incremento de 2026 pode não continuar. Para medir espera, registrar linha de base por protocolo, mediana/P90 e resultado após execução, sem inventar agora uma meta percentual. Contar separadamente exames entregues/laudados, vagas, tentativas, faltas, reagendamentos, baixas e encaminhamentos.

## 9. O que eu descartaria ou deixaria para depois

- Repetição geral de US/TC da carteira 1: pouca diferenciação e risco de disputar pedidos.
- US de articulação e RM de coluna/membros: sobreposição com IEV; partes moles continuam excluídas pela decisão anterior.
- Eco e ECG: reservados integralmente para a emenda de R$ 2 milhões de cardiologia; não usar para completar este envelope.
- Eco de estresse e próstata transretal: já alcançados por OCI aprovadas, demanda/estrutura distintas.
- Mamografia como eixo do orçamento: relevância assistencial existe, mas remuneração versus preço publicado ficou fraca; confirmar necessidade por região e integrar retorno de achados/SISCAN.
- PET-CT como primeira escolha: tarifa alta não demonstra margem; faltam proposta FDG comparável, fluxo e validação dos registros de realização. Não há incremento 38.01 localizado para esse código.
- Cintilografia miocárdica: boa necessidade aparente, mas pacote e número de pacientes únicos não estão medidos. Estresse e repouso podem ser duas etapas do mesmo cuidado, não duas pessoas.
- Renal/paratireoides: complementos de menor volume, com protocolo e custo próprios. Na renal dinâmica não aplicar os 300% da renal estática por semelhança de nome.
- Obstétrica: pedido antigo pode já não corresponder a gestação atual; não comprar o estoque sem revalidação clínica e regulatória.
- OCT, endoscopias e imagem odontológica: podem justificar estudo específico, mas não receberam aqui carteira fechada nem equivalência tarifária improvisada. A base ampla anterior tinha 54.227 pedidos de endoscopia em 29/10; é outra operação, com preparo, sedação e custos específicos, e não deve ser misturada ao recorte de 02/11 como se fosse a mesma coleta.

## 10. Pendências que realmente mudam a escolha

1. **SES/SUCONV e área de faturamento:** número/exercício da emenda, instrumento, competência e valor por código; cabimento do parâmetro incrementado neste convênio e sua continuidade no período real. Se 2027, obter fundamento vigente e não apenas expectativa de prorrogação.
2. **Executor:** CNES da unidade que fará o exame, habilitação efetivamente válida, equipe, equipamentos e capacidade mensal; formalizar vínculo e responsabilidades assistenciais. Nenhuma habilitação antiga presumida foi tratada como atual.
3. **Prestadores:** propostas integrais comparáveis de cintilografia óssea, densitometria e RM de crânio, incluindo laudo, insumos, impostos quando aplicáveis, prazos, faltas, repetição técnica e responsabilidade por radiofármaco. Pedir alternativas com volume mensal e custo próprio quando pertinente. Não foram enviados contatos ou pedidos de orçamento.
4. **Regulação:** lista elegível e encaminhamento mensal por território; reserva nominal ao IEV; mapa atualizado dos contratos concorrentes. O acervo aprovado não é cadastro exaustivo de todos os instrumentos vigentes.
5. **Apoio:** orçamento por posto/serviço, sem duplicar o que vier na cotação assistencial; fluxo de desembolso e capital de giro. Orçamento autorizado não é recebimento em caixa imediato.

**Decisão recomendada hoje:** avançar na comparação e cotação das carteiras A e B, priorizando a A se houver executor nuclear e preço integral viável. A B é a alternativa com RM de crânio. Eco e ECG ficam na emenda de R$ 2 milhões de cardiologia. A lista final fica condicionada ao valor reconhecido, às propostas e ao fluxo de pacientes; não há base para prometer que a emenda já está economicamente fechada.

## Fontes e rastreabilidade

As fontes locais preservadas e as páginas públicas estão identificadas abaixo. Arquivos auxiliares guardam os recortes e a conferência das séries; a planilha contém o modelo editável. Consulta pública em 03/11/2026; bases assistenciais com datas anteriores explicitadas.

'''
for id,label,url in d['sources']:
 text+=f'- **{id}** — {label}. [Abrir fonte]({url.replace(" ","%20")}).\n'
(P/'Estudo da emenda de 1,5 milhao.md').write_text(text)
print('Relatório:',len(text.split()),'palavras')
