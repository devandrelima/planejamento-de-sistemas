# Planejamento de sistemas — instruções completas

> Versão de arquivo único, para IAs que não têm sistema de skills. Cole como instrução do
> projeto/assistente, ou anexe à base de conhecimento, e comece dizendo o que quer planejar.
>
> Tudo o que a skill original divide em arquivos está aqui, na ordem de leitura. Onde o texto disser
> "leia `references/x.md`" ou "modelo em `assets/y.md`", role até a seção correspondente deste
> arquivo — os títulos de nível 1 marcam cada um.
>
> Gerado em 2026-09-21.

---


<!-- ═══ SKILL.md ═══ -->

# ARQUIVO: SKILL.md

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


---


<!-- ═══ references/entrevista.md ═══ -->

# ARQUIVO: references/entrevista.md

# Entrevista de mapeamento

Onze blocos. Não são um formulário: são o que precisa estar respondido antes de a especificação
existir. Percorra na ordem, pulando o que não se aplica e o que você já conseguiu ler em vez de
perguntar.

**Ritmo:** 2 a 4 perguntas por rodada, com `AskUserQuestion` sempre que houver alternativas — opção
recomendada primeiro, com o motivo na descrição. Pergunta aberta só quando a resposta é um nome, uma
lista ou um número. Depois de cada bloco, uma frase confirmando o que você entendeu; ao final de
tudo, o resumo completo para aprovação.

**Padrão proposto:** quando o usuário não tiver opinião, proponha um padrão com uma linha de motivo
e siga — marcando no documento 00 que foi decidido por padrão, para ficar fácil derrubar depois.
Travar a entrevista numa escolha que o usuário não tem como fazer é desperdício.

**Sinal de "não sei":** vira decisão pendente registrada (o que falta, o que ela bloqueia, quem
decide). Nunca vira invenção silenciosa.

---

## Bloco 0 — Contexto da construção

Define o formato do conjunto inteiro; faça primeiro.

- Sistema novo do zero ou funcionalidade dentro de um repositório que já existe? (se existente, peça
  o caminho e **leia o código antes de continuar** — ver `sistema-existente.md`)
- Nome do sistema/módulo e do repositório.
- Quem constrói: IA em sessões (padrão), pessoa, ou os dois?
- Onde a especificação deve ser gravada e em qual caminho ela vai viver no repositório final (padrão:
  `docs/especificacao/`, porque os arquivos se citam por esse caminho).
- Existe prazo, entrega parcial obrigatória ou dependência externa com data?

## Bloco 1 — Produto e propósito

- O que o sistema é, em uma frase, para alguém que nunca ouviu falar dele.
- Que problema concreto ele resolve hoje, e como esse problema é resolvido enquanto ele não existe
  (planilha, sistema de terceiro, trabalho manual)? Isso costuma revelar o escopo real.
- Ele substitui algo? Se sim, o que precisa continuar funcionando igual durante e depois da troca?
- Como se sabe que deu certo? (métrica, volume, evento observável)
- **O que ele explicitamente não é.** Puxe: "isso não tem X, certo?" para as funcionalidades que
  sistemas desse tipo normalmente têm — relatórios, cobrança, chat, app móvel, multi-idioma,
  multiempresa. Cada "não" aqui economiza um prompt inteiro depois.

## Bloco 2 — Atores e acessos

Para cada tipo de gente ou sistema que interage:

- Quem é, por onde entra (painel, API, webhook, e-mail, CLI) e o que faz lá dentro.
- Como se autentica (usuário e senha, chave de API, OAuth, token de serviço) e se há 2FA.
- Há níveis de acesso diferentes? **Pergunte direto se um nível só resolve** — hierarquia de
  permissões custa caro em banco, API, testes e telas, e equipes pequenas quase sempre estão melhor
  com um nível e auditoria de tudo. Se houver níveis, peça a matriz: quem pode o quê.
- Quantos usuários simultâneos, na ordem de grandeza.
- Alguém de fora da organização acessa? (muda o modelo de isolamento de dados)

## Bloco 3 — Escopo funcional

- Liste as capacidades do sistema como frases de ação ("enviar mensagem", "aprovar pedido",
  "conciliar pagamento"). Peça a lista bruta e depois organize.
- Para cada uma: entra no primeiro corte ou fica para depois? O que fica para depois vai para uma
  seção "não construir agora" — presente no documento, ausente do código.
- Qual é o fluxo principal, do começo ao fim, na vida real? Peça para narrar um caso concreto, com
  nomes e valores. É a forma mais rápida de descobrir passos que ninguém menciona em abstrato.
- O que acontece quando o fluxo principal falha no meio? (é onde moram metade dos requisitos)
- Existe algo que roda sozinho: agendamento, varredura, lembrete, fechamento diário, importação?

## Bloco 4 — Dados e domínio

- Quais são as entidades e como se relacionam. Peça exemplos reais de cada uma.
- Para cada entidade: quem cria, quem altera, o que nunca pode mudar depois de criado.
- Estados e transições: uma entidade com status precisa da lista de estados e de quais transições
  são possíveis. Pergunte se algum estado pode voltar atrás — "nunca regride" é invariante clássico.
- Volume: quantas linhas por dia/mês hoje e em um ano. Ordem de grandeza basta e muda índice,
  paginação e retenção.
- Dados pessoais ou sensíveis? Quais, e o que a LGPD exige aqui (exclusão, exportação, consentimento).
- Retenção: o que se apaga, quando, e o que **nunca** se apaga. Padrão sugerido: configuração não se
  apaga, ganha status; só dado de log/tráfego tem expurgo por idade.
- Precisa de histórico/auditoria de quem mudou o quê? (padrão: sim para toda mutação de configuração)

## Bloco 5 — Integrações externas

Para cada serviço de terceiro (pagamento, mensageria, e-mail, ERP, IA, storage):

