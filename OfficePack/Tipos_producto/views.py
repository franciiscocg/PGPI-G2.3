from django.shortcuts import render,redirect
from .models import Tipo
from django.contrib.auth.decorators import login_required, user_passes_test

def tipos(request):
    tipos = Tipo.objects.all()
    return render(request, 'tipos.html', {
        'object-list': tipos
    })

def tipo(request, slug):
    tipo = Tipo.objects.filter(slug=slug).first()
    products = Tipo.products.all()
    
    return render(request, 'tipos.html', {
        'object-list': products,
        'tipo':tipo.title
    })

@login_required
#@user_passes_test(Admin.get_user_permissions)
def TipoDeleteView(request):
    tipo = Tipo.objects.filter(slug=slug).first()
    Tipo.delete(tipo)
    return redirect('/tipos')

@login_required
#@user_passes_test(Admin.get_user_permissions)
def TipoCreateView(request):
    if request.method == 'POST':
        
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        imagen = request.FILES.get('imagen')
        
        tipo = Tipo(title = titulo, description = descripcion, image = imagen)
        tipo.save()
        return redirect('/tipos')
    return render(request, 'createTipo.html')

@login_required
#@user_passes_test(Admin.get_user_permissions)
def TipoEditView(request, slug):
    tipo = Tipo.objects.filter(slug=slug).first()
    if request.methos == 'POST':
        
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        imagen = request.FILES.get('imagen')
        
        tipo.title = titulo
        tipo.description = descripcion
        tipo.image = imagen
        
        tipo.save()
        return redirect('/tipos')
    return render(request, 'editTipo.html', {
        'tipo':tipo
    })