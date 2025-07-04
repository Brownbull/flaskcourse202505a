from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user

from dashboard.extensions import db
from dashboard.models import User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    error = ""
    if request.method == 'POST':
        email_address = request.form.get('email_address')
        password = request.form.get('password')
        remember_me = True if request.form.get('remember_me') == 'on' else False

        user = User.query.filter_by(email_address=email_address).first()

        if not user or not user.verify_password(password):
            error = "Invalid email address or password. Please try again."
        
        if error:
            return render_template('login.html', error=error)
        else:
            login_user(user, remember = remember_me)
            return redirect(url_for('main.index'))

    return render_template('login.html', error=error)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    error = ""
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email_address = request.form.get('email_address')
        password1 = request.form.get('password')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email_address=email_address).first()
        password_match = password1 == password2

        if user:
            error = "Email address already exists. Please use a different email."
        elif not password_match:
            error = "Passwords do not match. Please try again."

        if error:
            return render_template('register.html', error=error)
        
        else:
            user = User(
                name=first_name + ' ' + last_name,
                email_address=email_address,
                password=password1
            )

            db.session.add(user)
            db.session.commit()

            return redirect(url_for('auth.login'))

    return render_template('register.html', error=error)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))