- O que o sistema pede a ele e o que ele manda de volta (inclusive webhooks/callbacks).
- Como se autentica, e de quem são as credenciais (da sua empresa ou de cada cliente).
- Limites conhecidos: tamanho, taxa, janela de tempo, validade de identificador, custo por chamada.
  **Anote que precisam ser reconferidos na documentação oficial antes de virar constante**, com a
  data da conferência.
- Existe ambiente de teste/sandbox? Se não, como se testa sem gastar dinheiro ou mandar mensagem
  para gente de verdade? (a resposta quase sempre é "falso dublê do serviço", e isso vira um prompt)
- O que fazer quando ele está fora do ar ou devolve erro: retentar, desistir, avisar quem?

## Bloco 6 — Contratos e interfaces de programa

Só se o sistema expõe API, eventos ou arquivos para alguém consumir.

- Quem consome, e já existe consumidor em produção? Se sim, **o contrato existente manda** — peça os
  arquivos ou exemplos reais e trate compatibilidade como invariante.
- Estilo: REST/JSON, RPC, fila, arquivo. Idioma e caixa dos campos.
- Formato de erro: corpo, códigos, e qual HTTP para cada família. Decida cedo, porque consumidor
  trata código por código.
- Idempotência: o chamador pode repetir a mesma requisição? Como se identifica repetição e o que se
  devolve na segunda vez? (obrigatório sempre que uma operação custa dinheiro ou é visível para um
  terceiro)
- O sistema chama de volta (callback/webhook)? Assinatura, ordem, retentativa, o que garante que não
  regride.
- Há operação em lote? Um item inválido invalida o lote ou os outros passam?
- Versionamento: o que se pode acrescentar sem quebrar e o que exige versão nova.

## Bloco 7 — Interface de uso

Só se houver painel, site ou app.

- Quem usa, com que frequência, em que dispositivo.
- **Qual é a tela inicial e o que se faz nela?** Essa resposta define a navegação inteira; insista
  até ela ficar concreta.
- Lista as telas principais e, para cada uma: o que mostra, o que dá para fazer, de onde se chega.
- Há um recorte que organiza tudo (por cliente, por número, por loja, por período)? Se sim, é bem
  provável que ele seja a estrutura de navegação, e que misturar recortes numa mesma tela seja um
  erro que você deve proibir por invariante.
- Precisa de tempo real/atualização automática, ou recarregar na mão resolve?
- Idioma, fuso horário de exibição, formato de data e moeda.
- Tem identidade visual/design system a seguir, ou padrão de biblioteca resolve?

## Bloco 8 — Requisitos não-funcionais

- Volume e pico esperados; quanto tempo uma operação pode demorar antes de incomodar.
- O que acontece se o sistema ficar fora do ar por uma hora? (define disponibilidade, fila,
  recuperação — e se a resposta for "nada grave", não construa alta disponibilidade)
- Perder um registro é aceitável? Se não, é o gatilho para "banco é a fonte de verdade, fila é só
  gatilho, varredura recupera o que ficou para trás".
- Segurança: segredos em repouso, mascaramento em log, 2FA, limite de taxa, bloqueio por IP.
- Observabilidade: log estruturado, métricas, alertas — e **para onde o alerta vai** e quem olha.
- Backup e restauração: frequência, e quem já testou restaurar.

## Bloco 9 — Stack e convenções

- Linguagens, frameworks, banco, fila, hospedagem: há preferência, restrição da equipe ou algo que
  já está em uso? Em repositório existente isso é leitura, não pergunta.
- Monorepo ou repositórios separados; pacotes compartilhados.
- Convenções de nome: idioma do código, do banco e do JSON. Podem ser diferentes entre si e isso
  precisa estar escrito, ou cada prompt escolhe uma.
- Política de versão: fixar as versões atuais ou usar a estável mais recente na instalação (padrão:
  a mais recente, com as versões da especificação valendo como mínimo, e o que for instalado indo
  para um ADR — a especificação envelhece entre a escrita e a obra).
- Há ferramenta de qualidade obrigatória (lint, formatador, CI, revisão)?

### 9.1 Testes — feche aqui, não depois

Estas respostas atravessam o conjunto inteiro (ver `testes.md`), e mudá-las no meio da obra custa
caro. Proponha os padrões e siga:

- Ferramenta de teste, de integração e de ponta a ponta; e **um comando único** que roda tudo.
- Piso de cobertura. Padrão proposto: **80% global** medido no CI, quebrando o build abaixo disso, e
  **90 a 95% nos módulos críticos**. Pergunte quais módulos são críticos — ou, melhor, proponha a
  partir do que você já mapeou: regra de negócio, idempotência, dinheiro, permissão, cifragem,
  transição de estado.
- Integração roda contra banco e fila **de verdade** (em container) ou contra dublê? Padrão: de
  verdade, porque é justamente o banco que mente nos testes em memória.
- Como se testa cada serviço externo sem gastar dinheiro nem falar com gente real. Se não há
  sandbox, o dublê controlável vira entrega de um prompt.
- Existe suíte hoje (repositório existente)? Está verde? Quanto tempo leva? Se for lenta demais para
  rodar a cada bloco, defina o subconjunto rápido por área e a suíte inteira ao fim de cada prompt.
- Alguma coisa fica **fora** da automação de propósito (envio real, integração de terceiro sem
  sandbox, aparência visual)? O que fica de fora precisa de um item de conferência manual no manual
  de operação — fora da automação não pode virar fora da verificação.

## Bloco 10 — Operação e entrega

- Onde roda: nuvem, VPS, máquina da empresa. Compartilha infraestrutura com outro sistema? (se sim,
  diga em uma frase o risco que isso cria — ponto único de falha, vizinho barulhento)
- Ambientes: desenvolvimento, homologação, produção. Dados de teste vêm de onde?
- Deploy: manual, script, CI. Quem aperta o botão e como se volta atrás.
- Se substitui um sistema existente: como é a virada? Os dois convivem? Tem rollback? Quem avisa os
  consumidores? **Isso costuma virar um manual humano próprio**, não um prompt.
