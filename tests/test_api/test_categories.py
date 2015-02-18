import pytest
import json

from sourcemash.models import Feed

def check_valid_header_type(headers):
    assert headers['Content-Type'] == 'application/json'

class TestCategoryListAPI:
    def test_get_categories_present(self, test_client, itemWithCategory):
        r = test_client.get('/api/categories')
        check_valid_header_type(r.headers)
        assert r.status_code == 200

        data = json.loads(r.data)
        print data
        assert data['categories'][0]['category'] == itemWithCategory.category_1 or \
                data['categories'][0]['category'] == itemWithCategory.category_2
        assert data['categories'][1]['category'] == itemWithCategory.category_1 or \
                data['categories'][1]['category'] == itemWithCategory.category_2

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
        assert r.status_code == 404

    def test_multiple_items_in_one_category(self, test_client, itemsWithCategory):
        r = test_client.get('/api/categories/' + itemsWithCategory[0].category_1)
        check_valid_header_type(r.headers)
        assert r.status_code == 200

        data = json.loads(r.data)
        assert len(data['items']) == 5