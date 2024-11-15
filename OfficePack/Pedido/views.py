from django.shortcuts import render, redirect
from .forms import PedidoForm
from .models import Pedido
from django.shortcuts import get_object_or_404


def crear_pedido(request):
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_pedidos') 
    else:
        form = PedidoForm()
    return render(request, 'crear_pedido.html', {'form': form})


def listar_pedido(request):
    pedidos = Pedido.objects.all()
    return render(request, 'listar_pedido.html', {'pedido': pedidos})


def actualizar_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    if request.method == 'POST':
        form = PedidoForm(request.POST, instance=pedido)
        if form.is_valid():
            form.save()
            return redirect('listar_pedidos')
    else:
        form = PedidoForm(instance=pedido)
    return render(request, 'actualizar_producto.html', {'form': form})


def eliminar_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    if request.method == 'POST':
        pedido.delete()
        return redirect('listar_pedidos')
    return render(request, 'eliminar_pedido.html', {'pedido': pedido})