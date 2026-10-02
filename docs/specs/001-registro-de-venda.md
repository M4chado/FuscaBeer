# Spec 001 — Registro de venda com forma de pagamento

| | |
|---|---|
| **Projeto** | Micro-SaaS Fusca Beer — ESW442 |
| **Equipe** | Augusto Wobeto, Eduardo Machado, Marcio Campos, Thiago Santana |
| **Versão** | 2 — endurecida no LAB 1 da Aula 08 |
| **Arquivo** | `docs/specs/001-registro-de-venda.md` |
| **Revisão cruzada** | `docs/specs/001-revisao.md` |

---

## 1. Objetivo

O Fusca Beer registra as vendas de cabeça e fecha o caixa no papel e na calculadora. Na entrevista, o proprietário, Gilmar Pereira Santos, relatou três dores: gasta de 20 a 30 minutos por dia fechando o caixa, já teve divergência entre o caixa e as formas de pagamento (dinheiro, cartão, Pix) e só descobre o que vendeu mais olhando o estoque.

Esta feature permite que o operador do balcão registre cada venda — produtos, quantidades e forma de pagamento — no momento em que ela acontece, e consulte o total do dia de operação, geral e por forma de pagamento.

> **Como** operador do balcão do Fusca Beer,
> **quero** registrar cada venda com os produtos, as quantidades e a forma de pagamento no momento em que ela acontece,
> **para que** o total do dia, geral e por forma de pagamento, esteja pronto no fim do expediente sem soma manual.

Esta é a feature de origem dos dados. As specs 002 (fechamento de caixa), 003 (produtos mais vendidos) e 004 (gestão de preços) leem o que esta feature registra.

---

## 2. Escopo

**Inclui**

1. Cadastrar produto (nome e preço), alterar o preço, inativar e reativar produto.
2. Montar uma venda com um ou mais itens (produto + quantidade).
3. Escolher uma forma de pagamento por venda: Dinheiro, Débito, Crédito ou Pix.
4. Em Dinheiro, informar o valor recebido e ver o troco.
5. Confirmar a venda.
6. Cancelar uma venda do dia de operação corrente, com motivo.
7. Consultar as vendas de um dia de operação, com total geral e total por forma de pagamento.

**Não inclui**

- Fechamento de caixa com conferência entre valor esperado e valor recebido → spec 002
- Relatório de produtos mais vendidos → spec 003
- Histórico de preços e análise de preço → spec 004
- Pagamento dividido em duas ou mais formas na mesma venda (D-03)
- Edição de venda confirmada (D-06)
- Exclusão definitiva de produto ou de venda (D-05, D-09)
- Desconto, acréscimo, gorjeta e couvert (D-15)
- Controle de estoque, emissão de nota fiscal, integração com maquininha de cartão ou com banco
- Mais de um login, perfis de permissão e mais de um estabelecimento (D-04)
- Registro de venda sem conexão com a internet (D-16)

---

## 3. Atores

| Ator | Quem é | O que pode fazer |
|---|---|---|
| **Operador** | A pessoa do Fusca Beer que usa o sistema no balcão — o proprietário ou quem estiver atendendo, com o mesmo login (D-04) | Os itens 1 a 7 do escopo |
| **Visitante** | Qualquer pessoa sem sessão ativa | Nada além da tela de login (RN-15) |

---

## 4. Dados

**Produto**

| Campo | Tipo | Obrigatório | Único | Regra |
|---|---|---|---|---|
| nome | texto, 2 a 60 caracteres | sim | sim, entre produtos ativos | RN-13 |
| preço | valor em R$, de R$ 0,01 a R$ 999,99 | sim | não | RN-12 |
| situação | Ativo ou Inativo | sim | não | produto novo começa Ativo |

**Venda**