- Quem opera no dia a dia e o que essa pessoa precisa conseguir fazer sozinha.
- Existe configuração que só uma pessoa consegue fazer (criar conta em serviço de terceiro, aprovar
  cadastro, pedir número)? Vira manual humano com passo a passo.

## Bloco 11 — Riscos e pendências

- O que ainda não está decidido e depende de alguém ou de algo externo.
- O que mais preocupa o usuário neste projeto. Pergunte diretamente; a resposta costuma apontar onde
  a especificação precisa ser mais dura (invariante, teste, alerta).
- O que já deu errado antes, aqui ou num sistema parecido.
- O que muda nos próximos meses e já é conhecido (mudança de preço, de API, de regra, de lei).

---

## Fechamento

Devolva o resumo em tópicos curtos, nesta ordem, e peça confirmação:

1. O que é o sistema, em uma frase.
2. Atores e como cada um entra.
3. Dentro do escopo — lista de capacidades.
4. **Fora do escopo** — lista explícita.
5. Decisões fechadas, numeradas, com motivo em meia linha (as que você propôs por padrão marcadas
   como tal).
6. Decisões pendentes, com o que cada uma bloqueia.
7. Riscos que você enxerga e que o usuário ainda não comentou.

Confirmado o resumo, ele vira o documento 00 quase literalmente.


---


<!-- ═══ references/estrutura-do-conjunto.md ═══ -->

# ARQUIVO: references/estrutura-do-conjunto.md

# Estrutura do conjunto: como fatiar o sistema em documentos

O conjunto tem quatro tipos de documento, e o tipo vai escrito no cabeçalho de cada arquivo porque
ele muda quem age:

| Tipo | Quem lê | O que faz com ele |
|---|---|---|
| **Referência** | Todos os prompts | Lê e obedece. Nunca é executado sozinho (visão geral, contrato) |
| **Prompt** | IA construtora | Executa numa sessão, do começo ao fim, e entrega um commit |
| **Manual** | Pessoa | Segue passo a passo fora do código (cadastro em terceiro, cutover, operação) |
| **Prompt de arranque** | IA construtora, uma vez | Organiza a execução de todos os outros |

## Como fatiar em prompts

Um prompt é **uma sessão de trabalho**. O corte bom tem quatro propriedades:

0. **Começa e termina com a suíte inteira verde.** É a propriedade que dá sentido às outras: a
   sessão mede a linha de base antes de mexer e só fecha quando tudo — o novo e o antigo — está
   verde, com a cobertura no piso. Ver `testes.md`.
1. **Fecha verde sozinho.** Ao fim dele, o projeto compila, os testes passam e existe algo
   verificável — nem que seja um endpoint de saúde. Um prompt que só faz sentido junto com o
   seguinte está cortado no lugar errado.
2. **Depende só do que já foi feito.** A ordem é a ordem de dependência real. Se A precisa de B e B
   precisa de A, o corte está errado: separe a parte comum num prompt anterior.
3. **Cabe numa sessão.** Na prática, 200 a 600 linhas de especificação. Acima disso, divida por
   camada ("fundação" e "telas") ou por área ("envio" e "recebimento").
4. **Tem um commit só.** Se você não consegue escrever a mensagem de commit em uma linha, são dois
   prompts.

Cortes que funcionam, em ordem de preferência: **por camada** (fundação → dados → núcleo → domínio →
interface → operação), depois **por fluxo** (envio, recebimento, conciliação), depois **por
superfície** (API pública, API interna, telas). Corte ruim: por entidade do banco — espalha a mesma
camada por dez sessões e cada uma reinventa a estrutura.

## Sequência típica — sistema novo

Adapte; nem todo projeto tem todas as etapas, e a numeração deve refletir a ordem real de execução.

| # | Prompt | Entrega |
|---|---|---|
| 00 | *(referência)* Visão geral e decisões | O contrato entre todos os prompts |
| 01 | Fundação | Estrutura do repositório, ferramentas, lint, **arcabouço de teste com medição de cobertura e o piso já configurado**, comando único de verificação, ambiente local, CI que quebra abaixo do piso, `CLAUDE.md`, ADRs iniciais |
| 02 | Dados | Schema completo, migrations, seeds, infraestrutura de teste de integração |
| 03 | Núcleo | Configuração, log, erros, cifragem, autenticação, auditoria, filas, saúde, métricas |
| 04 | Integrações externas | Cliente do serviço de terceiro, classificação de erros, **dublê falso para teste** |
| 05 | *(referência)* Contrato | Endpoints/eventos campo a campo, erros, exemplos |
| 06+ | Domínio | Um prompt por fluxo grande: o que o sistema faz de fato |
| … | Entrada assíncrona | Webhook/consumo de fila: receber, validar, gravar, processar |
| … | Trabalhos periódicos | Varreduras, sincronizações, alertas, retenção |
| … | API interna | Endpoints que a interface consome |
| … | Interface — fundação | App, login, layout, navegação, componentes base, cliente tipado |
| … | Interface — telas | Todas as telas, campo a campo |
| … | Testes de ponta a ponta | Compatibilidade com consumidores reais, E2E, checklist de segurança |
| … | Infraestrutura e deploy | Imagens, orquestração, proxy, deploy, backup, observabilidade |
| … | *(manual)* Configuração externa | O que só uma pessoa faz: contas, credenciais, cadastros |
| … | *(manual)* Integração/virada | Ligar consumidores existentes, cutover, rollback, desligar o antigo |
| … | Prompt de arranque | O que colar na primeira sessão |

**Variações por tipo de sistema:**

- **Só API/serviço:** sem os prompts de interface; o contrato ganha mais peso e os testes de
  compatibilidade viram obrigatórios.
- **Painel sobre dados existentes:** fundação → leitura do schema existente → API interna →
  interface; sem prompt de dados.
- **Integração entre sistemas prontos:** fundação → contratos dos dois lados (referência) →
  tradução/roteamento → reprocessamento e conciliação → manuais de virada.
- **Processamento de dados em lote:** fundação → modelo → ingestão → transformação → publicação →
  qualidade/reconciliação → agendamento.
