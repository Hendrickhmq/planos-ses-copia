from pathlib import Path
import json
O=Path(__file__).resolve().parent;d=json.loads((O/'dados_ampliados.json').read_text())
def br(v):return '—' if v is None else f'{v:,.2f}'.replace(',','X').replace('.',',').replace('X','.')
s='''# Pesquisa ampliada — emenda federal de bancada de R$ 1,5 milhão

Pesquisa em 03/11/2026. Complementa e qualifica o estudo anterior. Eco e eletrocardiograma permanecem reservados à emenda de R$ 2 milhões de cardiologia.

## O que muda na decisão

A oferta potencial no DF é mais ampla que os três nomes iniciais, mas a quantidade de filiais não representa o mesmo número de concorrentes. A pesquisa reúne **19 perfis de prestadores e pistas**, **23 instalações autorizadas para medicina nuclear no DF** e **34 códigos de procedimentos** com demanda e referências de remuneração. Os 19 perfis incluem públicos, prestadores com oferta explícita e pistas ainda não confirmadas; não são 19 clínicas de cintilografia validadas.

Minha recomendação é abrir três frentes de cotação comparáveis: **densitometria; RM não ortopédica; e um lote nuclear limitado, executado em serviço existente**. A cintilografia óssea continua candidata, mas não há fundamento para comprometer nela a maior parte dos R$ 1,5 milhão antes de confirmar tarifa, custo integral e capacidade. A seleção anterior de quantidades é cenário de planejamento, não carteira economicamente validada.

## Prestadores: o que foi efetivamente encontrado

A [base oficial ANSN/CNEN](https://appasp2019.cnen.gov.br/dados-abertos/dados-abertos-ansn-download.asp?op=2), disponível em 03/11/2026, foi baixada e filtrada por **Estado = DF e Área de atuação = MEDICINA NUCLEAR**, com igualdade exata. Resultaram 23 registros: sete do IMEB, quatro do Centro de Medicina Nuclear de Brasília, dois Biocárdios e dez outros registros. A planilha contém matrícula, designação e validade de cada um. O CSV original foi preservado.

A autorização evidencia situação regulatória declarada na base. Não confirma todos os exames, a unidade física de execução, disponibilidade comercial, licença sanitária local ou credenciamento SES. O vínculo entre marca, CNPJ, matrícula e endereço deve ser conferido na proposta.

| Prestador | Evidência e utilidade para a carteira |
|---|---|
| [IMEB](https://imeb.com.br/nossos_exames/cintilografia/) | Publica óssea, miocárdica, renal DMSA/DTPA, tireoide, paratireoides e outros tipos. Tem sete registros na base nuclear DF. Cotar por filial executante. |
| [Núcleos](https://nucleos.med.br/procedimentos/medicina-nuclear-exames/) | Publica cintilografia/SPECT, PET-CT e cirurgia radioguiada. O site lista Centro Médico, Advance, OHB, Lago Sul e Santa Lúcia. Não contar as cinco unidades como cinco concorrentes independentes. |
| [IRB](https://irbmedicina.com/exames_de_medicina_nuclear/) | Catálogo detalhado: óssea, DMSA, renal dinâmica, perfusão miocárdica, paratireoide, digestivas, pulmonares e cerebrais. Matrícula 15209, validade 24/07/2027. |
| [Biocárdios](https://biocardios.com.br/exames/cintilografia) | Confirma cinco famílias: perfusão miocárdica, salivares, tireoide com Tc99m, paratireoide e DMSA. Dois registros autorizados. Óssea não está confirmada nessa página. |
| [Hospital do Coração do Brasil](https://www.rededorsaoluiz.com.br/hospital/coracaodobrasil/servicos/medicina-nuclear) | Confirma miocárdio em repouso e estresse físico/farmacológico; protocolo em um período ou dois dias. Publica outras categorias, sem detalhamento por exame. |
| [HOME](https://www.homehospital.com.br/Noticia,Abrir,19472,4693.aspx) | Publicação institucional anuncia medicina nuclear e cirurgia radioguiada; autorização até 06/10/2029. A notícia não tem ano visível: confirmar catálogo e agenda atuais. |
| [Villas Boas](https://www.clinicavillasboas.com.br/exames/) | PET-CT confirmado; autorização até 27/08/2028. Não inferir cintilografia convencional a partir do equipamento PET. |
| [Sírio-Libanês](https://siriolibanes.org.br/unidades/diagnostico-asa-sul) | PET-CT e imagem convencional confirmados em Brasília. Há autorização da unidade Brasília III até 16/07/2028; conferir endereço exato antes de vinculá-la à proposta. |
| Santa Lúcia | Autorização própria na base; existe também unidade Núcleos Santa Lúcia. Conciliar operador, CNPJ e portfólio para evitar duplicar a oferta. |
| Hospitais Integrados da Gávea | Autorização nuclear na base, mas isso não confirma serviço diagnóstico contratável. Há divergência documental sobre oferta no DF Star, detalhada abaixo. |

**Concorrência efetiva:** não atribuí independência societária a IRB e Núcleos. Há referência histórica de integração entre eles, mas não foi concluída verificação societária atual. Também não atribuí às unidades hospitalares um operador independente sem prova.

**Ponto de atenção concreto:** a matrícula 17134 do Centro de Medicina Nuclear de Brasília tem validade declarada até **25/11/2026**. Identificar a unidade e sua renovação antes de prever execução posterior.

**Divergência a resolver:** o CSV inclui Hospitais Integrados da Gávea. Um [dossiê público apresentado ao Senado](https://www12.senado.leg.br/transparencia/licitacoes-e-contratos/sadcon/habilitacao-hospitais-integrados-da-gavea.pdf/%40%40download/file/Habilita%C3%A7%C3%A3o%20Hospitais%20Integrados%20da%20Gavea.pdf) contém declaração do DF Star, de 26/03/2026, de que não prestava medicina nuclear. As datas, CNPJ/unidade e a possível diferença entre terapia e diagnóstico impedem tratar esses documentos como confirmação automática de oferta de cintilografia.

Outros três perfis merecem investigação, sem contabilizá-los como prestadores nucleares confirmados: **Vila Rica**, que se apresenta em medicina nuclear, mas cujo catálogo consultado detalha principalmente radiologia; **Diagnostik** e **Taguacor**, com pistas cadastrais de equipamento. Não houve correspondência nominal desses três no CSV nuclear DF. Razão social diferente ou operação por terceiro pode explicar a ausência; não equivale a declaração de irregularidade.

## O que o Mapa Social comprova

Consulta pela interface pública do [Mapa Social](https://paineis-ext.mpdft.mp.br/extensions/mapasauderegulamentacao/mapasauderegulamentacao.html), atualização **03/11/2026 14:32:34**, sem filtro de ano, status ou unidade. Cada consulta tinha apenas o grupo ou nome exato indicado abaixo.

| Recorte | Agendamentos no histórico exibido | Executores | Identificado |
|---|---:|---:|---|
| Grupo Procedimento = GRUPO - CINTILOGRAFIA | 5.328 | 1 | HUB |
| Procedimento = TOMOGRAFIA POR EMISSÃO DE PÓSITRONS (PET-CT) | 4.983 | 1 | HBDF |

No grupo Cintilografia, a série exibiu 1.828 agendamentos em 2025 e 3.500 em 2026. O comparativo exibiu 1.064 e 1.618 realizados, respectivamente. Para PET-CT, a série de 2021 a 2026 soma 4.983. O executor foi identificado na tabela de detalhes e confrontado com o KPI de unidade única.

O painel classifica o HUB em contratado/credenciado, mas ele é hospital universitário público federal. A categoria gráfica não indica clínica privada. O [Plano Distrital de Saúde 2024–2027](https://info.saude.df.gov.br/wp-content/uploads/2024/10/Plano_134313201_PDS_2024_FINAL_26.02.24.pdf) já descreve a contratualização SES/Ebserh para cintilografia no HUB. O [protocolo SES de PET-CT](https://www.saude.df.gov.br/documents/37101/0/Protocolo%2Bde%2Bacesso%2BPETCT2.pdf/1dcf4b5d-6afc-34b0-6b6a-b249f3c325f6?t=1732730740845) prevê agendamento no HBDF.

**Limite:** esses resultados valem para os recortes disponíveis no painel. Não provam que nunca houve produção privada, compra judicial, contratação fora do SISREG ou procedimentos classificados em outro grupo. O JSON de evidência preserva filtros e totais agregados; não houve exportação integral por prestador nem acesso a dados pessoais.

Localizei [ato da SES de 2015 em favor do Núcleos](https://www.sinj.df.gov.br/sinj/Diario/efcfaea0bcad49018b65a11fa713cf89/b40be1da-8510-3764-937d-f1612bee39cf/arq/0/Se%C3%A7%C3%A3o03-%20207.pdf), para cintilografia óssea a R$ 450. É evidência de autorização de despesa antiga, não de execução comprovada, preço atual ou credenciamento vigente. Também surgiu publicação secundária da Deliberação 22/2026, que aprova proposta de credenciamento pelo ETP 426/2026; sem edital final, habilitados e contratos localizados, não tratei isso como oferta privada já contratada.

## Procedimentos nucleares: demanda e remuneração

A base preservada de 02/11/2026 contém 23 códigos nucleares, somando **5.663 pedidos**, não pessoas únicas. Os seis códigos de maior fila concentram 5.385 pedidos; todos os demais somam apenas 278. Repouso e estresse podem ser etapas do mesmo paciente. Por isso, ampliar o catálogo inteiro não significa ampliar proporcionalmente o público atendido.

As colunas de remuneração abaixo são **referências distintas**. Base SA e incremento vêm do pacote SIGTAP 10/2026; Candanga vem do anexo oficial SIA já preservado no acervo. Incremento depende de habilitação, modalidade de financiamento, registro e reconhecimento aplicáveis. Não somar incremento e Candanga. “—” no incremento indica ausência de percentual 38.01 localizado; não é autorização de pagamento por outra via.

| SIGTAP | Nome oficial | Fila | Base SA R$ | Com incremento 38.01 R$ | Candanga R$ |
|---|---|---:|---:|---:|---:|
'''
for x in d['procedures']:
 if x['family']=='Medicina nuclear':s+=f"| {x['code']} | {x['name']} | {x['stock']} | {br(x['base'])} | {br(x['incremental']) if x['inc'] is not None else '—'} | {br(x['candanga'])} |\n"
