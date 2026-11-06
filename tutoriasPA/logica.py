"""Lógica del sistema de tutorías.

Los profesores tienen horarios fijos cada semana y los estudiantes se apuntan
a una fecha concreta. Las acciones devuelven (ok, mensaje).
"""
import json
import os
import unicodedata
from datetime import datetime, timedelta

RUTA_DATOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datos.json")

DIAS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
         "agosto", "septiembre", "octubre", "noviembre", "diciembre"]

DIAS_PARA_CANCELAR = 3
VENTANA_DIAS = 7
MAX_NOTA = 200
MAX_LUGAR = 40


# ---------------------------------------------------------------- apoyo

def ahora():
    # aparte para poder simular la fecha al probar
    return datetime.now()


def cargar_datos():
    with open(RUTA_DATOS, encoding="utf-8") as archivo:
        return json.load(archivo)


def guardar_datos(datos):
    with open(RUTA_DATOS, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=2)


def juntar_fecha_y_hora(fecha, hora):
    """('2026-11-03', '10:00') -> datetime"""
    return datetime.strptime(fecha + " " + hora, "%Y-%m-%d %H:%M")


def describir(momento):
    """datetime -> 'martes 3 de noviembre, 10:00'"""
    dia = DIAS[momento.weekday()].lower()
    mes = MESES[momento.month - 1]
    return f"{dia} {momento.day} de {mes}, {momento:%H:%M}"


def clave_horario(horario):
    return (DIAS.index(horario["dia"]), horario["hora"])


def clave_fecha(elemento):
    return elemento["dt"]


def clave_profesor(profesor):
    return (profesor["materia"], profesor["nombre"])


def sin_tildes(texto):
    return unicodedata.normalize("NFD", texto)


def buscar_horario(profesor_info, horario_id):
    for horario in profesor_info["horarios"]:
        if horario["id"] == horario_id:
            return horario
    return None


def buscar_inscripcion(datos, inscripcion_id, estudiante):
    for inscripcion in datos["inscripciones"]:
        if inscripcion["id"] == inscripcion_id and inscripcion["estudiante"] == estudiante:
            return inscripcion
    return None


def inscripciones_futuras(datos, profesor, horario_id):
    futuras = []
    for inscripcion in datos["inscripciones"]:
        if inscripcion["profesor"] != profesor or inscripcion["horario"] != horario_id:
            continue
        momento = juntar_fecha_y_hora(inscripcion["fecha"], inscripcion["hora"])
        if momento > ahora():
            futuras.append(inscripcion)
    return futuras


def sesiones_de_profesor(datos, profesor, estudiante=None):
    """Fechas concretas de los horarios del profesor en los próximos 7 días."""
    profesor_info = datos["profesores"].get(profesor)
    if profesor_info is None:
        return []

    hoy = ahora().date()
    sesiones = []

    for horario in profesor_info["horarios"]:
        for dias_desde_hoy in range(VENTANA_DIAS):
            fecha = hoy + timedelta(days=dias_desde_hoy)
            if DIAS[fecha.weekday()] != horario["dia"]:
                continue

            fecha_texto = fecha.isoformat()
            momento = juntar_fecha_y_hora(fecha_texto, horario["hora"])
            if momento <= ahora():
                continue

            cantidad = 0
            mi_inscripcion = None
            for inscripcion in datos["inscripciones"]:
                es_esta_sesion = (inscripcion["profesor"] == profesor
                                  and inscripcion["horario"] == horario["id"]
                                  and inscripcion["fecha"] == fecha_texto)
                if es_esta_sesion:
                    cantidad = cantidad + 1
                    if inscripcion["estudiante"] == estudiante:
                        mi_inscripcion = inscripcion["id"]

            sesiones.append({
                "horario": horario["id"],
                "fecha": fecha_texto,
                "dt": momento,
                "hora": horario["hora"],
                "lugar": horario["lugar"],
                "inscritos": cantidad,
                "mia": mi_inscripcion,
            })

    sesiones.sort(key=clave_fecha)
    return sesiones


