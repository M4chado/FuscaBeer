# language: pt
Funcionalidade: Fechamento de caixa com conferência por forma de pagamento
  Spec: docs/specs/002-fechamento-de-caixa.md

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
