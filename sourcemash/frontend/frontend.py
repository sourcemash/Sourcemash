from . import bp

from flask import render_template


@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html')
