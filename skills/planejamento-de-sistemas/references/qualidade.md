# Checklist de qualidade do plano

## Planejamento e entregas

- [ ] O MVP tem prazo, recursos, riscos e fluxo utilizável definidos.
- [ ] Cada sprint entrega uma versão que o usuário pode iniciar e experimentar.
- [ ] Existem 1–3 prompts-mapa por sprint; maps relacionam tasks e não repetem toda a memória.
- [ ] Cada task contém objetivo, saída, contexto, leituras/escritas, dependências, testes e aceite observável.
- [ ] Contratos compartilhados estão definidos antes de tarefas paralelas.
- [ ] Execução de agentes independentes não disputa arquivos e usa integração controlada.

## Contexto e decisões

- [ ] A memória global é curta e não inclui segredos.
- [ ] Cada task recebe somente o domínio e arquivos relevantes.
- [ ] Contratos são fonte única de verdade, sem cópias divergentes.
- [ ] Mudanças de contratos invalidam contextos dependentes e atualizam manifestos.
- [ ] Orçamento estimado de tokens não omite condições de segurança.

## Testes, experiência e aceite

- [ ] Testes locais cobrem a task que está sendo escrita.
- [ ] Testes dos fluxos afetados verificam a sprint integrada.
- [ ] Cobertura do código alterado >=80% é medida, não presumida.
- [ ] Suíte completa e cobertura global >=80% ocorrem na terceira sprint, última ou antes por risco.
- [ ] Tasks de UI usam apenas skills realmente disponíveis e revisão visual, acessibilidade e estados de interface.
- [ ] A próxima sprint fica bloqueada até feedback e aceite humano.
- [ ] Plano e estado passam por scripts/fluxo.py validar.
- [ ] Não se afirma execução real, cobertura, economia de tokens ou produtividade sem evidências externas.
