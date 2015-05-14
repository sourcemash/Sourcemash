from tests.factories import *

from sourcemash.models import Category

class CategoryFactory(SQLAlchemyModelFactory):
    FACTORY_FOR = Category
    FACTORY_SESSION = db.session

    id = factory.Sequence(lambda n: n)
    category = factory.Sequence(lambda n: u'category%d' % n)
