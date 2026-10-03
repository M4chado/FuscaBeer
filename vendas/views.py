from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.http import require_GET, require_http_methods

from .models import ItemVenda, Produto, Venda
from .regras import calcular_total, calcular_troco, formatar_reais


def dia_operacao(momento):
    """RN-11: o dia de operação começa às 06:00."""
    return (timezone.localtime(momento) - timedelta(hours=6)).date()


def para_centavos(texto):
    return int(texto.replace(".", "").replace(",", ""))


@login_required
@require_GET
def nova(request):
    produtos = Produto.objects.filter(ativo=True)
    return render(request, "vendas/nova.html", {"produtos": produtos, "formas": Venda.FORMAS})


def registrar(request):
    produto = Produto.objects.get(pk=request.POST["produto"], ativo=True)
    quantidade = int(request.POST["quantidade"])
    forma = request.POST["forma"]
    agora = timezone.now()
    total = calcular_total([(quantidade, produto.preco_centavos)])
    recebido = troco = None
    if forma == Venda.DINHEIRO:
        recebido = para_centavos(request.POST["valor_recebido"])
        troco = calcular_troco(total, recebido)
    with transaction.atomic():
        venda = Venda.objects.create(
            criada_em=agora,
            dia_operacao=dia_operacao(agora),
            forma=forma,
            total_centavos=total,
            recebido_centavos=recebido,
            troco_centavos=troco,
        )
        ItemVenda.objects.create(
            venda=venda,
            produto=produto,
            nome=produto.nome,
            quantidade=quantidade,
            preco_unitario_centavos=produto.preco_centavos,
            subtotal_centavos=total,
        )
    if troco is not None:
        messages.success(request, f"Troco: R$ {formatar_reais(troco)}")
    return redirect("/vendas/")


def listar(request):
    dia = dia_operacao(timezone.now())
    vendas = [
        {"total": formatar_reais(v.total_centavos), "forma": v.forma}
        for v in Venda.objects.filter(dia_operacao=dia).order_by("-criada_em")
    ]
    return render(request, "vendas/lista.html", {"vendas": vendas})


@login_required
@require_http_methods(["GET", "POST"])
def vendas(request):
    return registrar(request) if request.method == "POST" else listar(request)
