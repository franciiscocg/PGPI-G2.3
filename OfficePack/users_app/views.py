from django.shortcuts import render, redirect

from django.contrib.auth import login as log
from django.contrib.auth import logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CustomLoginForm, CustomUserCreationForm, EditProfileForm


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            backend = 'users_app.authentication.EmailBackend'

            log(request, user, backend=backend)
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})


def login(request):

    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')  # 'username' es en realidad el correo electrónico
            password = form.cleaned_data.get('password')

            # Usar el email para autenticar
            user = authenticate(request, username=email, password=password)
            if user is not None:
                log(request, user)
                return redirect('home')  # Redirigir al home después de iniciar sesión
            else:
                form.add_error(None, "Correo electrónico o contraseña incorrectos.")  # Error en caso de fallo de autenticación
    else:
        form = CustomLoginForm()

    return render(request, 'login.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'profile.html')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/perfil/')
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})


def signout(request):
    logout(request)
    return redirect('home')


def home(request):
    return render(request, 'home.html')
