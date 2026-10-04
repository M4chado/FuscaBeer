import re

PRECO_MINIMO = 1  # RN-12: R$ 0,01
PRECO_MAXIMO = 99999  # RN-12: R$ 999,99


def calcular_total(itens):
    """RN-05: total = soma de quantidade × preço unitário, em centavos."""
    return sum(quantidade * preco for quantidade, preco in itens)


def calcular_troco(total, recebido):
    """RN-07: troco = valor recebido − total, em centavos."""
    return recebido - total


def formatar_reais(centavos):
    reais, resto = divmod(centavos, 100)
    return f"{reais:,}".replace(",", ".") + f",{resto:02d}"


def para_centavos(texto):
    """Lê um valor em R$ no formato brasileiro ("1.234,56") e devolve centavos, ou None."""
    limpo = texto.replace("R$", "").strip().replace(".", "")
    if not re.fullmatch(r"\d+(,\d{1,2})?", limpo):
        return None
    reais, _, centavos = limpo.partition(",")
    return int(reais) * 100 + int(centavos.ljust(2, "0"))


def preco_valido(centavos):
    return centavos is not None and PRECO_MINIMO <= centavos <= PRECO_MAXIMO


QUANTIDADE_MAXIMA = 99  # RN-01


def ler_itens(valores):
    """Lê itens "id_do_produto:quantidade" e soma o mesmo produto numa linha (RN-02).

    Devolve [(id, quantidade)] na ordem em que entraram, ou None se alguma quantidade
    informada ou somada sair de 1 a 99 (RN-01).
    """
    itens = {}
    for valor in valores:
        produto, _, quantidade = valor.partition(":")
        if not produto.isdigit() or not quantidade.lstrip("-").isdigit():
            return None
        quantidade = int(quantidade)
        if not 1 <= quantidade <= QUANTIDADE_MAXIMA:
            return None
        itens[int(produto)] = itens.get(int(produto), 0) + quantidade
    if any(quantidade > QUANTIDADE_MAXIMA for quantidade in itens.values()):
        return None
    return list(itens.items())
