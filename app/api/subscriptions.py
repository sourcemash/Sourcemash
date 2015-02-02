from . import api
from app.database import db

from flask import abort
from flask.ext.restful import Resource, reqparse, fields, marshal
from flask.ext.security import current_user, login_required

from app.models import Feed
import feedparser
from datetime import datetime

subscription_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'url': fields.String,
    'uri': fields.Url('api.subscription')
}

class SubscriptionListAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('feed_url', type=str, required=True,
                                    help='No feed url provided')
        super(SubscriptionListAPI, self).__init__()

    @login_required
    def get(self):
        return {'subscriptions': [marshal(subscription, subscription_fields) for subscription in current_user.subscribed]}

    @login_required
    def post(self):
        args = self.reqparse.parse_args()

        try:
            feed = Feed.query.filter(Feed.url==args.feed_url).one()
        except:
            rss_feed = feedparser.parse(args.feed_url)
            
            if rss_feed['bozo']: # invalid feed
                abort(400)

            feed = Feed(title=rss_feed['feed']['title'],
                        url=rss_feed['url'],
                        last_updated=datetime.min)

            db.session.add(feed)
            db.session.commit()

        current_user.subscribed.append(feed)
        db.session.commit()

        subscription = current_user.subscribed.filter(Feed.id==feed.id).first()
        return {'subscription': marshal(subscription, subscription_fields)}, 201

class SubscriptionAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('mergeable', type=bool)
        super(SubscriptionAPI, self).__init__()

    @login_required
    def get(self, id):
        subscription = current_user.subscribed.filter(Feed.id==id).first()
        
        if not subscription:
            abort(404)

        return {'subscription': marshal(subscription, subscription_fields)}

    @login_required
    def put(self, id):
        args = self.reqparse.parse_args()

        subscription = current_user.subscribed.filter(Feed.id==id).first()
        
        if not subscription:
            abort(404)

        if args.mergeable:
            subscription['mergeable'] = args.mergeable

        db.session.commit()

        return {'subscription': marshal(subscription, subscription_fields)}

    @login_required
    def delete(self, id):
        subscription = current_user.subscribed.filter(Feed.id==id).first()
        
        if not subscription:
            abort(404)

        current_user.subscribed.remove(subscription)
        db.session.commit()

        return {'result': True}

api.add_resource(SubscriptionListAPI, '/subscriptions', endpoint='subscriptions')
api.add_resource(SubscriptionAPI, '/subscriptions/<int:id>', endpoint='subscription')