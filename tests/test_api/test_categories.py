import pytest
import json

from . import TestBase

from sourcemash.models import Feed

def check_valid_header_type(headers):
    assert headers['Content-Type'] == 'application/json'

class TestCategoryListAPI:
    def test_get_categories_present(self, test_client, itemWithCategory):
        r = test_client.get('/api/categories')
        check_valid_header_type(r.headers)
        assert r.status_code == 200

        data = json.loads(r.data)
        assert set([data['categories'][0]['category'], data['categories'][1]['category']]) == \
                set([itemWithCategory.category_1, itemWithCategory.category_2])


class TestUserCategoryListAPI(TestBase):
    def test_get_user_categories_unsubscribed(self, test_client, user):
        self.login(test_client, user.email, user.password)

        r = test_client.get('/api/users/%d/categories' % user.id)
        check_valid_header_type(r.headers)
        assert r.status_code == 200

        data = json.loads(r.data)
        assert data['categories'] == []


    def test_get_user_categories_not_current_user(self, test_client, user, userWithPopulatedFeed):
        self.login(test_client, user.email, user.password)

        r = test_client.get('/api/users/%d/categories' % userWithPopulatedFeed.id)
        assert r.status_code == 401


    def test_get_user_categories_missing_items(self, test_client, userWithFeed, itemWithCategory):
        self.login(test_client, userWithFeed.email, userWithFeed.password)

        r = test_client.get('/api/users/%d/categories' % userWithFeed.id)
        check_valid_header_type(r.headers)
        assert r.status_code == 200

        data = json.loads(r.data)
        assert data['categories'] == []


    def test_get_user_categories_present(self, test_client, userWithPopulatedFeed):
        self.login(test_client, userWithPopulatedFeed.email, userWithPopulatedFeed.password)

        feed = userWithPopulatedFeed.subscribed.first()
        item = feed.items.first()

        r = test_client.get('/api/users/%d/categories' % userWithPopulatedFeed.id)
        check_valid_header_type(r.headers)
        assert r.status_code == 200

        data = json.loads(r.data)

        assert set([data['categories'][0]['category'], data['categories'][1]['category']]) == \
                set([item.category_1, item.category_2])

        assert data['categories'][0]['count'] == 5


class TestCategoryItemListAPI:

    def test_get_category_items_present(self, test_client, itemWithCategory):
        r = test_client.get('/api/categories/' + itemWithCategory.category_1)
        check_valid_header_type(r.headers)
        assert r.status_code == 200

        data = json.loads(r.data)
        assert len(data['items']) == 1

    def test_get_category_items_missing_category(self, test_client):
        r = test_client.get('/api/categories/nonexistent_category')
        check_valid_header_type(r.headers)
        assert r.status_code == 200

        data = json.loads(r.data)
        assert len(data['items']) == 0

    def test_multiple_items_in_one_category(self, test_client, itemsWithCategory):
        r = test_client.get('/api/categories/' + itemsWithCategory[0].category_1)
        check_valid_header_type(r.headers)
        assert r.status_code == 200

        data = json.loads(r.data)
        assert len(data['items']) == 5