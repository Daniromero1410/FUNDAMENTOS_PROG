
# Ejercicio 8: Sensor de medición de anomalias
medicion = int(input("Ingrese la medición: "))

if medicion >= 40:
    print("El sensor detecto una ANOMALIA", medicion)
else:
    print("El sensor considera la medición normal", medicion)
