from app import app

from flask import abort, render_template, redirect, request, flash, url_for
from flask.ext.security import LoginForm, RegisterForm, current_user, login_user, logout_user
from flask.ext.security.utils import encrypt_password

from app.models import User, user_datastore
from app.users.forms import RegisterForm

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated():
        return redirect('/')

    form = RegisterForm()

    if form.validate_on_submit():
        user = user_datastore.create_user(email=form.email.data, password=encrypt_password(form.password.data))
        role = user_datastore.find_or_create_role('user')

        user_datastore.add_role_to_user(user, role)
        user_datastore.commit()

        login_user(user)
        user_datastore.commit()
        flash('Account created successfully', 'info')
        return render_template('profile.html',
                                email=current_user.email)

    return render_template('register.html',
                           form=form)

@app.route('/profile')
def profile():
    return render_template('profile.html',
                            email=current_user.email) 

@app.route('/logout')
def logout():
    logout_user()
    flash('Logged out successfully.', 'info')
    return render_template('register.html',
                           form=form,
                           login_failed=login_failed)