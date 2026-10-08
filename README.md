# FUNDAMENTOS_PROG

## Integrantes

- Juan David Rosas Vera --- 01250372016

- Juan Diego Alvarez Anteliz --- 01250372001

## Proyecto de aula: Tienda virtual en Python

Programa de consola que simula una tienda virtual: el usuario consulta un catálogo, arma un carrito de compras y paga con una factura en tabla. Desarrollado para la materia Fundamentos de Programación (UDES).

## Funcionalidades

- **Catálogo** con nombre, precio (USD) y stock de cada producto.
- **Comprar** eligiendo producto y cantidad. El stock baja al agregar al carrito y no permite pedir más de lo disponible.
- **Ver carrito** en tabla con producto, cantidad, precio unitario, subtotal y total.
- **Eliminar** parte o todas las unidades de un producto. El stock se devuelve al inventario.
- **Vaciar carrito** completo, devolviendo todo el stock.
- **Pagar y salir** con factura final en tabla. Si el carrito está vacío, avisa y vuelve al menú.
- **Validación de entradas**: rechaza texto, vacío, 0, negativos y números fuera de rango, sin cerrarse.

## Cómo ejecutarlo

Requiere Python 3.6 o superior. Desde la carpeta del proyecto:

```bash
python proyecto.py
```

En algunos sistemas el comando es `python3 proyecto.py`.

## Estructura del código

Todo está en `proyecto.py`, organizado en funciones de una sola tarea:

| Función                           | Qué hace                                                         |
| --------------------------------- | ---------------------------------------------------------------- |
| `mostrar_catalogo()`              | Imprime los productos con precio y stock                         |
| `agregar_al_carrito()`            | Valida la entrada, descuenta stock y agrega o suma al carrito    |
| `buscar_en_carrito()`             | Busca un producto en el carrito por su número                    |
| `calcular_total()`                | Devuelve la suma de `precio * cantidad`                          |
| `mostrar_tabla_carrito()`         | Imprime el carrito como tabla alineada                           |
| `ver_carrito()`                   | Muestra la tabla y el total                                      |
| `eliminar_del_carrito()`          | Quita unidades de un producto y devuelve el stock                |
| `vaciar_carrito()`                | Vacía el carrito y devuelve todo el stock                        |
| `facturar()`                      | Imprime la factura. Devuelve `True` si se facturó, `False` si no |
| `limpiar_pantalla()` y `pausar()` | Mejoran la lectura en consola                                    |
| `menu_principal()`                | Ciclo del menú que llama a todo lo anterior                      |

### Estructuras de datos

- `catalogo`: diccionario anidado. La llave es el número del producto y el valor lleva `nombre`, `precio` y `stock`.
- `carrito`: lista de diccionarios con `numero`, `nombre`, `precio` y `cantidad`. Cada producto aparece una sola vez.

## Librerías

Solo la librería estándar: `os`, usada para limpiar la consola.
