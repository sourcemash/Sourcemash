from app import app, db
from flask import abort
from flask.ext.restful import Api, Resource, reqparse, fields, marshal

from app.models import Item

api = Api(app)

item_fields = {
    'title': fields.String,
    'url': fields.String,
    'publication_date': fields.DateTime,
    'author': fields.String,
    'category': fields.String,
    'description': fields.String,
    'uri': fields.Url('item')
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

api.add_resource(ItemListAPI, '/api/feeds/<int:feed_id>/items', endpoint='items')
api.add_resource(ItemAPI, '/api/feeds/<int:feed_id>/items/<int:id>', endpoint='item')