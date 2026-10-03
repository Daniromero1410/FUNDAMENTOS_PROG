#Proyecto carrito de compras en python
#Primera entrega del proyecto de Fundamentos de Programación
#--------------------------------------------------------------------------------------------------------------------------------------------

import os

#Catalogo de productos (definido desde el inicio)
#Precio en USD
catalogo = {
    1: {"nombre": "Laptop", "precio": 800},
    2: {"nombre": "Monitor", "precio": 150},
    3: {"nombre": "Teclado mecanico", "precio": 80},
    4: {"nombre": "Mouse inalambrico", "precio": 25},
    5: {"nombre": "Audifonos inalambricos", "precio": 60},
}

#carrito de compras (inicialmente vacío)
carrito = []

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
        print(f"{numero}. {producto['nombre']} - ${producto['precio']}")

#--------------------------------------------------------------------------------------------------------------------------------------------
# Agregar producto al carrito
def agregar_al_carrito():
    entrada = input("\nIngrese el número del producto que desea agregar al carrito: ")

    #evitar errores de ingreso de datos
    if not entrada.isdigit():
        print("Por favor, ingrese un número válido.")
        return
        
    # Se convierte la entrada a un número entero
    numero_producto = int(entrada)

    if numero_producto in catalogo:
        producto = catalogo[numero_producto]
        carrito.append(producto)
        print(f"\n{producto['nombre']} ha sido agregado al carrito.")
    else:
        print("No existe ese producto en el catálogo.")

#--------------------------------------------------------------------------------------------------------------------------------------------
# Opcion de ver carrito.
def ver_carrito():
    if len(carrito) == 0:
        print("\nEl carrito está vacío.")
    else:
        for item in carrito:
            print(f"\n- {item['nombre']} (${item['precio']})")
            
        print(f"\nTotal a pagar: ${calcular_total()}")

#--------------------------------------------------------------------------------------------------------------------------------------------
# Calcular el carrito total 

def calcular_total():
    total = 0
    for item in carrito:
        total += item['precio']
    return total

#--------------------------------------------------------------------------------------------------------------------------------------------
# Facturar

def facturar():
    if calcular_total() == 0:
        print("\nEl carrito está vacío. No se puede generar una factura.")
        return False
    print("\n========================================")
    print("              FACTURA FINAL             ")
    print("========================================")
    ver_carrito()
    print("\n¡Gracias por tu compra! Vuelve pronto.")
    return True
    

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
        print("4. Pagar y salir")
 
        opcion = input("\nSeleccione una opción (1-4): ")
 
        # Se limpia otra vez para que el resultado se vea solo, sin el menú encima
        limpiar_pantalla()
 
        if opcion == "1":
            mostrar_catalogo()
        elif opcion == "2":
            agregar_al_carrito()
        elif opcion == "3":
            ver_carrito()
        elif opcion == "4":
            if facturar():
                break # Esto rompe el ciclo while y finaliza el programa (sin pausa, la factura queda visible)
        else:
            print("Opción inválida. Por favor, seleccione una opción del 1 al 4.")
 
        # Pausa antes de volver al menú para que alcance a leer el resultado
        pausar()

#--------------------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    menu_principal()
#---------------------------------------------------------------------------------------------------------------------------------------------


