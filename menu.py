"""
SISTEMA DE GESTION DE FARMACIA - TPO Programacion I - Grupo 4

Archivo principal: ejecutar este archivo para iniciar el programa.
    python menu.py

Modulos:
    archivos.py     -> lectura/escritura de JSON y del historial ventas.txt
    validaciones.py -> funciones para validar datos ingresados (str e int)
    precarga.py     -> carga inicial desde productos_inicial.json y clientes_inicial.json
    crud.py         -> alta, consulta, modificacion y baja de productos y clientes
    ventas.py       -> registro de ventas
    informes.py     -> reportes matriciales
"""

import precarga
import crud
import ventas
import informes
import validaciones


def menu_productos():
    """
    Submenu con el CRUD completo de productos.
    """
    while True:
        print("\nMENU DE PRODUCTOS")
        print("1. Ver todos los productos")
        print("2. Ver productos ordenados por precio")
        print("3. Buscar un producto")
        print("4. Agregar producto")
        print("5. Modificar producto")
        print("6. Eliminar producto")
        print("0. Volver al menu principal")

        opcion = input("Seleccione una opcion: ").strip()

        if opcion == "1":
            crud.ver_productos()
        elif opcion == "2":
            crud.ver_productos("precio")
        elif opcion == "3":
            crud.ver_producto()
        elif opcion == "4":
            crud.agregar_producto()
        elif opcion == "5":
            crud.modificar_producto()
        elif opcion == "6":
            crud.eliminar_producto()
        elif opcion == "0":
            break
        else:
            print("Opcion incorrecta.")


def menu_clientes():
    """
    Submenu con el CRUD completo de clientes.
    """
    while True:
        print("\nMENU DE CLIENTES")
        print("1. Ver todos los clientes")
        print("2. Buscar un cliente")
        print("3. Agregar cliente")
        print("4. Modificar cliente")
        print("5. Eliminar cliente")
        print("0. Volver al menu principal")

        opcion = input("Seleccione una opcion: ").strip()

        if opcion == "1":
            crud.ver_clientes()
        elif opcion == "2":
            crud.ver_cliente()
        elif opcion == "3":
            crud.agregar_cliente()
        elif opcion == "4":
            crud.modificar_cliente()
        elif opcion == "5":
            crud.eliminar_cliente()
        elif opcion == "0":
            break
        else:
            print("Opcion incorrecta.")


def menu_informes():
    """
    Submenu de informes y reportes matriciales.
    """
    while True:
        print("\nMENU DE INFORMES")
        print("1. Informe de stock y valor del inventario")
        print("2. Resumen por categoria (con grafico)")
        print("3. Productos con bajo stock")
        print("4. Ventas por forma de pago y categoria")
        print("0. Volver al menu principal")

        opcion = input("Seleccione una opcion: ").strip()

        if opcion == "1":
            informes.informe_stock()
        elif opcion == "2":
            informes.informe_categorias()
        elif opcion == "3":
            informes.informe_bajo_stock()
        elif opcion == "4":
            informes.informe_ventas()
        elif opcion == "0":
            break
        else:
            print("Opcion incorrecta.")


def menu_principal():
    """
    Menu principal del sistema. Antes de mostrarlo, hace la precarga
    de datos si los archivos de trabajo todavia no existen.
    """
    precarga.cargar_datos()

    while True:
        print("\n================================")
        print(" SISTEMA DE GESTION DE FARMACIA")
        print("================================")
        print("1. Gestionar productos")
        print("2. Gestionar clientes")
        print("3. Realizar venta")
        print("4. Ver informes")
        print("5. Restaurar datos iniciales")
        print("0. Salir")

        opcion = input("Seleccione una opcion: ").strip()

        if opcion == "1":
            menu_productos()
        elif opcion == "2":
            menu_clientes()
        elif opcion == "3":
            ventas.realizar_venta()
        elif opcion == "4":
            menu_informes()
        elif opcion == "5":
            if validaciones.validar_si_no("Se perderan los cambios. ¿Continuar? (si/no): "):
                precarga.restaurar_datos()
        elif opcion == "0":
            print("Gracias por utilizar el sistema.")
            break
        else:
            print("Opcion incorrecta.")


try:
    menu_principal()
except (KeyboardInterrupt, EOFError):
    # Si el usuario aprieta Ctrl+C, el programa termina sin mostrar errores
    print("\nPrograma finalizado por el usuario.")