- **Biblioteca/CLI:** fundação → API pública da biblioteca (referência) → núcleo → comandos →
  documentação e publicação.

O prompt de fundação é o único lugar onde o arcabouço de teste pode nascer. Se ele sair sem medição
de cobertura, sem o comando único de verificação e sem o CI quebrando abaixo do piso, nenhum prompt
seguinte vai instalar isso por conta própria — e o conjunto inteiro perde a garantia que o
diferencia.

## Documentos de referência à parte

Crie um documento de contrato separado quando a mesma especificação é lida por três ou mais prompts
(a API pública lida por quem implementa, por quem recebe webhook e por quem testa, por exemplo).
Repetir contrato dentro dos prompts garante que as cópias divirjam.

Um contrato traz, campo a campo: autenticação, convenções, erros com código e HTTP, cada operação
com tabela de campos (nome, tipo, obrigatório, regra), exemplo real de requisição e resposta,
callbacks, e a regra de versionamento (o que é aditivo e o que exige versão nova).

## Manuais humanos

Tudo que exige gente vira manual, nunca prompt: criar conta em serviço de terceiro, pedir aprovação,
obter credencial, virar tráfego de produção, restaurar backup. O prompt de arranque precisa dizer à
IA que esses arquivos **não são para executar** — só avisar quando chegar a hora deles.

Um manual bom tem pré-requisitos, passos numerados com o que se vê na tela, o que copiar para onde,
como conferir que deu certo e uma seção de problemas comuns.

## O índice (`README.md`)

Modelo em `assets/README_indice.md` — grave-o como `README.md` na pasta de saída.

É a primeira coisa que qualquer leitor abre. Precisa ter:

1. Uma abertura de três linhas: o que é o sistema e o que esta pasta é.
2. **Tabela de decisões fechadas** — tema e decisão, sem motivo (o motivo está no 00). Serve para o
   usuário reconferir num relance se o plano é o que ele pediu.
3. **Como usar:** copiar a pasta para o repositório, uma sessão por prompt, o que fazer ao fim de
   cada sessão (critérios de aceite, verificação, revisão, commit), e a regra de que a documentação
   oficial vence a especificação, com a divergência virando ADR.
4. **Tabela do índice:** arquivo, tipo, depende de, entrega. Uma linha por arquivo, em ordem.
5. O que pode ser feito em paralelo, quando houver.
6. Onde este sistema toca outros sistemas, se tocar.

## Numeração

Numere na ordem de execução, com dois dígitos, e mantenha referências e manuais na mesma sequência
(a posição deles indica quando são lidos). Não renumere depois de a obra começar: um documento novo
entra como `07a` ou no fim. O nome do arquivo descreve a entrega, não a camada abstrata:
`08_prompt_webhook_meta.md`, não `08_prompt_modulo_3.md`.

## Continuidade entre sessões

O conjunto precisa de um mecanismo de retomada, porque nenhuma sessão vê a anterior:

- **`ESTADO.md` na raiz do repositório** (criado pelo prompt de arranque): uma linha por prompt, com
  situação, mensagem de commit, hash, suíte/cobertura e observações, e as regras de abertura e
  fechamento de sessão escritas no próprio corpo do arquivo. É o que a sessão seguinte lê primeiro, e
  o protocolo inteiro — incluindo como reconciliar com o git quando ele estiver desatualizado — está
  em `continuidade-entre-sessoes.md`. Escrever a tabela sem o protocolo não resolve: o arquivo só
  funciona se toda sessão for obrigada a abrir e fechar nele.
- **`CLAUDE.md` do projeto** (criado pelo prompt de fundação): comandos, estrutura, invariantes,
  convenções e o que não fazer. Escreva o conteúdo dele **literalmente** dentro do prompt de
  fundação — é o resumo que toda sessão futura carrega, e deixá-lo a cargo da IA é perder o controle
  da parte mais reutilizada da documentação.
- **`decisoes/`** com o modelo de ADR: onde a IA registra divergência entre a especificação e a
  realidade encontrada (versão de biblioteca, mudança na API de terceiro). Sem esse lugar, a
  divergência vira comentário perdido no meio de um commit.


---


<!-- ═══ references/documento-00.md ═══ -->

# ARQUIVO: references/documento-00.md

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


---


<!-- ═══ references/continuidade-entre-sessoes.md ═══ -->

# ARQUIVO: references/continuidade-entre-sessoes.md

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


---


<!-- ═══ references/testes.md ═══ -->

# ARQUIVO: references/testes.md

# Testes: a espinha dorsal da especificação

Esta é a parte que separa um planejamento útil de um documento bonito. Quem executa a obra é uma IA
numa sessão sem memória, e ela tem uma tendência forte a **declarar pronto**. Teste escrito depois
nasce viciado: ele é desenhado para passar no código que acabou de sair, e por isso confirma o que o
código faz em vez de verificar o que o sistema deveria fazer. O teste escrito **antes** é a única
coisa que a IA não consegue enganar sem perceber que está enganando.

Por isso a especificação não "inclui testes": ela é escrita **a partir** deles. Os cenários da seção
de testes de cada prompt são a tradução executável dos critérios de aceite, e a ordem de trabalho da
sessão é escrever esses cenários primeiro.

## O ciclo, por bloco

Bloco = uma seção numerada do prompt (uma tabela, um endpoint, um worker, uma tela). Não é o prompt
inteiro: o ciclo curto é o que faz a regressão aparecer perto da causa, enquanto ainda é barata.

Todo prompt manda a sessão repetir isto em cada bloco:

1. **Linha de base.** Rodar a suíte **inteira** antes de tocar em qualquer coisa e anotar o
   resultado. Suíte já vermelha → parar e avisar; construir sobre vermelho é construir no escuro,
   porque daí em diante ninguém sabe qual falha é nova.
2. **Vermelho.** Escrever os testes do bloco, tirados da seção de testes do prompt, e vê-los falhar
   — **conferindo a mensagem de falha**. Um teste que falha pelo motivo errado (import quebrado,
   fixture ausente) não é vermelho: é teste quebrado. E um teste que **passa** antes da implementação
   não testa nada e precisa ser reescrito na hora.
