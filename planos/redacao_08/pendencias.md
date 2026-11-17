# Pendências — redacao_08 (OCI de Cardiologia, Instituto Fazer o Bem, Faz Bem, Emenda 41360018/2024)

## Do usuário

| | pendência | de quem | estado |
|---|---|---|---|
| P-01 | **Os três produtos.** Pré-projeto = o "Projeto" curto que a entidade manda à SES antes do ofício da ARINS (exemplo: o projeto de cardiologia do IEV de 22/12/2025, 6 p.); PT simplificado = o formulário "Modelo Parceria" da ARINS (pré-plano); PT detalhado = o plano de convênio, no modelo da SES de 21/10/2026. Os três nesta pasta (usuário, 22/10/2026: "tudo que for de um projeto deve ficar junto") | usuário | **resolvido em 22/10/2026** |
| P-02 | **Qual OCI.** Sai do dossiê: as sete do subgrupo 09.02.01, a fila no DF e os projetos em andamento, "para nada se sobrepor" (usuário, 22/10/2026) | usuário, depois do dossiê | aberto |
| P-03 | **Como executar.** O Instituto não tem CNES (nem a matriz, no RJ desde 2014, nem a filial do DF, de 25/08/2026), é o primeiro convênio dele, e a atividade de saúde no CNPJ é só secundária, sem exames. O usuário prevê "parceria com clínicas", sem quarteirizar. Decidir o que o Instituto faz por conta própria (com CNES próprio no DF) e o que vai às clínicas, ver a nota abaixo | usuário | aberto |
| P-04 | **O processo.** A ARINS ainda não pediu o PT simplificado; o usuário vai se adiantar. Falta o objeto da proposta cadastrada em 2024 para os R$ 12,3 mi do Fundo (perguntar à ARINS quando houver contato) | usuário | aberto |
| P-05 | **Vigência e apoio.** Depois do dossiê: "depende se a OCI paga bem" (usuário, 22/10/2026). O dossiê usa 10% provisório | usuário, depois do dossiê | aberto |
| P-06 | **O modelo de convênio da SES** foi ao `main` em 22/10/2026 (`biblioteca/instrumento/modelo_ses/`, commit d924899), com a regra de que vale o mais recente (`metodo/comum.md`, regra 15) | usuário | **resolvido em 22/10/2026** |
| P-08 | **A fila do risco cirúrgico.** A consulta de risco cirúrgico tem 10.041 pessoas, mas o pedido traz o CID da cirurgia, não o da 001-8 (56 pessoas) nem o da 007-7 (85). Decidir se essa fila conta para a OCI (`dados/fontes/mapa_social_20261022.md`, "a decidir") | usuário | aberto |
| P-07 | **Documentos do Instituto** (o usuário perguntou para quê). Pela lista de habilitação da SES (`biblioteca/instrumento/modelo_ses/`): estatuto (2.2), CNPJ com CNAE de saúde (2.3), CNES (2.4), certidões (2.5 a 2.13, 3.2, 3.3), dirigentes (3.1) e capacidade técnica (4.1: portfólio, instrumentos com outros entes, experiência em projetos semelhantes, responsável técnico, currículos). O plano usa a identificação e o representante; a capacidade técnica é o ponto fraco de um CNPJ distrital novo | usuário | aberto, sem pressa |

**Nota sobre a P-03.** Por que importa onde se executa:
- a OCI se registra em APAC no CNES de quem executa, e a ficha pede CBO e equipamento (`biblioteca/instrumento/enquadramento_cnes.md`);
- a lista de habilitação da SES pede o CNES (2.4);
- o MPCDF chamou de quarteirização a execução do IEV toda em clínicas de terceiros, com o IEV como consultório isolado no CNES (CT-002);
- o ISHP foi atacado por CNPJ distrital recente e sem experiência comprovada (LI-024);
- a subdelegação só vale se o plano listar o que vai a terceiro, e nunca a execução inteira (LI-025, art. 33 do Decreto 48.727/2026).

Parceria com clínica cabe, desde que o núcleo assistencial fique com o Instituto e o plano diga o que vai a cada clínica. O que o CNES não tiver na data do plano entra como etapa de implantação, no mês 1, com responsável.

## Do assistente (fase 0)

| | tarefa | estado |
|---|---|---|
| A-01 | A emenda no Portal da Transparência: individual (RP 6), R$ 20,7 mi empenhados e pagos, R$ 12,3 mi ao Fundo de Saúde do DF em 2024 (`estado.yaml`, `recurso`). Falta confirmar a norma de 2024 (a GM/MS 3.283/2024, fora do acervo) pelo agente `normas` | **feito em 22/10/2026**, menos a norma |
| A-02 | CNES e matriz do Instituto: sem CNES; matriz no RJ desde 2014; dirigente na Receita (`estado.yaml`, `proponente_dados`) | **feito em 22/10/2026** |
| A-03 | Fichas do SIGTAP das sete OCI, competência 10/2026 (agente `ficha-sigtap`), 6/7: falta o catálogo do grupo 09 de 10/2026. A 10/2026 foi reconstituída pelas Notas Técnicas, porque o site estava parado em 05/2026: reler na tela quando voltar | **feito em 22/10/2026**, com a releitura pendente |
| A-04 | Fila no Mapa Social (`dados/fontes/mapa_social_20261022.md`, 7/7) e preços (`dados/precos.md`, 8/9, a I não se aplica). Cotações a pedir no DF: cintilografia, eco de estresse e pacotes por volume (`dados/precos.md`, seção 7) | **feito em 22/10/2026** |
| A-07 | Estudos para o usuário (como a OCI se paga e muda, o IEV e o erro dele, a habilitação do Instituto, com Word e PDF para a equipe): `estudos/` | **feito em 22/10/2026** |
| A-05 | Reaproveitar o estudo de agosto (`planos/redacao/regras_oci_cardiologia.md`), reconferido contra as fichas novas | aberto |
| A-06 | Sobreposição com os projetos em andamento: `dossie/sobreposicao.md` | **feito em 22/10/2026** |
| A-08 | Dossiê das sete OCI: `dossie/comparativo.md` e `justificativa.md`, 8/8. A suíte do ramo dá 32/40: as oito falhas são o catálogo do grupo 09 de 10/2026, que não existe (vigia de normas) | **feito em 22/10/2026** |
