from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length
from DZ.dz03.modelsDB import User


class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])


