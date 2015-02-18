import pytest
import json

from . import TestBase

from tests.factories import feed_factories
from sourcemash.models import Feed

def check_valid_header_type(headers):
    assert headers['Content-Type'] == 'application/json'

class TestSubscriptionAPI(TestBase):

    def test_get_subscription_present(self, test_client, userWithFeed):
        feed = userWithFeed.subscribed.first()

        self.login(test_client, userWithFeed.email, userWithFeed.password)

        r = test_client.get('/api/subscriptions/%d' % feed.id)
        check_valid_header_type(r.headers)
        assert r.status_code == 200

        data = json.loads(r.data)
        assert data['subscription']['id'] == feed.id
        assert data['subscription']['feed']['id'] == feed.id

    def test_get_subscription_missing(self, test_client, user):
        self.login(test_client, user.email, user.password)

        r = test_client.get('/api/subscriptions/0')
        check_valid_header_type(r.headers)
        assert r.status_code == 404

    def test_delete_subscription_present(self, test_client, userWithFeed):
        feed = userWithFeed.subscribed.first()

        self.login(test_client, userWithFeed.email, userWithFeed.password)

        # Remove Dummy Feed
        delete = test_client.delete('api/subscriptions/%d' % feed.id)
        check_valid_header_type(delete.headers)
        data = json.loads(delete.data)

        assert data['result'] == True

        # Dummy feed should no longer be reachable
        get = test_client.get('api/subscriptions/%d' % feed.id)
        assert get.status_code == 404

    def test_delete_subscription_invalid_feed_id(self, test_client, userWithFeed):
        feed = userWithFeed.subscribed.first()

        self.login(test_client, userWithFeed.email, userWithFeed.password)

        # Failed remove Dummy Feed
        delete = test_client.delete('api/subscriptions/%d' % (int(feed.id)+1))
        check_valid_header_type(delete.headers)
        assert delete.status_code == 404       

class TestSubscriptionListAPI(TestBase):

    def login(self, test_client, email, password):
        return test_client.post('/login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)

    def test_get_users_subscriptions(self, test_client, userWithFeed):
        self.login(test_client, userWithFeed.email, userWithFeed.password)

        user_feed = userWithFeed.subscribed.first()

        r = test_client.get('/api/subscriptions')
        check_valid_header_type(r.headers)
        assert r.status_code == 200

        data = json.loads(r.data)
        assert len(data['subscriptions']) == 1

        assert data['subscriptions'][0]['feed']['title'] == user_feed.title

    def test_post_subscription_validURL_new_feed(self, test_client, user):
        self.login(test_client, user.email, user.password)

        subscription_data = dict(url='http://online.wsj.com/xml/rss/3_7085.xml')
        r = test_client.post('/api/subscriptions', data=subscription_data)

        check_valid_header_type(r.headers)
        assert r.status_code == 201
        assert Feed.query.first().url == 'http://online.wsj.com/xml/rss/3_7085.xml'

    def test_post_subscription_validURL_old_feed(self, test_client, user, real_feed):
        self.login(test_client, user.email, user.password)

        existent_feed = Feed.query.first()
        subscription_data = dict(url=existent_feed.url)
        r = test_client.post('/api/subscriptions', data=subscription_data)

        check_valid_header_type(r.headers)
        assert r.status_code == 201

    def test_post_subscription_invalid_feed_url(self, test_client, user):
        self.login(test_client, user.email, user.password)

        subscription_data = dict(url='http://nonexistentURL')
        r = test_client.post('/api/subscriptions', data=subscription_data)

        check_valid_header_type(r.headers)
        assert r.status_code == 422

        data = json.loads(r.data)
        assert len(data['errors']['url']) == 1
        assert 'not a valid feed' in data['errors']['url'][0]

    def test_post_subscription_already_subscribed_feed(self, test_client, userWithRealFeed):
        self.login(test_client, userWithRealFeed.email, userWithRealFeed.password)

        feed = userWithRealFeed.subscribed.first()

        subscription_data = dict(url=feed.url)
        r = test_client.post('/api/subscriptions', data=subscription_data)

        check_valid_header_type(r.headers)
        assert r.status_code == 409

        data = json.loads(r.data)
        assert len(data['errors']['url']) == 1
        assert 'Already subscribed' in data['errors']['url'][0]



