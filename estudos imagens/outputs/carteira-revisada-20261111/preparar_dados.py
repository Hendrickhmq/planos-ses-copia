import csv, json, re, unicodedata, hashlib
from pathlib import Path

HERE=Path(__file__).parent
ROOT=Path('/Users/hendrick/Projetos/planos-ses')
P=ROOT/'planos/redacao_04'
raw=json.loads((P/'dados/fontes/mapa_social_20261102_imagem_bruto/coleta_20261102.json').read_text())
original=json.loads(Path('/tmp/carteira_audit_extract.json').read_text())
cells={s['sheet']:{c['cell']:c for row in s['rows'] for c in row} for s in original}
def value(sheet,cell): return cells[sheet][cell]['value']
def norm(s):return re.sub(r'\s+',' ',''.join(x for x in unicodedata.normalize('NFD',s) if not unicodedata.combining(x))).strip().upper()
prices={r['codigo_sigtap']:float(r['valor']) for r in csv.DictReader((HERE/'candanga_oficial.csv').open()) if r['modalidade']=='SIA' and r['valor']}

# Contagens agregadas efetivamente lidas no painel durante a revisão anterior, neste mesmo dia.
live_raw=[
('063. TC DO ABDOMEN SUPERIOR ADULTO C/CONTRASTE S/SEDACAO',3522),
('111. TC DE PELVE OU BACIA ADULTO C/CONTRASTE S/SEDACAO',3104),
('055. TC DO TORAX ADULTO C/CONTRASTE S/SEDACAO',1978),
('119. TC DE PESCOCO ADULTO C/CONTRASTE S/SEDACAO',403),
('061. TC DO ABDOMEN SUPERIOR ADULTO S/CONTRASTE S/SEDACAO',23),
('109. TC DE PELVE OU BACIA ADULTO S/CONTRASTE S/SEDACAO',20),
('053. TC DO TORAX ADULTO S/CONTRASTE S/SEDACAO',89),
('029. TC DE CRANIO ADULTO S/CONTRASTE S/SEDACAO',36),
('ECOGRAFIA DE MAMAS - BILATERAL',12874),('ECOGRAFIA TRANSVAGINAL',9251),
('ECOGRAFIA DE ABDOMEN TOTAL ADULTO',10042),('ECOGRAFIA DE ABDOMEN TOTAL INFANTIL',439),
('ULTRASONOGRAFIA DE PAREDE ABDOMINAL',3318),('ECOGRAFIA DE ABDOMEN SUPERIOR ADULTO',2238),
('ECOGRAFIA DE BOLSA ESCROTAL ADULTO',713),('ECOGRAFIA DE BOLSA ESCROTAL INFANTIL',229),
('ECOGRAFIA DO APARELHO URINARIO (RINS, BEXIGA) ADULTO',3694),('ULTRASSONOGRAFIA RENAL',72),
('ECOGRAFIA DO APARELHO URINARIO (RINS, BEXIGA) INFANTIL',278),
('ECOGRAFIA DE PROSTATA ( VIA ABDOMINAL )',2981),('ECOGRAFIA DE TIREOIDE ADULTO',2906),
('ULTRA-SONOGRAFIA DOPPLER DE TIREOIDE',813),('ECOGRAFIA DE TIREOIDE INFANTIL',61),
('ULTRA-SONOGRAFIA DOPPLER VENOSO - MMII ( BILATERAL)',9989),
('ULTRA-SONOGRAFIA DOPPLER ARTERIAL - MMII (BILATERAL)',1799),('ECOGRAFIA DE PARTES MOLES',3081)]
live={norm(n):v for n,v in live_raw}
candidates=[]
for r in range(5,29):
    if r in (18,27):continue
    candidates.append(dict(id=f'V2-{r}',name=value('Escolhidos',f'A{r}'),mod=value('Escolhidos',f'B{r}'),
      code=value('Escolhidos',f'C{r}'),price=float(value('Escolhidos',f'E{r}')),
      minutes=float(value('Escolhidos',f'F{r}')),cost=float(value('Escolhidos',f'E{r}'))*(1-float(value('Escolhidos',f'G{r}'))),
      condition='livre',note=value('Escolhidos',f'M{r}')))
for c in candidates:
    if c['id']=='V2-16':
        c.update(name='US de parede abdominal (estruturas superficiais)',code='02.05.02.006-2',price=70.97,note='Código de planejamento pela Deliberação DF 16/2025. Cadastro observado permanece em abdômen total. Confirmar no instrumento; 20 min e custo da v2 preservados.')
    if c['id']=='V2-28':
        c.update(name='US de estruturas superficiais: partes moles, inguinal, pescoço e axilas',note='Excluídos quadril e coluna infantis até conferência de CID/escopo do IEV; demais indicações ainda sujeitas à regulação.')
