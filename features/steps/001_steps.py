from datetime import datetime
from unittest import mock
from zoneinfo import ZoneInfo

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


def vendas_na_lista(resposta):
    """Linhas da lista do dia como o operador as lê."""
    linhas = []
    for linha in pagina(resposta).select(".venda"):
        campos = {
            campo: linha.select_one(f".{campo}").get_text(" ", strip=True)
            for campo in ("total", "forma", "itens", "recebido", "troco", "situacao")
            if linha.select_one(f".{campo}")
        }
        linhas.append({"id": linha["id"], **campos})
    return linhas


def contar_vendas_do_dia(context):
    return len(vendas_na_lista(context.test.client.get("/vendas/")))


def confirmar(context, dados):
    context.vendas_antes = contar_vendas_do_dia(context)
    context.resposta = context.test.client.post("/vendas/", dados, follow=True)


@when("confirma a venda")
@when("confirma a venda sem adicionar produto")
@when("confirma a venda sem escolher a forma de pagamento")
def step_confirma(context):
    dados = {
        "item": itens_ocultos(montagem(context)),
        "forma": getattr(context, "forma", ""),
        "valor_recebido": getattr(context, "valor_recebido", ""),
    }
    confirmar(context, dados)


@when('informa o valor recebido "{recebido}"')
def step_valor_recebido_texto(context, recebido):
    context.valor_recebido = "" if recebido == "(vazio)" else recebido


@when(
    'o operador envia uma venda de {quantidade:d} "{nome:Nome}" em "{forma}" '
    "com valor recebido de R$ {valor}"
)
def step_envia_venda(context, quantidade, nome, forma, valor):
    produto = Produto.objects.get(nome=nome)
    dados = {"item": f"{produto.pk}:{quantidade}", "forma": forma, "valor_recebido": valor}
    confirmar(context, dados)


@then('o sistema recusa a venda com a mensagem "{mensagem}"')
def step_recusa_venda(context, mensagem):
    assert context.resposta.status_code == 422, context.resposta.status_code
    step_mostra_mensagem(context, mensagem)


@then('a venda em montagem continua com {quantidade:d} "{nome:Nome}"')
def step_montagem_continua(context, quantidade, nome):
    context.montagem = pagina(context.resposta)
    linhas = [(linha["nome"], linha["quantidade"]) for linha in linhas_da_montagem(context)]
    assert linhas == [(nome, str(quantidade))], linhas


@when('o operador escolhe a forma de pagamento "{forma}"')
def step_operador_forma(context, forma):
    context.forma = forma


@when("o operador abre a tela de nova venda")
def step_abre_nova(context):
    context.resposta = context.test.client.get("/vendas/nova/")
    context.montagem = pagina(context.resposta)


@then("a tela mostra o troco de R$ {valor}")
def step_mostra_troco(context, valor):
    assert f"Troco: R$ {valor}" in texto(context.resposta), texto(context.resposta)


def achar_venda(context, total, forma):
    linhas = vendas_na_lista(context.resposta)
    achadas = [v for v in linhas if v["total"] == f"R$ {total}" and v["forma"] == forma]
    assert achadas, linhas
    context.venda = achadas[0]  # a mais recente: a lista vem da mais nova para a mais antiga
    return context.venda


@then('a lista do dia mostra uma venda de R$ {total} em "{forma}"')
def step_lista_do_dia(context, total, forma):
    achar_venda(context, total, forma)


@then('a lista do dia mostra uma venda de R$ {total} em "{forma}" com {itens:d} itens')
def step_lista_do_dia_itens(context, total, forma, itens):
    venda = achar_venda(context, total, forma)
    assert venda["itens"] == f"{itens} itens", venda


@then("essa venda não mostra valor recebido nem troco")
def step_sem_recebido_troco(context):
    assert "recebido" not in context.venda and "troco" not in context.venda, context.venda


@then("a lista do dia não mostra venda nova")
def step_sem_venda_nova(context):
    assert contar_vendas_do_dia(context) == context.vendas_antes


@then('o sistema recusa uma venda enviada com "{nome:Nome}" com a mensagem "{mensagem}"')
def step_recusa_produto(context, nome, mensagem):
    produto = Produto.objects.get(nome=nome)
    antes = contar_vendas_do_dia(context)
    resposta = context.test.client.post("/vendas/", {"item": f"{produto.pk}:1", "forma": "Pix"})
    assert resposta.status_code == 422, resposta.status_code
    context.resposta = resposta
    step_mostra_mensagem(context, mensagem)
    assert contar_vendas_do_dia(context) == antes


# ---------- Histórico ----------


