# Prueba general del backend. No toca tus datos: trabaja sobre una copia temporal
# y simula que hoy es domingo 8 de noviembre de 2026, 09:00.
# Ids de los datos de ejemplo: estudiantes Ana=1, Luis=2, Camila=3; profesores 1 a 5; horarios 1 a 10.
import os
import shutil
import tempfile
from datetime import datetime

import modules.utils as utils
import modules.estudiantes as estudiante
import modules.profesores as profesor

carpeta_temporal = tempfile.mkdtemp()
for nombre in ["estudiantes", "profesores", "horarios", "inscripciones"]:
    shutil.copy(os.path.join(utils.RUTA_STORAGE, nombre + ".json"), carpeta_temporal)
utils.RUTA_STORAGE = carpeta_temporal


def reloj_falso():
    return datetime(2026, 11, 8, 9, 0)


utils.fecha_hora_actual = reloj_falso

total = 0
fallos = 0


def revisar(descripcion, obtenido, esperado):
    global total, fallos
    total = total + 1
    if obtenido == esperado:
        print("OK     " + descripcion)
    else:
        fallos = fallos + 1
        print("FALLÓ  " + descripcion)
        print("       esperado: " + str(esperado))
        print("       obtenido: " + str(obtenido))


# --- Estudiante: consultas ---
revisar("listar_profesores devuelve 5", len(estudiante.listar_profesores()), 5)
revisar("proximas_global devuelve 10", len(estudiante.proximas_global()), 10)
fechas_p1 = []
for tutoria in estudiante.proximas_tutorias(1):
    fechas_p1.append(tutoria["fecha"])
revisar("proximas_tutorias del profesor 1", fechas_p1, ["2026-11-10", "2026-11-12"])
revisar("proximas_tutorias de profesor inexistente", estudiante.proximas_tutorias(99), [])
revisar("Ana tiene 2 tutorías", len(estudiante.mis_tutorias(1)), 2)

# --- Estudiante: nota ---
revisar("nota vacía", estudiante.revisar_nota("   ")[0], False)
revisar("nota con espacios se limpia", estudiante.revisar_nota("  Hola  "), (True, "Hola"))
revisar("nota muy larga", estudiante.revisar_nota("a" * 201)[0], False)
revisar("editar nota ajena", estudiante.editar_nota(1, 2, "Hola")[0], False)
revisar("editar nota propia", estudiante.editar_nota(1, 1, "  Integrales  ")[0], True)
revisar("la nota quedó guardada y limpia", estudiante.mis_tutorias(1)[0]["nota"], "Integrales")

# --- Estudiante: apuntarse ---
revisar("apuntarse duplicado", estudiante.apuntarse(1, 1, "2026-11-10", "x")[0], False)
revisar("apuntarse fuera de ventana", estudiante.apuntarse(1, 1, "2026-11-17", "x")[0], False)
revisar("apuntarse a horario inexistente", estudiante.apuntarse(1, 99, "2026-11-10", "x")[0], False)
revisar("apuntarse con nota vacía", estudiante.apuntarse(1, 2, "2026-11-12", " ")[0], False)
revisar("apuntarse bien", estudiante.apuntarse(1, 2, "2026-11-12", "  Límites  ")[0], True)
revisar("Ana ahora tiene 3", len(estudiante.mis_tutorias(1)), 3)
revisar("la nota se guardó limpia", estudiante.mis_tutorias(1)[-1]["nota"], "Límites")
# Luis ya tiene el horario 1 (martes 10:00); el horario 5 también es martes 10:00 -> choque de hora
revisar("choque de hora el mismo día", estudiante.apuntarse(2, 5, "2026-11-10", "x")[0], False)
# id nuevo = mayor + 1, aunque se cancele uno del medio
estudiante.cancelar(5, 1)
estudiante.apuntarse(2, 3, "2026-11-09", "Hola")
ids = []
for inscripcion in utils.cargar_datos("inscripciones"):
    ids.append(inscripcion["id"])
revisar("ids no se repiten", len(ids), len(set(ids)))

# --- Estudiante: cancelar ---
revisar("cancelar ajena", estudiante.cancelar(2, 1)[0], False)
revisar("cancelar con menos de 3 días", estudiante.cancelar(1, 1)[0], False)
revisar("cancelar inexistente", estudiante.cancelar(99, 1)[0], False)
revisar("cancelar con 5 días", estudiante.cancelar(4, 3)[0], True)

# --- Profesor ---
revisar("horarios del profesor 1", len(profesor.horarios_de_profesor(1)), 2)
revisar("ver_inscritos del profesor 1", len(profesor.ver_inscritos(1)), 3)
revisar("crear: día inválido", profesor.crear_horario(1, "Sabado", "10:00", "x")[0], False)
revisar("crear: hora 25:00", profesor.crear_horario(1, "Sábado", "25:00", "x")[0], False)
revisar("crear: hora 10-00", profesor.crear_horario(1, "Sábado", "10-00", "x")[0], False)
revisar("crear: lugar vacío", profesor.crear_horario(1, "Sábado", "10:00", "  ")[0], False)
revisar("crear: lugar largo", profesor.crear_horario(1, "Sábado", "10:00", "a" * 41)[0], False)
revisar("crear: profesor inexistente", profesor.crear_horario(99, "Sábado", "10:00", "x")[0], False)
revisar("crear: choque", profesor.crear_horario(1, "Martes", "10:00", "x")[0], False)
revisar("crear bien", profesor.crear_horario(1, "Sábado", "09:30", " Sala 1 ")[0], True)
revisar("el horario nuevo tiene id 11", profesor.horarios_de_profesor(1)[-1]["id"], 11)
revisar("el lugar se guardó limpio", profesor.horarios_de_profesor(1)[-1]["lugar"], "Sala 1")
revisar("editar solo lugar con inscritos", profesor.editar_horario(1, 1, "Martes", "10:00", "Sala nueva")[0], True)
revisar("editar hora con inscritos", profesor.editar_horario(1, 1, "Martes", "11:00", "x")[0], False)
revisar("eliminar con inscritos", profesor.eliminar_horario(1, 1)[0], False)
revisar("editar horario de otro profesor", profesor.editar_horario(1, 3, "Viernes", "08:00", "x")[0], False)
revisar("eliminar horario de otro profesor", profesor.eliminar_horario(1, 3)[0], False)
revisar("editar horario 11 (sin inscritos)", profesor.editar_horario(1, 11, "Viernes", "08:00", "Sala 2")[0], True)
revisar("eliminar horario 11", profesor.eliminar_horario(1, 11)[0], True)

# hay_inscritos debe ignorar las inscripciones que ya pasaron, y eliminar borra esas inscripciones viejas
inscripciones = utils.cargar_datos("inscripciones")
inscripciones.append({"id": 50, "estudiante_id": 1, "horario_id": 9, "fecha": "2026-11-02", "nota": "vieja"})
utils.guardar_datos("inscripciones", inscripciones)
revisar("eliminar horario con inscripción ya pasada", profesor.eliminar_horario(5, 9)[0], True)
quedan = []
for inscripcion in utils.cargar_datos("inscripciones"):
    quedan.append(inscripcion["id"])
revisar("su inscripción vieja se borró en cascada", 50 in quedan, False)

print()
print(str(total - fallos) + " de " + str(total) + " pruebas bien.")
shutil.rmtree(carpeta_temporal)
