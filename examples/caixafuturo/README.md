# CaixaFuturo — demonstração reproduzível

**Este é um estudo de planejamento, não o aplicativo financeiro.** Não houve execução dos prompts por uma IA construtora nem medição de economia de tempo.

## Solicitação inicial (cenário fixo)

Quero um MVP local para pequenas empresas que importe CSV de entradas/saídas, resuma saldo mensal e indique risco de saldo negativo por uma projeção simples. Uma pessoa, três dias, custo externo zero; sem APIs de IA, login, integração bancária ou deploy.

## Resultado da skill

- Entrevista curta e restrições transformadas em D1–D5 no documento 00.
- Recorte explícito do MVP contra evolução futura.
- Prompt 01: importação e consolidação, com TDD e critérios verificáveis.
- Prompt 02: projeção simples e riscos, com TDD e critérios verificáveis.
- Prompt de arranque: ordem e continuidade independente de conversa.

## Reproduzir

Na raiz deste repositório, execute:

    python3 skills/planejamento-de-sistemas/scripts/validar.py examples/caixafuturo/especificacao
    python3 skills/planejamento-de-sistemas/scripts/validar.py examples/caixafuturo/especificacao --json
    python3 -m unittest discover -s tests -v

A saída esperada do validador para este exemplo é zero erros e zero avisos. O exit code 0 significa que **as regras estruturais implementadas** passaram, não que o plano é perfeito ou que o produto já existe.

## Limites

O validador não entende semântica de negócio, não avalia acurácia estatística e não substitui revisão humana. A construção real do CaixaFuturo será trabalho posterior. Este material foi escrito como exemplo verificável; não é resultado de um experimento comparando versões da skill.
