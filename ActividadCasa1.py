#Actividad En Casa #1

#EJERCICIO 1
minutos = int(input("Introduce los minutos: "))

horas = minutos // 60
minutos_restantes = minutos % 60

print(f"{minutos} minutos son {horas} horas y {minutos_restantes} minutos.")

#EJERCICIO 2
año = int(input("Introduce el año: "))

if año % 4 == 0:
    print("Es bisiesto")
else:
    print("No es bisiesto")

#EJERCICIO 3
nota = float(input("Introduce la nota: "))

if nota >= 4:
    print("Nota Alta")
elif nota >= 3:
    print("Nota Media")
else:
    print("Nota Baja")

#EJERCICIO 4
N = int(input("Ingrese cantidad de personas: "))

mayores = 0

for i in range(1, N + 1):
    edad = int(input("Ingrese edad: "))

    if edad >= 18:
        mayores = mayores + 1

print("Mayores de edad:", mayores)
