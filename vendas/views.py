from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.http import require_GET, require_http_methods

from .models import ItemVenda, Produto, Venda
from .regras import (
    calcular_total,
    calcular_troco,
    formatar_reais,
    ler_itens,
    para_centavos,
    preco_valido,
)


def dia_operacao(momento):
    """RN-11: o dia de operação começa às 06:00."""
    return (timezone.localtime(momento) - timedelta(hours=6)).date()


MSG_QUANTIDADE = "Informe uma quantidade de 1 a 99"
MSG_INATIVO = "Produto inativo"


def montar_linhas(itens):
    """Linhas da venda com o preço atual de cada produto; o subtotal é calculado aqui (RN-05)."""
    produtos = Produto.objects.in_bulk([produto for produto, _ in itens])
    return [
        {
            "produto": produtos[produto],
            "quantidade": quantidade,
            "subtotal": quantidade * produtos[produto].preco_centavos,
        }
        for produto, quantidade in itens
        if produto in produtos
    ]


def tela_nova(request, itens, dados, erros=(), status=200):
    linhas = montar_linhas(itens)
    contexto = {
        "produtos": Produto.objects.filter(ativo=True),
        "linhas": linhas,
        "total": sum(linha["subtotal"] for linha in linhas),
        "formas": Venda.FORMAS,
        "dados": dados,
        "erros": erros,
    }
    return render(request, "vendas/nova.html", contexto, status=status)


@login_required
@require_GET
def nova(request):
    """Tela de nova venda. Com ?produto=, adiciona o produto à venda em montagem (RN-01 a RN-03)."""
    atuais = request.GET.getlist("item")
    itens = ler_itens(atuais) or []
    erros = []
    produto = request.GET.get("produto", "")
    if produto:
        ativo = produto.isdigit() and Produto.objects.filter(pk=produto, ativo=True).exists()
        novos = ler_itens([*atuais, f"{produto}:{request.GET.get('quantidade', '')}"])
        if not ativo:
            erros.append(MSG_INATIVO)
        elif novos is None:
            erros.append(MSG_QUANTIDADE)
        else:
            itens = novos
    return tela_nova(request, itens, {}, erros, status=422 if erros else 200)


MSG_SEM_ITENS = "Adicione pelo menos um produto"
MSG_FORMA = "Escolha a forma de pagamento"


def registrar(request):
    """POST /vendas/: valida tudo antes de gravar; venda e itens entram juntos ou nada entra."""
    erros = []
    itens = ler_itens(request.POST.getlist("item"))
    if itens is None:
        erros.append(MSG_QUANTIDADE)
        itens = []
    elif not itens:
        erros.append(MSG_SEM_ITENS)
    linhas = montar_linhas(itens)
    if len(linhas) < len(itens) or any(not linha["produto"].ativo for linha in linhas):
        erros.append(MSG_INATIVO)  # RN-03
    forma = request.POST.get("forma", "")
    if forma not in dict(Venda.FORMAS):
        erros.append(MSG_FORMA)  # RN-06
    recebido = troco = None
    total = calcular_total(
        (linha["quantidade"], linha["produto"].preco_centavos) for linha in linhas
    )
    if forma == Venda.DINHEIRO:
        recebido = para_centavos(request.POST["valor_recebido"])
        troco = calcular_troco(total, recebido)
    if erros:
        return tela_nova(request, itens, request.POST, erros, status=422)

    agora = timezone.now()
    with transaction.atomic():
        venda = Venda.objects.create(
            criada_em=agora,
            dia_operacao=dia_operacao(agora),
            forma=forma,
            total_centavos=total,
            recebido_centavos=recebido,
            troco_centavos=troco,
        )
        ItemVenda.objects.bulk_create(
            ItemVenda(
                venda=venda,
                produto=linha["produto"],
                nome=linha["produto"].nome,  # RN-04: cópia do nome e do preço
                quantidade=linha["quantidade"],
                preco_unitario_centavos=linha["produto"].preco_centavos,
                subtotal_centavos=linha["subtotal"],
            )
            for linha in linhas
        )
    if troco is not None:
        messages.success(request, f"Troco: R$ {formatar_reais(troco)}")
    return redirect("/vendas/")


def listar(request):
    dia = dia_operacao(timezone.now())
    vendas = (
        Venda.objects.filter(dia_operacao=dia)
        .annotate(qtd_itens=Count("itens"))
        .order_by("-criada_em", "-pk")
    )
    return render(request, "vendas/lista.html", {"vendas": vendas, "dia": dia})


@login_required
@require_http_methods(["GET", "POST"])
def vendas(request):
    return registrar(request) if request.method == "POST" else listar(request)


# ---------- Produtos ----------

MSG_NOME = "Informe um nome de 2 a 60 caracteres"
MSG_NOME_EM_USO = "Já existe um produto ativo com este nome"
MSG_PRECO = "Informe um preço de R$ 0,01 a R$ 999,99"


def nome_em_uso(nome, exceto=None):
    """RN-13: compara sem diferenciar maiúsculas; o nome já chega sem espaços nas pontas."""
    return Produto.objects.filter(ativo=True, nome__iexact=nome).exclude(pk=exceto).exists()


def tela_produtos(request, erros=(), dados=None, status=200):
    contexto = {"produtos": Produto.objects.all(), "erros": erros, "dados": dados or {}}
    return render(request, "vendas/produtos.html", contexto, status=status)


def cadastrar_produto(request):
    nome = request.POST.get("nome", "").strip()
    preco = para_centavos(request.POST.get("preco", ""))
    erros = []
    if not 2 <= len(nome) <= 60:
        erros.append(MSG_NOME)
    elif nome_em_uso(nome):
        erros.append(MSG_NOME_EM_USO)
    if not preco_valido(preco):
        erros.append(MSG_PRECO)
    if erros:
        return tela_produtos(request, erros, request.POST, status=422)
    Produto.objects.create(nome=nome, preco_centavos=preco)
    messages.success(request, f"Produto {nome} cadastrado.")
    return redirect("/produtos/")


@login_required
@require_http_methods(["GET", "POST"])
def produtos(request):
    return cadastrar_produto(request) if request.method == "POST" else tela_produtos(request)
