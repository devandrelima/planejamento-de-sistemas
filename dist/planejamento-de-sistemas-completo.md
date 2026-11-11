# Planejamento de Sistemas 2.0 — instruções completas

> Documento único para assistentes sem suporte a skills. Para executar a CLI e seus testes,
> utilize o pacote da skill com o script scripts/fluxo.py.
> Este documento contém exclusivamente instruções e modelos da metodologia atual.
> Gerado de forma reproduzível a partir das fontes do repositório.

---


<!-- ARQUIVO: SKILL.md -->

# ARQUIVO: SKILL.md

# Planejamento de Sistemas 2.0

A única metodologia deste repositório organiza a construção de software em PROJETO → SPRINT → PROMPT-MAPA → TASK. O humano recebe os mapas; o agente recebe a task e seu contexto mínimo. Toda sprint deve entregar um incremento executável, integrado, testado e avaliado pelo humano antes da seguinte.

## Fase 1 — Descobrir e definir

Leia references/entrevista.md, references/planejamento-mvp.md e, se houver código prévio, references/sistema-existente.md. Identifique usuário, problema, prazo, recursos, riscos, dados, integrações, stack e a primeira funcionalidade que a pessoa realmente poderá executar. Separe Agora / Depois / Não construir. Confirme decisões e pendências que bloqueiam a execução.

## Fase 2 — Planejar entregas

Leia references/fluxo-v2.md, references/paralelismo-v2.md e references/design-adaptativo.md. Para cada sprint:
- Descreva o valor entregue, como executar o aplicativo, os dados de teste e os fluxos de regressão.
- Defina 1–3 prompts-mapa (preferência por 2, sem criar trabalho artificial).
- Decomponha os mapas em tasks pequenas, com dependências, contexto, comandos de testes, arquivos de leitura/escrita e critérios objetivos.
- Feche contratos compartilhados antes de autorizar agentes em paralelo.
- Escolha skills de design realmente instaladas somente nas tarefas que precisam delas.

## Fase 3 — Gerar a especificação

Leia references/contexto-v2.md e references/testes-progressivos.md. Use exclusivamente os modelos de assets/v2/. Para o projeto que será construído, gere:

- docs/especificacao/README.md e 00_visao_geral_e_decisoes.md.
- docs/especificacao/plano.json, com schema_version "2.0", human_gate true, coverage_min 80, full_suite_every 3.
- docs/especificacao/sprints/S01/P01.md como mapa humano e sprints/S01/tasks/T01.json e demais tasks.
- docs/especificacao/memoria/global.md, memórias curtas de cada domínio e contratos canônicos quando necessários.
- ESTADO.json na raiz, com tasks pendentes e sprints sem aceite; docs/decisoes/ com registros de decisão, quando necessário.

Mapas e manifestos no plano são caminhos relativos à pasta docs/especificacao. Contexto, leituras e escritas de cada task são relativos à raiz do aplicativo. Não exigir o repositório todo por padrão nem repetir contrato em vários resumos. Decisões que impactam tasks futuras exigem revisão de seus manifestos.

## Fase 4 — Validar e executar

A ferramenta scripts/fluxo.py roda com Python 3.10+ sem dependências externas. Executando-a a partir deste repositório, prefixe skills/planejamento-de-sistemas/scripts/.

Exemplos de comandos no projeto do aplicativo:

    python3 scripts/fluxo.py --repo CAMINHO validar
    python3 scripts/fluxo.py --repo CAMINHO prontas
    python3 scripts/fluxo.py --repo CAMINHO contexto S01-P01-T01
    python3 scripts/fluxo.py --repo CAMINHO sincronizar

O humano entrega um prompt-mapa; o executor carrega cada task pelo comando contexto, implementa, roda testes locais e registra commit e resultados. O integrador inspeciona mudanças e evidências, testa regressão dos fluxos afetados, mede cobertura do código alterado >=80%, executa o aplicativo e apresenta roteiro de demonstração.

**Pausa obrigatória após cada sprint:** aguardar decisão explícita da pessoa. Se pedir mudanças, reformular tasks e sincronizar o estado sem apagar histórico. Se aprovar, registrar feedback, testes, cobertura e demo. Rodar suíte completa com cobertura global >=80% na terceira sprint, na última e antecipadamente por risco elevado ou impacto transversal.

