from datetime import datetime

from flask import request, session, abort, make_response, jsonify, render_template
from flaskps.db import get_db

from flaskps.forms.ciclo.form_ciclo_create import CicloCreateForm

from flaskps.models import siteconfig
from flaskps.models.ciclo_lectivo import CicloLectivo

from flaskps.helpers.permission import has_permission
from flaskps.helpers.role import has_role


def create():
    s_config = siteconfig.get_config()
    if not has_permission("ciclolectivo_new", session) or (
        s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    form = CicloCreateForm()

    op_response = dict()

    if form.validate_on_submit():
        params = request.form.to_dict()

        params["fecha_inicio"] = datetime.strptime(
            params["fecha_inicio"], "%d/%m/%Y"
        ).date()

        params["fecha_fin"] = datetime.strptime(params["fecha_fin"], "%d/%m/%Y").date()

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
            abort(make_response(jsonify(op_response), 422))

    else:
        if len(form.errors) >= 2:
            op_response["msg"] = "Complete todos los datos del ciclo lectivo"
            op_response["type"] = "error"
        else:
            error_msg = "".join(list(form.errors.values())[0]).strip("'[]")
            op_response["msg"] = error_msg
            op_response["type"] = "error"

        abort(make_response(jsonify(op_response), 400))

    return make_response(jsonify(op_response), 201)


def get_ciclos():
    s_config = siteconfig.get_config()
    if not has_permission("ciclolectivo_index", session) or (
        s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    CicloLectivo.db = get_db()
    ciclos = CicloLectivo.all()

    for dict_item in ciclos:
        dict_item["fecha_ini"] = dict_item["fecha_ini"].strftime("%d-%m-%Y")
        dict_item["fecha_fin"] = dict_item["fecha_fin"].strftime("%d-%m-%Y")

    ciclos = jsonify(ciclos)

    return make_response(ciclos, 200)


def destroy():
    s_config = siteconfig.get_config()
    if not has_permission("ciclolectivo_destroy", session) or (
        s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    params = request.form.to_dict()
    cid = params["id"]

    CicloLectivo.db = get_db()
    success = CicloLectivo.destroy(cid)

    op_response = dict()

    if success:
        op_response["msg"] = "Se ha eliminado al el ciclo lectivo exitosamente"
        op_response["type"] = "success"
    else:
        op_response["msg"] = "El ciclo lectivo esta actualmente en uso!"
        op_response["type"] = "error"
        abort(make_response(jsonify(op_response), 422))

    return make_response(jsonify(op_response), 204)


def get_talleres():
    s_config = siteconfig.get_config()
    if not has_permission("ciclolectivo_index", session) or (
        s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    c_id = request.args.get("id")
    CicloLectivo.db = get_db()
    talleres = CicloLectivo.talleres(c_id)

    if talleres is None:
        abort(404)

    return make_response(jsonify(talleres), 200)


def ciclo_table():
    s_config = siteconfig.get_config()
    if not has_permission("ciclolectivo_index", session) or (
            s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    CicloLectivo.db = get_db()
    ciclos = CicloLectivo.all()

    for ciclo in ciclos:
        ciclo["fecha_ini"] = ciclo["fecha_ini"].strftime("%d-%m-%Y")
        ciclo["fecha_fin"] = ciclo["fecha_fin"].strftime("%d-%m-%Y")

    return render_template("tables/ciclos.html", ciclos=ciclos)
