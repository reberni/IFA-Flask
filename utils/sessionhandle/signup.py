#Forms
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, Email

def BuildSignUpForm():
    class SignUpForm(FlaskForm):
        username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
        email = StringField('Email', validators=[InputRequired(), Email()])
        password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=80)])
        confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
        submit = SubmitField('Sign Up')
    return SignUpForm