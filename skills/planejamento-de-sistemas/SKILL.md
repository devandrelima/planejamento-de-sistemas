---
name: planejamento-de-sistemas
description: Transforma uma ideia de sistema numa pasta de especificação executável — entrevista o usuário em blocos, fecha as decisões e escreve um documento de visão geral, um índice, prompts numerados prontos para uma IA construir (um por sessão, com critérios de aceite e commit), manuais humanos e registros de decisão (ADRs). Use sempre que o usuário quiser planejar, especificar, documentar ou "mapear" um sistema, produto, API, painel, integração ou módulo novo antes de programar — inclusive quando ele disser "quero criar um sistema que…", "preciso de um plano/PRD/especificação", "me ajuda a organizar como construir isso", "quero gerar os prompts para o Claude Code construir X", ou quando pedir uma funcionalidade grande dentro de um repositório que já existe. Use também para revisar, completar ou reescrever um planejamento que já existe nesse formato.
---

# Planejamento de sistemas

Esta skill produz **especificação executável**: uma pasta de documentos que basta entregar a uma IA
construtora (Claude Code, uma sessão por prompt) para o sistema sair de pé, sem que ela precise
adivinhar nada nem ter acesso à conversa original.

O teste de qualidade do que você escreve é este: **duas pessoas (ou duas sessões) diferentes, lendo
só esta pasta, constroem a mesma coisa.** Se um trecho admite duas implementações razoavelmente
diferentes, ele ainda não está pronto.

## O que você entrega

```
<pasta-de-saida>/
├── especificacao/
│   ├── README.md                      índice: tipo, dependências e entrega de cada arquivo
│   ├── 00_visao_geral_e_decisoes.md   referência-mãe: escopo, atores, arquitetura, glossário,
│   │                                  decisões numeradas, stack, convenções, invariantes, limites
│   ├── 01..NN_prompt_*.md             prompts executáveis, um por sessão, em ordem de dependência
│   ├── NN_contrato_*.md               referências de contrato (API, eventos, formatos), quando houver
│   ├── NN_manual_*.md                 manuais para pessoas (cadastros externos, cutover, operação)
│   └── NN_prompt_inicial_execucao.md  o que colar na primeira sessão da IA construtora
└── decisoes/
    └── 0000-modelo.md                 modelo de ADR para a IA registrar divergências durante a obra
```

Nem todo projeto usa tudo. O conjunto sai da entrevista, não de uma lista fixa.

**Onde gravar:** dentro do repositório do projeto, em `docs/especificacao/` e `docs/decisoes/`,
quando ele já existe. Quando o repositório ainda não existe, grave em
`./planejamento_<nome>/{especificacao,decisoes}/` na pasta atual — os documentos já se citam pelo
caminho `docs/especificacao/…`, e o prompt de arranque manda a IA construtora mover a pasta para lá
na primeira sessão.

## Princípios (o porquê do formato)

1. **Cada arquivo é autossuficiente.** Ele pode citar outros arquivos *desta mesma pasta*, nunca a
   conversa, nunca um repositório que o leitor talvez não tenha. Quem executa abre uma sessão limpa.
2. **Prompt é unidade de sessão, e sessão não tem memória.** Um prompt = uma sessão = uma camada
   coerente que fica verde sozinha = um commit, terminando em critérios de aceite verificáveis. Como
   a sessão seguinte não viu nada do que aconteceu, todo prompt **abre e fecha no `ESTADO.md`**: na
   abertura confere se os anteriores realmente terminaram, reconciliando com o histórico do git
   quando o arquivo estiver desatualizado; no fechamento registra a conclusão no mesmo commit do
   trabalho. `references/continuidade-entre-sessoes.md` tem o protocolo.
3. **Teste antes, sempre — é o diferencial deste formato.** A especificação não "inclui testes":
   ela nasce deles. Os cenários de cada prompt são escritos para serem implementados **primeiro**, em
   ciclo curto por bloco: suíte inteira verde como linha de base → testes do bloco falhando →
   implementação mínima → testes do bloco verdes → suíte inteira verde de novo. Teste escrito depois
   confirma o que o código faz; teste escrito antes verifica o que o sistema deveria fazer, e é a
   única coisa que uma IA construtora não consegue declarar pronta sem ser desmentida. Escreva todo
   prompt sabendo disso — `references/testes.md` tem a doutrina inteira e é leitura obrigatória antes
   da Fase 3.

