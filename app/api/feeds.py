from app import app, db
from flask import abort
from flask.ext.restful import Api, Resource, reqparse, fields, marshal

from datetime import datetime, date

import feedparser

from app.models import Feed

api = Api(app)

feed_fields = {
    'title': fields.String,
    'url': fields.String,
    'last_updated': fields.DateTime,
    'uri': fields.Url('feed')
}

class FeedListAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('url', type=str, required=True,
                                    help='No feed url provided')
        super(FeedListAPI, self).__init__()

    def get(self):
        return {'feeds': [marshal(feed, feed_fields) for feed in Feed.query.all()]}

    def post(self):
        args = self.reqparse.parse_args()

        rss_feed = feedparser.parse(args['url'])

        feed = Feed(title=rss_feed['feed']['title'],
                    url=args['url'],
                    last_updated=datetime.min)
        
        db.session.add(feed)
        db.session.commit()

        return {'feed': marshal(feed, feed_fields)}, 201

class FeedAPI(Resource):

    def get(self, id):
        feed = Feed.query.get(id)
        
        if not feed:
            abort(404)

        return {'feed': marshal(feed, feed_fields)}

    def delete(self, id):
        feed = Feed.query.get(id)
        
        if not feed:
            abort(404)

        db.session.delete(feed)
        db.session.commit()

        return {'result': True}

api.add_resource(FeedListAPI, '/api/feeds', endpoint='feeds')
api.add_resource(FeedAPI, '/api/feeds/<int:id>', endpoint='feed')