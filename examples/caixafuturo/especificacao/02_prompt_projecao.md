# 02 — Prompt: previsão e riscos

> **Tipo:** prompt executável. Exige conclusão do prompt 01. Ler 00_visao_geral_e_decisoes.md.

## Objetivo

Adicionar projeção offline transparente conforme D3, D4 e D5, sem login ou API externa.

## Ordem de trabalho

**Abrir:** ler ESTADO.md, conferir git status, commit e suíte do prompt 01. Diante de conflito ou alterações não commitadas, reconciliar o trabalho anterior; não descartar arquivos. Para cada bloco, teste vermelho, implementação mínima e suíte completa verde.

**Fechar:** testar a suíte toda; atualizar ESTADO.md no mesmo commit da entrega. Nunca declarar sucesso com testes falhando.

## 1. Estrutura e entregas

| Arquivo | Resultado |
|---|---|
| src/projecao.py | Média de até três resultados líquidos mensais |
| src/cli.py | Argumentos CSV e saldo inicial; relatório explicativo |
| tests/test_projecao.py | Projeções e falhas de dados |

Regras: usar os últimos três meses disponíveis (menos, se houver só um ou dois); sem mês válido retornar dados insuficientes. Saldo previsto = saldo inicial + total histórico + média projetada. Alertar somente quando saldo previsto for negativo. Nomear explicitamente a estimativa e suas limitações.

## 2. Testes

- [ ] Resultados 10, 20, 30 geram média 20.
- [ ] Quatro meses usam apenas os três mais recentes.
- [ ] Um mês usa seu único resultado; zero meses não gera projeção.
- [ ] Saldo final negativo produz alerta de risco.
- [ ] Entradas idênticas produzem saídas idênticas.
- [ ] Arquivo CSV inválido nunca gera previsão parcial.

## Critérios de aceite

- [ ] Cenários acima automatizados e verdes.
- [ ] python3 -m unittest discover -s tests -v executa a suíte inteira sem falhas.
- [ ] Relatório identifica a previsão como estimativa.
- [ ] Sem dependência de APIs pagas.
- [ ] ESTADO.md incluído no commit.
- [ ] Commit: feat(caixafuturo): projetar saldo offline.
