from flask import Blueprint, render_template

from .extensions import db
from .wtf import RegisterForm

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

@main.route('/register')
def register():
    form = RegisterForm()
    return render_template('register.html', form=form)