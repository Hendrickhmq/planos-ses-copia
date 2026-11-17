from pathlib import Path
P=Path(__file__).resolve().parent
def replace_all(file,pairs):
 s=(P/file).read_text()
 for a,b in pairs:
  assert a in s,(file,a[:100])
  s=s.replace(a,b)
 (P/file).write_text(s)
replace_all('preparar.py',[
 ("'Ecocardiograma transtorácico','Prioridade para cotar, com incremento'","'Ecocardiograma transtorácico','Reservado à emenda de R$ 2 milhões de cardiologia'"),
 ("'Densitometria óssea','Complemento de carteira, com incremento'","'Densitometria óssea','Prioridade para cotar, com incremento'"),
 ("sources=[","sources=[\n ['D1','Decisão do usuário em 03/11/2026: reservar eco e eletro à emenda de R$ 2 milhões de cardiologia','Conversa deste estudo; eletro entendido como eletrocardiograma'],"),
])
replace_all('gerar_relatorio.py',[
 ('**Eu levaria duas carteiras para cotação: (A) cintilografia óssea + ecocardiograma adulto; (B) ecocardiograma adulto + densitometria.** A primeira prioriza um gargalo de medicina nuclear pouco atendido no registro consultado; a segunda tende a ter implantação mais simples e tem, na densitometria, a melhor diferença entre remuneração com incremento e preço local publicado entre as comparações obtidas. A escolha entre elas depende da oferta real dos prestadores, do enquadramento remuneratório e da lista que a SES encaminhará.',
 '**Eco e eletro ficam reservados à emenda de R$ 2 milhões de cardiologia, conforme orientação do usuário em 03/11/2026.** Eletro foi entendido como eletrocardiograma (ECG); já não compunha a carteira de imagem. Nenhuma meta ou orçamento dessa emenda de cardiologia foi fechado aqui.\n\n**Para os R$ 1,5 milhão, eu levaria duas carteiras para cotação: (A) cintilografia óssea + densitometria; (B) cintilografia óssea + RM de crânio.** A primeira combina o gargalo registrado da medicina nuclear com a comparação econômica local mais favorável da densitometria sob incremento. A segunda substitui parte dessa demanda por ressonância não ortopédica. A escolha depende das propostas integrais, da remuneração reconhecida e do encaminhamento da SES. Eco permanece nas tabelas apenas como referência para a emenda de cardiologia, com meta zero neste orçamento.'),
 ('a carteira proposta é adulta. Reservar','esse recorte é referência para a futura emenda de cardiologia, não para os R$ 1,5 milhão. Reservar'),
 ('### A — Cintilografia óssea + ecocardiograma adulto','### A — Cintilografia óssea + densitometria'),
 ("{portfolio([('0208050035',1000),('0205010032',3600)])}","{portfolio([('0208050035',1200),('0204060028',1900)])}"),
 ('Minha primeira carteira para testar com prestadores, se houver executor de medicina nuclear viável. As 1.000 cintilografias equivalem a 63,0% do estoque desse exame; não dependem de consumir toda a lista. Os 3.600 ecos cabem, em quantidade agregada, abaixo da fila adulta após reserva conservadora ao IEV. Não é necessário ampliar para pediatria para justificar o volume.',
 'Minha primeira carteira para testar com prestadores, se houver executor de medicina nuclear viável. As 1.200 cintilografias equivalem a 75,6% do estoque desse exame. As 1.900 densitometrias equivalem a 87,2% do estoque; é uma parcela elevada e exige confirmação do fluxo, pois a rede já realiza o exame. O volume não é demanda acessível garantida. As metas podem ser reduzidas ou redistribuídas por protocolo após pactuação, sem ocupar os pedidos da cardiologia.'),
 ('R$ 435.286,00 em assistência','R$ 333.878,00 em assistência'),
 ('### B — Ecocardiograma adulto + densitometria','### B — Cintilografia óssea + RM de crânio'),
 ("{portfolio([('0205010032',7000),('0204060028',1000)])}","{portfolio([('0208050035',1000),('0207010064',1150)])}"),
 ('É minha alternativa de implantação, se não houver rede de medicina nuclear, ou se a proposta integral da cintilografia não fechar. Os 7.000 ecos correspondem a aproximadamente 57,2% da fila adulta após reserva de 1.000; os 1.000 exames ósseos equivalem a 45,9% do estoque de densitometria. A tarifa incrementada do eco fica abaixo do preço público local de R$ 180: precisa de proposta de volume ou execução própria demonstrada. Não presumir que uma margem maior na densitometria autorize cobrar despesas ou manter quantidades artificiais em outro item.',
 'Alternativa se a oferta de densitometria encaminhável for menor ou se a proposta de RM for mais favorável. As 1.000 cintilografias equivalem a 63,0% do estoque; as 1.150 RM, a 81,4% do estoque agregado de crânio. Esse estoque inclui protocolos distintos: a regulação precisa confirmar a parte sem sedação que será realmente ofertada, o uso de contraste, o custo integral e as respectivas regras. Não tratar todas as 1.412 pendências como elegíveis ao mesmo protocolo. As duas carteiras continuam dependentes de executor nuclear; sem proposta viável, será preciso recompor a carteira de imagem, preservando eco e ECG para a cardiologia.'),
 ('Na carteira A, são 125 cintilografias e 450 ecos realizados por mês. A 20% de faltas, exigem pelo menos 157 e 563 tentativas mensais, arredondando cada modalidade. Com 30%: 179 e 643. Uma cintilografia com dose preparada tem perda econômica diferente de uma vaga de eco desocupada; a proposta deve disciplinar confirmação e responsabilidade pelas doses.',
 'Na carteira A, são 150 cintilografias e 237,5 densitometrias realizadas por mês, em média. A 20% de faltas, exigem pelo menos 188 e 297 tentativas mensais, arredondando cada modalidade. Com 30%: 215 e 340. Uma cintilografia com dose preparada tem perda econômica própria; a proposta deve disciplinar confirmação e responsabilidade pelas doses.'),
 ('Na carteira B, são 875 ecos e 125 densitometrias realizados por mês: ao menos 1.094 e 157 tentativas a 20% de faltas; 1.250 e 179 a 30%. Em 21 dias úteis, o eco exige cerca de 42 realizações/dia. Se o protocolo consumir 30 minutos e houver 8 horas efetivas/dia, isso equivale a pelo menos 3 salas-equipe simultâneas pelo volume realizado e 4 pelo tempo de agenda a 20% de faltas sem recuperação. É dimensionamento ilustrativo, não capacidade de executor comprovada. Na carteira A, o eco equivale a 2 salas-equipe nessa mesma hipótese. Uma sala física sem médico/equipamento disponível não é capacidade assistencial.',
 'Na carteira B, são 125 cintilografias e 143,75 RM realizadas por mês: ao menos 157 e 180 tentativas a 20% de faltas; 179 e 206 a 30%. Na carteira A, 21 dias úteis equivalem a aproximadamente 7,1 cintilografias e 11,3 densitometrias entregues por dia. Na B, a aproximadamente 6,0 cintilografias e 6,8 RM. São cargas para cotar; duração de protocolo, radiofármaco, disponibilidade do equipamento, equipe e perdas precisam ser demonstrados pelo executor. Uma sala física sem equipe/equipamento disponível não é capacidade assistencial.'),
 ('- Eco de estresse e próstata transretal:', '- Eco e ECG: reservados integralmente para a emenda de R$ 2 milhões de cardiologia; não usar para completar este envelope.\n- Eco de estresse e próstata transretal:'),
 ('de cintilografia óssea, eco adulto e densitometria','de cintilografia óssea, densitometria e RM de crânio'),
 ('A B é a alternativa operacional.', 'A B é a alternativa com RM de crânio. Eco e ECG ficam na emenda de R$ 2 milhões de cardiologia.'),
])
replace_all('gerar_planilha.mjs',[
 ("r.code==='0208050035'?1000:r.code==='0205010032'?3600:0","r.code==='0208050035'?1200:r.code==='0204060028'?1900:0"),
 ("['1 - cotar','Ecocardiograma adulto',null,null,null,null,'Fila adulta grande; reservar IEV; preco integral precisa fechar.']","['Reservado - cardiologia','Ecocardiograma adulto',null,null,null,null,'Meta zero aqui. Eco e ECG reservados a emenda de R$ 2 milhoes de cardiologia.']"),
 ("['2 - complemento','Densitometria'","['1 - cotar','Densitometria'"),
 ("1.000 cintilografias osseas + 3.600 ecos adultos","1.200 cintilografias osseas + 1.900 densitometrias"),
 ("7.000 ecos adultos + 1.000 densitometrias","1.000 cintilografias osseas + 1.150 RM de cranio"),
 ("Quantidade nao e compromisso de contratacao. Priorizar a lista adulta; nao usar pediatria para completar valor.","Quantidade nao e compromisso. Eco e ECG reservados a emenda de R$ 2 milhoes de cardiologia."),
 ("435286","333878"),("914714","1016122"),("1340500","1335512"),("9500","14488"),
 ("val('Modelo','C19',1001);expect('Modelo','B13',1341263.96);val('Modelo','C19',1000);","val('Modelo','C19',1201);expect('Modelo','B13',1336275.96);val('Modelo','C19',1200);"),
 ("val('Modelo','G19',800);expect('Modelo','I19',-36040);val('Modelo','G20',100);expect('Modelo','B16',30500);","val('Modelo','G19',800);expect('Modelo','I19',-43248);val('Modelo','G21',100);expect('Modelo','B16',35512);"),
 ("expect('Modelo','K20',643)","expect('Modelo','K21',340)"),
 ("val('Modelo','B5',160000);expect('Modelo','B15',-500);","val('Modelo','B5',170000);expect('Modelo','B15',-5512);"),
 ("['G19','G20']","['G19','G21']"),
])
print('Geradores atualizados: eco e ECG reservados à cardiologia de R$ 2 milhões.')
