from sourcemash.database import db
from flask.ext.security import UserMixin, RoleMixin

subscriptions = db.Table('subscriptions',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('feed_id', db.Integer, db.ForeignKey('feed.id'))
)

role_users = db.Table('roles_users',
        db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer, db.ForeignKey('role.id')))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean)
    confirmed_at = db.Column(db.DateTime)
    subscribed = db.relationship('Feed',
                                secondary=subscriptions,
                                backref=db.backref('subscribers', lazy='dynamic'),
                                lazy='dynamic')
    roles = db.relationship('Role',
                            secondary=role_users,
                            backref=db.backref('users', lazy='dynamic'),
                            lazy='dynamic')
    
    def __repr__(self):
        return "<User %r (%d)>" % (self.email, self.id)

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

    def __repr__(self):
        return "<Role %r (%d)>" % (self.name, self.id)