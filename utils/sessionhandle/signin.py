from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length

def BuildSignInForm():
    class SignInForm(FlaskForm):
        username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
        password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=80)])
        submit = SubmitField('Sign In')
    return SignInForm