"""Frontend Flask del sistema de tutorías. Solo recibe clics y llama a logica.py."""
from functools import wraps

from flask import (Flask, abort, flash, redirect, render_template, request,
                   session, url_for)

import tutoriasPA.modules.utils as utils

app = Flask(__name__)
app.secret_key = "demo-tutorias-cambiar-si-se-publica"

PALETA = [255, 160, 22, 330, 195, 45]  # tonos para avatares y materias


# ------------------------------------------------------------------ filtros

@app.template_filter("hue")
def filtro_hue(materia):
    todas = utils.materias()
    return PALETA[todas.index(materia) % len(PALETA)] if materia in todas else PALETA[0]


@app.template_filter("hue_n")
def filtro_hue_n(indice):
    return PALETA[indice % len(PALETA)]


@app.template_filter("dia")
def filtro_dia(fecha):
    return f"{utils.DIAS[fecha.weekday()]} {fecha.day} de {utils.MESES[fecha.month - 1]}"


@app.template_filter("dia_semana")
def filtro_dia_semana(fecha):
    return utils.DIAS[fecha.weekday()]


@app.template_filter("mes_corto")
def filtro_mes_corto(fecha):
    return utils.MESES[fecha.month - 1][:3]


# ------------------------------------------------------------------ sesión

def usuario_actual():
    """(rol, usuario) si la sesión es válida; (None, None) si no."""
    rol, usuario = session.get("rol"), session.get("usuario")
    datos = utils.cargar_datos()
    if rol == "estudiante" and usuario in datos["estudiantes"]:
        return rol, usuario
    if rol == "profesor" and usuario in datos["profesores"]:
        return rol, usuario
    return None, None


def requiere(rol_necesario):
    def decorador(vista):
        @wraps(vista)
        def envoltura(*args, **kwargs):
            rol, _ = usuario_actual()
            if rol != rol_necesario:
                return redirect(url_for("inicio"))
            return vista(*args, **kwargs)
        return envoltura
    return decorador


@app.context_processor
def contexto():
    rol, usuario = usuario_actual()
    nombre = usuario
    if rol == "profesor":
        nombre = utils.obtener_profesor(usuario)["nombre"]
    return {"rol": rol, "usuario": usuario, "nombre_usuario": nombre, "logica": utils}


# -------------------------------------------------------------------- inicio

@app.get("/")
def inicio():
    return render_template("inicio.html",
                           estudiantes=utils.estudiantes(),
                           profesores=utils.listar_profesores(),
                           proximas=utils.proximas_global(5))


@app.post("/entrar")
def entrar():
    rol, usuario = request.form.get("rol", ""), request.form.get("usuario", "")
    session["rol"], session["usuario"] = rol, usuario
    rol_ok, _ = usuario_actual()
    if rol_ok == "estudiante":
        return redirect(url_for("profesores"))
    if rol_ok == "profesor":
        return redirect(url_for("panel"))
    session.clear()
    flash("Elige un usuario de la lista.", "error")
    return redirect(url_for("inicio"))


@app.get("/salir")
def salir():
    session.clear()
    return redirect(url_for("inicio"))


# ---------------------------------------------------------------- estudiante

@app.get("/profesores")
@requiere("estudiante")
def profesores():
    materia = request.args.get("materia") or None
    return render_template("profesores.html",
                           profesores=utils.listar_profesores(materia),
                           materias=utils.materias(),
                           materia_activa=materia)


@app.get("/profesor/<pid>")
@requiere("estudiante")
def profesor(pid):
    info = utils.obtener_profesor(pid)
    if info is None:
        abort(404)
    sesiones = utils.proximas_tutorias(pid, session["usuario"])
    dias = {}
    for sesion in sesiones:
        dias.setdefault(sesion["dt"].date(), []).append(sesion)
    return render_template("profesor.html", prof=info, dias=list(dias.items()))


@app.post("/apuntarse")
@requiere("estudiante")
def apuntarse():
    f = request.form
    pid = f.get("profesor", "")
    ok, mensaje = utils.apuntarse(session["usuario"], pid, f.get("horario", ""),
                                   f.get("fecha", ""), f.get("nota", ""))
    flash(mensaje, "ok" if ok else "error")
    if ok:
        return redirect(url_for("mis_tutorias"))
    if utils.obtener_profesor(pid):
        return redirect(url_for("profesor", pid=pid))
    return redirect(url_for("profesores"))


@app.get("/mis-tutorias")
@requiere("estudiante")
def mis_tutorias():
    return render_template("mis_tutorias.html",
                           tutorias=utils.mis_tutorias(session["usuario"]))


@app.post("/tutoria/<int:iid>/nota")
@requiere("estudiante")
def editar_nota(iid):
    ok, mensaje = utils.editar_nota(session["usuario"], iid, request.form.get("nota", ""))
    flash(mensaje, "ok" if ok else "error")
    return redirect(url_for("mis_tutorias"))


@app.post("/tutoria/<int:iid>/cancelar")
@requiere("estudiante")
def cancelar(iid):
    ok, mensaje = utils.cancelar(session["usuario"], iid)
    flash(mensaje, "ok" if ok else "error")
    return redirect(url_for("mis_tutorias"))


# ------------------------------------------------------------------ profesor

@app.get("/panel")
@requiere("profesor")
def panel():
    pid = session["usuario"]
    return render_template("panel_profesor.html",
                           prof=utils.obtener_profesor(pid),
                           horarios=utils.horarios_de(pid),
                           inscritos=utils.ver_inscritos(pid))


@app.post("/panel/horarios")
@requiere("profesor")
def panel_crear():
    f = request.form
    ok, mensaje = utils.crear_horario(session["usuario"], f.get("dia", ""),
                                       f.get("hora", ""), f.get("lugar", ""))
    flash(mensaje, "ok" if ok else "error")
    return redirect(url_for("panel"))


@app.post("/panel/horarios/<hid>/editar")
@requiere("profesor")
def panel_editar(hid):
    f = request.form
    ok, mensaje = utils.editar_horario(session["usuario"], hid, f.get("dia", ""),
                                        f.get("hora", ""), f.get("lugar", ""))
    flash(mensaje, "ok" if ok else "error")
    return redirect(url_for("panel"))


@app.post("/panel/horarios/<hid>/eliminar")
@requiere("profesor")
def panel_eliminar(hid):
    ok, mensaje = utils.eliminar_horario(session["usuario"], hid)
    flash(mensaje, "ok" if ok else "error")
    return redirect(url_for("panel"))


if __name__ == "__main__":
    app.run(debug=True)
