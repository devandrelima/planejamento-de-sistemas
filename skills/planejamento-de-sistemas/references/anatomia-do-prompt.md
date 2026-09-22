# Anatomia de um prompt executável

Um prompt é lido por uma sessão que não viu nada do que veio antes, a não ser os arquivos que ele
mandar ler. Ele precisa dizer o que construir, com que forma, **em que ordem de trabalho** e como
saber que terminou. Modelo em `assets/NN_prompt.md`; a doutrina de testes que sustenta a ordem de
trabalho está em `testes.md` e deve ser lida antes.

## Esqueleto

```markdown
# NN — Prompt: <entrega em três palavras>

> **Como usar:** sessão nova na raiz do `<repositório>`. Pré-requisito: prompt <NN-1> concluído.
> Leia `docs/especificacao/00_visao_geral_e_decisoes.md` e este arquivo.
>
> **Revisões:** `/code-review` ao final. <e `/security-review`, quando mexe em segredo, autenticação,
> pagamento ou dado pessoal>

---

## Objetivo

Um parágrafo: o que esta sessão entrega e, em negrito, **o que ela não faz** (o que vem no próximo
prompt). A fronteira importa tanto quanto o conteúdo — sem ela a sessão avança sobre o prompt
seguinte e entrega os dois pela metade.

---

## Ordem de trabalho

O ciclo vermelho-verde, bloco a bloco. Copie do modelo — é idêntico em todo prompt.

## 1. Estrutura de arquivos

Árvore em bloco de código, com um comentário curto no que não é autoexplicativo.

## 2..N. Especificação

Uma seção por assunto — cada uma é um **bloco** do ciclo —, na ordem em que se constrói. Tabelas
para tudo que é enumerável.

## N+1. Testes

Cenários concretos com resultado esperado, **agrupados pelo bloco a que pertencem**, porque é essa
a ordem em que serão escritos.

---

## Critérios de aceite

- [ ] …
- [ ] Commit: `tipo(escopo): mensagem`
```

## A seção "Ordem de trabalho"

Vai logo depois do objetivo, antes de qualquer especificação, porque é ela que impede a sessão de
implementar tudo e testar no fim. Ela abre no `ESTADO.md` e fecha nele — o protocolo está em
`continuidade-entre-sessoes.md`. Texto padrão, ajustando só os comandos:

```markdown
## Ordem de trabalho

**Passo 0 — abrir a sessão.** Leia `ESTADO.md` e confira `git status`. Os prompts anteriores
precisam estar concluídos; se algum estiver pendente ou em andamento, reconcilie pelo histórico:
commit encontrado + entregas presentes + suíte verde → marque concluído e siga; entrega parcial ou
suíte vermelha → termine o anterior antes; nada encontrado → pare e avise.

Depois, bloco a bloco, na ordem das seções abaixo. Para cada bloco:

1. Rode `<comando da suíte completa>` e anote o resultado. **Se já estiver vermelho, pare e avise** —
   não se constrói sobre suíte vermelha.
2. Escreva os testes do bloco (§N, grupo correspondente) e veja-os falhar **pelo motivo certo**.
   Teste que passa antes da implementação não testa nada: reescreva.
3. Implemente o mínimo que faz esses testes passarem, sem adiantar o bloco seguinte.
4. Rode os testes do bloco → verdes.
5. Rode `<comando da suíte completa>` → verde. Quebrou algo? Conserte o **código**, não o teste,
   salvo quando a especificação previr a mudança — e aí diga no commit qual decisão a autoriza.
6. Refatore com a suíte verde e rode de novo.

**Passo final — fechar a sessão.** Critérios de aceite conferidos, suíte e cobertura anotadas,
`ESTADO.md` atualizado e incluído **no mesmo commit** do trabalho.

Não feche a sessão no vermelho e não faça commit com teste pulado ou cobertura abaixo do piso.
```

## Nível de detalhe

