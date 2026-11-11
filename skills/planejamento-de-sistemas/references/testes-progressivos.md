# Testes progressivos e checkpoints

A versão 2.0 substitui a suíte completa a cada bloco do fluxo 1.x por testes proporcionais ao impacto.

**Task:** antes de implementar comportamento, escreva o teste local e observe a falha correta. Implemente, rode testes locais, lint, tipagem e build rápidos quando aplicáveis. Registre comandos, resultados e arquivos alterados.

**Sprint:** após integrar as tasks, rode a regressão de todos os fluxos afetados (inclusive fluxos antigos que dependem das alterações), inicie o sistema e demonstre a entrega. Meça cobertura >=80% do código novo ou modificado e registre a ferramenta real utilizada.

**Checkpoint global:** a cada 3 sprints por padrão, no encerramento do projeto e antecipadamente por risco crítico, mudança transversal, autenticação, permissão, esquema compartilhado ou impacto desconhecido, execute a suíte completa e meça cobertura global >=80%.

Testes de segurança, cálculo monetário, isolamento e concorrência não desaparecem quando a cobertura de linhas atinge 80%. Cobertura não é garantia de correção. Se não há medição confiável, registre como pendência em vez de inventar percentual ou aprovar.

A CLI exige evidências declaradas de regressão, demo e cobertura alterada no aceite; em checkpoint também exige suíte completa e cobertura global. Ela não executa os testes do aplicativo, e o integrador deve verificar logs/CI.

Não diminuir o piso para passar, não pular testes e não mascarar falhas. Projeto legado abaixo de 80% precisa de plano de recuperação antes de prometer conformidade.
