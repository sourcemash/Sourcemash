from sqlalchemy.ext.associationproxy import association_proxy
from sourcemash.database import db


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(250), index=True, unique=True)

    items = association_proxy('categories', 'items')


    def __init__(self, category):
        self.category = category

    def __repr__(self):
        return "<Category %r>" % (self.category)
