from pathlib import Path
import json, math
from openpyxl import load_workbook
P=Path(__file__).resolve().parents[1]
d=json.loads((P/'dados_plano_20_salas.json').read_text())
w=load_workbook(P/'Carteira 1 - plano em 20 salas.xlsx',data_only=True)
checks=0
def eq(a,b,tol=1e-7):
    global checks
    assert abs(a-b)<tol,(a,b)
    checks+=1
n=w['Plano em 20 salas'];a=w['Agenda e absenteismo']
eq(n['C18'].value,20);eq(n['D18'].value,64915)
eq(a['B6'].value,8);eq(a['B7'].value,21);eq(a['B8'].value,10)
f=.2;r=.8;lost=f*(1-r)/(1-f*r)
eq(a['B12'].value,lost)
for j,p in enumerate(d['polos']):
    row=j+12;rs=[x for x in d['records'] if x['polo']==p]
    h=sum(x['horas'] for x in rs);q=sum(x['meta'] for x in rs);salas=d['salas'][j]
    eq(n[f'D{row}'].value,q);eq(n[f'G{row}'].value,h/salas)
    eq(n[f'H{row}'].value,h/(salas*8*21*10*.8*.8))
    # Método independente: duração de todas as tentativas menos tempo recuperado.
    agenda=h/(1-f)*(1-f*r)
    eq(n[f'I{row}'].value,agenda/(salas*8*21*10*.8))
    assert agenda<=salas*8*21*10*.8
hours=sum(x['horas'] for x in d['records'])
eq(hours,23906.166666666668)
eq(hours-20*8*21*10*.8*.8,2402.166666666668)
lim=max(sum(x['horas'] for x in d['records'] if x['polo']==p)/s for p,s in zip(d['polos'],d['salas']))
eq(a['C20'].value,(1-1344*.8/lim)/.2)
for row,ff in zip(range(20,25),[.2,.25,.3,.4,.43]):
    eq(a[f'B{row}'].value,ff*(1-r)/(1-ff*r))
    eq(a[f'C{row}'].value,max(0,(1-1344*(1-ff)/lim)/ff))
for row,months,rec in [(25,8,0),(26,8,.8),(27,10,0),(28,7,.8)]:
    required=lim/(1-f)*(1-f*rec)
    eq(n[f'F{row}'].value,required/(months*21*10*.8))
assert n['H25'].value=='Não cabe' and n['H26'].value=='Cabe nas premissas'
assert n['H27'].value=='Cabe nas premissas' and n['H28'].value=='Não cabe'
e=w['Exames e metas'];eq(e['F24'].value,79219);eq(e['J24'].value,10636506.41,.005)
for i,c in enumerate(sorted(d['codes'],key=lambda x:x['codigo']),7):
    eq(e[f'F{i}'].value,c['meta']);eq(e[f'E{i}'].value,c['estoque'])
    eq(e[f'H{i}'].value,math.ceil(c['meta']/.8))
