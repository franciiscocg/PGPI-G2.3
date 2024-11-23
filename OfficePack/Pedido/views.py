from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .forms import PedidoForm
from .models import Pedido
from Producto.models import Producto
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


def listar_pedidos(request):
    pedidos = Pedido.objects.all()
    return render(request, 'listar_pedidos.html', {'pedido': pedidos})


def mostrar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    return render(request, 'mostrar_pedido.html', {'pedido': pedido})


@login_required(login_url='/login/')
def listar_mis_pedidos(request):
    pedidos = Pedido.objects.filter(email=request.user.email)
    return render(request, 'listar_pedidos.html', {'pedidos': pedidos})


def eliminar_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    if request.method == 'POST':
        pedido.delete()
        return redirect('listar_pedidos')
    return render(request, 'eliminar_pedido.html', {'pedido': pedido})


# Operaciones con la cesta


def añadir_a_cesta(request, producto_id):
    cantidad = int(request.POST.get('cantidad', 1))
    producto = Producto.objects.get(id=producto_id)
    if 'cesta' not in request.session:
        request.session['cesta'] = {}
    cesta = request.session['cesta']
    if producto.cantidad_almacen >= cantidad:
        if str(producto_id) in cesta:
            nueva_cantidad = min(cesta[str(producto_id)]['cantidad'] + cantidad, producto.cantidad_almacen)
            cesta[str(producto_id)]['cantidad'] = nueva_cantidad
        else:
            cesta[str(producto_id)] = {
                'nombre': producto.nombre,
                'foto': producto.foto,
                'precio': float(producto.precio),
                'cantidad': cantidad
            }
        request.session.modified = True
    else:
        return render(request, 'mensaje_error.html', {'mensaje': 'Este producto está agotado.'})
    return redirect('ver_cesta')


def ver_cesta(request):
    cesta = request.session.get('cesta', {})
    total = sum(item['precio'] * item['cantidad'] for item in cesta.values())
    return render(request, 'ver_cesta.html', {'cesta': cesta, 'total': round(total, 2)})


def aumentar_cantidad_producto_en_cesta(request, producto_id):
    cesta = request.session.get('cesta', {})
    producto = Producto.objects.get(id=producto_id)
    if str(producto_id) in cesta:
        if cesta[str(producto_id)]['cantidad'] < producto.cantidad_almacen:
            cesta[str(producto_id)]['cantidad'] += 1
            request.session.modified = True
        else:
            return render(request, 'mensaje_error.html', {'mensaje': 'No hay suficiente stock para añadir más de este producto.'})
    return redirect('ver_cesta')


def disminuir_cantidad_producto_en_cesta(request, producto_id):
    cesta = request.session.get('cesta', {})
    if str(producto_id) in cesta:
        if cesta[str(producto_id)]['cantidad'] > 1:
            cesta[str(producto_id)]['cantidad'] -= 1
            request.session.modified = True
        else:
            return eliminar_de_cesta(request, producto_id)
    return redirect('ver_cesta')


def eliminar_de_cesta(request, producto_id):
    cesta = request.session.get('cesta', {})
    if str(producto_id) in cesta:
        del cesta[str(producto_id)]
        request.session.modified = True
    return redirect('ver_cesta')

# Operaciones de pago


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
        if request.user.is_authenticated:
            email = request.user.email
        else:
            email = request.POST.get('email')
        direccion = request.POST.get('direccion')
        payment_intent_id = request.POST.get('payment_intent_id')

        # Se verifica que el PaymentIntent haya ido bien
        try:
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        except stripe.error.StripeError as e:
            return render(request, 'mensaje_error.html', {'mensaje': f"Error con Stripe: {str(e)}"})

        if intent.status == 'succeeded':
            # Se crea el pedido
            pedido = Pedido.objects.create(usuario=request.user, importe=total, email=email, direccion=direccion)
            for producto_id, item in cesta.items():
                producto = Producto.objects.get(id=producto_id)
                cantidad = item['cantidad']
                # Actualizar el stock
                producto.cantidad_almacen -= cantidad
                producto.save()

            # Vaciar la cesta
            request.session['cesta'] = {}
            request.session.modified = True

            # Se envia correo de confirmación
            asunto = 'Confirmación de Pedido'
            mensaje = f"Hola {request.user.username},\n\nTu pedido ha sido confirmado. El importe total es {total}.\nGracias por tu compra."
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = email  # El correo del usuario que realizó la compra

            try:
                send_mail(asunto, mensaje, from_email, [to_email])
            except Exception as e:
                # Se maneja posible errorer de envío de correo 
                return render(request, 'mensaje_error.html', {'mensaje': f"Hubo un problema al enviar el correo: {str(e)}"})

            return render(request, 'pedido_confirmado.html', {'pedido': pedido})
        else:
            return render(request, 'mensaje_error.html', {'mensaje': 'Hubo un error con tu pago. Intenta nuevamente.'})

    return redirect('ver_cesta')