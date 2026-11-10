capacidad = 10
vehiculos = []

opcion = 0
while opcion != 4:
    print("\n===== PARQUEADERO =====")
    print("1. Ingresar vehículo")
    print("2. Retirar vehículo")
    print("3. Ver vehículos")
    print("4. Salir")
    opcion = int(input("Elige una opción: "))

    if opcion == 1:
        if len(vehiculos) >= capacidad:
            print("Parqueadero lleno")
        else:
            placa = input("Placa: ").upper()
            if placa in vehiculos:
                print("Esa placa ya está registrada")
            else:
                vehiculos.append(placa)
                print("Vehículo registrado")

    elif opcion == 2:
        placa = input("Placa a retirar: ").upper()
        if placa in vehiculos:
            vehiculos.remove(placa)
            print("Vehículo retirado")
        else:
            print("No se encontró la placa")

    elif opcion == 3:
        print("Vehículos dentro:")
        for v in vehiculos:
            print("-", v)

    elif opcion != 4:
        print("Opción no válida")

    # Se muestra después de cada acción
    ocupados = len(vehiculos)
    libres = capacidad - ocupados
    print(f"Espacios ocupados: {ocupados} | Espacios libres: {libres}")