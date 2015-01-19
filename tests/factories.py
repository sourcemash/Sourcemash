import factory
from factory.alchemy import SQLAlchemyModelFactory

from app import db
from app.models import User

class UserFactory(SQLAlchemyModelFactory):
	class Meta:
		model = User
		sqlalchemy_session = db.session

	id = factory.Sequence(lambda n: n)
	email = factory.Sequence(lambda n: u'user%d@test.com' % n)