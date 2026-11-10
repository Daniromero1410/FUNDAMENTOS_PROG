# AVANCE - RENTA DE AUTOS (sin librerías)
# Usa: listas, diccionarios, if/elif/else, while y for

# ----------------------------------------------------------------------
# DATOS
# ----------------------------------------------------------------------

# Lista de diccionarios: cada diccionario es un vehículo
vehiculos = [
    {"placa": "ABC123", "marca": "Chevrolet", "modelo": "Spark", "precio_dia": 80000, "disponible": True},
    {"placa": "GHI789", "marca": "Mazda", "modelo": "3", "precio_dia": 140000, "disponible": True},
    {"placa": "MNO345", "marca": "Kia", "modelo": "Sportage", "precio_dia": 220000, "disponible": True},
    {"placa": "STU901", "marca": "Mercedes", "modelo": "C200", "precio_dia": 400000, "disponible": True},
]

# Diccionario de clientes: la llave es la cédula
clientes = {
    "1001": {"nombre": "Ana Torres", "telefono": "3001112233"},
}

# Lista donde se guardan los alquileres
alquileres = []


# ----------------------------------------------------------------------
# FUNCIONES
# ----------------------------------------------------------------------

def mostrar_vehiculos():
    print("\n--- VEHÍCULOS ---")
    for v in vehiculos:
        if v["disponible"]:
            estado = "Disponible"
        else:
            estado = "Alquilado"
        print(f"{v['placa']} | {v['marca']} {v['modelo']} | ${v['precio_dia']} por día | {estado}")


def registrar_cliente():
    print("\n--- REGISTRAR CLIENTE ---")
    cedula = input("Cédula: ")

    if cedula in clientes:
        print("Ese cliente ya está registrado.")
    else:
        nombre = input("Nombre: ")
        telefono = input("Teléfono: ")
        clientes[cedula] = {"nombre": nombre, "telefono": telefono}
        print("Cliente registrado.")


def alquilar():
    print("\n--- ALQUILAR VEHÍCULO ---")
    cedula = input("Cédula del cliente: ")

    if cedula not in clientes:
        print("El cliente no existe. Primero regístralo.")
        return

    mostrar_vehiculos()
    placa = input("Placa del vehículo: ").upper()

    # Buscar el vehículo en la lista
    auto = None
    for v in vehiculos:
        if v["placa"] == placa:
            auto = v

    if auto is None:
        print("Esa placa no existe.")
    elif auto["disponible"] == False:
        print("Ese vehículo ya está alquilado.")
    else:
        dias = int(input("¿Cuántos días? "))

        # Descuento según los días
        if dias >= 7:
            descuento = 0.15
        elif dias >= 3:
            descuento = 0.05
        else:
            descuento = 0

        total = auto["precio_dia"] * dias * (1 - descuento)

        alquiler = {
            "cliente": clientes[cedula]["nombre"],
            "placa": placa,
            "dias": dias,
            "total": total,
            "activo": True,
        }
        alquileres.append(alquiler)
        auto["disponible"] = False

        print(f"Alquiler realizado. Descuento: {int(descuento * 100)}%")
        print(f"Total a pagar: ${total:,.0f}")


def devolver():
    print("\n--- DEVOLVER VEHÍCULO ---")
    placa = input("Placa del vehículo a devolver: ").upper()

    encontrado = False
    for a in alquileres:
        if a["placa"] == placa and a["activo"]:
            a["activo"] = False
            encontrado = True

    if encontrado:
        for v in vehiculos:
            if v["placa"] == placa:
                v["disponible"] = True
        print("Vehículo devuelto. Ya está disponible otra vez.")
    else:
        print("No hay un alquiler activo con esa placa.")


def ver_alquileres():
    print("\n--- ALQUILERES ---")
    if len(alquileres) == 0:
        print("Todavía no hay alquileres.")
    else:
        for a in alquileres:
            if a["activo"]:
                estado = "Activo"
            else:
                estado = "Finalizado"
            print(f"{a['cliente']} | {a['placa']} | {a['dias']} días | ${a['total']:,.0f} | {estado}")

        # Suma de lo ganado
        ganancias = 0
        for a in alquileres:
            ganancias = ganancias + a["total"]
        print(f"\nTotal ganado: ${ganancias:,.0f}")


# ----------------------------------------------------------------------
# MENÚ PRINCIPAL
# ----------------------------------------------------------------------

opcion = ""
while opcion != "6":
    print("\n===== RENTA DE AUTOS =====")
    print("1. Ver vehículos")
    print("2. Registrar cliente")
    print("3. Alquilar vehículo")
    print("4. Devolver vehículo")
    print("5. Ver alquileres")
    print("6. Salir")

    opcion = input("Elige una opción: ")

    if opcion == "1":
        mostrar_vehiculos()
    elif opcion == "2":
        registrar_cliente()
    elif opcion == "3":
        alquilar()
    elif opcion == "4":
        devolver()
    elif opcion == "5":
        ver_alquileres()
    elif opcion == "6":
        print("Hasta pronto.")
    else:
        print("Opción no válida.")
