from flask import render_template

from flaskps.db import get_db
from flaskps.models.ciclo_lectivo import CicloLectivo


def administracion():
    CicloLectivo.db = get_db()
    ciclos = CicloLectivo.all()

    for ciclo in ciclos:
        ciclo["fecha_ini"] = ciclo["fecha_ini"].strftime("%d-%m-%Y")
        ciclo["fecha_fin"] = ciclo["fecha_fin"].strftime("%d-%m-%Y")

    return render_template(
        "user/moduloadministrativo.html",
        ciclos=ciclos
        #username=user["username"],
    )