import json
import os
from datetime import datetime

# Ruta de la carpeta storage (una carpeta arriba de modules)
RUTA_STORAGE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "storage")

DIAS_PARA_CANCELAR = 3
VENTANA_DIAS = 7

# Máximo de caracteres
MAX_NOTA = 200   # descripción de la nota
MAX_LUGAR = 40   # nombre del salón

DIAS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]


def cargar_datos(nombre):
    ruta = os.path.join(RUTA_STORAGE, nombre + ".json")
    with open(ruta, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def guardar_datos(nombre, datos):
    ruta = os.path.join(RUTA_STORAGE, nombre + ".json")
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=2, ensure_ascii=False)


def fecha_hora_actual():
    return datetime.now()


# Recibe la fecha y la hora en texto y devuelve un datetime
def construir_fecha_hora(fecha_texto, hora_texto):
    return datetime.fromisoformat(fecha_texto + " " + hora_texto)   # "2026-11-10" y "10:00"


# Devuelve la fila con ese id dentro de la lista (estudiantes, profesores, horarios...), o None
def buscar_por_id(lista, id_buscado):
    for fila in lista:
        if fila["id"] == id_buscado:
            return fila
    return None


# Devuelve el id para una fila nueva: el mayor que exista + 1
def nuevo_id(lista):
    id_nuevo = 1
    for fila in lista:
        if fila["id"] >= id_nuevo:
            id_nuevo = fila["id"] + 1
    return id_nuevo


# La inscripción guarda solo horario_id y fecha; la hora se busca en el horario
def fecha_hora_de_inscripcion(inscripcion, horarios):
    horario = buscar_por_id(horarios, inscripcion["horario_id"])
    return construir_fecha_hora(inscripcion["fecha"], horario["hora"])
