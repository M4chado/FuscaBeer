from django.db import models


class Fechamento(models.Model):
    """Conferência de um dia de operação (spec 002). Valores por forma, em centavos."""

    PENDENTE, FECHADO = "Pendente", "Fechado"

    dia_operacao = models.DateField(unique=True)  # RN-01: um fechamento por dia
    situacao = models.CharField(max_length=30, choices=[(PENDENTE, PENDENTE), (FECHADO, FECHADO)])
    esperado = models.JSONField()  # {forma: centavos}, guardado na conferência (RN-02)
    contado = models.JSONField()  # {forma: centavos}, informado pelo conferente (RN-03)
    conferido_em = models.DateTimeField()

    def __str__(self):
        return f"Caixa {self.dia_operacao:%d/%m/%Y} ({self.situacao})"
