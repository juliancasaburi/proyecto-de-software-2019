from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, DataRequired


class LoginForm(FlaskForm):
    username = StringField(
        "username", [InputRequired(message="Complete el nombre de usuario")]
    )
    password = PasswordField(
        "password", validators=[DataRequired(message="Complete la contraseña")]
    )
