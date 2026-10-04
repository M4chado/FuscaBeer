from behave import given, register_type, then, when
from bs4 import BeautifulSoup
from django.contrib.auth import get_user_model
from parse import with_pattern

from vendas.models import Produto


@with_pattern(r'[^"]+')
def _nome(texto):
    return texto


# {nome:Nome} não aceita aspas: 'adiciona 2 "A" e 1 "B"' não casa com 'adiciona {n} "{nome}"'.
register_type(Nome=_nome)


def centavos(texto):
    return int(texto.replace(".", "").replace(",", ""))


def pagina(resposta):
    return BeautifulSoup(resposta.content.decode(), "html.parser")


def texto(resposta):
    return " ".join(pagina(resposta).get_text(" ").split())


def entrar_como_operador(context):
    context.test.client.force_login(get_user_model().objects.get(username="operador"))


@given("que o operador está com sessão ativa")
def step_sessao_ativa(context):
    get_user_model().objects.create_user("operador", password="senha-de-teste")
    entrar_como_operador(context)


@given("que existem os produtos:")
def step_produtos(context):
    for linha in context.table:
        Produto.objects.create(
            nome=linha["nome"],
            preco_centavos=centavos(linha["preço"]),
            ativo=linha["situação"] == "Ativo",
        )


# ---------- Venda em montagem (dirigida pela tela de nova venda) ----------


def montagem(context):
    """Página atual da nova venda; abre a tela na primeira vez."""
    if getattr(context, "montagem", None) is None:
        context.montagem = pagina(context.test.client.get("/vendas/nova/"))
    return context.montagem


def itens_ocultos(tela):
    return [campo["value"] for campo in tela.select("form#venda input[name=item]")]


def adicionar(context, quantidade, nome):
    """Toca no botão do produto com a quantidade digitada, como o operador faz."""
    tela = montagem(context)
    botao = next(b for b in tela.select("button.produto") if b.select_one(".nome").text == nome)
    dados = {"item": itens_ocultos(tela), "quantidade": quantidade, "produto": botao["value"]}
    context.resposta = context.test.client.get("/vendas/nova/", dados)
    context.montagem = pagina(context.resposta)


def linhas_da_montagem(context):
    return [
        {
            campo: linha.select_one(f".{campo}").get_text(strip=True)
            for campo in ("nome", "quantidade", "subtotal")
        }
        for linha in montagem(context).select(".montagem tr.item")
    ]


@when('o operador adiciona {quantidade:d} "{nome:Nome}"')
def step_adiciona(context, quantidade, nome):
    adicionar(context, quantidade, nome)


@when('o operador adiciona {q1:d} "{nome1:Nome}" e {q2:d} "{nome2:Nome}"')
def step_adiciona_dois(context, q1, nome1, q2, nome2):
    adicionar(context, q1, nome1)
    adicionar(context, q2, nome2)


@when('adiciona mais {quantidade:d} "{nome:Nome}"')
def step_adiciona_mais(context, quantidade, nome):
    adicionar(context, quantidade, nome)


@when('o operador tenta adicionar {quantidade} "{nome:Nome}"')
def step_tenta_adicionar(context, quantidade, nome):
    adicionar(context, quantidade, nome)


@then(
    'a venda em montagem mostra 1 linha "{nome:Nome}" com quantidade {quantidade:d} '
    "e subtotal R$ {subtotal}"
)
def step_montagem_linha(context, nome, quantidade, subtotal):
    linhas = linhas_da_montagem(context)
    esperada = {"nome": nome, "quantidade": str(quantidade), "subtotal": f"R$ {subtotal}"}
    assert linhas == [esperada], linhas


@then("a venda em montagem não mostra o item")
def step_montagem_vazia(context):
    assert linhas_da_montagem(context) == [], linhas_da_montagem(context)


# ---------- Pagamento e confirmação ----------


@when('escolhe a forma de pagamento "{forma}"')
def step_forma(context, forma):
    context.forma = forma


@when("informa o valor recebido de R$ {valor}")
def step_valor_recebido(context, valor):
    context.valor_recebido = valor


@when("confirma a venda")
def step_confirma(context):
    dados = {
        "item": itens_ocultos(montagem(context)),
        "forma": getattr(context, "forma", ""),
        "valor_recebido": getattr(context, "valor_recebido", ""),
    }
    context.resposta = context.test.client.post("/vendas/", dados, follow=True)


@then("a tela mostra o troco de R$ {valor}")
def step_mostra_troco(context, valor):
    assert f"Troco: R$ {valor}" in texto(context.resposta), texto(context.resposta)


@then('a lista do dia mostra uma venda de R$ {total} em "{forma}"')
def step_lista_do_dia(context, total, forma):
    assert f"R$ {total} em {forma}" in texto(context.resposta), texto(context.resposta)


# ---------- Acesso ----------


@when("o visitante abre o endereço da tela de nova venda")
def step_visitante_abre_nova(context):
    context.resposta = context.test.client.get("/vendas/nova/")


@then("o sistema exibe a tela de login")
def step_exibe_login(context):
    resposta = context.resposta
    assert resposta.status_code == 302, resposta.status_code
    assert resposta["Location"].startswith("/login/"), resposta["Location"]
    tela = context.test.client.get(resposta["Location"])
    assert tela.status_code == 200, tela.status_code
    assert pagina(tela).select_one("form#login"), texto(tela)


@then("o sistema não registra venda")
def step_nao_registra(context):
    chopp = Produto.objects.get(nome="Chopp 300 ml")
    envio = context.test.client.post("/vendas/", {"item": f"{chopp.pk}:1", "forma": "Pix"})
    assert envio.status_code == 302, envio.status_code
    assert envio["Location"].startswith("/login/"), envio["Location"]
    entrar_como_operador(context)
    lista = pagina(context.test.client.get("/vendas/"))
    assert not lista.select(".venda"), lista.get_text(" ")


# ---------- Mensagens e lista de produtos (tela atual) ----------


@then('a tela mostra a mensagem "{mensagem}"')
def step_mostra_mensagem(context, mensagem):
    mensagens = [li.get_text(" ", strip=True) for li in pagina(context.resposta).select(".erro")]
    assert mensagem in mensagens, (context.resposta.status_code, mensagens)


def nomes_de_produto(resposta):
    return [n.get_text(strip=True) for n in pagina(resposta).select(".produto .nome")]


@then('a lista de produtos continua com {quantidade:d} produto chamado "{nome:Nome}"')
def step_lista_produtos_com(context, quantidade, nome):
    nomes = nomes_de_produto(context.resposta)
    assert nomes.count(nome) == quantidade, nomes


@then('a lista de produtos não mostra "{nome:Nome}"')
def step_lista_produtos_sem(context, nome):
    nomes = nomes_de_produto(context.resposta)
    assert nomes, "a tela não tem lista de produtos"
    assert nome not in nomes, nomes


# ---------- Produtos ----------


@when('o operador cadastra o produto "{nome:Nome}" com preço R$ {preco}')
def step_cadastra_produto(context, nome, preco):
    context.resposta = context.test.client.post("/produtos/", {"nome": nome, "preco": preco})
