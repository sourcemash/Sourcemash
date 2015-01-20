from nose.tools import assert_true, assert_false, eq_
import json
import os
from config import basedir

from app import app, db
from app.models import User, Role
from factories import UserFactory, RoleFactory

def check_valid_header_type(headers):
	eq_(headers['Content-Type'], 'application/json')

class TestUser():

	def setUp(self):
		self.app = app.test_client()

		app.config['TESTING'] = True
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
			os.path.join(basedir, 'test.db')
		db.create_all()
		user_role = RoleFactory()
		user = UserFactory.create(role=user_role)

		self.user_uri = '/api/users/%d' % user.id
		self.user_email = user.email

	def test_remove_role_on_deleted_user(self):
		'''
		Proof that many-to-many relationships are deleted when
		removing one side of the mapping (e.g. User).
		'''
		eq_(len(Role.query.filter(Role.users.any(email=self.user_email)).all()), 1)

		rv = self.app.delete(self.user_uri)
		check_valid_header_type(rv.headers)
		eq_(rv.status_code, 200)

		eq_(len(Role.query.filter(Role.users.any(email=self.user_email)).all()), 0)

	def tearDown(self):
		db.session.remove()
		db.drop_all()