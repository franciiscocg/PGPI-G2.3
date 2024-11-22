from .models import Producto_pedido
from django.db import models
from django.shortcuts import get_object_or_404


# módulo que realizará consultas a la bbdd
class Producto_pedidoManager(models.Manager):
    def getAll():
        return list(Producto_pedido.objects.values())

    def getById(id):
        return get_object_or_404(Producto_pedido, id == id)

    def save(prod_ped: Producto_pedido):
        return Producto_pedido.objects.update_or_create(id=prod_ped.id,
                                                        create_defaults={
                                                            "producto": prod_ped.producto,
                                                            "pedido": prod_ped.pedido,
                                                            "cantidad": prod_ped.cantidad
                                                            }
                                                        )

    def delete(prod_ped: Producto_pedido):
        try:
            print()
        except Exception as e:
            print(e)

    def getByPedido(pedido_id: int):
        return list(Producto_pedido.objects.filter(pedido=pedido_id))

    def getByProducto(producto_id: int):
        return list(Producto_pedido.objects.filter(producto=producto_id))

    def getByUser(user_email: str):
        return list(Producto_pedido.objects.filter(email=user_email))
    