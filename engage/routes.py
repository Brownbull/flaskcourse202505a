from flask import Blueprint, render_template

from .extensions import db
from .wtf import RegisterForm

from werkzeug.utils import secure_filename
import os
from flask import current_app
UPLOAD_FOLDER = 'static/uploads'  # or your preferred path

main = Blueprint('main', __name__)
@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
def profile():
    return render_template('profile.html')

@main.route('/timeline')
def timeline():
    return render_template('timeline.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    
    if form.validate_on_submit():
        image_filename = None
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            # Get the absolute path to the static/uploads folder inside your app
            upload_folder = os.path.join(current_app.static_folder, 'uploads/photos')
            os.makedirs(upload_folder, exist_ok=True)
            image_path = os.path.join(upload_folder, filename)
            form.image.data.save(image_path)
            image_filename = filename
        # Save image_filename to your user model if needed
        return f'<h1>name: {form.name.data}, username: {form.username.data}, image: {image_filename}</h1>'

        return render_template('profile.html', form=form)
    return render_template('register.html', form=form)