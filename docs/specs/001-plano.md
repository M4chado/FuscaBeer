# Plano de tarefas — Spec 001 (Registro de venda)

| | |
|---|---|
| **Spec** | `docs/specs/001-registro-de-venda.md` (versão 2) |
| **Equipe** | Augusto Wobeto, Eduardo Machado, Marcio Campos, Thiago Santana |
| **Ciclo** | especificar → planejar → implementar → verificar → atualizar a spec (Aula 07) |
| **Revisão do plano pela equipe** | [nome de quem revisou] em [dd/mm/2026] — antes do primeiro commit de código |

## Como cada tarefa é feita

1. Copiar da spec, sem mudar uma palavra, o cenário de cada CA da tarefa para `features/001-registro-de-venda.feature`.
2. Escrever os passos que faltam em `features/steps/001_steps.py`. O `Então` confere só o que o operador vê (status, texto, redirecionamento), nunca o banco.
3. Rodar o cenário e ver **falhar** pelo motivo esperado.
4. Implementar o mínimo para passar. Regra de cálculo ganha teste de unidade em `tests/`.
5. Prova: `ruff check . && ruff format --check .`, `pytest` e `python manage.py behave` inteiros.
6. Um commit por tarefa, citando spec e critérios: `feat(001): <o que mudou> (CA-xx, CA-yy)`.

## Tarefas

| # | Tarefa | Critérios | Regras | Arquivos principais | Pronto quando |
|---|---|---|---|---|---|
| T0 | Este plano, revisado pela equipe | — | — | `docs/specs/001-plano.md` | Equipe registrou a revisão acima |
| T1 | Esqueleto das telas: `base.html` para celular (360 px, toque de 44 px), HTMX vendorizado em `static/`, `/login/` e `/logout/`, `/` redireciona para a nova venda, toda rota de `/produtos/` e `/vendas/` exige sessão | CA-20 | RN-15, RS-03 (layout), RS-04 | `config/`, `templates/`, `static/`, `tests/test_acesso.py` | CA-20 e o teste de RS-04 passam |
| T2 | Produto: cadastro com nome de 2 a 60 caracteres, único entre ativos sem diferenciar maiúsculas e espaços nas pontas, preço de R$ 0,01 a R$ 999,99. Conversão "1.234,56" ↔ centavos | CA-18, CA-19 | RN-12, RN-13 | `vendas/models.py`, migração `0002`, `vendas/regras.py`, `/produtos/` | CA-18 e CA-19 passam; unidade de `para_centavos` |
| T3 | Venda em montagem: produtos ativos como botões, quantidade de 1 a 99, mesmo produto soma na linha existente (até 99), subtotal calculado no servidor | CA-04, CA-08, CA-10 (1ª parte) | RN-01, RN-02, RN-03, RN-05 | `GET /vendas/nova/`, `nova.html`, `regras.somar_item` | CA-04 e CA-08 passam |
| T4 | Registro de venda com vários itens e uma forma de pagamento, tudo ou nada; recusas de venda vazia, sem forma e com produto inativo | CA-01, CA-03, CA-07, CA-09, CA-10 | RN-01, RN-03, RN-04, RN-05, RN-06 | `POST /vendas/`, `lista.html` | CA-01, CA-03, CA-07, CA-09, CA-10 passam e CA-02 continua passando |
| T5 | Pagamento em dinheiro: valor recebido obrigatório e ≥ total, troco; recusa de valor recebido fora do dinheiro | CA-02, CA-05, CA-06 | RN-07, RN-08 | `POST /vendas/`, `tests/test_regras_venda.py` (tabela de exemplos) | Cenários e os 7 casos da tabela de exemplos passam |
| T6 | Alterar preço, inativar e reativar produto (`POST /produtos/{id}/`); a venda confirmada guarda cópia do nome e do preço | CA-11 | RN-04, RN-13 (reativar) | `vendas/views.py`, `produtos.html` | CA-11 passa |
| T7 | Consulta de um dia de operação: `?dia=AAAA-MM-DD`, dia de 06:00 a 05:59:59, quantidade de confirmadas, total geral, total das 4 formas, lista da mais recente para a mais antiga | CA-12, CA-13 | RN-11, RN-14 | `regras.dia_operacao`, `regras.totais_do_dia`, `lista.html` | CA-12 e CA-13 passam; unidade das bordas 05:59:59 / 06:00 |
| T8 | Cancelamento com motivo de 3 a 200 caracteres, só do dia corrente, sem cancelar duas vezes; cancelada fica na lista e sai dos totais | CA-14, CA-15, CA-16, CA-17 | RN-09, RN-10 | migração `0003`, `POST /vendas/{id}/cancelamento/` | Os quatro cenários passam |
| T9 | Fechar o ciclo: `AGENTS.md` com o comando de criar o login do operador, declaração sobre a spec, diário do agente | — | — | `AGENTS.md`, `docs/harness/diario-001.md` | Clone limpo roda seguindo só o `AGENTS.md` |

