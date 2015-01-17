from nose.tools import assert_true, assert_false, eq_

from app import app

def check_valid_header_type(headers):
	eq_(headers['Content-Type'], 'application/json')

# Here's our "unit tests".
class TestUsers():

	def setUp(self):
		self.app = app.test_client()

	def tearDown(self):
		pass

	def test_get(self):
		rv = self.app.get('/api/users')
		eq_(len(rv.data),125) # size of sample input text

	def test_post(self):
		d = dict(email="happy@rock.com")
		rv = self.app.post('/api/users', data=d)
		eq_(rv.headers['Content-Type'], 'application/json')
		eq_(rv.status_code,201)
