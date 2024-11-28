from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .forms import PedidoForm
from .models import Pedido
from Producto.models import Producto
import stripe
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.http import HttpResponseForbidden

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY


@login_required(login_url='/login/')
def crear_pedido(request):
    # comprobamos que el user sea el admin
    if request.user.email != "officepack@gmail.com":
        return HttpResponseForbidden("No tienes autoridad para realizar esta operación")
    
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/gestionar_pedidos/')
    else:
        form = PedidoForm()
    return render(request, 'crear_pedido.html', {'form': form})

@login_required(login_url='/login/')
def actualizar_pedido(request, pedido_id):
    # comprobamos que el user sea el admin
    if request.user.email != "officepack@gmail.com":
        return HttpResponseForbidden("No tienes autoridad para realizar esta operación")
    
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/gestionar_pedidos/')
    else:
        form = PedidoForm(instance=get_object_or_404(Pedido, id=pedido_id))
    return render(request, 'actualizar_pedido.html', {'form': form})


@login_required(login_url='/login/')
def listar_pedidos(request):
    # comprobamos que el user sea el admin
    if request.user.email != "officepack@gmail.com":
        return HttpResponseForbidden("No tienes autoridad para realizar esta operación")
    
    pedidos = Pedido.objects.all()
    return render(request, 'gestionar_pedidos.html', {'pedidos': pedidos})


def mostrar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    return render(request, 'mostrar_pedido.html', {'pedido': pedido})


@login_required(login_url='/login/')
def listar_mis_pedidos(request):
    pedidos = Pedido.objects.filter(email=request.user.email)
    return render(request, 'listar_pedidos.html', {'pedidos': pedidos})


@login_required(login_url='/login/')
def eliminar_pedido(request, pedido_id):
    # comprobamos que el user sea el admin
    if request.user.email != "officepack@gmail.com":
        return HttpResponseForbidden("No tienes autoridad para realizar esta operación")
    
    pedido = get_object_or_404(Pedido, id=pedido_id)
    if request.method == 'POST':
        pedido.delete()
        return redirect('/gestionar_pedidos')
    return redirect(request.META.get('HTTP_REFERER', ''))


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
    return redirect(request.META.get('HTTP_REFERER', 'ver_cesta'))


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
    return redirect(request.META.get('HTTP_REFERER', '/cesta'))


def disminuir_cantidad_producto_en_cesta(request, producto_id):
    cesta = request.session.get('cesta', {})
    if str(producto_id) in cesta:
        if cesta[str(producto_id)]['cantidad'] > 1:
            cesta[str(producto_id)]['cantidad'] -= 1
            request.session.modified = True
        else:
            return eliminar_de_cesta(request, producto_id)
    return redirect(request.META.get('HTTP_REFERER', 'ver_cesta'))


def eliminar_de_cesta(request, producto_id):
    cesta = request.session.get('cesta', {})
    if str(producto_id) in cesta:
        del cesta[str(producto_id)]
        request.session.modified = True
    return redirect(request.META.get('HTTP_REFERER', 'ver_cesta'))


def obtener_cesta(request):
    cesta = request.session.get('cesta', {})
    cesta_html = render_to_string('cesta.html', {'cesta': cesta})
    return JsonResponse({'status': 'success', 'html': cesta_html})


# Operaciones de pago


def pagar(request):
    # Total de la cesta
    cesta = request.session.get('cesta', {})
    total = sum(item['precio'] * item['cantidad'] for item in cesta.values())

    # Costes de envío
    if total < 30:
        total += 5

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

    # Costes de envío
    if total < 30:
        total += 5

    if request.method == 'POST':

        if request.user.is_authenticated:
            # Usuario autenticado
            email = request.user.email
            usuario = request.user
        else:
            # Usuario no autenticado
            email = request.POST.get('email')  # Correo proporcionado en el formulario
            usuario = None  # No hay un usuario autenticado, se manejará solo con el email

        direccion = request.POST.get('direccion')
        metodo_pago = request.POST.get('metodo_pago')
        
        if metodo_pago == 'T':
            payment_intent_id = request.POST.get('payment_intent_id')

            # Se verifica que el PaymentIntent haya ido bien
            try:
                intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            except stripe.error.StripeError as e:
                return render(request, 'mensaje_error.html', {'mensaje': f"Error con Stripe: {str(e)}"})
        elif metodo_pago == 'C':
            # Para el pago contra reembolso, no se necesita verificar con Stripe
            intent = {
                'id': 'manual_payment',
                'status': 'succeeded',
            }
        else:
            return render(request, 'mensaje_error.html', {'mensaje': 'Método de pago no válido.'})
            
         
            
        if intent['status'] == 'succeeded':
            # Verificar el stock antes de crear el pedido
            for producto_id, item in cesta.items():
                producto = Producto.objects.get(id=producto_id)
                if item['cantidad'] > producto.cantidad_almacen:
                    # Si el stock es insuficiente, muestra un mensaje y no se crea el pedido
                    return render(request, 'mensaje_error.html', {
                        'mensaje': f"No hay suficiente stock de '{producto.nombre}' para completar tu pedido."
                    })

            # Si hay stock suficiente, se crea el pedido
            pedido = Pedido.objects.create(usuario=usuario, importe=total, email=email, direccion=direccion)

            # Se guarda una copia de la cesta para el mensaje del correo
            productos_comprados = []

            for producto_id, item in cesta.items():
                producto = Producto.objects.get(id=producto_id)
                cantidad = item['cantidad']

                producto.cantidad_almacen -= cantidad
                producto.save()

                # Guardamos el producto y su cantidad
                productos_comprados.append(f"- {producto.nombre}: {cantidad} x {producto.precio}€")

            # Vaciar la cesta
            request.session['cesta'] = {}
            request.session.modified = True

            # Enviar correo de confirmación
            asunto = 'Confirmación de Pedido'
            mensaje = f"Hola, \n\nTu pedido ha sido confirmado. El importe total es {total}.\n\nLos productos comprados son:\n"
            mensaje += "\n".join(productos_comprados)
            mensaje += "\nGracias por tu compra."

            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = email  # El correo proporcionado por el usuario no autenticado

            try:
                send_mail(asunto, mensaje, from_email, [to_email])
            except Exception as e:
                # Se maneja posible error de envío de correo
                return render(request, 'mensaje_error.html', {'mensaje': f"Hubo un problema al enviar el correo: {str(e)}"})

            return render(request, 'pedido_confirmado.html', {'pedido': pedido})
        else:
            return render(request, 'mensaje_error.html', {'mensaje': 'Hubo un error con tu pago. Intenta nuevamente.'})

    return redirect('ver_cesta')
