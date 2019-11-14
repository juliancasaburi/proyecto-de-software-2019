from flask import (
    render_template,
    session,
    abort,
    request,
)
from flaskps.db import get_db
from flaskps.helpers import permission
from flask import jsonify, make_response
from flaskps.helpers.tipos_documento import tipos_documento
from flaskps.helpers.localidades import localidades

from flaskps.models.role import Role
from flaskps.models import siteconfig
from flaskps.models.genero import Genero
from flaskps.models.siteconfig import SiteConfig


def user_table():
    if not permission.has_permission("usuario_index", session):
        abort(401)

    Role.db = get_db()
    roles = Role.all()

    return render_template("user/actions/usuarios.html", roles=roles)


def user_edit_form():
    if not permission.has_permission("usuario_update", session):
        abort(401)

    Role.db = get_db()
    roles = Role.all()

    return render_template("user/actions/usuario_editar.html", roles=roles)


def user_destroy_form():
    if not permission.has_permission("usuario_destroy", session):
        abort(401)

    Role.db = get_db()
    roles = Role.all()

    return render_template("user/actions/usuario_eliminar.html", roles=roles)


def user_new_form():
    if not permission.has_permission("usuario_new", session):
        abort(401)

    Role.db = get_db()
    roles = Role.all()

    return render_template("user/actions/usuario_crear.html", roles=roles)


def maintenance_mode():
    if not permission.has_permission("config_update", session):
        abort(401)

    SiteConfig.db = get_db()
    config = siteconfig.get_config()
    modo_mantenimiento = config["modo_mantenimiento"]

    if modo_mantenimiento == 0:
        siteconfig.update_maintenance(1)
    else:
        siteconfig.update_maintenance(0)

    config = siteconfig.get_config()
    modo_mantenimiento = config["modo_mantenimiento"]

    data = {"modo_mantenimiento": modo_mantenimiento}
    return make_response(jsonify(data), 200)


def config_update():
    if not permission.has_permission("config_update", session):
        abort(401)

    params = request.form.to_dict()

    SiteConfig.db = get_db()

    data = {"msg": "Configuración actualizada exitosamente"}

    success = siteconfig.update_config(params)

    if success:
        return make_response(jsonify(data), 200)
    else:
        data = {"msg": "Ha ocurrido un error al actualizar la configuración"}
        return make_response(jsonify(data), 500)


def docente_table():
    if not permission.has_permission("docente_index", session):
        abort(401)

    Genero.db = get_db()
    generos = Genero.all()

    return render_template(
        "user/actions/docentes.html",
        localidades=localidades(),
        tipodoc=tipos_documento(),
        generos=generos,
    )
