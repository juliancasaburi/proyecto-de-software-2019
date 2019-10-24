from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Email


class EmailUpdateForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
