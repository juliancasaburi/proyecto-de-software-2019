from flask import jsonify, make_response
from flaskps.db import get_db
from flaskps.models.role import Role


def all_roles():
    Role.db = get_db()
    roles = Role.all()
    data = jsonify(roles)
    return make_response(data, 200)
