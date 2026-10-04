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
