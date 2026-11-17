from pathlib import Path
import json
O=Path(__file__).resolve().parent;d=json.loads((O/'dados_leque.json').read_text());by={x['code']:x for x in d['procedures']}
def br(x):return 'Não localizado' if x is None else f'{x:,.2f}'.replace(',','X').replace('.',',').replace('X','.')
def num(x):return 'Não localizada' if x is None else f'{x:,}'.replace(',','.')
s='''# Leque de possibilidades e dificuldades para a emenda

Estudo em 04/11/2026. Emenda federal de bancada de R$ 1,5 milhão. A análise considera prestação de exames e percursos diagnósticos. Eco e ECG continuam destinados à emenda de cardiologia de R$ 2 milhões, conforme decisão do usuário.

## O resultado da exploração

Ampliei a leitura para o inventário geral preservado do Mapa Social, com 1.026 filas nominais pendentes. Selecionei **99 filas nominais**, cruzei **84 códigos SIGTAP** e organizei **38 possibilidades**, incluindo todos os **54 procedimentos do subgrupo de medicina nuclear**. As opções incluem exames individuais e agrupamentos assistenciais; não são 38 contratos propostos nem 38 públicos distintos.

Há duas decisões diferentes: quais procedimentos têm interesse assistencial e operacional, e quais podem ser pagos no instrumento da emenda. Endoscopia, neurofisiologia, sono e função pulmonar ampliam muito o leque, mas sua inclusão depende da compatibilidade do objeto. Não foi demonstrado que uma emenda restrita a imagem radiológica possa custeá-los automaticamente.

Minha ordem de investigação é: **densitometria e RM não ortopédica** para continuidade do objeto de imagem; **endoscopia/colonoscopia, ENMG e polissonografia** se o objeto admitir diagnóstico especializado mais amplo; **OCT/campimetria e punções guiadas** como linhas específicas a validar; **um lote nuclear direcionado**, com serviço existente, caso a compra seja economicamente sustentável. Não há margem financeira comprovada para nenhuma dessas frentes sem propostas integrais de prestadores.

## Como interpretar os números

As filas vêm da recarga de **02/11/2026 às 10:31:47**, com solicitações até 28/10/2026. Não são filas atualizadas em 04/11. A janela de agendamentos do inventário é **28/10/2025 a 27/10/2026**, diferente dos 12 meses fechados de produção usados em parte dos estudos anteriores. Agendamento não é realização.

As somas por código e opção representam pedidos nas filas nominais selecionadas. Uma pessoa pode ter dois membros, repouso e estresse ou mais de um exame. Não há soma global de pessoas. “Últimos 24 meses” informa a data do pedido, não confirma indicação clínica atual. “Não localizada” informa ausência neste recorte, sem concluir que não exista demanda reprimida fora do painel.

## Comparação das 38 possibilidades

| Possibilidade | Pedidos localizados | Pedidos dos últimos 24m | Encaminhamento | Dificuldade principal | Escopo ou sobreposição |
|---|---:|---:|---|---|---|
'''
for x in d['options']:s+=f"| {x['label']} | {num(x['stock'])} | {num(x['recent'])} | {x['decision']} | {x['difficulty']} | {x['scope']} |\n"
s+='''
## As alternativas novas mais relevantes

**Endoscopia e colonoscopia.** A fila nominal de endoscopia digestiva alta tem 26.155 pedidos; colonoscopia simples, 22.560. As grafias adicionais de colonoscopia com anestesia e um pedido antigo elevam o conjunto do código a 22.943. Há escala para um projeto, mas também preparo, sedação, recuperação, acompanhante, desinfecção do aparelho e possibilidade de biópsia/polipectomia. Não basta comprar minutos de aparelho. Uma proposta deve dizer se inclui anatomopatológico, materiais, anestesia, repetição por preparo inadequado e encaminhamento de achados.

A [RDC Anvisa 6/2013](https://anvisalegis.datalegis.net/action/ActionDatalegis.php?acao=abrirTextoAto&cod_menu=9434&cod_modulo=310&numeroAto=00000006&orgao=RDC%2FDC%2FANVISA%2FMS&seqAto=000&tipo=RDC&valorAno=2013) disciplina funcionamento, processamento e recuperação desses serviços. É uma alternativa de impacto, cuja dificuldade operacional pode ser maior que a de densitometria ou RM sem sedação. Para a fila específica com anestesia, a [nota técnica SES de 2024](https://www.saude.df.gov.br/documents/37101/0/Nota%2BT%C3%A9cnica%2BN.%C2%BA%2B1-2024%2B%E2%80%93%2BSES-SAIS-DUAEC-GESCIR-CATC%2BRegulacao%2Bde%2BExame%2BDe%2BColonoscopia%2Bcom%2BAnestesia%2B-%2BSISREGIII%2Bc%C3%B3digo%2B0113006.pdf/d9d14740-044f-5053-8ca9-9f12c33c2763?t=1732795679246) descrevia HBDF como executor e uma regulação própria. Esse documento não permite afirmar exclusividade atual em 2026.

**Eletroneuromiografia.** As duas grandes filas são membros inferiores, 5.079, e superiores, 4.058. Há ainda um pedido em outra grafia; o código soma 9.138. Oportunidade interessante de diagnóstico especializado, com dependência forte da agenda do médico e do protocolo por segmentos. A [página do INNEB](https://inneb.com.br/exame-eletroneuromiografia/) publica exame de membros superiores e inferiores e duração de duas horas para seu protocolo. Essa duração não deve ser generalizada para todo prestador, mas mostra por que não se pode presumir dezenas de exames por médico em um turno.

**Polissonografia.** A fila basal tem 8.529 pedidos; o mesmo código reúne mais um pedido antigo de CPAP/BIPAP/split-night. Só 4.110 pedidos do conjunto são dos últimos 24 meses. O estoque precisa de confirmação de indicação e contato antes de virar meta. É possível contratar laboratório ou modalidade domiciliar compatível, mas [PSG completa e teste tipo III](https://sites.usp.br/guiacseb/wp-content/uploads/sites/943/2025/01/PROTOCOLO-POLISSONOGRAFIA.pdf) têm capacidades diferentes. Não substituir toda a fila basal por um aparelho domiciliar simplificado apenas para reduzir custo. Laudo, instalação, recolhimento, perda de sinal e repetição devem fazer parte da proposta. Diagnosticar apneia também exige fluxo para avaliação e eventual tratamento, que não fica automaticamente pago pelo exame.

**OCT e campimetria.** O código de OCT reúne 3.906 pedidos, dos quais 2.359 estão na fila chamada OCT glaucoma e 1.547 na chamada OCT. Campimetria tem 3.816. São possibilidades de uma linha diagnóstica de glaucoma/retina, com equipamento e profissionais próprios. OCT anterior, posterior, OCT-A e exames de córnea não são a mesma aquisição nem o mesmo faturamento. A ausência de preço Candanga localizado para 0211060283 é pendência de verificação, não autorização para usar preço de outro código.

**PAAF de tireoide e core biópsia mamária.** São 530 pedidos de PAAF tireoidiana e 292 de biópsia guiada, estes distribuídos em 215 pela ultrassonografia e 77 pela mamografia. Podem formar uma linha de esclarecimento de achados, sobretudo quando já se oferece exame de imagem inicial. A quantidade é menor, mas o valor assistencial pode ser alto. É necessário incluir coleta, processamento, citologia/histologia, rastreabilidade, amostra insatisfatória e devolução do resultado à rede. O preço do procedimento isolado não demonstra que o percurso inteiro cabe na remuneração. O código genérico de biópsia guiada não iguala custo de mama, pulmão e outros órgãos.

**Videolaringoscopia e endoscopia nasal.** O mesmo código local reúne 3.720 pedidos de nasal flexível, 447 de nasal rígida, 221 de avaliação da deglutição e outras descrições, totalizando 4.603. A fila é relevante. A primeira tarefa é revisar esse agrupamento: nome local e código oficial não demonstram equivalência entre equipamento, equipe e protocolo. Só depois faz sentido fechar preço e meta.

**Espirometria, EEG, colposcopia, audiologia e BERA.** Ampliam a visão sobre o que é possível, mas precisam de enquadramento e, em vários casos, sofrem com tarifa básica baixa. Espirometria tem 2.561 pedidos; o EEG selecionado soma 3.472 em dois códigos. A colposcopia tem 696. Audiologia e BERA precisam de revisão da cobertura do IEV antes de nova compra. Não recomendo escolher uma dessas linhas apenas pelo tamanho da fila.

## Mais medicina nuclear: do lote viável às demandas raras

Nos 54 procedimentos oficiais, há **23 códigos com pedidos pendentes localizados**, **quatro com nome no catálogo local e sem fila pendente localizada**, e **27 localizados apenas no SIGTAP neste cruzamento**. Os quatro sem pendência localizada são coração com gálio, pulmão com gálio, Meckel e hemorragia digestiva não ativa. Isso evita chamar existência na tabela de demanda demonstrada.

| Família | O que acrescenta ao leque | Dificuldade que altera o projeto |
|---|---|---|
| Óssea | 1.587 pedidos na fila principal | Radiofármaco e imagens tardias; conciliar indicações oncológicas já cobertas |
| Renal DMSA e DTPA | 179 e 234 pedidos | São protocolos diferentes; DTPA não reproduz incremento de DMSA |
| Paratireoides | 152 pedidos | Definir aquisição, permanência e eventual SPECT/CT na proposta |
| Miocárdio | 1.737 estresse e 1.496 repouso | Mesmo paciente pode gerar duas etapas; preparar e contratar percurso completo |
| Salivares e tireoide | 58 e 28 pedidos | Bom complemento se houver agenda e insumo; escala pequena |
| Trânsito gástrico | 34 pedidos, líquidos e sólidos no mesmo código local | Refeição marcada e aquisição seriada; conferir protocolo |
| Trânsito esofágico e refluxo | 11 pedidos no conjunto selecionado | Volume pequeno e indicação/protocolo específicos |
| Linfocintilografia | 22 pedidos | Extremidades e sentinela exigem desenhos diferentes; sentinela depende da cirurgia |
| Pesquisa de corpo inteiro | 25 pedidos | Confirmar traçador, preparo e linha de cuidado; não equivale ao PET |
| Pulmonar por perfusão | 15 pedidos | Ventilação/inalação é outro procedimento; integrar indicação clínica |
| Estudos com gálio e cerebrais | Pequeno volume localizado | Insumos e finalidade específicos; não mapear TRODAT para ECD ou tálio por semelhança do nome |
| Outras modalidades da tabela | Ventriculografia, cistocintilografia, cisternocintilografia, medula óssea, estudos de shunt, fígado/vias biliares, mama e outras | Precisam de demanda local e executor/protocolo confirmados antes de orçamento |

O [protocolo vigente da SES para cintilografia](https://www.saude.df.gov.br/documents/d/saude/protocolo-de-acesso-ao-exame-de-cintilografia-pdf) prevê regulação, execução no HUB e aplicação dos fluxos também a outros contratados. Informa agenda mensal com antecedência mínima de 45 dias e dependência de insumos. Alguns recortes contemplam pacientes internados. Portanto, não se deve transformar todo o catálogo em um lote eletivo indistinto. A logística precisa ser pactuada por protocolo.

Minha leitura é que um lote nuclear enxuto pode ser executável em serviço já instalado. Um projeto pulverizado por dezenas de cintilografias raras perde escala, complica marcação e pode depender de radiofármacos de utilização esporádica. A existência de fornecedores privados no DF torna a cotação possível; não garante disponibilidade mensal ou preço compatível.

## Remuneração: por que a mesma fila pode ser boa ou inviável

Valores em reais. **Base SA** é o serviço ambulatorial no SIGTAP 10/2026; **incremento 38.01** é um cenário condicionado; **Candanga** é referência distinta do anexo oficial extraído. Não somar as três colunas nem acrescentar SH/SP à SA como receita ambulatorial automática. Não foi obtida nova cotação vinculante de prestador.

| Procedimento | Base SA | Com incremento 38.01, se aplicável | Candanga localizada |
|---|---:|---:|---:|
'''
for c in ['0204060028','0204030188','0207010064','0209010037','0209010029','0211050105','0211050083','0211060283','0211060038','0211050040','0211080055','0201010470','0201010542','0209040041','0208050035','0208040056','0208040102','0208030018','0206010095']:
 x=by[c];s+=f"| {x['name']} ({c}) | {br(x['base'])} | {br(x['incremental'])} | {br(x['candanga'])} |\n"
