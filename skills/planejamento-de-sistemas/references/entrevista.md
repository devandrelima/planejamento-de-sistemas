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
