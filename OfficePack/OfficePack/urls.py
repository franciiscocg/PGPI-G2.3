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
from Pedido import views as viewsPedido
from Producto import views as viewsProducto
from users_app import views as viewsUser



urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', viewsUser.home, name='home'),
    path('register/', viewsUser.register),
    path('logout/', viewsUser.signout, name='signout'),
    path('login/', viewsUser.login, name='login'),
   
    path('añadir/<int:producto_id>/', viewsPedido.añadir_a_cesta, name='añadir_a_cesta'),
    path('cesta/', viewsPedido.ver_cesta, name='ver_cesta'),
    path('pagar/', viewsPedido.pagar, name='pagar'),
    path('confirmar_pago/', viewsPedido.confirmar_pago, name='confirmar_pago'),
    path('eliminar_de_cesta/<int:producto_id>/', viewsPedido.eliminar_de_cesta, name='eliminar_de_cesta'),
    
    path('catalogo/', viewsProducto.listar_productos, name='listar_productos'),
    path('crear_producto/', viewsProducto.crear_producto, name='crear_producto'),
    path('actualizar_producto/<int:id>/', viewsProducto.actualizar_producto, name='actualizar_producto'),
    path('eliminar_producto/<int:id>/', viewsProducto.eliminar_producto, name='eliminar_producto'),
]
