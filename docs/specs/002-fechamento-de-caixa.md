# Spec 002 — Fechamento de caixa com conferência por forma de pagamento

| | |
|---|---|
| **Projeto** | Micro-SaaS Fusca Beer — ESW442 |
| **Equipe** | Augusto Wobeto, Eduardo Machado, Marcio Campos, Thiago Santana |
| **Versão** | 1 — rascunho para a prática de TDD de 24/10 |
| **Arquivo** | `docs/specs/002-fechamento-de-caixa.md` |
| **Depende de** | `docs/specs/001-registro-de-venda.md` (vendas, totais por forma, dia de operação) |

---

## 1. Objetivo

Na entrevista, o Gilmar relatou que gasta de 20 a 30 minutos por dia fechando o caixa no papel e na calculadora, e que já teve divergência entre o caixa e as formas de pagamento. A spec 001 deixou pronto o total do dia por forma de pagamento. Esta feature usa esse total como **valor esperado** e o compara com o **valor contado** pelo conferente no fim do expediente, forma por forma.

> **Como** conferente do caixa do Fusca Beer,
> **quero** informar, no fim do expediente, quanto contei em cada forma de pagamento e ver a diferença para o que o sistema registrou,
> **para que** a divergência apareça na hora, forma por forma, e o caixa só fique fechado quando bater ou quando a diferença estiver justificada.

---

## 2. Escopo

**Inclui**

1. Abrir a conferência de um dia de operação e ver o valor esperado de cada forma de pagamento.
2. Informar o valor contado de cada uma das quatro formas: Dinheiro, Débito, Crédito e Pix.
3. Ver a divergência de cada forma (falta ou sobra) e a situação do caixa.
4. Refazer a conferência de um caixa Pendente (recontagem).
5. Fechar um caixa Pendente com justificativa da divergência.
6. Reabrir um caixa fechado com divergência justificada, ou um caixa fechado cujo total do dia mudou depois do fechamento.
7. Consultar um caixa fechado sem divergência, só para visualização.

**Não inclui**

- Trava de vendas depois do fechamento: o fechamento não impede registrar nem cancelar venda (D-02)
- Registro do fundo de troco (valor inicial na gaveta) no sistema (D-06)
- Sangria, suprimento e retirada de dinheiro durante o expediente (D-06)
- Tolerância de diferença: qualquer diferença a partir de R$ 0,01 é divergência (D-05)
- Conferência por turno ou por operador; o caixa é um por dia de operação (D-01)
- Integração com maquininha de cartão ou com banco para trazer o valor contado
- Perfis de permissão: o conferente usa o login único do operador (D-04 da spec 001)
- Relatório de produtos mais vendidos → spec 003

---

## 3. Atores

| Ator | Quem é | O que pode fazer |
|---|---|---|
| **Conferente** | Quem confere o caixa no fim do expediente — o proprietário ou quem ele indicar, com o mesmo login do operador (D-04 da spec 001) | Os itens 1 a 7 do escopo |
| **Visitante** | Qualquer pessoa sem sessão ativa | Nada além da tela de login (RN-15 da spec 001) |

---

## 4. Dados

**Fechamento de caixa**

| Campo | Tipo | Obrigatório | Único | Regra |
|---|---|---|---|---|
| dia de operação | data | sim | sim | RN-01 |
| situação | Pendente, Fechado ou Fechado com divergência | sim | não | RN-05, RN-06, RN-08 |
| esperado de cada forma | valor em R$, um por forma (4) | sim | não | o sistema calcula e guarda na conferência (RN-02) |
| contado de cada forma | valor em R$, um por forma (4) | sim | não | o conferente informa (RN-03) |
| divergência de cada forma | valor em R$, com sinal | sim | não | o sistema calcula (RN-04) |
| justificativa | texto, 3 a 200 caracteres | só em Fechado com divergência | não | RN-06 |
| conferido em | data e hora de Brasília | sim | não | o sistema preenche a cada conferência |
| fechado em | data e hora de Brasília | só se Fechado ou Fechado com divergência | não | o sistema preenche no fechamento |

---

## 5. Regras de negócio

