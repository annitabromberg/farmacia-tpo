"""
Modulo validaciones: funciones para pedir datos por teclado de forma segura.

Cada funcion repite la pregunta hasta que el usuario ingresa un valor valido,
asi el programa nunca se corta por un dato mal escrito.
"""

import datetime


CATEGORIAS = ("Medicamentos", "Cuidado personal", "Perfumeria")
FORMAS_PAGO = ("efectivo", "debito", "credito")


def validar_registros(datos, tipo):
    """
    Comprueba la estructura y los tipos de los registros leidos o a guardar.

    Parametros:
        datos (dict): diccionario de productos o clientes.
        tipo (str): "productos" o "clientes".

    Retorna:
        bool: True cuando todos los registros son validos.

    Lanza ValueError con el detalle del dato invalido.
    """
    if tipo == "productos":
        campos = [
            ("nombre", str),
            ("categoria", str),
            ("precio", int),
            ("stock", int),
            ("requiere_receta", bool),
            ("laboratorio", str)
        ]
    elif tipo == "clientes":
        campos = [
            ("nombre", str),
            ("apellido", str),
            ("obra_social", str),
            ("receta_online", bool),
            ("telefono", str)
        ]
    else:
        raise ValueError("tipo de registros desconocido: " + str(tipo))
    if type(datos) != dict:
        raise ValueError("el contenido debe ser un objeto JSON")

    for codigo, registro in datos.items():
        if type(codigo) != str or not codigo.isdigit() or codigo[0] == "0":
            raise ValueError("el codigo de cada registro debe ser un entero positivo")
        try:
            numero_codigo = int(codigo)
        except ValueError:
            raise ValueError("el codigo de cada registro debe ser un entero positivo")
        if numero_codigo < 1:
            raise ValueError("el codigo de cada registro debe ser un entero positivo")
        if type(registro) != dict:
            raise ValueError("el registro " + codigo + " debe ser un objeto")
        if len(registro) != len(campos):
            raise ValueError("el registro " + codigo + " no tiene los campos esperados")

        for campo, tipo_esperado in campos:
            if campo not in registro:
                raise ValueError("falta el campo " + campo + " en el registro " + codigo)
            valor = registro[campo]
            if type(valor) != tipo_esperado:
                raise ValueError(
                    "el campo " + campo + " del registro " + codigo
                    + " debe ser de tipo " + tipo_esperado.__name__
                )
            if type(valor) == str:
                if valor.strip() == "":
                    raise ValueError("el campo " + campo + " del registro " + codigo + " no puede estar vacio")
                if ";" in valor or "\n" in valor or "\r" in valor:
                    raise ValueError("el campo " + campo + " del registro " + codigo + " contiene caracteres invalidos")

        if tipo == "productos":
            if len(registro["nombre"].strip()) < 2 or len(registro["laboratorio"].strip()) < 2:
                raise ValueError("nombre y laboratorio del producto " + codigo + " deben tener al menos dos caracteres")
            if registro["categoria"] not in CATEGORIAS:
                raise ValueError("categoria invalida en el producto " + codigo)
            if registro["precio"] < 1 or registro["stock"] < 0:
                raise ValueError("precio o stock invalido en el producto " + codigo)
        else:
            if len(registro["nombre"].strip()) < 2 or len(registro["apellido"].strip()) < 2:
                raise ValueError("nombre y apellido del cliente " + codigo + " deben tener al menos dos caracteres")
            if len(registro["obra_social"].strip()) < 2:
                raise ValueError("obra social del cliente " + codigo + " debe tener al menos dos caracteres")
            telefono = registro["telefono"]
            if not (telefono.isascii() and telefono.isdigit() and 8 <= len(telefono) <= 13):
                raise ValueError("telefono invalido en el cliente " + codigo)

    return True


def validar_linea_venta(linea):
    """
    Comprueba que una linea del historial tenga los siete campos esperados.

    Parametros:
        linea (str): datos de una venta separados por ';'.

    Retorna:
        list: los siete campos de la venta.

    Lanza ValueError si algun campo es invalido.
    """
    if not isinstance(linea, str):
        raise ValueError("la venta debe ser una cadena de texto")
    if "\r" in linea or "\n" in linea:
        raise ValueError("la venta no puede contener saltos de linea")
    campos = linea.split(";")
    if len(campos) != 7:
        raise ValueError("la venta debe tener exactamente siete campos no vacios")
    for campo in campos:
        if campo.strip() == "":
            raise ValueError("la venta debe tener exactamente siete campos no vacios")

    fecha, cliente, producto, categoria, cantidad, total, forma_pago = campos
    try:
        fecha_parseada = datetime.datetime.strptime(fecha, "%d/%m/%Y")
    except ValueError:
        raise ValueError("la fecha de la venta no es valida")
    if fecha_parseada.strftime("%d/%m/%Y") != fecha:
        raise ValueError("la fecha de la venta no tiene el formato esperado")
    if categoria not in CATEGORIAS:
        raise ValueError("categoria invalida en la venta")
    if forma_pago not in FORMAS_PAGO:
        raise ValueError("forma de pago invalida en la venta")
    if not cliente.strip() or not producto.strip():
        raise ValueError("cliente y producto de la venta no pueden estar vacios")
    if not cantidad.isdigit() or not total.isdigit():
        raise ValueError("cantidad y total de la venta deben ser enteros positivos")
    try:
        cantidad = int(cantidad)
        total = int(total)
    except ValueError:
        raise ValueError("cantidad y total de la venta deben ser enteros positivos")
    if cantidad < 1 or total < 1:
        raise ValueError("cantidad y total de la venta deben ser enteros positivos")
    return campos


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
        if len(texto) >= largo_minimo and not any(caracter in texto for caracter in ";\r\n"):
            return texto
        if any(caracter in texto for caracter in ";\r\n"):
            print("Error: no se permiten ';' ni saltos de linea.")
        else:
            print("Error: debe ingresar al menos", largo_minimo, "caracteres.")


def validar_texto_opcional(mensaje, largo_minimo=2):
    """
    Pide un texto que se puede dejar vacio (se usa al modificar).

    Parametros:
        mensaje (str): texto que se muestra al usuario.

    Retorna:
        str: el texto ingresado con la longitud minima, o "" si se dejo vacio.
    """
    while True:
        texto = input(mensaje).strip()
        if texto == "":
            return texto
        if len(texto) >= largo_minimo and not any(caracter in texto for caracter in ";\r\n"):
            return texto
        if any(caracter in texto for caracter in ";\r\n"):
            print("Error: no se permiten ';' ni saltos de linea.")
        else:
            print("Error: ingrese al menos", largo_minimo, "caracteres o deje el campo vacio.")


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
        if telefono.isascii() and telefono.isdigit() and 8 <= len(telefono) <= 13:
            return telefono
        print("Error: el telefono debe tener solo numeros (entre 8 y 13 digitos).")
