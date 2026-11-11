# Planejar uma alteração num sistema existente

Antes da entrevista, leia o código real. Documentos desatualizados e convenções inventadas produzem tasks que quebram o sistema.

## Reconhecimento seletivo

Inspecione README, configurações, scripts de execução e CI, um módulo recente completo, tipos/contratos, modelo de dados, autenticação e testes da área afetada. Verifique alterações recentes. Não mande todo o código aos executores: produza um mapa curto com **arquivos afetados, dependentes e contratos canônicos**.

## Decisões

- O que já existe e será preservado?
- O que muda e como afeta usuários/consumidores?
- É necessária migração ou reversão?
- Que fluxos anteriormente aprovados podem sofrer regressão?
- Que parte do trabalho pode ser paralela após estabilizar os contratos?
- Quem integra e aprova o incremento?

## Transformar em tasks

Cada task de alteração deve declarar arquivos de leitura e escrita, decisão que a autoriza, comportamento preservado, novos casos de teste e critérios de aceite. Exija teste de regressão reproduzindo comportamentos existentes antes de fazer alterações arriscadas. Se a suíte inteira for muito lenta, identifique subconjunto local seguro; no fechamento da sprint rode a regressão afetada e antecipe suíte completa quando o risco for transversal ou incerto.

A demonstração de cada sprint deve iniciar o sistema existente e exercitar o fluxo novo sem romper o anterior. Mantenha histórico de alterações de contratos e regenere pacotes de contexto das tasks dependentes.