| ID | Regra |
|---|---|
| RN-01 | Existe no máximo um fechamento por dia de operação (RN-11 da spec 001). O conferente confere apenas o dia de operação corrente ou um anterior. |
| RN-02 | O valor esperado de cada forma é a soma dos totais das vendas Confirmadas daquele dia de operação e daquela forma, calculada no momento da conferência (o mesmo total da RN-14 da spec 001). Venda Cancelada fica fora. Em Dinheiro, o esperado é a soma dos totais, e não dos valores recebidos: o troco já saiu da gaveta. |
| RN-03 | O conferente informa o valor contado das quatro formas, cada um maior ou igual a R$ 0,00. A conferência que tenha forma sem valor contado é recusada. |
| RN-04 | Divergência de uma forma = contado − esperado. Negativa é falta; positiva é sobra; zero é sem divergência. Qualquer diferença a partir de R$ 0,01 conta (D-05). |
| RN-05 | Se as quatro formas ficam sem divergência, o caixa vai para Fechado. Se pelo menos uma forma tem divergência, o caixa vai para Pendente e a tela mostra, para cada forma, o esperado, o contado e a falta ou a sobra. |
| RN-06 | Em caixa Pendente, o conferente pode refazer a conferência, informando de novo os quatro valores contados. O sistema recalcula o esperado e a divergência e aplica a RN-05. Também pode fechar o caixa com uma justificativa de 3 a 200 caracteres: o caixa vai para Fechado com divergência e mantém os valores da última conferência. |
| RN-07 | Um caixa Fechado ou Fechado com divergência guarda o esperado da conferência. Uma venda registrada ou cancelada depois do fechamento não muda esse valor; a tela do fechamento avisa quando o total atual do dia é diferente do esperado guardado (D-02). |
| RN-08 | O conferente reabre um caixa Fechado com divergência, ou um caixa Fechado cujo total atual do dia é diferente do esperado guardado (RN-07). O caixa volta para Pendente com os valores e a justificativa anteriores à vista. Um caixa Fechado sem divergência e sem mudança no total do dia depois do fechamento não é reaberto: fica disponível só para visualização (D-03, D-08). |
| RN-09 | O sistema recusa conferir ou fechar com justificativa um caixa que já está Fechado ou Fechado com divergência. |

---

## 6. Critérios de aceite

Cada critério abaixo vira um teste automatizado de aceitação com o mesmo identificador, em `features/002-fechamento-de-caixa.feature`. As vendas do Contexto são as do CA-12 da spec 001, mais uma venda cancelada.

