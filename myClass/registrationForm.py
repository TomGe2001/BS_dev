from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Create a Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Your Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


