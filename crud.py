"""
Modulo crud: alta, consulta, modificacion y baja de productos y clientes.

Productos y clientes se guardan como DICCIONARIO DE DICCIONARIOS:
la clave es el codigo (como texto, porque JSON siempre guarda las claves
como texto) y el valor es otro diccionario con los atributos.

Ejemplo:
    {"1": {"nombre": "Paracetamol 500mg", "categoria": "Medicamentos",
           "precio": 2500, "stock": 20, "requiere_receta": false,
           "laboratorio": "Bayer"}}

Create, Update y Delete sobrescriben el archivo con la ultima version
del diccionario. Read lee esa ultima version.
"""

import archivos
import validaciones


CATEGORIAS = ("Medicamentos", "Cuidado personal", "Perfumeria")   # tupla


# ----------------------------------------------------------------------
# Funciones auxiliares
# ----------------------------------------------------------------------

def nuevo_codigo(diccionario):
    """
    Calcula el proximo codigo libre (el mayor codigo + 1).

    Parametros:
        diccionario (dict): productos o clientes.

    Retorna:
        str: el nuevo codigo, como texto.
    """
    codigos = [int(clave) for clave in diccionario]   # lista por comprension
    if len(codigos) == 0:
        return "1"
    return str(max(codigos) + 1)


def buscar(diccionario, codigo):
    """
    Busca un registro por su codigo.

    Parametros:
        diccionario (dict): productos o clientes.
        codigo (int): codigo ingresado por el usuario.

    Retorna:
        dict: el registro encontrado, o None si no existe.
    """
    try:
        return diccionario[str(codigo)]
    except KeyError:
        return None


def texto_si_no(valor):
    """
    Convierte un booleano en "Si" o "No" para mostrarlo en pantalla.

    Parametros:
        valor (bool): valor a convertir.

    Retorna:
        str: "Si" o "No".
    """
    if valor:
        return "Si"
    return "No"


# ----------------------------------------------------------------------
# PRODUCTOS
# ----------------------------------------------------------------------

def mostrar_producto(codigo, producto):
    """
    Muestra en una linea los datos de un producto.

    Parametros:
        codigo (str): codigo del producto.
        producto (dict): datos del producto.
    """
    print(
        codigo.rjust(3), "|",
        producto["nombre"].ljust(24), "|",
        producto["categoria"].ljust(16), "| $",
        str(producto["precio"]).rjust(6), "| Stock:",
        str(producto["stock"]).rjust(3), "| Receta:",
        texto_si_no(producto["requiere_receta"])
    )


def ver_productos(orden="codigo"):
    """
    READ general: lista todos los productos.

    Parametros:
        orden (str): "codigo" o "precio". Para ordenar por precio se usa
                     una funcion lambda como criterio de ordenamiento.
    """
    productos = archivos.leer_json(archivos.RUTA_PRODUCTOS)
    if len(productos) == 0:
        print("No hay productos cargados.")
        return

    items = list(productos.items())
    if orden == "precio":
        items.sort(key=lambda item: item[1]["precio"])        # lambda
    else:
        items.sort(key=lambda item: int(item[0]))

    print("\nLISTADO DE PRODUCTOS")
    print("-" * 95)
    for codigo, producto in items:
        mostrar_producto(codigo, producto)


def ver_producto():
    """
    READ individual: muestra todos los datos de un producto.
    """
    productos = archivos.leer_json(archivos.RUTA_PRODUCTOS)
    codigo = validaciones.validar_entero("Ingrese el codigo del producto: ", 1)
    producto = buscar(productos, codigo)

    if producto is None:
        print("No se encontro el producto.")
        return

    print("\nDATOS DEL PRODUCTO")
    print("Codigo:", codigo)
    print("Nombre:", producto["nombre"])
    print("Categoria:", producto["categoria"])
    print("Precio: $", producto["precio"])
    print("Stock:", producto["stock"])
    print("Requiere receta:", texto_si_no(producto["requiere_receta"]))
    print("Laboratorio:", producto["laboratorio"])


