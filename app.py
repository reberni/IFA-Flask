from dotenv import load_dotenv
import os
from flask import Flask, render_template, redirect, url_for, flash


#Database
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from utils.db.model import createDatabase

#signin/signup
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user
from utils.user.usermodel import userModel
from utils.sessionhandle.signup import BuildSignUpForm
from utils.sessionhandle.signin import BuildSignInForm

#local
#from utils.user.usermodel import User
# from utils.db.model import initdb
# from app import db, app

load_dotenv()

class Base(DeclarativeBase):
  pass

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("MYSQL")
app.config['SECRET_KEY'] = 'your_secret_key' 
db = SQLAlchemy(app)
createDatabase(db, app)

login_manager = LoginManager(app)
User = userModel(db.Model)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Define a simple sign-in form using Flask-WTF
SignInForm = BuildSignInForm()
# Define a simple sign-on form using Flask-WTF
SignUpForm = BuildSignUpForm()

# Route for the signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm() # Instantiate the SignUpForm
    if form.validate_on_submit():
        # Hash the password before storing it in the database
        hashed_password = generate_password_hash(form.password.data)
        # Create a new user object
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()
        flash('User successfully signed up!', 'success')
        return redirect(url_for('index'))
    return render_template('signup.html', form=form)


# Route for the sign-in page
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SignInForm()  # Instantiate the SignInForm

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Retrieve the user from the database based on the username
        user = User.query.filter_by(username=username).first()

        # Check if the user exists and the password is correct
        if user and check_password_hash(user.password, password):
            # Log in the user
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('index'))  # Redirect to the homepage

        # If the user doesn't exist or the password is incorrect, display an error message
        flash('Invalid username or password', 'error')

    return render_template('signin.html', form=form)  # Pass the form to the template

# Route for logout
@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

# Route for the profile page
@app.route('/profile')
@login_required # Profile page is only accessable for signed in users
def profile():
    return render_template('profile.html')

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
