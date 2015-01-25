from app import db

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250))
    link = db.Column(db.String(120), index=True, unique=True)
    last_updated = db.Column(db.DateTime)
    author = db.Column(db.String(120))
    summary = db.Column(db.String(500))
    feed_id = db.Column(db.Integer, db.ForeignKey('feed.id'))

    def __repr__(self):
        return "<Item %r (%r)>" % (self.title, self.url)