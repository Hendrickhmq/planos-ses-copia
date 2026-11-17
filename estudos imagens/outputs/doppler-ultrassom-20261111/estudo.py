from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
src=ROOT/'tmp/estudo-integrado/fontes/mapa_social_20261102_inventario_bruto/motor_20261102.json'
d=json.loads(src.read_text())
t=next(iter(d['panorama'].values()))['filas']
rows=[dict(zip(t['cols'],r)) for r in t['linhas']]
cat=json.loads((ROOT/'tmp/estudo-integrado/classificacao.json').read_text())
keys={(r['nome'],r['codigo']) for r in cat if r['modalidade']=='Ultrassonografia e Doppler'}
us=[r for r in rows if (r['nome'],r['codigo']) in keys]
prices={r['codigo']:r for r in json.loads((ROOT.parent/'outputs/estudo_imagem_candanga_20261101/tabela_oficial_sia.json').read_text())}
groups={}
for r in us:
    c=r['codigo'].zfill(10)
    g=groups.setdefault(c,dict(codigo=c,nome=prices[c]['nome'],pendentes=0,recentes=0,candanga=prices[c]['preco']))
    g['pendentes']+=r['fila'];g['recentes']+=r['fila_viva']
live=[dict(nome='10. ECODOPPLER DE CAROTIDAS',antes=4143,hoje=4322,pessoas=4322,devolvidas=2751),dict(nome='ULTRA-SONOGRAFIA DOPPLER VENOSO - MMII ( BILATERAL)',antes=10045,hoje=9989,pessoas=9986,devolvidas=597),dict(nome='ULTRA-SONOGRAFIA DOPPLER ARTERIAL - MMII (BILATERAL)',antes=1800,hoje=1799,pessoas=1799,devolvidas=333)]
def br(v,n=0):return f'{v:,.{n}f}'.replace(',','X').replace('.',',').replace('X','.')
costh=(5500+5918)/168+100
assert sum(x['pendentes'] for x in groups.values())==83041
assert sum(x['recentes'] for x in groups.values())==57945
assert round(costh*40/60+3,2)==114.98
table='\n'.join(f"| {g['nome']} ({g['codigo']}) | {br(g['pendentes'])} | {br(g['recentes'])} | {br(g['candanga'],2)} |" for g in sorted(groups.values(),key=lambda x:-x['pendentes']))
lt='\n'.join(f"| {r['nome']} | {br(r['antes'])} | {br(r['hoje'])} | {br(r['hoje']-r['antes'])} | {br(r['devolvidas'])} |" for r in live)
costrows=[]
for name,price,minutes in [('Doppler de carótidas',115.61,20),('Doppler de membros bilateral',115.61,40),('US de abdômen total',117.51,20),('US do aparelho urinário',90.53,15),('US transvaginal',83.77,15),('US de tireoide',64.07,15),('US mamária bilateral',70.97,20),('US pélvica ginecológica',43.41,15)]:
    c=costh*minutes/60+3
    costrows.append(dict(nome=name,preco=price,minutos=minutes,custo=c,folga=price-c,margem=(price-c)/price))
