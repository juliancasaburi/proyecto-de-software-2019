from flask import redirect, render_template, request, url_for, session, abort
from flaskps.db import get_db
from flaskps.models.user import User
from flaskps.helpers.auth import authenticated
from flaskps.helpers import permission


def user_list():
    if not authenticated(session) or not permission.has_permission('usuario_index', session):
        abort(401)

    User.db = get_db()
    users = User.all()

    for dict_item in users:
        dict_item['nombre'] = dict_item['first_name']
        del dict_item['first_name']
        dict_item['apellido'] = dict_item['last_name']
        del dict_item['last_name']
        dict_item['rol'] = dict_item['rol_nombre']
        del dict_item['rol_nombre']
        dict_item['usuario'] = dict_item['username']
        del dict_item['username']
        del dict_item['password']
        dict_item['registrado'] = dict_item['created_at']
        del dict_item['created_at']
        dict_item['actualizado'] = dict_item['updated_at']
        del dict_item['updated_at']

    return render_template('usuarios.html', users=users)
