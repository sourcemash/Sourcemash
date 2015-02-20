from . import api
from sourcemash.database import db
from flask import abort
from flask.ext.restful import Resource, reqparse, fields, marshal
from flask.ext.security import current_user, login_required

from feeds import feed_fields
from sourcemash.models import Item

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
    'feed': fields.Nested(feed_fields),
    'uri': fields.Url('api.item')
}


class ItemAPI(Resource):

    def get(self, id):
        item = Item.query.get_or_404(id)
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

