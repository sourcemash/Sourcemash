from nose.tools import assert_true, assert_false, eq_
import json

from app import app, db
from app.models import User, Role
from factories import UserFactory, RoleFactory

def check_valid_header_type(headers):
    eq_(headers['Content-Type'], 'application/json')

class TestUserListAPI():

    def setUp(self):
        self.app = app.test_client()
        db.create_all()
        self.user_role = RoleFactory()
        user = UserFactory.create(role=self.user_role)

    def test_get_all_users(self):
        user = UserFactory.create(role=self.user_role)

        rv = self.app.get('/api/users')
        check_valid_header_type(rv.headers)
        eq_(rv.status_code, 200)

        data = json.loads(rv.data)
        eq_(len(data['users']),2)

    def test_post_new_user_valid(self):
        # Create user
        user_data = dict(email='user1@test.com', password='password')
        rv = self.app.post('/api/users', data=user_data)
        
        check_valid_header_type(rv.headers)
        eq_(rv.status_code,201)

        data = json.loads(rv.data)
        eq_(data['user']['email'], 'user1@test.com')

        eq_(len(Role.query.filter(Role.users.any(email='user1@test.com')).all()), 1)

    def test_post_new_user_missing_email(self):
        user_data = dict()
        rv = self.app.post('/api/users', data=user_data)
        
        check_valid_header_type(rv.headers)
        eq_(rv.status_code,400)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

class TestUserAPI():

    def setUp(self):
        self.app = app.test_client()
        db.create_all()

        user_role = RoleFactory()
        user = UserFactory.create(role=user_role)

        self.user_uri = '/api/users/%d' % user.id
        self.user_email = user.email

    def test_get_user_present(self):
        rv = self.app.get(self.user_uri)
        check_valid_header_type(rv.headers)
        eq_(rv.status_code, 200)

        data = json.loads(rv.data)
        eq_(data['user']['email'], self.user_email)

    def test_get_user_missing(self):
        rv = self.app.get('/api/users/0')
        check_valid_header_type(rv.headers)
        eq_(rv.status_code, 404)

    def test_put_user_valid(self):
        # Edit dummy user
        user_data_new = dict(email=u"admin@admin.com")
        put = self.app.put(self.user_uri, data=user_data_new)
        check_valid_header_type(put.headers)
        data = json.loads(put.data)
        eq_(data['user']['email'], u"admin@admin.com")
        eq_(put.status_code, 200)

    def test_put_user_missing_email(self):
        # Edit dummy user
        user_data_new = dict()
        put = self.app.put(self.user_uri, data=user_data_new)
        check_valid_header_type(put.headers)
        data = json.loads(put.data)
        eq_(put.status_code, 400)

    def test_delete_user_present(self):
        # Remove dummy user
        delete = self.app.delete(self.user_uri)
        check_valid_header_type(delete.headers)
        data = json.loads(delete.data)
        eq_(data['result'], True)

        # Dummy user should no longer be reachable
        get = self.app.get(self.user_uri)
        eq_(get.status_code, 404)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
