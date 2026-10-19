"""
Modulo ventas: registra la venta de un producto a un cliente.

Reglas de negocio:
- Solo se vende si hay stock suficiente.
- Si el producto requiere receta, el cliente debe tener receta online.
- Los clientes con obra social tienen 40% de descuento en Medicamentos.
- Cada venta descuenta stock (se sobrescribe productos.json) y se guarda
  una linea en ventas.txt (historial en texto plano).
"""

import datetime
import archivos
import validaciones
import crud


FORMAS_PAGO = {"efectivo", "debito", "credito"}   # conjunto
DESCUENTO_OBRA_SOCIAL = 40                        # porcentaje


def calcular_total(precio, cantidad, tiene_obra_social, categoria):
    """
    Calcula subtotal, descuento y total de una venta.

    Parametros:
        precio (int): precio unitario.
        cantidad (int): unidades compradas.
        tiene_obra_social (bool): si el cliente tiene obra social.
        categoria (str): categoria del producto.

    Retorna:
        tuple: (subtotal, descuento, total)
    """
    subtotal = precio * cantidad
    descuento = 0
    if tiene_obra_social and categoria == "Medicamentos":
        descuento = subtotal * DESCUENTO_OBRA_SOCIAL // 100
    total = subtotal - descuento
    return (subtotal, descuento, total)


def realizar_venta():
    """
    Pide cliente, producto, cantidad y forma de pago, valida las reglas
    de negocio y registra la venta.
    """
    productos = archivos.leer_json(archivos.RUTA_PRODUCTOS, "productos")
    clientes = archivos.leer_json(archivos.RUTA_CLIENTES, "clientes")
    if productos is None or clientes is None:
        return

    print("\nNUEVA VENTA")
    print("-" * 30)

    codigo_cliente = validaciones.validar_entero("Codigo del cliente: ", 1)
    cliente = crud.buscar(clientes, codigo_cliente)
    if cliente is None:
        print("El cliente no existe.")
        return

    codigo_producto = validaciones.validar_entero("Codigo del producto: ", 1)
    producto = crud.buscar(productos, codigo_producto)
    if producto is None:
        print("El producto no existe.")
        return

    if producto["stock"] == 0:
        print("El producto no tiene stock.")
        return

    if producto["requiere_receta"] and not cliente["receta_online"]:
        print("Este producto requiere receta online y el cliente no la tiene.")
        return

    cantidad = validaciones.validar_entero(
        "Cantidad a comprar (disponibles: " + str(producto["stock"]) + "): ",
        1, producto["stock"]
    )

    tiene_obra_social = cliente["obra_social"].lower() != "ninguna"
    subtotal, descuento, total = calcular_total(
        producto["precio"], cantidad, tiene_obra_social, producto["categoria"]
    )

    print("\nRESUMEN DE LA VENTA")
    print("Cliente:", cliente["nombre"], cliente["apellido"])
    print("Producto:", producto["nombre"])
    print("Cantidad:", cantidad)
    print("Subtotal: $", subtotal)
    print("Descuento: $", descuento)
    print("Total a pagar: $", total)

    print("\nFormas de pago disponibles:", ", ".join(sorted(FORMAS_PAGO)))
    forma_pago = validaciones.validar_opcion("Forma de pago: ", FORMAS_PAGO)

    if not validaciones.validar_si_no("¿Confirmar la venta? (si/no): "):
        print("Venta cancelada.")
        return

    stock_anterior = producto["stock"]
    producto["stock"] = producto["stock"] - cantidad
    if not archivos.guardar_json(archivos.RUTA_PRODUCTOS, productos, "productos"):
        print("No se pudo actualizar el stock. La venta no se registro.")
        return

    fecha = datetime.date.today().strftime("%d/%m/%Y")
    linea = ";".join([
        fecha,
        cliente["nombre"] + " " + cliente["apellido"],
        producto["nombre"],
        producto["categoria"],
        str(cantidad),
        str(total),
        forma_pago
    ])
    if not archivos.registrar_venta_txt(linea):
        producto["stock"] = stock_anterior
        if not archivos.guardar_json(archivos.RUTA_PRODUCTOS, productos, "productos"):
            print("Error: no se pudo restaurar el stock despues del fallo.")
        print("No se pudo guardar la venta en el historial.")
        return

    print("\nVenta realizada correctamente.")
    print("Stock restante de", producto["nombre"] + ":", producto["stock"])
