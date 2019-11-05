import pickle

from flask import Flask, redirect, render_template, request, url_for, session, flash
from wtforms import ValidationError

from flaskps.db import get_db
from flask_bcrypt import Bcrypt

from flaskps.forms.form_login import LoginForm
from flaskps.helpers.auth import authenticated
from flaskps.models.user import User
from flaskps.helpers import siteconfig as helper_siteconfig
from flaskps.helpers.siteconfig import SiteConfig

app = Flask(__name__)
bcrypt = Bcrypt(app)


def login():
    if not authenticated(session):
        return render_template("auth/login.html")
    else:
        return redirect(url_for("index"))


def authenticate():

    form = LoginForm()

    if form.validate_on_submit():
        params = request.form
        User.db = get_db()
        user = User.find_by_user(params["username"])

        if (
            user
            and user["activo"] == 1
            and bcrypt.check_password_hash(user["password"], params["password"])
        ):
            SiteConfig.db = get_db()
            config = helper_siteconfig.get_config()
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
