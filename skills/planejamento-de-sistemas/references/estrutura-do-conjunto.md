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
