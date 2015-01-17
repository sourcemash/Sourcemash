from app import app
from flask import abort
from flask.ext.restful import Api, Resource, reqparse, fields, marshal

api = Api(app)

logged_in_user_id = 1

subscriptions = [
	{
		'user_id': 1,
		'feed_id': 3,
		'mergeable': True
	},
	{
		'user_id': 2,
		'feed_id': 4,
		'mergeable': True
	},
	{
		'user_id': 2,
		'feed_id': 2,
		'mergeable': True
	}
]

subscription_fields = {
    'mergeable': fields.Boolean,
    'uri': fields.Url('subscription')
}

def get_user_subscriptions():
	return (subscription for subscription in subscriptions if subscription['user_id'] == logged_in_user_id)

class SubscriptionListAPI(Resource):

	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('feed_id', type=int, required=True,
									help='No feed ID provided')
		super(SubscriptionListAPI, self).__init__()

	def get(self):
		return {'subscriptions': [marshal(subscription, subscription_fields) for subscription in get_user_subscriptions()]}

	def post(self):
		args = self.reqparse.parse_args()

		subscription = {
			'user_id': logged_in_user_id,
			'feed_id': args['feed_id'],
			'mergeable': True
		}
		subscriptions.append(subscription)
		return {'subscription': marshal(subscription, subscription_fields)}, 201

class SubscriptionAPI(Resource):

	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('mergeable', type=bool, required=True,
									help='No mergeable provided')
		super(SubscriptionAPI, self).__init__()

	def get(self, feed_id):
		try:
			subscription = next((subscription for subscription in get_user_subscriptions() if subscription['feed_id'] == feed_id))
		except StopIteration:
			abort(404)

		return {'subscription': marshal(subscription, subscription_fields)}

	def put(self, feed_id):
		args = self.reqparse.parse_args()

		try:
			subscription = next((subscription for subscription in get_user_subscriptions() if subscription['feed_id'] == feed_id))
		except StopIteration:
			abort(404)

		subscription['mergeable'] = args.mergeable
		return {'subscription': marshal(subscription, subscription_fields)}

	def delete(self, feed_id):
		try:
			subscription = next((subscription for subscription in get_user_subscriptions() if subscription['feed_id'] == feed_id))
		except StopIteration:
			abort(404)

		subscriptions.remove(subscription)
		return {'result': True}

api.add_resource(SubscriptionListAPI, '/api/subscriptions', endpoint='subscriptions')
api.add_resource(SubscriptionAPI, '/api/subscriptions/<int:feed_id>', endpoint='subscription')