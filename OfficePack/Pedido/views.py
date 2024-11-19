from django.shortcuts import render, redirect
from .forms import PedidoForm
from .models import Pedido
from Producto.models import Producto
from Producto_pedido.models import ProductoPedido
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required


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



# Operaciones con la cesta


@login_required
def añadir_a_cesta(request, producto_id):
    producto = Producto.objects.get(id=producto_id)
    
    # Verificar si ya existe una cesta activa
    if 'cesta' not in request.session:
        request.session['cesta'] = {}

    cesta = request.session['cesta']

    # Si el producto ya está en la cesta, aumentamos la cantidad
    if str(producto_id) in cesta:
        cesta[str(producto_id)]['cantidad'] += 1
    else:
        cesta[str(producto_id)] = {
            'nombre': producto.nombre,
            'precio': str(producto.precio),
            'cantidad': 1
        }

    request.session.modified = True  # Indicamos que la sesión ha sido modificada
    return redirect('ver_cesta')


def ver_cesta(request):
    cesta = request.session.get('cesta', {})
    total = sum(float(item['precio']) * item['cantidad'] for item in cesta.values())
    return render(request, 'ver_cesta.html', {'cesta': cesta, 'total': total})


@login_required(login_url='/accounts/login/')
def realizar_pedido(request):
    cesta = request.session.get('cesta', {})
    if not cesta:
        return redirect('ver_cesta')  # Si la cesta está vacía, redirige al carrito

    # Crear un nuevo pedido
    pedido = Pedido.objects.create(usuario=request.user, importe=0)
    
    # Añadir los productos a la tabla de ItemPedido
    total = 0
    for producto_id, item in cesta.items():
        producto = Producto.objects.get(id=producto_id)
        cantidad_almacen = item['cantidad']
        precio_unitario = producto.precio
        total += precio_unitario * cantidad_almacen

        ProductoPedido.objects.create(pedido=pedido, producto=producto, cantidad=cantidad_almacen, precio_unitario=precio_unitario)

    # Actualizar el total del pedido
    pedido.total = total
    pedido.save()

    # Vaciar la cesta
    request.session['cesta'] = {}
    request.session.modified = True
    
    return render(request, 'pedido_confirmado.html', {'pedido': pedido})

