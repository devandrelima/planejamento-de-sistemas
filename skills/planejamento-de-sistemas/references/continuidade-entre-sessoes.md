# Continuidade entre sessões: o protocolo do `ESTADO.md`

Cada prompt roda numa sessão que não viu nenhuma das anteriores. O `ESTADO.md` é a única memória
que atravessa essa fronteira, e por isso toda sessão **abre** e **fecha** nele. Sem abertura, a
sessão constrói sobre uma base que talvez não exista; sem fechamento, a próxima não sabe onde
parou — e o trabalho é refeito ou pulado.

O ponto delicado: `ESTADO.md` é uma **afirmação**, e o git é a **evidência**. Uma sessão que ficou
sem contexto, travou ou foi interrompida deixa a afirmação desatualizada, dizendo "pendente" sobre
algo que já está pronto, ou "concluído" sobre algo que ficou pela metade. O protocolo existe para
resolver essa divergência com o histórico, não com o otimismo.

## A regra que quase elimina a divergência

**A atualização do `ESTADO.md` entra no mesmo commit do trabalho do prompt.** Assim "o commit
existe" e "o estado está atualizado" passam a ser o mesmo fato, e a reconciliação vira exceção em
vez de rotina.

Por isso a linha do `ESTADO.md` é identificada pela **mensagem de commit canônica** — aquela que o
próprio prompt fixa nos critérios de aceite —, e não pelo hash: o hash não existe antes do commit,
então usá-lo como identificador obrigaria a um segundo commit, abrindo de novo a janela em que o
estado e o código divergem. A coluna de hash é preenchida por quem passar depois, na conferência de
abertura; é informação útil, nunca a fonte de verdade.

## Abertura da sessão (antes de qualquer outra coisa)

1. **Ler o `ESTADO.md`** e localizar o prompt desta sessão e todos os anteriores.
2. **Conferir a árvore de trabalho** (`git status`): alteração não commitada é sinal de sessão
   interrompida. Nunca descartar nada por conta própria — descrever o que há e perguntar.
3. Se todos os anteriores estão **concluídos**: conferência rápida — o commit de cada um existe no
   histórico (`git log --grep "<mensagem canônica>"`) e a suíte completa está verde. Verde e
   commits no lugar → seguir para o prompt da vez.
4. Se algum anterior está **pendente** ou **em andamento**, reconciliar com o histórico antes de
   qualquer coisa (abaixo).

## Reconciliação: o que o histórico diz

Para o prompt em dúvida, reúna três evidências — nesta ordem, porque cada uma é mais barata que a
seguinte:

- **Commit:** `git log --grep "<mensagem canônica do prompt>"` encontra o commit dele?
- **Entrega:** os arquivos e comportamentos que os critérios de aceite exigem existem de fato?
- **Verificação:** a suíte completa passa, com a cobertura no piso?

Três desfechos, e só três:

| Evidência | Desfecho |
|---|---|
| Commit existe, entregas presentes, suíte verde | **Marcar como concluído** no `ESTADO.md`, anotando "reconciliado a partir do histórico em AAAA-MM-DD" e o hash encontrado, e seguir para o prompt da vez |
| Parte das entregas presente, ou suíte vermelha | **Não começar o prompt novo.** Terminar o anterior primeiro, pelos critérios de aceite dele, e só então prosseguir |
| Nada encontrado, ou evidências que se contradizem | **Parar e avisar**, dizendo o que procurou, o que achou e o que falta. Não adivinhar |

A regra que sustenta as três: **nunca marcar como concluído o que não foi verificado nesta sessão.**
Um `ESTADO.md` que mente é pior que um `ESTADO.md` vazio, porque a sessão seguinte confia nele e
constrói sobre o vazio — e o erro só aparece duas camadas adiante, longe da causa.

A situação inversa também é reconciliação: o `ESTADO.md` diz "concluído", mas a entrega não está lá
ou a suíte está vermelha. Aí a linha volta para "em andamento", com o que falta anotado, e o prompt
anterior é terminado antes do novo.

## Fechamento da sessão

Antes do commit final, e como parte dele:

1. Conferir **todos** os critérios de aceite do prompt, um a um.
2. Rodar a suíte completa e a cobertura; anotar os números.
3. Atualizar a linha do prompt no `ESTADO.md`: situação **concluído**, mensagem de commit, resultado
   da suíte e da cobertura, e observações — o que ficou de fora, o que divergiu e qual ADR registra
   a divergência.
4. Incluir o `ESTADO.md` **no mesmo commit** do trabalho.
5. Responder ao usuário dizendo o que entregou, o resultado da verificação e qual é o próximo prompt.

Se a sessão precisar parar antes de terminar o prompt — contexto acabando, problema que não cede —,
o fechamento muda mas não desaparece: situação **em andamento**, com o que já está feito, o que
falta e onde parou, commitado antes de encerrar. Uma sessão que morre sem deixar rastro é a única
falha que este protocolo não consegue consertar sozinho.

## O que o `ESTADO.md` precisa ter

Uma linha por prompt, com: prompt, situação (pendente · em andamento · concluído), mensagem de
commit, hash (preenchido na conferência seguinte), resultado da suíte e da cobertura, e observações.

O arquivo carrega, no próprio corpo, as regras de abertura e fechamento — ele é lido por toda sessão
e é o lugar mais confiável para essa instrução viver. Modelo em `assets/ESTADO.md`.
