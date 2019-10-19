import os
from flask import render_template, session, abort
from flaskps.db import get_db
from flaskps.models.user import User
from flaskps.helpers.auth import authenticated
from flaskps.helpers import permission
from flask import jsonify, make_response
from pyutil import filereplace


def user_list():
    if not authenticated(session) or not permission.has_permission('usuario_index', session):
        abort(401)

    User.db = get_db()
    users = User.all()

    roles = User.get_all_roles()

    for dict_item in users:
        dict_item['ID'] = dict_item['id']
        del dict_item['id']
        dict_item['Activo'] = dict_item['activo']
        del dict_item['activo']
        dict_item['Nombre'] = dict_item['first_name']
        del dict_item['first_name']
        dict_item['Apellido'] = dict_item['last_name']
        del dict_item['last_name']
        dict_item['Rol'] = dict_item['rol_nombre']
        del dict_item['rol_nombre']
        dict_item['Nombre de usuario'] = dict_item['username']
        del dict_item['username']
        del dict_item['password']
        dict_item['Email'] = dict_item['email']
        del dict_item['email']
        dict_item['Registrado'] = dict_item['created_at']
        del dict_item['created_at']
        dict_item['Actualizado'] = dict_item['updated_at']
        del dict_item['updated_at']

    return render_template('user/actions/usuarios.html', users=users, roles=roles)


def user_new_form():
    if not authenticated(session) or not permission.has_permission('usuario_new', session):
        abort(401)

    User.db = get_db()
    roles = User.get_all_roles()

    return render_template('user/actions/usuario_crear.html', roles=roles)


def maintenance_mode():
    modo_mantenimiento = os.getenv("MODO_MANTENIMIENTO")
    if modo_mantenimiento == '0':
        filereplace("flaskps/config/config.cfg", f"MODO_MANTENIMIENTO = '0'", "MODO_MANTENIMIENTO = '1'")
        os.environ['MODO_MANTENIMIENTO'] = '1'
    else:
        filereplace("flaskps/config/config.cfg", f"MODO_MANTENIMIENTO = '1'", "MODO_MANTENIMIENTO = '0'")
        os.environ['MODO_MANTENIMIENTO'] = '0'
    data = {'success':True}
    return make_response(jsonify(data), 200)

