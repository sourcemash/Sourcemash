from sqlalchemy.ext.associationproxy import association_proxy
from sourcemash.database import db
from sourcemash.models import Category

categories = db.Table('categories',
                      db.Column('item_id', db.Integer,
                                db.ForeignKey('item.id')),
                      db.Column('category_id', db.Integer,
                                db.ForeignKey('category.id')))

def _find_or_create_category(cat):
    category = Category.query.filter_by(category=cat).first()
    if not category:
        category = Category(category=cat)
    return category


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250))
    link = db.Column(db.String(400), index=True)
    last_updated = db.Column(db.DateTime)
    author = db.Column(db.String(120))
    summary = db.Column(db.Text)
    image_url = db.Column(db.String(400))
    text = db.Column(db.Text)
    feed_id = db.Column(db.Integer, db.ForeignKey('feed.id'))
    voteSum = db.Column(db.Integer, default=0)
    cats = db.relationship('Category',
                                 secondary=categories,
                                 backref=db.backref('items', lazy='dynamic'),
                                 lazy='dynamic')
    categorized = db.Column(db.Boolean, default=False)

    categories = association_proxy('cats', 'category', creator=_find_or_create_category)

    def __repr__(self):
        return "<Item %r (%r)>" % (self.title, self.link)
