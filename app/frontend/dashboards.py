from app import app

from flask import render_template, redirect, request, flash, url_for
from flask.ext.security import LoginForm, RegisterForm, current_user, login_user, logout_user

from app.models import User, user_datastore
from app.users.forms import RegisterForm

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/register', methods=['GET', 'POST'])
@app.route('/register/<provider_id>', methods=['GET', 'POST'])
def register(provider_id=None):
    if current_user.is_authenticated():
        return redirect(request.referrer or '/')

    form = RegisterForm()

    if form.validate_on_submit():
        user = user_datastore.create_user(email=form.email.data, password=form.password.data)
        user_datastore.add_role_to_user(user, 'user')
        user_datastore.commit()

        login_user(user)
        user_datastore.commit()
        flash('Account created successfully', 'info')
        return "PROFILE PAGE"

    login_failed = int(request.args.get('login_failed', 0))

    return render_template('register.html',
                           form=form,
                           login_failed=login_failed)

@app.route('/logout')
def logout():
	logout_user()
	flash('Logged out successfully.', 'info')
	return render_template('register.html',
                           form=form,
                           login_failed=login_failed)