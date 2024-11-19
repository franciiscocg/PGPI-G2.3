"""
URL configuration for OfficePack project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from Pedido import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('producto/', include("Pedido.urls")),
    path('añadir/<int:producto_id>/', views.añadir_a_cesta, name='añadir_a_cesta'),
    path('cesta/', views.ver_cesta, name='ver_cesta'),
    path('realizar_pedido/', views.realizar_pedido, name='realizar_pedido'),
    path('', views.listar_productos, name='listar_productos'),
    path('catalogo', views.listar_productos, name='listar_productos'),
    path('crear_producto/', views.crear_producto, name='crear_producto'),
    path('actualizar_producto/<int:id>/', views.actualizar_producto, name='actualizar_producto'),
    path('eliminar_producto/<int:id>/', views.eliminar_producto, name='eliminar_producto'),
]
