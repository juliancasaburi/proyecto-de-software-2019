from datetime import datetime

from flask import (
    request,
    session,
    abort,
    make_response,
    jsonify,
    flash,
    json,
    render_template,
)
from flaskps.db import get_db

from flaskps.forms.estudiante.form_estudiante_create import EstudianteCreateForm

from flaskps.models.estudiante import Estudiante
from flaskps.models.barrio import Barrio
from flaskps.models.escuela import Escuela
from flaskps.models.genero import Genero
from flaskps.models.nivel import Nivel
from flaskps.models.responsable_tipo import Responsable_tipo
from flaskps.models import siteconfig

from flaskps.helpers.permission import has_permission
from flaskps.helpers.role import has_role

from flaskps.helpers.tipos_documento import tipo_documento
from flaskps.helpers.localidades import localidad
from flaskps.helpers.localidades import localidades
from flaskps.helpers.tipos_documento import tipos_documento


def get_estudiantes():
    s_config = siteconfig.get_config()
    if not has_permission("estudiante_index", session) or (
        s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    Estudiante.db = get_db()
    estudiantes = Estudiante.all()

    for dict_item in estudiantes:
        dict_item["fecha_nac"] = dict_item["fecha_nac"].strftime("%d-%m-%Y")
        loc = localidad(dict_item["localidad_id"])
        dict_item["localidad"] = loc["nombre"]
        del dict_item["localidad_id"]
        dict_item["género"] = dict_item["g.nombre"]
        del dict_item["g.nombre"]
        dict_item["escuela"] = dict_item["es.nombre"]
        del dict_item["es.nombre"]
        dict_item["barrio"] = dict_item["b.nombre"]
        del dict_item["b.nombre"]
        tipo_doc = tipo_documento(dict_item["tipo_doc_id"])
        dict_item["tipo_doc"] = tipo_doc["nombre"]
        del dict_item["tipo_doc_id"]
        dict_item["numero_doc"] = dict_item["numero"]
        del dict_item["numero"]
        if "tel" not in dict_item:
            dict_item["tel"] = "No tiene"
        dict_item["nivel"] = dict_item["n.nombre"]
        del dict_item["n.nombre"]
        dict_item["responsable"] = dict_item["r.nombre"]
        del dict_item["r.nombre"]
        dict_item["created_at"] = dict_item["created_at"].strftime("%d-%m-%Y %H:%M:%S")
        dict_item["updated_at"] = dict_item["updated_at"].strftime("%d-%m-%Y %H:%M:%S")

    estudiantes = jsonify(estudiantes)

    return make_response(estudiantes, 200)


def pasarChoices(form):
    db = get_db()
    locs = localidades()
    Barrio.db = db
    barrios = Barrio.all()
    Genero.db = db
    generos = Genero.all()
    tipos_doc = tipos_documento()
    Escuela.db = db
    escuelas = Escuela.all()
    Nivel.db = db
    niveles = Nivel.all()
    Responsable_tipo.db = db
    responsables_tipos = Responsable_tipo.all()

    # choices de los selects
    form.select_localidad.choices = [
        (localidad["id"], localidad["nombre"]) for localidad in locs
    ]
    form.select_barrio.choices = [
        (barrio["id"], barrio["nombre"]) for barrio in barrios
    ]
    form.select_genero.choices = [
        (genero["id"], genero["nombre"]) for genero in generos
    ]
    form.select_tipo.choices = [(tipo["id"], tipo["nombre"]) for tipo in tipos_doc]
    form.select_escuela.choices = [
        (escuela["id"], escuela["nombre"]) for escuela in escuelas
    ]
    form.select_nivel.choices = [(nivel["id"], nivel["nombre"]) for nivel in niveles]
    form.select_responsable_tipo.choices = [
        (responsable_tipo["id"], responsable_tipo["nombre"])
        for responsable_tipo in responsables_tipos
    ]

    return form


def create():
    s_config = siteconfig.get_config()
    if not has_permission("estudiante_new", session) or (
        s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    form = EstudianteCreateForm()
    form = pasarChoices(form)

    op_response = dict()
    responsecode = 201

    if form.validate_on_submit():
        params = request.form.to_dict()
        params["fecha_nacimiento"] = datetime.strptime(
            params["fecha_nacimiento"], "%d/%m/%Y"
        ).date()

        Estudiante.db = get_db()
        created = Estudiante.create(params)

        if created:
            op_response["msg"] = "Se ha agregado al estudiante exitosamente"
            op_response["type"] = "success"
        else:
            op_response["msg"] = "Ha ocurrido un error al crear al estudiante"
            op_response["type"] = "error"
            abort(make_response(jsonify(op_response), 409))

    else:
        if len(form.errors) >= 2:
            op_response["msg"] = "Complete todos los datos del nuevo estudiante"
            op_response["type"] = "error"
        else:
            error_msg = "".join(list(form.errors.values())[0]).strip("'[]")
            op_response["msg"] = error_msg
            op_response["type"] = "error"

        abort(make_response(jsonify(op_response), 500))

    return make_response(jsonify(op_response), responsecode)


def update():
    s_config = siteconfig.get_config()
    if not has_permission("estudiante_update", session) or (
        s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    form = EstudianteCreateForm()  # uso este porq es igual
    form = pasarChoices(form)

    op_response = dict()
    responsecode = 201

    if form.validate_on_submit():
        params = request.form.to_dict()
        params["fecha_nacimiento"] = datetime.strptime(
            params["fecha_nacimiento"], "%d/%m/%Y"
        ).date()

        Estudiante.db = get_db()

        updated = Estudiante.update(params)

        if updated:
            op_response["msg"] = "Se ha modificado al estudiante con éxito"
            op_response["type"] = "success"
        else:
            op_response["msg"] = "Ocurrió un error"
            op_response["type"] = "error"
            abort(make_response(jsonify(op_response), 409))

    else:
        if len(form.errors) >= 2:
            op_response["msg"] = "Complete todos los datos del estudiante a modificar"
            op_response["type"] = "error"
        else:
            error_msg = "".join(list(form.errors.values())[0]).strip("'[]")
            op_response["msg"] = error_msg
            op_response["type"] = "error"

        abort(make_response(jsonify(op_response), 500))

    return make_response(jsonify(op_response), responsecode)


def destroy():
    s_config = siteconfig.get_config()
    if not has_permission("estudiante_destroy", session) or (
        s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    params = json.loads(request.data)
    eid = params["id"]
    activo = params["activo"]

    Estudiante.db = get_db()
    success = Estudiante.delete(eid)

    op_response = dict()
    responsecode = 200

    if success:
        condicion = "bloqueado" if activo else "activado"
        op_response["msg"] = "Se ha " + condicion + " al estudiante exitosamente"
        op_response["type"] = "success"
    else:
        condicion = "bloquear" if activo else "activar"
        op_response["msg"] = "El estudiante a " + condicion + " no existe"
        op_response["type"] = "error"
        responsecode = 404

    return make_response(jsonify(op_response), responsecode)


# por id
def estudiante_data():
    s_config = siteconfig.get_config()
    if not has_permission("estudiante_show", session) or (
        s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    if request.args.get("id"):
        Estudiante.db = get_db()
        eid = request.args.get("id")
        estudiante = Estudiante.find_by_id(eid)
        if estudiante != None:
            # lo tuve que pasar a string desde acá
            estudiante["fecha_nac"] = datetime.strftime(
                estudiante["fecha_nac"], "%d/%m/%Y"
            )
            data = jsonify(estudiante)
            return make_response(data, 200)
        else:
            flash("El estudiante con ID:" + eid + "no existe.", "error")
            return abort(404)

    else:
        abort(400)


def estudiante_table():
    if not has_permission("estudiante_index", session):
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
        "tables/estudiantes.html",
        localidades=loc,
        tipodoc=tipo_doc,
        generos=generos,
        barrios=barrios,
        escuelas=escuelas,
        niveles=niveles,
        responsables_tipos=responsables_tipos,
    )
