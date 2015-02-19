import pytest
import json

from . import TestBase
from tests.factories import item_factories


def check_valid_header_type(headers):
    assert headers['Content-Type'] == 'application/json'

class TestItemAPI(TestBase):

    def test_get_item_present(self, test_client, item):
        r = test_client.get('/api/items/%d' % item.id)
        check_valid_header_type(r.headers)
        assert r.status_code == 200

        data = json.loads(r.data)
        assert data['item']['title'] == item.title

    def test_get_item_missing(self, test_client):
        r = test_client.get('/api/items/%d' % 10)
        check_valid_header_type(r.headers)
        assert r.status_code == 404

    def test_put_item_upvote(self, test_client, user, item):
        self.login(test_client, user.email, user.password)

        upvote = dict(vote=1)
        r = test_client.put('/api/items/%d' % item.id, data=upvote)
        check_valid_header_type(r.headers)
        assert r.status_code == 200

        data = json.loads(r.data)
        assert data['item']['totalVotes'] == 1

    def test_put_item_downvote(self, test_client, user, item):
        self.login(test_client, user.email, user.password)

        downvote = dict(vote=-1)
        r = test_client.put('/api/items/%d' % item.id, data=downvote)
        check_valid_header_type(r.headers)
        assert r.status_code == 200

        data = json.loads(r.data)
        assert data['item']['totalVotes'] == -1

    def test_put_item_too_big_vote(self, test_client, user, item):
        self.login(test_client, user.email, user.password)

        original_vote_count = item.totalVotes
        too_big_vote = dict(vote=5)
        r = test_client.put('/api/items/%d' % item.id, data=too_big_vote)
        check_valid_header_type(r.headers)
        assert r.status_code == 406

        data = json.loads(r.data)
        assert data['item']['totalVotes'] == original_vote_count

    def test_put_item_non_integer_vote(self, test_client, user, item):
        self.login(test_client, user.email, user.password)

        non_integer_vote = dict(vote=0.33)
        r = test_client.put('/api/items/%d' % item.id, data=non_integer_vote)
        check_valid_header_type(r.headers)
        assert r.status_code == 400

    def test_put_vote_missing(self, test_client, user, item):
        self.login(test_client, user.email, user.password)

        no_vote = dict()
        r = test_client.put('/api/items/%d' % item.id, data=no_vote)
        check_valid_header_type(r.headers)
        assert r.status_code == 400

    def test_put_item_missing(self, test_client, user, item):
        self.login(test_client, user.email, user.password)

        upvote = dict(vote=1)
        r = test_client.put('/api/items/%d' % (int(item.id+1)), data=upvote)
        check_valid_header_type(r.headers)
        assert r.status_code == 404

class TestFeedItemListAPI:

    def test_get_items(self, test_client, item):
        r = test_client.get('/api/feeds/%d/items' % item.feed.id)

        check_valid_header_type(r.headers)
        assert r.status_code == 200

        data = json.loads(r.data)
        assert len(data['items']) == 1


class TestCategoryItemListAllAPI:

    def test_get_category_items_missing_category(self, test_client):
        r = test_client.get('/api/categories/nonexistent_category/items/all')
        check_valid_header_type(r.headers)
        assert r.status_code == 200

        data = json.loads(r.data)
        assert len(data['items']) == 0

    def test_get_category_items_present(self, test_client, itemsWithCategory):
        r = test_client.get('/api/categories/' + itemsWithCategory[0].category_1 + '/items/all')

        check_valid_header_type(r.headers)
        assert r.status_code == 200

        data = json.loads(r.data)
        assert len(data['items']) == 5


class TestCategoryItemListAPI(TestBase):

    def test_get_items_present(self, test_client, userWithPopulatedFeed):
        self.login(test_client, userWithPopulatedFeed.email, userWithPopulatedFeed.password)

        feed = userWithPopulatedFeed.subscribed.first()

        r = test_client.get('/api/categories/' + feed.items[0].category_1 + '/items')

        check_valid_header_type(r.headers)
        assert r.status_code == 200

        data = json.loads(r.data)
        assert len(data['items']) == 5


    def test_get_items_case_insensitive_categories(self, test_client, userWithPopulatedFeed):
        self.login(test_client, userWithPopulatedFeed.email, userWithPopulatedFeed.password)

        feed = userWithPopulatedFeed.subscribed.first()

        r = test_client.get('/api/categories/' + feed.items[0].category_1.lower() + '/items')

        check_valid_header_type(r.headers)
        assert r.status_code == 200

        data = json.loads(r.data)
        assert len(data['items']) == 5


    def test_get_items_category_missing(self, test_client, userWithPopulatedFeed):
        self.login(test_client, userWithPopulatedFeed.email, userWithPopulatedFeed.password)

        outside_item = item_factories.ItemWithCategoryFactory(category_1="nonexistent_category")

        r = test_client.get('/api/categories/' + outside_item.category_1 + '/items')

        check_valid_header_type(r.headers)
        assert r.status_code == 200

        data = json.loads(r.data)
        assert len(data['items']) == 0


    def test_get_items_category_with_unsubscribed_item(self, test_client, userWithPopulatedFeed, itemsWithCategory):
        self.login(test_client, userWithPopulatedFeed.email, userWithPopulatedFeed.password)

        feed = userWithPopulatedFeed.subscribed.first()
        user_items_length = feed.items.count()

        r = test_client.get('/api/categories/' + feed.items[0].category_1 + '/items')

        check_valid_header_type(r.headers)
        assert r.status_code == 200

        data = json.loads(r.data)
        assert len(data['items']) == user_items_length + 1
        assert len(filter(lambda item: item['feed']['subscribed'] == False, data['items'])) == 1
