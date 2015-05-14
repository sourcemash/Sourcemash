import pytest
import json

from . import TestBase

from sourcemash.models import Feed

def check_valid_header_type(headers):
    assert headers['Content-Type'] == 'application/json'


class TestCategory(TestBase):
    def test_get_category_present(self, test_client, itemWithCategory):
        category = itemWithCategory.cats.first()
        r = test_client.get('/api/categories/%d' % (category.id))
        check_valid_header_type(r.headers)
        assert r.status_code == 200

        data = json.loads(r.data)
        assert data['category']['name'] == category.category

    def test_put_new_category_mark_read(self, test_client, user, itemWithCategory):
        category = itemWithCategory.cats.first()
        self.login(test_client, user.email, user.password)

        mark_read = dict(unread=False)
        r = test_client.put('/api/categories/%d' % category.id, data=mark_read)
        check_valid_header_type(r.headers)
        assert r.status_code == 200

        data = json.loads(r.data)
        assert data['category']['unread'] == False

    def test_put_existing_category_mark_read(self, test_client, user_category):
        self.login(test_client, user_category.user.email, user_category.user.password)

        mark_read = dict(unread=False)
        r = test_client.put('/api/categories/%d' % user_category.category.id, data=mark_read)
        check_valid_header_type(r.headers)
        assert r.status_code == 200

        data = json.loads(r.data)
        assert data['category']['unread'] == False


class TestCategoryListAllAPI:
    def test_get_categories_present(self, test_client, itemWithCategory):
        r = test_client.get('/api/categories/all')
        check_valid_header_type(r.headers)
        assert r.status_code == 200

        data = json.loads(r.data)
        assert set([data['categories'][0]['name'], data['categories'][1]['name']]) == set(itemWithCategory.categories)


class TestCategoryListAPI(TestBase):
    def test_get_user_categories_unsubscribed(self, test_client, user):
        self.login(test_client, user.email, user.password)

        r = test_client.get('/api/categories')
        check_valid_header_type(r.headers)
        assert r.status_code == 200

        data = json.loads(r.data)
        assert data['categories'] == []

    def test_get_user_categories_unauthenticated(self, test_client):
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

        assert set([data['categories'][0]['name'], data['categories'][1]['name']]) == \
                set(item.categories)

        assert data['categories'][0]['item_count'] == 5


    def test_get_user_categories_with_unsubscribed_item(self, test_client, userWithPopulatedFeed, itemsWithCategory):
        self.login(test_client, userWithPopulatedFeed.email, userWithPopulatedFeed.password)

        feed = userWithPopulatedFeed.subscribed.first()
        item = feed.items.first()

        r = test_client.get('/api/categories')
        check_valid_header_type(r.headers)
        assert r.status_code == 200

        data = json.loads(r.data)

        assert data['categories'][0]['item_count'] == feed.items.count() + 1
