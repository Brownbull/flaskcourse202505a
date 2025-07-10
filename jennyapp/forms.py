from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import FileField, StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import InputRequired, DataRequired, Length, EqualTo

ALLOWED_IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif', 'bmp']

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired('Email is required'), Length(max=120, message='Email must be less than 120 characters')])
    password = PasswordField('Password', validators=[InputRequired('Password is required'), Length(min=6, max=120, message='Password must be between 6 and 120 characters')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired('Password is required'), EqualTo('password')])

