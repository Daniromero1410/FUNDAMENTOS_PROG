#PARCIAL 2DO CORTE - ANGEL RANGEL Y EDWIN OSORIO

capacidad = 10
placas = []   
tipos = []   

opcion = 0
while opcion != 4:
    print("\n===== PARQUEADERO =====")
    print("1. Ingresar vehículo")
    print("2. Retirar vehículo")
    print("3. Ver vehículos")
    print("4. Salir")
    opcion = int(input("Elige una opción: "))

    if opcion == 1:
        if len(placas) >= capacidad:
            print("Parqueadero lleno")
        else:
            placa = input("Placa: ").upper()
            if placa in placas:
                print("Esa placa ya está registrada")
            else:
            
                tipo = ""
                while tipo == "":
                    print("Tipo de vehículo: 1. Carro  2. Moto  3. Bicicleta")
                    t = input("Elige el tipo: ")
                    if t == "1":
                        tipo = "carro"
                    elif t == "2":
                        tipo = "moto"
                    elif t == "3":
                        tipo = "bicicleta"
                    else:
                        print("Tipo no válido, intenta de nuevo")

                placas.append(placa)
                tipos.append(tipo)
                print(f"Vehículo registrado: {placa} ({tipo})")

    elif opcion == 2:
        placa = input("Placa a retirar: ").upper()
        if placa in placas:
            posicion = placas.index(placa)   
            tipo = tipos[posicion]
            placas.pop(posicion)             
            tipos.pop(posicion)
            print(f"Vehículo retirado: {placa} ({tipo})")
        else:
            print("No se encontró la placa")

    elif opcion == 3:
        print("Vehículos dentro:")
        for i in range(len(placas)):
            print(f"- {placas[i]} | {tipos[i]}")

    elif opcion != 4:
        print("Opción no válida")

    ocupados = len(placas)
    libres = capacidad - ocupados
    print(f"Espacios ocupados: {ocupados} | Espacios libres: {libres}")
