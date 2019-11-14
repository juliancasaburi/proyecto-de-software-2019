from datetime import datetime

import requests
from flask import (
    request,
    session,
    abort,
    make_response,
    jsonify,
    )
from flaskps.db import get_db

from flaskps.forms.form_estudiante_create import EstudianteCreateForm
from flaskps.models.barrio import Barrio
from flaskps.models.escuela import Escuela

from flaskps.models.estudiante import Estudiante

from flaskps.helpers.permission import has_permission

from flaskps.helpers.tipos_documento import tipos_documento
from flaskps.helpers.localidades import localidades
from flaskps.models.genero import Genero
from flaskps.models.nivel import Nivel


def get_estudiantes():
    if not has_permission("estudiante_index", session):
        abort(401)

    Estudiante.db = get_db()
    estudiantes = Estudiante.all()

    tipo_doc = tipos_documento()
    locs = localidades()

    for dict_item in estudiantes:
        dict_item["ID"] = dict_item["id"]
        del dict_item["id"]
        dict_item["Nombre"] = dict_item["nombre"]
        del dict_item["nombre"]
        dict_item["Apellido"] = dict_item["apellido"]
        del dict_item["apellido"]
        dict_item["Fecha de nacimiento"] = dict_item["fecha_nac"]
        del dict_item["fecha_nac"]
        for loc in locs:
            if int(loc['id']) == dict_item["localidad_id"]:
                dict_item["Localidad"] = loc['nombre']
                break
        del dict_item["localidad_id"]
        dict_item["Domicilio"] = dict_item["domicilio"]
        del dict_item["domicilio"]
        dict_item["Género"] = dict_item["g.nombre"]
        del dict_item["g.nombre"]
        dict_item["Escuela"] = dict_item["es.nombre"]
        del dict_item["es.nombre"]
        dict_item["Barrio"] = dict_item["b.nombre"]
        del dict_item["b.nombre"]
        for t_doc in tipo_doc:
            if int(t_doc['id']) == dict_item["tipo_doc_id"]:
                dict_item["Tipo de documento"] = t_doc['nombre']
                break
        del dict_item["tipo_doc_id"]
        dict_item["Número de documento"] = dict_item["numero"]
        del dict_item["numero"]
        dict_item["Número telefónico"] = dict_item["tel"]
        del dict_item["tel"]
        dict_item["Nivel"] = dict_item["n.nombre"]
        del dict_item["n.nombre"]

    estudiantes = jsonify(estudiantes)

    return make_response(estudiantes, 200)


def create():
    if not has_permission("estudiante_new", session):
        abort(401)

    form = EstudianteCreateForm()

    locs = localidades()
    Barrio.db = get_db()
    barrios = Barrio.all()
    Genero.db = get_db()
    generos = Genero.all()
    tipos_doc = tipos_documento()
    Escuela.db = get_db()
    escuelas = Escuela.all()
    Nivel.db = get_db()
    niveles = Nivel.all()

    # choices de los selects
    form.select_localidad.choices = [
        (localidad["id"], localidad["nombre"]) for localidad in locs
    ]
    form.select_barrio.choices = [
        (barrio["id"], barrio["nombre"]) for barrio in barrios
    ]
    form.select_genero.choices = [
        (genero["id"], genero["nombre"]) for genero in generos
    ]
    form.select_tipo.choices = [
        (tipo["id"], tipo["nombre"]) for tipo in tipos_doc
    ]
    form.select_escuela.choices = [
        (escuela["id"], escuela["nombre"]) for escuela in escuelas
    ]
    form.select_nivel.choices = [
        (nivel["id"], nivel["nombre"]) for nivel in niveles
    ]

    op_response = dict()
    responsecode = 201

    if form.validate_on_submit():
        params = request.form.to_dict()
        params['fecha_nacimiento'] = datetime.strptime(params['fecha_nacimiento'], '%d/%m/%Y').date()

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
            op_response["msg"] = form.errors
            op_response["type"] = "error"

        abort(make_response(jsonify(op_response), 500))

    return make_response(jsonify(op_response), responsecode)