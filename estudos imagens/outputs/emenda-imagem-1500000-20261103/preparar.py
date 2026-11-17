from pathlib import Path
import sys,json,zipfile,hashlib
from decimal import Decimal, ROUND_HALF_UP
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
REPO=ROOT.parent
sys.path.insert(0,str(REPO/'ferramentas'))
import ler_tabela_unificada as sig
import montar_coleta as coleta
def money(v): return float(Decimal(str(v)).quantize(Decimal('.01'),rounding=ROUND_HALF_UP))
rev=json.loads((ROOT/'revisao_carteira1_20261102/dados_revisao.json').read_text())
raw=json.loads((ROOT/'revisao_carteira1_20261102/fontes_preservadas/dados/fontes/mapa_social_20261102_imagem_bruto/coleta_20261102.json').read_text())
prices={x['codigo']:x for x in json.loads((REPO/'outputs/estudo_imagem_candanga_20261101/tabela_oficial_sia.json').read_text())}
profiles=[
 ('0208050035','Cintilografia óssea','Prioridade para cotar, com incremento','Sem cobertura identificada no acervo aprovado',0,464,'Referência exploratória sem localização confirmada; não é cotação DF','https://examesocial.com.br/'),
 ('0205010032','Ecocardiograma transtorácico','Reservado à emenda de R$ 2 milhões de cardiologia','IEV: até 1.000 OCI de insuficiência cardíaca; reservar pacientes',1000,180,'Preço publicado DF; confirmar protocolo e unidade','https://minhaclinica.com/exames/'),
 ('0204060028','Densitometria óssea','Prioridade para cotar, com incremento','Não identificada no IEV/plano 4; CID ortopédico não reserva o exame',0,77.99,'A partir de; CNC 01, Taguatinga; validar coluna/fêmur e laudo','https://app.drachei.com.br/preco-densitometria-ossea-brasilia-df'),
 ('0204030188','Mamografia de rastreamento','Segunda linha; negociar custo','Fora do plano 4 e das OCI aprovadas mapeadas',0,188.48,'A partir de; CNC 01, Taguatinga; exame digital bilateral','https://app.drachei.com.br/preco-mamografia-digital-bilateral-brasilia-df'),
 ('0207010064','RM de crânio','Alternativa com incremento','Fora das seis RM ortopédicas do IEV; separar protocolos',0,400,'A partir de, rede Brasília; unidade e protocolo não publicados','https://doctorsaude.com.br/ressonancia-magnetica-brasilia'),
 ('0207030014','RM de abdômen superior','Alternativa com incremento','Sem cobertura identificada no acervo aprovado',0,None,'Sem cotação comparável DF para este protocolo',''),
 ('0207030022','RM de pelve/bacia','Alternativa com separação assistencial','Pode atingir ortopedia do IEV; recortar indicação e pacientes',0,None,'Sem cotação comparável DF para este protocolo',''),
 ('0207030049','Colangiorressonância','Complemento de pequeno volume','Sem cobertura identificada no acervo aprovado',0,270,'Exploratória, Digem; localização não confirmada','https://examesocial.com.br/'),
 ('0208010025','Cintilografia miocárdica: estresse','Alternativa: cotar pacote completo','Não consta como obrigatório da OCI coronariana mapeada; verificar outros instrumentos',0,None,'Pacote estresse+repouso exploratório R$ 1.440, não avulso','https://examesocial.com.br/'),
 ('0208010033','Cintilografia miocárdica: repouso','Alternativa: cotar pacote completo','Mesmo paciente pode ter pedido de estresse; não somar como pessoas',0,None,'Não dividir preço de pacote por dois sem proposta','https://examesocial.com.br/'),
 ('0208040102','Cintilografia renal dinâmica','Complemento especializado','Sem cobertura identificada no acervo aprovado',0,468,'Exploratória, Digem; localização não confirmada','https://examesocial.com.br/'),
 ('0208040056','Cintilografia renal/renograma','Complemento especializado','Nome DMSA da fila exige confirmar código/protocolo',0,468,'Exploratória, Digem; localização não confirmada','https://examesocial.com.br/'),
 ('0208030018','Cintilografia de paratireoides','Complemento de pequeno volume','Sem cobertura identificada no acervo aprovado',0,None,'Sem cotação comparável DF',''),
 ('0206010095','PET-CT','Somente com proposta fechada viável','Sem incremento 38.01 localizado; protocolo oncológico específico',0,None,'Sem preço comparável DF de FDG; não usar PSMA como substituto',''),
 ('0207010048','RM de coluna lombossacra','Excluir da carteira inicial','Sobreposição com OCI ortopédica do IEV',0,None,'Sem cotação neste estudo',''),
 ('0205020062','US de articulação/partes moles','Excluir da carteira inicial','Articulação reservada ao IEV; partes moles excluídas por decisão anterior',0,None,'Cadastro local de partes moles não valida faturamento como articulação',''),
 ('0206010060','TC de sela túrcica','Residual; não sustenta o orçamento','Confirmar órbita versus sela; recorte eletivo',0,None,'Sem cotação neste estudo',''),
]
fichas=sig.ler('102026',[x[0] for x in profiles])
increments={}
with zipfile.ZipFile(sig.pacote('102026')) as z:
 for row in sig.linhas(z,'rl_procedimento_incremento'):
  if row['CO_HABILITACAO']=='3801': increments[row['CO_PROCEDIMENTO']]=int(row['VL_PERCENTUAL_SA'])/10000
