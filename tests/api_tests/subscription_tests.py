from nose.tools import assert_true, assert_false, eq_
import json

from app import app, db
from factories import FeedFactory, UserFactory, RoleFactory

from flask.ext.security import current_user

def check_valid_header_type(headers):
    eq_(headers['Content-Type'], 'application/json')

class TestSubscriptionAPI():

    def setUp(self):
        self.app = app.test_client()

        db.create_all()
        feed = FeedFactory()
        role = RoleFactory()
        self.user = UserFactory(roles=[role],subscribed=[feed])

        self.subscription_uri = '/api/subscriptions/%d' % feed.id

    def login(self, email, password):
        return self.app.post('/login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)

    def test_get_subscription_present(self):
        self.login(self.user.email, self.user.password)
        r = self.app.get(self.subscription_uri)
        check_valid_header_type(r.headers)
        eq_(r.status_code, 200)

        data = json.loads(r.data)
        eq_(data['subscription']['uri'], self.subscription_uri)

    def test_get_subscription_missing(self):
        self.login(self.user.email, self.user.password)
        r = self.app.get('/api/subscriptions/0')
        check_valid_header_type(r.headers)
        eq_(r.status_code, 404)

    def test_delete_subscription_present(self):
        self.login(self.user.email, self.user.password)

        # Remove Dummy Feed
        delete = self.app.delete(self.subscription_uri)
        check_valid_header_type(delete.headers)
        data = json.loads(delete.data)
        eq_(data['result'], True)

        # Dummy feed should no longer be reachable
        get = self.app.get(self.subscription_uri)
        eq_(get.status_code, 404)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

class TestSubscriptionListAPI():

    def setUp(self):
        self.app = app.test_client()

        db.create_all()
        feed = FeedFactory()
        role = RoleFactory()
        self.user = UserFactory(roles=[role],subscribed=[feed])

    def login(self, email, password):
        return self.app.post('/login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)

    def test_get_users_subscriptions(self):
        self.login(self.user.email, self.user.password)
        r = self.app.get('/api/subscriptions')
        check_valid_header_type(r.headers)
        eq_(r.status_code, 200)

        data = json.loads(r.data)
        eq_(len(data['subscriptions']), 1)

    def test_post_subscription_valid(self):
        self.login(self.user.email, self.user.password)
        new_feed = FeedFactory(url='http://techcrunch.com/feed/', title="TechCrunch")
        subscription_data = dict(feed_uri='api/feeds/%d' % new_feed.id)
        r = self.app.post('/api/subscriptions', data=subscription_data)

        check_valid_header_type(r.headers)
        eq_(r.status_code, 201)

        data = json.loads(r.data)
        eq_(data['subscription']['uri'], '/api/subscriptions/%d' % new_feed.id)

    def test_post_subscription_missing_feed_uri(self):
        self.login(self.user.email, self.user.password)
        subscription_data = dict()
        r = self.app.post('/api/subscriptions', data=subscription_data)

        check_valid_header_type(r.headers)
        eq_(r.status_code, 400)

    def test_post_subscription_invalid_feed_uri(self):
        self.login(self.user.email, self.user.password)

        subscription_data = dict(feed_uri='/api/feeds10')
        r = self.app.post('/api/subscriptions', data=subscription_data)

        check_valid_header_type(r.headers)
        eq_(r.status_code, 400)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

