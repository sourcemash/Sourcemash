from tests.factories import *

from sourcemash.models import Item
from feed_factories import FeedFactory

class ItemFactory(SQLAlchemyModelFactory):
    FACTORY_FOR = Item
    FACTORY_SESSION = db.session

    id = factory.Sequence(lambda n: n)
    title = factory.Sequence(lambda n: u'Item %d' % n)
    link = factory.Sequence(lambda n: u"ImportantItem.com/%d" % n)
    last_updated = datetime.utcnow()
    author = 'Scott Gladstone'
    summary = 'Summary of the feed item.'
    text = 'Text of the feed item.'
    feed = factory.SubFactory(FeedFactory)