s+='''
Os exemplos mais claros são polissonografia, com base SA de R$ 125 e referência Candanga de R$ 819,01, e ENMG, com R$ 27 e R$ 348,93. A oportunidade financeira depende de qual remuneração pode ser formalmente adotada na emenda federal e de qual protocolo o prestador aceita entregar por esse valor. Não é possível concluir que o exame “paga bem” usando apenas a coluna maior.

Na endoscopia e colonoscopia há incremento localizado, mas ainda faltam elegibilidade, vigência no período de execução e proposta completa. Para execução em 2027, não extrapolar automaticamente efeitos normativos previstos até 31/12/2026 no estudo anterior. Para OCT, BERA e VENG, a falta de correspondência no anexo extraído exige verificação específica.

**O que mede viabilidade:** receita reconhecida por exame concluído menos preço integral do executor menos custos operacionais atribuíveis e perdas. Custos de mobilização ou apoio precisam caber no instrumento. Não foi presumido percentual de lucro, taxa de apoio ou quantidade para gastar exatamente os R$ 1,5 milhão.

## Cobertura existente e limites da ampliação

O acervo traz 11.590 OCI auditivas do IEV. No pacote SIGTAP, as OCI 0904010015 e 0904010023 têm audiometria tonal obrigatória, imitanciometria compatível e, na progressão, potenciais auditivos. A fila local “audiometria e imitanciometria” usa código de audiometria em campo livre. Somar os nomes e atribuir uma tarifa de pacote seria inadequado sem revisão.

Para oftalmologia, os planos ISHP somam 44.400 OCI contratadas no acervo, em faixas etárias diferentes. Mapeamento de retina é obrigatório nessas OCI. Quantidade contratada não significa concluída, mas exige conciliação antes de comprar a mesma prestação. OCT e campimetria não aparecem como componentes dessas duas OCI específicas na competência examinada; isso não exclui cobertura em outros contratos.

O IEV também cobre linhas ortopédicas, GIN1, próstata e cardiologia já examinadas. RM de pelve/bacia é código misto; os 1.519 pedidos mostrados ainda incluem possíveis indicações ortopédicas. Não foram rotulados como demanda não ortopédica livre. PAAF, core biópsia, endoscopia e exames oncológicos precisam ser conciliados com os instrumentos específicos da SES, além do IEV. A decisão deve ocorrer por pedido, indicação e percurso, sem partição apenas por CID.

Existe oferta pública de várias dessas modalidades. O [relatório HCB de março/2026](https://www.hcb.org.br/arquivos/downloads/1_relatorio_de_gestao_mensal_marco_de_2026.pdf) registra oferta de EEG, ENMG, espirometria e outros exames pediátricos. Isso demonstra serviço existente; não mede a capacidade atual de toda a rede ou a cobertura adulta. Em 03/11, o recorte do Mapa Social consultado mostrou HUB na cintilografia e HBDF no PET. Esta pesquisa de 04/11 não refez uma coleta completa de executores para as novas modalidades.

## Prestadores adicionais para uma futura rodada de propostas

São evidências de oferta publicada, não credenciamento SES ou confirmação de capacidade para o projeto:

| Frente | Prestadores e fonte | O que a proposta precisa esclarecer |
|---|---|---|
| Endoscopia/colonoscopia | [Gastrocentro Brasília](https://clinicagastrocentro.com.br/) | Anestesia/sedação, biópsia, patologia, polipectomia, recuperação e repetições |
| Sono/função pulmonar | [Clinar](https://www.clinar.com.br/) | Tipos de PSG, leitos, noites/mês, equipe, laudo e espirometria |
| Sono | [MedSono](https://www.medsono.com.br/) e [Otoface](https://www.polissonografiabrasilia.com/) | Laboratorial versus domiciliar, protocolo, capacidade e perdas técnicas |
| ENMG | [INNEB](https://inneb.com.br/exame-eletroneuromiografia/) | Membros/segmentos, duração, insumos e médico executor |
| Oftalmologia | [HOB](https://www.hobr.com.br/servicos/exames) e [Occhio](https://occhiobrasilia.com.br/) | Exame exato, olhos, indicação, unidade e seguimento |
| PAAF | [INMED](https://inmedonline.com.br/exames/paaf) | Guia de imagem, citologia, adequação da amostra e resultado integrado |
| Nuclear | [IMEB](https://imeb.com.br/nossos_exames/cintilografia/), [IRB](https://irbmedicina.com/exames_de_medicina_nuclear/), Núcleos e demais perfis do estudo de 03/11 | Traçador, unidade autorizada, radiofármaco, equipe, slots e laudo |

Não houve contato ou envio de mensagens aos prestadores. Licenças, CNPJ, capacidade, contratação e preços comerciais devem ser conferidos na etapa de proposta.

## Quatro desenhos possíveis para os R$ 1,5 milhão

1. **Imagem ambulatorial com menor dependência de sedação:** densitometria e RM não ortopédica, com protocolos delimitados. É a continuidade mais direta da investigação atual. A quantidade dependerá da tarifa e das propostas.
2. **Imagem com esclarecimento diagnóstico:** mamografia e/ou exame inicial associado a biópsias indicadas e patologia. Pode reduzir perdas entre suspeita e diagnóstico, mas exige regulação integrada e conciliação da cobertura oncológica.
3. **Medicina nuclear complementar:** óssea, renal, paratireoide e outros pedidos regulados em volume limitado. Exige prestador existente, capacidade por traçador e logística pactuada. Não montar o projeto para consumir todo o orçamento apenas porque uma tarifa é alta.
4. **Diagnóstico especializado ampliado:** endoscopia/colonoscopia, ENMG ou sono como frente principal, se o objeto e a remuneração permitirem. São oportunidades novas de grande fila, com dificuldades muito diferentes. Não recomendo contratar todas no mesmo instrumento sem uma razão assistencial e capacidade de gestão.

Holter/MAPA merecem avaliação na carteira de R$ 2 milhões de cardiologia, junto da demanda já reservada de eco e ECG; essa alocação adicional é sugestão, não decisão do usuário.

O próximo filtro para escolher entre esses desenhos é obter propostas comparáveis e uma definição formal da remuneração/fonte. Antes disso, o leque está aberto e a contratação não está economicamente validada.

## Apêndice: todos os 54 procedimentos nucleares

“Somente SIGTAP” não significa execução disponível no DF. Fila ausente não é demanda zero comprovada.

| SIGTAP | Nome oficial | Pedidos localizados | Evidência | Base SA R$ | Candanga R$ |
|---|---|---:|---|---:|---:|
'''
for x in d['procedures']:
 if x['code'] in d['nuclear_codes']:s+=f"| {x['code']} | {x['name']} | {num(x['stock'])} | {x['evidence']} | {br(x['base'])} | {br(x['candanga'])} |\n"
s+='''
## Arquivos e verificações

A planilha contém o leque, o universo nuclear, as referências por código, as 99 filas nominais e as fontes. O JSON e o manifesto preservam origem e hash da fotografia de demanda. Foram conferidos os cruzamentos e o arredondamento dos valores incrementais. A análise de sobreposição usa OCI do pacote oficial 10/2026 e os planos já presentes no acervo, sem tratar consultas registradas como OCI concluídas.
'''
(O/'Leque de possibilidades e dificuldades.md').write_text(s)
print('Relatório',len(s.split()),'palavras')
