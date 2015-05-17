from sourcemash.database import db


class UserCategory(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), primary_key=True)
    unread = db.Column(db.Boolean, default=True)
    user = db.relationship('User')
    category = db.relationship('Category')

    def __repr__(self):
        return "<UserFeed: %s, %s (unread: %d)>" % (self.user, self.category, self.unread)
