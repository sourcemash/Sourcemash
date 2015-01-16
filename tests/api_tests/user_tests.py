from nose.tools import assert_true, assert_false, eq_

from app import app

# Here's our "unit tests".
class TestUsers():

	def setUp(self):
		self.app = app.test_client()

	def tearDown(self):
		pass

	def test_get(self):
		rv = self.app.get('/api/users')
		eq_(len(rv.data),355) # size of sample input text

	def test_post(self):
		d = dict(first_name="Scott", 
			last_name="Gladstone",
			screenname="lhpglad", 
			email="happy@rock.com",  
			location="New York",
			description="")
		rv = self.app.post('/api/users', data=d)
		eq_(rv.headers['Content-Type'], 'application/json')
		eq_(rv.status_code,201)