ps=w['Filas atendidas'];eq(ps['E54'].value,79219)
reg=w['Encaminhamento SES'];eq(reg['C25'].value,79219);eq(reg['G25'].value,348);eq(reg['H25'].value,0)
errors=[(s.title,c.coordinate,c.value) for s in w for row in s for c in row if c.data_type=='e']
assert not errors,errors
result={'conferencias':checks,'abas':w.sheetnames,'salas':20,'dias_uteis_mes':21,'horas_dia':10,'sabados':False,'meta':79219,'perda_liquida_com_reposicao_meta':lost,'recuperacao_minima_20pct_faltas':a['C20'].value,'erros':errors}
(P/'verificacao/plano20_conferencia_independente.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
report='''# Carteira 1 em 20 salas — proposta de execução

A nova apresentação é **Carteira 1 - plano em 20 salas.xlsx**, com cinco abas: Plano em 20 salas, Exames e metas, Filas atendidas, Agenda e absenteismo e Encaminhamento SES. As planilhas anteriores permanecem preservadas.

O usuário definiu **até 20 salas, apenas dias úteis e 10 horas por dia**. A referência continua sendo oito meses, com 21 dias úteis por mês e 80% do tempo disponível para agenda. As 20 salas são de ultrassom; a tomografia exige rede própria de equipamentos confirmada separadamente. Não foram reduzidos tempos nem revisados custos.

## Arranjo escolhido

| Região de origem | Execução | Salas US | Meta US |
|---|---|---:|---:|
| Central e Centro-Sul | Asa Sul | 3 | 10.844 |
| Leste | São Sebastião | 3 | 9.743 |
| Norte | Sobradinho | 2 | 4.690 |
| Oeste | Ceilândia | 1 | 3.267 |
| Sudoeste | Samambaia | 6 | 21.039 |
| Sul | Gama | 5 | 15.332 |
| Total | | 20 | 64.915 |

A distribuição é a única que minimiza a maior carga por sala entre 11.628 combinações inteiras de 20 salas nos seis polos, antes de remanejar demanda. Depois, 504 Dopplers venosos bilaterais de MMII da região Norte passam a ser executados na Asa Sul. Isso equilibra a carga por sala de Norte e Central, preservando 40 minutos por exame. A origem desses 504 pedidos continua sendo Norte. O deslocamento depende da regulação. O rateio territorial permanece uma aproximação com base nas participações de 15/09, não medição atual por protocolo.

## Carteira mantida e filas

Mantidos 79.219 exames: 64.915 US e 14.304 TC, em 17 códigos e 47 filas com meta, por R$ 10.636.506,41 de procedimentos. A lista completa por nome exato está em Filas atendidas, com pedidos na coleta, elegibilidade estimada, meta, complemento ao estoque, tempo por exame e tentativas de agenda. Exames e metas consolida esses dados por código.

O estoque disponível é o da recarga de 02/11/2026 às 10h31, com solicitações até 28/10. Não houve consulta nova ao painel. Fila total do código e fila elegível são medidas distintas; a total contém protocolos excluídos. Devolvidas ficam separadas. Pedidos não equivalem a pessoas únicas, e reserva ou filtro estimado pode produzir quantidades fracionárias de modelagem. A SES pode atender parte do estoque antes da execução.

A parede abdominal permanece com 3.304 exames e precisa de confirmação de enquadramento e faturamento da SES. Angio coronária e articulação ficam excluídas, com 4.000 transvaginais reservadas ao IEV. Permanecem as pendências de elegibilidade explicitadas no estudo completo.

## Como cumprir em oito meses

**20 salas com 20% de faltas e sem recuperação de vagas não comportam toda a carteira em oito meses.** Faltam pelo menos 2.402 horas assistenciais de US no agregado. No arranjo proposto, o polo limitante ficaria com carga de 117%.

Para manter a carteira em oito meses, é necessário comprovar recuperação de tempo de sala. Com 20% de faltas brutas, o mínimo no polo limitante é recuperar 72,7% do tempo das tentativas frustradas. A meta operacional proposta é recuperar 80%, o que corresponde a perda líquida de 4,8% e carga máxima de 98,3%. A folga é pequena. Essa recuperação é hipótese operacional, não resultado já observado.

O cálculo distingue tentativas e tempo físico. Para horas assistenciais H, faltas brutas f e recuperação líquida de tempo r: tentativas equivalentes de duração = H/(1−f); tempo físico de agenda = H/(1−f) × (1−f×r). A perda líquida é f×(1−r)/(1−f×r). A mesma vaga recuperada não é contada duas vezes como tempo físico. Confirmar alguém ou reagendar para outro dia não recupera, sozinho, o tempo que já se perdeu.

O fluxo proposto é: receber exclusivamente pedidos regulados e checar vínculo; confirmar disponibilidade três dias antes; reconfirmar na véspera; manter lista de suplentes autorizada pela SES para o mesmo protocolo; preencher vagas liberadas somente quando houver tempo para executar o exame completo; registrar falta e submeter reagendamento ao fluxo pactuado, usando o mesmo ID do pedido. Não se presume retorno automático à fila nem reposição imediata de toda falta. Cancelamentos antecipados, faltas e reposições efetivamente realizadas devem ser medidos separadamente.

Sem recuperação das vagas, o mesmo arranjo cabe matematicamente em **dez meses**, mantendo dias úteis, 10 horas/dia, 80% de agenda e 20% de faltas. É alternativa de prazo, sujeita a decisão posterior e sem mudança no plano oficial. Não se afirma que dez meses sejam o mínimo possível em qualquer arranjo territorial. Sete meses não bastam com a meta de recuperação proposta.

O histórico de faltas da SES, entre cerca de 24% e 43% nos códigos da carteira, está na aba Agenda e absenteismo. Os 20% são uma hipótese do projeto. Com falta maior, a recuperação exigida também aumenta; a tabela mostra esse efeito. Medir semanalmente por polo e protocolo: tentativas, faltas, cancelamentos, minutos efetivamente recuperados, perda líquida, exames realizados e laudos. Se a perda líquida ultrapassar 5%, revisar o planejamento; acima de 6,4% no polo limitante, a meta deixa de caber no prazo de referência.

Reagendamento não é demanda nova, baixa administrativa não é exame e a soma de tentativas não é número de pessoas. Não foi retomada a conclusão superada de necessidade de 12.884 a 27.004 pedidos novos por faltas.

## Encaminhamento da SES

A quinta aba mostra os déficits por código se a SES mantiver sua oferta, se encaminhar 50% ou se concentrar o recorte eletivo selecionado no projeto. O cenário de 50% ainda deixa 348 exames de déficit em quatro protocolos de TC sem contraste. A concentração integral sustenta o mix apenas sob os rateios e a hipótese de oferta transferível usada. Essa parcela ainda precisa ser medida e pactuada; não se assume que toda a produção histórica possa ser suspensa pela SES. Emergências não são transferidas e a oferta de outros convênios deve ser preservada.

Antes de iniciar, a regulação precisa confirmar enquadramento da parede, estoque elegível atualizado, quantidade mensal encaminhada, parcela de oferta transferida, lista de reposição, destino após falta, prevenção de sobreposição e regras de remanejamento. Transferir demanda não cria pedidos adicionais para o sistema.
'''
(P/'Carteira 1 - orientacoes do plano em 20 salas.md').write_text(report)
print(json.dumps(result,ensure_ascii=False,indent=2))
