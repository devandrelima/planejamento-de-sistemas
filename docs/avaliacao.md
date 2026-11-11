# Avaliação reproduzível da metodologia

Documento de critérios, não de resultados. Um conjunto de manifestos correto não é evidência de software funcional ou economia real.

## Cenários de avaliação

1. Aplicativo pequeno com CSV, visualização e cálculo offline.
2. Fluxo de autenticação com interface, serviço e persistência.
3. Mudança num módulo existente com consumidores e testes anteriores.

Cada cenário deve utilizar mesmo modelo, mesmo escopo, mesmos dados, mesmas permissões e critérios de aceite para comparação. Ao medir eficiência, registre tempo humano, tokens efetivamente consumidos por modelo, tentativas, replanejamento, retrabalho e erros observados.

## Matriz de revisão

| Dimensão | Evidência |
|---|---|
| MVP e prazo | Escopo cabe nos recursos e gera entrega utilizável |
| Sprint funcional | Demo inicia e executa o fluxo previsto |
| Prompt-mapa | Serve ao humano; referencia as tasks apropriadas |
| Task verificável | Contratos, instruções, dependências e testes específicos |
| Contexto mínimo | Só arquivos autorizados, sem omissão de invariantes |
| Dependências | Ordem possível, sem ciclos e sem colisão de escrita em paralelismo |
| Qualidade | Testes locais, regressão afetada e checkpoints globais |
| Cobertura | Métricas medidas >=80% quando exigidas |
| Design | Acessibilidade, usabilidade e coerência visual avaliadas |
| Aceite | Feedback humano registrado antes da sprint seguinte |
| Auditabilidade | Commits, logs, versões e evidências acessíveis |

Use o validador como checagem estrutural, não como avaliação semântica ou execução. Não divulgar resultados quantitativos até executar experimentos independentes e registrar dados brutos.