s+='''
**Prioridades de cotação:** óssea, DMSA e paratireoides podem compor um lote limitado com o mesmo prestador, condicionado ao custo e à agenda. DTPA deve ter proposta separada: sua referência não reproduz o incremento encontrado para DMSA. Miocárdio merece cotação do percurso completo; as bases de estresse e repouso somam R$ 791,59 e os cenários incrementais somam R$ 1.779,80, apenas quando ambas as etapas forem indicadas, autorizadas e registráveis. Não converter dois códigos automaticamente em dois pacientes ou em direito a duas cobranças.

Tireoide, salivares e digestivas têm espaço como complemento, mas não sustentam uma emenda desse tamanho pelo estoque observado. Linfonodo sentinela exige articulação com a cirurgia; não é bom objeto isolado para gerar volume. Terapias com radioisótopos ficam fora desta carteira diagnóstica. TRODAT, PSMA, FDG e outros traçadores não devem receber código e tarifa genéricos por aproximação de nome.

## Alternativas fora da cintilografia

Ampliei o levantamento para oito códigos de RM não predominantemente ortopédicos, PET-CT, densitometria e mamografia. Todos estão na planilha, com produção, fila, preço e ressalvas.

| SIGTAP | Procedimento oficial | Fila | Base SA R$ | Cenário incremental R$ | Candanga R$ |
|---|---|---:|---:|---:|---:|
'''
for x in d['procedures']:
 if x['family']!='Medicina nuclear':s+=f"| {x['code']} | {x['name']} | {x['stock']} | {br(x['base'])} | {br(x['incremental']) if x['inc'] is not None else '—'} | {br(x['candanga'])} |\n"
