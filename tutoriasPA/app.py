from flask import Flask, render_template
import modules.estudiantes as estudiante

app = Flask(__name__)

@app.route("/profesores")
def ver_profesores():
    profesores = estudiante.listar_profesores()
    return render_template("profesores.html", profesores=profesores)

@app.get("/profesor/<profesor_id>")
def ver_profesor(profesor_id):
    tutorias = estudiante.proximas_tutorias(profesor_id)
    return render_template("profesor.html", profesor_id=profesor_id, tutorias=tutorias)

if __name__ == "__main__":
    app.run(debug=True)
