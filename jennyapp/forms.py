from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import FileField, StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import InputRequired, DataRequired, Length, EqualTo

ALLOWED_IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif', 'bmp']

