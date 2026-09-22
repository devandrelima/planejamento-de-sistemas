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
