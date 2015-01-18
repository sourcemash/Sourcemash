from nose.tools import assert_true, assert_false, eq_
import json

from app import app

def check_valid_header_type(headers):
	eq_(headers['Content-Type'], 'application/json')

class TestSubscriptionAPI():

	def setUp(self):
		self.app = app.test_client()

		# Add dummy subscription
		subscription_data = dict(feed_uri='/api/feeds/4')
		post = self.app.post('/api/subscriptions', data=subscription_data)
		data = json.loads(post.data)
		subscription_uri = data['subscription']['uri']

	def test_get_feed_present(self):
		r = self.app.get('/api/subscriptions/3')
		check_valid_header_type(r.headers)
		eq_(r.status_code, 200)

		data = json.loads(r.data)
		eq_(data['subscription']['uri'], '/api/subscriptions/3')

	def test_get_subscription_missing(self):
		r = self.app.get('/api/subscriptions/0')
		check_valid_header_type(r.headers)
		eq_(r.status_code, 404)

	def test_delete_subscription_present(self):
		# Remove Dummy Feed
		delete = self.app.delete('/api/subscriptions/4')
		check_valid_header_type(delete.headers)
		data = json.loads(delete.data)
		eq_(data['result'], True)

		# Dummy feed should no longer be reachable
		get = self.app.get('/api/subscriptions/4')
		eq_(get.status_code, 404)

	def tearDown(self):
		# Remove Dummy Feed
		delete = self.app.delete('/api/subscriptions/4')

class TestSubscriptionListAPI():

	def setUp(self):
		self.app = app.test_client()

	def test_get_users_subscriptions(self):
		r = self.app.get('/api/subscriptions')
		check_valid_header_type(r.headers)
		eq_(r.status_code, 200)

		data = json.loads(r.data)
		eq_(len(data['subscriptions']), 1)

	def test_post_subscription_valid(self):
		subscription_data = dict(feed_uri='/api/feeds/5')
		r = self.app.post('/api/subscriptions', data=subscription_data)

		check_valid_header_type(r.headers)
		eq_(r.status_code, 201)

		data = json.loads(r.data)
		eq_(data['subscription']['uri'], '/api/subscriptions/5')

	def test_post_subscription_missing_feed_uri(self):
		subscription_data = dict()
		r = self.app.post('/api/subscriptions', data=subscription_data)

		check_valid_header_type(r.headers)
		eq_(r.status_code, 400)

	def test_post_subscription_invalid(self):
		subscription_data = dict(feed_uri='/api/feeds/10/')
		r = self.app.post('/api/subscriptions', data=subscription_data)

		check_valid_header_type(r.headers)
		eq_(r.status_code, 201)

		data = json.loads(r.data)
		eq_(data['subscription']['uri'], '/api/subscriptions/10')

	def tearDown(self):
		pass
