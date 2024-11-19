from .models import Pedido
from django.db import models
from django.shortcuts import get_object_or_404

# módulo que realizará consultas a la bbdd
class PedidoManager(models.Manager):
    def getAll():
        return list(Pedido.objects.values())

    def getById(id:int):
        return get_object_or_404(Pedido,id==id)

    def save(pedido:Pedido):
        return Pedido.objects.update_or_create(id=pedido.id,
                                                create_defaults={"email":pedido.email,
                                                                "direccion":pedido.direccion,
                                                                "importe":pedido.importe,
                                                                "estado":pedido.estado
                                                                }
                                                )

    def delete(pedido:Pedido):
        try:
            pedido.delete()
        except Exception as e:
            print(e)