| Campo | Tipo | Obrigatório | Único | Regra |
|---|---|---|---|---|
| identificador | gerado pelo sistema | sim | sim | — |
| data e hora | data e hora de Brasília | sim | não | o sistema preenche na confirmação |
| dia de operação | data | sim | não | RN-11 |
| itens | lista de Item da venda | sim, no mínimo 1 | não | RN-01, RN-02 |
| forma de pagamento | Dinheiro, Débito, Crédito ou Pix | sim | não | RN-06 |
| total | valor em R$ | sim | não | o sistema calcula (RN-05) |
| valor recebido | valor em R$ | só em Dinheiro | não | RN-07, RN-08 |
| troco | valor em R$ | só em Dinheiro | não | o sistema calcula (RN-07) |
| situação | Confirmada ou Cancelada | sim | não | RN-10 |
| motivo do cancelamento | texto, 3 a 200 caracteres | só se Cancelada | não | RN-10 |
| data e hora do cancelamento | data e hora de Brasília | só se Cancelada | não | o sistema preenche no cancelamento |

**Item da venda**

| Campo | Tipo | Obrigatório | Único | Regra |
|---|---|---|---|---|
| produto | referência a um produto Ativo | sim | sim, dentro da mesma venda | RN-02, RN-03 |
| nome do produto | texto | sim | não | cópia feita na confirmação (RN-04) |
| quantidade | número inteiro de 1 a 99 | sim | não | RN-01 |
| preço unitário | valor em R$ | sim | não | cópia feita na confirmação (RN-04) |
| subtotal | valor em R$ | sim | não | quantidade × preço unitário (RN-05) |

---

## 5. Regras de negócio

| ID | Regra |
|---|---|
| RN-01 | Uma venda tem no mínimo 1 item. Cada item tem quantidade inteira de 1 a 99. |
| RN-02 | Quando o operador adiciona um produto que já está na venda, o sistema soma a quantidade na linha existente. A soma respeita o limite de 99 da RN-01. |
| RN-03 | O sistema oferece e aceita na venda apenas produtos com situação Ativo. |
| RN-04 | Na confirmação, o sistema copia o nome e o preço do produto para o item. Uma alteração posterior no produto não muda vendas já confirmadas. |
| RN-05 | Subtotal = quantidade × preço unitário. Total da venda = soma dos subtotais. O operador não informa preço nem total. |
| RN-06 | Cada venda tem exatamente uma forma de pagamento: Dinheiro, Débito, Crédito ou Pix. |
| RN-07 | Em Dinheiro, o operador informa o valor recebido, que precisa ser maior ou igual ao total. O sistema calcula troco = valor recebido − total. |
| RN-08 | Em Débito, Crédito ou Pix, o sistema recusa a venda que traga valor recebido e não calcula troco. |
| RN-09 | O operador não edita venda confirmada. Para corrigir, cancela a venda e registra outra. |
| RN-10 | O operador cancela apenas venda Confirmada do dia de operação corrente, informando motivo de 3 a 200 caracteres. A venda cancelada continua na lista do dia, marcada como Cancelada, e o sistema a exclui do total geral e do total da sua forma de pagamento. |
| RN-11 | O dia de operação começa às 06:00 de uma data e termina às 05:59:59 da data seguinte, no horário de Brasília. Exemplo: uma venda às 01:30 de 02/10 pertence ao dia de operação 01/10. |
| RN-12 | O preço de um produto vai de R$ 0,01 a R$ 999,99. |
| RN-13 | O nome de produto é único entre produtos Ativos. A comparação ignora diferença entre maiúsculas e minúsculas e espaços no início e no fim. O sistema recusa reativar um produto cujo nome está em uso por outro produto Ativo. |
| RN-14 | A consulta de um dia de operação mostra: a quantidade de vendas Confirmadas, o total geral, o total de cada uma das quatro formas de pagamento (R$ 0,00 quando a forma não teve venda) e a lista de vendas, da mais recente para a mais antiga, com as Canceladas marcadas. |
| RN-15 | Sem sessão ativa, o sistema não executa nenhum item do escopo e exibe a tela de login. |

---

## 6. Critérios de aceite

