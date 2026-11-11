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
