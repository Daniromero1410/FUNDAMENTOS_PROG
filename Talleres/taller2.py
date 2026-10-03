# #Ejercicio 1
numero = float(input("Ingrese un número: "))

if numero < 0:
    print("AVISO: El número ingresado es negativo")

# #Ejercicio 2
numero1 = float(input("Ingrese el primer número: "))
numero2 = float(input("Ingrese el segundo número: "))

if numero1 > numero2:
    print(numero1)
else:
    print(numero2)

#Ejercicio 3
temperatura = float(input("Ingrese la temperatura en grados Celsius: "))
if temperatura > 25:
    print("Calor")
elif temperatura < 13:
    print("Frio")
else:
    print("Templado")

# #Ejercicio 4
nota = float(input("Ingrese la nota: "))
asistencia = float(input("Ingrese la asistencia: "))
if nota >= 3.0 and asistencia >= 0.8:
    print("Aprobado")
else:
    print("Reprobado")

# #Ejercicio 5
numero = float(input("Ingrese un número: "))
if numero % 3 == 0:
    print("El número es divisible por 3")
else:
    print("El número no es divisible por 3")
