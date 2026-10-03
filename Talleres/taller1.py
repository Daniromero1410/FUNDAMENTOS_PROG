
# Ejercicio 1: Convertir minutos a horas y minutos
time = int(input("Ingrese los minutos: "))

horas = time // 60
minutos = time % 60

print(horas, "horas y", minutos, "minutos")

# Ejercicio 2: Determinar si un año es bisiesto
year= int(input("Ingrese el año: "))

if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
    print(year, "es un año bisiesto")
else:
    print(year, "no es un año bisiesto")

# Ejercicio 3: Clasificar una nota
note= float(input("Ingrese la nota: "))

if note >= 4.0:
    print("Alta")

elif note >= 3.0 and note < 3.9:
    print("Media")

else:
    print("Baja")

# Ejercicio 4: Contar cuántas personas son mayores de edad
edades = [23, 12, 48, 15, 11, 10]

count = 0
for edad in edades:
    if edad >= 18:
        count += 1

print("Número de personas mayores de edad:", count)