s+='''
Novos nomes úteis para cotar RM: [Radiolinea](https://www.radiolinea.com.br/exames/), que detalha crânio, sela, mastoides, colangio-RM e angio-RM; [Tesla Diagnóstico por Imagem DF](https://www.teslaimagem.com.br/páginas/exames/ressonancia.html), que publica RM de abdômen e pelve; e [Sabin Imagem Brasília](https://sabin.com.br/unidades/brasilia-df/imagem/), com RM, mamografia e densitometria. Villas Boas, Sírio-Libanês e Vila Rica também oferecem modalidades relevantes. Isso amplia a concorrência a investigar, sem presumir preço ou disponibilidade para o SUS. A Radiolinea anuncia “Tabela Especial SUS”; o anúncio sozinho não comprova contrato com a SES.

O código de RM pode reunir diversos nomes locais. Não se deve vender o estoque de um código como se todos os pedidos fossem o protocolo simples cotado. Contraste, sedação, pediatria e equipamentos compatíveis precisam constar expressamente na proposta. O código 0207010021, por exemplo, tem nome oficial amplo de articulação temporomandibular e base do crânio; a maior fila local é descrita como mastoides.

## Complexidade e viabilidade econômica

Sua preocupação com a cintilografia procede. A [RDC 38/2008, art. 2º](https://anvisalegis.datalegis.net/action/ActionDatalegis.php?acao=abrirTextoAto&cod_menu=9431&cod_modulo=310&link=S&numeroAto=00000038&orgao=RDC%2FDC%2FANVISA%2FMS&seqAto=000&tipo=RDC&valorAno=2008) exige autorização nuclear e licenciamento sanitário local. Há requisitos de instalações, equipe, proteção radiológica, controle de qualidade e gerenciamento de materiais. O [serviço de fornecimento do IPEN](https://www.gov.br/pt-br/servicos/obter-radiofarmacos-do-instituto-de-pesquisas-energeticas-e-nucleares?id=3284&origem=servico) também exige autorização e licença e informa preços dependentes do produto e da atividade requerida.

Contratar um serviço já instalado reduz a necessidade de investimento inicial e implantação, mas não elimina o custo dos radiofármacos, perdas, remarcações e supervisão. DMSA ou tireoide não se tornam exames comuns de ultrassom por terem protocolo diferente. No miocárdio somam-se preparo, estresse e possibilidade de duas etapas. Na óssea, a permanência e retorno para aquisição dificultam operação de mutirão rápido. É necessário cotar slots e exames concluídos por mês, não apenas horas de máquina.

**Ainda não há base para dizer “paga bem” ou estimar lucro.** Tarifa de referência alta é receita potencial; custo integral e elegibilidade ainda não estão demonstrados. A equação para cada procedimento é: valor efetivamente aprovado e recebido menos preço completo do prestador menos custos operacionais atribuíveis e perdas contratuais. O valor anunciado ao particular em outro estado não substitui cotação DF.

A origem federal de bancada não torna Candanga automaticamente aplicável. A complementação distrital depende da fonte e do instrumento próprio. O incremento nacional precisa de enquadramento; a norma considerada no estudo anterior tem efeitos até 31/12/2026, sem continuidade posterior comprovada nesta pesquisa. A análise de 2027 deve ser refeita antes de assumir execução plurimensal. A planilha apresenta cenários lado a lado, sem escolher o maior como receita garantida.

## Relação com o IEV, a carteira anterior e a SES

As RM ortopédicas predominantes, ultrassonografias e TC já mapeadas na carteira anterior não voltaram como novas oportunidades. A carteira anterior é planejamento: quantidade escolhida não equivale a exame já realizado. A RM de pelve/bacia permanece sob ressalva por poder alcançar o IEV; precisa de recorte de indicação e pacientes. Não se resolve sobreposição apenas pelo CID.

A ausência de cintilografia entre os itens obrigatórios das OCI mapeadas não demonstra ausência de outra cobertura oncológica ou contratual da SES. O edital oncológico 02/2025 inclui óssea em determinadas linhas de cuidado: conciliar o pedido com o tratamento e o contrato correspondente antes de financiá-lo novamente. A oferta HUB/HBDF deve integrar o desenho da compra adicional. A emenda pode complementar uma insuficiência demonstrada, sem apresentar como inexistente um serviço já ofertado.

## Encaminhamento pronto para cotação

Para cada prestador selecionado, a proposta deve informar código/protocolo exato, CNPJ e endereço executor, matrícula nuclear quando aplicável, licença sanitária, preço integral por exame concluído, radiofármaco/contraste/estresse/sedação incluídos ou separados, prazo de laudo, slots mensais, atendimento pediátrico e regras para falta, remarcação e falha de insumo. Para miocárdio, discriminar etapas e preço do percurso completo. Para PET, discriminar traçador e indicação.

Não houve contato com prestadores nesta pesquisa. O resultado entregue é um mapa ampliado e verificável para selecionar cotações, com limites explícitos. A prioridade final e as quantidades dos R$ 1,5 milhão devem ser fechadas após essas propostas e o reconhecimento formal da remuneração. Densitometria e RM não ortopédica devem avançar em paralelo à avaliação do lote nuclear.

## Arquivos e método

A planilha **Pesquisa ampliada de imagem.xlsx** contém Decisao, Procedimentos, Prestadores, Autorizacoes e Fontes. São 34 códigos, 19 perfis e as 23 autorizações nucleares. Os preços incrementais são fórmulas reconciliadas com o cálculo decimal do pacote oficial. Fontes comerciais aparecem por linha de prestador; CSV, catálogo IRB e manifesto de hashes foram preservados.

As filas e a produção usam a mesma fotografia de 02/11/2026 do estudo anterior, com solicitações até 28/10/2026 e janela fechada out/2025–set/2026. A consulta de executores usa outra recarga, 03/11/2026 14:32:34, e histórico completo disponível no filtro. Não se misturaram esses períodos para calcular cobertura ou evolução de estoque. Entrantes no método original somam solicitações abertas e agendadas; não devem ser chamados de demanda nova líquida. Realizado é o status registrado no painel, sem auditoria assistencial externa.
'''
(O/'Pesquisa ampliada e recomendacoes.md').write_text(s)
print('Relatório',len(s.split()),'palavras')
