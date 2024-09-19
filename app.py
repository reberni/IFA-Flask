from dotenv import load_dotenv
import os
from flask import Flask, render_template, redirect, url_for, flash, jsonify


#Database
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from typing import List

#signin/signup
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from utils.user.usermodel import userModel
from utils.sessionhandle.signup import BuildSignUpForm
from utils.sessionhandle.signin import BuildSignInForm

#products
from utils.product.productform import ProductForm
from utils.product.productModel import productModel

from sqlalchemy.ext.declarative import declarative_base

#local
#from utils.user.usermodel import User
# from utils.db.model import initdb
# from app import db, app

load_dotenv()

class Base(DeclarativeBase):
  pass



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://reberni:asdf1234@localhost:3306/photographyequipment" #os.getenv("MYSQL")
app.config['SECRET_KEY'] = 'your_secret_key' 
db = SQLAlchemy(app)



Base = declarative_base()

class Userdata(db.Model):
    __tablename__ = 'userdata'
    id = db.mapped_column(db.Integer, primary_key=True)
    username = db.mapped_column(db.String(50), unique=True)
    email = db.mapped_column(db.String(120))
    password = db.mapped_column(db.String(500), nullable=False)
    active = db.mapped_column(db.Boolean, default=True)
    # One-to-Many relationship with Products
    ownedproducts: Mapped[List["Product"]] = db.relationship(back_populates="creator")

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    productname = db.mapped_column(db.String(50), unique=False)
    productdescription = db.mapped_column(db.String(500), unique=False)
    productprice = db.mapped_column(db.Integer, unique=False)
    productbrand = db.mapped_column(db.String(50), unique=False)
    # Foreign Key to link with User
    creator_id: Mapped[int] = mapped_column(db.ForeignKey("userdata.id"))
    # Relationship to User
    creator: Mapped["Userdata"] = db.relationship(back_populates="ownedproducts")



with app.app_context():
    db.create_all()




login_manager = LoginManager(app)
User = userModel(Userdata)
@login_manager.user_loader
def load_user(User_id):
    return User.query.get(int(User_id))

#Products = productModel(db.Model)


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
        return redirect(url_for('signin'))
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
        print(user)
        # Check if the user exists and the password is correct
        if user and check_password_hash(user.password, password):
            # Log in the user
            print("if")
            print(user.password)
            print (password)
            login = login_user(user)
            print(login)
            print(User)
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
    # Fetch all products and their related creator
    all_products = Product.query.all()
    print(all_products)
    # You can now access the creator through the relationship
    for product in all_products:
        print(f"Product: {product.productname}, Creator: {product}")
    
    return render_template('products.html', products=all_products)

# Route for creating a new product
@app.route('/newproduct', methods=['GET', 'POST'])
@login_required
def create_product():
    form = ProductForm()

    if form.validate_on_submit():
        # Create a new product object
        new_product = Product(
            productname=form.productname.data,
            productdescription=form.productdescription.data,
            productprice=form.productprice.data,
            productbrand=form.productbrand.data,
            creator_id=current_user.id # Link the current user as the creator
        )
        # Add the new product to the database
        db.session.add(new_product)
        db.session.commit()
        flash('Product successfully created!', 'success')
        return redirect(url_for('products'))

    return render_template('newproduct.html', form=form)

# Route for the products API (GET method)
@app.route('/api/products', methods=['GET'])
def get_products():
    # Fetch all products from the database
    all_products = Product.query.all()
    
    # Serialize the products data into a list of dictionaries
    products_list = [
        {
            'id': product.id,
            'name': product.productname,
            'description': product.productdescription,
            'price': product.productprice,
            'brand': product.productbrand,
            #'creatorID': product.productcreator,
            'creatorUsername' :product.creator.username  # Assuming this field exists
        } for product in all_products
    ]
    
    # Return the serialized data as JSON
    return jsonify(products_list)
# Route for the home page
@app.route('/')
def index():
    # Fetch all products from the database
    all_products = Product.query.all()
    
    # Render the template and pass the product data
    return render_template('index.html', products=all_products)

if __name__ == '__main__':
    app.run(debug=True)
