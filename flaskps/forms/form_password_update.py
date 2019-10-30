from flask_wtf import FlaskForm
from wtforms import PasswordField
from wtforms.validators import DataRequired, EqualTo


class PasswordUpdateForm(FlaskForm):
    password = PasswordField('password', validators=[DataRequired(message='Complete la contraseña')])
    confirm_password = PasswordField('confirm_password', validators=[DataRequired(message='Complete ambos campos, y recuerde que deben ser iguales'), EqualTo('password', 'Las contraseñas deben coincidir, verifique los campos')])
