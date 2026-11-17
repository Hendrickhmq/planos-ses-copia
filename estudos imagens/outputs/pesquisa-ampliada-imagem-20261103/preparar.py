from pathlib import Path
import json,sys,re,zipfile,csv,hashlib
from decimal import Decimal,ROUND_HALF_UP
O=Path(__file__).resolve().parent;ROOT=O.parents[1];REPO=ROOT.parent
sys.path.insert(0,str(REPO/'ferramentas'));import ler_tabela_unificada as sig
raw=json.loads((ROOT/'revisao_carteira1_20261102/fontes_preservadas/dados/fontes/mapa_social_20261102_imagem_bruto/coleta_20261102.json').read_text())
rev=json.loads((ROOT/'revisao_carteira1_20261102/dados_revisao.json').read_text());old=json.loads((ROOT/'outputs/emenda-imagem-1500000-20261103/dados_estudo.json').read_text());old={r['code']:r for r in old['records']}
prices={x['codigo']:x for x in json.loads((REPO/'outputs/estudo_imagem_candanga_20261101/tabela_oficial_sia.json').read_text())}
def code(s):return re.sub(r'\D','',s)
excluded={'0207030030','0207010048','0207020027','0207010030','0207010056','0207020019'}
items=[r for r in raw['rumo'] if code(r['codigo']).startswith('0208') or (code(r['codigo']).startswith('0207') and code(r['codigo']) not in excluded) or code(r['codigo']) in ['0204060028','0204030188','0206010095']]
fichas=sig.ler('102026',[code(r['codigo']) for r in items]);incs={}
with zipfile.ZipFile(sig.pacote('102026')) as z:
 for r in sig.linhas(z,'rl_procedimento_incremento'):
  if r['CO_HABILITACAO']=='3801':incs[r['CO_PROCEDIMENTO']]=int(r['VL_PERCENTUAL_SA'])/10000
records=[]
for r in items:
 c=code(r['codigo']);f=fichas[c];b=f['valor_sa'];inc=incs.get(c);p=prices.get(c,{})
 decision='Complemento de baixo volume; confirmar protocolo'
 if c in ['0208050035','0208040056','0208030018']:decision='Cotar carteira nuclear com prestador existente'
 if c in ['0208010025','0208010033']:decision='Cotar pacote cardíaco; decidir alocação entre emendas'
 if c=='0208040102':decision='Cotar DTPA separado; incremento não localizado'
 if c=='0206010095':decision='Somente com preço integral e indicação SUS validados'
 if c=='0204060028':decision='Prioridade operacional para cotação'
 if c=='0204030188':decision='Alternativa; fluxo para achados e tarifa pendentes'
 if c.startswith('0207'):decision='Alternativa de RM; cotar contraste/sedação separados'
 overlap='Sem cobertura identificada no plano 4/OCI mapeados; conciliar pacientes'
 if c=='0207030022':overlap='Separar pelve não ortopédica da bacia ortopédica do IEV'
 if c in ['0208010025','0208010033']:overlap='Possível mesmo paciente nas duas etapas; evitar dupla contagem'
 records.append(dict(code=c,name=f['nome'],local_name=r['fila_maior'],family='Medicina nuclear' if c.startswith('0208') else 'PET-CT' if c=='0206010095' else 'Ressonância' if c.startswith('0207') else 'Radiologia',stock=r['fila'],recent=r['fila_viva'],entries=r['entrantes_12m'],scheduled=r['oferta_12m'],performed=r['realizados_12m'],absent=r['faltas_12m'],base=b,inc=inc,incremental=float((Decimal(str(b))*(1+Decimal(str(inc or 0)))).quantize(Decimal('.01'),rounding=ROUND_HALF_UP)),candanga=p.get('preco'),page=p.get('pagina'),decision=decision,overlap=overlap))
