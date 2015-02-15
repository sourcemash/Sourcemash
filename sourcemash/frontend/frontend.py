from . import bp

from flask import render_template
from flask.ext.security import current_user, login_required


@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html')

@bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html',
                            email=current_user.email)

@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')