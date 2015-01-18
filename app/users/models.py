from app import db

subscriptions = db.Table('subscriptions',
	db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
	db.Column('feed_id', db.Integer, db.ForeignKey('feed.id')),
	db.Column('mergeable', db.Boolean)
)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(120), index=True, unique=True)
	subscribed = db.relationship('Feed',
								secondary=subscriptions,
								backref=db.backref('subscribers', lazy='dynamic'),
								lazy='dynamic')

	def __repr__(self):
		return "<User %r (%d)>" % (self.email, self.id)