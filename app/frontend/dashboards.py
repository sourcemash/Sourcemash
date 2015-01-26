from app import app

from flask import abort, render_template, redirect
from flask.ext.security import current_user, login_required

from app.models import User

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html',
                            email=current_user.email)