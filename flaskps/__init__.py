import os

from flask import Flask, render_template
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_session import Session
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_wtf.csrf import CSRFProtect

import flaskps.resources.helpers.serverside_dt.serverside_table_docente
import flaskps.resources.helpers.serverside_dt.serverside_table_preceptor
import flaskps.resources.helpers.serverside_dt.serverside_table_user
from flaskps.config import Config
from flaskps.helpers import auth as helper_auth, handler
from flaskps.helpers import permission as helper_permission
from flaskps.helpers import role as helper_role
from flaskps.models import siteconfig as sc

# ----------------- App Config -----------------
app = Flask(__name__)
app.config.from_object(Config)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["JSON_AS_ASCII"] = False
# Flask Uploads
app.config["UPLOADED_FILES_DEST"] = os.path.join(app.root_path, "static/uploads")
app.config["UPLOADED_IMAGES_DEST"] = os.path.join(app.root_path, "static/uploads")
images = UploadSet("images", IMAGES)
configure_uploads(app, images)
# Mail Config
app.config["MAIL_SERVER"] = Config.MAIL_SERVER
app.config["MAIL_PORT"] = Config.MAIL_PORT
app.config["MAIL_USERNAME"] = Config.MAIL_USERNAME
app.config["MAIL_PASSWORD"] = Config.MAIL_PASSWORD
app.config["MAIL_USE_TLS"] = Config.MAIL_USE_TLS
app.config["MAIL_USE_SSL"] = Config.MAIL_USE_SSL
mail = Mail(app)
# Server Side session
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
# CSRF
csrf = CSRFProtect(app)
# BCRYPT
bcrypt = Bcrypt(app)
# ---------------- .App Config -----------------

# Resources
from flaskps.resources import auth, ciclo_lectivo, nucleo, administracion
from flaskps.resources import user
from flaskps.resources import role
from flaskps.resources import docente
from flaskps.resources import preceptor
from flaskps.resources import taller
from flaskps.resources import estudiante
from flaskps.resources import instrumento
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


# Home/Index
@app.route("/")
def index():
    return render_template("index.html")


# Error Handlers
app.register_error_handler(404, handler.not_found_error)
app.register_error_handler(401, handler.unauthorized_error)
app.register_error_handler(500, handler.internal_server_error)

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

# Auth
app.add_url_rule("/logout", "auth_logout", auth.logout)
app.add_url_rule(
    "/authenticate", "auth_authenticate", auth.authenticate, methods=["POST"]
)

# Cuenta/Perfil
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
app.add_url_rule("/panel", "user_dashboard", user.dashboard)

# Roles
app.add_url_rule("/roles", "roles", role.all_roles, methods=["GET"])

# Forms
app.add_url_rule("/login", "auth_login", auth.login)
app.add_url_rule("/taller/alta", "taller_new_form", taller.taller_new_form)
app.add_url_rule(
    "/taller/asociar/ciclo", "taller_set_ciclo_form", taller.taller_set_ciclo_form
)
app.add_url_rule(
    "/taller/asociar/docentes",
    "taller_set_docentes_form",
    taller.taller_set_docentes_form,
)
app.add_url_rule(
    "/taller/asociar/estudiantes",
    "taller_set_estudiantes_form",
    taller.taller_set_estudiantes_form,
)

# User
app.add_url_rule("/usuario", "user", user.user_data)
app.add_url_rule("/tablausuarios", "user_table", user.user_table)
app.add_url_rule(
    "/usuarios_serverside_table",
    "user_serverside_table_content",
    flaskps.resources.helpers.serverside_dt.serverside_table_user.serverside_table_content,
)
app.add_url_rule("/usuario/alta", "user_new", user.new, methods=["POST"])
app.add_url_rule("/usuario/bloquear", "user_destroy", user.destroy, methods=["POST"])
app.add_url_rule("/usuario/actualizar", "user_update", user.update, methods=["POST"])

# Docente
app.add_url_rule("/docente", "docente", docente.data)
app.add_url_rule("/tabladocentes", "docente_table", docente.docente_table)
app.add_url_rule(
    "/docente_serverside_table",
    "docente_serverside_table_content",
    flaskps.resources.helpers.serverside_dt.serverside_table_docente.serverside_table_content,
)
app.add_url_rule("/docente/alta", "docente_new", docente.new, methods=["POST"])
app.add_url_rule("/docente/baja", "docente_destroy", docente.destroy, methods=["POST"])
app.add_url_rule(
    "/docente/actualizar", "docente_update", docente.update, methods=["POST"]
)

