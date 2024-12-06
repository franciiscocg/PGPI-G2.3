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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from Pedido import views as viewsPedido
from Producto import views as viewsProducto
from users_app import views as viewsUser
from Producto_pedido import views as viewsProducto_pedido


urlpatterns = [
    path('admin/', admin.site.urls),
    path('gestionar_usuarios/', viewsUser.gestionar_usuarios, name='gestionar_usuarios'),
    path('gestionar_usuarios/editar/<int:user_id>/', viewsUser.editar_usuario, name='editar_usuario'),
    path('gestionar_usuarios/eliminar/<int:user_id>/', viewsUser.eliminar_usuario, name='eliminar_usuario'),

    path('', viewsUser.home, name='home'),
    path('register/', viewsUser.register, name='register'),
    path('logout/', viewsUser.signout, name='signout'),
    path('login/', viewsUser.login, name='login'),
    path('perfil/', viewsUser.profile, name='profile'),
    path('editar_perfil/<int:user_id>', viewsUser.edit_profile, name='edit_profile'),

    path('pedidos/', viewsPedido.listar_pedidos, name='listar_pedidos'),
    path('mis_pedidos/', viewsPedido.listar_mis_pedidos, name='listar_mis_pedidos'),
    path('pedido/<int:pedido_id>/', viewsPedido.mostrar_pedido, name='mostrar_pedido'),
    path('añadir/<int:producto_id>/', viewsPedido.añadir_a_cesta, name='añadir_a_cesta'),
    path('cesta/', viewsPedido.ver_cesta, name='ver_cesta'),
    path('pagar/', viewsPedido.pagar, name='pagar'),
    path('confirmar_pago/', viewsPedido.confirmar_pago, name='confirmar_pago'),
    path('eliminar_de_cesta/<int:producto_id>/', viewsPedido.eliminar_de_cesta, name='eliminar_de_cesta'),
    path('aumentar_cantidad/<int:producto_id>/', viewsPedido.aumentar_cantidad_producto_en_cesta, name='aumentar_cantidad_producto_en_cesta'),
    path('disminuir_cantidad/<int:producto_id>/', viewsPedido.disminuir_cantidad_producto_en_cesta, name='disminuir_cantidad_producto_en_cesta'),
    path('obtener_cesta/', viewsPedido.obtener_cesta, name='obtener_cesta'),

    path('producto/<int:producto_id>/', viewsProducto.mostrar_producto, name='mostrar_producto'),
    path('catalogo/', viewsProducto.listar_productos, name='listar_productos'),
    path('catalogo/buscar/', viewsProducto.buscar_por_nombre, name='buscar_por_nombre'),
    path('gestionar_productos/buscar/', viewsProducto.buscar_por_nombre_gestionar, name='buscar_por_nombre_gestionar'),
    
    path('gestionar_productos/', viewsProducto.gestionar_productos, name='gestionar_productos'),
    path('gestionar_productos/actualizar_producto/<int:producto_id>', viewsProducto.actualizar_producto, name='actualizar_producto'),
    path('gestionar_productos/eliminar_producto/<int:producto_id>', viewsProducto.eliminar_producto, name='eliminar_producto'),
    path('gestionar_productos/crear_producto/', viewsProducto.crear_producto, name='crear_producto'),
    
    path('gestionar_pedidos/', viewsPedido.listar_pedidos, name='gestionar_pedidos'),
    path('gestionar_pedidos/actualizar_pedido/<int:pedido_id>', viewsPedido.actualizar_pedido, name='actualizar_pedido'),
    path('gestionar_pedidos/eliminar_pedido/<int:pedido_id>', viewsPedido.eliminar_pedido, name='eliminar_pedido'),
    path('gestionar_pedidos/crear_pedido/', viewsPedido.crear_pedido, name='crear_pedido'),

    path('rastrear/', viewsProducto_pedido.rastrear_pedido, name='rastrear_pedido'),
    path('rastrear/cambiar_direccion/<int:pedido_id>', viewsProducto_pedido.cambiar_direccion, name='cambiar_direccion'),
    path('compra_rapida/<int:producto_id>/', viewsProducto.compra_rapida, name='compra_rapida'),



    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
