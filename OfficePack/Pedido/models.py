from django.db import models
from django.contrib.auth.models import User


class EstadoPedido(models.TextChoices):
    PENDIENTE = 'P', 'Pendiente'
    EN_PROCESO = 'EP', 'En proceso'
    ENVIADO = 'E', 'Enviado'
    ENTREGADO = 'ET', 'Entregado'
    CANCELADO = 'C', 'Cancelado'

class MetodoPago(models.TextChoices):
    TARJETA = 'T', 'Tarjeta de Crédito'
    CONTRAREEMBOLSO = 'C', 'Contra Reembolso'

class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(max_length=255)
    importe = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    direccion = models.CharField(max_length=200)
    estado = models.CharField(
        max_length=2,
        choices=EstadoPedido.choices,
        default=EstadoPedido.PENDIENTE
    )
    metodo_pago = models.CharField(
        max_length=2,
        choices=MetodoPago.choices,
        default=MetodoPago.TARJETA
    )



def __str__(self):
    return f'Pedido {self.id} - {self.email}'
