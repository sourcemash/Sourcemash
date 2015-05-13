import pytest


class TestHomePage:

    def test_home_page(self, test_client):
        rv = test_client.get('/')
        assert "Sourcemash" in rv.data

    def test_index_page(self, test_client):
        rv = test_client.get('/index')
        assert "Sourcemash" in rv.data

    def test_register(self, test_client, worker, outbox):
        data = {'email': 'user@sourcemash.com', 'password': 'password'}
        test_client.post('/register', data=data)
        worker.work(burst=True)
        assert len(outbox) == 1
        assert "Welcome to Sourcemash!" in outbox[0].subject
