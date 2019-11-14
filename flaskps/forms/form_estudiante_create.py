from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, IntegerField, DateTimeField
from wtforms.validators import InputRequired


class EstudianteCreateForm(FlaskForm):
    first_name = StringField(
        "first_name", [InputRequired(message="Complete el nombre")]
    )
    last_name = StringField(
        "last_name", [InputRequired(message="Complete el apellido")]
    )
    fecha_nacimiento = DateField(
        "fecha_nacimiento",
        format="%d/%m/%Y",
        validators=[InputRequired(message="Complete la fecha de nacimiento")],
    )
    select_localidad = SelectField("select_localidad")
    domicilio = StringField(
        "domicilio", [InputRequired(message="Complete el domicilio")]
    )
    select_barrio = SelectField(
        "select_barrio",
        coerce=int,
        validators=[InputRequired(message="Seleccione el barrio")],
    )
    select_genero = SelectField(
        "select_genero",
        coerce=int,
        validators=[InputRequired(message="Seleccione el género")],
    )
    select_tipo = SelectField(
        "select_tipo",
        validators=[InputRequired(message="Seleccione el tipo de documento")],
    )
    documento_numero = IntegerField(
        "documento_numero", [InputRequired(message="Ingrese su documento")]
    )
    """
    select_responsable = SelectField(
        "select_responsable",
        validators=[InputRequired(message="Seleccione el responsable a cargo")]
    )
    """
    telefono_numero = StringField("telefono_numero")
    select_escuela = SelectField(
        "select_escuela",
        coerce=int,
        validators=[InputRequired(message="Seleccione la escuela de la cual proviene")],
    )
    select_nivel = SelectField(
        "select_nivel",
        coerce=int,
        validators=[InputRequired(message="Seleccione el nivel")],
    )
