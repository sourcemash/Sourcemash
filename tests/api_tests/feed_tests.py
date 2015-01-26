from nose.tools import assert_true, assert_false, eq_
import json

from app import app, db
from app.models import Feed
from factories import FeedFactory

def check_valid_header_type(headers):
    eq_(headers['Content-Type'], 'application/json')

class TestFeedAPI(object):

    def setUp(self):
        self.app = app.test_client()
        db.create_all()
        feed = FeedFactory()

        self.feed_uri = '/api/feeds/%d' % feed.id
        self.title = feed.title

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

    def tearDown(self):
        db.session.remove()
        db.drop_all()

class TestFeedListAPI():

    def setUp(self):
        self.app = app.test_client()
        db.create_all()
        FeedFactory()

    def test_get_feeds(self):
        r = self.app.get('/api/feeds')
        check_valid_header_type(r.headers)
        eq_(r.status_code, 200)

        data = json.loads(r.data)
        eq_(len(data['feeds']), 1)

    def test_post_feed_valid(self):
        feed_data = dict(url="http://techcrunch.com/feed/")
        r = self.app.post('/api/feeds', data=feed_data)

        check_valid_header_type(r.headers)
        eq_(r.status_code, 201)

        data = json.loads(r.data)
        eq_(data['feed']['title'], u"TechCrunch")

    def test_post_feed_missing_url(self):
        feed_data = dict()
        r = self.app.post('/api/feeds', data=feed_data)

        check_valid_header_type(r.headers)
        eq_(r.status_code, 400)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
