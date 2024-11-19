from django.db import models
from Producto.models import Producto
from Pedido.models import Pedido


class ProductoPedido(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)


def __str__(self):
    return f'Pedido {self.cantidad} x {self.producto.nombre} en pedido {self.pedido.id}'
