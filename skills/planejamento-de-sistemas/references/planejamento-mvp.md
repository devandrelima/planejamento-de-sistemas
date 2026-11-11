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