Cada critério abaixo vira um teste automatizado de aceitação com o mesmo identificador. A equipe escolheu produtos e valores fictícios com contas que fecham.

```gherkin
# language: pt
Funcionalidade: Registro de venda com forma de pagamento

  Contexto:
    Dado que o operador está com sessão ativa
    E que existem os produtos:
      | nome                | preço | situação |
      | Chopp 300 ml        | 8,00  | Ativo    |
      | Cerveja lata 350 ml | 6,00  | Ativo    |
      | Água 500 ml         | 4,00  | Ativo    |
      | Refrigerante lata   | 5,00  | Inativo  |

  # ---------- Registro ----------

  Cenário: CA-01 Venda com dois produtos paga no Pix
    Quando o operador adiciona 2 "Chopp 300 ml" e 1 "Água 500 ml"
    E escolhe a forma de pagamento "Pix"
    E confirma a venda
    Então a lista do dia mostra uma venda de R$ 20,00 em "Pix" com 2 itens
    E essa venda não mostra valor recebido nem troco

  Cenário: CA-02 Venda em dinheiro com troco
    Quando o operador adiciona 3 "Cerveja lata 350 ml"
    E escolhe a forma de pagamento "Dinheiro"
    E informa o valor recebido de R$ 20,00
    E confirma a venda
    Então a tela mostra o troco de R$ 2,00
    E a lista do dia mostra uma venda de R$ 18,00 em "Dinheiro"

  Esquema do Cenário: CA-03 Venda em cartão ou Pix sem valor recebido
    Quando o operador adiciona 1 "Chopp 300 ml"
    E escolhe a forma de pagamento "<forma>"
    E confirma a venda
    Então a lista do dia mostra uma venda de R$ 8,00 em "<forma>"

    Exemplos:
      | forma   |
      | Débito  |
      | Crédito |
      | Pix     |

  Cenário: CA-04 Mesmo produto adicionado duas vezes
    Quando o operador adiciona 2 "Chopp 300 ml"
    E adiciona mais 1 "Chopp 300 ml"
    Então a venda em montagem mostra 1 linha "Chopp 300 ml" com quantidade 3 e subtotal R$ 24,00

  # ---------- Recusas ----------

  Esquema do Cenário: CA-05 Valor recebido em dinheiro inválido
    Quando o operador adiciona 3 "Cerveja lata 350 ml"
    E escolhe a forma de pagamento "Dinheiro"
    E informa o valor recebido "<recebido>"
    E confirma a venda
    Então a tela mostra a mensagem "<mensagem>"
    E a venda em montagem continua com 3 "Cerveja lata 350 ml"
    E a lista do dia não mostra venda nova

    Exemplos:
      | recebido | mensagem                                  |
      | 17,99    | Valor recebido menor que o total da venda |
      | (vazio)  | Informe o valor recebido                  |

  Cenário: CA-06 Valor recebido em pagamento que não é dinheiro
    Quando o operador envia uma venda de 1 "Chopp 300 ml" em "Pix" com valor recebido de R$ 20,00
    Então o sistema recusa a venda com a mensagem "Valor recebido só vale para pagamento em dinheiro"
    E a lista do dia não mostra venda nova

  Cenário: CA-07 Venda sem itens
    Quando o operador escolhe a forma de pagamento "Pix"
    E confirma a venda sem adicionar produto
    Então a tela mostra a mensagem "Adicione pelo menos um produto"
    E a lista do dia não mostra venda nova

  Esquema do Cenário: CA-08 Quantidade fora do limite
    Quando o operador tenta adicionar <qtd> "Chopp 300 ml"
    Então a tela mostra a mensagem "Informe uma quantidade de 1 a 99"
    E a venda em montagem não mostra o item

    Exemplos:
      | qtd |
      | 0   |
      | -1  |
      | 100 |

  Cenário: CA-09 Venda sem forma de pagamento
    Quando o operador adiciona 1 "Chopp 300 ml"
    E confirma a venda sem escolher a forma de pagamento
    Então a tela mostra a mensagem "Escolha a forma de pagamento"
    E a lista do dia não mostra venda nova

  Cenário: CA-10 Produto inativo fora da venda
    Quando o operador abre a tela de nova venda
    Então a lista de produtos não mostra "Refrigerante lata"
    E o sistema recusa uma venda enviada com "Refrigerante lata" com a mensagem "Produto inativo"

  # ---------- Histórico ----------

  Cenário: CA-11 Alteração de preço não muda venda confirmada
    Dado que o operador confirmou uma venda de 1 "Chopp 300 ml" em "Pix"
    Quando o operador altera o preço de "Chopp 300 ml" para R$ 9,00
    Então a venda já confirmada continua mostrando total de R$ 8,00
    E uma venda nova de 1 "Chopp 300 ml" mostra total de R$ 9,00

  # ---------- Consulta do dia ----------

  Cenário: CA-12 Totais do dia por forma de pagamento
    Dado que no dia de operação 01/10/2026 o operador confirmou as vendas:
      | itens                                | forma    |
      | 2 Chopp 300 ml e 1 Água 500 ml       | Pix      |
      | 3 Cerveja lata 350 ml                | Dinheiro |
      | 1 Chopp 300 ml                       | Crédito  |
      | 1 Cerveja lata 350 ml                | Pix      |
    Quando o operador consulta o dia de operação 01/10/2026
    Então a tela mostra 4 vendas e total geral de R$ 52,00
    E a tela mostra os totais por forma de pagamento:
      | forma    | total |
      | Dinheiro | 18,00 |
      | Débito   | 0,00  |
      | Crédito  | 8,00  |
      | Pix      | 26,00 |

  Cenário: CA-13 Venda depois da meia-noite pertence ao dia anterior
    Dado que o operador confirmou uma venda de 1 "Chopp 300 ml" em "Pix" às 01:30 de 02/10/2026
    Quando o operador consulta o dia de operação 01/10/2026
    Então essa venda aparece na lista
    E ela não aparece na consulta do dia de operação 02/10/2026

  # ---------- Cancelamento ----------

  Cenário: CA-14 Cancelar venda do dia com motivo
    Dado o dia de operação do CA-12
    Quando o operador cancela a venda em "Crédito" com o motivo "Lançada em duplicidade"
    Então a lista do dia mostra essa venda marcada como "Cancelada"
    E a tela mostra 3 vendas e total geral de R$ 44,00
    E a tela mostra total em "Crédito" de R$ 0,00

  Cenário: CA-15 Cancelar sem motivo
    Dado que o operador confirmou uma venda de 1 "Chopp 300 ml" em "Pix"
    Quando o operador tenta cancelar essa venda sem informar motivo
    Então a tela mostra a mensagem "Informe o motivo do cancelamento"
    E a lista do dia mostra essa venda como "Confirmada"

  Cenário: CA-16 Cancelar venda de dia de operação anterior
    Dado que existe uma venda Confirmada no dia de operação anterior ao corrente
    Quando o operador tenta cancelar essa venda com o motivo "Erro de lançamento"
    Então a tela mostra a mensagem "Só é possível cancelar vendas do dia de operação atual"
    E a consulta daquele dia mostra essa venda como "Confirmada"

  Cenário: CA-17 Cancelar venda já cancelada
    Dado que o operador cancelou uma venda com o motivo "Lançada em duplicidade"
    Quando o operador tenta cancelar a mesma venda de novo
    Então a tela mostra a mensagem "Esta venda já está cancelada"

  # ---------- Produtos ----------

  Cenário: CA-18 Nome de produto repetido
    Quando o operador cadastra o produto " chopp 300 ML " com preço R$ 10,00
    Então a tela mostra a mensagem "Já existe um produto ativo com este nome"
    E a lista de produtos continua com 1 produto chamado "Chopp 300 ml"

  Esquema do Cenário: CA-19 Preço fora da faixa
    Quando o operador cadastra o produto "Suco 300 ml" com preço R$ <preço>
    Então a tela mostra a mensagem "Informe um preço de R$ 0,01 a R$ 999,99"
    E a lista de produtos não mostra "Suco 300 ml"

    Exemplos:
      | preço    |
      | 0,00     |
      | 1.000,00 |

  # ---------- Acesso ----------

  Cenário: CA-20 Acesso sem sessão
    Dado que o visitante não tem sessão ativa
    Quando o visitante abre o endereço da tela de nova venda
    Então o sistema exibe a tela de login
    E o sistema não registra venda
```

