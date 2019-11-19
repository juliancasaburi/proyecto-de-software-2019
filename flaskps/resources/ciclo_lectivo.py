from datetime import datetime

from flask import (
    request,
    session,
    abort,
    make_response,
    jsonify,
)
from flaskps.db import get_db
from flaskps.forms.form_ciclo_create import CicloCreateForm

from flaskps.models.ciclo_lectivo import CicloLectivo

from flaskps.helpers.permission import has_permission


def create():
    if not has_permission("ciclolectivo_new", session):
        abort(401)

    form = CicloCreateForm()

    op_response = dict()
    responsecode = 201

    if form.validate_on_submit():
        params = request.form.to_dict()

        params["fecha_inicio"] = datetime.strptime(
            params["fecha_inicio"], "%d/%m/%Y"
        ).date()

        params["fecha_fin"] = datetime.strptime(
            params["fecha_fin"], "%d/%m/%Y"
        ).date()

        fecha_ini = params["fecha_inicio"]
        fecha_fin = params["fecha_fin"]

        if fecha_fin <= fecha_ini:
            op_response[
                "msg"
            ] = "La fecha de finalización es menor o igual a la fecha de inicio"
            op_response["type"] = "error"
            abort(make_response(jsonify(op_response), 400))

        CicloLectivo.db = get_db()
        created = CicloLectivo.create(params)

        if created:
            op_response["msg"] = "Se ha agregado el ciclo lectivo exitosamente"
            op_response["type"] = "success"
        else:
            op_response["msg"] = "Ha ocurrido un error al crear el ciclo lectivo"
            op_response["type"] = "error"
            abort(make_response(jsonify(op_response), 409))

    else:
        if len(form.errors) >= 2:
            op_response["msg"] = "Complete todos los datos del ciclo lectivo"
            op_response["type"] = "error"
        else:
            error_msg = "".join(list(form.errors.values())[0]).strip("'[]")
            op_response["msg"] = error_msg
            op_response["type"] = "error"

        abort(make_response(jsonify(op_response), 500))

    return make_response(jsonify(op_response), responsecode)


def get_ciclos():
    if not has_permission("ciclolectivo_index", session):
        abort(401)

    CicloLectivo.db = get_db()
    ciclos = CicloLectivo.all()

    for ciclo in ciclos:
        ciclo["fecha_ini"] = ciclo["fecha_ini"].strftime("%d-%m-%Y")
        ciclo["fecha_fin"] = ciclo["fecha_fin"].strftime("%d-%m-%Y")

    for dict_item in ciclos:
        dict_item["ID"] = dict_item["id"]
        del dict_item["id"]
        dict_item["Fecha de inicio"] = dict_item["fecha_ini"]
        del dict_item["fecha_ini"]
        dict_item["Fecha de fin"] = dict_item["fecha_fin"]
        del dict_item["fecha_fin"]
        dict_item["Semestre"] = dict_item["semestre"]
        del dict_item["semestre"]

    ciclos = jsonify(ciclos)

    return make_response(ciclos, 200)


def get_talleres():
    c_id = request.args.get("id")
    CicloLectivo.db = get_db()
    talleres = CicloLectivo.talleres(c_id)

    if talleres is None:
        abort(404)

    return make_response(jsonify(talleres), 200)
