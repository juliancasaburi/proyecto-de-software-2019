from flask import session, abort, make_response, jsonify, request

from flaskps.helpers.permission import has_permission
from flaskps.models import siteconfig


def maintenance_mode():
    if not has_permission("config_update", session):
        abort(401)

    config = siteconfig.get_config()
    modo_mantenimiento = config["modo_mantenimiento"]

    if modo_mantenimiento == 0:
        siteconfig.update_maintenance(1)
    else:
        siteconfig.update_maintenance(0)

    config = siteconfig.get_config()
    modo_mantenimiento = config["modo_mantenimiento"]

    data = {"modo_mantenimiento": modo_mantenimiento}
    return make_response(jsonify(data), 200)


def config_update():
    if not has_permission("config_update", session):
        abort(401)

    params = request.form.to_dict()

    data = {"msg": "Configuración actualizada exitosamente"}

    success = siteconfig.update_config(params)

    if success:
        return make_response(jsonify(data), 200)
    else:
        data = {"msg": "Ha ocurrido un error al actualizar la configuración"}
        return make_response(jsonify(data), 500)
