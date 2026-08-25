#ejercicio1:
minutos=int(input("ingresa los minutos: "))
horas=minutos//60
minutos_restantes=minutos%60
print(f"el tiempo es {horas} horas y {minutos_restantes} minutos")


#ejercicio2:
año=int(input("ingresar un año: "))
if año % 4 == 0 and (año % 100 != 0 or año % 400 == 0):
    print(f"el año {año} es bisiesto")
else:
    print(f"el año {año} no es bisiesto")



#ejercicio3:
nota=float(input("ingresar la nota del estudiante: "))
if nota >= 4.0:
    categoria="alta" 
if nota >= 3.0 and nota < 4.0:
    categoria="media"
if nota < 3.0:
    categoria="baja"
print(f"la nota del estudiante es {nota} y su categoria es {categoria}")


#ejercicio4:
numero_de_personas=int(input("ingresar la edad del personas: "))
contador=0
for i in range(1, numero_de_personas + 1):
    edad=int(input(f"ingresar la edad de la persona {i}: "))
    if edad >=18:
       contador += 1
print(f"el numero de personas mayores de edad es {contador}")

#pdf



 
 
