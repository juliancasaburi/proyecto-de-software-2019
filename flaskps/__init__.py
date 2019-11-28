from flask import Flask, render_template
from flask_session import Session

from flaskps.config import Config
from flaskps.helpers import auth as helper_auth, handler
from flaskps.helpers import permission as helper_permission
from flaskps.helpers import role as helper_role
from flaskps.models import siteconfig as sc
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
from flask_mail import Mail

# Configuración inicial de la app
app = Flask(__name__)
app.config.from_object(Config)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["JSON_AS_ASCII"] = False
# Mail Config
app.config["MAIL_SERVER"] = Config.MAIL_SERVER
app.config["MAIL_PORT"] = Config.MAIL_PORT
app.config["MAIL_USERNAME"] = Config.MAIL_USERNAME
app.config["MAIL_PASSWORD"] = Config.MAIL_PASSWORD
app.config["MAIL_USE_TLS"] = Config.MAIL_USE_TLS
app.config["MAIL_USE_SSL"] = Config.MAIL_USE_SSL
# Server Side session
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
csrf = CSRFProtect(app)
bcrypt = Bcrypt(app)
mail = Mail(app)

# Resources
from flaskps.resources import auth, ciclo_lectivo
from flaskps.resources import user
from flaskps.resources import role
from flaskps.resources import docente
from flaskps.resources import taller
from flaskps.resources import estudiante
from flaskps.resources import siteconfig

# Funciones que se exportan al contexto de Jinja2
app.jinja_env.globals.update(
    is_authenticated=helper_auth.authenticated,
    has_permission=helper_permission.has_permission,
    has_role=helper_role.has_role,
)


@app.context_processor
def utility_processor():
    def siteconf():
        return sc.get_config()

    return dict(siteconfig=siteconf())


# Home
@app.route("/")
def index():
    return render_template("index.html")


# Autenticación
app.add_url_rule("/login", "auth_login", auth.login)
app.add_url_rule("/logout", "auth_logout", auth.logout)
app.add_url_rule(
    "/authenticate", "auth_authenticate", auth.authenticate, methods=["POST"]
)

# Cuenta
app.add_url_rule("/perfil", "user_profile", user.profile)
app.add_url_rule(
    "/perfil/actualizar_email", "user_email_update", user.email_update, methods=["POST"]
)
app.add_url_rule(
    "/perfil/actualizar_contraseña",
    "user_password_update",
    user.password_update,
    methods=["POST"],
)

# Dashboard
app.add_url_rule("/dashboard", "user_dashboard", user.dashboard)

# Configuracion del sitio
app.add_url_rule(
    "/mantenimiento", "maintenance", siteconfig.maintenance_mode, methods=["POST"],
)
app.add_url_rule(
    "/configuracion/actualizar",
    "config_update",
    siteconfig.config_update,
    methods=["POST"],
)

# Roles
app.add_url_rule("/roles", "roles", role.all_roles, methods=["GET"])

# Forms
app.add_url_rule("/usuario/crear", "user_new_form", user.user_new_form)
app.add_url_rule("/usuario/editar", "user_edit_form", user.user_edit_form)
app.add_url_rule("/usuario/bloquear", "user_destroy_form", user.user_destroy_form)
app.add_url_rule("/taller/crear", "taller_new_form", taller.taller_new_form)

# Usuarios
app.add_url_rule("/usuario", "user", user.user_data)
app.add_url_rule("/tablausuarios", "user_table", user.user_table)
app.add_url_rule(
    "/usuarios_serverside_table",
    "user_serverside_table_content",
    user.serverside_table_content,
)
app.add_url_rule("/usuarios", "user_all", user.get_users)
app.add_url_rule("/usuario/crear", "user_new", user.create, methods=["POST"])
app.add_url_rule("/usuario/bloquear", "user_destroy", user.destroy, methods=["POST"])
app.add_url_rule("/usuario/actualizar", "user_update", user.update, methods=["POST"])

# Docentes
app.add_url_rule("/docente", "docente", docente.data)
app.add_url_rule("/tabladocentes", "docente_table", docente.docente_table)
app.add_url_rule(
    "/docente_serverside_table",
    "docente_serverside_table_content",
    docente.serverside_table_content,
)
app.add_url_rule("/docentes", "docente_all", docente.get_docentes)
app.add_url_rule("/docentes/crear", "docente_new", docente.create, methods=["POST"])
app.add_url_rule("/docente/baja", "docente_destroy", docente.destroy, methods=["POST"])
app.add_url_rule(
    "/docente/actualizar", "docente_update", docente.update, methods=["POST"]
)

# Talleres
app.add_url_rule("/taller/crear", "taller_new", taller.create, methods=["POST"])
app.add_url_rule("/taller/ciclos", "taller_ciclos", taller.get_ciclos)
app.add_url_rule(
    "/taller/asociar/ciclo", "taller_set_ciclo", taller.set_ciclo, methods=["POST"]
)
app.add_url_rule(
    "/taller/asociar/ciclo", "taller_set_ciclo_form", taller.taller_set_ciclo_form
)
app.add_url_rule(
    "/taller/asociar/docentes",
    "taller_set_docentes_form",
    taller.taller_set_docentes_form,
)
app.add_url_rule(
    "/taller_ciclo/docentes", "taller_ciclo_docentes", taller.get_docentes_ciclo
)
app.add_url_rule(
    "/taller/asociar/docentes",
    "taller_set_docentes",
    taller.set_docentes,
    methods=["POST"],
)
app.add_url_rule(
    "/taller_ciclo/estudiantes",
    "taller_ciclo_estudiantes",
    taller.get_estudiantes_ciclo,
)
app.add_url_rule(
    "/taller/asociar/estudiantes",
    "taller_set_estudiantes_form",
    taller.taller_set_estudiantes_form,
)
app.add_url_rule(
    "/taller/asociar/estudiantes",
    "taller_set_estudiantes",
    taller.set_estudiantes,
    methods=["POST"],
)

# Ciclos lectivos
app.add_url_rule(
    "/ciclolectivo/crear", "ciclo_new", ciclo_lectivo.create, methods=["POST"]
)
app.add_url_rule("/tabla_ciclos_lectivos", "ciclo_table", ciclo_lectivo.ciclo_table)
app.add_url_rule("/ciclos", "ciclo_all", ciclo_lectivo.get_ciclos)
app.add_url_rule("/ciclo/talleres", "ciclo_talleres", ciclo_lectivo.get_talleres)
app.add_url_rule(
    "/ciclos/baja", "ciclo_destroy", ciclo_lectivo.destroy, methods=["POST"]
)

# Handlers
app.register_error_handler(404, handler.not_found_error)
app.register_error_handler(401, handler.unauthorized_error)
app.register_error_handler(500, handler.internal_server_error)

# Estudiantes
app.add_url_rule("/estudiante", "estudiante", estudiante.estudiante_data)
app.add_url_rule("/tablaestudiantes", "estudiante_table", estudiante.estudiante_table)
app.add_url_rule("/estudiantes", "estudiante_all", estudiante.get_estudiantes)
app.add_url_rule(
    "/estudiantes/crear", "estudiante_new", estudiante.create, methods=["POST"]
)
app.add_url_rule(
    "/estudiante/actualizar", "estudiante_update", estudiante.update, methods=["POST"]
)
app.add_url_rule(
    "/estudiante/baja", "estudiante_destroy", estudiante.destroy, methods=["POST"]
)
