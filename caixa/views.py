from datetime import date

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.http import require_GET, require_POST

from vendas.models import Venda
from vendas.regras import FORMAS, dia_operacao, para_centavos, totais_do_dia

from .models import Fechamento
from .regras import descrever_divergencia


def esperado_do_dia(dia):
    """RN-02: total das vendas Confirmadas do dia, por forma (o mesmo da RN-14 da spec 001)."""
    vendas = Venda.objects.filter(dia_operacao=dia, situacao=Venda.CONFIRMADA)
    return totais_do_dia([(v.forma, v.total_centavos) for v in vendas])["por_forma"]


def linhas_da_conferencia(dia, fechamento):
    """Uma linha por forma. Sem conferência, só o esperado atual; com ela, o esperado guardado,
    o contado e a divergência (RN-04, RN-07)."""
    if fechamento is None:
        esperado = esperado_do_dia(dia)
        return [
            {"forma": forma, "esperado": esperado[forma], "contado": None, "divergencia": ""}
            for forma in FORMAS
        ]
    return [
        {
            "forma": forma,
            "esperado": fechamento.esperado[forma],
            "contado": fechamento.contado[forma],
            "divergencia": descrever_divergencia(
                fechamento.esperado[forma], fechamento.contado[forma]
            ),
        }
        for forma in FORMAS
    ]


def tela_conferencia(request, dia, erros=(), status=200):
    fechamento = Fechamento.objects.filter(dia_operacao=dia).first()
    linhas = linhas_da_conferencia(dia, fechamento)
    contexto = {"dia": dia, "fechamento": fechamento, "linhas": linhas, "erros": erros}
    return render(request, "caixa/conferencia.html", contexto, status=status)


@login_required
@require_GET
def conferencia(request):
    """GET /caixa/?dia=AAAA-MM-DD: conferência de um dia de operação (sem parâmetro: corrente)."""
    texto_dia = request.GET.get("dia")
    dia = date.fromisoformat(texto_dia) if texto_dia else dia_operacao(timezone.now())
    return tela_conferencia(request, dia)


@login_required
@require_POST
def conferir(request):
    """POST /caixa/conferencia/: grava os quatro valores contados e a situação (RN-05)."""
    dia = date.fromisoformat(request.POST["dia"])
    contado = {forma: para_centavos(request.POST.get(f"contado_{forma}", "")) for forma in FORMAS}
    # RN-03: as quatro formas precisam de valor contado; nada é gravado se faltar algum.
    erros = [f"Informe o valor contado de {forma}" for forma in FORMAS if contado[forma] is None]
    if erros:
        return tela_conferencia(request, dia, erros, status=422)
    esperado = esperado_do_dia(dia)
    situacao = Fechamento.FECHADO if contado == esperado else Fechamento.PENDENTE
    Fechamento.objects.update_or_create(
        dia_operacao=dia,
        defaults={
            "situacao": situacao,
            "esperado": esperado,
            "contado": contado,
            "conferido_em": timezone.now(),
        },
    )
    return redirect(f"/caixa/?dia={dia.isoformat()}")
