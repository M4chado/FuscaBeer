# language: pt
Funcionalidade: Registro de venda com forma de pagamento
  Spec: docs/specs/001-registro-de-venda.md

  Contexto:
    Dado que o operador está com sessão ativa
    E que existem os produtos:
      | nome                | preço | situação |
      | Chopp 300 ml        | 8,00  | Ativo    |
      | Cerveja lata 350 ml | 6,00  | Ativo    |
      | Água 500 ml         | 4,00  | Ativo    |
      | Refrigerante lata   | 5,00  | Inativo  |

  Cenário: CA-02 Venda em dinheiro com troco
    Quando o operador adiciona 3 "Cerveja lata 350 ml"
    E escolhe a forma de pagamento "Dinheiro"
    E informa o valor recebido de R$ 20,00
    E confirma a venda
    Então a tela mostra o troco de R$ 2,00
    E a lista do dia mostra uma venda de R$ 18,00 em "Dinheiro"

  # ---------- Acesso ----------

  Cenário: CA-20 Acesso sem sessão
    Dado que o visitante não tem sessão ativa
    Quando o visitante abre o endereço da tela de nova venda
    Então o sistema exibe a tela de login
    E o sistema não registra venda
