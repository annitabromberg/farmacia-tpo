"""
Modulo archivos: lectura y escritura de los archivos del sistema.

Persistencia en dos formatos:
- JSON: productos y clientes (diccionario de diccionarios).
- Texto plano (.txt): historial de ventas, una venta por linea.
"""

import json
import os


# Carpeta donde esta este archivo. Asi el programa encuentra los .json
# aunque se ejecute desde otra carpeta (por ejemplo, desde VS Code).
CARPETA = os.path.dirname(os.path.abspath(__file__))

RUTA_PRODUCTOS = os.path.join(CARPETA, "productos.json")
RUTA_CLIENTES = os.path.join(CARPETA, "clientes.json")
RUTA_PRODUCTOS_INICIAL = os.path.join(CARPETA, "productos_inicial.json")
RUTA_CLIENTES_INICIAL = os.path.join(CARPETA, "clientes_inicial.json")
RUTA_VENTAS = os.path.join(CARPETA, "ventas.txt")


def leer_json(ruta):
    """
    Lee un archivo JSON y devuelve su contenido como diccionario.

    Parametros:
        ruta (str): ruta del archivo a leer.

    Retorna:
        dict: los datos leidos, o un diccionario vacio si hubo un error.
    """
    try:
        archivo = open(ruta, "r", encoding="utf-8")
    except FileNotFoundError:
        print("Error: no se encontro el archivo", os.path.basename(ruta))
        return {}
    except OSError:
        print("Error: no se pudo abrir el archivo", os.path.basename(ruta))
        return {}

    try:
        datos = json.load(archivo)
    except ValueError:
        # json.load lanza un error de este tipo si el archivo esta mal escrito
        print("Error: el archivo", os.path.basename(ruta), "tiene un formato invalido.")
        datos = {}
    finally:
        archivo.close()

    return datos


def guardar_json(ruta, datos):
    """
    Sobrescribe un archivo JSON con la ultima version del diccionario.

    Parametros:
        ruta (str): ruta del archivo a escribir.
        datos (dict): diccionario a guardar.

    Retorna:
        bool: True si se guardo bien, False si hubo un error.
    """
    try:
        archivo = open(ruta, "w", encoding="utf-8")
        json.dump(datos, archivo, indent=4, ensure_ascii=False)
        archivo.close()
        return True
    except OSError:
        print("Error: no se pudo guardar el archivo", os.path.basename(ruta))
        return False


def registrar_venta_txt(linea):
    """
    Agrega una venta al final del archivo de texto ventas.txt.

    Parametros:
        linea (str): datos de la venta separados por ';'.

    Retorna:
        bool: True si se registro bien, False si hubo un error.
    """
    try:
        archivo = open(RUTA_VENTAS, "a", encoding="utf-8")
        archivo.write(linea + "\n")
        archivo.close()
        return True
    except OSError:
        print("Error: no se pudo registrar la venta en", os.path.basename(RUTA_VENTAS))
        return False


def leer_ventas_txt():
    """
    Lee el historial de ventas desde ventas.txt.

    Retorna:
        list: lista de listas, una por venta:
              [fecha, cliente, producto, categoria, cantidad, total, forma_pago]
    """
    ventas = []
    try:
        archivo = open(RUTA_VENTAS, "r", encoding="utf-8")
    except FileNotFoundError:
        # Si todavia no hubo ventas, el archivo no existe: no es un error grave
        return ventas

    try:
        for linea in archivo:
            linea = linea.strip()
            if linea != "":
                ventas.append(linea.split(";"))
    finally:
        archivo.close()

    return ventas
