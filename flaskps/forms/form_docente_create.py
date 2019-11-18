from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, IntegerField
from wtforms.validators import InputRequired


class DocenteCreateForm(FlaskForm):
    nombre = StringField(
        "nombre", [InputRequired(message="Complete el nombre")]
    )
    apellido = StringField(
        "nombre", [InputRequired(message="Complete el apellido")]
    )
    select_genero = SelectField(
        "select_genero",
        coerce=int,
        validators=[InputRequired(message="Seleccione el género")],
    )
    fecha_nacimiento = DateField(
        "fecha_nacimiento",
        format="%d/%m/%Y",
        validators=[InputRequired(message="Complete la fecha de nacimiento")],
    )
    select_localidad = SelectField(
        "select_localidad",
        validators=[InputRequired(message="Seleccione la localidad")],
    )
    domicilio = StringField(
        "domicilio", [InputRequired(message="Complete el domicilio")]
    )
    select_tipo = SelectField(
        "select_tipo",
        validators=[InputRequired(message="Seleccione el tipo de documento")],
    )
    documento_numero = IntegerField(
        "documento_numero", [InputRequired(message="Ingrese su documento")]
    )
