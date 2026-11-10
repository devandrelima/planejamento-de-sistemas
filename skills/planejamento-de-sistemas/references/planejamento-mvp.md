# Planejamento orientado a MVP

Use esta referência antes de fatiar a implementação quando houver prazo, equipe ou orçamento limitados.

## Contrato de viabilidade

Registre no documento 00, de forma explícita:

| Campo | Pergunta a responder |
|---|---|
| Modo | MVP com entrega verificável ou projeto completo? |
| Prazo | Data de entrega, capacidade em horas e margem de segurança |
| Pessoas | Quantidade, experiência com stack e disponibilidade |
| Recursos | Orçamento, infraestrutura, ferramentas e limites de APIs |
| Essenciais | Fluxos sem os quais não existe entrega utilizável |
| Desejáveis | Melhorias adiáveis, com prioridade |
| Excluídos | Não construir agora, mesmo que pareçam úteis |
| Dependências | Credenciais, aprovações, fontes de dados e terceiros |
| Riscos | Incerteza, gargalo, integração e mitigação |
| Critério de entrega | Testes, demonstração e resultado observável mínimos |

Não confundir MVP com protótipo inseguro: integridade dos dados, isolamento, privacidade e testes de fluxos críticos continuam obrigatórios quando aplicáveis.

## Algoritmo de recorte

1. Escreva o fluxo de valor ponta a ponta em uma frase que possa ser demonstrada.
2. Separe cada capacidade em **indispensável**, **desejável** ou **posterior**. Só a primeira entra no MVP.
3. Identifique dependências e riscos de cada indispensável; se uma dependência não couber no prazo, substitua o fluxo por alternativa segura, ou declare a entrega inviável.
4. Estime por faixa, não por falsa precisão: pequeno, médio, grande. Reserve tempo para testes e integração.
5. Prefira o menor número de prompts que termine com entrega verificável. Não crie automaticamente as camadas da "sequência típica".
6. Pare de acrescentar prompts quando o critério mínimo de entrega já estiver coberto. Registre o restante como evolução, não como tarefa parcialmente executada.
7. Se a previsão ultrapassar prazo/capacidade, renegocie escopo ou prazo com o usuário antes de declarar plano viável.

## Casos particulares

- Projeto offline sem usuários remotos: não invente login, OAuth, filas, nuvem ou deploy.
- Projeto local sem banco: não imponha containers, migrations ou testes de banco inexistente.
- Números financeiros: testes de precisão, entradas inválidas e fronteiras não são opcionais.
- Testes: defina comandos reais e piso mensurável quando houver ferramenta configurada. Não afirme medição de cobertura sem executá-la.
- Segurança: analise superfícies existentes; ausência de requisito não significa licença para vazar dados.

## Saída obrigatória

No documento 00, inclua tabela **Agora / Depois / Não construir**, restrições de entrega, riscos e uma demonstração mínima com critérios verificáveis. No índice, cada prompt deve acrescentar valor observável ao MVP. A revisão final deve rejeitar ambição que não cabe no prazo, mesmo com todos os documentos formalmente corretos.
