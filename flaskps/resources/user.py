from flask import Flask, redirect, render_template, request, url_for, session, abort, json, make_response, jsonify
from flaskps.db import get_db
from flask_bcrypt import Bcrypt
from flaskps.models.user import User
from flaskps.helpers.auth import authenticated
from flaskps.helpers.permission import has_permission

app = Flask = Flask(__name__)
bcrypt = Bcrypt(app)


def index():
    if not authenticated(session):
        abort(401)

    User.db = get_db()
    users = User.all()

    return render_template('user/administrador.html', users=users)


def create():
    if not authenticated(session):
        abort(401)

    params = request.form.to_dict()
    params['password'] = bcrypt.generate_password_hash(params['password']).decode('utf - 8')
    params['roles'] = request.form.getlist('rol_id')

    User.db = get_db()
    User.create(params)
    return redirect(url_for('user_dashboard'))


def destroy():
    if not authenticated(session) and has_permission('user_destroy', session):
        abort(401)

    params = json.loads(request.data)
    uid = params['id']

    User.db = get_db()
    User.delete(uid)
    data = {'success': True}
    return make_response(jsonify(data), 200)


def dashboard():
    if not authenticated(session):
        abort(401)

    User.db = get_db()
    role = User.role(session.get('user'))
    roles = User.get_all_roles()

    if 'administrador' in role.values():
        return render_template('user/administrador.html', roles=roles)
    else:
        return redirect(url_for('index'))
