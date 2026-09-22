# NN — Prompt: <entrega em três palavras>

> **Como usar:** sessão nova na raiz do `<repositório>`. Pré-requisito: prompt <NN-1> concluído.
> Leia `docs/especificacao/00_visao_geral_e_decisoes.md` e este arquivo.
>
> **Revisões:** `/code-review` ao final. <`/security-review` também, quando houver segredo,
> autenticação, pagamento ou dado pessoal.>

---

## Objetivo

<O que esta sessão entrega.> **Nesta sessão não se faz <o que fica para o próximo prompt>.**

---

## Ordem de trabalho

**Passo 0 — abrir a sessão.** Leia `ESTADO.md` e confira `git status`. Os prompts anteriores
precisam estar concluídos; se algum estiver pendente ou em andamento, reconcilie pelo histórico
(`git log --grep "<mensagem canônica do prompt anterior>"` + entregas presentes + suíte verde):
tudo no lugar → marque concluído e siga; entrega parcial ou suíte vermelha → **termine o anterior
antes**; nada encontrado ou evidências contraditórias → **pare e avise**. Nunca marque como
concluído o que não verificou nesta sessão.

Depois, bloco a bloco, na ordem das seções abaixo. Para cada bloco:

1. Rode `<comando da suíte completa>` e anote o resultado. **Se já estiver vermelho, pare e avise** —
   não se constrói sobre suíte vermelha.
2. Escreva os testes do bloco (§N, grupo correspondente) e veja-os falhar **pelo motivo certo**.
   Teste que passa antes da implementação não testa nada: reescreva.
3. Implemente o mínimo que faz esses testes passarem, sem adiantar o bloco seguinte.
4. Rode os testes do bloco → verdes.
5. Rode `<comando da suíte completa>` → verde. Quebrou algo que já existia? Conserte o **código**,
   não o teste — salvo quando esta especificação previr a mudança, e aí diga no commit qual decisão
   a autoriza.
6. Refatore com a suíte verde e rode de novo.

**Passo final — fechar a sessão.** Confira todos os critérios de aceite, rode a suíte completa e a
cobertura, atualize a sua linha no `ESTADO.md` (situação concluído, mensagem de commit, números da
suíte e da cobertura, observações) e inclua o `ESTADO.md` **no mesmo commit** do trabalho. Se
precisar parar no meio do prompt, deixe a linha em "em andamento" dizendo o que falta e onde parou,
e commite isso antes de encerrar.

Não feche a sessão no vermelho. Não faça commit com teste pulado (`skip`/`only`), asserção afrouxada
ou cobertura abaixo do piso. Bug encontrado no caminho entra com o teste que o reproduz antes da
correção.

---

## 1. Estrutura de arquivos

```
<árvore com comentário curto no que não é autoexplicativo>
```

<Em repositório existente, acrescente a tabela de arquivos alterados:>

| Arquivo existente | O que muda |
|---|---|
| `<caminho>` | <mudança> |

---

## 2. <Bloco: assunto>

<Tabelas para tudo que é enumerável. Regras em frases curtas. Código literal só quando reconstruí-lo
daria margem a erro.>

| <Campo> | <Tipo> | <Obrigatório> | <Regras> |
|---|---|---|---|
| | | | |

---

## N. Testes

Ficam em `<caminho>`; rodam com `<comando só destes testes>`; a suíte completa é
`<comando da suíte completa>`. O mundo externo é substituído por `<dublê>` — credencial real, nunca.

### Bloco 2 — <assunto>

- [ ] <caminho feliz, com o corpo real> → <resultado esperado>
- [ ] <cada erro previsto> → <código e mensagem exatos>
- [ ] Repetição: <a mesma operação duas vezes> → <mesma resposta, um efeito só>
- [ ] Concorrência: <N simultâneas no mesmo alvo> → <um vencedor, sem duplicata>
- [ ] Fronteira: <vazio, um, máximo, máximo+1> → <resultado>
- [ ] Isolamento: <dado de outro dono> → <não aparece nem pode ser alterado>
- [ ] Falha externa: <fora do ar / tempo esgotado / resposta inesperada / incerteza> → <resultado>
- [ ] Ordem: <evento adiantado ou atrasado> → <não sobrescreve estado mais avançado>
- [ ] Invariante <N> do documento 00: <como se prova que não foi violado>

### Bloco 3 — <assunto>

- [ ] …

---

## Critérios de aceite

- [ ] <verificável sem interpretação>
- [ ] Todos os cenários da §N implementados e verdes.
- [ ] `<comando da suíte completa>` verde — inclusive o que já existia antes deste prompt.
- [ ] Cobertura no piso combinado (<X>% global, <Y>% em `<módulos críticos>`), nenhum teste pulado,
      nenhuma asserção afrouxada.
- [ ] `ESTADO.md` atualizado nesta linha e incluído no commit do trabalho.
- [ ] Commit: `<tipo(escopo): mensagem>`
