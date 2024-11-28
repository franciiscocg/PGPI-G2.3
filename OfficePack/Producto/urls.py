from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_productos, name='lista_productos'),
    path('mostrar_producto/<int:producto_id>', views.mostrar_producto, name='mostrar_productos')
]
