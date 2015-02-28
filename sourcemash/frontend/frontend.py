from . import bp

from flask import render_template
from flask.ext.security import current_user, login_required


@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html')

@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')