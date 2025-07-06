from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import FileField, StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired, DataRequired, Length, EqualTo

ALLOWED_IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif', 'bmp']

class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired('Name is required'), Length(max=80, message='Name must be less than 80 characters')])
    username = StringField('Username', validators=[InputRequired('Username is required'), Length(max=80, message='Username must be less than 80 characters')])
    password = PasswordField('Password', validators=[InputRequired('Password is required'), Length(min=6, max=120, message='Password must be between 6 and 120 characters')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired('Password is required'), EqualTo('password')])
    image = FileField('Profile Image', validators=[FileAllowed(ALLOWED_IMAGE_EXTENSIONS, 'Images only!')])
    # submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired('Username is required'), Length(max=80, message='Username must be less than 80 characters')])
    password = PasswordField('Password', validators=[InputRequired('Password is required'), Length(min=6, max=120, message='Password must be between 6 and 120 characters')])
    remember_me = BooleanField('Remember Me', default=False)
    # submit = SubmitField('Login')