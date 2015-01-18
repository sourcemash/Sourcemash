import factory
from factory.alchemy import SQLAlchemyModelFactory

from app import db
from app.models import User, Feed
from datetime import datetime

class UserFactory(SQLAlchemyModelFactory):
	class Meta:
		model = User
		sqlalchemy_session = db.session

	id = factory.Sequence(lambda n: n)
	email = factory.Sequence(lambda n: u'user%d@test.com' % n)

class FeedFactory(SQLAlchemyModelFactory):
	class Meta:
		model = Feed
		sqlalchemy_session = db.session   # the SQLAlchemy session object

	id = factory.Sequence(lambda n: n)
	title = "TechCrunch"
	url = "http://feeds.feedburner.com/TechCrunch/"
	last_updated = datetime.utcnow()
