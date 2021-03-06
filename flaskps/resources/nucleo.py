from flask import (
    request,
    session,
    abort,
    make_response,
    jsonify,
    json,
    render_template,
)

from flaskps.forms.nucleo.form_nucleo_create import NucleoCreateForm
from flaskps.helpers.permission import has_permission
from flaskps.helpers.role import has_role
from flaskps.models import siteconfig
from flaskps.models.nucleo import Nucleo


def get_nucleos():
    s_config = siteconfig.get_config()
    if not has_permission("nucleo_index", session) or (
        s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    nucleos = Nucleo.all()

    nucleos = jsonify(nucleos)

    return make_response(nucleos, 200)


def get_nucleos_activos():
    s_config = siteconfig.get_config()
    if s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session):
        abort(401)

    nucleos = Nucleo.activos()

    nucleos = jsonify(nucleos)

    return make_response(nucleos, 200)


def new():
    s_config = siteconfig.get_config()
    if not has_permission("nucleo_new", session) or (
        s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    form = NucleoCreateForm()

    op_response = dict()

    if form.validate_on_submit():
        params = request.form.to_dict()

        created = Nucleo.create(params)

        if created:
            op_response["msg"] = "Se ha agregado al núcleo exitosamente"
            op_response["type"] = "success"
        else:
            op_response["msg"] = "Ha ocurrido un error al crear al núcleo"
            op_response["type"] = "error"
            abort(make_response(jsonify(op_response), 422))

    else:
        if len(form.errors) >= 2:
            op_response["msg"] = "Complete todos los datos del nuevo núcleo"
            op_response["type"] = "error"
        else:
            error_msg = "".join(list(form.errors.values())[0]).strip("'[]")
            op_response["msg"] = error_msg
            op_response["type"] = "error"

        abort(make_response(jsonify(op_response), 400))

    return make_response(jsonify(op_response), 201)


def update():
    s_config = siteconfig.get_config()
    if not has_permission("nucleo_update", session) or (
        s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    form = NucleoCreateForm()  # uso este porq es igual

    op_response = dict()

    if form.validate_on_submit():
        params = request.form.to_dict()

        updated = Nucleo.update(params)

        if updated:
            op_response["msg"] = "Se ha modificado al núcleo con éxito"
            op_response["type"] = "success"
        else:
            op_response["msg"] = "Ocurrió un error"
            op_response["type"] = "error"
            abort(make_response(jsonify(op_response), 422))

    else:
        if len(form.errors) >= 2:
            op_response["msg"] = "Complete todos los datos del núcleo a modificar"
            op_response["type"] = "error"
        else:
            error_msg = "".join(list(form.errors.values())[0]).strip("'[]")
            op_response["msg"] = error_msg
            op_response["type"] = "error"

        abort(make_response(jsonify(op_response), 400))

    return make_response(jsonify(op_response), 200)


def destroy():
    s_config = siteconfig.get_config()
    if not has_permission("nucleo_destroy", session) or (
        s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    params = json.loads(request.data)
    nid = params["id"]

    success = Nucleo.delete(nid)

    op_response = dict()

    activo = params["activo"]

    if success:
        condicion = "bloqueado" if activo else "activado"
        op_response["msg"] = "Se ha " + condicion + " al núcleo exitosamente"
        op_response["type"] = "success"
    else:
        condicion = "bloquear" if activo else "activar"
        op_response["msg"] = "El núcleo a " + condicion + " no existe"
        op_response["type"] = "error"
        abort(jsonify(op_response), 422)

    return make_response(jsonify(op_response), 204)


# por id
def nucleo_data():
    s_config = siteconfig.get_config()
    if not has_permission("nucleo_show", session) or (
        s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    id = request.args.get("id")
    if id:

        nucleo = Nucleo.find_by_id(id)
        if nucleo is not None:
            data = jsonify(nucleo)
            return make_response(data, 200)
        else:
            abort(422)

    else:
        abort(400)


def nucleo_table():
    s_config = siteconfig.get_config()
    if not has_permission("nucleo_index", session) or (
        s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    return render_template("tables/nucleos.html")
