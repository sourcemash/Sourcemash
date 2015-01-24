from nose.tools import assert_true, assert_false, eq_

from app import app, db
from factories import FeedFactory
from app.models import Item, Feed

from worker_tasks.feed_scraper import store_items

def check_valid_header_type(headers):
	eq_(headers['Content-Type'], 'application/json')

class TestUser():

	def setUp(self):
		self.app = app.test_client()
		db.create_all()
		FeedFactory()

	def test_ingest_feeds(self):
		for feed in Feed.query.all():
			store_items.run(feed.id, feed.last_updated, feed.url)
		assert_true(len(Item.query.all()) > 0)

	def tearDown(self):
		db.session.remove()
		db.drop_all()