O comando prontas identifica tasks elegíveis e um lote sem conflitos diretos de escrita. Se paralelizar, usar worktrees/branches independentes, integrar em sequência e manter um único responsável por ESTADO.json. A ferramenta não inicia agentes, não impõe isolamento de arquivos, não autentica o aprovador e não executa os testes do aplicativo. Evidências e métricas registradas são declarações que precisam ser verificadas em Git, logs e CI.

## Regras de qualidade

- Segurança, integridade e contratos nunca podem ser sacrificados para reduzir tokens.
- Não invente medições de cobertura, testes executados, consumo de tokens, skills instaladas ou aplicativos demonstrados.
- Cada task deve ser suficientemente precisa para um modelo menos capaz, sem repetir informações desnecessárias.
- Evite componentes sem uso e infraestrutura que não faça parte do MVP.
- Interface precisa de revisão visual, acessibilidade, estados e responsividade.
- Se o contexto autorizado for insuficiente, ampliar de modo justificado e atualizar o manifesto; nunca truncar invariantes.
- Não iniciar a próxima sprint sem aceite humano.

## Referências disponíveis

| Caminho | Responsabilidade |
|---|---|
| references/entrevista.md | Descoberta e decisões |
| references/planejamento-mvp.md | Recorte viável |
| references/sistema-existente.md | Planejamento em código existente |
| references/fluxo-v2.md | Hierarquia e execução por entregas |
| references/contexto-v2.md | Memória seletiva e orçamento |
| references/testes-progressivos.md | Testes por task, sprint e checkpoint |
| references/paralelismo-v2.md | Dependências e agentes isolados |
| references/design-adaptativo.md | Seleção de skills e qualidade visual |
| references/qualidade.md | Checklist de revisão |
| assets/v2/ | Templates do formato atual |
| scripts/fluxo.py | CLI e validador estrutural |


---


<!-- ARQUIVO: references/entrevista.md -->

# ARQUIVO: references/entrevista.md

# Entrevista para planejamento de sistemas

Objetivo: fechar apenas as decisões que afetam execução, demonstração e segurança. Pergunte em rodadas curtas, propondo padrões fundamentados; leia o repositório antes de perguntar algo já documentado.

## 1. Problema e resultado

- Quem usa? Que necessidade resolve? Como a pessoa resolve isso hoje?
- Qual fluxo o usuário precisa conseguir realizar para considerar a primeira entrega útil?
- Como será demonstrado e avaliado: dados fictícios, dispositivo, ambiente local, acesso?
- Qual prazo, equipe, experiência com a stack e recursos disponíveis?
- O que é indispensável agora, o que pode vir depois e o que está expressamente excluído?

## 2. Dados, papéis e regras

- Quais entradas, saídas, entidades, regras e cálculos devem existir?
- Quem pode consultar, editar e excluir o quê? É necessário login ou autorização?
- Quais erros esperados e estados vazios o usuário encontrará?
- Quais dados são sensíveis? Que operações precisam de auditoria, precisão, idempotência ou isolamento?
- Há migração de sistema existente? Que comportamento é obrigatório preservar?

## 3. Integrações e arquitetura

- Há sistemas externos, formatos CSV/JSON, limites de serviço, autenticação de API ou credenciais necessárias?
- Que stack e ambiente já existem? Qual solução simples atende aos requisitos de agora?
- Quais contratos compartilhados precisam ser definidos antes de paralelizar backend e interface?
- Quais dependências e riscos podem bloquear a primeira demonstração?

## 4. Interface, testes e operação

- Estilo visual, referências, usuários-alvo, dispositivo principal, acessibilidade e navegação?
- Como iniciar o projeto e alimentar dados de teste, sem depender de segredos reais?
- Que testes comprovam comportamento e regressão? Qual ferramenta mede os 80%?
- O que exige ação humana (conta, token, aprovação, deploy) e o que não pode ser executado pelo agente sem permissão?

## 5. Fechamento

Consolide: objetivo do produto, Agora/Depois/Não construir, decisões com motivos, pendências bloqueadoras, riscos e roteiro executável da primeira sprint. Confirme o resumo com o humano antes de expandir em mapas e tasks. Não prolongue a entrevista para escolher detalhes que podem ser resolvidos com padrões explícitos e seguros.


