# Prueba general del backend. No toca tus datos: trabaja sobre una copia temporal
# y simula que hoy es domingo 8 de noviembre de 2026, 09:00.
import os
import shutil
import tempfile
from datetime import datetime

import modules.utils as utils
import modules.estudiantes as estudiante
import modules.profesores as profesor

carpeta_temporal = tempfile.mkdtemp()
for nombre in ["estudiantes", "profesores", "inscripciones"]:
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
fechas_gomez = []
for tutoria in estudiante.proximas_tutorias("gomez"):
    fechas_gomez.append(tutoria["fecha"])
revisar("proximas_tutorias de Gómez", fechas_gomez, ["2026-11-10", "2026-11-12"])
revisar("proximas_tutorias de profesor inexistente", estudiante.proximas_tutorias("xx"), [])
revisar("Ana tiene 2 tutorías", len(estudiante.mis_tutorias("Ana")), 2)

# --- Estudiante: nota ---
revisar("nota vacía", estudiante.revisar_nota("   "), (False, "La nota no puede estar vacía."))
revisar("nota con espacios se limpia", estudiante.revisar_nota("  Hola  "), (True, "Hola"))
revisar("nota muy larga", estudiante.revisar_nota("a" * 201)[0], False)
revisar("editar nota ajena", estudiante.editar_nota(1, "Luis", "Hola")[0], False)
revisar("editar nota propia", estudiante.editar_nota(1, "Ana", "  Integrales  ")[0], True)
revisar("la nota quedó guardada", estudiante.mis_tutorias("Ana")[0]["nota"], "Integrales")

# --- Estudiante: apuntarse ---
revisar("apuntarse duplicado", estudiante.apuntarse("Ana", "gomez", "h1", "2026-11-10", "x")[0], False)
revisar("apuntarse fuera de ventana", estudiante.apuntarse("Ana", "gomez", "h1", "2026-11-17", "x")[0], False)
revisar("apuntarse a profesor inexistente", estudiante.apuntarse("Ana", "xx", "h1", "2026-11-10", "x")[0], False)
revisar("apuntarse a horario inexistente", estudiante.apuntarse("Ana", "gomez", "h9", "2026-11-10", "x")[0], False)
revisar("apuntarse con nota vacía", estudiante.apuntarse("Ana", "gomez", "h2", "2026-11-12", " ")[0], False)
revisar("apuntarse bien", estudiante.apuntarse("Ana", "gomez", "h2", "2026-11-12", "Límites")[0], True)
revisar("Ana ahora tiene 3", len(estudiante.mis_tutorias("Ana")), 3)
# Luis ya tiene Gómez martes 10:00; Ruiz también es martes 10:00 -> choque de hora
revisar("choque de hora el mismo día", estudiante.apuntarse("Luis", "ruiz", "h5", "2026-11-10", "x")[0], False)
# id nuevo = mayor + 1, aunque se cancele uno del medio
estudiante.cancelar(5, "Ana")
estudiante.apuntarse("Luis", "paredes", "h3", "2026-11-09", "Hola")
ids = []
for inscripcion in utils.cargar_datos("inscripciones"):
    ids.append(inscripcion["id"])
revisar("ids no se repiten", len(ids), len(set(ids)))

# --- Estudiante: cancelar ---
revisar("cancelar ajena", estudiante.cancelar(2, "Ana")[0], False)
revisar("cancelar con menos de 3 días", estudiante.cancelar(1, "Ana")[0], False)
revisar("cancelar inexistente", estudiante.cancelar(99, "Ana")[0], False)
revisar("cancelar con 4 días", estudiante.cancelar(4, "Camila")[0], True)

# --- Profesor ---
revisar("horarios_de Gómez", len(profesor.horarios_de_profesor("gomez")), 2)
revisar("ver_inscritos de Gómez", len(profesor.ver_inscritos("gomez")), 3)
revisar("crear: día inválido", profesor.crear_horario("gomez", "Sabado", "10:00", "x")[0], False)
revisar("crear: hora 25:00", profesor.crear_horario("gomez", "Sábado", "25:00", "x")[0], False)
revisar("crear: hora 10-00", profesor.crear_horario("gomez", "Sábado", "10-00", "x")[0], False)
revisar("crear: lugar vacío", profesor.crear_horario("gomez", "Sábado", "10:00", "  ")[0], False)
revisar("crear: lugar largo", profesor.crear_horario("gomez", "Sábado", "10:00", "a" * 41)[0], False)
revisar("crear: choque", profesor.crear_horario("gomez", "Martes", "10:00", "x")[0], False)
revisar("crear bien", profesor.crear_horario("gomez", "Sábado", "09:30", " Sala 1 ")[0], True)
revisar("id nuevo es h11", profesor.horarios_de_profesor("gomez")[-1]["id"], "h11")
revisar("editar solo lugar con inscritos", profesor.editar_horario("gomez", "h1", "Martes", "10:00", "Sala nueva")[0], True)
revisar("editar hora con inscritos", profesor.editar_horario("gomez", "h1", "Martes", "11:00", "x")[0], False)
revisar("eliminar con inscritos", profesor.eliminar_horario("gomez", "h1")[0], False)
revisar("editar horario de otro profesor", profesor.editar_horario("gomez", "h3", "Viernes", "08:00", "x")[0], False)
revisar("editar h11 (sin inscritos)", profesor.editar_horario("gomez", "h11", "Viernes", "08:00", "Sala 2")[0], True)
revisar("eliminar h11", profesor.eliminar_horario("gomez", "h11")[0], True)

# hay_inscritos debe ignorar inscripciones que ya pasaron
inscripciones = utils.cargar_datos("inscripciones")
inscripciones.append({"id": 50, "estudiante": "Ana", "profesor": "torres", "horario": "h9",
                      "fecha": "2026-11-02", "hora": "14:00", "nota": "vieja"})
utils.guardar_datos("inscripciones", inscripciones)
revisar("eliminar horario con inscripción ya pasada", profesor.eliminar_horario("torres", "h9")[0], True)

print()
print(str(total - fallos) + " de " + str(total) + " pruebas bien.")
shutil.rmtree(carpeta_temporal)
