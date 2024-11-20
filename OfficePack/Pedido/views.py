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


@login_required(login_url='/login/')
def añadir_a_cesta(request, producto_id):
    producto = Producto.objects.get(id=producto_id)

    # Se verifica si ya existe una cesta activa
    if 'cesta' not in request.session:
        request.session['cesta'] = {}

    cesta = request.session['cesta']

    # Se verifica si el stock es suficiente para añadir el producto
    if producto.cantidad_almacen > 0:
        # Si el producto ya está en la cesta, se aumentta la cantidad si hay stock suficiente
        if str(producto_id) in cesta:
            if cesta[str(producto_id)]['cantidad'] < producto.cantidad_almacen:
                cesta[str(producto_id)]['cantidad'] += 1
            else:
                # Si el stock es insuficiente, muestra un mensaje
                return render(request, 'mensaje_error.html', {'mensaje': 'No hay suficiente stock para añadir más de este producto.'})
        else:
            cesta[str(producto_id)] = {
                'nombre': producto.nombre,
                'precio': float(producto.precio),
                'cantidad': 1
            }
        request.session.modified = True  # Indicamos que la sesión ha sido modificada
    else:
        # Si el producto no tiene stock, muestra un mensaje
        return render(request, 'mensaje_error.html', {'mensaje': 'Este producto está agotado.'})

    return redirect('ver_cesta')


def ver_cesta(request):
    cesta = request.session.get('cesta', {})
    total = sum(item['precio'] * item['cantidad'] for item in cesta.values())
    return render(request, 'ver_cesta.html', {'cesta': cesta, 'total': round(total, 2)})


def eliminar_de_cesta(request, producto_id):
    cesta = request.session.get('cesta', {})
    if str(producto_id) in cesta:
        del cesta[str(producto_id)]
        request.session.modified = True
    return redirect('ver_cesta')


@login_required(login_url='/login/')
def realizar_pedido(request):
    cesta = request.session.get('cesta', {})
    if not cesta:
        return redirect('ver_cesta')  # Si la cesta está vacía, redirige al carrito

    # Se crea un nuevo pedido
    pedido = Pedido.objects.create(usuario=request.user, importe=0)
    
    total = 0  # Se inicia el total
    for producto_id, item in cesta.items():
        producto = Producto.objects.get(id=producto_id)
        cantidad_almacen = item['cantidad']
        precio_unitario = item['precio']
        subtotal = precio_unitario * cantidad_almacen
        total += subtotal  # Sumar el subtotal del producto al total

        # Se verifica si hay suficiente stock
        if producto.cantidad_almacen < cantidad_almacen:
            return render(request, 'mensaje_error.html', {'mensaje': 'No hay suficiente stock para completar tu pedido.'})

        # Se crean los registros en la tabla de productos del pedido
        ProductoPedido.objects.create(pedido=pedido, producto=producto, cantidad=cantidad_almacen, precio_unitario=precio_unitario)

        # Se actualiza el stock del producto
        producto.cantidad_almacen -= cantidad_almacen
        producto.save()

    # Se actualiza el total del pedido
    pedido.total = total
    pedido.save()

    # Se vacia la cesta
    request.session['cesta'] = {}
    request.session.modified = True

    return render(request, 'pedido_confirmado.html', {'pedido': pedido})

