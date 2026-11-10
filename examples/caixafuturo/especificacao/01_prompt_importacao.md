# 01 — Prompt: importação e consolidação

> **Tipo:** prompt executável. Ler 00_visao_geral_e_decisoes.md. Pré-requisito: nenhum prompt anterior.

## Objetivo

Criar parser de CSV e resumo mensal offline conforme D1, D2 e D3. Não construir previsão.

## Ordem de trabalho

**Abrir:** ler ESTADO.md, conferir git status e histórico. Rodar suíte se existir. Para cada bloco, escrever os testes primeiro e vê-los falhar pelo motivo certo, implementar o mínimo e rodar toda a suíte novamente.

**Fechar:** conferir critérios, rodar suíte completa e registrar situação e resultado em ESTADO.md no mesmo commit. Não marcar como concluído sem evidência.

## 1. Estrutura e entregas

| Arquivo | Resultado |
|---|---|
| src/importacao.py | CSV UTF-8 e erros por linha |
| src/consolidacao.py | Totais de entrada, saída e saldo por mês |
| tests/test_importacao.py | Parser e limites |
| tests/test_consolidacao.py | Totais determinísticos |

## 2. Testes

- [ ] CSV com 2 entradas e 1 saída produz saldo correto.
- [ ] Cabeçalho faltando causa erro claro.
- [ ] Data inválida informa a linha.
- [ ] Valor zero, negativo e três casas decimais são recusados.
- [ ] CSV vazio retorna série vazia, não exceção de divisão por zero.
- [ ] Reprocessar o mesmo arquivo produz o mesmo resultado.

## Critérios de aceite

- [ ] Arquivos citados criados e os seis cenários verdes.
- [ ] python3 -m unittest discover -s tests -v executa a suíte completa sem falhas.
- [ ] Nenhum valor monetário usa float.
- [ ] ESTADO.md incluído no mesmo commit.
- [ ] Commit: feat(caixafuturo): importar e consolidar csv.
