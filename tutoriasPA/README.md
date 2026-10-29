# Sistema de tutorías (CRUD)

Python + Flask + HTML/CSS. La lógica está en `logica.py` y Flask (`app.py`) solo recibe los clics y la llama.

Cada profesor tiene horarios fijos que se repiten cada semana. El estudiante se apunta a una fecha concreta (sin cupo máximo) y deja una nota con el tema.

## Cómo correrlo

```bash
cd tutorias
pip install -r requirements.txt
python app.py
```

Abre http://127.0.0.1:5000 y entra como estudiante (Ana, Luis, Camila) o como profesor (datos de prueba, sin contraseña).

## CRUD

| | Estudiante | Profesor |
|---|---|---|
| Create | `apuntarse` | `crear_horario` |
| Read | `proximas_tutorias`, `mis_tutorias` | `horarios_de`, `ver_inscritos` |
| Update | `editar_nota` | `editar_horario` |
| Delete | `cancelar` | `eliminar_horario` |

## Validaciones

- Cancelar solo con 3 días o más de anticipación.
- Apuntarse solo a los próximos 7 días, a una fecha que no haya pasado.
- No apuntarse dos veces a la misma tutoría ni a dos tutorías a la misma hora.
- La nota y el lugar tienen un largo máximo.
- El profesor no puede eliminar ni cambiar el día u hora de un horario con estudiantes apuntados.

## Contrato de `logica.py`

Sin `input()` ni `print()`. Las acciones devuelven `(ok, mensaje)`.

Consultas: `estudiantes()`, `materias()`, `obtener_profesor(pid)`, `listar_profesores(materia)`, `proximas_tutorias(pid, estudiante)`, `proximas_global(limite)`, `mis_tutorias(estudiante)`, `horarios_de(pid)`, `ver_inscritos(pid)`.

Acciones: `apuntarse(estudiante, pid, horario, fecha, nota)`, `editar_nota(estudiante, inscripcion, nota)`, `cancelar(estudiante, inscripcion)`, `crear_horario(pid, dia, hora, lugar)`, `editar_horario(pid, horario, dia, hora, lugar)`, `eliminar_horario(pid, horario)`.

## Datos (`datos.json`)

- `estudiantes`: lista de nombres.
- `profesores`: por id, con `nombre`, `materia` y `horarios` (`id`, `dia`, `hora`, `lugar`).
- `inscripciones`: `id`, `estudiante`, `profesor`, `horario`, `fecha` (`AAAA-MM-DD`), `hora` y `nota`.

## Nota sobre las fechas de prueba

Los horarios fijos no caducan, pero las inscripciones de ejemplo van del 29 de octubre al 3 de noviembre de 2026. Después de esa fecha dejan de aparecer.
