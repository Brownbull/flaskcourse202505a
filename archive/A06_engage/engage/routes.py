from flask import Blueprint, render_template, url_for, redirect, request, current_app, abort
from flask_login import login_user, current_user, login_required, logout_user
from datetime import datetime

from .extensions import db
from .forms import RegisterForm, LoginForm, PostForm
from .models import User, Post, followers

from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os
UPLOAD_FOLDER = 'static/uploads'

main = Blueprint('main', __name__)
@main.route('/')
def index():
    form = LoginForm()

    return render_template('index.html', form=form)

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
                image=image_url,
                join_date=datetime.now()  # Store the current date and time
            )
            login_user(new_user, remember=False)
            db.session.add(new_user)
            db.session.commit()


        return redirect(url_for('main.profile'))  # Redirect to 'profile.html', form=form)
    return render_template('register.html', form=form)

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

def get_user(username=None):
    """Get a user object by username or return the current user if None is passed."""
    if username:
        user = User.query.filter_by(username=username).first_or_404()
    else:
        user = current_user

    return user

def get_users_to_watch(current_user):
    """Get a list of users to watch (not including the current user)."""
    users_to_watch = []
    users_to_watch_limit = 4

    for user in User.query.order_by(db.func.random()).all():
        if user != current_user:
            users_to_watch.append(user)
            if len(users_to_watch) == users_to_watch_limit:
                break

    return users_to_watch

def get_user_posts(user):
    return Post.query.filter_by(user=user).order_by(Post.date_created.desc()).all()

def get_user_following_posts(user):
    return Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)
        ).filter(
            followers.c.follower_id == user.id
        ).order_by(
            Post.date_created.desc()
        ).all()
def get_followed_by(user):
    return user.followed_by.all()

def set_display_follow(user, followed_by):
    if current_user == user:
        return "self"
    elif current_user in followed_by:
        return "following"
    else:
        return "not following"

@main.route('/profile', defaults = {'username': None})
@main.route('/profile/<username>')
def profile(username):
    
    user = get_user(username)
    activity_posts_qty = 5

    posts = get_user_posts(user)[:activity_posts_qty]
    followed_by = get_followed_by(user)
    display_follow = set_display_follow(user, followed_by)
    who_to_watch = get_users_to_watch(user)

    return render_template('profile.html', 
        current_user=user, 
        posts=posts, 
        followed_by=followed_by, 
        display_follow=display_follow, 
        who_to_watch=who_to_watch)

@main.route('/timeline', defaults = {'username': None})
@main.route('/timeline/<username>')
@login_required
def timeline(username):
    
    form = PostForm()
    current_time = datetime.now()

    user = get_user(username)

    user_posts = get_user_posts(user)
    followed_by = get_followed_by(user)
    user_following_posts = get_user_following_posts(user)
    who_to_watch = get_users_to_watch(user)

    return render_template('timeline.html', 
        form=form, 
        current_user=user, 
        user_posts=user_posts, 
        user_following_posts = user_following_posts,
        current_time=current_time,
        who_to_watch=who_to_watch,
        followed_by=followed_by)

@main.route('/new_post', methods=['POST'])
@login_required
def new_post():
    form = PostForm()

    if form.validate():
        content = form.content.data
        if content:
            new_post = Post(user_id=current_user.id, content=content, date_created=datetime.now())
            db.session.add(new_post)
            db.session.commit()
            return redirect(url_for('main.timeline'))
    return render_template('timeline.html', form=form, current_user=current_user, error='Post content is required')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main.route('/follow/<username>')
@login_required
def follow(username):
    user_to_follow = User.query.filter_by(username=username).first()
    if user_to_follow:
        current_user.following.append(user_to_follow)
        db.session.commit()
    return redirect(url_for('main.profile', username=username))

@main.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user_to_unfollow = User.query.filter_by(username=username).first()
    if user_to_unfollow:
        current_user.following.remove(user_to_unfollow)
        db.session.commit()
    return redirect(url_for('main.profile', username=username))
