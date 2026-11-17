# Melhorias na planilha organizada do estudo das filas de imagem

**Mapeado e aplicado em 02/11/2026,** a partir do que o usuário disse ao revisar
`estudo_filas_imagem_20261102_organizada.xlsx`. Os números vêm de `estudo_filas_imagem_20261102.py`, e a forma vem de
`formatar_estudo_filas_imagem_20261102.py`. A carteira 1 não mudou: as cinco carteiras saem iguais às da manhã.

## 1. As cinco abas que o usuário pediu para melhorar — aplicado

| aba | o que o usuário disse | o que mudou |
|---|---|---|
| **Encaminhamento SES** | "não ficou legal" | abre com a pergunta "a SES precisa passar pedidos ao projeto?"; um exemplo resolvido (transvaginal); uma tabela exame a exame com "sobra para o projeto", "basta?" (sobram/faltam) e "quanto a SES precisa passar"; os três jeitos de a SES agir ficam embaixo, para comparar; a origem dos números no fim |
| **Faltas e pedidos** | "ficou ruim" | um exemplo resolvido (mama); depois duas tabelas separadas: o que a SES registrou nos 12 meses (agendamentos, realizados, faltas, cancelados, sem desfecho), e o que isso quer dizer para o projeto (vagas a publicar, faltas esperadas, pedidos gastos) |
| **Rumo das filas** | precisa melhorar | primeiro os 17 exames do plano, com entram, a SES agenda, sobra, a variação observada (15/09 a 02/11), os meses para zerar e "o que acontece com a fila" em palavras; depois os outros códigos, com menos colunas |
| **Filas** | precisa melhorar | primeiro as filas da carteira 1, por exame, com o que entra na carteira, os pedidos novos e o que fica fora; depois as outras filas, com 10 colunas e filtro |
| **Viabilidade** | só o que está no plano; cálculo mais preciso | só as filas da carteira 1; o custo aberto em sala, médico e insumo; o efeito da falta não reposta (20%); a sobra por exame, por hora de sala e na carteira; o que falta para a conta ficar precisa |

**Viabilidade: o que a conta mostra agora**
- **Todo exame da carteira tem sobra positiva com as faltas repostas.**
- **Com 20% das faltas sem reposição, a pélvica fica negativa,** e o Doppler de membros (40 minutos) sobra R$ 2 por
  exame. A mama também fica fina.
- **A sala rateada em 168 horas por mês está certa:** são as 8 horas de exame por dia útil × 21 dias. Não é
  inconsistência, como o mapa anterior sugeria.
- **Continuam premissas, para a etapa de custos:**
  - o médico a R$ 100 por hora e a forma de pagamento (por hora ou por exame);
  - o aluguel real da sala;
  - o insumo a R$ 3;
  - laudo, encargos e gestão;
  - o preço da TC por clínica;
  - o tempo real por exame.

## 2. Ofertas que estavam sem resposta — aplicado

| o quê | onde |
|---|---|
| quadro "Como ler", com o polo Sudoeste, no topo da aba Capacidade por polo | feito; a aba Encaminhamento SES tem o seu, com a transvaginal |
| aba IEV: "Pessoas" virou "Pessoas esperando na fila", e entrou um segundo quadro com as consultas que o IEV fez de 29/04 a 26/10 | feito |
| CNES das três unidades do IEV e da CIG Gama | feito: `../dados/fontes/cnes_unidades_iev_20261102.md`. Os três CNES existem, com os nomes e locais dos planos do IEV, mas são clínicas privadas, cada uma com o seu CNPJ; nenhuma é do IEV. A ligação com o IEV continua por indício. A CIG Gama é a mesma clínica indicada para o polo Sul do plano 4 |

## 3. Feito antes, na mesma tarde

- **Quem oferta:** só os 17 códigos da carteira 1, com a coleta `mapa_social_20261102_executante_c`. Fica uma
  limitação: o painel dá a unidade por código, e não por fila; na TC, entra a emergência do mesmo código.
- **Quem atende o quê:** a origem do número de OCI do IEV (plano e item da planilha) e a coluna "Com o IEV".
- **Enquadramento e Capacidade por polo:** 20 salas, 5 tomógrafos, 8 meses e a Região medida em 02/11.
- **Passo a passo do painel:** `passo_a_passo_painel/README.md`.

## 4. Decisões que continuam com o usuário

| decisão | por que importa |
|---|---|
| se a rede atende criança, inclusive transfontanela | 1.756 exames da carteira 1 são de filas infantis e de transfontanela |
| qual polo fica sem tomógrafo | a conta usou o cenário de 5 polos do estudo de 20/10, com a Leste atendida na Central e Centro-Sul |
| a CIG Gama no polo Sul | se ela também executa o IEV, as salas e o tomógrafo dela se dividem entre os dois convênios |