4. **Separe referência de execução.** Documento de referência (visão geral, contrato) é lido por
   vários prompts e **não é executado**; manual é feito por uma pessoa; prompt é executado por uma
   IA. Marque o tipo no cabeçalho — misturar os três é a causa mais comum de a IA construir a coisa
   errada ou executar um manual.
5. **Decisão sem motivo não é decisão.** Toda escolha que alguém poderia questionar vira linha
   numerada (D1, D2, …) com o motivo ao lado. Os prompts depois citam "D12" em vez de repetir o
   argumento, e quem for mudar algo sabe o que está derrubando.
6. **Invariantes acima de instruções.** Uma lista curta (10 a 15) de coisas que nunca podem quebrar,
   escritas de forma verificável, vale mais que parágrafos de recomendação — elas sobrevivem a
   refatorações e viram teste.
7. **Tabelas em vez de prosa** para tudo que é enumerável: campos, colunas, enums, endpoints, telas,
   erros, variáveis de ambiente, alertas. Prosa esconde lacunas; tabela expõe a célula vazia.
8. **Descreva a forma e as regras, não o código.** Escreva a árvore de arquivos, as assinaturas, as
   validações e os casos-limite. Só escreva código literal quando reconstruí-lo daria margem a erro
   (um trecho de SQL, um JSON de configuração, o payload exato de um contrato).
9. **Fora de escopo é parte do escopo.** Liste explicitamente o que **não** se constrói. Sem isso a
   IA construtora inventa caixa de entrada, cobrança e painel de administração por conta própria.
10. **Fatos externos levam data.** Limite de API, preço, versão de biblioteca: registre "conferido em
   AAAA-MM-DD" e a regra de que a documentação oficial vence a especificação, com a divergência indo
   para um ADR. A especificação envelhece; essa regra impede que ela minta.

## Fluxo

### Fase 1 — Entrevista

Leia `references/entrevista.md`: banco de perguntas por bloco, o que inferir sem perguntar e como
propor padrões.

Conduza **em rodadas temáticas**, não numa lista única. Use `AskUserQuestion` com 2 a 4 perguntas
por rodada, sempre com uma opção recomendada primeiro e o motivo na descrição — decidir entre
alternativas explicadas é muito mais rápido, para o usuário, do que redigir requisitos do zero. Use
pergunta aberta quando a resposta for um nome, uma lista ou uma quantidade.

Deixe a resposta anterior mudar a próxima rodada: quem não tem interface não responde sobre telas;
quem não tem integração externa não responde sobre limites de terceiros.

Três reflexos que separam uma entrevista boa de um questionário:

- **Não pergunte o que dá para ler.** Em repositório existente, leia antes (stack, convenções,
  estrutura, migrations) e traga como afirmação a confirmar: "vi que o projeto usa X e Y; mantenho?".
- **Não deixe "não sei" virar invenção.** Vira "decisão pendente" no documento 00, com o que ela
  bloqueia e quem decide. Fingir que foi decidido custa muito mais caro depois.
- **Insista onde o erro é caro** (dinheiro, dado que some, mensagem enviada duas vezes, segredo
  vazado) e aceite padrão onde não é. O usuário raramente sabe onde isso está — você sabe.

Antes de escrever qualquer documento, devolva um **resumo do mapeamento** (o que é, quem usa, o que
está dentro, o que está fora, as decisões fechadas e as pendentes) e peça confirmação. É mais barato
corrigir um resumo de trinta linhas que uma pasta de quinze arquivos.

### Fase 2 — Plano do conjunto

Com o escopo fechado, decida **quais documentos existem e em que ordem**, usando
`references/estrutura-do-conjunto.md` (como fatiar em prompts, a sequência típica, a tabela de
dependências, quando criar contrato e manual separados).

Mostre o índice proposto ao usuário antes de escrever — uma tabela de arquivo / tipo / depende de /
entrega. É a última chance barata de perceber que falta uma camada inteira.

### Fase 3 — Escrita

Leia `references/testes.md` antes de escrever a primeira linha: a estratégia de testes atravessa o
documento 00, o prompt de fundação, cada prompt de funcionalidade e os critérios de aceite, e
enxertá-la depois nunca fica coerente.

Escreva **o documento 00 primeiro** (`references/documento-00.md`) e só então os prompts
(`references/anatomia-do-prompt.md`), na ordem do índice. O 00 é o contrato entre os prompts: se
decisões, convenções e invariantes não estiverem fechados ali, cada prompt reinventa os seus e o
sistema sai incoerente.

