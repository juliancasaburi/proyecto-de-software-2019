from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, IntegerField
from wtforms.validators import InputRequired


class DocenteUpdateForm(FlaskForm):
    nombre = StringField("nombre", [InputRequired(message="Complete el nombre")])
    apellido = StringField("apellido", [InputRequired(message="Complete el apellido")])
    fecha_nacimiento = DateField(
        "fecha_nacimiento",
        format="%d/%m/%Y",
        validators=[InputRequired(message="Complete la fecha de nacimiento")],
    )
    domicilio = StringField(
        "domicilio", [InputRequired(message="Complete el domicilio")],
    )
    documento_numero = IntegerField(
        "documento_numero", [InputRequired(message="Ingrese su documento")],
    )
    select_genero = IntegerField(
        "select_genero", [InputRequired(message="Seleccione el género")],
    )
    select_localidad = IntegerField(
        "select_localidad", [InputRequired(message="Seleccione la localidad")],
    )
    select_tipo = IntegerField(
        "select_tipo", [InputRequired(message="Seleccione el tipo de documento")],
    )
