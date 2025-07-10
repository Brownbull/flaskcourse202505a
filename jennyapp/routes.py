from flask import Blueprint, render_template, url_for, redirect, request, current_app, abort
from flask_login import login_user, current_user, login_required, logout_user
from datetime import datetime

from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os
UPLOAD_FOLDER = 'static/uploads'

from .extensions import db
from .forms import RegisterForm, LoginForm, PatientForm
from .models import User

main = Blueprint('main', __name__)
@main.route('/')
def index():
    return render_template('index.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    form = RegisterForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            error = "Email address already exists. Please use a different email."
        else:
            register_user = User(
                email=form.email.data,
                password=form.password.data,
                join_date=datetime.now()
            )
            db.session.add(register_user)
            db.session.commit()
            login_user(register_user, remember=False) 
            return redirect(url_for('main.dashboard'))
        
    context = {
        'form': form,
        'error': error
    }
    return render_template('register.html', **context)

@main.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user or not user.verify_password(form.password.data):
            error = 'Invalid username or password'
        else:
            login_user(user, remember=form.remember_me.data) 
            return redirect(url_for('main.dashboard'))

    context = {
        'form': form,
        'error': error,
    }
    return render_template('login.html', **context)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard/dashboard.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('dashboard/profile.html')

@main.route('/activity')
@login_required
def activity():
    return render_template('dashboard/activity.html')

@main.route('/patients')
@login_required
def patients():
    return render_template('dashboard/patients/pat_index.html')

@main.route('/add_patient', methods=['GET', 'POST'])
@login_required
def add_patient():
    error = None
    form = PatientForm()

    if form.validate_on_submit():
        print(f"full_name: {form.full_name.data}")
        print(f"date_of_birth: {form.date_of_birth.data}")
        print(f"gender: {form.gender.data}")
        print(f"email: {form.email.data}")
        print(f"phone_number: {form.phone_number.data}")
        print(f"address: {form.address.data}")
        print(f"adresss2: {form.adresss2.data}")
        print(f"city: {form.city.data}")
        print(f"region: {form.region.data}")
        print(f"zip_code: {form.zip_code.data}")
        print(f"country: {form.country.data}")
        print(f"notifications: {form.notifications.data}")
        

        # patient = User(
        #     full_name = form.full_name.data,
        #     date_of_birth = form.date_of_birth.data,
        #     gender = form.gender.data,
        #     email = form.email.data,
        #     phone = form.phone.data,
        #     address = form.address.data,
        #     join_date = datetime.now()
        # )
        # db.session.add(patient)
        # db.session.commit()
        return redirect(url_for('main.patients'))
    
    context = {
        'form': form,
        'error': error
    }
    return render_template('dashboard/patients/pat_add.html', **context)

@main.route('/session')
@login_required
def session():
    return render_template('dashboard/session.html')

@main.route('/calendar')
@login_required
def calendar():
    return render_template('dashboard/calendar.html')

@main.route('/documents')
@login_required
def documents():
    return render_template('dashboard/documents.html')
