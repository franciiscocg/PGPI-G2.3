from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está registrado.")
        return email

class CustomLoginForm(AuthenticationForm):
    username = forms.EmailField(label="Correo electrónico", required=True)

    def clean_username(self):
        email = self.cleaned_data.get('username')
        try:
            user = get_user_model().objects.get(email=email)
        except get_user_model().DoesNotExist:
            raise forms.ValidationError("Este correo electrónico no está registrado.")
        return email

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'username', 'direccion']