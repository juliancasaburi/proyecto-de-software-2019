from datetime import datetime

from flask import (
    request,
    session,
    abort,
    make_response,
    jsonify,
    json,
    render_template,
)

from flaskps.forms.estudiante import forms_estudiante
from flaskps.forms.estudiante.forms_estudiante import EstudianteForm
from flaskps.helpers.localidades import localidad
from flaskps.helpers.localidades import localidades
from flaskps.helpers.permission import has_permission
from flaskps.helpers.role import has_role
from flaskps.helpers.tipos_documento import tipo_documento
from flaskps.helpers.tipos_documento import tipos_documento
from flaskps.models import siteconfig
from flaskps.models.barrio import Barrio
from flaskps.models.escuela import Escuela
from flaskps.models.estudiante import Estudiante
from flaskps.models.genero import Genero
from flaskps.models.nivel import Nivel
from flaskps.models.responsable_tipo import Responsable_tipo


def get_estudiantes():
    s_config = siteconfig.get_config()
    if not has_permission("estudiante_index", session) or (
        s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

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


def new():
    s_config = siteconfig.get_config()
    if not has_permission("estudiante_new", session) or (
        s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    # Instanciar el form de WTForm para la validación
    select_field_choices = forms_estudiante.crud_choices()
    form = EstudianteForm(select_field_choices)

    op_response = dict()

    if form.validate_on_submit():
        params = request.form.to_dict()
        params["fecha_nacimiento"] = datetime.strptime(
            params["fecha_nacimiento"], "%d/%m/%Y"
        ).date()

        created = Estudiante.create(params)

        if created:
            op_response["msg"] = "Se ha agregado al estudiante exitosamente"
            op_response["type"] = "success"
        else:
            op_response["msg"] = "Ha ocurrido un error al crear al estudiante"
            op_response["type"] = "error"
            abort(make_response(jsonify(op_response), 422))

    else:
        if len(form.errors) >= 2:
            op_response["msg"] = "Complete todos los datos del nuevo estudiante"
            op_response["type"] = "error"
        else:
            error_msg = "".join(list(form.errors.values())[0]).strip("'[]")
            op_response["msg"] = error_msg
            op_response["type"] = "error"

        abort(make_response(jsonify(op_response), 400))

    return make_response(jsonify(op_response), 201)


def update():
    s_config = siteconfig.get_config()
    if not has_permission("estudiante_update", session) or (
        s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    # Instanciar el form de WTForm para la validación
    select_field_choices = forms_estudiante.crud_choices()
    form = EstudianteForm(select_field_choices)

    op_response = dict()

    if form.validate_on_submit():
        params = request.form.to_dict()
        params["fecha_nacimiento"] = datetime.strptime(
            params["fecha_nacimiento"], "%d/%m/%Y"
        ).date()

        updated = Estudiante.update(params)

        if updated:
            op_response["msg"] = "Se ha modificado al estudiante con éxito"
            op_response["type"] = "success"
        else:
            op_response["msg"] = "Ocurrió un error"
            op_response["type"] = "error"
            abort(make_response(jsonify(op_response), 422))

    else:
        if len(form.errors) >= 2:
            op_response["msg"] = "Complete todos los datos del estudiante a modificar"
            op_response["type"] = "error"
        else:
            error_msg = "".join(list(form.errors.values())[0]).strip("'[]")
            op_response["msg"] = error_msg
            op_response["type"] = "error"

        abort(make_response(jsonify(op_response), 400))

    return make_response(jsonify(op_response), 200)


def destroy():
    s_config = siteconfig.get_config()
    if not has_permission("estudiante_destroy", session) or (
        s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    params = json.loads(request.data)
    eid = params["id"]

    success = Estudiante.delete(eid)

    op_response = dict()

    activo = params["activo"]

    if success:
        condicion = "bloqueado" if activo else "activado"
        op_response["msg"] = "Se ha " + condicion + " al estudiante exitosamente"
        op_response["type"] = "success"
    else:
        condicion = "bloquear" if activo else "activar"
        op_response["msg"] = "El estudiante a " + condicion + " no existe"
        op_response["type"] = "error"
        abort(jsonify(op_response), 422)

    return make_response(jsonify(op_response), 204)


# por id
def estudiante_data():
    s_config = siteconfig.get_config()
    if not has_permission("estudiante_show", session) or (
        s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    id = request.args.get("id")
    if id:

        estudiante = Estudiante.find_by_id(id)

        if estudiante is not None:
            # lo tuve que pasar a string desde acá
            estudiante["fecha_nac"] = datetime.strftime(
                estudiante["fecha_nac"], "%d/%m/%Y"
            )
            data = jsonify(estudiante)
            return make_response(data, 200)
        else:
            abort(422)
    else:
        abort(400)


def estudiante_table():
    s_config = siteconfig.get_config()
    if not has_permission("estudiante_index", session) or (
        s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    loc = localidades()

    tipo_doc = tipos_documento()

    generos = Genero.all()

    barrios = Barrio.all()

    niveles = Nivel.all()

    responsables_tipos = Responsable_tipo.all()

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
