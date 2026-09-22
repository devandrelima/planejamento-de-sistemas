# NN — Prompt inicial: colar na primeira sessão da IA construtora

> **Tipo:** prompt de arranque. Não descreve funcionalidade nova: organiza a execução dos prompts
> <primeiro> a <último>.
>
> **Antes de colar:** <o que precisa existir — repositório clonado, especificação dentro dele>.

---

## 1. Prompt de arranque (primeira sessão)

````markdown
Você vai construir o **<Sistema>**, <uma frase>, a partir de uma especificação pronta que está neste
repositório. A especificação é a fonte de verdade; não invente escopo nem mude decisões por conta
própria.

**Leia primeiro, inteiros:** o `README.md` e o `00_visao_geral_e_decisoes.md` da pasta da
especificação.

## Passo 0 — preparar o repositório (só nesta primeira sessão)

1. Confirme que está na raiz de um repositório git. Se não houver, **pare e me avise**.
2. Mova a especificação para `docs/especificacao/`, que é o caminho pelo qual os arquivos se citam.
3. Crie `ESTADO.md` na raiz a partir do modelo da especificação: as regras de abertura e fechamento
   de sessão no topo, e a tabela com uma linha por prompt (prompt, situação, mensagem de commit
   canônica, hash, suíte/cobertura, observações). Todos começam em **pendente**. Este arquivo é a
   memória entre sessões — toda sessão abre e fecha nele.
4. Commit: `chore: especificação do <Sistema>`.

## Como trabalhar

- **Ordem:** <lista dos prompts executáveis>. Os arquivos <lista> são **referência** (leia, não
  execute) e <lista> são **manuais para pessoas** — não execute e me avise quando chegar a hora.
- **Abra toda sessão pelo `ESTADO.md`.** Confira que os prompts anteriores estão concluídos e que
  `git status` está limpo. Se algum anterior estiver pendente ou em andamento, reconcilie pelo
  histórico antes de começar: commit encontrado por `git log --grep` + entregas presentes + suíte
  verde → marque concluído (anotando que foi reconciliado, com a data) e siga; entrega parcial ou
  suíte vermelha → termine o prompt anterior primeiro; nada encontrado ou evidências que se
  contradizem → **pare e me avise**, dizendo o que procurou, o que achou e o que falta. Nunca marque
  como concluído o que você não verificou na própria sessão.
- **Feche toda sessão pelo `ESTADO.md`.** Situação, mensagem de commit, resultado da suíte e da
  cobertura e observações, **no mesmo commit** do trabalho. Parou no meio? Deixe "em andamento" com
  o que falta e onde parou, commitado antes de encerrar.
- **Um prompt por vez.** Para cada um: leia o arquivo inteiro → siga a "Ordem de trabalho" dele,
  bloco a bloco → confira **todos** os critérios de aceite → rode `<comando de verificação>` → rode
  `/code-review` (e `/security-review` quando o arquivo pedir) → corrija → faça o commit indicado no
  próprio arquivo → atualize o `ESTADO.md`.
- **Testes primeiro, sempre.** Em cada bloco: rode a suíte completa e anote a linha de base; escreva
  os testes daquele bloco e veja-os falhar pelo motivo certo; implemente o mínimo para passar; rode
  os testes do bloco; rode a **suíte completa** de novo para provar que nada quebrou. Só então o
  próximo bloco. Teste que passa antes da implementação não testa nada — reescreva.
- **Suíte vermelha é parada obrigatória.** Se a linha de base já estiver vermelha, pare e me avise.
  Não feche sessão nem faça commit no vermelho, com teste pulado (`skip`/`only`), asserção afrouxada
  ou cobertura abaixo do piso — e nunca baixe o piso para o build passar.
- **Teste antigo que falha:** conserte o **código**. Só altere o teste quando a especificação previr
  a mudança, e diga no commit qual decisão a autoriza.
- **Bug encontrado no caminho:** primeiro o teste que o reproduz, falhando; depois a correção.
- **Só avance com o anterior verde.** Se o mesmo problema resistir a três tentativas, pare e me
  explique o que travou, com o erro.
- **Contexto:** quando a sessão ficar longa, pare **no fim de um prompt**, nunca no meio, com o
  `ESTADO.md` atualizado e commitado, e me diga para abrir uma sessão nova. Se for inevitável parar
  no meio, o `ESTADO.md` precisa dizer exatamente onde você parou — é o que a próxima sessão lê.
- **Divergências:** se a especificação conflitar com a documentação oficial de um serviço ou de uma
  biblioteca instalada, a **documentação oficial vence**. Siga-a, registre em `docs/decisoes/` e me
  avise na resposta.
- **Fora de escopo é fora de escopo:** o que a §1.1 do arquivo 00 exclui não se constrói.

## Limites (não faça sem eu autorizar explicitamente)

- Nada de deploy nem comando que mexa em <infraestrutura, containers, banco de produção>.
- Não toque em nenhum arquivo fora deste repositório.
- Nenhum segredo no git; `.env` nunca é commitado.
- Nenhuma credencial real de <serviço externo>: os testes usam <o dublê falso>.
- Não abra pull request nem faça push para `main` sem eu pedir.

## Formato das respostas

Ao terminar cada prompt, responda em até cinco linhas: o que entregou, o que ficou de fora, o
resultado da suíte completa e da cobertura, o hash do commit e o próximo prompt da fila.

**Comece pelo Passo 0 e siga para o prompt <primeiro>.**
````

---

## 2. Prompt das sessões seguintes

````markdown
Continue a construção do <Sistema>.

1. Leia `ESTADO.md` (as regras de abertura estão no topo dele), depois
   `docs/especificacao/README.md` e `docs/especificacao/00_visao_geral_e_decisoes.md`.
2. **Confira o estado antes de começar:** `git status` limpo e prompts anteriores concluídos. Se
   algum estiver pendente ou em andamento, reconcilie pelo histórico (`git log --grep` da mensagem
   de commit, entregas presentes, suíte verde) e siga o desfecho que a tabela do `ESTADO.md` indica
   — marcar concluído, terminar o anterior, ou parar e me avisar.
3. Rode `<comando de verificação>`: essa é a linha de base. Vermelha → pare e me avise.
4. Execute o **próximo prompt pendente**, um só, com as mesmas regras: ciclo vermelho-verde por
   bloco, critérios de aceite conferidos, suíte inteira verde, cobertura no piso, revisões pedidas,
   commit indicado e `ESTADO.md` atualizado **no mesmo commit**.
5. Valem os mesmos limites do prompt de arranque.

Ao terminar, me diga em até cinco linhas o que entregou e qual é o próximo.
````

---

## 3. Antes da primeira sessão (feito por uma pessoa)

1. <o que a pessoa precisa providenciar: repositório, contas, credenciais, ferramentas>

**O que depende de você, e não da IA:** <manuais humanos e decisões pendentes>.
