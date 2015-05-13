from sourcemash.database import db


class UserFeed(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    feed_id = db.Column(db.Integer, db.ForeignKey('feed.id'), primary_key=True)
    unread = db.Column(db.Boolean, default=True)
    user = db.relationship('User')
    feed = db.relationship('Feed')

    def __repr__(self):
        return "<UserFeed: %s, %s (unread: %d)>" % (self.user, self.feed, self.unread)
