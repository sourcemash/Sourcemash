import pytest
import json

from . import TestBase
from tests.factories import item_factories


def check_valid_header_type(headers):
    assert headers['Content-Type'] == 'application/json'

class TestItemAPI:

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

    def test_get_users_items_present(self, test_client, userWithPopulatedFeed):
        self.login(test_client, userWithPopulatedFeed.email, userWithPopulatedFeed.password)

        feed = userWithPopulatedFeed.subscribed.first()

        r = test_client.get('/api/categories/' + feed.items[0].category_1 + '/items')

        check_valid_header_type(r.headers)
        assert r.status_code == 200

        data = json.loads(r.data)
        assert len(data['items']) == 5


    def test_get_users_items_case_insensitive_categories(self, test_client, userWithPopulatedFeed):
        self.login(test_client, userWithPopulatedFeed.email, userWithPopulatedFeed.password)

        feed = userWithPopulatedFeed.subscribed.first()

        r = test_client.get('/api/categories/' + feed.items[0].category_1.lower() + '/items')

        check_valid_header_type(r.headers)
        assert r.status_code == 200

        data = json.loads(r.data)
        assert len(data['items']) == 5


    def test_get_users_matching_categories_missing(self, test_client, userWithPopulatedFeed):
        self.login(test_client, userWithPopulatedFeed.email, userWithPopulatedFeed.password)

        outside_item = item_factories.ItemWithCategoryFactory(category_1="nonexistent_category")

        r = test_client.get('/api/categories/' + outside_item.category_1 + '/items')

        check_valid_header_type(r.headers)
        assert r.status_code == 200

        data = json.loads(r.data)
        assert len(data['items']) == 0
