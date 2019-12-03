from flask import (
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
from flaskps.models.user import User
from flaskps.models.role import Role
from flaskps.models import siteconfig

from flaskps.forms.user.form_user_create import UserCreateForm
from flaskps.forms.user.form_user_update import UserUpdateForm
from flaskps.forms.user.form_email_update import EmailUpdateForm
from flaskps.forms.user.form_password_update import PasswordUpdateForm

from flaskps.helpers.auth import authenticated
from flaskps.helpers.permission import has_permission
from flaskps.helpers.role import has_role

from flaskps.resources.helpers.email_threading import send_async

from flaskps import bcrypt

from flaskps.resources.helpers.serverside_dt.serverside_table_usuarios import (
    UsuariosServerSideTable,
)
from flaskps.resources.helpers.serverside_dt import table_schemas


def users():
    User.db = get_db()
    users = User.all()

    for dict_item in users:
        del dict_item["password"]
        dict_item["created_at"] = dict_item["created_at"].strftime("%d-%m-%Y %H:%M:%S")
        dict_item["updated_at"] = dict_item["updated_at"].strftime("%d-%m-%Y %H:%M:%S")

    return users


def get_users():
    s_config = siteconfig.get_config()
    if not has_permission("usuario_index", session) or (
            s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    all_users = jsonify(users())

    return make_response(all_users, 200)


def collect_data_serverside(req):
    columns = table_schemas.SERVERSIDE_USUARIOS_TABLE_COLUMNS

    return UsuariosServerSideTable(req, users(), columns).output_result()


def serverside_table_content():
    s_config = siteconfig.get_config()
    if not has_permission("usuario_index", session) or (
            s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    data = collect_data_serverside(request)
    return jsonify(data)


def create():
    s_config = siteconfig.get_config()
    if not has_permission("usuario_new", session) or (
            s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    Role.db = get_db()
    roles = Role.all()
    form = UserCreateForm()
    form.rol_id.choices = [
        (rol["id"], rol["nombre"]) for rol in roles
    ]  # lo de las choices no sé si funciona, pero el required funciona perfecto

    op_response = dict()

    if form.validate_on_submit():
        params = request.form.to_dict()

        plain_pw = params["password"]
        params["password"] = bcrypt.generate_password_hash(plain_pw).decode("utf - 8")

        params["roles"] = request.form.getlist("rol_id")

        User.db = get_db()
        created = User.create(params)

        if created:
            html = render_template(
                "emails/mail_alta_usuario.html",
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
            abort(make_response(jsonify(op_response), 422))

    else:
        if len(form.errors) >= 2:
            op_response["msg"] = "Complete todos los datos del nuevo usuario"
            op_response["type"] = "error"
        else:
            error_msg = "".join(list(form.errors.values())[0]).strip("'[]")
            op_response["msg"] = error_msg
            op_response["type"] = "error"

        abort(make_response(jsonify(op_response), 400))

    return make_response(jsonify(op_response), 201)


def destroy():
    s_config = siteconfig.get_config()
    if not has_permission("usuario_destroy", session) or (
            s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    params = json.loads(request.data)
    uid = params["id"]

    User.db = get_db()
    success = User.delete(uid)

    op_response = dict()

    activo = params["activo"]

    if success:
        # TODO: Email notificando bloqueo de la cuenta
        condicion = "bloqueado" if activo else "activado"
        op_response["msg"] = "Se ha " + condicion + " al usuario exitosamente"
        op_response["type"] = "success"
    else:
        condicion = "bloquear" if activo else "activar"
        op_response["msg"] = "El usuario a " + condicion + " no existe"
        op_response["type"] = "error"
        abort(jsonify(op_response), 422)

    return make_response(jsonify(op_response), 204)


def update():
    s_config = siteconfig.get_config()
    if not has_permission("usuario_update", session) or (
            s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    Role.db = get_db()
    roles = Role.all()
    form = UserUpdateForm()
    form.rol_id.choices = [
        (rol["id"], rol["nombre"]) for rol in roles
    ]  # lo de las choices no sé si funciona, pero el required funciona perfecto

    op_response = dict()

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

        if updated:
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

            new_email = User.find_by_id(uid)["email"]

            if old_email != new_email:
                # Mail al email viejo
                html = render_template(
                    "emails/mail_oldmail_change.html", nombre=params["first_name"]
                )
                send_async(
                    old_email,
                    "Email Modificado | Grupo2 - Orquesta Escuela de Berisso",
                    html,
                )

                # Mail al email nuevo
                html = render_template(
                    "emails/mail_newmail_change.html", nombre=params["first_name"]
                )
                send_async(
                    new_email,
                    "Email Modificado | Grupo2 - Orquesta Escuela de Berisso",
                    html,
                )

            # Mail por defecto de que hubo un update
            html = render_template(
                "emails/mail_update_usuario.html", params=params, roles=roles_names
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
            abort(make_response(jsonify(op_response), 422))

    else:
        if len(form.errors) >= 2:
            op_response["msg"] = "Complete todos los datos del usuario a modificar"
            op_response["type"] = "error"
        else:
            error_msg = "".join(list(form.errors.values())[0]).strip("'[]")
            op_response["msg"] = error_msg
            op_response["type"] = "error"

        abort(make_response(jsonify(op_response), 400))

    return make_response(jsonify(op_response), 200)


def dashboard():
    s_config = siteconfig.get_config()
    if not authenticated(session) or (
            s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)
    else:
        Role.db = get_db()
        roles = Role.all()

        return render_template("user/dashboard.html", roles=roles)


def profile():
    s_config = siteconfig.get_config()
    if not authenticated(session) or (
            s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
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
    s_config = siteconfig.get_config()
    if not authenticated(session) or (
            s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    form = EmailUpdateForm()

    if form.validate_on_submit():
        email = request.form.get("email")
        User.db = get_db()
        updated = User.update_email(email, session.get("user"))
        if updated:
            # TODO: Email a la dirección de email anterior y a la nueva notificando actualización del email
            flash("El email se ha modificado con éxito", "success")
        else:
            flash("Se ha producido un error al actualizar el email", "error")

    else:
        error_msg = "".join(list(form.errors.values())[0]).strip("'[]")
        flash(error_msg, "error")

    return redirect(url_for("user_profile"))


def password_update():
    s_config = siteconfig.get_config()
    if not authenticated(session) or (
            s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    form = PasswordUpdateForm()
    if form.validate_on_submit():
        password = request.form.get("password")
        bcrypt_password = bcrypt.generate_password_hash(password).decode("utf - 8")
        User.db = get_db()
        updated = User.update_password(bcrypt_password, session.get("user"))
        if updated:
            # TODO: Email notificando la actualización de contraseña
            flash("La contraseña se ha modificado con éxito", "success")
        else:
            flash("Se ha producido un error al actualizar la contraseña", "error")

    else:
        error_msg = "".join(list(form.errors.values())[0]).strip("'[]")
        flash(error_msg, "error")

    return redirect(url_for("user_profile"))


def user_data():
    s_config = siteconfig.get_config()
    if not has_permission("usuario_index", session) or (
            s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
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


def user_table():
    s_config = siteconfig.get_config()
    if not has_permission("usuario_index", session) or (
            s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    Role.db = get_db()
    roles = Role.all()

    return render_template("tables/usuarios.html", roles=roles)


def user_edit_form():
    s_config = siteconfig.get_config()
    if not has_permission("usuario_update", session) or (
            s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    Role.db = get_db()
    roles = Role.all()

    return render_template("user/actions/usuario_editar.html", roles=roles)


def user_destroy_form():
    s_config = siteconfig.get_config()
    if not has_permission("usuario_destroy", session) or (
            s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    Role.db = get_db()
    roles = Role.all()

    return render_template("user/actions/usuario_bloquear.html", roles=roles)


def user_new_form():
    s_config = siteconfig.get_config()
    if not has_permission("usuario_new", session) or (
            s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    Role.db = get_db()
    roles = Role.all()

    return render_template("user/actions/usuario_crear.html", roles=roles)