**Rastreabilidade**

| Regra | Critérios |
|---|---|
| RN-01 | CA-07, CA-08 |
| RN-02 | CA-04 |
| RN-03 | CA-10 |
| RN-04 | CA-11 |
| RN-05 | CA-01, CA-04, CA-12 |
| RN-06 | CA-03, CA-09 |
| RN-07 | CA-02, CA-05, Tabela de exemplos |
| RN-08 | CA-06 |
| RN-09, RN-10 | CA-14, CA-15, CA-16, CA-17 |
| RN-11 | CA-13 |
| RN-12 | CA-19 |
| RN-13 | CA-18 |
| RN-14 | CA-12, CA-14 |
| RN-15 | CA-20 |

---

## 7. Restrições

**Stack e repositório**

| Camada | Escolha |
|---|---|
| Linguagem | Python 3.13 |
| Framework | Django 6.1 |
| Banco | PostgreSQL 17, também no ambiente local (Docker Compose) |
| Telas | Templates do Django + HTMX, renderizadas no servidor |
| Testes de unidade | pytest + pytest-django |
| Testes de aceitação | behave + behave-django, um cenário por critério desta spec |
| Qualidade | ruff no hook de pré-commit |

- Os comandos de instalar, rodar e testar ficam no `AGENTS.md`, na raiz do repositório.
- Esta spec fica em `docs/specs/001-registro-de-venda.md`. Mudança de comportamento altera esta spec primeiro, por pull request.
- O commit que implementa um critério cita a spec e o critério. Exemplo: `feat(001): calcula troco em dinheiro (CA-02)`.