def registrar_pela_tela(context, itens, forma):
    """Faz uma venda inteira pela tela e devolve a linha dela na lista do dia.

    Em dinheiro, o cliente paga o valor exato (o total que a montagem mostra).
    """
    context.montagem = None
    for quantidade, nome in itens:
        adicionar(context, quantidade, nome)
    context.forma = forma
    context.valor_recebido = ""
    if forma == "Dinheiro":
        total = montagem(context).select_one(".montagem .total").get_text(strip=True)
        context.valor_recebido = total.removeprefix("R$ ")
    step_confirma(context)
    assert context.resposta.status_code == 200, context.resposta.status_code
    context.venda = vendas_na_lista(context.resposta)[0]
    return context.venda


def venda_na_lista(context, url="/vendas/"):
    linhas = vendas_na_lista(context.test.client.get(url))
    return next((v for v in linhas if v["id"] == context.venda["id"]), None)


@given('que o operador confirmou uma venda de {quantidade:d} "{nome:Nome}" em "{forma}"')
def step_confirmou_venda(context, quantidade, nome, forma):
    registrar_pela_tela(context, [(quantidade, nome)], forma)


@when('o operador altera o preço de "{nome:Nome}" para R$ {preco}')
def step_altera_preco(context, nome, preco):
    tela = pagina(context.test.client.get("/produtos/"))
    linha = next(li for li in tela.select(".produto") if li.select_one(".nome").text == nome)
    acao = linha.select_one("form.alterar-preco")["action"]
    context.resposta = context.test.client.post(acao, {"acao": "preco", "preco": preco})
    assert context.resposta.status_code == 302, context.resposta.status_code


@then("a venda já confirmada continua mostrando total de R$ {total}")
def step_venda_mantem_total(context, total):
    venda = venda_na_lista(context)
    assert venda and venda["total"] == f"R$ {total}", venda


@then('uma venda nova de {quantidade:d} "{nome:Nome}" mostra total de R$ {total}')
def step_venda_nova_total(context, quantidade, nome, total):
    venda = registrar_pela_tela(context, [(quantidade, nome)], "Pix")
    assert venda["total"] == f"R$ {total}", venda


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
    assert contar_vendas_do_dia(context) == 0


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


# ---------- Consulta do dia ----------

BRASILIA = ZoneInfo("America/Sao_Paulo")


def acertar_relogio(context, momento):
    """Fixa timezone.now() no momento dado até o fim do cenário."""
    if getattr(context, "relogio", None) is None:
        patcher = mock.patch("django.utils.timezone.now")
        context.relogio = patcher.start()
        context.add_cleanup(patcher.stop)
    context.relogio.return_value = momento


def em_brasilia(data, hora="20:00"):
    return datetime.strptime(f"{data} {hora}", "%d/%m/%Y %H:%M").replace(tzinfo=BRASILIA)


def url_do_dia(data):
    return "/vendas/?dia=" + datetime.strptime(data, "%d/%m/%Y").strftime("%Y-%m-%d")


def ler_itens_da_tabela(texto_itens):
    """'2 Chopp 300 ml e 1 Água 500 ml' → [(2, 'Chopp 300 ml'), (1, 'Água 500 ml')]"""
    itens = []
    for parte in texto_itens.split(" e "):
        quantidade, nome = parte.strip().split(" ", 1)
        itens.append((int(quantidade), nome))
    return itens


@given("que no dia de operação {data} o operador confirmou as vendas:")
def step_vendas_do_dia(context, data):
    for minuto, linha in enumerate(context.table):
        acertar_relogio(context, em_brasilia(data, f"20:{minuto:02d}"))
        context.vendas = getattr(context, "vendas", [])
        context.vendas.append(
            registrar_pela_tela(context, ler_itens_da_tabela(linha["itens"]), linha["forma"])
        )


@given(
    'que o operador confirmou uma venda de {quantidade:d} "{nome:Nome}" em "{forma}" '
    "às {hora} de {data}"
)
def step_venda_em_horario(context, quantidade, nome, forma, hora, data):
    acertar_relogio(context, em_brasilia(data, hora))
    registrar_pela_tela(context, [(quantidade, nome)], forma)


@when("o operador consulta o dia de operação {data}")
def step_consulta_dia(context, data):
    context.resposta = context.test.client.get(url_do_dia(data))
    assert context.resposta.status_code == 200, context.resposta.status_code


@then("a tela mostra {quantidade:d} vendas e total geral de R$ {total}")
def step_resumo_do_dia(context, quantidade, total):
    tela = pagina(context.resposta)
    resumo = (tela.select_one(".qtd-vendas").text, tela.select_one(".total-geral").text)
    assert resumo == (str(quantidade), f"R$ {total}"), resumo


def totais_por_forma(resposta):
    return {
        linha.select_one("th").get_text(strip=True): linha.select_one("td").get_text(strip=True)
        for linha in pagina(resposta).select("#totais-por-forma tbody tr")
    }


