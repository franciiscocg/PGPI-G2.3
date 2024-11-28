from django.shortcuts import render, redirect, get_object_or_404
from Pedido.views import crear_pedido
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

def cambiar_direccion(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    if (pedido.estado == 'P' or pedido.estado == 'EP'):
        pedido.direccion = request.POST.get('direccion')
        pedido.save()
        
    return redirect(request.META.get('HTTP_REFERER', ''))
        
