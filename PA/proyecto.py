#Proyecto carrito de compras en python
#Primera y segunda entrega del proyecto de Fundamentos de Programación (hasta RF-18)
#--------------------------------------------------------------------------------------------------------------------------------------------

import os

#Catalogo de productos (definido desde el inicio)
#Precio en USD
catalogo = {
    1: {"nombre": "Laptop", "precio": 800, "stock": 10},
    2: {"nombre": "Monitor", "precio": 150, "stock": 5},
    3: {"nombre": "Teclado mecanico", "precio": 80, "stock": 20},
    4: {"nombre": "Mouse inalambrico", "precio": 25, "stock": 15},
    5: {"nombre": "Audifonos inalambricos", "precio": 60, "stock": 8},
}

#carrito de compras (inicialmente vacío)
#Cada elemento: {"numero": llave del catálogo, "nombre": ..., "precio": ..., "cantidad": ...}
carrito = []

#--------------------------------------------------------------------------------------------------------------------------------------------
# Limpiar la consola (cls en Windows, clear en Mac y Linux)
def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

#--------------------------------------------------------------------------------------------------------------------------------------------
# Pausa para que el usuario alcance a leer antes de volver al menú
def pausar():
    input("\nPresiona Enter para continuar...")

#--------------------------------------------------------------------------------------------------------------------------------------------
# Mostrar catalogo con ciclo for
def mostrar_catalogo():
    print("\n--- CATÁLOGO ---")
    for numero, producto in catalogo.items():
        print(f"{numero}. {producto['nombre']} - ${producto['precio']} (Stock: {producto['stock']})")

#--------------------------------------------------------------------------------------------------------------------------------------------
# Buscar un producto dentro del carrito por su número de catálogo
# Devuelve el elemento del carrito, o None si no está
def  buscar_en_carrito(numero_producto):
    for item in carrito:
        if item["numero"] == numero_producto:
            return item
    return None

#--------------------------------------------------------------------------------------------------------------------------------------------
# Agregar producto al carrito
def agregar_al_carrito():
    mostrar_catalogo()
    entrada = input("\nIngrese el número del producto que desea agregar al carrito: ")

    # RF-10: validar que sea un número
    if not entrada.isdigit():
        print("\nPor favor, ingrese un número válido.")
        return

    numero_producto = int(entrada)

    # RF-11: el producto debe existir en el catálogo
    if numero_producto not in catalogo:
        print("\nNo existe ese producto en el catálogo.")
        return

    producto = catalogo[numero_producto]
    texto_cantidad = input(f"Ingrese la cantidad de {producto['nombre']} que desea agregar: ")

    if not texto_cantidad.isdigit():
        print("\nPor favor, ingrese una cantidad válida.")
        return

    cantidad = int(texto_cantidad)

    # RF-11: la cantidad debe ser mayor que cero
    if cantidad <= 0:
        print("\nLa cantidad debe ser mayor que 0.")
        return

    # RF-15: no se permite pedir más de lo que hay en stock
    if cantidad > producto["stock"]:
        print(f"\nSolo quedan {producto['stock']} unidades de {producto['nombre']}.")
        return

    # RF-14: el stock baja al agregar al carrito
    producto["stock"] -= cantidad

    # RF-16: si el producto ya está en el carrito, se suma la cantidad; si no, se crea
    item = buscar_en_carrito(numero_producto)
    if item is not None:
        item["cantidad"] += cantidad
    else:
        carrito.append({
            "numero": numero_producto,
            "nombre": producto["nombre"],
            "precio": producto["precio"],
            "cantidad": cantidad,
        })

    print(f"\n{cantidad} x {producto['nombre']} agregado(s) al carrito.")

#--------------------------------------------------------------------------------------------------------------------------------------------
# Calcular el carrito total (suma de precio * cantidad)
def calcular_total():
    total = 0
    for item in carrito:
        total += item["precio"] * item["cantidad"]
    return total

#--------------------------------------------------------------------------------------------------------------------------------------------
# Imprimir el carrito como tabla alineada (RF-18)
# Columnas: producto, cantidad, precio unitario y subtotal
def mostrar_tabla_carrito():
    print(f"{'Num.':<6}{'Producto':<25}{'Cant.':>6}{'Precio':>10}{'Subtotal':>11}")
    print("-" * 58)
    for item in carrito:
        subtotal = item["precio"] * item["cantidad"]
        precio = "$" + str(item["precio"])
        subtotal = "$" + str(subtotal)
        print(f"{item['numero']:<6}{item['nombre']:<25}{item['cantidad']:>6}{precio:>10}{subtotal:>11}")
    print("-" * 58)

