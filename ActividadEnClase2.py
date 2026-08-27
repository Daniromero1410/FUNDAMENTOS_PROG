#ejercicio 1
N=int(input("ingrese un numero:")) 
if N<0:
    print("Aviso")
#ejercicio 2
N1=int(input("ingrese un numero:"))
N2=int(input("ingrese otro numero:"))
if N1>N2:
    print(f"{N1} es mayor")
else:
    print(f"{N2} es mayor")
#ejercicio 3
temp=float(input("ingrese la temperatura:"))
if temp<15:
    print("Frio")
elif temp>=15 and temp<=25:
    print("Templado")
else:
    print("Caliente")
#ejercicio 4
Nota=float(input("ingrese la nota:"))
Asistencia=float(input("ingrese la asistencia:"))
if Nota>=3 and Asistencia>=8:
    print("Aprobado")
else:
    print("Reprobado")  
#ejercicio 5
Num=int(input("ingrese un numero:"))
if Num%3==0:
    print("Es divisible de 3")
else:
    print("No")
    