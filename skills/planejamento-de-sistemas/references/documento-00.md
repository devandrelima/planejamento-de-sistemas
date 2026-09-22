# O documento 00 — visão geral, decisões e invariantes

É o único arquivo que **todo** prompt lê antes de agir. Ele existe para que nenhuma sessão precise
decidir de novo o que já foi decidido. Modelo em `assets/00_visao_geral_e_decisoes.md`.

Cabeçalho obrigatório, logo abaixo do título:

```markdown
> **Tipo:** referência. Não é um prompt para executar. Todos os prompts pressupõem que este
> arquivo foi lido.
```

Seções, na ordem. Pule as que não se aplicam, mas não invente ordem nova — quem lê vários planos
encontra a mesma coisa no mesmo lugar.

## 1. O que é

Dois a cinco parágrafos: o que o sistema é, para quem, e o que cada público obtém dele. Escreva para
alguém competente que nunca ouviu falar do projeto. Nada de marketing, nada de história.

### 1.1 Fora de escopo (não construir)

Lista explícita, cada item com meia linha do porquê ou de quem faz aquilo em vez do sistema. Inclua
o que é **quase** escopo — o que um implementador razoável construiria por conta própria achando que
ajuda. É a seção que mais economiza trabalho jogado fora.

## 2. Atores

Tabela: ator | como interage. Uma linha por tipo de gente ou sistema, incluindo o que nunca fala
direto com o sistema (usuário final que só recebe o resultado), porque isso evita telas inventadas.

## 3. Arquitetura

Um diagrama em bloco de texto (ASCII dentro de bloco de código), mostrando os processos, por onde
entra requisição, o que fala com o quê e onde os dados ficam. Um desenho medíocre que caiba na tela
vale mais que três parágrafos.

Logo abaixo, o **princípio central** da arquitetura em uma frase forte — a regra que decide empates
quando o implementador tiver dúvida. Exemplos: "o banco é a fonte de verdade; filas só aceleram, e
varreduras recuperam o que ficou para trás"; "nenhum estado vive no processo: qualquer réplica
atende qualquer requisição"; "o arquivo bruto nunca é alterado, só derivado".

## 4. Glossário

Tabela: termo | significado. Todo termo do domínio, do negócio ou de terceiro usado nos outros
documentos. Inclua identificadores externos com o formato real, porque é onde se erra
(`wamid.HBgM…`, `cus_…`). Regra prática: se o termo aparece num prompt e não está aqui, falta linha.

## 5. Decisões

Tabela numerada: `#` | decisão | motivo. D1, D2, D3… Cada decisão é uma frase afirmativa no
presente, e o motivo cabe em uma linha.

Entra aqui o que alguém poderia questionar depois: escolha de compatibilidade, modelo de permissão,
o que é obrigatório, como se resolve conflito, onde hospeda, o que se guarda cifrado, o que é
aditivo e o que quebra. Não entra o óbvio ("usar controle de versão").

Os prompts citam por número ("como manda a D12"), então **a numeração é estável**: decisão revogada
vira linha com a marca de revogada e a nova decisão entra no fim, nunca renumerando as outras.

Se houver decisões tomadas por padrão (o usuário não tinha preferência) ou pendentes, faça uma
subseção separada para elas, dizendo o que cada pendência bloqueia e quem decide. Uma pendência
visível é um risco administrado; escondida, é uma surpresa no meio da obra.

## 6. Stack

Tabela: camada | tecnologia. Diga explicitamente se as versões são mínimo ou travamento, e o que
fazer quando a versão instalada divergir (o padrão saudável: usar a estável mais recente, tratar a
tabela como mínimo e registrar o que foi instalado num ADR).

## 7. Convenções

Tabela: tema | regra. É o que impede que cada sessão escolha um estilo:

- Idioma da documentação, da interface, dos logs e das mensagens de erro.
- Idioma e caixa dos nomes no código, no banco e em cada API (podem diferir de propósito — se
  diferirem, diga o porquê, ou alguém vai "corrigir").
- Identificadores: tipo, quem gera, se são ordenáveis.
- Datas: tipo no banco, formato na API, fuso na exibição.
- Formato dos erros, por superfície.
- Paginação.
- Exclusão: o que se apaga de fato e o que só muda de status.
- Qualquer armadilha conhecida da stack que já custou tempo a alguém.

## 8. Invariantes (nunca quebrar)

Lista numerada, de 10 a 15 itens, cada um verificável — dá para escrever um teste ou apontar a linha
que viola. São as regras que sobrevivem a qualquer refatoração e que a IA construtora vai reler em
toda sessão pelo `CLAUDE.md`.

Dois invariantes sobre testes são quase sempre justos, porque protegem todos os outros: **nenhum
commit com a suíte vermelha ou com teste pulado**, e **bug corrigido só entra com o teste que o
reproduz, escrito antes da correção**.

Bom: "toda requisição aceita existe no banco antes de responder 202"; "nenhuma chamada ao serviço
externo fora do módulo `X/`"; "segredo nunca aparece em resposta, log ou erro"; "status nunca
regride".

Ruim: "o código deve ser limpo"; "ter boa cobertura de testes"; "seguir boas práticas". Não são
invariantes, são desejos — e ocupam o lugar dos que importam.

## 9. Estratégia de testes

A seção que faz o resto valer. Fecha, para o conjunto inteiro, o que cada prompt depois só cita
(detalhes e o porquê em `testes.md`):

- **Método:** ciclo vermelho-verde por bloco, com a suíte completa rodando como linha de base no
  começo de cada bloco e de novo depois dele. Diga isso aqui uma vez; os prompts repetem o ciclo na
  seção "Ordem de trabalho".
- **Níveis e o que cada um cobre:** unidade, integração com banco e fila reais, contrato das
  superfícies públicas, ponta a ponta nos fluxos principais, carga leve se houver limite de vazão.
- **Pisos de cobertura:** o global e o alto, com os **módulos de piso alto nomeados** (regra de
  negócio, idempotência, dinheiro, permissão, cifragem, transição de estado). Sem nome, o piso alto
  não é aplicado por ninguém.
- **O que fica fora da conta:** gerado, migrations, configuração, dublês.
- **Comando único de verificação** e o que ele roda; qual comando roda a suíte de integração.
- **Dublês:** qual serviço externo é substituído, por quê, onde mora o dublê e o que ele simula.
- **Determinismo:** relógio injetado, semente fixa, banco limpo entre testes, sem espera por tempo
  fixo.
- **Proibições:** pular teste, afrouxar asserção, apagar caso, baixar o piso para o build passar.

## 10. Limites e fatos externos

Quando o sistema depende de terceiro: tabela item | limite | conferido. A coluna "conferido" diz o
que foi verificado na documentação oficial e a seção traz a **data** da verificação. Acrescente onde
esses valores vivem no código (um arquivo só de constantes) e a instrução de reconferir antes de
implementar.

Inclua o que muda com data conhecida (preço, versão, regra que entra em vigor) — é informação que
salva de uma surpresa e some se ficar só na conversa.

## 11. Mapa dos documentos

Uma linha apontando para o `README.md` da pasta. Duplicar o índice aqui só cria duas versões para
divergirem.
