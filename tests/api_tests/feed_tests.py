from nose.tools import assert_true, assert_false, eq_
import json
import os
from config import basedir

from app import app, db
from app.models import Feed
from factories import FeedFactory

def check_valid_header_type(headers):
	eq_(headers['Content-Type'], 'application/json')

class TestFeedAPI():

	def setUp(self):
		self.app = app.test_client()

		app.config['TESTING'] = True
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
			os.path.join(basedir, 'test.db')
		db.create_all()
		feed = FeedFactory()

<<<<<<< HEAD
		self.feed_uri = '/api/feeds/%d' % feed.id
		self.title = feed.title
=======
		app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(basedir, 'test.db')
        db.create_all()
        FeedFactory()

	def test_get_feed_present(self):
		feed_uri = '/api/feeds/%d' % Feed.query.first().id
>>>>>>> Switch Feed API to use DB.

	def test_get_feed_present(self):
		r = self.app.get(self.feed_uri)
		check_valid_header_type(r.headers)
		eq_(r.status_code, 200)

		data = json.loads(r.data)
		eq_(data['feed']['title'], self.title)

	def test_get_feed_missing(self):
		r = self.app.get('/api/feeds/0')
		check_valid_header_type(r.headers)
		eq_(r.status_code, 404)

	def test_delete_feed_present(self):
		delete = self.app.delete(self.feed_uri)
		check_valid_header_type(delete.headers)
		data = json.loads(delete.data)
		eq_(data['result'], True)

		# Dummy feed should no longer be reachable
<<<<<<< HEAD
		get = self.app.get(self.feed_uri)
=======
		get = self.app.get('/api/feeds/1')
>>>>>>> Switch Feed API to use DB.
		eq_(get.status_code, 404)

	def tearDown(self):
		db.session.remove()
        db.drop_all()

class TestFeedListAPI():

	def setUp(self):
		self.app = app.test_client()

		app.config['TESTING'] = True
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
			os.path.join(basedir, 'test.db')
		db.create_all()
		FeedFactory()

		app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(basedir, 'test.db')
        db.create_all()
        FeedFactory()

	def test_get_feeds(self):
		r = self.app.get('/api/feeds')
		check_valid_header_type(r.headers)
		eq_(r.status_code, 200)

		data = json.loads(r.data)
		eq_(len(data['feeds']), 1)

	def test_post_feed_valid(self):
		feed_data = dict(url="http://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml")
		r = self.app.post('/api/feeds', data=feed_data)

		check_valid_header_type(r.headers)
		eq_(r.status_code, 201)

		data = json.loads(r.data)
		eq_(data['feed']['title'], u"NYT > Home Page")

	def test_post_feed_missing_url(self):
		feed_data = dict()
		r = self.app.post('/api/feeds', data=feed_data)

		check_valid_header_type(r.headers)
		eq_(r.status_code, 400)

	def tearDown(self):
		db.session.remove()
        db.drop_all()