base_cost=115.61*(1-float(value('Escolhidos','G18')))
bilat_cost=115.61*(1-float(value('Escolhidos','G27')))
for ident,name,mins,cost,cond,note in [
 ('D-CAR','Doppler de carótidas e vertebrais',20,base_cost,'livre','Mesmo código 02.05.01.004-0; não é intercambiável com exame de membros.'),
 ('D-REN','Doppler de artérias renais',20,base_cost,'livre','Separado de carótidas. Usa a referência de 20 min/custo já empregada para este grupo na v2.'),
 ('D-AOR','Doppler de aorta abdominal e vasos ilíacos',20,base_cost,'livre','Fila própria e mesmo código vascular. Referência de 20 min herdada do grupo extra membros.'),
 ('D-MMII-V','Doppler venoso dos membros inferiores bilateral',40,bilat_cost,'bilateral','Duas unidades por pedido somente no cenário autorizado; não multiplicar por vasos.'),
 ('D-MMII-A','Doppler arterial dos membros inferiores bilateral',40,bilat_cost,'bilateral','Não transformar pedido venoso em arterial. Indicação e laudo devem corresponder ao realizado.'),
 ('D-MMSS-V','Doppler venoso dos membros superiores bilateral',40,bilat_cost,'bilateral','Membros superiores: estavam dentro do grupo antigo de 12.043. Mesma referência de custo bilateral.'),
 ('D-MMSS-A','Doppler arterial dos membros superiores bilateral',40,bilat_cost,'bilateral','Membros superiores; cenário separado de MMII.')]:
    candidates.append(dict(id=ident,name=name,mod='US',code='02.05.01.004-0',price=115.61,minutes=mins,cost=cost,condition=cond,note=note))

def classify(f,universe):
    n=norm(f['nome']); cd=f['codigo']
    if 'EMERG' in n:return '', 'Emergência',0
    if 'C/SEDACAO' in n:return '', 'Sedação',0
    if cd=='02.05.01.004-0':
        if 'MMII' in n:return ('D-MMII-V' if 'VENOSO' in n else 'D-MMII-A'),'Doppler bilateral condicionado',0
        if 'MMSS' in n:return ('D-MMSS-V' if 'VENOSO' in n else 'D-MMSS-A'),'Doppler bilateral condicionado',0
        if 'CAROTID' in n or 'VERTEBRAIS' in n:return 'D-CAR','Candidato vascular',0
        if 'RENAIS' in n:return 'D-REN','Candidato vascular',0
        if 'AORTA' in n:return 'D-AOR','Candidato vascular',0
        if 'TRANSVAGINAL' in n:return '', 'Doppler transvaginal: avaliar GIN/IEV',0
        if any(x in n for x in ['MIE','MID','M I D','M I E','M S D','MEMBRO',' DE MI']):return '', 'Doppler unilateral: tempo e indicação não revistos',0
        return '', 'Doppler genérico/outra região: esclarecer indicação',0
    if universe=='ultrassonografia':
        if cd=='02.05.02.003-8' and n=='ECOGRAFIA DE ABDOMEN SUPERIOR ADULTO':return 'V2-13','Candidato',0
        if cd=='02.05.02.004-6':
            if n=='ECOGRAFIA DE ABDOMEN TOTAL ADULTO':return 'V2-15','Candidato',0
            if n=='ECOGRAFIA DE ABDOMEN TOTAL INFANTIL':return 'V2-23','Candidato',0
            if 'PAREDE ABDOMINAL' in n:return 'V2-16','Parede abdominal: código de planejamento corrigido',0
        if cd=='02.05.02.005-4':
            if 'INFANTIL' in n:return 'V2-24','Candidato',0
            if n in ('ECOGRAFIA DO APARELHO URINARIO (RINS, BEXIGA) ADULTO','ULTRASSONOGRAFIA RENAL'):return 'V2-17','Candidato',0
        if cd=='02.05.02.007-0':
            if n=='ECOGRAFIA DE BOLSA ESCROTAL ADULTO':return 'V2-14','Candidato',0
            if n=='ECOGRAFIA DE BOLSA ESCROTAL INFANTIL':return 'V2-25','Candidato',0
        if cd=='02.05.02.012-7':
            if n=='ECOGRAFIA DE TIREOIDE INFANTIL':return 'V2-26','Candidato',0
            if n in ('ECOGRAFIA DE TIREOIDE ADULTO','ULTRA-SONOGRAFIA DOPPLER DE TIREOIDE'):return 'V2-21','Candidato',0
        if cd=='02.05.02.009-7' and n=='ECOGRAFIA DE MAMAS - BILATERAL':return 'V2-22','Candidato',0
        if cd=='02.05.02.010-0' and n=='ECOGRAFIA DE PROSTATA ( VIA ABDOMINAL )':return 'V2-20','Candidato',0
        if cd=='02.05.02.018-6' and n=='ECOGRAFIA TRANSVAGINAL':return 'V2-19','Candidato com reserva IEV',4000
        if cd=='02.05.02.006-2':
            if any(x in n for x in ['COLUNA LOMBAR','USG QUADRIL','COXO-FEMURAL E INFANTIL','COXO-FEMURAL D INFANTIL','REGIAO LOMBAR']):return '', 'Quadril/coluna infantil: conferir OCI e CID',0
            if any(x in n for x in ['PARTES MOLES','REGIAO INGUINAL','PESCOCO','CERVICAL','SUBMANDIBULARES','AXILA']):return 'V2-28','Superficial: separar por indicação',0
            return '', 'Articulação/ortopedia: conferir IEV',0
        if cd=='02.05.02.016-0':return '', 'US pélvica: margem negativa na referência',0
        if cd=='02.05.02.017-8':return '', 'Transfontanela: decisão anterior de exclusão',0
        return '', 'Outra equipe/indicação de ultrassom',0
    if universe=='tomografia':
        if 'ANGIO' in n:return '', 'Angiotomografia: decisão anterior de exclusão',0
        mapping={'061.':5,'063.':9,'109.':6,'111.':10,'053.':7,'055.':11,'029.':8,'119.':12}
        for pref,r in mapping.items():
            if n.startswith(pref):return f'V2-{r}','Candidato com recorte histórico' if r in (6,10) else 'Candidato',1 if r==6 else 5 if r==10 else 0
        if cd=='02.06.01.009-5':return '', 'PET-CT: equipamento específico',0
        if 'CONE BEAN' in n or 'CONE BEAM' in n:return '', 'Cone beam: equipamento específico',0
        if cd=='02.06.01.006-0':return '', 'TC órbitas/sela: fora da seleção, avaliar separadamente',0
        if cd in ('02.06.01.001-0','02.06.01.002-8','02.06.01.003-6','02.06.02.001-5','02.06.03.002-9','02.06.02.002-3'):return '', 'TC musculoesquelética: conferir IEV',0
        return '', 'Outra TC não selecionada',0
    return '', 'Outra modalidade/equipamento',0