@then("a tela mostra os totais por forma de pagamento:")
def step_totais_por_forma(context):
    esperado = {linha["forma"]: f"R$ {linha['total']}" for linha in context.table}
    assert totais_por_forma(context.resposta) == esperado, totais_por_forma(context.resposta)


@then("essa venda aparece na lista")
def step_venda_aparece(context):
    ids = [v["id"] for v in vendas_na_lista(context.resposta)]
    assert context.venda["id"] in ids, ids


@then("ela não aparece na consulta do dia de operação {data}")
def step_venda_nao_aparece(context, data):
    resposta = context.test.client.get(url_do_dia(data))
    assert resposta.status_code == 200, resposta.status_code
    ids = [v["id"] for v in vendas_na_lista(resposta)]
    assert context.venda["id"] not in ids, ids


# ---------- Cancelamento ----------

VENDAS_DO_CA_12 = [
    ([(2, "Chopp 300 ml"), (1, "Água 500 ml")], "Pix"),
    ([(3, "Cerveja lata 350 ml")], "Dinheiro"),
    ([(1, "Chopp 300 ml")], "Crédito"),
    ([(1, "Cerveja lata 350 ml")], "Pix"),
]


def url_de_cancelamento(venda):
    return f"/vendas/{venda['id'].removeprefix('venda-')}/cancelamento/"


def cancelar_pela_tela(context, motivo):
    """Usa o formulário de cancelamento que a lista do dia mostra na linha da venda."""
    tela = pagina(context.test.client.get("/vendas/"))
    formulario = tela.select_one(f"#{context.venda['id']} form.cancelar")
    assert formulario, f"a lista não oferece cancelar {context.venda['id']}"
    resposta = context.test.client.post(formulario["action"], {"motivo": motivo}, follow=True)
    context.resposta = resposta


@given("o dia de operação do CA-12")
def step_dia_do_ca12(context):
    for minuto, (itens, forma) in enumerate(VENDAS_DO_CA_12):
        acertar_relogio(context, em_brasilia("01/10/2026", f"20:{minuto:02d}"))
        registrar_pela_tela(context, itens, forma)


@when('o operador cancela a venda em "{forma}" com o motivo "{motivo}"')
def step_cancela(context, forma, motivo):
    linhas = vendas_na_lista(context.test.client.get("/vendas/"))
    context.venda = next(v for v in linhas if v["forma"] == forma)
    cancelar_pela_tela(context, motivo)
    assert context.resposta.status_code == 200, context.resposta.status_code


@when("o operador tenta cancelar essa venda sem informar motivo")
def step_cancela_sem_motivo(context):
    cancelar_pela_tela(context, "")


@given("que existe uma venda Confirmada no dia de operação anterior ao corrente")
def step_venda_dia_anterior(context):
    acertar_relogio(context, em_brasilia("01/10/2026", "20:00"))
    registrar_pela_tela(context, [(1, "Chopp 300 ml")], "Pix")
    context.dia_da_venda = "01/10/2026"
    acertar_relogio(context, em_brasilia("02/10/2026", "20:00"))


@when('o operador tenta cancelar essa venda com o motivo "{motivo}"')
def step_tenta_cancelar(context, motivo):
    # A lista do dia corrente não oferece o botão; a requisição vai direto à rota.
    url = url_de_cancelamento(context.venda)
    context.resposta = context.test.client.post(url, {"motivo": motivo})


@given('que o operador cancelou uma venda com o motivo "{motivo}"')
def step_cancelou(context, motivo):
    registrar_pela_tela(context, [(1, "Chopp 300 ml")], "Pix")
    context.motivo = motivo
    cancelar_pela_tela(context, motivo)
    assert context.resposta.status_code == 200, context.resposta.status_code


@when("o operador tenta cancelar a mesma venda de novo")
def step_cancela_de_novo(context):
    url = url_de_cancelamento(context.venda)
    context.resposta = context.test.client.post(url, {"motivo": context.motivo})


@then('a lista do dia mostra essa venda marcada como "{situacao}"')
@then('a lista do dia mostra essa venda como "{situacao}"')
def step_situacao_na_lista(context, situacao):
    venda = venda_na_lista(context)
    assert venda and venda["situacao"] == situacao, venda


@then('a consulta daquele dia mostra essa venda como "{situacao}"')
def step_situacao_naquele_dia(context, situacao):
    venda = venda_na_lista(context, url_do_dia(context.dia_da_venda))
    assert venda and venda["situacao"] == situacao, venda


@then('a tela mostra total em "{forma}" de R$ {total}')
def step_total_da_forma(context, forma, total):
    totais = totais_por_forma(context.resposta)
    assert totais[forma] == f"R$ {total}", totais


# ---------- Produtos ----------


@when('o operador cadastra o produto "{nome:Nome}" com preço R$ {preco}')
def step_cadastra_produto(context, nome, preco):
    context.resposta = context.test.client.post("/produtos/", {"nome": nome, "preco": preco})
