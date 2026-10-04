import pytest

from vendas.regras import (
    calcular_total,
    calcular_troco,
    formatar_reais,
    ler_itens,
    para_centavos,
    preco_valido,
)


def test_total_e_soma_dos_subtotais():
    assert calcular_total([(3, 600)]) == 1800
    assert calcular_total([(1, 800), (1, 400)]) == 1200


@pytest.mark.parametrize(
    ("total", "recebido", "troco"),
    [(1800, 2000, 200), (1200, 5000, 3800), (1800, 1800, 0), (1800, 1801, 1)],
)
def test_troco_em_dinheiro(total, recebido, troco):
    assert calcular_troco(total, recebido) == troco


@pytest.mark.parametrize(
    ("texto", "centavos"),
    [
        ("8,00", 800),
        ("R$ 1.000,00", 100000),
        ("999,99", 99999),
        ("10", 1000),
        ("10,5", 1050),
        ("0,01", 1),
        ("", None),
        ("-1", None),
        ("1,234", None),
        ("abc", None),
    ],
)
def test_para_centavos(texto, centavos):
    assert para_centavos(texto) == centavos


@pytest.mark.parametrize(
    ("centavos", "valido"), [(None, False), (0, False), (1, True), (99999, True), (100000, False)]
)
def test_faixa_de_preco(centavos, valido):
    assert preco_valido(centavos) is valido


def test_formatar_reais():
    assert formatar_reais(123456) == "1.234,56"
    assert formatar_reais(5) == "0,05"


def test_mesmo_produto_soma_na_linha_existente():
    assert ler_itens(["1:2", "2:1", "1:1"]) == [(1, 3), (2, 1)]


@pytest.mark.parametrize(
    "valores", [["1:0"], ["1:-1"], ["1:100"], ["1:98", "1:2"], ["1:abc"], ["x:1"], ["1"]]
)
def test_quantidade_fora_de_1_a_99_e_recusada(valores):
    assert ler_itens(valores) is None


def test_limite_de_99_somado_e_aceito():
    assert ler_itens(["1:98", "1:1"]) == [(1, 99)]
