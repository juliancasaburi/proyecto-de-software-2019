import os
from flaskps import app
from werkzeug.utils import secure_filename
from flask import render_template, request, session, abort, make_response, jsonify
from flaskps.db import get_db

from flaskps.forms.instrumento.form_instrumento_create import InstrumentoCreateForm

from flaskps.models import siteconfig
from flaskps.models.instrumento import Instrumento

from flaskps.helpers.permission import has_permission
from flaskps.helpers.role import has_role


def instrumento_new_form():
    if not has_permission("instrumento_new", session):
        abort(401)

    # Tipos de instrumentos para el select
    Instrumento.db = get_db()
    tipos_instrumento = Instrumento.tipos_instrumento()

    return render_template(
        "user/actions/instrumento_crear.html", tipos=tipos_instrumento
    )


def create():
    s_config = siteconfig.get_config()
    if not has_permission("ciclolectivo_new", session) or (
        s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    form = InstrumentoCreateForm()

    # Tipos de instrumentos para el select
    Instrumento.db = get_db()
    tipos_instrumento = Instrumento.tipos_instrumento()

    form.tipo_id.choices = [
        (tipo_instrumento["id"], tipo_instrumento["nombre"])
        for tipo_instrumento in tipos_instrumento
    ]

    op_response = dict()
    responsecode = 201

    if form.validate_on_submit():
        params = request.form.to_dict()

        # Si el usuario seleccionó una imagen
        if request.files["photo"].filename != "":
            f = form.photo.data
            filename = secure_filename(f.filename)
            imagepath = os.path.join(app.config["UPLOADED_IMAGES_DEST"], filename)
            f.save(imagepath)
            params["image_path"] = imagepath

        Instrumento.db = get_db()
        created = Instrumento.create(params)

        if created:
            op_response["msg"] = "Se ha registrado el Instrumento exitosamente"
            op_response["type"] = "success"
        else:
            op_response["msg"] = "Ha ocurrido un error al registrar el Instrumento"
            op_response["type"] = "error"
            abort(make_response(jsonify(op_response), 409))

    else:
        if len(form.errors) >= 2:
            op_response["msg"] = "Complete todos los datos del Instrumento"
            op_response["type"] = "error"
        else:
            error_msg = "".join(list(form.errors.values())[0]).strip("'[]")
            op_response["msg"] = error_msg
            op_response["type"] = "error"

        abort(make_response(jsonify(op_response), 500))

    return make_response(jsonify(op_response), responsecode)
