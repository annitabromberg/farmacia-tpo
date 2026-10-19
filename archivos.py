"""
Modulo archivos: lectura y escritura de los archivos del sistema.

Persistencia en dos formatos:
- JSON: productos y clientes (diccionario de diccionarios).
- Texto plano (.txt): historial de ventas, una venta por linea.
"""

import json
import os

import validaciones


# Carpeta donde esta este archivo. Asi el programa encuentra los .json
# aunque se ejecute desde otra carpeta (por ejemplo, desde VS Code).
CARPETA = os.path.dirname(os.path.abspath(__file__))

RUTA_PRODUCTOS = os.path.join(CARPETA, "productos.json")
RUTA_CLIENTES = os.path.join(CARPETA, "clientes.json")
RUTA_PRODUCTOS_INICIAL = os.path.join(CARPETA, "productos_inicial.json")
RUTA_CLIENTES_INICIAL = os.path.join(CARPETA, "clientes_inicial.json")
RUTA_VENTAS = os.path.join(CARPETA, "ventas.txt")


def leer_json(ruta, tipo):
    """
    Lee un archivo JSON y devuelve su contenido como diccionario.

    Parametros:
        ruta (str): ruta del archivo a leer.
        tipo (str): tipo de registros ("productos" o "clientes").

    Retorna:
        dict o None: los datos leidos, o None si hubo un error.
    """
    try:
        archivo = open(ruta, "r", encoding="utf-8")
    except FileNotFoundError:
        print("Error: no se encontro el archivo", os.path.basename(ruta))
        return None
    except OSError:
        print("Error: no se pudo abrir el archivo", os.path.basename(ruta))
        return None

    try:
        datos = json.load(archivo)
    except json.JSONDecodeError:
        print("Error: el archivo", os.path.basename(ruta), "tiene un formato invalido.")
        return None
    except (OSError, UnicodeError):
        print("Error: no se pudo leer el archivo", os.path.basename(ruta))
        return None
    finally:
        archivo.close()

    try:
        validaciones.validar_registros(datos, tipo)
    except ValueError as error:
        print("Error: datos invalidos en", os.path.basename(ruta) + ":", error)
        return None

    return datos


def guardar_json(ruta, datos, tipo):
    """
    Sobrescribe un archivo JSON con la ultima version del diccionario.

    Parametros:
        ruta (str): ruta del archivo a escribir.
        datos (dict): diccionario a guardar.
        tipo (str): tipo de registros ("productos" o "clientes").

    Retorna:
        bool: True si se guardo bien, False si hubo un error.
    """
    try:
        validaciones.validar_registros(datos, tipo)
    except ValueError as error:
        print("Error: no se guardaron datos invalidos:", error)
        return False

    try:
        archivo = open(ruta, "w", encoding="utf-8")
    except OSError:
        print("Error: no se pudo guardar el archivo", os.path.basename(ruta))
        return False

    try:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)
        return True
    except OSError:
        print("Error: no se pudo guardar el archivo", os.path.basename(ruta))
        return False
    finally:
        archivo.close()


def registrar_venta_txt(linea):
    """
    Agrega una venta al final del archivo de texto ventas.txt.

    Parametros:
        linea (str): datos de la venta separados por ';'.

    Retorna:
        bool: True si se registro bien, False si hubo un error.
    """
    try:
        validaciones.validar_linea_venta(linea)
    except ValueError as error:
        print("Error: no se registro una venta con datos invalidos:", error)
        return False

    try:
        archivo = open(RUTA_VENTAS, "a", encoding="utf-8")
    except OSError:
        print("Error: no se pudo registrar la venta en", os.path.basename(RUTA_VENTAS))
        return False

    try:
        archivo.write(linea + "\n")
        return True
    except OSError:
        print("Error: no se pudo registrar la venta en", os.path.basename(RUTA_VENTAS))
        return False
    finally:
        archivo.close()


def leer_ventas_txt():
    """
    Lee el historial de ventas desde ventas.txt.

    Retorna:
        list o None: lista de listas, una por venta, o None si no se pudo leer:
              [fecha, cliente, producto, categoria, cantidad, total, forma_pago]
    """
    try:
        archivo = open(RUTA_VENTAS, "r", encoding="utf-8")
    except FileNotFoundError:
        # Si todavia no hubo ventas, el archivo no existe: no es un error grave
        return []
    except OSError:
        print("Error: no se pudo abrir el archivo", os.path.basename(RUTA_VENTAS))
        return None

    ventas = []
    try:
        numero_linea = 0
        for linea in archivo:
            numero_linea = numero_linea + 1
            linea = linea.rstrip("\r\n")
            if linea == "":
                continue
            try:
                ventas.append(validaciones.validar_linea_venta(linea))
            except ValueError as error:
                print("Aviso: se ignoro la linea", numero_linea, "de ventas.txt:", error)
    except (OSError, UnicodeError):
        print("Error: no se pudo leer el archivo", os.path.basename(RUTA_VENTAS))
        return None
    finally:
        archivo.close()

    return ventas
