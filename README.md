# Planejamento de Sistemas 2.0

Skill de IA para transformar uma ideia de software em um plano de construção com entregas frequentes, contexto enxuto e validação verificável.

**Fluxo:** Projeto → Sprint → Prompt-mapa → Task.

O humano recebe os prompts como mapas de trabalho; os agentes executam tasks com dependências explícitas, arquivos permitidos, contexto selecionado, testes e critérios de aceite. Cada sprint produz uma versão que o usuário pode executar e avaliar, e a próxima fica bloqueada até aprovação explícita.

## O que oferece

- **Entregas incrementais:** sprints com 1 a 3 prompts-mapa, preferencialmente 2, e tasks pequenas para execução especializada.
- **Memória seletiva:** contexto global mínimo e arquivos por domínio/task, com SHA-256 e orçamento estimado de tokens.
- **Testes progressivos:** testes locais durante cada task; regressão dos fluxos afetados ao fim da sprint; suíte completa a cada 3 sprints, na entrega final ou antes quando o risco exigir.
- **Cobertura exigida:** >=80% no código novo/alterado por sprint e >=80% global nos checkpoints, sempre medida por ferramenta adequada ao projeto.
- **Design adaptativo:** briefing visual, escolha contextual das skills disponíveis e revisão de usabilidade e acessibilidade.
- **Paralelismo controlado:** elegibilidade por dependências e detecção de colisão direta nos arquivos de escrita, com integração serial.
- **Avaliação humana:** a conclusão técnica da sprint não equivale a aprovação do usuário.

## Como experimentar

O exemplo [login incremental](examples/fluxo-v2/README.md) contém um planejamento com uma sprint, dois prompts e quatro tasks. Demonstra a **metodologia**, não um aplicativo de login pronto.

    git clone https://github.com/devandrelima/planejamento-de-sistemas.git
    cd planejamento-de-sistemas
    python3 -m unittest discover -s tests -v
    python3 skills/planejamento-de-sistemas/scripts/fluxo.py --repo examples/fluxo-v2 validar
    python3 skills/planejamento-de-sistemas/scripts/fluxo.py --repo examples/fluxo-v2 prontas
    python3 skills/planejamento-de-sistemas/scripts/fluxo.py --repo examples/fluxo-v2 contexto S01-P01-T01
    ./build.sh

O comando contexto entrega o pacote de execução apenas da task autorizada. Para adicionar tasks a um plano já em andamento, use o subcomando sincronizar; ele preserva evidências previamente registradas e impede remoções silenciosas de tasks.

A CLI exige apenas Python 3.10+ e utiliza manifestos JSON, sem bibliotecas adicionais. Para uso em outro repositório, mantenha o script disponível e passe o diretório do aplicativo com --repo.

## Instalação da skill

### Claude Code (plugin)

    /plugin marketplace add devandrelima/planejamento-de-sistemas
    /plugin install planejamento-de-sistemas

### Skill local

    git clone https://github.com/devandrelima/planejamento-de-sistemas.git
    ln -s "$PWD/planejamento-de-sistemas/skills/planejamento-de-sistemas" ~/.claude/skills/

### Outras ferramentas

Use o [pacote da skill](dist/planejamento-de-sistemas.skill) em aplicações que aceitem skills ZIP, ou o [documento único](dist/planejamento-de-sistemas-completo.md) como instruções anexadas a projetos do ChatGPT, Gemini, Cursor e ferramentas similares. Os comandos de execução dependem de acesso local a Python e aos arquivos do projeto.

## Estrutura

| Caminho | Conteúdo |
|---|---|
| skills/planejamento-de-sistemas/SKILL.md | Instruções principais |
| skills/planejamento-de-sistemas/references/ | Descoberta, planejamento, contexto, testes, design e paralelismo |
| skills/planejamento-de-sistemas/assets/v2/ | Modelos de visão geral, sprints, mapas, tasks, memória e estado |
| skills/planejamento-de-sistemas/scripts/fluxo.py | Validador, contexto seletivo e controle de tarefas |
| examples/fluxo-v2/ | Plano demonstrativo de login incremental |
| tests/test_fluxo.py | Testes automatizados da ferramenta |
| docs/avaliacao.md | Critérios objetivos de avaliação |
| build.sh | Gera artefatos reproduzíveis em dist/ |

## Limites do que foi implementado

A CLI valida a estrutura e registra **evidências declaradas**, mas não executa o aplicativo, não confere a identidade de quem aprova uma sprint, não audita sozinha os logs e não verifica cobertura automaticamente. Também não executa agentes, não faz merges e não impõe permissão real de arquivos; o integrador precisa conferir isso. A estimativa de tokens por tamanho textual não mede consumo nem custo faturado. Não atribuímos ganho de produtividade sem estudos de execução.

## Qualidade e contribuição

Antes de enviar mudanças, execute os testes, valide a demonstração e rode o build. O GitHub Actions testa o núcleo, confere a distribuição, valida a demonstração e verifica se a documentação é coerente. Consulte [avaliação dos planos](docs/avaliacao.md).

## Licença

MIT.
