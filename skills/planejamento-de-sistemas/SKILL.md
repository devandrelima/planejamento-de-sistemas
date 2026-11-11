---
name: planejamento-de-sistemas
description: Planeja sistemas e módulos com especificações executáveis para agentes de IA. Padrão v2 com sprints demonstráveis, prompts-mapa humanos, tasks JSON, memória seletiva, testes progressivos, revisão visual e aceite humano. Suporta o formato legado v1 com prompts executáveis. Use para planejamento, requisitos, MVP, arquitetura, decomposição em tasks, orquestração e desenvolvimento guiado por IA.
---

# Planejamento de Sistemas — 2.0

Converta a ideia do usuário em um plano operacional verificável que possa ser executado com agentes mais simples, pouco contexto e avaliação humana frequente. **A versão 2.0 é padrão em projetos novos.** Para continuar especificação 1.x já existente, use references/fluxo-v1.md e scripts/validar.py; não migre automaticamente.

## Organização obrigatória

**Projeto → Sprint → Prompt-mapa → Task executável.**

- Sprint: entrega de ponta a ponta que o usuário consegue iniciar, utilizar e avaliar. Nunca avançar sem aceite humano explícito.
- Prompt-mapa: documento para o humano selecionar e entregar ao agente; relaciona tarefas, dependências e entrega. Não é o contexto integral do executor.
- Task: instrução concreta para um agente, com dependências, arquivos autorizados, memória, testes locais, orçamento de contexto e critérios de aceite.

Use 1 a 3 prompts por sprint; 2 como preferência, não obrigação. Quebre tasks até que possam ser executadas sem decisão arquitetural implícita. A primeira sprint entrega valor verificável, não apenas infraestrutura sem interface/fluxo útil. Login é exemplo, não pré-requisito universal.

## Fase 1 — Entrevista, escopo e MVP

Leia references/entrevista.md e references/planejamento-mvp.md. Pergunte em rodadas curtas, proponha padrões, identifique prazo, orçamento, equipe, experiência, fluxo principal, stack, atores, segurança, dados, integrações, decisões, riscos e como a pessoa poderá testar cada entrega. Defina agora/depois/não construir. Leia o código de repositórios existentes antes de propor mudanças. Confirme o resumo das decisões.

## Fase 2 — Planejamento das sprints

Leia references/fluxo-v2.md, references/paralelismo-v2.md e references/design-adaptativo.md. Para cada sprint, escreva a entrega demonstrável e o comando de execução, escolha 1–3 prompts-mapa e decomponha em tasks pequenas. Declare as dependências de tasks, contratos canônicos, comandos de teste, contexto mínimo e arquivos de leitura/escrita. Feche contratos compartilhados antes de paralelizar backend e UI.

Para tarefas de interface, inventarie skills efetivamente instaladas no ambiente, selecione as úteis por UX, acessibilidade e compatibilidade e registre a justificativa e fallback. Não invente skills.

## Fase 3 — Criar a especificação 2.0

Leia references/contexto-v2.md e references/testes-progressivos.md; copie e preencha os modelos de assets/v2/. Dentro do repositório do aplicativo, gere:

- docs/especificacao/README.md e 00_visao_geral_e_decisoes.md
- docs/especificacao/plano.json, com schema_version 2.0, human_gate true, coverage_min 80 e full_suite_every 3
- docs/especificacao/sprints/S01/P01.md (mapa humano) e sprints/S01/tasks/T01.json etc.
- docs/especificacao/memoria/global.md e memórias por domínio, contratos canônicos quando aplicáveis
- ESTADO.json na raiz (fonte de verdade do protocolo 2.0) e docs/decisoes/ para ADRs

Em plano.json os caminhos dos mapas e tasks são relativos a docs/especificacao; em cada task, context, reads e writes são relativos à raiz do projeto. Nunca exigir o repositório inteiro como contexto por padrão. A memória global é pequena; arquivos específicos de UI não entram em task de backend.

## Fase 4 — Validar, executar, revisar

Ferramenta sem dependências externas: scripts/fluxo.py, Python 3.10+.
Ao executá-la a partir do repositório desta skill, seu caminho é skills/planejamento-de-sistemas/scripts/fluxo.py.

Exemplos:

    python3 scripts/fluxo.py --repo CAMINHO_DO_APLICATIVO validar
    python3 scripts/fluxo.py --repo CAMINHO_DO_APLICATIVO prontas
    python3 scripts/fluxo.py --repo CAMINHO_DO_APLICATIVO contexto S01-P01-T01
    python3 scripts/fluxo.py --repo CAMINHO_DO_APLICATIVO concluir S01-P01-T01 --commit HASH --evidencia "testes realmente executados"

A CLI monta contexto a partir de manifestos e SHA-256 das fontes, e estima tokens como caracteres / 4 (não é medição real). Se extrapolar orçamento, replaneje a task em vez de truncar regras essenciais.

O executor faz TDD local quando há comportamento. O integrador inspeciona commits e logs, testa os fluxos afetados e mede cobertura do código novo/modificado >=80%, iniciando o sistema e preparando o roteiro de demo. Pausar **sempre** para avaliação humana; o agente não pode se autoaprovar. Registrar ajuste ou aceite via CLI apenas com decisão explícita do humano, reconhecendo que evidências são declaradas e exigem verificação externa.

A cada terceira sprint, antes da entrega final e antes quando o risco for alto, executar suíte completa e medir cobertura global >=80%. Não afirmar resultados que não foram realmente medidos.

A execução paralela é opcional. A CLI lista um lote sem colisão direta de caminhos, mas não lança agentes nem isola filesystem. Use worktrees/branches por agente e um integrador para merge serial e atualização de ESTADO.json. Registrar feedback que afete contratos, atualizar tasks futuras e invalidar contextos dependentes antes de prosseguir.

## Regras inegociáveis

- Não revelar segredos, modificar outros projetos fora do escopo nem fazer deploy sem permissão.
- Não inventar testes, cobertura, commits, skills instaladas, ganhos de produtividade ou economia de tokens.
- Não criar tarefas gigantes nem exagerar camadas para um MVP.
- Não sacrificar segurança ou contratos para caber em orçamento de tokens.
- Não presumir que o registro da CLI constitui prova de execução: logs, Git, CI e demo são evidências externas.
- Usar uma única fonte canônica para cada contrato ou decisão.
- O formato legado continua suportado; referências de 1.x não se aplicam automaticamente aos checkpoints de 2.0.

## Arquivos principais

| Caminho | Leitura |
|---|---|
| references/fluxo-v2.md | Sprints, mapas, tasks e avaliação |
| references/contexto-v2.md | Pacotes seletivos, orçamento e invalidação |
| references/testes-progressivos.md | Testes por task/sprint e cobertura de 80% |
| references/paralelismo-v2.md | Dependências e agentes isolados |
| references/design-adaptativo.md | Seleção e revisão de skills de design |
| references/planejamento-mvp.md | Viabilidade e recorte |
| assets/v2/ | Modelos de manifestos e memórias |
| scripts/fluxo.py | Validação, elegibilidade, contexto e evidências |
| references/fluxo-v1.md | Continuação dos planejamentos legados |
