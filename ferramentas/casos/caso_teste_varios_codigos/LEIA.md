# caso_teste_varios_codigos/ — caso de teste, não é o plano 4

Cópia **congelada** do plano 4 (ultrassonografia e tomografia) na **v10, de 24/09/2026**.
Existe só para testar a conferência num plano de **vários códigos e vários unitários**.
É o único caso desse tipo; o `redacao_03` testa o plano de um código só.

**O plano 4 não mora aqui.** Ele está em andamento no ramo
`plano-04-ultrassom-tomografia`, na pasta `redacao_04/`. O conteúdo desta pasta está
desatualizado de propósito e não serve de fonte para nada do plano.

Quem usa esta pasta:
- `testar_tudo.py`, que roda nela o `conferir_plano.py` e, com `--mutacoes`, o
  `testar_conferencia_plano.py`;
- quem mexer na conferência e precisar de um plano de vários códigos para testar.

**Não editar.** Se uma mudança na conferência quebrar este caso, o defeito é da conferência
ou o caso precisa de uma atualização deliberada, registrada em commit próprio.

Origem: consolidação de 08/10/2026. Até então, esta cópia ficava em `redacao_04/` no
`main`, e eram duas versões do plano 4 com o mesmo nome.
