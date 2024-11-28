from django.shortcuts import render, redirect
from .forms import ProductoForm
from .models import Producto
from django.shortcuts import get_object_or_404


def gestionar_productos(request):
    productos = Producto.objects.all()
    return render(request, 'gestionar_productos.html', {'productos': productos})

def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    producto.delete()
    return redirect(request.META.get('HTTP_REFERER', ''))

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


def actualizar_producto(request, producto_id):
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

    productos = Producto.objects.all()

    if nombre:
        productos = productos.filter(nombre__icontains=nombre)
    if fabricante:
        productos = productos.filter(fabricante__icontains=fabricante)
    if material:
        productos = productos.filter(material__icontains=material)
    if tipo:
        productos = productos.filter(tipo__icontains=tipo)

    return render(request, 'listar_productos.html', {'productos': productos})