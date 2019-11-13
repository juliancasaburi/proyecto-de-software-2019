from flask import (
    current_app as app,
    redirect,
    render_template,
    request,
    url_for,
    session,
    abort,
    json,
    make_response,
    jsonify,
    flash,
)
from flaskps.db import get_db
from flask_bcrypt import Bcrypt

from flaskps.models.user import User
from flaskps.models.role import Role

from flaskps.forms.form_user_create import UserCreateForm
from flaskps.forms.form_user_update import UserUpdateForm
from flaskps.forms.form_email_update import EmailUpdateForm
from flaskps.forms.form_password_update import PasswordUpdateForm

from flaskps.helpers.auth import authenticated
from flaskps.helpers.permission import has_permission

from flaskps.resources.email_threading import send_async


def get_users():
    if not has_permission("usuario_index", session):
        abort(401)

    User.db = get_db()
    users = User.all()

    for dict_item in users:
        dict_item["ID"] = dict_item["id"]
        del dict_item["id"]
        dict_item["Activo"] = dict_item["activo"]
        del dict_item["activo"]
        dict_item["Nombre"] = dict_item["first_name"]
        del dict_item["first_name"]
        dict_item["Apellido"] = dict_item["last_name"]
        del dict_item["last_name"]
        dict_item["Rol"] = dict_item["rol_nombre"]
        del dict_item["rol_nombre"]
        dict_item["Nombre de usuario"] = dict_item["username"]
        del dict_item["username"]
        del dict_item["password"]
        dict_item["Email"] = dict_item["email"]
        del dict_item["email"]
        dict_item["Registrado"] = dict_item["created_at"]
        del dict_item["created_at"]
        dict_item["Actualizado"] = dict_item["updated_at"]
        del dict_item["updated_at"]

    users = jsonify(users)

    return make_response(users, 200)


def create():
    if not has_permission("usuario_new", session):
        abort(401)

    Role.db = get_db()
    roles = Role.all()
    form = UserCreateForm()
    form.rol_id.choices = [
        (rol["id"], rol["nombre"]) for rol in roles
    ]  # lo de las choices no sé si funciona, pero el required funciona perfecto

    op_response = dict()
    responsecode = 201

    if form.validate_on_submit():
        params = request.form.to_dict()

        bcrypt = Bcrypt(app)
        plain_pw = params["password"]
        params["password"] = bcrypt.generate_password_hash(plain_pw).decode("utf - 8")

        params["roles"] = request.form.getlist("rol_id")

        User.db = get_db()
        created = User.create(params)

        if created:
            html = render_template(
                "helpers/mail_alta_usuario.html",
                username=params["username"],
                passwd=plain_pw,
            )

            send_async(
                params["email"],
                "Cuenta Registrada | Grupo2 - Orquesta Escuela de Berisso",
                html,
            )

            op_response["msg"] = "Se ha agregado al usuario con éxito"
            op_response["type"] = "success"
        else:
            op_response["msg"] = "El nombre de usuario está en uso, intente con otro"
            op_response["type"] = "error"
            abort(make_response(jsonify(op_response), 409))

    else:
        if len(form.errors) >= 2:
            op_response["msg"] = "Complete todos los datos del nuevo usuario"
            op_response["type"] = "error"
        else:
            error_msg = "".join(list(form.errors.values())[0]).strip("'[]")
            op_response["msg"] = error_msg
            op_response["type"] = "error"

        abort(make_response(jsonify(op_response), 500))

    return make_response(jsonify(op_response), responsecode)


def destroy():
    if not has_permission("usuario_destroy", session):
        abort(401)

    params = json.loads(request.data)
    uid = params["id"]

    User.db = get_db()
    success = User.delete(uid)

    op_response = dict()
    responsecode = 200

    if success:
        op_response["msg"] = "Se ha eliminado al usuario exitosamente"
        op_response["type"] = "success"
    else:
        op_response["msg"] = "El usuario a eliminar no existe"
        op_response["type"] = "error"
        responsecode = 404

    return make_response(jsonify(op_response), responsecode)


