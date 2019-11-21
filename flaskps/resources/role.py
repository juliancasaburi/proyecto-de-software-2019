from flask import jsonify, make_response, session, abort
from flaskps.db import get_db

from flaskps.models.role import Role
from flaskps.models import siteconfig

from flaskps.helpers.permission import has_permission
from flaskps.helpers.role import has_role


def all_roles():
    s_config = siteconfig.get_config()
    if not has_permission("usuario_new", session) and (
            s_config['modo_mantenimiento'] == 1 and not has_role("administrador", session)):
        abort(401)

    Role.db = get_db()
    roles = Role.all()
    data = jsonify(roles)
    return make_response(data, 200)