3. **Verde.** Implementar o mínimo que faz aqueles testes passarem. Não adiantar o bloco seguinte.
4. **Regressão.** Rodar a suíte inteira de novo. Verde igual ou melhor que a linha de base é a única
   condição para seguir.
5. **Refatorar** com a suíte verde e rodar mais uma vez.
6. Próximo bloco.

Ao fim do prompt: suíte inteira verde, cobertura no piso combinado, nenhum teste pulado, e só então
o commit. **Nunca fechar um prompt com a suíte vermelha** — o prompt seguinte perde a linha de base
e o erro viaja para dentro de outra camada.

## Regressão: o que é inegociável

Um teste existente que passa a falhar é uma de duas coisas, e a sessão precisa dizer qual:

- **Quebra acidental** → conserta o código. Nunca o teste.
- **Mudança intencional prevista na especificação** → atualiza o teste, cita no commit qual decisão
  autoriza a mudança e registra em `decisoes/` se a especificação não previa exatamente aquilo.

O que a especificação proíbe, com todas as letras, porque é o atalho que toda IA encontra sozinha
quando está encurralada: pular teste (`skip`, `only`, comentar), afrouxar asserção para caber no
resultado observado, apagar caso de teste, baixar o piso de cobertura, ou trocar a asserção pelo que
o código devolveu. Se o teste está errado, isso se justifica em uma frase no commit; se não está, o
código é que cede.

**Correção de bug entra sempre em duas etapas:** primeiro o teste que reproduz o bug e falha, depois
a correção. Bug sem teste de reprodução volta — e volta sem ninguém perceber.

## Cobertura

Cobertura alta não prova que o sistema funciona; cobertura baixa prova que não se sabe se funciona.
Trate como piso, não como meta:

- **Piso global:** 80% de linhas e de ramos, medido no CI, quebrando o build abaixo disso.
- **Piso alto (90 a 95%) no que dói:** regra de negócio, idempotência, dinheiro, permissão, cifragem,
  classificação de erro de terceiro, transição de estado. Diga na especificação **quais módulos** são
  esses; sem nome, ninguém aplica.
- **Fora da conta:** código gerado, migrations, arquivos de configuração, o dublê de teste.
- **O piso nunca desce para o build passar.** Ou sobe o teste, ou a exceção vira ADR com prazo.

E deixe escrito o que cobertura não mede, porque é onde mora o dano: cenário que ninguém pensou,
concorrência, ordem de eventos, falha do serviço externo. Cobertura é o piso; **cenário é o teto**.

## Níveis e o que cada um protege

| Nível | Protege de | Onde usar |
|---|---|---|
| **Unidade** | Regra de negócio implementada errado | Funções puras: validação, cálculo, construção de payload, classificação de erro |
| **Integração** | Banco, fila e transação mentirem | Tudo que grava: com banco e fila **de verdade** em container, não em memória falsa |
| **Contrato** | Quebrar quem já consome | Congela requisição e resposta de cada operação pública, campo a campo |
| **Ponta a ponta** | A interface não ligar nos dados | Os três ou quatro fluxos que o usuário realmente faz |
| **Carga leve** | Limite de vazão e concorrência | Só quando houver limite externo ou pico conhecido |

A proporção saudável é muita unidade, integração farta no que grava, contrato para toda superfície
pública e E2E só nos fluxos principais — E2E é caro, lento e instável; usar E2E para cobrir regra de
negócio é trocar teste bom por teste caro.

## Como se testa o mundo externo

Serviço de terceiro **sempre** entra como dublê controlável, nunca credencial real — e o dublê é
entrega de um prompt, com nome e lugar definidos. Ele precisa saber simular, porque é isso que o
código de produção vai encontrar:

- resposta de sucesso normal;
- erro permanente (não adianta retentar) e erro transitório (adianta);
- limite de taxa estourado;
- credencial inválida/expirada;
- resposta fora do formato esperado;
- lentidão maior que o tempo limite — **inclusive o caso em que a operação aconteceu do outro lado e
  a resposta se perdeu**, que é o que causa cobrança dobrada e mensagem duplicada.

## Determinismo

Teste que falha uma vez a cada vinte ensina a equipe a ignorar teste vermelho, e aí a suíte inteira
para de valer. A especificação exige: tempo e aleatoriedade controlados (relógio injetado, semente
fixa), banco limpo entre testes com fábricas de dados, nenhuma espera por tempo fixo (espera-se pela
condição), e testes independentes da ordem em que rodam.

## Cenários que todo prompt precisa cobrir

Além do caminho feliz e de cada erro previsto, com código e mensagem exatos:

- **Repetição** — a mesma operação duas vezes: mesma resposta, um efeito só.
- **Concorrência** — N operações simultâneas sobre o mesmo alvo: um vencedor, sem duplicata.
- **Fronteira** — vazio, um, o máximo, o máximo mais um.
- **Isolamento** — dado de outro dono nunca aparece nem pode ser alterado.
- **Falha externa** — fora do ar, tempo esgotado, resposta inesperada, incerteza.
- **Ordem** — evento que chega adiantado ou atrasado não sobrescreve estado mais avançado.
- **Invariantes do documento 00** — cada um vira pelo menos um teste, nomeado com o número dele.

## Em repositório que já existe

A rede de proteção vem **antes** da primeira alteração: testes que descrevem o comportamento atual
da área afetada, inclusive o que parece errado (comportamento esquisito que alguém depende é
requisito, não bug — até alguém decidir o contrário). Sem essa rede, "não quebrei nada" é opinião.

Se a suíte existente já estiver vermelha ou for lenta demais para rodar a cada bloco, isso é achado
de planejamento: registre, e defina o subconjunto que roda a cada bloco (a área afetada) e a suíte
inteira que roda ao fim de cada prompt.

## O que isso vira nos documentos

