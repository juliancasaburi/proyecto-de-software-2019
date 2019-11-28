from flask import (
    render_template,
    session,
    abort,
)
from flaskps.db import get_db
from flaskps.helpers import permission

from flaskps.helpers.tipos_documento import tipos_documento
from flaskps.helpers.localidades import localidades

from flaskps.models.barrio import Barrio
from flaskps.models.escuela import Escuela
from flaskps.models.nivel import Nivel
from flaskps.models.role import Role
from flaskps.models.genero import Genero
from flaskps.models.taller import Taller
from flaskps.models.ciclo_lectivo import CicloLectivo
from flaskps.models.docente import Docente
from flaskps.models.estudiante import Estudiante
from flaskps.models.responsable_tipo import Responsable_tipo


def user_table():
    if not permission.has_permission("usuario_index", session):
        abort(401)

    Role.db = get_db()
    roles = Role.all()

    return render_template("user/actions/lists/usuarios.html", roles=roles)


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

    return render_template("user/actions/usuario_bloquear.html", roles=roles)


def user_new_form():
    if not permission.has_permission("usuario_new", session):
        abort(401)

    Role.db = get_db()
    roles = Role.all()

    return render_template("user/actions/usuario_crear.html", roles=roles)


def docente_table():
    if not permission.has_permission("docente_index", session):
        abort(401)

    Genero.db = get_db()
    generos = Genero.all()

    return render_template(
        "user/actions/lists/docentes.html",
        localidades=localidades(),
        tipodoc=tipos_documento(),
        generos=generos,
    )


def taller_new_form():
    if not permission.has_permission("taller_new", session):
        abort(401)

    return render_template("user/actions/taller_crear.html")


def estudiante_table():
    if not permission.has_permission("estudiante_index", session):
        abort(401)

    loc = localidades()

    tipo_doc = tipos_documento()

    Genero.db = get_db()
    generos = Genero.all()

    Barrio.db = get_db()
    barrios = Barrio.all()

    Nivel.db = get_db()
    niveles = Nivel.all()

    Responsable_tipo.db = get_db()
    responsables_tipos = Responsable_tipo.all()

    Escuela.db = get_db()
    escuelas = Escuela.all()

    return render_template(
        "user/actions/lists/estudiantes.html",
        localidades=loc,
        tipodoc=tipo_doc,
        generos=generos,
        barrios=barrios,
        escuelas=escuelas,
        niveles=niveles,
        responsables_tipos=responsables_tipos,
    )


def taller_set_ciclo_form():
    if not permission.has_permission("taller_update", session):
        abort(401)

    Taller.db = get_db()
    talleres = Taller.all()

    CicloLectivo.db = get_db()
    ciclos = CicloLectivo.all()

    for ciclo in ciclos:
        ciclo["fecha_ini"] = ciclo["fecha_ini"].strftime("%d-%m-%Y")
        ciclo["fecha_fin"] = ciclo["fecha_fin"].strftime("%d-%m-%Y")

    return render_template(
        "user/actions/taller_asociar_ciclo.html", talleres=talleres, ciclos=ciclos
    )


def taller_set_docentes_form():
    if not permission.has_permission("taller_update", session):
        abort(401)

    CicloLectivo.db = get_db()
    ciclos = CicloLectivo.all()

    Docente.db = get_db()
    docentes = Docente.all()

    for ciclo in ciclos:
        ciclo["fecha_ini"] = ciclo["fecha_ini"].strftime("%d-%m-%Y")
        ciclo["fecha_fin"] = ciclo["fecha_fin"].strftime("%d-%m-%Y")

    return render_template(
        "user/actions/taller_asociar_docentes.html", ciclos=ciclos, docentes=docentes
    )


def taller_set_estudiantes_form():
    if not permission.has_permission("taller_update", session):
        abort(401)

    CicloLectivo.db = get_db()
    ciclos = CicloLectivo.all()

    Estudiante.db = get_db()
    estudiantes = Estudiante.all()

    for ciclo in ciclos:
        ciclo["fecha_ini"] = ciclo["fecha_ini"].strftime("%d-%m-%Y")
        ciclo["fecha_fin"] = ciclo["fecha_fin"].strftime("%d-%m-%Y")

    return render_template(
        "user/actions/taller_asociar_estudiantes.html",
        ciclos=ciclos,
        estudiantes=estudiantes,
    )


def ciclo_table():
    if not permission.has_permission("ciclolectivo_index", session):
        abort(401)

    CicloLectivo.db = get_db()
    ciclos = CicloLectivo.all()

    for ciclo in ciclos:
        ciclo["fecha_ini"] = ciclo["fecha_ini"].strftime("%d-%m-%Y")
        ciclo["fecha_fin"] = ciclo["fecha_fin"].strftime("%d-%m-%Y")

    return render_template("user/actions/lists/ciclos.html", ciclos=ciclos)
