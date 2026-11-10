# Avaliação reproduzível da qualidade dos planejamentos

Este documento define **método**, não resultados. Não confunda quantidade de Markdown produzido com qualidade ou ganho de produtividade.

## Casos fixos

1. CaixaFuturo MVP: três dias, uma pessoa, CSV e projeção offline; sem APIs pagas.
2. API pequena: CRUD de três entidades, autenticação e testes.
3. Evolução de sistema existente: adicionar relatório sem alterar contrato público.

Para comparar versões A e B, use **mesmo pedido inicial**, mesmos esclarecimentos já respondidos, mesmo modelo de IA, mesma versão do modelo, mesmas permissões, mesmo repositório de referência, mesma capacidade de contexto e mesmo avaliador. Execute 3 repetições independentes por caso quando possível, com os artefatos arquivados. Registre o tempo real e esforço humano; não invente números.

## Avaliação por caso

| Dimensão | Evidência | Escala 0–2 |
|---|---|---|
| Requisitos | Fluxos, exceções, dados e entradas definidos | 0 ausente; 1 parcial; 2 verificável |
| Consistência | Não há conflito entre escopo, decisões e prompts | 0 contraditório; 1 ambíguo; 2 consistente |
| Aceite | Cada prompt possui condição observável | 0 ausente; 1 genérica; 2 testável |
| Dependências | Ordem executável sem ciclos ou faltas | 0 inválida; 1 ambígua; 2 demonstrável |
| Viabilidade MVP | Prazo, orçamento e recursos respeitados | 0 inviável; 1 incerto; 2 plausível |
| Continuidade | Pode retomar com evidências de Git e estado | 0 ausente; 1 parcial; 2 verificável |
| Testes | Cenários de erro e regressão reproduzíveis | 0 ausentes; 1 superficiais; 2 específicos |

Total possível: 14 por caso; resultado exige revisão humana e justificativa por item. Em paralelo, rode o validador e registre contagem de erros e avisos, comando, versão e exit code. Reporte separadamente quaisquer falsos positivos do validador.

## Critérios de decisão

Uma nova versão só deve ser considerada melhor quando reduz falhas relevantes ou aumenta critérios verificáveis **sem ultrapassar o prazo do cenário**. Pontuação maior isoladamente não prova melhor código, menor custo, nem aumento de produtividade. Para medir isso, execute os planos por agentes independentes e compare testes de aceitação, retrabalho, custo e tempo — estudos futuros, ainda não realizados.
