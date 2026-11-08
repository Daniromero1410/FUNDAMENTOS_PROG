from datetime import timedelta

import modules.utils as utils

# Devuelve la inscripción con el id dado, si existe y pertenece al estudiante dado; None en caso contrario.
def buscar_inscripcion(inscripciones, inscripcion_id, estudiante):
  for inscripcion in inscripciones:
    if inscripcion["id"] == inscripcion_id and inscripcion["estudiante"] == estudiante:
      return inscripcion
  return None

 # booleano y mensaje de error si la nota es inválida; la nota limpia si es válida
def revisar_nota(nota):
  nota = nota.strip() # elimina espacios al inicio y final
  if nota == "":
    return False, "La nota no puede estar vacía."
  if len(nota) > utils.MAX_NOTA:
    return False, f"La nota no puede tener más de {utils.MAX_NOTA} caracteres."
  return True, nota

def mis_tutorias(estudiante):
  inscripciones = utils.cargar_datos("inscripciones")
  resultado = []
  for inscripcion in inscripciones:
    if inscripcion["estudiante"] == estudiante:
      fecha_hora_tutoria = utils.construir_fecha_hora(inscripcion["fecha"], inscripcion["hora"])
      if fecha_hora_tutoria >= utils.fecha_hora_actual(): # Si la tutoria es futura, la agregamos a la lista
        resultado.append(inscripcion)
  return resultado # Retorna la lista de inscripciones futuras del estudiante

def cancelar(inscripcion_id, estudiante):
  inscripciones = utils.cargar_datos("inscripciones")

  inscripcion = buscar_inscripcion(inscripciones, inscripcion_id, estudiante)
  if inscripcion is None:
    return False, "No se encontró la inscripción."

  fecha_hora_tutoria = utils.construir_fecha_hora(inscripcion["fecha"], inscripcion["hora"])
  tiempo_restante = fecha_hora_tutoria - utils.fecha_hora_actual() # Calcula el tiempo restante hasta la tutoría
  # Verifica si el tiempo restante es menor a los días permitidos para cancelar
  if tiempo_restante.days < utils.DIAS_PARA_CANCELAR: # Usa .days() para obtener la cantidad de días completos
    return False, f"No se puede cancelar la tutoría con menos de {utils.DIAS_PARA_CANCELAR} días de anticipación."

  inscripciones.remove(inscripcion)
  utils.guardar_datos("inscripciones", inscripciones)
  return True, "Inscripción cancelada exitosamente."

def editar_nota(inscripcion_id, estudiante, nota_nueva):
  # Verifica si la inscripción existe y pertenece al estudiante
  nota_valida, mensaje = revisar_nota(nota_nueva)
  if not nota_valida:
    return False, mensaje

  inscripciones = utils.cargar_datos("inscripciones")

  inscripcion = buscar_inscripcion(inscripciones, inscripcion_id, estudiante)
  if inscripcion is None:
    return False, "No se encontró la inscripción."

  fecha_hora_tutoria = utils.construir_fecha_hora(inscripcion["fecha"], inscripcion["hora"])
  if fecha_hora_tutoria < utils.fecha_hora_actual(): # Verifica si la tutoría ya ha pasado
    return False, "No se puede editar la nota de una tutoría que ya ha pasado."

  inscripcion["nota"] = mensaje.strip() # Guardamos la nota limpia
  utils.guardar_datos("inscripciones", inscripciones)
  return True, "Nota editada exitosamente."


def proximas_fechas(horario):
  fechas = []
  hora_actual = utils.fecha_hora_actual()
  for dias_adelante in range(utils.VENTANA_DIAS): # Itera sobre los próximos días según la ventana definida
    numero_dia = hora_actual + timedelta(days=dias_adelante)
    nombre_dia = utils.DIAS[numero_dia.weekday()]
    if nombre_dia in horario["dia"]:
      fecha_texto = numero_dia.date().isoformat() # "2026-11-10"
      fecha_hora = utils.construir_fecha_hora(fecha_texto, horario["hora"])
      if fecha_hora >= hora_actual: # Solo agregamos fechas futuras
        fechas.append(fecha_texto)
  return fechas

def apuntarse(estudiante, profesor_id, horario_id, fecha_texto, nota):
  nota_valida, mensaje = revisar_nota(nota)
  if not nota_valida:
    return False, mensaje

  # Valida si el profesor y el horario existen y si la fecha es válida
  profesores = utils.cargar_datos("profesores")
  if profesor_id not in profesores:
    return False, "No se encontró el profesor."
  horario = utils.buscar_horario(profesores[profesor_id], horario_id)
  if horario is None:
    return False, "No se encontró el horario."

  if fecha_texto not in proximas_fechas(horario):
    return False, "Solo puedes apuntarte a tutorías de los próximos " + str(utils.VENTANA_DIAS) + " días."

   # Validar si el estudiante ya tiene una tutoría a la misma hora o ya está inscrito en la misma tutoría
  inscripciones = utils.cargar_datos("inscripciones")
  for inscripcion in inscripciones:
    if (inscripcion["estudiante"]) == estudiante and inscripcion["fecha"] == fecha_texto:
      if inscripcion["profesor"] == profesor_id and inscripcion["horario"] == horario_id:
        return False, "Ya estás inscrito en esta tutoría."
      if inscripcion["hora"] == horario["hora"]:
        return False, "Ya tienes otra tutoría a la misma hora." 

  # Aumentar el id de la nueva inscripción
  nuevo_id = 1
  for inscripcion in inscripciones:
    if inscripcion["id"] >= nuevo_id:
      nuevo_id = inscripcion["id"] + 1

  nueva_inscripcion = {
    "id": nuevo_id,
    "estudiante": estudiante,
    "profesor": profesor_id,
    "horario": horario_id,
    "fecha": fecha_texto,
    "hora": horario["hora"],
    "nota": mensaje.strip() # Guardamos la nota limpia
  }
  inscripciones.append(nueva_inscripcion)
  utils.guardar_datos("inscripciones", inscripciones)
  return True, "Te apuntaste a la tutoría exitosamente."


# LECTURAS

def listar_profesores():
  profesores = utils.cargar_datos("profesores")
  lista = []
  for profesor_id in profesores:
    profesor = profesores[profesor_id]
    lista.append({
      "id": profesor_id,
      "nombre": profesor["nombre"],
      "materia": profesor["materia"]
    })
  return lista

# Las tutorías concretas (con fecha) de un profesor en los próximos días
def proximas_tutorias(profesor_id):
  profesores = utils.cargar_datos("profesores")
  if profesor_id not in profesores:
    return []

  profesor = profesores[profesor_id]
  tutorias = []
  for horario in profesor["horarios"]:
    for fecha_texto in proximas_fechas(horario):
      tutorias.append({
          "profesor": profesor_id,
          "horario": horario["id"],
          "fecha": fecha_texto,
          "dia": horario["dia"],
          "hora": horario["hora"],
          "lugar": horario["lugar"],
      })
  return tutorias

def proximas_global():
    # Las tutorías de todos los profesores, con el nombre del profesor
    tutorias = []
    profesores = utils.cargar_datos("profesores")
    for profesor_id in profesores:
        for tutoria in proximas_tutorias(profesor_id):
            tutoria["profesor_nombre"] = profesores[profesor_id]["nombre"]
            tutorias.append(tutoria)
    return tutorias