---


<!-- ARQUIVO: references/planejamento-mvp.md -->

# ARQUIVO: references/planejamento-mvp.md

# Planejamento orientado a MVP

Um MVP deve produzir **valor utilizável**, não apenas estruturas de código. O fluxo de valor determina a sprint; dependências técnicas cabem dentro das tasks necessárias para entregar esse fluxo.

## Viabilidade

Registre prazo real, horas disponíveis, número e experiência dos executores, orçamento, ambiente, integrações, riscos e critério de demonstração. Divida capacidades em:
- **Agora:** sem elas, a primeira experiência não existe ou fica insegura.
- **Depois:** agregam valor, mas não bloqueiam o incremento atual.
- **Não construir:** estão expressamente fora do escopo.

## Recorte

1. Descreva o primeiro fluxo completo em uma frase observável pelo usuário.
2. Identifique requisitos de dados, interface e integração necessários ao fluxo.
3. Defina contratos estáveis, dependências e testes indispensáveis.
4. Divida em tasks pequenas, organizadas em até três prompts-mapa por sprint.
5. Faça estimativas por faixas de complexidade e reserve tempo para integrar, testar e receber feedback.
6. Se o plano exceder recursos, reduza funcionalidades; nunca remova verificações de segurança, precisão ou dados críticos.
7. Pare quando o incremento tiver um roteiro de execução real e critérios de aceite mensuráveis.

## Regras de bom senso

Projeto offline não precisa obrigatoriamente de login ou infraestrutura remota. Um CSV não implica banco de dados. Um recurso local não exige cloud ou API paga. Precisão financeira, isolamento de dados, tratamento de erros e testes essenciais continuam obrigatórios quando relevantes.

A revisão final rejeita dependências ocultas, interfaces inexecutáveis e sprints que apenas geram pastas sem funcionalidade utilizável.


---


<!-- ARQUIVO: references/sistema-existente.md -->

# ARQUIVO: references/sistema-existente.md

# Planejar uma alteração num sistema existente

Antes da entrevista, leia o código real. Documentos desatualizados e convenções inventadas produzem tasks que quebram o sistema.

## Reconhecimento seletivo

Inspecione README, configurações, scripts de execução e CI, um módulo recente completo, tipos/contratos, modelo de dados, autenticação e testes da área afetada. Verifique alterações recentes. Não mande todo o código aos executores: produza um mapa curto com **arquivos afetados, dependentes e contratos canônicos**.

## Decisões

- O que já existe e será preservado?
- O que muda e como afeta usuários/consumidores?
- É necessária migração ou reversão?
- Que fluxos anteriormente aprovados podem sofrer regressão?
- Que parte do trabalho pode ser paralela após estabilizar os contratos?
- Quem integra e aprova o incremento?

## Transformar em tasks

Cada task de alteração deve declarar arquivos de leitura e escrita, decisão que a autoriza, comportamento preservado, novos casos de teste e critérios de aceite. Exija teste de regressão reproduzindo comportamentos existentes antes de fazer alterações arriscadas. Se a suíte inteira for muito lenta, identifique subconjunto local seguro; no fechamento da sprint rode a regressão afetada e antecipe suíte completa quando o risco for transversal ou incerto.

A demonstração de cada sprint deve iniciar o sistema existente e exercitar o fluxo novo sem romper o anterior. Mantenha histórico de alterações de contratos e regenere pacotes de contexto das tasks dependentes.


---


<!-- ARQUIVO: references/fluxo-v2.md -->

# ARQUIVO: references/fluxo-v2.md

# Metodologia 2.0 — sprints, prompts-mapa e tasks

Este documento define o único fluxo de execução da skill.

## Hierarquia

- **Sprint:** incremento executável e demonstrável com 1 a 3 prompts (padrão recomendado: 2), encerrado somente após avaliação explícita do humano.
- **Prompt-mapa:** documento que a pessoa seleciona e entrega ao agente, descrevendo objetivo, tasks e dependências. Não é o contexto de execução inteiro.
- **Task:** instrução operacional pequena, com contrato, dependências, arquivos de leitura/escrita, critérios verificáveis, testes e orçamento contextual.

