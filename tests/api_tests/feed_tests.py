from nose.tools import assert_true, assert_false, eq_
import json

from app import app

def check_valid_header_type(headers):
	eq_(headers['Content-Type'], 'application/json')

class TestFeedAPI():

	def setUp(self):
		self.app = app.test_client()

	def test_get_feed_present(self):
		r = self.app.get('/api/feeds/1')
		check_valid_header_type(r.headers)
		eq_(r.status_code, 200)

		data = json.loads(r.data)
		eq_(data['feed']['title'], u"NYTimes")

	def test_get_feed_missing(self):
		r = self.app.get('/api/feeds/0')
		check_valid_header_type(r.headers)
		eq_(r.status_code, 404)

	def test_delete_feed_present(self):
		# Add dummy feed
		feed_data = dict(title=u'DummyFeed', url="http://dummyurl.com")
		post = self.app.post('/api/feeds', data=feed_data)
		data = json.loads(post.data)
		feed_uri = data['feed']['uri']

		# Remove Dummy Feed
		delete = self.app.delete(feed_uri)
		check_valid_header_type(delete.headers)
		data = json.loads(delete.data)
		eq_(data['result'], True)

		# Dummy feed should no longer be reachable
		get = self.app.get(feed_uri)
		eq_(get.status_code, 404)

	def tearDown(self):
		pass

class TestFeedListAPI():

	def setUp(self):
		self.app = app.test_client()

	def test_get_feeds(self):
		r = self.app.get('/api/feeds')
		check_valid_header_type(r.headers)
		eq_(r.status_code, 200)

		data = json.loads(r.data)
		eq_(len(data['feeds']), 2)

	def test_post_feed_valid(self):
		feed_data = dict(title=u'TechCrunch', url="http://feeds.feedburner.com/TechCrunch/")
		r = self.app.post('/api/feeds', data=feed_data)

		check_valid_header_type(r.headers)
		eq_(r.status_code, 201)

		data = json.loads(r.data)
		eq_(data['feed']['title'], u"TechCrunch")

	def test_post_feed_missing_title(self):
		feed_data = dict(url="http://feeds.feedburner.com/TechCrunch/")
		r = self.app.post('/api/feeds', data=feed_data)

		check_valid_header_type(r.headers)
		eq_(r.status_code, 400)

	def test_post_feed_missing_url(self):
		feed_data = dict(title=u'TechCrunch')
		r = self.app.post('/api/feeds', data=feed_data)

		check_valid_header_type(r.headers)
		eq_(r.status_code, 400)

	def tearDown(self):
		pass
