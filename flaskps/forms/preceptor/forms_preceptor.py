from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, IntegerField
from wtforms.validators import InputRequired

from flaskps.helpers.localidades import localidades
from flaskps.helpers.tipos_documento import tipos_documento
from flaskps.models.genero import Genero


class PreceptorForm(FlaskForm):
    username = StringField("username")
    nombre = StringField("nombre", [InputRequired(message="Complete el nombre")])
    apellido = StringField("nombre", [InputRequired(message="Complete el apellido")])
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

    def __init__(self, choices, *args, **kwargs):
        super(PreceptorForm, self).__init__(*args, **kwargs)
        self.select_genero.choices = choices["select_genero"]
        self.select_localidad.choices = choices["select_localidad"]
        self.select_tipo.choices = choices["select_tipo"]


def choices():
    choices_dict = dict()

    generos = Genero.all()
    choices_dict["select_genero"] = [(g["id"], g["nombre"]) for g in generos]

    locs = localidades()
    choices_dict["select_localidad"] = [(l["id"], l["nombre"]) for l in locs]

    tipos = tipos_documento()
    choices_dict["select_tipo"] = [(t["id"], t["nombre"]) for t in tipos]

    return choices_dict
