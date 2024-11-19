from django.shortcuts import render, redirect
from django.contrib.auth import login as log
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.http import HttpResponse


def register(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            user = form.save()
            log(request, user)  # Inicia sesión automáticamente
            return redirect('producto/')  # Redirige a la página principal
    else:
        form = AuthenticationForm()
    return render(request, 'registration/register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.post)
        if form.is_valid():
            user = form.save()
            log(request, user) 
            return redirect('listar_producto')  # Redirige a la página principal
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def signout(request):
    logout(request)
    return redirect('home')


def home(request):
    return render(request, 'home.html')
