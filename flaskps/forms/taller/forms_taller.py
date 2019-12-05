from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired


class TallerForm(FlaskForm):
    nombre = StringField("nombre", [InputRequired(message="Complete el nombre")])
    nombre_corto = StringField(
        "nombre_corto", [InputRequired(message="Complete el nombre")]
    )
