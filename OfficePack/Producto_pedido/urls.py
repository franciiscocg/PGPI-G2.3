from django.urls import path
from Pedido import views as ViewsPedido

urlpatterns = [
    path('rastrear/', ViewsPedido.rastrear_pedido, name='rastrear_pedido'),
]