from behave import given, then, when
from django.contrib.auth import get_user_model

from vendas.models import Produto


def centavos(texto):
    return int(texto.replace(".", "").replace(",", ""))


@given("que o operador está com sessão ativa")
def step_sessao_ativa(context):
    operador = get_user_model().objects.create_user("operador", password="senha-de-teste")
    context.test.client.force_login(operador)


@given("que existem os produtos:")
def step_produtos(context):
    for linha in context.table:
        Produto.objects.create(
            nome=linha["nome"],
            preco_centavos=centavos(linha["preço"]),
            ativo=linha["situação"] == "Ativo",
        )


@when('o operador adiciona {quantidade:d} "{nome}"')
def step_adiciona(context, quantidade, nome):
    context.itens = [{"produto": Produto.objects.get(nome=nome).pk, "quantidade": quantidade}]


@when('escolhe a forma de pagamento "{forma}"')
def step_forma(context, forma):
    context.forma = forma


@when("informa o valor recebido de R$ {valor}")
def step_valor_recebido(context, valor):
    context.valor_recebido = valor


@when("confirma a venda")
def step_confirma(context):
    item = context.itens[0]
    context.resposta = context.test.client.post(
        "/vendas/",
        {
            "produto": item["produto"],
            "quantidade": item["quantidade"],
            "forma": context.forma,
            "valor_recebido": context.valor_recebido,
        },
        follow=True,
    )


@then("a tela mostra o troco de R$ {valor}")
def step_mostra_troco(context, valor):
    assert f"Troco: R$ {valor}" in context.resposta.content.decode(), context.resposta.content


@then('a lista do dia mostra uma venda de R$ {total} em "{forma}"')
def step_lista_do_dia(context, total, forma):
    assert f"R$ {total} em {forma}" in context.resposta.content.decode(), context.resposta.content
