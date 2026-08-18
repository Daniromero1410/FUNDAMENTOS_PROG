ciudad = "Valledupar"
habitantes = 500000
temperatura = 32.2

UMBRAL_CALOR = 30.0
hace_calor = temperatura >= UMBRAL_CALOR

if hace_calor:
    print("Supera el umbral")
else:
    print("No supera el umbral")