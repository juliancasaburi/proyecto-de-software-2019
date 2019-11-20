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

from flaskps.serverside_dt.serverside_table_docentes import DocentesServerSideTable
from flaskps.serverside_dt import table_schemas


def docentes():
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
        dict_item["Creado"] = dict_item["created_at"].strftime("%d-%m-%Y %H:%M:%S")
        del dict_item["created_at"]
        dict_item["Actualizado"] = dict_item["updated_at"].strftime("%d-%m-%Y %H:%M:%S")
        del dict_item["updated_at"]

    return docentes


def get_docentes():
    if not has_permission("docente_index", session):
        abort(401)

    all_docentes = jsonify(docentes())

    return make_response(all_docentes, 200)


def collect_data_serverside(req):
    columns = table_schemas.SERVERSIDE_DOCENTES_TABLE_COLUMNS

    return DocentesServerSideTable(req, docentes(), columns).output_result()


def serverside_table_content():
    if not has_permission("docente_index", session):
        abort(401)

    data = collect_data_serverside(request)
    return jsonify(data)


def create():
    if not has_permission("docente_new", session):
        abort(401)

    # Validación - Fill choices
    form = DocenteCreateForm()

    Genero.db = get_db()
    generos = Genero.all()

    form.select_genero.choices = [(g["id"], g["nombre"]) for g in generos]

    locs = localidades()
    form.select_localidad.choices = [(l["id"], l["nombre"]) for l in locs]

    tipos = tipos_documento()
    form.select_tipo.choices = [(t["id"], t["nombre"]) for t in tipos]

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
    activo = params["activo"]

    Docente.db = get_db()
    success = Docente.delete(d_id)

    op_response = dict()
    responsecode = 200

    if success:
        condicion = 'bloqueado' if activo else 'activado'
        op_response["msg"] = "Se ha " + condicion + " al docente exitosamente"
        op_response["type"] = "success"
    else:
        condicion = 'bloquear' if activo else 'activar'
        op_response["msg"] = "El usuario a " + condicion + " no existe"
        op_response["type"] = "error"
        responsecode = 404

    return make_response(jsonify(op_response), responsecode)


def data():
    if not has_permission("docente_show", session):
        abort(401)

    Docente.db = get_db()
    d_id = request.args.get("id")
    docente = Docente.find_by_id(d_id)
    if docente != None:
        data = jsonify(docente)
        return make_response(data, 200)
    else:
        return abort(404)
