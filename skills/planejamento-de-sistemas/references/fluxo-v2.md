# Metodologia 2.0 — sprints, prompts-mapa e tasks

Este é o formato padrão dos novos planejamentos. O fluxo 1.x segue disponível em fluxo-v1.md para projetos legados.

## Hierarquia

- **Sprint:** incremento executável e demonstrável com 1 a 3 prompts (padrão recomendado: 2), encerrado somente após avaliação explícita do humano.
- **Prompt-mapa:** documento que a pessoa seleciona e entrega ao agente, descrevendo objetivo, tasks e dependências. Não é o contexto de execução inteiro.
- **Task:** instrução operacional pequena, com contrato, dependências, arquivos de leitura/escrita, critérios verificáveis, testes e orçamento contextual.

O primeiro incremento deve entregar valor real ponta a ponta, não apenas tabelas e arquivos isolados. Login só é a primeira entrega quando o produto realmente precisa disso.

## Sequência

1. Entrevistar e fechar decisões, prazo, recursos, MVP, riscos, contrato e demonstração.
2. Escolher sprints executáveis, até três prompts-mapa por sprint e tasks por prompt.
3. Criar docs/especificacao/plano.json, sprints/S01/P01.md, tasks JSON, memória global e por domínio, contratos, README, documento 00 e ESTADO.json na raiz do projeto.
4. Validar com fluxo.py validar; corrigir erros objetivos e revisar o planejamento semanticamente.
5. O humano seleciona o mapa. O executor carrega fluxo.py contexto ID, sem receber toda a especificação.
6. Em cada task, testes locais; após integrar, regressão dos fluxos afetados, cobertura alterada >=80% e demonstração executável.
7. Parar para avaliação humana; mudanças solicitadas exigem replanejamento dos próximos manifestos e invalidação do contexto afetado.
8. A cada terceira sprint, e antes quando houver risco alto, rodar suíte completa e verificar cobertura global >=80%.

As evidências de testes e commits registradas em ESTADO.json são **declaradas**, não verificadas automaticamente pela CLI. O integrador deve conferir logs e Git. A CLI não autentica a identidade da pessoa que aprova.

## Compatibilidade

Não migrar automaticamente um projeto 1.x em andamento. A versão anterior usa ESTADO.md e prompts executáveis, validáveis por scripts/validar.py. A versão nova usa ESTADO.json e tasks, validáveis por scripts/fluxo.py. O histórico original permanece preservado.
