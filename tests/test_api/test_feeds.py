import pytest
import json

from . import TestBase

def check_valid_header_type(headers):
    assert headers['Content-Type'] == 'application/json'

class TestFeedAPI(TestBase):

    def test_get_feed_present(self, test_client, feed):
        r = test_client.get('/api/feeds/%d' % feed.id)
        check_valid_header_type(r.headers)
        assert r.status_code == 200

        data = json.loads(r.data)
        assert data['feed']['title'] == feed.title

    def test_get_feed_missing(self, test_client):
        r = test_client.get('/api/feeds/0')
        check_valid_header_type(r.headers)
        assert r.status_code == 404

    def test_get_feed_present(self, test_client, real_feed):
        r = test_client.get('/api/feeds/%d' % real_feed.id)
        check_valid_header_type(r.headers)
        assert r.status_code == 200

        data = json.loads(r.data)
        assert data['feed']['topic'] == real_feed.topic

    def test_put_feed_subscribe(self, test_client, user, feed):
        self.login(test_client, user.email, user.password)

        subscribe_data = dict(subscribed=True)
        subscribe = test_client.put('/api/feeds/%d' % feed.id, data=subscribe_data)
        check_valid_header_type(subscribe.headers)
        data = json.loads(subscribe.data)

        assert data['feed']['subscribed'] == True
        assert user.subscribed.count() == 1


    def test_put_feed_already_subscribed(self, test_client, userWithFeed):
        feed = userWithFeed.subscribed.first()

        self.login(test_client, userWithFeed.email, userWithFeed.password)

        subscribe_data = dict(subscribed=True)
        subscribe = test_client.put('/api/feeds/%d' % feed.id, data=subscribe_data)
        check_valid_header_type(subscribe.headers)
        data = json.loads(subscribe.data)

        assert "Already subscribed" in data['errors']['subscribed'][0]

    def test_put_feed_unsubscribe(self, test_client, userWithFeed):
        feed = userWithFeed.subscribed.first()

        self.login(test_client, userWithFeed.email, userWithFeed.password)

        unsubscribe_data = dict(subscribed=False)
        unsubscribe = test_client.put('api/feeds/%d' % feed.id, data=unsubscribe_data)
        check_valid_header_type(unsubscribe.headers)
        data = json.loads(unsubscribe.data)
        print data

        assert data['feed']['subscribed'] == False
        assert userWithFeed.subscribed.count() == 0

    def test_put_feed_already_unsubscribed(self, test_client, user, feed):
        self.login(test_client, user.email, user.password)

        unsubscribe_data = dict(subscribed=False)
        unsubscribe = test_client.put('api/feeds/%d' % feed.id, data=unsubscribe_data)
        check_valid_header_type(unsubscribe.headers)
        data = json.loads(unsubscribe.data)

        assert 'already unsubscribed' in data['errors']['subscribed'][0]

    def test_put_feed_invalid_id(self, test_client, userWithFeed):
        feed = userWithFeed.subscribed.first()

        self.login(test_client, userWithFeed.email, userWithFeed.password)

        unsubscribe_data = dict(subscribed=False)

        unsubscribe = test_client.put('api/feeds/%d' % (int(feed.id)+1), data=unsubscribe_data)
        check_valid_header_type(unsubscribe.headers)
        assert unsubscribe.status_code == 404


class TestFeedListAllAPI:

    def test_get_feeds(self, test_client, feed):
        r = test_client.get('/api/feeds/all')
        check_valid_header_type(r.headers)
        assert r.status_code == 200

        data = json.loads(r.data)
        assert len(data['feeds']) == 1


class TestFeedListAPI(TestBase):

    def test_get_users_subscriptions(self, test_client, userWithFeed):
        self.login(test_client, userWithFeed.email, userWithFeed.password)

        user_feed = userWithFeed.subscribed.first()

        r = test_client.get('/api/feeds')
        check_valid_header_type(r.headers)
        assert r.status_code == 200

        data = json.loads(r.data)
        assert len(data['feeds']) == 1

        assert data['feeds'][0]['title'] == user_feed.title

    def test_post_subscription_validURL_new_feed(self, test_client, user):
        self.login(test_client, user.email, user.password)

        subscription_data = dict(url='http://online.wsj.com/xml/rss/3_7085.xml')
        r = test_client.post('/api/feeds', data=subscription_data)

        check_valid_header_type(r.headers)
        assert r.status_code == 201
        assert user.subscribed.first().url == 'http://online.wsj.com/xml/rss/3_7085.xml'

    def test_post_subscription_validURL_old_feed(self, test_client, user, real_feed):
        self.login(test_client, user.email, user.password)

        subscription_data = dict(url=real_feed.url)
        r = test_client.post('/api/feeds', data=subscription_data)

        check_valid_header_type(r.headers)
        assert r.status_code == 201

    def test_post_subscription_nonexistent_feed_url(self, test_client, user):
        self.login(test_client, user.email, user.password)

        subscription_data = dict(url='nonexistentURLforsourcemashtests')
        r = test_client.post('/api/feeds', data=subscription_data)

        check_valid_header_type(r.headers)
        assert r.status_code == 422

        data = json.loads(r.data)
        assert len(data['errors']['url']) == 1
        assert 'not a valid feed' in data['errors']['url'][0]

    def test_post_subscription_nonRSS_feed_url(self, test_client, user):
        self.login(test_client, user.email, user.password)

        subscription_data = dict(url='http://google.com')
        r = test_client.post('/api/feeds', data=subscription_data)

        check_valid_header_type(r.headers)
        assert r.status_code == 422

        data = json.loads(r.data)
        assert len(data['errors']['url']) == 1
        assert 'not a valid feed' in data['errors']['url'][0]

    def test_post_subscription_already_subscribed_feed(self, test_client, userWithRealFeed):
        self.login(test_client, userWithRealFeed.email, userWithRealFeed.password)

        feed = userWithRealFeed.subscribed.first()

        subscription_data = dict(url=feed.url)
        r = test_client.post('/api/feeds', data=subscription_data)

        check_valid_header_type(r.headers)
        assert r.status_code == 409

        data = json.loads(r.data)
        assert len(data['errors']['url']) == 1
        assert 'Already subscribed' in data['errors']['url'][0]

    def test_post_login_required(self, test_client, feed):
        subscription_data = dict(url=feed.url)
        rv = test_client.post('/api/feeds', data=subscription_data)
        check_valid_header_type(rv.headers)
        assert rv.status_code == 401

        data = json.loads(rv.data)
        assert 'not logged in' in data["errors"]["user"]
