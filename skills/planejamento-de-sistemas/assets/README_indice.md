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
