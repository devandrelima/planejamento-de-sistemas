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