ct='\n'.join(f"| {r['nome']} | {r['minutos']} | {br(r['preco'],2)} | {br(r['custo'],2)} | {br(r['folga'],2)} | {br(100*r['margem'],1)}% |" for r in costrows)
text=f'''# Doppler e ultrassom: demanda, Candanga e viabilidade

Estudo de 11/11/2026. Objetivo: orientar a escolha da carteira de exames. Valores em reais.

## Parecer

Há demanda relevante. Doppler de carótidas apresenta melhor relação entre preço e tempo que Doppler bilateral de membros. Na estrutura de custos interna, membros bilateral a R$ 115,61 por pedido e 40 minutos deixa somente R$ 0,63 por exame antes dos custos não incluídos. Eu priorizaria carótidas, abdômen total/superior e aparelho urinário; manteria membros condicionado a um custo contratado menor ou a uma regra de remuneração formalmente confirmada.

Essa é uma recomendação de composição financeira da carteira. A prioridade clínica dos pacientes permanece com a regulação.

## O que foi atualizado hoje

Consulta direta ao [Mapa Social da Saúde/MPDFT](https://paineis-ext.mpdft.mp.br/extensions/mapasauderegulamentacao/mapasauderegulamentacao.html), fonte SISREG/DATASUS. O cabeçalho mostrava atualização em **11/11/2026 00:32:28**. Foram retirados os filtros de ano e consultados individualmente os três nomes abaixo. Pendentes vêm do indicador Solicitações; devolvidas vêm de indicador separado e não foram somadas ou subtraídas dos pendentes.

| Fila nominal | Pendentes em 02/11 | Pendentes em 11/11 | Variação | Devolvidas em 11/11, fora da fila |
|---|---:|---:|---:|---:|
{lt}

Venoso bilateral tem 9.986 pessoas para 9.989 pedidos. As duas filas de pernas somam 11.788 pedidos, mas não necessariamente 11.788 pessoas distintas. Carótidas acima é a fila principal, não a união de todos os nomes antigos de carótidas/vertebrais. As três filas não esgotam o código vascular.

A queda líquida de uma fila não mede exames realizados: há entradas, saídas e ajustes. Não foi feita uma nova extração integral de ultrassom em 11/11. Tampouco se usaram os tempos médios dos cartões atuais: os indicadores de espera geral e de pendentes mostraram recortes diferentes, que exigiriam auditoria própria.

## Panorama completo disponível de ultrassom

Base preservada: recarga **02/11/2026 10:31:47**, solicitações até **28/10/2026**. São **83.041 pedidos na soma de 139 filas nominais**, dos quais **57.945** com solicitação nos últimos 24 meses (desde 28/10/2024). Aproximadamente 30% são mais antigos. Não são pessoas únicas, nem uma nova fotografia de 11/11. Solicitação recente não garante contato, indicação ainda válida ou disponibilidade para comparecer.

| Procedimento/código | Pendentes em 02/11 | Últimos 24 meses | Candanga R$ |
|---|---:|---:|---:|
{table}

O agrupamento é pelo código cadastrado. “Articulação” contém nomes locais que podem incluir partes moles; “abdômen total” inclui parede abdominal. Conferir o nome exato, a indicação e a compatibilidade antes de contratar. Ecocardiografia foi tratada separadamente e não integra esse total. A fila total bruta também não desconta reservas de outras carteiras, OCI, exclusões ou sobreposições dos planos em andamento.

No código vascular 0205010040 eram 16.844 pendentes em 02/11, 12.143 recentes e 12.675 agendamentos na janela de 28/10/2025 a 27/10/2026. Agendamento não equivale a execução. No venoso bilateral de pernas eram 10.045 pendentes e 3.496 agendamentos em 12 meses: estoque equivalente a 2,87 anos desse ritmo bruto, sem considerar entradas futuras. Isso dimensiona a pressão, não prevê tempo individual de atendimento.

## Como paga na Candanga

O anexo oficial preservado, documento SES/DF SEI 212117347, página 5, registra **0205010040 — Ultrassonografia Doppler colorido de vasos: R$ 115,61**. Abdômen total R$ 117,51; abdômen superior R$ 101,27; aparelho urinário R$ 90,53. Estes são os valores oficiais, e não o “Valor Máximo” da planilha comparativa de agosto. Aquela versão comparativa contém valores muito diferentes e não deve alimentar esta decisão.

Pela [Deliberação CG-SES 46/2026](https://www.sinj.df.gov.br/sinj/Norma/08cdc67f1b9a46158271100a13d7d382/ses_cg_dlb_46_2026.html), arts. 3–6 e 12–14, a Candanga é a referência total, formada por SIGTAP mais complementação distrital. Não somar o SIGTAP ou um incremento federal novamente ao preço Candanga. A aplicação depende do instrumento, orçamento, regulação e produção validada; contratos anteriores precisam de adequação formal. O valor tabelado não comprova prazo de recebimento ou histórico de pagamento. Não foram localizados neste estudo dados de glosas, prazo efetivo ou um contrato específico que garanta esta receita.

Se a fonte for emenda federal, a complementação e sua fonte precisam estar previstas no arranjo autorizado. Não presumir que a existência da tabela distrital permita usar qualquer fonte para pagar o total.

## Bilateralidade: não contar receita em dobro na base

A carteira final v2 de 11/11 condiciona Doppler de membros à hipótese de dois exames por pedido bilateral. Trata-se de condição pendente, não de uma autorização de faturamento.

A ficha SIGTAP preservada da competência 10/2026 permite até cinco procedimentos por paciente/competência no BPA-I e informa que as quantidades independem do número de vasos estudados. Isso **não demonstra que um pedido bilateral deva gerar duas unidades**. O limite de registro não deve ser usado como multiplicador automático. O enquadramento efetivo exige confirmação do gestor/auditoria, amparada nas regras do procedimento e no instrumento de contratação. Não foi confirmada ficha nova de 11/2026 nem regra local de pagamento em dobro nesta pesquisa.

Por prudência de cálculo, adotei R$ 115,61 pelo exame bilateral. R$ 231,22 é apenas uma hipótese caso duas unidades distintas sejam legalmente reconhecidas e autorizadas; não integra o cenário-base.

## Vale a pena executar? Conta por exame

Premissas do estudo interno revisto em 09/11: sala/aparelho R$ 5.500 por mês; dois auxiliares R$ 5.918 por mês; 168 horas produtivas/mês; médico R$ 100/h; insumos R$ 3/exame. Custo por exame = [(5.500 + 5.918)/168 + 100] × minutos/60 + 3.

Os tempos são premissas de planejamento do acervo, não tempos clínicos universais nem produtividade garantida. Médico, laudo e protocolo devem caber no tempo orçado.

| Exame | Minutos | Receita | Custo estimado | Folga | Folga/receita |
|---|---:|---:|---:|---:|---:|
{ct}

**Folga não é lucro.** O modelo não adiciona recepção/gestão, que o estudo anterior alocou fora dos exames, nem explicita todos os tributos, capital de giro, glosas e perdas. Os custos são premissas internas, não cotações atuais vinculantes. Se for convênio com prestação de contas, a folga tampouco equivale a lucro distribuível.

Com 40 minutos, membros rende R$ 173,42 de receita bruta por hora ocupada; carótidas de 20 minutos rende R$ 346,83. O custo operacional antes dos insumos é R$ 167,96/h. Isso explica a diferença apesar do mesmo código/preço.

O equilíbrio de membros ocorre em aproximadamente **40,23 minutos**, nesse custo e com ocupação integral das 168 horas consideradas. Logo, quase não há espaço para atraso ou ociosidade. Se toda a equipe e estrutura forem pagas pelo tempo disponível e apenas 80% dele produzir exames faturáveis, o custo de um exame de 40 minutos sobe a cerca de R$ 142,97. Esse é um cenário de sensibilidade, não uma taxa de faltas observada.

Alternativa já estudada no acervo: médico a R$ 1.000 por lote de 30 exames, equivalente a R$ 33,33/exame. Mantendo 40 minutos, sala, auxiliares e insumos, o custo cai para **R$ 81,64** e deixa **R$ 33,97 (29,4%)**. É uma hipótese de negociação: depende de o profissional aceitar o exame bilateral completo, laudo e responsabilidade por esse preço. Para reservar 20% da receita depois de todos os custos, o teto de custo total seria R$ 92,49 por exame; não é uma margem obrigatória.

## Decisão prática para a carteira

1. **Priorizar carótidas e ultrassons de abdômen/urinário.** Boa folga no modelo e demanda identificada, respeitando reservas e prioridade clínica.
2. **Doppler de membros: negociar antes de ampliar.** A necessidade assistencial é expressiva, mas médico por hora e 40 minutos não oferecem segurança financeira a R$ 115,61. Procurar preço fechado do prestador para bilateral completo ou remuneração médica por exame com qualidade preservada.
3. **Não fechar orçamento contando bilateralidade dobrada.** Confirmar por escrito unidade, protocolo arterial/venoso, lateralidade, quantidade autorizada e regras de registro/auditoria.
4. **US mamário e tireoide têm menos folga; pélvico fica negativo no modelo.** A pélvica já havia sido excluída por decisão registrada em 09/11. Articulação tem grande estoque bruto, mas a carteira atual a trata com restrição por possível sobreposição com OCI de ortopedia: não reutilizar todo o estoque como disponível.
5. **Meta inicial deve usar demanda validada.** Atualizar extração integral, retirar duplicidades/reservas, verificar contatos/indicações e obter capacidade/custo por protocolo antes de prometer zerar filas.

## Fontes locais e rastreabilidade

- `Tabela SUS Candanga.xlsx`, aba Tabela SUS Candanga, linha 266: código 0205010040, SIA, R$ 115,61, página oficial 5. Conferido na planilha original, sem alterá-la.
- `tmp/estudo-integrado/fontes/mapa_social_20261102_inventario_bruto/motor_20261102.json`: contagens agregadas e datas.
- `tmp/estudo-integrado/classificacao.json`: classificação das modalidades.
- `../outputs/estudo_imagem_candanga_20261101/tabela_oficial_sia.json`: extração do anexo oficial para os demais preços.
- `../planos/redacao_04/estudos/estudo_readequacao_candanga_margem_20261109.md`: custos e tempos internos.
- `../planos/redacao_04/estudos/gerar_carteira_final_v2_20261111.py`: condição sobre membros e restrição da articulação na carteira atual.
- `revisao_carteira1_20261102/fontes_preservadas/dados/fontes/sigtap_0205010040_102026.md`: ficha e descrição de registro preservadas.

Os caminhos acima são relativos à pasta de trabalho estudos imagens. A consulta de 11/11 usou somente indicadores agregados; não foram exportados dados individuais de pacientes.
'''
(OUT/'Estudo Doppler e ultrassom.md').write_text(text)
(OUT/'dados.json').write_text(json.dumps(dict(data='2026-11-11',painel_atualizacao='11/11/2026 00:32:28',filas_atuais=live,base_0211=list(groups.values()),custos=costrows),ensure_ascii=False,indent=2))
print(OUT/'Estudo Doppler e ultrassom.md')
print('Modelo: hora',costh,'membros por exame medico',((5500+5918)/168)*40/60+3+1000/30)
