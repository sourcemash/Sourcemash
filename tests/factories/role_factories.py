from tests.factories import *

from sourcemash.models import Role

class RoleFactory(SQLAlchemyModelFactory):
    FACTORY_FOR = Role
    FACTORY_SESSION = db.session

    id = factory.Sequence(lambda n: n)
    name = 'user'