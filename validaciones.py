"""
Modulo validaciones: funciones para pedir datos por teclado de forma segura.

Cada funcion repite la pregunta hasta que el usuario ingresa un valor valido,
asi el programa nunca se corta por un dato mal escrito.
"""


def validar_entero(mensaje, minimo=None, maximo=None):
    """
    Pide un numero entero y lo valida.

    Parametros:
        mensaje (str): texto que se muestra al usuario.
        minimo (int): valor minimo permitido (opcional).
        maximo (int): valor maximo permitido (opcional).

    Retorna:
        int: el numero ingresado, ya validado.
    """
    while True:
        try:
            numero = int(input(mensaje))
        except ValueError:
            print("Error: debe ingresar un numero entero.")
            continue

        if minimo is not None and numero < minimo:
            print("Error: el valor debe ser mayor o igual a", minimo)
        elif maximo is not None and numero > maximo:
            print("Error: el valor debe ser menor o igual a", maximo)
        else:
            return numero


def validar_entero_opcional(mensaje, minimo=None):
    """
    Pide un numero entero que se puede dejar vacio (se usa al modificar).

    Parametros:
        mensaje (str): texto que se muestra al usuario.
        minimo (int): valor minimo permitido (opcional).

    Retorna:
        int: el numero ingresado, o None si el usuario dejo el campo vacio.
    """
    while True:
        texto = input(mensaje).strip()
        if texto == "":
            return None
        try:
            numero = int(texto)
        except ValueError:
            print("Error: debe ingresar un numero entero o dejarlo vacio.")
            continue

        if minimo is not None and numero < minimo:
            print("Error: el valor debe ser mayor o igual a", minimo)
        else:
            return numero


def validar_texto(mensaje, largo_minimo=2):
    """
    Pide un texto que no este vacio.

    Parametros:
        mensaje (str): texto que se muestra al usuario.
        largo_minimo (int): cantidad minima de caracteres.

    Retorna:
        str: el texto ingresado, sin espacios al principio ni al final.
    """
    while True:
        texto = input(mensaje).strip()
        if len(texto) >= largo_minimo:
            return texto
        print("Error: debe ingresar al menos", largo_minimo, "caracteres.")


def validar_texto_opcional(mensaje):
    """
    Pide un texto que se puede dejar vacio (se usa al modificar).

    Parametros:
        mensaje (str): texto que se muestra al usuario.

    Retorna:
        str: el texto ingresado, o "" si se dejo vacio.
    """
    return input(mensaje).strip()


def validar_si_no(mensaje):
    """
    Pide una respuesta si/no.

    Parametros:
        mensaje (str): texto que se muestra al usuario.

    Retorna:
        bool: True si respondio "si", False si respondio "no".
    """
    respuestas_validas = {"si", "no"}   # conjunto
    respuesta = input(mensaje).strip().lower()
    while respuesta not in respuestas_validas:
        print("Error: responda 'si' o 'no'.")
        respuesta = input(mensaje).strip().lower()
    return respuesta == "si"


def validar_opcion(mensaje, opciones):
    """
    Pide un texto que tiene que estar dentro de una coleccion de opciones.
    No distingue mayusculas de minusculas.

    Parametros:
        mensaje (str): texto que se muestra al usuario.
        opciones (tuple o set): opciones permitidas.

    Retorna:
        str: la opcion elegida, escrita igual que en la coleccion.
    """
    while True:
        texto = input(mensaje).strip().lower()
        for opcion in opciones:
            if opcion.lower() == texto:
                return opcion
        print("Error: opcion invalida. Opciones:", ", ".join(opciones))


def validar_telefono(mensaje):
    """
    Pide un telefono: solo numeros y entre 8 y 13 digitos.

    Parametros:
        mensaje (str): texto que se muestra al usuario.

    Retorna:
        str: el telefono validado (se guarda como texto).
    """
    while True:
        telefono = input(mensaje).strip()
        if telefono.isdigit() and 8 <= len(telefono) <= 13:
            return telefono
        print("Error: el telefono debe tener solo numeros (entre 8 y 13 digitos).")
