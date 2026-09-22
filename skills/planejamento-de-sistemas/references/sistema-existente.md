# Planejar dentro de um repositório que já existe

Aqui o risco muda de lugar. Em projeto novo, o perigo é a especificação ser vaga; em projeto
existente, o perigo é ela **contradizer a realidade** — propor uma tabela que já existe com outro
nome, um padrão que o projeto abandonou, uma biblioteca que foi trocada. Uma especificação que briga
com o código é pior que nenhuma, porque a IA construtora obedece a ela e quebra o que funcionava.

## Antes de perguntar qualquer coisa: leia

Leia o repositório e chegue na entrevista com afirmações a confirmar, não com perguntas de
formulário. Levante:

- `README.md`, `CLAUDE.md`, `docs/`, ADRs — o que o projeto diz de si.
- Gerenciador de pacotes, versões, scripts de build, teste e execução.
- Estrutura de pastas e o padrão de organização (por camada, por funcionalidade, por domínio).
- Modelo de dados: migrations, schema, convenção de nome de tabela e coluna.
- Um módulo recente e completo — é o melhor retrato do padrão vigente, melhor que a documentação.
- Autenticação, autorização, tratamento de erro, log, configuração: como já são feitos.
- Testes: o que existe, onde ficam, como rodam, o que se usa no lugar de serviços externos.
- Histórico recente (`git log`): o que anda mudando e o que ninguém toca.

Anote o que você **não** conseguiu descobrir; isso vira pergunta com prioridade.

## O que muda na entrevista

Acrescente aos blocos de `entrevista.md`:

- O que já existe e resolve parte do problema? O novo módulo estende, substitui ou convive?
- O que **não pode quebrar** de jeito nenhum? (consumidores em produção, integrações, relatórios,
  jobs) Isso vira invariante, e normalmente vira também um prompt de testes de não-regressão.
- Há dívida conhecida nessa área que vale arrumar junto, ou passamos ao largo? Decida explicitamente:
  refatoração que aparece no meio da obra sem ter sido combinada é a maior fonte de atraso.
- Precisa de migração de dados? Quem faz, com que janela, e como se volta atrás.
- Há bandeira de funcionalidade (feature flag) ou o módulo nasce ligado?
- Quem revisa e como o código entra: branch, PR, aprovação.

## O que muda no documento 00

Continua sendo o contrato entre os prompts, mas ganha duas seções e perde peso nas outras:

- **§ O que já existe** — mapa curto do estado atual da área afetada: arquivos, tabelas, endpoints,
  jobs, com uma linha do que cada um faz hoje. É o que impede a IA de recriar o que já está lá.
- **§ O que muda e o que não muda** — tabela com três colunas: item | hoje | depois. Inclua as linhas
  "não muda" que alguém poderia achar que mudam.
- **Convenções** deixam de ser escolha e viram **observação**: "o projeto usa X; siga X mesmo que
  você prefira Y". Se algo precisa mesmo mudar, é decisão numerada com motivo, e o novo padrão vale
  só dali para frente, dito assim com todas as letras.

## O que muda nos prompts

- **Inventário no começo.** Cada prompt lista os arquivos que vai criar **e** os que vai alterar,
  dizendo o que muda em cada um. Editar um arquivo existente sem isso é como a especificação apaga
  comportamento por acidente.
- **Prompt de fundação vira prompt de reconhecimento.** Em vez de criar o repositório, a primeira
  sessão confirma que o ambiente sobe, os testes passam antes de qualquer mudança (a linha de base
  importa: sem ela ninguém sabe se a suíte já estava vermelha), e registra o estado num ADR.
- **Cada prompt termina com a suíte existente verde**, não só com os testes novos. Ponha isso nos
  critérios de aceite, explicitamente.
- **Compatibilidade como invariante.** Se há consumidor em produção, o contrato atual é lei: só
  acréscimo. Vale a pena um prompt só de testes que congelam o comportamento atual **antes** de
  mexer — é o que transforma "acho que não quebrei" em "sei que não quebrei".
- **Reversão.** Para mudança arriscada, o prompt diz como desfazer: bandeira, migração reversível,
  ordem de deploy.

## Ordem que costuma funcionar

| # | Prompt | Entrega |
|---|---|---|
| 00 | *(referência)* Visão geral, o que existe, o que muda | Contrato entre os prompts |
| 01 | Reconhecimento e linha de base | Ambiente sobe, suíte verde registrada, ADR do estado atual |
| 02 | Rede de proteção | Testes que congelam o comportamento atual da área afetada |
| 03 | Dados | Migrations novas, compatíveis com o que já está gravado |
| 04+ | Funcionalidade | Um prompt por fluxo, cada um com inventário de arquivos alterados |
| … | Integração com o que existe | Ligar o módulo novo aos pontos de entrada atuais |
| … | Migração e virada | Script de migração, bandeira, ordem de deploy, rollback |
| … | *(manual)* Operação | O que uma pessoa faz na virada e depois dela |