#--------------------------------------------------------------------------------------------------------------------------------------------
# Opcion de ver carrito.
def ver_carrito():
    if len(carrito) == 0:
        print("\nEl carrito está vacío.")
    else:
        print("\n--- TU CARRITO ---\n")
        mostrar_tabla_carrito()
        print(f"{'Total a pagar:':<47}{'$' + str(calcular_total()):>11}")

#--------------------------------------------------------------------------------------------------------------------------------------------
# Eliminar un producto del carrito (RF-17): el stock vuelve al inventario
def eliminar_del_carrito():
    if len(carrito) == 0:
        print("\nEl carrito está vacío, no hay nada que eliminar.")
        return

    ver_carrito()
    entrada = input("\nIngrese el número del producto que desea eliminar: ")

    if not entrada.isdigit():
        print("\nPor favor, ingrese un número válido.")
        return

    numero_producto = int(entrada)
    item = buscar_en_carrito(numero_producto)

    if item is None:
        print("\nEse producto no está en el carrito.")
        return

    texto = input(f"Tiene {item['cantidad']} de {item['nombre']}. "
                  f"¿Cuántas desea eliminar? (número o 'todo'): ").strip().lower()

    if texto == "todo":
        cantidad = item["cantidad"]
    elif texto.isdigit():
        cantidad = int(texto)
    else:
        print("\nPor favor, ingrese una cantidad válida.")
        return

    if cantidad <= 0:
        print("\nLa cantidad debe ser mayor que 0.")
        return

    if cantidad > item["cantidad"]:
        print(f"\nSolo tiene {item['cantidad']} unidades de {item['nombre']} en el carrito.")
        return

    # Se devuelve al inventario lo que se quita del carrito
    catalogo[numero_producto]["stock"] += cantidad
    item["cantidad"] -= cantidad

    # Si no queda ninguna unidad, el producto sale del carrito
    if item["cantidad"] == 0:
        carrito.remove(item)
        print(f"\n{item['nombre']} fue eliminado del carrito.")
    else:
        print(f"\nSe eliminaron {cantidad} unidades de {item['nombre']}. Quedan {item['cantidad']}.")

#--------------------------------------------------------------------------------------------------------------------------------------------
# Vaciar el carrito completo (RF-17): todo el stock vuelve al inventario
def vaciar_carrito():
    if len(carrito) == 0:
        print("\nEl carrito ya está vacío.")
        return

    for item in carrito:
        catalogo[item["numero"]]["stock"] += item["cantidad"]
    carrito.clear()
    print("\nSe vació el carrito.")

#--------------------------------------------------------------------------------------------------------------------------------------------
# Facturar
# Devuelve True si se generó la factura, False si el carrito estaba vacío
def facturar():
    if calcular_total() == 0:
        print("\nEl carrito está vacío. No se puede generar una factura.")
        return False
    print("\n========================================")
    print("              FACTURA FINAL             ")
    print("========================================\n")
    mostrar_tabla_carrito()
    print(f"{'Total a pagar:':<47}{'$' + str(calcular_total()):>11}")
    print("\n¡Gracias por tu compra! Vuelve pronto.")
    return True

#--------------------------------------------------------------------------------------------------------------------------------------------
#menu principal
def menu_principal():
    limpiar_pantalla()
    print("\n--- ¡Bienvenido a nuestra tienda virtual!  ---")
    pausar()

    while True:
        # Cada vuelta empieza con la pantalla limpia y solo el menú
        limpiar_pantalla()
        print("\n--- MENÚ PRINCIPAL ---")
        print("1. Mostrar catálogo")
        print("2. Comprar")
        print("3. Ver carrito")
        print("4. Eliminar un producto del carrito")
        print("5. Vaciar carrito")
        print("6. Pagar y salir")

        opcion = input("\nSeleccione una opción (1-6): ")

        # Se limpia otra vez para que el resultado se vea solo, sin el menú encima
        limpiar_pantalla()

        if opcion == "1":
            mostrar_catalogo()
        elif opcion == "2":
            agregar_al_carrito()
        elif opcion == "3":
            ver_carrito()
        elif opcion == "4":
            eliminar_del_carrito()
        elif opcion == "5":
            vaciar_carrito()
        elif opcion == "6":
            if facturar():
                break # Rompe el ciclo y finaliza el programa (sin pausa, la factura queda visible)
        else:
            print("Opción inválida. Por favor, seleccione una opción del 1 al 6.")

        # Pausa antes de volver al menú para que alcance a leer el resultado
        pausar()

#--------------------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    menu_principal()
#---------------------------------------------------------------------------------------------------------------------------------------------