Fora deste plano (fica para o diário e para a apresentação): RS-01 (cronometragem com o Gilmar no balcão) e RS-02 (script de carga com 5.000 vendas) não viram teste automatizado nesta feature.

## Suposições declaradas antes do código

Cada uma é uma leitura da spec; nenhuma muda comportamento descrito nela. Se a equipe discordar de alguma, a tarefa correspondente muda antes do commit.

| # | Trecho da spec | Leitura adotada |
|---|---|---|
| S-01 | CA-01 "com 2 itens" | Itens são as linhas da venda (Item da venda), não unidades: 2 Chopp + 1 Água = 2 itens. |
| S-02 | Rotas (D-20) não listam a montagem | A montagem usa a própria `GET /vendas/nova/`: os itens já escolhidos voltam ao servidor em campos ocultos `item=<id do produto>:<quantidade>`, e o servidor devolve a tela com a linha somada e o subtotal calculado. Nenhuma rota nova além de `/login/`, `/logout/` e `/`. |
| S-03 | Formato de valores digitados | Formato brasileiro: ponto separa milhar e vírgula separa centavos (`1.000,00`). Mais de duas casas decimais é valor inválido. |
| S-04 | RN-02 "a soma respeita o limite de 99" | Se a soma passar de 99, a linha não muda e a tela mostra "Informe uma quantidade de 1 a 99". |
| S-05 | RN-10 motivo de 3 a 200 caracteres | Motivo vazio, com menos de 3 ou com mais de 200 caracteres (sem os espaços das pontas) recebe "Informe o motivo do cancelamento". |
| S-06 | Ordem das recusas no cancelamento | 404 (venda não existe) → 409 já cancelada → 409 outro dia → 422 motivo. Por isso o CA-17 mostra "Esta venda já está cancelada" mesmo que o motivo seja válido. |
| S-07 | RN-15 "tela de login" | Um único login (D-04), criado com `python manage.py createsuperuser`. |
| S-08 | Cancelar a partir da lista | O botão de cancelar aparece só em venda Confirmada do dia corrente; a rota recusa as demais mesmo se chamada direto (CA-16). |

## Spec depois da implementação

**A implementação não mudou nenhum comportamento da spec 001.** Os 20 critérios de aceite estão em `features/001-registro-de-venda.feature`, copiados sem mudar uma palavra, e passam. Nenhuma regra, mensagem, rota ou código de resposta da seção 7 foi alterado. Por isso `docs/specs/001-registro-de-venda.md` não foi editada.

O que a implementação precisou decidir e a spec não diz está nas suposições S-01 a S-08 acima. Proposta para a equipe aprovar e levar à spec como decisões novas (por pull request, como pede a seção 7):

| Proposta | Origem | Onde entraria na spec |
|---|---|---|
| D-21: "itens" de uma venda são as linhas (Item da venda), não as unidades | S-01 | Seção 4, Venda › itens |
| D-22: a montagem da venda volta ao servidor por `GET /vendas/nova/?item=<id>:<qtd>&produto=<id>&quantidade=<n>` | S-02 | Seção 7, tabela de rotas |
| D-23: `GET /login/` e `POST /logout/` na tabela de rotas | S-07 | Seção 7, tabela de rotas |
| D-24: valores digitados no formato brasileiro (ponto de milhar, vírgula decimal) | S-03 | Seção 7, Padrões |
| D-25: soma acima de 99 recusada com "Informe uma quantidade de 1 a 99" | S-04 | RN-02 |
| D-26: motivo fora de 3 a 200 caracteres recebe "Informe o motivo do cancelamento"; recusa por estado vem antes da recusa por motivo | S-05, S-06 | RN-10 |

Continuam em aberto, como a própria spec já dizia: confirmar com o Gilmar o horário de corte do dia de operação (D-01) e a estabilidade do sinal no balcão (D-16).