**Padrões**

- O sistema armazena valores em R$ como número inteiro de centavos e os exibe na tela no formato R$ 1.234,56 (D-07).
- Datas e horas seguem o fuso America/Sao_Paulo.
- O registro da venda e dos seus itens acontece por inteiro ou não acontece.

**Rotas da aplicação (D-20)**

| Método e rota | Uso | Sucesso | Recusas |
|---|---|---|---|
| `GET /produtos/` | Lista de produtos | 200 | — |
| `POST /produtos/` | Cadastra produto | 302 para `/produtos/` | 422 |
| `POST /produtos/{id}/` | Altera preço, inativa ou reativa | 302 para `/produtos/` | 404, 422 |
| `GET /vendas/nova/` | Tela de nova venda, só com produtos ativos | 200 | — |
| `POST /vendas/` | Registra venda | 302 para `/vendas/` | 422 |
| `GET /vendas/?dia=AAAA-MM-DD` | Vendas e totais de um dia de operação (sem parâmetro: dia corrente) | 200 | 422 |
| `POST /vendas/{id}/cancelamento/` | Cancela venda | 302 para `/vendas/` | 404, 409, 422 |

- Recusa de validação responde 422 com o formulário de volta, os dados digitados mantidos e a mensagem do critério.
- Recusa por estado (venda de outro dia, venda já cancelada) responde 409 com a mensagem do critério.
- Requisição sem sessão recebe 302 para `/login/` (RN-15).
- O formulário nunca envia preço, subtotal nem total; o servidor calcula.

**Desempenho e uso no balcão**

