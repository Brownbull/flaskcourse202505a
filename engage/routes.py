from flask import Blueprint, render_template, url_for, redirect, request
from flask_login import login_user, current_user

from .extensions import db
from .wtf import RegisterForm, LoginForm
from .models import User

from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os
from flask import current_app
UPLOAD_FOLDER = 'static/uploads'  # or your preferred path

main = Blueprint('main', __name__)
@main.route('/')
def index():
    form = LoginForm()

    return render_template('index.html', form=form)

@main.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return redirect(url_for('main.index'))
    
    error = None
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)  # Assuming you have a login_user function to handle user login
            # User authenticated successfully
            return redirect(url_for('main.profile'))
        else:
            return render_template('index.html', form=form, error='Invalid username or password')
    return render_template('index.html', form=form)

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
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            # Get the absolute path to the static/uploads folder inside your app
            upload_folder = os.path.join(current_app.static_folder, 'uploads/photos')
            os.makedirs(upload_folder, exist_ok=True)
            image_path = os.path.join(upload_folder, filename)
            form.image.data.save(image_path)
            image_url = url_for('static', filename=f'uploads/photos/{filename}', _external=True)

            new_user = User(
                name=form.name.data,
                username=form.username.data,
                password=generate_password_hash(form.password.data),
                image=image_url
            )
            db.session.add(new_user)
            db.session.commit()


        return redirect(url_for('main.profile'))  # Redirect to 'profile.html', form=form)
    return render_template('register.html', form=form)