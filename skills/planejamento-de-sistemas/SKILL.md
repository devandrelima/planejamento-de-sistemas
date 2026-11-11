---
name: planejamento-de-sistemas
description: Transforma ideias de sistemas em planos executáveis por agentes de IA, com sprints funcionais, prompts-mapa para o humano, tasks JSON, memória contextual seletiva, testes progressivos, design adaptativo, execução paralela controlada e aprovação humana. Use para mapear MVP, requisitos, arquitetura, documentação, continuidade de agentes e planos de implementação.
---

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