| ID | Limite | Sensor |
|---|---|---|
| RS-01 | O operador registra uma venda de até 3 itens em até 15 segundos e até 6 toques, do toque em "Nova venda" até a confirmação na tela (D-17) | Cronometragem com o Gilmar no celular do balcão |
| RS-02 | `POST /vendas/` responde em até 500 ms no percentil 95, com 5.000 vendas registradas | Script de carga com limite de tempo |
| RS-03 | As telas funcionam a partir de 360 px de largura, com áreas de toque de no mínimo 44 × 44 px | Teste de interface em viewport de 360 px |
| RS-04 | Nenhuma rota de `/produtos/` ou `/vendas/` atende sem sessão | Teste que chama cada rota sem sessão e espera 302 para `/login/` |

---

## Tabela de exemplos — RN-07 (pagamento em dinheiro)

A regra mais importante da feature é a RN-07: o pagamento em dinheiro é onde nasce a divergência de caixa relatada pelo Gilmar, e a conferência da spec 002 depende de troco e valor recebido corretos.

| Caso | Itens | Total | Forma | Valor recebido | Resultado esperado |
|---|---|---|---|---|---|
| Feliz | 3 Cerveja lata 350 ml | R$ 18,00 | Dinheiro | R$ 20,00 | Venda registrada, troco R$ 2,00 |
| Feliz | 1 Chopp 300 ml e 1 Água 500 ml | R$ 12,00 | Dinheiro | R$ 50,00 | Venda registrada, troco R$ 38,00 |
| Borda | 3 Cerveja lata 350 ml | R$ 18,00 | Dinheiro | R$ 18,00 | Venda registrada, troco R$ 0,00 |
| Borda | 3 Cerveja lata 350 ml | R$ 18,00 | Dinheiro | R$ 18,01 | Venda registrada, troco R$ 0,01 |
| Erro | 3 Cerveja lata 350 ml | R$ 18,00 | Dinheiro | R$ 17,99 | Recusa: "Valor recebido menor que o total da venda" |
| Erro | 3 Cerveja lata 350 ml | R$ 18,00 | Dinheiro | (vazio) | Recusa: "Informe o valor recebido" |
| Erro | 3 Cerveja lata 350 ml | R$ 18,00 | Pix | R$ 20,00 | Recusa: "Valor recebido só vale para pagamento em dinheiro" (RN-08) |

---

## Decisões