- **Documento 00:** uma seção de estratégia de testes (níveis, pisos de cobertura, módulos de piso
  alto, dublês, determinismo) e pelo menos dois invariantes — suíte verde e nenhum teste pulado no
  commit; bug corrigido só com teste de reprodução.
- **Prompt de fundação:** o arcabouço de teste, o comando único de verificação, a medição de
  cobertura com o piso já configurado e o CI quebrando abaixo dele. Isso vem **antes** de qualquer
  regra de negócio, senão nunca vem.
- **Cada prompt:** a seção "Ordem de trabalho" com o ciclo acima, os cenários organizados por bloco
  (para a sessão saber quais escrever primeiro) e critérios de aceite exigindo suíte inteira verde,
  piso de cobertura e zero testes pulados.
- **Prompt de arranque:** a proibição de fechar sessão no vermelho e a regra de parar e avisar
  quando a linha de base já estiver quebrada.


---


<!-- ═══ references/anatomia-do-prompt.md ═══ -->

# ARQUIVO: references/anatomia-do-prompt.md

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


---


<!-- ═══ references/sistema-existente.md ═══ -->

# ARQUIVO: references/sistema-existente.md

# Planejar dentro de um repositório que já existe

Aqui o risco muda de lugar. Em projeto novo, o perigo é a especificação ser vaga; em projeto
existente, o perigo é ela **contradizer a realidade** — propor uma tabela que já existe com outro
nome, um padrão que o projeto abandonou, uma biblioteca que foi trocada. Uma especificação que briga
com o código é pior que nenhuma, porque a IA construtora obedece a ela e quebra o que funcionava.

## Antes de perguntar qualquer coisa: leia

Leia o repositório e chegue na entrevista com afirmações a confirmar, não com perguntas de
formulário. Levante:

- `README.md`, `CLAUDE.md`, `docs/`, ADRs — o que o projeto diz de si.
- Gerenciador de pacotes, versões, scripts de build, teste e execução.
- Estrutura de pastas e o padrão de organização (por camada, por funcionalidade, por domínio).
- Modelo de dados: migrations, schema, convenção de nome de tabela e coluna.
- Um módulo recente e completo — é o melhor retrato do padrão vigente, melhor que a documentação.
- Autenticação, autorização, tratamento de erro, log, configuração: como já são feitos.
- Testes: o que existe, onde ficam, como rodam, o que se usa no lugar de serviços externos.
- Histórico recente (`git log`): o que anda mudando e o que ninguém toca.

Anote o que você **não** conseguiu descobrir; isso vira pergunta com prioridade.

## O que muda na entrevista

Acrescente aos blocos de `entrevista.md`:

- O que já existe e resolve parte do problema? O novo módulo estende, substitui ou convive?
- O que **não pode quebrar** de jeito nenhum? (consumidores em produção, integrações, relatórios,
  jobs) Isso vira invariante, e normalmente vira também um prompt de testes de não-regressão.
- Há dívida conhecida nessa área que vale arrumar junto, ou passamos ao largo? Decida explicitamente:
  refatoração que aparece no meio da obra sem ter sido combinada é a maior fonte de atraso.
- Precisa de migração de dados? Quem faz, com que janela, e como se volta atrás.
- Há bandeira de funcionalidade (feature flag) ou o módulo nasce ligado?
- Quem revisa e como o código entra: branch, PR, aprovação.

## O que muda no documento 00

Continua sendo o contrato entre os prompts, mas ganha duas seções e perde peso nas outras:

- **§ O que já existe** — mapa curto do estado atual da área afetada: arquivos, tabelas, endpoints,
  jobs, com uma linha do que cada um faz hoje. É o que impede a IA de recriar o que já está lá.
- **§ O que muda e o que não muda** — tabela com três colunas: item | hoje | depois. Inclua as linhas
  "não muda" que alguém poderia achar que mudam.
- **Convenções** deixam de ser escolha e viram **observação**: "o projeto usa X; siga X mesmo que
  você prefira Y". Se algo precisa mesmo mudar, é decisão numerada com motivo, e o novo padrão vale
  só dali para frente, dito assim com todas as letras.

## O que muda nos prompts

- **Inventário no começo.** Cada prompt lista os arquivos que vai criar **e** os que vai alterar,
  dizendo o que muda em cada um. Editar um arquivo existente sem isso é como a especificação apaga
  comportamento por acidente.
- **Prompt de fundação vira prompt de reconhecimento.** Em vez de criar o repositório, a primeira
  sessão confirma que o ambiente sobe, os testes passam antes de qualquer mudança (a linha de base
  importa: sem ela ninguém sabe se a suíte já estava vermelha), e registra o estado num ADR.
- **Cada prompt termina com a suíte existente verde**, não só com os testes novos. Ponha isso nos
  critérios de aceite, explicitamente.
- **Compatibilidade como invariante.** Se há consumidor em produção, o contrato atual é lei: só
  acréscimo. Vale a pena um prompt só de testes que congelam o comportamento atual **antes** de
  mexer — é o que transforma "acho que não quebrei" em "sei que não quebrei".
- **Reversão.** Para mudança arriscada, o prompt diz como desfazer: bandeira, migração reversível,
  ordem de deploy.

## Ordem que costuma funcionar

| # | Prompt | Entrega |
|---|---|---|
| 00 | *(referência)* Visão geral, o que existe, o que muda | Contrato entre os prompts |
| 01 | Reconhecimento e linha de base | Ambiente sobe, suíte verde registrada, ADR do estado atual |
| 02 | Rede de proteção | Testes que congelam o comportamento atual da área afetada |
| 03 | Dados | Migrations novas, compatíveis com o que já está gravado |
| 04+ | Funcionalidade | Um prompt por fluxo, cada um com inventário de arquivos alterados |
| … | Integração com o que existe | Ligar o módulo novo aos pontos de entrada atuais |
| … | Migração e virada | Script de migração, bandeira, ordem de deploy, rollback |
| … | *(manual)* Operação | O que uma pessoa faz na virada e depois dela |


