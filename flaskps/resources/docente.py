from datetime import datetime

from flask import request, session, abort, make_response, jsonify, render_template
from flaskps.db import get_db

import json

from flaskps.forms.docente.form_docente_create import DocenteCreateForm
from flaskps.forms.docente.form_docente_update import DocenteUpdateForm

from flaskps.models.docente import Docente
from flaskps.models.genero import Genero
from flaskps.models import siteconfig

from flaskps.helpers.localidades import localidad, localidades
from flaskps.helpers.tipos_documento import tipo_documento, tipos_documento
from flaskps.helpers.permission import has_permission
from flaskps.helpers.role import has_role

from flaskps.resources.helpers.serverside_dt.serverside_table_docentes import (
    DocentesServerSideTable,
)
from flaskps.resources.helpers.serverside_dt import table_schemas


def docentes():
    Docente.db = get_db()
    docentes = Docente.all()

    for dict_item in docentes:
        dict_item["fecha_nacimiento"] = dict_item["fecha_nac"].strftime("%d-%m-%Y")
        del dict_item["fecha_nac"]
        loc = localidad(dict_item["localidad_id"])
        dict_item["localidad"] = loc["nombre"]
        del dict_item["localidad_id"]
        Genero.db = get_db()
        dict_item["genero"] = Genero.find_by_id(dict_item["genero_id"])[0]["nombre"]
        del dict_item["genero_id"]
        tipo_doc = tipo_documento(dict_item["tipo_doc_id"])
        dict_item["tipo_documento"] = tipo_doc["nombre"]
        del dict_item["tipo_doc_id"]
        dict_item["created_at"] = dict_item["created_at"].strftime("%d-%m-%Y %H:%M:%S")
        dict_item["updated_at"] = dict_item["updated_at"].strftime("%d-%m-%Y %H:%M:%S")

    return docentes


def get_docentes():
    s_config = siteconfig.get_config()
    if not has_permission("docente_index", session) or (
        s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
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
    s_config = siteconfig.get_config()
    if not has_permission("docente_new", session) or (
        s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
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
    s_config = siteconfig.get_config()
    if not has_permission("docente_destroy", session) or (
        s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    params = json.loads(request.data)
    d_id = params["id"]
    activo = params["activo"]

    Docente.db = get_db()
    success = Docente.delete(d_id)

    op_response = dict()
    responsecode = 200

    if success:
        condicion = "bloqueado" if activo else "activado"
        op_response["msg"] = "Se ha " + condicion + " al docente exitosamente"
        op_response["type"] = "success"
    else:
        condicion = "bloquear" if activo else "activar"
        op_response["msg"] = "El usuario a " + condicion + " no existe"
        op_response["type"] = "error"
        responsecode = 404

    return make_response(jsonify(op_response), responsecode)


def data():
    s_config = siteconfig.get_config()
    if not has_permission("docente_show", session) or (
        s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    Docente.db = get_db()
    d_id = request.args.get("id")
    docente = Docente.find_by_id(d_id)
    if docente != None:
        docente["fecha_nac"] = datetime.strftime(docente["fecha_nac"], "%d/%m/%Y")
        data = jsonify(docente)
        return make_response(data, 200)
    else:
        return abort(404)


def update():
    s_config = siteconfig.get_config()
    if not has_permission("docente_update", session) or (
        s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    form = DocenteUpdateForm()

    op_response = dict()
    responsecode = 201

    if form.validate_on_submit():
        params = request.form.to_dict()

        Docente.db = get_db()

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
            abort(make_response(jsonify(op_response), 409))

    else:
        if len(form.errors) >= 2:
            op_response["msg"] = "Complete todos los datos del usuario a modificar"
            op_response["type"] = "error"
        else:
            error_msg = "".join(list(form.errors.values())[0]).strip("'[]")
            op_response["msg"] = error_msg
            op_response["type"] = "error"

        abort(make_response(jsonify(op_response), 500))

    return make_response(jsonify(op_response), responsecode)


def docente_table():
    if not has_permission("docente_index", session):
        abort(401)

    Genero.db = get_db()
    generos = Genero.all()

    return render_template(
        "tables/docentes.html",
        localidades=localidades(),
        tipodoc=tipos_documento(),
        generos=generos,
    )
