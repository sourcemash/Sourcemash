from . import bp

from flask import render_template, redirect


@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html')


@bp.route('/survey')
def survey():
    return redirect('http://goo.gl/forms/wmnCAcbrLp')


@bp.app_errorhandler(404)
def page_not_found(e):
    return redirect('/#404')
