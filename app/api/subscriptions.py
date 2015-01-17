from app import app
from flask import abort
from flask.ext.restful import Api, Resource, reqparse, fields, marshal

from datetime import datetime, date

import feedparser

api = Api(app)

subscriptions = [
	{
		'user_id': 1,
		'feed_id': 3,
		'merged': True
	},
	{
		'user_id': 2,
		'feed_id': 4,
		'merged': True
	},
	{
		'user_id': 2,
		'feed_id': 2,
		'merged': True
	}
]

subscription_fields = {
    'merged': fields.Boolean,
    'uri': fields.Url('subscription')
}

class SubscriptionListAPI(Resource):

	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('url', type=str, required=True,
									help='No feed url provided')
		super(FeedListAPI, self).__init__()

	def get(self):
		return {'feeds': [marshal(feed, feed_fields) for feed in feeds]}

	def post(self):
		args = self.reqparse.parse_args()

		rss_feed = feedparser.parse(args['url'])

		feed = {
			'id': feeds[-1]['id'] + 1,
			'title': rss_feed['feed']['title'],
			'url': args['url'],
			'last_updated': datetime.min
		}
		feeds.append(feed)
		return {'feed': marshal(feed, feed_fields)}, 201

class SubscriptionAPI(Resource):

	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('url', type=str, required=True,
									help='No feed url provided')
		super(FeedListAPI, self).__init__()

	def get(self, id):
		try:
			feed = next((feed for feed in feeds if feed['id'] == id))
		except StopIteration:
			abort(404)

		return {'feed': marshal(feed, feed_fields)}

	def delete(self, id):
		try:
			feed = next((feed for feed in feeds if feed['id'] == id))
		except StopIteration:
			abort(404)

		feeds.remove(feed)
		return {'result': True}

api.add_resource(FeedListAPI, '/api/subscriptions', endpoint='subscriptions')
api.add_resource(FeedAPI, '/api/subscriptions/<int:id>', endpoint='subscription')