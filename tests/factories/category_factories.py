from tests.factories import *

from sourcemash.models import Category

class CategoryFactory(SQLAlchemyModelFactory):
    FACTORY_FOR = Category
    FACTORY_SESSION = db.session

    category = factory.Sequence(lambda n: u'Category %d' % n)
