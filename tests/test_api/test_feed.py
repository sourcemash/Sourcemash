import pytest
import json

from sourcemash.models import Feed

def check_valid_header_type(headers):
    assert headers['Content-Type'] == 'application/json'

class TestFeedAPI:

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


class TestFeedListAPI:

    def test_get_feeds(self, test_client, feed):
        r = test_client.get('/api/feeds')
        check_valid_header_type(r.headers)
        assert r.status_code == 200

        data = json.loads(r.data)
        assert len(data['feeds']) == 1