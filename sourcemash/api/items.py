from . import api
from sourcemash.database import db
from flask import abort
from flask.ext.restful import Resource, reqparse, fields, marshal

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
    'category_1': fields.String,
    'category_2': fields.String,
    'uri': fields.Url('api.item')
}

class ItemListAPI(Resource):

    def get(self, feed_id):
        return {'items': [marshal(item, item_fields) for item in Item.query.filter_by(feed_id=feed_id).all()]}

class ItemAPI(Resource):

    def get(self, feed_id, id):
        item = Item.query.get(id)
        
        if not item:
            abort(404)

        return {'item': marshal(item, item_fields)}

api.add_resource(ItemListAPI, '/feeds/<int:feed_id>/items', endpoint='items')
api.add_resource(ItemAPI, '/feeds/<int:feed_id>/items/<int:id>', endpoint='item')