Modelos em `assets/` para copiar e preencher. Em projeto dentro de repositório existente, leia
`references/sistema-existente.md` antes — o que muda é substancial.

Escreva cada arquivo inteiro de uma vez e siga em frente; não peça aprovação documento a documento.
Ao final de cada um, uma linha dizendo o que entregou e qual é o próximo.

### Fase 4 — Revisão e entrega

Passe o conjunto pela lista de `references/qualidade.md` — ela pega o que costuma faltar (prompt sem
critério de aceite, invariante não verificável, termo usado e não definido, dependência circular).

Entregue com: onde a pasta ficou, a ordem de execução, o que o usuário precisa fazer com as próprias
mãos (contas, credenciais, cadastros externos), as decisões pendentes e os riscos que você registrou.

## Regras que valem o tempo todo

- **Idioma:** documentos em português do Brasil, salvo pedido diferente ou projeto já em outro idioma.
  Nomes de arquivo sem acento e em snake_case (`03_prompt_backend_nucleo.md`).
- **Nada de placeholder.** "TODO", "a definir" e "conforme necessário" dentro de um prompt viram
  improviso da IA construtora. Ou você decide, ou marca como decisão pendente no 00 e o prompt que
  depende dela diz explicitamente o que fazer enquanto isso.
- **Nenhum segredo nos documentos.** Nomes de variáveis e formatos, sim; valores reais, nunca.
- **Nenhum prompt sem abertura e fechamento de sessão.** A "Ordem de trabalho" de todo prompt começa
  no `ESTADO.md` e termina nele. O arquivo é uma afirmação e o git é a evidência: quando divergirem,
  vale o histórico, e o que não foi verificado na própria sessão nunca é marcado como concluído.
- **Nenhum prompt sem testes.** Todo prompt que produz comportamento traz a seção de cenários
  organizada por bloco, a ordem de trabalho em ciclo vermelho-verde e critérios de aceite exigindo
  suíte **inteira** verde, piso de cobertura e zero testes pulados. Prompt que entrega só estrutura
  (configuração, imagens, documentação) diz explicitamente por que não tem cenário — o silêncio aqui
  é sempre esquecimento.
- **Riscos ditos na cara.** Se a arquitetura escolhida tem um ponto único de falha, um custo que
  escala mal ou um acoplamento incômodo, escreva isso no documento em uma frase. O usuário decidiu
  com essa informação; sem ela, decidiu no escuro.
- **Tamanho é consequência, não meta.** Um prompt costuma ficar entre 200 e 600 linhas. Muito menos
  que isso normalmente é falta de especificação; muito mais é uma sessão que não vai caber e pede
  divisão.

## Arquivos desta skill

| Arquivo | Leia quando |
|---|---|
| `references/entrevista.md` | Fase 1 — banco de perguntas por bloco e padrões a propor |
| `references/estrutura-do-conjunto.md` | Fase 2 — como fatiar o sistema em prompts e montar o índice |
| `references/documento-00.md` | Fase 3 — seção a seção do documento de visão geral |
| `references/continuidade-entre-sessoes.md` | Fase 3 — protocolo do `ESTADO.md`: abertura, reconciliação por git, fechamento |
| `references/testes.md` | **Antes da Fase 3, sempre** — TDD por bloco, cobertura, níveis, dublês, regressão |
| `references/anatomia-do-prompt.md` | Fase 3 — como escrever um prompt executável e o nível de detalhe |
| `references/sistema-existente.md` | Fase 3, quando o alvo é um repositório que já existe |
| `references/qualidade.md` | Fase 4 — revisão final do conjunto |
| `assets/00_visao_geral_e_decisoes.md` | Modelo do documento 00 |
| `assets/README_indice.md` | Modelo do índice (gravar como `README.md` na pasta de saída) |
| `assets/NN_prompt.md` | Modelo de prompt executável |
| `assets/NN_contrato.md` | Modelo de documento de contrato |
| `assets/NN_manual.md` | Modelo de manual humano |
| `assets/NN_prompt_inicial_execucao.md` | Modelo do prompt de arranque e do prompt das sessões seguintes |
| `assets/ESTADO.md` | Modelo do arquivo de progresso entre sessões |
| `assets/decisoes/0000-modelo.md` | Modelo de ADR, copiado para a pasta `decisoes/` da saída |
