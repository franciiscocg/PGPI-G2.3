from django.shortcuts import render, redirect
from .forms import ProductoForm
from .models import Producto
from django.shortcuts import get_object_or_404


def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_productos')
    else:
        form = ProductoForm()
    return render(request, 'crear_producto.html', {'form': form})


def listar_productos(request):
    productos = Producto.objects.filter(cantidad_almacen__gt=0)
    return render(request, 'listar_productos.html', {'productos': productos})


def listar_producto(request, id):
    pedido = get_object_or_404(Producto, id=id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=pedido)
        if form.is_valid():
            form.save()
            return redirect('listar_productos')
    else:
        form = ProductoForm(instance=pedido)
    return render(request, 'actualizar_producto.html', {'form': form})


def actualizar_producto(request, id):
    pedido = get_object_or_404(Producto, id=id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=pedido)
        if form.is_valid():
            form.save()
            return redirect('listar_productos')
    else:
        form = ProductoForm(instance=pedido)
    return render(request, 'actualizar_producto.html', {'form': form})


def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == 'POST':
        producto.delete()
        return redirect('listar_productos')
    return render(request, 'eliminar_producto.html', {'producto': producto})


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
