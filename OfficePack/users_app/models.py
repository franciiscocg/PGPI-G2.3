from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    direccion = models.CharField(max_length=255, blank=True, null=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Cambia el related_name para evitar conflictos
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # Cambia el related_name para evitar conflictos
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )