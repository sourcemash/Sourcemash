from flask import Blueprint, abort, render_template, redirect, url_for
from flask.ext.security import current_user, login_required

bp = Blueprint('frontend', __name__)

@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html')

@bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html',
                            email=current_user.email)

@bp.route('/feeds')
@login_required
def feeds():
    users_subscriptions = current_user.subscribed

    return render_template('feeds.html',
                            subscriptions=users_subscriptions)