# Sistema de gestion de farmacia

## Validacion de datos y persistencia

Los productos y clientes se guardan como objetos JSON cuyas claves son
codigos numericos positivos escritos como texto. Antes de utilizar un archivo,
`leer_json` valida la estructura de todos sus registros; `guardar_json` valida
los mismos datos antes de sobrescribir el archivo. Un archivo JSON mal formado,
con campos faltantes o adicionales, o con valores de tipo incorrecto no se
carga ni se guarda. La lectura informa el error y retorna `None`, por lo que la
operacion que la solicito se interrumpe sin tratar el archivo como una
coleccion vacia.

### Esquema de productos

Cada registro debe incluir exactamente estos campos:

| Campo | Tipo | Restriccion |
|---|---|---|
| `nombre` | texto | Al menos dos caracteres |
| `categoria` | texto | `Medicamentos`, `Cuidado personal` o `Perfumeria` |
| `precio` | entero | Mayor que cero |
| `stock` | entero | Cero o mayor |
| `requiere_receta` | booleano | `true` o `false` |
| `laboratorio` | texto | Al menos dos caracteres |

### Esquema de clientes

Cada registro debe incluir exactamente estos campos:

| Campo | Tipo | Restriccion |
|---|---|---|
| `nombre` | texto | Al menos dos caracteres |
| `apellido` | texto | Al menos dos caracteres |
| `obra_social` | texto | Al menos dos caracteres |
| `receta_online` | booleano | `true` o `false` |
| `telefono` | texto | Solo digitos, de 8 a 13 caracteres |

Los campos de texto no pueden contener `;` ni saltos de linea, para no alterar
el formato del historial. Los enteros del JSON se comprueban estrictamente:
un booleano no cuenta como entero.

El historial `ventas.txt` contiene una venta por linea y siete campos
separados por punto y coma: fecha (`dd/mm/aaaa`), cliente, producto,
categoria, cantidad, total y forma de pago. Al leerlo, se validan todos los
campos y se ignoran las lineas invalidas con un aviso que identifica el numero
de linea. Al escribir una venta, se rechazan registros que no cumplan el
formato.

La validacion de datos ingresados por teclado sigue en `validaciones.py`;
las validaciones de esquema tambien se aplican en las funciones de persistencia,
para proteger los datos aunque no provengan de los formularios de la aplicacion.
