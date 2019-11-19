from flask import request, session, abort, make_response, jsonify, render_template
from flaskps.db import get_db
from flaskps.models.taller import Taller

from flaskps.forms.form_taller_create import TallerCreateForm

from flaskps.helpers.permission import has_permission


def create():
    if not has_permission("taller_new", session):
        abort(401)

    form = TallerCreateForm()

    op_response = dict()
    responsecode = 201

    if form.validate_on_submit():
        params = request.form.to_dict()

        Taller.db = get_db()
        created = Taller.create(params)

        if created:
            op_response["msg"] = "Se ha agregado al taller con éxito"
            op_response["type"] = "success"
        else:
            op_response["msg"] = "Ha ocurrido un error al crear el Taller"
            op_response["type"] = "error"
            abort(make_response(jsonify(op_response), 409))

    else:
        if len(form.errors) >= 2:
            op_response["msg"] = "Complete todos los datos del nuevo Taller"
            op_response["type"] = "error"
        else:
            error_msg = "".join(list(form.errors.values())[0]).strip("'[]")
            op_response["msg"] = error_msg
            op_response["type"] = "error"

        abort(make_response(jsonify(op_response), 500))

    return make_response(jsonify(op_response), responsecode)


def set_ciclo():
    params = request.form.to_dict()
    params["ciclos"] = request.form.getlist("select_ciclos")

    Taller.db = get_db()
    created = Taller.set_ciclos(params)

    op_response = dict()
    responsecode = 201

    if created:
        op_response["msg"] = "Se ha establecido la relación"
        op_response["type"] = "success"
    else:
        op_response["msg"] = "Ha ocurrido un error al establecer la relación"
        op_response["type"] = "error"
        abort(make_response(jsonify(op_response), 409))

    return make_response(jsonify(op_response), responsecode)


def get_ciclos():
    t_id = request.args.get("id")
    Taller.db = get_db()
    ciclos = Taller.ciclos(t_id)

    if ciclos is None:
        abort(404)

    return make_response(jsonify(ciclos), 200)


def get_docentes_ciclo():
    t_id = request.args.get("t_id")
    c_id = request.args.get("c_id")

    Taller.db = get_db()
    docentes = Taller.docentes_ciclo(t_id, c_id)

    if docentes is None:
        abort(404)

    return make_response(jsonify(docentes), 200)


def set_docentes():
    params = request.form.to_dict()
    params["docentes"] = request.form.getlist("select_docentes")

    # TODO:
    Taller.db = get_db()
    created = Taller.set_docentes(params)

    op_response = dict()
    responsecode = 201

    if created:
        op_response["msg"] = "Se ha establecido la relación"
        op_response["type"] = "success"
    else:
        op_response["msg"] = "Ha ocurrido un error al establecer la relación"
        op_response["type"] = "error"
        abort(make_response(jsonify(op_response), 409))

    return make_response(jsonify(op_response), responsecode)


def set_estudiantes():
    params = request.form.to_dict()
    params["docentes"] = request.form.getlist("select_estudiantes")

    # TODO:
    Taller.db = get_db()
    created = Taller.set_ciclos(params)

    op_response = dict()
    responsecode = 201

    if created:
        op_response["msg"] = "Se ha establecido la relación"
        op_response["type"] = "success"
    else:
        op_response["msg"] = "Ha ocurrido un error al establecer la relación"
        op_response["type"] = "error"
        abort(make_response(jsonify(op_response), 409))

    return make_response(jsonify(op_response), responsecode)
