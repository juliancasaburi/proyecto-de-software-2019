from flask import (
    redirect,
    render_template,
    request,
    url_for,
    session,
    flash,
)

from flaskps import bcrypt
from flaskps.forms.auth.form_login import LoginForm
from flaskps.helpers.auth import authenticated
from flaskps.models import siteconfig
from flaskps.models.user import User


def login():
    if not authenticated(session):
        return render_template("auth/login.html")
    else:
        return redirect(url_for("index"))


def authenticate():

    form = LoginForm()

    if form.validate_on_submit():
        params = request.form

        user = User.find_by_user(params["username"])

        if (
            user
            and user["activo"] == 1
            and bcrypt.check_password_hash(user["password"], params["password"])
        ):

            config = siteconfig.get_config()
            modo_mantenimiento = config["modo_mantenimiento"]

            if modo_mantenimiento == 1 and (
                not User.has_role(params["username"], "administrador")
            ):
                flash("Sitio en mantenimiento", "error")
            else:
                session["user"] = user["username"]
                flash("La sesión se inició correctamente", "success")
                return redirect(url_for("user_dashboard"))

        elif user and user["activo"] == 0:
            flash("Su cuenta está bloqueada", "error")
        else:
            flash("Usuario o clave incorrecto", "error")

    # TODO: Mensajes de error
    else:
        if len(form.errors) == 2:
            flash("Complete los campos para poder loguearse", "error")
        else:
            error_msg = "".join(list(form.errors.values())[0]).strip("'[]")
            flash(error_msg, "error")

    return redirect(url_for("auth_login"))


def logout():
    if authenticated(session):
        [session.pop(key) for key in list(session.keys())]
        session.clear()
        flash("La sesión se cerró correctamente", "success")

        return redirect(url_for("auth_login"))
    else:
        return redirect(url_for("index"))
