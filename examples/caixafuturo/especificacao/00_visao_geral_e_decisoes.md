# 00 — Visão geral e decisões do CaixaFuturo

> **Tipo:** referência; não executar como prompt.

## 1. Objetivo e escopo MVP

Ferramenta local de linha de comando para um pequeno negócio importar CSV de movimentações, apurar saldo mensal e visualizar risco estimado de insuficiência de caixa. Não é software de aconselhamento financeiro.

| Restrição | Decisão |
|---|---|
| Modo e prazo | MVP em 3 dias, um desenvolvedor |
| Recursos | Python 3.11+, biblioteca padrão, sem APIs externas pagas |
| Experiência | Usuário técnico capaz de executar CLI local |
| Critério de entrega | CSV válido importado; totalização; projeção auditável; testes verdes |
| Dependências externas | Nenhuma API ou chave de IA |
| Riscos | Dados faltantes, ambiguidade de valores, estimativas enganosas |

| Agora (indispensável) | Depois (desejável) | Não construir |
|---|---|---|
| Importação e validação CSV | Interface gráfica | Login e autenticação remota |
| Saldos mensais | Sazonalidade | Open banking |
| Média móvel e alerta | Modelos estatísticos avançados | API de LLM |
| Testes de fronteira | Gráficos e dashboards | Deploy e multiempresa |

## 2. Formato e comportamentos

CSV UTF-8 com cabeçalho data,tipo,valor. Data YYYY-MM-DD, tipo entrada ou saida, valor decimal positivo com duas casas. CSV inválido falha com número da linha e sem resultado parcial. Saldo inicial é informado em CLI; diferença mensal = entradas − saídas. Projeção do próximo mês = média dos resultados líquidos dos até três meses disponíveis. Sem meses válidos, indicar dados insuficientes. Saldo futuro = saldo inicial + todos os resultados mensais + projeção. Alertar quando menor que zero.

## 3. Decisões

| # | Decisão | Motivo |
|---|---|---|
| D1 | Entrada é CSV UTF-8 com data,tipo,valor. | Escopo mínimo sem integração |
| D2 | Entradas e saídas têm valor positivo e tipo explícito. | Sinal sem ambiguidade |
| D3 | Valores monetários usam Decimal, não float. | Precisão financeira |
| D4 | Usar média dos até três meses anteriores disponíveis. | Modelo auditável e barato |
| D5 | Aplicativo local com unittest e sem API de IA. | Respeitar prazo e recursos |

## 4. Invariantes

1. Não usar float para valores financeiros.
2. Erro de entrada nunca produz previsão parcial.
3. A projeção sempre é rotulada como estimativa.
4. Nenhuma credencial externa é necessária.

## 5. Testes e limites

Aplicar TDD por bloco. Após construir a primeira suíte, rodar python3 -m unittest discover -s tests -v na abertura e no fechamento das sessões. Validar casos normais, negativos, zero meses e repetição determinística. Não declarar piso percentual de cobertura até instalar medição real. A precisão da previsão não está comprovada. Decisões de implantação e segurança remota pertencem a uma evolução futura.
