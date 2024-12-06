from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as log
from django.contrib.auth import logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import CustomLoginForm, CustomUserCreationForm, EditProfileForm
from Producto.models import Producto
from django.contrib.auth.models import User
from django.contrib import messages


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
                next_url = request.POST.get('next', 'home')
                if next_url == '':
                    next_url = 'home'
                return redirect(next_url)  # Redirigir a la URL anterior o a home
            else:
                form.add_error(None, "Correo electrónico o contraseña incorrectos.")  # Error en caso de fallo de autenticación
    else:
        form = CustomLoginForm()

    return render(request, 'login.html', {'form': form})

@login_required
def profile(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})

@login_required
def edit_profile(request, user_id):
    user = get_object_or_404(get_user_model(), id=user_id)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('/perfil/')
    else:
        form = EditProfileForm(instance=user)
    return render(request, 'edit_profile.html', {'form': form})


login_required(login_url='/login/')
@user_passes_test(lambda u: u.is_staff)
def gestionar_usuarios(request):
    usuarios = get_user_model().objects.all()
    return render(request, 'gestionar_usuarios.html', {'usuarios': usuarios})

@login_required(login_url='/login/')
@user_passes_test(lambda u: u.is_staff)
def editar_usuario(request, user_id):
    usuario = get_object_or_404(get_user_model(), id=user_id)
    if request.method == 'POST':
        usuario.username = request.POST.get('username')
        usuario.email = request.POST.get('email')
        usuario.save()
        messages.success(request, 'Usuario actualizado correctamente.')
        return redirect('gestionar_usuarios')
    return render(request, 'editar_usuario.html', {'usuario': usuario})

@login_required(login_url='/login/')
@user_passes_test(lambda u: u.is_staff)
def eliminar_usuario(request, user_id):
    usuario = get_object_or_404(get_user_model(), id=user_id)
    if request.method == 'POST':
        usuario.delete()
        messages.success(request, 'Usuario eliminado correctamente.')
        return redirect('gestionar_usuarios')
    return redirect('gestionar_usuarios')


def signout(request):
    logout(request)
    return redirect('home')


def home(request):
    ultimos_productos = Producto.objects.order_by('-fecha')[:4]  # Ajusta el número de productos según sea necesario
    return render(request, 'home.html', {'ultimos_productos': ultimos_productos})
