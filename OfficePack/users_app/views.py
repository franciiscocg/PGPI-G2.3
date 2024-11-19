from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Inicia sesión automáticamente
            return redirect('home')  # Redirige a la página principal
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def signout(request):
    logout(request)
    return redirect('home')


def home(request):
    return render(request, 'home.html')
