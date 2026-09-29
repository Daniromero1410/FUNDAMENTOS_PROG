#primer ejercicio
numero=1
while numero <= 10:
    print(numero)
    numero += 1


#segundo ejercicio
numero=int(input("ingresar un numero: "))
i = 1
while i <= 10:
    print(f"{numero} x {i} = {numero * i}")
    i += 1

#tercer ejercicio
for numero in range(1, 11):
    print(f" el cuadrado de {numero} es {numero ** 2}")


#cuarto ejercicio
nota=[0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
contador=0
for n in nota:
    if n >= 3.0:
        contador += 1  
print(f"notas mayores o iguales a 3.0 es: {contador}")


#quinto ejercicio
palabra = input("ingresar una palabra: ")
vocales = "aeiou" 
contador = 0
for letra in palabra:
    if letra in vocales:
        contador += 1
print(f"la palabra tiene: {contador} vocales")

