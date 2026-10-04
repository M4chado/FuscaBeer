"""RN-13 na reativação e RN-12 na alteração de preço (escopo 1 da spec 001)."""

import pytest
from django.contrib.auth import get_user_model

from vendas.models import Produto

pytestmark = pytest.mark.django_db


@pytest.fixture
def operador(client):
    client.force_login(get_user_model().objects.create_user("operador", password="x"))
    return client


def test_reativar_recusa_nome_em_uso_por_outro_ativo(operador):
    antigo = Produto.objects.create(nome="Chopp 300 ml", preco_centavos=800, ativo=False)
    Produto.objects.create(nome="CHOPP 300 ML", preco_centavos=900)
    resposta = operador.post(f"/produtos/{antigo.pk}/", {"acao": "reativar"})
    assert resposta.status_code == 422
    assert "Já existe um produto ativo com este nome" in resposta.content.decode()
    antigo.refresh_from_db()
    assert antigo.ativo is False


def test_inativar_e_reativar(operador):
    chopp = Produto.objects.create(nome="Chopp 300 ml", preco_centavos=800)
    assert operador.post(f"/produtos/{chopp.pk}/", {"acao": "inativar"}).status_code == 302
    chopp.refresh_from_db()
    assert chopp.ativo is False
    assert operador.post(f"/produtos/{chopp.pk}/", {"acao": "reativar"}).status_code == 302
    chopp.refresh_from_db()
    assert chopp.ativo is True


def test_alterar_preco_fora_da_faixa_e_recusado(operador):
    chopp = Produto.objects.create(nome="Chopp 300 ml", preco_centavos=800)
    resposta = operador.post(f"/produtos/{chopp.pk}/", {"acao": "preco", "preco": "0,00"})
    assert resposta.status_code == 422
    chopp.refresh_from_db()
    assert chopp.preco_centavos == 800


def test_produto_inexistente_responde_404(operador):
    assert operador.post("/produtos/999/", {"acao": "inativar"}).status_code == 404