def agregar_producto():
    """
    CREATE: da de alta un producto nuevo y sobrescribe productos.json.
    """
    productos = archivos.leer_json(archivos.RUTA_PRODUCTOS)

    nombre = validaciones.validar_texto("Nombre del producto: ")

    # Validacion con un conjunto: no se permiten nombres repetidos
    nombres_existentes = set()
    for producto in productos.values():
        nombres_existentes.add(producto["nombre"].lower())
    if nombre.lower() in nombres_existentes:
        print("Ya existe un producto con ese nombre.")
        return

    print("Categorias disponibles:", ", ".join(CATEGORIAS))
    categoria = validaciones.validar_opcion("Categoria: ", CATEGORIAS)
    precio = validaciones.validar_entero("Precio (sin centavos): $", 1)
    stock = validaciones.validar_entero("Stock inicial: ", 0)
    requiere_receta = validaciones.validar_si_no("¿Requiere receta? (si/no): ")
    laboratorio = validaciones.validar_texto("Laboratorio: ")

    codigo = nuevo_codigo(productos)
    productos[codigo] = {
        "nombre": nombre,
        "categoria": categoria,
        "precio": precio,
        "stock": stock,
        "requiere_receta": requiere_receta,
        "laboratorio": laboratorio
    }

    if archivos.guardar_json(archivos.RUTA_PRODUCTOS, productos):
        print("Producto agregado correctamente con el codigo", codigo)


def modificar_producto():
    """
    UPDATE: modifica los atributos de un producto en el diccionario interno
    y sobrescribe productos.json. Si se deja un campo vacio, no se cambia.
    """
    productos = archivos.leer_json(archivos.RUTA_PRODUCTOS)
    codigo = validaciones.validar_entero("Codigo del producto a modificar: ", 1)
    producto = buscar(productos, codigo)

    if producto is None:
        print("No existe un producto con ese codigo.")
        return

    print("Producto:", producto["nombre"])
    print("Deja el campo vacio si no queres cambiarlo.")

    nombre = validaciones.validar_texto_opcional("Nuevo nombre: ")
    if nombre != "":
        producto["nombre"] = nombre

    precio = validaciones.validar_entero_opcional("Nuevo precio: $", 1)
    if precio is not None:
        producto["precio"] = precio

    stock = validaciones.validar_entero_opcional("Nuevo stock: ", 0)
    if stock is not None:
        producto["stock"] = stock

    laboratorio = validaciones.validar_texto_opcional("Nuevo laboratorio: ")
    if laboratorio != "":
        producto["laboratorio"] = laboratorio

    if validaciones.validar_si_no("¿Cambiar si requiere receta? (si/no): "):
        producto["requiere_receta"] = validaciones.validar_si_no("¿Requiere receta? (si/no): ")

    if archivos.guardar_json(archivos.RUTA_PRODUCTOS, productos):
        print("Producto modificado correctamente.")


def eliminar_producto():
    """
    DELETE: elimina un producto (pidiendo confirmacion) y sobrescribe
    productos.json.
    """
    productos = archivos.leer_json(archivos.RUTA_PRODUCTOS)
    codigo = validaciones.validar_entero("Codigo del producto a eliminar: ", 1)

    try:
        nombre = productos[str(codigo)]["nombre"]
    except KeyError:
        print("No existe un producto con ese codigo.")
        return

    if not validaciones.validar_si_no("¿Seguro que desea eliminar " + nombre + "? (si/no): "):
        print("Operacion cancelada.")
        return

    del productos[str(codigo)]
    if archivos.guardar_json(archivos.RUTA_PRODUCTOS, productos):
        print("Producto eliminado correctamente.")


# ----------------------------------------------------------------------
# CLIENTES
# ----------------------------------------------------------------------

def ver_clientes():
    """
    READ general: lista todos los clientes.
    """
    clientes = archivos.leer_json(archivos.RUTA_CLIENTES)
    if len(clientes) == 0:
        print("No hay clientes cargados.")
        return

    print("\nLISTADO DE CLIENTES")
    print("-" * 80)
    for codigo in clientes:
        cliente = clientes[codigo]
        print(
            codigo.rjust(3), "|",
            (cliente["nombre"] + " " + cliente["apellido"]).ljust(22), "| Obra social:",
            cliente["obra_social"].ljust(14), "| Receta online:",
            texto_si_no(cliente["receta_online"])
        )


