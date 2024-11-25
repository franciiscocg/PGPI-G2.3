from django.shortcuts import render, get_object_or_404
from Pedido.models import Pedido
from Producto_pedido.models import ProductoPedido

def rastrear_pedido(request):
    pedido = None
    productos_pedido = None
    error = None

    if request.method == 'POST':
        pedido_id = request.POST.get('pedido_id')
        try:
            pedido = Pedido.objects.get(id=pedido_id)
            productos_pedido = ProductoPedido.objects.filter(pedido=pedido)
        except Pedido.DoesNotExist:
            error = "No se encontró ningún pedido con ese ID."

    return render(request, 'rastrear_pedido.html', {
        'pedido': pedido,
        'productos_pedido': productos_pedido,
        'error': error
    })