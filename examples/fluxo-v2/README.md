# Demonstração da metodologia 2.0 — login incremental

Este exemplo entrega **somente o plano de execução**, não um aplicativo de login. Não há backend, tela ou testes do produto implementados neste repositório.

## Cenário fixo

Uma pessoa deseja uma aplicação local com tela de login, backend e persistência, integrada desde a primeira sprint. O sistema precisa ser executável para revisão humana. O trabalho é organizado em dois prompts-mapa e quatro tasks. A interface e o backend podem evoluir em paralelo **depois da definição do contrato**.

## Experimentar a ferramenta

Na raiz do repositório Planejamento de Sistemas:

    python3 skills/planejamento-de-sistemas/scripts/fluxo.py --repo examples/fluxo-v2 validar
    python3 skills/planejamento-de-sistemas/scripts/fluxo.py --repo examples/fluxo-v2 prontas
    python3 skills/planejamento-de-sistemas/scripts/fluxo.py --repo examples/fluxo-v2 contexto S01-P01-T01

A task inicial carrega memória global + domínio autenticação + contrato de login. A memória visual não é carregada.

Para executar a task no projeto real, copie a pasta de especificação e o ESTADO.json para um **repositório de aplicativo separado**, complete as decisões concretas da stack e implemente os arquivos indicados. Não marque tasks como concluídas com commits inventados. O comando de demonstração será aplicável somente depois que a aplicação existir.

## Evidência e limites

A CLI valida estrutura, monta contexto e controla bloqueios de dependência e aceite **com base em evidências declaradas**. Ela não executa testes do aplicativo, não autentica quem usou a opção de aprovação e não faz merge ou orquestração automática de agentes. Em ambiente de produção, confirme commits, logs, cobertura e ações humanas externamente.

A medição de tokens é aproximada (caracteres / 4) e serve como orçamento preventivo, não como custo faturado por um modelo.
