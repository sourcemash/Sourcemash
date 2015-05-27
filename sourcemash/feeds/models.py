from sourcemash.database import db


class Feed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250))
    url = db.Column(db.String(2083), index=True, unique=True)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(2083))
    last_updated = db.Column(db.DateTime)
    topic = db.Column(db.String(50))
    public = db.Column(db.Boolean, default=False)
    item_count = db.Column(db.Integer, default=0)

    items = db.relationship('Item', backref='feed', lazy='dynamic')

    def __repr__(self):
        return "<Feed %r (%r)>" % (self.title, self.url)
