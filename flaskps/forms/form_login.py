from flask import flash
from flask_wtf import FlaskForm
from wtforms import ValidationError, StringField, PasswordField
from wtforms.validators import InputRequired, DataRequired, Email


class LoginForm(FlaskForm):
    username = StringField('username', [InputRequired(message='Complete el nombre de usuario')])
    password = PasswordField('password', validators=[DataRequired(message='Complete la contraseña')])