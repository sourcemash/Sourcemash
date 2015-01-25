from app import db

class Feed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250))
    url = db.Column(db.String(120), index=True, unique=True)
    last_updated = db.Column(db.DateTime)

    items = db.relationship('Item', backref='feed', lazy='dynamic')

    def __repr__(self):
        return "<Feed %r (%r)>" % (self.title, self.url)