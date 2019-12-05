from flask import request, session, abort, make_response, jsonify, render_template
from flaskps.db import get_db

from flaskps.models import siteconfig
from flaskps.models.ciclo_lectivo import CicloLectivo
from flaskps.models.docente import Docente
from flaskps.models.estudiante import Estudiante
from flaskps.models.taller import Taller

from flaskps.forms.taller.forms_taller import TallerForm

from flaskps.helpers.permission import has_permission
from flaskps.helpers.role import has_role


def create():
    s_config = siteconfig.get_config()
    if not has_permission("taller_new", session) or (
        s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    form = TallerForm()

    op_response = dict()

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
            abort(make_response(jsonify(op_response), 422))

    else:
        if len(form.errors) >= 2:
            op_response["msg"] = "Complete todos los datos del nuevo Taller"
            op_response["type"] = "error"
        else:
            error_msg = "".join(list(form.errors.values())[0]).strip("'[]")
            op_response["msg"] = error_msg
            op_response["type"] = "error"

        abort(make_response(jsonify(op_response), 400))

    return make_response(jsonify(op_response), 201)


def set_ciclo():
    s_config = siteconfig.get_config()
    if not has_permission("taller_update", session) or (
        s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    params = request.form.to_dict()
    params["taller_id"] = params["modal_id_taller"]
    params["ciclos"] = request.form.getlist("modal_select_ciclos")

    Taller.db = get_db()
    created = Taller.set_ciclos(params)

    op_response = dict()

    if created:
        op_response["msg"] = "Se ha establecido la relación"
        op_response["type"] = "success"
    else:
        op_response["msg"] = "Ha ocurrido un error al establecer la relación"
        op_response["type"] = "error"
        abort(make_response(jsonify(op_response), 422))

    return make_response(jsonify(op_response), 200)


def get_ciclos():
    s_config = siteconfig.get_config()
    if not has_permission("ciclolectivo_index", session) or (
        s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    t_id = request.args.get("id")
    Taller.db = get_db()
    ciclos = Taller.ciclos(t_id)

    for ciclo in ciclos:
        ciclo["fecha_ini"] = ciclo["fecha_ini"].strftime("%d-%m-%Y")
        ciclo["fecha_fin"] = ciclo["fecha_fin"].strftime("%d-%m-%Y")

    if ciclos is None:
        abort(404)

    return make_response(jsonify(ciclos), 200)


def get_docentes_ciclo():
    s_config = siteconfig.get_config()
    if not has_permission("docente_index", session) or (
        s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    t_id = request.args.get("t_id")
    c_id = request.args.get("c_id")

    Taller.db = get_db()
    docentes = Taller.docentes_ciclo(t_id, c_id)

    if docentes is None:
        abort(404)

    return make_response(jsonify(docentes), 200)


def set_docentes():
    s_config = siteconfig.get_config()
    if not has_permission("taller_update", session) or (
        s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    params = request.form.to_dict()
    params["docentes"] = request.form.getlist("modal_select_docentes")

    # TODO:
    Taller.db = get_db()
    created = Taller.set_docentes(params)

    op_response = dict()

    if created:
        op_response["msg"] = "Se ha establecido la relación"
        op_response["type"] = "success"
    else:
        op_response["msg"] = "Ha ocurrido un error al establecer la relación"
        op_response["type"] = "error"
        abort(make_response(jsonify(op_response), 422))

    return make_response(jsonify(op_response), 200)


def get_estudiantes_ciclo():
    s_config = siteconfig.get_config()
    if not has_permission("estudiante_index", session) or (
        s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    t_id = request.args.get("t_id")
    c_id = request.args.get("c_id")

    Taller.db = get_db()
    estudiantes = Taller.estudiantes_ciclo(t_id, c_id)

    if estudiantes is None:
        abort(404)

    return make_response(jsonify(estudiantes), 200)


def set_estudiantes():
    s_config = siteconfig.get_config()
    if not has_permission("taller_update", session) or (
        s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    params = request.form.to_dict()
    params["estudiantes"] = request.form.getlist("modal_select_estudiantes")

    # TODO:
    Taller.db = get_db()
    created = Taller.set_estudiantes(params)

    op_response = dict()

    if created:
        op_response["msg"] = "Se ha establecido la relación"
        op_response["type"] = "success"
    else:
        op_response["msg"] = "Ha ocurrido un error al establecer la relación"
        op_response["type"] = "error"
        abort(make_response(jsonify(op_response), 422))

    return make_response(jsonify(op_response), 200)


def taller_new_form():
    s_config = siteconfig.get_config()
    if not has_permission("taller_new", session) or (
        s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    return render_template("user/actions/taller_crear.html")


def taller_set_docentes_form():
    s_config = siteconfig.get_config()
    if not has_permission("taller_update", session) or (
        s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    CicloLectivo.db = get_db()
    ciclos = CicloLectivo.all()

    Docente.db = get_db()
    docentes = Docente.all()

    for ciclo in ciclos:
        ciclo["fecha_ini"] = ciclo["fecha_ini"].strftime("%d-%m-%Y")
        ciclo["fecha_fin"] = ciclo["fecha_fin"].strftime("%d-%m-%Y")

    return render_template(
        "user/actions/taller_asociar_docentes.html", ciclos=ciclos, docentes=docentes
    )


def taller_set_estudiantes_form():
    s_config = siteconfig.get_config()
    if not has_permission("taller_update", session) or (
        s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    CicloLectivo.db = get_db()
    ciclos = CicloLectivo.all()

    Estudiante.db = get_db()
    estudiantes = Estudiante.all()

    for ciclo in ciclos:
        ciclo["fecha_ini"] = ciclo["fecha_ini"].strftime("%d-%m-%Y")
        ciclo["fecha_fin"] = ciclo["fecha_fin"].strftime("%d-%m-%Y")

    return render_template(
        "user/actions/taller_asociar_estudiantes.html",
        ciclos=ciclos,
        estudiantes=estudiantes,
    )


def taller_set_ciclo_form():
    s_config = siteconfig.get_config()
    if not has_permission("taller_update", session) or (
        s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    Taller.db = get_db()
    talleres = Taller.all()

    CicloLectivo.db = get_db()
    ciclos = CicloLectivo.all()

    for ciclo in ciclos:
        ciclo["fecha_ini"] = ciclo["fecha_ini"].strftime("%d-%m-%Y")
        ciclo["fecha_fin"] = ciclo["fecha_fin"].strftime("%d-%m-%Y")

    return render_template(
        "user/actions/taller_asociar_ciclo.html", talleres=talleres, ciclos=ciclos
    )


def taller_table():
    s_config = siteconfig.get_config()
    if not has_permission("taller_index", session) or (
        s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    Taller.db = get_db()
    talleres = Taller.all()

    return render_template("partials/tabs/talleres.html", talleres=talleres)


def get_talleres():
    s_config = siteconfig.get_config()
    if not has_permission("taller_index", session) or (
        s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    Taller.db = get_db()
    all_talleres = Taller.all()

    all_talleres = jsonify(all_talleres)

    return make_response(all_talleres, 200)


def data():
    s_config = siteconfig.get_config()
    if not has_permission("taller_show", session) or (
        s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    Taller.db = get_db()
    t_id = request.args.get("id")
    taller = Taller.find_by_id(t_id)
    if taller != None:
        data = jsonify(taller)
        return make_response(data, 200)
    else:
        return abort(404)


def update():
    s_config = siteconfig.get_config()
    if not has_permission("taller_update", session) or (
        s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    form = TallerForm()

    op_response = dict()

    if form.validate_on_submit():
        params = request.form.to_dict()

        Taller.db = get_db()

        updated = Taller.update(params)

        if updated:
            op_response["msg"] = "Se ha modificado el taller con éxito"
            op_response["type"] = "success"
        else:
            op_response["msg"] = "Ha ocurrido un error al editar el taller"
            op_response["type"] = "error"
            abort(make_response(jsonify(op_response), 422))

    else:
        if len(form.errors) >= 2:
            op_response["msg"] = "Complete todos los datos del taller a modificar"
            op_response["type"] = "error"
        else:
            error_msg = "".join(list(form.errors.values())[0]).strip("'[]")
            op_response["msg"] = error_msg
            op_response["type"] = "error"

        abort(make_response(jsonify(op_response), 400))

    return make_response(jsonify(op_response), 200)