def revisar_nota(nota):
    """Devuelve (nota, error). Si no hay error, error es ''."""
    if nota is None:
        nota = ""
    nota = nota.strip()
    if len(nota) > MAX_NOTA:
        return nota, f"La nota no puede pasar de {MAX_NOTA} caracteres."
    return nota, ""


def revisar_horario(dia, hora, lugar):
    """Devuelve (error, hora, lugar). Si no hay error, error es ''."""
    if dia not in DIAS:
        return "Elige un día válido.", hora, lugar

    if hora is None:
        hora = ""
    try:
        hora = datetime.strptime(hora.strip(), "%H:%M").strftime("%H:%M")
    except ValueError:
        return "La hora debe tener formato HH:MM, por ejemplo 10:00.", hora, lugar

    if lugar is None:
        lugar = ""
    lugar = lugar.strip()
    if lugar == "":
        return "Escribe el lugar de la tutoría.", hora, lugar
    if len(lugar) > MAX_LUGAR:
        return f"El lugar no puede pasar de {MAX_LUGAR} caracteres.", hora, lugar

    return "", hora, lugar


# ------------------------------------------------------------- consultas

def estudiantes():
    return cargar_datos()["estudiantes"]


def materias():
    datos = cargar_datos()
    lista = []
    for profesor_info in datos["profesores"].values():
        if profesor_info["materia"] not in lista:
            lista.append(profesor_info["materia"])
    lista.sort(key=sin_tildes)
    return lista


def resumen_profesor(profesor_id, profesor_info):
    textos = []
    for horario in sorted(profesor_info["horarios"], key=clave_horario):
        textos.append(horario["dia"] + " " + horario["hora"])
    horarios_texto = ", ".join(textos)
    if horarios_texto == "":
        horarios_texto = "Sin horarios"

    return {
        "id": profesor_id,
        "nombre": profesor_info["nombre"],
        "materia": profesor_info["materia"],
        "horarios_texto": horarios_texto,
    }


def obtener_profesor(profesor):
    profesor_info = cargar_datos()["profesores"].get(profesor)
    if profesor_info is None:
        return None
    return resumen_profesor(profesor, profesor_info)


def listar_profesores(materia=None):
    datos = cargar_datos()
    resultado = []
    for profesor_id, profesor_info in datos["profesores"].items():
        if materia and profesor_info["materia"] != materia:
            continue
        resultado.append(resumen_profesor(profesor_id, profesor_info))
    resultado.sort(key=clave_profesor)
    return resultado


def proximas_tutorias(profesor, estudiante=None):
    return sesiones_de_profesor(cargar_datos(), profesor, estudiante)


def proximas_global(limite=5):
    datos = cargar_datos()
    todas = []
    for profesor_id, profesor_info in datos["profesores"].items():
        for sesion in sesiones_de_profesor(datos, profesor_id):
            sesion["profesor_id"] = profesor_id
            sesion["profesor"] = profesor_info["nombre"]
            sesion["materia"] = profesor_info["materia"]
            todas.append(sesion)
    todas.sort(key=clave_fecha)
    return todas[:limite]


def mis_tutorias(estudiante):
    datos = cargar_datos()
    tutorias = []

    for inscripcion in datos["inscripciones"]:
        if inscripcion["estudiante"] != estudiante:
            continue

        momento = juntar_fecha_y_hora(inscripcion["fecha"], inscripcion["hora"])
        if momento <= ahora():
            continue

        profesor_info = datos["profesores"].get(inscripcion["profesor"])
        if profesor_info is None:
            nombre = "Profesor"
            materia = ""
            lugar = ""
        else:
            nombre = profesor_info["nombre"]
            materia = profesor_info["materia"]
            horario = buscar_horario(profesor_info, inscripcion["horario"])
            if horario is None:
                lugar = ""
            else:
                lugar = horario["lugar"]

        falta = momento - ahora()
        cancelable = falta >= timedelta(days=DIAS_PARA_CANCELAR)

        tutorias.append({
            "id": inscripcion["id"],
            "profesor_id": inscripcion["profesor"],
            "profesor": nombre,
            "materia": materia,
            "fecha": inscripcion["fecha"],
            "dt": momento,
            "hora": inscripcion["hora"],
            "lugar": lugar,
            "nota": inscripcion["nota"],
            "cancelable": cancelable,
        })

    tutorias.sort(key=clave_fecha)
    return tutorias


