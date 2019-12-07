from flaskps.db import get_db
from flaskps.models.tipo_instrumento import TipoInstrumento

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import InputRequired
from flask_uploads import UploadSet, IMAGES
from flask_wtf.file import FileField, FileAllowed

images = UploadSet("images", IMAGES)


class InstrumentoCreateForm(FlaskForm):
    nombre = StringField("nombre", [InputRequired(message="Complete el nombre")])
    tipo_id = SelectField(
        "tipo_id", coerce=int, validators=[InputRequired(message="Seleccione el tipo")],
    )
    num_inventario = StringField(
        "num_inventario", [InputRequired(message="Complete el numero de inventario")]
    )
    photo = FileField(
        "photo", validators=[FileAllowed(images, "Solo se permiten imagenes!")],
    )

    def __init__(self, choices, *args, **kwargs):
        super(InstrumentoCreateForm, self).__init__(*args, **kwargs)
        self.tipo_id.choices = choices["tipo_id"]


def crud_choices():
    Tipo
    tipos_instrumento = TipoInstrumento.all()

    choices = dict()
    choices["tipo_id"] = [
        (tipo_instrumento["id"], tipo_instrumento["nombre"])
        for tipo_instrumento in tipos_instrumento
    ]
    return choices
