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


@login_required
@require_GET
def conferencia(request):
    """GET /caixa/?dia=AAAA-MM-DD: conferência de um dia de operação (sem parâmetro: corrente)."""
    texto_dia = request.GET.get("dia")
    dia = date.fromisoformat(texto_dia) if texto_dia else dia_operacao(timezone.now())
    fechamento = Fechamento.objects.filter(dia_operacao=dia).first()
    esperado = fechamento.esperado if fechamento else esperado_do_dia(dia)
    linhas = [
        {
            "forma": forma,
            "esperado": esperado[forma],
            "contado": fechamento.contado[forma] if fechamento else None,
            "divergencia": (
                descrever_divergencia(esperado[forma], fechamento.contado[forma])
                if fechamento
                else ""
            ),
        }
        for forma in FORMAS
    ]
    contexto = {"dia": dia, "fechamento": fechamento, "linhas": linhas}
    return render(request, "caixa/conferencia.html", contexto)


@login_required
@require_POST
def conferir(request):
    """POST /caixa/conferencia/: grava os quatro valores contados e a situação (RN-05)."""
    dia = date.fromisoformat(request.POST["dia"])
    esperado = esperado_do_dia(dia)
    contado = {forma: para_centavos(request.POST.get(f"contado_{forma}", "")) for forma in FORMAS}
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
