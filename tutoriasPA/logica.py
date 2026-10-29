"""Lógica del sistema de tutorías (CRUD).

Cada profesor tiene horarios fijos que se repiten cada semana. Los estudiantes
se apuntan a una fecha concreta de ese horario (sin cupo máximo) y dejan una
nota con el tema que necesitan ver.
"""
import json
import os
import unicodedata
from datetime import datetime, timedelta

RUTA_DATOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datos.json")

DIAS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
         "agosto", "septiembre", "octubre", "noviembre", "diciembre"]

DIAS_PARA_CANCELAR = 3   # solo se cancela con 3 días o más de anticipación
VENTANA_DIAS = 7         # el estudiante ve y se apunta a los próximos 7 días
MAX_NOTA = 200
MAX_LUGAR = 40


# ---------------------------------------------------------------- utilidades

def ahora():
    """Fecha y hora actual (aparte para poder simularla al probar)."""
    return datetime.now()


def cargar_datos():
    with open(RUTA_DATOS, encoding="utf-8") as archivo:
        return json.load(archivo)


def guardar_datos(datos):
    with open(RUTA_DATOS, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=2)


def _dt(fecha, hora):
    """('2026-11-03', '10:00') -> datetime."""
    return datetime.strptime(f"{fecha} {hora}", "%Y-%m-%d %H:%M")


def describir(dt):
    """datetime -> 'martes 3 de noviembre, 10:00'."""
    return f"{DIAS[dt.weekday()].lower()} {dt.day} de {MESES[dt.month - 1]}, {dt:%H:%M}"


def _orden_horario(horario):
    return (DIAS.index(horario["dia"]), horario["hora"])


def _texto_horarios(horarios):
    ordenados = sorted(horarios, key=_orden_horario)
    return ", ".join(f"{h['dia']} {h['hora']}" for h in ordenados)


def _buscar_horario(info, horario_id):
    for horario in info["horarios"]:
        if horario["id"] == horario_id:
            return horario
    return None


def _siguiente_id(inscripciones):
    return max((i["id"] for i in inscripciones), default=0) + 1


def _siguiente_id_horario(datos):
    numeros = [int(h["id"][1:]) for info in datos["profesores"].values() for h in info["horarios"]]
    return "h" + str(max(numeros, default=0) + 1)


def _inscripcion_de(datos, inscripcion_id, estudiante):
    for i in datos["inscripciones"]:
        if i["id"] == inscripcion_id and i["estudiante"] == estudiante:
            return i
    return None


def _futuras(datos, profesor, horario_id):
    """Inscripciones que todavía no han ocurrido para un horario fijo."""
    return [i for i in datos["inscripciones"]
            if i["profesor"] == profesor and i["horario"] == horario_id
            and _dt(i["fecha"], i["hora"]) > ahora()]


def _sesiones(datos, profesor, estudiante=None, dias=VENTANA_DIAS):
    """Fechas concretas de los horarios fijos de un profesor en los próximos días."""
    info = datos["profesores"].get(profesor)
    if info is None:
        return []
    hoy = ahora().date()
    sesiones = []
    for horario in info["horarios"]:
        for d in range(dias):
            fecha = hoy + timedelta(days=d)
            if DIAS[fecha.weekday()] != horario["dia"]:
                continue
            clave = fecha.isoformat()
            dt = _dt(clave, horario["hora"])
            if dt <= ahora():
                continue
            inscritos = [i for i in datos["inscripciones"]
                         if i["profesor"] == profesor and i["horario"] == horario["id"]
                         and i["fecha"] == clave]
            mia = next((i["id"] for i in inscritos if i["estudiante"] == estudiante), None)
            sesiones.append({
                "horario": horario["id"],
                "fecha": clave,
                "dt": dt,
                "hora": horario["hora"],
                "lugar": horario["lugar"],
                "inscritos": len(inscritos),
                "mia": mia,
            })
    sesiones.sort(key=lambda s: s["dt"])
    return sesiones


# ------------------------------------------------- READ (estudiante / público)

def estudiantes():
    return cargar_datos()["estudiantes"]


def materias():
    datos = cargar_datos()
    unicas = {p["materia"] for p in datos["profesores"].values()}
    return sorted(unicas, key=lambda m: unicodedata.normalize("NFD", m))


def obtener_profesor(profesor):
    """{'id', 'nombre', 'materia', 'horarios_texto'} o None si no existe."""
    info = cargar_datos()["profesores"].get(profesor)
    if info is None:
        return None
    return {"id": profesor, "nombre": info["nombre"], "materia": info["materia"],
            "horarios_texto": _texto_horarios(info["horarios"]) or "Sin horarios"}


def listar_profesores(materia=None):
    datos = cargar_datos()
    resultado = []
    for pid, info in datos["profesores"].items():
        if materia and info["materia"] != materia:
            continue
        resultado.append({"id": pid, "nombre": info["nombre"], "materia": info["materia"],
                          "horarios_texto": _texto_horarios(info["horarios"]) or "Sin horarios"})
    resultado.sort(key=lambda p: (p["materia"], p["nombre"]))
    return resultado


