from flask import Flask, redirect, render_template, request, url_for, abort, session, flash
from flaskps.db import get_db
from flask_bcrypt import Bcrypt
from flaskps.helpers.auth import authenticated
from flaskps.models.user import User

app = Flask(__name__)
bcrypt = Bcrypt(app)

def login():
    if not authenticated(session):
        return render_template('auth/login.html')
    else:
        return redirect(url_for('index'))


def authenticate():
    params = request.form

    User.db = get_db()
    user = User.find_by_user(params['username'])

    if user and bcrypt.check_password_hash(user['password'], params['password']):
        session['logged_in'] = True
        session['user'] = user['username']
        flash("La sesión se inició correctamente.")
        return redirect(url_for('index'))
    else:
        flash("Usuario o clave incorrecto.")
        return redirect(url_for('auth_login'))


def logout():
    [session.pop(key) for key in list(session.keys())]
    flash("La sesión se cerró correctamente.")

    return redirect(url_for('auth_login'))