---


<!-- ═══ references/qualidade.md ═══ -->

# ARQUIVO: references/qualidade.md

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


---


<!-- ═══ assets/00_visao_geral_e_decisoes.md ═══ -->

# ARQUIVO: assets/00_visao_geral_e_decisoes.md

# 00 — Visão geral, decisões e invariantes do <Sistema>

> **Tipo:** referência. Não é um prompt para executar. Todos os prompts pressupõem que este
> arquivo foi lido.

---

## 1. O que é o <Sistema>

<Dois a cinco parágrafos: o que é, para quem, e o que cada público obtém dele.>

- **Para <ator A>:** <o que ele ganha>
- **Para <ator B>:** <o que ele ganha>

### 1.1 Fora de escopo (não construir)

- <Funcionalidade que não existe> — <quem faz isso em vez do sistema, ou por que não existe>
- <Funcionalidade quase-escopo que um implementador construiria sozinho>

---

## 2. Atores

| Ator | Como interage |
|---|---|
| **<Ator>** | <por onde entra, como se autentica, o que faz> |

---

## 3. Arquitetura

```
<diagrama em texto: processos, entradas, dependências, onde os dados ficam>
```

**Princípio central:** <a regra que decide empates na hora de implementar>.

---

## 4. Glossário

| Termo | Significado |
|---|---|
| **<termo>** | <significado, com o formato real quando for identificador externo> |

---

## 5. Decisões

| # | Decisão | Motivo |
|---|---|---|
| D1 | <frase afirmativa no presente> | <uma linha> |

### 5.1 Decisões tomadas por padrão

<As que o usuário não opinou e você propôs; ficam aqui para serem fáceis de derrubar.>

### 5.2 Decisões pendentes

| Pendência | O que bloqueia | Quem decide | Enquanto isso |
|---|---|---|---|
| <o que falta decidir> | <prompt/funcionalidade parada> | <pessoa/área> | <o que fazer até lá> |

---

## 6. Stack

Use a **versão estável mais recente** de cada item no momento da instalação e fixe no lockfile. As
versões abaixo são o mínimo esperado. O que for instalado acima disso vai para `decisoes/`.

| Camada | Tecnologia |
|---|---|
| <camada> | <tecnologia e versão mínima> |

---

## 7. Convenções

| Tema | Regra |
|---|---|
| Idioma | <documentação, interface, logs, mensagens de erro> |
| Nomes no código | <idioma e caixa> |
| Banco | <idioma e caixa; exceções> |
| <API> | <idioma, caixa e por quê> |
| IDs | <tipo, quem gera, ordenável?> |
| Datas | <tipo no banco, formato na API, fuso na exibição> |
| Erros | <formato por superfície> |
| Paginação | <formato> |
| Exclusão | <o que se apaga de fato e o que muda de status> |

---

## 8. Invariantes (nunca quebrar)

1. <regra verificável>
2. <regra verificável>

---

## 9. Estratégia de testes

**Método:** ciclo vermelho-verde por bloco. Em cada bloco de cada prompt: suíte completa como linha
de base → testes do bloco escritos e falhando pelo motivo certo → implementação mínima → testes do
bloco verdes → suíte completa verde de novo → refatoração com a suíte verde. Nunca se fecha uma
sessão, nem se faz commit, com a suíte vermelha.

| Nível | Cobre | Onde fica | Comando |
|---|---|---|---|
| Unidade | <regras puras> | `<caminho>` | `<comando>` |
| Integração | <o que grava, com banco e fila reais> | `<caminho>` | `<comando>` |
| Contrato | <superfícies públicas> | `<caminho>` | `<comando>` |
| Ponta a ponta | <fluxos principais> | `<caminho>` | `<comando>` |

**Verificação completa:** `<comando único>` (roda <o que roda>).

**Cobertura:** piso global de <X>% de linhas e ramos, medido no CI e quebrando o build abaixo disso.
Piso de <Y>% em: `<módulo>`, `<módulo>` — <por que são críticos>. Fora da conta: código gerado,
migrations, configuração e dublês. **O piso não desce para o build passar**: ou sobe o teste, ou a
exceção vira ADR com prazo.

**Dublês:** `<serviço externo>` é substituído por `<dublê, com caminho>`, que simula sucesso, erro
permanente, erro transitório, limite de taxa, credencial inválida, resposta fora do formato e
lentidão maior que o tempo limite (inclusive com a operação tendo acontecido do outro lado).
Credencial real em teste, nunca.

**Determinismo:** relógio injetado, semente fixa, banco limpo entre testes por fábricas, espera por
condição e não por tempo fixo, testes independentes da ordem.

**Proibido:** pular teste (`skip`/`only`), afrouxar asserção para caber no resultado observado,
apagar caso de teste, baixar o piso de cobertura. Teste antigo que falha → conserta-se o código;
alterá-lo exige decisão desta especificação citada no commit.

---

## 10. Limites e fatos externos

**Conferido na documentação oficial de <serviço> em <AAAA-MM-DD>.** Reconferir antes de implementar;
as constantes ficam em `<caminho do arquivo de constantes>`. Se a documentação oficial divergir
desta tabela, **a documentação oficial vence**: siga-a e registre em `decisoes/`.

| Item | Limite | Conferido |
|---|---|---|
| <item> | <limite> | <sim/não> |

<Mudanças com data conhecida: preço, versão, regra que entra em vigor.>

---

## 11. Mapa dos documentos

Ver `README.md` desta pasta.


---


<!-- ═══ assets/README_indice.md ═══ -->

# ARQUIVO: assets/README_indice.md

# <Sistema>: especificação e prompts de construção

Esta pasta contém **tudo** o que é preciso para construir o **<Sistema>** <num repositório novo /
dentro do repositório `<repo>`>: <uma frase sobre o que o sistema é>.

Cada arquivo é autossuficiente ou aponta para outro arquivo **desta mesma pasta**.

---

## Decisões fechadas