O primeiro incremento entrega valor ponta a ponta, não apenas pastas e configurações. Login só é a primeira entrega quando o produto realmente precisa.

## Sequência

1. Entrevistar e fechar decisões, prazo, recursos, MVP, riscos, contratos e demonstração.
2. Escolher sprints executáveis, até três prompts-mapa por sprint e tasks por prompt.
3. Criar docs/especificacao/plano.json, sprints/S01/P01.md, tasks JSON, memória global/por domínio, contratos, README, documento 00 e ESTADO.json na raiz do projeto.
4. Validar com fluxo.py validar; corrigir erros objetivos e revisar qualidade semântica manualmente.
5. O humano seleciona o mapa; o executor carrega fluxo.py contexto ID, sem receber toda a especificação.
6. Cada task executa testes locais; após integrar, regressão dos fluxos afetados, cobertura alterada >=80% e demonstração executável.
7. Pausar para avaliação humana. Ajustes exigem replanejamento, e a sprint seguinte fica bloqueada até aceite.
8. A cada terceira sprint, na última e antes por risco elevado, rodar suíte completa e verificar cobertura global >=80%.

As evidências registradas em ESTADO.json são declarações, não verificação automática. O integrador confere commits, logs e resultados reais. A CLI não autentica a identidade de quem aprova.

## Replanejamento com feedback

Depois de registrar ajustes, acrescente novas tasks ao manifesto e use fluxo.py sincronizar para incluir somente novos IDs no ESTADO.json. O comando conserva evidências das tasks existentes, recusa eliminação silenciosa de IDs e proíbe acrescentar tasks a sprints aprovadas. Faça a atualização de documentos e estado em commits revisáveis.

## Regra de qualidade

Nenhuma sprint termina com apenas código isolado. O resultado é uma aplicação executável, preserva as entregas aprovadas e expõe uma funcionalidade observável ao usuário.


---


<!-- ARQUIVO: references/contexto-v2.md -->

# ARQUIVO: references/contexto-v2.md

# Memória seletiva por task

## Regras

A task declara context, reads e writes com caminhos relativos à raiz do projeto. O plano declara global_context. O executor recebe apenas memória global pequena, contexto do domínio, arquivos explicitamente autorizados e descrição da task.

A ferramenta fluxo.py contexto monta o pacote em ordem estável, registra SHA-256 de cada arquivo de origem e estima tokens como caracteres/4. Se ultrapassar context_budget_tokens, recusa sem truncar material importante. Esta estimativa não representa tokens faturáveis de modelos comerciais.

O pacote não deve repetir o repositório inteiro, documentação de domínios estranhos ou logs antigos. Contratos permanecem como fonte canônica; memórias apontam para eles, não criam cópias inconsistentes. Estado de execução fica em ESTADO.json e a prova real é Git + logs.

Mudança em contrato, API, schema ou decisão compartilhada invalida contextos dependentes, que precisam ser refeitos. Quando uma task descobrir dependência inesperada, registre o motivo e atualize seu manifesto antes de prosseguir. Não omita arquivo essencial só para baixar tokens.

Use modelos menores em tarefas fechadas e reserve revisão especializada para decisões complexas. Medir custo total de tokens exige contabilizar tentativas e retrabalho, não apenas tamanho do contexto inicial.


---


<!-- ARQUIVO: references/testes-progressivos.md -->

# ARQUIVO: references/testes-progressivos.md

# Testes progressivos e checkpoints

O ciclo divide verificações de acordo com a unidade de execução e o risco.

**Task:** antes de implementar comportamento, escreva teste local e observe a falha correta. Implemente, rode testes locais, lint, tipagem e build rápidos quando aplicáveis; registre comandos, resultados e arquivos alterados.

**Sprint:** após integrar as tasks, rode a regressão de todos os fluxos afetados, inclusive fluxos aprovados que dependem das alterações. Inicie o sistema e demonstre a entrega. Meça cobertura >=80% do código novo ou alterado com ferramenta compatível e registre escopo e comando.

