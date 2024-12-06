from django.db import models
import datetime
from django.utils import timezone


class Producto(models.Model):
    class TipoChoices(models.TextChoices):
        MUEBLE = 'MUEBLE', 'Mueble'
        ELECTRONICO = 'ELECTRONICO', 'Electronico'
        DECORACION = 'DECORACION', 'Decoracion'
        
    nombre = models.CharField(max_length=255)
    foto = models.URLField(max_length=500, blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad_almacen = models.IntegerField()
    fabricante = models.CharField(max_length=255)
    material = models.CharField(max_length=255)
    tipo = models.CharField(max_length=100)
    fecha = models.DateField(default=timezone.now)

    def __str__(self):
        return self.nombre