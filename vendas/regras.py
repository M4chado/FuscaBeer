import re
from datetime import timedelta
from zoneinfo import ZoneInfo

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


DINHEIRO = "Dinheiro"
MSG_RECEBIDO_VAZIO = "Informe o valor recebido"
MSG_RECEBIDO_MENOR = "Valor recebido menor que o total da venda"
MSG_RECEBIDO_FORA_DO_DINHEIRO = "Valor recebido só vale para pagamento em dinheiro"


def validar_pagamento(forma, total, recebido_texto):
    """RN-07 e RN-08. Devolve (recebido, troco, mensagem de recusa ou None), em centavos."""
    recebido_texto = recebido_texto.strip()
    if forma != DINHEIRO:
        if recebido_texto:
            return None, None, MSG_RECEBIDO_FORA_DO_DINHEIRO
        return None, None, None
    recebido = para_centavos(recebido_texto)
    if recebido is None:
        return None, None, MSG_RECEBIDO_VAZIO
    if recebido < total:
        return None, None, MSG_RECEBIDO_MENOR
    return recebido, calcular_troco(total, recebido), None


BRASILIA = ZoneInfo("America/Sao_Paulo")
FORMAS = (DINHEIRO, "Débito", "Crédito", "Pix")


def dia_operacao(momento):
    """RN-11: o dia de operação vai das 06:00 às 05:59:59 do dia seguinte, em Brasília."""
    return (momento.astimezone(BRASILIA) - timedelta(hours=6)).date()


def totais_do_dia(vendas):
    """RN-14: recebe [(forma, total)] das vendas confirmadas e devolve quantidade, total geral
    e o total de cada uma das quatro formas (zero quando a forma não teve venda)."""
    por_forma = dict.fromkeys(FORMAS, 0)
    for forma, total in vendas:
        por_forma[forma] += total
    return {"quantidade": len(vendas), "total": sum(por_forma.values()), "por_forma": por_forma}
