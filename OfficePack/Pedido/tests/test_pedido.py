# FILE: Pedido/tests/test_pedido.py
import unittest
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from Pedido.models import Pedido, EstadoPedido, MetodoPago
from Pedido.forms import PedidoForm

class PedidoModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345',is_staff=True)
        self.pedido = Pedido.objects.create(
            usuario=self.user,
            email='test@example.com',
            importe=100.00,
            direccion='123 Test St',
            estado=EstadoPedido.PENDIENTE,
            metodo_pago=MetodoPago.TARJETA
        )

    def test_pedido_creation(self):
        self.assertIsInstance(self.pedido, Pedido)
        self.assertEqual(self.pedido.email, 'test@example.com')
        self.assertEqual(self.pedido.importe, 100.00)
        self.assertEqual(self.pedido.direccion, '123 Test St')
        self.assertEqual(self.pedido.estado, EstadoPedido.PENDIENTE)
        self.assertEqual(self.pedido.metodo_pago, MetodoPago.TARJETA)

    def test_default_estado(self):
        pedido = Pedido.objects.create(
            usuario=self.user,
            email='default@example.com',
            importe=50.00,
            direccion='456 Default St'
        )
        self.assertEqual(pedido.estado, EstadoPedido.PENDIENTE)

    def test_default_metodo_pago(self):
        pedido = Pedido.objects.create(
            usuario=self.user,
            email='default@example.com',
            importe=50.00,
            direccion='456 Default St'
        )
        self.assertEqual(pedido.metodo_pago, MetodoPago.TARJETA)


class PedidoFormTest(TestCase):

    def test_valid_form(self):
        user = User.objects.create_user(username='testuser', password='12345',is_staff=True)
        data = {
            'usuario': user.id,
            'email': 'test@example.com',
            'importe': 100.00,
            'direccion': '123 Test St',
            'estado': EstadoPedido.PENDIENTE,
            'metodo_pago': MetodoPago.TARJETA
        }
        form = PedidoForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {
            'email': 'test@example.com',
            'importe': 100.00,
            'direccion': '123 Test St'
        }
        form = PedidoForm(data=data)
        self.assertFalse(form.is_valid())

class PedidoViewsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345',is_staff=True)
        self.pedido = Pedido.objects.create(
            usuario=self.user,
            email='test@example.com',
            importe=100.00,
            direccion='123 Test St',
            estado=EstadoPedido.PENDIENTE,
            metodo_pago=MetodoPago.TARJETA
        )

    def test_listar_pedidos_view(self):
        self.client.login(username='testuser', password='12345',is_staff=True)
        self.user.email = 'officepack@gmail.com'
        self.user.save()
        url = reverse('listar_pedidos')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.pedido.email)

    def test_mostrar_pedido_view(self):
        self.client.login(username='testuser', password='12345',is_staff=True)
        url = reverse('mostrar_pedido', args=[self.pedido.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.pedido.email)

    def test_crear_pedido_view(self):
        self.client.login(username='testuser', password='12345',is_staff=True)
        self.user.email = 'officepack@gmail.com'
        self.user.save()
        url = reverse('crear_pedido')
        data = {
            'usuario': self.user.id,
            'email': 'nuevo@example.com',
            'importe': 150.00,
            'direccion': '789 New St',
            'estado': EstadoPedido.EN_PROCESO,
            'metodo_pago': MetodoPago.CONTRAREEMBOLSO
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Pedido.objects.filter(email='nuevo@example.com').exists())

    def test_actualizar_pedido_view(self):
        self.client.login(username='testuser', password='12345',is_staff=True)
        url = reverse('actualizar_pedido', args=[self.pedido.id])
        data = {
            'usuario': self.user.id,
            'email': 'actualizado@example.com',
            'importe': 200.00,
            'direccion': '456 Updated St',
            'estado': EstadoPedido.ENVIADO,
            'metodo_pago': MetodoPago.TARJETA
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.pedido.refresh_from_db()
        self.assertEqual(self.pedido.email, 'actualizado@example.com')

    def test_eliminar_pedido_view(self):
        self.client.login(username='testuser', password='12345',is_staff=True, email='officepack@gmail.com')
        self.user.email = 'officepack@gmail.com'
        self.user.save()        
        url = reverse('eliminar_pedido', args=[self.pedido.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Pedido.objects.filter(id=self.pedido.id).exists())

if __name__ == '__main__':
    unittest.main()