from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from django.contrib.auth import login as log
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as log_out

from .forms import CustomUserCreationForm


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            log(request, user)  # Inicia sesión automáticamente
            return redirect('productos/')  # Redirige a la página principal
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.post)
        if form.is_valid():
            log(request, form.get_user())
            return redirect('productos/')  # Redirige a los productos
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout(request):
    log_out(request)  # Cierra la sesión del usuario
    return HttpResponseRedirect('/productos/')


@login_required
def profile(request):
    user = request.user  # Obtén el usuario logueado
    return render(request, 'profile.html', {'user': user})
