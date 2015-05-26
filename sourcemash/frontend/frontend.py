from . import bp

from flask import render_template, redirect


@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html')


@bp.route('/survey')
def survey():
    return redirect('http://goo.gl/forms/wmnCAcbrLp')


@bp.route('/<path:dummy>')
def fallback(dummy):
    return redirect('/#' + dummy)
