from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, IntegerField
from wtforms.validators import InputRequired


class DocenteCreateForm(FlaskForm):
    telefono_numero = StringField("telefono_numero")
