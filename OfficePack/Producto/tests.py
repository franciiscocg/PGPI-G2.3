from django.test import TestCase

# Create your tests here.
# FILE: Producto/tests/test_producto.py
import unittest
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from Producto.models import Producto
from Producto.forms import ProductoForm

class ProductoModelTest(TestCase):

    def setUp(self):
        self.producto = Producto.objects.create(
            nombre='Producto Test',
            foto='https://example.com/foto.jpg',
            precio=10.00,
            cantidad_almacen=100,
            fabricante='Fabricante Test',
            material='Material Test',
            tipo='MUEBLE',
            fecha='2024-01-01'
        )

    def test_producto_creation(self):
        self.assertIsInstance(self.producto, Producto)
        self.assertEqual(self.producto.nombre, 'Producto Test')
        self.assertEqual(self.producto.foto, 'https://example.com/foto.jpg')
        self.assertEqual(self.producto.precio, 10.00)
        self.assertEqual(self.producto.cantidad_almacen, 100)
        self.assertEqual(self.producto.fabricante, 'Fabricante Test')
        self.assertEqual(self.producto.material, 'Material Test')
        self.assertEqual(self.producto.tipo, 'MUEBLE')
        self.assertEqual(self.producto.fecha, '2024-01-01')

    def test_producto_str(self):
        self.assertEqual(str(self.producto), self.producto.nombre)

class ProductoViewsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345',is_staff=True)
        self.producto = Producto.objects.create(
            nombre='Producto Test',
            foto='https://example.com/foto.jpg',
            precio=10.00,
            cantidad_almacen=100,
            fabricante='Fabricante Test',
            material='Material Test',
            tipo='MUEBLE',
            fecha='2024-01-01'
        )
        self.producto2 = Producto.objects.create(
            nombre='Producto 2',
            foto='https://example.com/foto.jpg',
            precio=20.00,
            cantidad_almacen=100,
            fabricante='Fabricante 2',
            material='Material 2',
            tipo='ELECTRONICO',
            fecha='2024-11-11'
        )

    def test_mostrar_producto_view(self):
        url = reverse('mostrar_producto', args=[self.producto.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.producto.nombre)

    def test_listar_productos_view(self):
        url = reverse('listar_productos')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.producto.nombre)

    def test_crear_producto_view(self):
        self.client.login(username='testuser', password='12345',is_staff=True)
        url = reverse('crear_producto')
        data = {
            'nombre': 'Nuevo Producto',
            'foto': 'https://example.com/nueva_foto.jpg',
            'precio': 20.00,
            'cantidad_almacen': 50,
            'fabricante': 'Nuevo Fabricante',
            'material': 'Nuevo Material',
            'tipo': 'MUEBLE',
            'fecha': '2024-02-01'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Producto.objects.filter(nombre='Nuevo Producto').exists())

    def test_actualizar_producto_view(self):
        self.client.login(username='testuser', password='12345',is_staff=True)
        url = reverse('actualizar_producto', args=[self.producto.id])
        data = {
            'nombre': 'Producto Actualizado',
            'foto': 'https://example.com/actualizada_foto.jpg',
            'precio': 15.00,
            'cantidad_almacen': 80,
            'fabricante': 'Fabricante Actualizado',
            'material': 'Material Actualizado',
            'tipo': 'SILLA',
            'fecha': '2024-03-01'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.nombre, 'Producto Actualizado')

    def test_eliminar_producto_view(self):
        self.client.login(username='testuser', password='12345',is_staff=True)
        url = reverse('eliminar_producto', args=[self.producto.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Producto.objects.filter(id=self.producto.id).exists())
        
    def test_buscar_por_nombre_view(self):
        url = reverse('buscar_por_nombre')
        response = self.client.get(url, {'nombre': 'Producto 2'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['productos']), 1)
        self.assertNotContains(response, self.producto.nombre)
        
    def test_buscar_por_fabricante_view(self):
        url = reverse('buscar_por_nombre')
        response = self.client.get(url, {'fabricante': 'Fabricante 2'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['productos']), 1)
        self.assertNotContains(response, self.producto.nombre)
        self.assertContains(response, self.producto2.nombre)
        
    def test_buscar_por_material_view(self):
        url = reverse('buscar_por_nombre')
        response = self.client.get(url, {'material': 'Material 2'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['productos']), 1)
        self.assertNotContains(response, self.producto.nombre)
        self.assertContains(response, self.producto2.nombre)

    def test_buscar_entre_fechas_view(self):
        url = reverse('buscar_por_nombre')
        response = self.client.get(url, {'tipo': 'MUEBLE'})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.producto2.nombre)
        self.assertContains(response, self.producto.nombre)
        
        response = self.client.get(url, {
            'fecha_inicio': '2024-10-11',
            'fecha_fin': '2024-11-11'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['productos']), 1)
        self.assertNotContains(response, self.producto.nombre)
        self.assertContains(response, self.producto2.nombre)
    
class ProductoFormTest(TestCase):

    def test_valid_form(self):
        data = {
            'nombre': 'Producto Test',
            'foto': 'https://example.com/foto.jpg',
            'precio': 10.00,
            'cantidad_almacen': 100,
            'fabricante': 'Fabricante Test',
            'material': 'Material Test',
            'tipo': 'MUEBLE',
            'fecha': '2024-01-01'
        }
        form = ProductoForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_missing_fields(self):
        data = {
            'nombre': 'Producto Test',
            'precio': 10.00,
            'cantidad_almacen': 100,
            'fabricante': 'Fabricante Test',
            'material': 'Material Test',
            'tipo': 'MUEBLE'
        }
        form = ProductoForm(data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_form_incorrect_data(self):
        data = {
            'nombre': 'Producto Test',
            'foto': 'not_a_valid_url',
            'precio': 'not_a_number',
            'cantidad_almacen': 'not_an_integer',
            'fabricante': 'Fabricante Test',
            'material': 'Material Test',
            'tipo': 'MUEBLE',
            'fecha': 'not_a_date'
        }
        form = ProductoForm(data=data)
        self.assertFalse(form.is_valid())

if __name__ == '__main__':
    unittest.main()