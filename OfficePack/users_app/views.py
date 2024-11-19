from django.shortcuts import render, redirect
from django.contrib.auth import login as log
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            log(request, user)  # Inicia sesión automáticamente
            return redirect('producto/')  # Redirige a la página principal
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        fotm = AuthenticationForm(data=request.post)
        if form.is_valid():
            user = form.save()
            log(request, form.get_user()) 
            return redirect('listar_producto')  # Redirige a la página principal
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})
