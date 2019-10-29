from flask import Flask, redirect, render_template, request, url_for, session, abort, json, make_response, jsonify, \
    flash
from flaskps.db import get_db
from flask_bcrypt import Bcrypt
from flaskps.models.user import User
from flaskps.models.role import Role

from flaskps.helpers.auth import authenticated
from flaskps.helpers.permission import has_permission
from flaskps.forms.form_email_update import EmailUpdateForm
from flaskps.forms.form_password_update import PasswordUpdateForm
from flaskps.config import Config
from flask_mail import Mail, Message

app = Flask = Flask(__name__)
bcrypt = Bcrypt(app)

# Mail Config
app.config['MAIL_SERVER'] = Config.MAIL_SERVER
app.config['MAIL_PORT'] = Config.MAIL_PORT
app.config['MAIL_USERNAME'] = Config.MAIL_USERNAME
app.config['MAIL_PASSWORD'] = Config.MAIL_PASSWORD
app.config['MAIL_USE_TLS'] = Config.MAIL_USE_TLS
app.config['MAIL_USE_SSL'] = Config.MAIL_USE_SSL
mail = Mail(app)


def get_users():
    if not authenticated(session) or not has_permission('usuario_index', session):
        abort(401)

    User.db = get_db()
    users = User.all()

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

    users = jsonify(users)

    return make_response(users, 200)


def create():
    if not authenticated(session):
        abort(401)

    params = request.form.to_dict()
    plain_pw = params['password']
    params['password'] = bcrypt.generate_password_hash(plain_pw).decode('utf - 8')
    params['roles'] = request.form.getlist('rol_id')

    User.db = get_db()
    User.create(params)

    msg = Message("Cuenta Registrada | Grupo2 - Orquesta Escuela de Berisso",
                  sender="grupo2unlppds2019@gmail.com",
                  recipients=[params['email']],
                  charset='utf8')

    msg.html = render_template("helpers/mail_alta_usuario.html", username=params['username'], passwd=plain_pw)

    mail.send(msg)

    return redirect(url_for('user_new_form'))


def destroy():
    if not authenticated(session) and has_permission('usuario_destroy', session):
        abort(401)

    params = json.loads(request.data)
    uid = params['id']

    User.db = get_db()
    User.delete(uid)
    data = {'success': True}
    return make_response(jsonify(data), 200)


#REFACTORIZAR
def destroy_and_refresh():
    if not authenticated(session) and has_permission('usuario_destroy', session):
        abort(401)

    params = request.form.to_dict();
    uid = params['id']

    User.db = get_db()
    User.delete(uid)
    return redirect(url_for('user_destroy_form'))


def dashboard():
    if not authenticated(session):
        abort(401)

    Role.db = get_db()
    roles = Role.all()

    return render_template('user/dashboard.html', roles=roles)


def profile():
    if not authenticated(session):
        abort(401)

    username = session.get('user')

    User.db = get_db()
    user = User.find_by_user(username)

    roles = User.user_roles(username)

    return render_template('user/account.html', username=user['username'], email=user['email'], password=user['password'], first_name=user['first_name'], last_name=user['last_name'], roles=roles)


def email_update():
    if not authenticated(session):
        abort(401)

    form = EmailUpdateForm()

    if form.validate_on_submit():
        email = request.form.get('email')
        User.db = get_db()
        User.update_email(email, session.get('user'))

    #TODO: Mensajes de error

    return redirect(url_for('user_profile'))


def password_update():
    if not authenticated(session):
        abort(401)

    form = PasswordUpdateForm()
    if form.validate_on_submit():
        password = request.form.get('password')
        bcrypt_password = bcrypt.generate_password_hash(password).decode('utf - 8')
        User.db = get_db()
        User.update_password(bcrypt_password, session.get('user'))

    # TODO: Mensajes de error

    return redirect(url_for('user_profile'))


def user_data():
    if not authenticated(session) and has_permission('usuario_index', session):
        abort(401)
    User.db = get_db()
    uid = request.json['id']
    user = User.find_by_id(uid)
    if user != None:
        user['roles'] = User.user_roles(user['username'])
        data = jsonify(user)
        return make_response(data, 200)
    else:
        flash('El usuario con ID:' + uid + 'no existe.', 'error')
        return abort(404)


def update():
    if not authenticated(session) and has_permission('usuario_update', session):
        abort(401)

    params = request.form.to_dict()
    params['roles'] = request.form.getlist('rol_id')

    if 'activo' in params:
        params['activo'] = 1
    else:
        params['activo'] = 0

    User.db = get_db()
    User.update(params)

    return make_response(jsonify(params), 200)


#refactorizar
def update_and_refresh():
    if not authenticated(session) and has_permission('usuario_update', session):
        abort(401)

    params = request.form.to_dict()
    params['roles'] = request.form.getlist('rol_id')

    if 'activo' in params:
        params['activo'] = 1
    else:
        params['activo'] = 0

    User.db = get_db()
    User.update(params)
    return redirect(url_for('user_edit_form'))

