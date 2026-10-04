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