def proximas_tutorias(profesor, estudiante=None):
    """Tutorías de un profesor en los próximos 7 días, con cuántos se han apuntado."""
    return _sesiones(cargar_datos(), profesor, estudiante)


def proximas_global(limite=5):
    """Las próximas tutorías de todos los profesores, ordenadas por fecha."""
    datos = cargar_datos()
    todas = []
    for pid, info in datos["profesores"].items():
        for sesion in _sesiones(datos, pid):
            todas.append({**sesion, "profesor_id": pid,
                          "profesor": info["nombre"], "materia": info["materia"]})
    todas.sort(key=lambda s: s["dt"])
    return todas[:limite]


def mis_tutorias(estudiante):
    """Próximas tutorías a las que se apuntó el estudiante, ordenadas por fecha."""
    datos = cargar_datos()
    tutorias = []
    for i in datos["inscripciones"]:
        if i["estudiante"] != estudiante:
            continue
        dt = _dt(i["fecha"], i["hora"])
        if dt <= ahora():
            continue
        info = datos["profesores"].get(i["profesor"])
        horario = _buscar_horario(info, i["horario"]) if info else None
        tutorias.append({
            "id": i["id"],
            "profesor_id": i["profesor"],
            "profesor": info["nombre"] if info else "Profesor",
            "materia": info["materia"] if info else "",
            "fecha": i["fecha"],
            "dt": dt,
            "hora": i["hora"],
            "lugar": horario["lugar"] if horario else "",
            "nota": i["nota"],
            "cancelable": dt - ahora() >= timedelta(days=DIAS_PARA_CANCELAR),
        })
    tutorias.sort(key=lambda t: t["dt"])
    return tutorias


# --------------------------------------------- CREATE / UPDATE / DELETE (estudiante)

def apuntarse(estudiante, profesor, horario, fecha, nota=""):
    """CREATE: apunta al estudiante a la tutoría de un profesor en una fecha."""
    datos = cargar_datos()
    if estudiante not in datos["estudiantes"]:
        return False, "Estudiante no registrado."
    info = datos["profesores"].get(profesor)
    if info is None:
        return False, "Profesor no encontrado."
    h = _buscar_horario(info, horario)
    if h is None:
        return False, "Ese horario no existe."
    try:
        dt = _dt(fecha, h["hora"])
    except ValueError:
        return False, "La fecha no es válida."
    if DIAS[dt.weekday()] != h["dia"]:
        return False, f"Esa tutoría es el {h['dia'].lower()}."
    if dt <= ahora():
        return False, "Esa tutoría ya pasó."
    if dt.date() > ahora().date() + timedelta(days=VENTANA_DIAS - 1):
        return False, f"Solo puedes apuntarte a las tutorías de los próximos {VENTANA_DIAS} días."
    nota = (nota or "").strip()
    if len(nota) > MAX_NOTA:
        return False, f"La nota no puede pasar de {MAX_NOTA} caracteres."

    for i in datos["inscripciones"]:
        if i["estudiante"] != estudiante or i["fecha"] != fecha:
            continue
        if i["profesor"] == profesor and i["horario"] == horario:
            return False, "Ya te apuntaste a esa tutoría."
        if i["hora"] == h["hora"]:
            otro = datos["profesores"][i["profesor"]]["nombre"]
            return False, f"Ya tienes otra tutoría a esa hora con {otro}."

    datos["inscripciones"].append({
        "id": _siguiente_id(datos["inscripciones"]),
        "estudiante": estudiante,
        "profesor": profesor,
        "horario": horario,
        "fecha": fecha,
        "hora": h["hora"],
        "nota": nota,
    })
    guardar_datos(datos)
    return True, f"Quedó registrada tu asistencia a la tutoría de {info['nombre']}, {describir(dt)}."


def editar_nota(estudiante, inscripcion, nota):
    """UPDATE: cambia la nota de una tutoría propia que aún no ha pasado."""
    datos = cargar_datos()
    i = _inscripcion_de(datos, inscripcion, estudiante)
    if i is None:
        return False, "No encontré esa tutoría entre las tuyas."
    if _dt(i["fecha"], i["hora"]) <= ahora():
        return False, "Esa tutoría ya pasó."
    nota = (nota or "").strip()
    if len(nota) > MAX_NOTA:
        return False, f"La nota no puede pasar de {MAX_NOTA} caracteres."
    i["nota"] = nota
    guardar_datos(datos)
    return True, "Nota actualizada."


