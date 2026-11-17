from pathlib import Path
import json,sys,zipfile,hashlib
from decimal import Decimal,ROUND_HALF_UP
O=Path(__file__).resolve().parent;ROOT=O.parents[1];REPO=ROOT.parent
sys.path.insert(0,str(REPO/'ferramentas'));import ler_tabela_unificada as sig
src=ROOT/'tmp/estudo-integrado/fontes/mapa_social_20261102_inventario_bruto/motor_20261102.json'
raw=json.loads(src.read_text());t=next(iter(raw['panorama'].values()))['filas'];rows=[dict(zip(t['cols'],x)) for x in t['linhas']]
cat=json.loads((ROOT/'tmp/estudo-integrado/classificacao.json').read_text())
for x in rows:x['code']=x['codigo'].zfill(10)
prices={x['codigo']:x for x in json.loads((REPO/'outputs/estudo_imagem_candanga_20261101/tabela_oficial_sia.json').read_text())}
with zipfile.ZipFile(sig.pacote('102026')) as z:
 nuclear=[x['CO_PROCEDIMENTO'] for x in sig.linhas(z,'tb_procedimento') if x['CO_PROCEDIMENTO'].startswith('0208')]
 inc={x['CO_PROCEDIMENTO']:int(x['VL_PERCENTUAL_SA'])/10000 for x in sig.linhas(z,'rl_procedimento_incremento') if x['CO_HABILITACAO']=='3801'}
