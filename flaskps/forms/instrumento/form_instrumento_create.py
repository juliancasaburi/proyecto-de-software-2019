from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import InputRequired
from flask_uploads import UploadSet, IMAGES
from flask_wtf.file import FileField, FileAllowed, FileRequired


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
        "photo",
        validators=[
            FileAllowed(images, "Solo se permiten imagenes!"),
        ],
    )
