from datetime import UTC, date, datetime

import pytest

from vendas.regras import (
    BRASILIA,
    calcular_total,
    calcular_troco,
    dia_operacao,
    formatar_reais,
    ler_itens,
    para_centavos,
    preco_valido,
    totais_do_dia,
    validar_pagamento,
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


# Tabela de exemplos da RN-07 (spec 001), linha por linha.
@pytest.mark.parametrize(
    ("total", "forma", "recebido", "esperado"),
    [
        (1800, "Dinheiro", "20,00", (2000, 200, None)),
        (1200, "Dinheiro", "50,00", (5000, 3800, None)),
        (1800, "Dinheiro", "18,00", (1800, 0, None)),
        (1800, "Dinheiro", "18,01", (1801, 1, None)),
        (1800, "Dinheiro", "17,99", (None, None, "Valor recebido menor que o total da venda")),
        (1800, "Dinheiro", "", (None, None, "Informe o valor recebido")),
        (1800, "Pix", "20,00", (None, None, "Valor recebido só vale para pagamento em dinheiro")),
    ],
)
def test_tabela_de_exemplos_rn07(total, forma, recebido, esperado):
    assert validar_pagamento(forma, total, recebido) == esperado


@pytest.mark.parametrize("forma", ["Débito", "Crédito", "Pix"])
def test_cartao_e_pix_sem_valor_recebido_nao_tem_troco(forma):
    assert validar_pagamento(forma, 800, "") == (None, None, None)


@pytest.mark.parametrize(
    ("momento", "dia"),
    [
        (datetime(2026, 10, 1, 6, 0, tzinfo=BRASILIA), date(2026, 10, 1)),
        (datetime(2026, 10, 1, 23, 59, tzinfo=BRASILIA), date(2026, 10, 1)),
        (datetime(2026, 10, 2, 1, 30, tzinfo=BRASILIA), date(2026, 10, 1)),
        (datetime(2026, 10, 2, 5, 59, 59, tzinfo=BRASILIA), date(2026, 10, 1)),
        (datetime(2026, 10, 2, 6, 0, tzinfo=BRASILIA), date(2026, 10, 2)),
        (datetime(2026, 10, 2, 4, 30, tzinfo=UTC), date(2026, 10, 1)),  # 01:30 em Brasília
    ],
)
def test_dia_de_operacao_comeca_as_seis(momento, dia):
    assert dia_operacao(momento) == dia


def test_totais_do_dia_por_forma():
    vendas = [("Pix", 2000), ("Dinheiro", 1800), ("Crédito", 800), ("Pix", 600)]
    assert totais_do_dia(vendas) == {
        "quantidade": 4,
        "total": 5200,
        "por_forma": {"Dinheiro": 1800, "Débito": 0, "Crédito": 800, "Pix": 2600},
    }