| ID | Ambiguidade encontrada | Decisão | Motivo |
|---|---|---|---|
| D-01 | "Vendas do dia": dia do calendário (00:00–23:59) ou expediente? | Dia de operação das 06:00 às 05:59:59 do dia seguinte (RN-11) | Um bar pode fechar depois da meia-noite; a venda da 01:30 pertence ao mesmo expediente e ao mesmo fechamento. **Confirmar o horário de corte com o Gilmar.** |
| D-02 | "Cartão": uma forma ou duas? | Débito e Crédito separados | A maquininha mostra os dois separados; a conferência da spec 002 compara forma por forma. |
| D-03 | Cliente que paga parte em dinheiro e parte no Pix | Fora do escopo | Não apareceu na entrevista e muda o cálculo de troco e de totais. Reavaliar depois do piloto. |
| D-04 | Quem usa o sistema: o dono, o atendente ou os dois com permissões diferentes? | Um único perfil (Operador) e um login por estabelecimento | O piloto é um estabelecimento pequeno; perfis de permissão não resolvem nenhuma das três dores. |
| D-05 | "Cancelar venda": apagar, marcar ou estornar? | Marcar como Cancelada, com motivo; a venda continua visível e nenhum estorno acontece no sistema | Manter o registro permite investigar divergência de caixa; estorno de cartão ou Pix acontece fora do sistema. |
| D-06 | Editar venda confirmada? | Não; cancelar e registrar outra (RN-09) | Edição sem rastro esconderia o erro que o fechamento precisa enxergar. |
| D-07 | Precisão dos valores em R$ | Inteiro em centavos | Evita erro de arredondamento na soma de totais. |
| D-08 | Mudança de preço altera vendas antigas? | Não; o item guarda cópia do nome e do preço (RN-04) | As specs 003 e 004 precisam do preço praticado em cada venda. |
| D-09 | Excluir produto? | Apenas inativar e reativar | Vendas confirmadas apontam para o produto. |
| D-10 | "Chopp" e "chopp" são produtos diferentes? | Não; o nome é único entre ativos, sem diferenciar maiúsculas e ignorando espaços nas pontas (RN-13) | Nomes duplicados dividiriam as vendas de um produto em duas linhas no relatório da spec 003. |
| D-11 | Adicionar o mesmo produto duas vezes gera duas linhas? | Não; o sistema soma na linha existente (RN-02) | Uma linha por produto evita repetição na conferência da venda no balcão. |
| D-12 | Limite de quantidade por item | De 1 a 99 (RN-01) | Barra erro de digitação (100 no lugar de 10) e cobre a rodada de uma mesa grande. |
| D-13 | Faixa de preço do produto | De R$ 0,01 a R$ 999,99 (RN-12) | Preço zero criaria venda sem valor; o teto barra erro de casas decimais (R$ 8.000,00 no lugar de R$ 8,00). |
| D-14 | Valor recebido em Débito, Crédito ou Pix | O sistema recusa (RN-08) | Um valor recebido sem sentido distorceria a conferência da spec 002. |
| D-15 | Desconto, acréscimo, gorjeta e couvert | Fora do escopo | O Gilmar não os citou na entrevista; entram em spec própria se ele pedir. |
| D-16 | Registrar venda sem internet | Fora do escopo; o sistema exige conexão | Sincronização de vendas feitas sem conexão aumenta o escopo da primeira feature. **Confirmar com o Gilmar se o sinal no balcão é estável.** |
| D-17 | "Registrar sem atrasar o atendimento" (vagueza) | Até 15 segundos e 6 toques para uma venda de até 3 itens (RS-01) | Hoje o registro é de cabeça; um sistema mais lento que isso no balcão deixa de ser usado. |
| D-18 | Stack do projeto | Python 3.13, Django 6.1, PostgreSQL 17 e telas com templates + HTMX (seção 7) | A equipe já trabalha com Django; login, sessão, transação e painel admin vêm prontos; PostgreSQL também no ambiente local evita diferença de data e fuso entre ambientes, que afetaria a RN-11. |
| D-19 | Ordem da lista de vendas do dia | Da mais recente para a mais antiga (RN-14) | A venda que o operador quer conferir ou cancelar é a última registrada. |
| D-20 | Interface: API JSON ou páginas com formulários? | Páginas renderizadas no servidor, com formulários (seção 7) | O piloto tem um único cliente, a tela do balcão; uma API JSON separada seria uma segunda interface para manter e testar. |

**Varreduras da Aula 08**

| Varredura | Termos procurados | Resultado |
|---|---|---|
| Vagueza | rápido, fácil, amigável, intuitivo, robusto, eficiente, adequado, simples | Nenhuma ocorrência. "Sem atrasar o atendimento" virou o limite numérico da D-17. |
| Fuga | etc., entre outros, se necessário, quando aplicável, se possível, idealmente | Nenhuma ocorrência. |
| Ator e quantidade | voz passiva, todos, alguns, vários, a maioria, normalmente | Nenhuma ocorrência. Regras e critérios têm ator explícito (operador, sistema, visitante) e quantidades numéricas; as mensagens de erro "deve ser" viraram "Informe…". |

**Se o código fosse apagado agora, esta spec seria suficiente para reconstruí-lo?**

Para o comportamento, sim: objetivo, dados, 15 regras, 20 critérios de aceite, a tabela de exemplos e a stack da seção 7 definem o que construir, com o quê, e como verificar. Para a reconstrução completa, ainda faltam duas coisas: (1) a confirmação do horário de corte do dia de operação com o Gilmar (D-01); (2) o layout das telas, que esta spec não fixa de propósito — duas reconstruções teriam o mesmo comportamento com telas diferentes.
