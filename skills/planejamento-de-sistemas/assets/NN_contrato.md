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
