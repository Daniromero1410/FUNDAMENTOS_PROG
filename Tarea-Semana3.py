#De minutos a horas y minutos
minutos = int(input("Ingresa el número de minutos: "))
horas = minutos // 60
minutos_restantes = minutos % 60
print(f"{minutos} minutos son {horas} horas y {minutos_restantes} minutos.")

#Año bisiesto
Año = int(input("Ingrese el año:"))
if Año %  4 == 0:
    print("El año", Año, "es bisiesto")
else:
    print("El año", Año, "no es bisiesto")

#Nota del estudiante
Nota = float(input("Ingresa la nota del estudiante: "))
if Nota < 3.0:
    print ("La nota es baja")
elif Nota >= 3.0 and Nota < 4.0:
    print ("La nota es media")
elif Nota >= 4.0:
    print ("La nota es alta")

#Número de personas mayores de edad
Personas = int(input("Ingrese la cantidad de personas:"))
mayores = 0
for i in range(Personas):
    edad = int(input("Ingrese la edad de la persona:"))
    if edad >= 18:
        mayores = mayores + 1

print("La cantidad de personas mayores de 18 años es:", mayores)