# Sistema de tutorías

**Fundamentos de Programación · Ingeniería de Software · UDES**
Autores: Juan Rosas y Juan Diego
Tecnologías: Python, Flask, HTML/CSS, JSON

Documentos relacionados: [Diagramas de flujo](DIAGRAMAS_DE_FLUJO.md) · [Pseudocódigo por función](PSEUDOCODIGO.md)

---

## 1. Qué es

Aplicación web donde los **estudiantes** se apuntan a tutorías ofrecidas por **profesores**. Cada profesor define horarios semanales fijos (día, hora, lugar). El estudiante ve las tutorías de los próximos 7 días, se apunta con una nota que describe qué quiere repasar, y puede editarla o cancelar.

Los datos se guardan en archivos JSON, organizados como las tablas de una base de datos relacional. No hay cupos: pueden apuntarse todos los estudiantes que quieran.

## 2. Historias de usuario

| Rol | Quiero... | Operación |
|---|---|---|
| Estudiante | Ver los profesores y sus tutorías de los próximos 7 días | Leer |
| Estudiante | Apuntarme a una tutoría con una nota | Crear |
| Estudiante | Ver mis tutorías próximas | Leer |
| Estudiante | Editar la nota de una inscripción | Actualizar |
| Estudiante | Cancelar una inscripción | Eliminar |
| Profesor | Ver mis horarios y los estudiantes inscritos | Leer |
| Profesor | Crear un horario semanal | Crear |
| Profesor | Editar un horario | Actualizar |
| Profesor | Eliminar un horario | Eliminar |

## 3. Reglas del sistema

| Regla | Valor | Módulo |
|---|---|---|
| Ventana para apuntarse | próximos 7 días | estudiantes |
| Anticipación mínima para cancelar | 3 días | estudiantes |
| Inscripción repetida a la misma tutoría | no permitida | estudiantes |
| Dos tutorías el mismo día a la misma hora | no permitido | estudiantes |
| Largo máximo de la nota | 200 caracteres | estudiantes |
| Editar la nota de una tutoría que ya pasó | no permitido | estudiantes |
| Cada estudiante solo toca sus inscripciones | siempre | estudiantes |
| Formato de hora | HH:MM | profesores |
| Día de la semana | Lunes a Domingo | profesores |
| Largo máximo del lugar | 40 caracteres | profesores |
| Dos horarios del mismo profesor a la misma hora y día | no permitido | profesores |
| Horario con inscritos a futuro | solo se puede cambiar el lugar; no se puede eliminar | profesores |
| Cada profesor solo toca sus horarios | siempre | profesores |
| Eliminar un horario | borra también sus inscripciones viejas (cascada) | profesores |

El usuario siempre se toma de la sesión, nunca de un formulario, para que nadie pueda actuar como otro.

## 4. Datos

Cuatro archivos en `storage/`. Las relaciones se hacen por `id`.

| Archivo | Campos |
|---|---|
| `estudiantes.json` | id, nombre |
| `profesores.json` | id, nombre, materia |
| `horarios.json` | id, profesor_id, dia, hora, lugar |
| `inscripciones.json` | id, estudiante_id, horario_id, fecha, nota |

Una **tutoría** (un horario en una fecha concreta) no se guarda: se calcula en el momento a partir de los horarios y los próximos 7 días. Lo único que se guarda es la inscripción, con el horario y la fecha.

Los ids nuevos se calculan como el mayor existente más uno.

## 5. Estructura del proyecto

```
tutoriasPA/
├── app.py                  # rutas de Flask
├── probar.py               # pruebas de la lógica
├── reiniciar_demo.py       # deja inscripciones de ejemplo para la demo
├── requirements.txt
├── modules/
│   ├── utils.py            # constantes, lectura/escritura de JSON, fechas
│   ├── estudiantes.py      # lógica del estudiante
│   └── profesores.py       # lógica del profesor
├── storage/                # los cuatro JSON
├── templates/              # páginas HTML (Jinja)
└── static/estilos.css
```

**Separación de responsabilidades**

- `modules/` contiene toda la lógica. No usa `input()` ni `print()`: cada acción recibe datos y devuelve `(ok, mensaje)`.
- `app.py` solo recibe las peticiones web, llama a la lógica y muestra el mensaje con `flash`.
- `templates/` solo muestra datos.
- La hora actual se obtiene en una sola función (`fecha_hora_actual`) para poder simular fechas en las pruebas.

## 6. Diagramas de flujo y pseudocódigo

- [Diagramas de flujo](DIAGRAMAS_DE_FLUJO.md): flujo general, apuntarse, cancelar, crear, editar y eliminar horario.
- [Pseudocódigo por función](PSEUDOCODIGO.md): las 24 funciones de `utils`, `estudiantes` y `profesores`.

## 7. Pruebas

`probar.py` ejecuta **45 verificaciones** sobre una copia temporal de los datos y con un reloj simulado (domingo 8 de noviembre de 2026, 09:00), así que no dependen de los datos guardados ni de la fecha real.

| Grupo | Pruebas |
|---|---|
| Consultas | 5 |
| Nota | 6 |
| Apuntarse | 9 |
| Cancelar | 4 |
| Horarios del profesor | 12 |
| Editar y eliminar horario | 7 |
| Casos límite | 2 |

## 8. Cómo ejecutarlo

```bash
python -m venv venv
source venv/bin/activate        # en Windows: venv\Scripts\activate
pip install -r requirements.txt
python reiniciar_demo.py        # opcional: inscripciones de ejemplo en fechas próximas
python app.py
```

Abrir `http://127.0.0.1:5001`. Si el puerto está ocupado, cambiarlo en la última línea de `app.py`.

Para correr las pruebas: `python probar.py`.

**Usuarios de ejemplo:** estudiantes Ana, Luis y Camila; cinco profesores con sus materias. Se elige el rol y el usuario en la página de inicio (no hay contraseñas).

## 9. Decisiones y mejoras futuras

**Decisiones**

- Horarios semanales fijos y tutorías calculadas, en lugar de guardar cada fecha: menos datos y sin tener que renovarlos.
- Varios JSON relacionados por id, como una base de datos, para que migrar a una real sea directo.
- Código de nivel de fundamentos: ciclos, condicionales y funciones simples, sin trucos del lenguaje.
- Sin autenticación: el alcance es la lógica del sistema.

**Mejoras futuras**

- Inicio de sesión con contraseña.
- Cupos máximos por tutoría.
- Base de datos (SQLite) en lugar de JSON.
- Avisos por correo de inscripciones y cancelaciones.
- Que el profesor pueda cancelar una tutoría puntual avisando a los inscritos.
