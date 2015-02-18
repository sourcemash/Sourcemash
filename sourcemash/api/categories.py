from . import api
from flask import abort
from flask.ext.restful import Resource, fields, marshal

from sourcemash.models import Item
from items import item_fields

from sqlalchemy import func
from collections import Counter

category_fields = {
    'category': fields.String,
    'count': fields.String
}

class CategoryListAPI(Resource):

    def get(self):
        categories = Counter(dict(Item.query.with_entities(Item.category_1, func.count()).group_by(Item.category_1).all()))
        categories.update(dict(Item.query.with_entities(Item.category_2, func.count()).group_by(Item.category_2).all()))

        return {'categories': [{'category': category, 'count': categories[category]} for category in categories]}

class CategoryItemListAPI(Resource):

    def get(self, category):
        """ RETURNS EMPTY LIST IF NO ARTICLES PRESENT """ 
        cat1_items = Item.query.filter_by(category_1=category).all()
        cat2_items = Item.query.filter_by(category_2=category).all()
        items = set(cat1_items + cat2_items)

        return {'items': [marshal(item, item_fields) for item in items]}

api.add_resource(CategoryListAPI, '/categories', endpoint='categories')
api.add_resource(CategoryItemListAPI, '/categories/<string:category>', endpoint='category')