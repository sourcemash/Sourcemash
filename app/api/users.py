from flask import Flask
from flask.ext.restful import Api, Resource, fields, marshal, reqparse
from app import app

api = Api(app)

user_list = [
	{
		'id': 5743, 
		'first_name': "Scott", 
		'last_name': "Gladstone",
		'screenname': "lhpglad", 
		'email': "happy@rock.com",  
		'location': "New York",
		'description': ""
	},
	{
		'id': 5744, 
		'first_name': "Alex", 
		'last_name': "Gerstein",
		'screenname': "algae", 
		'email': "alex@shnoodles.com",  
		'location': "New York",
		'description': ""
	}
]

user_fields = {
	'first_name': fields.String,
	'last_name': fields.String,
	'screenname': fields.String,
	'email': fields.String,
	'location': fields.String(default = ""),
	'description': fields.String(default = ""),
	# 'links': fields.Nested({
	# 	'feeds': fields.Url('/api/users/{id}/feeds', absolute=True)
	# 	}),
	'uri': fields.Url('user')
}

class UserListAPI(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('first_name', type = str, required = True)
		self.reqparse.add_argument('last_name', type = str, required = True)
		self.reqparse.add_argument('screenname', type = str, required = True)
		self.reqparse.add_argument('email', type = str, required = True)
		self.reqparse.add_argument('location', type = str, required = False)
		self.reqparse.add_argument('description', type = str, default = "", help = 'Something about you')
		super(UserListAPI, self).__init__()

	def get(self):
		''' Show all Users '''
		return { 'users': [marshal(user, user_fields) for user in user_list] }

	def post(self):
		''' Create new User ''' 
		args = self.reqparse.parse_args()
		user = {}
		for key, val in args.iteritems():
			if val != None:
				user[key] = val
		user['id'] = user_list[-1]['id'] + 1
		return { 'user': user}, 201

class UserAPI(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('first_name', type = str)
		self.reqparse.add_argument('last_name', type = str)
		self.reqparse.add_argument('screenname', type = str)
		self.reqparse.add_argument('email', type = str)
		self.reqparse.add_argument('location', type = str)
		self.reqparse.add_argument('description', type = str, help = 'Something about you')
		super(UserAPI, self).__init__()

	def get(self, id):
		''' Show User @id '''
		return { 'user': [marshal(user, user_fields) for user in user_list if user['id']==id] }

	def put(self, id):
		''' Edit User @id '''
		args = self.reqparse.parse_args()
		user = {}
		for key, val in args.iteritems():
			if val != None:
				user[key] = val
		return { 'user': user }

	def delete(self, id):
		''' Destroy User @id '''
		pass

api.add_resource(UserListAPI, '/api/users', endpoint = 'users')
api.add_resource(UserAPI, '/api/users/<int:id>', endpoint = 'user')
