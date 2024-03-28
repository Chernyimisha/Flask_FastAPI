from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('male', 'Мужчина'), ('female', 'Женщина')])

# Валидация данных формы
# WTForms позволяет проводить валидацию данных формы. Для этого можно
# использовать готовые валидаторы, такие, как DataRequired, Email, Length и другие.
# Также можно написать свой собственный валидатор.


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

# В данном примере определен класс RegistrationForm, который наследуется от
# FlaskForm. Внутри класса определены три поля: email, password и confirm_password.
# Поле email проверяется на наличие данных и на соответствие формату email. Поле
# password проверяется на наличие данных и на минимальную длину (6 символов).
# Поле confirm_password проверяется на наличие данных и на соответствие значению
# поля password.
# 🔥 Важно! Для правильной работы кода необходимо отдельно установить
# валидатор электронной почты. Для этого достаточно выполнить команду:
# pip install email-validator


# WTForms предоставляет множество типов полей для формы. Вот некоторые из них:
# ● StringField — строковое поле для ввода текста;
# ● IntegerField — числовое поле для ввода целочисленных значений;
# ● FloatField — числовое поле для ввода дробных значений;
# ● BooleanField — чекбокс;
# ● SelectField — выпадающий список;
# ● DateField — поле для ввода даты;
# ● FileField — поле для загрузки файла.

