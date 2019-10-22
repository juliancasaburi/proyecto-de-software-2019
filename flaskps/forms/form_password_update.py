from flask_wtf import FlaskForm
from wtforms import PasswordField
from wtforms.validators import DataRequired, EqualTo


class PasswordUpdateForm(FlaskForm):
    password = PasswordField('password', validators=[DataRequired()])
    confirm_password = PasswordField('confirm_password', validators=[DataRequired(), EqualTo('password')])