```gherkin
# language: pt
Funcionalidade: Fechamento de caixa com conferência por forma de pagamento

  Contexto:
    Dado que o operador está com sessão ativa
    E que existem os produtos:
      | nome                | preço | situação |
      | Chopp 300 ml        | 8,00  | Ativo    |
      | Cerveja lata 350 ml | 6,00  | Ativo    |
      | Água 500 ml         | 4,00  | Ativo    |
    E que no dia de operação corrente o operador confirmou as vendas:
      | itens                          | forma    |
      | 2 Chopp 300 ml e 1 Água 500 ml | Pix      |
      | 3 Cerveja lata 350 ml          | Dinheiro |
      | 1 Chopp 300 ml                 | Crédito  |
      | 1 Cerveja lata 350 ml          | Pix      |
      | 1 Água 500 ml                  | Débito   |
    E que a venda em "Débito" foi cancelada com o motivo "Lançada em duplicidade"

  # ---------- Conferência ----------

  Cenário: CA-01 Conferência sem divergência fecha o caixa
    Quando o conferente abre a conferência do dia de operação corrente
    Então a tela mostra os valores esperados:
      | forma    | esperado |
      | Dinheiro | 18,00    |
      | Débito   | 0,00     |
      | Crédito  | 8,00     |
      | Pix      | 26,00    |
    Quando o conferente informa os valores contados 18,00 / 0,00 / 8,00 / 26,00
    Então o caixa fica "Fechado"
    E a tela não mostra divergência

  Esquema do Cenário: CA-02 Conferência com divergência deixa o caixa pendente
    Quando o conferente informa os valores contados <dinheiro> / 0,00 / 8,00 / <pix>
    Então o caixa fica "Pendente"
    E a tela mostra "<divergência>" em "<forma>"
    E as outras formas não mostram divergência

    Exemplos:
      | dinheiro | pix   | forma    | divergência       |
      | 16,00    | 26,00 | Dinheiro | Falta de R$ 2,00  |
      | 18,00    | 30,00 | Pix      | Sobra de R$ 4,00  |
      | 17,99    | 26,00 | Dinheiro | Falta de R$ 0,01  |

  Cenário: CA-03 Valor contado em branco
    Quando o conferente informa os valores contados (vazio) / 0,00 / 8,00 / 26,00
    Então a tela mostra a mensagem "Informe o valor contado de Dinheiro"
    E o dia de operação corrente continua sem conferência

  # ---------- Caixa pendente ----------

  Cenário: CA-04 Recontagem que bate fecha o caixa pendente
    Dado que o conferente informou os valores contados 16,00 / 0,00 / 8,00 / 26,00
    Quando o conferente informa os valores contados 18,00 / 0,00 / 8,00 / 26,00
    Então o caixa fica "Fechado"
    E a tela não mostra divergência

  Cenário: CA-05 Correção de venda antes da recontagem
    Dado que o conferente informou os valores contados 18,00 / 0,00 / 0,00 / 26,00
    E que o operador cancelou a venda em "Crédito" com o motivo "Cliente desistiu"
    Quando o conferente informa os valores contados 18,00 / 0,00 / 0,00 / 26,00
    Então o caixa fica "Fechado"
    E a tela mostra esperado de R$ 0,00 em "Crédito"

  Cenário: CA-06 Fechar caixa pendente com justificativa
    Dado que o conferente informou os valores contados 16,00 / 0,00 / 8,00 / 26,00
    Quando o conferente fecha o caixa com a justificativa "Troco dado a mais na venda das 21h"
    Então o caixa fica "Fechado com divergência"
    E a tela mostra "Falta de R$ 2,00" em "Dinheiro"
    E a tela mostra a justificativa "Troco dado a mais na venda das 21h"

  Esquema do Cenário: CA-07 Justificativa inválida
    Dado que o conferente informou os valores contados 16,00 / 0,00 / 8,00 / 26,00
    Quando o conferente fecha o caixa com a justificativa "<justificativa>"
    Então a tela mostra a mensagem "Informe a justificativa da divergência, de 3 a 200 caracteres"
    E o caixa continua "Pendente"

    Exemplos:
      | justificativa |
      | (vazio)       |
      | ok            |

  # ---------- Caixa fechado ----------

  Cenário: CA-08 Venda depois do fechamento não muda o caixa fechado
    Dado que o conferente informou os valores contados 18,00 / 0,00 / 8,00 / 26,00
    Quando o operador confirma uma venda de 1 "Chopp 300 ml" em "Pix"
    E o conferente abre a conferência do dia de operação corrente
    Então o caixa continua "Fechado" com esperado de R$ 26,00 em "Pix"
    E a tela mostra a mensagem "Houve vendas registradas ou canceladas depois do fechamento"

  Cenário: CA-09 Reabrir caixa fechado com divergência
    Dado que o conferente fechou o caixa com divergência e a justificativa "Troco dado a mais na venda das 21h"
    Quando o conferente reabre o caixa
    Então o caixa fica "Pendente"
    E a tela mostra "Falta de R$ 2,00" em "Dinheiro"
    E a tela mostra a justificativa "Troco dado a mais na venda das 21h"

  Cenário: CA-10 Caixa fechado sem divergência é só visualização
    Dado que o conferente informou os valores contados 18,00 / 0,00 / 8,00 / 26,00
    Quando o conferente tenta reabrir o caixa
    Então a tela mostra a mensagem "Caixa fechado sem divergência: disponível só para visualização"
    E o caixa continua "Fechado"

  Cenário: CA-11 Reabrir caixa fechado cujo total do dia mudou
    Dado que o conferente informou os valores contados 18,00 / 0,00 / 8,00 / 26,00
    E que o operador confirmou uma venda de 1 "Chopp 300 ml" em "Pix"
    Quando o conferente reabre o caixa
    E informa os valores contados 18,00 / 0,00 / 8,00 / 34,00
    Então o caixa fica "Fechado"
    E a tela mostra esperado de R$ 34,00 em "Pix"

  Cenário: CA-12 Conferir de novo um caixa já fechado
    Dado que o conferente informou os valores contados 18,00 / 0,00 / 8,00 / 26,00
    Quando o conferente tenta informar os valores contados 10,00 / 0,00 / 8,00 / 26,00
    Então a tela mostra a mensagem "Este caixa já está fechado"
    E o caixa continua "Fechado" sem divergência

  # ---------- Dia e acesso ----------

  Cenário: CA-13 Conferir dia de operação que ainda não começou
    Quando o conferente tenta informar os valores contados do dia de operação seguinte ao corrente
    Então a tela mostra a mensagem "Só é possível conferir um dia de operação já iniciado"

  Cenário: CA-14 Acesso sem sessão
    Dado que o visitante não tem sessão ativa
    Quando o visitante abre o endereço da conferência do dia de operação corrente
    Então o sistema exibe a tela de login
    E o sistema não registra conferência
```

**Rastreabilidade**

| Regra | Critérios |
|---|---|
| RN-01 | CA-12, CA-13 |
| RN-02 | CA-01, CA-05 |
| RN-03 | CA-03 |
| RN-04 | CA-02, Tabela de exemplos |
| RN-05 | CA-01, CA-02, CA-04 |
| RN-06 | CA-04, CA-05, CA-06, CA-07 |
| RN-07 | CA-08, CA-11 |
| RN-08 | CA-09, CA-10, CA-11 |
| RN-09 | CA-12 |
| RN-15 (spec 001) | CA-14 |

---

## 7. Restrições

