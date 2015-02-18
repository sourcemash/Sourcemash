from . import api
from flask import abort
from flask.ext.restful import Resource, fields, marshal

from sourcemash.models import Item
from items import item_fields

category_fields = {
    'category': fields.String
}

class CategoryListAPI(Resource):

    def get(self):
        categories = [item.category_1 for item in Item.query.group_by(Item.category_1).all()]
        categories += [item.category_2 for item in Item.query.group_by(Item.category_2).all()]
        categories = set(categories)

        return {'categories': [{'category': category} for category in categories]}

class CategoryItemListAPI(Resource):

    def get(self, category):
        """ RETURNS EMPTY LIST IF NO ARTICLES PRESENT """ 
        cat1_items = Item.query.filter_by(category_1=category).all()
        cat2_items = Item.query.filter_by(category_2=category).all()
        items = set(cat1_items + cat2_items)

        if not items:
            abort(404)

        return {'items': [marshal(item, item_fields) for item in items]}

api.add_resource(CategoryListAPI, '/categories', endpoint='categories')
api.add_resource(CategoryItemListAPI, '/categories/<string:category>', endpoint='category')