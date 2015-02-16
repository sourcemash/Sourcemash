from sourcemash.database import db

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250))
    link = db.Column(db.String(400), index=True)
    last_updated = db.Column(db.DateTime)
    author = db.Column(db.String(120))
    summary = db.Column(db.Text)
    text = db.Column(db.Text)
    feed_id = db.Column(db.Integer, db.ForeignKey('feed.id'))
    category_1 = db.Column(db.String(100))
    category_2 = db.Column(db.String(100))


    def __repr__(self):
        return "<Item %r (%r)>" % (self.title, self.link)