from datetime import date
import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProductoForm
from .models import Producto
from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_date
from django.http import HttpResponseForbidden

@login_required(login_url='/login/')
def gestionar_productos(request):
    # comprobamos que el user sea el admin
    if request.user.email != "officepack@gmail.com":
        return HttpResponseForbidden("No tienes autoridad para realizar esta operación")
    
    productos = Producto.objects.all()
    return render(request, 'gestionar_productos.html', {'productos': productos})

@login_required(login_url='/login/')
def eliminar_producto(request, producto_id):
    # comprobamos que el user sea el admin
    if request.user.email != "officepack@gmail.com":
        return HttpResponseForbidden("No tienes autoridad para realizar esta operación")
    
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        producto.delete()
        return redirect('/gestionar_productos')
    return redirect(request.META.get('HTTP_REFERER', ''))

@login_required(login_url='/login/')
def crear_producto(request):
    # comprobamos que el user sea el admin
    if request.user.email != "officepack@gmail.com":
        return HttpResponseForbidden("No tienes autoridad para realizar esta operación")
    
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/gestionar_productos/')
    else:
        form = ProductoForm()
    return render(request, 'crear_producto.html', {'form': form})

def listar_productos(request):
    productos = Producto.objects.all()
    return render(request, 'listar_productos.html', {'productos': productos})


def listar_producto(request, id):
    pedido = get_object_or_404(Producto, id=id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=pedido)
        if form.is_valid():
            form.save()
            return redirect(request.META.get('HTTP_REFERER', ''))
    else:
        form = ProductoForm(instance=pedido)
    return render(request, 'actualizar_producto.html', {'form': form})


def mostrar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'mostrar_producto.html', {'producto': producto})

@login_required(login_url='/login/')
def actualizar_producto(request, producto_id):
    # comprobamos que el user sea el admin
    if request.user.email != "officepack@gmail.com":
        return HttpResponseForbidden("No tienes autoridad para realizar esta operación")
    
    pedido = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=pedido)
        if form.is_valid():
            form.save()
            return redirect('/gestionar_productos/')
    else:
        form = ProductoForm(instance=pedido)
    return render(request, 'actualizar_producto.html', {'form': form})


def buscar_por_nombre(request):
    nombre = request.GET.get('nombre', '').strip()
    fabricante = request.GET.get('fabricante', '').strip()
    material = request.GET.get('material', '').strip()
    tipo = request.GET.get('tipo', '').strip()
    fecha_inicio = request.GET.get('fecha_inicio','').strip()
    fecha_fin = request.GET.get('fecha_fin','').strip()

    productos = Producto.objects.all()

    if nombre:
        productos = productos.filter(nombre__icontains=nombre)
    if fabricante:
        productos = productos.filter(fabricante__icontains=fabricante)
    if material:
        productos = productos.filter(material__icontains=material)
    if tipo:
        productos = productos.filter(tipo=tipo)
    if fecha_inicio:
        fecha_inicio = parse_date(fecha_inicio)
        productos = productos.filter(fecha__gte=fecha_inicio)
    if fecha_fin:
        fecha_fin = parse_date(fecha_fin)
        productos = productos.filter(fecha__lte=fecha_fin)


    tipos = Producto.TipoChoices.choices
    return render(request, 'listar_productos.html', {'productos': productos, 'tipos': tipos})