A régua: **descreva a forma e as regras; deixe a implementação para quem executa.** Nomes de
arquivo, assinaturas, campos, validações, casos-limite e mensagens de erro são forma. Laços,
tratamento de nulo e organização interna de função são implementação.

Escreva código literal em três situações, porque reconstruí-lo daria margem a erro:

- Trechos canônicos difíceis de re-derivar (uma função SQL, um arquivo de configuração, uma regra de
  proxy).
- O conteúdo de arquivos que precisam sair exatamente assim (o `CLAUDE.md` do projeto, o
  `.env.example`).
- Exemplos de requisição e resposta de um contrato — o exemplo é o contrato.

Fora disso, tabela e regra.

**Antes:** "Criar a tabela de mensagens com os campos necessários e índices adequados."

**Depois:** tabela de colunas (nome | tipo | regras), lista de restrições com o `CHECK` escrito,
lista de índices com as colunas e a condição parcial, e uma linha dizendo qual consulta cada índice
serve. A segunda versão é a única em que duas sessões produzem o mesmo banco.

## Padrões por tipo de conteúdo

**Banco.** Por tabela: para que serve (uma linha), tabela de colunas (coluna | tipo | regras),
restrições (único, verificação, chave estrangeira e o que acontece ao apagar) e índices com o motivo
de cada um. Enums em tabela à parte, com a observação de quando a ordem dos valores tem significado.

**Endpoint.** Método e caminho como título; tabela de campos de entrada (campo | tipo | obrigatório |
regras); tabela ou lista dos erros possíveis (código, HTTP, quando acontece); resposta de sucesso
com exemplo real; efeitos colaterais (o que grava, o que enfileira, o que notifica). Se há
idempotência, diga o que acontece na segunda chamada idêntica **e** na segunda chamada com a mesma
chave e corpo diferente.

**Processo assíncrono (worker, job, consumidor).** Gatilho, passo a passo numerado, o que faz em
cada classe de erro (retentar com que espera, desistir, alertar), o que garante que rodar duas vezes
não duplica efeito, e como o trabalho perdido é recuperado.

**Tela.** Rota; de onde vêm os dados; o que se vê, em ordem visual; o que dá para fazer e o que cada
ação dispara; filtros e colunas nomeados um a um; estados de vazio, carregando e erro; o que
atualiza sozinho e de quanto em quanto tempo. Especifique os textos que o usuário lê quando eles
comunicam risco ("este número não envia pela API enquanto não tiver aplicação vinculada").

**Integração externa.** O que se chama, com que corpo, como o erro dele é classificado (permanente,
transitório, "não sei"), e o que o sistema faz em cada classe. A classe "não sei" é a que costuma
faltar e a que causa dano — decida explicitamente o que fazer quando não se sabe se a operação
aconteceu do outro lado.

## A seção de testes

É a parte mais importante do prompt: ela vira código **antes** da implementação, então tudo que
estiver vago aqui vira implementação vaga lá. Escreva **cenários**, não instruções genéricas: cada
linha diz o que se faz e o que tem de acontecer. "Testar os casos de erro" não vale nada; "telefone
com letra → 422 `invalid_phone`" é executável.

Agrupe por bloco (`### Bloco 2 — <assunto>`) e diga, em uma linha no começo da seção, onde os testes
ficam, qual o comando que roda só eles, e o que substitui o mundo externo. Nomeie os testes que
verificam invariantes do documento 00 pelo número deles — assim a violação aparece com nome no
relatório de falha.

O que precisa aparecer, sempre que existir no prompt:

- O caminho feliz de cada operação, com o corpo real.
- Cada erro previsto, com código e mensagem exatos.
- **Repetição:** a mesma operação duas vezes — o que acontece.
- **Concorrência:** duas operações ao mesmo tempo sobre o mesmo alvo.
- **Fronteira:** vazio, um, o máximo permitido, o máximo mais um.
- **Isolamento:** dados de um cliente/aplicação não aparecem para outro.
- **Falha do que está fora:** terceiro fora do ar, tempo esgotado, resposta inesperada.
- **Ordem:** o evento que chega antes do esperado não sobrescreve o estado mais avançado.

