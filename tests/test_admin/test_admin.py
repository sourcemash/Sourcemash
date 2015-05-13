import pytest

class TestAdmin:

    def test_home_page(self, test_client):
        rv = test_client.get('/admin/feedview', follow_redirects=True)
        assert rv.status_code == 200
        assert "side-nav" in rv.data
