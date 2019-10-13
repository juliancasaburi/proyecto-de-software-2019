from os import path
from flask import Flask, render_template
from flaskps.config import Config

# Resources
from flaskps.resources import auth

# Configuración inicial de la app
app = Flask(__name__)
app.config.from_object(Config)

# Autenticación
app.add_url_rule("/login", 'auth_login', auth.login)
app.add_url_rule("/logout", 'auth_logout', auth.logout)
app.add_url_rule(
    "/authenticate",
    'auth_authenticate',
    auth.authenticate,
    methods=['POST']
)


@app.route("/")
def index():
    return render_template('index.html')
