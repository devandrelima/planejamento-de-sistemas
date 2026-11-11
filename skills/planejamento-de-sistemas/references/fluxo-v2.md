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
