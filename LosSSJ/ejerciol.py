#ejercicio1:

numero=int(input("ingresar un numero entero: "))
if numero % 2 ==0:
    print("el numero {numero} es par")
else:
    print("el numero {numero} es impar")

#ejercicio2:
nota=float(input("ingresar la nota del estudiante: "))
if nota >= 3.0 :
    print(f"el estudiante aprobo con nota {nota}")
else:
    print(f"el estudiante reprobo con nota {nota}")


#ejercicio3:
base=float(input("ingresar la base del triangulo: "))
altura=float(input("ingresar la altura del triangulo: "))
area=(base*altura)/2
print(f"el area del triangulo es {area}")
lado1=float(input("ingresar el primer lado del triangulo: "))
lado2=float(input("ingresar el segundo lado del triangulo: "))
lado3=float(input("ingresar el tercer lado del triangulo: "))
perimetro=lado1+lado2+lado3
print(f"el perimetro del triangulo es {perimetro}")




#ejercicio4:
medicion=float(input("ingresar la medicion del sensor"))
if medicion>= 40:
   print("se considera anomalia")
else:
   print("es normal")  
     






