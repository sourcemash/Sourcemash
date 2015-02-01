import pytest
import json

from tests.factories import feed_factories

def check_valid_header_type(headers):
    assert headers['Content-Type'] == 'application/json'

class TestSubscriptionAPI:

    def login(self, test_client, email, password):
        r = test_client.post('/login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)
        return r

    def test_get_subscription_present(self, test_client, user):
        feed = user.subscribed.first()

        self.login(test_client, user.email, user.password)

        r = test_client.get('/api/subscriptions/%d' % feed.id)
        check_valid_header_type(r.headers)
        assert r.status_code == 200

        data = json.loads(r.data)
        assert data['subscription']['uri'] == '/api/subscriptions/%d' % feed.id

    def test_get_subscription_missing(self, test_client, user):
        feed = user.subscribed.first()

        self.login(test_client, user.email, user.password)

        r = test_client.get('/api/subscriptions/0')
        check_valid_header_type(r.headers)
        assert r.status_code == 404

    def test_delete_subscription_present(self, test_client, user):
        feed = user.subscribed.first()

        self.login(test_client, user.email, user.password)

        # Remove Dummy Feed
        delete = test_client.delete('api/subscriptions/%d' % feed.id)
        check_valid_header_type(delete.headers)
        data = json.loads(delete.data)

        assert data['result'] == True

        # Dummy feed should no longer be reachable
        get = test_client.get('api/subscriptions/%d' % feed.id)
        assert get.status_code == 404

class TestSubscriptionListAPI:

    def login(self, test_client, email, password):
        return test_client.post('/login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)

    def test_get_users_subscriptions(self, test_client, user):
        self.login(test_client, user.email, user.password)

        r = test_client.get('/api/subscriptions')
        check_valid_header_type(r.headers)
        assert r.status_code == 200

        data = json.loads(r.data)
        assert len(data['subscriptions']) == 1

        assert data['subscriptions'][0]['title'] == "NYTimes"

    def test_post_subscription_valid(self, test_client, user, feed):
        self.login(test_client, user.email, user.password)

        subscription_data = dict(feed_uri='api/feeds/%d' % feed.id)
        r = test_client.post('/api/subscriptions', data=subscription_data)

        check_valid_header_type(r.headers)
        assert r.status_code == 201

        data = json.loads(r.data)
        assert data['subscription']['uri'] == '/api/subscriptions/%d' % feed.id

    def test_post_subscription_missing_feed_uri(self, test_client, user):
        self.login(test_client, user.email, user.password)

        subscription_data = dict()
        r = test_client.post('/api/subscriptions', data=subscription_data)

        check_valid_header_type(r.headers)
        assert r.status_code == 400

    def test_post_subscription_invalid_feed_uri(self, test_client, user):
        self.login(test_client, user.email, user.password)

        subscription_data = dict(feed_uri='/api/feeds10')
        r = test_client.post('/api/subscriptions', data=subscription_data)

        check_valid_header_type(r.headers)
        assert r.status_code == 400

