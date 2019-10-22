from flask import jsonify, make_response
from flaskps.db import get_db
from flaskps.models.user import User


def all_roles():
    User.db = get_db()
    roles = User.get_all_roles()
    data = jsonify(roles)
    return make_response(data, 200)
