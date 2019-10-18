from os import path
from flask import Flask, render_template
from flask_session import Session
from flaskps.config import Config
from flaskps.helpers import auth as helper_auth, handler
from flaskps.helpers import permission as helper_permission
from flaskps.helpers import role as helper_role
from flaskps.helpers import site_settings as helper_site_settings

# Resources
from flaskps.resources import auth
from flaskps.resources import user
from flaskps.resources import dashboard

# Configuración inicial de la app
app = Flask(__name__)
app.config.from_object(Config)

# Server Side session
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Funciones que se exportan al contexto de Jinja2
app.jinja_env.globals.update(items_per_page=helper_site_settings.items_per_page(),
                             is_authenticated=helper_auth.authenticated,
                             has_permission=helper_permission.has_permission,
                             has_role=helper_role.has_role,
                             contact_email=helper_site_settings.email(),
                             maintenance_mode=helper_site_settings.maintenance_mode())

# Home
@app.route("/")
def index():
    return render_template('index.html', titulo=helper_site_settings.titulo(),
                           descripcion=helper_site_settings.descripcion())


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

# Usuarios
app.add_url_rule("/usuarios", 'user_list', dashboard.user_list)

app.add_url_rule("/crear-usuario", 'crear_usuario', user.create, methods=['POST'])

# Handlers
app.register_error_handler(404, handler.not_found_error)
app.register_error_handler(401, handler.unauthorized_error)
# TODO: Implementar lo mismo para el error 500 y 401

