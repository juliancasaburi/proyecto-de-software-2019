from datetime import datetime

from flask import request, session, abort, make_response, jsonify, render_template
from flaskps.db import get_db

import json

from flaskps.forms.preceptor import forms_preceptor
from flaskps.forms.preceptor.forms_preceptor import PreceptorForm

from flaskps.models.preceptor import Preceptor
from flaskps.models.genero import Genero
from flaskps.models import siteconfig

from flaskps.helpers.localidades import localidades
from flaskps.helpers.tipos_documento import tipos_documento
from flaskps.helpers.permission import has_permission
from flaskps.helpers.role import has_role
from flaskps.models.user import User


def new():
    s_config = siteconfig.get_config()
    if not has_permission("preceptor_new", session) or (
        s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    # Validación - Fill choices
    choices = forms_preceptor.choices()
    form = PreceptorForm(choices)

    op_response = dict()

    if form.validate_on_submit():
        params = request.form.to_dict()
        params["fecha_nacimiento"] = datetime.strptime(
            params["fecha_nacimiento"], "%d/%m/%Y"
        ).date()

        if "username" in params:
            User.db = get_db()
            user = User.find_by_user(params["username"])
            if user:
                params["usuario_id"] = user["id"]

        Preceptor.db = get_db()
        created = Preceptor.create(params)

        if created:
            op_response["msg"] = "Se ha agregado al preceptor exitosamente"
            op_response["type"] = "success"
        else:
            op_response["msg"] = "Ha ocurrido un error al crear al preceptor"
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
    if not has_permission("preceptor_destroy", session) or (
        s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    params = json.loads(request.data)
    d_id = params["id"]
    activo = params["activo"]

    Preceptor.db = get_db()
    success = Preceptor.delete(d_id)

    op_response = dict()

    if success:
        condicion = "bloqueado" if activo else "activado"
        op_response["msg"] = "Se ha " + condicion + " al preceptor exitosamente"
        op_response["type"] = "success"
    else:
        condicion = "bloquear" if activo else "activar"
        op_response["msg"] = "El usuario a " + condicion + " no existe"
        op_response["type"] = "error"
        make_response(jsonify(op_response), 422)

    return make_response(jsonify(op_response), 204)


def data():
    s_config = siteconfig.get_config()
    if not has_permission("preceptor_show", session) or (
        s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    id = request.args.get("id")
    if id:
        Preceptor.db = get_db()
        preceptor = Preceptor.find_by_id(id)

        if preceptor is not None:
            preceptor["fecha_nac"] = datetime.strftime(
                preceptor["fecha_nac"], "%d/%m/%Y"
            )
            usuario_id = preceptor["usuario_id"]
            if usuario_id:
                User.db = get_db()
                user = User.find_by_id(usuario_id)
                preceptor["username"] = user["username"]
            data = jsonify(preceptor)
            return make_response(data, 200)
        else:
            abort(422)
    else:
        abort(400)


def update():
    s_config = siteconfig.get_config()
    if not has_permission("preceptor_update", session) or (
        s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    # Validación - Fill choices
    choices = forms_preceptor.choices()
    form = PreceptorForm(choices)

    op_response = dict()

    if form.validate_on_submit():
        params = request.form.to_dict()

        Preceptor.db = get_db()

        if "username" in params:
            User.db = get_db()
            user = User.find_by_user(params["username"])
            if user:
                params["usuario_id"] = user["id"]

        params["fecha_nacimiento"] = datetime.strptime(
            params["fecha_nacimiento"], "%d/%m/%Y"
        ).date()

        updated = Preceptor.update(params)

        if updated:
            op_response["msg"] = "Se ha modificado al preceptor con éxito"
            op_response["type"] = "success"
        else:
            op_response["msg"] = "Ha ocurrido un error al editar al preceptor"
            op_response["type"] = "error"
            abort(make_response(jsonify(op_response), 422))

    else:
        if len(form.errors) >= 2:
            op_response["msg"] = "Complete todos los datos del preceptor a modificar"
            op_response["type"] = "error"
        else:
            error_msg = "".join(list(form.errors.values())[0]).strip("'[]")
            op_response["msg"] = error_msg
            op_response["type"] = "error"

        abort(make_response(jsonify(op_response), 400))

    return make_response(jsonify(op_response), 200)


def preceptor_table():
    s_config = siteconfig.get_config()
    if not has_permission("preceptor_index", session) or (
        s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    Genero.db = get_db()
    generos = Genero.all()

    return render_template(
        "tables/preceptores.html",
        localidades=localidades(),
        tipodoc=tipos_documento(),
        generos=generos,
    )
