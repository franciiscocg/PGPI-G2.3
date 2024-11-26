from django.db import models
import datetime


class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    foto = models.URLField(max_length=500, blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad_almacen = models.IntegerField()
    fabricante = models.CharField(max_length=255)
    material = models.CharField(max_length=255, default='Material no especificado')
    tipo = models.CharField(max_length=100)
    fecha = models.DateField(default=datetime.date(2024,1,1))

    def __str__(self):
        return self.nombre
