from flask import redirect, render_template, request, url_for, abort, session, flash
from flaskps.db import get_db
from flaskps.helpers.auth import authenticated
from flaskps.models.user import User


def login():
    if not authenticated(session):
        return render_template('auth/login.html')
    else:
        return redirect(url_for('index'))


def authenticate():
    params = request.form

    User.db = get_db()
    user = User.find_by_user_and_pass(params['username'], params['password'])

    if not user:
        flash("Usuario o clave incorrecto.")
        return redirect(url_for('auth_login'))

    session['logged_in'] = True
    session['user'] = user['username']
    flash("La sesión se inició correctamente.")

    return redirect(url_for('index'))


def logout():
    [session.pop(key) for key in list(session.keys())]
    flash("La sesión se cerró correctamente.")

    return redirect(url_for('auth_login'))
