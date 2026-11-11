# Testes progressivos e checkpoints

O ciclo divide verificações de acordo com a unidade de execução e o risco.

**Task:** antes de implementar comportamento, escreva teste local e observe a falha correta. Implemente, rode testes locais, lint, tipagem e build rápidos quando aplicáveis; registre comandos, resultados e arquivos alterados.

**Sprint:** após integrar as tasks, rode a regressão de todos os fluxos afetados, inclusive fluxos aprovados que dependem das alterações. Inicie o sistema e demonstre a entrega. Meça cobertura >=80% do código novo ou alterado com ferramenta compatível e registre escopo e comando.

**Checkpoint global:** a cada 3 sprints por padrão, na última sprint e antecipadamente por risco alto/crítico, mudança transversal, autenticação, autorização, banco compartilhado ou impacto desconhecido, execute a suíte completa e meça cobertura global >=80%.

Testes de precisão financeira, segurança, isolamento e concorrência não desaparecem quando o percentual atinge 80%. Cobertura não prova correção. Se não há medição confiável, registre pendência em vez de inventar percentual ou aprovar.

A CLI exige evidências declaradas de regressão, demo e cobertura alterada para aprovação; nos checkpoints, exige suíte completa e cobertura global. Ela não executa testes do aplicativo; integrador e CI devem verificar comandos e logs.

Não baixar limites para passar, não pular testes ou mascarar falhas. Sistemas existentes abaixo de 80% devem possuir um plano de recuperação documentado antes de prometer conformidade.
