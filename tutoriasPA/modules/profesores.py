import modules.utils as utils


def horarios_de_profesor(profesor_id):
    horarios = utils.cargar_datos("horarios")
    horarios_del_profesor = []
    for horario in horarios:
        if horario["profesor_id"] == profesor_id:
            horarios_del_profesor.append(horario)
    return horarios_del_profesor


# Inscripciones futuras a las tutorías de este profesor, con el nombre del estudiante y el día y la hora
def ver_inscritos(profesor_id):
    inscripciones = utils.cargar_datos("inscripciones")
    horarios = utils.cargar_datos("horarios")
    estudiantes = utils.cargar_datos("estudiantes")
    inscritos = []
    for inscripcion in inscripciones:
        horario = utils.buscar_por_id(horarios, inscripcion["horario_id"])
        if horario["profesor_id"] == profesor_id:
            fecha_hora_tutoria = utils.fecha_hora_de_inscripcion(inscripcion, horarios)
            if fecha_hora_tutoria >= utils.fecha_hora_actual():   # solo inscripciones futuras
                estudiante = utils.buscar_por_id(estudiantes, inscripcion["estudiante_id"])
                inscritos.append({
                    "id": inscripcion["id"],
                    "horario_id": inscripcion["horario_id"],
                    "fecha": inscripcion["fecha"],
                    "nota": inscripcion["nota"],
                    "dia": horario["dia"],
                    "hora": horario["hora"],
                    "estudiante_nombre": estudiante["nombre"]
                })
    return inscritos


# Devuelve (False, mensaje de error) o (True, lugar limpio)
def validar_horario(dia, hora, lugar):
    if dia not in utils.DIAS:
        return False, "El día no es válido."

    if len(hora) != 5 or hora[2] != ":":
        return False, "La hora debe tener el formato HH:MM, por ejemplo 09:30."
    try:
        utils.construir_fecha_hora("2000-01-01", hora)
    except ValueError:
        return False, "La hora debe tener el formato HH:MM, por ejemplo 09:30."

    lugar = lugar.strip()
    if lugar == "":
        return False, "El lugar no puede estar vacío."
    if len(lugar) > utils.MAX_LUGAR:
        return False, f"El lugar no puede pasar de {utils.MAX_LUGAR} caracteres."
    return True, lugar


def crear_horario(profesor_id, dia, hora, lugar):
    horario_valido, mensaje = validar_horario(dia, hora, lugar)
    if not horario_valido:
        return False, mensaje   # aquí mensaje es el error

    profesores = utils.cargar_datos("profesores")
    if utils.buscar_por_id(profesores, profesor_id) is None:
        return False, "Profesor no encontrado."

    # El profesor no puede tener dos horarios el mismo día a la misma hora
    horarios = utils.cargar_datos("horarios")
    for horario in horarios:
        if horario["profesor_id"] == profesor_id and horario["dia"] == dia and horario["hora"] == hora:
            return False, "Ya existe un horario para ese día y hora."

    nuevo_horario = {
        "id": utils.nuevo_id(horarios),
        "profesor_id": profesor_id,
        "dia": dia,
        "hora": hora,
        "lugar": mensaje   # aquí mensaje es el lugar ya limpio
    }
    horarios.append(nuevo_horario)
    utils.guardar_datos("horarios", horarios)
    return True, "Horario creado."


# True si alguien está inscrito (a futuro) a este horario
def hay_inscritos(profesor_id, horario_id):
    for inscripcion in ver_inscritos(profesor_id):
        if inscripcion["horario_id"] == horario_id:
            return True
    return False


def editar_horario(profesor_id, horario_id, dia, hora, lugar):
    horario_valido, mensaje = validar_horario(dia, hora, lugar)
    if not horario_valido:
        return False, mensaje

    # El horario debe existir y ser de este profesor
    horarios = utils.cargar_datos("horarios")
    horario = utils.buscar_por_id(horarios, horario_id)
    if horario is None or horario["profesor_id"] != profesor_id:
        return False, "Ese horario no existe."

    cambia_dia_u_hora = False
    if dia != horario["dia"] or hora != horario["hora"]:
        cambia_dia_u_hora = True

    if cambia_dia_u_hora:
        if hay_inscritos(profesor_id, horario_id):
            return False, "Hay estudiantes inscritos: por ahora solo puedes cambiar el lugar."
        for otro_horario in horarios:
            if otro_horario["profesor_id"] == profesor_id and otro_horario["id"] != horario_id:
                if otro_horario["dia"] == dia and otro_horario["hora"] == hora:
                    return False, "Ya tienes un horario ese día a esa hora."

    horario["dia"] = dia
    horario["hora"] = hora
    horario["lugar"] = mensaje
    utils.guardar_datos("horarios", horarios)
    return True, "Horario actualizado."


def eliminar_horario(profesor_id, horario_id):
    horarios = utils.cargar_datos("horarios")
    horario = utils.buscar_por_id(horarios, horario_id)
    if horario is None or horario["profesor_id"] != profesor_id:
        return False, "Ese horario no existe."

    if hay_inscritos(profesor_id, horario_id):
        return False, "Hay estudiantes inscritos: no puedes eliminar este horario."

    # Borrado en cascada: las inscripciones viejas de este horario se van con él
    inscripciones = utils.cargar_datos("inscripciones")
    inscripciones_restantes = []
    for inscripcion in inscripciones:
        if inscripcion["horario_id"] != horario_id:
            inscripciones_restantes.append(inscripcion)

    horarios.remove(horario)
    utils.guardar_datos("horarios", horarios)
    utils.guardar_datos("inscripciones", inscripciones_restantes)
    return True, "Horario eliminado."
