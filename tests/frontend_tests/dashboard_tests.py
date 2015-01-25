from nose.tools import assert_true, assert_false

from app import app

class TestHomePage():

    def setUp(self):
        self.app = app.test_client()

    def test_home_page(self):
        rv = self.app.get('/')
        assert_true("Hello, World!" in rv.data)

    def test_index_page(self):
        rv = self.app.get('/index')
        assert_true("Hello, World!" in rv.data)

    def tearDown(self):
        pass
