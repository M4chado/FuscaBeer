"""RS-04 e RN-15: nenhuma rota de /produtos/ ou /vendas/ atende sem sessão."""

import pytest

ROTAS = [
    ("get", "/vendas/nova/"),
    ("get", "/vendas/"),
    ("post", "/vendas/"),
]


@pytest.mark.parametrize(("metodo", "rota"), ROTAS)
def test_rota_sem_sessao_vai_para_o_login(client, metodo, rota):
    resposta = getattr(client, metodo)(rota)
    assert resposta.status_code == 302
    assert resposta["Location"].startswith("/login/")
