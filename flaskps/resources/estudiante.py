from datetime import datetime

from flask import request, session, abort, make_response, jsonify, flash, json
from flaskps.db import get_db

from flaskps.forms.form_estudiante_create import EstudianteCreateForm
from flaskps.helpers.estudiante import pasarChoices

from flaskps.models.estudiante import Estudiante

from flaskps.helpers.permission import has_permission

from flaskps.helpers.tipos_documento import tipo_documento
from flaskps.helpers.localidades import localidad


def get_estudiantes():
    if not has_permission("estudiante_index", session):
        abort(401)

    Estudiante.db = get_db()
    estudiantes = Estudiante.all()

    for dict_item in estudiantes:
        dict_item["ID"] = dict_item["id"]
        del dict_item["id"]
        dict_item["Activo"] = dict_item["activo"]
        del dict_item["activo"]
        dict_item["Nombre"] = dict_item["nombre"]
        del dict_item["nombre"]
        dict_item["Apellido"] = dict_item["apellido"]
        del dict_item["apellido"]
        dict_item["Fecha de nacimiento"] = dict_item["fecha_nac"].strftime("%d-%m-%Y")
        del dict_item["fecha_nac"]
        loc = localidad(dict_item["localidad_id"])
        dict_item["Localidad"] = loc["nombre"]
        del dict_item["localidad_id"]
        dict_item["Domicilio"] = dict_item["domicilio"]
        del dict_item["domicilio"]
        dict_item["Género"] = dict_item["g.nombre"]
        del dict_item["g.nombre"]
        dict_item["Escuela"] = dict_item["es.nombre"]
        del dict_item["es.nombre"]
        dict_item["Barrio"] = dict_item["b.nombre"]
        del dict_item["b.nombre"]
        tipo_doc = tipo_documento(dict_item["tipo_doc_id"])
        dict_item["Tipo de documento"] = tipo_doc["nombre"]
        dict_item["Número de documento"] = dict_item["numero"]
        del dict_item["numero"]
        if dict_item["tel"]:
            dict_item["Número telefónico"] = dict_item["tel"]
        else:
            dict_item["Número telefónico"] = "No tiene"
        del dict_item["tel"]
        dict_item["Nivel"] = dict_item["n.nombre"]
        del dict_item["n.nombre"]
        dict_item["Responsable a cargo"] = dict_item["r.nombre"]
        del dict_item["r.nombre"]

    estudiantes = jsonify(estudiantes)

    return make_response(estudiantes, 200)


def create():
    if not has_permission("estudiante_new", session):
        abort(401)

    form = EstudianteCreateForm()
    form = pasarChoices(form)

    op_response = dict()
    responsecode = 201

    if form.validate_on_submit():
        params = request.form.to_dict()
        params["fecha_nacimiento"] = datetime.strptime(
            params["fecha_nacimiento"], "%d/%m/%Y"
        ).date()

        Estudiante.db = get_db()
        created = Estudiante.create(params)

        if created:
            op_response["msg"] = "Se ha agregado al estudiante exitosamente"
            op_response["type"] = "success"
        else:
            op_response["msg"] = "Ha ocurrido un error al crear al estudiante"
            op_response["type"] = "error"
            abort(make_response(jsonify(op_response), 409))

    else:
        if len(form.errors) >= 2:
            op_response["msg"] = "Complete todos los datos del nuevo estudiante"
            op_response["type"] = "error"
        else:
            error_msg = "".join(list(form.errors.values())[0]).strip("'[]")
            op_response["msg"] = error_msg
            op_response["type"] = "error"

        abort(make_response(jsonify(op_response), 500))

    return make_response(jsonify(op_response), responsecode)


def update():
    if not has_permission("estudiante_update", session):
        abort(401)

    form = EstudianteCreateForm()  # uso este porq es igual
    form = pasarChoices(form)

    op_response = dict()
    responsecode = 201

    if form.validate_on_submit():
        params = request.form.to_dict()
        params["fecha_nacimiento"] = datetime.strptime(
            params["fecha_nacimiento"], "%d/%m/%Y"
        ).date()

        Estudiante.db = get_db()

        updated = Estudiante.update(params)

        if updated:
            op_response["msg"] = "Se ha modificado al estudiante con éxito"
            op_response["type"] = "success"
        else:
            op_response["msg"] = "Ocurrió un error"
            op_response["type"] = "error"
            abort(make_response(jsonify(op_response), 409))

    else:
        if len(form.errors) >= 2:
            error_msg = "".join(form.errors)
            op_response["msg"] = error_msg
            #op_response["msg"] = "Complete todos los datos del estudiante a modificar"
            op_response["type"] = "error"
        else:
            error_msg = "".join(list(form.errors.values())[0]).strip("'[]")
            op_response["msg"] = error_msg
            op_response["type"] = "error"

        abort(make_response(jsonify(op_response), 500))

    return make_response(jsonify(op_response), responsecode)


def destroy():
    if not has_permission("estudiante_destroy", session):
        abort(401)

    params = json.loads(request.data)
    eid = params["id"]

    Estudiante.db = get_db()
    success = Estudiante.delete(eid)

    op_response = dict()
    responsecode = 200

    if success:
        op_response["msg"] = "Se ha bloqueado/activado al estudiante exitosamente"
        op_response["type"] = "success"
    else:
        op_response["msg"] = "El estudiante a bloquear/activar no existe"
        op_response["type"] = "error"
        responsecode = 404

    return make_response(jsonify(op_response), responsecode)


# por id
def estudiante_data():
    if not has_permission("estudiante_index", session):
        abort(401)

    if request.args.get("id"):
        Estudiante.db = get_db()
        eid = request.args.get("id")
        estudiante = Estudiante.find_by_id(eid)
        if estudiante != None:
            data = jsonify(estudiante)
            return make_response(data, 200)
        else:
            flash("El estudiante con ID:" + eid + "no existe.", "error")
            return abort(404)

    else:
        abort(400)