Valem a stack, os padrões e as regras de repositório da seção 7 da spec 001. O commit que implementa um critério cita esta spec: `feat(002): fecha caixa sem divergência (CA-01)`.

**Rotas da aplicação**

| Método e rota | Uso | Sucesso | Recusas |
|---|---|---|---|
| `GET /caixa/?dia=AAAA-MM-DD` | Conferência de um dia de operação (sem parâmetro: dia corrente) | 200 | 422 |
| `POST /caixa/conferencia/` | Informa os quatro valores contados do dia | 302 para `/caixa/?dia=` | 409, 422 |
| `POST /caixa/justificativa/` | Fecha caixa Pendente com justificativa | 302 para `/caixa/?dia=` | 404, 409, 422 |
| `POST /caixa/reabertura/` | Reabre caixa Fechado com divergência ou com total do dia mudado | 302 para `/caixa/?dia=` | 404, 409 |

- Recusa de validação (valor contado, justificativa, dia futuro) responde 422 com o formulário de volta e a mensagem do critério.
- Recusa por estado (caixa já fechado, reabrir caixa sem divergência) responde 409 com a mensagem do critério.
- O formulário nunca envia valor esperado nem divergência; o servidor calcula.
- Requisição sem sessão recebe 302 para `/login/`.

---

## Tabela de exemplos — RN-04 (divergência)

| Caso | Esperado | Contado | Divergência | Exibição |
|---|---|---|---|---|
| Feliz | R$ 18,00 | R$ 18,00 | 0 | sem divergência |
| Falta | R$ 18,00 | R$ 16,00 | −200 | Falta de R$ 2,00 |
| Sobra | R$ 26,00 | R$ 30,00 | +400 | Sobra de R$ 4,00 |
| Borda | R$ 18,00 | R$ 17,99 | −1 | Falta de R$ 0,01 |
| Borda | R$ 18,00 | R$ 18,01 | +1 | Sobra de R$ 0,01 |
| Zero | R$ 0,00 | R$ 0,00 | 0 | sem divergência |
| Erro | R$ 18,00 | (vazio) | — | Recusa: "Informe o valor contado de Dinheiro" |

---

## Decisões

| ID | Ambiguidade encontrada | Decisão | Motivo |
|---|---|---|---|
| D-01 | Quando o caixa é conferido? | No fim do expediente, um fechamento por dia de operação (RN-01) | Confirmado com a equipe em 24/10: o caixa é conferido no fim do expediente. O dia de operação da spec 001 já cobre a noite que passa de meia-noite. |
| D-02 | O fechamento trava novas vendas? | Não. O esperado fica guardado no fechamento e a tela avisa quando o total do dia mudou depois dele (RN-07) | Confirmado em 24/10: o fechamento não trava vendas. Sem guardar o esperado, um caixa que bateu passaria a mostrar divergência sozinho. |
| D-03 | Caixa fechado pode ser reaberto? | Só o Fechado com divergência; o Fechado sem divergência fica só para visualização (RN-08) | Confirmado em 24/10: reabre para justificar ou arrumar o erro; caixa que deu certo só se visualiza. |
| D-04 | Divergência trava o fechamento? | Sim: o caixa fica Pendente até a recontagem bater ou até haver justificativa (RN-05, RN-06) | Confirmado em 24/10: o caixa com diferença fica pendente para o conferente descobrir o motivo. |
| D-05 | Tolerância para diferença de centavos | Nenhuma: R$ 0,01 já é divergência (RN-04) | A dor relatada é justamente a divergência; uma tolerância a esconderia. |
| D-06 | Fundo de troco, sangria e suprimento | Fora do escopo. O conferente informa em Dinheiro só o que entrou pelas vendas (contado na gaveta − fundo de troco) | Confirmado com a equipe em 24/10: o caixa começa com um fundo de troco, mas esse valor não é informado no sistema. |
| D-07 | "Arrumar o que estava com erro": o que o conferente corrige? | O valor contado (recontagem, RN-06) e, pelas regras da spec 001, a venda lançada errada (cancelar e registrar outra, CA-05) | Confirmado com a equipe em 24/10. A RN-10 da spec 001 só cancela venda do dia de operação corrente: depois das 06:00 do dia seguinte, a correção de venda sai do alcance e sobra a justificativa. |
| D-08 | Caixa Fechado sem divergência que recebe venda depois do fechamento | Pode ser reaberto quando o total atual do dia é diferente do esperado guardado (RN-08, CA-11) | Confirmado com a equipe em 24/10. Só com a D-03, esse caixa ficaria errado e sem conserto, porque o fechamento não trava vendas (D-02). |
| D-09 | Reabertura pede motivo? | Não; a justificativa anterior continua à vista | O login é único (D-04 da spec 001), então o motivo não identificaria quem reabriu. |
