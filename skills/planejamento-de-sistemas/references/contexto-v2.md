# Memória seletiva por task

## Regras

A task declara context, reads e writes com caminhos relativos à raiz do projeto. O plano declara global_context. O executor recebe apenas memória global pequena, contexto do domínio, arquivos explicitamente autorizados e descrição da task.

A ferramenta fluxo.py contexto monta o pacote em ordem estável, registra SHA-256 de cada arquivo de origem e estima tokens como caracteres/4. Se ultrapassar context_budget_tokens, recusa sem truncar material importante. Esta estimativa não representa tokens faturáveis de modelos comerciais.

O pacote não deve repetir o repositório inteiro, documentação de domínios estranhos ou logs antigos. Contratos permanecem como fonte canônica; memórias apontam para eles, não criam cópias inconsistentes. Estado de execução fica em ESTADO.json e a prova real é Git + logs.

Mudança em contrato, API, schema ou decisão compartilhada invalida contextos dependentes, que precisam ser refeitos. Quando uma task descobrir dependência inesperada, registre o motivo e atualize seu manifesto antes de prosseguir. Não omita arquivo essencial só para baixar tokens.

Use modelos menores em tarefas fechadas e reserve revisão especializada para decisões complexas. Medir custo total de tokens exige contabilizar tentativas e retrabalho, não apenas tamanho do contexto inicial.
