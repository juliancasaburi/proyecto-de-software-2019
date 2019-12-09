from flask import jsonify, make_response, session, abort

from flaskps.helpers.permission import has_permission
from flaskps.helpers.role import has_role
from flaskps.models import siteconfig
from flaskps.models.role import Role


def all_roles():
    s_config = siteconfig.get_config()
    if not has_permission("usuario_new", session) or (
        s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    roles = Role.all()
    data = jsonify(roles)
    return make_response(data, 200)
