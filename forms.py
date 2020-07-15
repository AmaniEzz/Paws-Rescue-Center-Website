from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email,EqualTo , Length, ValidationError


def my_length_check(form, field):
    if len(field.data) > 50:
        raise ValidationError('Field must be less than 50 characters')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')


class SignupForm(FlaskForm):
    username = StringField('Full name', validators=[InputRequired(), my_length_check])
    email = StringField('Email', validators=[InputRequired(), Email(message="Invalid Email addresse")])
    password = PasswordField('Password', validators = [InputRequired()])
    confirm  = PasswordField('Confirm Password', validators = [InputRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Sign Up')

class AdoptationForm(FlaskForm):
    Fullname = StringField('Full name', validators=[InputRequired(), my_length_check])
    Adresse = StringField('Adresse', validators=[InputRequired()])
    reasone = PasswordField('Why do you want to adopt this pet?', validators = [InputRequired()])
    submit = SubmitField('Submit ')
