from datetime import timedelta

import modules.utils as utils


# Devuelve la inscripción con el id dado, si existe y pertenece al estudiante; None en caso contrario
def buscar_inscripcion(inscripciones, inscripcion_id, estudiante_id):
    for inscripcion in inscripciones:
        if inscripcion["id"] == inscripcion_id and inscripcion["estudiante_id"] == estudiante_id:
            return inscripcion
    return None


# Devuelve (False, mensaje de error) si la nota es inválida, o (True, nota limpia) si es válida
def revisar_nota(nota):
    nota = nota.strip()   # elimina espacios al inicio y al final
    if nota == "":
        return False, "La nota no puede estar vacía."
    if len(nota) > utils.MAX_NOTA:
        return False, f"La nota no puede tener más de {utils.MAX_NOTA} caracteres."
    return True, nota


def mis_tutorias(estudiante_id):
    inscripciones = utils.cargar_datos("inscripciones")
    horarios = utils.cargar_datos("horarios")
    inscripciones_futuras = []
    for inscripcion in inscripciones:
        if inscripcion["estudiante_id"] == estudiante_id:
            fecha_hora_tutoria = utils.fecha_hora_de_inscripcion(inscripcion, horarios)
            if fecha_hora_tutoria >= utils.fecha_hora_actual():   # solo las que aún no han pasado
                inscripciones_futuras.append(inscripcion)
    return inscripciones_futuras


def cancelar(inscripcion_id, estudiante_id):
    inscripciones = utils.cargar_datos("inscripciones")
    horarios = utils.cargar_datos("horarios")

    inscripcion = buscar_inscripcion(inscripciones, inscripcion_id, estudiante_id)
    if inscripcion is None:
        return False, "No se encontró la inscripción."

    fecha_hora_tutoria = utils.fecha_hora_de_inscripcion(inscripcion, horarios)
    tiempo_restante = fecha_hora_tutoria - utils.fecha_hora_actual()
    if tiempo_restante.days < utils.DIAS_PARA_CANCELAR:   # .days son los días completos que faltan
        return False, f"No se puede cancelar la tutoría con menos de {utils.DIAS_PARA_CANCELAR} días de anticipación."

    inscripciones.remove(inscripcion)
    utils.guardar_datos("inscripciones", inscripciones)
    return True, "Inscripción cancelada exitosamente."


def editar_nota(inscripcion_id, estudiante_id, nota_nueva):
    nota_valida, mensaje = revisar_nota(nota_nueva)
    if not nota_valida:
        return False, mensaje   # aquí mensaje es el error

    inscripciones = utils.cargar_datos("inscripciones")
    horarios = utils.cargar_datos("horarios")

    inscripcion = buscar_inscripcion(inscripciones, inscripcion_id, estudiante_id)
    if inscripcion is None:
        return False, "No se encontró la inscripción."

    fecha_hora_tutoria = utils.fecha_hora_de_inscripcion(inscripcion, horarios)
    if fecha_hora_tutoria < utils.fecha_hora_actual():
        return False, "No se puede editar la nota de una tutoría que ya ha pasado."

    inscripcion["nota"] = mensaje   # aquí mensaje es la nota ya limpia
    utils.guardar_datos("inscripciones", inscripciones)
    return True, "Nota editada exitosamente."


# Fechas (texto) de los próximos VENTANA_DIAS días en que cae este horario y que aún no han pasado
def proximas_fechas(horario):
    fechas = []
    ahora = utils.fecha_hora_actual()
    for dias_adelante in range(utils.VENTANA_DIAS):
        dia = ahora + timedelta(days=dias_adelante)
        nombre_dia = utils.DIAS[dia.weekday()]
        if nombre_dia == horario["dia"]:
            fecha_texto = dia.date().isoformat()   # "2026-11-10"
            fecha_hora = utils.construir_fecha_hora(fecha_texto, horario["hora"])
            if fecha_hora >= ahora:
                fechas.append(fecha_texto)
    return fechas


def apuntarse(estudiante_id, horario_id, fecha_texto, nota):
    nota_valida, mensaje = revisar_nota(nota)
    if not nota_valida:
        return False, mensaje

    horarios = utils.cargar_datos("horarios")
    horario = utils.buscar_por_id(horarios, horario_id)
    if horario is None:
        return False, "No se encontró el horario."

    if fecha_texto not in proximas_fechas(horario):
        return False, f"Solo puedes apuntarte a tutorías de los próximos {utils.VENTANA_DIAS} días."

    # No repetir la misma tutoría ni tener dos a la misma hora el mismo día
    inscripciones = utils.cargar_datos("inscripciones")
    for inscripcion in inscripciones:
        if inscripcion["estudiante_id"] == estudiante_id and inscripcion["fecha"] == fecha_texto:
            if inscripcion["horario_id"] == horario_id:
                return False, "Ya estás inscrito en esta tutoría."
            otro_horario = utils.buscar_por_id(horarios, inscripcion["horario_id"])
            if otro_horario["hora"] == horario["hora"]:
                return False, "Ya tienes otra tutoría a la misma hora."

    nueva_inscripcion = {
        "id": utils.nuevo_id(inscripciones),
        "estudiante_id": estudiante_id,
        "horario_id": horario_id,
        "fecha": fecha_texto,
        "nota": mensaje
    }
    inscripciones.append(nueva_inscripcion)
    utils.guardar_datos("inscripciones", inscripciones)
    return True, "Te apuntaste a la tutoría exitosamente."


# LECTURAS

def listar_profesores():
    return utils.cargar_datos("profesores")


# Las tutorías concretas (con fecha) de un profesor en los próximos días
def proximas_tutorias(profesor_id):
    horarios = utils.cargar_datos("horarios")
    tutorias = []
    for horario in horarios:
        if horario["profesor_id"] == profesor_id:
            for fecha_texto in proximas_fechas(horario):
                tutorias.append({
                    "profesor_id": profesor_id,
                    "horario_id": horario["id"],
                    "fecha": fecha_texto,
                    "dia": horario["dia"],
                    "hora": horario["hora"],
                    "lugar": horario["lugar"]
                })
    return tutorias


# Las tutorías de todos los profesores, con el nombre del profesor
def proximas_global():
    profesores = utils.cargar_datos("profesores")
    tutorias = []
    for profesor in profesores:
        for tutoria in proximas_tutorias(profesor["id"]):
            tutoria["profesor_nombre"] = profesor["nombre"]
            tutorias.append(tutoria)
    return tutorias