records=[]
rumo={x['codigo']:x for x in raw['rumo']}
months,_=coleta.meses_fechados(raw)
for c,label,decision,overlap,reserve,retail,quality,url in profiles:
 f=fichas[c];r=rumo.get(f['codigo'],{}); p=prices.get(c,{})
 inc=increments.get(c)
 rows=[x for x in rev['invent'] if x['codigo']==f['codigo']]
 e=sum(x[2]+x[3] for x in raw['por_codigo']['entrantes']['linhas'] if x[0]==f['codigo'] and x[1] in months)
 a=sum(x[2] for x in raw['por_codigo']['oferta']['linhas'] if x[0]==f['codigo'] and x[1] in months)
 real=sum(x[3] for x in raw['por_codigo']['oferta']['linhas'] if x[0]==f['codigo'] and x[1] in months)
 assert (e,a,real)==(r['entrantes_12m'],r['oferta_12m'],r['realizados_12m'])
 records.append(dict(code=c,code_fmt=f['codigo'],name=label,official=f['nome'],decision=decision,overlap=overlap,reserve=reserve,stock=r['fila'],recent=r['fila_viva'],entries=e,scheduled=a,performed=real,absent=r['faltas_12m'],base=f['valor_sa'],increment=inc,with_increment=money(Decimal(str(f['valor_sa']))*(1+Decimal(str(inc)))) if inc is not None else f['valor_sa'],candanga=p.get('preco'),page=p.get('pagina'),retail=retail,retail_quality=quality,retail_url=url,protocols=[{'name':x['nome'],'stock':x['fila'],'recent':x['fila_viva']} for x in rows]))
sources=[
 ['D1','Decisão do usuário em 03/11/2026: reservar eco e eletro à emenda de R$ 2 milhões de cardiologia','Conversa deste estudo; eletro entendido como eletrocardiograma'],
 ['S1','Fila e produção: Mapa Social, recarga 02/11/2026; pedidos até 28/10/2026',str(ROOT/'revisao_carteira1_20261102/fontes_preservadas/dados/fontes/mapa_social_20261102_imagem_bruto/coleta_20261102.json')],
 ['S2','Carteira 1: estudo revisado; proposta em elaboração, não contrato executado',str(ROOT/'revisao_carteira1_20261102/estudo_carteira1_revisado.md')],
 ['S3','IEV/OCI aprovadas e correção da fronteira por CID: seção 7',str(ROOT/'revisao_carteira1_20261102/versao_anterior/estudo_outros_planos_imagem_20261102.md')],
 ['S4','SIGTAP 10/2026: base SA e incremento 38.01 no pacote oficial em cache',str(sig.pacote('102026'))],
 ['S5','Anexo oficial Candanga SIA; não é Valor Máximo do estudo de agosto',str(REPO/'outputs/estudo_imagem_candanga_20261101/tabela_oficial_sia.json')],
 ['S6','Deliberação CG-SES 46/2026; complementação distrital e requisitos','https://www.sinj.df.gov.br/sinj/Norma/08cdc67f1b9a46158271100a13d7d382/Delibera_o_46_21_09_2026.html'],
 ['S7','SAES 4.694/2026, arts. 2 a 6; habilitação e efeitos até 31/12/2026',str(REPO/'biblioteca/extraidos_normas/SAES 4694-2026 rol imagem ambulatorial/texto.md')],
 ['S8','GM/MS 12.116/2026: permissão federal não equivale a adoção automática local','https://bvsms.saude.gov.br/bvs/saudelegis/gm/2026/prt12116_24_08_2026.html'],
 ['S9','Lei DF 7.897/2026, art. 4º §1º: complemento próprio',str(REPO/'biblioteca/extraidos_normas/Lei DF 7897 de 28_05_2026 Tabela SUS Candanga/texto.md')],
 ['S10','Ministério da Saúde: incremento no componente Crédito Financeiro; não é convênio automaticamente','https://www.gov.br/saude/pt-br/assuntos/noticias/2026/julho/ministerio-da-saude-atualiza-valores-para-oferta-de-tomografias-e-ressonancias-na-rede-privada-pelo-sus'],
 ['S11','Minha Clínica, preço publicado de ecocardiograma; consultado 03/11/2026','https://minhaclinica.com/exames/'],
 ['S12','Dr.Achei, densitometria Taguatinga, a partir de; consultado 03/11/2026','https://app.drachei.com.br/preco-densitometria-ossea-brasilia-df'],
 ['S13','Dr.Achei, mamografia Taguatinga, a partir de; consultado 03/11/2026','https://app.drachei.com.br/preco-mamografia-digital-bilateral-brasilia-df'],
 ['S14','Doctor Saúde, RM Brasília, a partir de; sem executor/protocolo definido','https://doctorsaude.com.br/ressonancia-magnetica-brasilia'],
 ['S15','Exame Social, referências exploratórias sem cidade confirmada; não usar como custo contratado','https://examesocial.com.br/'],
]
out={'date':'03/11/2026','funding':'Federal de bancada, confirmado pelo usuário','months':months,'dates':raw['datas'],'records':records,'sources':sources,'selected_plan4_codes':sorted(set(x['codigo'] for x in rev['items'])),'plan4_total':sum(x['meta'] for x in rev['items']),'fichas':fichas,'operating_assumptions':{'budget':1500000,'months':8,'support':150000,'absence':0.2,'overhead_share':0.1,'formal_recognition':0,'legal_period_confirmed':0}}
(OUT/'dados_estudo.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
(OUT/'verificacao_fontes.json').write_text(json.dumps({'months':months,'source_sha256':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [sig.pacote('102026'),ROOT/'revisao_carteira1_20261102/dados_revisao.json']},'independent_monthly_reconciliation':len(records)*3},indent=2))
print('Meses fechados:',months[0],months[-1])
for r in records: print(r['name'],r['stock'],r['base'],r['with_increment'],r['candanga'],round((r['entries']-r['performed'])/12,1))