def ver_cliente():
    """
    READ individual: muestra todos los datos de un cliente.
    """
    clientes = archivos.leer_json(archivos.RUTA_CLIENTES)
    codigo = validaciones.validar_entero("Ingrese el codigo del cliente: ", 1)
    cliente = buscar(clientes, codigo)

    if cliente is None:
        print("No se encontro el cliente.")
        return

    print("\nDATOS DEL CLIENTE")
    print("Codigo:", codigo)
    print("Nombre:", cliente["nombre"], cliente["apellido"])
    print("Obra social:", cliente["obra_social"])
    print("Receta online:", texto_si_no(cliente["receta_online"]))
    print("Telefono:", cliente["telefono"])


def agregar_cliente():
    """
    CREATE: da de alta un cliente nuevo y sobrescribe clientes.json.
    """
    clientes = archivos.leer_json(archivos.RUTA_CLIENTES)

    nombre = validaciones.validar_texto("Nombre del cliente: ")
    apellido = validaciones.validar_texto("Apellido del cliente: ")
    obra_social = validaciones.validar_texto("Obra social (o Ninguna): ")
    receta = validaciones.validar_si_no("¿Tiene receta online? (si/no): ")
    telefono = validaciones.validar_telefono("Telefono: ")

    codigo = nuevo_codigo(clientes)
    clientes[codigo] = {
        "nombre": nombre.title(),
        "apellido": apellido.title(),
        "obra_social": obra_social,
        "receta_online": receta,
        "telefono": telefono
    }

    if archivos.guardar_json(archivos.RUTA_CLIENTES, clientes):
        print("Cliente agregado correctamente con el codigo", codigo)


def modificar_cliente():
    """
    UPDATE: modifica los datos de un cliente y sobrescribe clientes.json.
    Si se deja un campo vacio, no se cambia.
    """
    clientes = archivos.leer_json(archivos.RUTA_CLIENTES)
    codigo = validaciones.validar_entero("Codigo del cliente a modificar: ", 1)
    cliente = buscar(clientes, codigo)

    if cliente is None:
        print("No existe un cliente con ese codigo.")
        return

    print("Cliente:", cliente["nombre"], cliente["apellido"])
    print("Deja el campo vacio si no queres cambiarlo.")

    obra_social = validaciones.validar_texto_opcional("Nueva obra social: ")
    if obra_social != "":
        cliente["obra_social"] = obra_social

    telefono = validaciones.validar_texto_opcional("Nuevo telefono: ")
    if telefono != "":
        if telefono.isdigit() and 8 <= len(telefono) <= 13:
            cliente["telefono"] = telefono
        else:
            print("Telefono invalido. Se mantiene el anterior.")

    if validaciones.validar_si_no("¿Cambiar receta online? (si/no): "):
        cliente["receta_online"] = validaciones.validar_si_no("¿Tiene receta online? (si/no): ")

    if archivos.guardar_json(archivos.RUTA_CLIENTES, clientes):
        print("Cliente modificado correctamente.")


def eliminar_cliente():
    """
    DELETE: elimina un cliente (pidiendo confirmacion) y sobrescribe
    clientes.json.
    """
    clientes = archivos.leer_json(archivos.RUTA_CLIENTES)
    codigo = validaciones.validar_entero("Codigo del cliente a eliminar: ", 1)

    try:
        cliente = clientes[str(codigo)]
    except KeyError:
        print("No existe un cliente con ese codigo.")
        return

    nombre = cliente["nombre"] + " " + cliente["apellido"]
    if not validaciones.validar_si_no("¿Seguro que desea eliminar a " + nombre + "? (si/no): "):
        print("Operacion cancelada.")
        return

    del clientes[str(codigo)]
    if archivos.guardar_json(archivos.RUTA_CLIENTES, clientes):
        print("Cliente eliminado correctamente.")
