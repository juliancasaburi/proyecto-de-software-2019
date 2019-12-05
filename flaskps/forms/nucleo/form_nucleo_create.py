from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField
from wtforms.validators import InputRequired


class NucleoCreateForm(FlaskForm):
    nombre = StringField("nombre", [InputRequired(message="Complete el nombre")])
    direccion = StringField(
        "direccion", [InputRequired(message="Complete la dirección")]
    )
    telefono = StringField("telefono", [InputRequired(message="Complete el teléfono")])
    lat = DecimalField("lat", [InputRequired(message="Complete la latitud")])
    lng = DecimalField("lng", [InputRequired(message="Complete la longitud")])
