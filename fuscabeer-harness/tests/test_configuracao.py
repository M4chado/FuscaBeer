"""Testes da base do projeto (sem feature). Garantem que a configuração da spec 001 está ativa."""

from django.conf import settings


def test_fuso_horario_de_brasilia():
    assert settings.TIME_ZONE == "America/Sao_Paulo"
    assert settings.USE_TZ is True


def test_banco_e_postgresql():
    assert settings.DATABASES["default"]["ENGINE"] == "django.db.backends.postgresql"
