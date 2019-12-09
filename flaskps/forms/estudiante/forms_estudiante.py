from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, IntegerField
from wtforms.validators import InputRequired

from flaskps.helpers.localidades import localidades
from flaskps.helpers.tipos_documento import tipos_documento
from flaskps.models.barrio import Barrio
from flaskps.models.escuela import Escuela
from flaskps.models.genero import Genero
from flaskps.models.nivel import Nivel
from flaskps.models.responsable_tipo import Responsable_tipo


class EstudianteForm(FlaskForm):
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
    select_localidad = SelectField(
        "select_localidad", validators=[InputRequired(message="Complete la localidad")]
    )
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
    select_responsable_tipo = SelectField(
        "select_responsable_tipo",
        coerce=int,
        validators=[InputRequired(message="Seleccione el responsable a cargo")],
    )
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

    def __init__(self, choices, *args, **kwargs):
        super(EstudianteForm, self).__init__(*args, **kwargs)
        self.select_localidad.choices = choices["select_localidad"]
        self.select_barrio.choices = choices["select_barrio"]
        self.select_genero.choices = choices["select_genero"]
        self.select_tipo.choices = choices["select_tipo"]
        self.select_responsable_tipo.choices = choices["select_responsable_tipo"]
        self.select_escuela.choices = choices["select_escuela"]
        self.select_nivel.choices = choices["select_nivel"]


def crud_choices():
    locs = localidades()
    barrios = Barrio.all()
    generos = Genero.all()
    tipos_doc = tipos_documento()
    escuelas = Escuela.all()
    niveles = Nivel.all()
    responsables_tipos = Responsable_tipo.all()

    choices = dict()
    choices["select_localidad"] = [
        (localidad["id"], localidad["nombre"]) for localidad in locs
    ]
    choices["select_barrio"] = [(barrio["id"], barrio["nombre"]) for barrio in barrios]
    choices["select_genero"] = [(genero["id"], genero["nombre"]) for genero in generos]
    choices["select_tipo"] = [(tipo["id"], tipo["nombre"]) for tipo in tipos_doc]
    choices["select_escuela"] = [
        (escuela["id"], escuela["nombre"]) for escuela in escuelas
    ]
    choices["select_nivel"] = [(nivel["id"], nivel["nombre"]) for nivel in niveles]
    choices["select_responsable_tipo"] = [
        (responsable_tipo["id"], responsable_tipo["nombre"])
        for responsable_tipo in responsables_tipos
    ]

    return choices
