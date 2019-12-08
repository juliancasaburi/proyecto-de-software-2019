from flask import render_template

from flaskps.models.ciclo_lectivo import CicloLectivo
from flaskps.models.docente import Docente
from flaskps.models.estudiante import Estudiante


def administracion():

    ciclos = CicloLectivo.all()

    docentes = Docente.all()

    estudiantes = Estudiante.all()

    for ciclo in ciclos:
        ciclo["fecha_ini"] = ciclo["fecha_ini"].strftime("%d-%m-%Y")
        ciclo["fecha_fin"] = ciclo["fecha_fin"].strftime("%d-%m-%Y")

    return render_template(
        "user/moduloadministrativo.html",
        ciclos=ciclos,
        docentes=docentes,
        estudiantes=estudiantes
        # username=user["username"],
    )
