from flask import Blueprint, render_template, url_for, redirect, request, current_app, abort
from flask_login import login_user, current_user, login_required, logout_user
from datetime import datetime

from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os
UPLOAD_FOLDER = 'static/uploads'

from .extensions import db

main = Blueprint('main', __name__)
@main.route('/')
def index():
    return render_template('index.html')

@main.route('/register')
def register():
    return render_template('register.html')

@main.route('/login')
def login():
    return render_template('login.html')

@main.route('/dashboard')
def dashboard():
    return render_template('dashboard/dashboard.html')

@main.route('/profile')
def profile():
    return render_template('dashboard/profile.html')

@main.route('/activity')
def activity():
    return render_template('dashboard/activity.html')

@main.route('/patients')
def patients():
    return render_template('dashboard/patients.html')

@main.route('/session')
def session():
    return render_template('dashboard/session.html')

@main.route('/calendar')
def calendar():
    return render_template('dashboard/calendar.html')

@main.route('/documents')
def documents():
    return render_template('dashboard/documents.html')
