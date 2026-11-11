# Dependências e agentes paralelos

A CLI lista tasks prontas somente quando as dependências foram concluídas e as sprints anteriores receberam aceite humano.

A seleção parallel_batch evita colisões diretas nos caminhos declarados em writes. Tasks declaradas no mesmo parallel_group com conflito de escrita causam erro de validação. O detector não substitui análise de dependências semânticas.

Execução recomendada: agente integrador escolhe tasks, cria worktrees ou branches isoladas e fornece a cada executor somente seu pacote. Cada executor roda testes locais, registra commit e entrega relatório. O integrador revisa os diffs, faz merge serial, resolve conflitos e é o único responsável por atualizar ESTADO.json.

Contrato precisa estar estabilizado antes de backend e UI trabalharem em paralelo. Se surgirem arquivos compartilhados não previstos, suspenda paralelismo, corrija manifestos e regenere contexto.

A CLI **não lança agentes, não faz merge e não impede um agente de editar arquivos fora de writes**. Para isso são necessárias permissões e isolamento externos. Paralelismo pode reduzir tempo de calendário e aumentar custo de tokens; medir quando for relevante.
