def calcular_total(itens):
    """RN-05: total = soma de quantidade × preço unitário, em centavos."""
    return sum(quantidade * preco for quantidade, preco in itens)


def calcular_troco(total, recebido):
    """RN-07: troco = valor recebido − total, em centavos."""
    return recebido - total


def formatar_reais(centavos):
    reais, resto = divmod(centavos, 100)
    return f"{reais:,}".replace(",", ".") + f",{resto:02d}"
