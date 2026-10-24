from vendas.regras import formatar_reais


def descrever_divergencia(esperado, contado):
    """RN-04: divergência = contado − esperado, em centavos. Negativa é falta, positiva é sobra."""
    divergencia = contado - esperado
    if divergencia < 0:
        return f"Falta de R$ {formatar_reais(-divergencia)}"
    if divergencia > 0:
        return f"Sobra de R$ {formatar_reais(divergencia)}"
    return ""