**Checkpoint global:** a cada 3 sprints por padrão, na última sprint e antecipadamente por risco alto/crítico, mudança transversal, autenticação, autorização, banco compartilhado ou impacto desconhecido, execute a suíte completa e meça cobertura global >=80%.

Testes de precisão financeira, segurança, isolamento e concorrência não desaparecem quando o percentual atinge 80%. Cobertura não prova correção. Se não há medição confiável, registre pendência em vez de inventar percentual ou aprovar.

A CLI exige evidências declaradas de regressão, demo e cobertura alterada para aprovação; nos checkpoints, exige suíte completa e cobertura global. Ela não executa testes do aplicativo; integrador e CI devem verificar comandos e logs.

Não baixar limites para passar, não pular testes ou mascarar falhas. Sistemas existentes abaixo de 80% devem possuir um plano de recuperação documentado antes de prometer conformidade.


---


<!-- ARQUIVO: references/paralelismo-v2.md -->

# ARQUIVO: references/paralelismo-v2.md

# Dependências e agentes paralelos

A CLI lista tasks prontas somente quando as dependências foram concluídas e as sprints anteriores receberam aceite humano.

A seleção parallel_batch evita colisões diretas nos caminhos declarados em writes. Tasks declaradas no mesmo parallel_group com conflito de escrita causam erro de validação. O detector não substitui análise de dependências semânticas.

Execução recomendada: agente integrador escolhe tasks, cria worktrees ou branches isoladas e fornece a cada executor somente seu pacote. Cada executor roda testes locais, registra commit e entrega relatório. O integrador revisa os diffs, faz merge serial, resolve conflitos e é o único responsável por atualizar ESTADO.json.

Contrato precisa estar estabilizado antes de backend e UI trabalharem em paralelo. Se surgirem arquivos compartilhados não previstos, suspenda paralelismo, corrija manifestos e regenere contexto.

A CLI **não lança agentes, não faz merge e não impede um agente de editar arquivos fora de writes**. Para isso são necessárias permissões e isolamento externos. Paralelismo pode reduzir tempo de calendário e aumentar custo de tokens; medir quando for relevante.


---


<!-- ARQUIVO: references/design-adaptativo.md -->

# ARQUIVO: references/design-adaptativo.md

# Direção de design adaptativa

Antes de gerar tasks de interface, registrar público, dispositivos, navegação principal, referências visuais, estilo, acessibilidade, performance e expectativas do usuário.

Inventariar **skills de design realmente disponíveis** no ambiente em que o agente executará. Selecionar o conjunto mínimo útil com base em UX/UI, stack, acessibilidade, conflitos entre instruções e custo contextual; documentar motivo e fallback quando não existirem skills compatíveis. Não inventar ferramentas instaladas nem prometer beleza objetiva.

Toda task de interface inclui design.review e design.skills_selection, além de contexto de UI; tasks de backend não carregam esses materiais. Revisão final: hierarquia, estados de erro/vazio/carregamento, responsividade, navegação por teclado, foco e contraste. Se puder executar ou capturar a interface, avaliar visualmente; caso contrário, registrar a limitação.

O feedback da sprint atualiza o briefing e as tasks ainda não realizadas. Mudanças visuais exigem testes dos fluxos afetados e novo aceite humano.


---


<!-- ARQUIVO: references/qualidade.md -->

# ARQUIVO: references/qualidade.md

# Checklist de qualidade do plano

## Planejamento e entregas

- [ ] O MVP tem prazo, recursos, riscos e fluxo utilizável definidos.
- [ ] Cada sprint entrega uma versão que o usuário pode iniciar e experimentar.
- [ ] Existem 1–3 prompts-mapa por sprint; maps relacionam tasks e não repetem toda a memória.
- [ ] Cada task contém objetivo, saída, contexto, leituras/escritas, dependências, testes e aceite observável.
- [ ] Contratos compartilhados estão definidos antes de tarefas paralelas.
- [ ] Execução de agentes independentes não disputa arquivos e usa integração controlada.

## Contexto e decisões

- [ ] A memória global é curta e não inclui segredos.
- [ ] Cada task recebe somente o domínio e arquivos relevantes.
- [ ] Contratos são fonte única de verdade, sem cópias divergentes.
- [ ] Mudanças de contratos invalidam contextos dependentes e atualizam manifestos.
- [ ] Orçamento estimado de tokens não omite condições de segurança.

