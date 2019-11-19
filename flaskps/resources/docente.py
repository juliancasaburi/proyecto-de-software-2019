from datetime import datetime

from flask import (
    request,
    session,
    abort,
    make_response,
    jsonify,
)
from flaskps.db import get_db

import json

from flaskps.forms.form_docente_create import DocenteCreateForm

from flaskps.models.docente import Docente
from flaskps.models.genero import Genero

from flaskps.helpers.permission import has_permission
from flaskps.helpers.localidades import localidad, localidades
from flaskps.helpers.tipos_documento import tipo_documento, tipos_documento


def get_docentes():
    if not has_permission("docente_index", session):
        abort(401)

    Docente.db = get_db()
    docentes = Docente.all()

    for dict_item in docentes:
        dict_item["fecha de nacimiento"] = dict_item["fecha_nac"].strftime("%d-%m-%Y")
        del dict_item["fecha_nac"]
        loc = localidad(dict_item["localidad_id"])
        dict_item["localidad"] = loc["nombre"]
        del dict_item["localidad_id"]
        Genero.db = get_db()
        dict_item["genero"] = Genero.find_by_id(dict_item["genero_id"])[0]["nombre"]
        del dict_item["genero_id"]
        tipo_doc = tipo_documento(dict_item["tipo_doc_id"])
        dict_item["tipo de documento"] = tipo_doc["nombre"]
        del dict_item["tipo_doc_id"]

    docentes = jsonify(docentes)

    return make_response(docentes, 200)


def create():
    if not has_permission("docente_new", session):
        abort(401)

    # Validación - Fill choices
    form = DocenteCreateForm()

    Genero.db = get_db()
    generos = Genero.all()

    form.select_genero.choices = [(g['id'], g['nombre']) for g in generos]

    locs = localidades()
    form.select_localidad.choices = [(l['id'], l['nombre']) for l in locs]

    tipos = tipos_documento()
    form.select_tipo.choices = [(t['id'], t['nombre']) for t in tipos]

    op_response = dict()
    responsecode = 201

    if form.validate_on_submit():
        params = request.form.to_dict()
        params["fecha_nacimiento"] = datetime.strptime(
            params["fecha_nacimiento"], "%d/%m/%Y"
        ).date()

        Docente.db = get_db()
        created = Docente.create(params)

        if created:
            op_response["msg"] = "Se ha agregado al docente exitosamente"
            op_response["type"] = "success"
        else:
            op_response["msg"] = "Ha ocurrido un error al crear al docente"
            op_response["type"] = "error"
            abort(make_response(jsonify(op_response), 409))

    else:
        error_msg = "".join(list(form.errors.values())[0]).strip("'[]")
        op_response["msg"] = error_msg
        op_response["type"] = "error"
        abort(make_response(jsonify(op_response), 500))

    return make_response(jsonify(op_response), responsecode)


def destroy():
    if not has_permission("docente_destroy", session):
        abort(401)

    params = json.loads(request.data)
    d_id = params["id"]

    Docente.db = get_db()
    success = Docente.delete(d_id)

    op_response = dict()
    responsecode = 200

    if success:
        op_response["msg"] = "Se ha bloqueado/activado al docente exitosamente"
        op_response["type"] = "success"
    else:
        op_response["msg"] = "El usuario a bloquear/activar no existe"
        op_response["type"] = "error"
        responsecode = 404

    return make_response(jsonify(op_response), responsecode)


def data():
    if not has_permission("docente_index", session):
        abort(401)

    Docente.db = get_db()
    d_id = request.args.get("id")
    docente = Docente.find_by_id(d_id)
    if docente != None:
        data = jsonify(docente)
        return make_response(data, 200)
    else:
        return abort(404)
