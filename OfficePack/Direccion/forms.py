from django import forms
from .models import Direccion


class EditDireccionForm(forms.ModelForm):
    class Meta:
        model = Direccion
        fields = ['calle', 'pais', 'codigo_postal', 'ciudad']
        
    def __init__(self, *args, **kwargs):
        super(EditDireccionForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False
            
    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('calle'):
            cleaned_data['calle'] = 'Calle'
        if not cleaned_data.get('pais'):
            cleaned_data['pais'] = 'País'
        if not cleaned_data.get('codigo_postal'):
            cleaned_data['codigo_postal'] = 00000
        if not cleaned_data.get('ciudad'):
            cleaned_data['ciudad'] = 'Ciudad'
        return cleaned_data