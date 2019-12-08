import os
from datetime import datetime

from flask import render_template, request, session, abort, make_response, jsonify
from werkzeug.utils import secure_filename

from flaskps import app
from flaskps.forms.instrumento import forms_instrumento
from flaskps.forms.instrumento.forms_instrumento import InstrumentoCreateForm
from flaskps.helpers.permission import has_permission
from flaskps.helpers.role import has_role
from flaskps.models import siteconfig
from flaskps.models.instrumento import Instrumento
from flaskps.models.tipo_instrumento import TipoInstrumento


def get_instrumentos():
    s_config = siteconfig.get_config()
    if not has_permission("instrumento_index", session) or (
        s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    instrumentos = Instrumento.all()

    for dict_item in instrumentos:
        tipo_instrumento = TipoInstrumento.find_by_id(dict_item["tipo_id"])
        dict_item["tipo"] = tipo_instrumento["nombre"]
        del dict_item["tipo_id"]
        dict_item["created_at"] = dict_item["created_at"].strftime("%d-%m-%Y %H:%M:%S")
        if dict_item["updated_at"] is not None:
            dict_item["updated_at"] = dict_item["updated_at"].strftime(
                "%d-%m-%Y %H:%M:%S"
            )
        else:
            dict_item["updated_at"] = "Nunca"

    instrumentos = jsonify(instrumentos)

    return make_response(instrumentos, 200)


# por id
def instrumento_data():
    s_config = siteconfig.get_config()
    if not has_permission("instrumento_show", session) or (
        s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    if request.args.get("id"):

        eid = request.args.get("id")
        instrumento = Instrumento.find_by_id(eid)
        if instrumento is not None:
            data = jsonify(instrumento)
            return make_response(data, 200)
        else:
            return abort(404)
    else:
        abort(400)


def new():
    s_config = siteconfig.get_config()
    if not has_permission("instrumento_new", session) or (
        s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    # Instanciar el form de WTForm para la validación
    choices = forms_instrumento.crud_choices()
    form = InstrumentoCreateForm(choices)

    op_response = dict()

    if form.validate_on_submit():
        params = request.form.to_dict()

        # Si el usuario seleccionó una imagen
        if request.files["photo"].filename != "":
            f = form.photo.data
            parts = f.filename.split(".")
            filename = (
                "".join(parts[:-1])
                + "_"
                + datetime.now().strftime("%d-%m-%Y_%I-%M-%S_%p")
                + "."
                + parts[-1]
            )
            filename = secure_filename(filename)
            imagepath = os.path.join(app.config["UPLOADED_IMAGES_DEST"], filename)
            f.save(imagepath)
            params["image_name"] = filename

        created = Instrumento.create(params)

        if created:
            op_response["msg"] = "Se ha registrado el Instrumento exitosamente"
            op_response["type"] = "success"
        else:
            op_response["msg"] = "Ha ocurrido un error al registrar el Instrumento"
            op_response["type"] = "error"
            abort(make_response(jsonify(op_response), 422))

    else:
        if len(form.errors) >= 2:
            op_response["msg"] = "Complete todos los datos del Instrumento"
            op_response["type"] = "error"
        else:
            error_msg = "".join(list(form.errors.values())[0]).strip("'[]")
            op_response["msg"] = error_msg
            op_response["type"] = "error"

        abort(make_response(jsonify(op_response), 400))

    return make_response(jsonify(op_response), 201)


def update():
    s_config = siteconfig.get_config()
    if not has_permission("instrumento_update", session) or (
        s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    # Instanciar el form de WTForm para la validación
    choices = forms_instrumento.crud_choices()
    form = InstrumentoCreateForm(choices)

    op_response = dict()

    if form.validate_on_submit():
        params = request.form.to_dict()

        # Si el usuario seleccionó una imagen
        if request.files["photo"].filename != "":
            if Instrumento.image_name(params["id"])["image_name"]:
                # Eliminar la foto anterior
                old_image_path = os.path.join(
                    app.config["UPLOADED_IMAGES_DEST"],
                    Instrumento.image_name(params["id"])["image_name"],
                )
                try:
                    os.remove(old_image_path)
                except FileNotFoundError:
                    print(old_image_path + " no existe.")
            f = form.photo.data
            parts = f.filename.split(".")
            filename = (
                "".join(parts[:-1])
                + "_"
                + datetime.now().strftime("%d-%m-%Y_%I-%M-%S_%p")
                + "."
                + parts[-1]
            )
            filename = secure_filename(filename)
            imagepath = os.path.join(app.config["UPLOADED_IMAGES_DEST"], filename)
            f.save(imagepath)
            params["image_name"] = filename

        updated = Instrumento.update(params)

        if updated:
            op_response["msg"] = "Se ha modificado al Instrumento con éxito"
            op_response["type"] = "success"
        else:
            op_response["msg"] = "Ocurrió un error"
            op_response["type"] = "error"
            abort(make_response(jsonify(op_response), 422))

    else:
        if len(form.errors) >= 2:
            op_response["msg"] = "Complete todos los datos del Instrumento a modificar"
            op_response["type"] = "error"
        else:
            error_msg = "".join(list(form.errors.values())[0]).strip("'[]")
            op_response["msg"] = error_msg
            op_response["type"] = "error"

        abort(make_response(jsonify(op_response), 400))

    return make_response(jsonify(op_response), 201)


def instrumento_table():
    s_config = siteconfig.get_config()
    if not has_permission("instrumento_index", session) or (
        s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    # Tipos de instrumentos para el select
    tipos_instrumento = TipoInstrumento.all()

    return render_template("tables/instrumentos.html", tipos=tipos_instrumento)


def instrumento_info():
    s_config = siteconfig.get_config()
    if not has_permission("instrumento_show", session) or (
        s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    id_instrumento = request.args.get("id")

    instrumento = Instrumento.find_by_id(id_instrumento)

    if instrumento:
        # Tipo del instrumento
        tipo = TipoInstrumento.find_by_id(instrumento["tipo_id"])
        instrumento["tipo"] = tipo["nombre"]
        instrumento["created_at"] = instrumento["created_at"].strftime(
            "%d-%m-%Y %H:%M:%S"
        )
        if instrumento["updated_at"] is not None:
            instrumento["updated_at"] = instrumento["updated_at"].strftime(
                "%d-%m-%Y %H:%M:%S"
            )
        else:
            instrumento["updated_at"] = "Nunca"

        # Tipos de instrumentos para el select
        tipos_instrumento = TipoInstrumento.all()

        return render_template(
            "user/instrumento.html", instrumento=instrumento, tipos=tipos_instrumento
        )
    else:
        abort(404)
