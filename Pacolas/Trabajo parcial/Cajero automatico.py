PIN_CORRECTO = "1234"
saldo = 100000
intentos = 3

print("=== CAJERO AUTOMATICO ===")

while intentos > 0:
	pin = input("Ingrese su PIN: ")

	if pin == PIN_CORRECTO:
		print("\nAcceso permitido.")
		break

	intentos -= 1
	print(f"PIN incorrecto. Intentos restantes: {intentos}")
else:
	print("Tarjeta bloqueada por exceso de intentos.")
	raise SystemExit

while True:
	print("\n--- MENU PRINCIPAL ---")
	print("1. Consultar saldo")
	print("2. Retirar dinero")
	print("3. Depositar dinero")
	print("4. Salir")

	opcion = input("Seleccione una opcion: ")

	if opcion == "1":
		print(f"Su saldo actual es: ${saldo:,.0f}")
	elif opcion == "2":
		try:
			retiro = int(input("Ingrese el valor a retirar: "))
			if retiro <= 0:
				print("El valor debe ser mayor que cero.")
			elif retiro > saldo:
				print("Saldo insuficiente.")
			else:
				saldo -= retiro
				print(f"Retiro exitoso. Su nuevo saldo es: ${saldo:,.0f}")
		except ValueError:
			print("Ingrese un valor numerico valido.")
	elif opcion == "3":
		try:
			deposito = int(input("Ingrese el valor a depositar: "))
			if deposito <= 0:
				print("El valor debe ser mayor que cero.")
			else:
				saldo += deposito
				print(f"Deposito exitoso. Su nuevo saldo es: ${saldo:,.0f}")
		except ValueError:
			print("Ingrese un valor numerico valido.")
	elif opcion == "4":
		print("Gracias por usar el cajero automatico.")
		break
	else:
		print("Opcion no valida.")
