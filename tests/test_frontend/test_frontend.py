import pytest


class TestHomePage:

    def test_home_page(self, test_client):
        rv = test_client.get('/')
        assert "Sourcemash" in rv.data

    def test_index_page(self, test_client):
        rv = test_client.get('/index')
        assert "Sourcemash" in rv.data
