from django import forms
from .models import Pedido


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'foto', 'precio', 'cantidad_almacen', 'fabricante', 'material', 'tipo']