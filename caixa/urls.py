from django.urls import path

from . import views

urlpatterns = [
    path("caixa/", views.conferencia),
    path("caixa/conferencia/", views.conferir),
]
