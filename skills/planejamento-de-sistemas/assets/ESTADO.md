# Estado da construção do <Sistema>

Memória entre sessões. Toda sessão **abre** e **fecha** neste arquivo.

## Ao abrir a sessão

1. Leia a tabela abaixo e confira `git status` — alteração não commitada é sinal de sessão
   interrompida; descreva o que há e pergunte, não descarte nada.
2. Se todos os prompts anteriores ao seu estão **concluídos**: confirme que o commit de cada um
   existe (`git log --grep "<mensagem de commit>"`) e que `<comando de verificação>` está verde.
   Estando, siga para o seu prompt.
3. Se algum anterior está **pendente** ou **em andamento**, reconcilie com o histórico antes de
   começar:

   | O que você encontra | O que fazer |
   |---|---|
   | Commit existe, entregas presentes, suíte verde | Marque **concluído** aqui (anotando "reconciliado em AAAA-MM-DD" e o hash), e siga |
   | Entregas parciais, ou suíte vermelha | **Não comece o prompt novo.** Termine o anterior pelos critérios de aceite dele |
   | Nada encontrado, ou evidências que se contradizem | **Pare e avise**: diga o que procurou, o que achou e o que falta |

   Vale o inverso: se diz "concluído" mas a entrega não está lá ou a suíte está vermelha, volte a
   linha para **em andamento** com o que falta e termine aquele prompt primeiro.

**Nunca marque como concluído o que você não verificou nesta sessão.** Um estado que mente é pior
que um estado vazio: a sessão seguinte confia nele e constrói sobre o vazio.

## Ao fechar a sessão

Confira todos os critérios de aceite, rode a suíte completa e a cobertura, atualize a sua linha
(situação, commit, números, observações) e inclua este arquivo **no mesmo commit** do trabalho —
assim "o commit existe" e "o estado está atualizado" são o mesmo fato.

Se precisar parar no meio: situação **em andamento**, com o que está feito, o que falta e onde
parou, commitado antes de encerrar.

---

| Prompt | Situação | Commit | Hash | Suíte / cobertura | Observações |
|---|---|---|---|---|---|
| 01 — <nome> | pendente | `<mensagem canônica>` | — | — | |
| 02 — <nome> | pendente | `<mensagem canônica>` | — | — | |

Situações: **pendente** · **em andamento** · **concluído**.
Hash: preenchido pela sessão seguinte, na conferência de abertura.
Observações: o que ficou de fora, o que divergiu e qual ADR de `docs/decisoes/` registra a divergência.
