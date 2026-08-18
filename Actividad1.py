#PUNTO 1
num = int(input("Ingrese un numero: "))
if num%2==0:
    print("Es par") 
else:
    print("Es impar")


#PUNTO 2
nota=float(input("Ingrese la nota: "))
if nota>=3.0:
    print("Aprobo")
else:
    print("Reprobo")


#PUNTO 3
base = float(input("Ingrese la base del triangulo: "))
altura = float(input("Ingrese la altura del triangulo: "))
area = (base * altura) / 2
perimetro = 2*(base + altura)
print(f"El area del triangulo es: {area} y el perimetro es: {perimetro}")


#PUNTO 4
medicion = int(input("Ingrese la medicion: "))
if medicion >= 40:
    print("Es ANOMALIA")
else:
    print("Es NORMAL")
