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


def listar_producto(request):
    pedidos = Producto.objects.all()
    return render(request, 'listar_productos.html', {'pedido': pedidos})


def listar_productos(request, id):
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
    pedido = get_object_or_404(Producto, id=id)
    if request.method == 'POST':
        pedido.delete()
        return redirect('listar_pedidos')
    return render(request, 'eliminar_producto.html', {'producto': pedido})
