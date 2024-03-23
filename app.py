from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from utils.db.model import initdb

class Base(DeclarativeBase):
  pass

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key' 
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://reberni:asdf1234@localhost:3306/photographyequipment" # Change this to a secret key of your choice
db = SQLAlchemy(model_class=Base)
db.init_app(app)
initdb()


# Define a simple sign-in form using Flask-WTF
class SignInForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=80)])
    submit = SubmitField('Sign In')

# Route for the sign-in page
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SignInForm()
    if form.validate_on_submit():
        # Here you can add code to check username and password against your database or any other storage
        # For demonstration, we'll just print them
        print(form.username.data + form.password.data)
        return redirect(url_for('index'))
    return render_template('signin.html', form=form)

# Route for the products page
@app.route('/products')
def products():
    return render_template('products.html')

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