# ------------------------------------------------- acciones del estudiante

def apuntarse(estudiante, profesor, horario, fecha, nota=""):
    datos = cargar_datos()

    if estudiante not in datos["estudiantes"]:
        return False, "Estudiante no registrado."

    profesor_info = datos["profesores"].get(profesor)
    if profesor_info is None:
        return False, "Profesor no encontrado."

    horario_info = buscar_horario(profesor_info, horario)
    if horario_info is None:
        return False, "Ese horario no existe."

    try:
        momento = juntar_fecha_y_hora(fecha, horario_info["hora"])
    except ValueError:
        return False, "La fecha no es válida."

    if DIAS[momento.weekday()] != horario_info["dia"]:
        return False, f"Esa tutoría es el {horario_info['dia'].lower()}."

    if momento <= ahora():
        return False, "Esa tutoría ya pasó."

    ultimo_dia = ahora().date() + timedelta(days=VENTANA_DIAS - 1)
    if momento.date() > ultimo_dia:
        return False, f"Solo puedes apuntarte a las tutorías de los próximos {VENTANA_DIAS} días."

    nota, error = revisar_nota(nota)
    if error:
        return False, error

    for inscripcion in datos["inscripciones"]:
        if inscripcion["estudiante"] != estudiante or inscripcion["fecha"] != fecha:
            continue

        if inscripcion["profesor"] == profesor and inscripcion["horario"] == horario:
            return False, "Ya te apuntaste a esa tutoría."

        if inscripcion["hora"] == horario_info["hora"]:
            otro_profesor = datos["profesores"][inscripcion["profesor"]]["nombre"]
            return False, f"Ya tienes otra tutoría a esa hora con {otro_profesor}."

    mayor_id = 0
    for inscripcion in datos["inscripciones"]:
        if inscripcion["id"] > mayor_id:
            mayor_id = inscripcion["id"]

    datos["inscripciones"].append({
        "id": mayor_id + 1,
        "estudiante": estudiante,
        "profesor": profesor,
        "horario": horario,
        "fecha": fecha,
        "hora": horario_info["hora"],
        "nota": nota,
    })
    guardar_datos(datos)
    return True, f"Quedó registrada tu asistencia a la tutoría de {profesor_info['nombre']}, {describir(momento)}."


def editar_nota(estudiante, inscripcion, nota):
    datos = cargar_datos()

    inscripcion_info = buscar_inscripcion(datos, inscripcion, estudiante)
    if inscripcion_info is None:
        return False, "No encontré esa tutoría entre las tuyas."

    momento = juntar_fecha_y_hora(inscripcion_info["fecha"], inscripcion_info["hora"])
    if momento <= ahora():
        return False, "Esa tutoría ya pasó."

    nota, error = revisar_nota(nota)
    if error:
        return False, error

    inscripcion_info["nota"] = nota
    guardar_datos(datos)
    return True, "Nota actualizada."


def cancelar(estudiante, inscripcion):
    datos = cargar_datos()

    inscripcion_info = buscar_inscripcion(datos, inscripcion, estudiante)
    if inscripcion_info is None:
        return False, "No encontré esa tutoría entre las tuyas."

    momento = juntar_fecha_y_hora(inscripcion_info["fecha"], inscripcion_info["hora"])
    if momento <= ahora():
        return False, "Esa tutoría ya pasó."

    falta = momento - ahora()
    if falta < timedelta(days=DIAS_PARA_CANCELAR):
        return False, (f"Solo se puede cancelar con {DIAS_PARA_CANCELAR} días de "
                       "anticipación. Escríbele al profesor.")

    datos["inscripciones"].remove(inscripcion_info)
    guardar_datos(datos)
    return True, "Tutoría cancelada."


# ------------------------------------------------------- panel profesor

