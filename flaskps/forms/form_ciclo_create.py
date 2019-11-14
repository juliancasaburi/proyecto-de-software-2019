from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms import DateField
from wtforms.validators import InputRequired


class CicloCreateForm(FlaskForm):

    semestre = IntegerField(
        "semestre", [InputRequired(message="Ingrese el semestre")],
    )

    fecha_inicio = DateField(
        "fecha_inicio",
        validators=[InputRequired(message="Complete la fecha de inicio")],
    )

    fecha_fin = DateField(
        "fecha_fin",
        validators=[InputRequired(message="Complete la fecha de finalización")],
    )

