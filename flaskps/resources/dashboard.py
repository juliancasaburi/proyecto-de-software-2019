import os
from flask import Flask, render_template, session, abort, request, redirect, url_for
from flaskps.db import get_db
from flaskps.models.user import User
from flaskps.models.role import Role
from flaskps.helpers.auth import authenticated
from flaskps.helpers import permission
from flask import jsonify, make_response
from pyutil import filereplace, fileoverwrite

app = Flask(__name__)

def user_list():
    if not authenticated(session) or not permission.has_permission('usuario_index', session):
        abort(401)

    User.db = get_db()
    users = User.all()

    Role.db = get_db()
    roles = Role.all()

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


#REFACTORIZAR con user_list
def user_edit_form():
    if not authenticated(session) or not permission.has_permission('usuario_index', session):
        abort(401)

    User.db = get_db()
    users = User.all()

    Role.db = get_db()
    roles = Role.all()

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

    return render_template('user/actions/usuario_editar.html', users=users, roles=roles)


#REFACTORIZAR con user_list
def user_destroy_form():
    if not authenticated(session) or not permission.has_permission('usuario_index', session):
        abort(401)

    User.db = get_db()
    users = User.all()

    Role.db = get_db()
    roles = Role.all()

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

    return render_template('user/actions/usuario_eliminar.html', users=users, roles=roles)


def user_new_form():
    if not authenticated(session) or not permission.has_permission('usuario_new', session):
        abort(401)

    Role.db = get_db()
    roles = Role.all()

    return render_template('user/actions/usuario_crear.html', roles=roles)


def maintenance_mode():
    if not authenticated(session) or not permission.has_permission('config_update', session):
        abort(401)

    app.config.from_pyfile('../config/config.cfg')
    modo_mantenimiento = app.config['MODO_MANTENIMIENTO']
    if modo_mantenimiento == '0':
        filereplace("../config/config.cfg", f"MODO_MANTENIMIENTO = '0'", "MODO_MANTENIMIENTO = '1'")
        os.environ['MODO_MANTENIMIENTO'] = '1'
    else:
        filereplace("../config/config.cfg", f"MODO_MANTENIMIENTO = '1'", "MODO_MANTENIMIENTO = '0'")
        os.environ['MODO_MANTENIMIENTO'] = '0'

    data = {'modo_mantenimiento': os.environ['MODO_MANTENIMIENTO']}
    return make_response(jsonify(data), 200)


def config_update():
    if not authenticated(session) or not permission.has_permission('config_update', session):
        abort(401)

    params = request.form.to_dict()

    app.config.from_pyfile('../config/config.cfg')

    newline = '\n'
    text = (f"TITULO = '{params['titulo_home']}'{newline}"
            f"DESCRIPCION = '{params['descripcion']}'{newline}"
            f"EMAIL_CONTACTO = '{params['email']}'{newline}"
            f"MODO_MANTENIMIENTO = '{app.config['MODO_MANTENIMIENTO']}'{newline}"
            f"ITEMS_POR_PAGINA = '{params['items_por_pagina']}'{newline}"
            )
    fileoverwrite("../config/config.cfg", text)
    return redirect(url_for('user_dashboard'))


def config_edit():
    if not authenticated(session) or not permission.has_permission('config_update', session):
        abort(401)

    return render_template('/user/actions/configuracion_editar.html')

