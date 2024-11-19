from django.urls import path
from . import views
urlpatterns = [
    path('', views.listar_pedido, name='listar_pedido'),
    path('crear/', views.crear_pedido, name='crear_pedido'),
    path('actualizar/<int:pk>/', views.actualizar_pedido, name='actualizar_pedido'),
    path('eliminar/<int:pk>/', views.eliminar_pedido, name='eliminar_pedido'),
]