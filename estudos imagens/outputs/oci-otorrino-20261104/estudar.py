from pathlib import Path
import json,sys,csv,zipfile,hashlib
O=Path(__file__).resolve().parent;ROOT=O.parents[1];REPO=ROOT.parent
sys.path.insert(0,str(REPO/'ferramentas'));import ler_tabela_unificada as sig
src=ROOT/'tmp/estudo-integrado/fontes/mapa_social_20261102_inventario_bruto/motor_20261102.json'
r=json.loads(src.read_text());t=next(iter(r['panorama'].values()))['filas'];allrows=[dict(zip(t['cols'],x)) for x in t['linhas']]
names=['CONSULTA EM OTORRINOLARINGOLOGIA - GERAL','CONSULTA EM ATENCAO A SAUDE AUDITIVA - MEDIA E ALTA COMPLEXIDADE','VIDEOENDOSCOPIA  NASAL  FLEXIVEL','VIDEOENDOSCOPIA NASAL RIGIDA','VIDEOLARINGOSCOPIA','AUDIOMETRIA E IMITANCIOMETRIA – ATÉ 7 ANOS','AUDIOMETRIA E IMITANCIOMETRIA – 8 A 64 ANOS','AUDIOMETRIA E IMITANCIOMETRIA – ACIMA DE 65 ANOS','POTENCIAL EVOCADO AUDITIVO BERA – ATÉ 4 ANOS','POTENCIAL EVOCADO AUDITIVO BERA – ACIMA DE 5 ANOS','VECTOELETRONISTAGMOGRAFIA(VENG)','TESTES DE PROCESSAMENTO AUDITIVO','VIDEOENDOSCOPIA DA DEGLUTICAO  ( VED)','CONSULTA PARA RESPIRADOR BUCAL','CONSULTA EM  RINOLOGIA']
rows=[next(x for x in allrows if x['nome']==n) for n in names]
codes=['0904010015','0904010023','0904010031'];f=sig.ler('102026',codes);prices={x['codigo']:x for x in json.loads((REPO/'outputs/estudo_imagem_candanga_20261101/tabela_oficial_sia.json').read_text())}
details={}
with zipfile.ZipFile(sig.pacote('102026')) as z:
 dt={x['CO_DETALHE']:x['NO_DETALHE'] for x in sig.linhas(z,'tb_detalhe')}
 for c in codes:details[c]=[dict(code=x['CO_DETALHE'],name=dt[x['CO_DETALHE']]) for x in sig.linhas(z,'rl_procedimento_detalhe') if x['CO_PROCEDIMENTO']==c]
