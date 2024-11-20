from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from django.contrib.auth import login as log
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            log(request, user)  # Inicia sesión automáticamente
            return redirect('home')  # Redirige a la página principal
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            log(request, user)
            return redirect('home')  # Redirige a la página principal
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def signout(request):
    logout(request)
    return redirect('home')


def home(request):
    return render(request, 'home.html')