def update():
    if not has_permission("usuario_update", session):
        abort(401)

    Role.db = get_db()
    roles = Role.all()
    form = UserUpdateForm()
    form.rol_id.choices = [
        (rol["id"], rol["nombre"]) for rol in roles
    ]  # lo de las choices no sé si funciona, pero el required funciona perfecto

    op_response = dict()
    responsecode = 201

    if form.validate_on_submit():
        params = request.form.to_dict()
        params["roles"] = request.form.getlist("rol_id")

        if "activo" in params:
            params["activo"] = 1
        else:
            params["activo"] = 0

        User.db = get_db()

        uid = params["id"]
        old_email = User.find_by_id(uid)["email"]

        updated = User.update(params)

        # armo el string de roles para el mail
        roles_dict = User.user_roles(params["username"])
        roles_names = ""
        first = True
        for rol in roles_dict:
            if first:
                first = False
            else:
                roles_names += ", "
            roles_names += rol["nombre"]

        if updated:
            new_email = User.find_by_id(uid)["email"]

            if old_email != new_email:
                # Mail al email viejo
                html = render_template(
                    "helpers/mail_oldmail_change.html", nombre=params["first_name"]
                )
                send_async(
                    old_email,
                    "Email Modificado | Grupo2 - Orquesta Escuela de Berisso",
                    html,
                )

                # Mail al email nuevo
                html = render_template(
                    "helpers/mail_newmail_change.html", nombre=params["first_name"]
                )
                send_async(
                    new_email,
                    "Email Modificado | Grupo2 - Orquesta Escuela de Berisso",
                    html,
                )

            # Mail por defecto de que hubo un update
            html = render_template(
                "helpers/mail_update_usuario.html", params=params, roles=roles_names
            )
            send_async(
                params["email"],
                "Cuenta Modificada | Grupo2 - Orquesta Escuela de Berisso",
                html,
            )

            op_response["msg"] = "Se ha modificado al usuario con éxito"
            op_response["type"] = "success"
        else:
            op_response["msg"] = "El nombre de usuario está en uso, intente con otro"
            op_response["type"] = "error"
            abort(make_response(jsonify(op_response), 409))

    else:
        if len(form.errors) >= 2:
            op_response["msg"] = "Complete todos los datos del usuario a modificar"
            op_response["type"] = "error"
        else:
            error_msg = "".join(list(form.errors.values())[0]).strip("'[]")
            op_response["msg"] = error_msg
            op_response["type"] = "error"

        abort(make_response(jsonify(op_response), 500))

    return make_response(jsonify(op_response), responsecode)


def dashboard():
    if not authenticated(session):
        abort(401)

    Role.db = get_db()
    roles = Role.all()

    return render_template("user/dashboard.html", roles=roles)


def profile():
    if not authenticated(session):
        abort(401)

    username = session.get("user")

    User.db = get_db()
    user = User.find_by_user(username)

    roles = User.user_roles(username)

    return render_template(
        "user/account.html",
        username=user["username"],
        email=user["email"],
        password=user["password"],
        first_name=user["first_name"],
        last_name=user["last_name"],
        roles=roles,
    )


def email_update():
    if not authenticated(session):
        abort(401)

    form = EmailUpdateForm()

    if form.validate_on_submit():
        email = request.form.get("email")
        User.db = get_db()
        User.update_email(email, session.get("user"))
        flash("El email se ha modificado con éxito", "success")

    # TODO: Mensajes de error
    else:
        error_msg = "".join(list(form.errors.values())[0]).strip("'[]")
        flash(error_msg, "error")

    return redirect(url_for("user_profile"))


def password_update():
    if not authenticated(session):
        abort(401)

    form = PasswordUpdateForm()
    if form.validate_on_submit():
        password = request.form.get("password")
        bcrypt = Bcrypt(app)
        bcrypt_password = bcrypt.generate_password_hash(password).decode("utf - 8")
        User.db = get_db()
        User.update_password(bcrypt_password, session.get("user"))
        flash("La contraseña se ha modificado con éxito", "success")

    # TODO: Mensajes de error
    else:
        error_msg = "".join(list(form.errors.values())[0]).strip("'[]")
        flash(error_msg, "error")

    return redirect(url_for("user_profile"))


def user_data():
    if not has_permission("usuario_index", session):
        abort(401)

    if request.args.get("id"):
        User.db = get_db()
        uid = request.args.get("id")
        user = User.find_by_id(uid)
        if user != None:
            user["roles"] = User.user_roles(user["username"])
            data = jsonify(user)
            return make_response(data, 200)
        else:
            flash("El usuario con ID:" + uid + "no existe.", "error")
            return abort(404)

    elif request.args.get("username"):
        User.db = get_db()
        username = request.args.get("username")
        user = User.find_by_user(username)
        if user != None:
            user["roles"] = User.user_roles(user["username"])
            data = jsonify(user)
            return make_response(data, 200)
        else:
            flash("El usuario " + username + "no existe.", "error")
            return abort(404)

    else:
        abort(400)
