"""
Modulo precarga: carga inicial de datos.

Los datos iniciales ya no estan escritos dentro del programa: se leen de
los archivos productos_inicial.json y clientes_inicial.json y se copian a
los archivos de trabajo (productos.json y clientes.json) la primera vez
que se ejecuta el sistema.
"""

import os
import archivos


def copiar_archivo_inicial(ruta_inicial, ruta_trabajo):
    """
    Si el archivo de trabajo no existe, lo crea a partir del archivo inicial.

    Parametros:
        ruta_inicial (str): archivo con los datos de precarga.
        ruta_trabajo (str): archivo que usa el programa (CRUD).
    """
    if os.path.exists(ruta_trabajo):
        return

    datos = archivos.leer_json(ruta_inicial)
    if len(datos) == 0:
        print("Aviso: no hay datos de precarga en", os.path.basename(ruta_inicial))

    archivos.guardar_json(ruta_trabajo, datos)
    print("Precarga realizada:", len(datos), "registros en", os.path.basename(ruta_trabajo))


def cargar_datos():
    """
    Prepara los archivos de trabajo de productos y clientes al iniciar.
    """
    copiar_archivo_inicial(archivos.RUTA_PRODUCTOS_INICIAL, archivos.RUTA_PRODUCTOS)
    copiar_archivo_inicial(archivos.RUTA_CLIENTES_INICIAL, archivos.RUTA_CLIENTES)


def restaurar_datos():
    """
    Vuelve los datos al estado inicial: borra los cambios hechos en
    productos.json y clientes.json y los copia otra vez desde los iniciales.
    """
    productos = archivos.leer_json(archivos.RUTA_PRODUCTOS_INICIAL)
    clientes = archivos.leer_json(archivos.RUTA_CLIENTES_INICIAL)
    archivos.guardar_json(archivos.RUTA_PRODUCTOS, productos)
    archivos.guardar_json(archivos.RUTA_CLIENTES, clientes)
    print("Datos restaurados a la precarga inicial.")
