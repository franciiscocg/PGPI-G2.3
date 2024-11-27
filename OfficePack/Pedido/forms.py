from django import forms
from .models import Pedido


class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['email', 'importe', 'direccion', 'estado', 'metodo_pago']