# Rótulo, códigos, dificuldade prática, posição no estudo, sobreposição/escopo.
options=[
('Densitometria',['0204060028'],'Agenda curta relativamente às modalidades com sedação. Confirmar coluna/fêmur, laudo e equipamento.','Cotar primeiro','Imagem; sem cobertura identificada no plano 4 ou OCI mapeadas'),
('Mamografia',['0204030188'],'Qualidade e laudo especializado. Prever investigação dos achados; não encerrar o cuidado no exame.','Cotar em paralelo','Imagem; conferir rastreamento versus diagnóstico no mesmo código local'),
('RM de crânio',['0207010064'],'Triagem para implantes, claustrofobia, contraste e sedação. Não cotar tudo como RM simples.','Cotar primeiro','Imagem; separar protocolos pediátricos e sedação'),
('RM abdômen superior',['0207030014'],'Definir protocolo e contraste, preparo e limite de peso.','Cotar em paralelo','Imagem; sem cobertura identificada na carteira anterior'),
('RM pelve/bacia, recorte a definir',['0207030022'],'Protocolos de pelve, próstata e bacia não são intercambiáveis em custo. Fila mostrada é do código inteiro, ainda sem retirar ortopedia.','Cotar com recorte','Imagem; conciliar bacia ortopédica do IEV e indicação urológica'),
('Colangiorressonância',['0207030049'],'Exige protocolo de vias biliares e preparo. Não equivale a exame endoscópico terapêutico.','Complemento de carteira','Imagem; volume menor'),
('Angio-RM cerebral',['0207010013'],'Definir arterial/venosa, território e contraste. Código genérico não padroniza protocolo.','Complemento de carteira','Imagem; cruzar pedido e protocolo'),
('RM sela/base do crânio/mastoides',['0207010072','0207010021'],'Recortar sela, mastoides, ATM e base do crânio. Equipe e sequências dedicadas.','Complemento de carteira','Imagem; duas referências SIGTAP distintas'),
('PAAF de tireoide',['0201010470'],'Punção guiada e citopatologia precisam formar um percurso completo. Definir adequação da amostra e repetição.','Explorar linha diagnóstica','Procedimento guiado; confirmar objeto e composição remunerável'),
('Core biópsia guiada',['0201010542'],'Dispositivo, anestesia local, guia por US/mamografia/TC e anatomopatológico. Não tratar todos os órgãos como o mesmo custo.','Explorar linha diagnóstica','Inclui filas mamárias; conciliar cobertura oncológica e indicação'),
('OCT oftalmológico',['0211060283'],'Equipamento dedicado, segmento ocular e indicação SUS. OCT anterior, retina e OCT-A não são equivalentes.','Investigar tarifa antes','Imagem oftalmológica; Candanga não localizada por esse código no anexo extraído'),
('Campimetria',['0211060038'],'Cooperação do paciente, repetibilidade e definição de olhos/cobrança. Exame especializado.','Investigar linha de glaucoma','Método oftalmológico; revisar objeto da emenda e contratos existentes'),
('Mapeamento de retina',['0211060127'],'Consulta/exame por oftalmologista, dilatação quando indicada e fluxo para tratamento.','Sobreposição a conciliar','ISHP tem 44.400 OCI oftalmológicas contratadas no acervo; exame obrigatório'),
('Retinografia fluorescente',['0211060186'],'Contraste, avaliação clínica e suporte a intercorrências. Não confundir com retinografia colorida.','Complemento especializado','Imagem oftalmológica; cruzar cobertura assistencial'),
('Endoscopia digestiva alta',['0209010037'],'Sedação quando indicada, recuperação, acompanhante, processamento do endoscópio e biópsia/patologia.','Grande alternativa se escopo permitir','Endoscopia; confirmar objeto além de imagem radiológica'),
('Colonoscopia',['0209010029'],'Preparo intestinal, sedação/anestesia, recuperação e eventual polipectomia/patologia. Preparação ruim gera repetição.','Grande alternativa se escopo permitir','Endoscopia; separar a fila com anestesia e retaguarda'),
('Videolaringoscopia e endoscopia nasal',['0209040041'],'Higienização, equipamento flexível/rígido e profissional. VED e videolaringoscopia não são automaticamente o mesmo pacote.','Alternativa com validação do código','Mesmo código local reúne nasal, laringe e deglutição; validar mapeamento'),
('Polissonografia',['0211050105'],'Leito/noite, técnico, laudo do sono e perdas técnicas. Tipo III domiciliar não substitui toda indicação de PSG completa.','Grande fila para projeto próprio','Diagnóstico do sono; depende de adequação do objeto'),
('Eletroneuromiografia',['0211050083'],'Tempo do especialista, segmentos, agulhas e protocolo. Duas filas podem pertencer à mesma pessoa.','Grande alternativa se escopo permitir','Neurofisiologia; não foi demonstrada cobertura pelo IEV só por diagnóstico ortopédico'),
('EEG em vigília e sono espontâneo',['0211050040','0211050024'],'Preparação, qualidade da aquisição, duração e laudo. Separar sono induzido e vídeo-EEG.','Alternativa de neurodiagnóstico','Neurofisiologia; não é ECG reservado à cardiologia'),
('Espirometria',['0211080055'],'Técnico treinado, manobras reprodutíveis, controle de qualidade e broncodilatador. Tarifa baixa.','Explorar apenas com custo fechado','Função pulmonar; requer adequação de escopo e conciliação da oferta SES'),
('Audiometria/imitanciometria',['0211070033'],'Nome local é conjunto; código aponta campo livre. Validar tonal, vocal e imitanciometria sem faturar por aproximação.','Revisar código e IEV antes','IEV tem 11.590 OCI auditivas no acervo; forte risco de sobreposição'),
('BERA/potencial evocado auditivo',['0211050113'],'Idade, colaboração, eventual sedação e tipo de potencial. Código e indicação alteram remuneração.','Revisar código e IEV antes','Compatibilidades das OCI auditivas precisam ser conciliadas'),
('VENG/otoneurológico',['0211070351'],'Protocolo vestibular e interpretação especializados. Não há preço Candanga localizado neste código.','Investigação secundária','Fora da imagem convencional; validar financiamento e código'),
('Colposcopia',['0211040029'],'Profissional, insumos e eventual biópsia/histologia. Tarifa isolada pequena.','Complemento de linha da mulher','GIN1 IEV não torna colposcopia automaticamente incluída; verificar outros instrumentos'),
('Holter e MAPA',['0211020044','0211020052'],'Aparelhos reutilizáveis, logística de retirada/devolução, perdas, instalação e laudo.','Avaliar na emenda de cardiologia','Usuário reservou eco e ECG; alocação de Holter/MAPA ainda não decidida'),
('PET-CT',['0206010095'],'Traçador específico, logística, preparo e indicação coberta pelo SUS. Não usar PSMA como preço de FDG.','Condicionado a preço integral','Imagem nuclear; oferta regulada HBDF identificada em 03/11'),
('Cintilografia óssea',['0208050035'],'Serviço nuclear licenciado, radiofármaco e imagens tardias. Não comporta fluxo de ultrassom rápido.','Cotar lote limitado','Imagem nuclear; conciliar cobertura oncológica e HUB'),
('Cintilografia renal DMSA',['0208040056'],'Radiofármaco, aquisição tardia e protocolo pediátrico quando aplicável.','Cotar como complemento','Imagem nuclear; confirmar vínculo do nome local ao código'),
('Cintilografia renal DTPA',['0208040102'],'Aquisição dinâmica e possível diurético. Não copiar tarifa ou protocolo de DMSA.','Cotar separadamente','Imagem nuclear; incremento 38.01 não localizado'),
('Cintilografia paratireoides',['0208030018'],'Aquisições e permanência prolongada; definir SPECT/CT se indicado e se incluído.','Cotar como complemento','Imagem nuclear; quantidade moderada'),
('Miocárdio repouso e estresse',['0208010025','0208010033'],'Preparo, estresse físico/farmacológico, equipe e duas etapas. Somar códigos não conta pessoas únicas.','Cotar percurso completo','Decidir imagem versus cardiologia; não assumido como reservado'),
('Salivares e tireoide',['0208020039','0208030026'],'Traçador, preparo e correlação clínica. Diferenciar tireoide diagnóstica de tratamento com iodo.','Complemento de pequeno volume','Imagem nuclear; filas menores'),
('Trânsito/esvaziamento gástrico',['0208020071','0208020055','0208020063','0208020110'],'Refeição/traçador, líquido versus sólido e aquisição seriada. Códigos locais podem reunir protocolos distintos.','Complemento de pequeno volume','Imagem nuclear; não sustenta sozinho o orçamento'),
('Linfocintilografia',['0208080040'],'Extremidades versus linfonodo sentinela. No sentinela, integrar horário e equipe da cirurgia.','Somente com percurso definido','Imagem nuclear; não comprar isoladamente como mutirão de alto volume'),
('Pulmonar por perfusão',['0208070044'],'Radiofármaco e indicação específica. Ventilação/inalação é outro procedimento, não equivalente.','Complemento especializado','Imagem nuclear; fila pequena localizada'),
('Pesquisa de corpo inteiro',['0208030042'],'Confirmar traçador, finalidade e preparo. Não equivale a toda cintilografia de corpo inteiro ou PET.','Complemento especializado','Imagem nuclear; conciliar linha oncológica'),
('Cerebral e estudos com gálio',['0208060030','0208060014','0208050043','0208090010'],'Traçador e finalidade definem exame. TRODAT não deve ser associado a ECD/tálio só pelo termo cerebral.','Explorar sob demanda confirmada','Imagem nuclear; custo de insumo e volume baixo'),
]
codes=sorted(set(nuclear+[c for x in options for c in x[1]]));f=sig.ler('102026',codes)
records=[]
for c in codes:
 q=[x for x in rows if x['code']==c];cats=[x for x in cat if x['codigo'].zfill(10)==c];base=f[c]['valor_sa'];pct=inc.get(c)
 stock=sum(x['fila'] for x in q) if q else None
 records.append(dict(code=c,name=f[c]['nome'],stock=stock,recent=sum(x['fila_viva'] for x in q) if q else None,scheduled=sum(x['agendadas_12m'] or 0 for x in q) if q and any(x['agendadas_12m'] is not None for x in q) else None,base=base,inc=pct,incremental=float((Decimal(str(base))*(1+Decimal(str(pct)))).quantize(Decimal('.01'),rounding=ROUND_HALF_UP)) if pct is not None else None,candanga=prices.get(c,{}).get('preco'),page=prices.get(c,{}).get('pagina'),catalogued=bool(cats),evidence='Fila pendente localizada' if stock else 'Catálogo local sem fila pendente localizada' if cats else 'Somente SIGTAP; demanda local não localizada',max_quantity=f[c]['quantidade_maxima'],financing=f[c]['financiamento']))
