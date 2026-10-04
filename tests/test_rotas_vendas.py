"""Recusas das rotas de /vendas/ previstas na seção 7 da spec 001 que não têm CA próprio."""

import pytest
from django.contrib.auth import get_user_model

pytestmark = pytest.mark.django_db


@pytest.fixture
def operador(client):
    client.force_login(get_user_model().objects.create_user("operador", password="x"))
    return client


def test_consulta_com_dia_invalido_responde_422(operador):
    resposta = operador.get("/vendas/?dia=01/10/2026")
    assert resposta.status_code == 422
    assert "Informe o dia no formato AAAA-MM-DD" in resposta.content.decode()


def test_cancelar_venda_inexistente_responde_404(operador):
    resposta = operador.post("/vendas/999/cancelamento/", {"motivo": "Erro de lançamento"})
    assert resposta.status_code == 404
