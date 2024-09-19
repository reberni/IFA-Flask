from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class ProductForm(FlaskForm):
    productname = StringField('Product Name', validators=[DataRequired()])
    productdescription = StringField('Product Description', validators=[DataRequired()])
    productprice = IntegerField('Product Price ($)', validators=[DataRequired(), NumberRange(min=0, message="Price must be a positive number.")])
    productbrand = StringField('Product Brand', validators=[DataRequired()])
    submit = SubmitField('Add Product')