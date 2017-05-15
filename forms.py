from flask_wtf import Form
from wtforms import StringField, PasswordField, SelectField, DecimalField
from wtforms.validators import DataRequired, EqualTo, Length, NumberRange

import models

# Set your classes here.

from flask_wtf import FlaskForm

class RegisterForm(FlaskForm):
    name = StringField(
        'Username', validators=[DataRequired(), Length(min=6, max=25)]
    )
    email = StringField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )
    password = PasswordField(
        'Password', validators=[DataRequired(), Length(min=6, max=40)]
    )
    confirm = PasswordField(
        'Repeat Password',
        [DataRequired(),
        EqualTo('password', message='Passwords must match')]
    )


class LoginForm(FlaskForm):
    name = StringField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])


class ForgotForm(FlaskForm):
    email = StringField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )


class CreateTransaction(FlaskForm):
    user = SelectField(
        'Username',
        validators=[DataRequired()],
        choices=map(lambda user: (user.name, user.name), models.User.query.all())
    )
    amount = DecimalField(
        'Amount',
        places=2,
        validators=[
            DataRequired(),
            NumberRange(min=0)
        ]
    )
    description = StringField(
        'Description',
        validators=[Length(max=200)]
    )
