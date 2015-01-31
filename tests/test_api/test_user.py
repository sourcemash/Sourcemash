import pytest
import json

def check_valid_header_type(headers):
    assert headers['Content-Type'] == 'application/json'

class TestUserListAPI:

    def test_get_all_users(self, test_client, user):
        rv = test_client.get('/api/users')
        check_valid_header_type(rv.headers)
        assert rv.status_code == 200

        data = json.loads(rv.data)

        print data
        assert len(data['users']) == 1

    def test_post_new_user_valid(self, test_client):
        user_data = dict(email='user1@test.com', password='password')
        rv = test_client.post('/api/users', data=user_data)
        
        check_valid_header_type(rv.headers)
        assert rv.status_code == 201

        data = json.loads(rv.data)
        assert data['user']['email'] == 'user1@test.com'

    def test_post_new_user_missing_email(self, test_client):
        user_data = dict()
        rv = test_client.post('/api/users', data=user_data)
        
        check_valid_header_type(rv.headers)
        assert rv.status_code == 400


class TestUserAPI:

    def test_get_user_present(self, test_client, user):
        rv = test_client.get('/api/users/%d' % user.id)
        check_valid_header_type(rv.headers)
        assert rv.status_code == 200

        data = json.loads(rv.data)
        assert data['user']['email'] == user.email

    def test_get_user_missing(self, test_client):
        rv = test_client.get('/api/users/0')
        check_valid_header_type(rv.headers)
        assert rv.status_code == 404

    def test_put_user_valid(self, test_client, user):
        # Edit dummy user
        user_data_new = dict(email=u"admin@admin.com")
        put = test_client.put('/api/users/%d' % user.id, data=user_data_new)
        check_valid_header_type(put.headers)
        data = json.loads(put.data)
        assert data['user']['email'] == u"admin@admin.com"
        assert put.status_code == 200

    def test_put_user_missing_email(self, test_client, user):
        # Edit dummy user
        user_data_new = dict()
        put = test_client.put('/api/users/%d' % user.id, data=user_data_new)
        check_valid_header_type(put.headers)
        data = json.loads(put.data)
        assert put.status_code == 400

    def test_delete_user_present(self, test_client, user):
        # Remove dummy user
        delete = test_client.delete('/api/users/%d' % user.id)
        check_valid_header_type(delete.headers)
        data = json.loads(delete.data)
        assert data['result'] == True

        # Dummy user should no longer be reachable
        get = test_client.get('/api/users/%d' % user.id)
        assert get.status_code == 404
