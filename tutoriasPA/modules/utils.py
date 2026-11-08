import json 
import os
from datetime import datetime

# ruta datos
RUTA_STORAGE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "storage") 

DIAS_PARA_CANCELAR = 3
VENTANA_DIAS = 7

# maximo caracteres
MAX_NOTA = 200 # descripcion de la nota
MAX_LUGAR = 40 # nombre del salon

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

# Recibe la hora y fecha en formato de texto y devuelve un objeto datetime
def construir_fecha_hora(fecha_texto, hora_texto):
    return datetime.fromisoformat(fecha_texto + " " + hora_texto) # "2026-11-10" y "10:00"

# Devuelve el horario del profesor con el id dado
def buscar_horario(profesor, horario_id):
    for horario in profesor["horarios"]:
        if horario["id"] == horario_id:
            return horario
    return None
