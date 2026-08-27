numero=int(input("ingresar un numero entero: "))
if numero<0:
    print(f"el numero {numero} es negativo")


numero1=int(input("ingresar primer numero entero: "))
numero2=int(input("ingresar segundo numero entero: "))
if numero1>numero2:
    print(f"el numero {numero1} es mayor que {numero2}")
elif numero2>numero1:
    print(f"el numero {numero2} es mayor que {numero1}")
else:
    print(f"el numero {numero1} es igual que {numero2}")



temperatura=int(input("ingresar la temperatura: "))
if temperatura<15:
    print(f"la temperatura {temperatura} es fria") 
elif temperatura>=15 and temperatura<=25:
    print(f"la temperatura {temperatura} es templada")    
elif temperatura>25:
    print(f"la temperatura {temperatura} es caliente")     




nota=float(input("ingresa tu nota (0-5.0): "))
asistencia=float(input("ingresa tu asistencia(0-5.0): "))
if nota>=3.0 and asistencia>=0.8:
    print("aprobado")
else:
    print("reprobado")




numero=int(input("ingresar un numero entero: "))
if numero%3==0:
    print(f"el numero {numero} es divisible entre 3")
else:
    print(f"el numero {numero} no es divisible entre 3")


