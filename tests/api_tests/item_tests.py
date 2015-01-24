from nose.tools import assert_true, assert_false, eq_
import json

from app import app, db
from app.models import Item
from factories import ItemFactory

def check_valid_header_type(headers):
	eq_(headers['Content-Type'], 'application/json')

class TestItemAPI(object):

	def setUp(self):
		self.app = app.test_client()
		db.create_all()
		item = ItemFactory()

		self.item_uri = '/api/feeds/%d/items/%d' % (item.feed_id, item.id)
		self.title = item.title

	def test_get_item_present(self):
		r = self.app.get(self.item_uri)
		check_valid_header_type(r.headers)
		eq_(r.status_code, 200)

		data = json.loads(r.data)
		eq_(data['item']['title'], self.title)

	def test_get_item_missing(self):
		r = self.app.get(self.item_uri + '10')
		check_valid_header_type(r.headers)
		eq_(r.status_code, 404)

	def tearDown(self):
		db.session.remove()
		db.drop_all()

class TestItemListAPI():

	def setUp(self):
		self.app = app.test_client()
		db.create_all()
		item = ItemFactory()

		self.item_uri = '/api/feeds/%d/items' % (item.feed_id)

	def test_get_items(self):
		r = self.app.get(self.item_uri)

		check_valid_header_type(r.headers)
		eq_(r.status_code, 200)

		data = json.loads(r.data)
		eq_(len(data['items']), 1)

	def tearDown(self):
		db.session.remove()
		db.drop_all()
