from . import api
from sourcemash.database import db

from flask import abort, request
from flask.ext.restful import Resource, reqparse, fields, marshal
from flask.ext.security import current_user, login_required

from sourcemash.models import Feed
from sourcemash.forms import FeedForm
import feedparser
from datetime import datetime

from feeds import feed_fields

subscription_fields = {
    'id': fields.Integer,
    'feed': fields.Nested(feed_fields)
}

class SubscriptionListAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('url', type=str, required=True,
                                    help='No url provided')
        super(SubscriptionListAPI, self).__init__()

    @login_required
    def get(self):
        subscriptions = []
        for subscription in current_user.subscribed:
            subscription.feed = Feed.query.get(subscription.id)
            subscriptions.append(subscription)

        return {'subscriptions': [marshal(subscription, subscription_fields) for subscription in subscriptions]}

    @login_required
    def post(self):
        args = self.reqparse.parse_args()
        form = FeedForm(obj=args)

        if not form.validate_on_submit():
            return form.errors, 422

        rss_feed = feedparser.parse(form.url.data)

        try:
            feed = Feed.query.filter(Feed.url==rss_feed['url']).one()
        except:

            feed = Feed(title=rss_feed['feed']['title'],
                        url=rss_feed['url'],
                        last_updated=datetime.min)

            db.session.add(feed)
            db.session.commit()

        try:
            subscription = current_user.subscribed.filter(Feed.id==feed.id).one()
            return {"url": "Already subscribed"}, 409
        except:
            current_user.subscribed.append(feed)
            db.session.commit()

        subscription = current_user.subscribed.filter(Feed.id==feed.id).first()
        subscription.feed = feed
        return marshal(subscription, subscription_fields), 201

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

        subscription.feed = Feed.query.get(id)

        return {"subscription": marshal(subscription, subscription_fields)}

    @login_required
    def put(self, id):
        args = self.reqparse.parse_args()

        subscription = current_user.subscribed.filter(Feed.id==id).first()
        
        if not subscription:
            abort(404)

        subscription.feed = Feed.query.get(id)

        if args.mergeable:
            subscription['mergeable'] = args.mergeable

        db.session.commit()

        return {"subscription": marshal(subscription, subscription_fields)}

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