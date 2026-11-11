# Índice de especificação executável

Este projeto usa exclusivamente a metodologia 2.0: sprint como entrega funcional, prompt como mapa humano, task como unidade real de execução.

| Item | Tipo | Dependências | Entrega |
|---|---|---|---|
| 00_visao_geral_e_decisoes.md | Referência | — | Contrato de produto e arquitetura |
| plano.json | Manifesto | Documento 00 | Sprints, mapas e tasks |
| sprints/S01/P01.md | Mapa humano | Plano | Sequência de tarefas para o agente |
| sprints/S01/tasks/T01.json | Task | Contratos citados no manifesto | Alteração e teste verificáveis |
| memoria/global.md | Contexto global | Documento 00 | Invariantes de todas as tasks |
| memoria/dominio.md | Contexto do domínio | Contratos | Decisões locais e arquivos relevantes |
| ESTADO.json (na raiz) | Estado | Plano | Progressão, commits e aceite humano |

O executor deve obter o contexto da task com scripts/fluxo.py contexto, e não ler todos os documentos antecipadamente.
