"""Confere resultados calculados no XLSX com cálculo independente e gera o relatório."""
from pathlib import Path
from collections import defaultdict
import json,math,hashlib
from openpyxl import load_workbook
P=Path(__file__).resolve().parents[1]
d=json.loads((P/'dados_revisao.json').read_text())
w=load_workbook(P/'estudo_filas_imagem_20261102_organizada_revisada.xlsx',data_only=True)
wf=load_workbook(P/'estudo_filas_imagem_20261102_organizada_revisada.xlsx',data_only=False)
checks=[]
def check(label,got,exp,tol=1e-6):
    ok=abs(got-exp)<tol if isinstance(exp,(int,float)) else got==exp
    if not ok: raise AssertionError((label,got,exp))
    checks.append(label)
check('Meta',w['Resumo']['B4'].value,79219)
check('Procedimentos R$',w['Resumo']['D4'].value,10636506.41,.005)
hu=sum(i['meta']*i['minutos']/60 for i in d['items'] if i['modalidade']=='Ultrassom')
ht=sum(i['meta']*i['minutos']/60 for i in d['items'] if i['modalidade']=='Tomografia')
check('Horas US',hu,23906.166666666668)
check('Horas TC',ht,4739)
h=defaultdict(float)
for r in d['regional']:
    i=d['items'][r['item']-1]
    if i['modalidade']=='Ultrassom': h[r['polo']]+=r['meta']*i['minutos']/60
for row in list(w['Salas por polo'].values)[6:42]:
    origem,polo,m,f=row[:4];hours=h[polo];cap=m*21*10*.8
    check(f'Horas {polo}/{m}/{f}',row[5],hours)
    check(f'Salas {polo}/{m}/{f}',row[10],math.ceil(hours/(1-f)/cap))
    check(f'Utilização {polo}/{m}/{f}',row[11],hours/(1-f)/(cap*row[10]))
    check(f'Agenda perdida {polo}/{m}/{f}',row[7],hours/(1-f)-hours)

for j in range(len(d['items'])):
    check('Rateio soma item '+str(j+1),sum(r['meta'] for r in d['regional'] if r['item']==j+1),d['items'][j]['meta'])
for row in list(w['Cenarios SES'].values)[6:6+len(d['protocols'])*12]:
    c,m,lag,code,name,source=row[:6];p=d['protocols'][source-7]
    q=p['estoque'];e=p['entrada_mes'];base=p['producao_mes'];t={'a':0,'b':.5,'c':1}[c] if p['meta'] else 0
    opening=max(0,q+e*lag-min(q+e*lag,base*lag))
    supply=opening+e*m
    ses=min(supply,base*m*(1-t));available=supply-ses
    real=min(available,p['meta']);end=available-real
    check('Estoque inicial '+str(len(checks)),row[9],opening)
    check('SES realizada '+str(len(checks)),row[15],ses)
    check('Projeto realizado '+str(len(checks)),row[18],real)
    check('Estoque final '+str(len(checks)),row[20],end)
    check('Balanço de pedidos '+str(len(checks)),opening+row[10]-row[12]-row[15]-row[18]-row[26]-row[20],0)
    check('Transferência não cria entrada '+str(len(checks)),row[10],e*m)

# Remanejo concreto: há Dopplers venosos bilaterais suficientes no Sul e horas em todos os receptores.
source_items={j+1 for j,i in enumerate(d['items']) if i['nome']=='ULTRA-SONOGRAFIA DOPPLER VENOSO - MMII ( BILATERAL)'}
assert sum(r['meta'] for r in d['regional'] if r['regiao']=='Sul' and r['item'] in source_items)>=1371
for r in range(7,13):
    assert w['Redistribuicao 20'][f'J{r}'].value<1e-6
    assert w['Redistribuicao 20'][f'I{r}'].value<=1+1e-9
