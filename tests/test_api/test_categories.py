import pytest
import json

from . import TestBase

from sourcemash.models import Feed

def check_valid_header_type(headers):
    assert headers['Content-Type'] == 'application/json'

class TestCategoryListAllAPI:
    def test_get_categories_present(self, test_client, itemWithCategory):
        r = test_client.get('/api/categories/all')
        check_valid_header_type(r.headers)
        assert r.status_code == 200

        data = json.loads(r.data)
        assert set([data['categories'][0]['category'], data['categories'][1]['category']]) == \
                set([itemWithCategory.category_1, itemWithCategory.category_2])


class TestCategoryListAPI(TestBase):
    def test_get_user_categories_unsubscribed(self, test_client, user):
        self.login(test_client, user.email, user.password)

        r = test_client.get('/api/categories')
        check_valid_header_type(r.headers)
        assert r.status_code == 200

        data = json.loads(r.data)
        assert data['categories'] == []


    def test_get_user_categories_missing_items(self, test_client, userWithFeed, itemWithCategory):
        self.login(test_client, userWithFeed.email, userWithFeed.password)

        r = test_client.get('/api/categories')
        check_valid_header_type(r.headers)
        assert r.status_code == 200

        data = json.loads(r.data)
        assert data['categories'] == []


    def test_get_user_categories_present(self, test_client, userWithPopulatedFeed):
        self.login(test_client, userWithPopulatedFeed.email, userWithPopulatedFeed.password)

        feed = userWithPopulatedFeed.subscribed.first()
        item = feed.items.first()

        r = test_client.get('/api/categories')
        check_valid_header_type(r.headers)
        assert r.status_code == 200

        data = json.loads(r.data)

        assert set([data['categories'][0]['category'], data['categories'][1]['category']]) == \
                set([item.category_1, item.category_2])

        assert data['categories'][0]['count'] == 5


    def test_get_user_categories_with_unsubscribed_item(self, test_client, userWithPopulatedFeed, itemsWithCategory):
        self.login(test_client, userWithPopulatedFeed.email, userWithPopulatedFeed.password)

        feed = userWithPopulatedFeed.subscribed.first()
        item = feed.items.first()

        r = test_client.get('/api/categories')
        check_valid_header_type(r.headers)
        assert r.status_code == 200

        data = json.loads(r.data)

        assert set([data['categories'][0]['category'], data['categories'][1]['category']]) == \
                set([item.category_1, item.category_2])

        assert data['categories'][0]['count'] == feed.items.count() + 1
