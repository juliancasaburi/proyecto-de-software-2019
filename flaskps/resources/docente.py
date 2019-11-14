from flask import (
    request,
    session,
    abort,
    make_response,
    jsonify,
)
from flaskps.db import get_db

from flaskps.forms.form_docente_create import DocenteCreateForm

from flaskps.models.docente import Docente
from flaskps.models.genero import Genero

from flaskps.helpers.permission import has_permission
from flaskps.helpers.localidades import localidades
from flaskps.helpers.tipos_documento import tipos_documento


def get_docentes():
    if not has_permission("docente_index", session):
        abort(401)

    Docente.db = get_db()
    docentes = Docente.all()

    for dict_item in docentes:
        dict_item["ID"] = dict_item["id"]
        del dict_item["id"]
        dict_item["Nombre"] = dict_item["nombre"]
        del dict_item["nombre"]
        dict_item["Apellido"] = dict_item["apellido"]
        del dict_item["apellido"]
        dict_item["Fecha de nacimiento"] = dict_item["fecha_nac"]
        del dict_item["fecha_nac"]
        locs = localidades()
        dict_item["Localidad"] = locs[dict_item["localidad_id"]]["nombre"]
        del dict_item["localidad_id"]
        dict_item["Domicilio"] = dict_item["domicilio"]
        del dict_item["domicilio"]
        Genero.db = get_db()
        dict_item["Genero"] = Genero.find_by_id(dict_item["ID"])[0]["nombre"]
        del dict_item["genero_id"]
        tipos_doc = tipos_documento()
        dict_item["Tipo de documento"] = tipos_doc[dict_item["tipo_doc_id"]]["nombre"]
        del dict_item["tipo_doc_id"]
        dict_item["Numero de documento"] = dict_item["numero"]
        del dict_item["numero"]
        dict_item["Numero telefónico"] = dict_item["tel"]
        del dict_item["tel"]

    docentes = jsonify(docentes)

    return make_response(docentes, 200)


def create():
    if not has_permission("docente_new", session):
        abort(401)

    form = DocenteCreateForm()

    op_response = dict()
    responsecode = 201

    if form.validate_on_submit():
        params = request.form.to_dict()

        Docente.db = get_db()
        created = Docente.create(params)

        if created:
            op_response["msg"] = "Se ha agregado al Docente exitosamente"
            op_response["type"] = "success"
        else:
            op_response["msg"] = "Ha ocurrido un error al crear al Docente"
            op_response["type"] = "error"
            abort(make_response(jsonify(op_response), 409))

    else:
        if len(form.errors) >= 2:
            op_response["msg"] = "Complete todos los datos del nuevo docente"
            op_response["type"] = "error"
        else:
            error_msg = "".join(list(form.errors.values())[0]).strip("'[]")
            op_response["msg"] = error_msg
            op_response["type"] = "error"

        abort(make_response(jsonify(op_response), 500))

    return make_response(jsonify(op_response), responsecode)
