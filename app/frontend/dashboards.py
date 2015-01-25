from app import app, user_datastore

from flask import abort, render_template, redirect, request, flash, url_for
from flask.ext.security import current_user, login_user, logout_user
from flask.ext.security.utils import encrypt_password

from app.models import User

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/profile')
def profile():
    return render_template('profile.html',
                            email=current_user.email)