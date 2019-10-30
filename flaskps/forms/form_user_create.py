from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectMultipleField
from wtforms.validators import InputRequired, DataRequired, Email, EqualTo


class UserCreateForm(FlaskForm):
    first_name = StringField('first_name', [InputRequired(message='Complete el nombre')])
    last_name = StringField('last_name', [InputRequired(message='Complete el apellido')])
    email = StringField('email', validators=[DataRequired(message='Complete el email'), Email(message='El email no es válido, verifique el campo')])
    username = StringField('username', [InputRequired(message='Complete el nombre de usuario')])
    password = PasswordField('password', validators=[DataRequired(message='Complete la contraseña')])
    confirm_password = PasswordField('confirm_password', validators=[DataRequired(message='Complete nuevamente la contraseña'), EqualTo('password', 'Las contraseñas deben coincidir, verifique los campos')])
    rol_id = SelectMultipleField('rol_id', coerce=int, validators=[InputRequired(message='Seleccione por lo menos un rol')])