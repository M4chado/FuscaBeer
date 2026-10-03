import pytest

from vendas.regras import calcular_total, calcular_troco


def test_total_e_soma_dos_subtotais():
    assert calcular_total([(3, 600)]) == 1800
    assert calcular_total([(1, 800), (1, 400)]) == 1200


@pytest.mark.parametrize(
    ("total", "recebido", "troco"),
    [(1800, 2000, 200), (1200, 5000, 3800), (1800, 1800, 0), (1800, 1801, 1)],
)
def test_troco_em_dinheiro(total, recebido, troco):
    assert calcular_troco(total, recebido) == troco