records.sort(key=lambda x:(0 if x['family']=='Medicina nuclear' else 1,-x['stock']))
a=list(csv.DictReader((O/'fontes/autorizacoes_ansn_20261103.csv').read_text(encoding='cp1252').splitlines(),delimiter=';'))
lic=[x for x in a if x['Estado']=='DF' and x['Área de atuação']=='MEDICINA NUCLEAR'];assert len(lic)==23
urlansn='https://appasp2019.cnen.gov.br/dados-abertos/dados-abertos-ansn-download.asp?op=2'
providers=[
['IMEB','Oferta explícita e autorização','Óssea, miocárdio, DMSA/DTPA, tireoide, paratireoide, pulmonar, cerebral, digestivas','7 registros; vincular matrículas a cada unidade','Asa Sul, Asa Norte, Gama e Taguatinga','61 3771-3800 / 99976-4074','Não identificado como executor no recorte consultado','https://imeb.com.br/nossos_exames/cintilografia/','Confirmar filial, licença e agenda de cada protocolo'],
['Núcleos / Centro de Medicina Nuclear de Brasília','Oferta explícita e autorização','Cintilografia/SPECT, cirurgia radioguiada e PET-CT','4 registros CMN; não equivalem a 4 concorrentes','Centro Médico, Advance, OHB, Lago Sul, Santa Lúcia','61 3031-7200','Ato SES de 2015; execução atual não comprovada','https://nucleos.med.br/procedimentos/medicina-nuclear-exames/','Matrícula 17134 vence 25/11/2026; identificar unidade e renovação'],
['IRB','Oferta explícita e autorização','Óssea, DMSA, renal dinâmica, miocárdio, paratireoide e outras','15209 até 24/07/2027','SHIS QI 15 bloco O, Victoria Medical Center','61 3364-4252 / 99153-5170','Não identificado como executor no recorte consultado','https://irbmedicina.com/exames_de_medicina_nuclear/','Checar vínculo societário com Núcleos antes de contar concorrentes'],
['Biocárdios','Oferta explícita e autorização','Perfusão miocárdica, salivares, tireoide Tc99m, paratireoide e DMSA','15776 até 02/08/2027; 17932 até 17/10/2028','SEPS 709/909 Biocenter; Sobradinho Q Central bloco 5','61 3442-6300','Não identificado como executor no recorte consultado','https://biocardios.com.br/exames/cintilografia','Óssea não confirmada na página; não atribuir portfólio completo'],
['Hospital do Coração do Brasil / Rede D’Or','Oferta explícita e autorização','Miocárdio em repouso e estresse físico/farmacológico','16410 até 12/01/2029','SHLS 716 conjunto G, Asa Sul','61 3213-4000','Não identificado como executor no recorte consultado','https://www.rededorsaoluiz.com.br/hospital/coracaodobrasil/servicos/medicina-nuclear','Demais sistemas são categorias; confirmar exame por exame'],
['HOME','Oferta institucional e autorização','Cintilografias e cirurgia radioguiada; catálogo/agenda a validar','16379 até 06/10/2029','SGAS 613 conjunto C, Asa Sul','61 3878-2878','Não identificado como executor no recorte consultado','https://www.homehospital.com.br/Noticia,Abrir,19472,4693.aspx','Notícia sem ano visível; confirmar serviço comercial atual'],
['Clínica Villas Boas','PET-CT explícito e autorização','PET-CT; múltiplos radiofármacos, não intercambiáveis no SUS','14479 até 27/08/2028','SHLS 716 conjunto N bloco D','61 2191-5050 / 2191-5051','Não identificado como executor no recorte consultado','https://www.clinicavillasboas.com.br/exames/','Não inferir cintilografia convencional a partir de PET-CT'],
['Sírio-Libanês Brasília','PET-CT explícito e autorização','PET-CT, RM, TC, mamografia e densitometria','16264 até 16/07/2028','Centro Diagnósticos Asa Sul; conferir endereço executor com licença','61 2141-4000','Não identificado como executor no recorte consultado','https://siriolibanes.org.br/unidades/diagnostico-asa-sul','Não transferir autorização da unidade III para outro endereço'],
['Hospital Santa Lúcia','Autorização; operador a conciliar','Não validar lista por exame só pela autorização','15241 até 04/10/2028','DF; há unidade Núcleos Santa Lúcia','Via central Núcleos 61 3031-7200','Não identificado como executor no recorte consultado',urlansn,'Pode duplicar oferta do Núcleos; vincular CNPJ/unidade'],
['Hospitais Integrados da Gávea','Autorização; oferta diagnóstica não confirmada','Há pista de terapia; não prova cintilografia diagnóstica','17325 até 24/06/2029','DF; unidade/CNPJ precisam ser vinculados','Não validado','Não identificado como executor no recorte consultado',urlansn,'Documento DF Star 26/03/2026 declara não prestar medicina nuclear; resolver divergência'],
['HUB','Público; executor no Mapa Social','Cintilografia no grupo regulado','11576 até 01/12/2028','SGAN 605, Asa Norte','Regulação SES','Único executor do grupo Cintilografia consultado','https://paineis-ext.mpdft.mp.br/extensions/mapasauderegulamentacao/mapasauderegulamentacao.html','Categoria contratado/credenciado no painel não torna HUB privado'],
['HBDF / IGESDF','Público; executor no Mapa Social','PET-CT regulado','16867 até 03/09/2027','SMHS 101, Asa Sul','Regulação SES','Único executor do PET-CT consultado','https://paineis-ext.mpdft.mp.br/extensions/mapasauderegulamentacao/mapasauderegulamentacao.html','Expandir acesso deve complementar oferta existente'],
['Hospital das Forças Armadas','Público militar; autorização','Óssea, renal, cardíaca, tireoide e outras','15936 até 05/10/2027','HFA, Brasília','Marcação na clínica, conforme elegibilidade','Acesso SES não demonstrado','https://www.gov.br/hfa/pt-br/servicos-e-informacoes/consultas-e-exames/exames-disponiveis/cintilografia','Não tratar acesso militar como vaga disponível para SES'],
['Vila Rica','Pista institucional; nuclear não confirmada','RM, colangio-RM, densitometria e mamografia; nuclear sem catálogo específico','Sem correspondência nominal encontrada no CSV nuclear DF','Asa Sul e Sobradinho','Consultar site','Não demonstrado','https://clinicavilarica.com.br/','Não confundir Vila Rica com Villas Boas'],
['Diagnostik','Pista CNES; nuclear não confirmada','Radiologia; gama-câmara cadastrada não prova cintilografia','Sem correspondência nominal encontrada no CSV nuclear DF','Hospital Alvorada, SEPS 710/910 bloco B','61 3244-6999 / 99427-2885','Não demonstrado','https://www.diagnostik.com.br/','CNES 3056414; não contabilizar como fornecedor nuclear validado'],
['Taguacor','Pista CNES; nuclear não confirmada','Gama-câmara cadastrada; portfólio não validado','Sem correspondência nominal encontrada no CSV nuclear DF','Taguatinga; endereço cadastral a reconfirmar','Não validado','Não demonstrado','https://cnes2.datasus.gov.br/Mod_Ind_Equipamentos_Listar.asp?VCod_Equip=01&VComp=&VEstado=53&VListar=1&VMun=&VTipo_Equip=1','CNES 7009445; exige investigação antes de cotar nuclear']]
providers += [
['Radiolinea','Oferta explícita de imagem','RM, angio-RM, colangio-RM, sela, mastoides e TC','Não se aplica licença nuclear para validar RM','Brasília; unidade a confirmar na proposta','61 3771-3737','Anuncia Tabela Especial SUS; isso não prova contrato SES','https://www.radiolinea.com.br/exames/','Cotar protocolos e esclarecer natureza comercial da tabela anunciada'],
['Tesla Diagnóstico por Imagem DF','Oferta explícita de RM','RM de abdômen, pelve e outros protocolos','Não se aplica licença nuclear para validar RM','Cléo Otávio, W1 Norte, salas 7 e 8','61 3326-9456 / 3326-9565','Não verificado neste recorte de RM','https://www.teslaimagem.com.br/páginas/exames/ressonancia.html','Domínio .com.br; homônimo .com é de Jacobina/BA'],
['Sabin Imagem Brasília','Oferta explícita de imagem','RM, mamografia, densitometria e TC','Não se aplica licença nuclear para validar RM','Unidades de Brasília/DF; confirmar exame por unidade','61 3329-8000','Não verificado neste recorte de imagem','https://sabin.com.br/unidades/brasilia-df/imagem/','Cotar unidade executante, contraste/sedação e prazo do laudo']]
mapa={'fonte':'https://paineis-ext.mpdft.mp.br/extensions/mapasauderegulamentacao/mapasauderegulamentacao.html','atualizado':'03/11/2026 14:32:34','metodo':'Leitura agregada da interface pública; sem ano, status ou unidade selecionados. Filtro de grupo ou nome exato conforme linha. Executor identificado pela tabela de detalhes e KPI de unidade única. Não é auditoria de contrato nem coleta completa da base.','recortes':[{'filtro':'Grupo Procedimento = GRUPO - CINTILOGRAFIA','agendamentos':5328,'unidades':1,'executor':'HUB','anos_agendados':{'2025':1828,'2026':3500},'realizados_exibidos':{'2025':1064,'2026':1618}},{'filtro':'Procedimento = TOMOGRAFIA POR EMISSÃO DE PÓSITRONS (PET-CT)','agendamentos':4983,'unidades':1,'executor':'HBDF','anos_agendados':{'2021':65,'2022':1407,'2023':653,'2024':808,'2025':928,'2026':1122},'realizados_exibidos':None}]}
(O/'mapa_social_agregado.json').write_text(json.dumps(mapa,ensure_ascii=False,indent=2))
d={'procedures':records,'providers':providers,'licenses':lic,'mapa':mapa,'sources':[
['Demanda','Mapa Social preservado 02/11/2026; pedidos até 28/10; produção out/2025-set/2026',str(ROOT/'revisao_carteira1_20261102/fontes_preservadas/dados/fontes/mapa_social_20261102_imagem_bruto/coleta_20261102.json')],
['Preços','SIGTAP 10/2026 e incremento habilitação 38.01',str(sig.pacote('102026'))],
['Candanga','Anexo oficial SIA; referência não adotada automaticamente na emenda federal',str(REPO/'outputs/estudo_imagem_candanga_20261101/tabela_oficial_sia.json')],
['Licenças','CSV ANSN/CNEN disponível em 03/11/2026; filtro exato DF + MEDICINA NUCLEAR',urlansn],
['Painel','UI 03/11/2026 14:32:34; universo consultado e limites em mapa_social_agregado.json',mapa['fonte']],
['CNES','Equipamento cadastrado não comprova operação ou oferta por exame','https://cnes2.datasus.gov.br/Mod_Ind_Equipamentos_Listar.asp?VCod_Equip=01&VComp=&VEstado=53&VListar=1&VMun=&VTipo_Equip=1'],
['Regulação','RDC38/2008 art2; licença nuclear e sanitária','https://anvisalegis.datalegis.net/action/ActionDatalegis.php?acao=abrirTextoAto&cod_menu=9431&cod_modulo=310&link=S&numeroAto=00000038&orgao=RDC%2FDC%2FANVISA%2FMS&seqAto=000&tipo=RDC&valorAno=2008'],
['Histórico SES','Dispensa156/2015 Núcleos, cintilografia óssea450; não prova execução nem contrato atual','https://www.sinj.df.gov.br/sinj/Diario/efcfaea0bcad49018b65a11fa713cf89/b40be1da-8510-3764-937d-f1612bee39cf/arq/0/Se%C3%A7%C3%A3o03-%20207.pdf'],
['PET SUS','Protocolo SES: encaminhamento ao HBDF; indicações específicas','https://www.saude.df.gov.br/documents/37101/0/Protocolo%2Bde%2Bacesso%2BPETCT2.pdf/1dcf4b5d-6afc-34b0-6b6a-b249f3c325f6?t=1732730740845']
]}
(O/'dados_ampliados.json').write_text(json.dumps(d,ensure_ascii=False,indent=2))
(O/'fontes/manifesto.json').write_text(json.dumps({p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (O/'fontes').iterdir() if p.is_file()},indent=2))
print('procedimentos',len(records),'nuclear',len([r for r in records if r['family']=='Medicina nuclear']),'licenças',len(lic),'perfis',len(providers))
for r in records:print(r['code'],r['stock'],r['base'],r['incremental'],r['candanga'])
