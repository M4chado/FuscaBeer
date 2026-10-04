from django import template

from vendas.regras import formatar_reais

register = template.Library()


@register.filter
def reais(centavos):
    """Exibe centavos no formato R$ 1.234,56 (spec 001, seção 7)."""
    return f"R$ {formatar_reais(centavos)}"