by={x['code']:x for x in records}
opt=[]
for label,cs,difficulty,decision,scope in options:
 q=[by[c] for c in cs];opt.append(dict(label=label,codes=cs,stock=sum(x['stock'] or 0 for x in q) if any(x['stock'] is not None for x in q) else None,recent=sum(x['recent'] or 0 for x in q) if any(x['recent'] is not None for x in q) else None,decision=decision,difficulty=difficulty,scope=scope))
filas=sorted([x for x in rows if x['code'] in codes],key=lambda x:-x['fila'])
links=[
['S1','Demanda','Motor preservado de 02/11/2026 10:31:47. Pedidos até 28/10/2026. Janela de agendamentos 28/10/2025–27/10/2026.','https://paineis-ext.mpdft.mp.br/extensions/mapasauderegulamentacao/mapasauderegulamentacao.html'],
['S2','Preços','Pacote oficial SIGTAP 10/2026 em cache. Não é competência 11/2026.','ftp://ftp2.datasus.gov.br/pub/sistemas/tup/downloads/'],
['S3','Candanga','Anexo oficial SIA extraído no acervo. Não gera direito automático ao pagamento.','https://www.sinj.df.gov.br/sinj/TextoArquivoDiario.aspx?id_file=b1ab0081-31d9-3075-89ba-381ea030182a'],
['S4','Nuclear','Regulamento de funcionamento dos serviços nucleares.','https://anvisalegis.datalegis.net/action/ActionDatalegis.php?acao=abrirTextoAto&numeroAto=00000038&tipo=RDC&valorAno=2008&orgao=RDC%2FDC%2FANVISA%2FMS'],
['S5','Endoscopia','RDC 6/2013, requisitos de funcionamento, recuperação e processamento.','https://anvisalegis.datalegis.net/action/ActionDatalegis.php?acao=abrirTextoAto&cod_menu=9434&cod_modulo=310&numeroAto=00000006&orgao=RDC%2FDC%2FANVISA%2FMS&seqAto=000&tipo=RDC&valorAno=2013'],
['S6','Colonoscopia SES','Nota técnica: acesso à fila específica com anestesia. Descreve HBDF como executor naquele documento, não prova exclusividade atual.','https://www.saude.df.gov.br/documents/37101/0/Nota%2BT%C3%A9cnica%2BN.%C2%BA%2B1-2024%2B%E2%80%93%2BSES-SAIS-DUAEC-GESCIR-CATC%2BRegulacao%2Bde%2BExame%2BDe%2BColonoscopia%2Bcom%2BAnestesia%2B-%2BSISREGIII%2Bc%C3%B3digo%2B0113006.pdf/d9d14740-044f-5053-8ca9-9f12c33c2763?t=1732795679246'],
['S7','SES pediatria','HCB março/2026: oferta registrada de EEG, ENMG, espirometria e outros.','https://www.hcb.org.br/arquivos/downloads/1_relatorio_de_gestao_mensal_marco_de_2026.pdf'],
['S8','Sono','Distinção entre tipos I e III em protocolo de outra rede; não é regra de faturamento DF.','https://sites.usp.br/guiacseb/wp-content/uploads/sites/943/2025/01/PROTOCOLO-POLISSONOGRAFIA.pdf'],
['S9','Gastrocentro','Oferta privada publicada de endoscopia e colonoscopia em Brasília.','https://clinicagastrocentro.com.br/'],
['S10','Clinar','Oferta privada publicada de polissonografia e função pulmonar.','https://www.clinar.com.br/'],
['S11','MedSono','Oferta privada publicada de PSG laboratorial e domiciliar em Brasília.','https://www.medsono.com.br/'],
['S12','INNEB','Oferta publicada de ENMG em Brasília; validar CNPJ e unidade da proposta.','https://inneb.com.br/exame-eletroneuromiografia/'],
['S13','HOB','Oferta publicada de exames oftalmológicos; disponibilidade depende da unidade.','https://www.hobr.com.br/servicos/exames'],
['S14','Occhio','Oferta publicada de OCT e campimetria no Lago Sul.','https://occhiobrasilia.com.br/'],
['S15','INMED','Oferta publicada de PAAF no Recanto das Emas.','https://inmedonline.com.br/exames/paaf'],
['S16','IRB','Catálogo de medicina nuclear; não equivale a compatibilidade SIGTAP para cada nome comercial.','https://irbmedicina.com/exames_de_medicina_nuclear/'],
['S17','IMEB','Oferta de múltiplas cintilografias em Brasília.','https://imeb.com.br/nossos_exames/cintilografia/'],
['S18','Protocolo nuclear SES','Fluxo HUB e demais contratados, antecedência de agenda e dependência de insumos; exames eletivos e hospitalares não formam o mesmo lote.','https://www.saude.df.gov.br/documents/d/saude/protocolo-de-acesso-ao-exame-de-cintilografia-pdf'],
]
data=dict(date='04/11/2026',options=opt,procedures=records,nuclear_codes=nuclear,queues=filas,sources=links,source_dates=raw['datas'],oci=sig.ler('102026',['0904010015','0904010023','0906010012','0905010035','0905010019']))
(O/'dados_leque.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
(O/'manifesto.json').write_text(json.dumps({'source':str(src),'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'sigtap':str(sig.pacote('102026')),'sigtap_sha256':hashlib.sha256(sig.pacote('102026').read_bytes()).hexdigest()},indent=2))
print('OPÇÕES',len(opt),'CÓDIGOS',len(records),'NUCLEAR',len(nuclear),'FILAS NOMINAIS',len(filas))
for x in opt:print(x['label'],x['stock'],x['recent'])
