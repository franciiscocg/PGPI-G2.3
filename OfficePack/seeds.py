from Producto.models import Producto


def cargar_datos_prueba():
    # Crear productos de prueba
    Producto.objects.create(
        nombre="Escritorio Ejecutivo",
        foto="https://cdn1.valemob.es/775-large_default/escritorio-de-oficina-recto-madera.jpg",
        precio=299.99,
        cantidad_almacen=50,
        fabricante="OfiMuebles S.A.",
        material="Madera de roble",
        tipo="Escritorio"
    )

    Producto.objects.create(
        nombre="Silla ergonómica de oficina",
        foto="https://scontent.fsvq5-1.fna.fbcdn.net/v/t39.30808-6/462189418_3818431675095595_2725084864217893511_n.jpg?_nc_cat=100&ccb=1-7&_nc_sid=6ee11a&_nc_ohc=hPco0uqYsJYQ7kNvgFekUU5&_nc_zt=23&_nc_ht=scontent.fsvq5-1.fna&_nc_gid=Aq9qujqwdhV19mdDbgMkEPs&oh=00_AYDwh0yiEugWhSDg-yNlsi3P5jyGyeNSBZWYC3laYo7foA&oe=674900B5",
        precio=119.99,
        cantidad_almacen=100,
        fabricante="Sillas Comfort",
        material="Tela y base de aluminio",
        tipo="Silla"
    )

    Producto.objects.create(
        nombre="Estante modular",
        foto="https://preview.redd.it/4vooyo2jtfu41.jpg?auto=webp&s=3d60ce1bd9a86ca2e6f79c6425afb2f7b4fb3e7c",
        precio=89.50,
        cantidad_almacen=30,
        fabricante="Almacenaje y Diseño",
        material="Madera MDF",
        tipo="Estante"
    )

    Producto.objects.create(
        nombre="Pizarra blanca",
        foto="https://adrada.es/74490-large_default/pizarra-lacada-magnetica-blanca-perfil-de-aluminio-90x120cm.jpg",
        precio=45.75,
        cantidad_almacen=200,
        fabricante="Oficina Express",
        material="Vidrio templado",
        tipo="Pizarra"
    )

    Producto.objects.create(
        nombre="Lámpara de escritorio LED",
        foto="https://s.libertaddigital.com/2021/10/25/290/0/lampara-de-escritorio-led-jukstg-1906-1.jpg",
        precio=35.99,
        cantidad_almacen=75,
        fabricante="LuzPro",
        material="Plástico y metal",
        tipo="Lámpara"
    )

    Producto.objects.create(
        nombre="Archivador metálico",
        foto="https://example.com/images/archivador_metalico.jpg",
        precio=99.99,
        cantidad_almacen=40,
        fabricante="OfiMetal",
        material="Acero pintado",
        tipo="Archivador"
    )

    print("Datos de prueba cargados correctamente.")


# Llamar a la función para cargar los datos
if __name__ == "__main__":
    cargar_datos_prueba()
