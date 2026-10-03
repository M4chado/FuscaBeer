import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Produto",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("nome", models.CharField(max_length=60)),
                ("preco_centavos", models.PositiveIntegerField()),
                ("ativo", models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name="Venda",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("criada_em", models.DateTimeField()),
                ("dia_operacao", models.DateField()),
                (
                    "forma",
                    models.CharField(
                        choices=[
                            ("Dinheiro", "Dinheiro"),
                            ("Débito", "Débito"),
                            ("Crédito", "Crédito"),
                            ("Pix", "Pix"),
                        ],
                        max_length=10,
                    ),
                ),
                ("total_centavos", models.PositiveIntegerField()),
                ("recebido_centavos", models.PositiveIntegerField(blank=True, null=True)),
                ("troco_centavos", models.PositiveIntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="ItemVenda",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("nome", models.CharField(max_length=60)),
                ("quantidade", models.PositiveSmallIntegerField()),
                ("preco_unitario_centavos", models.PositiveIntegerField()),
                ("subtotal_centavos", models.PositiveIntegerField()),
                (
                    "produto",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="vendas.produto"
                    ),
                ),
                (
                    "venda",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="itens",
                        to="vendas.venda",
                    ),
                ),
            ],
        ),
    ]
