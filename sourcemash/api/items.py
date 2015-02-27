from . import api
from sourcemash.database import db
from flask import abort
from flask.ext.restful import Resource, reqparse, inputs, fields, marshal
from flask.ext.security import current_user, login_required

from feeds import feed_fields
from sourcemash.models import Item, UserItem
from sourcemash.forms import VoteForm

class getVote(fields.Raw):
    def output(self, key, item):
        try:
            vote = UserItem.query.filter_by(user=current_user, item=item).one().vote
        except:
            vote = 0

        return vote

class getUnreadStatus(fields.Raw):
    def output(self, key, item):
        try:
            unread = UserItem.query.filter_by(user=current_user, item=item).one().unread
        except:
            unread = True

        return unread

item_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'text': fields.String,
    'link': fields.String,
    'last_updated': fields.DateTime,
    'author': fields.String,
    'category_1': fields.String,
    'category_2': fields.String,
    'summary': fields.String,
    'image_url': fields.String,
    'feed': fields.Nested(feed_fields),
    'unread': getUnreadStatus,
    'vote': getVote,
    'voteSum': fields.Integer,
    'uri': fields.Url('api.item')
}


class ItemAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('vote', type = int, default=0)
        self.reqparse.add_argument('unread', type = inputs.boolean)
        super(ItemAPI, self).__init__()

    def get(self, id):
        item = Item.query.get_or_404(id)
        return {'item': marshal(item, item_fields)}

    @login_required
    def put(self, id):
        ''' Update item vote count (& mark as read/unread)'''
        args = self.reqparse.parse_args()
        form = VoteForm(obj=args)

        if not form.validate():
            return {"errors": form.errors}, 422

        item = Item.query.get_or_404(id)
        
        # Reject if user has already voted
        # Check vote column of user_items table
        try:
            user_item = UserItem.query.filter_by(user=current_user, item=item).one()
        except:
            user_item = UserItem(user=current_user, item=item, feed_id=item.feed_id, 
                                 category_1=item.category_1, category_2=item.category_2)
            db.session.add(user_item)
            db.session.commit()

        # Cast vote (if vote isn't zero or revote)
        if args.vote != 0:
            if user_item.vote == args.vote:
                return {'errors': {'vote': ["You have already voted on this item."]}}, 422

            item.voteSum += args.vote - user_item.vote # + new vote - old vote
            user_item.vote = args.vote
            db.session.commit()
        
        # Mark unread as Read / read as Unread
        if args.unread != None:
            user_item.unread = args.unread
            db.session.commit()

        return {'item': marshal(item, item_fields)}

class FeedItemListAPI(Resource):

    def get(self, feed_id):
        return {'items': [marshal(item, item_fields) for item in Item.query.filter_by(feed_id=feed_id).all()]}


class CategoryItemListAPI(Resource):

    @login_required
    def get(self, category):
        category = category.title()
        user_feed_ids = [feed.id for feed in current_user.subscribed]

        items = Item.query.filter((Item.category_1 == category) | (Item.category_2 == category))    \
                            .filter(Item.feed_id.in_(user_feed_ids))                                \
                            .all()

        unsubscribed_item = Item.query.filter((Item.category_1 == category) | (Item.category_2 == category))     \
                                        .filter(~Item.feed_id.in_(user_feed_ids))                               \
                                        .first()

        if unsubscribed_item:
            items.append(unsubscribed_item)

        return {'items': [marshal(item, item_fields) for item in items]}


class CategoryItemListAllAPI(Resource):

    def get(self, category):
        category = category.title()
        items = Item.query.filter((Item.category_1 == category) | (Item.category_2 == category)).all()
        return {'items': [marshal(item, item_fields) for item in items]}


api.add_resource(ItemAPI, '/items/<int:id>', endpoint='item')
api.add_resource(FeedItemListAPI, '/feeds/<int:feed_id>/items', endpoint='feed_items')
api.add_resource(CategoryItemListAPI, '/categories/<string:category>/items', endpoint='category_items')
api.add_resource(CategoryItemListAllAPI, '/categories/<string:category>/items/all', endpoint='category_items_all')