- **Invariantes** do documento 00 que este prompt pode violar, um teste cada.

Quando o prompt é o primeiro a tocar num serviço externo, o dublê controlável é **entrega dele**,
com lugar e nome definidos, e a lista do que ele precisa simular (erro permanente, transitório,
limite de taxa, credencial inválida, resposta fora do formato, lentidão maior que o tempo limite com
a operação tendo acontecido do outro lado). Credencial real em teste nunca, em nenhum prompt.

## Critérios de aceite

São a definição de pronto, e por isso precisam ser conferíveis sem interpretação: o comando que
passa, a tela que mostra tal coisa, o arquivo que existe, os testes da seção anterior verdes.

Três deles são fixos em todo prompt que produz comportamento, e existem porque são exatamente os
que uma sessão apressada pula:

```markdown
- [ ] `ESTADO.md` atualizado e incluído no commit do trabalho.
- [ ] Todos os cenários da §N implementados e verdes.
- [ ] `<comando da suíte completa>` verde — inclusive o que já existia antes deste prompt.
- [ ] Cobertura no piso combinado (<X>% global, <Y>% em `<módulos críticos>`), nenhum teste pulado,
      nenhuma asserção afrouxada.
```

A última linha é sempre a mensagem de commit, escrita por extenso. Parece detalhe; é o que faz o
histórico do repositório contar a mesma história que a especificação.

Bom: "`pnpm verificar` verde"; "`GET /health` responde 200"; "o painel mostra o número recém-cadastrado
na lista"; "nenhum segredo aparece em `GET /api/admin/contas`".

Ruim: "código funcionando"; "testes adequados"; "sem bugs".

## Erros comuns ao escrever prompts

| Erro | Efeito | Correção |
|---|---|---|
| Repetir o contrato dentro do prompt | As cópias divergem e ninguém sabe qual vale | Cite o documento de referência e a seção |
| "Conforme necessário", "se aplicável" | A sessão decide sozinha e cada uma decide diferente | Decida, ou marque como pendência com o que fazer enquanto isso |
| Prompt sem fronteira superior | A sessão invade o prompt seguinte | Diga no objetivo o que **não** faz |
| Prompt que não abre nem fecha no `ESTADO.md` | A sessão seguinte não sabe se pode começar, e refaz ou pula trabalho | Passo 0 e passo final na "Ordem de trabalho", e item nos critérios de aceite |
| `ESTADO.md` atualizado num commit separado | Sessão interrompida entre os dois deixa estado e código divergentes | Mesma mensagem de commit do trabalho, com o `ESTADO.md` dentro |
| Especificar a implementação inteira | Vira código mal escrito em markdown, e a sessão não consegue melhorar | Forma e regras; código só no que é canônico |
| Testes como "cobrir os casos" | Cobertura do caminho feliz e nada mais | Cenários nomeados com resultado esperado |
| Seção de testes no fim sem ordem de trabalho | A sessão implementa tudo e escreve teste de carimbo no final | Ciclo por bloco logo após o objetivo, cenários agrupados por bloco |
| Aceite pedindo só "testes novos verdes" | Regressão passa despercebida até a camada seguinte | Exigir a **suíte inteira** verde e a linha de base conferida no começo |
| Não dizer o que fazer quando um teste antigo falha | A sessão ajusta o teste e segue | Regra explícita: conserta o código; alterar teste só com decisão que autorize, dita no commit |
| Segredo ou dado real no exemplo | Vaza no repositório | Valores fictícios, sempre |
| Prompt gigante ("faça o backend") | Não cabe na sessão e termina pela metade | Divida por camada ou por fluxo |
