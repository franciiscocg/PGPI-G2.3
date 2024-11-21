from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


from .forms import PedidoForm
from .models import Pedido

from Producto.models import Producto
from Producto_pedido.models import ProductoPedido
from django.conf import settings

import stripe

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY


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


#Operaciones de pago

def pagar(request):
    # Total de la cesta
    cesta = request.session.get('cesta', {})
    total = sum(item['precio'] * item['cantidad'] for item in cesta.values())

    # PaymentIntent con el total de la cesta
    intent = stripe.PaymentIntent.create(
        amount=int(total * 100),  # Cantidad en centavos
        currency='eur',
    )

    # Se pasa la clave pública de Stripe y el client secret al html de pagar
    return render(request, 'pagar.html', {
        'stripe_public_key': settings.STRIPE_TEST_PUBLIC_KEY,
        'client_secret': intent.client_secret,
    })


def confirmar_pago(request):
    cesta = request.session.get('cesta', {})
    total = sum(item['precio'] * item['cantidad'] for item in cesta.values())

    if request.method == 'POST':
        payment_intent_id = request.POST.get('payment_intent_id')

        # Se verifica que el PaymentIntent haya ido bien
        try:
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        except stripe.error.StripeError as e:
            return render(request, 'mensaje_error.html', {'mensaje': f"Error con Stripe: {str(e)}"})

        if intent.status == 'succeeded':
            # Crear el pedido
            pedido = Pedido.objects.create(usuario=request.user, total=total)
            for producto_id, item in cesta.items():
                producto = Producto.objects.get(id=producto_id)
                cantidad = item['cantidad']
                # Actualizar el stock
                producto.stock -= cantidad
                producto.save()

            # Vaciar la cesta
            request.session['cesta'] = {}
            request.session.modified = True

            return render(request, 'pedido_confirmado.html', {'pedido': pedido})
        else:
            return render(request, 'mensaje_error.html', {'mensaje': 'Hubo un error con tu pago. Intenta nuevamente.'})

    return redirect('ver_cesta')