cid_lower={x['nome']:sum(n for c,n in x['cid_principais'] if c in f['0904010031']['cid_principal']) for x in rows}
data={'date':'04/11/2026','snapshot':r['datas'],'queues':rows,'oci':f,'details':details,'candanga':{c:prices[c] for c in codes},'nasopharynx_top5_cid_count':cid_lower,'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest()}
(O/'dados_otorrino.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
with (O/'Filas de otorrino.csv').open('w',encoding='utf-8-sig',newline='') as out:
 w=csv.writer(out,delimiter=';');w.writerow(['Fila','Código local','Pedidos pendentes','Pedidos dos últimos 24m','Pessoas nessa fila','Espera mediana dias','Idade mediana anos','Agendados 28/10/2025–27/10/2026','Pedidos devolvidos, fora da fila']);
 for x in rows:w.writerow([x['nome'],x['codigo'].zfill(10),x['fila'],x['fila_viva'],x['pessoas'],round(x['espera_mediana'],1),x['idade_mediana'],x['agendadas_12m'],x['devolvidas']])
def br(v):return f'{v:,.2f}'.replace(',','X').replace('.',',').replace('X','.')
s='''# Filas de otorrino e execução de OCI

Análise de 04/11/2026. Demanda do Mapa Social preservada em 02/11/2026, recarga 10:31:47, pedidos até 28/10/2026. Não é consulta atualizada do painel em 04/11. Valores e atributos conferidos no pacote oficial SIGTAP 10/2026.

## Conclusão

**A OCI 09.04.01.003-1, nasofaringe/orofaringe, é a primeira candidata a aprofundar.** Há uma fila endoscópica importante e o acervo do convênio IEV 030977/2026 contempla as duas OCI auditivas, sem a 003-1 identificada naquele instrumento. Isso não comprova ausência de outro contrato para nasofaringe ou disponibilidade de todos os pedidos para um novo executor.

O acervo já contém um plano de nasofaringe em redacao_05, com recurso de R$ 1.502.687,00 e meta de 3.504 OCI. Trata-se de plano em elaboração no estado preservado, não comprovação de contratação ou execução. A identidade da proposta/fonte deve ser conciliada antes de tratar essa frente como uma segunda aplicação de outro recurso de R$ 1,5 milhão.

## As três OCI

| Código | Linha | Valor SA SIGTAP 10/2026 | Referência Candanga extraída | Percurso e regra essencial |
|---|---|---:|---:|---|
| 0904010015 | Avaliação inicial de déficit auditivo | R$ 100,00 | R$ 127,80 | Consulta especializada e avaliação audiológica. Audiometria tonal 0211070041 obrigatória. Im itanciometria consta como compatível na tabela. |
| 0904010023 | Progressão da avaliação de déficit auditivo | R$ 471,57 | R$ 191,71 | Consulta, audiometria tonal 0211070041 e potencial auditivo 0211070262 obrigatório. O BERA local 0211050113 é apenas compatível, não substitui automaticamente o componente obrigatório. |
| 0904010031 | Avaliação diagnóstica de nasofaringe/orofaringe | R$ 393,55 | R$ 255,61 | Consulta e laringoscopia 0209040025 ou videolaringoscopia 0209040041. Atributo 072 exige um dos exames executado e registrado na APAC. |

As referências financeiras não se somam. Os valores Candanga menores que o SIGTAP atualizado da 002-3 e 003-1 mostram uma defasagem entre os referenciais; não permitem escolher automaticamente o maior nem corrigir a tabela distrital por conta própria. Não foram localizados nesta pesquisa ato de atualização específico desses três valores distritais ou proposta comercial completa. O valor efetivamente aplicável depende do instrumento, fonte e reconhecimento da SES.

A [Portaria SAES/MS 4.795/2026](https://www.in.gov.br/web/dou/-/portaria-saes/ms-n-4.795-de-26-de-agosto-de-2026-729109381), preservada no acervo e relacionada na [página oficial do Ministério](https://www.gov.br/saude/pt-br/composicao/saes/agora-tem-especialistas/legislacao/legislacao), atualizou valores e instituiu o atributo 072. No pacote de outubro, os dois exames endoscópicos aparecem como compatíveis individualmente, mas a exigência de um deles continua pelo atributo. Não concluir que bastaria consulta para faturar essa OCI.

O [Manual PMAE de produção](https://www.gov.br/saude/pt-br/centrais-de-conteudo/publicacoes/guias-e-manuais/2024/manual-pmae-registro-da-producao-controle-e-avaliacao.pdf) exige consulta/teleconsulta compatível e registro da OCI na APAC. Para as três OCI examinadas, a consulta presencial está entre os componentes compatíveis. O preço remunera o percurso, não gera uma cobrança adicional automática para cada componente. Eventual retorno e fechamento devem estar previstos no custo.

## Filas encontradas

Pedidos de consulta e exame podem pertencer às mesmas pessoas. Não somar esta tabela como número de pacientes ou OCI. Devolvidas para complementação estão fora da contagem pendente.

| Fila | Pedidos | Pedidos dos últimos 24m | Espera mediana, dias | Idade mediana | Agendados 12m |
|---|---:|---:|---:|---:|---:|
'''
for x in rows:s+=f"| {x['nome']} | {x['fila']} | {x['fila_viva']} | {x['espera_mediana']:.0f} | {x['idade_mediana']} | {x['agendadas_12m']} |\n"
s+='''
A janela de agendamentos é 28/10/2025–27/10/2026. São agendamentos, não exames concluídos. A fila de consulta especializada geral compartilha o mesmo código 0301010072 de inúmeras especialidades; não se deve usar o total desse código como oferta de otorrino. O mesmo cuidado vale para o código endoscópico 0209040041, que agrega descrições locais diferentes.

## Onde está a oportunidade de nasofaringe

As três filas de exame mais próximas dessa linha somam **4.382 pedidos**: nasal flexível 3.720, nasal rígida 447 e videolaringoscopia 215. Não são 4.382 OCI elegíveis nem pessoas únicas. A fila flexível tem idade mediana de oito anos, espera mediana de 622 dias e 2.210 pedidos dos últimos 24 meses: capacidade pediátrica e confirmação da indicação são centrais.

Os cinco CID principais publicados por fila identificam **ao menos 3.337 pedidos com CID J30–J39** nessas três filas: 3.063 na flexível e 274 na rígida. Na consulta geral há ao menos 1.518 pedidos desses CID entre os cinco principais, de um total de 5.471. Esses recortes são incompletos e podem se sobrepor; CID compatível orienta triagem, mas não comprova indicação, necessidade de todo o pacote ou ausência de cobertura anterior.

Respirador bucal tem 876 pedidos e rinologia 190. São frentes complementares com potencial clínico, mas estavam fora do objeto escolhido no estado preservado de redacao_05, por decisão anterior do usuário. Foram mostradas para dimensionar o universo, sem incorporá-las à meta atual. VED/deglutição, de 221 pedidos, tem perfil diferente e não deve ser incluída automaticamente apenas porque usa o mesmo código local.

O problema de mapeamento é concreto: videoendoscopia nasal aparece no SISREG como videolaringoscopia. Nome da fila e código local não bastam para comprovar que o procedimento realizado satisfará o atributo 072. O desenho assistencial e o registro devem ser validados pela SES; não se deve fazer exame sem indicação para completar faturamento.

## Linha auditiva e IEV

As três filas nominais de audiometria/imitanciometria somam 8.068 pedidos; as duas de BERA somam 4.647. Não equivalem a públicos exclusivos das OCI inicial e de progressão. Há pacientes já diagnosticados ou em reabilitação, pedidos pediátricos com outras indicações e possível sobreposição entre consulta e exame.

O convênio 030977/2026 do IEV traz 6.250 OCI iniciais a R$ 100 e 5.340 de progressão a R$ 150, preços do instrumento na época. O valor SIGTAP atual da progressão é R$ 471,57, mas isso não demonstra reajuste automático do contrato antigo. A leitura de SISREG preservada de 26/10 encontrou 80 consultas de otorrino agendadas nos locais associados ao projeto e 28 realizadas com CID compatível. **Esses números não comprovam quantas OCI foram concluídas, quantas faltam ou que toda a capacidade contratada esteja disponível para outra entidade.**

Antes de acrescentar nova compra auditiva, conciliar metas contratadas, APAC aprovadas, vigência e pedidos atribuídos a cada executor. Não subtrair consultas realizadas de metas de OCI. Também não reservar ou liberar pessoas apenas pelo CID do pedido.

As maiores filas pediátricas têm muitos CID F80/F84 e outras indicações fora do conjunto H60–H95 das duas OCI auditivas no pacote examinado. Precisam de avaliação clínica e diagnóstico correto, sem alterar CID para enquadrar faturamento. O código local de audiometria em campo livre 0211070033 também não equivale automaticamente à audiometria tonal 0211070041 exigida na OCI.

## Releitura do plano já elaborado

A coleta específica de 08/10/2026 às 21:32, filtrada por CID, encontrou 3.478 pedidos e 3.459 pessoas nas três filas endoscópicas, além de 1.988 pedidos em consulta geral. Na união de exames e consulta eram 5.402 pessoas. Outra recarga anterior do mesmo dia, usada na minuta, trazia 3.477 pessoas nos exames. Os números não devem ser misturados.

A minuta fixou 3.504 OCI a R$ 393,55: produção de R$ 1.378.999,20 mais apoio de R$ 123.600,00, total de R$ 1.502.599,20 dentro do recurso de R$ 1.502.687,00. Essa conta aritmética continua correta como cenário histórico. A justificativa de zerar a fila precisa de atualização: o levantamento de novembro tem outro recorte, não foi deduplicado por CID e não confirma quantos pacientes ainda estão indicados e descobertos. Não compare 4.382 pedidos sem filtro em novembro com 3.459 pessoas filtradas em outubro para calcular crescimento.

Se esta for outra emenda, o orçamento, apoio, proposta e objeto precisam ser próprios. Não se transplanta automaticamente a reserva de apoio aprovada para redacao_05. A presente análise não altera os planos anteriores.

## Dificuldade e viabilidade de execução

Nasofaringe precisa de médico otorrino, endoscópio adequado ao público, equipe e insumos de processamento, sala, documentação de imagem/laudo, conclusão e contrarreferência. O predomínio pediátrico muda produtividade e acolhimento. Não pressupor sedação de rotina; casos que a exijam precisam de percurso e estrutura apropriados.

Auditiva inicial requer consulta e bateria audiológica adequada, profissional habilitado e ambiente/equipamento com qualidade aferida. É operacionalmente organizável em circuito, mas R$ 100 por percurso pode ser apertado quando há retorno, perdas e custos de coordenação. A progressão remunera mais no SIGTAP, porém envolve potencial auditivo e maior dificuldade em crianças pequenas, sono, colaboração e eventual necessidade de sedação. Tarifa maior não demonstra lucro maior.

Sem cotação integral, não há margem comprovada. Solicitar preço por OCI concluída e registrada, identificando consulta, exames, conclusão, retornos necessários, insumos, processamento e perdas. O estabelecimento executor e sua vinculação ao programa precisam ser regularizados na modalidade efetivamente contratada. Financiamento FAEC na ficha não significa que a emenda federal produzirá automaticamente novo repasse FAEC. Evitar financiar duas vezes o mesmo percurso.

O acervo já contém simulação de 3.504 OCI em três polos com seis meses assistenciais: cerca de 195 concluídas por mês por polo, ou 9,7 por dia em 20 dias mensais. Com conversão hipotética de 80% da capacidade em percursos concluídos, estimavam-se 13 agendas por dia/polo. São hipóteses, não produtividade ou taxa de falta observadas, e dependem de equipe, pediatria, processamento e retornos. Não tornam três polos obrigatórios.

## Encaminhamento recomendado

Priorizar a análise de 0904010031 com consulta + exame indicado + conclusão, começando pela fila endoscópica e pela separação de adultos/crianças. Pactuar com a SES o uso dos nomes locais, os critérios de conversão para OCI e a lista de pedidos sem cobertura contratual duplicada. Cotar percurso completo em unidade já equipada antes de fechar quantidade.

Manter 0904010015 e 0904010023 como alternativas condicionadas à conciliação com o IEV. Não propor um lote para toda a fila de otorrino nem prometer que cada consulta gerará uma OCI. A oportunidade assistencial em nasofaringe é consistente; o quantitativo elegível, a capacidade e a rentabilidade ainda precisam ser demonstrados.

## Fontes e trilha

- Inventário Mapa Social preservado em 02/11/2026: motor_20261102.json, análise de 15 filas nominais sem dados pessoais.
- Pacote oficial TabelaUnificada_202610_v2610271043.zip: três OCI, compatibilidades, CID, registro e atributo 072.
- Anexo oficial Candanga SIA extraído no acervo, página 16; não confundir com valor máximo de estudos anteriores.
- redacao_05: estado.yaml, plano_v2_nasofaringe.md, dados/fontes/mapa_social_20261008.md e simulação de capacidade de 09/10.
- Planos aprovados: estudo_outros_planos_imagem_20261102.md e fonte do convênio IEV 030977/2026.
- JSON desta análise preserva as filas, fontes temporais, dados SIGTAP e hash do inventário; CSV contém a tabela para consulta.
'''
s=s.replace('Im itanciometria','Imitanciometria')
(O/'Estudo das filas e OCI de otorrino.md').write_text(s)
assert sum(x['fila'] for x in rows[2:5])==4382
assert sum(cid_lower[x['nome']] for x in rows[2:5])==3337
assert sum(x['fila'] for x in rows[5:8])==8068
assert sum(x['fila'] for x in rows[8:10])==4647
assert round(3504*393.55+123600,2)==1502599.20
print('15 filas, 3 OCI; recortes e orçamento histórico conferidos. Relatório:',len(s.split()),'palavras')
