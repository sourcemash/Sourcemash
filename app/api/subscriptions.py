from app import app, db
from flask import abort
from flask.ext.restful import Api, Resource, reqparse, fields, marshal
from flask.ext.security import current_user, login_required

from app.models import Feed

api = Api(app)

subscription_fields = {
    'mergeable': fields.Boolean,
    'uri': fields.Url('subscription')
}

class SubscriptionListAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('feed_uri', type=str, required=True,
                                    help='No feed ID provided')
        super(SubscriptionListAPI, self).__init__()

    @login_required
    def get(self):
        return {'subscriptions': [marshal(subscription, subscription_fields) for subscription in current_user.subscribed]}

    @login_required
    def post(self):
        args = self.reqparse.parse_args()

        try:
            feed = Feed.query.get(int(args['feed_uri'].split('/')[-1]))
        except ValueError:
            abort(400)

        if not feed:
            abort(400)

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

api.add_resource(SubscriptionListAPI, '/api/subscriptions', endpoint='subscriptions')
api.add_resource(SubscriptionAPI, '/api/subscriptions/<int:id>', endpoint='subscription')