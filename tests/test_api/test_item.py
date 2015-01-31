import pytest
import json

def check_valid_header_type(headers):
    assert headers['Content-Type'] == 'application/json'

class TestItemAPI:

    def test_get_item_present(self, test_client, item):
        r = test_client.get('/api/feeds/%d/items/%d' % (item.feed.id, item.id))
        check_valid_header_type(r.headers)
        assert r.status_code == 200

        data = json.loads(r.data)
        assert data['item']['title'] == item.title

    def test_get_item_missing(self, test_client, item):
        r = test_client.get('/api/feeds/%d/items/%d' % (item.feed.id, 10))
        check_valid_header_type(r.headers)
        assert r.status_code == 404

class TestItemListAPI:

    def test_get_items(self, test_client, item):
        r = test_client.get('/api/feeds/%d/items' % (item.feed.id))

        check_valid_header_type(r.headers)
        assert r.status_code == 200

        data = json.loads(r.data)
        assert len(data['items']) == 1