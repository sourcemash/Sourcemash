import pytest
import json

def check_valid_header_type(headers):
    assert headers['Content-Type'] == 'application/json'

class TestItemAPI:

    def login(self, test_client, email, password):
        r = test_client.post('/login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)
        return r

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

    def test_put_item_upvote(self, test_client, user, item):
        self.login(test_client, user.email, user.password)

        upvote = dict(vote=1)
        r = test_client.put('/api/feeds/%d/items/%d' % (item.feed.id, item.id), data=upvote)
        check_valid_header_type(r.headers)
        assert r.status_code == 200

        data = json.loads(r.data)
        assert data['item']['totalVotes'] == 1

    def test_put_item_downvote(self, test_client, user, item):
        self.login(test_client, user.email, user.password)

        downvote = dict(vote=-1)
        r = test_client.put('/api/feeds/%d/items/%d' % (item.feed.id, item.id),
                            data=downvote)
        check_valid_header_type(r.headers)
        assert r.status_code == 200

        data = json.loads(r.data)
        assert data['item']['totalVotes'] == -1

    def test_put_item_vote_missing(self, test_client, user, item):
        self.login(test_client, user.email, user.password)

        no_vote = dict()
        r = test_client.put('/api/feeds/%d/items/%d' % (item.feed.id, item.id),
                            data=no_vote)
        check_valid_header_type(r.headers)
        assert r.status_code == 400

class TestItemListAPI:

    def test_get_items(self, test_client, item):
        r = test_client.get('/api/feeds/%d/items' % (item.feed.id))

        check_valid_header_type(r.headers)
        assert r.status_code == 200

        data = json.loads(r.data)
        assert len(data['items']) == 1