| Tema | Decisão |
|---|---|
| <tema> | <decisão, sem o motivo — o motivo está no 00> |
| Testes | TDD por bloco; suíte completa verde antes e depois de cada bloco; piso de cobertura de <X>% global e <Y>% nos módulos críticos, verificado no CI |

---

## Como usar

1. <Criar/clonar o repositório.>
2. Copiar **esta pasta inteira** para `docs/especificacao/` dentro do repositório. Os prompts se
   referenciam por esse caminho.
3. Abrir a IA construtora na raiz do repositório.
4. Para cada prompt, **em ordem**, numa sessão nova:

   > Leia `CLAUDE.md` (se existir) e `docs/especificacao/NN_nome_do_arquivo.md` e execute o prompt.
   > Siga os critérios de aceite do final do arquivo.

5. Dentro de cada sessão, o trabalho é bloco a bloco, em ciclo vermelho-verde: suíte completa como
   linha de base, testes do bloco escritos **antes** da implementação, implementação, testes do
   bloco verdes, suíte completa verde de novo. A "Ordem de trabalho" de cada prompt traz o ciclo.
6. No fim de cada sessão: conferir os critérios de aceite, rodar `<comando de verificação>` (suíte
   inteira verde e cobertura no piso, sem teste pulado), pedir `/code-review` (e `/security-review`
   nos prompts marcados) e fazer o commit indicado.
7. Se algo desta especificação conflitar com a documentação oficial da versão instalada de uma
   biblioteca ou de um serviço externo, **a documentação oficial vence**. Registre a divergência em
   `docs/decisoes/` e siga.

---

## Índice

| Arquivo | Tipo | Depende de | Entrega |
|---|---|---|---|
| [00_visao_geral_e_decisoes.md](00_visao_geral_e_decisoes.md) | Referência | — | <o que traz> |
| [01_prompt_<nome>.md](01_prompt_<nome>.md) | Prompt | 00 | <o que entrega> |
| [NN_manual_<nome>.md](NN_manual_<nome>.md) | Manual (humano) | — | <o que orienta> |

<O que pode ser feito em paralelo, se houver.>

---

## Onde este plano toca outros sistemas

<Dependências externas, consumidores, riscos de infraestrutura compartilhada — em uma ou duas frases
honestas.>


---


<!-- ═══ assets/NN_prompt.md ═══ -->

# ARQUIVO: assets/NN_prompt.md

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


---


<!-- ═══ assets/NN_contrato.md ═══ -->

# ARQUIVO: assets/NN_contrato.md

# NN — Contrato <nome> (<superfície>)

> **Tipo:** referência. Não é um prompt para executar. Lido pelos prompts <lista>.

---

## 1. Compatibilidade

<Com quem precisa ser compatível, o que é lei, o que pode crescer.>

## 2. Autenticação

<Como o chamador se identifica; o que acontece quando falha.>

## 3. Convenções

<Idioma e caixa dos campos, formato de data, identificadores, tamanho máximo do corpo.>

### 3.1 Idempotência

<Como se identifica repetição, o que se devolve na segunda chamada igual e na segunda com o mesmo
identificador e corpo diferente.>

## 4. Erros

| Código | HTTP | Quando acontece |
|---|---|---|
| `<codigo_snake_case>` | <HTTP> | <situação> |

Formato do corpo de erro:

```json
{ "error": "<codigo>", "errors": ["<mensagem legível>"] }
```

## 5. Operações

### 5.1 `<MÉTODO> <caminho>` — <o que faz>

| Campo | Tipo | Obrigatório | Regras |
|---|---|---|---|
| | | | |

Exemplo:

```json
<requisição real>

<status>
<resposta real>
```

Efeitos: <o que grava, o que enfileira, o que notifica>.

## 6. Callbacks / eventos de saída

<Regras comuns: assinatura, ordem, retentativa, o que nunca regride.> Corpo de cada tipo, com
exemplo.

## 7. Ciclo de vida

<Estados e transições possíveis, de ponta a ponta.>

## 8. Versionamento

<O que é aditivo e pode entrar a qualquer momento; o que exige versão nova.>


---


<!-- ═══ assets/NN_manual.md ═══ -->

# ARQUIVO: assets/NN_manual.md

# NN — Manual: <o que a pessoa vai fazer>

> **Tipo:** manual para uma pessoa. A IA construtora **não executa** este arquivo — só avisa quando
> chegar a hora dele.

---

## Visão geral da ordem

<Lista curta dos passos, para a pessoa saber onde está entrando e quanto tempo leva.>

## 1. Pré-requisitos

- <acesso, conta, permissão, informação que precisa estar em mãos>

## 2. <Passo>

1. <ação concreta, com o que se vê na tela>
2. <o que copiar e para onde>

**Como conferir que deu certo:** <o sinal observável>.

## N. Problemas comuns

| Sintoma | Causa provável | O que fazer |
|---|---|---|
| | | |


---


<!-- ═══ assets/NN_prompt_inicial_execucao.md ═══ -->

# ARQUIVO: assets/NN_prompt_inicial_execucao.md

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


---


<!-- ═══ assets/ESTADO.md ═══ -->

# ARQUIVO: assets/ESTADO.md

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


---


<!-- ═══ assets/decisoes/0000-modelo.md ═══ -->

# ARQUIVO: assets/decisoes/0000-modelo.md

# NNNN — Título curto da decisão

- **Data:** AAAA-MM-DD
- **Situação:** proposta | aceita | substituída por [NNNN](NNNN-titulo.md) | revogada

## Contexto

O que motivou a decisão: o problema, a restrição, o conflito entre a especificação e a documentação
oficial de uma biblioteca ou de um serviço externo. Fatos, não opiniões.

## Decisão

O que foi decidido, na voz ativa e no presente: "o sistema usa…", "o campo X passa a…".

## Alternativas consideradas

| Alternativa | Por que não |
|---|---|
| … | … |

## Consequências

O que passa a ser verdade depois da decisão — o bom e o ruim. Inclua o que precisa ser revisto mais
tarde e o que os outros prompts da especificação precisam saber.


---
