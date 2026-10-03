
# Ejercicio 5: Determinar si un número es par o impar
num = int(input("Ingrese un número: "))

if num % 2 == 0:
    print(f"El número {num} es par.")
else:
    print(f"El número {num} es impar.")

# Ejercicio 6: Determinar si un estudiante aprobo o no considerando nota definitiva
nota = int(input("Ingrese la nota: "))

if nota <= 3.0:
  print("Si aprobo")
else:
  print("No aprobo")

# Ejercicio 7: Calcular el área y el perímetro de un rectángulo
base = float(input("Ingrese la base de su rectángulo: "))
altura = float(input("Ingrese la altura de su rectángulo: "))

area = base * altura
perimetro = 2 * (base + altura)

print("El área del rectángulo es:", area)
print("El perímetro del rectángulo es:", perimetro)

# Ejercicio 8: Sensor de medición de anomalias
medicion = int(input("Ingrese la medición: "))

if medicion >= 40:
    print("El sensor detecto una ANOMALIA", medicion)
else:
    print("El sensor considera la medición normal", medicion)
