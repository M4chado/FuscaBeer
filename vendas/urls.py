from django.urls import path

from . import views

urlpatterns = [
    path("vendas/nova/", views.nova),
    path("vendas/", views.vendas),
    path("produtos/", views.produtos),
    path("produtos/<int:pk>/", views.produto),
]
