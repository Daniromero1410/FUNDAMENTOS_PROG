# EJERCICIO #1
num = 1
while num <= 10:
    print(num)
    num = num + 1

# EJERCICIO #2
n = int(input("Ingresa número a saber su tabla: "))
i = 1
while i <=10:
    
    resultado = n * i
    print(resultado)
    i = i + 1

# EJERCICIO #3

for numero in range(1,11):
    cuadrado = numero **2
    print(f"el cuadrado de {numero} es: {cuadrado}")

# EJERCICIO #4
list = [4.5, 5, 3.8, 2.5, 3,]
contador = 0
for i in list:
    if i >= 3:
        contador = contador + 1
print(f"Los cantidad de notas mayores o iguales a 3 son: {contador}")

# EJERCICIO #5
palabra = input("Ingresa una palabra: ")
contador2 = 0
for letra in palabra:
    if letra in "aeiou":
        contador2 = contador2 + 1
print (contador2)