def cancelar(estudiante, inscripcion):
    """DELETE: cancela una tutoría propia, solo con 3 días o más de anticipación."""
    datos = cargar_datos()
    i = _inscripcion_de(datos, inscripcion, estudiante)
    if i is None:
        return False, "No encontré esa tutoría entre las tuyas."
    dt = _dt(i["fecha"], i["hora"])
    if dt <= ahora():
        return False, "Esa tutoría ya pasó."
    if dt - ahora() < timedelta(days=DIAS_PARA_CANCELAR):
        return False, (f"Solo se puede cancelar con {DIAS_PARA_CANCELAR} días de "
                       "anticipación. Escríbele al profesor.")
    datos["inscripciones"].remove(i)
    guardar_datos(datos)
    return True, "Tutoría cancelada."


# ------------------------------------------------------------- panel profesor

def horarios_de(profesor):
    """READ: horarios fijos del profesor, con cuántos se han apuntado a próximas fechas."""
    datos = cargar_datos()
    info = datos["profesores"].get(profesor)
    if info is None:
        return []
    horarios = []
    for h in sorted(info["horarios"], key=_orden_horario):
        horarios.append({**h, "proximos": len(_futuras(datos, profesor, h["id"]))})
    return horarios


def ver_inscritos(profesor):
    """READ: quién se apuntó a las próximas tutorías, agrupado por fecha y hora."""
    datos = cargar_datos()
    info = datos["profesores"].get(profesor)
    if info is None:
        return []
    grupos = {}
    for i in datos["inscripciones"]:
        if i["profesor"] != profesor:
            continue
        dt = _dt(i["fecha"], i["hora"])
        if dt <= ahora():
            continue
        horario = _buscar_horario(info, i["horario"])
        grupo = grupos.setdefault((i["fecha"], i["horario"]), {
            "dt": dt,
            "hora": i["hora"],
            "lugar": horario["lugar"] if horario else "",
            "estudiantes": [],
        })
        grupo["estudiantes"].append({"nombre": i["estudiante"], "nota": i["nota"]})
    return sorted(grupos.values(), key=lambda g: g["dt"])


def _validar_horario(dia, hora, lugar):
    """Devuelve ((dia, hora, lugar), '') si todo está bien, o (None, mensaje)."""
    if dia not in DIAS:
        return None, "Elige un día válido."
    try:
        hora = datetime.strptime((hora or "").strip(), "%H:%M").strftime("%H:%M")
    except ValueError:
        return None, "La hora debe tener formato HH:MM, por ejemplo 10:00."
    lugar = (lugar or "").strip()
    if not lugar:
        return None, "Escribe el lugar de la tutoría."
    if len(lugar) > MAX_LUGAR:
        return None, f"El lugar no puede pasar de {MAX_LUGAR} caracteres."
    return (dia, hora, lugar), ""


def crear_horario(profesor, dia, hora, lugar):
    """CREATE: agrega un horario fijo semanal al profesor."""
    datos = cargar_datos()
    info = datos["profesores"].get(profesor)
    if info is None:
        return False, "Profesor no encontrado."
    valores, error = _validar_horario(dia, hora, lugar)
    if valores is None:
        return False, error
    dia, hora, lugar = valores
    if any(h["dia"] == dia and h["hora"] == hora for h in info["horarios"]):
        return False, "Ya tienes un horario ese día a esa hora."
    info["horarios"].append({"id": _siguiente_id_horario(datos), "dia": dia,
                             "hora": hora, "lugar": lugar})
    guardar_datos(datos)
    return True, f"Horario agregado: {dia} {hora}."


def editar_horario(profesor, horario, dia, hora, lugar):
    """UPDATE: cambia día, hora o lugar. Si ya hay estudiantes apuntados, solo el lugar."""
    datos = cargar_datos()
    info = datos["profesores"].get(profesor)
    if info is None:
        return False, "Profesor no encontrado."
    h = _buscar_horario(info, horario)
    if h is None:
        return False, "Ese horario no existe."
    valores, error = _validar_horario(dia, hora, lugar)
    if valores is None:
        return False, error
    dia, hora, lugar = valores
    if any(o["id"] != horario and o["dia"] == dia and o["hora"] == hora for o in info["horarios"]):
        return False, "Ya tienes otro horario ese día a esa hora."
    cambia_fecha = (dia, hora) != (h["dia"], h["hora"])
    if cambia_fecha and _futuras(datos, profesor, horario):
        return False, "Hay estudiantes apuntados. Por ahora solo puedes cambiar el lugar."
    h["dia"], h["hora"], h["lugar"] = dia, hora, lugar
    guardar_datos(datos)
    return True, "Horario actualizado."


def eliminar_horario(profesor, horario):
    """DELETE: elimina un horario fijo si nadie está apuntado a próximas fechas."""
    datos = cargar_datos()
    info = datos["profesores"].get(profesor)
    if info is None:
        return False, "Profesor no encontrado."
    h = _buscar_horario(info, horario)
    if h is None:
        return False, "Ese horario no existe."
    if _futuras(datos, profesor, horario):
        return False, "No puedes eliminarlo: hay estudiantes apuntados a próximas tutorías."
    info["horarios"].remove(h)
    guardar_datos(datos)
    return True, "Horario eliminado."