# Preceptor
app.add_url_rule("/preceptor", "preceptor", preceptor.data)
app.add_url_rule("/tablapreceptores", "preceptor_table", preceptor.preceptor_table)
app.add_url_rule(
    "/preceptor_serverside_table",
    "preceptor_serverside_table_content",
    flaskps.resources.helpers.serverside_dt.serverside_table_preceptor.serverside_table_content,
)
app.add_url_rule("/preceptor/alta", "preceptor_new", preceptor.new, methods=["POST"])
app.add_url_rule(
    "/preceptor/baja", "preceptor_destroy", preceptor.destroy, methods=["POST"]
)
app.add_url_rule(
    "/preceptor/actualizar", "preceptor_update", preceptor.update, methods=["POST"]
)

# Taller
app.add_url_rule("/taller/alta", "taller_new", taller.new, methods=["POST"])
app.add_url_rule("/taller", "taller", taller.data)
app.add_url_rule("/taller/ciclos", "taller_ciclos", taller.get_ciclos)
app.add_url_rule("/tablatalleres", "taller_table", taller.taller_table)
app.add_url_rule("/talleres", "taller_all", taller.get_talleres)
app.add_url_rule("/taller/actualizar", "taller_update", taller.update, methods=["POST"])
app.add_url_rule(
    "/taller/asociar/ciclo", "taller_set_ciclo", taller.set_ciclo, methods=["POST"]
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
    "taller_set_estudiantes",
    taller.set_estudiantes,
    methods=["POST"],
)

# CicloLectivo
app.add_url_rule("/ciclolectivo/alta", "ciclo_new", ciclo_lectivo.new, methods=["POST"])
app.add_url_rule("/tabla_ciclos_lectivos", "ciclo_table", ciclo_lectivo.ciclo_table)
app.add_url_rule("/ciclos", "ciclo_all", ciclo_lectivo.get_ciclos)
app.add_url_rule("/ciclo/talleres", "ciclo_talleres", ciclo_lectivo.get_talleres)
app.add_url_rule(
    "/ciclos/baja", "ciclo_destroy", ciclo_lectivo.destroy, methods=["POST"]
)

# Estudiante
app.add_url_rule("/estudiante", "estudiante", estudiante.estudiante_data)
app.add_url_rule("/tablaestudiantes", "estudiante_table", estudiante.estudiante_table)
app.add_url_rule("/estudiantes", "estudiante_all", estudiante.get_estudiantes)
app.add_url_rule(
    "/estudiantes/alta", "estudiante_new", estudiante.new, methods=["POST"]
)
app.add_url_rule(
    "/estudiante/actualizar", "estudiante_update", estudiante.update, methods=["POST"]
)
app.add_url_rule(
    "/estudiante/baja", "estudiante_destroy", estudiante.destroy, methods=["POST"]
)

# Instrumento
app.add_url_rule(
    "/instrumento/alta", "instrumento_new", instrumento.new, methods=["POST"]
)
app.add_url_rule(
    "/instrumento_informacion", "instrumento_info", instrumento.instrumento_info
)
app.add_url_rule("/instrumento", "instrumento", instrumento.instrumento_data)
app.add_url_rule(
    "/tablainstrumentos", "instrumento_table", instrumento.instrumento_table
)
app.add_url_rule("/instrumentos", "instrumento_all", instrumento.get_instrumentos)
app.add_url_rule(
    "/instrumento/actualizar",
    "instrumento_update",
    instrumento.update,
    methods=["POST"],
)

# Módulo administrativo
app.add_url_rule("/administracion", "administracion", administracion.administracion)
app.add_url_rule(
    "/administracion/docente/talleres",
    "administracion_docente_talleres",
    administracion.docente_talleres,
)
app.add_url_rule(
    "/administracion/docente/taller/ciclos",
    "administracion_docente_taller_ciclos",
    administracion.ciclos_taller_docente,
)
app.add_url_rule(
    "/administracion/docente/taller/ciclo/nucleo/dias",
    "administracion_docente_taller_ciclo_nucleo_dias",
    administracion.dias_nucleo_ciclo_taller_docente,
)
app.add_url_rule(
    "/docente/asociar_horario",
    "docente_set_horario",
    administracion.docente_set_horario,
    methods=["POST"],
)

# Nucleo
app.add_url_rule("/nucleo/alta", "nucleo_new", nucleo.new, methods=["POST"])
"""
app.add_url_rule(
    "/nucleo_informacion", "nucleo_info", nucleo.nucleo_info
)
"""
app.add_url_rule("/nucleo", "nucleo", nucleo.nucleo_data)
app.add_url_rule("/tablanucleos", "nucleo_table", nucleo.nucleo_table)
app.add_url_rule("/nucleos", "nucleo_all", nucleo.get_nucleos)
app.add_url_rule("/nucleos_activos", "nucleo_activos", nucleo.get_nucleos_activos)
app.add_url_rule(
    "/nucleo/actualizar", "nucleo_update", nucleo.update, methods=["POST"],
)
app.add_url_rule("/nucleo/baja", "nucleo_destroy", nucleo.destroy, methods=["POST"])
