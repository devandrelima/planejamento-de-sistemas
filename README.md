# Planejamento de sistemas

Uma skill de IA que transforma uma ideia de sistema numa **especificação executável**: uma pasta de
documentos que você entrega a uma IA construtora (Claude Code, Cursor, o que for) para o sistema
sair de pé, sem ela precisar adivinhar nada nem ter visto a conversa original.

O critério de qualidade é este: **duas sessões diferentes, lendo só essa pasta, constroem a mesma
coisa.**

## O que ela faz

1. **Entrevista você em blocos** — produto, atores, escopo, dados, integrações, contratos,
   interface, requisitos não-funcionais, stack, operação, riscos —, propondo padrões em vez de
   exigir que você redija requisitos do zero, e adaptando as perguntas às respostas anteriores.
2. **Fecha as decisões** e devolve um resumo para você confirmar antes de escrever qualquer coisa.
3. **Escreve o conjunto de documentos:**

```
docs/especificacao/
├── README.md                      índice: tipo, dependências e entrega de cada arquivo
├── 00_visao_geral_e_decisoes.md   escopo, atores, arquitetura, glossário, decisões numeradas,
│                                  stack, convenções, invariantes, estratégia de testes, limites
├── 01..NN_prompt_*.md             prompts executáveis, um por sessão, em ordem de dependência
├── NN_contrato_*.md               contratos de API/eventos, campo a campo
├── NN_manual_*.md                 manuais para pessoas (cadastros externos, cutover, operação)
└── NN_prompt_inicial_execucao.md  o que colar na primeira sessão da IA construtora
docs/decisoes/0000-modelo.md       modelo de ADR para registrar divergências durante a obra
ESTADO.md                          memória entre sessões
```

Serve tanto para sistema novo do zero quanto para funcionalidade grande dentro de um repositório que
já existe — nesse caso ela lê o código antes de perguntar, e monta uma rede de proteção de testes
antes de deixar qualquer coisa ser alterada.

## O que a diferencia

**Testes primeiro, sempre.** A especificação não "inclui testes": ela nasce deles. Cada prompt traz
uma seção "Ordem de trabalho" com ciclo vermelho-verde **por bloco** — suíte inteira verde como
linha de base → testes do bloco falhando pelo motivo certo → implementação mínima → testes do bloco
verdes → suíte inteira verde de novo. Teste escrito depois confirma o que o código faz; teste
escrito antes verifica o que o sistema deveria fazer, e é a única coisa que uma IA construtora não
consegue declarar pronta sem ser desmentida. Os critérios de aceite exigem a suíte **inteira** verde
(não só os testes novos), piso de cobertura e zero testes pulados.

**Continuidade entre sessões.** Como cada prompt roda numa sessão sem memória, todo prompt abre e
fecha no `ESTADO.md`. Na abertura, confere se os anteriores realmente terminaram — e quando o
arquivo está desatualizado (sessão que travou, contexto que acabou), reconcilia com o histórico do
git: commit encontrado + entregas presentes + suíte verde → marca concluído e segue; entrega parcial
→ termina o anterior antes; nada encontrado → para e avisa. O `ESTADO.md` entra no **mesmo commit**
do trabalho, então "o commit existe" e "o estado está atualizado" são o mesmo fato.

## Como usar

### Claude Code — como plugin (recomendado)

```
/plugin marketplace add devandrelima/planejamento-de-sistemas
/plugin install planejamento-de-sistemas
```

Depois é só dizer o que quer planejar; ela dispara sozinha, ou você chama por
`/planejamento-de-sistemas`. Atualiza com `/plugin marketplace update`.

### Claude Code — como skill local

```bash
git clone https://github.com/devandrelima/planejamento-de-sistemas.git
ln -s "$PWD/planejamento-de-sistemas/skills/planejamento-de-sistemas" ~/.claude/skills/
```

### Claude.ai e Claude Desktop

Baixe [`dist/planejamento-de-sistemas.skill`](dist/planejamento-de-sistemas.skill) e envie em
Configurações → Capacidades → Skills. (É um zip comum; se a interface pedir `.zip`, renomeie.)

### ChatGPT, Gemini, Cursor e outras

Use a versão de arquivo único —
[`dist/planejamento-de-sistemas-completo.md`](dist/planejamento-de-sistemas-completo.md), com os 17
arquivos concatenados na ordem de leitura:

- **ChatGPT Projects / Gemini Gems / Claude Projects:** anexe o arquivo à base de conhecimento e
  ponha na instrução: *"Siga PLANEJAMENTO. Comece pela Fase 1 (entrevista), uma rodada de perguntas
  por vez."*
- **Cursor / Windsurf / Cline:** salve como regra do projeto (`.cursor/rules/planejamento.md`) e
  chame por `@planejamento`.
- **Por link:** mande a URL raw e peça para ela ler o arquivo inteiro antes de começar:

  ```
  https://raw.githubusercontent.com/devandrelima/planejamento-de-sistemas/main/dist/planejamento-de-sistemas-completo.md
  ```

  Funciona, com uma ressalva: a IA busca o conteúdo uma vez e pode truncar ou resumir. Anexar o
  arquivo é mais confiável que mandar o link.
- **Contexto apertado:** cole só o `SKILL.md` (~160 linhas) e vá colando a referência de cada fase
  quando chegar nela — é o que o Claude Code faz sozinho com divulgação progressiva.

## Estrutura do repositório

| Caminho | O que é |
|---|---|
| `skills/planejamento-de-sistemas/SKILL.md` | O fluxo em 4 fases, os princípios e as regras |
| `skills/planejamento-de-sistemas/references/` | Entrevista, estrutura do conjunto, documento 00, continuidade entre sessões, testes, anatomia do prompt, sistema existente, checklist de revisão |
| `skills/planejamento-de-sistemas/assets/` | Modelos prontos de cada tipo de documento |
| `dist/` | Artefatos gerados: pacote `.skill` e versão de arquivo único |
| `build.sh` | Regera `dist/` (roda sozinho no CI a cada push em `skills/`) |

## Licença

MIT.
