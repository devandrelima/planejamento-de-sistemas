# Revisão final do conjunto

Passe por esta lista antes de entregar. Ela é feita do que costuma faltar — e o custo de cada falha
é uma sessão de obra desperdiçada, não um comentário de revisão.

## Coerência do conjunto

- [ ] Todo arquivo citado existe, e nenhum arquivo cita algo de fora da pasta (nem a conversa, nem
      um repositório que o leitor talvez não tenha).
- [ ] O `README.md` tem o índice com tipo, dependência e entrega de cada arquivo, e bate com os
      arquivos que existem de fato.
- [ ] As dependências entre prompts formam uma ordem possível: nenhum depende de algo que vem depois.
- [ ] Cada arquivo diz no cabeçalho o que é (referência, prompt, manual, arranque).
- [ ] Nada importante está escrito em dois lugares. Onde houver repetição inevitável (invariantes no
      00 e no `CLAUDE.md`), os textos são idênticos, não parecidos.
- [ ] As decisões numeradas citadas pelos prompts existem com esse número no 00.

## Documento 00

- [ ] Fora de escopo está escrito, e inclui o que um implementador construiria por conta própria.
- [ ] Todo termo de domínio usado nos prompts está no glossário.
- [ ] Toda decisão tem motivo em uma linha; decisões tomadas por padrão e pendências estão marcadas
      como tal, com o que cada pendência bloqueia.
- [ ] Os invariantes são verificáveis um a um — dá para escrever o teste ou apontar a violação.
      Nenhum deles é um desejo genérico ("código limpo", "boa cobertura").
- [ ] Convenções cobrem idioma, nomes, identificadores, datas, erros, paginação e exclusão.
- [ ] Fatos externos (limites, preços, versões) têm data de verificação e a regra de que a
      documentação oficial vence a especificação.

## Cada prompt

- [ ] Cabeçalho com pré-requisito, o que ler antes e quais revisões rodar ao final.
- [ ] Objetivo diz o que entrega **e** o que não faz.
- [ ] Estrutura de arquivos, com os arquivos alterados também, quando o repositório já existe.
- [ ] Nenhum "a definir", "conforme necessário", "se aplicável", "implementar adequadamente".
- [ ] Tudo que é enumerável está em tabela: campos, colunas, enums, erros, telas, variáveis, alertas.
- [ ] Cada erro tem código, situação que o causa e o que o consumidor recebe.
- [ ] Seção de testes com cenários nomeados e resultado esperado, cobrindo repetição, concorrência,
      fronteira, isolamento, falha do serviço externo e ordem de eventos.
- [ ] Critérios de aceite conferíveis sem interpretação, terminando na mensagem de commit.
- [ ] Cabe numa sessão (200 a 600 linhas). Se passou muito, divida; se ficou muito curto, provavelmente
      está vago.

## Testes (é onde este formato ganha ou perde)

- [ ] O documento 00 tem a seção de estratégia de testes: método, níveis, pisos de cobertura com os
      **módulos críticos nomeados**, comando único de verificação, dublês, determinismo e proibições.
- [ ] O prompt de fundação entrega arcabouço de teste, medição de cobertura com o piso configurado e
      CI que quebra abaixo dele — antes de qualquer regra de negócio.
- [ ] Todo prompt que produz comportamento tem a seção "Ordem de trabalho" com o ciclo por bloco, e
      os cenários da seção de testes estão **agrupados por bloco**.
- [ ] Nenhum prompt manda implementar antes de escrever o teste do bloco.
- [ ] Os critérios de aceite de cada prompt exigem a **suíte inteira** verde (não só os testes
      novos), o piso de cobertura e zero testes pulados.
- [ ] Está escrito o que fazer quando um teste antigo falha: consertar o código; alterar o teste só
      com decisão que autorize, citada no commit.
- [ ] Está escrito que bug entra com teste de reprodução antes da correção.
- [ ] Cada serviço externo tem dublê definido, com a lista do que ele simula — inclusive o caso da
      operação que aconteceu do outro lado e cuja resposta se perdeu.
- [ ] Nenhum teste usa credencial real.
- [ ] Os invariantes do documento 00 aparecem como cenário em algum prompt, nomeados pelo número.
- [ ] O que ficou de fora da automação está dito, com o item de conferência manual correspondente.

## Segurança e dados

- [ ] Nenhum segredo, credencial, token ou dado pessoal real em exemplo algum.
- [ ] Está dito o que é cifrado em repouso, o que é mascarado em log e o que nunca volta numa
      resposta de API.
- [ ] Autenticação e autorização de cada superfície estão especificadas, inclusive as internas.
- [ ] Os prompts que mexem com segredo, autenticação, pagamento ou dado pessoal pedem revisão de
      segurança no cabeçalho.
- [ ] Testes usam dublê do serviço externo, nunca credencial de verdade.

## Execução

- [ ] Existe prompt de arranque dizendo a ordem, o que é referência, o que é manual (e que manual
      não se executa), quando parar e como retomar.
- [ ] Existe `ESTADO.md` com as regras de abertura e fechamento no próprio corpo, e a tabela tem
      situação, mensagem de commit canônica, hash, suíte/cobertura e observações.
- [ ] Todo prompt abre no `ESTADO.md` (passo 0, com a reconciliação por histórico e os três
      desfechos: marcar concluído, terminar o anterior, ou parar e avisar) e fecha nele, no **mesmo
      commit** do trabalho.
- [ ] Está escrito que nunca se marca como concluído o que não foi verificado na própria sessão.
- [ ] Está escrito o que fazer quando a sessão precisa parar no meio de um prompt.
- [ ] A mensagem de commit de cada prompt é única e distintiva o bastante para ser encontrada por
      `git log --grep` — é ela que identifica a linha do `ESTADO.md`.
- [ ] Existe registro de divergências (`decisoes/` com modelo de ADR).
- [ ] Os limites do que a IA não pode fazer sem autorização estão escritos (deploy, tocar em outro
      repositório, apagar dados, abrir PR, usar credencial real).
- [ ] O que depende de uma pessoa está num manual, não escondido no meio de um prompt.

## Teste de leitura

Escolha o prompt do meio do conjunto e leia como se você fosse a sessão que vai executá-lo, sem
lembrar da conversa. Toda pergunta que aparecer na sua cabeça é uma lacuna: ou o prompt responde, ou
diz em que arquivo está a resposta.

Depois repita a leitura com uma pergunta só: **o que aqui admite duas implementações diferentes?**
Cada ponto encontrado vira uma linha de tabela ou um critério de aceite.
