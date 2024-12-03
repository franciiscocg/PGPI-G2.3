from datetime import date
import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import ProductoForm
from .models import Producto
from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_date
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User

@login_required(login_url='/login/') 
@user_passes_test(lambda u: u.is_staff)
def gestionar_productos(request):
    productos = Producto.objects.all()
    materiales = set(map(lambda x:x.material, productos))
    fabricantes = set(map(lambda x:x.fabricante, productos))

    return render(request, 'gestionar_productos.html', {'productos': productos, 'materiales': materiales, 'fabricantes': fabricantes, 'tipos': Producto.TipoChoices.choices})

@login_required(login_url='/login/')
@user_passes_test(lambda u: u.is_staff)
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        producto.delete()
        return redirect('/gestionar_productos')
    return redirect(request.META.get('HTTP_REFERER', ''))

@login_required(login_url='/login/')
@user_passes_test(lambda u: u.is_staff)
def crear_producto(request):
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
    materiales = set(map(lambda x:x.material, productos))
    fabricantes = set(map(lambda x:x.fabricante, productos))
    return render(request, 'listar_productos.html', {'productos': productos, 'materiales':materiales, 'fabricantes':fabricantes})


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
@user_passes_test(lambda u: u.is_staff)
def actualizar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('/gestionar_productos/')
    else:
        form = ProductoForm(instance=producto)
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
        productos = productos.filter(fabricante=fabricante)
    if material:
        productos = productos.filter(material=material)
    if tipo:
        productos = productos.filter(tipo=tipo)
    if fecha_inicio:
        fecha_inicio = parse_date(fecha_inicio)
        productos = productos.filter(fecha__gte=fecha_inicio)
    if fecha_fin:
        fecha_fin = parse_date(fecha_fin)
        productos = productos.filter(fecha__lte=fecha_fin)


    tipos = Producto.TipoChoices.choices
    materiales = set(map(lambda x:x.material, productos))
    fabricantes = set(map(lambda x:x.fabricante, productos))
    return render(request, 'listar_productos.html', {'productos': productos, 'tipos': tipos, 'materiales':materiales, 'fabricantes':fabricantes})

def buscar_por_nombre_gestionar(request):
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
        productos = productos.filter(fabricante=fabricante)
    if material:
        productos = productos.filter(material=material)
    if tipo:
        productos = productos.filter(tipo=tipo)
    if fecha_inicio:
        fecha_inicio = parse_date(fecha_inicio)
        productos = productos.filter(fecha__gte=fecha_inicio)
    if fecha_fin:
        fecha_fin = parse_date(fecha_fin)
        productos = productos.filter(fecha__lte=fecha_fin)


    tipos = Producto.TipoChoices.choices
    materiales = set(map(lambda x:x.material, productos))
    fabricantes = set(map(lambda x:x.fabricante, productos))
    return render(request, 'gestionar_productos.html', {'productos': productos, 'tipos': tipos, 'materiales':materiales, 'fabricantes':fabricantes})
