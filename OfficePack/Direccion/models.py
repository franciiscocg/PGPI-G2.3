from django.db import models
from django.contrib.auth.models import User


class Direccion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    calle = models.CharField(max_length=200, default='Calle')
    pais = models.CharField(max_length=100, default='Pais')
    codigo_postal = models.IntegerField(default=00000)
    ciudad = models.CharField(max_length=100, default='Ciudad')
    
    def __str__(self):
        return f'{self.calle}, {self.ciudad}, {self.pais}'