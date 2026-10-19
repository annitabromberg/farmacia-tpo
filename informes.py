"""
Modulo informes: reportes matriciales (listas de listas) con informacion
procesada de productos y ventas.
"""

import archivos
import validaciones
import crud


def imprimir_matriz(matriz, anchos):
    """
    Imprime una matriz (lista de listas) como tabla con columnas alineadas.
    La primera fila se toma como encabezado.

    Parametros:
        matriz (list): lista de listas; cada lista interna es una fila.
        anchos (list): ancho de cada columna.
    """
    for i in range(len(matriz)):
        fila = matriz[i]
        texto = ""
        for j in range(len(fila)):
            texto = texto + str(fila[j]).ljust(anchos[j]) + " | "
        print(texto)
        if i == 0:
            print("-" * len(texto))


def informe_stock():
    """
    Informe de stock: una fila por producto con su valor en stock
    (precio x unidades) y el total general al final.
    """
    productos = archivos.leer_json(archivos.RUTA_PRODUCTOS, "productos")
    if productos is None:
        return
    if len(productos) == 0:
        print("No hay productos cargados.")
        return

    matriz = [["Codigo", "Nombre", "Categoria", "Precio", "Stock", "Valor stock"]]
    valor_total = 0

    for codigo in productos:
        producto = productos[codigo]
        valor = producto["precio"] * producto["stock"]
        valor_total = valor_total + valor
        matriz.append([
            codigo,
            producto["nombre"],
            producto["categoria"],
            "$" + str(producto["precio"]),
            producto["stock"],
            "$" + str(valor)
        ])

    print("\nINFORME DE STOCK")
    imprimir_matriz(matriz, [6, 24, 16, 8, 5, 12])
    print("Valor total del inventario: $", valor_total)


def informe_categorias():
    """
    Resumen por categoria (reporte matricial): cantidad de productos,
    unidades en stock, valor del stock y productos con receta.
    Si matplotlib esta instalado, ademas muestra un grafico de barras.
    """
    productos = archivos.leer_json(archivos.RUTA_PRODUCTOS, "productos")
    if productos is None:
        return
    if len(productos) == 0:
        print("No hay productos cargados.")
        return

    matriz = [["Categoria", "Productos", "Unidades", "Valor stock", "Con receta"]]

    for categoria in crud.CATEGORIAS:
        # lista por comprension: productos de esta categoria
        de_la_categoria = [p for p in productos.values() if p["categoria"] == categoria]

        unidades = 0
        valor = 0
        con_receta = 0
        for producto in de_la_categoria:
            unidades = unidades + producto["stock"]
            valor = valor + producto["precio"] * producto["stock"]
            if producto["requiere_receta"]:
                con_receta = con_receta + 1

        matriz.append([categoria, len(de_la_categoria), unidades, "$" + str(valor), con_receta])

    print("\nRESUMEN POR CATEGORIA")
    imprimir_matriz(matriz, [16, 9, 8, 12, 10])

    graficar_categorias(matriz)


def graficar_categorias(matriz):
    """
    Muestra un grafico de barras con las unidades en stock por categoria
    y lo guarda como grafico_categorias.png.

    Parametros:
        matriz (list): la matriz generada en informe_categorias.
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("(Para ver el grafico instale matplotlib: pip install matplotlib)")
        return

    filas = matriz[1:]    # sin el encabezado
    categorias = [fila[0] for fila in filas]
    unidades = [fila[2] for fila in filas]

    plt.figure(figsize=(7, 4))
    plt.bar(categorias, unidades, color="#2a9d8f")
    plt.title("Unidades en stock por categoria")
    plt.ylabel("Unidades")
    plt.tight_layout()
    plt.savefig(archivos.CARPETA + "/grafico_categorias.png")
    print("Grafico guardado como grafico_categorias.png")
    plt.show()


def informe_bajo_stock():
    """
    Lista los productos con stock menor o igual a un limite que elige
    el usuario, ordenados de menor a mayor stock.
    """
    productos = archivos.leer_json(archivos.RUTA_PRODUCTOS, "productos")
    if productos is None:
        return
    limite = validaciones.validar_entero("Mostrar productos con stock menor o igual a: ", 0)

    # lista por comprension + lambda para ordenar
    bajo_stock = [p for p in productos.values() if p["stock"] <= limite]
    bajo_stock.sort(key=lambda p: p["stock"])

    print("\nPRODUCTOS CON STOCK MENOR O IGUAL A", limite)
    if len(bajo_stock) == 0:
        print("No hay productos con bajo stock.")
        return

    for producto in bajo_stock:
        print("-", producto["nombre"], "| Stock:", producto["stock"])


def informe_ventas():
    """
    Reporte matricial de ventas leido de ventas.txt:
    filas = formas de pago, columnas = categorias, celdas = total vendido ($).
    """
    ventas = archivos.leer_ventas_txt()
    if ventas is None:
        return
    if len(ventas) == 0:
        print("Todavia no hay ventas registradas.")
        return

    formas_pago = ("efectivo", "debito", "credito")    # tupla con el orden de las filas
    categorias = crud.CATEGORIAS

    # Matriz de ceros: una fila por forma de pago, una columna por categoria
    totales = [[0 for c in categorias] for f in formas_pago]

    for venta in ventas:
        categoria = venta[3]
        total = int(venta[5])
        forma_pago = venta[6]
        fila = formas_pago.index(forma_pago)
        columna = categorias.index(categoria)
        totales[fila][columna] = totales[fila][columna] + total

    matriz = [["Forma de pago"] + list(categorias) + ["TOTAL"]]
    for i in range(len(formas_pago)):
        matriz.append([formas_pago[i]] + totales[i] + [sum(totales[i])])

    print("\nVENTAS ($) POR FORMA DE PAGO Y CATEGORIA")
    print("Cantidad de ventas registradas:", len(ventas))
    imprimir_matriz(matriz, [14, 13, 17, 11, 10])
