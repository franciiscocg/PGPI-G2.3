from .models import Producto
from django.db import models
from django.shortcuts import get_object_or_404

# módulo que realizará consultas a la bbdd
class ProductoManager(models.Manager):
    def getAll():
        return list(Producto.objects.values())

    def getById(id:int):
        return get_object_or_404(Producto,id==id)

    def save(producto:Producto):
        return Producto.objects.update_or_create(id=producto.id,
                                                create_defaults={"nombre":producto.nombre,
                                                                "foto":producto.foto,
                                                                "precio":producto.precio,
                                                                "cantidad_almacen":producto.cantidad_almacen,
                                                                "fabricante":producto.fabricante,
                                                                "material":producto.material,
                                                                "tipo":producto.tipo
                                                                }
                                                )

    def delete(producto:Producto):
        try:
            producto.delete()
        except Exception as e:
            print(e)
    
    def getByTipo(t:str):
        return list(Producto.objects.filter(tipo=t))
    
    def getByMaterial(m:str):
        return list(Producto.objects.filter(material=m))
    
    def getByPrecio(lim_inf:float,lim_sup:float):
        return list(Producto.objects.filter(precio__gt=lim_inf, precio__lt=lim_sup))