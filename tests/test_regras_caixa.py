import pytest


# Tabela de exemplos da RN-04 (spec 002). O import fica no teste para que, enquanto a regra não
# existe, só estes casos falhem, e não a coleta do pytest inteiro.
@pytest.mark.parametrize(
    ("esperado", "contado", "exibicao"),
    [
        (1800, 1800, ""),
        (1800, 1600, "Falta de R$ 2,00"),
        (2600, 3000, "Sobra de R$ 4,00"),
        (1800, 1799, "Falta de R$ 0,01"),
        (1800, 1801, "Sobra de R$ 0,01"),
        (0, 0, ""),
    ],
)
def test_divergencia_e_contado_menos_esperado(esperado, contado, exibicao):
    from caixa.regras import descrever_divergencia

    assert descrever_divergencia(esperado, contado) == exibicao
