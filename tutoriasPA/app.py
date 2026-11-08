from flask import Flask, render_template, request, redirect, url_for, session, flash
import modules.utils as utils
import modules.estudiantes as Estudiante
import modules.profesores as Profesor

app = Flask(__name__)
app.secret_key = "tutorias-udes"   # Flask la usa para firmar la sesión (la "memoria" de quién entró)


# ===== Quién entró =====

# Devuelve quien entró (un diccionario de estudiantes o de profesores) o None si nadie ha entrado
def usuario_actual():
    usuario_id = session.get("usuario_id")
    rol = session.get("rol")
    if usuario_id is None:
        return None
    if rol == "estudiante":
        return utils.buscar_por_id(utils.cargar_datos("estudiantes"), usuario_id)
    if rol == "profesor":
        return utils.buscar_por_id(utils.cargar_datos("profesores"), usuario_id)
    return None


# True si quien entró tiene el rol que se necesita
def es_rol(rol_necesario):
    return session.get("rol") == rol_necesario and usuario_actual() is not None


# Guarda el mensaje para mostrarlo en la siguiente página: verde si salió bien, rojo si no
def avisar(ok, mensaje):
    if ok:
        flash(mensaje, "ok")
    else:
        flash(mensaje, "error")


# Hace que "usuario" y "rol" existan en todas las plantillas
@app.context_processor
def datos_para_plantillas():
    return {"usuario": usuario_actual(), "rol": session.get("rol")}


# ===== Entrar y salir =====

@app.get("/")
def inicio():
    return render_template(
        "inicio.html",
        estudiantes=utils.cargar_datos("estudiantes"),
        profesores=utils.cargar_datos("profesores"),
    )


@app.post("/entrar")
def entrar():
    session.clear()
    session["rol"] = request.form["rol"]
    session["usuario_id"] = int(request.form["usuario_id"])
    if session["rol"] == "profesor":
        return redirect(url_for("ver_panel"))
    return redirect(url_for("ver_profesores"))


@app.get("/salir")
def salir():
    session.clear()
    return redirect(url_for("inicio"))


# ===== Estudiante =====

@app.get("/profesores")
def ver_profesores():
    profesores = Estudiante.listar_profesores()
    return render_template("profesores.html", profesores=profesores)


@app.get("/profesor/<int:profesor_id>")
def ver_profesor(profesor_id):
    profesores = Estudiante.listar_profesores()
    profesor = utils.buscar_por_id(profesores, profesor_id)
    if profesor is None:
        return "Profesor no encontrado", 404
    tutorias = Estudiante.proximas_tutorias(profesor_id)
    return render_template("profesor.html", profesor=profesor, tutorias=tutorias)


@app.post("/apuntarse")
def apuntarse_a_tutoria():
    if not es_rol("estudiante"):
        return redirect(url_for("inicio"))

    profesor_id = int(request.form["profesor_id"])
    horario_id = int(request.form["horario_id"])
    fecha = request.form["fecha"]
    nota = request.form["nota"]

    ok, mensaje = Estudiante.apuntarse(usuario_actual()["id"], horario_id, fecha, nota)
    avisar(ok, mensaje)
    return redirect(url_for("ver_profesor", profesor_id=profesor_id))


@app.get("/mis-tutorias")
def ver_mis_tutorias():
    if not es_rol("estudiante"):
        return redirect(url_for("inicio"))

    tutorias = Estudiante.mis_tutorias(usuario_actual()["id"])
    return render_template("mis_tutorias.html", tutorias=tutorias)


@app.post("/tutoria/<int:inscripcion_id>/nota")
def cambiar_nota(inscripcion_id):
    if not es_rol("estudiante"):
        return redirect(url_for("inicio"))

    nota = request.form["nota"]
    ok, mensaje = Estudiante.editar_nota(inscripcion_id, usuario_actual()["id"], nota)
    avisar(ok, mensaje)
    return redirect(url_for("ver_mis_tutorias"))


@app.post("/tutoria/<int:inscripcion_id>/cancelar")
def cancelar_tutoria(inscripcion_id):
    if not es_rol("estudiante"):
        return redirect(url_for("inicio"))

    ok, mensaje = Estudiante.cancelar(inscripcion_id, usuario_actual()["id"])
    avisar(ok, mensaje)
    return redirect(url_for("ver_mis_tutorias"))


# ===== Profesor =====

@app.get("/panel")
def ver_panel():
    if not es_rol("profesor"):
        return redirect(url_for("inicio"))

    profesor_id = usuario_actual()["id"]
    return render_template(
        "panel_profesor.html",
        horarios=Profesor.horarios_de_profesor(profesor_id),
        inscritos=Profesor.ver_inscritos(profesor_id),
        dias=utils.DIAS,
    )


@app.post("/panel/horarios")
def crear_horario():
    if not es_rol("profesor"):
        return redirect(url_for("inicio"))

    ok, mensaje = Profesor.crear_horario(
        usuario_actual()["id"], request.form["dia"], request.form["hora"], request.form["lugar"]
    )
    avisar(ok, mensaje)
    return redirect(url_for("ver_panel"))


@app.post("/panel/horarios/<int:horario_id>/editar")
def editar_horario(horario_id):
    if not es_rol("profesor"):
        return redirect(url_for("inicio"))

    ok, mensaje = Profesor.editar_horario(
        usuario_actual()["id"], horario_id, request.form["dia"], request.form["hora"], request.form["lugar"]
    )
    avisar(ok, mensaje)
    return redirect(url_for("ver_panel"))


@app.post("/panel/horarios/<int:horario_id>/eliminar")
def eliminar_horario(horario_id):
    if not es_rol("profesor"):
        return redirect(url_for("inicio"))

    ok, mensaje = Profesor.eliminar_horario(usuario_actual()["id"], horario_id)
    avisar(ok, mensaje)
    return redirect(url_for("ver_panel"))


if __name__ == "__main__":
    app.run(debug=True)
