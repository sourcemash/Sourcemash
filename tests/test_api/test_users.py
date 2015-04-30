import pytest
import json

from . import TestBase

def check_valid_header_type(headers):
    assert headers['Content-Type'] == 'application/json'

class TestUserListAPI:

    def test_get_all_users(self, test_client, user):
        rv = test_client.get('/api/users')
        check_valid_header_type(rv.headers)
        assert rv.status_code == 200

        data = json.loads(rv.data)

        assert len(data['users']) == 1

    def test_post_new_user_valid(self, test_client):
        user_data = dict(email='asgman@test.com', password='password',
                         password_confirm='password')
        rv = test_client.post('/api/users', data=user_data)

        check_valid_header_type(rv.headers)
        assert rv.status_code == 201

        data = json.loads(rv.data)
        assert data['user']['email'] == 'asgman@test.com'

    def test_post_new_user_no_confirm(self, test_client):
        user_data = dict(email='asgman@test.com', password='password')
        rv = test_client.post('/api/users', data=user_data)

        check_valid_header_type(rv.headers)
        assert rv.status_code == 422

    def test_post_new_user_missing_email(self, test_client):
        user_data = dict()
        rv = test_client.post('/api/users', data=user_data)

        check_valid_header_type(rv.headers)
        assert rv.status_code == 400


class TestUserAPI(TestBase):

    def test_get_user_logged_in(self, test_client, user):
        self.login(test_client, user.email, user.password)

        rv = test_client.get('/api/user')
        check_valid_header_type(rv.headers)
        assert rv.status_code == 200

        data = json.loads(rv.data)
        assert data['user']['email'] == user.email

    def test_put_user_valid(self, test_client, user):
        self.login(test_client, user.email, user.password)

        user_data_new = dict(email=u"admin@admin.com")
        put = test_client.put('/api/user', data=user_data_new)
        check_valid_header_type(put.headers)
        data = json.loads(put.data)
        assert data['user']['email'] == u"admin@admin.com"
        assert put.status_code == 200

    def test_put_user_missing_email(self, test_client, user):
        self.login(test_client, user.email, user.password)

        user_data_new = dict()
        put = test_client.put('/api/user', data=user_data_new)
        check_valid_header_type(put.headers)
        data = json.loads(put.data)
        assert put.status_code == 400

    def test_delete_user(self, test_client, user):
        self.login(test_client, user.email, user.password)

        # Remove dummy user
        delete = test_client.delete('/api/user')
        check_valid_header_type(delete.headers)
        data = json.loads(delete.data)
        assert data['result'] == True