check('Remanejo conserva horas',sum(w['Redistribuicao 20'][f'G{r}'].value for r in range(7,13)),hu)
assert sum(w['Redistribuicao 20'][f'C{r}'].value for r in range(7,13))==20
errors=[(s.title,c.coordinate,c.value) for s in w for row in s for c in row if c.data_type=='e']
assert not errors,errors[:5]
formula_count=sum(c.data_type=='f' for s in wf for row in s for c in row)
assert formula_count>10000
for a in d['source_manifest']:
    check('Hash cópia '+a['copia'],hashlib.sha256((P/a['copia']).read_bytes()).hexdigest(),a['sha256'])
    check('Hash origem '+a['origem'],hashlib.sha256(Path(a['origem']).read_bytes()).hexdigest(),a['sha256'])
results={'verificacoes_aprovadas':len(checks),'formulas':formula_count,'erros_excel':errors,'horas_us':hu,'horas_tc':ht,'meta':79219,'valor':10636506.41}
(P/'verificacao/resultado.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
def pt(n,dec=0): return f'{n:,.{dec}f}'.replace(',','X').replace('.',',').replace('X','.')
summary=list(w['Resumo'].values)
cap_table='\n'.join('| '+ ' | '.join([row[0],row[1],pt(row[5],1),str(row[10]),str(list(w['Salas por polo'].values)[i+24][10]),str(list(w['Salas por polo'].values)[i+12][10]),str(list(w['Salas por polo'].values)[i+30][10])])+' |' for i,row in enumerate(list(w['Salas por polo'].values)[6:12]))
ses_table='\n'.join('| '+' | '.join([row[0],str(row[1]),str(row[2]),pt(row[3]),pt(row[4]),pt(row[5]),pt(row[7]),pt(row[8]),pt(row[9]),pt(row[10])])+' |' for row in summary[23:35])
mins=[]
for row in list(w['Protocolos'].values)[6:6+len(d['protocols'])]:
    if isinstance(row[14],(int,float)) and row[14]>.5 and row[3]: mins.append((row[1],row[3],row[14],row[15]))
min_table='\n'.join(f'| {n} | {q} | {pt(f*100,1)}% | {pt(g*100,1)}% |' for n,q,f,g in sorted(mins,key=lambda x:-x[2]))
text=f'''# Carteira 1 — revisão de capacidade, demanda e encaminhamento

Revisão de 02/11/2026, na pasta de trabalho `estudos imagens`. A apresentação principal é `estudo_filas_imagem_20261102_organizada_revisada.xlsx`. Fontes e versões anteriores estão preservadas nesta pasta com hashes. O plano oficial, `estado.yaml` e documentos de outros planos não foram alterados. Sem commit ou envio externo.

## Resultado para decisão

A carteira 1 mantém **79.219 exames e R$ 10.636.506,41 em procedimentos**. Há {pt(hu,1)} horas assistenciais de US e {pt(ht,1)} de TC. A parede abdominal, com 3.304 exames, permanece essencial e sujeita à confirmação expressa da SES sobre enquadramento e faturamento. A angio coronária permanece excluída. A US de articulação fica fora inteira e 4.000 transvaginais ficam reservadas ao IEV, sem liberação automática por prazo presumido.

**Até 20 salas não é um arranjo robusto para a distribuição territorial atual aproximada.** Sem mover demanda, são 21 salas em oito meses ou 23 em sete, mesmo sem perda adicional por faltas. Se 20% das vagas forem perdidas além da disponibilidade operacional de 80%, são 24 e 29 salas. Com 30%, são 29 e 33. O mínimo puramente agregado com 20% de perdas seria 23 e 26, antes de arredondar por polo.

Um teste de 20 salas só cabe em oito meses, com faltas já integralmente absorvidas na eficiência final de 80% ou vagas repostas sem perda adicional, e com remanejamento de 1.371 Dopplers venosos bilaterais do Sul: 915 para Asa Sul e 456 para Ceilândia. O arranjo fica em 3 salas na Asa Sul, 3 em São Sebastião, 3 em Sobradinho, 1 em Ceilândia, 6 em Samambaia e 4 no Gama. Gama e Asa Sul ficam praticamente no teto de agenda. Esse teste matemático depende de deslocamento viável, regulação, equipe e salas confirmadas. Não constitui capacidade instalada nem recomendação territorial aprovada.

## Salas por região de origem e polo de atendimento

| Origem aproximada | Execução proposta | Horas US | 8m sem perda extra | 7m sem perda extra | 8m com 20% extra | 7m com 20% extra |
|---|---|---:|---:|---:|---:|---:|
{cap_table}

As participações por família vêm de **15/09/2026**: fila de US e total de solicitações na TC, transcritos em `calculo_v19/calculo.py`. Protocolos sem equivalente usam o mix regional antigo de 20/10 como premissa. Foram rateadas quantidades inteiras por maiores restos por item, conservando as metas e os tempos. A distribuição de 02/11 está disponível somente para modalidades inteiras, sem cruzamento com elegibilidade e protocolos. Ela inclui URD, credenciados e registros sem região e não foi renormalizada silenciosamente para simular residência. A região do registro precisa ser validada como origem geográfica antes da pactuação.

O total de US equivale a 17,79 salas de 1.344 horas em oito meses antes do arredondamento territorial. Em sete meses, cada sala tem 1.176 horas. Vagas de agenda, horas assistenciais e horas perdidas estão separadas. Os tempos do gerador anterior foram preservados, incluindo 40 minutos para Doppler bilateral de membros. A referência ao CBR 2017 é a atribuição documental herdada e não uma validação clínica nova. Unidade de faturamento bilateral precisa de conferência.

Os 80% têm duas interpretações explicitadas: (1) disponibilidade operacional, com pausas e indisponibilidades, descontando faltas separadamente; (2) eficiência final já com faltas, sem descontá-las novamente. A segunda só é válida se as perdas totais couberem nos 20%. Com faltas de 20%, sobra zero margem para outras perdas; com 30%, eficiência final de 80% requer reposição. As salas não foram ajustadas por redução artificial de tempos.

TC foi dimensionada separadamente, por origem, no arranjo local de seis polos, em `Salas por polo`. No caso de oito meses sem perdas adicionais, são sete tomógrafos locais (dois para a Sudoeste), contra mínimo agregado de quatro. Não foi presumido que os seis equipamentos herdados ou o roteiro antigo estão confirmados. A redistribuição da TC precisa ser pactuada separadamente, com contraste, agenda e prestadores disponíveis.

## O encaminhamento da SES que sustenta as metas

Foram modelados os três cenários solicitados, por protocolo: a) manutenção da oferta; b) transferência de 50% da oferta eletiva selecionada atribuída à SES; c) transferência integral desse recorte, reduzindo a oferta correspondente. A produção dos demais prestadores é mantida. Protocolos sem meta própria não têm a oferta suspensa. Emergência, angio coronária, sedação e reservas são excluídas antes da projeção.

**Nas hipóteses do modelo, somente a concentração integral dos protocolos selecionados assegura todo o mix sem remanejamento de metas.** Isso não comprova que tal encaminhamento esteja disponível: a separação entre produção SES e outros convênios no mesmo protocolo não foi medida. A hipótese inicial atribui 100% da produção habitual à parcela transferível, como teto ilustrativo. O percentual é editável e os resultados se alteram quando parte dessa oferta pertence a outros prestadores não transferíveis.

| Cenário | Meses | Espera até início | Estoque inicial | Entradas elegíveis | SES atendida | Projeto possível | Déficit de meta | Estoque final | Aumento líquido rede |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
{ses_table}

Os totais são pedidos equivalentes de modelagem, arredondados só na apresentação. A coluna de outros convênios/prestadores está na planilha e vale zero na hipótese extrema inicial, **não por medição de ausência**. O estoque final pode crescer mesmo com cumprimento da meta porque a rede reduz a oferta em c. Transferência não cria demanda nova nem equivale a aumento líquido de atendimento. O aumento líquido compara a produção total do cenário com a produção habitual possível sobre o mesmo estoque e entradas.

No cenário b, faltam 348 realizações em quatro protocolos sem contraste. A pactuação pode selecionar percentuais diferentes por protocolo em vez de suspender tudo. Para estes quatro, a proxy sugere transferência mínima superior a 50%:

| Protocolo | Meta | Transferência mínima 8m | Transferência mínima 7m |
|---|---:|---:|---:|
{min_table}

Esses percentuais são cenários, sem confirmação de fluxos por protocolo. Não são quantidades comprovadas a contratar. A planilha expõe as frações mínimas para todos os protocolos em `Protocolos`. É preciso pactuar com a regulação: lista eletiva e critérios de elegibilidade, identificação da oferta própria efetivamente transferível, oferta preservada de outros convênios, quantitativo mensal encaminhado, destino após falta/cancelamento, bloqueio de dupla vinculação e remanejamento de metas autorizado. A SES deve confirmar também parede abdominal e unidade de faturamento do Doppler bilateral.

## Faltas, reagendamentos e baixas

A conclusão de **12.884 a 27.004 pedidos novos necessários está superada**. Para 79.219 realizações, meta/(1−faltas) gera cerca de 99.024 tentativas a 20% ou 113.170 a 30%, arredondando no total. Arredondar separadamente por protocolo gera mais vagas. Essas tentativas podem pertencer à mesma solicitação reapresentada, portanto não comprovam pacientes ou pedidos novos. Reagendamento não é entrada e não é realização.

Pessoas únicas, solicitações, tentativas de agendamento, faltas, reagendamentos, cancelamentos, outras baixas e realizações são medidas distintas. A fonte tem pessoas por par/modalidade, pendências por nome e situações/produção agregadas por código. Não tem chave longitudinal que permita reconstruir destinos ou deduplicar pessoas da carteira. Cancelamento de agenda não demonstra cancelamento do pedido. Não foi inventada regra de retorno à fila.

Se a mesma solicitação puder ser reapresentada no prazo, faltas afetam vagas e capacidade, sem necessariamente aumentar demanda única. Se uma falta retirar o pedido da execução sem retorno, a disponibilidade pode cair: nesse cenário extremo, uma tentativa por pedido requer mais solicitações acessíveis, mas a regra e a perda definitiva precisam ser medidas antes de quantificar necessidade de novos pedidos. Baixas administrativas podem reduzir o registro da fila sem resolver a indicação assistencial. Não contam como produção. O modelo começa com baixas e cancelamentos adicionais iguais a zero como hipóteses explícitas, com campos próprios.

## Crescimento, estoques e intervalo até execução

A projeção usa o mesmo inventário elegível da carteira, incluindo nomes pequenos como disponibilidade possível, sem incluí-los artificialmente nas metas. O estoque elegível é **77.981,35 pedidos equivalentes**, frente a 77.976 antes: a diferença vem de filas pequenas e truncamentos por nome. A fração de pelve de 7/5.944 é conservada como premissa legada pendente, sem tratar CID como fronteira. A reserva transvaginal permanece 4.000 no estoque; a aplicação proporcional ao fluxo é apenas hipótese de rateio.

Não há entradas e produção realizada por protocolo no mesmo recorte. Entradas são estimadas pelo fluxo do código vezes a participação elegível no estoque. Produção usa os agendamentos dos nomes multiplicados pela razão realizados/agendados do código e pela fração elegível. As janelas e o mix não são idênticos. Não se pode tratar o fluxo integral do código nem a agenda como produção acessível garantida. A planilha separa fonte, proxy e realização projetada. Os saldos negativos são mantidos e reduzem o estoque quando a rede atende acima das entradas.

Há comparações com zero e dois meses entre coleta e início. O início real permanece desconhecido. Os dados mais recentes de solicitações na recarga de 02/11 vão até 28/10, informação que também afeta o calendário efetivo. A produção anterior ao início é descontada antes da nova execução. Meses para zerar são projeções condicionadas ao saldo e não previsões garantidas. O balanço acumulado não prova disponibilidade mês a mês, acesso geográfico, elegibilidade individual ou conclusão de toda a fila da extração.

## Formulação a avaliar posteriormente

Propõe-se substituir a promessa de zerar a extração por **produção efetivamente realizada de 79.219 exames elegíveis, encaminhados pela regulação, por código e prazo**, com identificação individual, laudo e registro único, sem dupla contagem. A quantidade de vagas ofertadas é indicador separado. Remanejamento só após pactuação prévia e preservando limites e enquadramento. A redução da espera deve ser acompanhada por protocolo, com mediana e P90 medidos na linha de base e nos períodos, antes de fixar percentual de redução. Reagendamentos e baixas administrativas têm indicadores próprios. Esta proposta não altera o texto oficial nesta etapa.

## Registro das mudanças e verificação

- Mantida a carteira 1, com parede e sem angio, em lugar de voltar a discutir carteiras alternativas.
- Substituída a afirmação de 137% sobre 13 salas por cálculo territorial e comparação explícita com até 20.
- Separadas horas realizadas, tempo de agenda e perdas, corrigindo a afirmação antiga de que faltas não mudam salas.
- Retirada a inferência de pedidos novos a partir de tentativas de agenda.
- Substituídos crescimento apenas positivo e oferta agendada por balanços com produção estimada, contração e defasagem.
- Acrescentados cenários de divisão da produção com a SES e distinção entre transferência e expansão líquida da rede.
- Identificadas as distribuições antigas, a parcela sem origem geográfica validada e as pendências de medição.
- Custos e cotação médica não foram reabertos.

Verificação independente: {len(checks)} conferências, {formula_count} fórmulas e nenhum erro de fórmula Excel identificado. Conferidos meta, valor, horas, arredondamento por polo, balanços de todos os cenários, conservação de horas no remanejo e hashes das cópias e origens. O cálculo independente valida a implementação, não as premissas nem a viabilidade clínica/territorial. As prévias da planilha ficam em `verificacao`.

Para regenerar: executar `scripts/preparar.py`, `scripts/gerar_planilha.mjs` e `scripts/verificar_e_relatar.py`, nesta ordem, com Python/openpyxl de leitura e Node com `@oai/artifact-tool`. Os scripts antigos são evidência preservada, não geradores desta revisão. As fontes já copiadas permitem reproduzir os cálculos sem nova consulta ao painel.
'''
(P/'estudo_carteira1_revisado.md').write_text(text)
(P/'LEIA-ME.md').write_text('''# Estudo revisado da carteira 1

Abra primeiro **estudo_filas_imagem_20261102_organizada_revisada.xlsx**. O relatório de apoio é **estudo_carteira1_revisado.md**.

- `scripts`: preparação dos dados, gerador da planilha e verificação independente.
- `dados_revisao.json`: dados e recortes usados pelo gerador.
- `fontes_preservadas`: cópias das fontes, sem edição.
- `versao_anterior`: estudos de 02/11 anteriores a esta revisão, com conclusões superadas.
- `manifesto_fontes.json`: origens e SHA-256 das cópias.
- `verificacao`: conferências e prévias de leitura.

As hipóteses editáveis ficam em Premissas. Os cenários a/b/c e os horizontes de 7/8 meses são comparações simultâneas. A distribuição territorial permanece aproximada. Nenhuma capacidade instalada ou decisão de encaminhamento da SES foi presumida confirmada.
''')
print(json.dumps(results,ensure_ascii=False,indent=2))
print('Protocolos com transferência mínima >50%:',[(n,round(f,4)) for n,q,f,g in mins])
