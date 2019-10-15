from os import path
from flask import Flask, render_template
from flask_session import Session
from flaskps.config import Config
from flaskps.helpers import auth as helper_auth
from flaskps.helpers import permission as helper_permission

# Resources
from flaskps.resources import auth
from flaskps.resources import user

# Configuración inicial de la app
app = Flask(__name__)
app.config.from_object(Config)

# Server Side session
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Funciones que se exportan al contexto de Jinja2
app.jinja_env.globals.update(is_authenticated=helper_auth.authenticated,
                             has_permission=helper_permission.has_permission)

# Home
@app.route("/")
def index():
    return render_template('index.html')


# Autenticación
app.add_url_rule("/login", 'auth_login', auth.login)
app.add_url_rule("/logout", 'auth_logout', auth.logout)
app.add_url_rule(
    "/authenticate",
    'auth_authenticate',
    auth.authenticate,
    methods=['POST']
)


# Dashboard
app.add_url_rule("/dashboard", 'user_dashboard', user.dashboard)

