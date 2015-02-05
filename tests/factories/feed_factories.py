from tests.factories import *

from sourcemash.models import Feed

class FeedFactory(SQLAlchemyModelFactory):
    FACTORY_FOR = Feed
    FACTORY_SESSION = db.session

    id = factory.Sequence(lambda n: n)
    title = factory.Sequence(lambda n: u'Feed %d' % n)
    url = factory.Sequence(lambda n: u'superfeed%d.com/rss' % n)
    last_updated = datetime.min

class NYTFeedFactory(FeedFactory):
    title = "NYTimes"
    url = "http://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"