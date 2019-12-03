from flask import render_template

from flaskps.db import get_db
from flaskps.models.ciclo_lectivo import CicloLectivo
from flaskps.models.docente import Docente
from flaskps.models.estudiante import Estudiante


def administracion():

    CicloLectivo.db = get_db()
    ciclos = CicloLectivo.all()

    Docente.db = get_db()
    docentes = Docente.all()

    Estudiante.db = get_db()
    estudiantes = Estudiante.all()

    for ciclo in ciclos:
        ciclo["fecha_ini"] = ciclo["fecha_ini"].strftime("%d-%m-%Y")
        ciclo["fecha_fin"] = ciclo["fecha_fin"].strftime("%d-%m-%Y")

    return render_template(
        "user/moduloadministrativo.html",
        ciclos=ciclos,
        docentes=docentes,
        estudiantes=estudiantes
        #username=user["username"],
    )