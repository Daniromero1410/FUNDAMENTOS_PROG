
# Ejercicio 4: Contar cuántas personas son mayores de edad
edades = [23, 12, 48, 15, 11, 10]

count = 0
for edad in edades:
    if edad >= 18:
        count += 1

print("Número de personas mayores de edad:", count)
