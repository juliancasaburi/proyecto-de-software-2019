from flask import jsonify, make_response, session, abort
from flaskps.db import get_db
from flaskps.models.role import Role
from flaskps.helpers.auth import authenticated
from flaskps.helpers import permission


def all_roles():
    if not authenticated(session) or not permission.has_permission(
        "usuario_new", session
    ):
        abort(401)

    Role.db = get_db()
    roles = Role.all()
    data = jsonify(roles)
    return make_response(data, 200)
