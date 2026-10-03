from django.db import models


class Produto(models.Model):
    nome = models.CharField(max_length=60)
    preco_centavos = models.PositiveIntegerField()
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome


class Venda(models.Model):
    DINHEIRO = "Dinheiro"
    FORMAS = [(f, f) for f in (DINHEIRO, "Débito", "Crédito", "Pix")]

    criada_em = models.DateTimeField()
    dia_operacao = models.DateField()
    forma = models.CharField(max_length=10, choices=FORMAS)
    total_centavos = models.PositiveIntegerField()
    recebido_centavos = models.PositiveIntegerField(null=True, blank=True)
    troco_centavos = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"Venda {self.pk} ({self.forma})"


class ItemVenda(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE, related_name="itens")
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    nome = models.CharField(max_length=60)
    quantidade = models.PositiveSmallIntegerField()
    preco_unitario_centavos = models.PositiveIntegerField()
    subtotal_centavos = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantidade} {self.nome}"
