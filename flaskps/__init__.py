from flask import Flask, render_template
from flask_session import Session
from flaskps.config import Config
from flaskps.helpers import auth as helper_auth, handler
from flaskps.helpers import permission as helper_permission
from flaskps.helpers import role as helper_role

# Resources
from flaskps.resources import auth
from flaskps.resources import user
from flaskps.resources import dashboard

# Configuración inicial de la app
app = Flask(__name__)
app.config.from_object(Config)
app.config.from_pyfile('config/config.cfg')
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Server Side session
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Funciones que se exportan al contexto de Jinja2
app.jinja_env.globals.update(is_authenticated=helper_auth.authenticated,
                             has_permission=helper_permission.has_permission,
                             has_role=helper_role.has_role)

@app.context_processor
def utility_processor():
    app.config.from_pyfile('config/config.cfg')
    def maintenance_mode():
        return app.config['MODO_MANTENIMIENTO']

    def email():
        return app.config['EMAIL_CONTACTO']

    def titulo():
        return app.config['TITULO']

    def descripcion():
        return app.config['DESCRIPCION']

    def items_per_page():
        return app.config['ITEMS_POR_PAGINA']

    return dict(maintenance_mode=maintenance_mode(),
                email=email(),
                titulo=titulo(),
                descripcion=descripcion(),
                items_per_page=items_per_page())

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

# Configuracion del sitio
app.add_url_rule("/mantenimiento", 'maintenance', dashboard.maintenance_mode, methods=['POST'])

# Usuarios
app.add_url_rule("/usuarios", 'user_list', dashboard.user_list)
app.add_url_rule("/usuario/crear", 'user_new_form', dashboard.user_new_form)
app.add_url_rule("/usuario/crear", 'user_new', user.create, methods=['POST'])

# Handlers
app.register_error_handler(404, handler.not_found_error)
app.register_error_handler(401, handler.unauthorized_error)
# TODO: Implementar lo mismo para el error 500 y 401

