from . import bp

from flask import render_template, url_for


@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html')

@bp.route('/login')
def login():
    return redirect(url_for('index'))
