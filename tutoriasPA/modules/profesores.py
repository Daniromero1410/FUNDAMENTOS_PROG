import modules.utils as utils

def horarios_de_profesor(profesor_id):
    profesores = utils.cargar_datos("profesores")
    if profesor_id not in profesores:
        return []
    return profesores[profesor_id]["horarios"]

def ver_inscritos(profesor_id):
    inscripciones = utils.cargar_datos("inscripciones")
    inscritos = []
    for inscripcion in inscripciones:
        if inscripcion["profesor"] == profesor_id:
            fecha_hora_tutoria = utils.construir_fecha_hora(inscripcion["fecha"], inscripcion["hora"])
            if fecha_hora_tutoria >= utils.fecha_hora_actual(): # Solo inscripciones futuras
                inscritos.append(inscripcion)
    return inscritos

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
        return False, "El lugar no puede pasar de " + str(utils.MAX_LUGAR) + " caracteres."
    return True, lugar

def crear_horario(profesor_id, dia, hora, lugar):
    horario_valido, mensaje = validar_horario(dia, hora, lugar)
    if not horario_valido:
        return False, mensaje

    # Valida que no exista un horario con el mismo día y hora para el profesor
    profesores = utils.cargar_datos("profesores")
    if profesor_id not in profesores:
        return False, "Profesor no encontrado."
    profesor = profesores[profesor_id]
    for horario in profesor["horarios"]:
        if horario["dia"] == dia and horario["hora"] == hora:
            return False, "Ya existe un horario para ese día y hora."

    # Encontrar el número más alto de los horarios existentes para asignar un nuevo ID
    numero_mayor = 0
    for otro_id in profesores:
        for horario in profesores[otro_id]["horarios"]:
            numero = int(horario["id"][1:]) # Tomamos el número después de la "h"
            if numero > numero_mayor:
                numero_mayor = numero

    nuevo_horario = {
        "id": "h" + str(numero_mayor + 1),
        "dia": dia,
        "hora": hora,
        "lugar": mensaje.strip(), # Guardamos el lugar limpio
    }
    profesor["horarios"].append(nuevo_horario)
    utils.guardar_datos("profesores", profesores)
    return True, "Horario creado."

# Profesor revisa si hay inscritos en un horario específico
def hay_inscritos(profesor_id, horario_id):
    for inscripcion in ver_inscritos(profesor_id):
        if inscripcion["horario"] == horario_id:
            return True
    return False

def editar_horario(profesor_id, horario_id, dia, hora, lugar):
    horario_valido, mensaje = validar_horario(dia, hora, lugar)
    if not horario_valido:
        return False, mensaje

    # Validar que el profesor y el horario existan
    profesores = utils.cargar_datos("profesores")
    if profesor_id not in profesores:
        return False, "Ese profesor no existe."
    profesor = profesores[profesor_id]
    horario = utils.buscar_horario(profesor, horario_id)
    if horario is None:
        return False, "Ese horario no existe."

    cambia_dia_u_hora = False
    if dia != horario["dia"] or hora != horario["hora"]: # Valida si se cambió el día o la hora
        cambia_dia_u_hora = True

    if cambia_dia_u_hora:
        if hay_inscritos(profesor_id, horario_id):
            return False, "Hay estudiantes inscritos: por ahora solo puedes cambiar el lugar."
        for otro_horario in profesor["horarios"]:
            if otro_horario["id"] != horario_id:
                if otro_horario["dia"] == dia and otro_horario["hora"] == hora:
                    return False, "Ya tienes un horario ese día a esa hora."

    horario["dia"] = dia
    horario["hora"] = hora
    horario["lugar"] = mensaje.strip() # Guardamos el lugar limpio
    utils.guardar_datos("profesores", profesores)
    return True, "Horario actualizado."


def eliminar_horario(profesor_id, horario_id):
    profesores = utils.cargar_datos("profesores")
    if profesor_id not in profesores:
        return False, "Ese profesor no existe."
    profesor = profesores[profesor_id]

    horario = utils.buscar_horario(profesor, horario_id)
    if horario is None:
        return False, "Ese horario no existe."

    if hay_inscritos(profesor_id, horario_id):
        return False, "Hay estudiantes inscritos: no puedes eliminar este horario."

    profesor["horarios"].remove(horario)
    utils.guardar_datos("profesores", profesores)
    return True, "Horario eliminado."
        