## Testes, experiência e aceite

- [ ] Testes locais cobrem a task que está sendo escrita.
- [ ] Testes dos fluxos afetados verificam a sprint integrada.
- [ ] Cobertura do código alterado >=80% é medida, não presumida.
- [ ] Suíte completa e cobertura global >=80% ocorrem na terceira sprint, última ou antes por risco.
- [ ] Tasks de UI usam apenas skills realmente disponíveis e revisão visual, acessibilidade e estados de interface.
- [ ] A próxima sprint fica bloqueada até feedback e aceite humano.
- [ ] Plano e estado passam por scripts/fluxo.py validar.
- [ ] Não se afirma execução real, cobertura, economia de tokens ou produtividade sem evidências externas.


---


<!-- ARQUIVO: assets/v2/00_visao_geral_e_decisoes.md -->

# ARQUIVO: assets/v2/00_visao_geral_e_decisoes.md

# Visão geral e decisões

## Produto e público
- Nome e objetivo:
- Usuários e necessidades:
- Fluxo de valor que será demonstrado:

## Viabilidade e escopo
| Agora | Depois | Não construir |
|---|---|---|
| Funcionalidade mínima demonstrável | Evolução posterior | Limite explícito |

Prazo, equipe, experiência, orçamento e dependências:

## Arquitetura e dados
- Stack confirmada e justificativa:
- Entidades e persistência:
- Contratos e formatos de dados:
- Execução local e dados fictícios:

## Decisões
| ID | Escolha | Motivo | Impacto |
|---|---|---|---|
| D1 | Decisão concreta | Razão verificável | Tasks relacionadas |

## Invariantes e segurança
- Regras que nunca podem quebrar:
- Dados sensíveis, autenticação e permissões:
- Critérios de erro e recuperação:

## Estratégia de entrega e testes
- Primeira sprint e demo executável:
- Testes locais por task, regressão afetada por sprint:
- Cobertura alterada >=80%; global >=80% nos checkpoints:
- Pausa e avaliação humana obrigatórias:

## Riscos e pendências
| Questão | Impacto | Responsável | Como resolver |
|---|---|---|---|
| Decisão pendente, se houver | Task bloqueada | Pessoa responsável | Ação concreta |


---


<!-- ARQUIVO: assets/v2/README_indice.md -->

# ARQUIVO: assets/v2/README_indice.md

# Índice de especificação executável

Este projeto usa exclusivamente a metodologia 2.0: sprint como entrega funcional, prompt como mapa humano, task como unidade real de execução.

| Item | Tipo | Dependências | Entrega |
|---|---|---|---|
| 00_visao_geral_e_decisoes.md | Referência | — | Contrato de produto e arquitetura |
| plano.json | Manifesto | Documento 00 | Sprints, mapas e tasks |
| sprints/S01/P01.md | Mapa humano | Plano | Sequência de tarefas para o agente |
| sprints/S01/tasks/T01.json | Task | Contratos citados no manifesto | Alteração e teste verificáveis |
| memoria/global.md | Contexto global | Documento 00 | Invariantes de todas as tasks |
| memoria/dominio.md | Contexto do domínio | Contratos | Decisões locais e arquivos relevantes |
| ESTADO.json (na raiz) | Estado | Plano | Progressão, commits e aceite humano |

O executor deve obter o contexto da task com scripts/fluxo.py contexto, e não ler todos os documentos antecipadamente.


---


<!-- ARQUIVO: assets/v2/SPRINT.md -->

# ARQUIVO: assets/v2/SPRINT.md

# S01 — Primeira entrega utilizável

## Valor e viabilidade
Que fluxo o usuário poderá executar? Qual o prazo e recursos?

## Demonstração
Comando local, dados fictícios, roteiro para pessoa testar, critérios de aceite.

## Mapas
| Mapa | Tasks | Dependências | Entrega |
|---|---|---|---|
| P01 | S01-P01-T01 | — | Resultado observável |

## Qualidade
Testes locais por task, regressão afetada por sprint, cobertura alterada >=80%.
Suíte completa e cobertura global >=80% em checkpoint ou risco elevado.
Aguardar aprovação humana após demonstração.