def horarios_de(profesor):
    datos = cargar_datos()
    profesor_info = datos["profesores"].get(profesor)
    if profesor_info is None:
        return []

    resultado = []
    for horario in sorted(profesor_info["horarios"], key=clave_horario):
        futuras = inscripciones_futuras(datos, profesor, horario["id"])
        resultado.append({
            "id": horario["id"],
            "dia": horario["dia"],
            "hora": horario["hora"],
            "lugar": horario["lugar"],
            "proximos": len(futuras),
        })
    return resultado


def ver_inscritos(profesor):
    datos = cargar_datos()
    profesor_info = datos["profesores"].get(profesor)
    if profesor_info is None:
        return []

    grupos = {}   # clave: (fecha, id del horario)

    for inscripcion in datos["inscripciones"]:
        if inscripcion["profesor"] != profesor:
            continue

        momento = juntar_fecha_y_hora(inscripcion["fecha"], inscripcion["hora"])
        if momento <= ahora():
            continue

        clave = (inscripcion["fecha"], inscripcion["horario"])
        if clave not in grupos:
            horario = buscar_horario(profesor_info, inscripcion["horario"])
            if horario is None:
                lugar = ""
            else:
                lugar = horario["lugar"]
            grupos[clave] = {
                "dt": momento,
                "hora": inscripcion["hora"],
                "lugar": lugar,
                "estudiantes": [],
            }

        grupos[clave]["estudiantes"].append({
            "nombre": inscripcion["estudiante"],
            "nota": inscripcion["nota"],
        })

    resultado = list(grupos.values())
    resultado.sort(key=clave_fecha)
    return resultado


def crear_horario(profesor, dia, hora, lugar):
    datos = cargar_datos()
    profesor_info = datos["profesores"].get(profesor)
    if profesor_info is None:
        return False, "Profesor no encontrado."

    error, hora, lugar = revisar_horario(dia, hora, lugar)
    if error:
        return False, error

    for horario in profesor_info["horarios"]:
        if horario["dia"] == dia and horario["hora"] == hora:
            return False, "Ya tienes un horario ese día a esa hora."

    # los ids son "h1", "h2"...: busco el número mayor y le sumo 1
    mayor_numero = 0
    for otro_profesor in datos["profesores"].values():
        for horario in otro_profesor["horarios"]:
            numero = int(horario["id"][1:])
            if numero > mayor_numero:
                mayor_numero = numero

    profesor_info["horarios"].append({
        "id": "h" + str(mayor_numero + 1),
        "dia": dia,
        "hora": hora,
        "lugar": lugar,
    })
    guardar_datos(datos)
    return True, f"Horario agregado: {dia} {hora}."


def editar_horario(profesor, horario, dia, hora, lugar):
    datos = cargar_datos()
    profesor_info = datos["profesores"].get(profesor)
    if profesor_info is None:
        return False, "Profesor no encontrado."

    horario_info = buscar_horario(profesor_info, horario)
    if horario_info is None:
        return False, "Ese horario no existe."

    error, hora, lugar = revisar_horario(dia, hora, lugar)
    if error:
        return False, error

    for otro in profesor_info["horarios"]:
        if otro["id"] != horario and otro["dia"] == dia and otro["hora"] == hora:
            return False, "Ya tienes otro horario ese día a esa hora."

    cambia_dia_u_hora = dia != horario_info["dia"] or hora != horario_info["hora"]
    if cambia_dia_u_hora:
        if len(inscripciones_futuras(datos, profesor, horario)) > 0:
            return False, "Hay estudiantes apuntados. Por ahora solo puedes cambiar el lugar."

    horario_info["dia"] = dia
    horario_info["hora"] = hora
    horario_info["lugar"] = lugar
    guardar_datos(datos)
    return True, "Horario actualizado."


def eliminar_horario(profesor, horario):
    datos = cargar_datos()
    profesor_info = datos["profesores"].get(profesor)
    if profesor_info is None:
        return False, "Profesor no encontrado."

    horario_info = buscar_horario(profesor_info, horario)
    if horario_info is None:
        return False, "Ese horario no existe."

    if len(inscripciones_futuras(datos, profesor, horario)) > 0:
        return False, "No puedes eliminarlo: hay estudiantes apuntados a próximas tutorías."

    profesor_info["horarios"].remove(horario_info)
    guardar_datos(datos)
    return True, "Horario eliminado."