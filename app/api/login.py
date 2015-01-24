from flask import abort, redirect
from flask.ext.security import login_user, current_user, LoginForm
from flask.ext.security.utils import encrypt_password, verify_and_update_password
from app import app, db
from app.models import User, user_datastore

@app.route('/login', methods=['POST'])
def login(self, email, password):

	user = user_datastore.get_user(email)
	if user and verify_and_update_password(password, user):
		login_user(user)
		return

	return {'errors': ['Email/Password combination invalid.']}