---


<!-- ARQUIVO: assets/v2/PROMPT_MAPA.md -->

# ARQUIVO: assets/v2/PROMPT_MAPA.md

# P01 — Mapa humano da Sprint S01

Objetivo do incremento: resultado executável e visível ao usuário.

Tasks: S01-P01-T01, S01-P01-T02. Informar ordem, dependências, risco e possibilidade de paralelismo somente com contratos definidos.

O humano seleciona este mapa. O agente executa cada task liberada a partir do pacote retornado por fluxo.py contexto ID. Não passar o projeto inteiro para cada executor.

Ao integrar: verificar testes dos fluxos afetados, cobertura e demonstrar o sistema. Solicitar feedback e pausar antes da próxima sprint.


---


<!-- ARQUIVO: assets/v2/plano.json -->

# ARQUIVO: assets/v2/plano.json

{
  "schema_version": "2.0",
  "product": "NOME_DO_PRODUTO",
  "human_gate": true,
  "coverage_min": 80,
  "full_suite_every": 3,
  "global_context": [
    "docs/especificacao/memoria/global.md"
  ],
  "sprints": [
    {
      "id": "S01",
      "title": "Primeiro fluxo de valor",
      "delivery": "Fluxo utilizável e demonstrável",
      "demo_command": "COMANDO_LOCAL",
      "regression_tests": [
        "COMANDO_TESTES_AFETADOS"
      ],
      "risk": "low",
      "requires_full_suite": false,
      "prompts": [
        {
          "id": "P01",
          "map": "sprints/S01/P01.md",
          "tasks": [
            "sprints/S01/tasks/T01.json"
          ]
        }
      ]
    }
  ]
}


---


<!-- ARQUIVO: assets/v2/task.json -->

# ARQUIVO: assets/v2/task.json

{
  "id": "S01-P01-T01",
  "kind": "backend",
  "instruction": "Objetivo técnico concreto",
  "result": "Código e teste verificáveis",
  "depends_on": [],
  "context": [
    "docs/especificacao/memoria/dominio.md"
  ],
  "reads": [],
  "writes": [
    "src/modulo.py"
  ],
  "tests": [
    "COMANDO_TESTES_LOCAIS"
  ],
  "acceptance": [
    "Condição verificável da entrega"
  ],
  "context_budget_tokens": 2500
}


---


<!-- ARQUIVO: assets/v2/ESTADO.json -->

# ARQUIVO: assets/v2/ESTADO.json

{
  "schema_version": "2.0",
  "tasks": {
    "S01-P01-T01": {
      "status": "pendente"
    }
  },
  "sprints": {
    "S01": {
      "status": "pendente",
      "human_approved": false
    }
  }
}


---


<!-- ARQUIVO: assets/v2/memoria-global.md -->

# ARQUIVO: assets/v2/memoria-global.md

# Memória global (minimizar)

Objetivo: descrição curta do produto.
Invariantes: regras universais verificáveis, segurança e privacidade.
Contratos canônicos: links relativos para fonte de verdade.
Convenções mínimas: idioma, stack e organização.

Não copiar domínios inteiros, histórico de conversa, credenciais ou logs antigos.


---


<!-- ARQUIVO: assets/v2/memoria-dominio.md -->

# ARQUIVO: assets/v2/memoria-dominio.md

# Memória do domínio

Responsabilidade do domínio e fluxos envolvidos.
Contratos e decisões canônicos por caminho, sem cópias conflitantes.
Regras de negócio verificáveis e limites.
Testes locais e fluxos dependentes.
Diretórios permitidos e dependências compartilhadas.

Se mudar contrato, atualizar tasks e regenerar contextos.


---


<!-- ARQUIVO: assets/v2/ADR.md -->

# ARQUIVO: assets/v2/ADR.md

# NNNN — Título da decisão

Data: AAAA-MM-DD
Status: proposta | aceita | substituída | revogada

## Contexto e alternativas
Descrever fato observado, limitação e alternativas realmente analisadas.

## Decisão e motivo
Escolha inequívoca, critério de segurança/UX/custo e motivo.

## Impactos
Contratos e memórias afetados, IDs das tasks que precisam ser replanejadas, novos testes e possibilidade de reversão.


---
