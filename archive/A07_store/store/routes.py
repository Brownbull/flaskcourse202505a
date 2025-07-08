from flask import Blueprint, render_template, url_for, redirect, request, current_app, abort
from flask_login import login_user, current_user, login_required, logout_user
from datetime import datetime

from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os
UPLOAD_FOLDER = 'static/uploads'

from .extensions import db

store = Blueprint('store', __name__)
@store.route('/')
def index():
    return render_template('index.html')

@store.route('/product')
def product():
    return render_template('view-product.html')

@store.route('/cart')
def cart():
    return render_template('cart.html')

@store.route('/checkout')
def checkout():
    return render_template('checkout.html')

@store.route('/admin')
def admin():
    return render_template('admin/index.html', admin=True)

@store.route('/admin/add')
def add():
    return render_template('admin/add-product.html', admin=True)

@store.route('/admin/order')
def order():
    return render_template('admin/view-order.html', admin=True)