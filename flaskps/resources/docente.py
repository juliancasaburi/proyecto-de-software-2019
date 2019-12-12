import json
from datetime import datetime

from flask import request, session, abort, make_response, jsonify, render_template

from flaskps.forms.docente import forms_docente
from flaskps.forms.docente.forms_docente import DocenteForm
from flaskps.helpers.localidades import localidades
from flaskps.helpers.permission import has_permission
from flaskps.helpers.role import has_role
from flaskps.helpers.tipos_documento import tipos_documento
from flaskps.models import siteconfig
from flaskps.models.docente import Docente
from flaskps.models.genero import Genero
from flaskps.models.user import User


def new():
    s_config = siteconfig.get_config()
    if not has_permission("docente_new", session) or (
        s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    # Validación - Fill choices
    choices = forms_docente.choices()
    form = DocenteForm(choices)

    op_response = dict()

    if form.validate_on_submit():
        params = request.form.to_dict()
        params["fecha_nacimiento"] = datetime.strptime(
            params["fecha_nacimiento"], "%d/%m/%Y"
        ).date()

        if "username" in params:
            user = User.find_by_user(params["username"])
            if user:
                params["usuario_id"] = user["id"]

        created = Docente.create(params)

        if created:
            op_response["msg"] = "Se ha agregado al docente exitosamente"
            op_response["type"] = "success"
        else:
            op_response["msg"] = "Ha ocurrido un error al crear al docente"
            op_response["type"] = "error"
            abort(make_response(jsonify(op_response), 422))

    else:
        error_msg = "".join(list(form.errors.values())[0]).strip("'[]")
        op_response["msg"] = error_msg
        op_response["type"] = "error"
        abort(make_response(jsonify(op_response), 400))

    return make_response(jsonify(op_response), 201)


def destroy():
    s_config = siteconfig.get_config()
    if not has_permission("docente_destroy", session) or (
        s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    params = json.loads(request.data)
    d_id = params["id"]
    activo = params["activo"]

    success = Docente.delete(d_id)

    op_response = dict()

    if success:
        condicion = "bloqueado" if activo else "activado"
        op_response["msg"] = "Se ha " + condicion + " al docente exitosamente"
        op_response["type"] = "success"
    else:
        condicion = "bloquear" if activo else "activar"
        op_response["msg"] = "El docente a " + condicion + " no existe"
        op_response["type"] = "error"
        make_response(jsonify(op_response), 422)

    return make_response(jsonify(op_response), 204)


def data():
    s_config = siteconfig.get_config()
    if not has_permission("docente_show", session) or (
        s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    id = request.args.get("id")
    if id:

        docente = Docente.find_by_id(id)

        if docente is not None:
            docente["fecha_nac"] = datetime.strftime(docente["fecha_nac"], "%d/%m/%Y")
            usuario_id = docente["usuario_id"]
            if usuario_id:

                user = User.find_by_id(usuario_id)
                docente["username"] = user["username"]
            data = jsonify(docente)
            return make_response(data, 200)
        else:
            abort(422)
    else:
        abort(400)


def update():
    s_config = siteconfig.get_config()
    if not has_permission("docente_update", session) or (
        s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    # Validación - Fill choices
    choices = forms_docente.choices()
    form = DocenteForm(choices)

    op_response = dict()

    if form.validate_on_submit():
        params = request.form.to_dict()

        if "username" in params:

            user = User.find_by_user(params["username"])
            if user:
                params["usuario_id"] = user["id"]

        params["fecha_nacimiento"] = datetime.strptime(
            params["fecha_nacimiento"], "%d/%m/%Y"
        ).date()

        updated = Docente.update(params)

        if updated:
            op_response["msg"] = "Se ha modificado al docente con éxito"
            op_response["type"] = "success"
        else:
            op_response["msg"] = "Ha ocurrido un error al editar al docente"
            op_response["type"] = "error"
            abort(make_response(jsonify(op_response), 422))

    else:
        if len(form.errors) >= 2:
            op_response["msg"] = "Complete todos los datos del docente a modificar"
            op_response["type"] = "error"
        else:
            error_msg = "".join(list(form.errors.values())[0]).strip("'[]")
            op_response["msg"] = error_msg
            op_response["type"] = "error"

        abort(make_response(jsonify(op_response), 400))

    return make_response(jsonify(op_response), 200)


def docente_table():
    s_config = siteconfig.get_config()
    if not has_permission("docente_index", session) or (
        s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    generos = Genero.all()

    return render_template(
        "tables/docentes.html",
        localidades=localidades(),
        tipodoc=tipos_documento(),
        generos=generos,
    )


