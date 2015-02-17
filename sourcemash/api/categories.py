from . import api
from flask.ext.restful import Resource, fields, marshal

from sourcemash.models import Item
from items import item_fields

category_fields = {
    'category': fields.String
}

# category_item_fields = {
#     'category': fields.String,
#     'item': fields.Nested(item_fields)
# }

class CategoryListAPI(Resource):

    def get(self):
        cat1_items = Item.query.group_by(Item.category_1).all()
        cat2_items = Item.query.group_by(Item.category_2).all()

        categories = {'categories': []}
        for item in cat1_items:
            category = {'category': item.category_1}
            categories['categories'].append(marshal(category, category_fields))
        for item in cat2_items:
            category = {'category': item.category_2}
            categories['categories'].append(marshal(category, category_fields))

        return categories

class CategoryItemListAPI(Resource):

    def get(self, category):
        cat1_items = Item.query.filter_by(category_1=category).all()
        cat2_items = Item.query.filter_by(category_2=category).all()
        items = list(set(cat1_items + cat2_items))

        # category_items = []
        # for item in items:
        #     cat_item = {'category': item.category_1, 'item': item}
        #     category_items.append(cat_item)

        return {'items': [marshal(item, item_fields) for item in items]}
        # return {'items': [marshal(item, category_item_fields) for item in category_items]}

api.add_resource(CategoryListAPI, '/categories', endpoint='categories')
api.add_resource(CategoryItemListAPI, '/categories/<string:category>', endpoint='category')