allrows=[]
for universe,pano in raw['panorama'].items():
 for f in pano['filas']:
    cid,reason,reserve=classify(f,universe)
    allrows.append(dict(**f,universe=universe,candidate=cid,reason=reason,reserve=reserve,
       current=live.get(norm(f['nome'])),source_date='11/11/2026' if norm(f['nome']) in live else '02/11/2026',
       native_price=prices.get(f['codigo']),code_stock=sum(x['fila'] for p in raw['panorama'].values() for x in p['filas'] if x['codigo']==f['codigo'])))
bycode={}
for f in allrows:bycode.setdefault(f['codigo'],[]).append(f)
rumo={x['codigo']:x for x in raw['rumo']}
codes=[]
for cd,rows in sorted(bycode.items()):
    r=rumo.get(cd,{})
    codes.append(dict(code=cd,name=r.get('fila_maior',rows[0]['nome']),stock=sum(f['fila'] for f in rows),
      entries=r.get('entrantes_12m'),offer12=r.get('oferta_12m'),offer3=r.get('oferta_media_3m'),
      offer3annual=4*sum(x[2] for x in raw['por_codigo']['oferta']['linhas'] if x[0]==cd and x[1] in ('2026-07','2026-08','2026-09')),
      real12=r.get('realizados_12m'),real3annual=4*sum(x[3] for x in raw['por_codigo']['oferta']['linhas'] if x[0]==cd and x[1] in ('2026-07','2026-08','2026-09')),
      weight_stock=sum(f['fila'] for f in rows),weight_offer=sum(f['agendadas_12m'] or 0 for f in rows),price=prices.get(cd)))

# Organização dos candidatos por margem de referência, sem habilitar o cenário bilateral por conta própria.
for c in candidates:c['reference_margin']=(c['price']-c['cost'])/c['price']
candidates.sort(key=lambda c:(-c['reference_margin'],c['name']))
out=dict(candidates=candidates,filas=allrows,codes=codes,original=original,
  metadata=dict(stock_update='11/11/2026 parcial; demais filas 02/11/2026',flows='02/11/2026; entradas e agendamentos por código',
    original_sha256=hashlib.sha256((P/'estudos/carteira_final_v2_20261111.xlsx').read_bytes()).hexdigest(),
    source='https://paineis-ext.mpdft.mp.br/extensions/mapasauderegulamentacao/mapasauderegulamentacao.html'))
(HERE/'dados_modelo.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
print(json.dumps({'filas':len(allrows),'codigos':len(codes),'candidatos':len(candidates),'estoques_11_11':sum(f['current'] is not None for f in allrows),
 'doppler_0040':sum(f['fila'] for f in allrows if f['codigo']=='02.05.01.004-0'),
 'doppler_grupos':{c['id']:sum(f['fila'] for f in allrows if f['candidate']==c['id']) for c in candidates if c['id'].startswith('D-')}},ensure_ascii=False))
