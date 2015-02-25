from sourcemash.database import db


class UserItem(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), primary_key=True)
    vote = db.Column(db.Integer, default=0)
    unread = db.Column(db.Boolean, default=True)
    user = db.relationship('User')
    item = db.relationship('Item')

    def __repr__(self):
        return "<UserItem: %s, %s (vote: %d)>" % (self.user, self.item, self.vote)